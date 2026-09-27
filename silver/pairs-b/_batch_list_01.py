"""Handcrafted list_offered vs background_list pairs pb0251–pb0350."""
from __future__ import annotations

PAIRS = []


def add(
    n,
    text_a,
    prompt_a,
    opts_a,
    text_b,
    prompt_b,
    *,
    note_a,
    note_b,
    ka="m",
    kb="y",
    pa=False,
    pb=True,
    da="e",
    db="e",
    ms_a=False,
    amb_a=False,
    amb_b=False,
):
    PAIRS.append(
        {
            "n": n,
            "boundary": "list_offered/background_list",
            "a": {
                "text": text_a,
                "difficulty": da,
                "amb": amb_a,
                "contrast": note_a,
                "note": f"pair pb{n:04d}: {note_a}",
                "qs": [
                    {
                        "kind": ka,
                        "propose": pa,
                        "multi": ms_a,
                        "prompt": prompt_a,
                        "opts": opts_a,
                    }
                ],
            },
            "b": {
                "text": text_b,
                "difficulty": db,
                "amb": amb_b,
                "contrast": note_b,
                "note": f"pair pb{n:04d}: {note_b}",
                "qs": [{"kind": kb, "propose": pb, "prompt": prompt_b, "opts": []}],
            },
        }
    )


# --- git / branches ---
add(
    251,
    "Local `feature/cache-headers` is rebased and tests are green. I can land it a few ways:\n\n1. **Squash** into one commit on `main`\n2. **Cherry-pick** just the header fix\n3. **Open a PR** and let review decide\n\nWhich of these should I do?",
    "Which of these should I do?",
    ["Squash", "Cherry-pick", "Open a PR"],
    "Local `feature/cache-headers` is rebased and tests are green. Current plan on my side:\n\n1. **Squash** into one commit on `main`\n2. **Cherry-pick** just the header fix\n3. **Open a PR** and let review decide\n\nWant me to push the branch now?",
    "Want me to push the branch now?",
    note_a="numbered menu + which-of -> multi_choice from list",
    note_b="same steps as status plan; push proposal not a list pick",
    pa=True,
)

add(
    252,
    "Remote history diverged after the rebase. Two clean options:\n\n- **Force-with-lease** push to update the PR branch\n- **New branch** `feature/cache-headers-v2` and abandon the old remote\n\nWhich route do you prefer?",
    "Which route do you prefer?",
    ["Force-with-lease", "New branch"],
    "Remote history diverged after the rebase. Likely paths I see:\n\n- **Force-with-lease** push to update the PR branch\n- **New branch** `feature/cache-headers-v2` and abandon the old remote\n\nShall I fetch and show the divergent commits first?",
    "Shall I fetch and show the divergent commits first?",
    note_a="two-item fork -> either_or selects from list",
    note_b="inventory of paths; fetch proposal does not pick a list item",
    ka="e",
    pa=False,
)

add(
    253,
    "Merge conflict scan on `src/auth.ts` turned up three hunks:\n\n- **Imports** — both sides added JWT helpers\n- **Middleware** — timeout default differs\n- **Tests** — fixture name collision\n\nWhich hunk should I resolve first?",
    "Which hunk should I resolve first?",
    ["Imports", "Middleware", "Tests"],
    "Merge conflict scan on `src/auth.ts` turned up three hunks:\n\n- **Imports** — both sides added JWT helpers\n- **Middleware** — timeout default differs\n- **Tests** — fixture name collision\n\nWant me to start with the imports hunk?",
    "Want me to start with the imports hunk?",
    note_a="conflict menu -> multi_choice picks a hunk",
    note_b="same findings list; yes_no proposes one item without menu",
)

add(
    254,
    "Stash stack is getting deep. I can:\n\n- **Pop** the top stash onto current branch\n- **Apply** without dropping\n- **Drop** the WIP snapshot from Tuesday\n\nWhich stash action should I take?",
    "Which stash action should I take?",
    ["Pop", "Apply", "Drop"],
    "Stash stack is getting deep. Notes from `git stash list`:\n\n- **Pop** the top stash onto current branch\n- **Apply** without dropping\n- **Drop** the WIP snapshot from Tuesday\n\nReady for me to pop the latest stash?",
    "Ready for me to pop the latest stash?",
    note_a="action menu -> multi_choice",
    note_b="stash options as background; continue proposes pop",
    pa=True,
)

add(
    255,
    "Tag cut for `v2.4.0` is staged. Pick the release artifact:\n\n1. **Annotated tag** with signed message\n2. **Lightweight tag** on HEAD\n\nWhich should I create?",
    "Which should I create?",
    ["Annotated tag", "Lightweight tag"],
    "Tag cut for `v2.4.0` is staged. Release checklist:\n\n1. **Annotated tag** with signed message\n2. **Lightweight tag** on HEAD\n\nShall I create the annotated tag?",
    "Shall I create the annotated tag?",
    note_a="two release types -> either_or",
    note_b="checklist inventory; annotated tag proposal",
    ka="e",
    pa=True,
)

add(
    256,
    "Submodule pointers drifted on `vendor/libyaml`. Remediation options:\n\n- **Pin** to the commit CI expects\n- **Update** to latest upstream\n- **Remove** submodule and vendor the tarball\n\nWhich fix should I apply?",
    "Which fix should I apply?",
    ["Pin", "Update", "Remove"],
    "Submodule pointers drifted on `vendor/libyaml`. Remediation options on the board:\n\n- **Pin** to the commit CI expects\n- **Update** to latest upstream\n- **Remove** submodule and vendor the tarball\n\nWant me to pin to the CI commit?",
    "Want me to pin to the CI commit?",
    note_a="three fixes offered -> multi_choice",
    note_b="same options as plan; pin is proposed not selected",
    pa=True,
)

add(
    257,
    "`.gitattributes` LFS rules may be wrong for `*.bin`. I can:\n\n- **Audit** tracked blobs over 50MB\n- **Migrate** existing blobs to LFS\n- **Add** a `.lfsconfig` with remote URL\n\nWhich should I run first?",
    "Which should I run first?",
    ["Audit", "Migrate", "Add"],
    "`.gitattributes` LFS rules may be wrong for `*.bin`. Investigation so far:\n\n- **Audit** tracked blobs over 50MB\n- **Migrate** existing blobs to LFS\n- **Add** a `.lfsconfig` with remote URL\n\nWant me to run the audit?",
    "Want me to run the audit?",
    note_a="ordered task menu -> multi_choice",
    note_b="findings as background; audit proposal",
    pa=True,
)

add(
    258,
    "Bisect landed on `9f3a2c1`. Two ways to finish:\n\n- **Revert** that commit on `main`\n- **Fix forward** with a targeted patch\n\nWhich do you want?",
    "Which do you want?",
    ["Revert", "Fix forward"],
    "Bisect landed on `9f3a2c1`. Remaining work:\n\n- **Revert** that commit on `main`\n- **Fix forward** with a targeted patch\n\nShall I revert it on `main`?",
    "Shall I revert it on `main`?",
    note_a="revert vs fix -> either_or from list",
    note_b="status list; revert proposal",
    ka="e",
    pa=True,
)

add(
    259,
    "Hooks blocked the commit. Next steps I can take:\n\n1. **Fix** formatting in `cli/main.py`\n2. **Skip** hooks just this once (not recommended)\n3. **Disable** the noisy rule in `.pre-commit-config.yaml`\n\nWhich should I do?",
    "Which should I do?",
    ["Fix", "Skip", "Disable"],
    "Hooks blocked the commit. Next steps on the list:\n\n1. **Fix** formatting in `cli/main.py`\n2. **Skip** hooks just this once (not recommended)\n3. **Disable** the noisy rule in `.pre-commit-config.yaml`\n\nWant me to fix formatting in `cli/main.py`?",
    "Want me to fix formatting in `cli/main.py`?",
    note_a="hook recovery menu -> multi_choice",
    note_b="same steps as inventory; fix proposed",
    pa=True,
)

add(
    260,
    "Fork sync is behind upstream by 41 commits. Strategies:\n\n- **Merge** `upstream/main` into our default branch\n- **Rebase** our feature branches onto upstream\n\nWhich sync strategy should I use?",
    "Which sync strategy should I use?",
    ["Merge", "Rebase"],
    "Fork sync is behind upstream by 41 commits. Strategies under review:\n\n- **Merge** `upstream/main` into our default branch\n- **Rebase** our feature branches onto upstream\n\nWant me to merge upstream/main first?",
    "Want me to merge upstream/main first?",
    note_a="two sync strategies -> either_or",
    note_b="strategy inventory; merge proposed",
    ka="e",
    pa=True,
)

