# Is the kind-accuracy ceiling architectural?

This report is research only. No code, data, or runs were changed. The evidence comes from `gq/model.py`, `gq/compile.py`, `gq/teacher.py`, `docs/training.md`, `gold/CONVENTIONS.md`, and read-only statistics on the batch-1 dev turns in `gold/handlabeled.jsonl`.

## Short answer

The current evidence points mostly to a label and convention ceiling, with a smaller loss-alignment problem. Missing capacity or semantics is less likely to be the main cause. The strongest single fact is this: the Ettin-32m teacher, which has full attention and pretrained subword semantics, scored 84.9% kind on the 2,059-turn CV pool. The 533k-parameter student scored 84.8% on the same pool and makes the same yes_no/either_or mistakes. If semantics were the missing ingredient, a 60x larger pretrained encoder should have pulled ahead. That evidence has a caveat, though. The teacher recipe is weak: 4 epochs at lr 1e-4, a plain softmax token head without a CRF, first-subword label alignment, no silver data or minimal pairs, and no tuning. So the teacher result is a lower bound on what a strong encoder can do. It is not yet a real upper bound. Experiment 2 below closes that gap cheaply.

The arithmetic of the target also matters. The compiler scores 94.5% on gold spans, so reaching 90% overall means removing about 60% of the roughly 11.6 points currently lost to span errors. Earlier results showed a large split by difficulty: v6 reached 89.6% on unflagged turns but only 56.9% on turns the labeler flagged as ambiguous. Batch 3 was built to be boundary-heavy, and its kind accuracy is lower (81.3% against 82.9% pooled). Both facts suggest much of the remaining error sits on items where the convention itself is subtle. For example, `CONVENTIONS.md` labels "Want a diff or a walkthrough?" as either_or but "Want a different filename or speed?" as yes_no.

## 1. Is tag-then-compile limiting?

**Loss misalignment is real.** The compiler assigns kind almost entirely from the number of option spans (`len(opts)` in `compile_questions`: 0 or 1 gives yes_no/open, 2 gives either_or, 3 or more gives multi_choice). So one wrong `OPT_B` token out of about 250 flips the kind, while the CRF negative log-likelihood (`Tagger.nll`, averaged per token) barely notices it. Most of the listed confusions are exactly this kind of count error: either_or→yes_no (106), yes_no→either_or (63), and multi_choice→yes_no/open (90). No architecture change fixes that by itself. What helps is a decoder or loss that targets the structure the compiler reads.

**Why the naive kind head hurt.** The head (`kind_logits`) pools only over the *gold* question span during training (`kind_target` → `collate_kind`), but over the *predicted* span at inference. It shares the encoder at weight 0.5, so it competes with span learning. And it cannot directly see option lists outside the question span. Two better designs follow:

- **Soft spans:** use CRF marginals as structured attention (Kim et al. 2017, *Structured Attention Networks*, arXiv:1702.00887). This makes kind differentiable through the predicted spans, as the question suggests.
- **Rerank instead of override:** decode the k best CRF paths, compile each one, and choose by CRF score plus the log-probability of the head's kind. This keeps the compiler's guarantees, and the head can only choose among paths the tagger already considers plausible. This is essentially constrained inference over structured outputs (Roth & Yih 2005, "Integer Linear Programming Inference for Conditional Random Fields", ICML).

**Semi-Markov or span outputs.** Segment-level models (Sarawagi & Cohen 2004, NeurIPS; SpanNER, Fu et al. 2021, arXiv:2106.00641) usually gain only 0.5–1 F1 over BIO+CRF in NER. Their real advantage here would be features over a whole segment: option length, parallel structure between two conjuncts, and whether a segment starts after "or". The literature on coordination boundaries finds that similarity between conjuncts is the key signal (Ficler & Goldberg 2016, "A Neural Network for Coordination Boundary Prediction", EMNLP; Teranishi et al. 2019, NAACL). A semi-CRF with a maximum segment length L≈24 costs O(T·L·labels), which is still cheap in a browser. It is a larger rewrite than reranking, so I rank it below reranking.

## 2. Capacity and inductive bias

