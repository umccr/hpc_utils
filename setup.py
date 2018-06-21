#!/usr/bin/env python
from setuptools import setup

version = '0.3'
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
