# Silver queue 4 labeling progress

| checkpoint | items | with Q | neg | hard neg | amb | notes |
|---|---:|---:|---:|---:|---:|---|
| 150 | 150 | 80 | 70 | 30 | 2 | build+validate clean; s4_0006 privacy drop |
| 300 | 300 | 152 | 148 | 69 | 7 | build 0 span errors |
| 450 | 450 | — | — | — | — | build 0 span errors |
| 600 | 600 | 297 | 303 | 148 | 12 | build 0 span errors |
| 772 | 772 | 387 | 385 | 178 | 15 | complete; build 0 span errors |

## Final (772 / 772)

- With questions: **387**
- Negatives: **385** (hard: **178**)
- Ambiguous: **15**
- Privacy drops: **1** (`s4_0006`)
- Question records: **450**
- Proposals: **165**
- Kind distribution: open 202, yes_no 137, either_or 70, multi_choice 41

`validate_gold.py` reports duplicate-id errors from the queue itself (same session/turn duplicated across items), not span failures.
