# -*- coding: utf-8 -*-

"""
legit.core
~~~~~~~~~~

This module provides the basic functionality of legit.
"""

from clint import resources
from pygit2 import Repository

from .helpers import find_path_above
from .models import Branch



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


def get_branches():
    branches = dict(local=list(), remote=list(), current=None)

    repo = get_repo(path_to_repo())

    branches = map(Branch.new_from_ref, repo.listall_references())

    kosher = []

    for branch in branches:
        if branch.name not in [d.name for d in kosher]:
            kosher.append(branch)
        else:
            print branch

    return kosher

    # for branch in repo.listall_references():
    #     if branch.startswith('refs/heads/'):
    #         branch_name = branch.replace('refs/heads/', '')
    #         branches['local'].append(branch_name)
    #     elif branch.startswith('refs/remotes/'):
    #         branch_name = branch.replace('refs/remotes/', '')
    #         branches['remote'].append(branch_name)
    #     else:
    #         # print branch
    #         pass

    # current_branch = repo.lookup_reference('HEAD').resolve().name
    # current_branch = current_branch.replace('refs/heads/', '')

    # branches['current'] = current_branch

    return branches




# print get_branches()
# print
# print dir(repo)

# Init Resources

resources.init('kennethreitz', 'legit')
resources.user.write('config.ini', "we'll get there.")