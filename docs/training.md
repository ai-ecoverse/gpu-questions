# Training: first results

The run was on 2026-09-23, on an Apple M4 Max using PyTorch's Metal (MPS) backend and the internal disk.

## Setup

```sh
uv sync --python 3.13                                    # .venv with torch 2.14 (about 650 MB)
uv run python scripts/extract.py --export data/export    # scrubbed gold.jsonl and eot.jsonl (git-ignored)
uv run python -m gq.train --run v2-augment               # about 8 minutes: 12 epochs of 40k fresh samples
uv run python -m gq.evaluate runs/v2-augment/best.pt     # per-set report
uv run python -m gq.evaluate --heuristic                 # regex baseline on the same sets
uv run python -m gq.predict --checkpoint runs/v2-augment/best.pt "Want me to A, or B?"
uv run pytest -q tests
```

One epoch takes about 34 seconds on MPS and about 3 seconds of data generation across 10 worker processes. MPS is about 2.7 times faster than the CPU for this model.

## What was built (`gq/`)

| File          | Role                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| `tokenize.py` | Cleans text (code blocks become `[CODE]`, URLs become `[URL]`), tokenizes, and builds sparse feature rows: kind, length, case, 2048-bucket word hash, suffix hash, lines and paragraphs from the end, and flags such as list line, list marker, in a `?` sentence, after a colon, and wh-word. There is no vocabulary. |
| `labels.py`   | Six roles: `O, Q_B, Q_I, OPT_B, OPT_I, REC`                                                           |
| `data.py`     | Session-level train/test split, weak labels from real traces, and a synthetic generator that writes gold ask-tool questions back into prose (list after, list before, inline sentence, options inside the question, several questions) on top of real agent prose as filler text. |
| `model.py`    | gpu-time-style tagger: summed embeddings, a 5-tap depthwise convolution, 2 bidirectional gated affine-scan layers (hidden size 48), global context, and a CRF. 140,944 parameters. |
| `compile.py`  | Deterministic roles → `{kind, propose, prompt, options, default, multiSelect}`                          |
| `evaluate.py` | Token F1 per role and question-level checks. The gold side runs the compiler on gold labels (an oracle), so a mismatch is always a tagging error. |

## Data

- **Gold:** 325 structured ask-tool questions, split by session into 274 train and 50 test questions that have 2 or more options.
- **End-of-turn messages:** 5,581 interactive end-of-turn messages. Messages without a question serve as filler text and negatives: 3,732 train and 937 test.
- **Weak labels:** yes/no and either/or questions from the survey heuristics, applied only when the question sentence is unambiguous. The heuristic's list-option labels were dropped because they were too noisy (reading lists and status lists are not options).

## Results (held-out sessions)

| Set                          | Metric                    | Regex heuristic | Baseline | v2 (augmented) |
| ---------------------------- | ------------------------- | --------------- | -------- | -------------- |
| synthetic/gold (1,211)       | options exactly right     | 17.7%           | 58.6%    | **81.3%**      |
|                              | kind accuracy             |                 | 82.9%    | **94.1%**      |
|                              | default (recommended) accuracy |            | 94.5%    | **98.0%**      |
|                              | question found            | 86.8%           | 100%     | 100%           |
| synthetic/multi_question (143) | options exactly right   | 0%              | 75.6%    | **87.2%**      |
|                              | question count right      |                 | 92.3%    | 93.7%          |
| synthetic/yes_no (279)       | kind accuracy             |                 | 100%     | 97.1%          |
| real/yes_no+confirm (35)     | kind accuracy             | (labels come from the heuristic) | 97.1% | 97.1% |
| real/either_or (10)          | options exactly right     | (labels come from the heuristic) | 50% | 70% |
| real and synthetic negatives (1,060) | false question rate | 0%            | 0%       | 0%             |

**v2 changes over the baseline:**
- **Option augmentation.** 55% of gold renders swap in options mixed from other questions, or random word windows cut from real agent prose.
- **Identity dropout of 0.3.** Following gpu-time's `--identity-dropout`, each token's word and suffix hashes are hidden 30% of the time during training.

The baseline memorized the 274 training questions: its training loss reached 0.0003 while held-out option accuracy stayed at about 50%. The augmentation fixed most of that gap.

## Caveats

- **The real evaluation sets are weak.** `real/*` labels come from the same regex rules, so they only measure agreement with the heuristic, and `real/either_or` has just 10 samples. There is no hand-labeled real test set yet.
- **Checkpoint selection used the test sets.** `best.pt` is picked by test metrics, which is mildly optimistic. A separate validation split is needed.
- **Synthetic gold is easier than real prose.** The templates are cleaner than how agents actually write.
- **Known error pattern:** a qualifier after a comma is split into its own option. For example, "start on that in this thread, stacked on #2794, or wait" becomes three options instead of two. The regex rules split it the same way.
- **Model size:** 141k parameters, about 4 times gpu-time's size, mostly the word-hash table. It is not quantized yet; the fp32 checkpoint is 570 KB.

## v3: training on hand-labeled real turns

`gold/handlabeled.jsonl` contains 663 public Hugging Face agent turns. An AI agent labeled them, and a person spot-checked 18 of the ambiguous items: 17 were OK and 1 was corrected. Items have a `human_review` field, and verdicts live in `gold/review.jsonl`.

`gold/split.json` splits the set **by dataset**, so no dataset or session appears on both sides:

