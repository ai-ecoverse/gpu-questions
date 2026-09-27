"""Rebuild queue.jsonl + annotations.txt from all hand-authored batch modules."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from _emit import emit

ROOT = Path(__file__).resolve().parent
BATCHES = [
    "_batch_yn_eo_001_100.py",
    "_batch_yn_eo_101_200.py",
    "_batch_yn_eo_201_300.py",
    "_batch_yn_eo_301_450.py",
    "_batch_eo_mc_451_600.py",
    "_batch_ex_opt_601_700.py",
    "_batch_esc_701_800.py",
]


def load(name: str):
    path = ROOT / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PAIRS


def main():
    pairs = []
    for name in BATCHES:
        chunk = load(name)
        print(f"{name}: {len(chunk)}")
        pairs.extend(chunk)
    ns = [p["n"] for p in pairs]
    assert ns == list(range(1, 801)), f"expected 1..800, got {ns[0]}..{ns[-1]} ({len(ns)}), gaps={sorted(set(range(1,801))-set(ns))[:20]}"
    emit(pairs, mode="w")


if __name__ == "__main__":
    main()
