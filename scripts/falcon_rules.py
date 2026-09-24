import os
import re
import subprocess
import sys

SOURCE_EXTENSIONS = (".c", ".cc", ".cpp", ".h", ".hpp", ".inl")
COMMIT_TYPES = "feat|fix|perf|refactor|docs|chore|ci|build|test|style|revert"
COMMIT_TITLE = re.compile(r"^(" + COMMIT_TYPES + r")(\([a-z0-9._-]+\))?!?: [a-z0-9]")
DEBUG_OUTPUT = re.compile(r"\bLOG_DEBUG\s*\(|std::cerr\b|\bprintf\s*\(")
ONE_LINE_BODY = re.compile(r"\)\s*(const\s*)?(noexcept\s*)?(override\s*)?(final\s*)?\{\s*[^{}\s][^{}]*;\s*\}\s*;?\s*$")
ORDERED_FILE = "src/Protocol/MinecraftPackets.cpp"
ORDERED_PATTERNS = (
    re.compile(r'^#include "Protocol/Packets/(\w+)\.h"'),
    re.compile(r"^\s*registerPacket<(\w+)>\(\);"),
)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", check=True).stdout


def resolve_base(base, head):
    if base and not re.fullmatch(r"0+", base):
        return base
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    return parents[1] if len(parents) > 1 else git("hash-object", "-t", "tree", "/dev/null").strip()


def added_lines(base, head):
    diff = git("diff", "--unified=0", "--no-color", "--diff-filter=AM", f"{base}...{head}")
    result = {}
    current = None
    line_number = 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            path = raw[4:]
            current = path[2:] if path.startswith("b/") else None
            if current is not None:
                result.setdefault(current, [])
            continue
        if raw.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw)
            line_number = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            result[current].append((line_number, raw[1:]))
            line_number += 1
    return result


def added_files(base, head):
    return [path for path in git("diff", "--name-only", "--diff-filter=A", f"{base}...{head}").splitlines() if path]


def check_sources(lines_by_file, errors, warnings):
    for path, lines in lines_by_file.items():
        if not path.endswith(SOURCE_EXTENSIONS):
            continue
        for number, text in lines:
            if DEBUG_OUTPUT.search(text):
                errors.append(("Debug output left in the code", path, number, text.strip()))
            if ONE_LINE_BODY.search(text) and "[" not in text.split("(")[0]:
                warnings.append(("Function body on one line", path, number, text.strip()))


def check_ordering(lines_by_file, head, errors):
    added = lines_by_file.get(ORDERED_FILE)
    if not added:
        return
    content = git("show", f"{head}:{ORDERED_FILE}").splitlines()
    for pattern in ORDERED_PATTERNS:
        entries = []
        for number, text in enumerate(content, start=1):
            match = pattern.match(text)
            if match:
                entries.append((number, match.group(1)))
        positions = {number: position for position, (number, _) in enumerate(entries)}
        for number, text in added:
            if number not in positions:
                continue
            position = positions[number]
            name = entries[position][1]
            before = entries[position - 1][1] if position > 0 else None
            after = entries[position + 1][1] if position + 1 < len(entries) else None
            if (before is not None and before > name) or (after is not None and name > after):
                errors.append(("Not in alphabetical order", ORDERED_FILE, number, text.strip()))


def check_directories(files, errors):
    for path in files:
        if not path.endswith(SOURCE_EXTENSIONS):
            continue
        parts = path.split("/")
        for anchor in ("src", "include"):
            if anchor not in parts:
                continue
            for folder in parts[parts.index(anchor) + 1:-1]:
                if folder and not folder[0].isupper():
                    errors.append(("Folder is not PascalCase", path, 0, folder))
                    break
            break


def check_commits(base, head, errors):
    log = git("log", "--no-merges", "--format=%H%x1f%s%x1f%b%x1e", f"{base}..{head}")
    for record in log.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        sha, title, body = (record.split("\x1f") + ["", ""])[:3]
        short = sha[:7]
        if not COMMIT_TITLE.match(title):
            errors.append(("Commit title is not `type: lowercase description`", short, 0, title))
        if body.strip():
            errors.append(("Commit has a body, only a title is allowed", short, 0, title))


def cell(text):
    return text[:120].replace("|", "\\|").replace("`", "'")


def render(errors, warnings):
    lines = ["<!-- falcon-rules -->", "## Falcon rules", ""]
    if not errors and not warnings:
        lines.append("All rules pass.")
        return "\n".join(lines) + "\n"
    if errors:
        lines.append(f"**{len(errors)} problem(s) must be fixed**")
        lines.append("")
        lines.append("| Rule | Where | Line |")
        lines.append("|---|---|---|")
        for rule, where, number, text in errors:
            location = f"`{where}:{number}`" if number else f"`{where}`"
            lines.append(f"| {rule} | {location} | `{cell(text)}` |")
        lines.append("")
    if warnings:
        lines.append(f"{len(warnings)} warning(s)")
        lines.append("")
        lines.append("| Rule | Where | Line |")
        lines.append("|---|---|---|")
        for rule, where, number, text in warnings:
            lines.append(f"| {rule} | `{where}:{number}` | `{cell(text)}` |")
    return "\n".join(lines) + "\n"


def main():
    head = os.environ.get("RULES_HEAD") or git("rev-parse", "HEAD").strip()
    base = resolve_base(os.environ.get("RULES_BASE", ""), head)

    errors = []
    warnings = []
    lines_by_file = added_lines(base, head)
    check_sources(lines_by_file, errors, warnings)
    check_ordering(lines_by_file, head, errors)
    check_directories(added_files(base, head), errors)
    check_commits(base, head, errors)

    report = render(errors, warnings)
    with open(os.environ.get("RULES_REPORT", "rules-report.md"), "w", encoding="utf-8") as output:
        output.write(report)
    print(report)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as output:
            output.write(f"failed={'true' if errors else 'false'}\n")
            output.write(f"clean={'true' if not errors and not warnings else 'false'}\n")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
