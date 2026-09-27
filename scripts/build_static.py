"""Static word vectors for the tagger, taken from a pretrained model (model2vec-style).

    uv run --group teacher python scripts/build_static.py [--source static|encoder] [--vocab 20000] [--dim 32]

The vocabulary is the most frequent lowercased word tokens in development and
unlabeled public text (never the test-set owners). With `--source static` (default)
a word's vector is the mean of its subword rows in a model2vec static model
(minishlab/potion-base-8M, MIT). With `--source encoder`, each word is encoded alone
by a transformer encoder and its subword states are mean-pooled; that gave vectors
whose neighbours mostly share spelling, not meaning. PCA reduces either to `--dim`
dimensions. Writes runs/static/<name>.pt with {"vocab", "vectors", "source"}.
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

from gq.data import HAND_SPLIT, load_hand_dev, load_jsonl  # noqa: E402
from gq.tokenize import static_word, tokenize  # noqa: E402

POOLS = ["data/hf/candidates.jsonl", "data/hf2/candidates.jsonl", "data/hf3a/candidates.jsonl",
         "data/hf3b/candidates.jsonl"]


def word_counts(max_texts: int) -> collections.Counter:
    split = json.loads(HAND_SPLIT.read_text())
    test_owners = {d.split("/")[0] for d in split["batch2_test_datasets"]}
    texts = [r["text"] for r in load_hand_dev()]
    for p in POOLS:
        if (ROOT / p).exists():
            texts += [r["text"][-3000:] for r in load_jsonl(ROOT / p) if r["dataset"].split("/")[0] not in test_owners]
    counts = collections.Counter()
    for t in texts[:max_texts]:
        counts.update(static_word(tok.text) for tok in tokenize(t) if tok.text[:1].isalpha())
    return counts


def encode_static(model: str, vocab: list[str]) -> torch.Tensor:
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    from tokenizers import Tokenizer

    table = next(iter(load_file(hf_hub_download(model, "model.safetensors")).values())).float()
    tok = Tokenizer.from_file(hf_hub_download(model, "tokenizer.json"))
    special = {tok.token_to_id(t) for t in ("[CLS]", "[SEP]", "[PAD]", "[UNK]")} - {None}
    out = torch.zeros(len(vocab), table.shape[1])
    for i, enc in enumerate(tok.encode_batch(vocab, add_special_tokens=False)):
        ids = [j for j in enc.ids if j not in special]
        if ids:
            out[i] = table[ids].mean(0)
    return out


def encode_encoder(model: str, vocab: list[str]) -> torch.Tensor:
    from transformers import AutoModel, AutoTokenizer

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(model)
    net = AutoModel.from_pretrained(model).to(device).eval()
    states = []
    with torch.no_grad():
        for i in range(0, len(vocab), 512):
            enc = tok(vocab[i: i + 512], return_tensors="pt", padding=True).to(device)
            hidden = net(**enc).last_hidden_state
            keep = enc["attention_mask"].clone()
            keep[:, 0] = 0  # CLS
            keep[torch.arange(len(keep)), enc["attention_mask"].sum(1) - 1] = 0  # SEP
            keep = keep.unsqueeze(-1).float()
            states.append(((hidden * keep).sum(1) / keep.sum(1).clamp_min(1)).float().cpu())
    return torch.cat(states)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["static", "encoder"], default="static")
    ap.add_argument("--model", help="default: minishlab/potion-base-8M (static) or jhu-clsp/ettin-encoder-32m")
    ap.add_argument("--vocab", type=int, default=20000)
    ap.add_argument("--dim", type=int, default=32)
    ap.add_argument("--min-count", type=int, default=3)
    ap.add_argument("--max-texts", type=int, default=250000)
    ap.add_argument("--name")
    args = ap.parse_args()
    model = args.model or ("minishlab/potion-base-8M" if args.source == "static" else "jhu-clsp/ettin-encoder-32m")
    name = args.name or f"{model.split('/')[-1]}-{args.vocab // 1000}k-{args.dim}"

    counts = word_counts(args.max_texts)
    vocab = [w for w, c in counts.most_common(args.vocab) if c >= args.min_count]
    print(f"{len(counts)} distinct words, vocabulary {len(vocab)}", flush=True)
    x = (encode_static if args.source == "static" else encode_encoder)(model, vocab)
    x = x - x.mean(0)
    _, _, v = torch.pca_lowrank(x, q=args.dim, center=False)
    vectors = x @ v[:, : args.dim]
    vectors = vectors / vectors.std() * 0.3
    out = ROOT / "runs" / "static" / f"{name}.pt"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"vocab": vocab, "vectors": vectors, "source": model}, out)
    print(f"wrote {out}: {tuple(vectors.shape)}")


if __name__ == "__main__":
    main()
