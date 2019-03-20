# Vehicle routing problem

## Installation

All scripts were tested using Python 3.7.1 on a 64 bit system.
*ortools* library, which is one of project dependencies, 
at the moment works only with 64 bit Python installation. Furthermore, on Windows it might require 
[latest supported Visual C++ redistributable packages x64](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).

At first, install pipenv package:
https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
and run following command in project directory

```bash
pipenv install
```

## Usage

Scripts can be ran in terminal:

```bash
python vrp.py --help
```

Available parameters as environment variables:
- APP_KEY - application key for Google API

## Unit tests
```bash
make run-tests
```

## Static code analysis

Combination of *mypy* and typehints.

```bash
make run-mypy
```