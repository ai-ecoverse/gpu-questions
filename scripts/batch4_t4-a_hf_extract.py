"""Batch-4 t4-a copy of scripts/batch3_new-a_hf_extract.py (itself a copy of scripts/hf_extract.py).

Batch-4 changes:
  - a dataset entry may set "row_filter": {"path": "a.b", "regex": "..."}: the .jsonl file is
    streamed in full and only rows whose field matches are kept (recorded as "filtered");
  - .csv and .parquet files are downloaded too (entry "files" regex still applies), and
    whole-file downloads go to a .part file that is renamed only when the size matches the tree;
  - --more-formats also parses "User:/AI:" transcript CSVs (AnthropicInterviewer) and parquet
    message lists (needs pyarrow: `uv run --with pyarrow ...`);
  - --per-session defaults to 2 (the batch-4 spread rule).

Batch-3 new-a changes from the original (defaults otherwise unchanged):
  - a dataset entry may set "max_bytes": files larger than the remaining per-dataset
    budget are fetched with an HTTP Range request for their first max_bytes bytes,
    and a .jsonl file is cut back to its last complete line (recorded as "partial");
  - --more-formats also parses claudeset exports ({"turns": [{"type": "exchange", ...}]}).

Pull end-of-turn assistant messages from public Hugging Face agent-trace datasets.

Stdlib only. Two steps:
  uv run python scripts/hf_extract.py download   # pinned-revision files into data/hf/raw/
  uv run python scripts/hf_extract.py extract    # candidates into data/hf/candidates.jsonl

Batch 2 uses optional flags; without them the behaviour is unchanged:
  --root data/hf2              work directory (raw/, manifest.json, candidates.jsonl)
  --datasets FILE              JSON list of dataset ids or {"id", "agent", "files"} objects to download
  --exclude-sessions FILE ...  jsonl files whose `session` values are never extracted again
  --seen-datasets FILE ...     jsonl files whose `dataset` values mark candidates `seen_dataset`
  --more-formats               also parse the formats added for batch 2

A candidate is the last assistant text before the next real user message (or the
end of the session). Text is scrubbed with the redaction patterns from
scripts/extract.py, and anything that still looks personal is dropped.
"""

from __future__ import annotations

import argparse
import http.client
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from gq.tokenize import clean  # noqa: E402

HF = ROOT / "data" / "hf"
RAW = HF / "raw"
API = "https://huggingface.co/api/datasets"
PERMISSIVE = {"mit", "apache-2.0", "cc-by-4.0", "bsd-3-clause", "cc0-1.0"}
DATASET_CAP = 150_000_000
TOTAL_CAP = 2_500_000_000

# Interactive sessions with a human in the loop, chosen after reading each card.
DATASETS = [
    "thomasmustier/pi-mono-sessions",
    "thomasmustier/pi-extensions-sessions",
    "thomasmustier/pi-for-excel-sessions",
    "thomasmustier/pi-nes-sessions",
    "thomasmustier/economist-tui-sessions",
    "thomasmustier/clean-slides-sessions",
    "thomasmustier/pine-of-glass-sessions",
    "thomasmustier/pi-session-hud-sessions",
    "thomasmustier/pi-computer-use-sessions",
    "thomasmustier/pi-symphony-sessions",
    "thomasmustier/heypocket-reader-sessions",
    "julien-c/pi-sessions",
    "championswimmer/pi-coding-sessions",
    "abidlabs/gradio-pi-sessions",
    "abidlabs/trackio-pi-sessions",
    "OmarRabhI/pi-sessions",
    "Becks723/pi-traces",
    "woxQAQ/pi-web",
    "rgruchalski/combust-labs_pi-mono-docker",
    "lucacorbucci/llm_timeline_deepseek_v4_flash-pi",
    "thomwolf/am-session-sharing-design",
    "thomwolf/am-session-codex-check-d17941",
    "thomwolf/am-session-claude-code-1-c3cc0a",
    "thomwolf/am-session-claude-code-1-a66490",
    "victor/claude-fable-worldcup-2026-session",
    "build-small-hackathon/kirana-detective-build-traces",
    "naazimsnh02/tutordesk-agent-traces",
    "INONONO/fable-5.1-mario-trajectory",
    "INONONO/tarkov-customs-trajectory",
    "victor/fable-5-boeing-747-trace",
    "gabegoodhart/traces.claude-code.mlx-lm-granitemoehybrid",
    "kingkw1/read-along-ai-agent-traces",
    "ravi2505/homeroom-copilot-open-traces",
    "build-small-hackathon/hackathon-advisor-codex-traces",
    "build-small-hackathon/kicky-ai-codex-trace",
    "nielsr/r3al-vit-quantization-codex-trace",
    "drdavidtang/build-small-agent-trace",
    "vinhnx90/vtcode-sessions",
    "vedalken/merchantscroll-traces",
    "xhochy/conda-forge-agent-traces",
    "owao/qwen38-27B",
    "dacorvo/funes-recall-session-hermes-traces",
    "build-small-hackathon/MatchWise-agent-trace",
    "build-small-hackathon/TinyNarrator-agent-traces",
    "build-small-hackathon/sense-garden-traces",
    "build-small-hackathon/clue-vibes-traces",
    "build-small-hackathon/pit-wall-chaos-traces",
    "Samarth0710/traceweave",
    "AlinCiocan/fable-5-claude-code-traces",
    "yellowbeeblackbee/claude-traces",
    "armand0e/claude-fable-5-claude-code",
    "cfahlgren1/hermes-agent-trace-samples-2026-06-05",
]


