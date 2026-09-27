"""Tokenizer and sparse feature rows, after gpu-time's vocabulary-free design.

Each token maps to a handful of rows in disjoint regions of one embedding table.
Words are only seen through hashes, so there is no word list to maintain.
"""

from __future__ import annotations

import re
import zlib
from dataclasses import dataclass

MAX_TOKENS = 256

FENCE_RE = re.compile(r"```.*?(?:```|\Z)", re.S)
URL_RE = re.compile(r"https?://[^\s)>\]]+")
TOKEN_RE = re.compile(r"\n[ \t]*\n\s*|\n|\[CODE\]|\[URL\]|[^\W\d_]+(?:['’][^\W\d_]+)*|\d+|[^\s]")
LIST_MARKER_RE = re.compile(r"^[ \t]*(?:[-*•]|\d{1,2}[.)]|[A-Za-z][.)]|\([A-Za-z0-9]\)|\*\*[A-Za-z0-9][.)]?\*\*)[ \t]+")
WH_WORDS = {"what", "which", "where", "when", "why", "how", "who", "whose", "whom"}

KIND_WORD, KIND_NUM, KIND_PUNCT, KIND_NL, KIND_PARA, KIND_PLACEHOLDER = range(6)

HASH_ROWS = 2048
SUFFIX_ROWS = 256

# Row layout: every feature owns a disjoint slice of the embedding table.
OFF_KIND = 0
OFF_LEN = OFF_KIND + 8
OFF_CASE = OFF_LEN + 8
OFF_HASH = OFF_CASE + 8
OFF_SUFFIX = OFF_HASH + HASH_ROWS
OFF_LINE_POS = OFF_SUFFIX + SUFFIX_ROWS
OFF_PARA_POS = OFF_LINE_POS + 8
OFF_FLAGS = OFF_PARA_POS + 8
FLAG_NAMES = [
    "line_start",
    "list_line",
    "list_marker",
    "question_sentence",
    "question_line",
    "after_colon",
    "sentence_start",
    "wh_word",
]
FEATURE_ROWS = OFF_FLAGS + len(FLAG_NAMES)

# Version 2 adds bigger word/suffix tables, prefix and word-bigram hashes, and
# structure features (list position, where the '?' marks are, quotes, markup).
# The active version is process-wide: training sets it from its flags, and
# gq.predict.load sets it from the checkpoint, so features always match the model.
V2_HASH_ROWS = 8192
V2_SUFFIX_ROWS = 1024
V2_PREFIX_ROWS = 512
V2_BIGRAM_ROWS = 4096
V2_BUCKETS = 8
V2_STRUCT = ["list_index", "list_size", "qs_after", "next_q", "prev_q", "from_end", "sentence_q"]
V2_FLAGS = FLAG_NAMES + ["line_q_end", "line_colon_end", "prev_line_colon", "in_code", "in_quote", "in_parens",
                         "in_bold", "heading", "sentence_or", "sentence_offer", "after_q_same_para"]
V2_OFF_HASH = 24
V2_OFF_SUFFIX = V2_OFF_HASH + V2_HASH_ROWS
V2_OFF_PREFIX = V2_OFF_SUFFIX + V2_SUFFIX_ROWS
V2_OFF_BIGRAM = V2_OFF_PREFIX + V2_PREFIX_ROWS
V2_OFF_LINE_POS = V2_OFF_BIGRAM + V2_BIGRAM_ROWS
V2_OFF_PARA_POS = V2_OFF_LINE_POS + 8
V2_OFF_STRUCT = V2_OFF_PARA_POS + 8
V2_OFF_FLAGS = V2_OFF_STRUCT + len(V2_STRUCT) * V2_BUCKETS
V2_FEATURE_ROWS = V2_OFF_FLAGS + len(V2_FLAGS)
OFFER_RE = re.compile(r"\b(want me to|should i|shall i|would you like|do you want|can i|okay to|ok to|prefer)\b", re.I)

FEATURE_VERSION = 1


def set_feature_version(version: int):
    global FEATURE_VERSION
    FEATURE_VERSION = version


