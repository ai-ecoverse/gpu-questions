# Hand-labeled test set, batch 3 "dev": sources

`gold/batch3/dev/handlabeled.jsonl` holds 1,197 end-of-turn assistant messages: 683 with a
question (57.1%) and 514 without (373 of them hard negatives). They come from 70 public
Hugging Face agent-trace datasets (41 owners) that batches 1 and 2 already used, so every
record carries `seen_dataset: true`. No new data was downloaded.

## Selection

- Source pool: `data/batch3/pool_dev.jsonl` (13,199 unlabeled, already scrubbed turns from the
  batch-1/2 development datasets; test-set owners in `data/batch3/excluded_owners.json` and
  already-labeled turns removed upstream). No dataset from an excluded owner appears in the
  output (checked).
- `data/batch3/dev/make_queue.py` built the first 1,320 queue items (`d0000`–`d1319`): dedup on a
  normalized last-200 tail (also against batches 1–2), at most 3 turns per session counting
  earlier labels (checked on the output: max 3), per-dataset lanes of `?` and non-`?` items
  (boundary items first in the `?` lane, up to 60% of it), round-robin over datasets.
  `while-ai/tau2-simulated` was capped at 100 labeled turns; no dataset exceeds 150 (largest:
  `peteromallet/dataclaw-peteromallet`, 138).