- **Train side:** 27 datasets, 387 items. They are mixed into training (`--hand-rate 0.2`, meaning 20% of samples).
- **Test side:** 25 datasets, 276 items. They are only reported, as `hand/*`.

Checkpoint selection no longer looks at test sets: `final.pt` is the last epoch. (The earlier `best.pt` files were picked on test metrics.)

```sh
uv run python -m gq.train --run v3-hand --hand-rate 0.2
uv run python -m gq.evaluate runs/v3-hand/final.pt
```

Held-out results. The `hand/*` sets use only the 276 test items, and kind, options, and propose are scored against the hand-written expectations.

| Set (n)                 | Metric                     | v2    | **v3 (20% hand)** | v3 (40% hand) |
| ----------------------- | -------------------------- | ----- | ----------------- | ------------- |
| hand/all (276)          | question found             | 0.968 | 0.957             | 0.968         |
|                         | kind accuracy              | 0.722 | **0.747**         | 0.750         |
|                         | options exactly right      | 0.270 | **0.308**         | 0.277         |
|                         | question count right       | 0.878 | **0.916**         | 0.917         |
| hand/negative (90)      | false question rate        | 0.111 | **0.078**         | 0.089         |
| hand/open (36)          | kind accuracy              | 0.571 | **0.686**         | 0.714         |
| hand/multi (24)         | question count right       | 0.208 | **0.542**         | 0.478         |
| hand/choice (66)        | kind accuracy              | 0.619 | 0.585             | 0.600         |
| hand/yes_no (84)        | question found             | 0.976 | 0.929             | 0.952         |
| synthetic/gold (1,218)  | options exactly right      | 0.829 | 0.824             | 0.813         |

The synthetic set came out slightly different from the one in the v2 table above, because the generator's random draws changed. All three columns here use the same set.

**Takeaways**

- **Modest gains.** Real data improves false questions, open-question kind, question counts in multi-question messages, and option exactness slightly, without hurting synthetic scores.
- **Small test set.** A 4-point change in options exactness is about 3 items (roughly 65 test items have options), so treat these differences as directional.
- **More weight doesn't help.** Doubling the hand weight (40%) did not help further, which means more copies of the same 387 items is not the lever.
- **Remaining errors are structural:**
  - The compiler's `propose` and `kind` rules disagree with 79 and 27 gold items even on perfect tags (see `scripts/validate_gold.py`).
  - Choices written as "want A or B?" are still read as yes/no.
  - Option boundaries in real lists differ from the synthetic renderings.

## v4–v7: cross-validation, hard negatives, compiler rules

The targets were a false question rate below 5% and kind accuracy above 90% on real turns.

**Evaluation.** The fixed 276-item test side was too small and too different from the train side (one essay-heavy dataset, traceweave, sat almost entirely on one side). Evaluation therefore moved to 5-fold cross-validation grouped by dataset (`cv_folds` in `gold/split.json`, fold sizes 111 to 173). `gq.cv --train` fits one model per fold, 5 in parallel on MPS (about 23 minutes). Every hand-labeled turn is then scored by the model that never saw its dataset, and the metrics are pooled over all 663 turns. `gq.cv` without `--train` re-scores existing fold checkpoints, which is enough after a compiler-only change. Comma-separated runs (`--run a,b`) are scored as an ensemble. The fixed test side is now inside the folds, so it is no longer an untouched set.

**Changes**

- **Compiler** ([gq/compile.py](../gq/compile.py)):
  - Every question needs `?` or `？`. The one exception is a span ending in `:` that owns a list ("Would you like me to:"). Only 2 of 413 hand-written prompts lack a question mark, and both are that case.
  - A lone option inside "A, or B?" gets its other side recovered from the prompt.
  - "…, or something else" and "…, or do you have a preference" are escape hatches, not options, matching the hand labels.
  - One tagged span holding "`a`, `b`, `c`, or `d`" or "(1) … (2) …" is split into several options.
  - A single option is no choice, so the question becomes yes/no or open.
  - "Could you clarify/share/tell me…" without options is `open`.
  - With these rules, the compiler reaches 97.3% kind accuracy on gold spans (it was 95.9%).
- **Hard negatives** (`--hard-rate 0.12`). Before this change, the model had never seen a negative containing `?`. The new negatives include rhetorical questions the agent answers itself (sometimes as headings), quoted questions, `?` in inline code, URLs, and tables, self-review checklists, and jokes. A quarter are real local turns where every `?` is in code, quotes, a table, or mid-token. Real questions are now sometimes followed by a trailing statement, so trailing prose alone cannot veto a question.
- **More question shapes:** inline multi-choice lists ("Which package: `a`, `b`, or `c`?", "…? (a, b, c)"), clause-level pairs ("Want me to A, or would you rather B?", "I can A, or B. Which do you prefer?"), and escape hatches that must not be tagged as options.

**Pooled out-of-fold results (663 turns: 250 without a question, 413 with one)**

