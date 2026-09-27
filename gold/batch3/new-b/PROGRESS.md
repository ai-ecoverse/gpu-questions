# Batch 3 new-b progress

Round 1 in progress. c0007 dropped because it requests a full name in a PII-review workflow; this source will be checked closely for sensitive content.

c0170 dropped: private chat excerpts contain named participants and message identifiers; unnecessary privacy risk.

c0186 dropped: a personal repository namespace appears in a proposed publish command. c0188 dropped: the reply asks for a live write token; placeholders are scrubbed, but the item is privacy-sensitive.
- Round 1 (c0000–c0228, 2026-09-24): 225 items from 9 datasets, 149 with a question / 76 negatives (40 hard), 113 boundary questions, 7 amb. Four items dropped for privacy or doubtful PII context (c0007, c0170, c0186, c0188). build 0 errors, validate 0 errors; 97 compiler differences, chiefly `propose`.

Correction after coordinator's held-out mirror report (2026-09-24): removed all 33 `introvoyz041/my-personal-codex-data` labels and all 37 queue / 290 candidate rows from that source. Rebuilt 228 items with 0 build or validation errors. Rechecked every extracted candidate dataset against 418 held-out session IDs (full ID, path basename, and `#` suffix); the mirror had 75 overlapping candidates across 26 IDs, and no other dataset overlapped. Corrected round 1 now has 192 items from 8 datasets, 149 questions / 43 negatives, 7 ambiguous. Further sources will be checked before labeling.

Ranga continuation: c0304/c0306/c0307 were duplicate IDs from one source session, so only one turn per ID was retained. c0312 dropped because the tail included a specific physical address; c0306 and c0307 had duplicate turn IDs. The queue and annotations have no duplicate IDs.

Global session-cap audit (2026-09-24): several `hf-coding-tools-traces` datasets re-use the same underlying session IDs, and two Ranga sessions exceeded three selected turns. Retained at most three labeled turns for each session across all datasets and removed 90 excess annotations/queue rows. Current rebuilt total: 262 items, 9 datasets, 0 build/validation errors. These sources are related re-publications; counts should not be interpreted as nine independent corpora.

Betterwright review: c0410 dropped because the reply discusses login credentials. No credential value was added to annotations or output.
Final source-exhaustion round (2026-09-24): 188 items from 12 datasets, 113 questions / 75 negatives, at least 69 boundary-question items, 60 hard negatives, and 4 ambiguous labels. The 96 reviewed negatives left out for the requested class balance are in `reviewed_unused.txt`. The 1,500-turn target was not met because newly available licensed sources were dominated by answer-only benchmark reports, repeated source sessions, or reuploads. Build and validation both report 0 errors; validation warns that one full-text span lies before the model's 256-token tail.
