"""Where do kind errors and false questions come from?

    uv run python scripts/diagnose.py runs/v12-all-a/final.pt,runs/v12-all-b/final.pt --part val [--show 8]

Prints, for one side of the hand-labeled split:
  - the oracle: compiler on gold spans vs the hand-written kind (the ceiling)
  - the model: kind confusion (expected -> predicted) and false/missed questions
  - a few examples of each error type
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.compile import compile_questions  # noqa: E402
from gq.data import encode, hand_sample, load_hand  # noqa: E402
from gq.evaluate import model_questions  # noqa: E402
from gq.predict import load  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint")
    ap.add_argument("--part", default="val", choices=["train", "val", "test"])
    ap.add_argument("--show", type=int, default=6)
    args = ap.parse_args()
    records = load_hand(args.part)
    samples = [hand_sample(r) for r in records]

    oracle = collections.Counter()
    for r, s in zip(records, samples):
        if not r["expected"]:
            continue
        tokens, _, labels = encode(s)
        qs = compile_questions(s.text, tokens, labels)
        oracle["n"] += 1
        oracle["ok"] += bool(qs) and qs[-1].kind == r["expected"][-1]["kind"]
    print(f"oracle kind (compiler on gold spans): {oracle['ok']}/{oracle['n']} = {oracle['ok'] / max(1, oracle['n']):.3f}")

    predicted = model_questions(load(args.checkpoint), samples, "cpu")
    confusion = collections.Counter()
    examples = collections.defaultdict(list)
    neg = neg_false = pos = kind_ok = 0
    for r, s, pq in zip(records, samples, predicted):
        tail = s.text[-260:].replace("\n", " ⏎ ")
        if not r["expected"]:
            neg += 1
            if pq:
                neg_false += 1
                examples["false question"].append(f"[{pq[-1]['kind']}] …{tail}")
            continue
        exp = r["expected"][-1]["kind"]
        got = pq[-1]["kind"] if pq else "none"
        if pq:
            pos += 1
            kind_ok += exp == got
        confusion[(exp, got)] += 1
        if exp != got:
            opts = pq[-1]["options"] if pq else []
            examples[f"{exp} -> {got}"].append(f"exp opts={r['expected'][-1]['options']} got opts={opts} …{tail}")
    print(f"model false-question rate: {neg_false}/{neg} = {neg_false / max(1, neg):.3f}")
    print(f"model kind accuracy (when a question is found): {kind_ok}/{pos} = {kind_ok / max(1, pos):.3f}")
    kinds = ["yes_no", "either_or", "multi_choice", "open"]
    print("\nconfusion (rows expected, cols predicted):")
    print(f"{'':14}" + "".join(f"{k:>13}" for k in kinds + ["none"]))
    for e in kinds:
        print(f"{e:14}" + "".join(f"{confusion[(e, g)]:>13}" for g in kinds + ["none"]))
    for key, rows in sorted(examples.items(), key=lambda kv: -len(kv[1])):
        print(f"\n== {key} ({len(rows)})")
        for row in rows[: args.show]:
            print("  -", row[:420])


if __name__ == "__main__":
    main()
