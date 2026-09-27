"""Training samples: cleaned text plus character spans labeled Q, OPT or REC.

Labels come from how a sample was built, never from the model, as in gpu-time.
Sources:
  - gold: structured ask-tool questions rendered back into prose
  - weak: real end-of-turn questions labeled by the survey heuristics
  - carrier: real end-of-turn messages without a question (all O)
Splits are by session id so phrasings from one session never cross train/test.
"""

from __future__ import annotations

import json
import random
import re
import zlib
from dataclasses import dataclass, field
from pathlib import Path

from .labels import LABEL_ID
from .tokenize import MAX_TOKENS, clean, features, tail_start, tokenize

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "data" / "export"
HAND = ROOT / "gold" / "handlabeled.jsonl"
HAND2 = ROOT / "gold" / "batch2" / "handlabeled.jsonl"
HAND_SPLIT = ROOT / "gold" / "split.json"

REC_RE = re.compile(r"\s*\((?:recommended|default)\)\s*$", re.I)


@dataclass
class Sample:
    text: str
    spans: list[tuple[int, int, str]] = field(default_factory=list)
    source: str = ""
    kind: str | None = None  # hand-written kind of the last question, when known


def split_of(sid: str, test_fraction: float = 0.2) -> str:
    return "test" if zlib.crc32(sid.encode()) % 1000 < test_fraction * 1000 else "train"


def encode(sample: Sample, limit: int = MAX_TOKENS):
    """Return (tokens, feature rows, label ids) for the modeled tail of a sample."""
    tokens = tokenize(sample.text)
    rows = features(sample.text, tokens)
    labels = [LABEL_ID["O"]] * len(tokens)
    for start, end, kind in sorted(sample.spans):
        first = True
        for i, tok in enumerate(tokens):
            if tok.end <= start or tok.start >= end:
                continue
            if kind == "REC":
                labels[i] = LABEL_ID["REC"]
            elif kind == "OPT":
                labels[i] = LABEL_ID["OPT_B" if first else "OPT_I"]
            elif labels[i] == LABEL_ID["O"]:
                labels[i] = LABEL_ID["Q_B" if first else "Q_I"]
            first = False
    cut = tail_start(tokens, limit)
    return tokens[cut:], rows[cut:], labels[cut:]


# ----------------------------------------------------------------- loading
def load_jsonl(path: Path) -> list[dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh]


def load_hand(part: str) -> list[dict]:
    """Hand-labeled public turns for one side of gold/split.json (split by dataset)."""
    if not HAND.exists():
        return []
    split = json.loads(HAND_SPLIT.read_text())
    datasets = set(split[f"{part}_datasets"])
    return [r for r in load_jsonl(HAND) if r["dataset"] in datasets]


def hand3_paths() -> list[Path]:
    """Batch-3 outputs, one per labeler (gold/batch3/<labeler>/handlabeled.jsonl)."""
    return sorted(ROOT.glob("gold/batch3/*/handlabeled.jsonl"))


def load_hand_dev() -> list[dict]:
    """Every hand-labeled turn except the untouched batch-2 test set: batches 1 and 3 plus batch-2 development."""
    test = set(json.loads(HAND_SPLIT.read_text()).get("batch2_test_datasets", []))
    records = load_jsonl(HAND) if HAND.exists() else []
    if HAND2.exists():
        records += [r for r in load_jsonl(HAND2) if r["dataset"] not in test]
    for path in hand3_paths():
        records += load_jsonl(path)
    return records


def load_hand_test() -> list[dict]:
    """The untouched batch-2 test set. Score it only at milestones, never while tuning."""
    test = set(json.loads(HAND_SPLIT.read_text()).get("batch2_test_datasets", []))
    return [r for r in load_jsonl(HAND2) if r["dataset"] in test] if HAND2.exists() else []


def load_hand_test4() -> list[dict]:
    """The batch-4 test set: new owners only, never used for training, teachers, or static vectors."""
    return [r for p in sorted(ROOT.glob("gold/batch4/*/handlabeled.jsonl")) for r in load_jsonl(p)]


