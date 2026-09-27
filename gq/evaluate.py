"""Evaluation: token F1 per role, plus question-level checks through the compiler.

Gold questions are the compiler's output on gold labels (an oracle run), so a
mismatch is always a tagging error, never a compiler difference.
"""

from __future__ import annotations

import collections
import random
import re

import torch

from .compile import apply_kind, compile_questions
from .data import Generator, Sample, encode, hand_sample, load_hand, weak_sample
from .labels import LABELS
from .model import Ensemble, Tagger, collate

HEURISTIC_KIND = {"yes_no": "yes_no", "confirm_plan": "yes_no", "either_or": "either_or",
                  "multi_choice": "multi_choice", "open_wh": "open"}


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


OPTION_LABEL_RE = re.compile(r"^\s*(?:(?:my\s+)?(?:recommendation|suggestion|pick)\s*[:—-]|option\s+\w{1,2}\s*[:—-]|"
                             r"\(?[a-h1-9][.)]\s)\s*", re.I)
OPTION_STEM_RE = re.compile(r"^(?:do you want(?: me)?(?: to)?|would you (?:like|prefer)(?: me)?(?: to)?|want me to|"
                            r"should i|shall i|i can|i could|or)\s+", re.I)
GENERIC = {"option", "one", "it", "this", "that", "do", "yes", "no", "a", "b", "c", "the", "either", "both"}


def _option_words(s: str) -> list[str]:
    import unicodedata

    s = unicodedata.normalize("NFKC", s).replace("**", "").replace("`", "")
    s = OPTION_LABEL_RE.sub("", s)
    words = norm(s).split()
    text = " ".join(words)
    stem = OPTION_STEM_RE.match(text)
    return (text[stem.end():] if stem else text).split()


def _contains(long: list[str], short: list[str]) -> bool:
    n = len(short)
    return any(long[i: i + n] == short for i in range(len(long) - n + 1))


def options_match(gold: list[str], pred: list[str]) -> bool:
    """Same choices in the same order: equal after normalization, or each gold answer is a whole-word
    span of its predicted option (extra explanation allowed) that names no other gold option."""
    if len(gold) != len(pred):
        return False
    g_words, p_words = [_option_words(o) for o in gold], [_option_words(o) for o in pred]
    for i, (g, p) in enumerate(zip(g_words, p_words)):
        if g == p:
            continue
        short, long = (g, p) if len(g) <= len(p) else (p, g)
        if not short or set(short) <= GENERIC or not _contains(long, short):
            return False
        for j, other in enumerate(g_words):
            if j != i and other and not set(other) <= GENERIC and _contains(p, other) and not _contains(g, other):
                return False
    return True


def hand_sets(part: str = "test", records: list[dict] | None = None) -> tuple[dict[str, list[Sample]], dict[str, list[dict]]]:
    """Hand-labeled real turns from one side of gold/split.json, grouped by the kind of the last question.

    The train side is mixed into training, val is used while iterating, and test
    is only checked at milestones. Sets are named "hand/..." for test and
    "handval/..." for val. Returns the sets and each sample's hand-written expected
    questions, keyed by Sample.source. Those record what a human reads, which the
    compiler cannot always derive from spans (propose, multi-select, prose defaults).
    """
    if records is None:
        records = load_hand(part)
    if not records:
        return {}, {}
    prefix = "hand" if part == "test" else f"hand{part}"
    sets, expected = collections.defaultdict(list), {}
    for r in records:
        s = hand_sample(r)
        expected[s.source] = r["expected"]
        sets["all"].append(s)
        if not r["expected"]:
            sets["negative"].append(s)
            continue
        kind = r["expected"][-1]["kind"]
        sets["choice" if kind in ("either_or", "multi_choice") else kind].append(s)
        if len(r["expected"]) > 1:
            sets["multi"].append(s)
    order = ["all", "yes_no", "choice", "open", "multi", "negative"]
    return {f"{prefix}/{k}": sets[k] for k in order}, expected


def hand_agreement(samples: list[Sample], expected: dict[str, list[dict]], predicted: list[list]) -> dict:
    """Compare predicted questions (compiled, or the heuristic's) with the hand-written expectations."""
    q = collections.Counter()
    for sample, pq in zip(samples, predicted):
        ex = expected[sample.source]
        if not (ex and pq):
            continue
        g, p = ex[-1], pq[-1]
        q["both"] += 1
        q["kind_ok"] += g["kind"] == p["kind"]
        if "propose" in p:
            q["propose_n"] += 1
            q["propose_ok"] += g["propose"] == p["propose"]
            q["multi_ok"] += g["multiSelect"] == p["multiSelect"]
            q["default_ok"] += g["default"] == p["default"]
            q["count_ok"] += len(ex) == len(pq)
        if g["options"]:
            q["with_options"] += 1
            q["with_options_ok"] += [norm(o) for o in g["options"]] == [norm(o) for o in p["options"]]

    def rate(key, n):
        return round(q[key] / q[n], 3) if q[n] else None

    out = {"kind_acc": rate("kind_ok", "both"), "options_exact": rate("with_options_ok", "with_options")}
    if q["propose_n"]:
        out.update(propose_acc=rate("propose_ok", "propose_n"), multi_select_acc=rate("multi_ok", "propose_n"),
                   default_acc=rate("default_ok", "propose_n"), count_acc=rate("count_ok", "propose_n"))
    return out


