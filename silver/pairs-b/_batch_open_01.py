"""Handcrafted open vs yes_no pairs pb0001–pb0050."""
from __future__ import annotations

PAIRS = []


def add(
    n,
    text_a,
    prompt_a,
    text_b,
    prompt_b,
    *,
    note_a,
    note_b,
    ka="o",
    kb="y",
    pa=False,
    pb=False,
    da="e",
    db="e",
    amb_a=False,
    amb_b=False,
    opts_a=None,
    opts_b=None,
):
    PAIRS.append(
        {
            "n": n,
            "boundary": "open/yes_no",
            "a": {
                "text": text_a,
                "difficulty": da,
                "amb": amb_a,
                "contrast": note_a,
                "note": f"pair pb{n:04d}: {note_a}",
                "qs": [{"kind": ka, "propose": pa, "prompt": prompt_a, "opts": opts_a or []}],
            },
            "b": {
                "text": text_b,
                "difficulty": db,
                "amb": amb_b,
                "contrast": note_b,
                "note": f"pair pb{n:04d}: {note_b}",
                "qs": [{"kind": kb, "propose": pb, "prompt": prompt_b, "opts": opts_b or []}],
            },
        }
    )


# --- git / CI ---
add(
    1,
    "The push failed on `main`. CI shows a red X on the lint job but I can't see the log from here.\n\nCould you share the failing log?",
    "Could you share the failing log?",
    "The push failed on `main`. CI shows a red X on the lint job but I can't see the log from here.\n\nCould you rerun it with `-v`?",
    "Could you rerun it with `-v`?",
    note_a="asks for log content -> open",
    note_b="asks user to rerun action -> yes_no",
)

add(
    2,
    "Merge conflict in `src/auth.ts` between `feature/login` and `main`. I need the conflicted hunks to propose a resolution.\n\nCan you paste the conflict markers from that file?",
    "Can you paste the conflict markers from that file?",
    "Merge conflict in `src/auth.ts` between `feature/login` and `main`. I need the conflicted hunks to propose a resolution.\n\nCan you check out `feature/login` and try the merge again?",
    "Can you check out `feature/login` and try the merge again?",
    note_a="asks for pasted content -> open",
    note_b="asks user to retry merge -> yes_no",
)

add(
    3,
    "Git says the remote rejected a non-fast-forward. Before I force-push anything, I want to know what landed.\n\nDo you remember which commit was on origin/main last night?",
    "Do you remember which commit was on origin/main last night?",
    "Git says the remote rejected a non-fast-forward. Before I force-push anything, I want to know what landed.\n\nDo you want me to fetch and show the divergent commits?",
    "Do you want me to fetch and show the divergent commits?",
    note_a="asks for recalled fact -> open",
    note_b="asks approval to fetch -> yes_no/propose",
    pb=True,
)

add(
    4,
    "Pre-commit failed on `ruff format`. The hook output was truncated in the terminal capture.\n\nWould you share the full hook output?",
    "Would you share the full hook output?",
    "Pre-commit failed on `ruff format`. The hook output was truncated in the terminal capture.\n\nWould you run `ruff format --check` yourself and confirm it fails the same way?",
    "Would you run `ruff format --check` yourself and confirm it fails the same way?",
    note_a="asks to share output -> open",
    note_b="asks user to run check -> yes_no",
)

add(
    5,
    "Branch `hotfix/timeout` exists locally but I don't see it on the remote listing I have.\n\nCould you tell me which remote you pushed it to?",
    "Could you tell me which remote you pushed it to?",
    "Branch `hotfix/timeout` exists locally but I don't see it on the remote listing I have.\n\nCould you push it with `git push -u origin hotfix/timeout`?",
    "Could you push it with `git push -u origin hotfix/timeout`?",
    note_a="asks which remote (info) -> open",
    note_b="asks user to push -> yes_no",
)

