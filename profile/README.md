<p align="center">
	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="logo-white.png">
		<img src="logo.png" alt="Falcon" width="256">
	</picture>
	<br>
	<b>Minecraft: Bedrock Edition server software written from scratch in C++</b>
	<br>
	Not affiliated with Mojang AB.
</p>

<p align="center">
	<img src="https://img.shields.io/badge/minecraft-v1.26.50%20(Bedrock)-56383E" alt="Minecraft">
	<img src="https://img.shields.io/badge/protocol-2193-blue" alt="Protocol">
	<img src="https://img.shields.io/badge/language-C%2B%2B17-00599C" alt="C++17">
	<img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey" alt="Platform">
</p>

Falcon is a Minecraft: Bedrock Edition server built from the ground up in C++17. The protocol, world
storage, inventory, movement and gameplay systems are all reimplemented by hand, with no runtime to
install: the server ships as a single self-contained executable.

## Repositories

| Repository | Description |
|---|---|
| [Falcon](https://github.com/Falcon-MC/Falcon) | The server: world, gameplay, commands, generation and scripting |
| [Protocol](https://github.com/Falcon-MC/Protocol) | Bedrock packets, network types, NBT and binary streams |
| [Network](https://github.com/Falcon-MC/Network) | Transport layer: RakNet, NetherNet (WebRTC), compression and login verification |

## Getting started

Download the latest build from the [releases](https://github.com/Falcon-MC/Falcon/releases), or build
it yourself by following the instructions in the [Falcon README](https://github.com/Falcon-MC/Falcon#building).
