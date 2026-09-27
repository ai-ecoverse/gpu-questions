# pairs-b progress (generator B)

| Boundary | Target | Done |
|---|---|---|
| open/yes_no | 250 | 250 |
| list_offered/background_list | 200 | 200 |
| propose/not | 150 | 150 |
| question/no_question | 100 | 100 |
| **total** | **700** | **700** |

## Checkpoints

- 2026-09-25: pb0001–pb0250 (open/yes_no) built+validated — 500 items, 0 errors, compiler kind diffs on some open info-requests.
- 2026-09-25: pb0251–pb0450 (list_offered/background_list) built+validated — 900 items, 0 errors; propose/multiSelect compiler diffs common on list menus.
- 2026-09-25: pb0451–pb0600 (propose/not) + pb0601–pb0700 (question/no_question) — **1400 items, 0 errors**, 208 compiler differences (`kind` 20, `propose` 179, `multiSelect` 9). Labels follow `gold/CONVENTIONS.md`; diffs treated as compiler limitations.