@torch.no_grad()
def model_questions(model: Tagger, samples: list[Sample], device, kind_mode: str = "hybrid",
                    batch_size: int = 64, rerank_k: int = 8, rerank_lambda: float = 1.0) -> list[list[dict]]:
    from .predict import has_kind_head, kind_probs, rerank_path

    model.eval()
    encoded = [encode(s) for s in samples]
    keep = [i for i, e in enumerate(encoded) if e[0]]
    out = [[] for _ in samples]
    for c in range(0, len(keep), batch_size):
        chunk = keep[c: c + batch_size]
        rows, _, mask = collate([(encoded[i][1], [0] * len(encoded[i][1])) for i in chunk], device)
        is_ensemble = isinstance(model, Ensemble)
        if is_ensemble and has_kind_head(model):
            member_joined = [m.hidden(rows, mask).cpu() for m in model.members]
            emissions = model.emissions(rows, mask)
            joined = member_joined
        elif hasattr(model, "hidden"):
            joined = model.hidden(rows, mask)
            emissions = model.emissions_from(joined) if not is_ensemble else model.emissions(rows, mask)
            joined = joined.cpu()
        else:
            joined, emissions = None, model.emissions(rows, mask)
        emissions = emissions.cpu()
        mask_cpu = mask.cpu()
        if kind_mode == "rerank" and joined is not None and has_kind_head(model):
            for b, i in enumerate(chunk):
                tokens = encoded[i][0]
                j = [t[b: b + 1] for t in joined] if is_ensemble else joined[b: b + 1]
                qs = rerank_path(model, samples[i].text, tokens, j, emissions[b], mask_cpu[b],
                                rerank_k, rerank_lambda)
                out[i] = [{"kind": x.kind, "propose": x.propose, "prompt": x.prompt, "multiSelect": x.multi_select,
                           "default": x.default, "options": x.options} for x in qs]
            continue
        preds = model.decode(emissions, mask_cpu)
        for b, (i, pred) in enumerate(zip(chunk, preds)):
            tokens = encoded[i][0]
            qs = compile_questions(samples[i].text, tokens, pred)
            if qs and joined is not None:
                j = [t[b: b + 1] for t in joined] if is_ensemble else joined[b: b + 1]
                probs = kind_probs(model, j, tokens, qs[-1].span)
                if probs:
                    qs[-1] = apply_kind(qs[-1], probs, kind_mode)
            out[i] = [{"kind": x.kind, "propose": x.propose, "prompt": x.prompt, "multiSelect": x.multi_select,
                       "default": x.default, "options": x.options} for x in qs]
    return out


def eval_sets(sources: dict, seed: int = 1234, synthetic: int = 3000) -> dict[str, list[Sample]]:
    gen = Generator(sources["test"], random.Random(seed), augment_options=False)
    synth = collections.defaultdict(list)
    for _ in range(synthetic):
        s = gen.sample()
        if not s.source.startswith("weak"):
            synth[s.source].append(s)
    weak = [w for w in (weak_sample(r) for r in sources["test"]["eot"]) if w]
    sets = {f"synthetic/{k}": v for k, v in sorted(synth.items())}
    sets["real/yes_no+confirm"] = [w for w in weak if w.source in ("weak_yes_no", "weak_confirm_plan", "weak_open_wh")]
    sets["real/either_or"] = [w for w in weak if w.source == "weak_either_or"]
    sets["real/negative"] = [w for w in weak if w.source == "weak_negative"][:600]
    return sets


@torch.no_grad()
def predict(model: Tagger, encoded, device, batch_size: int = 128):
    model.eval()
    out = []
    for i in range(0, len(encoded), batch_size):
        chunk = encoded[i: i + batch_size]
        rows, _, mask = collate([(rows, [0] * len(rows)) for _, rows, _ in chunk], device)
        out.extend(model.decode(model.emissions(rows, mask), mask))
    return out


