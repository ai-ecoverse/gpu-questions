"""Small bidirectional affine-scan tagger with a linear-chain CRF.

Architecture follows gpu-time (MIT, Arik Chakma): summed sparse feature
embeddings, a depthwise 5-tap convolution, gated linear scans in both
directions, a pooled global context, and a CRF over token roles.
"""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .labels import LABELS
from .tokenize import STATIC_OFFSET, feature_rows

NUM_LABELS = len(LABELS)


def affine_scan(gate: Tensor, candidate: Tensor) -> Tensor:
    """Inclusive parallel scan of state[t] = gate[t] * state[t-1] + candidate[t] over dim 1."""
    width = gate.shape[1]
    stride = 1
    while stride < width:
        next_gate = gate[:, stride:] * gate[:, :-stride]
        next_candidate = candidate[:, stride:] + gate[:, stride:] * candidate[:, :-stride]
        gate = torch.cat((gate[:, :stride], next_gate), dim=1)
        candidate = torch.cat((candidate[:, :stride], next_candidate), dim=1)
        stride *= 2
    return candidate


class ScanLayer(nn.Module):
    def __init__(self, hidden: int):
        super().__init__()
        self.gate = nn.Linear(hidden, hidden)
        self.candidate = nn.Linear(hidden, hidden)
        self.combine = nn.Linear(hidden * 2, hidden)
        # Spread lanes across short and long memories from the start.
        with torch.no_grad():
            self.gate.bias.copy_(torch.linspace(0.0, 4.0, hidden))

    def forward(self, x: Tensor, mask: Tensor) -> Tensor:
        gate = torch.sigmoid(self.gate(x))
        candidate = (1 - gate) * torch.tanh(self.candidate(x)) * mask
        forward = affine_scan(gate, candidate)
        # Right padding has zero candidates, so the reversed scan starts clean.
        backward = affine_scan(gate.flip(1), candidate.flip(1)).flip(1)
        return (x + torch.tanh(self.combine(torch.cat((forward, backward), -1)))) * mask


