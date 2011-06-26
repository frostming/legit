# -*- coding: utf-8 -*-

"""
legit.scm
~~~~~~~~~

This module provides the main interface to Git.
"""

import os
from collections import namedtuple
from operator import attrgetter

from git import Repo, Git

from .helpers import find_path_above



repo = Repo('/Users/kreitz/repos/public/legit')
git = Git('/Users/kreitz/repos/public/legit')


Branch = namedtuple('Branch', ['name', 'published'])


def get_repo():
    """Returns the current Repo, based on path."""

    bare_path = find_path_above('.git')

    if bare_path:
        prelapsarian_path = os.path.split(bare_path)[0]
        return Repo(prelapsarian_path)
    else:
        return None


def get_branches():
    """Returns a list of local and remote branches."""

    branches = []

    # Remote refs.
    for b in repo.remotes[0].refs:
        name = '/'.join(b.name.split('/')[1:])

        branches.append(Branch(name, True))

    # Local refs.
    for b in [h.name for h in repo.heads]:

        if b not in [br.name for br in branches]:
            branches.append(Branch(b, False))


    return sorted(branches, key=attrgetter('name'))


def set_branch():
    pass


def fetch():
    pass