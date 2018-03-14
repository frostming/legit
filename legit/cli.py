# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module provides the CLI interface to legit.
"""
import os

import click
from clint import resources
from clint.textui import columns
import crayons

from .core import __version__
from .scm import SCMRepo
from .settings import legit_settings
from .utils import black, format_help, order_manually, output_aliases, status_log, verbose_echo


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
pass_scm = click.make_pass_decorator(SCMRepo)


class LegitGroup(click.Group):
    """Custom Group class with specially sorted command list"""

    command_aliases = {
        'pub': 'publish',
        'sw': 'switch',
        'sy': 'sync',
        'unp': 'unpublish',
        'un': 'undo',
    }

    def list_commands(self, ctx):
        """Override for showing commands in particular order"""
        commands = super(LegitGroup, self).list_commands(ctx)
        return [cmd for cmd in order_manually(commands)]

    def get_command(self, ctx, cmd_name):
        """Override to handle command aliases"""
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        cmd_name = self.command_aliases.get(cmd_name, "")
        return click.Group.get_command(self, ctx, cmd_name)

    def get_help_option(self, ctx):
        """Override for showing formatted main help via --help and -h options"""
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.obj:
                    # legit main help
                    click.echo(format_help(ctx.get_help()))
                else:
                    # legit sub-command help
                    click.echo(ctx.get_help(), color=ctx.color)
                ctx.exit()
        return click.Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help='Show this message and exit.')


@click.group(cls=LegitGroup, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=black('legit', bold=True), version=__version__)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@click.option('--install', is_flag=True, help='Install legit git aliases.')
@click.option('--uninstall', is_flag=True, help='Uninstall legit git aliases.')
@click.option('--config', is_flag=True, help='Edit legit configuration file.')
@click.pass_context
def cli(ctx, verbose, fake, install, uninstall, config):
    """legit command line interface"""
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_scm decorator.
    ctx.obj = SCMRepo()
    ctx.obj.fake = fake
    ctx.obj.verbose = fake or verbose

    if install:
        do_install(ctx, verbose, fake)
        ctx.exit()
    elif uninstall:
        do_uninstall(ctx, verbose, fake)
        ctx.exit()
    elif config:
        do_edit_settings(fake)
        ctx.exit()
    else:
        if ctx.invoked_subcommand is None:
            # Display help to user if no commands were passed.
            click.echo(format_help(ctx.get_help()))


@cli.command(short_help='Switches to specified branch.')
@click.argument('to_branch', required=False)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@pass_scm
def switch(scm, to_branch, verbose, fake):
    """Switches from one branch to another, safely stashing and restoring local changes.
    """
    scm.fake = fake
    scm.verbose = fake or verbose

    scm.repo_check()

    if to_branch is None:
        scm.display_available_branches()
        raise click.BadArgumentUsage('Please specify a branch to switch to')

    scm.stash_log()
    status_log(scm.checkout_branch, 'Switching to {0}.'.format(
        crayons.yellow(to_branch)), to_branch)
    scm.unstash_log()


@cli.command(short_help='Synchronizes the given branch with remote.')
@click.argument('to_branch', required=False)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@pass_scm
@click.pass_context
def sync(ctx, scm, to_branch, verbose, fake):
    """Stashes unstaged changes, Fetches remote data, Performs smart
    pull+merge, Pushes local commits up, and Unstashes changes.

    Defaults to current branch.
    """
    scm.fake = fake
    scm.verbose = fake or verbose

    scm.repo_check(require_remote=True)

    if to_branch:
        # Optional branch specifier.
        branch = scm.fuzzy_match_branch(to_branch)
        if branch:
            is_external = True
            original_branch = scm.get_current_branch_name()
        else:
            raise click.BadArgumentUsage(
                "Branch {0} does not exist. Use an existing branch."
                .format(crayons.yellow(branch)))
    else:
        # Sync current branch.
        branch = scm.get_current_branch_name()
        is_external = False

    if branch in scm.get_branch_names(local=False):
        if is_external:
            ctx.invoke(switch, to_branch=branch, verbose=verbose, fake=fake)
        scm.stash_log(sync=True)
        status_log(scm.smart_pull, 'Pulling commits from the server.')
        status_log(scm.push, 'Pushing commits to the server.', branch)
        scm.unstash_log(sync=True)
        if is_external:
            ctx.invoke(switch, to_branch=original_branch, verbose=verbose, fake=fake)
    else:
        raise click.BadArgumentUsage(
            "Branch {0} is not published. Publish before syncing."
            .format(crayons.yellow(branch)))


@cli.command(short_help='Publishes specified branch to the remote.')
@click.argument('to_branch', required=False)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@pass_scm
def publish(scm, to_branch, verbose, fake):
    """Pushes an unpublished branch to a remote repository."""
    scm.fake = fake
    scm.verbose = fake or verbose

    scm.repo_check(require_remote=True)
    branch = scm.fuzzy_match_branch(to_branch)

    if not branch:
        branch = scm.get_current_branch_name()
        scm.display_available_branches()
        if to_branch is None:
            click.echo("Using current branch {0}".format(crayons.yellow(branch)))
        else:
            click.echo(
                "Branch {0} not found, using current branch {1}"
                .format(crayons.red(to_branch), crayons.yellow(branch)))

    branch_names = scm.get_branch_names(local=False)

    if branch in branch_names:
        raise click.BadArgumentUsage(
            "Branch {0} is already published. Use a branch that is not published."
            .format(crayons.yellow(branch)))

    status_log(scm.publish_branch, 'Publishing {0}.'.format(
        crayons.yellow(branch)), branch)


@cli.command(short_help='Removes specified branch from the remote.')
@click.argument('published_branch', required=False)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@pass_scm
def unpublish(scm, published_branch, verbose, fake):
    """Removes a published branch from the remote repository."""
    scm.fake = fake
    scm.verbose = fake or verbose

    scm.repo_check(require_remote=True)
    branch = scm.fuzzy_match_branch(published_branch)

    if not branch:
        scm.display_available_branches()
        raise click.BadArgumentUsage('Please specify a branch to unpublish')

    branch_names = scm.get_branch_names(local=False)

    if branch not in branch_names:
        raise click.BadArgumentUsage(
            "Branch {0} is not published. Use a branch that is published."
            .format(crayons.yellow(branch)))

    status_log(scm.unpublish_branch, 'Unpublishing {0}.'.format(
        crayons.yellow(branch)), branch)


@cli.command()
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--fake', is_flag=True, help='Show but do not invoke git commands.')
@click.option('--hard', is_flag=True, help='Discard local changes.')
@pass_scm
def undo(scm, verbose, fake, hard):
    """Removes the last commit from history."""
    scm.fake = fake
    scm.verbose = fake or verbose

    scm.repo_check()

    status_log(scm.undo, 'Last commit removed from history.', hard)


@cli.command()
@pass_scm
def branches(scm):
    """Displays a list of branches."""
    scm.repo_check()

    scm.display_available_branches()


def do_install(ctx, verbose, fake):
    """Installs legit git aliases."""
    click.echo('The following git aliases will be installed:\n')
    aliases = cli.list_commands(ctx)
    output_aliases(aliases)

    if click.confirm('\n{}Install aliases above?'.format('FAKE ' if fake else ''), default=fake):
        for alias in aliases:
            cmd = '!legit ' + alias
            system_command = 'git config --global --replace-all alias.{0} "{1}"'.format(alias, cmd)
            verbose_echo(system_command, verbose, fake)
            if not fake:
                os.system(system_command)
        if not fake:
            click.echo("\nAliases installed.")
    else:
        click.echo("\nAliases will not be installed.")


def do_uninstall(ctx, verbose, fake):
    """Uninstalls legit git aliases, including deprecated legit sub-commands."""
    aliases = cli.list_commands(ctx)
    # Add deprecated aliases
    aliases.extend(['graft', 'harvest', 'sprout', 'resync', 'settings', 'install', 'uninstall'])
    for alias in aliases:
        system_command = 'git config --global --unset-all alias.{0}'.format(alias)
        verbose_echo(system_command, verbose, fake)
        if not fake:
            os.system(system_command)
    if not fake:
        click.echo('\nThe following git aliases are uninstalled:\n')
        output_aliases(aliases)


def do_edit_settings(fake):
    """Opens legit settings in editor."""

    path = resources.user.open('config.ini').name

    click.echo('Legit Settings:\n')

    for (option, _, description) in legit_settings.config_defaults:
        click.echo(columns([crayons.yellow(option), 25], [description, None]))
    click.echo("")  # separate settings info from os output

    if fake:
        click.echo(crayons.red('Faked! >>> edit {}'.format(path)))
    else:
        click.edit(path)


def handle_abort(aborted, type=None):
    click.echo('{0} {1}'.format(crayons.red('Error:'), aborted.message))
    click.echo(str(aborted.log))
    if type == 'merge':
        click.echo('Unfortunately, there was a merge conflict.'
                   ' It has to be merged manually.')
    elif type == 'unpublish':
        click.echo(
            '''It seems that the remote branch is deleted.
            If `legit branches` still shows it as published,
            then probably the branch has been deleted at the remote by someone else.
            You can run `git fetch --prune` to update remote information.
            ''')
    raise click.Abort


legit_settings.abort_handler = handle_abort