# --- tests ---
add(
    6,
    "Three tests failed in `test_billing.py`. The assertion messages look like fixture drift.\n\nCan you paste the failure block for `test_invoice_rounding`?",
    "Can you paste the failure block for `test_invoice_rounding`?",
    "Three tests failed in `test_billing.py`. The assertion messages look like fixture drift.\n\nCan you re-run just `test_invoice_rounding` with `-vv`?",
    "Can you re-run just `test_invoice_rounding` with `-vv`?",
    note_a="asks for failure text -> open",
    note_b="asks user to re-run test -> yes_no",
)

add(
    7,
    "Pytest is collecting 0 tests from `tests/unit/`. That usually means a naming or path issue.\n\nWhat does `pytest --collect-only -q` print on your machine?",
    "What does `pytest --collect-only -q` print on your machine?",
    "Pytest is collecting 0 tests from `tests/unit/`. That usually means a naming or path issue.\n\nCan you try running `pytest --collect-only -q` to see if you get more info?",
    "Can you try running `pytest --collect-only -q` to see if you get more info?",
    note_a="asks what it prints (info) -> open",
    note_b="asks to try running (action) -> yes_no",
    da="m",
    db="m",
)

add(
    8,
    "Flaky timeout on `test_websocket_reconnect`. I've only seen it in CI.\n\nCould you share the last CI run URL where it failed?",
    "Could you share the last CI run URL where it failed?",
    "Flaky timeout on `test_websocket_reconnect`. I've only seen it in CI.\n\nCould you trigger a re-run of the failed job?",
    "Could you trigger a re-run of the failed job?",
    note_a="asks for URL -> open",
    note_b="asks to re-run job -> yes_no",
)

add(
    9,
    "Coverage dropped below the gate on `src/parsers/`. I need the uncovered lines list.\n\nWould you paste the coverage report for that package?",
    "Would you paste the coverage report for that package?",
    "Coverage dropped below the gate on `src/parsers/`. I need the uncovered lines list.\n\nWould you open the HTML coverage report and skim the red lines?",
    "Would you open the HTML coverage report and skim the red lines?",
    note_a="asks for pasted report -> open",
    note_b="asks user to open/skim -> yes_no",
)

add(
    10,
    "The snapshot test updated 14 files. Before I accept them I want to know intent.\n\nWhich snapshots did you expect to change?",
    "Which snapshots did you expect to change?",
    "The snapshot test updated 14 files. Before I accept them I want to know intent.\n\nShould I accept all 14 snapshot updates?",
    "Should I accept all 14 snapshot updates?",
    note_a="asks which (info) -> open",
    note_b="asks approval -> yes_no/propose",
    pb=True,
)

# --- UI / frontend ---
add(
    11,
    "The modal still clips on mobile at 375px. I can't reproduce the exact layout without your viewport.\n\nCould you describe what looks wrong on the small screen?",
    "Could you describe what looks wrong on the small screen?",
    "The modal still clips on mobile at 375px. I can't reproduce the exact layout without your viewport.\n\nCould you hard-refresh and check again at 375px?",
    "Could you hard-refresh and check again at 375px?",
    note_a="asks for description -> open",
    note_b="asks user to refresh/check -> yes_no",
)

add(
    12,
    "Button label still says \"Save\" in the screenshot you mentioned, but my build shows \"Done\".\n\nWhich build are you looking at?",
    "Which build are you looking at?",
    "Button label still says \"Save\" in the screenshot you mentioned, but my build shows \"Done\".\n\nWant me to bump the cache-bust query on the asset?",
    "Want me to bump the cache-bust query on the asset?",
    note_a="asks which build -> open",
    note_b="offers agent action -> yes_no/propose",
    pb=True,
)

add(
    13,
    "Focus ring disappears after the first Tab press in Safari. Chromium looks fine here.\n\nCan you share a screen recording of the Tab sequence?",
    "Can you share a screen recording of the Tab sequence?",
    "Focus ring disappears after the first Tab press in Safari. Chromium looks fine here.\n\nCan you try the same Tab sequence in Safari Technology Preview?",
    "Can you try the same Tab sequence in Safari Technology Preview?",
    note_a="asks for recording -> open",
    note_b="asks user to try STP -> yes_no",
)

