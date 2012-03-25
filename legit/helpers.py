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
