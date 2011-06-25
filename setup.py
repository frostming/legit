#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from legit.core import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



if sys.argv[-1] == "publish":
    os.system('python setup.py sdist upload')
    sys.exit()

with open('reqs.txt') as f:
    required = f.readlines()


setup(
    name='legit',
    version=__version__,
    description='Sexy Git CLI, Inspired by GitHub for Mac.',
    long_description=open('README.rst').read(),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/legit',
    packages= ['legit',],
    install_requires=required,
    license='ISC',
    classifiers=(
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        # 'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
    entry_points={
        'console_scripts': [
            'legit = legit.cli:main',
        ],
    }
)
