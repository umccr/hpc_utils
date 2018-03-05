import collections
import os
import socket
import re


##############################
### HPC dependencies paths ###

def find_loc():
    """ Depending on the machine name, return a dict conatining system-dependant paths
        to human reference genomes and extras
    """
    Loc = collections.namedtuple('Loc',
         'name '
         'host_pattern '
         'hsapiens '
         'extras '
         'panel_of_normals_dir '
         'truth_sets ')

    hostname = socket.gethostname()
    loc_by_name = {
        'spartan': Loc(
            name='spartan',
            host_pattern=r'spartan.*\.hpc\.unimelb\.edu\.au',
            hsapiens='/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens',
            extras='/data/cephfs/punim0010/extras',
            panel_of_normals_dir='/data/cephfs/punim0010/extras/panel_of_normals',
            truth_sets={
                'mb': {
                    'GRCh37': {
                        'vcf': '/data/cephfs/punim0010/data/External/Reference/ICGC_MB/MB-benchmark.vcf.gz',
                    }
                },
                'dream': {
                    'GRCh37': {
                        'vcf': 'GRCh37/validation/dream-syn3/truth_small_variants.vcf.gz',
                        'bed': 'GRCh37/validation/dream-syn3/truth_regions.bed',
                    }
                },
                'giab': {
                    'GRCh37': {
                        'vcf': 'GRCh37/validation/giab-NA12878/truth_small_variants.vcf.gz',
                        'bed': 'GRCh37/validation/giab-NA12878/truth_regions.bed',
                    }
                },
                'colo': {
                    'GRCh37': {
                        'vcf': '/data/cephfs/punim0010/data/External/Reference/COLO829_Craig/truth_set/EGAZ00001226241_ListforNatureReports.IndelsandSNVs.final.Suppl1.snpEff.validated.SORTED.vcf'
                    }
                }
            },
        ),
        'raijin': Loc(
            name='raijin',
            host_pattern=r'^raijin|(r\d\d\d\d$)',
            hsapiens='/g/data/gx8/local/development/bcbio/genomes/Hsapiens',
            extras='/g/data3/gx8/extras',
            panel_of_normals_dir='/g/data3/gx8/extras/panel_of_normals',
            truth_sets={
                'giab': {
                    'GRCh37': {
                        'vcf': 'GRCh37/validation/giab-NA12878/truth_small_variants.vcf.gz',
                        'bed': 'GRCh37/validation/giab-NA12878/truth_regions.bed',
                    }
                }
            }
        ),
        'vlad': Loc(
            name='vlad',
            host_pattern=r'^5180L-135800-M.local$',
            hsapiens='/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens',
            extras='/Users/vsaveliev/googledrive/bio/extras',
            panel_of_normals_dir='/Users/vsaveliev/googledrive/bio/extras/panel_of_normals/GRCh37',
            truth_sets={
                'mb': {
                    'GRCh37': {
                        'vcf': '/Users/vsaveliev/googledrive/bio/extras/ICGC_MB/truth_small_variants.vcf.gz',
                    }
                },
                'giab': {
                    'GRCh37': {
                        'vcf': '/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_small_variants.vcf.gz',
                        'bed': '/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed',
                    },
                }
            }
        ),
        'travis': Loc(
            name='travis',
            host_pattern=r'^travis-',
            hsapiens='../../data/genomes/Hsapiens',
            # For tests, using the following in Hsapiens:
            # For germline subsampling: 'GRCh37/coverage/prioritize/cancer/az300.bed.gz'
            # For goleft depth:         'GRCh37/seq/GRCh37.fa
            # For bedtools slop :       'GRCh37/seq/GRCh37.fa.fai'
            extras='',
            panel_of_normals_dir='../../data/panel_of_normals',
            truth_sets={
                'giab': {
                    'GRCh37': {
                        'bed': 'GRCh37/validation/giab-NA12878/truth_regions.bed',
                    }
                },
                'mb': {
                    'GRCh37': {
                        'vcf': '/data/cephfs/punim0010/data/External/Reference/ICGC_MB/MB-benchmark.vcf.gz',
                    }
                }
            }
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
        raise Exception('Could not find loc for hostname ' + socket.gethostname())