| Run                                         | False questions | Recall | Kind      | Options exact |
| ------------------------------------------- | --------------- | ------ | --------- | ------------- |
| v3 config (baseline)                        | 0.144           | 0.978  | 0.770     | 0.312         |
| v3 + compiler rules                         | 0.116           | 0.961  | 0.804     | 0.343         |
| v4: + hard negatives, more compiler rules   | 0.036           | 0.959  | 0.828     | 0.390         |
| v5: + inline multi-choice lists, escapes    | 0.036           | 0.973  | 0.799     | 0.434         |
| v5, hidden 96                               | 0.044           | 0.973  | 0.803     | 0.425         |
| **v6: + clause pairs (shipped)**            | **0.040**       | 0.966  | **0.837** | 0.454         |
| v6, 35% hand                                | 0.032           | 0.976  | 0.831     | 0.462         |
| v7: v6 + hand augmentation, 35% hand        | 0.036           | 0.966  | 0.825     | 0.465         |
| v7: v6 + hand augmentation, 20% hand        | 0.040           | 0.969  | 0.833     | 0.489         |
| ensemble of v6, v6-35, v7, v7-20            | 0.032           | 0.966  | 0.830     | 0.472         |

Kind accuracy is measured when a question is found, so recall is reported next to it. One turn is about 0.25 points of kind accuracy, and differences of 1 to 2 points between runs are within seed noise.

**Outcome**

- **False questions: met.** The rate went from 14.4% to 4.0%.
- **Kind accuracy: not met.** It plateaued at 83–84%. On the 561 turns the labeler did not flag as ambiguous, v6 gets 89.6%. On the 102 flagged turns, it gets 56.9%.
- **Why it plateaued:**
  - Each fold model gets only 94–95% kind accuracy on its own training turns, and about 83% on unseen datasets. More capacity, more hand weight, hand augmentation, and ensembling did not change out-of-fold kind accuracy. The limit is generalization across datasets with 663 labels from 52 datasets.
  - The hand labels also contain a few borderline conventions. For example, "Want a different filename or speed?" is yes_no, while "Want a diff or a walkthrough?" is either_or.
- **Weak datasets:** kind accuracy is lowest on vtcode (69%), economist-tui (71%), pi-web (78%), and pi-mono (80%).

`runs/v6-all/final.pt` is v6 trained on all 663 hand-labeled turns (`--all-hand`). It is the default for `gq.predict` and the review server. No held-out number exists for this exact model; the cross-validation numbers above are its estimate.

## v8–v9: adjudicated labels, batch 2, and an untouched test set

**Adjudication.** A second agent (GPT-6-Sol) settled batch 1's 102 ambiguous items against the new `gold/CONVENTIONS.md`: 94 kept, 8 changed, none left ambiguous, plus 5 consistency fixes (`gold/adjudication.jsonl`). Retrained v6 cross-validation on the adjudicated labels: false questions 4.0%, kind 83.2%. So the ambiguous items were hard, not mislabeled.

**Batch 2.** A third agent (Opus 5.5) labeled 1,995 turns from 66 datasets that are not in batch 1 (`gold/batch2/`, sources in `gold/batch2/SOURCES.md`). 62.8% have a question, 333 of the 742 negatives are hard, and 70 are flagged ambiguous. Neither labeling agent saw model outputs.

**Split** (`scripts/make_split2.py`, groups are Hugging Face owners):

- **Untouched test set** (`batch2_test_datasets`): 599 batch-2 turns from 18 owners, 62.8% with a question. Owners that also appear in batch 1 were not eligible. It is scored only through `gq.cv --holdout`, which appends every run to `runs/holdout_log.jsonl`.
- **Development set:** batch 1 plus the other 1,396 batch-2 turns, 2,059 in total. The 5 cross-validation folds are grouped by owner, 411–412 turns each. `--all-hand` trains on this set.

**Changes**

- Compiler: a wh-word after a short lead-in ("Ready — what…") counts as open, as does "Can you confirm how/what…". A list of `?` items after "Would you like me to:" merges into one choice (a fallback; the model rarely produces the tags it needs).
- Generator: the "Would you like me to:\n1. A?\n2. B?" shape, where the question spans the whole list and the items are options, plus "Want me to tackle any of these?" after a list.

**Pooled out-of-fold results (2,059 turns)**

| Run                                     | False questions | Recall | Kind  | Options exact |
| --------------------------------------- | --------------- | ------ | ----- | ------------- |
| v8: v6 settings on the bigger pool      | 0.047           | 0.964  | 0.797 | 0.375         |
| v8, 35% hand                            | 0.049           | 0.967  | 0.808 | 0.404         |
| v8, 35% hand + compiler rules           | 0.049           | 0.967  | 0.811 | 0.404         |
| **v9: + offer-list shape, 35% hand**    | **0.040**       | 0.966  | **0.810** | 0.403     |
| v9, hidden 96                           | 0.040           | 0.977  | 0.801 | 0.389         |

On batch 1 alone, v9 gets 1.6% false questions and 81.4% kind. On the batch-2 development side, it gets 5.2% and 80.9%.

**Untouched test set, scored once** (`runs/v9-all/final.pt`, v9 trained on all 2,059 development turns):

| Metric | Value |
|---|---|
| False questions (223 negatives) | **4.0%** |
| Recall (376 with a question) | 96.0% |
| Kind accuracy | **79.2%** |
| Options exactly right | 32.7% |
| Question count right | 90.9% |

**Outcome**

- **The estimate held up.** The test set lands within 2 points of the cross-validation estimate, so the evaluation is honest.
- **False questions: met** on unseen owners.
- **Kind accuracy: not met.** It stays around 80%. Tripling the real data, adjudicating labels, doubling the width, and adding shapes each moved it by about a point or less.
- **Why:** the compiler reaches 96–97% on gold spans, so the loss is in tagging. The tagger has no vocabulary (hashed word features, 256-token tail) and fits its own training turns at only about 95%.

