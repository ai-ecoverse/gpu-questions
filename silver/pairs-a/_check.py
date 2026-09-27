"""Self-check hand-authored pair modules: Q/O spans must occur in text."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PAIRS


def check_pair(p: dict) -> list[str]:
    errs = []
    for side in ("a", "b"):
        text = p[f"text_{side}"]
        for line in p[f"ann_{side}"]:
            if line.startswith("Q "):
                _, _, q = line[2:].partition(" :: ")
                q = re.sub(r"\s+\^\d+$", "", q)
                # handle ~~ multi-line spans: only check head for presence loosely
                head = q.partition(" ~~ ")[0]
                if head not in text:
                    errs.append(f"pa{p['n']:04d}{side}: Q not in text: {head!r}")
            elif line.startswith("O "):
                o = re.sub(r"\s+\^\d+$", "", line[2:])
                head = o.partition(" ~~ ")[0]
                if head not in text:
                    errs.append(f"pa{p['n']:04d}{side}: O not in text: {head!r}")
        if not text.strip():
            errs.append(f"pa{p['n']:04d}{side}: empty text")
        if text != text.replace("\r\n", "\n"):
            pass
    return errs


def main():
    paths = [Path(p) for p in sys.argv[1:]]
    total = 0
    bad = 0
    for path in paths:
        pairs = load(path)
        print(f"{path.name}: {len(pairs)} pairs")
        total += len(pairs)
        for p in pairs:
            errs = check_pair(p)
            for e in errs:
                print(" ", e)
                bad += 1
    print(f"checked {total} pairs, {bad} span errors")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