def load_hand_fold(fold: int, side: str) -> list[dict]:
    """Cross-validation view over load_hand_dev(): side "test" is one owner-grouped fold, "train" the others."""
    folds = json.loads(HAND_SPLIT.read_text())["cv_folds"]
    return [r for r in load_hand_dev() if (folds[r["dataset"]] == fold) == (side == "test")]


def load_silver(pattern: str, fold: int | None = None) -> list[dict]:
    """LLM-labeled turns matching `pattern` (e.g. "silver/[0-9]*/labeled.jsonl"), deduplicated by id.

    Privacy drops are skipped. With a fold, turns from that fold's datasets are left out so they
    cannot leak into its held-out evaluation; synthetic and unassigned datasets are always kept.
    """
    folds = json.loads(HAND_SPLIT.read_text())["cv_folds"] if fold is not None else {}
    seen, out = set(), []
    for path in sorted(ROOT.glob(pattern)):
        for r in load_jsonl(path):
            if r["id"] in seen or r.get("note", "").startswith("drop"):
                continue
            if fold is not None and folds.get(r["dataset"]) == fold:
                continue
            seen.add(r["id"])
            out.append(r)
    return out


def hand_sample(r: dict) -> Sample:
    kind = r["expected"][-1]["kind"] if r.get("expected") else None
    return Sample(r["text"], [(a, b, k) for a, b, k, *_ in r["spans"]], source=r["id"], kind=kind)


def kind_target(sample: Sample, tokens, labels) -> tuple[int, int, int]:
    """(kind id, first token, last token) of the last question in the encoded tail; kind -1 if none."""
    from .compile import compile_questions
    from .model import KINDS

    questions = compile_questions(sample.text, tokens, labels)
    if not questions:
        return -1, 0, -1
    q = questions[-1]
    inside = [i for i, t in enumerate(tokens) if t.start < q.span[1] and t.end > q.span[0]]
    if not inside:
        return -1, 0, -1
    kind = sample.kind or q.kind
    return KINDS.index(kind), inside[0], inside[-1]


def load_sources():
    gold = load_jsonl(EXPORT / "gold.jsonl")
    eot = load_jsonl(EXPORT / "eot.jsonl")
    out = {}
    for part in ("train", "test"):
        g = [r for r in gold if split_of(r["sid"]) == part and len(r["options"]) >= 2]
        e = [r for r in eot if split_of(r["sid"]) == part]
        carriers = [clean(r["tail"]) for r in e if not r["is_question"] and "?" not in r["tail"][-400:]]
        carriers = [c for c in carriers if 40 < len(c)]
        hard = [t for t in (clean(r["tail"]) for r in e if not r["is_question"]) if only_embedded_qmarks(t)]
        out[part] = {"gold": g, "eot": e, "carriers": carriers, "hard_real": hard,
                     "hand": [hand_sample(r) for r in load_hand(part)]}
    return out


# ------------------------------------------------------ weak real labels
ABBREV_RE = re.compile(r"(?:\be\.g|\bi\.e|\b[ei]|\bvs|\betc|\bcf|\d)\.$", re.I)


def last_question_span(text: str) -> tuple[int, int] | None:
    """Span of the last sentence ending in '?', skipping list markers and markdown emphasis."""
    end = text.rfind("?")
    if end < 0:
        return None
    begin = end
    while begin > 0:
        ch = text[begin - 1]
        if ch == "." and ABBREV_RE.search(text[:begin]):
            begin -= 1
            continue
        if ch in ".!?\n":
            break
        begin -= 1
    while begin < end and text[begin] in " \t*_-•>#":
        begin += 1
    m = re.match(r"(?:\d{1,2}[.)]|[A-Za-z][.)]|\([A-Za-z0-9]\))\s+", text[begin:end])
    if m:
        begin += m.end()
    return (begin, end + 1) if end + 1 - begin > 3 else None


