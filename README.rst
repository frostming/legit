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

``sync``
    Syncronizes the current branch.
    Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.

``switch <branch>``
    Switches to specified branch.
    Automatically stashes and unstashes any changes.

``sprout <off-branch> <new-branch>``
    Creates a new branch off of the specified branch.
    Swiches to it immediately.

``graft <branch> <into-branch>``
    Merges specified branch into the second branch, and removes it.
    You can only graft unpublished branches.

``publish <branch>``
    Publishes specified branch to the remote.

``unpublish <branch>``
    Removes specified branch from the remote.

``add`` & ``commit`` are also available, but you should just use ``git`` for those.


The Installation
----------------

**Warning**: don't use this for anything mission critical. It's still new.

Installing Legit is easy with pip::

    $ pip install legit

You'll then have the wonderful ``legit`` command available. Run it within
a repository.

Binaries will be available soon.

