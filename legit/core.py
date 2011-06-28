# -*- coding: utf-8 -*-

"""
legit.core
~~~~~~~~~~

This module provides the basic functionality of legit.
"""

# from clint import resources

import os
import clint.textui.colored


__version__ = '0.0.9'
__author__ = 'Kenneth Reitz'
__license__ = 'BSD'


if 'LEGIT_NO_COLORS' in os.environ:
    clint.textui.colored.DISABLE_COLOR = True

# resources.init('kennethreitz', 'legit')
# resources.user.write('config.ini', "we'll get there.")