import collections
import os
from os.path import join, abspath, dirname, pardir, isfile, exists
import socket
import re
import sys
import yaml


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

def get_hostname():
    return os.environ.get('HOST') or os.environ.get('HOSTNAME') or socket.gethostname()


def find_loc():
    """ Depending on the machine name, return a dict conatining system-dependant paths
        to human reference genomes and extras
    """
    with open(join(package_path(), pardir, 'paths.yml')) as f:
        loc_by_name = {k: AttrDict(v) for k, v in yaml.load(f).items()}

    hostname = get_hostname()
    loc = None
    if 'TRAVIS' in os.environ.keys():
        loc = loc_by_name['travis']
    else:
        for l in loc_by_name.values():
            if re.match(l.host_pattern, hostname):
                loc = l

    print(f'hpc_utils: hostname: {hostname}, ' + (f'detected host is: {loc.name}' if loc else 'the host is not known.'))
    return loc


def get_loc():
    loc = find_loc()
    if loc:
        return loc
    else:
        critical(f'hpc.py: could not detect location by hostname {get_hostname()}')


def ref_file_exists(path_or_genome, key='fa', loc=None):
    try:
        return get_ref_file(path_or_genome, key, loc)
    except:
        return False


def get_ref_file(path_or_genome, key='fa', loc=None, must_exist=True):
    """ If path does not exist, checks the "genomes" dictionary for the location.
    """
    if exists(path_or_genome):
        return abspath(path_or_genome)

    loc = loc or get_loc()
    g_d = get_genomes_d(path_or_genome, loc)

    path = g_d
    keys = key if not isinstance(key, str) else [key]
    for k in keys:
        path = path.get(k)
        if not path:
            critical(f'hpc.py: {path_or_genome} is not found as file at {os.getcwd()},'
                     f' and no keys {", ".join(keys)} for genome "{path_or_genome}"'
                     f' for host "{loc.name}". Available keys: {", ".join(g_d)}')

    if '{g}' in path:
        fa = g_d['fa']
        g_basedir = abspath(join(dirname(fa), pardir))
        path = path.format(g=g_basedir)
    path = abspath(path)
    if must_exist and not exists(path):
        critical(f'hpc.py: {path} does not exist at host "{loc.name}" for genome "{path_or_genome}"')
    return path


def get_genomes_d(genome, loc=None):
    loc = loc or get_loc()
    if genome not in loc.genomes:
        critical(f'hpc.py: genome {genome} not found for host "{loc.name}". Available: {", ".join(loc.genomes)}')
    return loc.genomes[genome]
