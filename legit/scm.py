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
from clint.textui import colored, columns
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


class SCMRepo(object):
    repo = None
    remote = None
    verbose = False

    def __init__(self):
        try:
            self.repo = Repo(search_parent_directories=True)
            self.remote = self.get_remote()
        except InvalidGitRepositoryError:
            self.repo = None

    def repo_check(self, require_remote=False):
        if self.repo is None:
            print('Not a git repository.')
            sys.exit(128)

        # TODO: no remote fail
        if not self.repo.remotes and require_remote:
            print('No git remotes configured. Please add one.')
            sys.exit(128)

        # TODO: You're in a merge state.

    def stash_it(self, sync=False):
        self.repo_check()
        msg = 'syncing branch' if sync else 'switching branches'

        return self.repo.git.execute(
            [git, 'stash', 'save', '--include-untracked', LEGIT_TEMPLATE.format(msg)])

    def unstash_index(self, sync=False, branch=None):
        """Returns an unstash index if one is available."""

        self.repo_check()

        stash_list = self.repo.git.execute([git, 'stash', 'list'])

        if branch is None:
            branch = self.get_current_branch_name()

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

    def unstash_it(self, sync=False, branch=None):
        """Unstashes changes from current branch for branch sync."""

        self.repo_check()

        stash_index = self.unstash_index(sync=sync, branch=branch)

        if stash_index is not None:
            return self.repo.git.execute(
                [git, 'stash', 'pop', 'stash@{{{0}}}'.format(stash_index)])

    def smart_pull(self):
        """
        'git log --merges origin/master..master'
        """

        self.repo_check(require_remote=True)

        branch = self.get_current_branch_name()

        self.repo.git.execute([git, 'fetch', self.remote.name])

        return self.smart_merge('{0}/{1}'.format(self.remote.name, branch),
                                self.smart_merge_enabled())

    def smart_merge_enabled(self):
        reader = self.repo.config_reader()
        if reader.has_option('legit', 'smartMerge'):
            return reader.getboolean('legit', 'smartMerge')
        else:
            return True

    def smart_merge(self, branch, allow_rebase=True):

        self.repo_check()

        from_branch = self.get_current_branch_name()

        merges = self.repo.git.execute(
            [git, 'log', '--merges', '{0}..{1}'.format(branch, from_branch)])

        if allow_rebase:
            verb = 'merge' if merges.count('commit') else 'rebase'
        else:
            if self.git_pull_rebase():
                verb = 'rebase'
            else:
                verb = 'merge'

        if self.git_pull_ff_only():
            return self.repo.git.execute([git, verb, '--ff-only', branch])
        else:
            try:
                return self.repo.git.execute([git, verb, branch])
            except GitCommandError as why:
                log = self.repo.git.execute([git, verb, '--abort'])
                abort('Merge failed. Reverting.',
                      log='{0}\n{1}'.format(why, log), type='merge')

    def git_pull_rebase(self):
        reader = self.repo.config_reader()
        if reader.has_option('pull', 'rebase'):
            return reader.getboolean('pull', 'rebase')
        else:
            return False

    def git_pull_ff_only(self):
        reader = self.repo.config_reader()
        if reader.has_option('pull', 'ff'):
            if reader.getboolean('pull', 'ff') == "only":
                return True
            else:
                return False
        else:
            return False

    def push(self, branch=None):

        self.repo_check(require_remote=True)

        if branch is None:
            return self.repo.git.execute([git, 'push'])
        else:
            return self.repo.git.execute([git, 'push', self.remote.name, branch])

    def checkout_branch(self, branch):
        """Checks out given branch."""

        self.repo_check()

        _, stdout, stderr = self.repo.git.execute(
            [git, 'checkout', branch],
            with_extended_output=True)
        return '\n'.join([stderr, stdout])

    def unpublish_branch(self, branch):
        """Unpublishes given branch."""

        self.repo_check(require_remote=True)

        try:
            return self.repo.git.execute(
                [git, 'push', self.remote.name, ':{0}'.format(branch)])
        except GitCommandError:
            _, _, log = self.repo.git.execute(
                [git, 'fetch', self.remote.name, '--prune'],
                with_extended_output=True)
            abort('Unpublish failed. Fetching.', log=log, type='unpublish')

    def publish_branch(self, branch):
        """Publishes given branch."""

        self.repo_check(require_remote=True)

        return self.repo.git.execute(
            [git, 'push', '-u', self.remote.name, branch])

    def get_remote(self):

        self.repo_check()

        reader = self.repo.config_reader()

        # If there is no remote option in legit section, return default
        if reader.has_option('legit', 'remote'):
            remote_name = reader.get('legit', 'remote')
            if remote_name not in [r.name for r in self.repo.remotes]:
                if fallback_enabled(reader):
                    return self.get_default_remote()
                else:
                    print('Remote "{0}" does not exist!'.format(remote_name))
                    will_aborted = clint.textui.prompt.yn(
                        '\nPress `y` to abort now,\n' +
                        '`n` to use default remote and turn fallback on for this repo:')
                    if will_aborted:
                        print('\nAborted. Please update your git configuration.')
                        sys.exit(64)  # EX_USAGE
                    else:
                        writer = self.repo.config_writer()
                        writer.set_value('legit', 'remoteFallback', 'true')
                        print('\n`legit.RemoteFallback` changed to true for current repo.')
                        return self.get_default_remote()
            else:
                return self.remote(remote_name)
        else:
            return self.get_default_remote()

    def get_default_remote(self):
        if len(self.repo.remotes) == 0:
            return None
        else:
            return self.repo.remotes[0]

    def get_current_branch_name(self):
        """Returns current branch name"""

        self.repo_check()

        return self.repo.head.ref.name

    def fuzzy_match_branch(self, branch):
        if not branch:
            return False

        all_branches = self.get_branch_names()
        if branch in all_branches:
            return branch

        def branch_fuzzy_match(b):
            return b.startswith(branch)

        possible_branches = list(filter(branch_fuzzy_match, all_branches))

        if len(possible_branches) == 1:
            return possible_branches[0]

        return branch

    def get_branches(self, local=True, remote_branches=True):
        """Returns a list of local and remote branches."""

        self.repo_check()

        if not self.repo.remotes:
            remote_branches = False

        branches = []

        if remote_branches:

            # Remote refs.
            try:
                for b in self.remote.refs:
                    name = '/'.join(b.name.split('/')[1:])

                    if name not in settings.forbidden_branches:
                        branches.append(Branch(name, is_published=True))
            except (IndexError, AssertionError):
                pass

        if local:

            # Local refs.
            for b in [h.name for h in self.repo.heads]:

                if (not remote_branches) or (b not in [br.name for br in branches]):
                    if b not in settings.forbidden_branches:
                        branches.append(Branch(b, is_published=False))

        return sorted(branches, key=attrgetter('name'))

    def get_branch_names(self, local=True, remote_branches=True):

        self.repo_check()

        branches = self.get_branches(local=local, remote_branches=remote_branches)

        return [b.name for b in branches]

    def display_available_branches(self):
        """Displays available branches."""

        if not self.repo.remotes:
            remote_branches = False
        else:
            remote_branches = True
        branches = self.get_branches(local=True, remote_branches=remote_branches)

        if not branches:
            print(colored.red('No branches available'))
            return

        branch_col = len(max([b.name for b in branches], key=len)) + 1

        for branch in branches:

            try:
                branch_is_selected = (branch.name == self.get_current_branch_name())
            except TypeError:
                branch_is_selected = False

            marker = '*' if branch_is_selected else ' '
            color = colored.green if branch_is_selected else colored.yellow
            pub = '(published)' if branch.is_published else '(unpublished)'

            print(columns(
                [colored.red(marker), 2],
                [color(branch.name), branch_col],
                [colored.black(pub), 14]
            ))


# Instead of getboolean('legit', 'remoteFallback', fallback=False)
# since getboolean in Python 2 does not have fallback argument.
def fallback_enabled(reader):
    if reader.has_option('legit', 'remoteFallback'):
        return reader.getboolean('legit', 'remoteFallback')
    else:
        return False
