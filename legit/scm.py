# -*- coding: utf-8 -*-

"""
legit.scm
~~~~~~~~~

This module provides the main interface to Git.
"""

import os
from collections import namedtuple
from operator import attrgetter

from git import Repo, Git

from .helpers import find_path_above



GH_TEMPLATE = 'GitHub: stashing before switching branches.'


Branch = namedtuple('Branch', ['name', 'is_published'])



def stash_for_switch():
    """Stashes changes from current branch for branch switch."""

    return repo.git.execute(['git',
        'stash', 'save',
        GH_TEMPLATE.format(branch=repo.head.ref.name)])


def unstash_for_switch():
    """Unstashes changes from current branch for branch switch."""

    stash_list = repo.git.execute(['git',
        'stash', 'list'])

    stash_index = None

    for stash in stash_list.splitlines():
        if ('GitHub' in stash) and (repo.head.ref.name in stash):
            stash_index = stash[7]



    if stash_index is not None:
        return repo.git.execute(['git',
            'stash', 'pop', 'stash@{{0}}'.format(stash_index)])


def checkout_branch(branch):
    """Checks out given branch."""

    return repo.heads[branch].checkout()


def get_repo(git=False):
    """Returns the current Repo, based on path."""

    bare_path = find_path_above('.git')

    if bare_path:
        prelapsarian_path = os.path.split(bare_path)[0]
        if git:
            return Git(prelapsarian_path)
        else:
            return Repo(prelapsarian_path)
    else:
        return None


def get_branches(local=True, remote=True):
    """Returns a list of local and remote branches."""

    branches = []

    if local:

        # Remote refs.
        for b in repo.remotes[0].refs:
            name = '/'.join(b.name.split('/')[1:])

            branches.append(Branch(name, True))

    if remote:

        # Local refs.
        for b in [h.name for h in repo.heads]:

            if b not in [br.name for br in branches] or not local:
                branches.append(Branch(b, False))


    return sorted(branches, key=attrgetter('name'))


def get_branch_names(local=True, remote=True):
    branches = get_branches(local=local, remote=remote)

    return [b.name for b in branches]


def set_branch():
    pass


def fetch():
    pass


repo = get_repo()