## v10: structure features, kind head, teacher distillation, and size

Three ideas were tried alone and in combination, all with the v9 recipe (35% hand) and the same owner-grouped 5-fold CV:

- **A, structure features** (`--features 2`): hash tables of 8,192 rows, word bigrams, and list/line structure buckets (item index, list size, `?` at line end, questions before and after, code/quote/bold context). About 700k parameters at hidden 48.
- **B, kind head** (`--kind-head`): attention pooling over the last question span, trained jointly (weight 0.5). `--kind-mode` picks the compiler's kind, the head's, or a hybrid that lets a confident head override.
- **C, teacher distillation** (`gq/teacher.py`, `--distill`): fine-tune Ettin-32m (a ModernBERT-style encoder) on the same token roles, then tag about 15–19k unlabeled public turns per fold (never the held-out fold, the test owners, or labeled items) and mix them into training. `--distill-pos 0.5` balances turns with and without questions (only 14% of the pool has one), and `--distill-min-conf 0.9` drops uncertain teacher labels.

**Pooled out-of-fold results (2,059 turns)**

| Run | Params | False questions | Recall | Kind | Options exact |
|---|---|---|---|---|---|
| v9 baseline | 141k | 0.040 | 0.966 | 0.810 | 0.403 |
| A | 697k | 0.036 | 0.966 | 0.808 | 0.375 |
| B (hybrid / compiler / head) | 154k | 0.047 | 0.960 | 0.786 / 0.794 / 0.796 | 0.348 |
| C | 141k | 0.047 | 0.971 | 0.809 | 0.399 |
| C, balanced + augmented | 141k | 0.042 | 0.970 | 0.813 | 0.391 |
| A+B | 710k | 0.038 | 0.968 | 0.789 | 0.353 |
| A+B+C | 710k | 0.048 | 0.978 | 0.806 | 0.363 |
| Teacher (Ettin-32m, upper bound) | 32M | 0.036 | 0.990 | 0.849 | 0.510 |
| Big: hidden 128, 3 layers, no teacher | 533k | 0.045 | 0.977 | 0.847 | 0.474 |
| **Big + C** | 533k | **0.034** | 0.979 | **0.841** | 0.461 |
| Big + C, second seed | 533k | 0.043 | 0.983 | 0.833 | 0.477 |
| Big + C, hidden 192 | 1.1M | 0.045 | 0.982 | 0.838 | 0.467 |
| Big + C, 50% distill | 533k | 0.040 | 0.982 | 0.823 | 0.434 |
| Big + A + C | 2.0M | 0.049 | 0.991 | 0.818 | 0.437 |
| Big + B + C | 546k | 0.045 | 0.977 | 0.824 | 0.398 |
| **Big + C, two seeds averaged** | 1.07M | **0.032** | 0.980 | **0.848** | **0.500** |

Seed-to-seed spread is about one point on both metrics, so single-run differences under a point are noise.

**Findings**

- **Size was the missing ingredient, not features.** Going from hidden 48 × 2 layers to hidden 128 × 3 layers lifts kind accuracy about 3.5 points, with or without the teacher. Wider still (192) does not help further.
- **The teacher sets the ceiling, and the student reaches it.** A 32M pretrained encoder gets 84.9% kind. The 533k student gets 83–85%. Distillation's gain is mostly in false questions and stability, and it shows best when two seeds are averaged.
- **Bigger hash tables (A) and the kind head (B) hurt or do nothing.** A's 8k-row tables overfit (2M parameters at the big size). The kind head learns about what the compiler already knows, and joint training slightly worsens the spans.
- **What is left is semantic.** The largest confusion is yes/no against either/or (about 75 items out of fold): "Want a diff or a walkthrough?" is a choice, but "Want a different color or label?" is one yes/no offer (`gold/CONVENTIONS.md`). The teacher makes the same mistakes.

**Untouched test set, scored once** (second entry in `runs/holdout_log.jsonl`): `runs/v10-all-a` and `runs/v10-all-b`, the big + C recipe with seeds 20260923 and 7, trained on all 2,059 development turns plus 18,848 turns tagged by a teacher trained on the same turns, averaged at inference:

| Metric | v9 | **v10** |
|---|---|---|
| False questions (223 negatives) | 4.0% (9) | **5.8% (13)** |
| Recall (376 with a question) | 96.0% | 99.2% |
| Kind accuracy | 79.2% | **86.6%** |
| Options exactly right | 32.7% | 36.5% |
| Question count right | 90.9% | 92.8% |

Kind accuracy improved by 7.4 points and beat the CV estimate. False questions got worse: 4 more of 223 negatives, which is over the 5% target. The estimate for 223 negatives has a standard error of about 1.6 points, so this may be noise, but it cannot be tuned against the test set.

v10 runs at about 18 ms per message on the M4 Max CPU (two members, PyTorch eager). It has 1.07M parameters: 4.3 MB at fp32, or about 800 KB at 6 bits.

Reproduce:

