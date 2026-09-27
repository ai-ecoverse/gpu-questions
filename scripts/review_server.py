"""Spot-check UI for gold/handlabeled.jsonl.

    uv run python scripts/review_server.py [--port 8765] [--checkpoint a.pt,b.pt]

Shows each item with gold spans, the hand-written expectation, and the model's
prediction. Verdicts are appended to gold/review.jsonl (the latest entry per id wins).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import torch  # noqa: E402

from gq.compile import compile_questions  # noqa: E402
from gq.evaluate import norm  # noqa: E402
from gq.labels import LABELS  # noqa: E402
from gq.model import collate  # noqa: E402
from gq.predict import DEFAULT_CHECKPOINT, load  # noqa: E402
from gq.tokenize import features, tail_start, tokenize  # noqa: E402

GOLD = ROOT / "gold" / "handlabeled.jsonl"
REVIEW = ROOT / "gold" / "review.jsonl"
PAGE = Path(__file__).with_name("review.html")


def label_spans(tokens, labels) -> list[list]:
    spans = []
    for tok, lab in zip(tokens, labels):
        name = LABELS[lab]
        if name == "O":
            continue
        kind = name.split("_")[0]
        if spans and spans[-1][2] == kind and not name.endswith("_B"):
            spans[-1][1] = tok.end
        else:
            spans.append([tok.start, tok.end, kind])
    return spans


@torch.no_grad()
def predict_all(model, items):
    out = []
    for item in items:
        text = item["text"]
        tokens = tokenize(text)
        if not tokens:
            out.append(([], []))
            continue
        rows = features(text, tokens)
        cut = tail_start(tokens)
        tokens, rows = tokens[cut:], rows[cut:]
        r, _, m = collate([(rows, [0] * len(rows))], "cpu")
        labels = model.decode(model.emissions(r, m), m)[0]
        questions = [q.to_dict() for q in compile_questions(text, tokens, labels)]
        out.append((label_spans(tokens, labels), questions))
    return out


def disagreement(expected: list[dict], predicted: list[dict]) -> list[str]:
    reasons = []
    if bool(expected) != bool(predicted):
        return ["missed question" if expected else "false question"]
    if not expected:
        return reasons
    if len(expected) != len(predicted):
        reasons.append(f"count {len(expected)}→{len(predicted)}")
    e, p = expected[-1], predicted[-1]
    if e.get("kind") != p.get("kind"):
        reasons.append(f"kind {e.get('kind')}→{p.get('kind')}")
    if [norm(o) for o in e.get("options") or []] != [norm(o) for o in p.get("options") or []]:
        reasons.append("options")
    return reasons


def build(checkpoint: str) -> list[dict]:
    items = [json.loads(line) for line in GOLD.open()]
    preds = predict_all(load(checkpoint), items)
    out = []
    for item, (pspans, pq) in zip(items, preds):
        reasons = disagreement(item["expected"], pq)
        out.append({
            "id": item["id"],
            "dataset": item["dataset"],
            "license": item["license"],
            "agent": item["agent"],
            "session": item["session"],
            "turn": item["turn"],
            "text": item["text"],
            "gold_spans": [s[:3] for s in item["spans"]],
            "expected": item["expected"],
            "difficulty": item.get("difficulty"),
            "ambiguous": bool(item.get("ambiguous")),
            "note": item.get("note") or "",
            "model_spans": pspans,
            "predicted": pq,
            "disagree": reasons,
            "priority": (2 if item.get("ambiguous") else 0) + (1 if reasons else 0),
        })
    return out


def load_reviews() -> dict:
    reviews = {}
    if REVIEW.exists():
        for line in REVIEW.open():
            r = json.loads(line)
            reviews[r["id"]] = r
    return reviews


def make_handler(items: list[dict]):
    payload = json.dumps(items, ensure_ascii=False).encode()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, body: bytes, ctype: str, status: int = 200):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self.send(PAGE.read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/items":
                self.send(payload, "application/json")
            elif self.path == "/api/reviews":
                self.send(json.dumps(load_reviews()).encode(), "application/json")
            else:
                self.send(b"not found", "text/plain", 404)

        def do_POST(self):
            if self.path != "/api/review":
                self.send(b"not found", "text/plain", 404)
                return
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if body.get("verdict") not in ("ok", "wrong", "unsure", None) or not body.get("id"):
                self.send(b'{"ok":false}', "application/json", 400)
                return
            record = {"id": body["id"], "verdict": body.get("verdict"), "comment": (body.get("comment") or "")[:2000],
                      "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
            with REVIEW.open("a") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            self.send(b'{"ok":true}', "application/json")

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--checkpoint", default=",".join(str(ROOT / p) for p in DEFAULT_CHECKPOINT.split(",")))
    args = ap.parse_args()
    items = build(args.checkpoint)
    print(f"{len(items)} items, {sum(1 for i in items if i['priority'])} flagged; http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(items)).serve_forever()


if __name__ == "__main__":
    main()
