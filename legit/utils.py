import click
from clint.textui import colored, columns
import crayons

from .settings import legit_settings


def status_log(func, message, *args, **kwargs):
    """Emits header message, executes a callable, and echoes the return strings."""

    click.echo(message)
    log = func(*args, **kwargs)

    if log:
        out = []

        for line in log.split('\n'):
            if not line.startswith('#'):
                out.append(line)
        click.echo(black('\n'.join(out)))


def verbose_echo(str, verbose=False, fake=False):
    """Selectively output ``str``, with special formatting if ``fake`` is True"""
    verbose = fake or verbose

    if verbose:
        color = crayons.green
        prefix = ''
        if fake:
            color = crayons.red
            prefix = 'Faked!'
        click.echo(color('{} >>> {}'.format(prefix, str)))


def output_aliases(aliases):
    """Display git aliases"""
    for alias in aliases:
        cmd = '!legit ' + alias
        click.echo(columns([colored.yellow('git ' + alias), 20], [cmd, None]))


def order_manually(sub_commands):
    """Order sub-commands for display"""
    order = [
        "switch",
        "sync",
        "publish",
        "unpublish",
        "undo",
        "branches",
    ]
    ordered = []
    commands = dict(zip([cmd for cmd in sub_commands], sub_commands))
    for k in order:
        ordered.append(commands.get(k, ""))
        if k in commands:
            del commands[k]

    # Add commands not present in `order` above
    for k in commands:
        ordered.append(commands[k])

    return ordered


def format_help(help):
    """Format the help string."""
    help = help.replace('Options:', str(black('Options:', bold=True)))

    help = help.replace('Usage: legit', str('Usage: {0}'.format(black('legit', bold=True))))

    help = help.replace('  switch', str(crayons.green('  switch', bold=True)))
    help = help.replace('  sync', str(crayons.green('  sync', bold=True)))
    help = help.replace('  publish', str(crayons.green('  publish', bold=True)))
    help = help.replace('  unpublish', str(crayons.green('  unpublish', bold=True)))
    help = help.replace('  undo', str(crayons.green('  undo', bold=True)))
    help = help.replace('  branches', str(crayons.yellow('  branches', bold=True)))

    additional_help = \
        """Usage Examples:
Switch to specific branch:
$ {0}

Sync current branch with remote:
$ {1}

Sync current code with a specific remote branch:
$ {2}

Publish current branch to remote:
$ {3}

Publish to a specific branch to remote:
$ {4}

Unpublish a specific branch from remote:
$ {5}

Commands:""".format(
            crayons.red('legit switch <branch>'),
            crayons.red('legit sync'),
            crayons.red('legit sync <branch>'),
            crayons.red('legit publish'),
            crayons.red('legit publish <branch>'),
            crayons.red('legit unpublish <branch>'),
        )

    help = help.replace('Commands:', additional_help)

    return help


def black(s, **kwargs):
    if legit_settings.allow_black_foreground:
        return crayons.black(s, **kwargs)
    else:
        return s.encode('utf-8')