```sh
uv run --group teacher python -m gq.teacher cv --run teacher32        # per-fold teachers + upper bound
for k in 0 1 2 3 4; do uv run --group teacher python -m gq.teacher label --run teacher32 --fold $k; done
uv run python -m gq.cv --run cv-Cbig --train -- --workers 1 --hand-rate 0.35 --hand-augment --hidden 128 --layers 3 \
    --distill 'runs/teacher32/fold{fold}/distill.jsonl' --distill-pos 0.5 --distill-min-conf 0.9
uv run --group teacher python -m gq.teacher train --run teacher32 --all
uv run --group teacher python -m gq.teacher label --run teacher32 --all
uv run python -m gq.train --run v10-all-a --all-hand --hand-rate 0.35 --hand-augment --hidden 128 --layers 3 \
    --distill runs/teacher32/all/distill.jsonl --distill-pos 0.5 --distill-min-conf 0.9   # and v10-all-b with --seed 7
```

## Scoring audit

Exact option matching rejected outputs such as `recommendation: vhs for scripted/reproducible demos` against the gold option `vhs`. Two agents (GPT-6-Sol and Opus 5.5) judged 613 out-of-fold v10 results, mostly mismatches plus 80 exact matches as controls, from the UI's point of view (`runs/audit/`, reports `REPORT_1.md` and `REPORT_2.md`). They shared 100 items and agreed on options for all 100, on detection for all 100, on propose for 98, and on kind for 96.

- **Options were scored too strictly.** Of 297 option results the exact metric rejected, the auditors judged 90 equivalent and 11 acceptable. `gq.evaluate.options_match` now requires the same number of options in the same order. Each gold option must equal its prediction after normalization, or appear in it as a whole run of words (explanations, labels, and markup allowed), and a prediction must not contain a different gold option. It accepts 139 of the 140 results the auditors called match or equivalent and none of the 196 they called wrong. `gq.cv` reports it as `options_ok`, next to `options_exact`.
- **Kind and propose were scored fairly.** Only 6 of about 230 kind mismatches were judged acceptable, and 99 of 101 propose mismatches in packet 2 were real errors. Kind accuracy stays as it was.
- **Compiler cleanup:** option text now drops a leading "recommendation:" label and unbalanced backticks. The reports list more cleanup work (lead-in words, trailing explanations, splits inside parentheses) and 22 suspect gold labels, which have not been applied.

| | `options_exact` | `options_ok` |
|---|---|---|
| v9 CV | 40.3% | 63.1% |
| v10 recipe CV (two seeds) | 50.0% | 70.1% |
| v10 test set (third log entry; same model, metric change only) | 36.5% | 61.5% |

## v11: batch 3

Three more labeling agents worked on separate sources (`gold/batch3/<labeler>/`, conventions questions in `gold/batch3/QUESTIONS.md`), with at least a third of questions near the yes/no-versus-choice boundary. Batch 3 has 2,871 turns:

- **dev** (Opus 5.5): 1,197 turns from unlabeled turns of already-used development datasets.
- **new-a** (Opus 5.5): 1,486 turns from 26 new datasets (24 new owners), mostly Claude chat distills and Claude Code, Copilot, Cursor, and Gemini CLI exports. The chat distills are about 90% questions; the small coding-agent datasets are almost all hard negatives.
- **new-b** (GPT-6-Sol): 188 turns from 12 new datasets, as eligible sources ran out.

**Test-set mirror.** `introvoyz041/my-personal-codex-data` re-uploads `REXX-NEW/my-personal-codex-data`, a test-set dataset, under another owner, so the owner exclusion missed it. Its 33 labels were removed. Labelers now check each dataset against the test set's session IDs (`data/batch3/test_sessions.txt`). `scripts/add_batch3_folds.py` refuses batch-3 turns that share an owner, session, or message text with the test set, and the pipeline test checks the same for all development data. The teacher's unlabeled pool shares no sessions with the test set, and only one generic greeting.

`gq.data.load_hand_dev` includes every batch-3 file. `scripts/add_batch3_folds.py` adds new datasets to their owner's fold (new owners to the smallest fold) without moving existing assignments.

**CV with the first 2,423 batch-3 turns** (v10 recipe, two seeds averaged, 4,482 turns in 5 folds):

| Items scored | Trained on | False questions | Recall | Kind | `options_ok` |
|---|---|---|---|---|---|
| Batches 1+2 (2,059) | batches 1+2 | 0.032 | 0.980 | 0.848 | 0.701 |
| Batches 1+2 (2,059) | batches 1–3 | 0.031 | 0.981 | 0.846 | 0.663 |
| Batch 3 (2,423) | batches 1–3 | 0.041 | 0.952 | 0.782 | 0.561 |
| New-dataset turns (1,226) | v10, never saw batch 3 | 0.051 | 0.950 | 0.762 | 0.560 |
| New-dataset turns (1,226) | batches 1–3, out of fold | 0.037 | 0.927 | 0.792 | 0.516 |

More data leaves the old items unchanged, but on datasets v10 never saw, it raises kind accuracy by 3 points and lowers false questions from 5.1% to 3.7%, at a cost in recall and options. Batch 3 is harder than batches 1–2 (it is boundary-heavy by design; compiler oracle 94.6% overall, versus 96.1% before).

With all 2,871 batch-3 turns (4,930 in total), the two-seed CV gives false questions 2.9%, kind 84.6%, and `options_ok` 66.7% on batches 1+2, and 4.7%, 78.6%, and 54.6% on batch 3.

