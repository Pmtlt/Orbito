\[![PyPI - Version](https://img.shields.io/pypi/v/orbito.svg)](https://pypi.org/project/orbito)
\[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/orbito.svg)](https://pypi.org/project/orbito)


-----

**Table of Contents**

- [Description](#description)
- [Features](#features)
- [Installation](#installation) 
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Development](#development)
- [License](#license)

## Description

Orbito is a strategic board game where two players compete to align 4 balls of their color while using unique rotation mechanics. The game features a wooden-themed interface built with Tkinter and includes an AI opponent.

## Features

- Beautiful wooden-themed interface
- Single player mode against AI with different difficulty levels
- Automatic board rotation with animated central button 
- Visual effects including ball shine and wood grain
- Real-time turn indicators and game status
- Win/Draw detection

## Installation

### From PyPI
```console
pip install orbito
```

### From Source 
```console
git clone https://github.com/yourusername/orbito.git
cd orbito
pip install -e .
```

### Windows Executable
Download the latest release from the releases page and run `Orbito.exe`.

## Usage

To start the game:
```console 
python -m orbito
```

## Game Rules

1. Players take turns placing balls on the 4x4 board
2. After each move, the board automatically rotates:
  - Outer ring rotates clockwise
  - Inner square rotates counterclockwise
3. First player to align 4 balls of their color wins
4. Game ends in a draw if board is full with no winner

## AI Features

- Basic AI opponent
- Move evaluation considering:
  - Potential winning moves
  - Center control
  - Multiple ball alignments
- Automatic moves and rotation

## Development

### Running Tests
```console
pip install -e ".[dev]"
pytest
```

### Building the Executable
```console
python scripts/build_exe.py build
```

## License

`orbito` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.```
