import collections
import os
from os.path import join, abspath, dirname, pardir, isfile, exists
import socket
import re
import sys


def critical(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def package_path():
    return dirname(abspath(__file__))


##############################
### HPC dependencies paths ###

def get_hostname():
    return os.environ.get('HOST') or os.environ.get('HOSTNAME') or socket.gethostname()

def find_loc():
    """ Depending on the machine name, return a dict conatining system-dependant paths
        to human reference genomes and extras
    """
    Loc = collections.namedtuple('Loc',
         'name '
         'host_pattern '
         'extras '
         'pcgr_dir '
         'genomes ' 
         'cluster '
         'barcodes_10x '
    )

    hostname = get_hostname()
    loc_by_name = {
        'spartan': Loc(
            name='spartan',
            host_pattern=r'spartan*',
            extras='/data/cephfs/punim0010/extras',
            pcgr_dir='/data/cephfs/punim0010/extras/pcgr',
            cluster={
                'submit_cmd': 'sbatch -p vccc -n {threads} -t 24:00:00 --mem {resources.mem_mb}M -J {job_name} --output {log_file}',
            },
            barcodes_10x='/data/cephfs/punim0010/extras/10x/longranger-2.1.6/longranger-cs/2.1.6/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt',
            genomes={
                'GRCh37': dict(
                    fa='/data/cephfs/punim0010/local/stable/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    bwa='{g}/bwa/GRCh37.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
                    panel_of_normals_dir='/data/cephfs/punim0010/extras/panel_of_normals',
                    gnomad='{g}/variation/gnomad_genome.vcf.gz',
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
                            'vcf': '/data/cephfs/punim0010/data/External/Reference/COLO829_Craig/truth_set/EGAZ00001226241_ListforNatureReports.IndelsandSNVs.final.Suppl1.snpEff.validated.SORTED.vcf.gz'
                        }
                    },
                    ema='/data/cephfs/punim0010/extras/10x/ema_ref/GRCh37',
                ),
                'hg38': dict(
                    fa='/data/cephfs/punim0010/local/stable/bcbio/genomes/Hsapiens/hg38/seq/hg38.fa',
                    bwa='{g}/bwa/hg38.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
                    panel_of_normals_dir='/data/cephfs/punim0010/extras/panel_of_normals/hg38',
                    gnomad='{g}/variation/gnomad_genome.vcf.gz',
                    truth_sets={
                        'dream': {
                            'vcf': '{g}/validation/dream-syn3/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/dream-syn3/truth_regions.bed',
                        },
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        },
                    },
                ),
            },
        ),
        'raijin': Loc(
            name='raijin',
            host_pattern=r'^raijin|(r\d\d\d\d$)',
            extras='/g/data3/gx8/extras',
            pcgr_dir='/g/data3/gx8/extras/umccrise/pcgr',
            cluster={
                'jobscript': join(package_path(), 'jobscript_raijin.sh'),
                'submit_cmd': 'qsub -P gx8 -q normalsp -l wd -N {job_name} -o {log_file} -j oe '
                              '-l walltime=24:00:00,ncpus={threads},wd,mem={resources.mem_mb}M,jobfs={resources.disk_mb}M',
            },
            barcodes_10x='/g/data3/gx8/extras/10x/longranger-2.1.6/longranger-cs/2.1.6/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt',
            genomes={
                'GRCh37': dict(
                    fa='/g/data/gx8/local/development/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    bwa='{g}/bwa/GRCh37.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
                    panel_of_normals_dir='/g/data3/gx8/extras/panel_of_normals',
                    truth_sets={
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        },
                        'colo': {
                            'vcf': '/g/data3/gx8/extras/colo829_truth/EGAZ00001226241_ListforNatureReports.IndelsandSNVs.final.Suppl1.snpEff.validated.SORTED.vcf.gz',
                        }
                    }
                ),
                'hg38': dict(
                    fa='/g/data/gx8/local/development/bcbio/genomes/Hsapiens/hg38/seq/hg38.fa',
                    bwa='{g}/bwa/hg38.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
                    panel_of_normals_dir='/g/data3/gx8/extras/panel_of_normals/hg38',
                    truth_sets={
                        'giab': {
                            'vcf': '{g}/validation/giab-NA12878/truth_small_variants.vcf.gz',
                            'bed': '{g}/validation/giab-NA12878/truth_regions.bed',
                        }
                    }
                ),
            },
        ),
        'vlad': Loc(
            name='vlad',
            host_pattern=r'^5180L-135800-M.local$',
            extras='/Users/vsaveliev/googledrive/bio/extras',
            pcgr_dir='/Users/vsaveliev/git/pcgr',
            cluster={
                'submit_cmd': 'eval',
            },
            barcodes_10x='/Users/vsaveliev/googledrive/bio/reference_data/4M-with-alts-february-2016.txt',
            genomes={
                'GRCh37': dict(
                    fa='/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                    bwa='{g}/bwa/GRCh37.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
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
                'hg38': dict(
                    fa='/Users/vsaveliev/googledrive/bio/reference_data/genomes/Hsapiens/hg38/seq/hg38.fa',
                    gtf='{g}/rnaseq/ref-transcripts.gtf',
                ),
                'test-GRCh37': dict(
                    fa='/Users/vsaveliev/git/umccr/vcf_stuff/tests/data/test-GRCh37.fa',
                    panel_of_normals_dir='/Users/vsaveliev/git/umccr/vcf_stuff/tests/data/panel_of_normals',
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
            pcgr_dir='',
            cluster=None,
            barcodes_10x='',
            genomes={
                'GRCh37': dict(
                    # .fa for goleft depth and VCF normalisation:
                    fa='../../data/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
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
                    panel_of_normals_dir='tests/data/panel_of_normals',
                    truth_sets={
                        'test-mb': {
                            'vcf': 'tests/data/test-benchmark.vcf.gz',
                        }
                    }
                )
            },
        ),
        'umccrise_docker': Loc(
            name='umccrise_docker',
            host_pattern=r'^umccrise_docker$',
            extras='',
            cluster=None,
            barcodes_10x='',
            pcgr_dir='/pcgr',
            genomes={
                'GRCh37': dict(
                    fa='/ref.fa',
                    panel_of_normals_dir='/panel_of_normals',
                    truth_sets={
                        'giab': {
                            'bed': '/truth_regions.bed',
                        },
                    },
                ),
                'hg38': dict(
                    fa='/ref.fa',
                    panel_of_normals_dir='/panel_of_normals',
                    truth_sets={
                        'giab': {
                            'bed': '/truth_regions.bed',
                        },
                    },
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
