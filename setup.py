#!/usr/bin/env python
from setuptools import setup
import versionpy

import hpc_utils
pkg = hpc_utils.__name__

version = versionpy.get_version(pkg)

setup(
    name=pkg,
    version=version,
    author='Vlad Saveliev',
    author_email='vladislav.sav@gmail.com',
    description='Cluster utils and paths to the reference data in UMCCR servers',
    keywords='bioinformatics',
    url='https://github.com/umccr/' + pkg,
    license='GPLv3',
    packages=[
        pkg,
    ],
    package_data={
        pkg: versionpy.find_package_files('', pkg),
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=versionpy.get_reqs(),
)
