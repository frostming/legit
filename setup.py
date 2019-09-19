#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from codecs import open  # To use a consistent encoding

from setuptools import setup  # Always prefer setuptools over distutils

APP_NAME = "legit"

with open("legit/core.py") as f:
    VERSION = re.findall(r'^__version__ *= *[\'"](.+?)[\'"]', f.read(), flags=re.M)[0]


# Grab requirements.
with open("reqs.txt") as f:
    required = f.readlines()


settings = dict()


# Publish Helper.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
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
    install_requires=required,
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["legit = legit.cli:cli"]},
)


setup(**settings)
