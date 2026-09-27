#!/usr/bin/env python3
"""Survey local coding-agent traces for questions asked to the user.

Read-only: every store is opened for reading (sqlite via mode=ro URIs).
Outputs summary.json and sample.jsonl to data/survey/ (git-ignored), or --out DIR.
"""
import argparse
import collections
import glob
import json
import os
import random
import re
import sqlite3
import sys

HOME = os.path.expanduser("~")
ASK_TOOL_RE = re.compile(r"(ask_?(user|question)|question|user_input|elicit)", re.I)

# ---------------------------------------------------------------- redaction
_SECRET_RES = [
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    re.compile(r"\b(sk|pk|rk)-[A-Za-z0-9_-]{12,}"),
    re.compile(r"\b(ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{10,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*[a-z])[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}"),
    re.compile(r"\b[A-Fa-f0-9]{40,}\b"),
    re.compile(r"\b[A-Za-z0-9+/]{48,}={0,2}"),
    re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*\S+"),
]


def redact(s, n=200, keep_lines=False):
    if s is None:
        return None
    s = str(s)
    for r in _SECRET_RES:
        s = r.sub("[REDACTED]", s)
    if keep_lines:
        s = re.sub(r"[ \t]+", " ", s)
        s = re.sub(r"\n{3,}", "\n\n", s).strip()
    else:
        s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ------------------------------------------------------------ classification
FENCE_RE = re.compile(r"```.*?(```|$)", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
URL_RE = re.compile(r"https?://\S+")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)]|[A-Za-z][.)]|\(?[A-Za-z0-9]\))\s+(.*)$")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z*(\"'`])")

YESNO_START = re.compile(
    r"^(?:\W*)(should|shall|do|does|did|can|could|would|will|is|are|was|were|want|may|might|have|has|any|ok|okay|mind)\b",
    re.I,
)
YESNO_ANY = re.compile(r"\b(want me to|would you like( me)? to|do you want|should i|shall i|can i|may i|ok(ay)? if i|or not)\b", re.I)
CONFIRM_RE = re.compile(
    r"(\b(shall|should|can|may) (i|we) (go ahead|proceed|continue|start|begin|move forward|move on|implement|apply|commit|push|merge|ship|land|execute|run it)\b"
    r"|\b(ready|ok(ay)?|good|fine|clear) to (proceed|go|start|continue|ship|merge)\b"
    r"|\bproceed( with (this|that|the plan|it))?\s*\?"
    r"|\b(sound|look|seem)s? (good|right|ok(ay)?|reasonable|fine)\b"
    r"|\b(does|is) (this|that|the) (plan|approach|direction|proposal)\b.*\b(ok(ay)?|work|good|fine|right|make sense)"
    r"|\bgo ahead\s*\?|\bgreen ?light\b|\bany objections\b|\bgood to go\b|\bapprove\b)",
    re.I,
)
WH_RE = re.compile(r"\b(what|where|which|when|why|how|who|whose|whom)\b", re.I)
WH_START = re.compile(r"^(?:\W*)(?:[^,?]{0,60},\s*)?(what|where|which|when|why|how|who|whose|whom)\b", re.I)
OPTION_REF_RE = re.compile(r"\b(which|option|options|pick|choose|prefer|preference|one of|these|those|above|following|any of)\b", re.I)
EITHER_OR_RE = re.compile(r"\bor\b", re.I)
NOT_REAL_OR = re.compile(r"\bor (not|something( else)?|anything( else)?|otherwise|so|more|less|similar|both)\b", re.I)
DIRECTED_RE = re.compile(r"\b(you|your|i|me|we|us|let's|prefer|want|should|shall|would)\b", re.I)


def strip_markup(text):
    t = FENCE_RE.sub("\n[CODE]\n", text)
    t = URL_RE.sub("[URL]", t)
    t = INLINE_CODE_RE.sub(lambda m: m.group(0).replace("?", ""), t)
    return t


def tail_block(text):
    """Return (last_paragraph, preceding_list_items) after stripping code."""
    t = strip_markup(text).strip()
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    if not paras:
        return "", [], t
    last = paras[-1]
    # If the last paragraph is short and follows a list, bind the list to it.
    items = []
    lines = last.splitlines()
    own_items = [LIST_ITEM_RE.match(l) for l in lines]
    if any(own_items):
        items = [m.group(1) for m in own_items if m]
    elif len(paras) >= 2:
        prev = paras[-2].splitlines()
        pm = [LIST_ITEM_RE.match(l) for l in prev]
        if sum(1 for m in pm if m) >= 2:
            items = [m.group(1) for m in pm if m]
    return last, items, t


def question_sentences(par):
    out = []
    for line in par.splitlines():
        line = LIST_ITEM_RE.sub(r"\1", line).strip().strip("*_ ")
        for s in SENT_SPLIT_RE.split(line):
            s = s.strip()
            if "?" in s and len(s) > 3:
                # keep up to the last '?'
                out.append(s[: s.rfind("?") + 1])
    return out


