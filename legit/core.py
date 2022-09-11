"""
legit.core
~~~~~~~~~~

This module provides the basic functionality of legit.
"""

# workaround until clint#182 is merged and released
# https://github.com/kennethreitz-archive/clint/pull/182
import sys
if not sys.warnoptions:
    if sys.version_info > (3, 7):
        import warnings
        warnings.simplefilter("ignore", category=SyntaxWarning)

from . import bootstrap
del bootstrap

__version__ = '1.2.1'
__author__ = 'Kenneth Reitz'
__license__ = 'BSD'