The model has 537,200 parameters: 301k in the hash embedding table, 198k in the scan layers, 4k in the static projection, and about 33k in the head. Gated linear scans compress the whole left and right context into a fixed state per lane. They are known to be weak at associative recall and at pairwise comparison (Arora et al. 2023, *Zoology*, arXiv:2312.04927; Jelassi et al. 2024, arXiv:2402.01032). Hybrids that add a few attention layers close most of that gap (Griffin, De et al. 2024, arXiv:2402.19427, whose recurrence resembles `ScanLayer`; Jamba, arXiv:2403.19887). Three of the observed failures are pairwise by nature: judging whether two conjuncts are parallel, binding a list to the question that offers it, and picking one question among several. That is a real argument for adding one attention layer.

The counter-evidence is that the attention-based teacher did not do better. My estimate is that an attention layer is worth 0–2 points, not the 5 needed.

For small encoders, the Hugging Face configs show Ettin-17m at hidden 256, 7 layers, and a 50,368-token vocabulary: about 12.9M embedding parameters and 4M layer parameters. Ettin-32m is hidden 384, 10 layers, with about 19.3M embedding parameters. BERT-tiny (4.4M, Turc et al. 2019, arXiv:1908.08962) is also mostly embeddings. Pruning Ettin-17m to the roughly 16k subwords seen in agent text gives about 8M parameters (8 MB at int8). That runs in transformers.js with ONNX and WebGPU (https://huggingface.co/docs/transformers.js) but is 4–8x over budget. Browser latency is unmeasured. The v12 gain from potion static vectors (with pairs and silver, +1.7 kind points) suggests that the cheapest source of more semantics is a larger frozen table, for example 64 dimensions instead of 32. The table is frozen, so it adds almost no trainable parameters, and it would cost about 1.3 MB at int8.

## 3. Why the teacher caps near 85%

Label noise and an architecture ceiling predict different things:

- **Noise or convention ceiling:** very different models make the *same* errors, those errors concentrate on flagged or boundary items, and a fresh blind labeler disagrees with gold at a similar rate. The first two already hold: `training.md` says the teacher shares the student's mistakes, and flagged turns score 56.9%. The one data point on the third is weak. The auditors agreed on kind for 96 of 100 shared items, but those two agents were judging model outputs against gold. They did not relabel the items independently.
- **Architecture ceiling:** a much stronger encoder, trained well on the same labels, clearly beats 85%.

Diagnostics are experiments 1 and 2 below. Northcutt et al. (2021, arXiv:2103.14749) show that a few percent of test-label errors can reorder models, which is relevant here because a 2-point difference is at the limit of this test set's resolution.

## 4. Input framing

Read-only statistics on 663 batch-1 turns:

- The median length is 245 tokens and the 90th percentile is 389. 318 turns (48%) exceed `MAX_TOKENS=256`, but only 2 of them lose a gold span to the cut.
- From the first labeled span to the end of the message, the median is 21 tokens, the 95th percentile is 110, and the maximum is 367.
- " or " appears in 88% of either_or prompts, but also in 9% of yes_no prompts and 12% of open prompts. The word "or" is present in most of these cases. The difficulty is deciding what it coordinates.

So the tail does not lose needed context. If anything, 256 tokens carry many distracting background lists. A second pass over a focused window (the predicted question sentence plus the list directly above or below it, at most about 96 tokens) with explicit segment features would help a scan or attention model most. The candidate features are: token inside the predicted question, "or"/comma inside the question, list-item index, and list introduced by an offer line. Some of these flags already exist in `features_v2` (`sentence_or`, `sentence_offer`, `list_index`). But experiment A in v10 mixed them with 8k-row hash tables, which overfit, so the flags have never been tested alone.

## 5. Ranked experiments

| # | Experiment | Cost | Expected kind gain | Browser |
|---|---|---|---|---|
| 1 | Ceiling diagnostics | hours, no student training | decides direction | n/a |
| 2 | Strong teacher (Ettin-150m) as upper bound | ~1–2 GPU-h per 5 folds | decides direction | no (teacher only) |
| 3 | k-best rerank with a detached soft-span kind head | 1–2 days | +1–3 (if 1a is positive) | yes, +~20k params |
| 4 | One attention layer in the scan stack | 1 day | 0–2 | yes, +~66k params |
| 5 | v1 hashes + v2 structure flags; static dim 64 | < 1 day | 0–1.5 | yes |

**1. Ceiling diagnostics.**
- (a) *k-best oracle:* add k-best Viterbi next to `Tagger.decode`. Using the existing CV fold checkpoints, compute the out-of-fold kind accuracy you would get if an oracle picked the best of k=5 paths. If that exceeds 92%, reranking (experiment 3) is viable. If it stays near 85%, the correct structure is not among the tagger's hypotheses.
- (b) *Error overlap:* compute the Jaccard overlap between teacher and student kind errors, and the share of those errors on `ambiguous` or batch-3 boundary items.
- (c) *Blind relabel:* have a fresh agent relabel 300 random dev turns under `CONVENTIONS.md` without seeing gold, and measure kind agreement. If agreement is 90–93%, the >90% target is at the noise ceiling and the effort should go to conventions and labels.

**2. Strong teacher as upper bound.** Extend `gq/teacher.py:train` to include `load_silver` and the minimal pairs, which the student already uses. Then run `python -m gq.teacher cv --run teacher150 --model jhu-clsp/ettin-encoder-150m --epochs 8 --lr 5e-5` (ModernBERT-base is a comparable alternative) and score kind in compiler mode. A result of 89% or higher would indicate a real architecture or semantics gap. In that case, distill from this teacher and pursue experiments 3 and 4. A result near 86% would confirm a label ceiling.

**3. Kind-consistent reranking** (`gq/model.py`, `gq/evaluate.py:model_questions`, `gq/compile.py:apply_kind`).
- Change the kind head to (i) pool over the whole tail, weighted by the CRF marginals of `Q_*` and `OPT_*` (computed with forward-backward), and (ii) train on `joined.detach()`, so the head cannot degrade spans.
- Add a `--kind-mode rerank` mode that decodes k=8 paths, compiles each one, and picks the path maximizing CRF log-score + λ·log p(kind), with λ tuned on CV.
- Measure with `scripts/cv_pair.sh rerank --kind-head …` and then `python -m gq.cv --run rerank-a,rerank-b --kind-mode rerank`, and compare against `--kind-mode compiler` on the same checkpoints.
- Parameter count is about 537k + 20k. k-best Viterbi over 6 labels is trivial in TypeScript.

**4. Hybrid scan + attention.** In `Tagger.__init__`/`hidden`, insert one 4-head self-attention block (hidden 128, ALiBi or a 64-token window, residual connection plus layer norm) after the second `ScanLayer`. That adds about 66k parameters (plus 33k with a small feed-forward block). Measure with `scripts/cv_pair.sh attn --hidden 128 --layers 3 --attn 1 …` against the v12 pair. Attention over 256×256 is cheap in WGSL, and int6 quantization should be unaffected. The layer norm and softmax need a float path.

**5. Cheap feature ablations.** Both need small `tokenize.py` changes.
- Use the v1 hash tables with only the v2 structure flags added. This needs a new feature version, because version 2 couples the flags to the large hash tables.
- Rebuild the static table at 64 dimensions with `scripts/build_static.py`, and pass it with `--static`.

Measure both with `cv_pair.sh`. Each changes the parameter count by less than 10k trainable parameters.

**Deprioritized:** a semi-Markov CRF (unless experiment 1a shows boundary errors dominate and reranking fails), a pruned Ettin-17m student (about 8M parameters, over budget, no evidence it beats 85%), and a larger student (hidden192 and 2M parameters already failed).

## Uncertainty

The gain estimates are judgment, based on teacher/student parity and typical gains in the NER and coordination literature. None has been measured here. Seed noise is about 1 point, so every experiment should use the two-seed `cv_pair.sh` ensemble. The teacher's 84.9% and v12's 82.9% come from different pools (2,059 and 4,930 turns), so they are not directly comparable. Experiment 2 should report both pools.
