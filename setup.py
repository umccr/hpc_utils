#!/usr/bin/env python
from setuptools import setup
from ngs_utils import setup_utils

name = 'hpc_utils'

version = setup_utils.get_cur_version(name)

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
