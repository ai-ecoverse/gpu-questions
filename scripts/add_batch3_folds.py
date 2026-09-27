"""Add batch-3 datasets to the cross-validation folds in gold/split.json.

    uv run python scripts/add_batch3_folds.py

Existing assignments never move. A new dataset joins the fold of its Hugging Face
owner when the owner already has one; new owners go, largest first, to the fold
with the fewest labeled turns. Fails if any batch-3 turn comes from a test-set owner
or shares a session or message text with the test set.
Re-running is safe: datasets that already have a fold are left alone.
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.data import HAND_SPLIT, hand3_paths, load_hand_dev, load_hand_test, load_jsonl  # noqa: E402


def owner(dataset: str) -> str:
    return dataset.split("/")[0]


def main():
    split = json.loads(HAND_SPLIT.read_text())
    folds: dict[str, int] = split["cv_folds"]
    test_owners = {owner(d) for d in split["batch2_test_datasets"]}
    batch3 = [r for p in hand3_paths() for r in load_jsonl(p)]
    leaked = sorted({r["dataset"] for r in batch3 if owner(r["dataset"]) in test_owners})
    if leaked:
        sys.exit(f"batch-3 turns from test-set owners: {leaked}")
    # Some datasets are re-uploads of a test-set owner's data under another owner name.
    test = load_hand_test()
    sessions, tails = {r["session"] for r in test}, {r["text"][-300:] for r in test}
    mirrored = sorted({r["dataset"] for r in batch3 if r["session"] in sessions or r["text"][-300:] in tails})
    if mirrored:
        sys.exit(f"batch-3 datasets sharing sessions or text with the test set: {mirrored}")
    ids = collections.Counter(r["id"] for r in load_hand_dev())
    dupes = [i for i, n in ids.items() if n > 1]
    if dupes:
        sys.exit(f"{len(dupes)} ids labeled twice, e.g. {dupes[:5]}")

    owner_fold = {owner(d): k for d, k in folds.items()}
    new = collections.Counter(r["dataset"] for r in batch3 if r["dataset"] not in folds)
    load = collections.Counter(folds[r["dataset"]] for r in load_hand_dev() if r["dataset"] in folds)
    by_owner = collections.defaultdict(list)
    for d in new:
        by_owner[owner(d)].append(d)
    added = {}
    for o in sorted(by_owner, key=lambda o: -sum(new[d] for d in by_owner[o])):
        if o not in owner_fold:
            owner_fold[o] = min(sorted(load), key=lambda k: load[k])
        for d in by_owner[o]:
            added[d] = owner_fold[o]
            load[owner_fold[o]] += new[d]
    if added:
        split.setdefault("cv_folds_before_batch3", dict(folds))
        folds.update(added)
        split["cv_folds"] = dict(sorted(folds.items()))
        HAND_SPLIT.write_text(json.dumps(split, indent=1) + "\n")
    counts = collections.Counter(folds[r["dataset"]] for r in load_hand_dev())
    print(f"added {len(added)} datasets; turns per fold: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
