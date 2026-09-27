"""Dataset-grouped 5-fold cross-validation over the hand-labeled set.

    uv run python -m gq.cv --run cv-v3 --train [-- --hand-rate 0.2 ...]
    uv run python -m gq.cv --run cv-v3 [--show 6]

--train fits one model per fold (gq.train --fold k) into runs/<run>/fold<k>/.
Without --train the existing fold checkpoints are scored, which is enough after a
compiler-only change. Every hand-labeled item is predicted by the one model that
never saw its dataset, and the metrics are pooled over all of them.
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
import time

from .compile import compile_questions
from .data import (HAND2, HAND_SPLIT, ROOT, encode, hand3_paths, hand_sample, load_hand_fold, load_hand_test,
                   load_hand_test4, load_jsonl)
from .evaluate import model_questions, norm, options_match
from .model import Ensemble
from .predict import load

KINDS = ["yes_no", "either_or", "multi_choice", "open"]


def train_folds(run: str, folds: list[int], parallel: int, extra: list[str]):
    out = ROOT / "runs" / run
    out.mkdir(parents=True, exist_ok=True)
    pending, active = list(folds), []
    t0 = time.time()
    while pending or active:
        while pending and len(active) < parallel:
            k = pending.pop(0)
            log = open(out / f"fold{k}.log", "w")
            cmd = [sys.executable, "-m", "gq.train", "--run", f"{run}/fold{k}", "--fold", str(k), "--no-eval", *extra]
            active.append((k, subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT), log))
        time.sleep(5)
        for item in list(active):
            k, proc, log = item
            if proc.poll() is not None:
                log.close()
                active.remove(item)
                status = "ok" if proc.returncode == 0 else f"FAILED ({proc.returncode}), see {out}/fold{k}.log"
                print(f"fold {k}: {status} after {time.time() - t0:.0f}s", flush=True)
                if proc.returncode:
                    raise SystemExit(1)
    (out / "train_args.json").write_text(json.dumps(extra))


def oof_predictions(run: str, folds: list[int], kind_mode: str = "hybrid",
                    rerank_k: int = 8, rerank_lambda: float = 1.0):
    """(record, sample, predicted questions, fold) for every hand-labeled item, out of fold.

    run may list several runs ("a,b,c"); their fold-k models are averaged, which
    stays out of fold because none of them saw fold k.
    """
    rows = []
    for k in folds:
        members = [load(str(ROOT / "runs" / r / f"fold{k}" / "final.pt")) for r in run.split(",")]
        model = members[0] if len(members) == 1 else Ensemble(members).eval()
        records = load_hand_fold(k, "test")
        samples = [hand_sample(r) for r in records]
        for r, s, pq in zip(records, samples,
                            model_questions(model, samples, "cpu", kind_mode,
                                            rerank_k=rerank_k, rerank_lambda=rerank_lambda)):
            rows.append((r, s, pq, k))
    return rows


def metrics(rows) -> dict:
    c = collections.Counter()
    for r, _, pq, _ in rows:
        ex = r["expected"]
        if not ex:
            c["neg"] += 1
            c["false_q"] += bool(pq)
            continue
        c["pos"] += 1
        if not pq:
            continue
        c["found"] += 1
        g, p = ex[-1], pq[-1]
        c["kind_ok"] += g["kind"] == p["kind"]
        c["propose_ok"] += g["propose"] == p["propose"]
        c["count_ok"] += len(ex) == len(pq)
        if g["options"]:
            c["with_options"] += 1
            c["options_exact"] += [norm(o) for o in g["options"]] == [norm(o) for o in p["options"]]
            c["options_ok"] += options_match(g["options"], p["options"])

    def rate(a, b):
        return round(c[a] / c[b], 3) if c[b] else None

    return {"items": len(rows), "false_q": rate("false_q", "neg"), "recall": rate("found", "pos"),
            "kind_acc": rate("kind_ok", "found"), "options_exact": rate("options_exact", "with_options"),
            "options_ok": rate("options_ok", "with_options"),
            "propose_acc": rate("propose_ok", "found"), "count_acc": rate("count_ok", "found"),
            "negatives": c["neg"], "positives": c["pos"]}


def oracle_kind(rows) -> float:
    ok = n = 0
    for r, s, _, _ in rows:
        if r["expected"]:
            tokens, _, labels = encode(s)
            qs = compile_questions(s.text, tokens, labels)
            n += 1
            ok += bool(qs) and qs[-1].kind == r["expected"][-1]["kind"]
    return round(ok / max(1, n), 3)


def report(rows, show: int, label: str = "pooled out-of-fold"):
    print(f"{label}:", json.dumps(metrics(rows)))
    print("oracle kind (compiler on gold spans):", oracle_kind(rows))
    batch2 = {r["id"] for r in load_jsonl(HAND2)} if HAND2.exists() else set()
    batch3 = {r["id"] for p in hand3_paths() for r in load_jsonl(p)}
    for name, keep in (("batch 1", lambda r: r["id"] not in batch2 | batch3), ("batch 2", lambda r: r["id"] in batch2),
                       ("batches 1+2", lambda r: r["id"] not in batch3), ("batch 3", lambda r: r["id"] in batch3)):
        sub = [row for row in rows if keep(row[0])]
        if sub and len(sub) < len(rows):
            print(f"  {name}:", json.dumps(metrics(sub)))
    for k in sorted({row[3] for row in rows}):
        if len({row[3] for row in rows}) > 1:
            print(f"  fold {k}:", json.dumps(metrics([row for row in rows if row[3] == k])))
    confusion = collections.Counter()
    examples = collections.defaultdict(list)
    for r, s, pq, _ in rows:
        tail = s.text[-300:].replace("\n", " ⏎ ")
        ex = r["expected"]
        if not ex:
            if pq:
                examples["false question"].append(f"{r['id']} [{pq[-1]['kind']}] …{tail}")
            continue
        exp, got = ex[-1]["kind"], pq[-1]["kind"] if pq else "none"
        confusion[(exp, got)] += 1
        if exp != got:
            opts = pq[-1]["options"] if pq else []
            examples[f"{exp} -> {got}"].append(
                f"{r['id']} exp={ex[-1]['options']} got={opts} …{tail}")
    print("\nconfusion (rows expected, cols predicted):")
    print(f"{'':14}" + "".join(f"{k:>13}" for k in KINDS + ["none"]))
    for e in KINDS:
        print(f"{e:14}" + "".join(f"{confusion[(e, g)]:>13}" for g in KINDS + ["none"]))
    if show:
        for key, items in sorted(examples.items(), key=lambda kv: -len(kv[1])):
            print(f"\n== {key} ({len(items)})")
            for item in items[:show]:
                print("  -", item[:480])


def main():
    argv = sys.argv[1:]
    extra = argv[argv.index("--") + 1:] if "--" in argv else []
    argv = argv[: argv.index("--")] if "--" in argv else argv
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    ap.add_argument("--holdout", metavar="CHECKPOINT",
                    help="score one checkpoint on the untouched batch-2 test set (milestones only; logged)")
    ap.add_argument("--set", choices=["batch2", "batch4"], default="batch2",
                    help="which untouched test set --holdout scores (batch4: new owners, 218 turns)")
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--parallel", type=int, default=5)
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--kind-mode", choices=["compiler", "head", "hybrid", "rerank"], default="hybrid",
                    help="how a kind head (if the model has one) combines with the compiler")
    ap.add_argument("--rerank-k", type=int, default=8, help="k-best paths for --kind-mode rerank")
    ap.add_argument("--rerank-lambda", type=float, default=1.0,
                    help="weight of log p(kind) added to the CRF path score when reranking")
    ap.add_argument("--json", action="store_true", help="print only the pooled metrics")
    args = ap.parse_args(argv)
    if args.holdout:
        records = load_hand_test() if args.set == "batch2" else load_hand_test4()
        samples = [hand_sample(r) for r in records]
        predicted = model_questions(load(args.holdout), samples, "cpu", args.kind_mode,
                                    rerank_k=args.rerank_k, rerank_lambda=args.rerank_lambda)
        rows = [(r, s, p, 0) for r, s, p in zip(records, samples, predicted)]
        with open(ROOT / "runs" / "holdout_log.jsonl", "a") as log:
            log.write(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "checkpoint": args.holdout,
                                  "set": args.set, "kind_mode": args.kind_mode, **metrics(rows)}) + "\n")
        report(rows, args.show, label=f"{args.set} test (untouched)")
        return
    if not args.run:
        ap.error("--run is required unless --holdout is given")
    folds = sorted(set(json.loads(HAND_SPLIT.read_text())["cv_folds"].values()))
    if args.train:
        train_folds(args.run, folds, args.parallel, extra)
    rows = oof_predictions(args.run, folds, args.kind_mode, args.rerank_k, args.rerank_lambda)
    if args.json:
        print(json.dumps(metrics(rows)))
        return
    report(rows, args.show)


if __name__ == "__main__":
    main()