**v11** (`runs/v11-all-a`, `runs/v11-all-b`) is the v10 recipe trained on all 4,930 development turns, with a teacher retrained on the same turns (`runs/teacher32b`, 17,897 pool turns kept). It became the default before its test score was known, because it matches v10 on the old data and generalizes better to new sources. **Untouched test set, scored once** (fourth entry in `runs/holdout_log.jsonl`):

| Metric | v9 | v10 | **v11** |
|---|---|---|---|
| False questions (223 negatives) | 4.0% | 5.8% | **4.5%** |
| Recall (376 with a question) | 96.0% | 99.2% | 98.4% |
| Kind accuracy | 79.2% | 86.6% | **85.7%** |
| `options_ok` | — | 61.5% | 60.0% |
| Propose | — | 81.0% | 80.8% |

The false-question target is met again. Kind accuracy is unchanged within noise and still short of 90%.

## v12: LLM-labeled data and static word vectors

Four ideas were tried. Each was measured with the v11 recipe, 5-fold CV, and two seeds (the default seed and `--seed 7`), scored as an ensemble with `--kind-mode compiler` (`scripts/cv_pair.sh NAME [train args]`).

1. **Silver labels** (`--silver 'silver/[0-9]*/labeled.jsonl'`). Six Cursor (Auto model) agents labeled 4,631 queued turns from public pools, following `gold/CONVENTIONS.md` (`scripts/make_silver_queue.py`, `.bb-prompts/silver-label-N.md`). The queue excludes test-set owners, mirrors, sessions, and text tails, and turns that were already labeled. After duplicate IDs and privacy drops are removed, 4,572 turns remain. `gq.data.load_silver` leaves out a fold's own datasets when training that fold. One known inconsistency: queue 1 labels imperatives without `?` as no question, while queues 3 and 6 label them open.
2. **Minimal pairs** (`--pairs 'silver/pairs-*/labeled.jsonl'`). Two Cursor agents wrote 1,500 synthetic pairs (3,000 messages). The two messages in a pair differ only in the clause that decides the label:
   - `pairs-a`: yes/no versus either/or, either/or versus multi-choice, examples versus options, and escape hatches.
   - `pairs-b`: open versus yes/no, offered versus background lists, propose versus not, and question versus no question.
3. **Static word vectors** (`--static runs/static/potion-base-8M-20k-32.pt`). The tagger gets a frozen table of 20k word vectors, reduced to 32 dimensions with PCA (built by `scripts/build_static.py` from `minishlab/potion-base-8M`, MIT), plus a trained projection. That adds 4k trainable parameters. Vectors taken from the Ettin encoder's embeddings mostly encoded spelling, so they were not used.
4. **Propose rule** (compiler only). `is_proposal` now recognizes offers such as "Would you like a/help…", "Want a/the…", "Ready to…", "Sound right?", and French and Chinese offers. Questions that start with a wh-word are not proposals. On gold spans, propose accuracy rises from 87.6% to 94.3% on batches 1+2, and CV propose accuracy rises from 86.9% to 93.0%.

**CV, two-seed ensemble, all 4,930 development turns** (baseline rescored with the new propose rule):

| Run | False questions | Kind | `options_ok` | Batch 3 kind | Batch 3 `options_ok` |
|---|---|---|---|---|---|
| v11 recipe | 0.040 | 0.812 | 0.603 | 0.786 | 0.546 |
| + static | 0.046 | 0.818 | 0.626 | | |
| + pairs | 0.045 | 0.817 | 0.609 | | |
| + silver | 0.037 | 0.813 | 0.611 | | |
| + static + pairs | 0.044 | 0.823 | 0.633 | | |
| **+ static + pairs + silver** | **0.040** | **0.829** | **0.654** | **0.813** | **0.614** |

Taken one at a time, each addition is within seed noise. Static vectors and pairs raise false questions slightly, and silver lowers them. Together they add 1.7 points of kind accuracy and 5 points of `options_ok` at the same false-question rate, and most of the gain is on batch 3. The compiler's oracle kind accuracy on gold spans stays at 94.5%, so the remaining kind errors come from span errors.

**v12** (`runs/v12-all-a`, `runs/v12-all-b`) uses the winning recipe: all hand labels, `runs/teacher32b/all` distillation, all 4,572 silver turns, the 3,000 pairs, and static vectors. It was chosen on CV before its test score was known. **Untouched test set, scored once** (fifth entry in `runs/holdout_log.jsonl`):

| Metric | v11 | **v12** |
|---|---|---|
| False questions (223 negatives) | 4.5% | **3.6%** |
| Recall (376 with a question) | 98.4% | **98.9%** |
| Kind accuracy | 85.7% | 85.5% |
| `options_ok` | 60.0% | 59.8% |
| Propose | 80.8% | **87.9%** |

False questions and propose improve. The propose gain comes mostly from the compiler rule, which applies to any checkpoint. The CV gains in kind and options do not appear on the test set. The gap is within the test set's resolution of about 2 points, but it also suggests the gains are concentrated on batch-3-like sources.

**Compute.** The CV runs and the final models were split between the Mac (5 folds at a time, about 12 GB of RAM) and a RunPod RTX 4090 pod (`scripts/runpod_api.py`, key in the git-ignored `.env.local`). On the pod, each fold peaks at about 4 GB of GPU memory, so the 24 GB card holds 5 folds (`GQ_CUDA_MEM_FRACTION=0.19`, `scripts/pod_ablations.sh`). Data generation on the CPU dominates epoch time, so the pod was no faster per fold than the Mac.