def weak_sample(rec: dict) -> Sample | None:
    """Label a real end-of-turn question from the survey heuristics, or skip it."""
    text = clean(rec["tail"])
    if not rec["is_question"]:
        return Sample(text, [], "weak_negative") if "?" not in text else None
    # List-option heuristics are too noisy to train on (reading lists, status lists).
    if "rhetorical_suspect" in rec.get("flags", []) or rec["cls"] in ("multi_question", "other", "multi_choice"):
        return None
    last_para = text[text.rfind("\n\n") + 1:] if "\n\n" in text else text
    if last_para.count("?") != 1:
        return None
    q = last_question_span(text)
    if not q or not text[q[0]].isupper():
        return None
    line_start = text.rfind("\n", 0, q[0]) + 1
    if re.match(r"\s*(?:[-*•]|\d{1,2}[.)])\s", text[line_start:q[0] + 1]) or text[:q[0]].rstrip().endswith(":"):
        return None
    spans = [(q[0], q[1], "Q")]
    if rec["cls"] == "either_or":
        sentence = text[q[0]:q[1]]
        for opt in rec["options"]:
            k = sentence.find(opt)
            if k < 0 or len(opt) < 2:
                return None
            spans.append((q[0] + k, q[0] + k + len(opt), "OPT"))
    return Sample(text, spans, f"weak_{rec['cls']}")


# ---------------------------------------------------------- synthetic gold
LIST_STYLES = [
    lambda i: f"{i + 1}. ",
    lambda i: f"{i + 1}) ",
    lambda i: "- ",
    lambda i: "* ",
    lambda i: f"{'ABCDEFG'[i]}) ",
    lambda i: f"**{'ABCDEFG'[i]}.** ",
    lambda i: f"({'abcdefg'[i]}) ",
    lambda i: f"**Option {'ABCDEFG'[i]}:** ",
]
LIST_INTROS = ["Options:", "A few ways to go:", "I see a few paths:", "We could either:", "Choices:",
               "Here's what I can do:", "Possible approaches:", "Two ways to handle this:", ""]
LIST_QUESTIONS = ["Which do you prefer?", "Which one should I go with?", "Which approach would you like?",
                  "Which of these?", "Which way do you want to go?", "What's your preference?",
                  "Which should I pick?", "Which one?", "Let me know which you'd like — which one?",
                  "Want me to tackle any of these?", "Should I start on any of these?",
                  "What would you like to focus on?", "What would you like to do?"]
INLINE_LEADS = ["Options: ", "I can ", "Either ", "Choices are: ", "I could ", "Should I ", ""]
INLINE_QUESTIONS = ["Want me to {x}?", "Should I {x}?", "Do you want me to {x}?", "Would you like me to {x}?",
                    "Shall I {x}?", "Do you prefer {x}?", "{X}?", "Which is it: {x}?", "Prefer {x}?",
                    "Should we {x}?"]
YESNO_QUESTIONS = ["Want me to {a}?", "Should I {a}?", "Shall I {a}?", "Do you want me to {a}?",
                   "Would you like me to {a}?", "Okay to {a}?", "Should I go ahead and {a}?", "Can I {a}?"]
RHETORICAL = ["Why does this matter?", "What changed?", "So what's the fix?", "Why not just {w}?", "What about {w}?",
              "Is it worth it?", "How does {w} work?", "Does {w} matter?", "What went wrong?", "Why {w}?",
              "So where does that leave us?", "The real question: {w}?", "Which one wins?", "How bad is it?",
              "What does {w} actually do?", "Could {w} be the cause?", "Is {w} enough?", "Why is this hard?"]
SELF_ANSWERS = ["Because {s}", "Short answer: {s}", "Not really. {s}", "Yes — {s}", "No. {s}", "Mostly. {s}",
                "It turns out {s}", "{s}", "{s}", "Honestly, {s}", "In practice, {s}"]
QUOTE_LEADS = ["You asked: “{q}”", "Your question was \"{q}\"", "The prompt was: \"{q}\"",
               "Re “{q}” —", "(the user asked: \"{q}\")", "The issue title is \"{q}\"."]
CODE_QMARKS = ["`{w}?.value`", "`a ?? b`", "`?debug=1`", "`Option<{w}>?`", "`user?.name`", "`[URL]?page=2`",
               "`/api/search?q={w}`", "`{w}()?`", "`x ? y : z`", "`isReady?`"]
SELF_REVIEW_LEADS = ["Before submitting, ask yourself:", "A quick checklist for next time:", "Questions worth asking:",
                     "When reviewing, check:"]