- Labeling order: `d0000`–`d0261` sequentially; then `plan_tail.txt` (every `?` item plus 1 in 4
  non-`?` items). Because the pool's questions sit in a few owners, the head of the round-robin
  was negative-heavy, so before round 3 the remaining plan was revised (`plan_tail2.txt`): 35
  `Samarth0710/traceweave` and `Jadson/ox-alpha-pi-traces-emacs-bridge` `?` items (almost all
  quoted-`?` negatives, listed in `plan_skipped.txt`) were skipped unlabeled, and
  `data/batch3/dev/extend_queue.py` appended 202 more `?` items from question-rich datasets
  (`d1320`–`d1521`: peteromallet +25, tau2 +11, dacorvo/* up to +25 each) under the same dedup
  and session rules.
- 1,268 items were labeled. To keep the with-question share near 60%, 71 easy (non-hard)
  negatives were then moved to `annotations_reserve.txt` (drawn from datasets with several easy
  negatives, keeping at least two items per dataset); they remain buildable with
  `--ann gold/batch3/dev/annotations_reserve.txt`.
- Not labeled: the non-`?` tail items outside the 1-in-4 sample, the 35 skipped items above,
  `d0600` (tail starts mid-question, as batch-2 b0179), and two privacy drops (below).
- Boundary coverage: 357 of 811 questions (44%) contain "or" (or 或/还是) or take their options from
  a nearby list or list lead-in (`data/batch3/dev/progress_stats.py`).

## Scrubbing and privacy

The pool was already scrubbed (batch-1 secret patterns plus home paths, IPs, phone numbers).
Before building, the output was scanned again for key/token/JWT/PEM/email/IP/home-path/phone and
password patterns. Hits were only `127.0.0.1`/`0.0.0.0`, numbers that look like phone numbers
(timestamps, floats) and `@` in code decorators. Six email addresses written without a dot
(`…@gmailcom`) in three tau2 records slipped past the pool's email pattern; they are masked as
`[REDACTED]` in the queue text. Dropped: `d0064` (lists hardcoded demo usernames and passwords)
and `d0356` (quotes a database password).

## Labeling

Every item was read and labeled by hand (by an AI agent) in `gold/batch3/dev/annotations.txt`,
following `gold/CONVENTIONS.md` and the batch-2 decisions in `gold/batch2/SOURCES.md`. No model
output was consulted. `scripts/build_gold.py` resolves all spans (0 errors) and
`scripts/validate_gold.py` reports 0 errors; its 215 compiler differences are
expected-vs-compiler disagreements, not span errors. Progress per round is in
[`PROGRESS.md`](PROGRESS.md); cases where the conventions were unclear are appended to
`gold/batch3/QUESTIONS.md` (ids d0001, d0141, d0147, d0260, d0369, d0766, d1228).

| | Count |
|---|---:|
| items | 1,197 |
| with a question | 683 (57.1%) |
| negatives | 514 |
| hard negatives (note starts `hard:`) | 373 |
| ambiguous (`amb`) | 81 |
| questions | 811 |
| yes_no / open / either_or / multi_choice | 344 / 228 / 174 / 65 |
| boundary questions | 357 |
| propose | 408 |
| multiSelect | 4 |
| default set | 5 |
| difficulty easy / medium / hard | 482 / 652 / 63 |

Agents: claude-code 278, pi 274, opencode 177, hermes 169, goose 131, tau2 100, codex 25,
copilot 23, openclaw 9, gemini-cli 4, cursor 4, vtcode 3. Formats (datasets): pi 26,
message-list 13, claude 9, codex 9, hermes 4, opencode 3, goose 2, copilot 1, cursor 1,
openclaw 1, vtcode 1. Licenses of the 70 datasets: 42 MIT, 19 Apache-2.0, 7 CC-BY-4.0,
1 BSD-3-Clause, 1 CC0-1.0. Of the 70 datasets, 37 were used in batch 1 and 33 in batch 2.

Decisions worth knowing (items carry a note):

- **Identification requests** ("your email address or your name and zip code") are open; a bare
  "Could you double-check / verify … (and try again)?" stays yes_no.
- **Scripted `dacorvo/*` sessions**: leaked user-simulator reasoning ending in a drafted request is a
  hard negative (`amb` when the drafted line is a question); a bare user-style one-liner with no
  reasoning is labeled as a question to the reader and marked `amb` (batch-2 b0120/b0321).
- **Escape arms**: open "or adjust/change anything", "or something else", "or a different approach"
  arms make the question yes_no, also when the agent offers them ("or make any adjustments");
  a second arm tied to listed items ("or clarify these points first") is a real option.
- **"Should I/should we X or Y"** is not a proposal; "Do you want me to X, or should I Y" is.
- **Menus**: "Would you like me to:" with a numbered/bulleted list is multi_choice (their `?`
  excluded from options); a later "Which would you prefer?" restatement is the same record;
  "Something else" items are escapes; "Both" stays an option (multi_choice, not multiSelect).
- **Parenthetical enumerations** after a question ("(ZeroGPU vs. Dedicated GPU vs. CPU)") supply
  options (`amb`); with "etc.", "e.g." or "such as" they illustrate.

## Datasets

| Dataset | License | Revision | Agent | Format | Positives | Negatives |
|---|---|---|---|---|---:|---:|
| [`peteromallet/dataclaw-peteromallet`](https://huggingface.co/datasets/peteromallet/dataclaw-peteromallet) | mit | `b925056b0539` | claude-code | msglist | 123 | 15 |
| [`while-ai/tau2-simulated`](https://huggingface.co/datasets/while-ai/tau2-simulated) | apache-2.0 | `00b7ae79eb3a` | tau2 | msglist | 96 | 4 |
| [`dacorvo/transformers-coding-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-hermes-traces) | apache-2.0 | `72b27b7ba76c` | hermes | hermes | 62 | 21 |
| [`dacorvo/hf-hub-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-hermes-traces) | apache-2.0 | `24348966ce9a` | hermes | hermes | 68 | 14 |
| [`dacorvo/hf-hub-session-pi-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-pi-traces) | apache-2.0 | `54094d0a27d3` | pi | pi | 49 | 33 |
| [`dacorvo/transformers-coding-session-opencode-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-opencode-traces) | apache-2.0 | `ac0f520927b1` | opencode | opencode | 41 | 39 |
| [`dacorvo/hf-hub-session-opencode-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-opencode-traces) | apache-2.0 | `228a481c53d7` | opencode | opencode | 25 | 54 |
| [`dacorvo/transformers-coding-session-pi-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-pi-traces) | apache-2.0 | `4a37658db704` | pi | pi | 43 | 33 |
| [`dacorvo/transformers-coding-session-goose-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-goose-traces) | apache-2.0 | `742f2c040663` | goose | goose | 62 | 8 |
| [`dacorvo/hf-hub-session-goose-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-goose-traces) | apache-2.0 | `6be63cf51c1c` | goose | goose | 50 | 11 |
| [`peteromallet/my-dataclaw-data`](https://huggingface.co/datasets/peteromallet/my-dataclaw-data) | mit | `37a53ac4d696` | claude-code | msglist | 16 | 38 |
| [`Jadson/ox-alpha-pi-traces-emacs-bridge`](https://huggingface.co/datasets/Jadson/ox-alpha-pi-traces-emacs-bridge) | mit | `27ea6dfe7a6c` | pi | pi | 0 | 23 |
| [`Samarth0710/traceweave`](https://huggingface.co/datasets/Samarth0710/traceweave) | mit | `f5abd7e1c623` | copilot | copilot | 0 | 23 |
| [`C10X/k3`](https://huggingface.co/datasets/C10X/k3) | cc-by-4.0 | `885d18e0e3ae` | pi | pi | 0 | 21 |
| [`tillg/dataclaw-tillg`](https://huggingface.co/datasets/tillg/dataclaw-tillg) | mit | `a89cd3eae680` | claude-code | msglist | 15 | 5 |
| [`woctordho/dataclaw-windows`](https://huggingface.co/datasets/woctordho/dataclaw-windows) | mit | `0ffa574690ed` | gemini-cli, opencode | msglist | 0 | 20 |
| [`xuechengjiang/my-personal-codex-data`](https://huggingface.co/datasets/xuechengjiang/my-personal-codex-data) | mit | `44e33a9ba9f2` | claude-code | msglist | 17 | 1 |
| [`choucsan/mimo-claude-code-traces-1k`](https://huggingface.co/datasets/choucsan/mimo-claude-code-traces-1k) | mit | `39cc3fc3ed60` | claude-code | claude | 0 | 8 |
| [`thomasmustier/pi-mono-sessions`](https://huggingface.co/datasets/thomasmustier/pi-mono-sessions) | mit | `d0895347aaac` | pi | pi | 2 | 6 |
| [`A99311/my-dataclaw-data`](https://huggingface.co/datasets/A99311/my-dataclaw-data) | mit | `333b663a8718` | claude-code | msglist | 0 | 7 |
| [`AI45Research/ATBench-Claw`](https://huggingface.co/datasets/AI45Research/ATBench-Claw) | apache-2.0 | `75f70f4bfd83` | openclaw | openclaw | 0 | 7 |
| [`peteromallet/my-personal-codex-data`](https://huggingface.co/datasets/peteromallet/my-personal-codex-data) | mit | `8c9543389161` | codex | msglist | 0 | 7 |
| [`nixjoe/new-cpu-260310`](https://huggingface.co/datasets/nixjoe/new-cpu-260310) | mit | `1138b0882be9` | claude-code | msglist | 3 | 3 |
| [`woxQAQ/pi-web`](https://huggingface.co/datasets/woxQAQ/pi-web) | mit | `1928c53ba9e2` | pi | pi | 4 | 2 |
| [`armand0e/claude-fable-5-claude-code`](https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code) | mit | `7388ef96f317` | claude-code | claude | 0 | 5 |
| [`open-index/tomo-traces`](https://huggingface.co/datasets/open-index/tomo-traces) | apache-2.0 | `682082c82f69` | pi | pi | 0 | 5 |
| [`thomasmustier/pi-for-excel-sessions`](https://huggingface.co/datasets/thomasmustier/pi-for-excel-sessions) | mit | `052a7c665480` | pi | pi | 0 | 5 |
| [`thomasmustier/pine-of-glass-sessions`](https://huggingface.co/datasets/thomasmustier/pine-of-glass-sessions) | mit | `b9a6b263895c` | pi | pi | 1 | 4 |
| [`AlinCiocan/fable-5-claude-code-traces`](https://huggingface.co/datasets/AlinCiocan/fable-5-claude-code-traces) | cc-by-4.0 | `e33ebbca230a` | claude-code | claude | 0 | 4 |
| [`championswimmer/pi-coding-sessions`](https://huggingface.co/datasets/championswimmer/pi-coding-sessions) | mit | `f655c6c2aabf` | pi | pi | 0 | 4 |
| [`thomasmustier/clean-slides-sessions`](https://huggingface.co/datasets/thomasmustier/clean-slides-sessions) | mit | `0ecc915c7d32` | pi | pi | 0 | 4 |
| [`thomasmustier/heypocket-reader-sessions`](https://huggingface.co/datasets/thomasmustier/heypocket-reader-sessions) | mit | `70f6d07dfb7b` | pi | pi | 0 | 4 |
| [`thomasmustier/pi-extensions-sessions`](https://huggingface.co/datasets/thomasmustier/pi-extensions-sessions) | mit | `17e22c5903cb` | pi | pi | 0 | 4 |
| [`thomasmustier/pi-nes-sessions`](https://huggingface.co/datasets/thomasmustier/pi-nes-sessions) | mit | `47d55a2545e0` | pi | pi | 0 | 4 |
| [`vedalken/merchantscroll-traces`](https://huggingface.co/datasets/vedalken/merchantscroll-traces) | mit | `495c3ee7ba3e` | cursor | cursor | 1 | 3 |
| [`build-small-hackathon/kirana-detective-build-traces`](https://huggingface.co/datasets/build-small-hackathon/kirana-detective-build-traces) | mit | `d61ca08eac92` | claude-code | claude | 1 | 2 |
| [`drdavidtang/build-small-agent-trace`](https://huggingface.co/datasets/drdavidtang/build-small-agent-trace) | mit | `af8e727914b9` | codex | codex | 0 | 3 |
| [`julien-c/pi-sessions`](https://huggingface.co/datasets/julien-c/pi-sessions) | cc-by-4.0 | `700416886204` | pi | pi | 1 | 2 |
| [`kingkw1/read-along-ai-agent-traces`](https://huggingface.co/datasets/kingkw1/read-along-ai-agent-traces) | mit | `0bee208f7b13` | codex | codex | 0 | 3 |
| [`nixjoe/nes-cpu`](https://huggingface.co/datasets/nixjoe/nes-cpu) | mit | `f500a7789f7b` | claude-code | msglist | 1 | 2 |
| [`thomasmustier/economist-tui-sessions`](https://huggingface.co/datasets/thomasmustier/economist-tui-sessions) | mit | `95b6dba5c139` | pi | pi | 0 | 3 |
| [`trace-commons/agent-traces`](https://huggingface.co/datasets/trace-commons/agent-traces) | cc-by-4.0 | `112ebd4d03ce` | claude-code | claude | 1 | 2 |
| [`vinhnx90/vtcode-sessions`](https://huggingface.co/datasets/vinhnx90/vtcode-sessions) | mit | `78049282e2b4` | vtcode | vtcode | 0 | 3 |
| [`OmarRabhI/pi-sessions`](https://huggingface.co/datasets/OmarRabhI/pi-sessions) | apache-2.0 | `d3d60fea0914` | pi | pi | 1 | 1 |
| [`abidlabs/gradio-pi-sessions`](https://huggingface.co/datasets/abidlabs/gradio-pi-sessions) | mit | `7af63c1cf3cb` | pi | pi | 0 | 2 |
| [`akenove/my-personal-codex-data`](https://huggingface.co/datasets/akenove/my-personal-codex-data) | mit | `dd4600847b9c` | openclaw | msglist | 0 | 2 |
| [`andthattoo/etpi-pi-traces`](https://huggingface.co/datasets/andthattoo/etpi-pi-traces) | apache-2.0 | `63e5db6022ce` | pi | pi | 0 | 2 |
| [`build-small-hackathon/agent-trace-privacy-scrubber-codex-traces`](https://huggingface.co/datasets/build-small-hackathon/agent-trace-privacy-scrubber-codex-traces) | mit | `6e6993512af3` | codex | codex | 0 | 2 |
| [`build-small-hackathon/clue-vibes-traces`](https://huggingface.co/datasets/build-small-hackathon/clue-vibes-traces) | cc-by-4.0 | `fe8ba2792ec5` | codex | codex | 0 | 2 |
| [`build-small-hackathon/hackathon-advisor-codex-traces`](https://huggingface.co/datasets/build-small-hackathon/hackathon-advisor-codex-traces) | apache-2.0 | `c7a79f391597` | codex | codex | 0 | 2 |
| [`build-small-hackathon/pit-wall-chaos-traces`](https://huggingface.co/datasets/build-small-hackathon/pit-wall-chaos-traces) | cc-by-4.0 | `60bd7c2609d7` | codex | codex | 0 | 2 |
| [`cfahlgren1/hermes-agent-trace-samples-2026-06-05`](https://huggingface.co/datasets/cfahlgren1/hermes-agent-trace-samples-2026-06-05) | apache-2.0 | `80c32a72cc94` | hermes | hermes | 0 | 2 |
| [`crispwisp/wisp-claude-code-sessions`](https://huggingface.co/datasets/crispwisp/wisp-claude-code-sessions) | mit | `c2c90b591743` | claude-code | claude | 0 | 2 |
| [`dacorvo/funes-recall-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/funes-recall-session-hermes-traces) | apache-2.0 | `6384aea7e6d6` | hermes | hermes | 0 | 2 |
| [`dmnsh/auto-jepa-v1`](https://huggingface.co/datasets/dmnsh/auto-jepa-v1) | mit | `9d7df78ffc97` | opencode | opencode | 0 | 2 |
| [`moikapy/0xKobolds`](https://huggingface.co/datasets/moikapy/0xKobolds) | mit | `50d5828c6275` | pi | pi | 0 | 2 |
| [`naazimsnh02/tutordesk-agent-traces`](https://huggingface.co/datasets/naazimsnh02/tutordesk-agent-traces) | mit | `4d538090ddd3` | claude-code | claude | 0 | 2 |
| [`ravi2505/homeroom-copilot-open-traces`](https://huggingface.co/datasets/ravi2505/homeroom-copilot-open-traces) | mit | `3e53bfb74293` | codex | codex | 0 | 2 |
| [`rgruchalski/combust-labs_pi-mono-docker`](https://huggingface.co/datasets/rgruchalski/combust-labs_pi-mono-docker) | apache-2.0 | `7829c4a27427` | pi | pi | 0 | 2 |
| [`thomasmustier/pi-computer-use-sessions`](https://huggingface.co/datasets/thomasmustier/pi-computer-use-sessions) | mit | `8353644936ee` | pi | pi | 0 | 2 |
| [`xhochy/conda-forge-agent-traces`](https://huggingface.co/datasets/xhochy/conda-forge-agent-traces) | bsd-3-clause | `046e1aff3998` | pi | pi | 0 | 2 |
| [`yellowbeeblackbee/claude-traces`](https://huggingface.co/datasets/yellowbeeblackbee/claude-traces) | cc0-1.0 | `0cad5c49dfb8` | claude-code | claude | 0 | 2 |
| [`abidlabs/trackio-pi-sessions`](https://huggingface.co/datasets/abidlabs/trackio-pi-sessions) | mit | `4c1420de7fdd` | pi | pi | 0 | 1 |
| [`build-small-hackathon/TinyNarrator-agent-traces`](https://huggingface.co/datasets/build-small-hackathon/TinyNarrator-agent-traces) | mit | `0222953b6069` | codex | codex | 0 | 1 |
| [`build-small-hackathon/sense-garden-traces`](https://huggingface.co/datasets/build-small-hackathon/sense-garden-traces) | cc-by-4.0 | `1a13d90deb69` | codex | codex | 0 | 1 |
| [`dacorvo/funes-recall-session-pi-traces`](https://huggingface.co/datasets/dacorvo/funes-recall-session-pi-traces) | apache-2.0 | `4e2b658ea3de` | pi | pi | 0 | 1 |
| [`gabegoodhart/traces.claude-code.mlx-lm-granitemoehybrid`](https://huggingface.co/datasets/gabegoodhart/traces.claude-code.mlx-lm-granitemoehybrid) | apache-2.0 | `8717352ccbf2` | claude-code | claude | 0 | 1 |
| [`nixjoe/vue2egg-260310`](https://huggingface.co/datasets/nixjoe/vue2egg-260310) | mit | `1268b6618d57` | claude-code | msglist | 0 | 1 |
| [`parani01/dataclaw-parani01`](https://huggingface.co/datasets/parani01/dataclaw-parani01) | mit | `98a7d6ffad5b` | claude-code | msglist | 0 | 1 |
| [`thomasmustier/pi-symphony-sessions`](https://huggingface.co/datasets/thomasmustier/pi-symphony-sessions) | mit | `0697350f9654` | pi | pi | 0 | 1 |

Full revisions are in each record's `revision` field. CC-BY-4.0 datasets require attribution;
this table and each record's `dataset`, `revision` and `session` fields provide it.

## Rebuilding

```sh
uv run python scripts/build_gold.py --queue data/batch3/dev/queue.jsonl \
    --ann gold/batch3/dev/annotations.txt --out gold/batch3/dev/handlabeled.jsonl
uv run python scripts/validate_gold.py gold/batch3/dev/handlabeled.jsonl --quiet
uv run python scripts/gold_stats.py gold/batch3/dev/handlabeled.jsonl
```

`data/batch3/dev/` (queue, plans, `make_queue.py`, `extend_queue.py`, `progress_stats.py`,
viewers) is git-ignored along with the rest of `data/`.
