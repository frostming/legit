History
-------

1.0.0
+++++

* Refactor CLI using `click`
* Add --verbose option
* Add --fake option
* Move "install" command to --install option
* Add --uninstall option which unsets legit git aliases
* Move "settings" command to --config option
* Improve help output
* Add tests!
* Update CI configuration
* Update README
* Remove support for deprecated Python versions 2.6, 3.2, 3.3

0.5.0
+++++

* Remove 'rsync' command.
* Fix issues when using legit in repos without remotes.
* Except for the smart merge, `sync` also supports
  'never rebase', 'always rebase', and 'fast-forward only'.
* Fix some compatibility issues with Python 3.5 and Git 2.15.0.
* Refine some error & info messages.

0.4.1
+++++

* Remove commands: 'graft', 'harvest', 'sprout'.

0.3.1
+++++

* Added the new 'undo' command. 
* Refine some exit code.
* Run `legit` without args prints help message.

0.2.1
+++++

* Improve Python 3 support.
* Support special expression for branch.
* Improve completio
* Better help message.
* Add manpage.
* off_branch becomes optional.
* Use correct branch for unstaging in switch command.
* Fetch and abort if unpublishing branch not found.
* Fix remote name config with legit.remote.

0.2.0
+++++

* Particial Python 3 support.
* Add bash and zsh tab-completion.
* Fuzzy branch name matching.
* Default behavior to current branch on the command publish.
* `git config legit.remote <remote name>`
* Fix incorrect stash pop index and stash index with extra data.
* Fix synchronization in git stash.
* Handle failed smart_merge.
* Use correct branch for unstaging in switch command.
* Ensure parseability of git stash list output.
* Set up a tracking branch on publish.
* Handle detached head in legit branches.
* Handle repo with no branches or remotes.
* Fix exceptions of `get_repo`.
* Fixed 'legit install' failed and other issues on Windows
* Handle not git error.
* Use git to find root directory.

0.1.1
+++++

* Fix packaging.
* Update doc.

0.1.0
++++++

* Configuration System (new ``settings`` command)
* New Git Transparency Mode
    * Black Foreground Option
    * Disable Colors Option
* Update Available Alerts (via GitHub)
* New Harvest command
* New Install command


0.0.9 (?)
+++++++++

* Initial Release


