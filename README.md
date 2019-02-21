# UMCCR HPC paths

[![Build Status](https://travis-ci.org/umccr/hpc_utils.svg?branch=master)](https://travis-ci.org/umccr/hpc_utils)

[![Anaconda-Server Badge](https://anaconda.org/vladsaveliev/hpc_utils/badges/installer/conda.svg)](https://anaconda.org/vladsaveliev/hpc_utils)

🖥️ Cluster standard paths to the reference data in UMCCR servers, and python API to query them

[hpc_paths/paths.yml](hpc_paths/paths.yml) contains default data paths and settings for common UMCCR clusters. 

`from hpc_utils import hpc` is a python API that can detect the machine based on `hostname`. Usage:

```
>>> from hpc_utils import hpc
>>> hpc.name
'spartan'

>>> loc.extras
'/data/cephfs/punim0010/extras'

>>> hpc.get_ref_file(genome='GRCh37', 'fa')
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'

>>> hpc.get_ref_file('GRCh37', 'gnomad')
'/data/cephfs/punim0010/extras/umccrise/genomes/GRCh37/gnomad_genome.r2.1.common_pass_clean.norm.vcf.gz'

>>> hpc.get_ref_file(run.genome_build, ['truth_sets', 'giab', 'bed'])
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'

>>> hpc.get_genomes_dict('GRCh37')['truth_sets']['giab']['bed']
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'

>>> hpc.genomes_dir = '/data/genomes'  # on unknown hosts, you can override genomes dir explicitly
```

Available genomes: 

- `"GRCh37"`
- `"hg38"`

Available keys: see paths.yaml

Installation: `conda install -c vladsaveliev hpc_utils`