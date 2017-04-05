#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from distutils.core import Command
from distutils.command.build import build
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding


APP_NAME = 'legit'
APP_SCRIPT = './legit_r'
VERSION = '0.4.1'


# Grab requirements.
with open('reqs.txt') as f:
    required = f.readlines()


settings = dict()


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


class LegitBuildMan(Command):
    description = 'build man from README'
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        if not os.path.exists('extra/man'):
            os.makedirs('extra/man')
        os.system('rst2man.py README.rst > extra/man/legit.1')
class LegitBuild(build):
    """Run additional command with build command"""
    def run(self):
        self.run_command('build_man')
        build.run(self)
cmdclass = dict(
    build_man=LegitBuildMan,
    build=LegitBuild,
)


# Build Helper.
if sys.argv[-1] == 'build':
    import py2exe

    sys.argv.append('py2exe')

    settings.update(
        console=[{'script': APP_SCRIPT}],
        zipfile = None,
        options = {
            'py2exe': {
                'compressed': 1,
                'optimize': 0,
                'bundle_files': 1}})

settings.update(
    name=APP_NAME,
    version=VERSION,
    description='Git for Humans.',
    long_description=open('README.rst').read(),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/legit',
    packages= ['legit',],
    cmdclass=cmdclass,
    install_requires=required,
    license='BSD',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'legit = legit.cli:main',
        ],
    }
)



setup(**settings)
