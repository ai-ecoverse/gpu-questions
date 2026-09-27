# Hand-labeled test set, batch 2: sources

`gold/batch2/handlabeled.jsonl` holds 1,995 end-of-turn assistant messages: 1,253 with a
question and 742 without (333 of those hard negatives). They come from 66 public Hugging Face
agent-trace datasets, none of which appear in batch 1 (`gold/split.json`,
`gold/handlabeled.jsonl`), so no record carries `seen_dataset`. No session from batch 1 was
reused: batch-1 session ids were excluded at extraction time and re-checked on the output
(0 overlaps).

## Selection

- Surveyed 16,999 Hugging Face datasets through the API (`format:agent-traces` filter plus
  ~60 search terms for agent names and trace/session wording; `data/hf2/survey.py`).
- Kept batch 1's license rule (MIT, Apache-2.0, CC-BY-4.0, BSD-3-Clause, CC0-1.0) and
  size caps. 2,400 license-eligible datasets had their file trees fetched and classified by
  session format (`data/hf2/trees.py`, `byclass.json`). 67 were downloaded, all at a pinned
  revision: 1.87 GB total, largest 149.9 MB (caps: 150 MB per dataset, 2.5 GB total).
  Licenses of the 66 used datasets: 38 MIT, 18 Apache-2.0, 10 CC-BY-4.0.
  `cfahlgren1/gemma-vs-qwen-traces-6ee227` was downloaded but produced no candidates.
- Downloads were verified against the pinned tree (`data/hf2/verify.py`); 40 silently
  truncated files were re-fetched before extraction.
- Extraction reuses `scripts/hf_extract.py` with new optional flags (defaults unchanged):

  ```sh
  uv run python scripts/hf_extract.py download --root data/hf2 --datasets data/hf2/datasets.json
  uv run python scripts/hf_extract.py extract --root data/hf2 --more-formats \
      --exclude-sessions data/hf/queue.jsonl data/hf/candidates.jsonl gold/handlabeled.jsonl
  ```

  `--more-formats` adds parsers for message-list exports (dataclaw /
  `my-personal-*-data`, hermes, tau2, `type=message` wrappers), opencode, goose,
  opentraces and openclaw sessions. At most 3 turns per session, as in batch 1.
  Result: 19,911 candidates.
- Scrubbing is batch 1's: secret patterns from `scripts/extract.py`, plus home paths, IPs
  and phone numbers; doubtful items are dropped. After labeling, the output was scanned
  again for key/token/JWT/PEM/email/IP/home-path/phone patterns. The only hits were a false
  positive (`sk-` inside a flag id) and a GitHub username that the opentraces traces
  discuss as a leak; it is masked as `[USER]` in the two records that kept it.
- `data/hf2/make_queue.py` built the 2,763-item queue (`b0000`–`b2762`): dedup on the last
  300 characters and on a normalized last-200 tail, against batch 1 and within batch 2; a
  session used in one dataset is not reused from another; round-robin over datasets with
  about four `?` items per non-`?` item. Per-dataset lanes: 120 with `?` + 35 without by
  default; smaller lanes for template-heavy sources (the eight `dacorvo/*` scripted-scenario
  datasets 55/12, the two tau2 simulators 45/5, `AI45Research/ATBench-Claw` 17/12,
  `BeheraBoi/yasha-v200-traces` 0/20, `jedisct1/security-audits` 8/15,
  `Jadson/ox-alpha-pi-traces-emacs-bridge` 14/20, `andthattoo/etpi-pi-traces` 29/20,
  `C10X/k3` 20/15, `dmnsh/auto-jepa-v1` 0/15).
- Labeling order: `b0000`–`b1399` sequentially (each `dacorvo/*` dataset stopped at 40
  labeled turns), then `data/hf2/plan_tail.txt` for `b1400`–`b2762`: every `?` item plus
  every fifth non-`?` item, to keep the with-question share near 60%. No dataset exceeds
  150 labeled turns (largest: 131).
- Not labeled (768 of 2,763): 572 non-`?` tail items not drawn by the 1-in-5 sample, 190
  `dacorvo/*` items past the 40-per-dataset cap, and 6 individual items: `b0179` and
  `b1971` (tail starts mid-question), `b1446` (demo credentials in the text), `b1811` and
  `b1879` (a leaked username is the subject), `b2011` (a drafted support request quoting
  an OAuth client id).

## Labeling