# --- CI / pipelines ---
add(
    261,
    "CI matrix is red on three jobs:\n\n- **lint** — ruff import order\n- **test** — flaky websocket case\n- **build** — missing `VITE_API_URL`\n\nWhich job should I triage first?",
    "Which job should I triage first?",
    ["lint", "test", "build"],
    "CI matrix is red on three jobs:\n\n- **lint** — ruff import order\n- **test** — flaky websocket case\n- **build** — missing `VITE_API_URL`\n\nWant me to open the lint log?",
    "Want me to open the lint log?",
    note_a="job menu -> multi_choice",
    note_b="failure inventory; lint log proposal",
)

add(
    262,
    "Workflow dispatch inputs are ambiguous. I can wire:\n\n1. **Staging** deploy on `main` push\n2. **Preview** deploy per PR\n3. **Manual** promote from staging tag\n\nWhich pipeline should I implement?",
    "Which pipeline should I implement?",
    ["Staging", "Preview", "Manual"],
    "Workflow dispatch inputs are ambiguous. Planned pipelines:\n\n1. **Staging** deploy on `main` push\n2. **Preview** deploy per PR\n3. **Manual** promote from staging tag\n\nShall I implement the staging deploy first?",
    "Shall I implement the staging deploy first?",
    note_a="pipeline menu with implement -> multi_choice propose",
    note_b="plan list; staging implement proposal",
    pa=True,
)

add(
    263,
    "Cache restore missed on `~/.cargo/registry`. Fixes:\n\n- **Bump** cache key suffix\n- **Split** caches per crate group\n- **Disable** cache for the bench job only\n\nWhich cache tweak should I try?",
    "Which cache tweak should I try?",
    ["Bump", "Split", "Disable"],
    "Cache restore missed on `~/.cargo/registry`. Fixes considered:\n\n- **Bump** cache key suffix\n- **Split** caches per crate group\n- **Disable** cache for the bench job only\n\nWant me to bump the cache key suffix?",
    "Want me to bump the cache key suffix?",
    note_a="cache fix menu -> multi_choice",
    note_b="fix inventory; bump proposed",
    pa=True,
)

add(
    264,
    "Required checks on the PR:\n\n- **codecov** — below threshold on `parsers/`\n- **semgrep** — one finding in `upload.ts`\n- **license** — missing NOTICE for `lodash`\n\nWhich check should I unblock first?",
    "Which check should I unblock first?",
    ["codecov", "semgrep", "license"],
    "Required checks on the PR:\n\n- **codecov** — below threshold on `parsers/`\n- **semgrep** — one finding in `upload.ts`\n- **license** — missing NOTICE for `lodash`\n\nReady for me to fix the semgrep finding?",
    "Ready for me to fix the semgrep finding?",
    note_a="check menu -> multi_choice",
    note_b="check status; semgrep fix proposal",
    pa=True,
)

add(
    265,
    "Nightly workflow timed out. Two levers:\n\n- **Shard** tests across four runners\n- **Trim** the integration suite to smoke only\n\nWhich should we do?",
    "Which should we do?",
    ["Shard", "Trim"],
    "Nightly workflow timed out. Options on the table:\n\n- **Shard** tests across four runners\n- **Trim** the integration suite to smoke only\n\nWant me to shard tests across four runners?",
    "Want me to shard tests across four runners?",
    note_a="two CI levers -> either_or",
    note_b="option inventory; shard proposal",
    ka="e",
    pa=True,
)

add(
    266,
    "Deploy gate failed signature verification. Remediation paths:\n\n1. **Rotate** the cosign key\n2. **Pin** the digest in the workflow\n3. **Allowlist** the dev registry temporarily\n\nWhich path should I take?",
    "Which path should I take?",
    ["Rotate", "Pin", "Allowlist"],
    "Deploy gate failed signature verification. Remediation paths noted:\n\n1. **Rotate** the cosign key\n2. **Pin** the digest in the workflow\n3. **Allowlist** the dev registry temporarily\n\nShall I pin the digest in the workflow?",
    "Shall I pin the digest in the workflow?",
    note_a="three remediation paths -> multi_choice",
    note_b="path inventory; pin proposed",
    pa=True,
)

add(
    267,
    "Self-hosted runner disk is 94% full. Cleanup options:\n\n- **Prune** old Docker layers\n- **Purge** `_work` directories older than 7 days\n- **Expand** the volume (needs infra ticket)\n\nWhich cleanup should I run?",
    "Which cleanup should I run?",
    ["Prune", "Purge", "Expand"],
    "Self-hosted runner disk is 94% full. Cleanup options logged:\n\n- **Prune** old Docker layers\n- **Purge** `_work` directories older than 7 days\n- **Expand** the volume (needs infra ticket)\n\nWant me to prune old Docker layers?",
    "Want me to prune old Docker layers?",
    note_a="cleanup menu -> multi_choice",
    note_b="options as status; prune proposed",
    pa=True,
)

add(
    268,
    "Concurrency group blocked two workflows. Either:\n\n- **Cancel** the older run\n- **Queue** until the in-flight job finishes\n\nWhich concurrency policy do you prefer?",
    "Which concurrency policy do you prefer?",
    ["Cancel", "Queue"],
    "Concurrency group blocked two workflows. Policies compared:\n\n- **Cancel** the older run\n- **Queue** until the in-flight job finishes\n\nShall I cancel the older run?",
    "Shall I cancel the older run?",
    note_a="two policies -> either_or",
    note_b="policy comparison background; cancel proposed",
    ka="e",
    pa=False,
)

add(
    269,
    "Artifact upload failed on `coverage.xml`. I can:\n\n- **Re-run** the test job with debug logging\n- **Split** the artifact into two uploads\n- **Switch** to codecov CLI upload step\n\nWhich fix should I apply?",
    "Which fix should I apply?",
    ["Re-run", "Split", "Switch"],
    "Artifact upload failed on `coverage.xml`. Fix candidates:\n\n- **Re-run** the test job with debug logging\n- **Split** the artifact into two uploads\n- **Switch** to codecov CLI upload step\n\nWant me to switch to the codecov CLI upload step?",
    "Want me to switch to the codecov CLI upload step?",
    note_a="artifact fix menu -> multi_choice",
    note_b="candidates as inventory; switch proposed",
    pa=True,
)

add(
    270,
    "Branch protection wants two reviews but bot merges are stuck. Options:\n\n1. **Add** a CODEOWNERS rule for `infra/`\n2. **Exempt** dependabot with a label\n3. **Require** status checks only on `main`\n\nWhich policy change should I draft?",
    "Which policy change should I draft?",
    ["Add", "Exempt", "Require"],
    "Branch protection wants two reviews but bot merges are stuck. Policy ideas:\n\n1. **Add** a CODEOWNERS rule for `infra/`\n2. **Exempt** dependabot with a label\n3. **Require** status checks only on `main`\n\nReady for me to draft the CODEOWNERS rule?",
    "Ready for me to draft the CODEOWNERS rule?",
    note_a="policy menu -> multi_choice",
    note_b="ideas as background; CODEOWNERS draft proposed",
    pa=True,
)

# --- tests ---
add(
    271,
    "Pytest collection dropped 12 tests after the rename. Likely causes:\n\n- **Path** — `tests/unit` not in `pythonpath`\n- **Pattern** — files no longer match `test_*.py`\n- **Markers** — `@pytest.mark.integration` filter too strict\n\nWhich cause should I investigate first?",
    "Which cause should I investigate first?",
    ["Path", "Pattern", "Markers"],
    "Pytest collection dropped 12 tests after the rename. Likely causes noted:\n\n- **Path** — `tests/unit` not in `pythonpath`\n- **Pattern** — files no longer match `test_*.py`\n- **Markers** — `@pytest.mark.integration` filter too strict\n\nWant me to check the pythonpath first?",
    "Want me to check the pythonpath first?",
    note_a="diagnostic menu -> multi_choice",
    note_b="causes as findings; pythonpath check proposed",
)

add(
    272,
    "Snapshot drift in `Sidebar.test.tsx`:\n\n1. **Accept** all 6 updates\n2. **Reject** and fix the component\n3. **Split** — accept layout, reject typography\n\nWhich snapshot path should I take?",
    "Which snapshot path should I take?",
    ["Accept", "Reject", "Split"],
    "Snapshot drift in `Sidebar.test.tsx`:\n\n1. **Accept** all 6 updates\n2. **Reject** and fix the component\n3. **Split** — accept layout, reject typography\n\nShall I accept all six updates?",
    "Shall I accept all six updates?",
    note_a="snapshot strategy menu -> multi_choice",
    note_b="strategy inventory; accept proposed",
    pa=True,
)

add(
    273,
    "Flaky `test_websocket_reconnect` only fails in CI. Mitigations:\n\n- **Increase** wait timeout to 30s\n- **Retry** the test three times in CI\n- **Quarantine** with `@pytest.mark.flaky`\n\nWhich mitigation should I implement?",
    "Which mitigation should I implement?",
    ["Increase", "Retry", "Quarantine"],
    "Flaky `test_websocket_reconnect` only fails in CI. Mitigations under review:\n\n- **Increase** wait timeout to 30s\n- **Retry** the test three times in CI\n- **Quarantine** with `@pytest.mark.flaky`\n\nWant me to add the retry wrapper in CI?",
    "Want me to add the retry wrapper in CI?",
    note_a="mitigation menu with implement -> multi_choice propose",
    note_b="mitigation list as plan; retry proposed",
    pa=True,
)