class AttentionLayer(nn.Module):
    """Pre-norm multi-head self-attention plus feed-forward block over the unpadded tokens."""

    def __init__(self, hidden: int, heads: int):
        super().__init__()
        if hidden % heads:
            raise ValueError(f"hidden {hidden} is not divisible by {heads} attention heads")
        self.heads = heads
        self.norm = nn.LayerNorm(hidden)
        self.qkv = nn.Linear(hidden, hidden * 3)
        self.out = nn.Linear(hidden, hidden)
        self.ff_norm = nn.LayerNorm(hidden)
        self.ff = nn.Sequential(nn.Linear(hidden, hidden * 2), nn.GELU(), nn.Linear(hidden * 2, hidden))
        # Zero residual branches: training starts from the scan-only model's function.
        for layer in (self.out, self.ff[2]):
            nn.init.zeros_(layer.weight)
            nn.init.zeros_(layer.bias)

    def forward(self, x: Tensor, mask: Tensor) -> Tensor:
        batch, steps, hidden = x.shape
        q, k, v = self.qkv(self.norm(x)).view(batch, steps, 3, self.heads, hidden // self.heads).permute(2, 0, 3, 1, 4)
        keep = mask.squeeze(-1).bool()[:, None, None, :]
        attended = F.scaled_dot_product_attention(q, k, v, attn_mask=keep)
        x = x + self.out(attended.transpose(1, 2).reshape(batch, steps, hidden))
        x = x + self.ff(self.ff_norm(x))
        return x * mask


KINDS = ["yes_no", "either_or", "multi_choice", "open"]


class Tagger(nn.Module):
    def __init__(self, hidden: int = 48, layers: int = 2, feature_version: int = 1, kind_head: bool = False,
                 static_size: int = 0, static_dim: int = 0, static_train: bool = False, attn: int = 0,
                 attn_layers: int = 1, attn_first: bool = False):
        super().__init__()
        self.config = {"hidden": hidden, "layers": layers, "feature_version": feature_version, "kind_head": kind_head}
        rows = feature_rows(feature_version)
        self.embedding = nn.Embedding(rows + 1, hidden, padding_idx=rows)
        nn.init.normal_(self.embedding.weight, std=0.08)
        with torch.no_grad():
            self.embedding.weight[rows].zero_()
        if static_size:
            # Pretrained word vectors (last row: unknown word, zeros). Frozen unless static_train.
            self.config.update(static_size=static_size, static_dim=static_dim)
            table = torch.zeros(static_size + 1, static_dim)
            if static_train:
                self.config["static_train"] = True
                self.static_table = nn.Parameter(table)
            else:
                self.register_buffer("static_table", table)
            self.static_proj = nn.Linear(static_dim, hidden, bias=False)
        if kind_head:
            self.kind_attn = nn.Linear(hidden * 2, 1)
            self.kind_mlp = nn.Sequential(nn.Linear(hidden * 4, 64), nn.Tanh(), nn.Linear(64, len(KINDS)))
        self.convolution = nn.Conv1d(hidden, hidden, 5, padding=2, groups=hidden)
        self.layers = nn.ModuleList(ScanLayer(hidden) for _ in range(layers))
        self.global_gate = nn.Linear(hidden, hidden)
        self.head = nn.Linear(hidden * 2, 64)
        self.output = nn.Linear(64, NUM_LABELS)
        self.transition = nn.Parameter(torch.zeros(NUM_LABELS, NUM_LABELS))
        self.start = nn.Parameter(torch.zeros(NUM_LABELS))
        if attn:
            # Built last so the other modules draw the same initial weights as a model without attention.
            self.config.update(attn=attn, attn_layers=attn_layers)
            if attn_first:
                self.config["attn_first"] = True
            self.attention = nn.ModuleList(AttentionLayer(hidden, attn) for _ in range(attn_layers))

    def hidden(self, rows: Tensor, mask: Tensor) -> Tensor:
        """Per-token states joined with the pooled message context: (batch, steps, 2 * hidden)."""
        m = mask.unsqueeze(-1).float()
        if hasattr(self, "static_table"):
            is_static = rows >= STATIC_OFFSET
            size = self.static_table.shape[0] - 1
            ids = torch.where(is_static, rows - STATIC_OFFSET, size).clamp(0, size)
            vectors = (self.static_table[ids] * is_static.unsqueeze(-1)).sum(2)
            rows = torch.where(is_static, self.embedding.padding_idx, rows)
            x = self.embedding(rows).sum(2) + self.static_proj(vectors)
        else:
            x = self.embedding(rows).sum(2)
        x = torch.tanh(x + self.convolution(x.transpose(1, 2)).transpose(1, 2)) * m
        attention = list(getattr(self, "attention", ()))
        before = attention if self.config.get("attn_first") else []
        after = [] if before else attention
        for layer in [*before, *self.layers, *after]:
            x = layer(x, m)
        pooled = x.sum(1) / m.sum(1).clamp_min(1)
        context = torch.sigmoid(self.global_gate(pooled)) * pooled
        return torch.cat((x, context.unsqueeze(1).expand_as(x)), -1)

    def emissions_from(self, joined: Tensor) -> Tensor:
        return self.output(torch.tanh(self.head(joined)))

    def emissions(self, rows: Tensor, mask: Tensor) -> Tensor:
        return self.emissions_from(self.hidden(rows, mask))

    def kind_logits(self, joined: Tensor, span: Tensor) -> Tensor:
        """Kind of the question covering `span` (bool, batch x steps): attention pool plus span mean."""
        score = self.kind_attn(joined).squeeze(-1).masked_fill(~span, -1e4)
        attn = torch.softmax(score, 1).unsqueeze(-1)
        pooled = (attn * joined).sum(1)
        mean = (joined * span.unsqueeze(-1)).sum(1) / span.sum(1, keepdim=True).clamp_min(1)
        return self.kind_mlp(torch.cat((pooled, mean), -1))

    def nll(self, emissions: Tensor, labels: Tensor, mask: Tensor) -> Tensor:
        """Linear-chain CRF negative log-likelihood per token; sequences are right-padded."""
        batch, steps, _ = emissions.shape
        mask_f = mask.float()
        alpha = self.start + emissions[:, 0]
        score = self.start[labels[:, 0]] + emissions[:, 0].gather(1, labels[:, :1]).squeeze(1)
        for t in range(1, steps):
            live = mask[:, t]
            step = torch.logsumexp(alpha.unsqueeze(2) + self.transition, dim=1) + emissions[:, t]
            alpha = torch.where(live.unsqueeze(1), step, alpha)
            gold = self.transition[labels[:, t - 1], labels[:, t]] + emissions[:, t].gather(1, labels[:, t:t + 1]).squeeze(1)
            score = score + gold * mask_f[:, t]
        return (torch.logsumexp(alpha, 1) - score).sum() / mask_f.sum()

    @torch.no_grad()
    def decode(self, emissions: Tensor, mask: Tensor) -> list[list[int]]:
        emissions = emissions.float().cpu()
        mask = mask.cpu()
        transition = self.transition.detach().float().cpu()
        best = self.start.detach().float().cpu() + emissions[:, 0]
        pointers = []
        for t in range(1, emissions.shape[1]):
            scores, previous = (best.unsqueeze(2) + transition).max(1)
            scores = scores + emissions[:, t]
            best = torch.where(mask[:, t].unsqueeze(1), scores, best)
            pointers.append(torch.where(mask[:, t].unsqueeze(1), previous, torch.arange(NUM_LABELS).expand_as(previous)))
        out = []
        for b in range(emissions.shape[0]):
            n = int(mask[b].sum())
            label = int(best[b].argmax())
            path = [label]
            for t in range(n - 1, 0, -1):
                label = int(pointers[t - 1][b, label])
                path.append(label)
            out.append(path[::-1])
        return out

    @torch.no_grad()
    def decode_kbest(self, emissions: Tensor, mask: Tensor, k: int = 8) -> list[list[tuple[float, list[int]]]]:
        """For each batch row, the k highest-scoring label paths (score, path), best first."""
        emissions = emissions.float().cpu()
        mask = mask.cpu()
        start = self.start.detach().float().cpu()
        transition = self.transition.detach().float().cpu()
        out = []
        for b in range(emissions.shape[0]):
            n = int(mask[b].sum())
            out.append(kbest_paths(emissions[b, :n], start, transition, k) if n else [])
        return out

    def parameter_count(self) -> int:
        return sum(p.numel() for p in self.parameters())


def kbest_paths(emissions: Tensor, start: Tensor, transition: Tensor, k: int) -> list[tuple[float, list[int]]]:
    """k highest-scoring label paths for one sequence (steps x labels), best first."""
    emissions = emissions.detach().float()
    start = start.detach().float()
    transition = transition.detach().float()
    steps = emissions.shape[0]
    beams = [[(float(start[j] + emissions[0, j]), [j])] for j in range(NUM_LABELS)]
    for t in range(1, steps):
        new = []
        for j in range(NUM_LABELS):
            cand = [(s + float(transition[i, j] + emissions[t, j]), p) for i in range(NUM_LABELS) for s, p in beams[i]]
            cand.sort(key=lambda x: -x[0])
            new.append([(s, p + [j]) for s, p in cand[:k]])
        beams = new
    return sorted((c for beam in beams for c in beam), key=lambda x: -x[0])[:k]


class Ensemble(nn.Module):
    """Averages member emissions and CRF parameters; decodes like a single Tagger."""

    def __init__(self, members: list[Tagger]):
        super().__init__()
        self.members = nn.ModuleList(members)
        self.config = {"members": [m.config for m in members],
                       "kind_head": all(m.config.get("kind_head") for m in members)}
        self.transition = nn.Parameter(torch.stack([m.transition for m in members]).mean(0))
        self.start = nn.Parameter(torch.stack([m.start for m in members]).mean(0))

    def emissions(self, rows: Tensor, mask: Tensor) -> Tensor:
        return torch.stack([m.emissions(rows, mask) for m in self.members]).mean(0)

    def hidden(self, rows: Tensor, mask: Tensor) -> Tensor:
        return torch.stack([m.hidden(rows, mask) for m in self.members]).mean(0)

    def emissions_from(self, joined: Tensor) -> Tensor:
        # Prefer averaging member emissions from their own hiddens; this path is for a shared joined.
        return torch.stack([m.emissions_from(joined) for m in self.members]).mean(0)

    def kind_logits(self, joined: Tensor, span: Tensor) -> Tensor:
        return torch.stack([m.kind_logits(joined, span) for m in self.members]).mean(0)

    decode = Tagger.decode
    decode_kbest = Tagger.decode_kbest

    def parameter_count(self) -> int:
        return sum(m.parameter_count() for m in self.members)


def collate_kind(batch, steps: int, device) -> tuple[Tensor, Tensor]:
    """Kind targets (-1 when a sample has no question) and last-question span masks."""
    kinds = torch.full((len(batch),), -1, dtype=torch.long)
    span = torch.zeros((len(batch), steps), dtype=torch.bool)
    for b, item in enumerate(batch):
        kind, a, z = item[2], item[3], item[4]
        if kind >= 0 and z >= a:
            kinds[b] = kind
            span[b, a: z + 1] = True
    return kinds.to(device), span.to(device)


def collate(batch, device) -> tuple[Tensor, Tensor, Tensor]:
    """Batch items are (rows, labels, ...); extra fields are read by collate_kind."""
    batch = [(item[0], item[1]) for item in batch]
    pad = feature_rows()
    steps = max(1, max(len(rows) for rows, _ in batch))
    width = max(len(r) for rows, _ in batch for r in rows) if any(rows for rows, _ in batch) else 1
    rows_t = torch.full((len(batch), steps, width), pad, dtype=torch.long)
    labels_t = torch.zeros((len(batch), steps), dtype=torch.long)
    mask_t = torch.zeros((len(batch), steps), dtype=torch.bool)
    for b, (rows, labels) in enumerate(batch):
        for t, r in enumerate(rows):
            rows_t[b, t, : len(r)] = torch.tensor(r)
        labels_t[b, : len(labels)] = torch.tensor(labels)
        mask_t[b, : len(rows)] = True
    return rows_t.to(device), labels_t.to(device), mask_t.to(device)