Every item was read and labeled by hand (by an AI agent) in `gold/batch2/annotations.txt`,
following `gold/CONVENTIONS.md` (unchanged during the work). No model output was consulted.
`scripts/build_gold.py --queue data/hf2/queue.jsonl --ann gold/batch2/annotations.txt
--out gold/batch2/handlabeled.jsonl` resolves the spans (0 errors) and
`scripts/validate_gold.py gold/batch2/handlabeled.jsonl` reports 0 errors; its 491
compiler differences (mostly `propose`) are expected-vs-compiler disagreements, not span
errors. Progress per round is in [`PROGRESS.md`](PROGRESS.md).

| | Count |
|---|---:|
| items | 1,995 |
| with a question | 1,253 (62.8%) |
| negatives | 742 |
| hard negatives (note starts `hard:`) | 333 |
| ambiguous (`amb`) | 70 |
| questions | 1,530 |
| yes_no / either_or / open / multi_choice | 707 / 358 / 337 / 128 |
| propose | 757 |
| multiSelect | 6 |
| default set | 27 |
| difficulty easy / medium / hard | 1,502 / 410 / 83 |

Agents: claude-code 1,111, pi 262, opencode 160, hermes 112, tau2 97, codex 79,
openclaw 51, gemini-cli 51, goose 43, swival 26, nvim-ask 3. Formats (datasets): message-list
29, pi 13, claude 12, opencode 4, hermes 3, opentraces 3, goose 2, codex 2, openclaw 1.

Decisions made where the conventions were silent or unclear (items with such a decision
carry a note):

