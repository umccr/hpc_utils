# UMCCR HPC paths

[![Build Status](https://travis-ci.org/umccr/hpc_utils.svg?branch=master)](https://travis-ci.org/umccr/hpc_utils)

[![Anaconda-Server Badge](https://anaconda.org/vladsaveliev/hpc_utils/badges/installer/conda.svg)](https://anaconda.org/vladsaveliev/hpc_utils)

🖥️ Cluster standard paths to the reference data in UMCCR servers, and python API to query them

[hpc_paths/paths.yml](hpc_paths/paths.yml) contains default data paths and settings for common UMCCR clusters. 

`from hpc_utils import hpc` is a python API that can detect the machine based on `hostname`. Usage:

```
>>> find_loc().name
'spartan'

>>> find_loc().extras
'/data/cephfs/punim0010/extras'

>>> find_loc().genomes['GRCh37']['fa']
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'

>>> fp = get_ref_file('GRCh37')
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'

>>> get_ref_file('GRCh37', 'az300')
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/coverage/prioritize/cancer/az300.bed.gz'

>>> get_ref_file(run.genome_build, ['truth_sets', 'giab', 'bed'])
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'

>>> get_genomes_d('GRCh37')['truth_sets']['giab']['bed']
'/data/cephfs/punim0010/local/development/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'
```

Available genomes: 

- `"GRCh37"`

Available keys:

- `"fa"`: reference genome fasta; appending `".fai"` to the result guarantees existing index file
- `"az300"`
- `"panel_of_normals_dir"`
- `"truth_sets"`: returns a dictionaries of truth set dictionaries, each having `"vcf"` or optional `"bed"` keys:
  - `"giab"`:   GiaB NA12878 (germline variants)
    - `"vcf"`
    - `"bed"`
  - `"dream"`:  DREAM synthetic challenge 3 (somatic T/N)
    - `"vcf"`
    - `"bed"`
  - `"mb"`:     [ICGC medulloblastoma](https://www.nature.com/articles/ncomms10001) (somatic T/N)
    - `"vcf"`
  - `"colo"`:   [COLO829 metastatic melanoma cell line](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4837349) (somatic T/N)
    - `"vcf"`

Installation: `conda install -c vladsaveliev hpc_utils`