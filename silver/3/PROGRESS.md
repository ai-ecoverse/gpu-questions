# Silver queue_3 labeling progress

| checkpoint | items | with Q | negative | hard neg (approx) | amb |
|---|---:|---:|---:|---:|---:|
| 150 | 150 | ~60 | ~90 | ~40 | ~5 |
| 300 | 300 | ~125 | ~175 | ~75 | ~12 |
| 525 | 525 | ~260 | ~265 | ~95 | ~18 |
| **772 (done)** | **772** | **380** | **392** | **120** | **23** |

Final build: `uv run python scripts/build_gold.py …` → **772 items, 0 span errors**.
Validate: duplicate-id noise from the queue + compiler diffs only (no span/whitespace hard failures beyond known duplicate session ids in source data).

Ambiguous keys: s3_0024, s3_0076, s3_0088, s3_0096, s3_0170, s3_0177, s3_0206, s3_0218, s3_0223, s3_0379, s3_0404, s3_0451, s3_0529, s3_0556, s3_0607, s3_0648, s3_0661, s3_0687, s3_0692, s3_0699, s3_0720, s3_0747, s3_0763.
