"""Break down out-of-fold kind errors by what went wrong in the predicted spans.

    uv run python scripts/span_errors.py cv-SPSi,cv-SPSi-s2 [--show 5] [--json out.json]

Only CV folds are read, never the test sets. For each question the model found with the
wrong kind, the compiler is first run on the gold spans (the "oracle"). If the oracle is
also wrong, the error is in the compiler rules or the label. Otherwise the predicted spans
are compared with the gold ones and the first difference found names the error type.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.compile import compile_questions  # noqa: E402
from gq.cv import oof_predictions  # noqa: E402
from gq.data import HAND_SPLIT, encode, hand3_paths, load_jsonl  # noqa: E402
from gq.evaluate import norm, options_match  # noqa: E402


def overlap(a: str, b: str) -> bool:
    a, b = norm(a), norm(b)
    return bool(a and b) and (a in b or b in a or len(set(a.split()) & set(b.split())) >= max(2, len(b.split()) // 2))


def classify(r, s, pq) -> str:
    g, p = r["expected"][-1], pq[-1]
    tokens, _, labels = encode(s)
    oracle = compile_questions(s.text, tokens, labels)
    if not oracle or oracle[-1].kind != g["kind"]:
        return "oracle wrong too (compiler rule or label)"
    if not overlap(g["prompt"], p["prompt"]):
        return "different question picked"
    if norm(g["prompt"]) != norm(p["prompt"]):
        prompt_note = " + prompt boundary off"
    else:
        prompt_note = ""
    go, po = g["options"], p["options"]
    if go and not po:
        return "missed options" + prompt_note
    if po and not go:
        return "spurious options" + prompt_note
    if go and po and len(go) != len(po):
        return ("too few options" if len(po) < len(go) else "too many options") + prompt_note
    if go and po and not options_match(go, po):
        return "option boundaries off" + prompt_note
    if prompt_note:
        return "prompt boundary off only"
    return "same spans, different kind"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--json")
    args = ap.parse_args()
    folds = sorted(set(json.loads(HAND_SPLIT.read_text())["cv_folds"].values()))
    rows = oof_predictions(args.run, folds, "compiler")
    batch3 = {r["id"] for p in hand3_paths() for r in load_jsonl(p)}
    cats, by_pair, by_batch, examples = (collections.Counter(), collections.Counter(), collections.Counter(),
                                         collections.defaultdict(list))
    found = 0
    for r, s, pq, _ in rows:
        if not r["expected"] or not pq:
            continue
        found += 1
        g, p = r["expected"][-1], pq[-1]
        if g["kind"] == p["kind"]:
            continue
        c = classify(r, s, pq)
        cats[c] += 1
        by_pair[(c, f"{g['kind']}->{p['kind']}")] += 1
        by_batch[(c, "b3" if r["id"] in batch3 else "b12")] += 1
        examples[c].append({"id": r["id"], "gold": g["kind"], "pred": p["kind"], "gold_prompt": g["prompt"][-160:],
                            "pred_prompt": p["prompt"][-160:], "gold_options": g["options"],
                            "pred_options": p["options"], "amb": r.get("ambiguous")})
    total = sum(cats.values())
    print(f"found questions: {found}, kind errors: {total} ({total / found:.1%})")
    for c, n in cats.most_common():
        pairs = ", ".join(f"{k}:{v}" for (cc, k), v in by_pair.most_common() if cc == c)
        amb = sum(bool(e["amb"]) for e in examples[c])
        print(f"{n:5} {n / total:6.1%}  {c}  [b1+2 {by_batch[(c, 'b12')]}, b3 {by_batch[(c, 'b3')]}, amb {amb}]")
        print(f"        {pairs}")
        for e in examples[c][: args.show]:
            print(f"        - {e['id']} {e['gold']}->{e['pred']} gold={e['gold_options']} pred={e['pred_options']}"
                  f" | {e['gold_prompt']!r} vs {e['pred_prompt']!r}"[:400])
    if args.json:
        Path(args.json).write_text(json.dumps({"counts": dict(cats), "examples": examples}, indent=1))


if __name__ == "__main__":
    main()
