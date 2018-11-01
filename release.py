#!/usr/bin/env python

import sys, glob, os, subprocess

def write_version():
    COMPONENTS = ['MAJOR', 'MINOR', 'BUGFIX']
    arg = 'BUGFIX'
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg not in COMPONENTS and '.' not in arg:
            sys.stderr.write(f'Usage: {__file__} [BUGFIX,MINOR,MAJOR,1.2.1]\n')
            sys.exit(1)

    version_file = glob.glob('*/VERSION.txt') or glob.glob('VERSION.txt')

    if arg in COMPONENTS:
        assert version_file, 'Could not find current version file under VERSION.txt or */VERSION.txt'

        version_file = version_file[0]
        cur_version = open(version_file).read().strip()
        sys.stderr.write(f'Found current version file {version_file}, current version: {cur_version}\n')

        components = cur_version.split('.')
        assert len(components) == 3, f'Version must have 3 components. Read from {version_file}: {cur_version}'

        comp_ind = COMPONENTS.index(arg)
        sys.stderr.write(f'Incrementing {arg} component: "{components[comp_ind]}"\n')
        components[comp_ind] = str(int(components[comp_ind]) + 1)
        new_version = '.'.join(components)

    else:
        if version_file:
            version_file = version_file[0]
        else:
            version_file = 'VERSION.txt'
            sys.stderr.write(f'Could not find current version file under VERSION.txt or */VERSION.txt, creating a new file {version_file}\n')
        new_version = arg

    with open(version_file, 'w') as out:
        out.write(new_version)
    sys.stderr.write(f'New version: {new_version}, written to {version_file}\n')
    return version_file, new_version

def _run(cmd):
    sys.stderr.write(cmd + '\n')
    subprocess.run(cmd, shell=True, check=True)


version_file, new_version = write_version()
_run(f'git add {version_file}')
_run(f'git commit -m "Bump {new_version}"')
_run(f'git tag {new_version}')
_run(f'git push')
_run(f'git push --tags')