## Where kind errors come from

`scripts/span_errors.py cv-SPSi,cv-SPSi-s2` sorts each out-of-fold kind error by its first difference from the gold spans. It reads CV folds only, never a test set. It first reruns the compiler on the gold spans: if that also gets the kind wrong, the error belongs to the compiler rules or the label. 491 of 2,868 found questions have the wrong kind:

| Cause | Errors | Share | Mostly |
|---|---|---|---|
| Missed options (gold has options, prediction has none) | 200 | 41% | either_or → yes_no (89), multi_choice → open (42) |
| Compiler wrong even on gold spans | 116 | 24% | open → yes_no (88) |
| Spurious options (background list or "or" inside one proposal) | 92 | 19% | yes_no → either_or (58) |
| Too few or too many options | 39 | 8% | multi_choice ↔ either_or |
| Different question picked | 36 | 7% | |
| Only the prompt boundary differs | 8 | 2% | open ↔ yes_no |

Rows include errors where the prompt boundary is also off. So whether a question has options at all causes 60% of kind errors. Many missed options sit far from the prompt: an "Option A / B / C" plan followed by "What's your read?", or a parenthesized list inside a long question. Batch 3 has 1.6 times as many errors as batches 1+2.

**Open-question rule.** The compiler now treats information requests that do not start with a wh-word as `open` (`gq.compile.is_open`), following the conventions:
- a wh-word after a short lead-in ("If so, what…", "Now, to check your order, could you provide…");
- request verbs ("could you provide/share/list/paste/tell me…", "…and share the…");
- "Do you remember/know…" and "Do you have the … ID/URL/name?".

The rule was written from batches 1+2 only. On gold spans, it moves the compiler from 96.1% to 97.7% on batches 1+2 and from 93.2% to 94.1% on batch 3, which was not used to write it. Rescoring the v12-recipe CV ensemble gives kind 83.7% (was 82.9%), 85.8% on batches 1+2, and 82.0% on batch 3. No retraining is needed.

**Label noise found along the way.** Near-identical prompts carry opposite labels: "Anything else?" is `yes_no`, but "Anything I'm missing that you had in mind?" is `open`. "Could you double-check the filename?" is `open`, but "…the path?" is `yes_no`. The same Chinese offer (有什么我可以帮你的吗) appears once as `open` and once as `yes_no`. Rules for those phrasings were left out, because they only swap one set of errors for another. The conventions need a decision first.

## Label ceiling versus model ceiling

The architecture review ([architecture-research.md](architecture-research.md)) suggested three cheap checks before changing the model:

- **k-best oracle** (`scripts/ceiling_diagnostics.py`): the gold kind is in the student ensemble's best CRF path for 84.3% of found questions, and within the 5 best paths for 89.2%. Reranking alternative paths could recover at most about 5 points.
- **Error overlap:** the out-of-fold Ettin-32m teacher makes 63% of the student's kind errors. If the two models' errors were independent, the overlap would be about 16%. Both models fail on the same items.
- **Blind relabel** (`.bb-prompts/relabel-blind.md`, `scripts/relabel_agreement.py`): two fresh agents (Claude and Codex) relabeled 300 development turns without seeing gold. The set had 200 random turns and 100 turns whose kind the model gets wrong, shuffled.

| Kind agreement, turns where gold has a question | Random (104) | Model errors (100) |
|---|---|---|
| Gold vs Claude relabel | 95.2% | 83% |
| Gold vs Codex relabel | 91.3% | 81% |
| Claude vs Codex | 92.3% | 84% |

Independent labelers agree on about 92–95% of random questions, while the model reaches about 84%. On the items the model gets wrong, the relabelers side with gold about 80% of the time, and both disagree with gold on only 9 of 100 (5 of them gold `either_or` read as `yes_no`). So label noise explains only 1–2 points of the gap. Both models fail on items that labelers find hard but still label consistently, which is a model limit. The relabelers' unclear cases (open second arms such as "…or further refinement", menu lead-ins, "Do you have any X?") are listed in `data/relabel/*/NOTES.md`.

## Batch 4 test set

Batch 4 (`gold/batch4/`) has 218 turns from 12 owners that appear nowhere else (`data/batch4/excluded_owners.json`, `scripts/check_batch4.py`). It is frozen and scored with `python -m gq.cv --holdout RUN --set batch4`; a test keeps it out of training. Hugging Face sources with new owners are nearly used up, so it is small: 91 questions, so kind accuracy moves about ±5 points by chance.

v12 on batch 4: false questions 3.9%, recall 95.6%, kind 72.4%, options_ok 55.8%, propose 82.8%. The compiler applied to gold spans reaches only 91.2%, and the set is heavy in `either_or`, the student's weakest kind. Treat it as a coarse check on generalization, not a decision tool.

## Capacity and richer static vectors

Both experiments ran on RunPod (`scripts/pod_setup.sh`, `scripts/pod_static.sh`) with the same five owner-grouped folds. All numbers are pooled out-of-fold on the 4,930 development turns, with `is_open` in the compiler.

