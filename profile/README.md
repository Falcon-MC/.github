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
	<a href="https://falcon-mc.github.io"><img src="https://img.shields.io/badge/website-falcon--mc.github.io-2ea44f" alt="Website"></a>
	<img src="https://img.shields.io/badge/minecraft-v1.26.50%20(Bedrock)-56383E" alt="Minecraft">
	<img src="https://img.shields.io/badge/protocol-2193-blue" alt="Protocol">
	<img src="https://img.shields.io/badge/language-C%2B%2B17-00599C" alt="C++17">
	<img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey" alt="Platform">
	<img src="https://img.shields.io/badge/license-LGPL--3.0-orange" alt="LGPL-3.0">
</p>

Falcon is a Minecraft: Bedrock Edition server built from the ground up in C++17. The protocol, world
storage, inventory, movement and gameplay systems are all reimplemented by hand, with no runtime to
install: the server ships as a single self-contained executable.

Learn more on the website: **[falcon-mc.github.io](https://falcon-mc.github.io)**.

## Highlights

- Overworld, Nether and End, each with its own world storage, entities and block systems
- Own RakNet implementation and a NetherNet (WebRTC) transport
- Vanilla-like world generation with 3D biomes, aquifers, caves and ore veins
- Redstone, pistons, fire, TNT, portals and the vanilla game rules
- Behavior pack support with custom items, blocks and actors, and a QuickJS scripting API

## Repositories

| Repository | Description | Build |
|---|---|---|
| [Falcon](https://github.com/Falcon-MC/Falcon) | The server: world, gameplay, commands, generation and scripting | [![CI](https://github.com/Falcon-MC/Falcon/actions/workflows/ci.yml/badge.svg)](https://github.com/Falcon-MC/Falcon/actions/workflows/ci.yml) |
| [Protocol](https://github.com/Falcon-MC/Protocol) | Bedrock packets, network types, NBT and binary streams | [![CI](https://github.com/Falcon-MC/Protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/Falcon-MC/Protocol/actions/workflows/ci.yml) |
| [Network](https://github.com/Falcon-MC/Network) | Transport layer: RakNet, NetherNet (WebRTC), compression and login verification | [![CI](https://github.com/Falcon-MC/Network/actions/workflows/ci.yml/badge.svg)](https://github.com/Falcon-MC/Network/actions/workflows/ci.yml) |
| [falcon-mc.github.io](https://github.com/Falcon-MC/falcon-mc.github.io) | Source of the [website](https://falcon-mc.github.io) | |

## Getting started

Download the latest Windows or Linux build from the [releases](https://github.com/Falcon-MC/Falcon/releases).
Each binary comes with a `.sha256` checksum. To build it yourself, follow the instructions in the
[Falcon README](https://github.com/Falcon-MC/Falcon#building).

## License

Falcon, Protocol and Network are licensed under the
[GNU Lesser General Public License v3.0](https://github.com/Falcon-MC/Falcon/blob/main/LICENSE).
