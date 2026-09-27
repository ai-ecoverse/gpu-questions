"""Check gold/handlabeled.jsonl for span slips and compare it with the compiler.

  uv run python scripts/validate_gold.py [path] [--quiet]

Hard errors (exit 1): span out of bounds, span text mismatch, whitespace at a
span edge, overlapping spans, or `text` != clean(raw_tail).
Differences between `expected` and compile_questions() on the gold spans are
printed. Each one is either a labeling slip to fix or a compiler limitation,
which should be kept and mentioned in the item's note.
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.compile import compile_questions  # noqa: E402
from gq.data import Sample, encode  # noqa: E402
from gq.evaluate import norm  # noqa: E402
from gq.tokenize import clean, tail_start, tokenize  # noqa: E402

FIELDS = ("kind", "propose", "options", "default", "multiSelect")


def check_spans(r: dict) -> list[str]:
    errs = []
    text = r["text"]
    if clean(r["raw_tail"]) != text:
        errs.append("text != clean(raw_tail)")
    prev_end = -1
    for start, end, kind, span_text in sorted(r["spans"]):
        if not (0 <= start < end <= len(text)):
            errs.append(f"{kind} [{start},{end}) out of bounds")
            continue
        if text[start:end] != span_text:
            errs.append(f"{kind} [{start},{end}) is {text[start:end]!r}, stored {span_text!r}")
        if span_text != span_text.strip():
            errs.append(f"{kind} {span_text!r} has edge whitespace")
        if kind not in ("Q", "OPT", "REC"):
            errs.append(f"unknown span kind {kind}")
        # OPT and REC sit inside Q spans by design; only same-kind overlap is a slip.
        if kind != "Q" and start < prev_end:
            errs.append(f"{kind} {span_text!r} overlaps the previous option span")
        if kind != "Q":
            prev_end = end
    if bool(r["spans"]) != bool(r["expected"]):
        errs.append("spans and expected disagree on whether this is a negative")
    return errs


def compiled(r: dict):
    sample = Sample(r["text"], [(s, e, k) for s, e, k, _ in r["spans"]])
    tokens, _, labels = encode(sample)
    return compile_questions(r["text"], tokens, labels)


def outside_tail(r: dict) -> bool:
    tokens = tokenize(r["text"])
    cut = tail_start(tokens)
    return bool(cut) and any(s < tokens[cut].start for s, *_ in r["spans"])


def diff(r: dict) -> list[str]:
    got = compiled(r)
    exp = r["expected"]
    out = []
    if len(got) != len(exp):
        out.append(f"question count: expected {len(exp)}, compiler {len(got)}")
    for i, (e, g) in enumerate(zip(exp, got)):
        g = g.to_dict()
        if norm(e["prompt"]) != norm(g["prompt"]):
            out.append(f"q{i} prompt: expected {e['prompt']!r}, compiler {g['prompt']!r}")
        for f in FIELDS:
            ev, gv = e[f], g[f]
            if f == "options":
                ev, gv = [norm(o) for o in ev], [norm(o) for o in gv]
            if ev != gv:
                out.append(f"q{i} {f}: expected {e[f]!r}, compiler {g[f]!r}")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    path = Path(args[0]) if args else ROOT / "gold" / "handlabeled.jsonl"
    rows = [json.loads(line) for line in open(path)]
    hard = 0
    diffs = collections.Counter()
    ids = collections.Counter(r["id"] for r in rows)
    for r in rows:
        errs = check_spans(r)
        if ids[r["id"]] > 1:
            errs.append("duplicate id")
        if outside_tail(r):
            print(f"WARN  {r['id']}: a span lies before the modeled 256-token tail; the model cannot see it")
        for e in errs:
            print(f"ERROR {r['id']}: {e}")
        hard += len(errs)
        if errs:
            continue
        for d in diff(r):
            diffs[d.split(":")[0].split(" ", 1)[-1]] += 1
            if not quiet:
                print(f"DIFF  {r['id']}: {d}  [note: {r['note'] or '-'}]")
    print(f"{len(rows)} items, {hard} errors, {sum(diffs.values())} compiler differences {dict(diffs)}")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
