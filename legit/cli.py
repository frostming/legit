# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module povides the CLI interface to legit.
"""

import sys
from subprocess import call
from time import sleep

import clint.resources
from clint import args
from clint.eng import join as eng_join
from clint.textui import colored, puts, columns

from .core import __version__
from .settings import settings
from .helpers import is_lin, is_osx, is_win
from .scm import *


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

    if (args.get(0) in cmd_map) or (args.get(0) in short_map):
        arg = args.get(0)
        args.remove(arg)

        if arg in short_map:
            arg = short_map.get(arg)

        cmd_map.get(arg).__call__(args)
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
                settings.git_transparency = 'git'

            git_args[0] = settings.git_transparency

            sys.exit(call(' '.join(git_args), shell=True))

        else:
            display_info()
            sys.exit(1)


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


# --------
# Commands
# --------

def cmd_switch(args):
    """Legit Switch command."""

    to_branch = args.get(0)

    if not to_branch:
        print 'Please specify a branch to switch to:'
        display_available_branches()
        sys.exit()

    if to_branch not in get_branch_names():
        print 'Branch not found.'
        sys.exit(1)
    else:
        if repo.is_dirty():
            status_log(stash_it, 'Saving local changes.')

        status_log(checkout_branch, 'Switching to {0}.'.format(
            colored.yellow(to_branch)), to_branch)

        if unstash_index():
            status_log(unstash_it, 'Restoring local changes.')


def cmd_sync(args):
    """Stashes unstaged changes, Fetches remote data, Performs smart
    pull+merge, Pushes local commits up, and Unstashes changes.

    Defaults to current branch.
    """

    if args.get(0):
        # Optional branch specifier.
        if args.get(0) in get_branch_names():
            branch = args.get(0)
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

    branch = args.get(0)
    into_branch = args.get(1)

    if not branch:
        print 'Please specify a branch to graft:'
        display_available_branches()
        sys.exit()

    if not into_branch:
        into_branch = repo.head.ref.name

    branch_names = get_branch_names(local=True, remote=False)
    remote_branch_names = get_branch_names(local=False, remote=True)

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

    branch = args.get(0)

    if not branch:
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names(local=False)

    if branch in branch_names:
        print "{0} is already published. Use a branch that isn't.".format(
            colored.yellow(branch))
        sys.exit(1)

    status_log(publish_branch, 'Publishing {0}.'.format(
        colored.yellow(branch)), branch)



def cmd_unpublish(args):
    """Removes a published branch from the remote repository."""

    branch = args.get(0)

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

    from_branch = args.get(0)
    to_branch = args.get(1)

    if not from_branch:
        print 'Please specify a branch to harvest commits from:'
        display_available_branches()
        sys.exit()

    if to_branch:
        original_branch = repo.head.ref.name
        is_external = True
    else:
        is_external = False

    branch_names = get_branch_names(local=True, remote=False)

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

    aliases = {
        'branches': '\'!legit branches\'',
        'graft': '\'!legit graft "$@"\'',
        'harvest': '\'!legit harvest "$@"\'',
        'publish': '\'!legit publish "$@"\'',
        'unpublish': '\'!legit unpublish "$@"\'',
        'sprout': '\'!legit sprout "$@"\'',
        'sync': '\'!legit sync "$@"\'',
        'switch': '\'!legit switch "$@"\'',
    }

    print 'The following git aliases have been installed:\n'

    for (ak, av) in aliases.items():
        os.system('git config --global --replace-all alias.{0} {1}'.format(ak, av))
        print columns(['', 1], [colored.yellow('git ' + ak), 14], [av, None])

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

    help_info = dict()
    help_info['branches'] = 'branches\n\nGet a nice pretty list of ' \
                            'branches.'
    help_info['graft'] = 'graft <branch> <into-branch>\n\nMerges ' \
                         'specified branch into the second branch,' \
                         ' and removes it. You can only graft unpublished ' \
                         'branches.'
    help_info['harvest'] = None
    help_info['help'] = 'help <command>\n\n' \
                        'Display help for legit command.'
    help_info['publish'] = 'publish <branch>\n\n' \
                           'Publishes specified branch to the remote.'
    help_info['unpublish'] = 'unpublish <branch>' \
                             'Removes specified branch from the remote.'
    help_info['settings'] = None
    help_info['sprout'] = 'sprout [<branch>] <new-branch>\n\n' \
                          'Creates a new branch off of the specified branch.' \
                          'Defaults to current branch. Swiches to it immediately.'
    help_info['switch'] = 'switch <branch>\n\n' \
                          'Switches to specified branch. Automatically stashes and unstashes any changes.'

    help_info['sync'] = 'sync [<branch>]\n\n' \
                        'Syncronizes the given branch.' \
                        'Defaults to current branch.' \
                        'Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.'
    help_info['unpublish'] = 'unpublish <branch>\n\n' \
                             'Removes specified branch from the remote.'
    print help_info[command]

def display_available_branches():
    """Displays available branches."""

    branches = get_branches()

    branch_col = len(max([b.name for b in branches], key=len)) + 1

    for branch in branches:

        marker = '*' if (branch.name == repo.head.ref.name) else ' '
        color = colored.green if (branch.name == repo.head.ref.name) else colored.yellow
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
    puts('Commands: {0}.\n'.format(
        eng_join(
            [str(colored.green(c)) for c in sorted(cmd_map.keys())]
        )
    ))


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
    print black(aborted.log)
    print 'Unfortunately, there was a merge conflict. It has to be merged manually.'
    sys.exit(1)


settings.abort_handler = handle_abort


cmd_map = dict(
    switch=cmd_switch,
    sync=cmd_sync,
    sprout=cmd_sprout,
    graft=cmd_graft,
    harvest=cmd_harvest,
    publish=cmd_publish,
    unpublish=cmd_unpublish,
    branches=cmd_branches,
    settings=cmd_settings,
    help=cmd_help,
    install=cmd_install
)

short_map = dict(
    sw='switch',
    sy='sync',
    sp='sprout',
    gr='graft',
    pub='publish',
    unp='unpublish',
    br='branches',
    ha='harvest',
    hv='harvest',
    har='harvest',
    h='help'
)