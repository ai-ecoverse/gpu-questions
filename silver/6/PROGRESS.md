# Silver queue_6 labeling progress

| checkpoint | items | with Q | neg | hard neg | amb | notes |
|---|---:|---:|---:|---:|---:|---|
| 150 | 150 | 64 | 86 | ~35 | 8 | build+validate clean |
| 300 | 300 | ~130 | ~170 | ~70 | ~14 | build+validate clean |
| 450 | 450 | ~200 | ~250 | ~90 | ~20 | build clean; validate duplicate-id source warnings |
| 771 (done) | 771 | 359 | 412 | 105 | 27 | build 0 span errors; 0 privacy drops |

## Final counts (from labeled.jsonl)

- Items: 771
- With ≥1 question: 359
- Negatives: 412 (105 hard via note)
- Ambiguous: 27
- Privacy drops: 0
- Question records by kind: open 204, yes_no 103, either_or 57, multi_choice 55
- Proposals: 150
- multiSelect: 0