add(
    14,
    "The design token `--color-accent` resolves differently in Storybook vs the app shell.\n\nWhat value do you see in DevTools for that variable on the button?",
    "What value do you see in DevTools for that variable on the button?",
    "The design token `--color-accent` resolves differently in Storybook vs the app shell.\n\nCan you try inspecting the button in DevTools to see if you get more info?",
    "Can you try inspecting the button in DevTools to see if you get more info?",
    note_a="asks what value (info) -> open",
    note_b="asks to try inspecting (action) -> yes_no",
    da="m",
    db="m",
)

add(
    15,
    "Dark mode flash on first paint — I suspect `localStorage` is read after hydration.\n\nWhat does the first paint look like before the theme applies?",
    "What does the first paint look like before the theme applies?",
    "Dark mode flash on first paint — I suspect `localStorage` is read after hydration.\n\nWant me to move the theme script into `index.html`?",
    "Want me to move the theme script into `index.html`?",
    note_a="asks for visual description -> open",
    note_b="offers fix -> yes_no/propose",
    pb=True,
)

# --- data / infra ---
add(
    16,
    "The nightly ETL job wrote 0 rows to `events_daily`. Schema looks unchanged.\n\nCould you share the job's stdout from last night?",
    "Could you share the job's stdout from last night?",
    "The nightly ETL job wrote 0 rows to `events_daily`. Schema looks unchanged.\n\nCould you kick the job manually once?",
    "Could you kick the job manually once?",
    note_a="asks for stdout -> open",
    note_b="asks to kick job -> yes_no",
)

add(
    17,
    "Redis memory is at 91% on `cache-2`. Evictions started an hour ago.\n\nWhat is the current `used_memory_human` value?",
    "What is the current `used_memory_human` value?",
    "Redis memory is at 91% on `cache-2`. Evictions started an hour ago.\n\nCan you flush the `session:*` keys on `cache-2`?",
    "Can you flush the `session:*` keys on `cache-2`?",
    note_a="asks for metric value -> open",
    note_b="asks user to flush keys -> yes_no",
)

add(
    18,
    "Postgres connection pool exhausted during the load test. I need the wait-queue depth.\n\nWould you paste the output of `SELECT * FROM pg_stat_activity`?",
    "Would you paste the output of `SELECT * FROM pg_stat_activity`?",
    "Postgres connection pool exhausted during the load test. I need the wait-queue depth.\n\nWould you restart the API pods to clear stuck connections?",
    "Would you restart the API pods to clear stuck connections?",
    note_a="asks for query paste -> open",
    note_b="asks to restart pods -> yes_no",
)

add(
    19,
    "S3 sync reported `AccessDenied` on `s3://proj-artifacts/builds/`. Credentials may be stale.\n\nWhich IAM role is the runner assuming right now?",
    "Which IAM role is the runner assuming right now?",
    "S3 sync reported `AccessDenied` on `s3://proj-artifacts/builds/`. Credentials may be stale.\n\nCan you refresh the OIDC token on the runner and retry?",
    "Can you refresh the OIDC token on the runner and retry?",
    note_a="asks which role -> open",
    note_b="asks to refresh/retry -> yes_no",
)

add(
    20,
    "Kubernetes rollout of `api-gateway` is stuck at 1/3 ready.\n\nCould you share `kubectl describe pod` for one of the pending pods?",
    "Could you share `kubectl describe pod` for one of the pending pods?",
    "Kubernetes rollout of `api-gateway` is stuck at 1/3 ready.\n\nCould you delete the pending pods so the rollout recreates them?",
    "Could you delete the pending pods so the rollout recreates them?",
    note_a="asks for describe output -> open",
    note_b="asks to delete pods -> yes_no",
)