add(
    274,
    "Coverage gate failed on two packages:\n\n- **parsers** — missing branch on error path\n- **handlers** — untested middleware\n\nWhich package should I add tests for first?",
    "Which package should I add tests for first?",
    ["parsers", "handlers"],
    "Coverage gate failed on two packages:\n\n- **parsers** — missing branch on error path\n- **handlers** — untested middleware\n\nReady for me to add tests in `parsers/`?",
    "Ready for me to add tests in `parsers/`?",
    note_a="two packages -> either_or",
    note_b="coverage findings; parsers tests proposed",
    ka="e",
    pa=True,
)

add(
    275,
    "Property test shrank a counterexample. Next steps:\n\n- **Fix** the off-by-one in `paginate()`\n- **Tighten** the strategy bounds\n- **Mark** xfail until refactor lands\n\nWhich should I do?",
    "Which should I do?",
    ["Fix", "Tighten", "Mark"],
    "Property test shrank a counterexample. Next steps queued:\n\n- **Fix** the off-by-one in `paginate()`\n- **Tighten** the strategy bounds\n- **Mark** xfail until refactor lands\n\nWant me to fix the off-by-one in `paginate()`?",
    "Want me to fix the off-by-one in `paginate()`?",
    note_a="hypothesis recovery menu -> multi_choice",
    note_b="queued steps; fix proposed",
    pa=True,
)

add(
    276,
    "Playwright trace shows two failures:\n\n1. **Login** — storageState expired\n2. **Checkout** — `#pay-btn` detached\n\nWhich spec should I stabilize first?",
    "Which spec should I stabilize first?",
    ["Login", "Checkout"],
    "Playwright trace shows two failures:\n\n1. **Login** — storageState expired\n2. **Checkout** — `#pay-btn` detached\n\nShall I refresh the storageState fixture?",
    "Shall I refresh the storageState fixture?",
    note_a="two failing specs -> either_or",
    note_b="failure inventory; storageState fix proposed",
    ka="e",
    pa=True,
)

add(
    277,
    "Mock server recordings are stale for three endpoints:\n\n- **GET /health**\n- **POST /sessions**\n- **DELETE /sessions/:id**\n\nWhich endpoint(s) should I re-record?",
    "Which endpoint(s) should I re-record?",
    ["GET /health", "POST /sessions", "DELETE /sessions/:id"],
    "Mock server recordings are stale for three endpoints:\n\n- **GET /health**\n- **POST /sessions**\n- **DELETE /sessions/:id**\n\nWant me to re-record GET /health first?",
    "Want me to re-record GET /health first?",
    note_a="endpoint(s) in question -> multi_choice multiSelect",
    note_b="stale list background; health re-record proposed",
    ms_a=True,
    pa=True,
)

add(
    278,
    "Benchmark regression on `parse_json`:\n\n- **Revert** last SIMD tweak\n- **Profile** with `perf record`\n- **Gate** bench job to main only\n\nWhich approach do you prefer?",
    "Which approach do you prefer?",
    ["Revert", "Profile", "Gate"],
    "Benchmark regression on `parse_json`:\n\n- **Revert** last SIMD tweak\n- **Profile** with `perf record`\n- **Gate** bench job to main only\n\nReady for me to profile with `perf record`?",
    "Ready for me to profile with `perf record`?",
    note_a="bench recovery menu -> multi_choice",
    note_b="approaches as status; profile proposed",
    pa=False,
)

add(
    279,
    "Test fixtures conflict on `tmp_path`:\n\n1. **Rename** session-scoped fixture\n2. **Nest** fixtures under `conftest.py` hierarchy\n3. **Inline** minimal setup per test\n\nWhich fixture strategy should I use?",
    "Which fixture strategy should I use?",
    ["Rename", "Nest", "Inline"],
    "Test fixtures conflict on `tmp_path`:\n\n1. **Rename** session-scoped fixture\n2. **Nest** fixtures under `conftest.py` hierarchy\n3. **Inline** minimal setup per test\n\nWant me to rename the session-scoped fixture?",
    "Want me to rename the session-scoped fixture?",
    note_a="fixture strategy menu -> multi_choice",
    note_b="strategy list as plan; rename proposed",
    pa=True,
)

add(
    280,
    "Mutation score dropped after the refactor. Two tracks:\n\n- **Add** edge-case tests for `validate()`\n- **Relax** the mutation threshold temporarily\n\nWhich track should we take?",
    "Which track should we take?",
    ["Add", "Relax"],
    "Mutation score dropped after the refactor. Two tracks on the board:\n\n- **Add** edge-case tests for `validate()`\n- **Relax** the mutation threshold temporarily\n\nShall I add edge-case tests for `validate()`?",
    "Shall I add edge-case tests for `validate()`?",
    note_a="two tracks -> either_or",
    note_b="tracks as inventory; add tests proposed",
    ka="e",
    pa=True,
)

# --- UI / frontend ---
add(
    281,
    "Design review flagged three UI issues:\n\n- **Contrast** on secondary buttons\n- **Focus ring** missing on modals\n- **Spacing** in the filter bar\n\nWhich issue should I fix first?",
    "Which issue should I fix first?",
    ["Contrast", "Focus ring", "Spacing"],
    "Design review flagged three UI issues:\n\n- **Contrast** on secondary buttons\n- **Focus ring** missing on modals\n- **Spacing** in the filter bar\n\nWant me to fix the contrast on secondary buttons?",
    "Want me to fix the contrast on secondary buttons?",
    note_a="UI issue menu -> multi_choice",
    note_b="review findings; contrast fix proposed",
    pa=True,
)

add(
    282,
    "Component library migration options:\n\n1. **Incremental** — wrap old Button API\n2. **Big bang** — replace all imports in one PR\n3. **Parallel** — run both libraries behind a flag\n\nWhich migration should I start?",
    "Which migration should I start?",
    ["Incremental", "Big bang", "Parallel"],
    "Component library migration options:\n\n1. **Incremental** — wrap old Button API\n2. **Big bang** — replace all imports in one PR\n3. **Parallel** — run both libraries behind a flag\n\nReady for me to start the incremental wrap?",
    "Ready for me to start the incremental wrap?",
    note_a="migration menu -> multi_choice",
    note_b="options as plan; incremental start proposed",
    pa=True,
)

add(
    283,
    "Accessibility audit found:\n\n- **Labels** missing on search input\n- **Landmarks** — main nav not in `<nav>`\n- **Live region** for toast announcements\n\nWhich a11y fix should I implement?",
    "Which a11y fix should I implement?",
    ["Labels", "Landmarks", "Live region"],
    "Accessibility audit found:\n\n- **Labels** missing on search input\n- **Landmarks** — main nav not in `<nav>`\n- **Live region** for toast announcements\n\nShall I add labels to the search input?",
    "Shall I add labels to the search input?",
    note_a="a11y menu with implement -> multi_choice propose",
    note_b="audit findings; labels proposed",
    pa=True,
)

add(
    284,
    "Dark mode tokens are inconsistent:\n\n- **CSS variables** in `:root`\n- **Tailwind** `dark:` utilities only\n\nWhich theming approach do you prefer?",
    "Which theming approach do you prefer?",
    ["CSS variables", "Tailwind"],
    "Dark mode tokens are inconsistent:\n\n- **CSS variables** in `:root`\n- **Tailwind** `dark:` utilities only\n\nWant me to consolidate on CSS variables?",
    "Want me to consolidate on CSS variables?",
    note_a="two theming approaches -> either_or",
    note_b="approach comparison; CSS variables proposed",
    ka="e",
    pa=False,
)

add(
    285,
    "Bundle analyzer highlights three chunks:\n\n1. **vendor-react** — 180KB gzip\n2. **charts** — loaded on every route\n3. **icons** — entire sprite imported\n\nWhich chunk should I optimize first?",
    "Which chunk should I optimize first?",
    ["vendor-react", "charts", "icons"],
    "Bundle analyzer highlights three chunks:\n\n1. **vendor-react** — 180KB gzip\n2. **charts** — loaded on every route\n3. **icons** — entire sprite imported\n\nWant me to lazy-load the charts chunk?",
    "Want me to lazy-load the charts chunk?",
    note_a="chunk menu -> multi_choice",
    note_b="analyzer output; charts lazy-load proposed",
    pa=True,
)