- **Restated questions.** A question restated after its option list ("Which would you
  like?" after "Should I: 1… 2…") is one record; consecutive or differently worded
  questions are separate records.
- **propose.** "Should I X or Y?" and "Want to X…" / "Would you like to X…" without "me"
  are `propose=false`; "Want me to X or Y", "Do you want A, or should I B", "Ready to
  implement or …?", "May I read …?" and "Shall I …?" are `propose=true`.
- **Requests phrased as questions.** "Could you double-check / try again …?" is yes_no (as
  in the "Can you try running…" convention); "Could you share / tell me …?" asking for
  content is open.
- **Spec-review "open questions".** When the reply says it wrote open questions into a
  spec file and only summarizes them, the item is a hard negative (`amb`). When the list is
  addressed to the user ("Open Questions for You", "for your input"), each item is labeled;
  review-finding musings in the same message are not.
- **"What's your instinct / thoughts on these options?"** right after an options list is
  multi_choice over those options (with `default` when a lean is stated), marked `amb`.
- **Menus before "What would you like to do/focus on?"** (numbered capability lists) supply
  options; "such as" / "e.g." / "like" lists stay examples. "For example:" lists of
  diagnostic sub-questions supply options and are marked `amb`.
- **Dash lists after an offer** ("— a simpler version, a different language, or …")
  supply options.
- **Escape arms** such as "or is there anything else", "or something else", "or would you
  rather I go a different direction" are not options; with a single named alternative the
  question becomes yes_no.
- **Consultation prompts.** Messages that read like a question drafted for another reviewer
  ("Which test is more appropriate…") are labeled as questions but marked `amb`.
- **Hard negatives** include `?` in Windows `\\?\` paths, URLs, globs, regexes, ternaries,
  optional chaining and optional parameters; rhetorical headings and table headers;
  compaction summaries quoting the user; leaked reasoning and self-directed questions;
  questions drafted for a third party; offers without a question mark.
- **Non-English text** follows the same rules; the full-width `？` counts as a question
  mark.

## Datasets

| Dataset | License | Revision | Agent | Format | Positives | Negatives |
|---|---|---|---|---|---:|---:|
| [`peteromallet/dataclaw-peteromallet`](https://huggingface.co/datasets/peteromallet/dataclaw-peteromallet) | mit | `b925056b0539` | claude-code | msglist | 101 | 30 |
| [`tillg/dataclaw-tillg`](https://huggingface.co/datasets/tillg/dataclaw-tillg) | mit | `a89cd3eae680` | claude-code | msglist | 107 | 23 |
| [`choucsan/mimo-claude-code-traces-1k`](https://huggingface.co/datasets/choucsan/mimo-claude-code-traces-1k) | mit | `39cc3fc3ed60` | claude-code | claude | 92 | 18 |
| [`gutenbergpbc/john-masterclass-cc`](https://huggingface.co/datasets/gutenbergpbc/john-masterclass-cc) | mit | `9fe66122e3ca` | claude-code | msglist | 92 | 17 |
| [`peteromallet/my-dataclaw-data`](https://huggingface.co/datasets/peteromallet/my-dataclaw-data) | mit | `37a53ac4d696` | claude-code | msglist | 74 | 28 |
| [`OpenTraces/opentraces-devtime`](https://huggingface.co/datasets/OpenTraces/opentraces-devtime) | cc-by-4.0 | `22b0d09856d7` | claude-code | opentraces | 85 | 10 |
| [`davidkling/hf-coding-tools-traces-all`](https://huggingface.co/datasets/davidkling/hf-coding-tools-traces-all) | cc-by-4.0 | `86c821724655` | claude-code | claude | 79 | 13 |
| [`woctordho/dataclaw-windows`](https://huggingface.co/datasets/woctordho/dataclaw-windows) | mit | `0ffa574690ed` | gemini-cli, opencode | msglist | 39 | 46 |
| [`Jayfarei/test3`](https://huggingface.co/datasets/Jayfarei/test3) | cc-by-4.0 | `ef096d314fa0` | claude-code | opentraces | 48 | 16 |
| [`michaelwaves/my-personal-codex-data`](https://huggingface.co/datasets/michaelwaves/my-personal-codex-data) | mit | `2ac84737812d` | claude-code | msglist | 43 | 20 |
| [`Ev3lynx727/skeleton`](https://huggingface.co/datasets/Ev3lynx727/skeleton) | apache-2.0 | `f12a5065f3f5` | hermes, pi | hermes, msglist | 1 | 49 |
| [`while-ai/tau2-simulated`](https://huggingface.co/datasets/while-ai/tau2-simulated) | apache-2.0 | `00b7ae79eb3a` | tau2 | msglist | 45 | 5 |
| [`KermitCO/qwen3.5-9B-tau2bench-retail-baseline-traces`](https://huggingface.co/datasets/KermitCO/qwen3.5-9B-tau2bench-retail-baseline-traces) | mit | `35004f5b13db` | tau2 | msglist | 47 | 0 |
| [`wop/my-personal-codex-data`](https://huggingface.co/datasets/wop/my-personal-codex-data) | mit | `22e9073bd799` | claude-code, codex, opencode | msglist | 28 | 16 |
| [`dacorvo/hf-hub-session-goose-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-goose-traces) | apache-2.0 | `6be63cf51c1c` | goose | goose | 32 | 8 |
| [`dacorvo/hf-hub-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-hermes-traces) | apache-2.0 | `24348966ce9a` | hermes | hermes | 30 | 10 |
| [`dacorvo/hf-hub-session-opencode-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-opencode-traces) | apache-2.0 | `228a481c53d7` | opencode | opencode | 16 | 24 |
| [`dacorvo/hf-hub-session-pi-traces`](https://huggingface.co/datasets/dacorvo/hf-hub-session-pi-traces) | apache-2.0 | `54094d0a27d3` | pi | pi | 26 | 14 |
| [`dacorvo/transformers-coding-session-hermes-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-hermes-traces) | apache-2.0 | `72b27b7ba76c` | hermes | hermes | 35 | 5 |
| [`dacorvo/transformers-coding-session-opencode-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-opencode-traces) | apache-2.0 | `ac0f520927b1` | opencode | opencode | 22 | 18 |
| [`dacorvo/transformers-coding-session-pi-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-pi-traces) | apache-2.0 | `4a37658db704` | pi | pi | 27 | 13 |
| [`trace-commons/agent-traces`](https://huggingface.co/datasets/trace-commons/agent-traces) | cc-by-4.0 | `112ebd4d03ce` | claude-code | claude | 20 | 18 |
| [`andthattoo/etpi-pi-traces`](https://huggingface.co/datasets/andthattoo/etpi-pi-traces) | apache-2.0 | `63e5db6022ce` | pi | pi | 6 | 31 |
| [`moikapy/0xKobolds`](https://huggingface.co/datasets/moikapy/0xKobolds) | mit | `50d5828c6275` | pi | pi | 29 | 7 |
| [`REXX-NEW/my-personal-codex-data`](https://huggingface.co/datasets/REXX-NEW/my-personal-codex-data) | mit | `dda6aeef0fe2` | codex | msglist | 8 | 26 |
| [`A99311/my-dataclaw-data`](https://huggingface.co/datasets/A99311/my-dataclaw-data) | mit | `333b663a8718` | claude-code | msglist | 17 | 14 |
| [`akenove/my-personal-codex-data`](https://huggingface.co/datasets/akenove/my-personal-codex-data) | mit | `dd4600847b9c` | openclaw | msglist | 14 | 14 |
| [`peteromallet/my-personal-codex-data`](https://huggingface.co/datasets/peteromallet/my-personal-codex-data) | mit | `8c9543389161` | codex | msglist | 7 | 21 |
| [`AI45Research/ATBench-Claw`](https://huggingface.co/datasets/AI45Research/ATBench-Claw) | apache-2.0 | `75f70f4bfd83` | openclaw | claw | 17 | 6 |
| [`C10X/k3`](https://huggingface.co/datasets/C10X/k3) | cc-by-4.0 | `885d18e0e3ae` | pi | pi | 0 | 23 |
| [`Jadson/ox-alpha-pi-traces-emacs-bridge`](https://huggingface.co/datasets/Jadson/ox-alpha-pi-traces-emacs-bridge) | mit | `27ea6dfe7a6c` | pi | pi | 0 | 23 |
| [`open-index/tomo-traces`](https://huggingface.co/datasets/open-index/tomo-traces) | apache-2.0 | `682082c82f69` | pi | pi | 4 | 15 |
| [`vaynelee/dataclaw-vaynelee`](https://huggingface.co/datasets/vaynelee/dataclaw-vaynelee) | mit | `b92d400210a6` | claude-code | msglist | 2 | 14 |
| [`crispwisp/wisp-claude-code-sessions`](https://huggingface.co/datasets/crispwisp/wisp-claude-code-sessions) | mit | `c2c90b591743` | claude-code | claude | 4 | 11 |
| [`jedisct1/security-audits`](https://huggingface.co/datasets/jedisct1/security-audits) | mit | `6d527ff0081e` | swival | claude | 0 | 14 |
| [`Batman787/dataclaw-Batman787`](https://huggingface.co/datasets/Batman787/dataclaw-Batman787) | mit | `fd6ee0f00777` | claude-code | msglist | 5 | 7 |
| [`jedisct1/agent-traces-flashmania`](https://huggingface.co/datasets/jedisct1/agent-traces-flashmania) | mit | `978b00094cc3` | swival | claude | 1 | 11 |
| [`nixjoe/vue2egg-260310`](https://huggingface.co/datasets/nixjoe/vue2egg-260310) | mit | `1268b6618d57` | claude-code | msglist | 1 | 9 |
| [`sunsun123new/dataclaw-sunsun123new`](https://huggingface.co/datasets/sunsun123new/dataclaw-sunsun123new) | mit | `f93f5476b723` | claude-code | msglist | 5 | 5 |
| [`parani01/dataclaw-parani01`](https://huggingface.co/datasets/parani01/dataclaw-parani01) | mit | `98a7d6ffad5b` | claude-code | msglist | 4 | 5 |
| [`dmnsh/auto-jepa-v1`](https://huggingface.co/datasets/dmnsh/auto-jepa-v1) | mit | `9d7df78ffc97` | opencode | opencode | 0 | 8 |
| [`nixjoe/nes-cpu`](https://huggingface.co/datasets/nixjoe/nes-cpu) | mit | `f500a7789f7b` | claude-code | msglist | 3 | 5 |
| [`xuechengjiang/my-personal-codex-data`](https://huggingface.co/datasets/xuechengjiang/my-personal-codex-data) | mit | `44e33a9ba9f2` | claude-code | msglist | 5 | 3 |
| [`BeheraBoi/yasha-v200-traces`](https://huggingface.co/datasets/BeheraBoi/yasha-v200-traces) | mit | `f2d0b40c14b2` | claude-code | claude | 0 | 7 |
| [`lemonteaa/coding-trajectory`](https://huggingface.co/datasets/lemonteaa/coding-trajectory) | mit | `5bc2468cf409` | pi | pi | 0 | 7 |
| [`merve/hf-find-traces`](https://huggingface.co/datasets/merve/hf-find-traces) | apache-2.0 | `650d439f6d90` | pi | pi | 6 | 1 |
| [`nixjoe/new-cpu-260310`](https://huggingface.co/datasets/nixjoe/new-cpu-260310) | mit | `1138b0882be9` | claude-code | msglist | 5 | 2 |
| [`DJTRIXUK/dataclaw-DJTRIXUK`](https://huggingface.co/datasets/DJTRIXUK/dataclaw-DJTRIXUK) | mit | `821048832837` | claude-code | msglist | 5 | 1 |
| [`dacorvo/funes-recall-session-opencode-traces`](https://huggingface.co/datasets/dacorvo/funes-recall-session-opencode-traces) | apache-2.0 | `bedb923bc2b6` | opencode | opencode | 0 | 6 |
| [`wuuski/my-personal-codex-data`](https://huggingface.co/datasets/wuuski/my-personal-codex-data) | mit | `50d0d82b7867` | claude-code, codex | msglist | 2 | 4 |
| [`build-small-hackathon/agent-trace-privacy-scrubber-codex-traces`](https://huggingface.co/datasets/build-small-hackathon/agent-trace-privacy-scrubber-codex-traces) | mit | `6e6993512af3` | codex | codex | 0 | 5 |
| [`dacorvo/funes-recall-session-pi-traces`](https://huggingface.co/datasets/dacorvo/funes-recall-session-pi-traces) | apache-2.0 | `4e2b658ea3de` | pi | pi | 0 | 5 |
| [`davanstrien/agent-race-traces`](https://huggingface.co/datasets/davanstrien/agent-race-traces) | cc-by-4.0 | `4a8ac15d62c3` | claude-code, pi | claude, pi | 0 | 5 |
| [`licongxu/fable5-flamingo-research-trace`](https://huggingface.co/datasets/licongxu/fable5-flamingo-research-trace) | cc-by-4.0 | `995976038719` | claude-code | claude | 0 | 5 |
| [`sinhaankur/my-personal-codex-data`](https://huggingface.co/datasets/sinhaankur/my-personal-codex-data) | mit | `50fbf2bd5ac0` | claude-code | msglist | 4 | 1 |
| [`beyarkay/slash-bad`](https://huggingface.co/datasets/beyarkay/slash-bad) | cc-by-4.0 | `3d9a931379a3` | claude-code | claude | 0 | 4 |
| [`GolienHzmsr/dataclaw-GolienHzmsr`](https://huggingface.co/datasets/GolienHzmsr/dataclaw-GolienHzmsr) | mit | `1c2289df58a5` | claude-code | msglist | 3 | 0 |
| [`dacorvo/transformers-coding-session-goose-traces`](https://huggingface.co/datasets/dacorvo/transformers-coding-session-goose-traces) | apache-2.0 | `742f2c040663` | goose | goose | 2 | 1 |
| [`g0t4/ask_traces`](https://huggingface.co/datasets/g0t4/ask_traces) | mit | `8ebe0c7afbe9` | nvim-ask | pi | 0 | 3 |
| [`julien-c/opentraces`](https://huggingface.co/datasets/julien-c/opentraces) | cc-by-4.0 | `444025c5326b` | claude-code | opentraces | 0 | 3 |
| [`masterda/my-personal-codex-data`](https://huggingface.co/datasets/masterda/my-personal-codex-data) | mit | `9a2d1c5b2596` | claude-code | msglist | 1 | 2 |
| [`merve/agent_traces`](https://huggingface.co/datasets/merve/agent_traces) | apache-2.0 | `2e1b3fcebf28` | pi | pi | 2 | 1 |
| [`merve/gemma-vs-qwen-traces`](https://huggingface.co/datasets/merve/gemma-vs-qwen-traces) | apache-2.0 | `410476d775af` | hermes | msglist | 1 | 2 |
| [`cfahlgren1/web-fetch-harness-traces`](https://huggingface.co/datasets/cfahlgren1/web-fetch-harness-traces) | mit | `b05bc8a5c858` | claude-code, codex | claude, codex | 0 | 2 |
| [`victor/3d-world-session`](https://huggingface.co/datasets/victor/3d-world-session) | mit | `3f4e6f899bdd` | claude-code | claude | 0 | 2 |
| [`samzong/recall-sessions`](https://huggingface.co/datasets/samzong/recall-sessions) | cc-by-4.0 | `f08e85a6ad9d` | claude-code | msglist | 1 | 0 |


Full revisions are in each record's `revision` field and in `data/hf2/manifest.json`
(git-ignored). CC-BY-4.0 datasets require attribution; this table and each record's
`dataset`, `revision` and `session` fields provide it.

## Rebuilding

```sh
uv run python scripts/build_gold.py --queue data/hf2/queue.jsonl \
    --ann gold/batch2/annotations.txt --out gold/batch2/handlabeled.jsonl
uv run python scripts/validate_gold.py gold/batch2/handlabeled.jsonl --quiet
uv run python scripts/gold_stats.py gold/batch2/handlabeled.jsonl
```

`data/hf2/` (downloads, candidates, queue, helper scripts) is git-ignored.
