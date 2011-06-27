# -*- coding: utf-8 -*-

"""
legit.scm
~~~~~~~~~

This module provides the main interface to Git.
"""

import os
import sys
from collections import namedtuple
from operator import attrgetter

from git import Repo, Git

from .helpers import find_path_above

LEGIT_TEMPLATE = 'Legit: stashing before {0}.'


Branch = namedtuple('Branch', ['name', 'is_published'])



def stash_it(sync=False):

    msg = 'syncing banch' if sync else 'switching branches'

    return repo.git.execute(['git',
        'stash', 'save',
        LEGIT_TEMPLATE.format(msg)])


def unstash_index(sync=False):
    """Returns an unstash index if one is available."""

    stash_list = repo.git.execute(['git',
        'stash', 'list'])

    for stash in stash_list.splitlines():

        verb = 'syncing' if sync else 'switching'

        if (
            (('Legit' in stash) and
                (repo.head.ref.name in stash) and
                (verb in stash))
            or (('GitHub' in stash) and
                (repo.head.ref.name in stash) and
                (verb in stash))
        ):
            return stash[7]


def unstash_it(sync=False):
    """Unstashes changes from current branch for branch sync."""

    stash_index = unstash_index(sync=sync)

    if stash_index is not None:
        return repo.git.execute(['git',
            'stash', 'pop', 'stash@{{0}}'.format(stash_index)])


def fetch():
    return repo.git.execute(['git', 'fetch', repo.remotes[0].name])


def smart_pull():
    'git log --merges origin/master..master'

    remote = repo.remotes[0].name
    branch = repo.head.ref.name

    fetch()

    merges = repo.git.execute(['git',
        'log', '--merges', '{0}/{1}..{1}'.format(remote, branch)])

    verb = 'merge' if len(merges.split('commit')) else 'rebase'

    return repo.git.execute(['git', verb, '{0}/{1}'.format(remote, branch)])


def push(branch=None):
    if branch is None:
        return repo.git.execute(['git', 'push'])
    else:
        return repo.git.execute(['git', 'push', repo.remotes[0].name, branch])


def checkout_branch(branch):
    """Checks out given branch."""

    return repo.git.execute(['git', 'checkout', branch])


def sprout_branch(off_branch, branch):
    """Checks out given branch."""

    return repo.git.execute(['git', 'checkout', off_branch, '-b', branch])


def graft_branch(branch):
    """Merges branch into current branch, and deletes it."""

    log = []

    stat, out, err = repo.git.execute(
        ['git', 'merge', '--no-ff', branch], with_extended_output=True)

    log.append(out)

    if stat is 0:
        out = repo.git.execute(['git', 'branch', '-D', branch])
        log.append(out)
        return '\n'.join(log)
    else:
        return 'There was a problem merging, so the branch was not deleted.'


def unpublish_branch(branch):
    """Unpublishes given branch."""

    return repo.git.execute(['git',
        'push', repo.remotes[0].name, ':{0}'.format(branch)])


def publish_branch(branch):
    """Publishes given branch."""

    return repo.git.execute(['git',
        'push', repo.remotes[0].name, branch])


def get_repo():
    """Returns the current Repo, based on path."""

    bare_path = find_path_above('.git')

    if bare_path:
        prelapsarian_path = os.path.split(bare_path)[0]
        return Repo(prelapsarian_path)
    else:
        return None


def get_branches(local=True, remote=True):
    """Returns a list of local and remote branches."""

    # print local
    branches = []

    if remote:

        # Remote refs.
        for b in repo.remotes[0].refs:
            name = '/'.join(b.name.split('/')[1:])

            branches.append(Branch(name, True))

    if local:

        # Local refs.
        for b in [h.name for h in repo.heads]:

            if b not in [br.name for br in branches] or not remote:
                branches.append(Branch(b, False))


    return sorted(branches, key=attrgetter('name'))


def get_branch_names(local=True, remote=True):
    branches = get_branches(local=local, remote=remote)

    return [b.name for b in branches]



repo = get_repo()

if repo is None:
    print 'Not a git repository.'
    sys.exit(128)