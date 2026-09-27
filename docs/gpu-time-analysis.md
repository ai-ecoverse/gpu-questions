# How gpu-time works

Source: <https://gpu-time.arikko.dev>, repo <https://github.com/arikchakma/gpu-time> (MIT), npm `gpu-time@0.5.0`.

gpu-time turns English phrases such as "book dinner for October 2 at eight pm" into resolved dates and RFC 5545 rules. The core idea is that the neural model does very little: it only tags tokens. Everything else is ordinary deterministic code.

## Pipeline

```
text ──► tokenizer (TS, regex) ──► sparse feature rows per token
     ──► tiny tagger (~25–39k params) ──► per-token role + boundary score
     ──► CRF Viterbi decode (CPU)
     ──► compiler (TS) roles → typed Schedule   (rejects impossible role sequences)
     ──► resolver (TS) Schedule + reference + timezone → occurrences, RRULEs
```

The caller context (reference instant, timezone) never enters the model. The model is context-free with respect to "now".

## 1. Tokenizer and features (no vocabulary)

- Regex split: letters, digits, whitespace, single punctuation.
- Each token becomes about ten sparse feature rows that index disjoint regions of a 580-row embedding table:
  kind, length bucket, first and last character class, an 8-bit hash of the lowercased word, a 7-bit hash of the consonant skeleton ("tmrrw"), previous and next punctuation, and flags (casing, first or last token, and so on).
- There is no word list. The model never "knows" that "October" is a month; it learns from hashed spelling plus context. That keeps the model small and tolerant of typos and abbreviations.
- The row embeddings are summed into one 32-dimensional vector per token.

## 2. Model (`packages/training/torch/model.py`)

- Hidden size 32.
- A 5-tap depthwise convolution and neighbor weights provide local context.
- Bidirectional **affine scan** layers compute `state[t] = gate[t] * state[t-1] + candidate[t]`. This is a gated linear RNN, a minimal SSM, with 1 to 3 layers. It runs as a parallel prefix scan in WGSL, so long inputs parallelize on the GPU. Gate biases are initialized from 0 to 4 so that different lanes get short and long memories.
- Global mean-pool context is concatenated back to every token.
- A gated MLP head produces **40 role logits** (35 used) plus **1 boundary logit** per token. The boundary logit splits one input into several expressions, with a threshold of 0.75.
- An optional 40×40 transition matrix turns the classifier into a **linear-chain CRF**. Viterbi decoding runs on the CPU.
- Shipped with int6 weights (QAT from epoch 14), about 22 KB Brotli. The whole package must stay under 50 KB Brotli.

Roles are a flat BIO-less tag set: `O, NUM, ORD, UNIT, WEEKDAY, MONTH, HOUR, MINUTE, MERIDIEM, RANGE_START, RANGE_END, RECUR, FREQ, EXCEPT, JOIN, GLUE, ...`. The compiler interprets role sequences, not the model.

## 3. Training data is synthetic, not scraped

- `generate.py` renders schedules from **semantic slots**. Each slot knows its label and character span, so labels come for free and are exact. Labels never come from the runtime parser, so the model is not trained on its own output.
- `natural.py` adds natural phrasings. `background.py` adds carrier phrases ("the meeting is at …"). Filtered Tatoeba sentences provide negative prose where every token is labeled `O`, which teaches "no expression here".
- Augmentation covers casing, whitespace, and abbreviations.
- About 300k fresh samples are drawn each epoch (`--fresh-each-epoch`).
- **Leak control:** train, validation, and holdout splits are kept disjoint by *structural fingerprint*, not by rendered string, because holding out strings still leaks the phrase family. There is also a separate "unseen sentence frame" evaluation.
- `--real` can append hand-labeled real sentences to every epoch.

## 4. Loss and training tricks

- CRF negative log-likelihood with sqrt role weighting.
- `--risk-lambda`: a sequence-level ranking loss with a margin, which penalizes wrong full parses and not just wrong tokens.
- **Negative-flip control:** fine-tuning on a new phrase family broke 11 unrelated cases. The fix is focal distillation from Positive-Congruent Training (Yan et al., 2021) against the previous checkpoint. The key setting is `alpha=0, beta=5`: it only constrains tokens the reference already gets right, which leaves the model free to learn new families.
- **Promotion gate:** export compares the candidate against the shipped model on every gold set and family. No family may regress, and a pooled gain cannot hide a per-family regression. Each export records provenance and a sha256 hash.

## 5. Evaluation assets

- `data/gold/*.jsonl` holds hand-written grammar cases, mechanical variations, adversarial cases, negatives (time words used in non-time contexts), prose, and chat.
- `labels.jsonl` holds per-token gold tags. This enables an **oracle run**: run the compiler on perfect tags, which separates compiler bugs from model errors.
- CPU/GPU parity fixtures are checked in, so a clean clone can verify inference without the checkpoints.
- Per-token confidence is the emission softmax. Low confidence produces the "model is uncertain" hint shown on the demo page.

## What to copy for agent questions

| gpu-time                                     | gpu-questions analogue                                                      |
| -------------------------------------------- | --------------------------------------------------------------------------- |
| Token roles (HOUR, WEEKDAY, RANGE_START…)    | Span roles: question cue, option start and inside, option separator, default marker, and so on |
| Boundary score splits multiple expressions   | Split multi-question messages into separate questions                       |
| Compiler: roles → typed `Schedule`           | Compiler: roles → typed `Question { kind, prompt, options[], default }`     |
| Resolver adds reference/timezone after model | UI layer adds the answer widget (buttons, radio, free text) after the model |
| Synthetic generator with slot-derived labels | Template generator plus **free gold** from structured ask-tool calls in traces |
| Tatoeba negatives                            | Rhetorical questions, questions inside code blocks, non-question endings    |
| Structural-fingerprint splits                | Split by session or project to avoid leakage from repeated phrasings        |
| Oracle compiler eval                         | Run the compiler on gold tags to isolate compiler bugs                      |
| Focal distillation + per-family gate         | Same, applied per question kind or agent                                    |

The main lesson is to keep the neural part to span tagging and let deterministic code build the structure. A model of about 30k parameters is enough when it only has to label tokens.
