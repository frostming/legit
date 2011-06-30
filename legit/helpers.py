# -*- coding: utf-8 -*-

"""
legit.helpers
~~~~~~~~~~~~~

Various Python helpers.
"""


import os
import platform

_platform = platform.system().lower()

is_osx = (_platform == 'darwin')
is_win = (_platform == 'windows')
is_lin = (_platform == 'linux')


def find_path_above(*names):
    """Attempt to locate given path by searching parent dirs."""

    path = '.'

    while os.path.split(os.path.abspath(path))[1]:
        for name in names:
            joined = os.path.join(path, name)
            if os.path.exists(joined):
                return os.path.abspath(joined)
        path = os.path.join('..', path)


