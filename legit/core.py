# -*- coding: utf-8 -*-

"""
legit.core
~~~~~~~~~~

Not much.
"""

from clint import resources
resources.init('kennethreitz', 'legit')
resources.user.write('config.ini', "we'll get there.")


__version__ = '0.0.1'


def path_to_repo():
    """Returns the path the current repo, if there is one."""

    return None


def get_available_branches():
    """Returns a list of available branches in the repo."""

    return ('master', 'develop')


def get_current_branch():
    """Returns the active available branches in the repo."""

    return 'develop'


def sync_repo():
    """Git fetch. Auto branch of remotes? pull --rebase, push."""
    pass