#!/bin/sh
# Usage: scripts/pod_static.sh NAME:TABLE[:train] ...
# Runs the v12 recipe (silver + pairs) with each static table, two seeds each, one run at a time.
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=3 MKL_NUM_THREADS=3 GQ_CUDA_MEM_FRACTION=0.19 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
for spec in "$@"; do
    name=${spec%%:*}; rest=${spec#*:}; table=${rest%%:*}
    extra=""; [ "$rest" != "$table" ] && extra="--static-train"
    scripts/cv_pair.sh "$name" --silver 'silver/[0-9]*/labeled.jsonl' --pairs 'silver/pairs-*/labeled.jsonl' \
        --static "runs/static/$table.pt" $extra
done