def feature_rows(version: int | None = None) -> int:
    return V2_FEATURE_ROWS if (version or FEATURE_VERSION) == 2 else FEATURE_ROWS


def identity_cols(version: int | None = None) -> slice:
    """Feature columns that identify the word itself (dropped out during training)."""
    return slice(3, 7) if (version or FEATURE_VERSION) == 2 else slice(3, 5)


@dataclass
class Token:
    start: int
    end: int
    text: str
    kind: int


def clean(text: str) -> str:
    """Normalize raw agent output. Training and inference must use the same cleaning."""
    text = FENCE_RE.sub("[CODE]", text)
    text = URL_RE.sub("[URL]", text)
    return text.replace("\r\n", "\n").strip()


def _kind(tok: str) -> int:
    if tok.startswith("\n"):
        return KIND_PARA if tok.count("\n") >= 2 else KIND_NL
    if tok in ("[CODE]", "[URL]"):
        return KIND_PLACEHOLDER
    if tok[0].isdigit():
        return KIND_NUM
    if tok[0].isalpha():
        return KIND_WORD
    return KIND_PUNCT


def tokenize(text: str) -> list[Token]:
    return [Token(m.start(), m.end(), m.group(0), _kind(m.group(0))) for m in TOKEN_RE.finditer(text)]


def tail_start(tokens: list[Token], limit: int = MAX_TOKENS) -> int:
    """Index of the first token kept when only the last `limit` tokens are modeled."""
    return max(0, len(tokens) - limit)


def _hash(value: str, buckets: int) -> int:
    return zlib.crc32(value.encode()) % buckets


def _length_bucket(n: int) -> int:
    for i, bound in enumerate((1, 2, 3, 5, 8, 12)):
        if n <= bound:
            return i
    return 6


def _case(tok: str) -> int:
    if not tok[0].isalpha():
        return 0
    if tok.islower():
        return 1
    if tok.isupper() and len(tok) > 1:
        return 3
    if tok[0].isupper() and (len(tok) == 1 or tok[1:].islower()):
        return 2
    return 4


def _bucket(n: int | None) -> int:
    """0 for none, then 1, 2, 3-4, 5-8, 9-16, 17-32, 33+."""
    if n is None:
        return 0
    for i, bound in enumerate((1, 2, 4, 8, 16, 32), start=1):
        if n <= bound:
            return i
    return 7


# Static word vectors: each token gets one extra id, STATIC_OFFSET + its vocabulary index (len(vocab) when
# unknown). The offset keeps these ids apart from the hashed feature ids, whatever the row width.
STATIC_OFFSET = 1 << 24
STATIC_VOCAB: dict[str, int] | None = None


def set_static_vocab(vocab: list[str] | None):
    global STATIC_VOCAB
    STATIC_VOCAB = {w: i for i, w in enumerate(vocab)} if vocab else None


def static_word(tok: str) -> str:
    return tok.lower()


def features(text: str, tokens: list[Token]) -> list[list[int]]:
    rows = features_v2(text, tokens) if FEATURE_VERSION == 2 else features_v1(text, tokens)
    if STATIC_VOCAB is not None:
        unknown = len(STATIC_VOCAB)
        for row, tok in zip(rows, tokens):
            row.append(STATIC_OFFSET + STATIC_VOCAB.get(static_word(tok.text), unknown))
    return rows


