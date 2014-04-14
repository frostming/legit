# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module provides the CLI interface to legit.
"""

import os
import sys
from subprocess import call
from time import sleep

import clint.resources
from clint import Args
from clint.eng import join as eng_join
from clint.textui import colored, puts, columns

from .core import __version__
from .settings import settings
from .helpers import is_lin, is_osx, is_win
from .scm import *

args = Args()

def black(s):
    if settings.allow_black_foreground:
        return colored.black(s)
    else:
        return s.encode('utf-8')

# --------
# Dispatch
# --------

def main():
    """Primary Legit command dispatch."""

    command = Command.lookup(args.get(0))
    if command:
        arg = args.get(0)
        args.remove(arg)

        command.__call__(args)
        sys.exit()

    elif args.contains(('-h', '--help')):
        display_help()
        sys.exit(1)

    elif args.contains(('-v', '--version')):
        display_version()
        sys.exit(1)

    else:
        if settings.git_transparency:
            # Send everything to git
            git_args = list(sys.argv)
            if settings.git_transparency is True:
                settings.git_transparency = os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", 'git')

            git_args[0] = settings.git_transparency

            sys.exit(call(' '.join(git_args), shell=True))

        else:
            show_error(colored.red('Unknown command {0}'.format(args.get(0))))
            display_info()
            sys.exit(1)


def show_error(msg):
    sys.stdout.flush()
    sys.stderr.write(msg + '\n')


# -------
# Helpers
# -------

def status_log(func, message, *args, **kwargs):
    """Executes a callable with a header message."""

    print message
    log = func(*args, **kwargs)

    if log:
        out = []

        for line in log.split('\n'):
            if not line.startswith('#'):
                out.append(line)
        print black('\n'.join(out))


def switch_to(branch):
    """Runs the cmd_switch command with given branch arg."""

    switch_args = args.copy
    switch_args._args = [branch]

    return cmd_switch(switch_args)

def fuzzy_match_branch(branch):
    if not branch: return False

    all_branches = get_branch_names()
    if branch in all_branches:
        return branch

    def branch_fuzzy_match(b): return b.startswith(branch)
    possible_branches = filter(branch_fuzzy_match, all_branches)

    if len(possible_branches) == 1:
        return possible_branches[0]

    return False

# --------
# Commands
# --------

def cmd_switch(args):
    """Legit Switch command."""

    from_branch = repo.head.ref.name
    to_branch = args.get(0)
    to_branch = fuzzy_match_branch(to_branch)

    if not to_branch:
        print 'Please specify a branch to switch to:'
        display_available_branches()
        sys.exit()

    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.')

    status_log(checkout_branch, 'Switching to {0}.'.format(
        colored.yellow(to_branch)), to_branch)

    if unstash_index(branch=from_branch):
        status_log(unstash_it, 'Restoring local changes.', branch=from_branch)

def cmd_resync(args):
    """Stashes unstaged changes, 
    Fetches upstream data from master branch,
    Auto-Merge/Rebase from master branch 
    Performs smart pull+merge, 
    Pushes local commits up, and Unstashes changes.
    Defaults to current branch.
    """
    if args.get(0):
        upstream = fuzzy_match_branch(args.get(0))
        if upstream:
            is_external = True
            original_branch = repo.head.ref.name
        else:
            print "{0} doesn't exist. Use a branch that does.".format(
                colored.yellow(args.get(0)))
            sys.exit(1)
    else:
        upstream = "master"
    original_branch = repo.head.ref.name
    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.', sync=True)
    switch_to(upstream)
    status_log(smart_pull, 'Pulling commits from the server.')
    switch_to(original_branch)
    status_log(smart_merge, 'Grafting commits from {0}.'.format(
        colored.yellow(upstream)), upstream, allow_rebase=False)
    if unstash_index(sync=True):
        status_log(unstash_it, 'Restoring local changes.', sync=True)
    status_log(smart_pull, 'Pulling commits from the server.')
    status_log(push, 'Pushing commits to the server.', original_branch)

def cmd_sync(args):
    """Stashes unstaged changes, Fetches remote data, Performs smart
    pull+merge, Pushes local commits up, and Unstashes changes.

    Defaults to current branch.
    """

    if args.get(0):
        # Optional branch specifier.
        branch = fuzzy_match_branch(args.get(0))
        if branch:
            is_external = True
            original_branch = repo.head.ref.name
        else:
            print "{0} doesn't exist. Use a branch that does.".format(
                colored.yellow(args.get(0)))
            sys.exit(1)
    else:
        # Sync current branch.
        branch = repo.head.ref.name
        is_external = False

    if branch in get_branch_names(local=False):

        if is_external:
            switch_to(branch)

        if repo.is_dirty():
            status_log(stash_it, 'Saving local changes.', sync=True)

        status_log(smart_pull, 'Pulling commits from the server.')
        status_log(push, 'Pushing commits to the server.', branch)

        if unstash_index(sync=True):
            status_log(unstash_it, 'Restoring local changes.', sync=True)

        if is_external:
            switch_to(original_branch)

    else:
        print '{0} has not been published yet.'.format(
            colored.yellow(branch))
        sys.exit(1)


def cmd_sprout(args):
    """Creates a new branch of given name from given branch.
    Defaults to current branch.
    """

    off_branch = args.get(0)
    new_branch = args.get(1)

    if new_branch is None:
        new_branch = off_branch
        off_branch = repo.head.ref.name
    else:
        off_branch = fuzzy_match_branch(off_branch)

    if not off_branch:
        print 'Please specify branch to sprout:'
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names()

    if off_branch not in branch_names:
        print "{0} doesn't exist. Use a branch that does.".format(
            colored.yellow(off_branch))
        sys.exit(1)

    if new_branch in branch_names:
        print "{0} already exists. Use a unique name.".format(
            colored.yellow(new_branch))
        sys.exit(1)


    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.')

    status_log(sprout_branch, 'Branching {0} to {1}.'.format(
        colored.yellow(off_branch), colored.yellow(new_branch)),
        off_branch, new_branch)


def cmd_graft(args):
    """Merges an unpublished branch into the given branch, then deletes it."""

    branch = fuzzy_match_branch(args.get(0))
    into_branch = args.get(1)

    if not branch:
        print 'Please specify a branch to graft:'
        display_available_branches()
        sys.exit()

    if not into_branch:
        into_branch = repo.head.ref.name
    else:
        into_branch = fuzzy_match_branch(into_branch)

    branch_names = get_branch_names(local=True, remote_branches=False)
    remote_branch_names = get_branch_names(local=False, remote_branches=True)

    if branch not in branch_names:
        print "{0} doesn't exist. Use a branch that does.".format(
            colored.yellow(branch))
        sys.exit(1)

    if branch in remote_branch_names:
        print "{0} is published. To graft it, unpublish it first.".format(
            colored.yellow(branch))
        sys.exit(1)

    if into_branch not in branch_names:
        print "{0} doesn't exist. Use a branch that does.".format(
            colored.yellow(into_branch))
        sys.exit(1)

    # Go to new branch.
    switch_to(into_branch)

    status_log(graft_branch, 'Grafting {0} into {1}.'.format(
        colored.yellow(branch), colored.yellow(into_branch)), branch)


def cmd_publish(args):
    """Pushes an unpublished branch to a remote repository."""

    branch = fuzzy_match_branch(args.get(0))

    if not branch:
        branch = repo.head.ref.name
        display_available_branches()
        print "Branch {0} not found, using current branch {1}".format(colored.red(args.get(0)),colored.yellow(branch))

    branch_names = get_branch_names(local=False)

    if branch in branch_names:
        print "{0} is already published. Use a branch that isn't.".format(
            colored.yellow(branch))
        sys.exit(1)

    status_log(publish_branch, 'Publishing {0}.'.format(
        colored.yellow(branch)), branch)



def cmd_unpublish(args):
    """Removes a published branch from the remote repository."""

    branch = fuzzy_match_branch(args.get(0))

    if not branch:
        print 'Please specify a branch to unpublish:'
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names(local=False)

    if branch not in branch_names:
        print "{0} isn't published. Use a branch that is.".format(
            colored.yellow(branch))
        sys.exit(1)

    status_log(unpublish_branch, 'Unpublishing {0}.'.format(
        colored.yellow(branch)), branch)


def cmd_harvest(args):
    """Syncs a branch with given branch. Defaults to current."""

    from_branch = fuzzy_match_branch(args.get(0))
    to_branch = fuzzy_match_branch(args.get(1))

    if not from_branch:
        print 'Please specify a branch to harvest commits from:'
        display_available_branches()
        sys.exit()

    if to_branch:
        original_branch = repo.head.ref.name
        is_external = True
    else:
        is_external = False

    branch_names = get_branch_names(local=True, remote_branches=False)

    if from_branch not in branch_names:
        print "{0} isn't an available branch. Use a branch that is.".format(
            colored.yellow(from_branch))
        sys.exit(1)

    if is_external:
        switch_to(to_branch)

    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.')

    status_log(smart_merge, 'Grafting commits from {0}.'.format(
        colored.yellow(from_branch)), from_branch, allow_rebase=False)

    if is_external:
        switch_to(original_branch)

    if unstash_index():
        status_log(unstash_it, 'Restoring local changes.')


#

def cmd_branches(args):
    """Displays available branches."""

    display_available_branches()


def cmd_settings(args):
    """Opens legit settings in editor."""

    path = clint.resources.user.open('config.ini').name


    print 'Legit Settings:\n'

    for (option, _, description) in settings.config_defaults:
        print columns([colored.yellow(option), 25], [description, None])


    print '\nSee {0} for more details.'.format(settings.config_url)

    sleep(0.35)

    if is_osx:
        editor = os.environ.get('EDITOR') or os.environ.get('VISUAL') or 'open'
        os.system("{0} '{1}'".format(editor, path))
    elif is_lin:
        editor = os.environ.get('EDITOR') or os.environ.get('VISUAL') or 'pico'
        os.system("{0} '{1}'".format(editor, path))
    elif is_win:
        os.system("'{0}'".format(path))
    else:
        print "Edit '{0}' to manage Legit settings.\n".format(path)

    sys.exit()


def cmd_install(args):
    """Installs legit git aliases."""

    aliases = [
        'branches',
        'graft',
        'harvest',
        'publish',
        'unpublish',
        'sprout',
        'sync',
        'switch',
        'resync',
    ]

    print 'The following git aliases have been installed:\n'

    for alias in aliases:
        cmd = '!legit ' + alias
        os.system('git config --global --replace-all alias.{0} "{1}"'.format(alias, cmd))
        print columns(['', 1], [colored.yellow('git ' + alias), 20], [cmd, None])

    sys.exit()


def cmd_help(args):
    """Display help for individual commands."""
    command = args.get(0)
    help(command)

# -----
# Views
# -----

def help(command):
    if command == None:
        command = 'help'

    cmd = Command.lookup(command)
    usage = cmd.usage or ''
    help = cmd.help or ''
    help_text = '%s\n\n%s' % (usage, help)
    print help_text


def display_available_branches():
    """Displays available branches."""

    branches = get_branches()

    if not branches:
        print colored.red('No branches available')
        return

    branch_col = len(max([b.name for b in branches], key=len)) + 1

    for branch in branches:

        try:
            branch_is_selected = (branch.name == repo.head.ref.name)
        except TypeError:
            branch_is_selected = False

        marker = '*' if branch_is_selected else ' '
        color = colored.green if branch_is_selected else colored.yellow
        pub = '(published)' if branch.is_published else '(unpublished)'

        print columns(
            [colored.red(marker), 2],
            [color(branch.name), branch_col],
            [black(pub), 14]
        )


def display_info():
    """Displays Legit informatics."""

    puts('{0}. {1}\n'.format(
        colored.red('legit'),
        black(u'A Kenneth Reitz Project™')
    ))

    puts('Usage: {0}'.format(colored.blue('legit <command>')))
    puts('Commands:\n')
    for command in Command.all_commands():
        usage = command.usage or command.name
        help = command.help or ''
        puts('{0:40} {1}'.format(
                colored.green(usage),
                first_sentence(help)))


def first_sentence(s):
    pos = s.find('. ')
    if pos < 0:
        pos = len(s) - 1
    return s[:pos + 1]


def display_help():
    """Displays Legit help."""

    display_info()


def display_version():
    """Displays Legit version/release."""


    puts('{0} v{1}'.format(
        colored.yellow('legit'),
        __version__
    ))


def handle_abort(aborted):
    print colored.red('Error:'), aborted.message
    print black(str(aborted.log))
    print 'Unfortunately, there was a merge conflict. It has to be merged manually.'
    sys.exit(1)


settings.abort_handler = handle_abort


class Command(object):
    COMMANDS = {}
    SHORT_MAP = {}

    @classmethod
    def register(klass, command):
        klass.COMMANDS[command.name] = command
        if command.short:
            for short in command.short:
                klass.SHORT_MAP[short] = command

    @classmethod
    def lookup(klass, name):
        if name in klass.SHORT_MAP:
            return klass.SHORT_MAP[name]
        if name in klass.COMMANDS:
            return klass.COMMANDS[name]
        else:
            return None

    @classmethod
    def all_commands(klass):
        return sorted(klass.COMMANDS.values(),
                      key=lambda cmd: cmd.name)

    def __init__(self, name=None, short=None, fn=None, usage=None, help=None):
        self.name = name
        self.short = short
        self.fn = fn
        self.usage = usage
        self.help = help

    def __call__(self, *args, **kw_args):
        return self.fn(*args, **kw_args)


def def_cmd(name=None, short=None, fn=None, usage=None, help=None):
    command = Command(name=name, short=short, fn=fn, usage=usage, help=help)
    Command.register(command)


def_cmd(
    name='branches',
    fn=cmd_branches,
    usage='branches',
    help='Get a nice pretty list of branches.')

def_cmd(
    name='graft',
    short=['gr'],
    fn=cmd_graft,
    usage='graft <branch> <into-branch>',
    help=('Merges specified branch into the second branch, and removes it. '
          'You can only graft unpublished branches.'))

def_cmd(
    name='harvest',
    short=['ha', 'hv', 'har'],
    usage='harvest [<branch>] <into-branch>',
    help=('Auto-Merge/Rebase of specified branch changes into the second '
          'branch.'),
    fn=cmd_harvest)

def_cmd(
    name='help',
    short=['h'],
    fn=cmd_help,
    usage='help <command>',
    help='Display help for legit command.')

def_cmd(
    name='install',
    fn=cmd_install,
    usage='install',
    help='Installs legit git aliases.')

def_cmd(
    name='publish',
    short=['pub'],
    fn=cmd_publish,
    usage='publish <branch>',
    help='Publishes specified branch to the remote.')

def_cmd(
    name='settings',
    fn=cmd_settings,
    usage='settings',
    help='Opens legit settings in a text editor.')

def_cmd(
    name='sprout',
    short=['sp'],
    fn=cmd_sprout,
    usage='sprout [<branch>] <new-branch>',
    help=('Creates a new branch off of the specified branch. Defaults to '
          'current branch. Switches to it immediately.'))

def_cmd(
    name='switch',
    short=['sw'],
    fn=cmd_switch,
    usage='switch <branch>',
    help=('Switches to specified branch. Automatically stashes and unstashes '
          'any changes.'))

def_cmd(
    name='sync',
    short=['sy'],
    fn=cmd_sync,
    usage='sync <branch>',
    help=('Syncronizes the given branch. Defaults to current branch. Stash, '
          'Fetch, Auto-Merge/Rebase, Push, and Unstash.'))
def_cmd(
    name='resync',
    short=['rs'],
    fn=cmd_resync,
    usage='sync <branch>',
    help=('Syncronizes the given branch. Defaults to current branch. Stash, '
          'Fetch, Auto-Merge/Rebase, Push, and Unstash.'))

def_cmd(
    name='unpublish',
    short=['unp'],
    fn=cmd_unpublish,
    usage='unpublish <branch>',
    help='Removes specified branch from the remote.')