JOKES = ["A SQL query walks into a bar, approaches two tables, and asks: \"Mind if I join you?\"",
         "Why do programmers prefer dark mode? Because light attracts bugs.",
         "How many engineers does it take to change a light bulb? None, that's a hardware problem."]
EMBEDDED_Q_RE = re.compile(r"`[^`\n]*`|\"[^\"\n]*\"|“[^”\n]*”|^\|.*$|\?(?=[^\s)*_\"”'`])", re.M)


def only_embedded_qmarks(text: str) -> bool:
    """True when every '?' sits in inline code, a quote, a table row, or mid-token (`a?.b`, `?q=`)."""
    return "?" in text and "?" not in EMBEDDED_Q_RE.sub("", text)
INLINE_MULTI_HEADS = ["Which package(s) should I work on", "Which module do you want", "Which {n} should I start with",
                      "Which one should I target", "Want me to focus on one area", "Which deck did you want to try",
                      "Which of these should I tackle first", "Should it", "Which {n} do you mean",
                      "Anything you'd like next", "Which environment should I use"]
OFFER_LIST_LEADS = ["Would you like me to:", "Do you want me to:", "Want me to:", "Should I:", "Next, I could:",
                    "Would you like to:", "What would you like me to do next? I can:", "Shall I:"]
CLAUSE_PAIRS = [("Want me to ", ", or would you like to ", "?"), ("Want me to ", "? Or shall we ", "?"),
                ("Should I ", ", or would you rather ", "?"), ("Want me to ", ", or do you want to ", "?"),
                ("Do you want me to ", ", or should I ", "?"), ("Want to ", ", or should I ", "?"),
                ("Should I ", "? Or ", "?"), ("Would you like me to ", ", or would you prefer to ", "?"),
                ("Want me to ", ", or should we ", " first?"), ("Want me to ", ", or would you rather ", "?")]
OFFER_LEADS = ["I can ", "If you want, I can ", "Next I could ", "I could either ", "Happy to "]
OFFER_QUESTIONS = ["Which do you prefer?", "Which do you want?", "Which route do you prefer?",
                   "What's your read?", "Which would you like?", "Your call — which one?"]
ESCAPES = [", or do you have a preference", ", or do you have a different idea", ", or something else",
           ", or do you have something else in mind"]
REC_MARKERS = [" (recommended)", " (Recommended)", " (default)", " — recommended", " (my pick)"]
TRAILERS = ["", "", "", " Otherwise I'll leave it as is.", " No rush.", " Happy to do either.",
            " I'd lean toward the first.", " Let me know."]


def _lower_first(s: str) -> str:
    return s[:1].lower() + s[1:] if s[:2] != s[:2].upper() else s


class Builder:
    """Appends text while recording spans in the final string's coordinates."""

    def __init__(self):
        self.text = ""
        self.spans: list[tuple[int, int, str]] = []

    def add(self, s: str, kind: str | None = None):
        if kind and s.strip():
            lead = len(s) - len(s.lstrip())
            self.spans.append((len(self.text) + lead, len(self.text) + len(s.rstrip()), kind))
        self.text += s

    def mark(self, start: int, kind: str):
        self.spans.append((start, len(self.text), kind))


def split_gold_question(q: str) -> tuple[str, str]:
    """Split a gold question into leading context and the final asking sentence."""
    q = clean(q)
    span = last_question_span(q)
    if not span:
        return q + " ", ""
    return q[: span[0]], q[span[0]: span[1]]


def gold_options(rec: dict) -> tuple[list[str], int | None]:
    opts, rec_index = [], None
    for i, o in enumerate(rec["options"]):
        stripped = REC_RE.sub("", o).strip()
        if stripped != o.strip() and rec_index is None:
            rec_index = i
        opts.append(stripped)
    return [o for o in opts if o], rec_index


