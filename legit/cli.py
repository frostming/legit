# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module provides the CLI interface to legit.
"""

import click

from .core import __version__
from .scm import *


pass_repo = click.make_pass_decorator(SCMRepo)


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
    ctx.obj = SCMRepo()
    if ctx.obj:
        ctx.obj.verbose = verbose


@cli.command()
@click.argument('to_branch', required=False)
@pass_repo
def switch(scm, to_branch):
    """Switches from one branch to another, safely stashing and restoring local changes.
    """
    if to_branch is None:
        print('Please specify a branch to switch:')
        scm.display_available_branches()
        raise click.Abort

    if scm.repo.is_dirty():
        status_log(scm.stash_it, 'Saving local changes.')

    status_log(scm.checkout_branch, 'Switching to {0}.'.format(
        colored.yellow(to_branch)), to_branch)

    if scm.unstash_index():
        status_log(scm.repo.unstash_it, 'Restoring local changes.')


@cli.command()
@click.argument('to_branch', required=False)
@pass_repo
def sync(scm, to_branch):
    """Stashes unstaged changes, Fetches remote data, Performs smart
    pull+merge, Pushes local commits up, and Unstashes changes.

    Defaults to current branch.
    """

    scm.repo_check(require_remote=True)

    if to_branch:
        # Optional branch specifier.
        branch = scm.fuzzy_match_branch(to_branch)
        if branch:
            is_external = True
            original_branch = scm.get_current_branch_name()
        else:
            print("{0} doesn't exist. Use a branch that does.".format(
                colored.yellow(branch)))
            sys.exit(1)
    else:
        # Sync current branch.
        branch = scm.get_current_branch_name()
        is_external = False

    if branch in scm.get_branch_names(local=False):

        if is_external:
            switch(scm, branch)

        if scm.repo.is_dirty():
            status_log(scm.stash_it, 'Saving local changes.', sync=True)

        status_log(scm.smart_pull, 'Pulling commits from the server.')
        status_log(scm.push, 'Pushing commits to the server.', branch)

        if scm.unstash_index(sync=True):
            status_log(scm.unstash_it, 'Restoring local changes.', sync=True)

        if is_external:
            switch(scm, original_branch)

    else:
        print('{0} has not been published yet.'.format(
            colored.yellow(branch)))
        sys.exit(1)


@cli.command()
@pass_repo
def branches(scm):
    """Displays available branches."""
    scm.display_available_branches()


# -------
# Helpers
# -------

def status_log(func, message, *args, **kwargs):
    """Executes a callable with a header message."""

    click.echo(message)
    log = func(*args, **kwargs)

    if log:
        out = []

        for line in log.split('\n'):
            if not line.startswith('#'):
                out.append(line)
        click.secho('\n'.join(out), fg="black")
