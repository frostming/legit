# -*- coding: utf-8 -*-

"""
legit.core
~~~~~~~~~~

Not much.
"""
import os

from clint import resources


__version__ = '0.0.1'

def find_above(*names):
    """Attempt to locate given file by searching parent dirs."""

    path = '.'

    while os.path.split(os.path.abspath(path))[1]:
        for name in names:
            joined = os.path.join(path, name)
            if os.path.exists(joined):
                return os.path.abspath(joined)
        path = os.path.join('..', path)


def path_to_repo():
    """Returns the path the current repo, if there is one."""

    return find_above('.git')


def get_available_branches():
    """Returns a list of available branches in the repo."""

    return ('master', 'develop')


def get_current_branch():
    """Returns the active available branches in the repo."""

    return 'develop'


def sync_repo():
    """Git fetch. Auto branch of remotes? pull --rebase, push."""
    pass


print path_to_repo()
# Init Resources

resources.init('kennethreitz', 'legit')
resources.user.write('config.ini', "we'll get there.")