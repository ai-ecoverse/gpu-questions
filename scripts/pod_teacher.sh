#!/bin/sh
# Usage: scripts/pod_teacher.sh RUN TARGET...   (TARGET is a fold number or "all")
# Trains the Ettin-150m teacher (8 epochs, silver + pairs) for each target and labels its distillation pool.
cd "$(dirname "$0")/.."
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
run=$1; shift
for t in "$@"; do
    if [ "$t" = all ]; then sel="--all"; else sel="--fold $t"; fi
    .venv/bin/python -m gq.teacher train --run "$run" $sel --model jhu-clsp/ettin-encoder-150m --epochs 8 --batch 16 \
        --silver 'silver/[0-9]*/labeled.jsonl' --pairs 'silver/pairs-*/labeled.jsonl'
    .venv/bin/python -m gq.teacher label --run "$run" $sel
done