def inline_options(q):
    body = re.sub(r"^.*?:\s*", "", q) if ":" in q[:-1] else q
    body = body.rstrip("?").strip()
    if not EITHER_OR_RE.search(body) or NOT_REAL_OR.search(body):
        return []
    # "X, Y, or Z" / "X or Y"
    body = re.sub(r"^(should i|shall i|do you want( me)? to|would you (like|prefer)( me)? to|want me to|do you prefer|prefer)\s+", "", body, flags=re.I)
    parts = re.split(r",\s*(?:or\s+)?|\s+or\s+", body)
    parts = [p.strip(" ()*`'\"") for p in parts if p.strip()]
    return parts if 2 <= len(parts) <= 6 else []


def is_rhetorical(qs, last_par):
    # Question answered right after in the same paragraph ("Why? Because ...").
    if not qs:
        return False
    after = last_par[last_par.rfind("?") + 1:].strip()
    return len(after) > 80 and not DIRECTED_RE.search(qs[-1])


def classify(text):
    last, items, stripped = tail_block(text)
    qs = question_sentences(last)
    if not qs and items:
        # Questions may be the list items themselves.
        qs = [i for i in items if i.strip().endswith("?")]
    if not qs:
        return None
    if is_rhetorical(qs, last):
        cls_flags = ["rhetorical_suspect"]
    else:
        cls_flags = []
    q = qs[-1]
    question_items = [i for i in items if i.strip().endswith("?")]
    option_items = [i for i in items if not i.strip().endswith("?")]
    presentation = "absent"
    options = []
    if len(question_items) >= 2 or len(qs) >= 3:
        cls = "multi_question"
    elif len(option_items) >= 2 and OPTION_REF_RE.search(q):
        cls = "multi_choice"
        presentation = "list"
        options = option_items
    elif inline_options(q):
        cls = "either_or"
        presentation = "inline"
        options = inline_options(q)
    elif CONFIRM_RE.search(q):
        cls = "confirm_plan"
    elif YESNO_START.search(q) or YESNO_ANY.search(q):
        cls = "yes_no"
    elif WH_START.search(q):
        cls = "open_wh"
    elif len(q.split()) <= 15 and not WH_RE.search(q):
        # Elliptical proposals: "Try a different approach?", "Both?"
        cls = "yes_no"
        cls_flags.append("elliptical")
    else:
        cls = "other"
    if cls in ("yes_no", "confirm_plan") and len(option_items) >= 2:
        presentation = "list_context"
    if "[CODE]" in stripped:
        cls_flags.append("has_code_block")
    return {
        "cls": cls,
        "question": q,
        "n_questions_tail": len(qs),
        "n_questions_total": len(question_sentences(stripped)),
        "presentation": presentation,
        "options": options[:8],
        "flags": cls_flags,
    }


def reply_kind(reply, options):
    if reply is None:
        return "none"
    r = reply.strip()
    rl = r.lower().strip(" .!")
    if re.fullmatch(r"(y|yes|yep|yeah|yup|sure|ok|okay|go|go ahead|do it|please|please do|proceed|continue|lgtm|sounds good|ship it|yes please|approved?|correct|right|👍)", rl):
        return "affirm_short"
    if re.fullmatch(r"(n|no|nope|nah|don't|stop|skip|not now|no thanks)", rl):
        return "negate_short"
    if re.fullmatch(r"(option\s*)?([0-9]|[a-e])([.)])?", rl):
        return "option_pick_short"
    if re.match(r"(y|yes|yep|yeah|sure|ok|okay|go ahead|go|do it|please do|proceed|lgtm|sounds good|perfect|great)\b", rl):
        return "affirm_prefix"
    if re.match(r"(no|nope|nah|don't|do not|stop|wait)\b", rl):
        return "negate_prefix"
    if re.match(r"(option\s*)?([0-9]|[a-e])\b[.):,]?\s", rl) or re.match(r"(both|all|neither|the (first|second|third|last)( one)?|first|second)\b", rl):
        return "option_pick_prefix"
    if options:
        for o in options:
            o2 = o.lower().strip()[:25]
            if o2 and (rl.startswith(o2[:12]) or o2.startswith(rl)) and len(rl) >= 2:
                return "option_label"
    if len(r) <= 40:
        return "short_other"
    if len(r) <= 300:
        return "medium"
    return "long"


# --------------------------------------------------------------- normalizing
def norm_claude_ask(inp):
    qs = []
    for q in (inp or {}).get("questions", []) or []:
        opts = [o.get("label") if isinstance(o, dict) else str(o) for o in q.get("options", []) or []]
        qs.append({"question": q.get("question"), "header": q.get("header"), "multi": bool(q.get("multiSelect")), "options": opts})
    return qs


