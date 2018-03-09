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
        click.echo('Please specify a branch to switch:')
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
            click.echo("Branch {0} doesn't exist. Use a branch that does.".format(colored.yellow(branch)))
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
        click.echo('Branch {0} is not published. Publish before syncing.'.format(colored.yellow(branch)))
        sys.exit(1)


@cli.command()
@click.argument('to_branch', required=False)
@pass_repo
def publish(scm, to_branch):
    """Pushes an unpublished branch to a remote repository."""

    scm.repo_check(require_remote=True)
    branch = scm.fuzzy_match_branch(to_branch)

    if not branch:
        branch = scm.get_current_branch_name()
        scm.display_available_branches()
        if to_branch is None:
            click.echo("Using current branch {0}".format(colored.yellow(branch)))
        else:
            click.echo("Branch {0} not found, using current branch {1}".format(colored.red(to_branch), colored.yellow(branch)))

    branch_names = scm.get_branch_names(local=False)

    if branch in branch_names:
        click.echo("Branch {0} is already published. Use a branch that is not published.".format(
            colored.yellow(branch)))
        sys.exit(1)

    status_log(scm.publish_branch, 'Publishing {0}.'.format(
        colored.yellow(branch)), branch)

@cli.command()
@click.argument('published_branch', required=False)
@pass_repo
def cmd_unpublish(scm, published_branch):
    """Removes a published branch from the remote repository."""

    scm.repo_check(require_remote=True)
    branch = scm.fuzzy_match_branch(published_branch)

    if not branch:
        click.echo('Please specify a branch to unpublish:')
        scm.display_available_branches()
        raise click.Abort

    branch_names = scm.get_branch_names(local=False)

    if branch not in branch_names:
        click.echo("Branch {0} isn't published. Use a branch that is published.".format(
            colored.yellow(branch)))
        sys.exit(1)

    status_log(scm.unpublish_branch, 'Unpublishing {0}.'.format(
        colored.yellow(branch)), branch)


@cli.command()
@pass_repo
def branches(scm):
    """Displays available branches."""
    scm.display_available_branches()


@cli.command()
@pass_repo
def undo(scm):
    """Makes last commit not exist."""
    status_log(scm.undo, 'Last commit removed from history.')


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
