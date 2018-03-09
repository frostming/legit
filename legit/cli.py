# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module provides the CLI interface to legit.
"""

import click
from clint.textui import colored, columns

from .core import __version__
from .scm import *


pass_repo = click.make_pass_decorator(Repo)


@click.group()
@click.option('--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.version_option(__version__)
@click.pass_context
def cli(ctx, verbose):
    """Legit command dispatch"""
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_repo decorator.
    ctx.obj = get_repo()
    if ctx.obj:
        ctx.obj.remote = get_remote(ctx.obj)
        ctx.obj.verbose = verbose


@cli.command()
@click.argument('to_branch')
@pass_repo
def switch(repo, to_branch):
    """Switches from one branch to another, safely stashing/restoring local changes.
    """
    if to_branch is None:
        print('Please specify a branch to switch:')
        display_available_branches(repo)
        raise click.Abort

    if repo.is_dirty():
        status_log(stash_it, 'Saving local changes.', repo)

    status_log(checkout_branch, 'Switching to {0}.'.format(
        colored.yellow(to_branch)), repo, to_branch)

    if unstash_index(repo):
        status_log(unstash_it, 'Restoring local changes.', repo)


# -------
# Helpers
# -------

def status_log(func, message, repo, *args, **kwargs):
    """Executes a callable with a header message."""

    click.echo(message)
    log = func(repo, *args, **kwargs)

    if log:
        out = []

        for line in log.split('\n'):
            if not line.startswith('#'):
                out.append(line)
        click.secho('\n'.join(out), fg="black")


def display_available_branches(repo):
    """Displays available branches."""

    if not repo.remotes:
        remote_branches = False
    else:
        remote_branches = True
    branches = get_branches(repo, local=True, remote_branches=remote_branches)

    if not branches:
        print(colored.red('No branches available'))
        return

    branch_col = len(max([b.name for b in branches], key=len)) + 1

    for branch in branches:

        try:
            branch_is_selected = (branch.name == get_current_branch_name(repo))
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
