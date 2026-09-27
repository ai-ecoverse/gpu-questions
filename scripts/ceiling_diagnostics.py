"""Is the kind ceiling in the labels or in the model? Two cheap checks on CV folds only.

    uv run python scripts/ceiling_diagnostics.py cv-SPSi,cv-SPSi-s2 [--teacher teacher32] [--k 5]

1. k-best oracle: decode the k best CRF tag paths of the out-of-fold student ensemble, compile
   each, and count how often any of them gives the gold kind. A high value means a reranker
   could recover the errors; a value close to top-1 means the right answer is not in the
   model's beam at all.
2. Error overlap with the out-of-fold teacher: if both make the same mistakes on the same
   items, those items are more likely to be label or convention problems than capacity ones.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gq.compile import compile_questions  # noqa: E402
from gq.data import HAND_SPLIT, encode, hand_sample, load_hand_fold  # noqa: E402
from gq.model import NUM_LABELS, Ensemble, collate  # noqa: E402
from gq.predict import load  # noqa: E402


def kbest(emissions: torch.Tensor, start: torch.Tensor, transition: torch.Tensor, k: int) -> list[list[int]]:
    """k highest-scoring label paths for one sequence (steps x labels), best first."""
    steps = emissions.shape[0]
    # scores[label] = list of (score, path) ending in label
    beams = [[(float(start[j] + emissions[0, j]), [j])] for j in range(NUM_LABELS)]
    for t in range(1, steps):
        new = []
        for j in range(NUM_LABELS):
            cand = [(s + float(transition[i, j] + emissions[t, j]), p) for i in range(NUM_LABELS) for s, p in beams[i]]
            cand.sort(key=lambda x: -x[0])
            new.append([(s, p + [j]) for s, p in cand[:k]])
        beams = new
    final = sorted((c for b in beams for c in b), key=lambda x: -x[0])[:k]
    return [p for _, p in final]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--teacher", default="teacher32")
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()
    folds = sorted(set(json.loads(HAND_SPLIT.read_text())["cv_folds"].values()))
    hit = collections.Counter()
    found = 0
    student_wrong, teacher_wrong, both_found = set(), set(), set()
    teacher_available = (ROOT / "runs" / args.teacher / "fold0" / "teacher.json").exists()
    for fold in folds:
        members = [load(str(ROOT / "runs" / r / f"fold{fold}" / "final.pt")) for r in args.run.split(",")]
        model = (members[0] if len(members) == 1 else Ensemble(members)).eval()
        records = [r for r in load_hand_fold(fold, "test") if r["expected"]]
        samples = [hand_sample(r) for r in records]
        start = model.start.detach().float()
        transition = model.transition.detach().float()
        top1 = {}
        for r, s in zip(records, samples):
            tokens, rows, _ = encode(s)
            if not tokens:
                continue
            with torch.no_grad():
                rows_t, _, mask = collate([(rows, [0] * len(rows))], "cpu")
                em = model.emissions(rows_t, mask)[0].float()
            gold = r["expected"][-1]["kind"]
            kinds = []
            for path in kbest(em, start, transition, args.k):
                qs = compile_questions(s.text, tokens, path)
                kinds.append(qs[-1].kind if qs else None)
            if kinds[0] is None:
                continue
            found += 1
            top1[r["id"]] = kinds[0]
            for n in range(1, args.k + 1):
                hit[n] += gold in kinds[:n]
            if kinds[0] != gold:
                student_wrong.add(r["id"])
        if teacher_available:
            from gq.teacher import Teacher, teacher_questions

            predicted = teacher_questions(Teacher(ROOT / "runs" / args.teacher / f"fold{fold}"), samples)
            for r, pq in zip(records, predicted):
                if pq and r["id"] in top1:
                    both_found.add(r["id"])
                    if pq[-1]["kind"] != r["expected"][-1]["kind"]:
                        teacher_wrong.add(r["id"])
        print(f"fold {fold} done", flush=True)
    print(f"found questions: {found}")
    for n in range(1, args.k + 1):
        print(f"  gold kind within top-{n} paths: {hit[n] / found:.3f}")
    if teacher_available:
        s = student_wrong & both_found
        t = teacher_wrong & both_found
        print(f"items found by both: {len(both_found)}; student wrong {len(s)} ({len(s) / len(both_found):.3f}), "
              f"teacher wrong {len(t)} ({len(t) / len(both_found):.3f}), both wrong {len(s & t)}")
        print(f"  share of student errors the teacher also makes: {len(s & t) / max(1, len(s)):.3f}")
        print(f"  both-right rate if errors were independent: {(1 - len(s) / len(both_found)) * (1 - len(t) / len(both_found)):.3f}"
              f" vs observed {1 - len(s | t) / len(both_found):.3f}")


if __name__ == "__main__":
    main()
