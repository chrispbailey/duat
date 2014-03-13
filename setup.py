#!/usr/bin/env python
from distutils.core import setup
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='duat',
    version='0.2',
    packages=['duat'],
    description='A lightweight django UAT feedback tool.',
    long_description=README,
    author='Chris Bailey',
    author_email="chris.p.bailey@gmail.com",
    maintainer="Chris Bailey",
    maintainer_email="chris.p.bailey@gmail.com",
    license="GPL 2.0",
    url='https://github.com/chrispbailey/duat/',
)
