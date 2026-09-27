# Silver pairs-a progress (generator A)

Validation command after each checkpoint:

```
uv run python scripts/build_gold.py --queue silver/pairs-a/queue.jsonl --ann silver/pairs-a/annotations.txt --out silver/pairs-a/labeled.jsonl
uv run python scripts/validate_gold.py silver/pairs-a/labeled.jsonl --quiet
```

| pairs so far | yes_no/either_or | either_or/multi_choice | examples/options | escape_hatch | validate |
|---|---|---|---|---|---|
| 100 (pa0001–0100) | 100 | 0 | 0 | 0 | 0 hard errors |
| 200 (pa0001–0200) | 200 | 0 | 0 | 0 | 0 hard errors |
| 300 (pa0001–0300) | 300 | 0 | 0 | 0 | 0 hard errors |
| 450 (pa0001–0450) | 450 | 0 | 0 | 0 | 0 hard errors |
| 600 (pa0001–0600) | 450 | 150 | 0 | 0 | 0 hard errors |
| 700 (pa0001–0700) | 450 | 150 | 100 | 0 | 0 hard errors |
| **800 (pa0001–0800)** | **450** | **150** | **100** | **100** | **0 hard errors**; remaining diffs are compiler limitations (propose/kind on e.g.-open, terse prompt edges, `V__` option) |

## Final totals (generator A)

- 800 pairs / 1600 messages
- Keys `pa0001a`/`pa0001b` … `pa0800a`/`pa0800b`
- Kind counts (across 1600 messages' expected questions): either_or 724, yes_no 500, multi_choice 276, open 100
- Sources: `_batch_yn_eo_*.py`, `_batch_eo_mc_451_600.py`, `_batch_ex_opt_601_700.py`, `_batch_esc_701_800.py`
- Rebuild: `uv run python silver/pairs-a/_rebuild.py`
- Artifacts: `queue.jsonl`, `annotations.txt`, `labeled.jsonl`
