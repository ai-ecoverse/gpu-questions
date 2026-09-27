"""Check batch-4 test-set labels against everything the models or labelers have used.

    uv run python scripts/check_batch4.py gold/batch4/<labeler>/handlabeled.jsonl [...]

Fails (exit 1) if any turn comes from an excluded owner, or shares a session or a
normalized message tail with the development data, the batch-2 test set, the silver
labels, or the downloaded candidate pools. That catches re-uploads under a new owner.
Prints only ids and dataset names, never message text.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.data import load_hand_dev, load_hand_test, load_jsonl, load_silver  # noqa: E402

POOLS = ["data/hf/candidates.jsonl", "data/hf2/candidates.jsonl", "data/hf3a/candidates.jsonl",
         "data/hf3b/candidates.jsonl"]


def tail_key(text: str) -> str:
    return re.sub(r"\W+", " ", text[-300:].lower()).strip()[-200:]


def main():
    paths = sys.argv[1:]
    if not paths:
        sys.exit(__doc__)
    owners = set(json.loads((ROOT / "data/batch4/excluded_owners.json").read_text()))
    seen = load_hand_dev() + load_hand_test() + load_silver("silver/[0-9]*/labeled.jsonl")
    for p in POOLS:
        if (ROOT / p).exists():
            seen += [r for r in load_jsonl(ROOT / p) if r.get("text")]
    sessions = {r.get("session") for r in seen}
    tails = {tail_key(r["text"]) for r in seen}
    bad = 0
    for path in paths:
        mine_tails: dict[str, str] = {}
        for r in load_jsonl(Path(path)):
            problems = []
            if r["dataset"].split("/")[0] in owners:
                problems.append("excluded owner")
            if r.get("session") in sessions:
                problems.append("session already used")
            key = tail_key(r["text"])
            if key and key in tails:
                problems.append("text already used")
            if key in mine_tails:
                problems.append(f"duplicate of {mine_tails[key]}")
            mine_tails.setdefault(key, r["id"])
            if problems:
                bad += 1
                print(f"{r['id']}\t{r['dataset']}\t{', '.join(problems)}")
        print(f"{path}: {len(mine_tails)} checked")
    print("OK" if not bad else f"{bad} problem turns")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
