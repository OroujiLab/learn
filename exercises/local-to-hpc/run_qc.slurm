#!/bin/bash
#SBATCH --job-name=toy-fastq-qc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=256M
#SBATCH --time=00:05:00
#SBATCH --output=qc-%j.out
#SBATCH --error=qc-%j.err
set -euo pipefail
# SITE-SPECIFIC: check account, partition, Python and working directory before use.
python3 exercises/local-to-hpc/fastq_summary.py \
  exercises/local-to-hpc/toy_reads.fastq