# --- docs / refactors ---
add(
    21,
    "The README still documents the old `make serve` target; we renamed it to `make dev`.\n\nWhich sections still mention `make serve`?",
    "Which sections still mention `make serve`?",
    "The README still documents the old `make serve` target; we renamed it to `make dev`.\n\nWant me to sweep the README for `make serve`?",
    "Want me to sweep the README for `make serve`?",
    note_a="asks which sections -> open",
    note_b="offers sweep -> yes_no/propose",
    pb=True,
)

add(
    22,
    "I'm about to split `utils.py` into `paths.py` and `timefmt.py`. Call sites are unclear from the index alone.\n\nCan you list the files that import from `utils` today?",
    "Can you list the files that import from `utils` today?",
    "I'm about to split `utils.py` into `paths.py` and `timefmt.py`. Call sites are unclear from the index alone.\n\nCan you try grepping for `from utils import` on your side?",
    "Can you try grepping for `from utils import` on your side?",
    note_a="asks for list (info) -> open",
    note_b="asks user to try grep -> yes_no",
)

add(
    23,
    "API versioning note in `CHANGELOG.md` is missing the breaking change from last Tuesday.\n\nWhat breaking change should we document there?",
    "What breaking change should we document there?",
    "API versioning note in `CHANGELOG.md` is missing the breaking change from last Tuesday.\n\nShall I draft a changelog entry for last Tuesday's break?",
    "Shall I draft a changelog entry for last Tuesday's break?",
    note_a="asks what to document -> open",
    note_b="offers draft -> yes_no/propose",
    pb=True,
)

add(
    24,
    "The migration guide still references `v1/widgets`. We need the replacement path.\n\nWhat should readers use instead of `v1/widgets`?",
    "What should readers use instead of `v1/widgets`?",
    "The migration guide still references `v1/widgets`. We need the replacement path.\n\nWant me to replace `v1/widgets` with `v2/widgets` throughout the guide?",
    "Want me to replace `v1/widgets` with `v2/widgets` throughout the guide?",
    note_a="asks for replacement path -> open",
    note_b="offers replace -> yes_no/propose",
    pb=True,
)

add(
    25,
    "Comment in `Parser.tokenize` says \"see issue 482\" but that ticket is closed as unrelated.\n\nWhich issue did you mean?",
    "Which issue did you mean?",
    "Comment in `Parser.tokenize` says \"see issue 482\" but that ticket is closed as unrelated.\n\nWant me to delete that stale comment?",
    "Want me to delete that stale comment?",
    note_a="asks which issue -> open",
    note_b="offers delete -> yes_no/propose",
    pb=True,
)

# --- longer status + question ---
add(
    26,
    """Status after the morning pass:

- Fixed null check in `loadConfig`
- Added regression test `test_missing_env`
- Left `WARN` logs noisy on purpose

The remaining failure is intermittent and only shows up under load.

Could you share the load-test command you used last time?""",
    "Could you share the load-test command you used last time?",
    """Status after the morning pass:

- Fixed null check in `loadConfig`
- Added regression test `test_missing_env`
- Left `WARN` logs noisy on purpose

The remaining failure is intermittent and only shows up under load.

Could you re-run that load test once more?""",
    "Could you re-run that load test once more?",
    note_a="asks for command text -> open",
    note_b="asks to re-run -> yes_no",
)

add(
    27,
    """I pulled `origin/main` and rebuilt. Summary:

1. Typecheck clean
2. Unit tests green (412)
3. E2E still blocked on the staging cookie

What is the staging cookie name I should set locally?""",
    "What is the staging cookie name I should set locally?",
    """I pulled `origin/main` and rebuilt. Summary:

1. Typecheck clean
2. Unit tests green (412)
3. E2E still blocked on the staging cookie

Can you set the staging cookie in your browser and retry the E2E?""",
    "Can you set the staging cookie in your browser and retry the E2E?",
    note_a="asks for cookie name -> open",
    note_b="asks user to set cookie/retry -> yes_no",
)

