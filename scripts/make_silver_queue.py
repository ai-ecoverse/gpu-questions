"""Build labeling queues for LLM silver labels over unlabeled public turns.

    uv run python scripts/make_silver_queue.py [--shards 6] [--per-shard 1300]

Candidates come from the downloaded public datasets (data/hf*, never local traces).
Excluded: test-set owners, datasets that mirror the test set, test sessions and texts,
every hand-labeled id, and duplicate tails. About 70% of each shard ends with a `?`
near the tail (capped per dataset so chat distills do not dominate); the rest are
turns without one. Writes data/silver/queue_<n>.jsonl with keys s<n>_<index>.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.data import HAND_SPLIT, load_hand_dev, load_hand_test, load_jsonl  # noqa: E402

SOURCES = ["data/hf/candidates.jsonl", "data/hf2/candidates.jsonl", "data/hf3a/candidates.jsonl",
           "data/hf3b/candidates.jsonl"]
MIRRORS = {"introvoyz041/my-personal-codex-data"}
CHAT_AGENTS = {"claude-chat", "chat", "chat-assistant", "generic", "coding-assistant", "copilot-chat"}
# A simulated customer-service agent: useful, but not the target distribution.
SMALL_CAP = {"while-ai/tau2-simulated": 100}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", type=int, default=6)
    ap.add_argument("--per-shard", type=int, default=1300)
    ap.add_argument("--question-share", type=float, default=0.7)
    ap.add_argument("--cap-agent", type=int, default=1000, help="max `?` turns per coding-agent dataset")
    ap.add_argument("--cap-chat", type=int, default=150, help="max `?` turns per chat-distill dataset")
    ap.add_argument("--seed", type=int, default=20260925)
    args = ap.parse_args()

    split = json.loads(HAND_SPLIT.read_text())
    test_owners = {d.split("/")[0] for d in split["batch2_test_datasets"]}
    test = load_hand_test()
    test_sessions, test_tails = {r["session"] for r in test}, {r["text"][-300:] for r in test}
    labeled = load_hand_dev() + test
    labeled_ids, labeled_tails = {r["id"] for r in labeled}, {r["text"][-300:] for r in labeled}

    seen, pos, neg = set(), collections.defaultdict(list), collections.defaultdict(list)
    for src in SOURCES:
        path = ROOT / src
        if not path.exists():
            continue
        for r in load_jsonl(path):
            t = r.get("text") or ""
            tail = t[-300:]
            if (not t or r["dataset"].split("/")[0] in test_owners or r["dataset"] in MIRRORS
                    or r["id"] in labeled_ids or r.get("session") in test_sessions or tail in test_tails
                    or tail in labeled_tails or tail in seen):
                continue
            seen.add(tail)
            (pos if "?" in t[-400:] else neg)[r["dataset"]].append(r)

    rng = random.Random(args.seed)
    total = args.shards * args.per_shard
    picked_pos, picked_neg = [], []
    for d, rs in pos.items():
        rng.shuffle(rs)
        cap = args.cap_chat if rs[0].get("agent") in CHAT_AGENTS else args.cap_agent
        picked_pos += rs[: SMALL_CAP.get(d, cap)]
    rng.shuffle(picked_pos)
    picked_pos = picked_pos[: int(total * args.question_share)]
    per_neg = max(1, (total - len(picked_pos)) // max(1, len(neg)) + 1)
    for d, rs in neg.items():
        rng.shuffle(rs)
        picked_neg += rs[: min(per_neg, SMALL_CAP.get(d, per_neg) // 2)]
    rng.shuffle(picked_neg)
    items = picked_pos + picked_neg[: total - len(picked_pos)]
    rng.shuffle(items)

    out = ROOT / "data" / "silver"
    out.mkdir(parents=True, exist_ok=True)
    for n in range(args.shards):
        shard = items[n :: args.shards]
        with open(out / f"queue_{n + 1}.jsonl", "w") as fh:
            for i, r in enumerate(shard):
                rec = {k: v for k, v in r.items() if k != "reply"}
                fh.write(json.dumps({"k": f"s{n + 1}_{i:04d}", **rec}, ensure_ascii=False) + "\n")
        q = sum("?" in r["text"][-400:] for r in shard)
        print(f"shard {n + 1}: {len(shard)} items, {q} with '?', {len({r['dataset'] for r in shard})} datasets")


if __name__ == "__main__":
    main()
