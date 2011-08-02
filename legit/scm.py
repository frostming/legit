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
from git.exc import GitCommandError

from .helpers import find_path_above
from .settings import settings


LEGIT_TEMPLATE = 'Legit: stashing before {0}.'

git = 'git'

Branch = namedtuple('Branch', ['name', 'is_published'])


class Aborted(object):

    def __init__(self):
        self.message = None
        self.log = None


def abort(message, log=None):

    a = Aborted()
    a.message = message
    a.log = log

    settings.abort_handler(a)

def repo_check(require_remote=False):
    if repo is None:
        print 'Not a git repository.'
        sys.exit(128)

    # TODO: no remote fail
    if not repo.remotes and require_remote:
        print 'No git remotes configured. Please add one.'
        sys.exit(128)

    # TODO: You're in a merge state.



def stash_it(sync=False):
    repo_check()
    msg = 'syncing banch' if sync else 'switching branches'

    return repo.git.execute([git,
        'stash', 'save',
        LEGIT_TEMPLATE.format(msg)])


def unstash_index(sync=False):
    """Returns an unstash index if one is available."""

    repo_check()

    stash_list = repo.git.execute([git,
        'stash', 'list'])

    for stash in stash_list.splitlines():

        verb = 'syncing' if sync else 'switching'
        branch = repo.head.ref.name

        if (
            (('Legit' in stash) and
                ('On {0}:'.format(branch) in stash) and
                (verb in stash))
            or (('GitHub' in stash) and
                ('On {0}:'.format(branch) in stash) and
                (verb in stash))
        ):
            return stash[7]

def unstash_it(sync=False):
    """Unstashes changes from current branch for branch sync."""

    repo_check()

    stash_index = unstash_index(sync=sync)

    if stash_index is not None:
        return repo.git.execute([git,
            'stash', 'pop', 'stash@{{0}}'.format(stash_index)])


def fetch():

    repo_check()

    return repo.git.execute([git, 'fetch', repo.remotes[0].name])


def smart_pull():
    'git log --merges origin/master..master'

    repo_check()

    remote = repo.remotes[0].name
    branch = repo.head.ref.name

    fetch()

    return smart_merge('{0}/{1}'.format(remote, branch))


def smart_merge(branch, allow_rebase=True):

    repo_check()

    from_branch = repo.head.ref.name

    merges = repo.git.execute([git,
        'log', '--merges', '{0}..{1}'.format(branch, from_branch)])

    if allow_rebase:
        verb = 'merge' if len(merges.split('commit')) else 'rebase'
    else:
        verb = 'merge'

    try:
        return repo.git.execute([git, verb, branch])
    except GitCommandError, why:
        log = repo.git.execute([git,'merge', '--abort'])
        abort('Merge failed. Reverting.', log=why)



def push(branch=None):

    repo_check()

    if branch is None:
        return repo.git.execute([git, 'push'])
    else:
        return repo.git.execute([git, 'push', repo.remotes[0].name, branch])


def checkout_branch(branch):
    """Checks out given branch."""

    repo_check()

    return repo.git.execute([git, 'checkout', branch])


def sprout_branch(off_branch, branch):
    """Checks out given branch."""

    repo_check()

    return repo.git.execute([git, 'checkout', off_branch, '-b', branch])


def graft_branch(branch):
    """Merges branch into current branch, and deletes it."""

    repo_check()

    log = []

    try:
        msg = repo.git.execute([git, 'merge', '--no-ff', branch])
        log.append(msg)
    except GitCommandError, why:
        log = repo.git.execute([git,'merge', '--abort'])
        abort('Merge failed. Reverting.', log='{0}\n{1}'.format(why, log))


    out = repo.git.execute([git, 'branch', '-D', branch])
    log.append(out)
    return '\n'.join(log)


def unpublish_branch(branch):
    """Unpublishes given branch."""

    repo_check()

    return repo.git.execute([git,
        'push', repo.remotes[0].name, ':{0}'.format(branch)])


def publish_branch(branch):
    """Publishes given branch."""

    repo_check()

    return repo.git.execute([git,
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

    repo_check()

    # print local
    branches = []

    if remote:

        # Remote refs.
        try:
            for b in repo.remotes[0].refs:
                name = '/'.join(b.name.split('/')[1:])

                if name not in settings.forbidden_branches:
                    branches.append(Branch(name, True))
        except IndexError:
            pass


    if local:

        # Local refs.
        for b in [h.name for h in repo.heads]:

            if b not in [br.name for br in branches] or not remote:
                if b not in settings.forbidden_branches:
                    branches.append(Branch(b, False))


    return sorted(branches, key=attrgetter('name'))


def get_branch_names(local=True, remote=True):

    repo_check()

    branches = get_branches(local=local, remote=remote)

    return [b.name for b in branches]



repo = get_repo()
