# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module povides the CLI interface to legit.
"""

import sys

import clint
from clint.textui import colored, indent, puts


def main():

    puts('{0} by Kenneth Reitz <me@kennethreitz.com>'.format(colored.yellow('legit')))
    puts('https://github.com/kennethreitz/legit\n')
    puts('Usage: {0}'.format(colored.blue('legit <command>')))

    sys.exit(1)

