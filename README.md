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

  Simple process to create Vagrant file from given distribution

Options:
  -a, --ansible TEXT    Ansible playbook for provisionning
  -b, --box TEXT        Vagrant box name
  -c, --cpu INTEGER     Custom VM CPU - Default = 2
  -d, --distrib TEXT    Box configuration from configuration dictionnary -
                        Used only if box parameter is not set
  -m, --memory INTEGER  Custom VM memory - Default = 4096
  -p, --port TEXT       Ports to forward - machine:host format
  -s, --shell TEXT      Shell script for provisionning
  -v, --version TEXT    Vagrant box version
  --help                Show this message and exit.
```

To forward multiple ports:

```shell
$ python make-vagrant.py -d debian8 -p 80:8080 -p 6060:6060
```

Shell script will always be applied before Ansible playbook during provisionning. Update the resulting Vagrantfile to inverse this behavior if needed.

## Available distributions

* Amazon Linux 2
    * Version 2017.12.0.20171212.2
* Centos 7
    * Version 1802.01
* Debian 8
    * Version 8.10.0