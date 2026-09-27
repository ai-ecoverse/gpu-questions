"""Parse agent messages into structured questions.

    uv run python -m gq.predict "Want me to A, or B?"
    echo "..." | uv run python -m gq.predict --checkpoint runs/v12-all-a/final.pt,runs/v12-all-b/final.pt
"""

from __future__ import annotations

import argparse
import json
import sys

import torch

from .compile import apply_kind, compile_questions
from .model import KINDS, Ensemble, Tagger, collate
from .tokenize import clean, features, set_feature_version, set_static_vocab, tail_start, tokenize


DEFAULT_CHECKPOINT = "runs/v12-all-a/final.pt,runs/v12-all-b/final.pt"


def load(path: str) -> Tagger | Ensemble:
    """One checkpoint, or several comma-separated ones averaged as an ensemble."""
    if "," in path:
        return Ensemble([load(p) for p in path.split(",")]).eval()
    checkpoint = torch.load(path, map_location="cpu")
    set_feature_version(checkpoint["config"].get("feature_version", 1))
    set_static_vocab(checkpoint.get("static_vocab"))
    model = Tagger(**checkpoint["config"])
    model.load_state_dict(checkpoint["state"])
    model.eval()
    return model


def has_kind_head(model: Tagger | Ensemble) -> bool:
    return bool(getattr(model, "config", {}).get("kind_head"))


def kind_probs(model: Tagger | Ensemble, joined, tokens, span: tuple[int, int]) -> dict[str, float] | None:
    """Kind-head probabilities for the question at character `span`, or None without a head.

    `joined` is a (1, steps, dim) tensor for a single model, or a list of such tensors
    (one per ensemble member) when `model` is an Ensemble.
    """
    if not has_kind_head(model):
        return None
    inside = [i for i, t in enumerate(tokens) if t.start < span[1] and t.end > span[0]]
    if not inside:
        return None
    steps = joined[0].shape[1] if isinstance(joined, list) else joined.shape[1]
    mask = torch.zeros((1, steps), dtype=torch.bool)
    mask[0, inside] = True
    if isinstance(model, Ensemble):
        # Each member scores its own hidden state; average the probabilities.
        probs = torch.stack([
            torch.softmax(m.kind_logits(m_joined, mask), -1)[0]
            for m, m_joined in zip(model.members, joined)
        ]).mean(0).tolist()
    else:
        probs = torch.softmax(model.kind_logits(joined, mask), -1)[0].tolist()
    return dict(zip(KINDS, probs))


def _question_dicts(qs) -> list[dict]:
    return [{"kind": x.kind, "propose": x.propose, "prompt": x.prompt, "multiSelect": x.multi_select,
             "default": x.default, "options": x.options} for x in qs]


@torch.no_grad()
def rerank_path(model: Tagger | Ensemble, text: str, tokens, joined, emissions_row, mask_row,
                k: int = 8, lam: float = 1.0) -> list:
    """Rerank k-best CRF paths by CRF score + λ log p(compiled kind).

    Only runs when the top-1 path already compiles to a question. That keeps
    negatives from picking up a lower-ranked path that invents one (which blew
    up the false-question rate in the unconstrained version).
    """
    import math

    paths = model.decode_kbest(emissions_row.unsqueeze(0), mask_row.unsqueeze(0), k)[0]
    if not paths:
        return []
    top_qs = compile_questions(text, tokens, paths[0][1])
    if not top_qs:
        return []
    best_qs, best_score = top_qs, None
    for score, path in paths:
        qs = compile_questions(text, tokens, path)
        if not qs:
            continue
        total = score
        probs = kind_probs(model, joined, tokens, qs[-1].span)
        if probs:
            total = score + lam * math.log(max(probs.get(qs[-1].kind, 0.0), 1e-9))
        if best_score is None or total > best_score:
            best_score, best_qs = total, qs
    return best_qs


@torch.no_grad()
def parse(model: Tagger | Ensemble, message: str, kind_mode: str = "hybrid",
          rerank_k: int = 8, rerank_lambda: float = 1.0) -> list[dict]:
    text = clean(message)
    tokens = tokenize(text)
    if not tokens:
        return []
    rows = features(text, tokens)
    cut = tail_start(tokens)
    tokens, rows = tokens[cut:], rows[cut:]
    batch_rows, _, mask = collate([(rows, [0] * len(rows))], "cpu")
    if isinstance(model, Ensemble) and has_kind_head(model):
        member_joined = [m.hidden(batch_rows, mask) for m in model.members]
        emissions = model.emissions(batch_rows, mask)
        joined = member_joined
    elif isinstance(model, Ensemble):
        joined, emissions = None, model.emissions(batch_rows, mask)
    else:
        joined = model.hidden(batch_rows, mask)
        emissions = model.emissions_from(joined)
    if kind_mode == "rerank" and has_kind_head(model) and joined is not None:
        questions = rerank_path(model, text, tokens, joined, emissions[0], mask[0], rerank_k, rerank_lambda)
        return _question_dicts(questions)
    labels = model.decode(emissions, mask)[0]
    questions = compile_questions(text, tokens, labels)
    if questions and joined is not None:
        # For ensembles, kind_probs expects a list of per-member joined tensors.
        probs = kind_probs(model, joined, tokens, questions[-1].span)
        if probs:
            questions[-1] = apply_kind(questions[-1], probs, kind_mode)
    return _question_dicts(questions)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT, help="one path, or several comma-separated (ensemble)")
    ap.add_argument("message", nargs="?")
    args = ap.parse_args()
    model = load(args.checkpoint)
    message = args.message if args.message is not None else sys.stdin.read()
    print(json.dumps(parse(model, message), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
