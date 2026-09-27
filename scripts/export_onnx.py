#!/usr/bin/env python3
"""Export the emission network to ONNX for browser inference.

The ONNX graph maps padded feature rows → per-token CRF emissions.
CRF Viterbi, tokenization, features, and the question compiler stay in TypeScript
(see web/). Kind-head rerank is Python-only and is not exported.

    uv sync --group export
    uv run --group export python scripts/export_onnx.py \
        --checkpoint runs/v13-all-a/final.pt \
        --out web/public/model
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from torch import Tensor, nn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gq.model import Tagger, affine_scan  # noqa: E402
from gq.predict import load  # noqa: E402
from gq.tokenize import MAX_TOKENS, clean, feature_rows, features, tokenize  # noqa: E402

MAX_WIDTH = 16  # v1 features + static id; measured max on gold/silver is 14


def affine_scan_fixed(gate: Tensor, candidate: Tensor) -> Tensor:
    """ONNX-friendly scan: always 8 doublings (covers padded length 256)."""
    stride = 1
    for _ in range(8):
        next_gate = gate[:, stride:] * gate[:, :-stride]
        next_candidate = candidate[:, stride:] + gate[:, stride:] * candidate[:, :-stride]
        gate = torch.cat((gate[:, :stride], next_gate), dim=1)
        candidate = torch.cat((candidate[:, :stride], next_candidate), dim=1)
        stride *= 2
    return candidate


class EmissionsONNX(nn.Module):
    """Wrap a Tagger so ONNX sees only (rows) → emissions."""

    def __init__(self, tagger: Tagger):
        super().__init__()
        self.tagger = tagger

    def forward(self, rows: Tensor) -> Tensor:
        pad = self.tagger.embedding.padding_idx
        mask = (rows != pad).any(dim=-1)
        return self.tagger.emissions(rows, mask)


def pad_rows(row_lists: list[list[int]], steps: int = MAX_TOKENS, width: int = MAX_WIDTH) -> Tensor:
    pad = feature_rows()
    out = torch.full((1, steps, width), pad, dtype=torch.long)
    for t, r in enumerate(row_lists[:steps]):
        out[0, t, : min(len(r), width)] = torch.tensor(r[:width], dtype=torch.long)
    return out


def encode_text(text: str) -> tuple[Tensor, list, int]:
    tokens = tokenize(clean(text))
    start = max(0, len(tokens) - MAX_TOKENS)
    kept = tokens[start:]
    rows = features(text, kept)
    return pad_rows(rows), kept, start


def export_member(tagger: Tagger, out_dir: Path, name: str, example: Tensor) -> Path:
    import gq.model as model_mod

    model_mod.affine_scan = affine_scan_fixed
    wrapper = EmissionsONNX(tagger).eval()
    path = out_dir / f"{name}.onnx"
    torch.onnx.export(
        wrapper,
        example,
        str(path),
        input_names=["rows"],
        output_names=["emissions"],
        dynamic_axes=None,  # fixed 1 x 256 x 16 for ort-web simplicity
        opset_version=17,
        dynamo=False,
    )
    model_mod.affine_scan = affine_scan  # restore
    return path


def sidecar(tagger: Tagger | list[Tagger], out_dir: Path, checkpoint_paths: list[str]):
    members = tagger if isinstance(tagger, list) else [tagger]
    start = torch.stack([m.start.detach().float().cpu() for m in members]).mean(0)
    transition = torch.stack([m.transition.detach().float().cpu() for m in members]).mean(0)
    cfg = members[0].config
    ckpt = torch.load(checkpoint_paths[0], map_location="cpu", weights_only=False)
    meta = {
        "max_tokens": MAX_TOKENS,
        "max_width": MAX_WIDTH,
        "feature_rows": feature_rows(cfg.get("feature_version", 1)),
        "feature_version": cfg.get("feature_version", 1),
        "num_labels": int(start.numel()),
        "labels": ["O", "Q_B", "Q_I", "OPT_B", "OPT_I", "REC"],
        "hidden": cfg.get("hidden"),
        "layers": cfg.get("layers"),
        "static_size": cfg.get("static_size", 0),
        "static_dim": cfg.get("static_dim", 0),
        "static_offset": 1 << 24,
        "kind_head": False,  # browser uses compiler kind
        "members": [Path(p).name for p in checkpoint_paths],
        "onnx": [f"member{i}.onnx" for i in range(len(members))],
    }
    (out_dir / "config.json").write_text(json.dumps(meta, indent=2) + "\n")
    (out_dir / "crf.json").write_text(json.dumps({
        "start": start.tolist(),
        "transition": transition.tolist(),
    }) + "\n")
    vocab = ckpt.get("static_vocab") or []
    (out_dir / "static_vocab.json").write_text(json.dumps(vocab) + "\n")


def verify(tagger: Tagger, onnx_path: Path, text: str) -> float:
    import numpy as np
    import onnxruntime as ort

    rows, tokens, _ = encode_text(text)
    pad = tagger.embedding.padding_idx
    mask = (rows != pad).any(-1)
    with torch.no_grad():
        import gq.model as model_mod
        model_mod.affine_scan = affine_scan_fixed
        torch_out = tagger.emissions(rows, mask)[0, : len(tokens)].numpy()
        model_mod.affine_scan = affine_scan

    sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    ort_out = sess.run(None, {"rows": rows.numpy()})[0][0, : len(tokens)]
    err = float(np.max(np.abs(torch_out - ort_out)))
    print(f"  max |torch−onnx| on {len(tokens)} tokens: {err:.3e}")
    return err


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checkpoint", default="runs/cv-t150-kh/fold0/final.pt",
                    help="one path, or comma-separated ensemble members")
    ap.add_argument("--out", type=Path, default=Path("web/public/model"))
    ap.add_argument("--text", default="Want me to merge it now, or wait for CI?")
    args = ap.parse_args()

    paths = [p.strip() for p in args.checkpoint.split(",") if p.strip()]
    args.out.mkdir(parents=True, exist_ok=True)

    models = [load(p) for p in paths]
    # load() may return Ensemble; unwrap single members
    members: list[Tagger] = []
    for m in models:
        if hasattr(m, "members"):
            members.extend(list(m.members))
        else:
            members.append(m)

    example, _, _ = encode_text(args.text)
    print(f"exporting {len(members)} member(s) → {args.out}")
    for i, tagger in enumerate(members):
        if tagger.config.get("attn"):
            print(f"  warning: member{i} has attention; ONNX may fail or be slow")
        path = export_member(tagger, args.out, f"member{i}", example)
        print(f"  wrote {path} ({path.stat().st_size / 1024:.0f} KB)")
        verify(tagger, path, args.text)

    sidecar(members, args.out, paths)
    print(f"wrote sidecars in {args.out}")
    print("browser: npm --prefix web install && npm --prefix web run dev")


if __name__ == "__main__":
    main()