add(
    28,
    """Refactor of the billing client is in a draft PR:

- Extracted `RetryPolicy`
- Moved currency helpers
- Left the old facade as a thin wrapper

Which review comments are blockers for you?""",
    "Which review comments are blockers for you?",
    """Refactor of the billing client is in a draft PR:

- Extracted `RetryPolicy`
- Moved currency helpers
- Left the old facade as a thin wrapper

Want me to mark the draft ready for review?""",
    "Want me to mark the draft ready for review?",
    note_a="asks which comments -> open",
    note_b="offers mark ready -> yes_no/propose",
    pb=True,
)

add(
    29,
    """Docker image build failed at the `apt-get` layer:

[CODE]
E: Unable to locate package libfoo-dev
[CODE]

Which Ubuntu release is the base image supposed to target?""",
    "Which Ubuntu release is the base image supposed to target?",
    """Docker image build failed at the `apt-get` layer:

[CODE]
E: Unable to locate package libfoo-dev
[CODE]

Can you retry the build with `--no-cache`?""",
    "Can you retry the build with `--no-cache`?",
    note_a="asks which release -> open",
    note_b="asks to retry build -> yes_no",
)

add(
    30,
    """Feature flag `payments.v2` is on in staging, off in prod. The dual-write path looks correct in code review.

Where is the flag configured for production?""",
    "Where is the flag configured for production?",
    """Feature flag `payments.v2` is on in staging, off in prod. The dual-write path looks correct in code review.

Want me to flip `payments.v2` on in production?""",
    "Want me to flip `payments.v2` on in production?",
    note_a="asks where configured -> open",
    note_b="offers flip flag -> yes_no/propose",
    pb=True,
)

# --- Could you / Would you share vs try ---
add(
    31,
    "Stack overflow in the recursive descent parser on a 2k-line input. I need the truncated stack.\n\nCould you share the top 30 frames?",
    "Could you share the top 30 frames?",
    "Stack overflow in the recursive descent parser on a 2k-line input. I need the truncated stack.\n\nCould you try feeding it a 100-line input to see if you get more info?",
    "Could you try feeding it a 100-line input to see if you get more info?",
    note_a="asks to share frames -> open",
    note_b="asks to try smaller input -> yes_no",
    da="m",
    db="m",
)

add(
    32,
    "npm install fails with `ERESOLVE` on `eslint-plugin-react`.\n\nWould you paste your `npm ls eslint-plugin-react` output?",
    "Would you paste your `npm ls eslint-plugin-react` output?",
    "npm install fails with `ERESOLVE` on `eslint-plugin-react`.\n\nWould you try `npm install --legacy-peer-deps`?",
    "Would you try `npm install --legacy-peer-deps`?",
    note_a="asks for paste -> open",
    note_b="asks to try install flag -> yes_no",
)

add(
    33,
    "TypeScript reports `TS2589` deeply nested on the zod schema. The error cuts off mid-path.\n\nCan you share the full `tsc` diagnostic for that file?",
    "Can you share the full `tsc` diagnostic for that file?",
    "TypeScript reports `TS2589` deeply nested on the zod schema. The error cuts off mid-path.\n\nCan you bump `skipLibCheck` and rebuild once?",
    "Can you bump `skipLibCheck` and rebuild once?",
    note_a="asks for diagnostic -> open",
    note_b="asks to bump/rebuild -> yes_no",
)

add(
    34,
    "The webhook signature verification fails only for Stripe's `invoice.paid` events.\n\nWhat raw body bytes are you hashing on your side?",
    "What raw body bytes are you hashing on your side?",
    "The webhook signature verification fails only for Stripe's `invoice.paid` events.\n\nCan you disable signature checks temporarily on staging?",
    "Can you disable signature checks temporarily on staging?",
    note_a="asks what bytes -> open",
    note_b="asks to disable checks -> yes_no",
    da="h",
    db="e",
)

add(
    35,
    "CSV import rejected row 482 with a vague `invalid date`.\n\nCould you show me the exact cell value from that row?",
    "Could you show me the exact cell value from that row?",
    "CSV import rejected row 482 with a vague `invalid date`.\n\nCould you re-export the CSV with ISO dates and import again?",
    "Could you re-export the CSV with ISO dates and import again?",
    note_a="asks for cell value -> open",
    note_b="asks to re-export/import -> yes_no",
)

