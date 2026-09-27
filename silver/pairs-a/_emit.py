"""Assemble queue.jsonl + annotations.txt from hand-authored pair records.

Each pair record is a dict:
  n: int (pair number)
  boundary: str
  note_a / note_b: short contrast notes
  text_a / text_b: full message texts
  ann_a / ann_b: list of annotation body lines (Q/O/R), or empty for neg
  diff_a / diff_b: "e"|"m"|"h" (default e)
  flags_a / flags_b: extra == flags like "amb" (optional)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_FENCE_RE = re.compile(r"```.*?(?:```|\Z)", re.S)
_URL_RE = re.compile(r"https?://[^\s)>\]]+")


def clean(text: str) -> str:
    """Match gq.tokenize.clean without importing the package (uv path quirks)."""
    text = _FENCE_RE.sub("[CODE]", text)
    text = _URL_RE.sub("[URL]", text)
    return text.replace("\r\n", "\n").strip()


def emit(pairs: list[dict], mode: str = "a") -> None:
    """mode 'a' append, 'w' overwrite (rebuild from scratch when rebuilding all)."""
    queue_path = ROOT / "queue.jsonl"
    ann_path = ROOT / "annotations.txt"
    qa, aa = [], []
    for p in pairs:
        n = p["n"]
        boundary = p["boundary"]
        session = f"pairs:pa{n:04d}"
        for side, text, note, ann, diff, flags in (
            ("a", p["text_a"], p["note_a"], p["ann_a"], p.get("diff_a", "e"), p.get("flags_a", "")),
            ("b", p["text_b"], p["note_b"], p["ann_b"], p.get("diff_b", "e"), p.get("flags_b", "")),
        ):
            k = f"pa{n:04d}{side}"
            cleaned = clean(text)
            rec = {
                "k": k,
                "id": f"pairs:{k}",
                "dataset": "synthetic/minimal-pairs",
                "license": "generated",
                "revision": "n/a",
                "session": session,
                "turn": 0 if side == "a" else 1,
                "agent": "synthetic",
                "raw_tail": cleaned,
                "text": cleaned,
                "boundary": boundary,
            }
            qa.append(json.dumps(rec, ensure_ascii=False))
            flag_bits = f" {flags}" if flags else ""
            head = f"== {k} {diff}{flag_bits} | pair pa{n:04d}: {note}"
            body = "\n".join(ann) if ann else ""
            aa.append(head + ("\n" + body if body else ""))
    if mode == "w":
        queue_path.write_text("\n".join(qa) + ("\n" if qa else ""))
        header = (
            "# Silver minimal-pairs (generator A). Format: scripts/build_gold.py.\n"
            "# Rules: gold/CONVENTIONS.md. Pair keys share the number (pa0001a/pa0001b).\n\n"
        )
        ann_path.write_text(header + "\n\n".join(aa) + ("\n" if aa else ""))
    else:
        with queue_path.open("a") as fh:
            fh.write("\n".join(qa) + ("\n" if qa else ""))
        with ann_path.open("a") as fh:
            if ann_path.stat().st_size == 0:
                fh.write(
                    "# Silver minimal-pairs (generator A). Format: scripts/build_gold.py.\n"
                    "# Rules: gold/CONVENTIONS.md. Pair keys share the number (pa0001a/pa0001b).\n\n"
                )
            fh.write("\n\n".join(aa) + ("\n\n" if aa else ""))
    print(f"emitted {len(pairs)} pairs ({len(qa)} messages), mode={mode}")


if __name__ == "__main__":
    import importlib.util

    path = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location("pairs_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mode = sys.argv[2] if len(sys.argv) > 2 else "a"
    emit(mod.PAIRS, mode=mode)
