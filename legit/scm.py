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
LEGIT_TEMPLATE = 'Legit: stashing before syncing.'


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


def stash_for_sync():
    return repo.git.execute(['git',
        'stash', 'save',
        LEGIT_TEMPLATE.format(branch=repo.head.ref.name)])


def unstash_for_sync():
    """Unstashes changes from current branch for branch sync."""

    stash_list = repo.git.execute(['git',
        'stash', 'list'])

    stash_index = None

    for stash in stash_list.splitlines():
        if ('Legit' in stash) and (repo.head.ref.name in stash):
            stash_index = stash[7]

    if stash_index is not None:
        return repo.git.execute(['git',
            'stash', 'pop', 'stash@{{0}}'.format(stash_index)])


def fetch():
    return repo.git.execute(['git', 'fetch', repo.remotes[0].name])

def smart_pull():
    'git log --merges origin/master..master'

    local_merges = repo.git.execute(['git',
        'log', '--merges', '{0}/{1}..{1}'.format(
            repo.remotes[0].name, repo.head.ref.name
        )
    ])

    print local_merges


def pull(branch=None):
    if branch is None:
        return repo.git.execute(['git', 'pull', '--rebase'])
    else:
        return repo.git.execute(['git', 'pull', '--rebase', repo.remotes[0].name, branch])


def push(branch=None):
    if branch is None:
        return repo.git.execute(['git', 'push'])
    else:
        return repo.git.execute(['git', 'push', repo.remotes[0].name, branch])


def checkout_branch(branch):
    """Checks out given branch."""

    return repo.git.execute(['git', 'checkout', branch])


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

# fuck

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


def fetch():
    pass


repo = get_repo()