import collections
import os
from os.path import join, abspath, dirname, pardir, isfile, exists
import socket
import re
import sys


def critical(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


##############################
### HPC dependencies paths ###

def find_loc():
    """ Depending on the machine name, return a dict conatining system-dependant paths
        to human reference genomes and extras
    """
    Loc = collections.namedtuple('Loc',
         'name '
         'host_pattern '
         'extras '
         'genomes '
    )

    hostname = socket.gethostname()
    loc_by_name = {
        'spartan': Loc(
            name='spartan',
            host_pattern=r'spartan.*\.hpc\.unimelb\.edu\.au',
            extras='/data/cephfs/punim0010/extras',
            genomes={
                'GRCh37': dict(
                    fa='/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    az300='{g}/coverage/prioritize/cancer/az300.bed.gz',
                    panel_of_normals_dir='/data/cephfs/punim0010/extras/panel_of_normals',
                    truth_sets={
                        'mb': {
                            'vcf': '/data/cephfs/punim0010/data/External/Reference/ICGC_MB/MB-benchmark.vcf.gz',
                        },
                        'dream': {
                            'vcf': '{g}/validation/dream-syn3/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/dream-syn3/truth_regions.bed',
                        },
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        },
                        'colo': {
                            'vcf': '/data/cephfs/punim0010/data/External/Reference/COLO829_Craig/truth_set/EGAZ00001226241_ListforNatureReports.IndelsandSNVs.final.Suppl1.snpEff.validated.SORTED.vcf'
                        }
                    },
                ),
            },

        ),
        'raijin': Loc(
            name='raijin',
            host_pattern=r'^raijin|(r\d\d\d\d$)',
            genomes={
                'GRCh37': dict(
                    fa='/g/data/gx8/local/development/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    az300='{g}/coverage/prioritize/cancer/az300.bed.gz',
                    panel_of_normals_dir='/g/data3/gx8/extras/panel_of_normals',
                    truth_sets={
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        }
                    }
                ),
            },
            extras='/g/data3/gx8/extras',
        ),
        'vlad': Loc(
            name='vlad',
            host_pattern=r'^5180L-135800-M.local$',
            extras='/Users/vsaveliev/googledrive/bio/extras',
            genomes={
                'GRCh37': dict(
                    fa='/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    az300='{g}/coverage/prioritize/cancer/az300.bed.gz',
                    panel_of_normals_dir='/Users/vsaveliev/googledrive/bio/extras/panel_of_normals/GRCh37',
                    truth_sets={
                        'mb': {
                            'vcf': '/Users/vsaveliev/googledrive/bio/extras/ICGC_MB/truth_small_variants.vcf.gz',
                        },
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        },
                    }
                ),
                'test-GRCh37': dict(
                    fa='/Users/vsaveliev/git/umccr/vcf_stuff/tests/data/test-GRCh37.fa',
                    panel_of_normals_dir='/Users/vsaveliev/googledrive/bio/extras/panel_of_normals/GRCh37',
                    truth_sets={
                        'test-mb': {
                            'vcf': '/Users/vsaveliev/git/umccr/vcf_stuff/tests/data/test-benchmark.vcf.gz',
                        }
                    }
                )
            },
        ),
        'travis': Loc(
            name='travis',
            host_pattern=r'^travis-',
            extras='',
            genomes={
                'GRCh37': dict(
                    # .fa for goleft depth and VCF normalisation:
                    fa='../../data/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    # for germline subsampling:
                    az300='{g}/coverage/prioritize/cancer/az300.bed.gz',
                    panel_of_normals_dir='../../data/panel_of_normals',
                    truth_sets={
                        'giab': {
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        },
                        'test-mb': {
                            'test-GRCh37': {
                                'vcf': '../../data/test-benchmark.vcf.gz',
                            }
                        }
                    },
                ),
                'test-GRCh37': dict(
                    fa='tests/data/test-GRCh37.fa',
                    panel_of_normals_dir='tests/data/panel_of_normals/GRCh37',
                    truth_sets={
                        'test-mb': {
                            'vcf': 'tests/data/test-benchmark.vcf.gz',
                        }
                    }
                )
            },
        ),
    }
    if 'TRAVIS' in os.environ.keys():
        return loc_by_name['travis']
    else:
        for loc in loc_by_name.values():
            if re.match(loc.host_pattern, hostname):
                return loc

    return None


def get_loc():
    loc = find_loc()
    if loc:
        return loc
    else:
        critical(f'Could not detect location by hostname {socket.gethostname()}')


def get_ref_file(path_or_genome, key='fa', loc=None):
    """ If path does not exist, checks the "genomes" dictionary for the location.
    """
    if exists(path_or_genome):
        return path_or_genome

    loc = loc or get_loc()
    g_d = get_genomes_d(path_or_genome, loc)
    path = g_d.get(key)
    if not path:
        critical(f'{path_or_genome} is not found as file at {os.getcwd()}, and no "{key}" for genome "{path_or_genome}"'
                 f' for host "{loc.name}". Available keys: {", ".join(g_d)}')
    if '{g}' in path:
        fa = g_d['fa']
        g_basedir = abspath(join(dirname(fa), pardir))
        path = path.format(g=g_basedir)
    if not exists(path):
        critical(f'{path} at {os.getcwd()} does not exist at host "{loc.name}" for genome "{path_or_genome}"')
    return path


def get_genomes_d(genome, loc=None):
    loc = loc or get_loc()
    if genome not in loc.genomes:
        critical(f'Genome {genome} not found for host "{loc.name}". Available: {", ".join(loc.genomes)}')
    return loc.genomes[genome]
