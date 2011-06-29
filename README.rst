Legit: Sexy Git CLI, Inspired by GitHub for Mac™.
=================================================


The Concept
-----------

`GitHub for Mac <http://mac.github.com>`_ is not just a Git client.

This `comment <http://www.hackerne.ws/item?id=2684483>`_ on Hacker News
says it best:

    They haven't re-created the git CLI tool in a GUI, they've created something different. They've created a tool that makes Git more accessible. Little things like auto-stashing when you switch branches will confuse git veterans, but it will make Git much easier to grok for newcomers because of the assumptions it makes about your Git workflow.

Why not bring this innovation back to the command line?


The Interface
-------------

``branches``
    Get a nice pretty list of available branches.

``sync [<branch>]``
    Syncronizes the given branch. Defaults to current branch.
    Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.
    You can only sync published branches.

``switch <branch>``
    Switches to specified branch.
    Defaults to current branch.
    Automatically stashes and unstashes any changes.

``sprout [<branch>] <new-branch>``
    Creates a new branch off of the specified branch.
    Swiches to it immediately.

``graft <branch> <into-branch>``
    Merges specified branch into the second branch, and removes it.
    You can only graft unpublished branches.

``publish <branch>``
    Publishes specified branch to the remote.

``unpublish <branch>``
    Removes specified branch from the remote.

``rebase <branch>``
    Rebase onto the specified branch.
    Automatically stashes and unstashes any changes.

``add`` & ``commit`` are also available, but you should just use ``git`` for those.


The Installation
----------------

**Warning**: don't use this for anything mission critical. It's still new.

Installing Legit is easy with pip::

    $ pip install legit

You'll then have the wonderful ``legit`` command available. Run it within
a repository.

Binaries will be available soon.


Caveats
-------

- All remote operations are carried out by the first remote found.
- If a ``stash pop`` merge fails, Legit stops. I'd like to add checking
 for a merge failure, and undo the command with friendly error reporting.
- Pip install is cumbersome to people unfamiliar with Python. Package. (Py2App + PyInstaller)
