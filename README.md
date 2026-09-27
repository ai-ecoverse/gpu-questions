# gpu-questions

This project plans a tiny local model that turns an agent's free-text question into structured data. With that data, a UI can pre-populate answer choices that the agent already suggested:

```
"Want me to start on that in this thread, stacked on #2794, or wait for this one to merge?"
→ { kind: "either_or", action: "propose",
    options: ["start on that in this thread, stacked on #2794", "wait for this one to merge"],
    default: null }
```

The approach follows [gpu-time](https://gpu-time.arikko.dev): a model of about 30k parameters tags tokens, and deterministic code builds the structure.

- [docs/gpu-time-analysis.md](docs/gpu-time-analysis.md): how gpu-time works and what carries over.
- [docs/trace-survey.md](docs/trace-survey.md): how often agents on this machine ask questions, and in what shape.
- [scripts/extract.py](scripts/extract.py): read-only trace extractor. Writes to `data/survey/`, which is git-ignored. `--export data/export` writes the scrubbed training inputs.
- [docs/training.md](docs/training.md): first training runs, results, and caveats.
- [gq/](gq/): tokenizer, generator, model, compiler, training, evaluation, and prediction.

## Quick start

```sh
uv sync --python 3.13
uv run python scripts/extract.py --export data/export
uv run python -m gq.predict "Want me to merge it now, or wait for CI?"   # default: the v12 ensemble
# Browser product (gpu-ask.js):
#   uv sync --group export && uv run --group export python scripts/export_onnx.py \
#     --checkpoint runs/v13-all-a/final.pt,runs/v13-all-b/final.pt --out web/public/model
#   cd web && npm install && npm run dev
uv run python -m gq.cv --run cv-big --train -- --hand-rate 0.35 --hidden 128 --layers 3   # 5-fold CV
uv run python scripts/review_server.py   # spot-check UI for gold/handlabeled.jsonl
```

Training the ensemble (a teacher, then two students) is described in [docs/training.md](docs/training.md#v10-structure-features-kind-head-teacher-distillation-and-size); v11 uses the same recipe on more data, v12 adds [LLM-labeled data and static word vectors](docs/training.md#v12-llm-labeled-data-and-static-word-vectors), and [v13](docs/training.md#v13-ettin-150m-distillation-attention-and-constrained-kind-rerank) distills Ettin-150m (85.4% kind with constrained rerank). The browser product is **[@ai-ecoverse/gpu-ask.js](https://github.com/ai-ecoverse/gpu-ask.js)** ([live demo](https://ai-ecoverse.github.io/gpu-ask.js/)).

The current shipped recipe (v13) averages two taggers with about 571k parameters each (hidden 128, 3 layers, kind head, frozen 32-d word vectors), distilled from Ettin-150m. They are trained on:
- synthetic renderings and hard negatives
- 4,930 hand-labeled public agent turns (batches 1–3)
- about 4,600 public turns and 3,000 minimal pairs, labeled by an LLM
- about 18k unlabeled turns tagged by a fine-tuned Ettin-32m teacher

The browser product ships separately as **[@ai-ecoverse/gpu-ask.js](https://github.com/ai-ecoverse/gpu-ask.js)** ([demo](https://ai-ecoverse.github.io/gpu-ask.js/), [npm](https://www.npmjs.com/package/@ai-ecoverse/gpu-ask.js), [weights](https://huggingface.co/ai-ecoverse/gpu-ask.js)). `web/` here is the earlier in-repo demo; prefer the published package.

Its quality was measured on an untouched test set: 599 batch-2 turns from 18 Hugging Face owners it never saw.

- **False questions:** 3.6% of messages without a question get one (target below 5%, met).
- **Question kind:** 85.5% correct when a question is found, up from 79.2% for v9 (target above 90%, not met).
- **Recall:** 98.9% of real questions are found. The options are right 60% of the time, counting predictions that add explanation text to the right choices (`options_ok`, calibrated on a scoring audit); 38% match exactly.
- **Propose:** 87.9% correct, up from 80.8%, mostly from a compiler fix for offers like "Would you like a …".

See [docs/training.md](docs/training.md).

## Proposed design

### Output contract

```ts
type Question = {
  kind: "yes_no" | "either_or" | "multi_choice" | "open";  // open covers what, where, when, why, and how
  propose: boolean;          // "Want me to …?" and "Shall I …?", where yes means "do it"
  prompt: Span;              // the question text
  options: Span[];           // offered options, in order (empty for yes_no and open)
  default?: number;          // index of the option marked "(recommended)", "I'd go with…", and so on
  multiSelect: boolean;      // "and/or", "which ones"
};
parse(message) → Question[]  // a message can hold several questions
```

For yes/no questions, the UI synthesizes the options Yes and No. For open questions, it offers a text field, plus any candidates mentioned nearby ("Which branch, main or release/2.x?" counts as either_or).

### Token roles (the gpu-time "LABELS" analogue)

The implemented set is `O, Q_B, Q_I, OPT_B, OPT_I, REC` ([gq/labels.py](gq/labels.py)). `Q_B` marks where each question starts, which does the job of gpu-time's expression boundary. The compiler derives `kind`, `propose`, `default`, and `multiSelect` from the roles and the prompt text.

### Model

The model reuses gpu-time's recipe:
- hashed spelling features with no vocabulary
- a 5-tap convolution
- 1 to 2 bidirectional affine-scan layers with hidden size 32
- CRF transitions
- int6 QAT

Messages are longer than date phrases, so run the model only on the **tail of the message**: the last paragraph, plus the list directly above it. Replace code blocks with a placeholder token first.

### Data

1. **Synthetic prose from gold ask calls.** Render the 295 structured questions into prose templates ("Want me to A, B, or C?", numbered lists, "I'd go with A (recommended)"). The labels come from the slots, as in gpu-time.
2. **Weak labels from the 568 end-of-turn questions**, using the regex heuristics in `extract.py`, then hand-correct a gold set of about 200.
3. **Negatives.** Include status lists followed by "Want me to…?", where the list is not options. Also include rhetorical questions, questions inside code, and end-of-turn messages without a question.
4. **Splits by session or project**, never by string, to avoid leaking phrase families.

### Next steps

- [ ] Hand-label about 200 end-of-turn questions from `data/survey/sample.jsonl` into `gold/` (after scrubbing).
- [x] Write the prose renderer for ask-tool gold.
- [x] Port gpu-time's `model.py` and tokenizer with the new label set.
- [x] Build a compiler and oracle evaluation on gold tags.
- [ ] Add a validation split; shrink and quantize the model; port inference to TypeScript and WGSL.
