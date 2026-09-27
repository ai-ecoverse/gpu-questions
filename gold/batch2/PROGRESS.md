# Batch 2 labeling progress

One line per round: items labeled so far, datasets covered, question/negative split.

- Round 1 (queue b0000–b0254, 2026-09-24): 254 items, 64 datasets, 153 with a question / 101 negative (52 hard), 6 amb; b0179 skipped (tail starts mid-question). build 0 errors, validate 0 errors.
- Round 2 (queue b0255–b0494, 2026-09-24): 494 items, 66 datasets, 297 with a question / 197 negative (104 hard), 10 amb. build 0 errors, validate 0 errors.
- Round 3 (queue b0495–b0734, 2026-09-24): 734 items, 66 datasets, 438 with a question / 296 negative (159 hard), 21 amb. build 0 errors, validate 0 errors.
- Round 4 (queue b0735–b0974, 2026-09-24): 974 items, 66 datasets, 589 with a question / 385 negative (200 hard), 32 amb. dacorvo/* capped at 40 each from here. build 0 errors, validate 0 errors.
- Round 5 (queue b0975–b1214, 2026-09-24): 1214 items, 66 datasets, 739 with a question / 475 negative (238 hard), 36 amb. build 0 errors, validate 0 errors.
- Round 6 (queue b1215–b1399, 2026-09-24): 1358 items, 66 datasets, 829 with a question / 529 negative (264 hard), 38 amb. dacorvo/* reached their 40 caps (later dacorvo items skipped). build 0 errors, validate 0 errors.
- Round 7 (tail plan b1400–b1815: all `?` items plus 1 in 5 non-`?` items, 2026-09-24): 1601 items, 66 datasets, 1026 with a question / 575 negative (293 hard), 50 amb. b1446 dropped (demo credentials), b1811 dropped (leaked username is the subject). build 0 errors, validate 0 errors.
- Round 8 (tail plan positions 70–642 finished, 2026-09-24): 1995 items, 66 datasets, 1253 with a question / 742 negative (333 hard), 70 amb. b1879 dropped (same leaked username as b1811), b1971 skipped (tail starts mid-question), b2011 dropped (third-party OAuth client id). build 0 errors, validate 0 errors.
