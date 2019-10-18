import os
from os.path import join, abspath, dirname, pardir, exists, isdir
import re
import sys
import yaml
from ngs_utils.utils import hostname, update_dict


def critical(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def package_path():
    return dirname(abspath(__file__))


""" Depending on the machine name, return a dict conatining system-dependant paths
    to human reference genomes and extras
"""
with open(join(package_path(), 'paths.yml')) as f:
    loc_by_name = yaml.load(f)  #, Loader=yaml.FullLoader)

loc_dict = loc_by_name['generic']
if 'TRAVIS' in os.environ.keys():
    loc_dict = loc_by_name['travis']
else:
    for ld in loc_by_name.values():
        if 'host_pattern' in ld:
            if re.match(ld['host_pattern'], hostname):
                loc_dict = update_dict(loc_dict, ld)
                break

name = loc_dict.get('name')
genomes_dir = loc_dict.get('genomes_dir')
cluster_cmd = loc_dict.get('cluster_cmd')
cluster_jobscript = loc_dict.get('cluster_jobscript')
threads_on_node = loc_dict.get('threads_on_node', 1)
extras = loc_dict.get('extras')
genomes = loc_dict.get('genomes')


def ref_file_exists(genome='all', key='fa', path=None):
    try:
        return get_ref_file(genome, key, path=path)
    except:
        return False


def get_ref_file(genome='all', key='fa', path=None, must_exist=True):
    """ If path does not exist, checks the "genomes" dictionary for the location.
    """
    if path:
        if exists(path):
            return abspath(path)
        else:
            critical(f'Error: {path} is not found as file at {os.getcwd()}')

    g_d = get_genomes_dict(genome)
    d = g_d
    keys = key if not isinstance(key, str) else [key]
    for k in keys:
        d = d.get(k)
        if not d:
            critical(f'Can\'t find refererence file [{".".join(keys)}] for genome "{genome}"'
                     f' for host "{name or hostname}". Available keys: {", ".join(g_d)}')
    if isinstance(d, str):
        path = d
    else:
        critical(f'Error: path in genomes specified by keys [{".".join(keys)}] is not full.'
                 f'Genome: {genome}, cwd: {os.getcwd()}, host: "{name or hostname}"')

    # Resolve found path:
    if path.startswith('genomes'):
        if genomes_dir:
            if not isdir(genomes_dir):
                if must_exist:
                    critical(f'Could not find the genomes directory {genomes_dir} for host {name or hostname}')
                return None
            gd = genomes_dir
        else:
            gd = find_genomes_dir()
        path = abspath(join(gd, pardir, path))

    if not exists(path):
        if must_exist:
            critical(f'Error: {path} does not exist for genome "{genome}" at at host "{name or hostname}"')
        return None

    return path


def get_genomes_dict(genome):
    if genome not in genomes:
        critical(f'Error: genome {genome} not found for host "{name or hostname}". '
                 f'Available: {", ".join(genomes)}')
    return genomes[genome]


def find_genomes_dir():
    """
    Trying:
    1. genomes_dir (when probided explictily in paths.yaml or with --genomes-dir)
    2. if umccrise installation under umccrise/genomes
    2. at extras/umccrise/genomes
    """
    tried = []
    if genomes_dir and isdir(genomes_dir):
        # if genomes_dir was provided explicitly (in paths.yaml or with --genomes-dir)
        return genomes_dir
    tried.append(f'--genomes-dir flag')
    tried.append(f'genomes_dir in hpc_utils/paths.yaml for location {name or hostname}')

    try:
        from umccrise import package_path as umccrise_path
    except ImportError:
        tried.append(f'umccrsie package parent folder')
    else:
        from umccrise import package_path as umccrise_path
        gd = abspath(join(umccrise_path(), pardir, 'genomes'))
        if isdir(gd):
            return gd
        tried.append(f'umccrsie package parent folder ({gd})')

    gd = abspath(join(package_path(), pardir, 'genomes'))
    if isdir(gd):
        return gd
    tried.append(f'hpc_utils package parent folder ({gd})')

    if extras and isdir(extras):
        gd = join(extras, 'umccrise', 'genomes')
        if isdir(gd):
            return gd
        tried.append(f'production installation of "umccrise" extras ({gd})')

    critical(f'Cannot find "genomes" folder. Tried: {", ".join(tried)}')













