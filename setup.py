#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from codecs import open  # To use a consistent encoding
from shutil import rmtree

from setuptools import setup, Command  # Always prefer setuptools over distutils

APP_NAME = "legit"

with open("legit/core.py") as f:
    VERSION = re.findall(r'^__version__ *= *[\'"](.+?)[\'"]', f.read(), flags=re.M)[0]

settings = dict()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree('dist')
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git tag -a {0} -m "v{0}"'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


if sys.argv[-1] == "build_manpage":
    os.system("rst2man.py README.rst > extra/man/legit.1")
    sys.exit()


# Build Helper.
if sys.argv[-1] == "build":
    os.system("pyinstaller --onefile legit_r")

settings.update(
    name=APP_NAME,
    version=VERSION,
    description="Git for Humans.",
    long_description=open("README.rst").read(),
    author="Kenneth Reitz",
    author_email="me@kennethreitz.com",
    url="https://github.com/frostming/legit",
    packages=["legit"],
    install_requires=[
        'click',
        'clint',
        'crayons',
        'GitPython',
        'six'
    ],
    license="BSD",
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["legit = legit.cli:cli"]},
    cmdclass={"publish": UploadCommand}
)


setup(**settings)
