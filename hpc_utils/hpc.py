import os
from os.path import join, abspath, dirname, pardir, exists, isdir
import re
import sys
import yaml

from ngs_utils.file_utils import verify_dir, verify_file, adjust_path, verify_obj_by_path
from ngs_utils.utils import hostname, update_dict


def critical(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def info(msg):
    sys.stderr.write(msg + '\n')


def package_path():
    return dirname(abspath(__file__))


""" Depending on the machine name, return a dict conatining system-dependant paths
    to human reference genomes and extras
"""
with open(join(package_path(), 'paths.yml')) as f:
    loc_by_name = yaml.full_load(f)

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
try:
    ncpus_on_node = loc_dict.get('ncpus_on_node', len(os.sched_getaffinity(0)))
except:
    ncpus_on_node = loc_dict.get('ncpus_on_node', os.cpu_count())

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
        path = adjust_path(path)
        if exists(path):
            return adjust_path(path)
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
            gd = find_genomes_dir(genomes_dir)
        path = abspath(join(gd, pardir, path))

    path = adjust_path(path)
    if not exists(path):
        if must_exist:
            critical(f'Error: {path} does not exist for genome "{genome}" at host "{name or hostname}"')

    return path


def get_genomes_dict(genome):
    if genome not in genomes:
        critical(f'Error: genome {genome} not found for host "{name or hostname}". '
                 f'Available: {", ".join(genomes)}')
    return genomes[genome]


def find_genomes_dir(_genomes_dir=None):
    """
    Trying:
    1. genomes_dir (when provided explictily in paths.yaml or with --genomes-dir)
    2. if umccrise installation under umccrise/genomes
    2. at extras/umccrise/genomes
    """
    tried = []
    if _genomes_dir and isdir(_genomes_dir):
        info('Using genomes dir that was provided explicitly (in paths.yaml or with --genomes-dir)')
        return genomes_dir
    tried.append(f'--genomes-dir flag')
    tried.append(f'genomes_dir in hpc_utils/paths.yaml for location {name or hostname}')

    if os.environ.get('UMCCRISE_GENOMES') is not None:
        gd = os.environ.get('UMCCRISE_GENOMES')
        if not isdir(gd):
            critical(f'Directory $UMCCRISE_GENOMES={gd} does not exist or not a dir')
        info('Using genomes dir set by $UMCCRISE_GENOMES env var')
        return gd
    tried.append(f'$UMCCRISE_GENOMES env var')

    try:
        from umccrise import package_path as umccrise_path
    except ImportError:
        tried.append(f'umccrsie package parent folder')
    else:
        from umccrise import package_path as umccrise_path
        gd = abspath(join(umccrise_path(), pardir, 'genomes'))
        gd2 = abspath(join(umccrise_path(), pardir, pardir, 'genomes'))
        gd = gd if isdir(gd) else gd2
        if isdir(gd):
            info(f'Using genomes dir at umccrise package parent folder')
            return gd
        tried.append(f'umccrsie package parent folder ({gd})')

    gd = abspath(join(package_path(), pardir, 'genomes'))
    if isdir(gd):
        info(f'Using genomes dir at hpc_utils package parent folder')
        return gd
    tried.append(f'hpc_utils package parent folder ({gd})')

    if extras and isdir(extras):
        gd = join(extras, 'umccrise', 'genomes')
        if isdir(gd):
            info(f'Using genomes dir at production installation of "umccrise" extras')
            return gd
        tried.append(f'production installation of "umccrise" extras ({gd})')

    critical(f'Cannot find "genomes" folder. Tried: {", ".join(tried)}')


def set_genomes_dir(new_genomes_dir=None):
    global genomes_dir
    if new_genomes_dir:
        # genomes_dir was provided explicitly (in paths.yaml or with --genomes-dir)
        verify_dir(new_genomes_dir, is_critical=True)
        genomes_dir = new_genomes_dir
    else:
        genomes_dir = find_genomes_dir()
    if not genomes_dir:
        critical('Could not detect genomes dir. Please specify one with --genomes-dir or $UMCCRISE_GENOMES')


def secondary_conda_env(env_name='pcgr', is_critical=False):
    py_path = sys.executable  # e.g. /miniconda/envs/umccrise/bin/python
    env_path = dirname(dirname(py_path))  # e.g. /miniconda/envs/umccrise
    env_path = env_path + '_' + env_name  # e.g. /miniconda/envs/umccrise_pcgr
    if not isdir(env_path):
        if is_critical:
            critical(f'Can\'t find environment {env_path}')
        else:
            return None
    return env_path







