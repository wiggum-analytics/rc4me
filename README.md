# rc4me

[![Continuous Integration](https://github.com/wiggums-analytics/rc4me/actions/workflows/ci.yml/badge.svg)](https://github.com/wiggums-analytics/rc4me/actions/workflows/ci.yml)

Run Commands 4 Me: Quickly and easily set up your run commands files

## Project description

`rc4me` aims to simplify and expedite setting up your run command files (`.bashrc`,
`.bashprofile`, `.vimrc`...) on your computer. Work environment here is defined as the set
of run command files that define your shell configuration. If find yourself working on
different dev boxes, you may be interested in this package.  With a single command, you
are all set!

Example:
"M, check out this new vim plugin I've been using"-J
...M runs an `rc4me apply` command...
"Cool dude, but not for me"-M
...M reverts to his work environment using `rc4me revert`...

## Setup

There are two pieces of the set-up:
1. installing the package
2. 2. setting up a git repo with your run commands.

### 1. Install
#### pip

`rc4me` is available on `pip`. You'll need [pip](https://pip.pypa.io/en/stable/installing/).

```
pip install rc4me
```

#### From source

To install from source, you'll need to run a git clone then a local `pip` install (done
as a `make` command):

```
git clone wiggums-analytics/rc4me
make install
```

### 2. Setting up your run commands repo

You'll need to put your run commands on github for `rc4me` to find them. Run command
files are typically hidden---i.e., has a dot in front `~/.bashrc`. `rc4me` expects your
rc files in your repo to not hidden (no dot). For example

```
# My repo
bashrc
bash_profile
vimrc
```

An example repo can be found [here](https://github.com/mstefferson/rc-demo).

## Basic usage

Grab and setup rc files from `mstefferson/rc-demo`

```
rc4me apply mstefferson/rc-demo
```

If you want to reset everything:

```
rc4me reset
```

Note, `reset` will reset the configuration that `rc4me` saw when running it's first
command.


Note, after running commands, the changes will be applied in a new shell--i.e., we don't
source bash files.

### Getting help

List CLI commands:

```
rc4me --help
```

For help on a specific command (e.g., `apply`):

```
rc4me apply --help
```

## What is rcm4e doing?

`rc4me` downloads files for github and soft-links them on you computer. All the files
`rc4me` interacts with are saved in `~/.rc4me/`. `rc4me` softlinks files to the user
provided destination.

## Danger zone

`rc4me` can undo everything it does **unless** you nuke `~/.rc4me`.  It is highly
**recommended  to not delete `~/.rc4me` without running `rc4me reset` first**.
