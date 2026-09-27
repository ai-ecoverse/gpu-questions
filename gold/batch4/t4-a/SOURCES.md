# Hand-labeled test set, batch 4 (labeler t4-a): sources

`gold/batch4/t4-a/handlabeled.jsonl` holds 156 end-of-turn assistant messages: 54 with a question
and 102 without (34 of those hard negatives), 9 flagged `amb`. They come from 14 public Hugging
Face datasets of 10 owners, none of which is in `data/batch4/excluded_owners.json`.
`scripts/check_batch4.py gold/batch4/t4-a/handlabeled.jsonl` prints `OK`.

**The target of about 400 turns was not reached.** A full survey found only two new-owner,
permissively licensed sources of *interactive* Claude-family / IDE-agent sessions
(`zhiyaowang/dataclaw-zhiyaowang`, the Claude Code rows of `nmuendler/share-codex`), and both are
used up (zhiyaowang hit its 150 MB byte cap; share-codex has only 12 Claude sessions). The other
coding sources are autonomous benchmark runs, and those give only negatives. The owner rule was not relaxed.

## Selection

- Survey (`data/batch4/t4-a/survey*.py`, 2026-09-25): the `format:agent-traces` filter (501
  datasets, 371 without a license), about 90 name searches (agent names, "sessions", "traces",
  "dataclaw", "claude", "cursor", "copilot", "cline", "roo", "kilo", "zed", "continue", …) and
  tag filters (`dataclaw`, `claude-code`, `cursor`, `copilot`, `cline`, `windsurf`, `coding-agent`,
  `agent-traces`, …): 21,225 datasets. License rule of batch 1 (MIT, Apache-2.0, CC-BY-4.0,
  BSD-3-Clause, CC0-1.0); excluded owners dropped first. About 90 candidates had their card, tree and
  a sample read (`peek.py`, `peek.json`), plus their commit history ("Duplicate from …").
- Claims: `zhiyaowang/dataclaw-zhiyaowang` (all agents) and `nmuendler/share-codex` (Claude Code
  rows only; t4-b claimed the Codex rows first) are in `gold/batch4/CLAIMS.md`.
- Download/extract: `scripts/batch4_t4-a_hf_extract.py` (copy of the batch-3 new-a extractor), which adds
  a streamed row filter (share-codex: `metadata.collection_options_key` source `claude`), `.csv`/
  `.parquet`/`.md` inputs written via `.part` files with a size check, parsers for the
  AnthropicInterviewer transcript CSV, parquet message lists, markdown trace exports and
  `recordType` trace exports, an `autonomous` flag for `claude -p` logs that omit the task prompt,
  full-width `？` in the question preference, and `--per-session 2`. At most 2 turns per session
  (max used: 2). `data/batch4/t4-a/fetch_range.py` fetched byte ranges.

  ```sh
  uv run --with pyarrow python scripts/batch4_t4-a_hf_extract.py download --root data/batch4/t4-a --datasets data/batch4/t4-a/datasets.json
  uv run --with pyarrow python scripts/batch4_t4-a_hf_extract.py extract --root data/batch4/t4-a --more-formats
  uv run python scripts/check_batch4.py data/batch4/t4-a/candidates.jsonl > data/batch4/t4-a/precheck.txt
  python3 data/batch4/t4-a/make_queue.py     # quotas in data/batch4/t4-a/quota.json
  ```

  Result: 61,703 candidates. Every candidate id flagged by `check_batch4.py` was removed before
  queueing, and tails were deduplicated within t4-a. Queue: `data/batch4/t4-a/queue.jsonl`, keys
  `t4a:0000`–`t4a:0160`, per-dataset lanes q (`?`/`？` near the end, boundary patterns first),
  c (`?` in code/URL) and n (no `?`), round-robin. All 161 queued items were read; 156 labeled.
- Chat (the Interviewer transcripts, the Opus-Candid distill, claude-thinking): 31 of 156 items (19.9%).

## Skipped or dropped

- Mirrors / re-uploads: `ArkhAngelLifeJiggy/claude-fable-5-claude-code` (file list identical to
  excluded `armand0e`), `emperorfutures/dataclaw-code2` and `misterkerns/my-personal-claude-code-data`
  ("Duplicate from peteromallet/…"), `Quaxicron/dataclaw-zhiyaowang` (mirror of the original used
  here), all `*/dataclaw-peteromallet` forks, `dharshanrai/optim-agent-corpus-harvest`,
  `WhitzardAgent/*` and `nlile/misc-merged-claude-code-traces-v1` (compilations), `focustiki/sft-coding-agent-traces`
  (rows from pi-mono sessions), `clem/hf-coding-tools-traces_april26` (rehydrates davidkling's
  benchmark), `clem/opus4.7_reachy_mini_app_building` (identical to the reachy dataset used),
  `LanguaMan/claude-fable-worldcup-2026-session`, the `*-coding-and-debugging-traces`,
  `Complete-FABLE.5`, `claude-opus-4.6-10000x` and `TraceInversion` copies.