def score(model: Tagger, samples: list[Sample], device) -> dict:
    encoded = [encode(s) for s in samples]
    encoded = [(s, e) for s, e in zip(samples, encoded) if e[0]]
    preds = predict(model, [e for _, e in encoded], device)
    tp, fp, fn = collections.Counter(), collections.Counter(), collections.Counter()
    q = collections.Counter()
    for (sample, (tokens, _, gold)), pred in zip(encoded, preds):
        for g, p in zip(gold, pred):
            if g == p:
                tp[g] += 1
            else:
                fp[p] += 1
                fn[g] += 1
        gq = compile_questions(sample.text, tokens, gold)
        pq = compile_questions(sample.text, tokens, pred)
        q["n"] += 1
        q["has_q_gold"] += bool(gq)
        q["has_q_pred"] += bool(pq)
        q["has_q_both"] += bool(gq) and bool(pq)
        if gq and pq:
            g, p = gq[-1], pq[-1]
            q["kind_ok"] += g.kind == p.kind
            q["options_ok"] += [norm(o) for o in g.options] == [norm(o) for o in p.options]
            q["default_ok"] += g.default == p.default
            q["count_ok"] += len(gq) == len(pq)
            if g.options:
                q["with_options"] += 1
                q["with_options_ok"] += [norm(o) for o in g.options] == [norm(o) for o in p.options]
    f1 = {}
    for i, name in enumerate(LABELS):
        if name == "O" or tp[i] + fn[i] == 0:
            continue
        precision = tp[i] / max(1, tp[i] + fp[i])
        recall = tp[i] / max(1, tp[i] + fn[i])
        f1[name] = round(2 * precision * recall / max(1e-9, precision + recall), 3)
    both = max(1, q["has_q_both"])
    return {
        "samples": q["n"],
        "token_f1": f1,
        "question_recall": round(q["has_q_both"] / max(1, q["has_q_gold"]), 3) if q["has_q_gold"] else None,
        "false_question_rate": round((q["has_q_pred"] - q["has_q_both"]) / max(1, q["n"] - q["has_q_gold"]), 3)
        if q["n"] > q["has_q_gold"] else None,
        "kind_acc": round(q["kind_ok"] / both, 3) if q["has_q_both"] else None,
        "options_exact": round(q["with_options_ok"] / max(1, q["with_options"]), 3) if q["with_options"] else None,
        "default_acc": round(q["default_ok"] / both, 3) if q["has_q_both"] else None,
        "count_acc": round(q["count_ok"] / both, 3) if q["has_q_both"] else None,
    }


def load_extract():
    import importlib.util

    spec = importlib.util.spec_from_file_location("extract", ROOT / "scripts" / "extract.py")
    extract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extract)
    return extract


def heuristic_questions(samples: list[Sample]) -> list[list[dict]]:
    """The heuristic's last question per sample, in hand_agreement's shape (it has no propose/default)."""
    extract = load_extract()
    out = []
    for sample in samples:
        h = extract.classify(sample.text)
        out.append([{"kind": HEURISTIC_KIND.get(h["cls"]), "options": h["options"]}] if h else [])
    return out


def heuristic_score(samples: list[Sample]) -> dict:
    """Score the survey's regex classifier (scripts/extract.py) as a no-model baseline."""
    extract = load_extract()
    q = collections.Counter()
    for sample in samples:
        tokens, _, gold = encode(sample)
        gq = compile_questions(sample.text, tokens, gold)
        h = extract.classify(sample.text)
        q["n"] += 1
        q["gold_q"] += bool(gq)
        q["pred_q"] += bool(h)
        q["both"] += bool(gq) and bool(h)
        if gq and h:
            g = gq[-1]
            if g.options:
                q["with_options"] += 1
                q["with_options_ok"] += [norm(o) for o in g.options] == [norm(o) for o in h["options"]]
    return {
        "samples": q["n"],
        "question_recall": round(q["both"] / max(1, q["gold_q"]), 3) if q["gold_q"] else None,
        "false_question_rate": round((q["pred_q"] - q["both"]) / max(1, q["n"] - q["gold_q"]), 3) if q["n"] > q["gold_q"] else None,
        "options_exact": round(q["with_options_ok"] / max(1, q["with_options"]), 3) if q["with_options"] else None,
    }


def main():
    import argparse
    import json

    from .data import load_sources
    from .predict import load

    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint", nargs="?")
    ap.add_argument("--heuristic", action="store_true", help="score the regex baseline instead of a model")
    ap.add_argument("--part", choices=["val", "test"], default="val",
                    help="hand-labeled side to report (use test only at milestones)")
    ap.add_argument("--hand-only", action="store_true", help="skip the synthetic and weak real sets")
    args = ap.parse_args()
    sets = {} if args.hand_only else eval_sets(load_sources())
    hand, expected = hand_sets(args.part)
    sets.update(hand)
    if args.heuristic:
        for name, samples in sets.items():
            result = heuristic_score(samples)
            if name in hand:
                result["vs_hand"] = hand_agreement(samples, expected, heuristic_questions(samples))
            print(name, json.dumps(result))
        return
    model = load(args.checkpoint)
    for name, samples in sets.items():
        result = score(model, samples, "cpu")
        if name in hand:
            result["vs_hand"] = hand_agreement(samples, expected, model_questions(model, samples, "cpu"))
        print(name, json.dumps(result))


if __name__ == "__main__":
    main()
