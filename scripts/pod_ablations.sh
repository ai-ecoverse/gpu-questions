#!/bin/sh
# Pod runner: one 5-fold run at a time; each fold peaks near 4 GB of GPU memory on a 24 GB card.
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=3 MKL_NUM_THREADS=3 GQ_CUDA_MEM_FRACTION=0.19 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
scripts/cv_pair.sh cv-S --static runs/static/potion-base-8M-20k-32.pt
scripts/cv_pair.sh cv-Si --silver 'silver/[0-9]*/labeled.jsonl'
scripts/cv_pair.sh cv-P --pairs 'silver/pairs-*/labeled.jsonl'
