#!/bin/sh
# Usage: scripts/cv_pair.sh NAME [extra train args...]
# Trains the v11b CV recipe twice (seeds default and 7) with extra args, then scores the ensemble.
set -f
cd "$(dirname "$0")/.."
name=$1; shift
base="--workers 1 --hand-rate 0.35 --hand-augment --hidden 128 --layers 3 --distill runs/teacher32/fold{fold}/distill.jsonl --distill-pos 0.5 --distill-min-conf 0.9"
rm -rf "runs/$name" "runs/$name-s2"
# Seeds run one after another: two concurrent 5-fold runs already use ~25 GB of RAM.
.venv/bin/python -m gq.cv --run "$name" --train --kind-mode compiler -- $base "$@" > "runs/$name.txt" 2>&1
.venv/bin/python -m gq.cv --run "$name-s2" --train --kind-mode compiler -- $base "$@" --seed 7 > "runs/$name-s2.txt" 2>&1
.venv/bin/python -m gq.cv --run "$name,$name-s2" --kind-mode compiler > "runs/$name-ens.txt" 2>&1
