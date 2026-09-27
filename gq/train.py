"""Train the question tagger.

    uv run python -m gq.train --run baseline

Each epoch draws fresh synthetic samples (featurized in parallel worker processes).
Runs are written to runs/<name>/ (git-ignored).
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import time
from pathlib import Path

import torch

from .data import (ROOT, Generator, Sample, encode, hand_sample, kind_target, load_hand_dev, load_hand_fold,
                   load_jsonl, load_silver, load_sources)
from .evaluate import eval_sets, hand_sets, score
from .labels import LABEL_ID
from .model import Tagger, collate, collate_kind
from .tokenize import feature_rows, identity_cols, set_feature_version, set_static_vocab

_worker_gen: Generator | None = None


def _init_worker(sources, seed, hand_rate, hard_rate, hand_augment, feature_version, distill_rate, distill_pos,
                 static_vocab):
    global _worker_gen
    set_feature_version(feature_version)
    set_static_vocab(static_vocab)
    _worker_gen = Generator(sources, random.Random(seed), hand_rate=hand_rate, hard_rate=hard_rate,
                            hand_augment=hand_augment, distill_rate=distill_rate, distill_pos=distill_pos)


def _make(seed: int):
    _worker_gen.rng.seed(seed)
    sample = _worker_gen.sample()
    tokens, rows, labels = encode(sample)
    return (rows, labels, *kind_target(sample, tokens, labels))


def draw(pool, count: int, epoch: int, base_seed: int):
    seeds = [base_seed * 1_000_003 + epoch * 1_000_000 + i for i in range(count)]
    data = pool.map(_make, seeds, chunksize=256)
    return [d for d in data if d[0]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="baseline")
    ap.add_argument("--epochs", type=int, default=12)
    ap.add_argument("--samples", type=int, default=40000)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--layers", type=int, default=2)
    ap.add_argument("--seed", type=int, default=20260923)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--identity-dropout", type=float, default=0.3)
    ap.add_argument("--hand-rate", type=float, default=0.2,
                    help="share of samples drawn from the train side of the hand-labeled set")
    ap.add_argument("--hard-rate", type=float, default=0.12,
                    help="share of synthetic samples that are hard negatives ('?' that asks nothing)")
    ap.add_argument("--hand-augment", action="store_true",
                    help="swap option texts and leading context of hand-labeled samples")
    ap.add_argument("--fold", type=int, help="cross-validation fold to hold out (trains on all other hand folds)")
    ap.add_argument("--all-hand", action="store_true",
                    help="train on every hand-labeled item except the batch-2 test set (final model)")
    ap.add_argument("--no-eval", action="store_true", help="skip per-epoch evaluation (faster, used by gq.cv)")
    ap.add_argument("--features", type=int, choices=[1, 2], default=1,
                    help="feature version: 2 adds bigger hash tables, bigrams, and structure features")
    ap.add_argument("--kind-head", action="store_true", help="train a second head that predicts question kind")
    ap.add_argument("--kind-weight", type=float, default=0.5)
    ap.add_argument("--distill", help="jsonl of teacher-labeled samples (text, spans); {fold} is substituted")
    ap.add_argument("--distill-rate", type=float, default=0.3, help="share of samples drawn from --distill")
    ap.add_argument("--silver", help="glob of LLM silver labels to add to the hand pool, e.g. 'silver/[0-9]*/labeled.jsonl'")
    ap.add_argument("--pairs", help="glob of minimal-pair labels to add to the hand pool, e.g. 'silver/pairs-*/labeled.jsonl'")
    ap.add_argument("--static", help="static word vectors ({vocab, vectors}) from scripts/build_static.py")
    ap.add_argument("--static-train", action="store_true",
                    help="fine-tune the static table (at a tenth of --lr) instead of keeping it frozen")
    ap.add_argument("--attn", type=int, default=0,
                    help="heads of the self-attention block(s) after the scan layers (0: no attention)")
    ap.add_argument("--attn-layers", type=int, default=1, help="number of self-attention blocks when --attn is set")
    ap.add_argument("--attn-first", action="store_true",
                    help="put the self-attention block(s) before the scan layers instead of after them")
    ap.add_argument("--distill-pos", type=float,
                    help="share of distill draws that contain a question (default: natural pool ratio)")
    ap.add_argument("--distill-min-conf", type=float, default=0.0,
                    help="drop teacher-labeled samples whose least confident token is below this")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available()
                    else "mps" if torch.backends.mps.is_available() else "cpu")
    args = ap.parse_args()
    if args.device == "cuda" and os.environ.get("GQ_CUDA_MEM_FRACTION"):
        # Many folds share one GPU; without a cap each caching allocator grows until the card is full.
        torch.cuda.set_per_process_memory_fraction(float(os.environ["GQ_CUDA_MEM_FRACTION"]))

    torch.manual_seed(args.seed)
    set_feature_version(args.features)
    static = torch.load(args.static) if args.static else None
    static_vocab = static["vocab"] if static else None
    set_static_vocab(static_vocab)
    run = ROOT / "runs" / args.run
    run.mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    if args.fold is not None:
        sources["train"]["hand"] = [hand_sample(r) for r in load_hand_fold(args.fold, "train")]
    elif args.all_hand:
        sources["train"]["hand"] = [hand_sample(r) for r in load_hand_dev()]
    for pattern in filter(None, (args.silver, args.pairs)):
        extra = [hand_sample(r) for r in load_silver(pattern, args.fold)]
        sources["train"]["hand"] += extra
        print(f"added {len(extra)} LLM-labeled items from {pattern}", flush=True)
    if args.distill:
        path = args.distill.replace("{fold}", str(args.fold) if args.fold is not None else "all")
        sources["train"]["distill"] = [Sample(r["text"], [tuple(s) for s in r["spans"]], "distill")
                                       for r in load_jsonl(Path(path)) if r.get("conf", 1.0) >= args.distill_min_conf]
        print(f"distill samples: {len(sources['train']['distill'])} from {path}", flush=True)
    tests = {} if args.no_eval else eval_sets(sources)
    if not args.no_eval and args.fold is None and not args.all_hand:
        tests.update(hand_sets("val")[0])
    print(f"hand-labeled train items: {len(sources['train']['hand'])}", flush=True)
    device = torch.device(args.device)
    model = Tagger(args.hidden, args.layers, args.features, args.kind_head,
                   static_size=len(static_vocab) if static else 0,
                   static_dim=static["vectors"].shape[1] if static else 0,
                   static_train=bool(static and args.static_train), attn=args.attn, attn_layers=args.attn_layers,
                   attn_first=args.attn_first)
    if static:
        with torch.no_grad():
            model.static_table[: len(static_vocab)] = static["vectors"]
    model = model.to(device)
    print(f"parameters: {model.parameter_count():,}  device: {device}", flush=True)
    table = [p for n, p in model.named_parameters() if n == "static_table"]
    rest = [p for n, p in model.named_parameters() if n != "static_table"]
    groups = [{"params": rest}] + ([{"params": table, "lr": args.lr * 0.1, "weight_decay": 0.0}] if table else [])
    optimizer = torch.optim.AdamW(groups, lr=args.lr, weight_decay=1e-4)
    steps_total = args.epochs * (args.samples // args.batch)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, [g["lr"] for g in optimizer.param_groups],
                                                    total_steps=steps_total + 10, pct_start=0.1)
    history = []
    with mp.get_context("spawn").Pool(args.workers, _init_worker, (sources["train"], args.seed, args.hand_rate, args.hard_rate,
                                                                   args.hand_augment, args.features,
                                                                   args.distill_rate if args.distill else 0.0,
                                                                   args.distill_pos, static_vocab)) as pool:
        for epoch in range(args.epochs):
            t0 = time.time()
            data = draw(pool, args.samples, epoch, args.seed)
            t_data = time.time() - t0
            # Similar lengths per batch keep padding (and the CRF loop) short.
            data.sort(key=lambda d: len(d[0]))
            batches = [data[i: i + args.batch] for i in range(0, len(data), args.batch)]
            random.Random(epoch).shuffle(batches)
            model.train()
            total, count = 0.0, 0
            for batch in batches:
                rows, labels, mask = collate(batch, device)
                if args.identity_dropout:
                    cols = identity_cols()
                    drop = torch.rand(rows.shape[:2], device=device) < args.identity_dropout
                    rows[:, :, cols] = torch.where(drop.unsqueeze(-1), feature_rows(), rows[:, :, cols])
                joined = model.hidden(rows, mask)
                loss = model.nll(model.emissions_from(joined), labels, mask)
                if args.kind_head:
                    kinds, span = collate_kind(batch, rows.shape[1], device)
                    has = kinds >= 0
                    if has.any():
                        # Detach so the kind head cannot pull span features away from the CRF.
                        logits = model.kind_logits(joined[has].detach(), span[has])
                        loss = loss + args.kind_weight * torch.nn.functional.cross_entropy(logits, kinds[has])
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                if scheduler.last_epoch < steps_total:
                    scheduler.step()
                total += loss.item()
                count += 1
            t_train = time.time() - t0 - t_data
            report = {name: score(model, samples, device) for name, samples in tests.items()}
            summary = {
                "epoch": epoch + 1,
                "loss": round(total / max(1, count), 4),
                "data_s": round(t_data, 1),
                "train_s": round(t_train, 1),
            }
            if "synthetic/gold" in report:
                summary.update(synthetic_gold_options=report["synthetic/gold"]["options_exact"],
                               real_negative_false_q=report["real/negative"]["false_question_rate"])
            if "handval/all" in report:
                summary.update(val_options=report["handval/all"]["options_exact"],
                               val_negative_false_q=report["handval/negative"]["false_question_rate"])
            print(json.dumps(summary), flush=True)
            history.append({**summary, "report": report})
    # The final epoch is kept; picking an epoch by these test metrics would leak the test sets.
    torch.save({"state": model.state_dict(), "config": model.config, "epoch": args.epochs, "labels": list(LABEL_ID),
                "static_vocab": static_vocab}, run / "final.pt")
    (run / "history.json").write_text(json.dumps(history, indent=2))
    final = history[-1]["report"]
    (run / "report.json").write_text(json.dumps(final, indent=2))
    if final:
        print(json.dumps(final, indent=1))


if __name__ == "__main__":
    main()