add(
    286,
    "Form validation UX options:\n\n- **Inline** errors under each field\n- **Summary** banner at top on submit\n- **Both** inline and summary\n\nWhich validation pattern should I ship?",
    "Which validation pattern should I ship?",
    ["Inline", "Summary", "Both"],
    "Form validation UX options:\n\n- **Inline** errors under each field\n- **Summary** banner at top on submit\n- **Both** inline and summary\n\nReady for me to ship inline errors under each field?",
    "Ready for me to ship inline errors under each field?",
    note_a="validation pattern menu -> multi_choice",
    note_b="UX options as background; inline ship proposed",
    pa=True,
)

add(
    287,
    "Storybook stories missing for:\n\n- **DataTable** empty state\n- **Modal** focus trap\n- **Toast** queue behavior\n\nWhich story should I write first?",
    "Which story should I write first?",
    ["DataTable", "Modal", "Toast"],
    "Storybook stories missing for:\n\n- **DataTable** empty state\n- **Modal** focus trap\n- **Toast** queue behavior\n\nWant me to write the DataTable empty state story?",
    "Want me to write the DataTable empty state story?",
    note_a="story backlog menu -> multi_choice",
    note_b="missing stories inventory; DataTable proposed",
    pa=True,
)

add(
    288,
    "Responsive layout breaks at two breakpoints:\n\n- **768px** — sidebar overlaps content\n- **1024px** — table columns clip\n\nWhich breakpoint should I fix first?",
    "Which breakpoint should I fix first?",
    ["768px", "1024px"],
    "Responsive layout breaks at two breakpoints:\n\n- **768px** — sidebar overlaps content\n- **1024px** — table columns clip\n\nShall I fix the 768px sidebar overlap?",
    "Shall I fix the 768px sidebar overlap?",
    note_a="two breakpoints -> either_or",
    note_b="breakage inventory; 768px fix proposed",
    ka="e",
    pa=True,
)

add(
    289,
    "Animation polish candidates:\n\n1. **Skeleton** shimmer on load\n2. **Page** transition fade\n3. **Reduced motion** media query fallback\n\nWhich animation should I add?",
    "Which animation should I add?",
    ["Skeleton", "Page", "Reduced motion"],
    "Animation polish candidates:\n\n1. **Skeleton** shimmer on load\n2. **Page** transition fade\n3. **Reduced motion** media query fallback\n\nWant me to add the skeleton shimmer?",
    "Want me to add the skeleton shimmer?",
    note_a="animation menu -> multi_choice",
    note_b="candidates as backlog; skeleton proposed",
    pa=True,
)

add(
    290,
    "i18n gaps in the checkout flow:\n\n- **Copy** — hard-coded strings in `PaymentStep`\n- **Dates** — not using `Intl.DateTimeFormat`\n- **RTL** — layout mirrors incorrectly\n\nWhich i18n gap should I close first?",
    "Which i18n gap should I close first?",
    ["Copy", "Dates", "RTL"],
    "i18n gaps in the checkout flow:\n\n- **Copy** — hard-coded strings in `PaymentStep`\n- **Dates** — not using `Intl.DateTimeFormat`\n- **RTL** — layout mirrors incorrectly\n\nReady for me to extract copy in `PaymentStep`?",
    "Ready for me to extract copy in `PaymentStep`?",
    note_a="i18n menu -> multi_choice",
    note_b="gap inventory; copy extraction proposed",
    pa=True,
)

# --- data / backend ---
add(
    291,
    "Migration plan for the `users.email` split:\n\n1. **Expand** — add nullable `email_normalized`\n2. **Backfill** — batch job overnight\n3. **Contract** — drop legacy column\n\nWhich migration phase should I implement?",
    "Which migration phase should I implement?",
    ["Expand", "Backfill", "Contract"],
    "Migration plan for the `users.email` split:\n\n1. **Expand** — add nullable `email_normalized`\n2. **Backfill** — batch job overnight\n3. **Contract** — drop legacy column\n\nShall I implement the expand phase?",
    "Shall I implement the expand phase?",
    note_a="migration phase menu -> multi_choice propose",
    note_b="plan phases as background; expand proposed",
    pa=True,
)

add(
    292,
    "Query planner chose a seq scan on `orders`. Options:\n\n- **Index** on `(customer_id, created_at)`\n- **Rewrite** query to use covering index\n- **Materialized view** for dashboard aggregates\n\nWhich optimization should I try?",
    "Which optimization should I try?",
    ["Index", "Rewrite", "Materialized view"],
    "Query planner chose a seq scan on `orders`. Options logged:\n\n- **Index** on `(customer_id, created_at)`\n- **Rewrite** query to use covering index\n- **Materialized view** for dashboard aggregates\n\nWant me to add the composite index?",
    "Want me to add the composite index?",
    note_a="DB optimization menu -> multi_choice",
    note_b="options as findings; index proposed",
    pa=True,
)

add(
    293,
    "Redis cache invalidation strategies:\n\n- **TTL** — 5 minute expiry on session keys\n- **Pub/sub** — broadcast on write\n- **Version** — bump key prefix on schema change\n\nWhich strategy do you prefer?",
    "Which strategy do you prefer?",
    ["TTL", "Pub/sub", "Version"],
    "Redis cache invalidation strategies:\n\n- **TTL** — 5 minute expiry on session keys\n- **Pub/sub** — broadcast on write\n- **Version** — bump key prefix on schema change\n\nReady for me to wire pub/sub invalidation?",
    "Ready for me to wire pub/sub invalidation?",
    note_a="cache strategy menu -> multi_choice",
    note_b="strategy comparison; pub/sub proposed",
    pa=False,
)

add(
    294,
    "API versioning debate:\n\n1. **URL** prefix `/v2/`\n2. **Header** `Accept-Version: 2`\n\nWhich versioning style should we adopt?",
    "Which versioning style should we adopt?",
    ["URL", "Header"],
    "API versioning debate:\n\n1. **URL** prefix `/v2/`\n2. **Header** `Accept-Version: 2`\n\nWant me to draft the URL prefix approach?",
    "Want me to draft the URL prefix approach?",
    note_a="two versioning styles -> either_or",
    note_b="debate inventory; URL draft proposed",
    ka="e",
    pa=True,
)

add(
    295,
    "ETL job failed on three stages:\n\n- **Extract** — S3 permissions\n- **Transform** — schema mismatch on `amount`\n- **Load** — duplicate key on `id`\n\nWhich stage should I debug first?",
    "Which stage should I debug first?",
    ["Extract", "Transform", "Load"],
    "ETL job failed on three stages:\n\n- **Extract** — S3 permissions\n- **Transform** — schema mismatch on `amount`\n- **Load** — duplicate key on `id`\n\nShall I debug the extract permissions?",
    "Shall I debug the extract permissions?",
    note_a="ETL stage menu -> multi_choice",
    note_b="failure stages as status; extract debug proposed",
)

add(
    296,
    "GraphQL N+1 on the orders resolver. Fixes:\n\n- **DataLoader** batching\n- **JOIN** fetch in repository layer\n- **Persisted queries** allowlist\n\nWhich fix should I implement?",
    "Which fix should I implement?",
    ["DataLoader", "JOIN", "Persisted queries"],
    "GraphQL N+1 on the orders resolver. Fixes considered:\n\n- **DataLoader** batching\n- **JOIN** fetch in repository layer\n- **Persisted queries** allowlist\n\nWant me to add DataLoader batching?",
    "Want me to add DataLoader batching?",
    note_a="GraphQL fix menu with implement -> multi_choice propose",
    note_b="fix list as analysis; DataLoader proposed",
    pa=True,
)

add(
    297,
    "Feature flag rollout for `new_billing`:\n\n- **Internal** — staff only\n- **Percentage** — 10% of tenants\n- **Allowlist** — pilot customers\n\nWhich rollout mode should I configure?",
    "Which rollout mode should I configure?",
    ["Internal", "Percentage", "Allowlist"],
    "Feature flag rollout for `new_billing`:\n\n- **Internal** — staff only\n- **Percentage** — 10% of tenants\n- **Allowlist** — pilot customers\n\nReady for me to configure internal-only rollout?",
    "Ready for me to configure internal-only rollout?",
    note_a="rollout mode menu -> multi_choice",
    note_b="modes as plan; internal configure proposed",
    pa=True,
)

add(
    298,
    "Kafka consumer lag spiked on two topics:\n\n1. **events.clickstream**\n2. **events.billing**\n\nWhich topic should I scale consumers for?",
    "Which topic should I scale consumers for?",
    ["events.clickstream", "events.billing"],
    "Kafka consumer lag spiked on two topics:\n\n1. **events.clickstream**\n2. **events.billing**\n\nWant me to scale consumers for clickstream?",
    "Want me to scale consumers for clickstream?",
    note_a="two topics -> either_or",
    note_b="lag inventory; clickstream scale proposed",
    ka="e",
    pa=True,
)

