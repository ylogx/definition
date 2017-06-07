Definition
==========

[![Join the chat at https://gitter.im/shubhamchaudhary/definition](https://badges.gitter.im/shubhamchaudhary/definition.svg)](https://gitter.im/shubhamchaudhary/definition?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

| Version | Downloads |
| ------- | ------------------- |
| [![Latest Version](https://img.shields.io/pypi/v/definition.svg)](https://pypi.python.org/pypi/definition/) | [![PyPi downloads](https://img.shields.io/pypi/dm/definition.svg)](https://pypi.python.org/pypi/definition) |



Fetch definition from 5 or more online dictionaries
Available easily from PyPi

#### Installation

```sh
pip install definition
```

#### Usage
To fetch definition of <query>

```sh
definition <query>
```

```sh
$ definition -h

Usage: def [-p] [-r [INT]] [-e [INT]] query

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -w, --word            Show the word of the day
  -x, --xamples         Show 30 examples
  -e EXAMPLE, --example=EXAMPLE
                        Show specified number of examples
  -r, --random          Show random words
  -q, --quiet           don't print status messages to stdout
  -p, --pronunciation   Show detailed pronunciation
```
