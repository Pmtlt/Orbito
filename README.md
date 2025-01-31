# Orbito

[![PyPI - Version](https://img.shields.io/pypi/v/orbito.svg)](https://pypi.org/project/orbito)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/orbito.svg)](https://pypi.org/project/orbito)

-----

**Table of Contents**

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Description

Orbito is a strategic board game where two players compete to align 4 balls of their color while using unique rotation mechanics. The game features a wooden-themed interface built with Tkinter.

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
python -m orbito.main
```

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

`orbito` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.