DATASET_LIST = DATASETS


def get_json(url: str, tries: int = 5):
    for attempt in range(tries):  # the Hub API sometimes cuts a response short
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except (http.client.HTTPException, OSError, json.JSONDecodeError):
            if attempt == tries - 1:
                raise
            time.sleep(2 * (attempt + 1))


# ---------------------------------------------------------------- download
def download(args):
    RAW.mkdir(parents=True, exist_ok=True)
    manifest_path = HF / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    total = sum(p.stat().st_size for p in RAW.rglob("*") if p.is_file())
    for entry in DATASET_LIST:
        ds = entry["id"] if isinstance(entry, dict) else entry
        meta = get_json(f"{API}/{ds}")
        card = meta.get("cardData") or {}
        lic = card.get("license")
        lic = lic[0] if isinstance(lic, list) else lic
        if lic not in PERMISSIVE:
            print(f"skip {ds}: license {lic!r}")
            continue
        sha = meta["sha"]
        tree = get_json(f"{API}/{ds}/tree/{sha}?recursive=true")
        exts = tuple(entry.get("exts", [])) if isinstance(entry, dict) else ()
        files = [t for t in tree if t["type"] == "file" and t["path"].endswith((".jsonl", ".json", ".csv", ".parquet") + exts)]
        if isinstance(entry, dict) and entry.get("files"):  # regex over paths, e.g. to skip non-trace json
            files = [t for t in files if re.search(entry["files"], t["path"])]
        random.Random(ds).shuffle(files)
        used = 0
        kept = []
        for f in files:
            size = f.get("size", 0)
            dest = RAW / ds / f["path"]
            mb = entry.get("max_bytes") if isinstance(entry, dict) else None
            if mb and size > min(mb, DATASET_CAP - used) and used + mb <= DATASET_CAP and f["path"].endswith(".jsonl"):
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    url = f"https://huggingface.co/datasets/{ds}/resolve/{sha}/{urllib.parse.quote(f['path'])}"
                    req = urllib.request.Request(url, headers={"Range": f"bytes=0-{mb - 1}"})
                    buf = bytearray()
                    with urllib.request.urlopen(req, timeout=600) as r:
                        while chunk := r.read(1 << 20):
                            buf += chunk
                    buf = buf[: buf.rfind(b"\n") + 1]
                    dest.write_bytes(bytes(buf))
                got = dest.stat().st_size
                total += got
                used += got
                kept.append(f["path"])
                partial = manifest.setdefault(ds, {}).get("partial", {})
                partial[f["path"]] = got
                manifest[ds] = {**manifest.get(ds, {}), "partial": partial}
                continue
            rf = entry.get("row_filter") if isinstance(entry, dict) else None
            if rf and f["path"].endswith(".jsonl"):
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    url = f"https://huggingface.co/datasets/{ds}/resolve/{sha}/{urllib.parse.quote(f['path'])}"
                    pat = re.compile(rf["regex"])
                    kept_rows = read = 0
                    with urllib.request.urlopen(url, timeout=600) as r, open(str(dest) + ".part", "wb") as out:
                        for line in r:
                            read += len(line)
                            try:
                                v = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            for k in rf["path"].split("."):
                                v = v.get(k) if isinstance(v, dict) else None
                            if v is not None and pat.search(v if isinstance(v, str) else json.dumps(v)):
                                out.write(line)
                                kept_rows += 1
                    if read != size:
                        raise SystemExit(f"{ds}/{f['path']}: streamed {read} of {size} bytes")
                    Path(str(dest) + ".part").rename(dest)
                    print(f"  {f['path']}: kept {kept_rows} rows")
                got = dest.stat().st_size
                total += got
                used += got
                kept.append(f["path"])
                manifest.setdefault(ds, {})["filtered"] = {f["path"]: rf}
                continue
            if used + size > DATASET_CAP or total + size > TOTAL_CAP:
                continue
            if not dest.exists() or dest.stat().st_size != size:
                dest.parent.mkdir(parents=True, exist_ok=True)
                url = f"https://huggingface.co/datasets/{ds}/resolve/{sha}/{urllib.parse.quote(f['path'])}"
                for attempt in range(4):
                    with urllib.request.urlopen(url, timeout=300) as r, open(str(dest) + ".part", "wb") as out:
                        while chunk := r.read(1 << 20):
                            out.write(chunk)
                    if Path(str(dest) + ".part").stat().st_size == size:
                        break
                    print(f"  retry {f['path']}: size mismatch")
                else:
                    raise SystemExit(f"{ds}/{f['path']}: size mismatch after retries")
                Path(str(dest) + ".part").rename(dest)
                total += size
            used += size
            kept.append(f["path"])
        manifest[ds] = {"license": lic, "revision": sha, "files": kept, "bytes": used,
                        **{k: manifest[ds][k] for k in ("partial", "filtered") if k in manifest.get(ds, {})}}
        if isinstance(entry, dict) and entry.get("agent"):
            manifest[ds]["agent"] = entry["agent"]
        if isinstance(entry, dict) and entry.get("autonomous"):
            manifest[ds]["autonomous"] = True
        print(f"{ds}: {lic} {sha[:8]} {len(kept)} files {used / 1e6:.1f} MB (total {total / 1e6:.0f} MB)")
    manifest_path.write_text(json.dumps(manifest, indent=1))


