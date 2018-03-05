# UMCCR python utilities

🐍 Utilities that makes sense to reuse within UMCCR python-based projects.

### `python_utils/hpc.py`

Default reference data paths for UMCCR clusters. Detects the location by `hostname`. Usage:

```
fasta_path = find_loc().genomes['GRCh37']['fa']
mb_bench_f = find_loc().genomes['GRCh37']['truth_sets']['mb']['vcf']
extras = find_loc().extras
```
