# NUDGE PROTOCOL


<img src="assets/nudger.png" alt="logo"/>

A lightweight NUDGE application layer network protocol built on UDP, ideal for nudging your buddies in a LAN. This project provides both a command-line and desktop GUI implementation for sending and receiving short, low-latency notifications across a local network.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Protocol](#protocol)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [GUI](#gui)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [License](#license)

## Overview

NUDGE protocol implements a simple UDP-based notification protocol for LAN environments. It supports:

- Broadcast nudges to all devices on the subnet
- Direct nudges to one or more specific IP addresses
- Automatic device discovery
- Desktop UI with sender controls, device scanning, and listener toggling
- Audio and popup feedback for incoming nudges

The desktop app can act as both a sender and a listener at the same time.

## Features

- Protocol-based packet validation using a fixed magic header
- Minimal packet format for compatibility and speed
- Discovery request/response support for finding online peers
- Cross-platform Python implementation
- GUI built with `customtkinter`
- Sound notifications via `pygame`

## Architecture

The project is separated into two main interfaces:

1. `cli/` - Minimal command-line scripts for sending and receiving nudges.
2. `gui/` - A more user-friendly desktop application with device discovery, logging, and target selection.

Core NUDGE protocol behavior is implemented under `gui/nudge/` and reused by the GUI app.

## Protocol

The protocol uses UDP on port `7777` by default and defines a binary packet format with a magic header, a command byte, and an optional payload.

- `DEFAULT_PORT`: `7777`
- `MAGIC_HEADER`: `b'NUDG'`
- `CMD_NUDGE`: `b'\x01'`
- `CMD_DISCOVERY_REQ`: `b'\x02'`
- `CMD_DISCOVERY_RES`: `b'\x03'`

### Packet Layout

| Offset | Field | Size | Description |
| --- | --- | --- | --- |
| `0-3` | Magic header | 4 bytes | `NUDG` identifies protocol packets |
| `4` | Command | 1 byte | `01`, `02`, or `03` |
| `5+` | Payload | Variable | ASCII payload depends on command |

### Commands

- `CMD_NUDGE` (`0x01`): Send a nudge with the sender's name in the payload.
- `CMD_DISCOVERY_REQ` (`0x02`): Broadcast a discovery request to find online devices.
- `CMD_DISCOVERY_RES` (`0x03`): Reply to a discovery request with the local device name.

### Behavior

- The listener validates the magic header and command byte.
- For `CMD_NUDGE`, the listener displays the sender name and triggers audio/log feedback.
- For `CMD_DISCOVERY_REQ`, the listener responds with `CMD_DISCOVERY_RES` and its device name.
- For `CMD_DISCOVERY_RES`, the scanner registers the responding device for the GUI device list.

## Download & run executables

Download nudger GUI desktop app executables from the latest release:
https://github.com/fotioudim/nudge-protocol/releases/latest

## Installation

### Requirements

- Python 3.8+
- `customtkinter` (GUI)
- `pygame-ce` (GUI sound)

### Install dependencies

```bash
pip install -r gui/requirements.txt
```

## Usage

### CLI

#### Start the listener

Run the listener on a machine that should receive nudges:

```bash
cd cli
python listener.py
```

#### Send a broadcast nudge

Broadcast a nudge to every listener on the LAN:

```bash
python pinger.py -b -n "YourName"
```

#### Send a direct nudge

Target a specific IP address:

```bash
python pinger.py -i 192.168.1.50 -n "YourName"
```

#### See help

```bash
python pinger.py --help
```

### GUI

The GUI app provides an integrated sender, listener, and scanner.

#### Run the GUI app

```bash
cd gui
python nudger.py
```

#### What the GUI does

- Starts the listener automatically
- Lets you choose broadcast or specific IP targets
- Shows discovered devices in a scrollable list
- Logs sent and received nudges
- Plays a notification sound on incoming nudges
- Displays popup errors for invalid input

#### Scan the LAN

Click `Scan LAN` to send a discovery request. Online peers will appear in the list, and you can click them to add their IP to the target field.

## Project Structure

```
README.md
assets/
cli/
  listener.py
  pinger.py
gui/
  nudger.py
  requirements.txt
  helper/
    alert_window.py
    sound_manager.py
  nudge/
    listener.py
    pinger.py
    protocol.py
    scanner.py
```

### Key components

- `cli/listener.py`: A simple UDP listener that prints received nudges.
- `cli/pinger.py`: A CLI sender for broadcast or direct UDP nudges.
- `gui/nudger.py`: Main desktop application UI.
- `gui/nudge/protocol.py`: Protocol constants and packet definitions.
- `gui/nudge/listener.py`: Listener logic for processing all protocol commands.
- `gui/nudge/pinger.py`: Sender logic for building and transmitting nudge packets.
- `gui/nudge/scanner.py`: Discovery request sender and device registration.
- `gui/helper/alert_window.py`: GUI alerts for errors and notifications.
- `gui/helper/sound_manager.py`: Audio feedback for incoming nudges.