class Generator:
    def __init__(self, sources: dict, rng: random.Random, augment_options: bool = True, hand_rate: float = 0.0,
                 hard_rate: float = 0.12, hand_augment: bool = False, distill_rate: float = 0.0,
                 distill_pos: float | None = None):
        self.s = sources
        self.rng = rng
        self.hand_rate = hand_rate
        self.distill_rate = distill_rate
        self.distill_pos = distill_pos
        distill = sources.get("distill") or []
        self.distill_split = ([s for s in distill if any(k == "Q" for _, _, k in s.spans)],
                              [s for s in distill if not any(k == "Q" for _, _, k in s.spans)])
        self.hand_augment = hand_augment
        self.hard_rate = hard_rate
        self.weak = [w for w in (weak_sample(r) for r in sources["eot"]) if w]
        self.weak_pos = [w for w in self.weak if w.source != "weak_negative"]
        self.augment_options = augment_options
        self.option_pool = [o for r in sources["gold"] for o in gold_options(r)[0]]
        self.sentences = [s.strip() for c in sources["carriers"] for s in re.split(r"(?<=[.!])\s+|\n+", c)
                          if 4 <= len(s.split()) <= 40 and "[CODE]" not in s]

    def prose_option(self) -> str:
        """A random word window from real agent prose; teaches boundaries without memorized words."""
        words = self.rng.choice(self.sentences).split()
        n = self.rng.randint(1, min(12, len(words)))
        start = self.rng.randint(0, len(words) - n)
        text = " ".join(words[start:start + n]).strip(" ,;:.-*_`")
        return (text[:1].upper() + text[1:] if self.rng.random() < 0.5 else text) or "skip"

    def options_for(self, rec: dict) -> tuple[list[str], int | None]:
        opts, rec_index = gold_options(rec)
        r = self.rng.random()
        if r < 0.45 or not self.sentences:
            return opts, rec_index
        n = self.rng.choice([2, 2, 3, 3, 3, 4])
        mixed = []
        for _ in range(n):
            mixed.append(self.rng.choice(self.option_pool) if self.rng.random() < 0.4 else self.prose_option())
        return mixed, (0 if self.rng.random() < 0.4 else None)

    def carrier(self, b: Builder):
        if not self.s["carriers"] or self.rng.random() < 0.15:
            return
        c = self.rng.choice(self.s["carriers"])
        paras = [p for p in re.split(r"\n\s*\n", c) if p.strip()]
        take = paras[-self.rng.randint(1, min(3, len(paras))):]
        b.add("\n\n".join(take) + self.rng.choice(["\n\n", "\n\n", " "]))

    def option(self, b: Builder, text: str, rec: bool, lower: bool = False):
        start = len(b.text)
        b.add(_lower_first(text) if lower else text, "OPT")
        if rec:
            marker = self.rng.choice(REC_MARKERS)
            b.add(marker[: len(marker) - len(marker.lstrip())])
            b.add(marker.lstrip(), "REC")
        return start

    def render_list(self, b: Builder, opts: list[str], rec_index: int | None, rec_on: bool):
        style = self.rng.choice(LIST_STYLES)
        bold = self.rng.random() < 0.2
        for i, o in enumerate(opts):
            b.add(style(i))
            b.add("**" if bold else "")
            self.option(b, o, rec_on and i == rec_index)
            b.add("**" if bold else "")
            if self.rng.random() < 0.15:
                b.add(self.rng.choice([" — quickest.", " — safest.", ": more work but cleaner.", " (keeps scope small)"]))
            b.add("\n")

    def inline_opts(self, b: Builder, opts: list[str], rec_index: int | None, rec_on: bool, lower: bool):
        for i, o in enumerate(opts):
            if i:
                last = i == len(opts) - 1
                b.add(self.rng.choice([", or ", " or "] if last else [", "]))
            self.option(b, o, rec_on and i == rec_index, lower)

    def gold(self) -> Sample:
        rec = self.rng.choice(self.s["gold"])
        opts, rec_index = self.options_for(rec) if self.augment_options else gold_options(rec)
        if len(opts) < 2:
            return self.negative()
        context, ask = split_gold_question(rec["question"])
        # An ask that already offers "A or B" would need its own option spans; drop it.
        if re.search(r"\bor\b", ask):
            ask = ""
        rec_on = rec_index is not None and self.rng.random() < 0.6
        b = Builder()
        self.carrier(b)
        style = self.rng.random()
        if not ask:
            style = 0.9  # no usable question sentence: use a generic list question
        if context and self.rng.random() < 0.8:
            b.add(context)
        verbish = not any(re.match(r"(?:yes|no|i'll|i|you|don't|we)\b", o, re.I) for o in opts)
        if len(opts) == 2 and verbish and self.rng.random() < 0.3:
            self.clause_pair(b, opts, rec_index if rec_on else None)
        elif style < 0.35:  # question, then list
            b.add(ask, "Q")
            b.add(self.rng.choice(["\n\n", "\n"]))
            self.render_list(b, opts, rec_index, rec_on)
        elif style < 0.55:  # question, then inline options sentence
            b.add(ask, "Q")
            lead = self.rng.choice(INLINE_LEADS)
            b.add(" " + lead)
            self.inline_opts(b, opts, rec_index, rec_on, lower=bool(lead))
            b.add(self.rng.choice(["?", ".", ""]))
        elif style < 0.8 and len(opts) <= 3:  # options inside the question sentence
            template = self.rng.choice(INLINE_QUESTIONS)
            head, tail = template.split("{x}") if "{x}" in template else template.split("{X}")
            start = len(b.text)
            b.add(head)
            self.inline_opts(b, opts, rec_index, rec_on, lower=bool(head) or "{x}" in template)
            if tail == "?" and self.rng.random() < 0.2:
                tail = self.rng.choice([", or something else?", ", or something else entirely?"])
            b.add(tail)
            b.mark(start, "Q")
        else:  # list, then question
            intro = self.rng.choice(LIST_INTROS)
            if intro:
                b.add(intro + "\n")
            self.render_list(b, opts, rec_index, rec_on)
            b.add("\n")
            b.add(ask if ask and self.rng.random() < 0.4 else self.rng.choice(LIST_QUESTIONS), "Q")
        b.add(self.rng.choice(TRAILERS))
        self.trailing_prose(b)
        return Sample(b.text.strip(), b.spans, "gold")

    def clause_pair(self, b: Builder, opts: list[str], rec_index: int | None):
        """Two choices as separate clauses: "Want me to A, or would you like to B?" or "I can A, or B. Which?"."""
        a, c = (_lower_first(o) for o in opts)
        head, mid, tail = self.rng.choice(CLAUSE_PAIRS)
        if self.rng.random() < 0.3:  # the options sit in a statement before the question
            b.add(self.rng.choice(OFFER_LEADS))
            self.option(b, a, rec_index == 0)
            b.add(self.rng.choice([", or ", " or ", ", or I can "]))
            self.option(b, c, rec_index == 1)
            b.add(". ")
            b.add(self.rng.choice(OFFER_QUESTIONS), "Q")
            return
        start = len(b.text)
        b.add(head)
        self.option(b, a, rec_index == 0)
        b.add(mid)
        self.option(b, c, rec_index == 1)
        b.add(tail)
        # "…? Or shall we B?" is one question for the UI; the Q span covers both sentences.
        b.mark(start, "Q")

    def trailing_prose(self, b: Builder):
        """Real asks are sometimes followed by context, so a trailing statement alone must not veto a question."""
        if self.rng.random() < 0.15:
            b.add("\n\n" + self.sentence())

    def yes_no(self) -> Sample:
        rec = self.rng.choice(self.s["gold"])
        opts, _ = gold_options(rec)
        b = Builder()
        self.carrier(b)
        action = _lower_first(self.rng.choice(opts))
        ask = self.rng.choice(YESNO_QUESTIONS).format(a=action)
        if self.rng.random() < 0.15:
            ask = ask[:-1] + self.rng.choice(ESCAPES) + "?"
        b.add(ask, "Q")
        b.add(self.rng.choice(TRAILERS))
        self.trailing_prose(b)
        return Sample(b.text.strip(), b.spans, "synthetic_yes_no")

    def offer_list(self) -> Sample:
        """"Would you like me to:\\n1. A?\\n2. B?" is one question whose items are the options."""
        rec = self.rng.choice(self.s["gold"])
        opts, _ = self.options_for(rec)
        if len(opts) < 2:
            return self.yes_no()
        opts = opts[:5]
        b = Builder()
        self.carrier(b)
        start = len(b.text)
        b.add(self.rng.choice(OFFER_LIST_LEADS) + "\n")
        style = self.rng.choice(LIST_STYLES[:4])
        bold = self.rng.random() < 0.35
        for i, o in enumerate(opts):
            b.add(style(i))
            if bold:
                b.add("**")
                b.add(o, "OPT")
                b.add("**")
                if self.rng.random() < 0.5:
                    b.add(" " + self.rng.choice(["(e.g., " + self.phrase() + ")", "for " + self.phrase(),
                                                  "— " + self.phrase()]))
            else:
                b.add(_lower_first(o) if self.rng.random() < 0.3 else o, "OPT")
            b.add("?" if i == len(opts) - 1 or self.rng.random() < 0.85 else "")
            if i < len(opts) - 1:
                b.add("\n")
        b.mark(start, "Q")
        b.add(self.rng.choice(["", "\n\nLet me know!", "\n\nHappy to do any of these."]) if self.rng.random() < 0.5 else "")
        return Sample(b.text.strip(), b.spans, "offer_list")

    def short_item(self) -> str:
        words = re.sub(r"[`*\[\]()|#]", "", self.prose_option()).split()[: self.rng.randint(1, 3)]
        item = " ".join(words).strip(" ,;:.") or "core"
        return f"`{item}`" if self.rng.random() < 0.4 else item

    def inline_multi(self) -> Sample:
        """Many short choices inside or right after one question sentence."""
        items = [self.short_item() for _ in range(self.rng.randint(3, 7))]
        b = Builder()
        self.carrier(b)
        start = len(b.text)
        b.add(self.rng.choice(INLINE_MULTI_HEADS).format(n=self.phrase().split(" ")[0]))
        style = self.rng.random()
        if style < 0.55:  # "…: a, b, c, or d?"
            b.add(": " if self.rng.random() < 0.6 else " — ")
            for i, item in enumerate(items):
                if i:
                    b.add(self.rng.choice([", or ", " or "]) if i == len(items) - 1 else ", ")
                b.add(item, "OPT")
            if self.rng.random() < 0.2:
                b.add(", or something else")
            b.add("?")
            b.mark(start, "Q")
        elif style < 0.8:  # "…? (a, b, c)"
            b.add("?")
            b.mark(start, "Q")
            b.add(" (")
            for i, item in enumerate(items):
                b.add(", " if i else "")
                b.add(item, "OPT")
            b.add(")")
        else:  # "…: (1) a, (2) b, or (3) c?"
            b.add(" ")
            for i, item in enumerate(items[:4]):
                if i:
                    b.add(", or " if i == min(4, len(items)) - 1 else ", ")
                b.add(f"({i + 1}) ")
                b.add(self.phrase() if self.rng.random() < 0.5 else item, "OPT")
            b.add("?")
            b.mark(start, "Q")
        b.add(self.rng.choice(TRAILERS))
        return Sample(b.text.strip(), b.spans, "inline_multi")

    def multi_question(self) -> Sample:
        b = Builder()
        self.carrier(b)
        b.add(self.rng.choice(["A couple of questions:\n\n", "Open questions:\n", "Two things to decide:\n\n"]))
        for i in range(self.rng.randint(2, 3)):
            rec = self.rng.choice(self.s["gold"])
            opts, _ = gold_options(rec)
            _, ask = split_gold_question(rec["question"])
            b.add(f"{i + 1}. ")
            start = len(b.text)
            if ask and self.rng.random() < 0.5:
                b.add(ask)
            else:
                b.add(self.rng.choice(["Should I ", "Do you want ", "Prefer "]))
                self.inline_opts(b, opts[:2], None, False, lower=True)
                b.add("?")
            b.mark(start, "Q")
            b.add("\n")
        return Sample(b.text.strip(), b.spans, "multi_question")

    def negative(self) -> Sample:
        b = Builder()
        self.carrier(b)
        if not b.text:
            b.add(self.rng.choice(self.s["carriers"]))
        return Sample(b.text.strip(), [], "negative")

    def sentence(self) -> str:
        return self.rng.choice(self.sentences) if self.sentences else "That part is already handled."

    def phrase(self) -> str:
        return _lower_first(self.prose_option())

    def hard_negative(self) -> Sample:
        """Text with question marks that ask the user nothing: rhetorical, quoted, code, jokes, checklists."""
        hard = self.s.get("hard_real") or []
        if hard and self.rng.random() < 0.25:
            return Sample(self.rng.choice(hard), [], "hard_negative")
        b = Builder()
        self.carrier(b)
        r = self.rng.random()
        if r < 0.35:  # rhetorical question the agent answers itself, possibly as a heading
            q = self.rng.choice(RHETORICAL).format(w=self.phrase())
            if self.rng.random() < 0.35:
                mark = self.rng.choice(["## ", "### ", "**"])
                b.add(mark + q + ("**" if mark == "**" else "") + "\n\n")
            else:
                b.add(q + " ")
            s = self.sentence()
            b.add(self.rng.choice(SELF_ANSWERS).format(s=_lower_first(s)))
        elif r < 0.55:  # quoted question
            _, ask = split_gold_question(self.rng.choice(self.s["gold"])["question"])
            b.add(self.rng.choice(QUOTE_LEADS).format(q=ask or "Can you check this?") + " " + self.sentence())
        elif r < 0.75:  # question marks inside code
            b.add(self.sentence().rstrip(".") + ", using " + self.rng.choice(CODE_QMARKS).format(w=self.phrase().split(" ")[0]) + ".")
        elif r < 0.9:  # self-review checklist given as advice
            b.add(self.rng.choice(SELF_REVIEW_LEADS) + "\n")
            for _ in range(self.rng.randint(2, 3)):
                b.add("- " + self.rng.choice(RHETORICAL).format(w=self.phrase()) + "\n")
        else:
            b.add(self.rng.choice(JOKES))
        # A closing statement after the '?' is what separates these from real asks.
        b.add("\n\n" + self.sentence() if self.rng.random() < 0.8 else "")
        return Sample(b.text.strip(), [], "hard_negative")

    def augment_hand(self, s: Sample) -> Sample:
        """Real structure, fresh words: swap option texts and the leading context, remapping spans."""
        edits = []  # (start, end, replacement), non-overlapping
        if s.spans and self.rng.random() < 0.5:
            first = min(a for a, _, _ in s.spans)
            cut = s.text.rfind("\n\n", 0, first)
            if cut > 0:
                prefix = ""
                if self.s["carriers"] and self.rng.random() < 0.7:
                    c = self.rng.choice(self.s["carriers"])
                    prefix = "\n\n".join([p for p in re.split(r"\n\s*\n", c) if p.strip()][-2:])
                edits.append((0, cut, prefix))
        if self.rng.random() < 0.5:
            for a, b, kind in s.spans:
                if kind == "OPT" and self.rng.random() < 0.6:
                    new = self.rng.choice(self.option_pool) if self.rng.random() < 0.4 else self.prose_option()
                    edits.append((a, b, new.replace("\n", " ")))
        if not edits:
            return s
        edits.sort()

        def shift(pos: int) -> int:
            return pos + sum(len(new) - (b - a) for a, b, new in edits if b <= pos)

        text, last = [], 0
        for a, b, new in edits:
            text.append(s.text[last:a])
            text.append(new)
            last = b
        text.append(s.text[last:])
        spans = [(shift(a), shift(b), k) for a, b, k in s.spans]
        return Sample("".join(text), spans, s.source, s.kind)

    def sample(self) -> Sample:
        r = self.rng.random()
        hand = self.s.get("hand") or []
        if hand and r < self.hand_rate:
            s = self.rng.choice(hand)
            return self.augment_hand(s) if self.hand_augment else s
        distill = self.s.get("distill") or []
        if distill and self.rng.random() < self.distill_rate:
            pos, neg = self.distill_split
            if self.distill_pos is not None and pos and neg:
                s = self.rng.choice(pos if self.rng.random() < self.distill_pos else neg)
            else:
                s = self.rng.choice(distill)
            return self.augment_hand(s) if self.hand_augment else s
        r = self.rng.random()
        if r < 0.40:
            return self.gold()
        if r < 0.50:
            return self.yes_no()
        if r < 0.49:
            return self.multi_question()
        if r < 0.52:
            return self.inline_multi()
        if r < 0.55:
            return self.offer_list()
        if r < 0.63:
            return self.negative()
        if r < 0.63 + self.hard_rate:
            return self.hard_negative()
        return self.rng.choice(self.weak if self.rng.random() < 0.3 else self.weak_pos)
