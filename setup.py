#!/usr/bin/env python
from distutils.core import setup
import os

setup(
    name='duat',
    version='0.1',
    description='A lightweight django UAT feedback tool.',
    long_description=open(os.path.join(os.path.dirname(__file__),'README.md')).read(),
    author='Chris Bailey',
    maintainer="Chris Bailey",
    maintainer_email="chris.p.bailey@gmail.com",
    license="GPL 2.0",
    url='https://github.com/chrispbailey/duat/',
    packages=['duat'],
)
