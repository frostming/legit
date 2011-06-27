Legit: Sexy Git CLI, Inspired by GitHub for Mac™.
=================================================

Note: This is a **work in progress**. It's not ready for use yet.


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

``sprout <off-branch> <new-branch>``
    Creates a new branch off of the specified branch. Swiches to it immediately.

``graft <branch> <into-branch>``
    Merges specified branch into the second branch, and removes it.
    You can only graft unpublished branches.

``publish <branch>``
    Publishes specified branch to the remote.

``unpublish <branch>``
    Removes specified branch from the remote.
    Unlike GfM, this won't remove the local branch. That's messed up.


The Implementation
------------------

- Python + PyGit2 / Dulwich (Dulwich will likely make installation much simpler)
- Install via Static Binaries or Pip
- Likely send unknown commands back to ``git``, or something.


License
-------

BSD. ::

    Copyright (c) 2011, Kenneth Reitz
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the <organization> nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.