"""Agreement between the blind relabels and the gold labels (see .bb-prompts/relabel-blind.md).

    uv run python scripts/relabel_agreement.py [--show 10]

Compares the last question's kind ("none" for a negative) for every labeler pair, on the
random sample (an estimate of the label-noise ceiling) and on the items the model gets
wrong (how often gold itself is in doubt there).
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.data import load_hand_dev, load_jsonl  # noqa: E402
from gq.evaluate import options_match  # noqa: E402


def last(r: dict) -> tuple[str, list[str]]:
    return (r["expected"][-1]["kind"], r["expected"][-1]["options"]) if r["expected"] else ("none", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=0)
    args = ap.parse_args()
    mapping = {m["k"]: m for m in json.loads((ROOT / "runs" / "relabel_map.json").read_text())}
    dev = {r["id"]: r for r in load_hand_dev()}
    labels = {"gold": {k: last(dev[m["id"]]) for k, m in mapping.items()}}
    for path in sorted((ROOT / "data" / "relabel").glob("*/labeled.jsonl")):
        labels[path.parent.name] = {r["id"]: last(r) for r in load_jsonl(path)}
    names = list(labels)
    for group in ("random", "hard"):
        keys = [k for k, m in mapping.items() if m["group"] == group]
        print(f"\n{group} ({len(keys)} items)")
        for a, b in itertools.combinations(names, 2):
            both = [k for k in keys if k in labels[a] and k in labels[b]]
            if not both:
                continue
            kind = sum(labels[a][k][0] == labels[b][k][0] for k in both)
            q = [k for k in both if labels[a][k][0] != "none" and labels[b][k][0] != "none"]
            opt = [k for k in q if labels[a][k][1] and labels[b][k][1]]
            opt_ok = sum(options_match(labels[a][k][1], labels[b][k][1]) for k in opt)
            print(f"  {a} vs {b}: kind {kind / len(both):.3f} ({kind}/{len(both)}), "
                  f"question/no question {sum((labels[a][k][0] == 'none') == (labels[b][k][0] == 'none') for k in both) / len(both):.3f}, "
                  f"options_ok {opt_ok / max(1, len(opt)):.3f} ({len(opt)})")
        relabelers = [n for n in names if n != "gold"]
        if len(relabelers) >= 2:
            agree = [k for k in keys if all(k in labels[n] for n in relabelers)
                     and len({labels[n][k][0] for n in relabelers}) == 1]
            against = [k for k in agree if labels[relabelers[0]][k][0] != labels["gold"][k][0]]
            print(f"  relabelers agree on {len(agree)}; gold differs from both on {len(against)}")
            pairs = collections.Counter(f"gold {labels['gold'][k][0]} -> {labels[relabelers[0]][k][0]}" for k in against)
            print("   ", dict(pairs.most_common()))
            for k in against[: args.show]:
                print(f"    {k} {mapping[k]['id']}: gold {labels['gold'][k]} vs {labels[relabelers[0]][k]}")


if __name__ == "__main__":
    main()
