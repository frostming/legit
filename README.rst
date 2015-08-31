.. -*-restructuredtext-*-

Legit: Git for Humans
=====================

Inspired by GitHub for Mac.


The Concept
-----------

`GitHub for Mac <http://mac.github.com>`_ is not just a Git client.

This `comment <https://news.ycombinator.com/item?id=2684483>`_ on Hacker News
says it best:

    They haven't re-created the git CLI tool in a GUI, they've created something different. They've created a tool that makes Git more accessible. Little things like auto-stashing when you switch branches will confuse git veterans, but it will make Git much easier to grok for newcomers because of the assumptions it makes about your Git workflow.

Why not bring this innovation back to the command line?


The Interface
-------------

``branches``
    Get a nice pretty list of available branches.

``sync [<branch>]``
    Synchronizes the given branch. Defaults to current branch.
    Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.
    You can only sync published branches. (alias: ``sy``)

``resync <upstream-branch>``
    Stashes unstaged changes,
    Fetches, Auto-Merge/Rebase upstream data from specified upstream branch,
    Performs smart pull+merge for current branch,
    Pushes local commits up, and Unstashes changes.
    Default upstream branch is 'master'. (alias: ``rs``)

``switch <branch>``
    Switches to specified branch.
    Defaults to current branch.
    Automatically stashes and unstashes any changes. (alias: ``sw``)

``sprout [<branch>] <new-branch>``
    Creates a new branch off of the specified branch.
    Swiches to it immediately. (alias: ``sp``)

``harvest [<branch>] <into-branch>``
    Auto-Merge/Rebase of specified branch changes into the second branch.
    (alias: ``ha``, ``hv``, ``har``)

``graft <branch> <into-branch>``
    Auto-Merge/Rebase of specified branch into the second branch.
    Immediately removes specified branch. You can only graft unpublished branches.
    (alias: ``gr``)

``publish [<branch>]``
    Publishes specified branch to the remote. (alias: ``pub``)

``unpublish <branch>``
    Removes specified branch from the remote. (alias: ``unp``)

``install``
    Installs legit git aliases.

``help``
    Displays help for legit command. (alias: ``h``)


The Installation
----------------

.. image:: https://img.shields.io/pypi/v/legit.svg
    :target: https://pypi.python.org/pypi/legit/

From `PyPI <https://pypi.python.org/pypi/legit/>`_ with the Python package manager::

    pip install legit

Or download a standalone Windows executable from `GitHub Releases <https://github.com/kennethreitz/legit/releases>`_.

You'll then have the wonderful ``legit`` command available. Run it within
a repository.

To install the git aliases, run the following command::

    legit install


Caveats
-------

- All remote operations are carried out by the remote identified in ``$ git config legit.remote remotename``
- If a ``stash pop`` merge fails, Legit stops. I'd like to add checking for a failed merge, and undo the command with friendly error reporting.
