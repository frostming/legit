Legit: Sexy Git CLI, Inspired by GitHub for Mac™.
=================================================

Note: This is a **work in progress**.


The Concept
-----------

`GitHub for Mac <http://mac.github.com>`_ is not just a Git client.

This `comment <http://www.hackerne.ws/item?id=2684483>`_ on Hacker News
says it best:

    They haven't re-created the git CLI tool in a GUI, they've created something different. They've created a tool that makes Git more accessible. Little things like auto-stashing when you switch branches will confuse git veterans, but it will make Git much easier to grok for newcomers because of the assumptions it makes about your Git workflow.

Why not bring this innovation back to the command line?


The Interface
-------------

``sync``
    Syncronizes the current branch.

``switch <branch>``
    Switches to specified branch. Automatically Un/Stashes any changes.

``branch <off-branch> <new-branch>``
    Creates a new branch off of the specified branch.

``publish <branch>``
    Publishes specified branch to the remote.

``unpublish <branch>``
    Removes specified branch from the remote. Unlike GfM, this won't
    remove the local branch. That's messed up.


The Implementation
------------------

- Python
- PyGit2 / Dulwich
- Main ``legit`` runner, which will run sub-commands (e.g. ``legit-sync``),
  much like Git.