add(
    299,
    "Schema drift between staging and prod:\n\n- **users** — missing index\n- **invoices** — extra nullable column\n- **audit_log** — partition scheme differs\n\nWhich table should I reconcile first?",
    "Which table should I reconcile first?",
    ["users", "invoices", "audit_log"],
    "Schema drift between staging and prod:\n\n- **users** — missing index\n- **invoices** — extra nullable column\n- **audit_log** — partition scheme differs\n\nShall I reconcile the users table first?",
    "Shall I reconcile the users table first?",
    note_a="table drift menu -> multi_choice",
    note_b="drift findings; users reconcile proposed",
    pa=True,
)

add(
    300,
    "Backup restore validation options:\n\n- **Point-in-time** restore to scratch DB\n- **Logical dump** compare row counts\n- **Checksum** tables against prod sample\n\nWhich validation should I run?",
    "Which validation should I run?",
    ["Point-in-time", "Logical dump", "Checksum"],
    "Backup restore validation options:\n\n- **Point-in-time** restore to scratch DB\n- **Logical dump** compare row counts\n- **Checksum** tables against prod sample\n\nWant me to run a point-in-time restore to scratch?",
    "Want me to run a point-in-time restore to scratch?",
    note_a="validation menu -> multi_choice",
    note_b="options as checklist; PITR proposed",
    pa=True,
)

# --- infra / ops ---
add(
    301,
    "Terraform plan shows three changes:\n\n1. **RDS** — instance class bump\n2. **SG** — new ingress rule for bastion\n3. **S3** — lifecycle policy on logs bucket\n\nWhich change should I apply first?",
    "Which change should I apply first?",
    ["RDS", "SG", "S3"],
    "Terraform plan shows three changes:\n\n1. **RDS** — instance class bump\n2. **SG** — new ingress rule for bastion\n3. **S3** — lifecycle policy on logs bucket\n\nReady for me to apply the SG ingress rule?",
    "Ready for me to apply the SG ingress rule?",
    note_a="TF change menu -> multi_choice",
    note_b="plan output as inventory; SG apply proposed",
    pa=True,
)

add(
    302,
    "Kubernetes pod crash loop causes:\n\n- **OOM** — memory limit too low\n- **Probe** — liveness too aggressive\n- **Config** — missing `DATABASE_URL`\n\nWhich cause should I fix first?",
    "Which cause should I fix first?",
    ["OOM", "Probe", "Config"],
    "Kubernetes pod crash loop causes:\n\n- **OOM** — memory limit too low\n- **Probe** — liveness too aggressive\n- **Config** — missing `DATABASE_URL`\n\nWant me to raise the memory limit?",
    "Want me to raise the memory limit?",
    note_a="crash cause menu -> multi_choice",
    note_b="causes as diagnostics; OOM fix proposed",
    pa=True,
)

add(
    303,
    "Observability gaps after the outage:\n\n- **Traces** — missing span on checkout\n- **Metrics** — no SLO burn alert\n- **Logs** — PII in debug lines\n\nWhich gap should I close first?",
    "Which gap should I close first?",
    ["Traces", "Metrics", "Logs"],
    "Observability gaps after the outage:\n\n- **Traces** — missing span on checkout\n- **Metrics** — no SLO burn alert\n- **Logs** — PII in debug lines\n\nShall I add the checkout trace span?",
    "Shall I add the checkout trace span?",
    note_a="observability menu -> multi_choice",
    note_b="gap inventory; trace span proposed",
    pa=True,
)

add(
    304,
    "Secrets rotation paths:\n\n- **Vault** dynamic credentials\n- **Manual** rotate in AWS SM\n\nWhich rotation path do you prefer?",
    "Which rotation path do you prefer?",
    ["Vault", "Manual"],
    "Secrets rotation paths:\n\n- **Vault** dynamic credentials\n- **Manual** rotate in AWS SM\n\nWant me to wire Vault dynamic credentials?",
    "Want me to wire Vault dynamic credentials?",
    note_a="two rotation paths -> either_or",
    note_b="paths as comparison; Vault proposed",
    ka="e",
    pa=False,
)

add(
    305,
    "CDN cache purge scopes:\n\n1. **Single** object `/assets/app.js`\n2. **Prefix** `/assets/*`\n3. **Full** distribution flush\n\nWhich purge scope should I run?",
    "Which purge scope should I run?",
    ["Single", "Prefix", "Full"],
    "CDN cache purge scopes:\n\n1. **Single** object `/assets/app.js`\n2. **Prefix** `/assets/*`\n3. **Full** distribution flush\n\nReady for me to purge the `/assets/*` prefix?",
    "Ready for me to purge the `/assets/*` prefix?",
    note_a="purge scope menu -> multi_choice",
    note_b="scope options as plan; prefix purge proposed",
    pa=True,
)

add(
    306,
    "Autoscaling tuning levers:\n\n- **CPU** target 60%\n- **RPS** target 500 per pod\n- **Queue depth** on worker pool\n\nWhich signal should I optimize for?",
    "Which signal should I optimize for?",
    ["CPU", "RPS", "Queue depth"],
    "Autoscaling tuning levers:\n\n- **CPU** target 60%\n- **RPS** target 500 per pod\n- **Queue depth** on worker pool\n\nWant me to tune on RPS first?",
    "Want me to tune on RPS first?",
    note_a="autoscale signal menu -> multi_choice",
    note_b="levers as background; RPS tune proposed",
    pa=False,
)

add(
    307,
    "Incident comms templates ready:\n\n- **Statuspage** update draft\n- **Slack** #incidents post\n- **Customer email** for enterprise tier\n\nWhich comms piece should I send first?",
    "Which comms piece should I send first?",
    ["Statuspage", "Slack", "Customer email"],
    "Incident comms templates ready:\n\n- **Statuspage** update draft\n- **Slack** #incidents post\n- **Customer email** for enterprise tier\n\nShall I post the Slack #incidents update?",
    "Shall I post the Slack #incidents update?",
    note_a="comms menu -> multi_choice",
    note_b="templates as inventory; Slack post proposed",
    pa=True,
)

add(
    308,
    "DNS cutover options for `api.example.test`:\n\n- **Blue/green** — flip weighted records\n- **Maintenance** page during TTL drain\n\nWhich cutover should we use?",
    "Which cutover should we use?",
    ["Blue/green", "Maintenance"],
    "DNS cutover options for `api.example.test`:\n\n- **Blue/green** — flip weighted records\n- **Maintenance** page during TTL drain\n\nWant me to prepare the blue/green weighted flip?",
    "Want me to prepare the blue/green weighted flip?",
    note_a="two cutover modes -> either_or",
    note_b="cutover inventory; blue/green proposed",
    ka="e",
    pa=True,
)

add(
    309,
    "Cost anomaly on three services:\n\n1. **NAT gateway** — spike in egress\n2. **RDS** — storage autoscale\n3. **Lambda** — cold start retries\n\nWhich service should I investigate first?",
    "Which service should I investigate first?",
    ["NAT gateway", "RDS", "Lambda"],
    "Cost anomaly on three services:\n\n1. **NAT gateway** — spike in egress\n2. **RDS** — storage autoscale\n3. **Lambda** — cold start retries\n\nReady for me to pull NAT gateway metrics?",
    "Ready for me to pull NAT gateway metrics?",
    note_a="service menu -> multi_choice",
    note_b="anomaly list; NAT metrics proposed",
)

add(
    310,
    "Helm chart values drift:\n\n- **replicas** — prod at 6, chart default 3\n- **resources** — limits missing on worker\n- **ingress** — TLS secret name wrong\n\nWhich values file should I patch first?",
    "Which values file should I patch first?",
    ["replicas", "resources", "ingress"],
    "Helm chart values drift:\n\n- **replicas** — prod at 6, chart default 3\n- **resources** — limits missing on worker\n- **ingress** — TLS secret name wrong\n\nWant me to patch the ingress TLS secret name?",
    "Want me to patch the ingress TLS secret name?",
    note_a="values drift menu -> multi_choice",
    note_b="drift inventory; ingress patch proposed",
    pa=True,
)

# --- docs / misc ---
add(
    311,
    "Docs site rebuild needs:\n\n- **Sidebar** — new API section\n- **Search** — Algolia index refresh\n- **Redirects** — map old `/guide/*` paths\n\nWhich docs task should I tackle first?",
    "Which docs task should I tackle first?",
    ["Sidebar", "Search", "Redirects"],
    "Docs site rebuild needs:\n\n- **Sidebar** — new API section\n- **Search** — Algolia index refresh\n- **Redirects** — map old `/guide/*` paths\n\nWant me to add the API section to the sidebar?",
    "Want me to add the API section to the sidebar?",
    note_a="docs task menu -> multi_choice",
    note_b="needs list as backlog; sidebar proposed",
    pa=True,
)