- Leak: `efederici/capybara-claude-15k-ita` was downloaded, but 104 of its tails were already in
  earlier pools, so the whole dataset was dropped.
- License / terms: `SALT-NLP/SWE-chat` (ODC-By), `archit11/*`, `robin0307/*` (no license);
  `saidutta69/agentic-vibecoding-traces` (the card forbids redistribution of the raw data).
- Scope / format: token-hash-only corpora (semianalysisai, wchen22, intelchen, thangquang09, TraceLab),
  OpenHands/SWE-agent/pi/codex/gemini data (t4-b's families: ScaleAI swe-oec, vibeapps-chat-fabric,
  MRiabov, katana, npcsh), `fdicastri/tandem-sessions` and the other t4-b claims,
  `nassimjp/copilot-raw-chats` (Pashto, which I cannot label reliably), synthetic or non-trace
  datasets (Narmeen07, dicemy, compsciencelab, CodAGE, …).
- Items read but not labeled (5): t4a:0042 (verbatim duplicate question of t4a:0033), t4a:0115 and
  t4a:0135 (real names with session cookies), t4a:0138 (a domain containing a person's name),
  t4a:0125 (a partly redacted SSH password).

## Scrubbing

The extractor applies batch 1's scrubbing (secret patterns incl. emails, home paths, IPs, phone
numbers). Afterwards the output was scanned again for emails, key/token/JWT/PEM patterns, IPs, home paths,
phones, password assignments and long hex strings. The only hits were `127.0.0.1` and dataclaw's
own pseudonymized `/user_<hash>` home directories.

## Labeling

Every item was read and labeled by hand in `gold/batch4/t4-a/annotations.txt`, following
`gold/CONVENTIONS.md`, the batch-2 decisions in `gold/batch2/SOURCES.md` and `gold/batch3/QUESTIONS.md`.
No model output was consulted. `build_gold.py` 0 errors; `validate_gold.py` 0 errors (23 compiler
differences: Chinese yes/no phrasing, one-sentence double questions, spans after a dash).
New decisions are in `gold/batch4/QUESTIONS.md`. Progress per round: [`PROGRESS.md`](PROGRESS.md).

| | Count |
|---|---:|
| items | 156 |
| with a question | 54 (34.6%) |
| negatives (hard) | 102 (34) |
| questions | 72 |
| yes_no / either_or / multi_choice / open | 28 / 23 / 2 / 19 |
| boundary items (either/or, multi-choice, or an "or"/"还是"/"/" in the question) | 33 |
| propose / multiSelect / default | 26 / 1 / 1 |
| ambiguous | 9 |
| difficulty easy / medium / hard | 88 / 60 / 8 |

Agents: claude-code 83, claude-chat 31, codex 23, opencode 10, cursor 9 (codex/opencode come from the
mixed zhiyaowang export). Formats: dataclaw message list (zhiyaowang), share-codex message list, Claude
Code native / `claude -p` stream JSONL (rs545837, CooperBench, AgentNativeResearchLab, aibengineering),
markdown trace export and `recordType` trace export (clem), transcript CSV (AnthropicInterviewer),
ShareGPT JSON (Verdugie), parquet (claude-thinking). Languages: English and Chinese (zhiyaowang).

## Datasets

