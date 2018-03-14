Make-Vagrant
---

## Requirements

* click
* Jinja2

## Installation

On host

```shell
$ pip install -r requirements
```

Using Pipenv

```shell
$ pipenv install requirements
$ pipenv run -- python make-vagrant.py --help
```

## Usage

```shell
Usage: make-vagrant.py [OPTIONS]

  Simple process to create Vagrant file from given distrib

Options:
  -d, --distrib TEXT    Box distribution
  -p, --port INTEGER    Ports to forward
  --provider TEXT       Prodiver
  -m, --memory INTEGER  Custom VM memory
  -c, --cpu INTEGER     Custom VM CPU
  --help                Show this message and exit.
```

## Available distributions

* Amazon Linux 2
    * Version 2017.12.0.20171212.2
* Centos 7
    * Version 1802.01
* Debian 8
    * Version 8.10.0