"""Hold out part of batch 2 as an untouched test set and recompute CV folds.

    uv run python scripts/make_split2.py

Groups are Hugging Face owners (the part before "/"), so datasets from the same
account never straddle a boundary. Batch-2 owners that also appear in batch 1 stay
on the development side. Writes `batch2_test_datasets` and `cv_folds` (over batch 1
plus the batch-2 development side) into gold/split.json; the batch-1-only folds are
kept as `cv_folds_batch1`.
"""

from __future__ import annotations

import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPLIT = ROOT / "gold" / "split.json"
SEED = 20260924
TEST_SHARE = 0.30
MAX_OWNER_SHARE = 0.25
FOLDS = 5


def load(path):
    return [json.loads(line) for line in open(path)]


def owner(dataset: str) -> str:
    return dataset.split("/")[0]


def main():
    b1 = load(ROOT / "gold" / "handlabeled.jsonl")
    b2 = load(ROOT / "gold" / "batch2" / "handlabeled.jsonl")
    b1_owners = {owner(r["dataset"]) for r in b1}
    size = collections.Counter(owner(r["dataset"]) for r in b2)
    pos = collections.Counter(owner(r["dataset"]) for r in b2 if r["expected"])
    eligible = sorted(o for o in size if o not in b1_owners)
    target = TEST_SHARE * len(b2)
    pos_share = sum(pos.values()) / len(b2)
    rng = random.Random(SEED)
    best = None
    for _ in range(20000):
        order = eligible[:]
        rng.shuffle(order)
        pick, n = [], 0
        for o in order:
            if n >= target:
                break
            pick.append(o)
            n += size[o]
        if max(size[o] for o in pick) > MAX_OWNER_SHARE * n:
            continue
        p = sum(pos[o] for o in pick) / n
        cost = abs(n - target) / target + abs(p - pos_share)
        if best is None or cost < best[0]:
            best = (cost, sorted(pick), n, p)
    _, test_owners, n_test, p_test = best
    test_datasets = sorted({r["dataset"] for r in b2 if owner(r["dataset"]) in test_owners})

    dev = b1 + [r for r in b2 if r["dataset"] not in test_datasets]
    groups = collections.Counter(owner(r["dataset"]) for r in dev)
    best_folds = None
    for _ in range(5000):
        order = list(groups)
        rng.shuffle(order)
        load_ = [0] * FOLDS
        assign = {}
        for o in sorted(order, key=lambda o: -groups[o] * rng.uniform(0.9, 1.1)):
            k = min(range(FOLDS), key=lambda i: load_[i])
            assign[o] = k
            load_[k] += groups[o]
        spread = max(load_) - min(load_)
        if best_folds is None or spread < best_folds[0]:
            best_folds = (spread, assign, load_)
    _, assign, loads = best_folds
    cv = {d: assign[owner(d)] for d in sorted({r["dataset"] for r in dev})}

    split = json.loads(SPLIT.read_text())
    if "cv_folds_batch1" not in split:
        split["cv_folds_batch1"] = split["cv_folds"]
    split["batch2_test_datasets"] = test_datasets
    split["cv_folds"] = cv
    split["cv_note"] = (f"5 folds over batch 1 + batch-2 development side, grouped by HF owner "
                        f"(make_split2.py, seed {SEED}); fold sizes {loads}. batch2_test_datasets is the "
                        f"untouched test set: {n_test} items, {len(test_owners)} owners, "
                        f"{p_test:.1%} with a question. Score it only once per milestone.")
    SPLIT.write_text(json.dumps(split, indent=1) + "\n")
    print(split["cv_note"])
    print("test owners:", ", ".join(f"{o} ({size[o]})" for o in test_owners))


if __name__ == "__main__":
    main()
