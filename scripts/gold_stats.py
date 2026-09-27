"""Summarize gold/handlabeled.jsonl: counts per kind, category, difficulty and dataset."""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST_LINE_RE = re.compile(r"^[ \t]*(?:[-*•]|\d{1,2}[.)]|[A-Za-z][.)]|\([A-Za-z0-9]\))[ \t]+")


def categories(r: dict) -> set[str]:
    """Coverage categories used for the targets in the task (an item can be in several)."""
    if not r["expected"]:
        return {"negative_hard" if r["note"].startswith("hard") or "| hard" in r["note"] or r["note"].startswith("hard:")
                else "negative_plain"}
    cats = set()
    text = r["text"]
    line_start = lambda i: text.rfind("\n", 0, i) + 1
    opts = [s for s in r["spans"] if s[2] == "OPT"]
    for q in r["expected"]:
        cats.add({"yes_no": "yes_no", "open": "open"}.get(q["kind"], "choice"))
        if q["default"] is not None:
            cats.add("recommendation")
    if any(LIST_LINE_RE.match(text[line_start(s): s]) for s, *_ in opts):
        cats.add("choice_list")
    elif opts:
        cats.add("choice_inline")
    if len(r["expected"]) > 1:
        cats.add("multi_question")
    return cats


def is_hard_negative(r: dict) -> bool:
    return not r["expected"] and "hard:" in r["note"]


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "gold" / "handlabeled.jsonl"
    rows = [json.loads(line) for line in open(path)]
    pos = [r for r in rows if r["expected"]]
    neg = [r for r in rows if not r["expected"]]
    cat = collections.Counter(c for r in pos for c in categories(r))
    kinds = collections.Counter(q["kind"] for r in pos for q in r["expected"])
    print(f"items {len(rows)}: positives {len(pos)}, negatives {len(neg)} (hard {sum(map(is_hard_negative, neg))})")
    print("questions by kind", dict(kinds), "total", sum(kinds.values()))
    print("positive coverage", dict(cat))
    print("propose", sum(q["propose"] for r in pos for q in r["expected"]),
          "multiSelect", sum(q["multiSelect"] for r in pos for q in r["expected"]),
          "REC spans", sum(1 for r in pos for s in r["spans"] if s[2] == "REC"))
    print("difficulty", dict(collections.Counter(r["difficulty"] for r in rows)))
    print("ambiguous", sum(r["ambiguous"] for r in rows))
    print("agents", dict(collections.Counter(r["agent"] for r in rows)))
    if any(r.get("seen_dataset") for r in rows):  # batch 2 only
        print("seen_dataset", sum(bool(r.get("seen_dataset")) for r in rows),
              "datasets new", len({r["dataset"] for r in rows if not r.get("seen_dataset")}),
              "seen", len({r["dataset"] for r in rows if r.get("seen_dataset")}))
    ds = collections.Counter(r["dataset"] for r in rows)
    for d, n in ds.most_common():
        print(f"  {n:4d} {d}")


if __name__ == "__main__":
    main()
