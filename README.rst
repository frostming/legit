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

``switch <branch>``
    Switches to specified branch.
    Defaults to current branch.
    Automatically stashes and unstashes any changes. (alias: ``sw``)

``sync [<branch>]``
    Synchronizes the given branch. Defaults to current branch.
    Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.
    You can only sync published branches. (alias: ``sy``)

``publish [<branch>]``
    Publishes specified branch to the remote. (alias: ``pub``)

``unpublish <branch>``
    Removes specified branch from the remote. (alias: ``unp``)

``undo``
    Un-does the last commit in git history.  (alias: ``un``)

``branches``
    Display a list of available branches.


The Installation
----------------

.. image:: https://img.shields.io/pypi/v/legit.svg
    :target: https://pypi.python.org/pypi/legit/

.. image:: https://img.shields.io/travis/kennethreitz/legit.svg
    :target: https://travis-ci.org/kennethreitz/legit/

.. image:: https://img.shields.io/coveralls/github/kennethreitz/legit.svg
    :target: https://coveralls.io/r/kennethreitz/legit/


From `PyPI <https://pypi.python.org/pypi/legit/>`_ with the Python package manager::

    pip install legit

Or download a standalone Windows executable from `GitHub Releases <https://github.com/kennethreitz/legit/releases>`_.

To install the cutting edge version from the git repository::

    git clone https://github.com/kennethreitz/legit.git
    cd legit
    python setup.py install

Note: if you encountered `Permission denied`,
prepend `sudo` before the `pip` or `python setup.py` command.

You'll then have the wonderful ``legit`` command available. Run it within
a repository.

To view usage and examples, run ``legit`` with no commands or options::

    legit

To install the git aliases, run the following command::

    legit --install

To uninstall the git aliases, run the following command::

    legit --uninstall


Command Options
---------------

All legit commands support ``--verbose`` and ``--fake`` options.

In order to view the git commands invoked by legit, use the ``--verbose`` option::

    legit sync --verbose

If you want to see the git commands used by legit but don't want them invoked, use the ``--fake`` option::

    legit publish --fake


Caveats
-------

- All remote operations are carried out by the remote identified in ``$ git config legit.remote remotename``
- If a ``stash pop`` merge fails, Legit stops. I'd like to add checking for a failed merge, and undo the command with friendly error reporting.
