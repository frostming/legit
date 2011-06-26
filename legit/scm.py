# -*- coding: utf-8 -*-

"""
legit.scm
~~~~~~~~~

This module provides the main interface to Git.
"""


from collections import namedtuple
from operator import attrgetter


from git import Repo, Git



repo = Repo('/Users/kreitz/repos/public/legit')
git = Git('/Users/kreitz/repos/public/legit')


Branch = namedtuple('Branch', ['name', 'published'])


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