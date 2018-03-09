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

import clint
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from .settings import settings

LEGIT_TEMPLATE = 'Legit: stashing before {0}.'

git = os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", 'git')

Branch = namedtuple('Branch', ['name', 'is_published'])


class Aborted(object):

    def __init__(self):
        self.message = None
        self.log = None


def abort(message, log=None, type=None):

    a = Aborted()
    a.message = message
    a.log = log

    settings.abort_handler(a, type=type)


def repo_check(repo, require_remote=False):
    if repo is None:
        print('Not a git repository.')
        sys.exit(128)

    # TODO: no remote fail
    if not repo.remotes and require_remote:
        print('No git remotes configured. Please add one.')
        sys.exit(128)

    # TODO: You're in a merge state.


def stash_it(repo, sync=False):
    repo_check(repo)
    msg = 'syncing branch' if sync else 'switching branches'

    return repo.git.execute([git,
        'stash', 'save', '--include-untracked',
        LEGIT_TEMPLATE.format(msg)])


def unstash_index(repo, sync=False, branch=None):
    """Returns an unstash index if one is available."""

    repo_check(repo)

    stash_list = repo.git.execute([git, 'stash', 'list'])

    if branch is None:
        branch = get_current_branch_name(repo)

    for stash in stash_list.splitlines():

        verb = 'syncing' if sync else 'switching'

        if (
            (('Legit' in stash) and
                ('On {0}:'.format(branch) in stash) and
                (verb in stash))
            or (('GitHub' in stash) and
                ('On {0}:'.format(branch) in stash) and
                (verb in stash))
        ):
            return stash[7]


def unstash_it(repo, sync=False, branch=None):
    """Unstashes changes from current branch for branch sync."""

    repo_check(repo)

    stash_index = unstash_index(repo, sync=sync, branch=branch)

    if stash_index is not None:
        return repo.git.execute([git,
            'stash', 'pop', 'stash@{{{0}}}'.format(stash_index)])


def smart_pull(repo):
    'git log --merges origin/master..master'

    repo_check(require_remote=True)

    branch = get_current_branch_name()

    repo.git.execute([git, 'fetch', repo.remote.name])

    return smart_merge('{0}/{1}'.format(repo.remote.name, branch), smart_merge_enabled())


def smart_merge_enabled(repo):
    reader = repo.config_reader()
    if reader.has_option('legit', 'smartMerge'):
        return reader.getboolean('legit', 'smartMerge')
    else:
        return True


def smart_merge(repo, branch, allow_rebase=True):

    repo_check(repo)

    from_branch = get_current_branch_name()

    merges = repo.git.execute([git,
        'log', '--merges', '{0}..{1}'.format(branch, from_branch)])

    if allow_rebase:
        verb = 'merge' if merges.count('commit') else 'rebase'
    else:
        if git_pull_rebase():
            verb = 'rebase'
        else:
            verb = 'merge'

    if git_pull_ff_only():
        return repo.git.execute([git, verb, '--ff-only', branch])
    else:
        try:
            return repo.git.execute([git, verb, branch])
        except GitCommandError as why:
            log = repo.git.execute([git, verb, '--abort'])
            abort('Merge failed. Reverting.',
                  log='{0}\n{1}'.format(why, log), type='merge')


def git_pull_rebase(repo):
    reader = repo.config_reader()
    if reader.has_option('pull', 'rebase'):
        return reader.getboolean('pull', 'rebase')
    else:
        return False


def git_pull_ff_only(repo):
    reader = repo.config_reader()
    if reader.has_option('pull', 'ff'):
        if reader.getboolean('pull', 'ff') == "only":
            return True
        else:
            return False
    else:
        return False


def push(repo, branch=None):

    repo_check(repo, require_remote=True)

    if branch is None:
        return repo.git.execute([git, 'push'])
    else:
        return repo.git.execute([git, 'push', repo.remote.name, branch])


def checkout_branch(repo, branch):
    """Checks out given branch."""

    repo_check(repo)

    _, stdout, stderr = repo.git.execute([git, 'checkout', branch],
                                         with_extended_output=True)
    return '\n'.join([stderr, stdout])


def unpublish_branch(repo, branch):
    """Unpublishes given branch."""

    repo_check(repo, require_remote=True)

    try:
        return repo.git.execute([git,
            'push', repo.remote.name, ':{0}'.format(branch)])
    except GitCommandError:
        _, _, log = repo.git.execute([git, 'fetch', repo.remote.name, '--prune'],
                                     with_extended_output=True)
        abort('Unpublish failed. Fetching.', log=log, type='unpublish')


def publish_branch(repo, branch):
    """Publishes given branch."""

    repo_check(repo, require_remote=True)

    return repo.git.execute([git,
        'push', '-u', repo.remote.name, branch])


def get_repo():
    """Returns the current Repo, based on path."""

    try:
        return Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        pass


def get_remote(repo):

    repo_check(repo)

    reader = repo.config_reader()

    # If there is no remote option in legit section, return default
    if reader.has_option('legit', 'remote'):
        remote_name = reader.get('legit', 'remote')
        if remote_name not in [r.name for r in repo.remotes]:
            if fallback_enabled(reader):
                return get_default_remote()
            else:
                print('Remote "{0}" does not exist!'.format(remote_name))
                will_aborted = clint.textui.prompt.yn(
                    '\nPress `y` to abort now,\n' +
                    '`n` to use default remote and turn fallback on for this repo:')
                if will_aborted:
                    print('\nAborted. Please update your git configuration.')
                    sys.exit(64)  # EX_USAGE
                else:
                    writer = repo.config_writer()
                    writer.set_value('legit', 'remoteFallback', 'true')
                    print('\n`legit.RemoteFallback` changed to true for current repo.')
                    return get_default_remote(repo)
        else:
            return repo.remote(remote_name)
    else:
        return get_default_remote(repo)


# Instead of getboolean('legit', 'remoteFallback', fallback=False)
# since getboolean in Python 2 does not have fallback argument.
def fallback_enabled(reader):
    if reader.has_option('legit', 'remoteFallback'):
        return reader.getboolean('legit', 'remoteFallback')
    else:
        return False


def get_default_remote(repo):
    if len(repo.remotes) == 0:
        return None
    else:
        return repo.remotes[0]


def get_current_branch_name(repo):
    """Returns current branch name"""

    repo_check(repo)

    return repo.head.ref.name


def get_branches(repo, local=True, remote_branches=True):
    """Returns a list of local and remote branches."""

    repo_check(repo)

    if not repo.remotes:
        remote_branches = False

    branches = []

    if remote_branches:

        # Remote refs.
        try:
            for b in repo.remote.refs:
                name = '/'.join(b.name.split('/')[1:])

                if name not in settings.forbidden_branches:
                    branches.append(Branch(name, is_published=True))
        except (IndexError, AssertionError):
            pass

    if local:

        # Local refs.
        for b in [h.name for h in repo.heads]:

            if (not remote_branches) or (b not in [br.name for br in branches]):
                if b not in settings.forbidden_branches:
                    branches.append(Branch(b, is_published=False))


    return sorted(branches, key=attrgetter('name'))


def get_branch_names(repo, local=True, remote_branches=True):

    repo_check(repo)

    branches = get_branches(local=local, remote_branches=remote_branches)

    return [b.name for b in branches]
