#!/usr/bin/env python
import sys
import os
from os.path import join, isfile, abspath, dirname
from setuptools import setup

version = '0.2'
name = 'python_utils'

setup(
    name=name,
    version=version,
    author='UMCCR',
    description='Utilities that makes sense to reuse within UMCCR python-based projects',
    keywords='bioinformatics',
    license='GPLv3',
    packages=[
        name,
    ],
    include_package_data=True,
)