| Model | Params | False q | Kind | options_ok |
|---|---|---|---|---|
| Student v12 recipe (2-seed ensemble) | 537k | 4.0% | 83.7% | 65.4% |
| + Potion static 64-dim, 20k vocab | | 3.5% | 84.3% | 66.0% |
| + static 128-dim, 20k vocab | | 3.9% | 84.1% | 66.9% |
| + static 64-dim, 50k vocab | | 3.8% | 84.3% | 66.1% |
| + static 64-dim, trainable table | 1.82M | 4.0% | 84.0% | 65.2% |
| Ettin-32m teacher, 8 epochs, silver + pairs | 32M | 2.5% | 86.8% | 73.8% |
| Ettin-150m teacher, same recipe | 150M | 2.4% | 87.8% | 74.5% |

Richer or trainable static vectors add at most 0.6 points, which is within seed noise (single seeds differ by up to 0.7). The static table is not the bottleneck.

Capacity helps. The 32m teacher with the stronger recipe beats the student by 3 points, and 150m adds 1 more. Per fold the 150m teacher reaches 84–90%, so it does not clear the 89% bar pooled. Scaling the teacher alone will not reach 90%. Its advantage is also large on options (74.5% versus 65.4%), which the student's CRF finds hard.

## v13: Ettin-150m distillation, attention, and constrained kind rerank

All numbers are pooled out-of-fold on the 4,930 development turns (same folds as v12), with `is_open` in the compiler. The student recipe matches v12 except the distillation teacher is Ettin-150m (`runs/teacher150`) instead of Ettin-32m. Two seeds averaged unless noted.

| Model | Params | False q | Kind | options_ok |
|---|---|---|---|---|
| Student v12 recipe (32m distill) | 537k | 4.0% | 83.7% | 65.4% |
| **v13: 150m distill** (`cv-t150`) | 537k | 3.8% | **84.7%** | 65.9% |
| + attention (`--attn 4`) | 570k | 4.1% | 84.9% | 67.4% |
| + kind head, compiler kind (`cv-t150-kh`) | 571k | 3.7% | 84.9% | 67.0% |
| + kind head, unconstrained k-best rerank (λ=1) | 571k | **23.2%** | 84.3% | 66.3% |
| **+ kind head, constrained rerank (λ=1)** | 571k | **3.7%** | **85.4%** | **67.5%** |
| Ettin-150m teacher (ceiling) | 150M | 2.4% | 87.8% | 74.5% |

```sh
# Per-fold teachers already live in runs/teacher150/{fold,all}/
uv run python -m gq.cv --run cv-t150 --train -- \
  --hand-rate 0.35 --hand-augment --hidden 128 --layers 3 \
  --distill 'runs/teacher150/fold{fold}/distill.jsonl' --distill-pos 0.5 --distill-min-conf 0.9 \
  --silver 'silver/[0-9]*/labeled.jsonl' --pairs 'silver/pairs-*/labeled.jsonl' \
  --static runs/static/potion-base-8M-20k-32.pt
# Kind head + constrained rerank at score time:
uv run python -m gq.cv --run cv-t150-kh --train -- \
  ...same... --kind-head --kind-weight 0.5
uv run python -m gq.cv --run cv-t150-kh --score --kind-mode rerank --rerank-k 8 --rerank-lambda 1
```

**Findings.**

- **150m distillation transfers about 1 point of kind.** Closing the remaining ~2.4 points to the teacher needs something beyond soft labels from the same folds.
- **Attention helps options more than kind** (+1.5 options_ok, +0.2 kind) and raises false questions slightly. It is not worth the ONNX/export cost for the shipped browser path.
- **Unconstrained k-best rerank invents questions on negatives** (false_q 3.7% → 23%). The fix is constrained rerank: only rescore when the top-1 path already compiles a question. That keeps false_q flat and adds **+0.5 kind** over compiler-only kind head (85.4%).
- **90% kind is out of reach with this student.** The teacher ceiling is 87.8%; the best student is 85.4%. Further gains need better labels or a different architecture, not another hyperparameter sweep on the same pool.

**Ship recipe (v13).** Same data mix as v12, distill from `runs/teacher150/all`, `--kind-head`, compiler kind at inference (rerank is optional and Python-only for now). Browser/ONNX exports the emission network only; CRF Viterbi and the compiler stay in TypeScript.

```sh
uv run python -m gq.train --run v13-all-a --all-hand --no-eval --workers 1 \
  --hand-rate 0.35 --hand-augment --hidden 128 --layers 3 \
  --kind-head --kind-weight 0.5 \
  --distill runs/teacher150/all/distill.jsonl --distill-pos 0.5 --distill-min-conf 0.9 \
  --silver 'silver/[0-9]*/labeled.jsonl' --pairs 'silver/pairs-*/labeled.jsonl' \
  --static runs/static/potion-base-8M-20k-32.pt
# second seed: --run v13-all-b --seed 7
uv run python scripts/export_onnx.py \
  --checkpoint runs/v13-all-a/final.pt,runs/v13-all-b/final.pt \
  --out web/public/model
```

## Next steps

1. **Kind above 90% is blocked by the teacher ceiling (87.8%).** Settle unclear label conventions and the imperative-without-`?` silver inconsistency; do not expect another student tweak to clear 90% on this pool.
2. **Test sets.** `runs/holdout_log.jsonl` has five batch 2 entries, so batch 2 can no longer separate models within about 2 points. Batch 4 is frozen but small (see above). Score v13-all once on the untouched holdout when both seeds finish.
3. **Browser package.** Emission ONNX + TypeScript features/CRF/compile (`web/`). Quantize later (int8 static table, optional 6-bit QAT).
4. Optional: WGSL scan kernels after the ONNX path is correct.
