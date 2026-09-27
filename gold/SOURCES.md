# Hand-labeled test set: sources

`gold/handlabeled.jsonl` holds 663 final assistant turns (412 with a question, 251
without, after adjudication) from 52 public Hugging Face agent-trace datasets. None of it comes from the
local trace export that the tagger is trained on, so it is an independent test set.
`gq/evaluate.py` loads it as the `hand/*` sets.

## Selection

- Surveyed 500 Hugging Face datasets tagged or named as agent traces/sessions (API, June 2026).
- Kept only permissive licenses: MIT, Apache-2.0, CC-BY-4.0, BSD-3-Clause, CC0-1.0.
  Skipped AGPL, "other", unlicensed, and non-commercial datasets, plus one 222 MB dataset
  (size cap: 150 MB per dataset, 2.5 GB total).
- Every download is pinned to the revision in the table below (full SHAs in each
  record's `revision` field and in `data/hf/manifest.json`, which is git-ignored).
- `scripts/hf_extract.py` downloads, parses Claude Code / Codex / pi / Cursor /
  opencode / vtcode / hermes / Copilot session formats, takes the last assistant text
  of each turn, and keeps at most 3 turns per session (preferring turns with a `?`).
- Scrubbing reuses the secret patterns from `scripts/extract.py` and adds home paths,
  IPs, and phone numbers; items that still look doubtful are dropped. `raw_tail` is the
  last 1500 characters after scrubbing and `text` is that tail after `gq.tokenize.clean`.
- Candidates were deduplicated on their last 300 characters. All 563 candidates with a
  `?` were reviewed and 559 kept; three repeated greetings and one tail that cuts off
  its own options (`kirana-detective`, "Option A" truncated) were skipped. From the 260
  negative candidates (no question detected), the first 100 in queue order were labeled,
  plus the 4 later ones that contain a question mark. Two of those 6 use the full-width
  `？` and turned out to be real questions.

## Labeling

Every item was read and labeled by hand (by an AI agent, see below) in
`gold/annotations.txt`; `scripts/build_gold.py` only locates the written span texts and
`scripts/validate_gold.py` checks spans and compares the hand-written expectation with
what `gq/compile.py` derives from the spans. Remaining differences (166 after adjudication, mostly
`propose`) are documented compiler limitations, not label errors; the item's `note`
says why.

A second agent (GPT-6-Sol) later adjudicated the 102 items flagged ambiguous against the
rules in `gold/CONVENTIONS.md`: 94 labels kept, 8 changed, none left ambiguous. A
consistency sweep then fixed 5 unflagged items. Every decision is in
`gold/adjudication.jsonl`. The coverage table below predates adjudication.

Main guideline decisions (see [`CONVENTIONS.md`](CONVENTIONS.md) for adjudicated rules and examples):

- **Q spans** cover the question sentence from its first word through `?`, or an
  interrogative lead-in through `:` when its choice list completes the question.
  Labels such as `**Share unit** —` or `1.` are excluded when they are not part of
  the question. A choice split over two sentences ("Shall I…? Or would you rather…?")
  is one span.
- **Options** are distinct answers or deliverables offered to the user, including a
  nearby list when the question asks the user to choose from it. Use the bold label
  or short phrase before a description; exclude trailing explanatory parentheticals.
  Escape hatches such as "or something else" and illustrative `e.g.` examples inside
  a question are not options. A later `For example:` list of selectable diagnostic
  sub-questions can supply options without their `?`. Incomplete lists do not supply
  a partial choice set.
- **kind** is either_or for two distinct alternatives and multi_choice for three or
  more, including "Want me to X or Y?" offers. A single adjustment with two possible
  attributes ("different color or label?") is yes_no. Clarification and other
  information requests are open even when phrased "Could you…?" or "Do you know…?".
  A single named possibility plus an open-ended escape hatch is yes_no for a
  confirmation and open for a request to name an unspecified alternative.
- **propose** is true when a yes answer lets the agent act: "Want me to…", "Want a
  diff?", "Shall I…", "OK if I…", confirm-the-plan questions. "Should I work on X or Y?"
  which-questions and "How can I help?" are false.
- **multiSelect** for "(s)", "any of these", "and/or", "some or all", or when the agent
  suggests doing both, provided there are enumerated options to select.
- **default** comes from a recommendation marker ("(recommended)", "(my lean)",
  labeled as REC spans) or from prose ("I'd lean toward…", "My recommendation: …").
- **Negatives** have no question addressed to the user. Hard negatives (note starts
  with `hard:`) include rhetorical or self-answered questions, quoted questions,
  `?` in URLs or code, and offers without a question ("If you want, I can…").
- `difficulty` is the labeler's estimate (easy / medium / hard); `ambiguous` is kept
  only when two readings remain equally valid after applying the conventions.

## Coverage

| | Target | Got |
|---|---:|---:|
| yes/no | 80 | 195 |
| inline choice | 60 | 109 |
| list choice | 50 | 53 |
| open | 30 | 87 |
| multi-question | 20 | 44 |
| recommendation / default | 30 | **14** (3 explicit REC spans) |
| negatives | 150 | 250 |
| hard negatives | 50 | 148 |

The recommendation target was not met: only 15 candidates in all 2,592 extracted turns
carry an explicit marker, and prose defaults are rare. 86 of the hard negatives come
from `Samarth0710/traceweave`, whose final turns are mostly model-comparison judgments
full of quoted questions; they are real but repetitive.

## Datasets

| Dataset | License | Revision | Agent | Positives | Negatives |
|---|---|---|---|---:|---:|
| [`thomasmustier/pi-extensions-sessions`](https://huggingface.co/datasets/thomasmustier/pi-extensions-sessions) | mit | `17e22c5903cb` | pi | 128 | 6 |
| [`Samarth0710/traceweave`](https://huggingface.co/datasets/Samarth0710/traceweave) | mit | `f5abd7e1c623` | claude-code, copilot | 4 | 89 |
| [`thomasmustier/pi-for-excel-sessions`](https://huggingface.co/datasets/thomasmustier/pi-for-excel-sessions) | mit | `052a7c665480` | pi | 72 | 15 |
| [`thomasmustier/pi-mono-sessions`](https://huggingface.co/datasets/thomasmustier/pi-mono-sessions) | mit | `d0895347aaac` | pi | 60 | 12 |
| [`vedalken/merchantscroll-traces`](https://huggingface.co/datasets/vedalken/merchantscroll-traces) | mit | `495c3ee7ba3e` | cursor | 17 | 8 |
| [`thomasmustier/economist-tui-sessions`](https://huggingface.co/datasets/thomasmustier/economist-tui-sessions) | mit | `95b6dba5c139` | pi | 17 | 3 |
| [`vinhnx90/vtcode-sessions`](https://huggingface.co/datasets/vinhnx90/vtcode-sessions) | mit | `78049282e2b4` | vtcode | 16 | 4 |
| [`armand0e/claude-fable-5-claude-code`](https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code) | mit | `7388ef96f317` | claude-code | 12 | 7 |
| [`woxQAQ/pi-web`](https://huggingface.co/datasets/woxQAQ/pi-web) | mit | `1928c53ba9e2` | pi | 9 | 8 |
| [`thomasmustier/pi-nes-sessions`](https://huggingface.co/datasets/thomasmustier/pi-nes-sessions) | mit | `47d55a2545e0` | pi | 14 | 2 |
| [`thomasmustier/pine-of-glass-sessions`](https://huggingface.co/datasets/thomasmustier/pine-of-glass-sessions) | mit | `b9a6b263895c` | pi | 10 | 3 |
| [`naazimsnh02/tutordesk-agent-traces`](https://huggingface.co/datasets/naazimsnh02/tutordesk-agent-traces) | mit | `4d538090ddd3` | claude-code | 8 | 4 |
| [`thomasmustier/clean-slides-sessions`](https://huggingface.co/datasets/thomasmustier/clean-slides-sessions) | mit | `0ecc915c7d32` | pi | 10 | 2 |
| [`julien-c/pi-sessions`](https://huggingface.co/datasets/julien-c/pi-sessions) | cc-by-4.0 | `700416886204` | pi | 6 | 3 |
| [`AlinCiocan/fable-5-claude-code-traces`](https://huggingface.co/datasets/AlinCiocan/fable-5-claude-code-traces) | cc-by-4.0 | `e33ebbca230a` | claude-code | 2 | 5 |
| [`rgruchalski/combust-labs_pi-mono-docker`](https://huggingface.co/datasets/rgruchalski/combust-labs_pi-mono-docker) | apache-2.0 | `7829c4a27427` | pi | 5 | 2 |
| [`abidlabs/gradio-pi-sessions`](https://huggingface.co/datasets/abidlabs/gradio-pi-sessions) | mit | `7af63c1cf3cb` | pi | 2 | 4 |
| [`build-small-hackathon/kirana-detective-build-traces`](https://huggingface.co/datasets/build-small-hackathon/kirana-detective-build-traces) | mit | `d61ca08eac92` | claude-code | 2 | 4 |
| [`yellowbeeblackbee/claude-traces`](https://huggingface.co/datasets/yellowbeeblackbee/claude-traces) | cc0-1.0 | `0cad5c49dfb8` | claude-code | 3 | 3 |
| [`OmarRabhI/pi-sessions`](https://huggingface.co/datasets/OmarRabhI/pi-sessions) | apache-2.0 | `d3d60fea0914` | pi | 3 | 2 |
| [`xhochy/conda-forge-agent-traces`](https://huggingface.co/datasets/xhochy/conda-forge-agent-traces) | bsd-3-clause | `046e1aff3998` | pi | 1 | 4 |
| [`dacorvo/funes-recall-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/funes-recall-session-hermes-traces) | apache-2.0 | `6384aea7e6d6` | hermes | 2 | 2 |
| [`drdavidtang/build-small-agent-trace`](https://huggingface.co/datasets/drdavidtang/build-small-agent-trace) | mit | `af8e727914b9` | codex | 1 | 3 |
| [`kingkw1/read-along-ai-agent-traces`](https://huggingface.co/datasets/kingkw1/read-along-ai-agent-traces) | mit | `0bee208f7b13` | codex | 0 | 4 |
| [`Becks723/pi-traces`](https://huggingface.co/datasets/Becks723/pi-traces) | mit | `70163ead1b50` | pi | 2 | 1 |
| [`build-small-hackathon/hackathon-advisor-codex-traces`](https://huggingface.co/datasets/build-small-hackathon/hackathon-advisor-codex-traces) | apache-2.0 | `c7a79f391597` | codex | 0 | 3 |
| [`build-small-hackathon/kicky-ai-codex-trace`](https://huggingface.co/datasets/build-small-hackathon/kicky-ai-codex-trace) | apache-2.0 | `b69aff032c2f` | codex | 3 | 0 |
| [`nielsr/r3al-vit-quantization-codex-trace`](https://huggingface.co/datasets/nielsr/r3al-vit-quantization-codex-trace) | mit | `364ab50da7fc` | codex | 0 | 3 |
| [`ravi2505/homeroom-copilot-open-traces`](https://huggingface.co/datasets/ravi2505/homeroom-copilot-open-traces) | mit | `3e53bfb74293` | codex | 0 | 3 |
| [`thomasmustier/pi-session-hud-sessions`](https://huggingface.co/datasets/thomasmustier/pi-session-hud-sessions) | mit | `041268c03fd2` | pi | 1 | 2 |
| [`thomasmustier/pi-symphony-sessions`](https://huggingface.co/datasets/thomasmustier/pi-symphony-sessions) | mit | `0697350f9654` | pi | 0 | 3 |
| [`thomwolf/am-session-sharing-design`](https://huggingface.co/datasets/thomwolf/am-session-sharing-design) | apache-2.0 | `36dd5850a4f0` | claude-code | 3 | 0 |
| [`victor/fable-5-boeing-747-trace`](https://huggingface.co/datasets/victor/fable-5-boeing-747-trace) | mit | `e146afb46a99` | claude-code | 0 | 3 |
| [`abidlabs/trackio-pi-sessions`](https://huggingface.co/datasets/abidlabs/trackio-pi-sessions) | mit | `4c1420de7fdd` | pi | 0 | 2 |
| [`build-small-hackathon/MatchWise-agent-trace`](https://huggingface.co/datasets/build-small-hackathon/MatchWise-agent-trace) | mit | `10606ddabd12` | codex | 0 | 2 |
| [`build-small-hackathon/TinyNarrator-agent-traces`](https://huggingface.co/datasets/build-small-hackathon/TinyNarrator-agent-traces) | mit | `0222953b6069` | codex | 0 | 2 |
| [`build-small-hackathon/clue-vibes-traces`](https://huggingface.co/datasets/build-small-hackathon/clue-vibes-traces) | cc-by-4.0 | `fe8ba2792ec5` | codex | 0 | 2 |
| [`build-small-hackathon/pit-wall-chaos-traces`](https://huggingface.co/datasets/build-small-hackathon/pit-wall-chaos-traces) | cc-by-4.0 | `60bd7c2609d7` | codex | 0 | 2 |
| [`build-small-hackathon/sense-garden-traces`](https://huggingface.co/datasets/build-small-hackathon/sense-garden-traces) | cc-by-4.0 | `1a13d90deb69` | codex | 0 | 2 |
| [`cfahlgren1/hermes-agent-trace-samples-2026-06-05`](https://huggingface.co/datasets/cfahlgren1/hermes-agent-trace-samples-2026-06-05) | apache-2.0 | `80c32a72cc94` | hermes | 0 | 2 |
| [`championswimmer/pi-coding-sessions`](https://huggingface.co/datasets/championswimmer/pi-coding-sessions) | mit | `f655c6c2aabf` | pi | 0 | 2 |
| [`gabegoodhart/traces.claude-code.mlx-lm-granitemoehybrid`](https://huggingface.co/datasets/gabegoodhart/traces.claude-code.mlx-lm-granitemoehybrid) | apache-2.0 | `8717352ccbf2` | claude-code | 0 | 2 |
| [`lucacorbucci/llm_timeline_deepseek_v4_flash-pi`](https://huggingface.co/datasets/lucacorbucci/llm_timeline_deepseek_v4_flash-pi) | mit | `b46eaa8c12b4` | pi | 0 | 2 |
| [`owao/qwen38-27B`](https://huggingface.co/datasets/owao/qwen38-27B) | mit | `2998889fe3f2` | opencode | 0 | 2 |
| [`thomasmustier/heypocket-reader-sessions`](https://huggingface.co/datasets/thomasmustier/heypocket-reader-sessions) | mit | `70f6d07dfb7b` | pi | 0 | 2 |
| [`thomasmustier/pi-computer-use-sessions`](https://huggingface.co/datasets/thomasmustier/pi-computer-use-sessions) | mit | `8353644936ee` | pi | 0 | 2 |
| [`thomwolf/am-session-claude-code-1-c3cc0a`](https://huggingface.co/datasets/thomwolf/am-session-claude-code-1-c3cc0a) | apache-2.0 | `037d661cb58d` | claude-code | 0 | 2 |
| [`INONONO/fable-5.1-mario-trajectory`](https://huggingface.co/datasets/INONONO/fable-5.1-mario-trajectory) | mit | `210c7cea2e75` | claude-code | 0 | 1 |
| [`INONONO/tarkov-customs-trajectory`](https://huggingface.co/datasets/INONONO/tarkov-customs-trajectory) | mit | `a0557bb951af` | claude-code | 0 | 1 |
| [`thomwolf/am-session-claude-code-1-a66490`](https://huggingface.co/datasets/thomwolf/am-session-claude-code-1-a66490) | apache-2.0 | `e8a022e9f8bf` | claude-code | 0 | 1 |
| [`thomwolf/am-session-codex-check-d17941`](https://huggingface.co/datasets/thomwolf/am-session-codex-check-d17941) | apache-2.0 | `d89ae23edfef` | codex | 0 | 1 |
| [`victor/claude-fable-worldcup-2026-session`](https://huggingface.co/datasets/victor/claude-fable-worldcup-2026-session) | cc-by-4.0 | `3a8b426a4235` | claude-code | 0 | 1 |

CC-BY-4.0 datasets require attribution; this table and each record's `dataset`,
`revision`, and `session` fields provide it.

## Rebuilding

```sh
uv run python scripts/hf_extract.py          # download + extract (needs network)
uv run python scripts/build_gold.py          # annotations -> gold/handlabeled.jsonl
uv run python scripts/validate_gold.py --quiet
uv run python scripts/gold_stats.py
```

`build_gold.py` reads the candidate queue in `data/hf/queue.jsonl`, which is git-ignored
along with the downloads.