add(
    312,
    "README gaps for new contributors:\n\n1. **Prerequisites** — Node vs pnpm version\n2. **Env** — sample `.env.example` fields\n3. **Troubleshooting** — common Docker errors\n\nWhich README section should I write?",
    "Which README section should I write?",
    ["Prerequisites", "Env", "Troubleshooting"],
    "README gaps for new contributors:\n\n1. **Prerequisites** — Node vs pnpm version\n2. **Env** — sample `.env.example` fields\n3. **Troubleshooting** — common Docker errors\n\nShall I draft the Prerequisites section?",
    "Shall I draft the Prerequisites section?",
    note_a="README section menu -> multi_choice",
    note_b="gaps inventory; Prerequisites draft proposed",
    pa=True,
)

add(
    313,
    "Changelog format choices:\n\n- **Keep a Changelog** sections\n- **Conventional Commits** auto-summary\n\nWhich changelog format do you prefer?",
    "Which changelog format do you prefer?",
    ["Keep a Changelog", "Conventional Commits"],
    "Changelog format choices:\n\n- **Keep a Changelog** sections\n- **Conventional Commits** auto-summary\n\nReady for me to set up Keep a Changelog sections?",
    "Ready for me to set up Keep a Changelog sections?",
    note_a="two changelog formats -> either_or",
    note_b="format comparison; Keep a Changelog proposed",
    ka="e",
    pa=False,
)

add(
    314,
    "ADR backlog for the auth rewrite:\n\n- **Session** storage model\n- **OAuth** provider matrix\n- **Token** refresh semantics\n\nWhich ADR should I draft first?",
    "Which ADR should I draft first?",
    ["Session", "OAuth", "Token"],
    "ADR backlog for the auth rewrite:\n\n- **Session** storage model\n- **OAuth** provider matrix\n- **Token** refresh semantics\n\nWant me to draft the session storage ADR?",
    "Want me to draft the session storage ADR?",
    note_a="ADR menu -> multi_choice",
    note_b="backlog inventory; session ADR proposed",
    pa=True,
)

add(
    315,
    "Onboarding doc updates:\n\n1. **Local dev** — seed data script\n2. **CI** — how to read failing checks\n3. **Release** — tagging checklist\n\nWhich onboarding page should I refresh?",
    "Which onboarding page should I refresh?",
    ["Local dev", "CI", "Release"],
    "Onboarding doc updates:\n\n1. **Local dev** — seed data script\n2. **CI** — how to read failing checks\n3. **Release** — tagging checklist\n\nShall I refresh the local dev page?",
    "Shall I refresh the local dev page?",
    note_a="onboarding page menu -> multi_choice",
    note_b="update list as plan; local dev refresh proposed",
    pa=True,
)

add(
    316,
    "API reference generation options:\n\n- **OpenAPI** from code annotations\n- **TypeDoc** from exported types\n- **Hand-written** examples in MDX\n\nWhich generator should I wire up?",
    "Which generator should I wire up?",
    ["OpenAPI", "TypeDoc", "Hand-written"],
    "API reference generation options:\n\n- **OpenAPI** from code annotations\n- **TypeDoc** from exported types\n- **Hand-written** examples in MDX\n\nWant me to wire up OpenAPI generation?",
    "Want me to wire up OpenAPI generation?",
    note_a="generator menu -> multi_choice",
    note_b="options as comparison; OpenAPI proposed",
    pa=True,
)

add(
    317,
    "Runbook sections for database failover:\n\n- **Detection** — alert thresholds\n- **Failover** — promote replica steps\n- **Verification** — smoke queries\n\nWhich runbook section should I expand?",
    "Which runbook section should I expand?",
    ["Detection", "Failover", "Verification"],
    "Runbook sections for database failover:\n\n- **Detection** — alert thresholds\n- **Failover** — promote replica steps\n- **Verification** — smoke queries\n\nReady for me to expand the failover steps?",
    "Ready for me to expand the failover steps?",
    note_a="runbook section menu -> multi_choice",
    note_b="sections as outline; failover expand proposed",
    pa=True,
)

add(
    318,
    "License audit findings:\n\n1. **GPL** — transitive dep in `sharp`\n2. **Apache-2.0** — missing NOTICE file\n\nWhich license issue should I resolve first?",
    "Which license issue should I resolve first?",
    ["GPL", "Apache-2.0"],
    "License audit findings:\n\n1. **GPL** — transitive dep in `sharp`\n2. **Apache-2.0** — missing NOTICE file\n\nWant me to add the Apache NOTICE file?",
    "Want me to add the Apache NOTICE file?",
    note_a="two license issues -> either_or",
    note_b="audit findings; NOTICE proposed",
    ka="e",
    pa=True,
)

add(
    319,
    "Style guide enforcement:\n\n- ** Vale** prose linter rules\n- **Markdownlint** for docs\n- **Custom** spellcheck dictionary\n\nWhich linter should I enable in CI?",
    "Which linter should I enable in CI?",
    ["Vale", "Markdownlint", "Custom"],
    "Style guide enforcement:\n\n- **Vale** prose linter rules\n- **Markdownlint** for docs\n- **Custom** spellcheck dictionary\n\nShall I enable Vale in CI?",
    "Shall I enable Vale in CI?",
    note_a="linter menu -> multi_choice",
    note_b="enforcement options; Vale enable proposed",
    pa=True,
)

add(
    320,
    "Diagram updates for architecture doc:\n\n- **Sequence** — checkout flow\n- **C4** — container boundaries\n\nWhich diagram should I redraw?",
    "Which diagram should I redraw?",
    ["Sequence", "C4"],
    "Diagram updates for architecture doc:\n\n- **Sequence** — checkout flow\n- **C4** — container boundaries\n\nWant me to redraw the sequence diagram?",
    "Want me to redraw the sequence diagram?",
    note_a="two diagram types -> either_or",
    note_b="update list; sequence redraw proposed",
    ka="e",
    pa=True,
)

# --- mixed / code blocks / URLs ---
add(
    321,
    "Refactor targets in `src/parser.rs`:\n\n[CODE]\n- split_token() — 400 lines\n- parse_expr() — recursion depth\n- error recovery — duplicated match arms\n[/CODE]\n\nWhich function should I refactor first?",
    "Which function should I refactor first?",
    ["split_token()", "parse_expr()", "error recovery"],
    "Refactor targets in `src/parser.rs`:\n\n[CODE]\n- split_token() — 400 lines\n- parse_expr() — recursion depth\n- error recovery — duplicated match arms\n[/CODE]\n\nWant me to refactor `split_token()` first?",
    "Want me to refactor `split_token()` first?",
    note_a="code block list menu -> multi_choice",
    note_b="targets as inventory; split_token proposed",
    pa=True,
)

add(
    322,
    "PR review threads still open:\n\n1. **Naming** — `fetchData` vs `loadData`\n2. **Error handling** — swallow vs propagate\n\nWhich thread should I address first?",
    "Which thread should I address first?",
    ["Naming", "Error handling"],
    "PR review threads still open:\n\n1. **Naming** — `fetchData` vs `loadData`\n2. **Error handling** — swallow vs propagate\n\nShall I reply on the naming thread?",
    "Shall I reply on the naming thread?",
    note_a="two review threads -> either_or",
    note_b="open threads inventory; naming reply proposed",
    ka="e",
    pa=True,
)

add(
    323,
    "Security scan severities:\n\n- **Critical** — RCE in dependency\n- **High** — SSRF in webhook handler\n- **Medium** — verbose error pages\n\nWhich severity bucket should I patch first?",
    "Which severity bucket should I patch first?",
    ["Critical", "High", "Medium"],
    "Security scan severities:\n\n- **Critical** — RCE in dependency\n- **High** — SSRF in webhook handler\n- **Medium** — verbose error pages\n\nWant me to patch the critical RCE finding?",
    "Want me to patch the critical RCE finding?",
    note_a="severity menu -> multi_choice",
    note_b="scan output; critical patch proposed",
    pa=True,
)

add(
    324,
    "Monorepo package bumps pending:\n\n- **@app/web** — React 19\n- **@app/api** — Fastify 5\n- **@app/shared** — zod 4 beta\n\nWhich package(s) should I upgrade today?",
    "Which package(s) should I upgrade today?",
    ["@app/web", "@app/api", "@app/shared"],
    "Monorepo package bumps pending:\n\n- **@app/web** — React 19\n- **@app/api** — Fastify 5\n- **@app/shared** — zod 4 beta\n\nReady for me to upgrade `@app/web` first?",
    "Ready for me to upgrade `@app/web` first?",
    note_a="package(s) menu -> multi_choice multiSelect",
    note_b="pending bumps inventory; web upgrade proposed",
    ms_a=True,
    pa=True,
)

add(
    325,
    "Local repro steps from the ticket:\n\n1. **Clone** fresh and `pnpm i`\n2. **Export** `API_BASE=[URL]`\n3. **Run** `pnpm dev` and hit `/health`\n\nWhich step fails on your machine?",
    "Which step fails on your machine?",
    ["Clone", "Export", "Run"],
    "Local repro steps from the ticket:\n\n1. **Clone** fresh and `pnpm i`\n2. **Export** `API_BASE=[URL]`\n3. **Run** `pnpm dev` and hit `/health`\n\nWant me to try the clone step in a clean dir?",
    "Want me to try the clone step in a clean dir?",
    note_a="repro step menu -> multi_choice",
    note_b="steps as background; clone try proposed",
)

