"""A pretrained-encoder teacher for the tiny tagger (needs `uv sync --group teacher`).

    uv run --group teacher python -m gq.teacher train --run teacher32 --fold 0
    uv run --group teacher python -m gq.teacher cv --run teacher32          # train all folds, pooled OOF metrics
    uv run --group teacher python -m gq.teacher label --run teacher32 --fold 0

The teacher fine-tunes a small encoder (Ettin, ModernBERT recipe) to predict the
same token roles as the tiny tagger. Subword labels come from the tiny tagger's
tokens: each subword takes the role of the token under its first character, and
a token's prediction is read from the subword covering its first character.
`label` tags unlabeled real turns (never from the held-out fold or the batch-2 test
set) and writes them as samples that `gq.train --distill` mixes into training.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import torch

from .compile import compile_questions
from .data import (EXPORT, HAND_SPLIT, ROOT, Generator, Sample, encode, hand_sample, load_hand_dev, load_hand_fold,
                   load_jsonl, load_sources)
from .labels import LABEL_ID, LABELS
from .tokenize import clean

MAX_SUBWORDS = 512
POOLS = [ROOT / "data" / "hf" / "candidates.jsonl", ROOT / "data" / "hf2" / "candidates.jsonl"]
BEGIN_TO_INSIDE = {LABEL_ID["Q_B"]: LABEL_ID["Q_I"], LABEL_ID["OPT_B"]: LABEL_ID["OPT_I"]}


def _device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def _align(tok, sample: Sample):
    """Encode the modeled tail: (our tokens, our labels, subword ids, subword labels, char->subword map, base)."""
    tokens, _, labels = encode(sample)
    if not tokens:
        return None
    base = tokens[0].start
    tail = sample.text[base:]
    enc = tok(tail, return_offsets_mapping=True, add_special_tokens=False)
    ids, offsets = enc["input_ids"], enc["offset_mapping"]
    if len(ids) > MAX_SUBWORDS - 2:
        ids, offsets = ids[-(MAX_SUBWORDS - 2):], offsets[-(MAX_SUBWORDS - 2):]
    char_tok = [-1] * len(tail)
    for j, t in enumerate(tokens):
        for c in range(t.start - base, min(t.end - base, len(tail))):
            char_tok[c] = j
    char_sub = [-1] * len(tail)
    sub_labels, last_tok = [], -1
    for s, (a, b) in enumerate(offsets):
        for c in range(a, b):
            if char_sub[c] < 0:
                char_sub[c] = s
        first = next((c for c in range(a, b) if tail[c] not in " \t"), a)
        j = char_tok[first] if first < len(tail) else -1
        lab = labels[j] if j >= 0 else LABEL_ID["O"]
        if j >= 0 and j == last_tok:
            lab = BEGIN_TO_INSIDE.get(lab, lab)
        sub_labels.append(lab)
        last_tok = j
    ids = [tok.cls_token_id] + list(ids) + [tok.sep_token_id]
    sub_labels = [-100] + sub_labels + [-100]
    return tokens, labels, ids, sub_labels, char_sub, base


def _batches(items, size):
    items = sorted(items, key=lambda x: len(x[0]))
    chunks = [items[i: i + size] for i in range(0, len(items), size)]
    random.shuffle(chunks)
    return chunks


def _pad(chunk, pad_id, device):
    n = max(len(ids) for ids, _ in chunk)
    ids = torch.full((len(chunk), n), pad_id, dtype=torch.long)
    labs = torch.full((len(chunk), n), -100, dtype=torch.long)
    att = torch.zeros((len(chunk), n), dtype=torch.long)
    for b, (x, y) in enumerate(chunk):
        ids[b, : len(x)] = torch.tensor(x)
        labs[b, : len(y)] = torch.tensor(y)
        att[b, : len(x)] = 1
    return ids.to(device), att.to(device), labs.to(device)


def train(run: str, fold: int | None, model_name: str, epochs: int, synthetic: int, lr: float, batch: int, seed: int,
          extra: tuple[str, ...] = ()):
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    from .data import load_silver

    random.seed(seed)
    torch.manual_seed(seed)
    out = ROOT / "runs" / run / (f"fold{fold}" if fold is not None else "all")
    out.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(LABELS)).to(_device())
    hand = [hand_sample(r) for r in (load_hand_fold(fold, "train") if fold is not None else load_hand_dev())]
    for pattern in extra:
        hand += [hand_sample(r) for r in load_silver(pattern, fold)]
    sources = load_sources()["train"]
    sources["hand"] = hand
    gen = Generator(sources, random.Random(seed), hand_augment=True)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    steps = epochs * ((2 * len(hand) + synthetic) // batch + 1)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, lr, total_steps=steps + 10, pct_start=0.1)
    t0 = time.time()
    for epoch in range(epochs):
        samples = hand + [gen.augment_hand(s) for s in hand] + [gen.sample() for _ in range(synthetic)]
        items = [(a[2], a[3]) for a in (_align(tok, s) for s in samples) if a]
        model.train()
        total = n = 0
        for chunk in _batches(items, batch):
            ids, att, labs = _pad(chunk, tok.pad_token_id, _device())
            loss = model(input_ids=ids, attention_mask=att, labels=labs).loss
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            if sched.last_epoch < steps:
                sched.step()
            total += loss.item()
            n += 1
        print(json.dumps({"fold": fold, "epoch": epoch + 1, "loss": round(total / max(1, n), 4),
                          "items": len(items), "s": round(time.time() - t0)}), flush=True)
    model.save_pretrained(out)
    tok.save_pretrained(out)
    (out / "teacher.json").write_text(json.dumps({"base": model_name, "epochs": epochs, "synthetic": synthetic,
                                                  "lr": lr, "fold": fold, "extra": list(extra)}))
    return out


class Teacher:
    def __init__(self, path: Path):
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        self.tok = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForTokenClassification.from_pretrained(path).to(_device()).eval()

    @torch.no_grad()
    def tag(self, samples: list[Sample], batch: int = 32):
        """Per sample: (our tail tokens, predicted labels, confidence) or None when the sample is empty."""
        aligned = [_align(self.tok, s) for s in samples]
        order = sorted((i for i, a in enumerate(aligned) if a), key=lambda i: len(aligned[i][2]))
        out = [None] * len(samples)
        for c in range(0, len(order), batch):
            chunk = order[c: c + batch]
            ids, att, _ = _pad([(aligned[i][2], aligned[i][3]) for i in chunk], self.tok.pad_token_id, _device())
            probs = torch.softmax(self.model(input_ids=ids, attention_mask=att).logits.float(), -1).cpu()
            for b, i in enumerate(chunk):
                tokens, _, _, _, char_sub, base = aligned[i]
                labels, confs, last_sub = [], [], None
                for t in tokens:
                    c0 = t.start - base
                    s = char_sub[c0] if 0 <= c0 < len(char_sub) else -1
                    if s < 0:
                        labels.append(LABEL_ID["O"])
                        confs.append(1.0)
                        continue
                    p = probs[b, s + 1]
                    lab = int(p.argmax())
                    if s == last_sub:
                        lab = BEGIN_TO_INSIDE.get(lab, lab)
                    labels.append(lab)
                    confs.append(float(p.max()))
                    last_sub = s
                out[i] = (tokens, labels, min(confs) if confs else 1.0)
        return out


def teacher_questions(teacher: Teacher, samples: list[Sample]) -> list[list[dict]]:
    out = []
    for s, tagged in zip(samples, teacher.tag(samples)):
        if not tagged:
            out.append([])
            continue
        tokens, labels, _ = tagged
        out.append([{"kind": q.kind, "propose": q.propose, "multiSelect": q.multi_select, "default": q.default,
                     "options": q.options} for q in compile_questions(s.text, tokens, labels)])
    return out


def _spans(tokens, labels) -> list[list]:
    spans, cur = [], None
    for t, lab in zip(tokens, labels):
        name = LABELS[lab]
        kind = {"Q": "Q", "OPT": "OPT", "REC": "REC"}.get(name.split("_")[0])
        begins = name.endswith("_B") or name == "REC" or (cur is None or cur[2] != kind)
        if kind is None:
            cur = None
            continue
        if begins:
            cur = [t.start, t.end, kind]
            spans.append(cur)
        else:
            cur[1] = t.end
    return spans


def pool_texts(fold: int | None) -> list[str]:
    """Unlabeled turns allowed for a fold: never its own datasets, the batch-2 test set, or labeled items."""
    split = json.loads(HAND_SPLIT.read_text())
    banned = set(split.get("batch2_test_datasets", []))
    if fold is not None:
        banned |= {d for d, k in split["cv_folds"].items() if k == fold}
    labeled = {r["id"] for r in load_hand_dev()}
    texts = []
    for path in POOLS:
        if path.exists():
            texts += [r["text"] for r in load_jsonl(path) if r["dataset"] not in banned and r["id"] not in labeled]
    texts += [clean(r["tail"]) for r in load_jsonl(EXPORT / "eot.jsonl")]
    seen, unique = set(), []
    for t in texts:
        key = t[-300:]
        if t and key not in seen:
            seen.add(key)
            unique.append(t)
    return unique


def label(run: str, fold: int | None):
    path = ROOT / "runs" / run / (f"fold{fold}" if fold is not None else "all")
    teacher = Teacher(path)
    texts = pool_texts(fold)
    samples = [Sample(t) for t in texts]
    t0 = time.time()
    tagged = teacher.tag(samples)
    with open(path / "distill.jsonl", "w") as fh:
        for s, tg in zip(samples, tagged):
            if tg:
                fh.write(json.dumps({"text": s.text, "spans": _spans(tg[0], tg[1]), "conf": round(tg[2], 3)}) + "\n")
    print(f"labeled {len(samples)} pool turns for fold {fold} in {time.time() - t0:.0f}s -> {path / 'distill.jsonl'}")


def main():
    from .cv import metrics, report

    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["train", "cv", "label"])
    ap.add_argument("--run", required=True)
    ap.add_argument("--fold", type=int)
    ap.add_argument("--all", action="store_true", help="train/label on all development data (final teacher)")
    ap.add_argument("--model", default="jhu-clsp/ettin-encoder-32m")
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--synthetic", type=int, default=6000)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20260924)
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--silver", help="glob of LLM silver labels to add to the hand pool")
    ap.add_argument("--pairs", help="glob of minimal-pair labels to add to the hand pool")
    args = ap.parse_args()
    fold = None if args.all else args.fold
    extra = tuple(filter(None, (args.silver, args.pairs)))
    if args.step == "train":
        train(args.run, fold, args.model, args.epochs, args.synthetic, args.lr, args.batch, args.seed, extra)
    elif args.step == "label":
        label(args.run, fold)
    else:
        folds = sorted(set(json.loads(HAND_SPLIT.read_text())["cv_folds"].values()))
        rows = []
        for k in folds:
            path = ROOT / "runs" / args.run / f"fold{k}"
            if not (path / "teacher.json").exists():
                train(args.run, k, args.model, args.epochs, args.synthetic, args.lr, args.batch, args.seed, extra)
            records = load_hand_fold(k, "test")
            samples = [hand_sample(r) for r in records]
            predicted = teacher_questions(Teacher(path), samples)
            rows += [(r, s, p, k) for r, s, p in zip(records, samples, predicted)]
            print(f"fold {k}:", json.dumps(metrics([x for x in rows if x[3] == k])), flush=True)
        report(rows, args.show, label=f"teacher {args.run} pooled out-of-fold")


if __name__ == "__main__":
    main()
