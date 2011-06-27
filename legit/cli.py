# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module povides the CLI interface to legit.
"""

import sys

from clint import args
from clint.eng import join as eng_join
from clint.textui import colored, indent, puts, columns

from .core import __version__
from .scm import *


# --------
# Dispatch
# --------

def main():
    """Primary Legit command dispatch."""

    if args.get(0) in cmd_map:

        arg = args.get(0)
        args.remove(arg)

        cmd_map.get(arg).__call__(args)
        sys.exit()

    elif args.contains(('-h', '--help')):
        display_help()
        sys.exit(1)

    elif args.contains(('-v', '--version')):
        display_version()
        sys.exit(1)

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
        print colored.black('\n'.join(out))


# --------
# Commands
# --------

def cmd_switch(args):
    """Legit Switch command."""

    to_branch = args.get(0)

    if not to_branch:
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
    """Legit Sync command."""

    branch = repo.head.ref.name

    if branch in get_branch_names(local=False):

        if repo.is_dirty():
            status_log(stash_it, 'Saving local changes.', sync=True)

        status_log(smart_pull, 'Pulling commits from the server.')

        status_log(push, 'Pushing commits to the server.', branch)

        if unstash_index(sync=True):
            status_log(unstash_it, 'Restoring local changes.', sync=True)
    else:
        print 'This branch has not been published yet.'
        sys.exit(1)


def cmd_sprout(args):
    """Legit Sprout command."""

    off_branch = args.get(0)
    new_branch = args.get(1)

    if not off_branch:
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names()

    if off_branch not in branch_names:
        print "{0} doesn't exist. Use a branch that does.".format(
            colored.yellow(off_branch))
        sys.exit(1)

    if new_branch in branch_names:
        print "{0} already exists. Use a unique name.".format(
            colored.yellow(off_branch))
        sys.exit(1)


    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.')

    status_log(sprout_branch, 'Branching {0} to {1}.'.format(
        colored.yellow(off_branch), colored.yellow(new_branch)),
        off_branch, new_branch)


def cmd_graft(args):

    branch = args.get(0)
    into_branch = args.get(1)

    if not branch:
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names()
    remote_branch_names = get_branch_names(local=False)

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

    switch_args = args.copy
    switch_args._args = [into_branch]

    cmd_switch(switch_args)

    status_log(graft_branch, 'Grafting {0} into {1}.'.format(
        colored.yellow(branch), colored.yellow(into_branch)), branch)


def cmd_publish(args):

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

    branch = args.get(0)

    if not branch:
        display_available_branches()
        sys.exit()

    branch_names = get_branch_names(local=False)

    if branch not in branch_names:
        print "{0} isn't published. Use a branch that is.".format(
            colored.yellow(branch))
        sys.exit(1)

    status_log(unpublish_branch, 'Unpublishing {0}.'.format(
        colored.yellow(branch)), branch)


def cmd_add(args):
    commands = ['git', 'add']
    commands.extend(args._args)

    status_log(repo.git.execute, '', commands)


def cmd_commit(args):
    commands = ['git', 'commit']
    commands.extend(args._args)

    status_log(repo.git.execute, '', commands)


def cmd_branches(args):
    """d"""
    display_available_branches()



# -----
# Views
# -----

def display_available_branches():
    """Displays available branches."""

    branches = get_branches()

    branch_col = len(max([b.name for b in branches], key=len)) + 1

    for branch in branches:

        marker = '*' if (branch.name == repo.head.ref.name) else ' '
        pub = '(published)' if branch.is_published else '(unpublished)'

        print columns(
            [colored.red(marker), 2],
            [colored.yellow(branch.name), branch_col],
            [colored.black(pub), 14]
        )


def display_info():
    """Displays Legit informatics."""

    puts('{0}. {1}\n'.format(
        colored.red('legit'),
        colored.black(u'A Kenneth Reitz Project™')
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



cmd_map = dict(
    switch=cmd_switch,
    sync=cmd_sync,
    sprout=cmd_sprout,
    graft=cmd_graft,
    publish=cmd_publish,
    unpublish=cmd_unpublish,
    add=cmd_add,
    commit=cmd_commit,
    branches=cmd_branches
)