# --- terse CLI agent style ---
add(
    36,
    "Done. Lint clean. One flake left in CI.\n\nWhat's the flake name?",
    "What's the flake name?",
    "Done. Lint clean. One flake left in CI.\n\nWant me to quarantine it?",
    "Want me to quarantine it?",
    note_a="asks flake name -> open",
    note_b="offers quarantine -> yes_no/propose",
    pb=True,
)

add(
    37,
    "Rebased onto main. Conflicts resolved in `Cargo.lock` only.\n\nWhich crate version did you intend for `serde`?",
    "Which crate version did you intend for `serde`?",
    "Rebased onto main. Conflicts resolved in `Cargo.lock` only.\n\nShall I run `cargo update -p serde`?",
    "Shall I run `cargo update -p serde`?",
    note_a="asks intended version -> open",
    note_b="offers cargo update -> yes_no/propose",
    pb=True,
)

add(
    38,
    "Migrated the SQLite dump. 12k rows in, 11.8k out — some dropped.\n\nWhich rows are allowed to drop?",
    "Which rows are allowed to drop?",
    "Migrated the SQLite dump. 12k rows in, 11.8k out — some dropped.\n\nWant me to abort and restore the backup?",
    "Want me to abort and restore the backup?",
    note_a="asks which rows -> open",
    note_b="offers abort/restore -> yes_no/propose",
    pb=True,
)

add(
    39,
    "Patched the race in the worker pool. Need a second pair of eyes on the barrier.\n\nWhat still looks wrong in `worker.rs`?",
    "What still looks wrong in `worker.rs`?",
    "Patched the race in the worker pool. Need a second pair of eyes on the barrier.\n\nWant me to add a stress test for the barrier?",
    "Want me to add a stress test for the barrier?",
    note_a="asks what looks wrong -> open",
    note_b="offers stress test -> yes_no/propose",
    pb=True,
)

add(
    40,
    "Cut a release branch `release/1.4.0`. Changelog draft is empty.\n\nWhat should the highlight bullets say?",
    "What should the highlight bullets say?",
    "Cut a release branch `release/1.4.0`. Changelog draft is empty.\n\nShall I draft highlight bullets from the merged PRs?",
    "Shall I draft highlight bullets from the merged PRs?",
    note_a="asks what bullets should say -> open",
    note_b="offers draft -> yes_no/propose",
    pb=True,
)

# --- chatty assistant + markdown ---
add(
    41,
    """I've walked through the auth middleware and the session store. A few things still unclear:

- How long sessions should live
- Whether refresh tokens rotate
- Where logout should revoke

**Could you clarify the intended session lifetime?**""",
    "Could you clarify the intended session lifetime?",
    """I've walked through the auth middleware and the session store. A few things still unclear:

- How long sessions should live
- Whether refresh tokens rotate
- Where logout should revoke

**Could you try logging out on two devices to see if you get more info?**""",
    "Could you try logging out on two devices to see if you get more info?",
    note_a="asks to clarify lifetime -> open",
    note_b="asks to try logout experiment -> yes_no",
    da="m",
    db="m",
)

add(
    42,
    """Here's what I changed in the PR:

| File | Change |
|------|--------|
| `api/routes.ts` | rate limit headers |
| `api/metrics.ts` | histogram buckets |

I still don't know your SLO target for p99.

What p99 latency are we aiming for?""",
    "What p99 latency are we aiming for?",
    """Here's what I changed in the PR:

| File | Change |
|------|--------|
| `api/routes.ts` | rate limit headers |
| `api/metrics.ts` | histogram buckets |

I still don't know your SLO target for p99.

Want me to add a p99 alert at 300ms as a starting point?""",
    "Want me to add a p99 alert at 300ms as a starting point?",
    note_a="asks for SLO number -> open",
    note_b="offers alert -> yes_no/propose",
    pb=True,
)