def norm_bb_questions(qlist):
    qs = []
    for q in qlist or []:
        opts = [o.get("label") for o in q.get("options", []) or [] if isinstance(o, dict)]
        qs.append({"question": q.get("prompt"), "header": q.get("shortLabel"), "multi": bool(q.get("multiSelect")), "options": opts})
    return qs


def norm_droid_questionnaire(s):
    qs = []
    cur = None
    for line in (s or "").splitlines():
        m = re.match(r"^\s*\d+\.\s*\[question\]\s*(.*)", line)
        if m:
            cur = {"question": m.group(1), "header": None, "multi": False, "options": []}
            qs.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\s*\[(topic|option|multi|multiselect|multi-select)\]\s*(.*)", line, re.I)
        if m:
            k = m.group(1).lower()
            if k == "topic":
                cur["header"] = m.group(2)
            elif k == "option":
                cur["options"].append(m.group(2))
            else:
                cur["multi"] = True
        elif line.strip() and not cur["options"]:
            cur["question"] += " " + line.strip()
    return qs


def norm_generic_ask(name, inp):
    if isinstance(inp, str):
        try:
            inp = json.loads(inp)
        except Exception:
            return [{"question": inp, "header": None, "multi": False, "options": []}]
    if not isinstance(inp, dict):
        return []
    if "questionnaire" in inp:
        return norm_droid_questionnaire(inp["questionnaire"])
    if "questions" in inp and isinstance(inp["questions"], list):
        out = []
        for q in inp["questions"]:
            if isinstance(q, str):
                out.append({"question": q, "header": None, "multi": False, "options": []})
                continue
            opts = q.get("options") or q.get("choices") or []
            opts = [o.get("label") or o.get("value") if isinstance(o, dict) else str(o) for o in opts]
            out.append({"question": q.get("question") or q.get("prompt") or q.get("text"), "header": q.get("header") or q.get("id"),
                        "multi": bool(q.get("multiSelect") or q.get("multiple")), "options": opts})
        return out
    q = inp.get("question") or inp.get("prompt") or inp.get("message")
    opts = inp.get("options") or inp.get("choices") or []
    opts = [o.get("label") if isinstance(o, dict) else str(o) for o in opts]
    return [{"question": q, "header": None, "multi": False, "options": opts}] if q else []


# ------------------------------------------------------------------ records
class Collector:
    def __init__(self):
        self.sessions = collections.Counter()
        self.sub_sessions = collections.Counter()
        self.eot = []   # end-of-turn records
        self.asks = []  # structured ask records
        self.ask_tool_names = collections.Counter()
        self.errors = collections.Counter()
        self.session_count = 0

    def session(self, agent, turns, subagent=False):
        """turns: list of events in order: ('user', text) | ('assistant', text) | ('ask', name, questions, answer)"""
        (self.sub_sessions if subagent else self.sessions)[agent] += 1
        self.session_count += 1
        self.sid = f"{agent}:{self.session_count}"
        last_asst = None
        pending_ask = []
        for ev in turns:
            if ev[0] == "assistant":
                if ev[1] and ev[1].strip():
                    last_asst = ev[1]
            elif ev[0] == "ask":
                self.ask_tool_names[(agent, ev[1])] += 1
                rec = {"agent": agent, "sid": self.sid, "tool": ev[1], "questions": ev[2], "answer": ev[3] if len(ev) > 3 else None, "subagent": subagent}
                self.asks.append(rec)
            elif ev[0] == "user":
                if last_asst is not None:
                    self._eot(agent, last_asst, ev[1], subagent)
                last_asst = None
        if last_asst is not None:
            self._eot(agent, last_asst, None, subagent)

    def _eot(self, agent, text, reply, subagent):
        c = classify(text)
        rec = {"agent": agent, "sid": self.sid, "subagent": subagent, "is_question": c is not None, "len": len(text)}
        if c:
            rec.update(c)
            rec["text_tail"] = text[-600:]
            rec["reply_kind"] = reply_kind(reply, c["options"])
            rec["reply"] = reply[:120] if reply else None
        else:
            rec["reply_kind"] = "none" if reply is None else "n/a"
        rec["export_tail"] = text[-1500:]
        self.eot.append(rec)


def is_ask_tool(name):
    # BB toolCall "names" are display titles ("Fetch: https://...?ask=..."), so reject anything with spaces.
    return bool(name) and not re.search(r"[\s:]", name) and bool(ASK_TOOL_RE.search(name))


def blocks_text(content, kinds=("text", "output_text", "input_text")):
    if isinstance(content, str):
        return content
    out = []
    for b in content or []:
        if isinstance(b, dict) and b.get("type") in kinds and isinstance(b.get("text"), str):
            out.append(b["text"])
    return "\n".join(out)


