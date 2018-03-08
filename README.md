# UMCCR python utilities

🐍 Utilities that makes sense to reuse within UMCCR python-based projects.

#### HPC paths 
`/python_utils/hpc.py`

Default reference data paths for UMCCR clusters. Detects location by `hostname`. 

Usage:

```
>>> find_loc().name
'spartan'

>>> find_loc().extras
'/data/cephfs/punim0010/extras'

>>> find_loc().genomes['GRCh37']['fa']
'/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'

>>> fp = get_ref_file('GRCh37')
'/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'

>>> get_ref_file('GRCh37', 'az300')    
'/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/coverage/prioritize/cancer/az300.bed.gz'

>>> get_ref_file(run.genome_build, ['truth_sets', 'giab', 'bed'])
'/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'

>>> get_genomes_d('GRCh37')['truth_sets']['giab']['bed']
'/data/projects/punim0010/local/share/bcbio/genomes/Hsapiens/GRCh37/validation/giab-NA12878/truth_regions.bed'
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