add(
    43,
    """I can't reproduce the CORS failure locally. Staging returns:

[CODE]
Access-Control-Allow-Origin: null
[CODE]

Which origin header is your browser sending?""",
    "Which origin header is your browser sending?",
    """I can't reproduce the CORS failure locally. Staging returns:

[CODE]
Access-Control-Allow-Origin: null
[CODE]

Can you retry the request from an incognito window?""",
    "Can you retry the request from an incognito window?",
    note_a="asks which origin -> open",
    note_b="asks to retry incognito -> yes_no",
)

add(
    44,
    """Docs build warning:

> [WARNING] Duplicate label `install` on lines 40 and 118

Which of those `install` labels should stay?""",
    "Which of those `install` labels should stay?",
    """Docs build warning:

> [WARNING] Duplicate label `install` on lines 40 and 118

Want me to rename the second `install` label?""",
    "Want me to rename the second `install` label?",
    note_a="asks which label stays -> open",
    note_b="offers rename -> yes_no/propose",
    pb=True,
)

add(
    45,
    """GraphQL schema drift: client expects `User.avatarUrl`, server still has `User.avatar`.

What field name should be canonical going forward?""",
    "What field name should be canonical going forward?",
    """GraphQL schema drift: client expects `User.avatarUrl`, server still has `User.avatar`.

Want me to add a deprecated alias so both work?""",
    "Want me to add a deprecated alias so both work?",
    note_a="asks canonical name -> open",
    note_b="offers alias -> yes_no/propose",
    pb=True,
)

# --- double-check / verify patterns ---
add(
    46,
    "The ID in the ticket doesn't match any row I can find.\n\nCould you double-check the id or provide more details?",
    "Could you double-check the id or provide more details?",
    "The ID in the ticket doesn't match any row I can find.\n\nCould you double-check the id and try again?",
    "Could you double-check the id and try again?",
    note_a="double-check or provide details -> open (info arms)",
    note_b="double-check and try again -> yes_no",
    da="m",
    db="e",
)

add(
    47,
    "Build succeeded on my machine with Node 20; CI uses Node 18.\n\nWhat Node version is pinned in your `.nvmrc`?",
    "What Node version is pinned in your `.nvmrc`?",
    "Build succeeded on my machine with Node 20; CI uses Node 18.\n\nCan you switch to Node 20 and rebuild?",
    "Can you switch to Node 20 and rebuild?",
    note_a="asks nvmrc version -> open",
    note_b="asks to switch/rebuild -> yes_no",
)

add(
    48,
    "Email preview renders fine in Litmus but Gmail clips the footer.\n\nHow tall is the footer in the design spec?",
    "How tall is the footer in the design spec?",
    "Email preview renders fine in Litmus but Gmail clips the footer.\n\nCan you send yourself a test email and scroll to the footer?",
    "Can you send yourself a test email and scroll to the footer?",
    note_a="asks for height -> open",
    note_b="asks to send/scroll -> yes_no",
)

add(
    49,
    "The cron expression `0 */3 * * *` may not match what ops expected.\n\nWhat cadence did ops request?",
    "What cadence did ops request?",
    "The cron expression `0 */3 * * *` may not match what ops expected.\n\nWant me to change it to hourly?",
    "Want me to change it to hourly?",
    note_a="asks what cadence -> open",
    note_b="offers change -> yes_no/propose",
    pb=True,
)

add(
    50,
    "I'd like to confirm the product name before the rename lands in strings and docs.\n\nWhat should we call the feature in the UI?",
    "What should we call the feature in the UI?",
    "I'd like to confirm the product name before the rename lands in strings and docs.\n\nWant me to rename it to **Pulse** everywhere?",
    "Want me to rename it to **Pulse** everywhere?",
    note_a="asks for name -> open",
    note_b="offers rename -> yes_no/propose",
    pb=True,
)

assert len(PAIRS) == 50
assert [p["n"] for p in PAIRS] == list(range(1, 51))