SYNTH_USER_RE = re.compile(
    r"^\s*(<(command-|local-command|system-reminder|environment_context|user_instructions|permissions|collaboration_mode|skills_instructions|app-context|turn_aborted|subagent_notification|user_info|task-notification)|Caveat:|\[Request interrupted)",
    re.I,
)


def clean_user(text):
    if not text:
        return None
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S).strip()
    if not t or SYNTH_USER_RE.match(t):
        return None
    return t


# ------------------------------------------------------------------ parsers
def parse_claude(col, stats):
    files = glob.glob(os.path.join(HOME, ".claude/projects/**/*.jsonl"), recursive=True)
    for f in files:
        turns = []
        sub = "/subagents/" in f or os.path.basename(f).startswith("agent-")
        ask_ids = {}
        try:
            fh = open(f, errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("isSidechain"):
                    sub = True
                t = d.get("type")
                m = d.get("message") or {}
                if t == "assistant":
                    content = m.get("content") or []
                    txt = blocks_text(content, ("text",))
                    if txt:
                        turns.append(("assistant", txt))
                    for b in content if isinstance(content, list) else []:
                        if isinstance(b, dict) and b.get("type") == "tool_use":
                            n = b.get("name", "")
                            if n == "AskUserQuestion":
                                ask_ids[b.get("id")] = len(turns)
                                turns.append(["ask", n, norm_claude_ask(b.get("input")), None])
                            elif is_ask_tool(n):
                                ask_ids[b.get("id")] = len(turns)
                                turns.append(["ask", n, norm_generic_ask(n, b.get("input")), None])
                elif t == "user":
                    if d.get("isMeta") or d.get("isCompactSummary"):
                        continue
                    content = m.get("content")
                    if isinstance(content, list):
                        for b in content:
                            if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in ask_ids:
                                ans = d.get("toolUseResult")
                                a = ans.get("answers") if isinstance(ans, dict) else None
                                if a is None:
                                    a = blocks_text(b.get("content")) if not isinstance(b.get("content"), str) else b.get("content")
                                turns[ask_ids[b["tool_use_id"]]][3] = a
                        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                            continue
                    u = clean_user(blocks_text(content))
                    if u:
                        turns.append(("user", u))
        col.session("claude-code", turns, sub)


def parse_codex(col, stats):
    files = glob.glob(os.path.join(HOME, ".codex/sessions/**/*.jsonl"), recursive=True)
    for f in files:
        turns = []
        sub = False
        call_idx = {}
        with open(f, errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                p = d.get("payload") or {}
                if d.get("type") == "session_meta":
                    src = p.get("source")
                    if isinstance(src, dict) or p.get("parent_thread_id") or src == "exec":
                        sub = True
                    continue
                if d.get("type") != "response_item":
                    continue
                pt = p.get("type")
                if pt == "message":
                    if p.get("role") == "assistant":
                        txt = blocks_text(p.get("content"))
                        if txt:
                            turns.append(("assistant", txt))
                    elif p.get("role") == "user":
                        u = clean_user(blocks_text(p.get("content")))
                        if u:
                            turns.append(("user", u))
                elif pt in ("function_call", "custom_tool_call") and is_ask_tool(p.get("name")):
                    call_idx[p.get("call_id")] = len(turns)
                    turns.append(["ask", p.get("name"), norm_generic_ask(p.get("name"), p.get("arguments") or p.get("input")), None])
                elif pt in ("function_call_output", "custom_tool_call_output") and p.get("call_id") in call_idx:
                    turns[call_idx[p["call_id"]]][3] = str(p.get("output"))[:500]
        col.session("codex", turns, sub)


def parse_droid(col, stats):
    files = glob.glob(os.path.join(HOME, ".factory/sessions/**/*.jsonl"), recursive=True)
    for f in files:
        turns = []
        sub = False
        ask_ids = {}
        with open(f, errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") == "session_start":
                    if d.get("callingSessionId"):
                        sub = True
                    continue
                if d.get("type") != "message":
                    continue
                m = d.get("message") or {}
                content = m.get("content") or []
                if m.get("role") == "assistant":
                    txt = blocks_text(content, ("text",))
                    if txt:
                        turns.append(("assistant", txt))
                    for b in content if isinstance(content, list) else []:
                        if isinstance(b, dict) and b.get("type") == "tool_use" and is_ask_tool(b.get("name")):
                            ask_ids[b.get("id")] = len(turns)
                            turns.append(["ask", b.get("name"), norm_generic_ask(b.get("name"), b.get("input")), None])
                elif m.get("role") == "user":
                    has_tr = False
                    if isinstance(content, list):
                        for b in content:
                            if isinstance(b, dict) and b.get("type") == "tool_result":
                                has_tr = True
                                if b.get("tool_use_id") in ask_ids:
                                    c = b.get("content")
                                    turns[ask_ids[b["tool_use_id"]]][3] = (c if isinstance(c, str) else blocks_text(c))[:500]
                    if has_tr:
                        continue
                    u = clean_user(blocks_text(content))
                    if u:
                        turns.append(("user", u))
        col.session("droid", turns, sub)


def parse_gemini(col, stats):
    for f in glob.glob(os.path.join(HOME, ".gemini/tmp/*/chats/*.json")):
        try:
            d = json.load(open(f, errors="replace"))
        except Exception:
            continue
        turns = []
        for m in d.get("messages", []):
            c = m.get("content")
            if isinstance(c, list):
                c = blocks_text(c)
            if m.get("type") == "user":
                u = clean_user(c)
                if u:
                    turns.append(("user", u))
            elif m.get("type") == "gemini":
                if c:
                    turns.append(("assistant", c))
                for tc in m.get("toolCalls") or []:
                    if is_ask_tool(tc.get("name")):
                        turns.append(["ask", tc.get("name"), norm_generic_ask(tc.get("name"), tc.get("args")), None])
        col.session("gemini", turns)


def parse_pi(col, stats):
    for f in glob.glob(os.path.join(HOME, ".pi/agent/sessions/**/*.jsonl"), recursive=True):
        turns = []
        with open(f, errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") != "message":
                    continue
                m = d.get("message") or {}
                if m.get("role") == "assistant":
                    txt = blocks_text(m.get("content"), ("text",))
                    if txt:
                        turns.append(("assistant", txt))
                    for b in m.get("content") or []:
                        if isinstance(b, dict) and b.get("type") == "toolCall" and is_ask_tool(b.get("name")):
                            turns.append(["ask", b.get("name"), norm_generic_ask(b.get("name"), b.get("arguments")), None])
                elif m.get("role") == "user":
                    u = clean_user(blocks_text(m.get("content")))
                    if u:
                        turns.append(("user", u))
        col.session("pi", turns)


def _pb_ids(buf):
    i, out = 0, []
    while i < len(buf):
        tag = buf[i]
        i += 1
        ln = sh = 0
        while i < len(buf):
            b = buf[i]
            i += 1
            ln |= (b & 0x7F) << sh
            sh += 7
            if b < 0x80:
                break
        if tag & 7 != 2:
            break
        val = buf[i:i + ln]
        i += ln
        if tag == 0x0A and ln == 32:
            out.append(val.hex())
    return out


def parse_cursor(col, stats):
    for f in glob.glob(os.path.join(HOME, ".cursor/chats/*/*/store.db")) + glob.glob(os.path.join(HOME, ".cursor/acp-sessions/*/store.db")):
        agent = "cursor-acp" if "acp-sessions" in f else "cursor"
        try:
            c = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
            meta = dict(c.execute("select key, value from meta"))
            m = json.loads(bytes.fromhex(meta["0"]).decode())
            blobs = dict(c.execute("select id, data from blobs"))
            c.close()
        except Exception:
            col.errors["cursor_open"] += 1
            continue
        root = blobs.get(m.get("latestRootBlobId"))
        if not root:
            continue
        turns = []
        for h in _pb_ids(root):
            try:
                j = json.loads(blobs[h])
            except Exception:
                continue
            role = j.get("role")
            content = j.get("content")
            if role == "user":
                u = clean_user(blocks_text(content))
                if u:
                    u = re.sub(r"^.*?<user_query>\s*|\s*</user_query>.*$", "", u, flags=re.S)
                    turns.append(("user", u))
            elif role == "assistant":
                txt = blocks_text(content, ("text",))
                if txt:
                    turns.append(("assistant", txt))
                for b in content if isinstance(content, list) else []:
                    if isinstance(b, dict) and b.get("type") == "tool-call" and is_ask_tool(b.get("toolName")):
                        turns.append(["ask", b.get("toolName"), norm_generic_ask(b.get("toolName"), b.get("args")), None])
        col.session(agent, turns)


def parse_augment(col, stats):
    for f in glob.glob(os.path.join(HOME, ".augment/sessions/*.json")):
        try:
            d = json.load(open(f, errors="replace"))
        except Exception:
            continue
        hist = d.get("chatHistory") or []
        first = next((h["exchange"].get("request_message") for h in hist if h.get("exchange", {}).get("request_message")), "") or ""
        sub = bool(re.match(r"\s*(\[Role Reminder|Generate a com|TASK TITLE:)", first))
        turns = []
        for h in hist:
            ex = h.get("exchange") or {}
            if h.get("isHistorySummary"):
                continue
            u = clean_user(ex.get("request_message"))
            if u:
                turns.append(("user", u))
            for n in ex.get("response_nodes") or []:
                tu = n.get("tool_use") if isinstance(n, dict) else None
                if tu and is_ask_tool(tu.get("tool_name")):
                    turns.append(["ask", tu.get("tool_name"), norm_generic_ask(tu.get("tool_name"), tu.get("input_json")), None])
            if ex.get("response_text"):
                turns.append(("assistant", ex["response_text"]))
        col.session("augment", turns, sub)


def parse_copilot(col, stats):
    files = glob.glob(os.path.join(HOME, ".copilot/session-state/*.jsonl")) + glob.glob(os.path.join(HOME, ".copilot/session-state/*/events.jsonl"))
    for f in files:
        turns = []
        with open(f, errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                t = d.get("type")
                data = d.get("data") or {}
                if t == "user.message":
                    u = clean_user(data.get("content"))
                    if u:
                        turns.append(("user", u))
                elif t == "assistant.message":
                    if data.get("content"):
                        turns.append(("assistant", data["content"]))
                    for tr in data.get("toolRequests") or []:
                        if is_ask_tool(tr.get("name")):
                            turns.append(["ask", tr.get("name"), norm_generic_ask(tr.get("name"), tr.get("arguments")), None])
        col.session("copilot", turns)


def parse_opencode(col, stats):
    db = os.path.join(HOME, ".local/share/opencode/opencode.db")
    if not os.path.exists(db):
        return
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = c.execute(
        "select p.session_id, m.time_created, m.id, json_extract(m.data,'$.role'), p.data "
        "from part p join message m on m.id = p.message_id order by p.session_id, m.time_created, p.time_created"
    )
    cur, turns, msg_role, buf = None, [], None, {}
    sessions = collections.OrderedDict()
    for sid, _, mid, role, pdata in rows:
        try:
            p = json.loads(pdata)
        except Exception:
            continue
        s = sessions.setdefault(sid, collections.OrderedDict())
        entry = s.setdefault(mid, {"role": role, "text": [], "asks": []})
        if p.get("type") == "text" and not p.get("synthetic"):
            entry["text"].append(p.get("text") or "")
        elif p.get("type") == "tool" and is_ask_tool(p.get("tool")):
            st = p.get("state") or {}
            entry["asks"].append(["ask", p.get("tool"), norm_generic_ask(p.get("tool"), st.get("input")), str(st.get("output"))[:300]])
    c.close()
    for sid, msgs in sessions.items():
        turns = []
        for e in msgs.values():
            txt = "\n".join(e["text"]).strip()
            if e["role"] == "user":
                u = clean_user(txt)
                if u:
                    turns.append(("user", u))
            else:
                if txt:
                    turns.append(("assistant", txt))
                turns.extend(e["asks"])
        col.session("opencode", turns)


BB_LOCAL_DUP = {"claude-code", "codex", "acp-droid", "acp-cursor", "acp-auggie", "acp-gh-copilot"}


def parse_bb(col, stats, bb_all=False):
    db = os.path.join(HOME, ".bb/bb.db")
    if not os.path.exists(db):
        return
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    prov = dict(c.execute("select id, provider_id from threads"))
    parent = dict(c.execute("select id, parent_thread_id from threads"))
    # Structured asks (all providers; tagged so they can be de-duplicated).
    answers = {}
    for (data,) in c.execute("select data from events where type='system/userQuestion/lifecycle'"):
        try:
            d = json.loads(data)
        except Exception:
            continue
        r = d.get("resolution") or {}
        if r.get("kind") == "user_answer":
            answers[d.get("interactionId")] = r.get("answers")
    for iid, tid, pid, rid, status, payload, resolution in c.execute(
        "select id, thread_id, provider_id, renderer_id, status, payload, resolution from pending_interactions"
    ):
        try:
            p = json.loads(payload)
        except Exception:
            continue
        if p.get("kind") == "user_question":
            qs = norm_bb_questions(p.get("questions"))
        elif rid == "ask-user-question":
            qs = norm_bb_questions((p.get("data") or {}).get("questions"))
        else:
            continue
        tprov = prov.get(tid) or pid or "?"
        col.asks.append({"agent": f"bb:{tprov}", "sid": f"bb:{tid}", "tool": rid or "provider_user_question", "questions": qs,
                         "answer": answers.get(iid) or status, "subagent": bool(parent.get(tid)),
                         "bb_dup_of_local": tprov in BB_LOCAL_DUP})
        col.ask_tool_names[(f"bb:{tprov}", rid or "provider_user_question")] += 1
    q = (
        "select thread_id, type, item_kind, "
        "case when item_kind='agentMessage' then json_extract(data,'$.item.text') "
        "when type='client/turn/requested' then data "
        "else json_extract(data,'$.item.tool') end "
        "from events where (type='item/completed' and item_kind in ('agentMessage','toolCall')) "
        "or type='client/turn/requested' order by thread_id, sequence"
    )
    cur, turns = None, []

    def flush():
        if cur is None:
            return
        p = prov.get(cur, "?")
        if not bb_all and p in BB_LOCAL_DUP:
            return
        col.session(f"bb:{p}", turns, bool(parent.get(cur)))

    for tid, typ, kind, val in c.execute(q):
        if tid != cur:
            flush()
            cur, turns = tid, []
        if kind == "agentMessage":
            if val:
                turns.append(("assistant", val))
        elif typ == "client/turn/requested":
            try:
                d = json.loads(val)
            except Exception:
                continue
            if d.get("initiator") not in (None, "user"):
                continue
            txt = "\n".join(i.get("text", "") for i in d.get("input") or [] if isinstance(i, dict))
            u = clean_user(txt)
            if u:
                turns.append(("user", u))
        elif kind == "toolCall" and val and is_ask_tool(val):
            col.ask_tool_names[(f"bb:{prov.get(tid)}:toolCall", val[:60])] += 1
    flush()
    c.close()


PARSERS = [
    ("claude-code", parse_claude), ("codex", parse_codex), ("droid", parse_droid), ("gemini", parse_gemini),
    ("pi", parse_pi), ("cursor", parse_cursor), ("augment", parse_augment), ("copilot", parse_copilot),
    ("opencode", parse_opencode), ("bb", parse_bb),
]


def summarize(col):
    main = [r for r in col.eot if not r["subagent"]]
    sub = [r for r in col.eot if r["subagent"]]

    def block(rs):
        qs = [r for r in rs if r["is_question"]]
        by_agent = collections.defaultdict(lambda: {"eot": 0, "questions": 0, "by_class": collections.Counter()})
        for r in rs:
            a = by_agent[r["agent"]]
            a["eot"] += 1
            if r["is_question"]:
                a["questions"] += 1
                a["by_class"][r["cls"]] += 1
        for a in by_agent.values():
            a["question_rate"] = round(a["questions"] / a["eot"], 3) if a["eot"] else 0
            a["by_class"] = dict(a["by_class"].most_common())
        reply_by_class = collections.defaultdict(collections.Counter)
        for r in qs:
            reply_by_class[r["cls"]][r["reply_kind"]] += 1
        return {
            "end_of_turn_messages": len(rs),
            "ending_with_question": len(qs),
            "question_rate": round(len(qs) / len(rs), 3) if rs else 0,
            "by_class": dict(collections.Counter(r["cls"] for r in qs).most_common()),
            "presentation": dict(collections.Counter(r["presentation"] for r in qs).most_common()),
            "multi_question_messages(>1 q in tail)": sum(1 for r in qs if r["n_questions_tail"] > 1),
            "rhetorical_suspect": sum(1 for r in qs if "rhetorical_suspect" in r["flags"]),
            "reply_kind": dict(collections.Counter(r["reply_kind"] for r in qs).most_common()),
            "reply_kind_by_class": {k: dict(v.most_common()) for k, v in reply_by_class.items()},
            "reply_kind_non_question_eot": dict(collections.Counter(r["reply_kind"] for r in rs if not r["is_question"]).most_common()),
            "by_agent": {k: v for k, v in sorted(by_agent.items(), key=lambda kv: -kv[1]["eot"])},
        }

    asks_main = [a for a in col.asks if not a.get("bb_dup_of_local")]
    nq = collections.Counter()
    nopt = collections.Counter()
    multi = 0
    by_agent_tool = collections.Counter()
    answered = collections.Counter()
    for a in asks_main:
        by_agent_tool[f"{a['agent']}::{a['tool']}"] += 1
        nq[len(a["questions"])] += 1
        for q in a["questions"]:
            nopt[len(q.get("options") or [])] += 1
            multi += bool(q.get("multi"))
        ans = a.get("answer")
        if ans is None:
            answered["unknown"] += 1
        elif isinstance(ans, str) and re.search(r"cancel|reject|interrupt|denied", ans, re.I):
            answered["cancelled/interrupted"] += 1
        else:
            answered["answered"] += 1
    return {
        "sessions": dict(col.sessions),
        "subagent_or_automated_sessions": dict(col.sub_sessions),
        "total_sessions": sum(col.sessions.values()),
        "total_subagent_sessions": sum(col.sub_sessions.values()),
        "interactive": block(main),
        "subagent_or_automated": block(sub),
        "structured_ask_calls": {
            "total_calls_dedup": len(asks_main),
            "total_calls_including_bb_duplicates": len(col.asks),
            "by_agent_tool": dict(by_agent_tool.most_common()),
            "questions_per_call": dict(sorted(nq.items())),
            "options_per_question": dict(sorted(nopt.items())),
            "total_questions": sum(k * v for k, v in nq.items()),
            "multi_select_questions": multi,
            "answer_status": dict(answered),
        },
        "ask_like_tool_names_seen": {f"{a}::{t}": n for (a, t), n in col.ask_tool_names.most_common()},
        "errors": dict(col.errors),
    }


def export(col, out):
    os.makedirs(out, exist_ok=True)
    seen = set()
    with open(os.path.join(out, "gold.jsonl"), "w") as fh:
        for a in col.asks:
            if a["subagent"]:
                continue
            for q in a["questions"]:
                text = redact(q.get("question"), 4000, keep_lines=True)
                opts = [redact(o, 400) for o in (q.get("options") or []) if o]
                key = (text, tuple(opts))
                # The bb-bridge tool shows up both as a local MCP call and as a BB interaction.
                if not text or key in seen:
                    continue
                seen.add(key)
                fh.write(json.dumps({"sid": a["sid"], "agent": a["agent"], "tool": a["tool"], "question": text,
                                     "header": redact(q.get("header"), 80), "options": opts, "multi": bool(q.get("multi"))},
                                    ensure_ascii=False) + "\n")
    with open(os.path.join(out, "eot.jsonl"), "w") as fh:
        for r in col.eot:
            if r["subagent"]:
                continue
            rec = {"sid": r["sid"], "agent": r["agent"], "is_question": r["is_question"],
                   "tail": redact(r["export_tail"], 1500, keep_lines=True)}
            if r["is_question"]:
                rec.update({"cls": r["cls"], "question": redact(r["question"], 600), "presentation": r["presentation"],
                            "options": [redact(o, 200) for o in r["options"]], "flags": r["flags"],
                            "reply_kind": r["reply_kind"], "reply": redact(r.get("reply"), 120)})
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "survey"),
    )
    ap.add_argument("--sample", type=int, default=300)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--bb-all", action="store_true", help="also parse BB threads whose provider has its own local store")
    ap.add_argument("--export", help="also write full scrubbed gold.jsonl and eot.jsonl (interactive only) to this dir")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    col = Collector()
    for name, fn in PARSERS:
        if args.only and name not in args.only:
            continue
        print(f"parsing {name}…", file=sys.stderr)
        try:
            if name == "bb":
                fn(col, None, args.bb_all)
            else:
                fn(col, None)
        except Exception as e:  # keep going on one broken store
            col.errors[f"{name}:{type(e).__name__}"] += 1
            print(f"  {name} failed: {e}", file=sys.stderr)
    if args.export:
        export(col, args.export)
    summ = summarize(col)
    # Examples per class, stratified by agent.
    rnd = random.Random(7)
    qs = [r for r in col.eot if r["is_question"] and not r["subagent"]]
    examples = collections.defaultdict(list)
    for r in rnd.sample(qs, len(qs)):
        if len(examples[r["cls"]]) < 4:
            examples[r["cls"]].append({"agent": r["agent"], "q": redact(r["question"], 190), "options": [redact(o, 60) for o in r["options"][:5]],
                                        "reply_kind": r["reply_kind"]})
    summ["examples"] = examples
    summ["structured_examples"] = [
        {"agent": a["agent"], "tool": a["tool"], "q": redact(q.get("question"), 190), "header": redact(q.get("header"), 40),
         "options": [redact(o, 60) for o in (q.get("options") or [])[:5]], "multi": q.get("multi")}
        for a in rnd.sample(col.asks, min(8, len(col.asks))) for q in a["questions"][:1]
    ]
    with open(os.path.join(args.out, "summary.json"), "w") as fh:
        json.dump(summ, fh, indent=2, default=str)
    # Stratified sample: all structured asks (capped) + questions per class/agent.
    sample = []
    for a in rnd.sample(col.asks, min(60, len(col.asks))):
        for q in a["questions"]:
            sample.append({"source": "structured", "agent": a["agent"], "tool": a["tool"], "text": redact(q.get("question"), 300),
                           "header": redact(q.get("header"), 40), "options": [redact(o, 80) for o in q.get("options") or []],
                           "multi": q.get("multi"), "gold": True})
    per = max(1, (args.sample - len(sample)) // max(1, len(set(r["cls"] for r in qs))))
    byc = collections.defaultdict(list)
    for r in rnd.sample(qs, len(qs)):
        byc[r["cls"]].append(r)
    picked = []
    i = 0
    while len(sample) + len(picked) < args.sample and any(i < len(v) for v in byc.values()):
        for cls, rs in byc.items():
            if i < len(rs) and len(sample) + len(picked) < args.sample:
                picked.append((cls, rs[i]))
        i += 1
    for cls, r in picked:
        if True:
            sample.append({"source": "end_of_turn", "agent": r["agent"], "cls": cls, "presentation": r["presentation"],
                           "question": redact(r["question"], 300), "tail": redact(r["text_tail"][-400:], 400),
                           "options": [redact(o, 80) for o in r["options"]], "n_questions_tail": r["n_questions_tail"],
                           "flags": r["flags"], "reply_kind": r["reply_kind"], "reply": redact(r.get("reply"), 40), "gold": False})
    with open(os.path.join(args.out, "sample.jsonl"), "w") as fh:
        for s in sample[: max(args.sample, 300)]:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(json.dumps({k: summ[k] for k in ("sessions", "total_sessions")}, indent=1), file=sys.stderr)


if __name__ == "__main__":
    main()
