"""Turn token roles into structured questions. Deterministic, no model involved."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .labels import LABELS
from .tokenize import KIND_NL, KIND_PARA, Token

# A wh-word first, or right after a short lead-in ("Ready — what…", "Now: which…", "So, how…").
WH_START_RE = re.compile(
    r"^\W*(?:(?:ok(?:ay)?|so|and|now|ready|great|alright|also|then)\W+)?(what|which|where|when|why|how|who|whose|whom)\b",
    re.I)
PROPOSE_RE = re.compile(
    r"\b(want me to|should i|shall i|would you like me to|do you want me to|can i|may i|okay to|ok to|should we|shall we)\b",
    re.I,
)
# Offers that do not say "me to": "Would you like a diff?", "Want the timeout adjusted?", "Need help with…?",
# plus common French and Chinese offer forms.
OFFER_RE = re.compile(
    r"\bwould you (?:also )?like (?:a|an|the|some|more|help|me|us|recommendations|examples?|guidance|assistance)\b|"
    r"^\W*want (?:a|an|the|another|some|more|diffs?|help|it|them|this|that)\b|"
    r"\bdo you want (?:help|more|another)\b|\bwould you like to proceed\b|"
    r"\bneed (?:any )?help\b|\bready (?:to (?:proceed|go|start|move on|publish|implement)|for)\b|"
    r"^\W*(?:sound (?:right|good)|ok(?:ay)?|good to go|do you (?:agree|approve))\b|"
    r"\bis there anything (?:else )?(?:i can|you(?:'d| would) like me)\b|"
    r"\b(?:voulez-vous|veux-tu|souhaites-tu|souhaitez-vous) que (?:je|j'|nous|on)|\btu veux que (?:je|j'|on)|"
    r"\btu veux qu'on|要我|需要我|我可以帮",
    re.I,
)
MULTI_RE = re.compile(r"\b(and/or|which ones|any of|all of these|pick several|select all)\b", re.I)


def is_proposal(prompt: str) -> bool:
    """Yes means the assistant acts. Wh-questions ("How can I help?", "Which module should I work on?")
    gather information or a preference, so they are not proposals even when they say "should I"."""
    if WH_START_RE.search(prompt):
        return False
    return bool(PROPOSE_RE.search(prompt) or OFFER_RE.search(prompt))


@dataclass
class Question:
    prompt: str
    kind: str
    propose: bool
    options: list[str] = field(default_factory=list)
    default: int | None = None
    multi_select: bool = False
    span: tuple[int, int] = (0, 0)

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "propose": self.propose,
            "prompt": self.prompt,
            "options": self.options,
            "default": self.default,
            "multiSelect": self.multi_select,
            "span": list(self.span),
        }


REC_TAIL_RE = re.compile(r"\s*(?:\((?:recommended|default|my pick)\)|—\s*recommended)\s*$", re.I)


REC_HEAD_RE = re.compile(r"^\s*(?:my\s+)?(?:recommendation|suggestion|pick)\s*[:—-]\s*", re.I)


def _clean_option(s: str) -> str:
    s = REC_TAIL_RE.sub("", s.replace("**", "").replace("__", ""))
    s = REC_HEAD_RE.sub("", s)
    s = re.sub(r"^\s*\(\d{1,2}\)\s*", "", s)
    if s.count("(") != s.count(")"):
        s = s.strip("()")
    s = s.strip().strip("*_\"'“”:").strip()
    if s.count("`") % 2:
        s = s.replace("`", "")
    elif s.count("`") == 2 and s.startswith("`") and s.endswith("`"):
        s = s[1:-1]
    return s.strip().strip("*_\"'“”:").strip()


QMARK_RE = re.compile(r"[?？]")
# "…, or something else?" and "…, or do you have a preference?" leave the choice open; they are not options.
ESCAPE_RE = re.compile(
    r"^(?:(?:something|anything)(?: else)?\b|(?:do )?you have (?:a|any)\b.*\b(?:preference|take|idea|thought|suggestion)s?\b|"
    r"other\b|neither\b|none of (?:these|the above)\b|your call\b)", re.I)
OPEN_ASK_RE = re.compile(
    r"^\W*(?:(?:could|can|would) you (?:please )?(?:clarify|share|tell me|let me know|specify|provide|describe|paste|"
    r"point me)\b|(?:could|can) you (?:please )?confirm (?:how|what|which|where|who|when)\b)",
    re.I)
# Information requests that do not start with a wh-word (CONVENTIONS: "An open information request is open,
# even when it begins Could you, Can you, or Do you remember").
WH_AFTER_LEAD_RE = re.compile(
    r"^[^?]{0,60}?(?:[,:!—–]|\b(?:if so|in the meantime|also|and|now))\s*(?:what|which|where|when|why|how|who)\b", re.I)
REQUEST_RE = re.compile(
    r"\b(?:could|can|would) you (?:please )?(?:also )?(?:provide|share|list|give|send|drop|paste|"
    r"tell me|let me know|point me|specify|describe|confirm (?:the|your|which|what|how|where))\b|"
    r"\band (?:share|paste|send) (?:the|me|it|your)\b|"
    r"^\W*do you (?:remember|recall)\b|^\W*do you know (?:what|which|where|how|who|when|the)\b|"
    r"^\W*do you have (?:the|a|any) (?:specific |exact )?[\w -]{0,30}?\b(?:id|url|name|path|link|version|handy)\b|"
    r"\bne yap|\bne\s*[?？]|"
    r"\b(?:could|can|would) you (?:please )?(?:rephrase|restate|clarify|explain|elaborate|post)\b|"
    r"^\W*do you have (?:any )?(?:idea|sense)\b|"
    r"^\W*(?:and )?any (?:thoughts|feedback|ideas)\b|"
    r"^\W*(?:quel(?:le)?s?|combien|comment|où|pourquoi|qu['’]est-ce)\b|\b(?:tu as|as-tu|avez-vous) combien\b|"
    r"有什么|什么|哪(?:个|些|里)|怎么|多少",
    re.I)


def is_open(prompt: str) -> bool:
    return bool(WH_START_RE.search(prompt) or OPEN_ASK_RE.search(prompt) or WH_AFTER_LEAD_RE.search(prompt)
                or REQUEST_RE.search(prompt))


ENUM_RE = re.compile(r"\(\d{1,2}\)\s*|\b[a-z]\)\s+")
OR_AFTER_RE = re.compile(r"\s*,?\s+or\s+(?!something\b|anything\b|not\b|do you have\b|you have\b)")
OR_BEFORE_RE = re.compile(r"(?:,\s*|\s+)or\s+$")
PAIR_END_RE = re.compile(r"[?？]|,\s|;|\s\(|\s—|$")
PAIR_LEAD_RE = re.compile(
    r"(?:\b(?:want me to|should i|shall i|would you like me to|do you want me to|do you want|would you prefer|"
    r"do you prefer|prefer|like me to|either|between)\s+|[:—(]\s*)", re.I)


def _complete_pair(text: str, q: dict, opt: dict) -> list[dict]:
    """A lone option inside "A, or B?" means the tagger missed the other side; recover it from the prompt."""
    after = OR_AFTER_RE.match(text, opt["end"], q["end"])
    if after:
        end = PAIR_END_RE.search(text, after.end(), q["end"])
        stop = end.start() if end else q["end"]
        if stop - after.end() >= 2:
            return [opt, {"start": after.end(), "end": stop, "rec": False}]
    before = OR_BEFORE_RE.search(text[q["start"]: opt["start"]])
    if before:
        head = text[q["start"]: q["start"] + before.start()]
        leads = list(PAIR_LEAD_RE.finditer(head))
        start = q["start"] + (leads[-1].end() if leads else 0)
        stop = q["start"] + before.start()
        if stop - start >= 2 and len(text[start:stop].split()) <= 15:
            return [{"start": start, "end": stop, "rec": False}, opt]
    return [opt]


def _split_inline(text: str, opt: dict) -> list[dict]:
    """One tagged span holding "`a`, `b`, `c`, or `d`" (or "(1) … (2) …") is several short options."""
    body = text[opt["start"]: opt["end"]]
    base = opt["start"]
    if ": " in body:  # "work on: `ai`, `agent`" — drop the lead-in
        cut = body.rindex(": ") + 2
        if body[cut:].count(",") >= 1:
            base, body = base + cut, body[cut:]
    enums = list(ENUM_RE.finditer(body))
    if len(enums) >= 2:
        bounds = [m.end() for m in enums]
        pieces = [(b, (enums[i + 1].start() if i + 1 < len(enums) else len(body))) for i, b in enumerate(bounds)]
    else:
        if body.count(",") < 2:
            return [opt]
        pieces, pos = [], 0
        for m in re.finditer(r",\s*(?:or\s+|and\s+)?|\s+or\s+", body):
            pieces.append((pos, m.start()))
            pos = m.end()
        pieces.append((pos, len(body)))
        if any(len(body[a:b].split()) > 4 for a, b in pieces):
            return [opt]
    out = []
    for a, b in pieces:
        seg = body[a:b]
        seg_s = seg.rstrip(" ,;").rstrip()
        lead = len(seg) - len(seg.lstrip(" ("))
        stop = a + len(seg_s)
        if seg_s.endswith(")") and "(" not in seg_s[lead:]:
            stop -= 1
        if stop - (a + lead) >= 1:
            out.append({"start": base + a + lead, "end": base + stop, "rec": False})
    if out:
        out[-1]["rec"] = opt["rec"]
    return out if len(out) >= 2 else [opt]


def compile_questions(text: str, tokens: list[Token], labels: list[int]) -> list[Question]:
    names = [LABELS[i] for i in labels]
    questions: list[dict] = []
    options: list[dict] = []  # {start, end, rec, q (index of owning question or None)}
    cur_q = None
    cur_opt = None
    for tok, name in zip(tokens, names):
        if name == "Q_B" or (name == "Q_I" and cur_q is None):
            cur_q = {"start": tok.start, "end": tok.end}
            questions.append(cur_q)
            cur_opt = None
        elif name == "Q_I":
            cur_q["end"] = tok.end
        elif name == "OPT_B" or (name == "OPT_I" and cur_opt is None):
            cur_opt = {"start": tok.start, "end": tok.end, "rec": False, "after_q": len(questions) - 1}
            options.append(cur_opt)
        elif name == "OPT_I":
            cur_opt["end"] = tok.end
        elif name == "REC":
            if cur_opt is not None:
                cur_opt["rec"] = True
        if name == "O" and tok.kind in (KIND_NL, KIND_PARA):
            cur_opt = None
            if tok.kind == KIND_PARA:
                cur_q = None
    if not questions:
        return []

    def asks(i: int) -> bool:
        span = text[questions[i]["start"]: questions[i]["end"]]
        if QMARK_RE.search(span):
            return True
        # "Would you like me to:" followed by a list asks without a question mark.
        return span.rstrip().endswith(":") and sum(o["after_q"] == i for o in options) >= 2

    # Hand-labeled asks virtually always carry a '?'; spans without one are tagging slips.
    kept = [i for i in range(len(questions)) if asks(i)]
    if not kept:
        return []
    for opt in options:
        if opt["after_q"] >= 0 and opt["after_q"] not in kept:
            opt["after_q"] = max((k for k in kept if k < opt["after_q"]), default=-1)
        opt["after_q"] = kept.index(opt["after_q"]) if opt["after_q"] in kept else -1
    questions = [questions[i] for i in kept]
    owned: list[list[dict]] = [[] for _ in questions]
    for opt in options:
        # A list before any question ("Options: … Which one?") belongs to the first
        # question; otherwise options belong to the question they follow or sit in.
        owned[max(opt["after_q"], 0)].append(opt)
    out = []
    for q, opts in zip(questions, owned):
        prompt = text[q["start"]: q["end"]].strip()
        if len(opts) <= 2:
            opts = [piece for o in opts for piece in _split_inline(text, o)]
        escaped = [o for o in opts if ESCAPE_RE.search(_clean_option(text[o["start"]: o["end"]]))]
        opts = [o for o in opts if o not in escaped]
        if len(opts) == 1 and not escaped:
            opts = _complete_pair(text, q, opts[0])
        if len(opts) == 1:
            opts = []  # a single option is no choice; the question is yes/no or open
        labels_text = [_clean_option(text[o["start"]: o["end"]]) for o in opts]
        kind = "either_or" if len(opts) == 2 else "multi_choice" if len(opts) > 2 else (
            "open" if is_open(prompt) else "yes_no")
        default = next((i for i, o in enumerate(opts) if o["rec"]), None)
        out.append(Question(
            prompt=prompt,
            kind=kind,
            propose=is_proposal(prompt),
            options=labels_text,
            default=default,
            multi_select=bool(MULTI_RE.search(prompt)),
            span=(q["start"], q["end"]),
        ))
    return _merge_offer_lists(text, out)


def apply_kind(q: Question, probs: dict[str, float], mode: str = "hybrid", drop: float = 0.6) -> Question:
    """Combine the compiler's kind with a kind classifier's probabilities.

    head:   trust the classifier; non-choice kinds clear the options.
    hybrid: the classifier may drop options it is confident are spurious (p(yes_no)+p(open) > drop)
            and decides yes_no vs open, but it never invents a choice without tagged options.
    """
    if mode == "compiler" or not probs:
        return q
    plain = max(("yes_no", "open"), key=probs.get)
    if mode == "head":
        kind = max(probs, key=probs.get)
        if kind in ("yes_no", "open"):
            return Question(q.prompt, kind, q.propose, [], None, False, q.span)
        return Question(q.prompt, kind, q.propose, q.options, q.default, q.multi_select, q.span)
    if q.options:
        if probs["yes_no"] + probs["open"] > drop:
            return Question(q.prompt, plain, q.propose, [], None, False, q.span)
        return q
    return Question(q.prompt, plain, q.propose, [], None, q.multi_select, q.span)


LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d{1,2}[.)]|\(?[a-zA-Z]\))\s+[*_`]*$")
OFFER_LEAD_RE = re.compile(
    r"\b(?:would you like me to|do you want me to|want me to|should i|shall i|would you like to|do you want to|"
    r"would you prefer|do you prefer|i can|next steps?|options?)\b[^\n]*:\s*$", re.I)


def _list_item_line(text: str, start: int) -> int | None:
    """Start of the line if the question at `start` is a list item ("1. Add X?"), else None."""
    line = text.rfind("\n", 0, start) + 1
    return line if LIST_ITEM_RE.match(text[line:start]) else None


def _merge_offer_lists(text: str, questions: list[Question]) -> list[Question]:
    """"Would you like me to:\\n1. A?\\n2. B?" is one choice among the items, not several yes/no questions."""
    out, i = [], 0
    while i < len(questions):
        j = i
        while (j < len(questions) and not questions[j].options
               and _list_item_line(text, questions[j].span[0]) is not None):
            j += 1
        if j - i >= 2:
            first = _list_item_line(text, questions[i].span[0])
            lead_start = text.rfind("\n", 0, max(0, first - 1)) + 1
            lead = text[lead_start:first].strip()
            if OFFER_LEAD_RE.search(lead):
                items = [_clean_option(q.prompt.rstrip("?？ ")) for q in questions[i:j]]
                prompt = f"{lead} {' / '.join(items)}?"
                out.append(Question(
                    prompt=prompt,
                    kind="either_or" if len(items) == 2 else "multi_choice",
                    propose=is_proposal(lead),
                    options=items,
                    multi_select=bool(MULTI_RE.search(lead)),
                    span=(lead_start + len(text[lead_start:first]) - len(text[lead_start:first].lstrip()),
                          questions[j - 1].span[1]),
                ))
                i = j
                continue
        out.append(questions[i])
        i += 1
    return out
