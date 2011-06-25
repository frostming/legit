# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module povides the CLI interface to legit.
"""

import sys

import clint
from clint.textui import colored, indent, puts

from .core import __version__


def main():
    dispatch()


def dispatch():

    if clint.args.contains(('-h', '--help')):
        display_info()
        sys.exit(1)

    elif clint.args.contains(('-v', '--version')):
        display_version()
        sys.exit(1)

    else:
        display_info()
        sys.exit(1)





def display_info():
    puts('{0} by Kenneth Reitz <me@kennethreitz.com>'.format(colored.yellow('legit')))
    puts('https://github.com/kennethreitz/legit\n')
    puts('Usage: {0}'.format(colored.blue('legit <command>')))


def display_version():
    puts('{0} v{1}'.format(
        colored.yellow('legit'),
        __version__
    ))



