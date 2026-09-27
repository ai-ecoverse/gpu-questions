"""Assemble queue.jsonl + annotations.txt from handcrafted pair records.

Each pair record is a dict with keys:
  n: int (pair number)
  boundary: str
  a, b: side dicts with text, difficulty (e|m|h), note, qs
  qs: list of {kind, propose?, multi?, default?, prompt, opts?}
       or empty list for negative (no question)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent.parent))
from gq.tokenize import clean  # noqa: E402


def side_key(n: int, side: str) -> str:
    return f"pb{n:04d}{side}"


def sanitize_side(side: dict) -> dict:
    """Apply gold clean() so text == clean(raw_tail); drop Q/O spans that vanish."""
    raw = side["text"]
    text = clean(raw)
    # collapse accidental double placeholders from "[CODE]\\n```...```"
    while "[CODE]\n[CODE]" in text:
        text = text.replace("[CODE]\n[CODE]", "[CODE]")
    qs_out = []
    for q in side.get("qs") or []:
        prompt = q["prompt"]
        if prompt not in text:
            # prompt may have lived inside a fence that became [CODE]
            raise ValueError(f"prompt not in cleaned text: {prompt!r}")
        opts = []
        for o in q.get("opts") or []:
            ot = o["text"] if isinstance(o, dict) else o
            if ot not in text:
                raise ValueError(f"option not in cleaned text: {ot!r}")
            if isinstance(o, dict):
                opts.append(o)
            else:
                opts.append(ot)
        qs_out.append({**q, "prompt": prompt, "opts": opts})
    out = dict(side)
    out["text"] = text
    out["raw_tail"] = raw if raw != text else text
    # Prefer storing already-clean raw_tail so raw_tail == text (matches gold habit).
    out["raw_tail"] = text
    out["qs"] = qs_out
    return out


def format_ann_block(key: str, side: dict, pair_n: int, boundary: str, which: str) -> str:
    diff = side["difficulty"]
    amb = " amb" if side.get("amb") else ""
    neg = " neg" if not side.get("qs") else ""
    note = side.get("note") or f"pair pb{pair_n:04d}: {which}"
    lines = [f"== {key} {diff}{amb}{neg} | {note}"]
    for q in side.get("qs") or []:
        flags = [q["kind"]]
        if q.get("propose"):
            flags.append("p")
        if q.get("multi"):
            flags.append("ms")
        if q.get("default") is not None:
            flags.append(f"d={q['default']}")
        lines.append(f"Q {' '.join(flags)} :: {q['prompt']}")
        for o in q.get("opts") or []:
            if isinstance(o, dict):
                lines.append(f"O {o['text']}")
                if o.get("rec"):
                    lines.append(f"R {o['rec']}")
            else:
                lines.append(f"O {o}")
    return "\n".join(lines) + "\n"


def queue_row(n: int, side: str, text: str, boundary: str) -> dict:
    k = side_key(n, side)
    return {
        "k": k,
        "id": f"pairs:{k}",
        "dataset": "synthetic/minimal-pairs",
        "license": "generated",
        "revision": "n/a",
        "session": f"pairs:pb{n:04d}",
        "turn": 0 if side == "a" else 1,
        "agent": "synthetic",
        "raw_tail": text,
        "text": text,
        "boundary": boundary,
    }


def emit(pairs: list[dict], mode: str = "a") -> None:
    """Append (mode='a') or rewrite (mode='w') queue + annotations from pairs."""
    qpath = ROOT / "queue.jsonl"
    apath = ROOT / "annotations.txt"
    with qpath.open(mode, encoding="utf-8") as qf, apath.open(mode, encoding="utf-8") as af:
        if mode == "w":
            af.write(
                "# Generator-B minimal pairs. Format: see scripts/build_gold.py.\n"
                "# Keys pbNNNNa/b. Labels follow gold/CONVENTIONS.md.\n\n"
            )
        for p in pairs:
            n = p["n"]
            boundary = p["boundary"]
            for side_name, which in (("a", p["a"].get("contrast", "a")), ("b", p["b"].get("contrast", "b"))):
                try:
                    side = sanitize_side(p[side_name])
                except ValueError as e:
                    raise ValueError(f"pb{n:04d}{side_name}: {e}") from e
                text = side["text"]
                qf.write(json.dumps(queue_row(n, side_name, text, boundary), ensure_ascii=False) + "\n")
                af.write(format_ann_block(side_key(n, side_name), side, n, boundary, which))
                af.write("\n")


def count_pairs() -> dict[str, int]:
    qpath = ROOT / "queue.jsonl"
    if not qpath.exists():
        return {}
    seen = set()
    bounds: dict[str, int] = {}
    for line in qpath.read_text().splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        sess = o["session"]
        if sess in seen:
            continue
        seen.add(sess)
        b = o.get("boundary", "?")
        bounds[b] = bounds.get(b, 0) + 1
    return bounds
