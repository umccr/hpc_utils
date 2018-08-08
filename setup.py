#!/usr/bin/env python
from setuptools import setup

version = '0.5'
name = 'hpc_utils'

setup(
    name=name,
    version=version,
    author='UMCCR',
    description='Cluster utils and paths to the reference data in UMCCR servers',
    keywords='bioinformatics',
    license='GPLv3',
    packages=[
        name,
    ],
    include_package_data=True,
)
