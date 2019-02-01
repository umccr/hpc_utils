import os
from os.path import join, abspath, dirname, pardir, isfile, exists, isdir
import re
import sys
import yaml
from ngs_utils.utils import hostname


def critical(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def package_path():
    return dirname(abspath(__file__))


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


##############################
### HPC dependencies paths ###

def find_loc():
    """ Depending on the machine name, return a dict conatining system-dependant paths
        to human reference genomes and extras
    """
    with open(join(package_path(), 'paths.yml')) as f:
        loc_by_name = {k: AttrDict(v) for k, v in yaml.load(f).items()}

    loc = None
    if 'TRAVIS' in os.environ.keys():
        loc = loc_by_name['travis']
    else:
        for l in loc_by_name.values():
            if re.match(l.host_pattern, hostname):
                loc = l
    return loc


def get_loc():
    loc = find_loc()
    if loc:
        return loc
    else:
        critical(f'hpc.py: could not detect location by hostname {hostname}')


def ref_file_exists(genome, key='fa', loc=None, path=None):
    try:
        return get_ref_file(genome, key, loc, path=path)
    except:
        return False


def get_ref_file(genome=None, key='fa', loc=None, path=None, must_exist=True):
    """ If path does not exist, checks the "genomes" dictionary for the location.
    """
    if path:
        if exists(path):
            return abspath(path)
        else:
            critical(f'hpc.py: {path} is not found as file at {os.getcwd()}')

    loc = loc or get_loc()
    g_d = get_genomes_d(genome, loc)

    path = g_d
    keys = key if not isinstance(key, str) else [key]
    for k in keys:
        path = path.get(k)
        if not path:
            critical(f'hpc.py: {genome} is not found as file at {os.getcwd()},'
                     f' and no keys "{", ".join(keys)}" for genome "{genome}"'
                     f' for host "{loc.name}". Available keys: {", ".join(g_d)}')

    if path.startswith('/'):
        fa = g_d['fa']
        g_basedir = abspath(join(dirname(fa), pardir))
        path = path.format(g=g_basedir, extras=loc.extras)
        path = abspath(path)
    elif path.startswith('genomes'):
        path = abspath(join(find_genomes_dir(loc), path))

    if must_exist and not exists(path):
        critical(f'hpc.py: {path} does not exist at host "{loc.name}" for genome "{genome}"')
    return path


def get_genomes_d(genome, loc=None):
    loc = loc or get_loc()
    if genome not in loc.genomes:
        critical(f'hpc.py: genome {genome} not found for host "{loc.name}". Available: {", ".join(loc.genomes)}')
    return loc.genomes[genome]


def find_genomes_dir(loc):
    tried = []

    try:
        from umccrise import package_path as um_path
    except:
        pass
    else:
        gd = abspath(join(um_path(), pardir, 'genomes'))
        if isdir(gd):
            return gd
        tried.append(f'umccrsie package parent folder ({gd}')

    gd = abspath(join(package_path(), pardir, 'genomes'))
    if isdir(gd):
        return gd
    tried.append(f'hpc_utils package parent folder ({gd}')

    if loc is not None:
        gd = join(loc.extras, 'umccrise', 'genomes')
        if isdir(gd):
            return gd
        tried.append(f'extras/umccrise location ({gd})')

    critical('Cannot find "genomes" Folder. Tried: ' + ', '.join(tried))