def features_v2(text: str, tokens: list[Token]) -> list[list[int]]:
    base = features_v1(text, tokens)
    lines = text.split("\n")
    line_starts, pos = [], 0
    for line in lines:
        line_starts.append(pos)
        pos += len(line) + 1

    def line_of(offset: int) -> int:
        lo, hi = 0, len(lines) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo

    # List position: index of the item within its run of list lines, and the run's size.
    prev_nonempty, last = [""] * len(lines), ""
    for li, line in enumerate(lines):
        prev_nonempty[li] = last
        if line.strip():
            last = line.rstrip()
    item_index, run_size, run = [0] * len(lines), [0] * len(lines), []
    for li, line in enumerate(lines + [""]):
        if li < len(lines) and LIST_MARKER_RE.match(line):
            run.append(li)
            item_index[li] = len(run)
        elif line.strip() or li == len(lines):
            for r in run:
                run_size[r] = len(run)
            run = []
    q_positions = [i for i, t in enumerate(tokens) if t.text in ("?", "？")]
    # Character-level context: inline code, quotes, parentheses, bold.
    in_code = in_quote = False
    depth = 0
    bold = False
    i_char = 0
    marks = {}
    while i_char < len(text):
        ch = text[i_char]
        if text.startswith("**", i_char):
            bold = not bold
            marks[i_char] = (in_code, in_quote, depth > 0, bold)
            marks[i_char + 1] = marks[i_char]
            i_char += 2
            continue
        if ch == "`":
            in_code = not in_code
        elif not in_code and ch in "\"“”":
            in_quote = not in_quote if ch == "\"" else ch == "“"
        elif not in_code and ch == "(":
            depth += 1
        elif not in_code and ch == ")":
            depth = max(0, depth - 1)
        marks[i_char] = (in_code, in_quote, depth > 0, bold)
        i_char += 1
    # Sentence-level cues: does the sentence end with '?', contain " or ", or an offer phrase.
    sent_id, sentences, begin = [0] * len(tokens), [], 0
    for i, tok in enumerate(tokens):
        if tok.kind in (KIND_NL, KIND_PARA) or tok.text in (".", "!", "?", "？") or i == len(tokens) - 1:
            sentences.append((begin, i))
            for j in range(begin, i + 1):
                sent_id[j] = len(sentences) - 1
            begin = i + 1
    sent_text = [text[tokens[a].start: tokens[b].end] if tokens else "" for a, b in sentences]
    sent_or = [bool(re.search(r"\bor\b", s, re.I)) for s in sent_text]
    sent_offer = [bool(OFFER_RE.search(s)) for s in sent_text]
    sent_q = [s.rstrip().endswith(("?", "？")) for s in sent_text]
    para_of = [0] * len(tokens)
    p = 0
    for i, tok in enumerate(tokens):
        if tok.kind == KIND_PARA:
            p += 1
        para_of[i] = p
    last_q_para = {para_of[q] for q in q_positions}

    rows = []
    n = len(tokens)
    qi = 0
    for i, tok in enumerate(tokens):
        r = base[i]
        lower = tok.text.lower()
        prev = tokens[i - 1].text.lower() if i else "<s>"
        li = line_of(tok.start)
        line = lines[li].rstrip()
        prev_line = prev_nonempty[li]
        while qi < len(q_positions) and q_positions[qi] < i:
            qi += 1
        qs_after = len(q_positions) - qi
        next_q = q_positions[qi] - i if qi < len(q_positions) else None
        prev_q = i - q_positions[qi - 1] if qi > 0 else None
        code, quote, parens, in_bold = marks.get(tok.start, (False, False, False, False))
        flags = {
            "line_q_end": line.endswith(("?", "？", "?**", "?*")),
            "line_colon_end": line.endswith((":", ":**")),
            "prev_line_colon": prev_line.endswith((":", ":**")),
            "in_code": code,
            "in_quote": quote,
            "in_parens": parens,
            "in_bold": in_bold,
            "heading": line.lstrip().startswith("#"),
            "sentence_or": sent_or[sent_id[i]] if tokens else False,
            "sentence_offer": sent_offer[sent_id[i]] if tokens else False,
            "after_q_same_para": prev_q is not None and para_of[i] in last_q_para,
        }
        struct = [min(item_index[li], 7), min(run_size[li], 7), _bucket(qs_after or None), _bucket(next_q),
                  _bucket(prev_q), _bucket(n - i), int(sent_q[sent_id[i]]) + 1 if tokens else 0]
        v2 = [
            r[0], r[1], r[2],
            V2_OFF_HASH + _hash(lower, V2_HASH_ROWS),
            V2_OFF_SUFFIX + _hash("~" + lower[-3:], V2_SUFFIX_ROWS),
            V2_OFF_PREFIX + _hash(lower[:3] + "~", V2_PREFIX_ROWS),
            V2_OFF_BIGRAM + _hash(prev + " " + lower, V2_BIGRAM_ROWS),
            V2_OFF_LINE_POS + (r[5] - OFF_LINE_POS),
            V2_OFF_PARA_POS + (r[6] - OFF_PARA_POS),
        ]
        v2.extend(V2_OFF_STRUCT + s * V2_BUCKETS + v for s, v in enumerate(struct))
        v2.extend(V2_OFF_FLAGS + k for k, name in enumerate(FLAG_NAMES) if OFF_FLAGS + k in r[7:])
        v2.extend(V2_OFF_FLAGS + len(FLAG_NAMES) + k for k, name in enumerate(V2_FLAGS[len(FLAG_NAMES):])
                  if flags[name])
        rows.append(v2)
    return rows


