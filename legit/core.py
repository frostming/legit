# -*- coding: utf-8 -*-

"""
legit.core
~~~~~~~~~~

This module provides the basic functionality of legit.
"""

from clint import resources
from pygit2 import Repository

from .helpers import find_path_above



__version__ = '0.0.1'
__author__ = 'Kenneth Reitz'
__license__ = 'TBD'


def get_repo(path_to_repo):
    return Repository(path_to_repo)


def path_to_repo():
    """Returns the path the current repo, if there is one."""

    return find_path_above('.git')


def get_available_branches():
    """Returns a list of available branches in the repo."""

    return ('master', 'develop')


def switch_to_branch(branch):
    pass


def sync_repo():
    """Git fetch. Auto branch of remotes? pull --rebase, push."""
    pass



# print get_branches()
# print
# print dir(repo)

# Init Resources

resources.init('kennethreitz', 'legit')
resources.user.write('config.ini', "we'll get there.")