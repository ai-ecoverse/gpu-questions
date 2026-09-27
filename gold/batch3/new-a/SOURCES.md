# Hand-labeled set, batch 3 (labeler new-a): sources

`gold/batch3/new-a/handlabeled.jsonl` holds 1,486 end-of-turn assistant messages: 874 with a
question and 612 without (348 of those hard negatives), 79 flagged `amb`. They come from 26
public Hugging Face datasets of Claude-family / IDE-agent / coding-assistant traces and chats.
None of the 26 datasets appears in batch 1 or batch 2; two owners do (`woctordho`,
`victor`), with different datasets. No batch-1/2 session was reused (excluded at extraction
time via `--exclude-sessions`, tails also deduplicated against batch 1/2 gold, the hf/hf2
pools and `data/batch3/pool_dev.jsonl`).

## Test-set checks

- No dataset from an owner in `data/batch3/excluded_owners.json` was downloaded or read.
- Every candidate's session id and every raw file was checked against
  `data/batch3/test_sessions.txt` (`data/hf3a/testcheck.py`, ids of length >= 12 containing a
  digit): 0 hits in all 26 datasets. The final output was re-checked (session/id tokens and
  full text): 0 hits.
- Skipped as mirrors/compilations of other uploads: dataclaw forks and re-uploads
  (ArkhAngelLifeJiggy, peteromallet forks, TeichAI Claude-Opus-Dataclaw-Unredacted), a
  Complete-FABLE mirror, Nexlab, mondk. Skipped for other reasons: rbinrs (leaked source
  code), clem/davidkling hf-coding-tools variants (claimed by new-b or duplicates of a
  batch-2 dataset), MRiabov and RangaPrasath (codex/gemini, new-b's scope), GTML-LAB (not traces).

## Selection

- Survey, file trees, peeks and format classification: `data/hf3a/survey.py`, `trees.py`,
  `peek.py`, `classify.py` (license rule of batch 1: MIT, Apache-2.0, CC-BY-4.0,
  BSD-3-Clause, CC0-1.0). All 26 datasets are claimed in `gold/batch3/CLAIMS.md`.
- Download and extraction use a copy of the batch-2 extractor,
  `scripts/batch3_new-a_hf_extract.py`, which adds (a) a Range download of the first
  `max_bytes` of an oversized `.jsonl` file (trimmed to the last full line, recorded as
  `partial` in `data/hf3a/manifest.json`) and (b) a parser for claudeset-style `turns`
  exports. At most 3 turns per session.

  ```sh
  uv run python scripts/batch3_new-a_hf_extract.py download --root data/hf3a --datasets data/hf3a/datasets.json
  uv run python scripts/batch3_new-a_hf_extract.py extract --root data/hf3a --more-formats \
      --seen-datasets gold/handlabeled.jsonl gold/batch2/handlabeled.jsonl \
      --exclude-sessions gold/handlabeled.jsonl gold/batch2/handlabeled.jsonl
  ```

  Result: 199,659 candidates.
- Queue and plans (`data/hf3a/queue.jsonl`, keys `a0000`-`a2015`):
  - `make_queue.py`: round-robin queue a0000-a1460 with lanes b (boundary patterns),
    q ('?' at the end), c ('?' in code) and n (no '?'); labeled a0000-a0519 in order.
  - `plan2.py`: the round-robin queue gave too many negatives, so the rest of the queue was
    filtered to items whose tail ends in a likely addressed question, plus a few code-'?' and
    plain negatives per dataset, and 436 new likely-question items were appended
    (a1461-a1896); order in `plan2.txt` (850 items, all labeled).
  - `plan3.py`: 119 items (a1897-a2015) topping up the small agentic/coding datasets, mostly
    mid-turn and code '?' (hard-negative candidates); order in `plan3.txt`, all labeled.
- Per-dataset cap about 150 (max used: 118), 3 turns per session (max used: 3).

## Scrubbing and drops

Batch 1's scrubbing (secret patterns, home paths, IPs, phone numbers, emails) is applied by
the extractor. After labeling, the output was scanned again for hex keys, `sk-`, `sk1_/pk1_`,
GitHub/Slack/Google/AWS tokens, JWTs, PEM keys, emails, IPs, phones, home paths and
password/secret/token assignments. Dropped (not annotated): a0458 (credentials), a1131 and
a1458 (API keys; removed from the plan), a1459 (a registrar secret key), a0680 (a real
docker-compose service password). a0134's `PASS=ton_password` is a placeholder and was kept.

## Datasets

Licenses of the 26 datasets: see the table (items: 853 Apache-2.0, 489 MIT, 145 CC-BY-4.0).
Downloaded bytes are for the pinned revision; "range-fetched prefix" means only the first part
of an oversized file was used.

| dataset | license | pinned revision | downloaded | agents | items | with Q | neg (hard) |
|---|---|---|---|---|---:|---:|---:|
| `TeichAI/Claude-Sonnet-4.6-Reasoning-1100x` | apache-2.0 | `eeae70a977547fa98f49954be71ec0026dde08ee` | 4.5 MB | claude-chat 118 | 118 | 110 | 8 (2) |
| `TeichAI/lordx64-claude-opus-4.7-max-cleaned` | apache-2.0 | `adc58234989e8b837d4d4bb2313d99f0abf89d9c` | 35.1 MB | claude-chat 110 | 110 | 83 | 27 (23) |
| `kth8/multi-turn-conversation-50000x` | apache-2.0 | `87edea1c74729570d832aea19967c48b21db4a38` | 40.0 MB (range-fetched prefix) | chat-assistant 107 | 107 | 100 | 7 (1) |
| `anthracite-org/kalo-opus-instruct-22k-no-refusal` | apache-2.0 | `18556bcc00e1fd180349e6f3faf9062b93bbd70f` | 78.9 MB | claude-chat 105 | 105 | 79 | 26 (22) |
| `Gryphe/Opus-4.6-Reasoning-24k` | apache-2.0 | `b9fb504373024921a3114619aed72eb4ed7d922b` | 140.1 MB (range-fetched prefix) | claude-chat 95 | 95 | 66 | 29 (25) |
| `Roman1111111/claude-sonnet-4.6-100000X-filtered` | mit | `424495a8cf73d46f8c6039dd288e6e97f9dce1da` | 60.0 MB (range-fetched prefix) | claude-chat 95 | 95 | 60 | 35 (31) |
| `NoSlop4U/sonnet-3.7-1000x` | cc-by-4.0 | `759727f787efaf59da29aeea11468380e877b8b5` | 4.6 MB | claude-chat 93 | 93 | 82 | 11 (4) |
| `lelouch0110/claudeset-community` | mit | `fe11da9ac006d5592378a3d284ee2ed81ffb7578` | 14.4 MB | claude-code 92 | 92 | 71 | 21 (2) |
| `woctordho/dataclaw` | mit | `f097b4788f08422922c16826c29a1fc5758bb20d` | 147.9 MB (range-fetched prefix) | gemini-cli 44, opencode 19, claude-code 14, codex 10 | 87 | 55 | 32 (16) |
| `Roman1111111/claude-opus-4.6-10000x` | mit | `d6fe6aafcf5db8141153a0828c791eeee512b171` | 13.4 MB | claude-chat 75 | 75 | 46 | 29 (21) |
| `WithinUsAI/microsoft_copilot_distilled_25k` | mit | `e9235dbe024347ca0e3fed7cbededc59b8ac4cd0` | 36.6 MB | copilot-chat 67 | 67 | 63 | 4 (0) |
| `AronDaron/Refactor-Dialogue-1.4k-Multi-turn-Refactoring-Conversations` | apache-2.0 | `e7074293f846cc6949359247ef0685960fffdf9f` | 12.6 MB | coding-assistant 58 | 58 | 13 | 45 (39) |
| `di-zhang-fdu/Fable-sharegpt` | apache-2.0 | `2c16c6c1d755796c4c16f57390c9ddc72694ef9e` | 148.5 MB (range-fetched prefix) | coding-assistant 57 | 57 | 23 | 34 (27) |
| `Crownelius/Agentic-SFT-1000x` | apache-2.0 | `1187a912ecae9cb3f0c80863019dcc30cd40085a` | 59.9 MB (range-fetched prefix) | coding-assistant 49 | 49 | 10 | 39 (33) |
| `dalisoft/claude-opus-4.6-high-reasoning-700x` | apache-2.0 | `59dfd255963e8a3159ba91ac8b4708d5b04e6ab3` | 21.7 MB | claude-chat 39 | 39 | 0 | 39 (29) |
| `TeichAI/Fable-5-Cursor-Traces` | apache-2.0 | `ef02bb803c55d53f47e2ede862b315c3e89459e3` | 57.9 MB | cursor 29 | 29 | 1 | 28 (2) |
| `TeichAI/Hunter-Alpha-UIGEN-T3-Agent-SFT` | mit | `985a95a206e9996754083a41731beb804727845c` | 39.8 MB (range-fetched prefix) | coding-assistant 26 | 26 | 3 | 23 (9) |
| `CodeFlame/FIXED-Cleaned-Claude-Sonnet-5-Grok-4.5-ChatGPT-5.6-Luna-Qwen-3.8-MAX` | mit | `c8bf4335f802467c8265ba15bd91d79f503b00a4` | 1.5 MB | claude-chat 26 | 26 | 0 | 26 (17) |
| `mencosk/gomodel-go-expert-v4` | apache-2.0 | `d4ba7867cce29d264193fa6d1df61d6966916554` | 45.9 MB | coding-assistant 25 | 25 | 4 | 21 (11) |
| `NoSlop4U/opus-3-1000x` | cc-by-4.0 | `c4f4b4a791de5c5d13e037a97671d24c659ce781` | 2.6 MB | claude-chat 25 | 25 | 4 | 21 (10) |
| `greghavens/glm-5.2-coding-and-debugging-traces` | cc-by-4.0 | `f115b6689332e3bb2d22c6a42bd22a3ebb95625b` | 35.3 MB | coding-assistant 24 | 24 | 0 | 24 (8) |
| `11-47/Fable-5.1-Max-Reasoning-5K` | apache-2.0 | `c98bf169630dd49d663d8b2001f28d8737b616be` | 40.0 MB (range-fetched prefix) | coding-assistant 21 | 21 | 0 | 21 (3) |
| `OpenCoven/fable-forge-10k` | mit | `334f3b5e13b9cec4b319b75be9a1fb25090c029a` | 18.9 MB | claude-chat 20 | 20 | 0 | 20 (0) |
| `kdrapel/csharp-dotnet-reviewing-reasoning-traces` | apache-2.0 | `42719518ffd3de8023ba251c3317b216d17a5192` | 4.1 MB | coding-assistant 20 | 20 | 0 | 20 (8) |
| `el4/Xenon-Mixed-Agentic-Dataset-v2` | apache-2.0 | `b5dbb957bc236f861f1e4f84a04961ca324de18f` | 40.0 MB (range-fetched prefix) | coding-assistant 20 | 20 | 0 | 20 (5) |
| `victor/claude-worldcup-2026-wallchart-traces` | cc-by-4.0 | `c2c03b28a499f4244e912b55d983870cf527055d` | 0.3 MB | claude-code 3 | 3 | 1 | 2 (0) |

`woctordho/dataclaw` is a mixed export (claude-code, gemini-cli, codex, opencode sessions);
it was claimed by new-a as a whole, so its 73 non-Claude turns are included here.

## Rebuild

```sh
uv run python scripts/build_gold.py --queue data/hf3a/queue.jsonl \
    --ann gold/batch3/new-a/annotations.txt --out gold/batch3/new-a/handlabeled.jsonl
uv run python scripts/validate_gold.py gold/batch3/new-a/handlabeled.jsonl --quiet
```