add(
    326,
    "Logging verbosity options after the incident:\n\n- **JSON** structured logs everywhere\n- **Sampling** debug lines at 1%\n- **Redaction** middleware for emails\n\nWhich logging change should I ship?",
    "Which logging change should I ship?",
    ["JSON", "Sampling", "Redaction"],
    "Logging verbosity options after the incident:\n\n- **JSON** structured logs everywhere\n- **Sampling** debug lines at 1%\n- **Redaction** middleware for emails\n\nShall I ship JSON structured logs?",
    "Shall I ship JSON structured logs?",
    note_a="logging menu -> multi_choice",
    note_b="options as postmortem plan; JSON ship proposed",
    pa=True,
)

add(
    327,
    "Rate limit tuning knobs:\n\n1. **Burst** — 100 req/10s\n2. **Sustained** — 1000 req/min\n3. **Bypass** header for internal traffic\n\nWhich knob should I adjust?",
    "Which knob should I adjust?",
    ["Burst", "Sustained", "Bypass"],
    "Rate limit tuning knobs:\n\n1. **Burst** — 100 req/10s\n2. **Sustained** — 1000 req/min\n3. **Bypass** header for internal traffic\n\nWant me to lower the burst limit?",
    "Want me to lower the burst limit?",
    note_a="rate limit menu -> multi_choice",
    note_b="knobs as inventory; burst adjust proposed",
    pa=True,
)

add(
    328,
    "Email template variants ready:\n\n- **Plain** text receipt\n- **HTML** branded receipt\n\nWhich template should I send for the pilot?",
    "Which template should I send for the pilot?",
    ["Plain", "HTML"],
    "Email template variants ready:\n\n- **Plain** text receipt\n- **HTML** branded receipt\n\nReady for me to send the HTML branded receipt?",
    "Ready for me to send the HTML branded receipt?",
    note_a="two templates -> either_or",
    note_b="variants inventory; HTML send proposed",
    ka="e",
    pa=True,
)

add(
    329,
    "Dependency update strategies for Renovate:\n\n- **Grouped** minor/patch weekly\n- **Separate** PRs per major\n- **Automerge** patch only\n\nWhich Renovate rule set should I apply?",
    "Which Renovate rule set should I apply?",
    ["Grouped", "Separate", "Automerge"],
    "Dependency update strategies for Renovate:\n\n- **Grouped** minor/patch weekly\n- **Separate** PRs per major\n- **Automerge** patch only\n\nShall I apply the grouped minor/patch rule?",
    "Shall I apply the grouped minor/patch rule?",
    note_a="Renovate strategy menu -> multi_choice",
    note_b="strategies as config plan; grouped apply proposed",
    pa=True,
)

add(
    330,
    "Performance budget failures:\n\n1. **LCP** — hero image unoptimized\n2. **TTI** — main thread blocked 1.2s\n3. **CLS** — ad slot shifts layout\n\nWhich metric should I optimize first?",
    "Which metric should I optimize first?",
    ["LCP", "TTI", "CLS"],
    "Performance budget failures:\n\n1. **LCP** — hero image unoptimized\n2. **TTI** — main thread blocked 1.2s\n3. **CLS** — ad slot shifts layout\n\nWant me to optimize LCP on the hero image?",
    "Want me to optimize LCP on the hero image?",
    note_a="web vitals menu -> multi_choice",
    note_b="budget failures inventory; LCP optimize proposed",
    pa=True,
)

add(
    331,
    "CLI subcommands to expose:\n\n- **migrate** — run pending SQL\n- **seed** — load demo tenants\n- **doctor** — env and connectivity checks\n\nWhich subcommand should I implement next?",
    "Which subcommand should I implement next?",
    ["migrate", "seed", "doctor"],
    "CLI subcommands to expose:\n\n- **migrate** — run pending SQL\n- **seed** — load demo tenants\n- **doctor** — env and connectivity checks\n\nReady for me to implement `doctor`?",
    "Ready for me to implement `doctor`?",
    note_a="subcommand menu with implement -> multi_choice propose",
    note_b="subcommand backlog; doctor implement proposed",
    pa=True,
)

add(
    332,
    "Webhook delivery retries configured as:\n\n- **Linear** backoff 1s, 2s, 4s\n- **Exponential** with jitter cap 60s\n\nWhich retry policy do you prefer?",
    "Which retry policy do you prefer?",
    ["Linear", "Exponential"],
    "Webhook delivery retries configured as:\n\n- **Linear** backoff 1s, 2s, 4s\n- **Exponential** with jitter cap 60s\n\nWant me to switch to exponential backoff with jitter?",
    "Want me to switch to exponential backoff with jitter?",
    note_a="two retry policies -> either_or",
    note_b="policy comparison; exponential switch proposed",
    ka="e",
    pa=False,
)

add(
    333,
    "Sentry issue grouping fixes:\n\n1. **Fingerprint** — normalize UUIDs in message\n2. **Ignore** — browser extension noise\n3. **Assign** — route checkout errors to payments\n\nWhich grouping fix should I apply?",
    "Which grouping fix should I apply?",
    ["Fingerprint", "Ignore", "Assign"],
    "Sentry issue grouping fixes:\n\n1. **Fingerprint** — normalize UUIDs in message\n2. **Ignore** — browser extension noise\n3. **Assign** — route checkout errors to payments\n\nShall I add the UUID fingerprint rule?",
    "Shall I add the UUID fingerprint rule?",
    note_a="Sentry fix menu -> multi_choice",
    note_b="fixes as backlog; fingerprint proposed",
    pa=True,
)

add(
    334,
    "Mobile build flavors:\n\n- **Dev** — debuggable, internal API\n- **Staging** — TestFlight track\n- **Prod** — App Store release\n\nWhich flavor should I build for QA?",
    "Which flavor should I build for QA?",
    ["Dev", "Staging", "Prod"],
    "Mobile build flavors:\n\n- **Dev** — debuggable, internal API\n- **Staging** — TestFlight track\n- **Prod** — App Store release\n\nWant me to kick off a staging build?",
    "Want me to kick off a staging build?",
    note_a="build flavor menu -> multi_choice",
    note_b="flavors as inventory; staging build proposed",
    pa=True,
)

add(
    335,
    "Code review focus areas on this diff:\n\n- **Correctness** — edge cases in `normalize()`\n- **Performance** — allocation in hot loop\n- **Security** — user input in SQL fragment\n\nWhich area should I deep-dive first?",
    "Which area should I deep-dive first?",
    ["Correctness", "Performance", "Security"],
    "Code review focus areas on this diff:\n\n- **Correctness** — edge cases in `normalize()`\n- **Performance** — allocation in hot loop\n- **Security** — user input in SQL fragment\n\nReady for me to deep-dive correctness in `normalize()`?",
    "Ready for me to deep-dive correctness in `normalize()`?",
    note_a="review focus menu -> multi_choice",
    note_b="focus areas as checklist; correctness proposed",
    pa=True,
)

add(
    336,
    "Export formats for the analytics dump:\n\n1. **CSV** — wide table\n2. **Parquet** — columnar for warehouse\n3. **JSONL** — streaming friendly\n\nWhich export format should I generate?",
    "Which export format should I generate?",
    ["CSV", "Parquet", "JSONL"],
    "Export formats for the analytics dump:\n\n1. **CSV** — wide table\n2. **Parquet** — columnar for warehouse\n3. **JSONL** — streaming friendly\n\nShall I generate Parquet for the warehouse?",
    "Shall I generate Parquet for the warehouse?",
    note_a="export format menu -> multi_choice",
    note_b="formats as options list; Parquet generate proposed",
    pa=True,
)

add(
    337,
    "Auth middleware order debate:\n\n- **JWT-then-rate** — verify JWT before rate limit\n- **Rate-then-JWT** — rate limit before JWT verify\n\nWhich middleware order should we ship?",
    "Which middleware order should we ship?",
    ["JWT-then-rate", "Rate-then-JWT"],
    "Auth middleware order debate:\n\n- **JWT-then-rate** — verify JWT before rate limit\n- **Rate-then-JWT** — rate limit before JWT verify\n\nWant me to ship JWT-then-rate?",
    "Want me to ship JWT-then-rate?",
    note_a="two orderings -> either_or",
    note_b="debate inventory; JWT-first ship proposed",
    ka="e",
    pa=True,
)