# ---------------------------------------------------------------- scrubbing
def _load_local_extract():
    import importlib.util

    spec = importlib.util.spec_from_file_location("extract", ROOT / "scripts" / "extract.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_extract = _load_local_extract()
SECRET_RES = _extract._SECRET_RES
clean_user = _extract.clean_user

HOME_PATH_RE = re.compile(r"(/Users/|/home/|[A-Za-z]:\\{1,2}Users\\{1,2})([^/\\\s\"'`]+)")
PHONE_RE = re.compile(r"(?<![\w.])(?:\+\d{1,3}[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?![\w.])")
IP_RE = re.compile(r"\b(?!127\.0\.0\.1\b|0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b")
# Items that mention these are dropped rather than scrubbed.
DOUBTFUL_RE = re.compile(r"(?i)\b(ssn|social security|passport number|credit card number|iban|date of birth)\b")


def scrub(text: str) -> str | None:
    for r in SECRET_RES:
        text = r.sub("[REDACTED]", text)
    text = HOME_PATH_RE.sub(lambda m: m.group(1) + "[USER]", text)
    text = IP_RE.sub("[IP]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    if DOUBTFUL_RE.search(text):
        return None
    return text


# ---------------------------------------------------------------- parsing
# Each parser yields (session id, events), where events are ("user", text) or
# ("assistant", text). Tool results and injected context never count as "user".
def _blocks(content, kinds=("text", "output_text", "input_text")) -> str:
    if isinstance(content, str):
        return content
    out = []
    for b in content or []:
        if isinstance(b, dict) and b.get("type") in kinds and isinstance(b.get("text"), str):
            out.append(b["text"])
    return "\n".join(out)


def _read_jsonl(path: Path):
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def parse_pi(path: Path):
    events = []
    for d in _read_jsonl(path):
        if d.get("type") != "message":
            continue
        m = d.get("message") or {}
        role = m.get("role")
        if role == "user":
            u = clean_user(_blocks(m.get("content")))
            if u:
                events.append(("user", u))
        elif role == "assistant":
            t = _blocks(m.get("content"), ("text",))
            if t.strip():
                events.append(("assistant", t))
    yield path.stem, events


def parse_claude(path: Path):
    sessions: dict[str, list] = {}
    for d in _read_jsonl(path):
        t = d.get("type")
        if d.get("isSidechain"):
            continue
        events = sessions.setdefault(d.get("sessionId") or path.stem, [])
        m = d.get("message") or {}
        if t == "assistant":
            txt = _blocks(m.get("content"), ("text",))
            if txt.strip():
                events.append(("assistant", txt))
        elif t == "user":
            if d.get("isMeta") or d.get("isCompactSummary"):
                continue
            content = m.get("content")
            if isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                continue
            u = clean_user(_blocks(content))
            if u:
                events.append(("user", u))
    yield from sessions.items()


def parse_codex(path: Path):
    # Some exports keep only event_msg records, so collect both streams and prefer response_item.
    items: dict[str, list] = {}
    events: dict[str, list] = {}
    sid = path.stem
    for d in _read_jsonl(path):
        p = d.get("payload") or {}
        if d.get("type") == "session_meta":
            sid = p.get("id") or sid
            continue
        key = d.get("session_id") or sid
        if d.get("type") == "response_item" and p.get("type") == "message":
            role, text = p.get("role"), _blocks(p.get("content"), ("output_text", "input_text", "text"))
            stream = items.setdefault(key, [])
        elif d.get("type") == "event_msg" and p.get("type") in ("user_message", "agent_message"):
            role = "user" if p["type"] == "user_message" else "assistant"
            text = p.get("message") if isinstance(p.get("message"), str) else ""
            stream = events.setdefault(key, [])
        else:
            continue
        if role == "user":
            u = clean_user(text)
            if u and not u.lstrip().startswith(("# AGENTS.md", "<INSTRUCTIONS>")):
                stream.append(("user", u))
        elif role == "assistant" and text.strip():
            stream.append(("assistant", text))
    for key in dict.fromkeys([*items, *events]):
        ev = items.get(key, [])
        yield key, ev if any(k == "user" for k, _ in ev) else events.get(key, [])


def parse_hermes(path: Path):
    for d in _read_jsonl(path):
        events = []
        for m in d.get("messages") or []:
            c = m.get("content")
            if not isinstance(c, str) or not c.strip():
                continue
            if m.get("role") in ("user", "assistant"):
                events.append((m["role"], c))
        yield d.get("id") or path.stem, events


def parse_vtcode(path: Path):
    d = json.loads(path.read_text(errors="replace"))
    events = []
    for m in d.get("messages") or []:
        c = m.get("content")
        c = c if isinstance(c, str) else _blocks(c)
        if not c or not c.strip():
            continue
        role = str(m.get("role")).lower()
        if role == "user":
            u = clean_user(c)
            if u:
                events.append(("user", u))
        elif role == "assistant":
            events.append(("assistant", c))
    yield path.stem, events


def sniff(path: Path):
    if path.suffix == ".json":
        return parse_vtcode if path.name.startswith("session-vtcode") else None
    for d in _read_jsonl(path):
        if not isinstance(d, dict):
            return None
        if "messages" in d and "system_prompt" in d:
            return parse_hermes
        t = d.get("type")
        if t in ("session_meta", "response_item", "event_msg", "turn_context"):
            return parse_codex
        if t in ("session", "message", "model_change"):
            return parse_pi
        if t in ("user", "assistant", "summary", "system", "mode", "permission-mode", "file-history-snapshot",
                 "attachment", "ai-title", "last-prompt"):
            return parse_claude
    return None


# ---------------------------------------------------------------- batch-2 formats (--more-formats)
# User text that is tool output or shell echo rather than something the user typed.
NOT_USER_RE = re.compile(r"^\s*(<bash-|<local-command|\{'ToolUseResults'|<tool_result|\[Tool result|<environment_details>)")
# Per-session agent names for exports that mix harnesses in one file.
SESSION_AGENT: dict[str, str] = {}


def _user2(text):
    u = clean_user(text if isinstance(text, str) else _blocks(text))
    if u and not NOT_USER_RE.match(u):
        return u
    return None


def _msg_text(m: dict) -> str:
    c = m.get("content")
    if c is None and isinstance(m.get("text"), str):
        c = m["text"]
    if isinstance(c, list):
        c = _blocks(c, ("text", "output_text", "input_text"))
    return c if isinstance(c, str) else ""


def _msg_events(msgs):
    events = []
    for m in msgs or []:
        if not isinstance(m, dict):
            continue
        role = str(m.get("role") or m.get("from") or "").lower()
        text = _msg_text(m) if "value" not in m else (m.get("value") or "")
        if role in ("user", "human"):
            u = _user2(text)
            if u:
                events.append(("user", u))
        elif role in ("assistant", "gpt", "agent", "model") and text.strip():
            events.append(("assistant", text))
    return events


SOURCE_AGENT = {"claude": "claude-code", "claude-code": "claude-code", "codex": "codex", "cursor": "cursor",
                "opencode": "opencode", "gemini": "gemini-cli", "kiro": "kiro-cli", "kiro-cli": "kiro-cli",
                "hermes": "hermes", "pi": "pi", "openclaw": "openclaw"}


def _agent_from_model(model, source=None) -> str | None:
    src = str(source or "").lower()
    if src in SOURCE_AGENT:
        return SOURCE_AGENT[src]
    m = str(model or "").lower()
    if m.startswith("claude"):
        return "claude-code"
    if m.startswith(("gpt-", "o3", "o4", "codex")):
        return "codex"
    if "composer" in m:
        return "cursor"
    return None


def parse_msglist(path: Path):
    """One session per line (or per .json file) with a `messages` list: dataclaw, hermes, tau2, etc."""
    if path.suffix == ".json":
        d = json.loads(path.read_text(errors="replace"))
        records = d if isinstance(d, list) else [d]
    else:
        records = list(_read_jsonl(path))
    wrapped = [r for r in records if isinstance(r, dict) and r.get("type") == "message" and "message" in r]
    if wrapped:  # one chat per file, one message per line
        yield path.stem, _msg_events(r["message"] for r in wrapped)
        return
    for i, d in enumerate(records):
        if not isinstance(d, dict):
            continue
        msgs = d.get("messages") or d.get("conversations")
        if isinstance(msgs, str):
            try:
                msgs = json.loads(msgs)
            except json.JSONDecodeError:
                continue
        sid = str(d.get("session_id") or d.get("id") or d.get("task_id") or f"{path.stem}-{i}")
        if len(records) > 1 and not (d.get("session_id") or d.get("id")):
            sid = f"{path.stem}-{i}"
        agent = _agent_from_model(d.get("model"), d.get("source") or d.get("harness"))
        if not agent and "git_branch" in d and not d.get("source"):
            agent = "claude-code"  # dataclaw exports without a source field come from Claude Code
        if agent:
            SESSION_AGENT[sid] = agent
        yield sid, _msg_events(msgs)


def parse_opencode(path: Path):
    d = json.loads(path.read_text(errors="replace"))
    events = []
    for m in d.get("messages") or []:
        role = (m.get("info") or {}).get("role")
        parts = [p for p in m.get("parts") or [] if p.get("type") == "text" and not p.get("synthetic")]
        text = "\n".join(p.get("text") or "" for p in parts)
        if role == "user":
            u = _user2(text)
            if u:
                events.append(("user", u))
        elif role == "assistant" and text.strip():
            events.append(("assistant", text))
    yield (d.get("info") or {}).get("id") or path.stem, events


def parse_goose(path: Path):
    d = json.loads(path.read_text(errors="replace"))
    msgs = d.get("conversation") or d.get("messages") or []
    if isinstance(msgs, dict):
        msgs = msgs.get("messages") or []
    events = []
    for m in msgs:
        role = m.get("role")
        content = m.get("content")
        text = _blocks(content, ("text",)) if isinstance(content, list) else (content or "")
        if role == "user":
            # tool responses arrive as user messages without text blocks
            u = _user2(text) if text.strip() else None
            if u:
                events.append(("user", u))
        elif role == "assistant" and text.strip():
            events.append(("assistant", text))
    yield str(d.get("id") or path.stem), events


def parse_opentraces(path: Path):
    for d in _read_jsonl(path):
        events = []
        for st in d.get("steps") or []:
            if st.get("call_type") not in (None, "main"):
                continue
            text = st.get("content") or ""
            if st.get("role") == "user":
                u = _user2(text)
                if u:
                    events.append(("user", u))
            elif st.get("role") in ("agent", "assistant") and text.strip():
                events.append(("assistant", text))
        sid = d.get("session_id") or d.get("trace_id") or path.stem
        name = (d.get("agent") or {}).get("name")
        if name:
            SESSION_AGENT[sid] = name
        yield sid, events


def parse_claw(path: Path):
    """ATBench-Claw: a JSON list of {"trajectory": {"type": "session", "events": [...]}} (pi-like events)."""
    for i, rec in enumerate(json.loads(path.read_text(errors="replace"))):
        tr = rec.get("trajectory") or {}
        events = []
        for e in tr.get("events") or []:
            m = e.get("message") if isinstance(e.get("message"), dict) else e
            role = m.get("role")
            if role == "user":
                u = _user2(_blocks(m.get("content")))
                if u:
                    events.append(("user", u))
            elif role == "assistant":
                t = _blocks(m.get("content"), ("text",))
                if t.strip():
                    events.append(("assistant", t))
        yield str(rec.get("id") or f"{path.stem}-{i}"), events


def parse_claudeset(path: Path):
    """claudeset exports: one session per line, turns of type "exchange" (user text + assistant dict)."""
    for i, d in enumerate(_read_jsonl(path)):
        events = []
        for t in d.get("turns") or []:
            if t.get("type") != "exchange":
                continue
            u = _user2(t.get("user") or "")
            if u:
                events.append(("user", u))
            a = t.get("assistant")
            text = a.get("text") if isinstance(a, dict) else a
            if isinstance(text, str) and text.strip() and text.strip() != "(no content)":
                events.append(("assistant", text.replace("(no content)\n\n", "")))
        sid = str(d.get("id") or f"{path.stem}-{i}")
        SESSION_AGENT[sid] = "claude-code"
        yield sid, events


TRANSCRIPT_TURN_RE = re.compile(r"^(User|AI|Assistant):[ \t]?", re.M)


def parse_transcript_csv(path: Path):
    """AnthropicInterviewer: CSV rows (transcript_id, text), text is "Assistant:/AI:/User:" turns."""
    import csv

    csv.field_size_limit(1 << 30)
    with open(path, newline="", errors="replace") as fh:
        for i, row in enumerate(csv.DictReader(fh)):
            text = row.get("text") or ""
            parts = TRANSCRIPT_TURN_RE.split(text)
            events = []
            for who, body in zip(parts[1::2], parts[2::2]):
                body = body.strip()
                if not body:
                    continue
                if who == "User":
                    events.append(("user", body))
                else:
                    events.append(("assistant", body))
            yield str(row.get("transcript_id") or f"{path.stem}-{i}"), events


def parse_parquet_msgs(path: Path):
    """Parquet rows with a `messages` / `conversations` list of {role|from, content|value}."""
    import pyarrow.parquet as pq

    t = pq.read_table(path)
    col = "messages" if "messages" in t.schema.names else "conversations"
    ids = t.column("id").to_pylist() if "id" in t.schema.names else (
        t.column("hash").to_pylist() if "hash" in t.schema.names else None)
    for i, msgs in enumerate(t.column(col).to_pylist()):
        msgs = [json.loads(m) if isinstance(m, str) else m for m in msgs or []]
        yield str(ids[i] if ids else f"{path.stem}-{i}"), _msg_events(msgs)


MD_TURN_RE = re.compile(r"^## (User|Assistant)\s*$", re.M)


def parse_trace_md(path: Path):
    """Markdown trace exports: "# Trace: …", "Agent: …" line, then "## User" / "## Assistant" sections."""
    text = path.read_text(errors="replace")
    m = re.search(r"^Agent:\s*([\w-]+)", text, re.M)
    if m:
        SESSION_AGENT[path.stem] = {"cursor": "cursor", "claude": "claude-code", "claude-code": "claude-code"}.get(
            m.group(1).lower(), m.group(1).lower())
    parts = MD_TURN_RE.split(text)
    events = []
    for who, body in zip(parts[1::2], parts[2::2]):
        body = re.sub(r"\n---\s*$", "", body.strip()).strip()
        if not body:
            continue
        if who == "User":
            u = _user2(body)
            if u:
                events.append(("user", u))
        else:
            events.append(("assistant", body))
    yield path.stem, events


def parse_recordtype(path: Path):
    """Trace-viewer exports: {"recordType": "trace"|"message", "role", "textContent", "parts"}."""
    events = []
    for d in _read_jsonl(path):
        if d.get("recordType") == "trace":
            if d.get("agentId"):
                SESSION_AGENT[path.stem] = d["agentId"]
            continue
        if d.get("recordType") != "message":
            continue
        text = d.get("textContent")
        if not isinstance(text, str):
            text = "\n".join(p["content"]["text"] for p in d.get("parts") or []
                             if p.get("type") == "text" and isinstance((p.get("content") or {}).get("text"), str))
        if not text.strip():
            continue
        if d.get("role") == "user":
            u = _user2(text)
            if u:
                events.append(("user", u))
        elif d.get("role") == "assistant":
            events.append(("assistant", text))
    yield path.stem, events


def sniff2(path: Path):
    if path.suffix == ".md":
        with open(path, errors="replace") as fh:
            head = fh.read(400)
        return parse_trace_md if head.startswith("# Trace:") else None
    if path.suffix == ".csv":
        with open(path, errors="replace") as fh:
            head = fh.readline()
        return parse_transcript_csv if "transcript_id" in head else None
    if path.suffix == ".parquet":
        try:
            import pyarrow.parquet as pq
        except ImportError:
            print(f"warn {path}: pyarrow missing (run with `uv run --with pyarrow`)", file=sys.stderr)
            return None
        names = pq.read_schema(path).names
        return parse_parquet_msgs if ("messages" in names or "conversations" in names) else None
    if path.suffix == ".json":
        try:
            d = json.loads(path.read_text(errors="replace"))
        except (OSError, json.JSONDecodeError):
            return None
        first = d[0] if isinstance(d, list) and d else d
        if not isinstance(first, dict):
            return None
        if "info" in first and "messages" in first:
            return parse_opencode
        if "working_dir" in first:
            return parse_goose
        if isinstance(first.get("trajectory"), dict) and "events" in first["trajectory"]:
            return parse_claw
        if "messages" in first or "conversations" in first:
            return parse_msglist
        return None
    for d in _read_jsonl(path):
        if not isinstance(d, dict):
            return None
        if "steps" in d and "schema_version" in d:
            return parse_opentraces
        if d.get("recordType") in ("trace", "message"):
            return parse_recordtype
        if isinstance(d.get("turns"), list) and "claude_version" in d:
            return parse_claudeset
        if "messages" in d or "conversations" in d or (d.get("type") == "message" and "message" in d):
            return parse_msglist
        return None
    return None


AGENT_BY_PARSER = {parse_pi: "pi", parse_claude: "claude-code", parse_codex: "codex", parse_hermes: "hermes",
                   parse_vtcode: "vtcode"}
AGENT_BY_PARSER2 = {parse_msglist: "unknown", parse_opencode: "opencode", parse_goose: "goose", parse_claudeset: "claude-code",
                    parse_opentraces: "unknown", parse_claw: "openclaw", parse_transcript_csv: "unknown",
                    parse_parquet_msgs: "unknown", parse_trace_md: "unknown", parse_recordtype: "unknown"}
# Pi-format exports written by another harness.
AGENT_OVERRIDE = {"vedalken/merchantscroll-traces": "cursor", "owao/qwen38-27B": "opencode"}


def end_of_turn(events):
    """(turn index, final assistant text, next user message or None) for each turn."""
    out = []
    last = None
    turn = 0
    for kind, text in events:
        if kind == "assistant":
            last = text
        elif kind == "user":
            if last is not None:
                out.append((turn, last, text))
                turn += 1
            last = None
    if last is not None:
        out.append((turn, last, None))
    return out


def _field_values(paths, field):
    vals = set()
    for p in paths or []:
        for line in open(p):
            vals.add(json.loads(line)[field])
    return vals


def extract(args):
    manifest = json.loads((HF / "manifest.json").read_text())
    rng = random.Random(7)
    out = []
    stats = {}
    excluded = _field_values(args.exclude_sessions, "session")
    seen = _field_values(args.seen_datasets, "dataset")
    for ds, info in manifest.items():
        n = 0
        for rel in info["files"]:
            path = RAW / ds / rel
            parser = sniff(path) or (sniff2(path) if args.more_formats else None)
            if parser is None:
                continue
            agent = info.get("agent") or AGENT_OVERRIDE.get(ds) or {**AGENT_BY_PARSER, **AGENT_BY_PARSER2}[parser]
            if ds == "Samarth0710/traceweave":  # one harness per file, named in the prefix
                agent = rel.split("__")[0].replace("_", "-")
            try:
                sessions = list(parser(path))
            except Exception as e:  # one malformed file should not stop the run
                print(f"warn {ds}/{rel}: {e}", file=sys.stderr)
                continue
            for sid, events in sessions:
                if not any(k == "user" for k, _ in events):
                    if not (info.get("autonomous") and events):
                        continue
                    # `claude -p` logs omit the task prompt: treat the run as one turn
                    events = [("user", "[task]")] + events
                if f"{rel}#{sid}" in excluded:
                    continue
                turns = end_of_turn(events)
                sess_agent = agent if info.get("agent") else SESSION_AGENT.get(sid, agent)
                with_q = [t for t in turns if any(q in clean(t[1][-1500:])[-600:] for q in "?？")]
                without = [t for t in turns if t not in with_q]
                rng.shuffle(with_q)
                rng.shuffle(without)
                picked = (with_q + without)[:args.per_session]
                for turn, text, reply in sorted(picked, key=lambda t: t[0]):
                    raw_tail = scrub(text.strip()[-1500:])
                    if not raw_tail or len(raw_tail) < 20:
                        continue
                    cleaned = clean(raw_tail)
                    rec = {
                        "id": f"{ds.split('/')[-1]}:{sid[-12:]}:{turn}",
                        "dataset": ds, "license": info["license"], "revision": info["revision"],
                        "session": f"{rel}#{sid}", "turn": turn, "agent": sess_agent,
                        "raw_tail": raw_tail, "text": cleaned, "has_q": "?" in cleaned[-600:] or "？" in cleaned[-600:],
                        "reply": scrub(reply[:300]) if reply else None,
                    }
                    if ds in seen:
                        rec["seen_dataset"] = True
                    out.append(rec)
                    n += 1
        stats[ds] = n
    with open(HF / "candidates.jsonl", "w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for ds, n in stats.items():
        print(f"{n:5d} {ds}")
    print(f"{len(out)} candidates, {sum(r['has_q'] for r in out)} with '?' in the tail")


def main():
    global HF, RAW, DATASET_LIST
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["download", "extract"])
    ap.add_argument("--root", type=Path, default=HF, help="work directory (default data/hf)")
    ap.add_argument("--datasets", type=Path, help="JSON list of datasets to download (default: DATASETS)")
    ap.add_argument("--exclude-sessions", nargs="*", type=Path, help="jsonl files with sessions to skip")
    ap.add_argument("--seen-datasets", nargs="*", type=Path, help="jsonl files with already-used datasets")
    ap.add_argument("--per-session", type=int, default=2, help="turns kept per session (default 2)")
    ap.add_argument("--more-formats", action="store_true", help="also parse the batch-2 formats")
    args = ap.parse_args()
    HF, RAW = args.root, args.root / "raw"
    if args.datasets:
        DATASET_LIST = json.loads(args.datasets.read_text())
    {"download": download, "extract": extract}[args.step](args)


if __name__ == "__main__":
    main()