| dataset | license | pinned revision | downloaded | agents | items | with Q | neg (hard) |
|---|---|---|---|---|---:|---:|---:|
| [`zhiyaowang/dataclaw-zhiyaowang`](https://huggingface.co/datasets/zhiyaowang/dataclaw-zhiyaowang) | mit | `f5157333cbc22489661122a9bc5347b137144900` | 149.5 MB (range-fetched prefix) | codex 23, claude-code 11, opencode 10, cursor 7 | 51 | 17 | 34 (15) |
| [`nmuendler/share-codex`](https://huggingface.co/datasets/nmuendler/share-codex) | cc-by-4.0 | `368d63924356a773add5fe73f31ec014642ed0f1` | 12.6 MB (Claude rows only) | claude-code 24 | 24 | 16 | 8 (3) |
| [`Verdugie/opus-candid-training-data`](https://huggingface.co/datasets/Verdugie/opus-candid-training-data) | apache-2.0 | `59a614a5cac6730c81dc489cd91cc2ab05934f5b` | 106.7 MB | claude-chat 18 | 18 | 11 | 7 (4) |
| [`rs545837/entity-native-agent-sessions`](https://huggingface.co/datasets/rs545837/entity-native-agent-sessions) | mit | `d5575a8e0d85d3f41071d27c4e587b5a0807f3b4` | 9.8 MB | claude-code 14 | 14 | 0 | 14 (2) |
| [`CooperBench/qwen9b-coop-claude-code`](https://huggingface.co/datasets/CooperBench/qwen9b-coop-claude-code) | mit | `6013d5c8c6ad78498bcd9d8dd1635aa0dd97abae` | 35.1 MB | claude-code 11 | 11 | 0 | 11 (3) |
| [`CooperBench/qwen9b-solo-claude-code`](https://huggingface.co/datasets/CooperBench/qwen9b-solo-claude-code) | mit | `7394d24338afee35bea8d65c8e2304ed52aebe37` | 50.2 MB | claude-code 10 | 10 | 0 | 10 (2) |
| [`Anthropic/AnthropicInterviewer`](https://huggingface.co/datasets/Anthropic/AnthropicInterviewer) | mit | `c9e1ec1e6b093712b9c42235c7303ece647490e9` | 11.4 MB | claude-chat 9 | 9 | 9 | 0 (0) |
| [`clem/traces_april26`](https://huggingface.co/datasets/clem/traces_april26) | apache-2.0 | `4a4449efa07184e14c24a17d6a1c204f7191b9a6` | 0.2 MB | claude-code 4, cursor 2 | 6 | 0 | 6 (3) |
| [`SethBurkart/claude-thinking`](https://huggingface.co/datasets/SethBurkart/claude-thinking) | apache-2.0 | `265a5abfb0a47528fe1a685ff1112c334209182e` | 0.6 MB | claude-chat 4 | 4 | 0 | 4 (2) |
| [`AgentNativeResearchLab/tbs-claude-opus5-high-trajectories`](https://huggingface.co/datasets/AgentNativeResearchLab/tbs-claude-opus5-high-trajectories) | apache-2.0 | `8382b78c29b59eb109a0ffef1cce7f5b2f00ca75` | 3.0 MB | claude-code 3 | 3 | 0 | 3 (0) |
| [`AgentNativeResearchLab/arc-agi3-cc-opus4.8-g50t`](https://huggingface.co/datasets/AgentNativeResearchLab/arc-agi3-cc-opus4.8-g50t) | cc-by-4.0 | `246a02595c9f6ea20818ec27ace800aa4a9b57ea` | 1.0 MB | claude-code 2 | 2 | 0 | 2 (0) |
| [`clem/opus_4.7_buildmyfirstreachyminiapp`](https://huggingface.co/datasets/clem/opus_4.7_buildmyfirstreachyminiapp) | apache-2.0 | `968788a885ae08947f7d0d233c9a66fa5ba307f7` | 0.3 MB | claude-code 2 | 2 | 1 | 1 (0) |
| [`AgentNativeResearchLab/arc-agi3-cc-fable5-ft09`](https://huggingface.co/datasets/AgentNativeResearchLab/arc-agi3-cc-fable5-ft09) | cc-by-4.0 | `7195030827bd6acfd25bd1068b4fcc3f0fd6f8ef` | 0.7 MB | claude-code 1 | 1 | 0 | 1 (0) |
| [`aibengineering/beat-the-game-minecraft`](https://huggingface.co/datasets/aibengineering/beat-the-game-minecraft) | cc-by-4.0 | `de4bfb91972d263e592276c3a33a8b49d3e75d81` | 13.6 MB | claude-code 1 | 1 | 0 | 1 (0) |

CC-BY-4.0 datasets require attribution; this table and each record's `dataset`, `revision` and
`session` fields provide it. `data/batch4/t4-a/` (downloads, candidates, queue, helper scripts) is local
only.

## Rebuilding

```sh
uv run python scripts/build_gold.py --queue data/batch4/t4-a/queue.jsonl \
    --ann gold/batch4/t4-a/annotations.txt --out gold/batch4/t4-a/handlabeled.jsonl
uv run python scripts/validate_gold.py gold/batch4/t4-a/handlabeled.jsonl --quiet
uv run python scripts/check_batch4.py gold/batch4/t4-a/handlabeled.jsonl
```