def features_v1(text: str, tokens: list[Token]) -> list[list[int]]:
    lines = text.split("\n")
    line_starts = []
    pos = 0
    for line in lines:
        line_starts.append(pos)
        pos += len(line) + 1
    n_lines = len(lines)
    para_breaks = [m.start() for m in re.finditer(r"\n[ \t]*\n", text)]

    def line_index(offset: int) -> int:
        lo, hi = 0, n_lines - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo

    # A sentence ends at . ! ? or a newline; mark tokens whose sentence ends with '?'.
    in_question = [False] * len(tokens)
    sentence_start = [False] * len(tokens)
    begin = 0
    for i, tok in enumerate(tokens):
        ends = tok.kind in (KIND_NL, KIND_PARA) or tok.text in (".", "!", "?")
        if ends or i == len(tokens) - 1:
            if tok.text == "?":
                for j in range(begin, i + 1):
                    in_question[j] = True
            begin = i + 1
    first_in_sentence = True
    for i, tok in enumerate(tokens):
        if tok.kind in (KIND_NL, KIND_PARA):
            first_in_sentence = True
            continue
        sentence_start[i] = first_in_sentence and tok.kind in (KIND_WORD, KIND_NUM, KIND_PLACEHOLDER)
        if sentence_start[i]:
            first_in_sentence = False
        if tok.text in (".", "!", "?"):
            first_in_sentence = True

    rows = []
    prev_line = -1
    after_colon = False
    for i, tok in enumerate(tokens):
        li = line_index(tok.start)
        line = lines[li]
        marker = LIST_MARKER_RE.match(line)
        lower = tok.text.lower()
        flags = {
            "line_start": li != prev_line and tok.kind not in (KIND_NL, KIND_PARA),
            "list_line": bool(marker),
            "list_marker": bool(marker) and tok.start - line_starts[li] < marker.end(),
            "question_sentence": in_question[i],
            "question_line": "?" in line,
            "after_colon": after_colon,
            "sentence_start": sentence_start[i],
            "wh_word": lower in WH_WORDS,
        }
        if tok.kind not in (KIND_NL, KIND_PARA):
            prev_line = li
        if tok.text == ":":
            after_colon = True
        elif tok.kind in (KIND_NL, KIND_PARA) or tok.text in (".", "?", "!"):
            after_colon = False
        lines_from_end = n_lines - 1 - li
        paras_from_end = sum(1 for b in para_breaks if b >= tok.end)
        r = [
            OFF_KIND + tok.kind,
            OFF_LEN + _length_bucket(len(tok.text)),
            OFF_CASE + _case(tok.text),
            OFF_HASH + _hash(lower, HASH_ROWS),
            OFF_SUFFIX + _hash("~" + lower[-3:], SUFFIX_ROWS),
            OFF_LINE_POS + min(lines_from_end, 7),
            OFF_PARA_POS + min(paras_from_end, 7),
        ]
        r.extend(OFF_FLAGS + k for k, name in enumerate(FLAG_NAMES) if flags[name])
        rows.append(r)
    return rows