add(
    338,
    "Pending cleanup tasks after the spike:\n\n- **Remove** feature flag `spike_search`\n- **Delete** temp branch `spike/search-ui`\n- **Archive** design notes in Notion\n\nWhich cleanup tasks — some or all — should I handle now?",
    "Which cleanup tasks — some or all — should I handle now?",
    ["Remove", "Delete", "Archive"],
    "Pending cleanup tasks after the spike:\n\n- **Remove** feature flag `spike_search`\n- **Delete** temp branch `spike/search-ui`\n- **Archive** design notes in Notion\n\nWant me to remove the `spike_search` flag?",
    "Want me to remove the `spike_search` flag?",
    note_a="some or all in question -> multi_choice multiSelect",
    note_b="cleanup backlog; flag remove proposed",
    ms_a=True,
    pa=True,
)

add(
    339,
    "Error budget burn sources:\n\n1. **Deploy** — bad rollout Friday\n2. **Dependency** — upstream API timeout\n3. **Traffic** — marketing spike\n\nWhich source should we mitigated first?",
    "Which source should we mitigated first?",
    ["Deploy", "Dependency", "Traffic"],
    "Error budget burn sources:\n\n1. **Deploy** — bad rollout Friday\n2. **Dependency** — upstream API timeout\n3. **Traffic** — marketing spike\n\nReady for me to draft mitigations for the dependency timeouts?",
    "Ready for me to draft mitigations for the dependency timeouts?",
    note_a="burn source menu -> multi_choice",
    note_b="sources as postmortem; dependency mitigations proposed",
    pa=True,
)

add(
    340,
    "Sandbox environments available:\n\n- **EU** — `sandbox-eu.example.test`\n- **US** — `sandbox-us.example.test`\n\nWhich sandbox should I deploy the branch to?",
    "Which sandbox should I deploy the branch to?",
    ["EU", "US"],
    "Sandbox environments available:\n\n- **EU** — `sandbox-eu.example.test`\n- **US** — `sandbox-us.example.test`\n\nWant me to deploy to the EU sandbox?",
    "Want me to deploy to the EU sandbox?",
    note_a="two sandboxes -> either_or",
    note_b="env inventory; EU deploy proposed",
    ka="e",
    pa=True,
)

add(
    341,
    "Lint rule suppressions pending review:\n\n- **no-explicit-any** — 12 occurrences\n- **react-hooks/exhaustive-deps** — 4 warnings\n- **import/order** — auto-fixable\n\nWhich lint bucket should I clean up first?",
    "Which lint bucket should I clean up first?",
    ["no-explicit-any", "react-hooks/exhaustive-deps", "import/order"],
    "Lint rule suppressions pending review:\n\n- **no-explicit-any** — 12 occurrences\n- **react-hooks/exhaustive-deps** — 4 warnings\n- **import/order** — auto-fixable\n\nShall I auto-fix import/order?",
    "Shall I auto-fix import/order?",
    note_a="lint bucket menu -> multi_choice",
    note_b="suppression inventory; import/order fix proposed",
    pa=True,
)

add(
    342,
    "Meeting follow-ups captured:\n\n1. **Spike** GraphQL federation\n2. **Schedule** load test for Black Friday\n3. **Document** rollback for payments v2\n\nWhich follow-up should I schedule first?",
    "Which follow-up should I schedule first?",
    ["Spike", "Schedule", "Document"],
    "Meeting follow-ups captured:\n\n1. **Spike** GraphQL federation\n2. **Schedule** load test for Black Friday\n3. **Document** rollback for payments v2\n\nWant me to schedule the load test?",
    "Want me to schedule the load test?",
    note_a="follow-up menu -> multi_choice",
    note_b="meeting notes inventory; load test proposed",
    pa=True,
)

add(
    343,
    "Container base image choices:\n\n- **distroless** — minimal attack surface\n- **alpine** — smaller, musl caveats\n- **debian-slim** — glibc compatibility\n\nWhich base image should I use for the API?",
    "Which base image should I use for the API?",
    ["distroless", "alpine", "debian-slim"],
    "Container base image choices:\n\n- **distroless** — minimal attack surface\n- **alpine** — smaller, musl caveats\n- **debian-slim** — glibc compatibility\n\nReady for me to switch the API to debian-slim?",
    "Ready for me to switch the API to debian-slim?",
    note_a="base image menu -> multi_choice",
    note_b="choices as comparison; debian-slim switch proposed",
    pa=True,
)

add(
    344,
    "Two ways to unblock the release:\n\n- **Hotfix** branch off the tag\n- **Revert** the offending merge on `main`\n\nWhich unblock path do you prefer?",
    "Which unblock path do you prefer?",
    ["Hotfix", "Revert"],
    "Two ways to unblock the release:\n\n- **Hotfix** branch off the tag\n- **Revert** the offending merge on `main`\n\nShall I cut a hotfix branch off the tag?",
    "Shall I cut a hotfix branch off the tag?",
    note_a="two release paths -> either_or",
    note_b="paths as status; hotfix proposed",
    ka="e",
    pa=False,
)

add(
    345,
    "Observed regressions in the canary:\n\n- **Latency** p99 +40ms\n- **Errors** 502 rate 0.3%\n- **Saturation** CPU 85% on two pods\n\nWhich regression should I roll back for?",
    "Which regression should I roll back for?",
    ["Latency", "Errors", "Saturation"],
    "Observed regressions in the canary:\n\n- **Latency** p99 +40ms\n- **Errors** 502 rate 0.3%\n- **Saturation** CPU 85% on two pods\n\nWant me to roll back for the 502 error rate?",
    "Want me to roll back for the 502 error rate?",
    note_a="regression menu -> multi_choice",
    note_b="canary metrics inventory; 502 rollback proposed",
    pa=True,
)

add(
    346,
    "Plugin API surface to stabilize:\n\n1. **Hooks** — lifecycle callbacks\n2. **Commands** — CLI extension points\n3. **Themes** — token overrides\n\nWhich surface should we stabilize in v1?",
    "Which surface should we stabilize in v1?",
    ["Hooks", "Commands", "Themes"],
    "Plugin API surface to stabilize:\n\n1. **Hooks** — lifecycle callbacks\n2. **Commands** — CLI extension points\n3. **Themes** — token overrides\n\nReady for me to draft the hooks API?",
    "Ready for me to draft the hooks API?",
    note_a="API surface menu -> multi_choice",
    note_b="surface list as roadmap; hooks draft proposed",
    pa=True,
)

add(
    347,
    "Data retention policies to document:\n\n- **Logs** — 30 days hot, 1 year cold\n- **Metrics** — 13 months\n- **Traces** — 7 days sampled\n\nWhich retention policy should I write up first?",
    "Which retention policy should I write up first?",
    ["Logs", "Metrics", "Traces"],
    "Data retention policies to document:\n\n- **Logs** — 30 days hot, 1 year cold\n- **Metrics** — 13 months\n- **Traces** — 7 days sampled\n\nShall I write up the logs retention policy?",
    "Shall I write up the logs retention policy?",
    note_a="retention menu -> multi_choice",
    note_b="policies as inventory; logs write-up proposed",
    pa=True,
)

add(
    348,
    "Quick wins from the profiler run:\n\n- **Memoize** `selectVisibleRows`\n- **Virtualize** the 10k-row table\n\nWhich quick win should I land in this PR?",
    "Which quick win should I land in this PR?",
    ["Memoize", "Virtualize"],
    "Quick wins from the profiler run:\n\n- **Memoize** `selectVisibleRows`\n- **Virtualize** the 10k-row table\n\nWant me to memoize `selectVisibleRows` in this PR?",
    "Want me to memoize `selectVisibleRows` in this PR?",
    note_a="two perf wins -> either_or",
    note_b="profiler findings; memoize proposed",
    ka="e",
    pa=True,
)

add(
    349,
    "Support macros drafted for the runbook:\n\n1. **Ack** — we are investigating\n2. **Mitigated** — workaround live\n3. **Resolved** — root cause fixed\n\nWhich macro should I post to the status thread?",
    "Which macro should I post to the status thread?",
    ["Ack", "Mitigated", "Resolved"],
    "Support macros drafted for the runbook:\n\n1. **Ack** — we are investigating\n2. **Mitigated** — workaround live\n3. **Resolved** — root cause fixed\n\nReady for me to post the Ack macro?",
    "Ready for me to post the Ack macro?",
    note_a="macro menu -> multi_choice",
    note_b="macros as drafts; Ack post proposed",
    pa=True,
)

add(
    350,
    "Final pre-merge checklist:\n\n- **Squash** commits with conventional title\n- **Update** PR description with test plan\n- **Request** review from `@platform-team`\n\nWhich checklist item should I do first?",
    "Which checklist item should I do first?",
    ["Squash", "Update", "Request"],
    "Final pre-merge checklist:\n\n- **Squash** commits with conventional title\n- **Update** PR description with test plan\n- **Request** review from `@platform-team`\n\nWant me to update the PR description?",
    "Want me to update the PR description?",
    note_a="checklist menu -> multi_choice",
    note_b="checklist as background; description update proposed",
    pa=True,
)

assert len(PAIRS) == 100
assert [p["n"] for p in PAIRS] == list(range(251, 351))
