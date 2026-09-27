"""Turn hand annotations (gold/annotations.txt) into gold/handlabeled.jsonl.

The annotation file is written by hand, one block per item:

    == <key> <e|m|h> [amb] [neg] [| note]
    Q <y|e|m|o> [p] [ms] [d=N] :: <exact question text>[ ^N]
    O <exact option text>[ ^N]
    R <exact recommendation marker>[ ^N]

Kinds: y yes_no, e either_or, m multi_choice, o open. `p` marks a proposal
("Want me to…?"), `ms` multi-select, `d=N` the default option index when it is
given in prose. O lines belong to the Q line above them; R lines to the O line
above them, which also makes that option the default. A block with no Q lines is
a negative. Hard negatives say so in the note ("hard: rhetorical", …).

This script only locates the written span texts in `text`; it never decides a
label. Q spans take the last occurrence, options the one nearest their question,
and markers the first one after their option, unless `^N` picks the Nth.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "hf" / "queue.jsonl"
ANN = ROOT / "gold" / "annotations.txt"
OUT = ROOT / "gold" / "handlabeled.jsonl"
KINDS = {"y": "yes_no", "e": "either_or", "m": "multi_choice", "o": "open"}
DIFF = {"e": "easy", "m": "medium", "h": "hard"}
OCC_RE = re.compile(r"^(.*?)\s+\^(\d+)$")


def parse(path: Path) -> list[dict]:
    items, cur = [], None
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        try:
            if line.startswith("== "):
                head, _, note = line[3:].partition("|")
                parts = head.split()
                cur = {"key": parts[0], "difficulty": DIFF[parts[1]], "ambiguous": "amb" in parts[2:],
                       "note": note.strip(), "qs": [], "line": n}
                items.append(cur)
            elif line.startswith("Q "):
                flags, _, text = line[2:].partition(" :: ")
                f = flags.split()
                d = next((int(x[2:]) for x in f if x.startswith("d=")), None)
                cur["qs"].append({"kind": KINDS[f[0]], "propose": "p" in f, "multi": "ms" in f, "default": d,
                                  "text": text, "opts": []})
            elif line.startswith("O "):
                cur["qs"][-1]["opts"].append({"text": line[2:], "rec": None})
            elif line.startswith("R "):
                cur["qs"][-1]["opts"][-1]["rec"] = line[2:]
            else:
                raise ValueError("unknown line type")
        except Exception as e:
            raise SystemExit(f"{path}:{n}: {e}: {line!r}")
    return items


def split_occ(s: str) -> tuple[str, int | None]:
    m = OCC_RE.match(s)
    return (m.group(1), int(m.group(2))) if m else (s, None)


def occurrences(text: str, s: str) -> list[int]:
    out, i = [], text.find(s)
    while i >= 0:
        out.append(i)
        i = text.find(s, i + 1)
    return out


def locate(text: str, raw: str, pick) -> tuple[int, int, str]:
    """`A ~~ B` spans from A through the next B, for spans that cross lines."""
    s, nth = split_occ(raw)
    head, sep, tail = s.partition(" ~~ ")
    occ = occurrences(text, head)
    if not occ:
        raise ValueError(f"span not found: {head!r}")
    start = occ[nth - 1] if nth else pick(occ)
    end = start + len(head)
    if sep:
        j = text.find(tail, end)
        if j < 0:
            raise ValueError(f"span end not found: {tail!r}")
        end = j + len(tail)
    return start, end, text[start:end]


WRAP = {"`": "`", '"': '"', "'": "'", "“": "”"}


def option_label(s: str) -> str:
    s = s.replace("**", "").strip()
    # Unwrap only a quote pair around the whole label; inner code quotes stay.
    if len(s) > 1 and s[0] in WRAP and s.endswith(WRAP[s[0]]) and s.count(s[0]) == (2 if s[0] == WRAP[s[0]] else 1):
        s = s[1:-1].strip()
    return s


def build(item: dict, rec: dict) -> dict:
    text = rec["text"]
    spans, expected = [], []
    for q in item["qs"]:
        qs, qe, qt = locate(text, q["text"], lambda o: o[-1])
        spans.append([qs, qe, "Q", qt])
        options, default = [], q["default"]
        prev = None
        for i, o in enumerate(q["opts"]):
            # First option: inside the question if it occurs there, else nearest to it.
            # Later options: the next occurrence after the previous option.
            def pick(occ, prev=prev):
                if prev is not None:
                    after = [x for x in occ if x >= prev]
                    if after:
                        return after[0]
                inside = [x for x in occ if qs <= x < qe]
                return inside[0] if inside else min(occ, key=lambda x: abs(x - qs))

            os_, oe, ot = locate(text, o["text"], pick)
            prev = oe
            spans.append([os_, oe, "OPT", ot])
            options.append(option_label(ot))
            if o["rec"]:
                rs, re_, rt = locate(text, o["rec"], lambda occ: min((x for x in occ if x >= oe), default=occ[0]))
                spans.append([rs, re_, "REC", rt])
                default = i if default is None else default
        expected.append({"kind": q["kind"], "propose": q["propose"], "prompt": qt, "options": options,
                         "default": default, "multiSelect": q["multi"]})
    spans.sort()
    out = {
        "id": rec["id"], "dataset": rec["dataset"], "license": rec["license"], "revision": rec["revision"],
        "session": rec["session"], "turn": rec["turn"], "agent": rec["agent"],
        "raw_tail": rec["raw_tail"], "text": text, "spans": spans, "expected": expected,
        "difficulty": item["difficulty"], "ambiguous": item["ambiguous"], "note": item["note"],
    }
    if rec.get("seen_dataset"):  # batch 2: unused session from a batch-1 dataset
        out["seen_dataset"] = True
    return out


def main():
    ap = argparse.ArgumentParser(description="Build hand-labeled gold from annotations (defaults: batch 1).")
    ap.add_argument("--queue", type=Path, default=QUEUE)
    ap.add_argument("--ann", type=Path, default=ANN)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    queue = {}
    with open(args.queue) as fh:
        for line in fh:
            r = json.loads(line)
            queue[r["k"]] = r
    items = parse(args.ann)
    out, errors, seen = [], 0, set()
    for item in items:
        if item["key"] in seen:
            print(f"line {item['line']}: duplicate key {item['key']}")
            errors += 1
            continue
        seen.add(item["key"])
        try:
            out.append(build(item, queue[item["key"]]))
        except (ValueError, KeyError) as e:
            print(f"line {item['line']} {item['key']}: {e}")
            errors += 1
    args.out.parent.mkdir(exist_ok=True)
    with open(args.out, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    shown = args.out.resolve().relative_to(ROOT) if args.out.resolve().is_relative_to(ROOT) else args.out
    print(f"{len(out)} items written to {shown}, {errors} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
