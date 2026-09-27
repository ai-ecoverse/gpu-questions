"""Handcrafted open vs yes_no pairs pb0051–pb0150."""
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
    51,
    "The rebase stopped at commit `a3f91c2` with a conflict in `Makefile`. I can't see your local tree.\n\nCould you paste the conflicted section from `Makefile`?",
    "Could you paste the conflicted section from `Makefile`?",
    "The rebase stopped at commit `a3f91c2` with a conflict in `Makefile`. I can't see your local tree.\n\nCould you abort the rebase and stash your WIP first?",
    "Could you abort the rebase and stash your WIP first?",
    note_a="asks for pasted conflict -> open",
    note_b="asks user to abort/stash -> yes_no",
)

add(
    52,
    "GitHub Actions shows the deploy job skipped because of a missing secret. The workflow references `STAGING_API_KEY`.\n\nDo you remember where that secret was last set?",
    "Do you remember where that secret was last set?",
    "GitHub Actions shows the deploy job skipped because of a missing secret. The workflow references `STAGING_API_KEY`.\n\nWant me to add a placeholder secret so the job can run?",
    "Want me to add a placeholder secret so the job can run?",
    note_a="asks for recalled location -> open",
    note_b="offers add secret -> yes_no/propose",
    pb=True,
)

add(
    53,
    "The tag `v2.1.0` points at a commit that never landed on `main`.\n\nWhich branch was that tag cut from?",
    "Which branch was that tag cut from?",
    "The tag `v2.1.0` points at a commit that never landed on `main`.\n\nShall I delete the tag locally and recreate it from `main`?",
    "Shall I delete the tag locally and recreate it from `main`?",
    note_a="asks which branch -> open",
    note_b="offers delete/recreate tag -> yes_no/propose",
    pb=True,
)

add(
    54,
    "Dependabot opened six PRs overnight; two touch the same lockfile.\n\nWhich two should we merge first?",
    "Which two should we merge first?",
    "Dependabot opened six PRs overnight; two touch the same lockfile.\n\nWant me to batch-merge the non-conflicting four?",
    "Want me to batch-merge the non-conflicting four?",
    note_a="asks which PRs -> open",
    note_b="offers batch merge -> yes_no/propose",
    pb=True,
)

add(
    55,
    "The release workflow failed at the `cosign sign` step with a key-not-found error.\n\nCould you share the cosign output from the failed run?",
    "Could you share the cosign output from the failed run?",
    "The release workflow failed at the `cosign sign` step with a key-not-found error.\n\nCould you re-run the signing step with debug logging enabled?",
    "Could you re-run the signing step with debug logging enabled?",
    note_a="asks for output -> open",
    note_b="asks to re-run with debug -> yes_no",
)

add(
    56,
    "`git lfs pull` is hanging on the design assets submodule.\n\nWhat does `git lfs ls-files | wc -l` show in that submodule?",
    "What does `git lfs ls-files | wc -l` show in that submodule?",
    "`git lfs pull` is hanging on the design assets submodule.\n\nCan you try `git lfs pull` with `GIT_TRACE=1` to see if you get more info?",
    "Can you try `git lfs pull` with `GIT_TRACE=1` to see if you get more info?",
    note_a="asks what command prints -> open",
    note_b="asks to try with trace -> yes_no",
    da="m",
    db="m",
)

add(
    57,
    "The CODEOWNERS rule for `infra/` didn't request review on your last PR.\n\nWhich path did you actually change under `infra/`?",
    "Which path did you actually change under `infra/`?",
    "The CODEOWNERS rule for `infra/` didn't request review on your last PR.\n\nWant me to add a CODEOWNERS entry for `infra/terraform/`?",
    "Want me to add a CODEOWNERS entry for `infra/terraform/`?",
    note_a="asks which path -> open",
    note_b="offers add entry -> yes_no/propose",
    pb=True,
)

add(
    58,
    "CI cache restore hit 100% but build time didn't drop.\n\nWould you paste the cache key line from the job log?",
    "Would you paste the cache key line from the job log?",
    "CI cache restore hit 100% but build time didn't drop.\n\nWould you clear the workflow cache and trigger a fresh build?",
    "Would you clear the workflow cache and trigger a fresh build?",
    note_a="asks for log line -> open",
    note_b="asks to clear cache -> yes_no",
)

add(
    59,
    "The monorepo filter `--filter=@app/web` still builds `@app/shared` twice.\n\nWhat turbo version is pinned in the root `package.json`?",
    "What turbo version is pinned in the root `package.json`?",
    "The monorepo filter `--filter=@app/web` still builds `@app/shared` twice.\n\nCan you try `turbo run build --filter=@app/web --dry-run` to see if you get more info?",
    "Can you try `turbo run build --filter=@app/web --dry-run` to see if you get more info?",
    note_a="asks for version number -> open",
    note_b="asks to try dry-run -> yes_no",
    da="m",
    db="m",
)

add(
    60,
    "The required status check `integration/e2e` is stuck pending on a draft PR.\n\nCould you share the run URL for that check?",
    "Could you share the run URL for that check?",
    "The required status check `integration/e2e` is stuck pending on a draft PR.\n\nCould you mark the PR ready for review so the check starts?",
    "Could you mark the PR ready for review so the check starts?",
    note_a="asks for URL -> open",
    note_b="asks to mark ready -> yes_no",
)

# --- tests ---
add(
    61,
    "Playwright timed out waiting for `#checkout-submit` in `checkout.spec.ts`.\n\nCan you paste the screenshot path from the failure artifact?",
    "Can you paste the screenshot path from the failure artifact?",
    "Playwright timed out waiting for `#checkout-submit` in `checkout.spec.ts`.\n\nCan you re-run that spec with `--headed` locally?",
    "Can you re-run that spec with `--headed` locally?",
    note_a="asks for path -> open",
    note_b="asks to re-run headed -> yes_no",
)

add(
    62,
    "Jest snapshot mismatch in `Sidebar.test.tsx` — 3 lines differ.\n\nWhich visual change did you intend in the sidebar?",
    "Which visual change did you intend in the sidebar?",
    "Jest snapshot mismatch in `Sidebar.test.tsx` — 3 lines differ.\n\nShould I update the snapshot?",
    "Should I update the snapshot?",
    note_a="asks which change -> open",
    note_b="asks approval to update -> yes_no/propose",
    pb=True,
)

add(
    63,
    "Property test `prop_roundtrip` shrank to a 1-byte input that still fails.\n\nWould you share the shrunk counterexample?",
    "Would you share the shrunk counterexample?",
    "Property test `prop_roundtrip` shrank to a 1-byte input that still fails.\n\nWould you bump the shrink limit and run it again?",
    "Would you bump the shrink limit and run it again?",
    note_a="asks for counterexample -> open",
    note_b="asks to bump/rerun -> yes_no",
)

add(
    64,
    "Integration test `test_webhook_retry` passes locally but fails in CI on the third attempt.\n\nWhat retry backoff does the CI env use?",
    "What retry backoff does the CI env use?",
    "Integration test `test_webhook_retry` passes locally but fails in CI on the third attempt.\n\nCan you add a sleep before the third attempt in CI?",
    "Can you add a sleep before the third attempt in CI?",
    note_a="asks for backoff value -> open",
    note_b="asks to add sleep -> yes_no",
)

add(
    65,
    "The contract test against the payments API returned 404 for `/v2/refunds`.\n\nWhich base URL is the pact broker pointing at?",
    "Which base URL is the pact broker pointing at?",
    "The contract test against the payments API returned 404 for `/v2/refunds`.\n\nWant me to publish a fresh pact from main?",
    "Want me to publish a fresh pact from main?",
    note_a="asks which URL -> open",
    note_b="offers publish pact -> yes_no/propose",
    pb=True,
)

add(
    66,
    "Load test harness reports 12% error rate above 800 RPS.\n\nCould you describe the error responses you're seeing at peak?",
    "Could you describe the error responses you're seeing at peak?",
    "Load test harness reports 12% error rate above 800 RPS.\n\nCould you dial concurrency back to 500 RPS and rerun?",
    "Could you dial concurrency back to 500 RPS and rerun?",
    note_a="asks for description -> open",
    note_b="asks to dial back/rerun -> yes_no",
)

add(
    67,
    "Mutation testing killed 94% of mutants but left three survivors in `validateEmail`.\n\nCan you paste the survivor report for that function?",
    "Can you paste the survivor report for that function?",
    "Mutation testing killed 94% of mutants but left three survivors in `validateEmail`.\n\nCan you try running mutmut on just `validateEmail` to see if you get more info?",
    "Can you try running mutmut on just `validateEmail` to see if you get more info?",
    note_a="asks for report paste -> open",
    note_b="asks to try scoped run -> yes_no",
    da="m",
    db="m",
)

add(
    68,
    "Benchmark regression: `BenchmarkParseJSON` is 18% slower on this branch.\n\nWhat was the baseline ns/op on your machine last week?",
    "What was the baseline ns/op on your machine last week?",
    "Benchmark regression: `BenchmarkParseJSON` is 18% slower on this branch.\n\nWant me to revert the allocator change in `parse.go`?",
    "Want me to revert the allocator change in `parse.go`?",
    note_a="asks for baseline number -> open",
    note_b="offers revert -> yes_no/propose",
    pb=True,
)

add(
    69,
    "The test container for Postgres failed to start — port 5432 already bound.\n\nWhich process is listening on 5432 on your host?",
    "Which process is listening on 5432 on your host?",
    "The test container for Postgres failed to start — port 5432 already bound.\n\nCan you stop the local Postgres service and retry the suite?",
    "Can you stop the local Postgres service and retry the suite?",
    note_a="asks which process -> open",
    note_b="asks to stop/retry -> yes_no",
)

add(
    70,
    "Visual regression flagged 6 pixels on the hero banner.\n\nWould you share the diff image from Percy?",
    "Would you share the diff image from Percy?",
    "Visual regression flagged 6 pixels on the hero banner.\n\nWould you approve the Percy build if the shift looks intentional?",
    "Would you approve the Percy build if the shift looks intentional?",
    note_a="asks for diff image -> open",
    note_b="asks to approve build -> yes_no",
)

# --- UI / frontend ---
add(
    71,
    "The date picker shows Sunday as the first day of the week in German locale.\n\nWhich weekday should be first for `de-DE`?",
    "Which weekday should be first for `de-DE`?",
    "The date picker shows Sunday as the first day of the week in German locale.\n\nWant me to wire `weekStartsOn` from the locale bundle?",
    "Want me to wire `weekStartsOn` from the locale bundle?",
    note_a="asks which weekday -> open",
    note_b="offers wire locale -> yes_no/propose",
    pb=True,
)

add(
    72,
    "Virtualized list jumps when new items arrive at the top.\n\nCan you share a screen recording of the jump?",
    "Can you share a screen recording of the jump?",
    "Virtualized list jumps when new items arrive at the top.\n\nCan you scroll to the top and trigger a refresh to reproduce?",
    "Can you scroll to the top and trigger a refresh to reproduce?",
    note_a="asks for recording -> open",
    note_b="asks to reproduce -> yes_no",
)

add(
    73,
    "Tooltip on the info icon renders off-screen at the right edge.\n\nWhat viewport width are you using when it clips?",
    "What viewport width are you using when it clips?",
    "Tooltip on the info icon renders off-screen at the right edge.\n\nCan you try flipping the tooltip placement to `left` in Storybook?",
    "Can you try flipping the tooltip placement to `left` in Storybook?",
    note_a="asks for width -> open",
    note_b="asks to try placement -> yes_no",
)

add(
    74,
    "Hydration mismatch on the pricing page — server HTML differs from client.\n\nCould you paste the React hydration warning from the console?",
    "Could you paste the React hydration warning from the console?",
    "Hydration mismatch on the pricing page — server HTML differs from client.\n\nCould you disable SSR on the pricing page temporarily to isolate it?",
    "Could you disable SSR on the pricing page temporarily to isolate it?",
    note_a="asks for console paste -> open",
    note_b="asks to disable SSR -> yes_no",
)

add(
    75,
    "The skeleton loader never resolves on slow 3G in Chrome DevTools.\n\nWhich network profile did you throttle with?",
    "Which network profile did you throttle with?",
    "The skeleton loader never resolves on slow 3G in Chrome DevTools.\n\nWant me to add a timeout fallback after 8s?",
    "Want me to add a timeout fallback after 8s?",
    note_a="asks which profile -> open",
    note_b="offers timeout fallback -> yes_no/propose",
    pb=True,
)

add(
    76,
    "Drag-and-drop reorder works in Firefox but not Safari.\n\nWhat Safari version are you on?",
    "What Safari version are you on?",
    "Drag-and-drop reorder works in Firefox but not Safari.\n\nCan you try the same drag sequence in Safari Technology Preview?",
    "Can you try the same drag sequence in Safari Technology Preview?",
    note_a="asks for version -> open",
    note_b="asks to try STP -> yes_no",
)

add(
    77,
    "The toast stack overlaps the fixed footer on short viewports.\n\nCould you describe how the overlap looks at 640px height?",
    "Could you describe how the overlap looks at 640px height?",
    "The toast stack overlaps the fixed footer on short viewports.\n\nCould you resize to 640px height and confirm the overlap?",
    "Could you resize to 640px height and confirm the overlap?",
    note_a="asks for description -> open",
    note_b="asks to resize/confirm -> yes_no",
)

add(
    78,
    "CSS grid gap collapses in the print stylesheet.\n\nWhat margin settings does your print dialog use?",
    "What margin settings does your print dialog use?",
    "CSS grid gap collapses in the print stylesheet.\n\nCan you print to PDF and check whether the gap is missing there too?",
    "Can you print to PDF and check whether the gap is missing there too?",
    note_a="asks for margin settings -> open",
    note_b="asks to print/check -> yes_no",
)

add(
    79,
    "The autocomplete dropdown renders behind the modal backdrop.\n\nWhat z-index does DevTools show on `.modal-backdrop`?",
    "What z-index does DevTools show on `.modal-backdrop`?",
    "The autocomplete dropdown renders behind the modal backdrop.\n\nWant me to raise the popover z-index above the modal layer?",
    "Want me to raise the popover z-index above the modal layer?",
    note_a="asks for z-index value -> open",
    note_b="offers raise z-index -> yes_no/propose",
    pb=True,
)

add(
    80,
    "Keyboard trap in the settings drawer — Tab cycles inside but never reaches Save.\n\nWhich element receives focus after the last field?",
    "Which element receives focus after the last field?",
    "Keyboard trap in the settings drawer — Tab cycles inside but never reaches Save.\n\nShall I add a focus sentinel before the Save button?",
    "Shall I add a focus sentinel before the Save button?",
    note_a="asks which element -> open",
    note_b="offers focus sentinel -> yes_no/propose",
    pb=True,
)

# --- data / infra ---
add(
    81,
    "BigQuery job `events_backfill_202409` scanned 4.2 TB instead of the expected 400 GB.\n\nCould you share the job statistics panel?",
    "Could you share the job statistics panel?",
    "BigQuery job `events_backfill_202409` scanned 4.2 TB instead of the expected 400 GB.\n\nCould you cancel the running job before costs spike further?",
    "Could you cancel the running job before costs spike further?",
    note_a="asks for stats panel -> open",
    note_b="asks to cancel job -> yes_no",
)

add(
    82,
    "Kafka consumer lag on `orders` spiked to 45 minutes.\n\nWhat is the current lag in messages for partition 3?",
    "What is the current lag in messages for partition 3?",
    "Kafka consumer lag on `orders` spiked to 45 minutes.\n\nCan you restart the consumer group on the staging cluster?",
    "Can you restart the consumer group on the staging cluster?",
    note_a="asks for lag number -> open",
    note_b="asks to restart consumers -> yes_no",
)

add(
    83,
    "Terraform plan wants to replace the RDS instance because of a parameter group change.\n\nWhich parameter did you change in the group?",
    "Which parameter did you change in the group?",
    "Terraform plan wants to replace the RDS instance because of a parameter group change.\n\nWant me to import the existing parameter group instead?",
    "Want me to import the existing parameter group instead?",
    note_a="asks which parameter -> open",
    note_b="offers import -> yes_no/propose",
    pb=True,
)

add(
    84,
    "Elasticsearch cluster health is yellow — unassigned shards on the hot tier.\n\nWould you paste `GET _cat/shards?v` for the hot nodes?",
    "Would you paste `GET _cat/shards?v` for the hot nodes?",
    "Elasticsearch cluster health is yellow — unassigned shards on the hot tier.\n\nWould you reroute the unassigned shards manually?",
    "Would you reroute the unassigned shards manually?",
    note_a="asks for shard paste -> open",
    note_b="asks to reroute -> yes_no",
)

add(
    85,
    "The Snowflake warehouse auto-suspended mid-query during the dbt run.\n\nWhat warehouse size was selected for that job?",
    "What warehouse size was selected for that job?",
    "The Snowflake warehouse auto-suspended mid-query during the dbt run.\n\nCan you resume the warehouse and rerun the failed models?",
    "Can you resume the warehouse and rerun the failed models?",
    note_a="asks for size -> open",
    note_b="asks to resume/rerun -> yes_no",
)

add(
    86,
    "Prometheus alert `HighErrorRate` fired but Grafana shows flat 200s.\n\nWhich scrape target is the alert query using?",
    "Which scrape target is the alert query using?",
    "Prometheus alert `HighErrorRate` fired but Grafana shows flat 200s.\n\nWant me to silence the alert for an hour while we investigate?",
    "Want me to silence the alert for an hour while we investigate?",
    note_a="asks which target -> open",
    note_b="offers silence -> yes_no/propose",
    pb=True,
)

add(
    87,
    "Nomad job `indexer` is pending — no eligible nodes.\n\nCould you share `nomad job status indexer` output?",
    "Could you share `nomad job status indexer` output?",
    "Nomad job `indexer` is pending — no eligible nodes.\n\nCould you drain one dev node and retry the allocation?",
    "Could you drain one dev node and retry the allocation?",
    note_a="asks for status output -> open",
    note_b="asks to drain/retry -> yes_no",
)

add(
    88,
    "CloudFront still serves the old `app.js` after yesterday's deploy.\n\nWhat is the `Age` header on the asset from your edge?",
    "What is the `Age` header on the asset from your edge?",
    "CloudFront still serves the old `app.js` after yesterday's deploy.\n\nCan you create an invalidation for `/static/app.js`?",
    "Can you create an invalidation for `/static/app.js`?",
    note_a="asks for header value -> open",
    note_b="asks to invalidate -> yes_no",
)

add(
    89,
    "The backup restore to the staging DB took 6 hours — twice the SLA.\n\nWhich table dominated the restore time?",
    "Which table dominated the restore time?",
    "The backup restore to the staging DB took 6 hours — twice the SLA.\n\nWant me to exclude the audit table from the next staging restore?",
    "Want me to exclude the audit table from the next staging restore?",
    note_a="asks which table -> open",
    note_b="offers exclude table -> yes_no/propose",
    pb=True,
)

add(
    90,
    "Vault lease renewal failed for the database role `app-readonly`.\n\nCould you paste the renewal error from the sidecar log?",
    "Could you paste the renewal error from the sidecar log?",
    "Vault lease renewal failed for the database role `app-readonly`.\n\nCould you revoke the lease and request a fresh credential?",
    "Could you revoke the lease and request a fresh credential?",
    note_a="asks for error paste -> open",
    note_b="asks to revoke/request -> yes_no",
)

# --- security ---
add(
    91,
    "Semgrep flagged SQL injection in `searchUsers` but the query uses parameter binding.\n\nCan you share the exact rule ID and matched lines?",
    "Can you share the exact rule ID and matched lines?",
    "Semgrep flagged SQL injection in `searchUsers` but the query uses parameter binding.\n\nCan you suppress the finding for that function pending review?",
    "Can you suppress the finding for that function pending review?",
    note_a="asks for rule/lines -> open",
    note_b="asks to suppress -> yes_no",
)

add(
    92,
    "The OAuth redirect URI in the app config doesn't match the provider console.\n\nWhich redirect URI is registered in the provider?",
    "Which redirect URI is registered in the provider?",
    "The OAuth redirect URI in the app config doesn't match the provider console.\n\nWant me to update our config to match the provider entry?",
    "Want me to update our config to match the provider entry?",
    note_a="asks which URI -> open",
    note_b="offers update config -> yes_no/propose",
    pb=True,
)

add(
    93,
    "CSP report-only logged a blocked inline script on `/checkout`.\n\nWould you paste the report payload from the browser?",
    "Would you paste the report payload from the browser?",
    "CSP report-only logged a blocked inline script on `/checkout`.\n\nWould you switch CSP to enforce mode on staging?",
    "Would you switch CSP to enforce mode on staging?",
    note_a="asks for report paste -> open",
    note_b="asks to switch enforce -> yes_no",
    da="h",
    db="e",
)

add(
    94,
    "Certificate for `api.internal.example` expires in 9 days.\n\nDo you remember which ACME account issued it?",
    "Do you remember which ACME account issued it?",
    "Certificate for `api.internal.example` expires in 9 days.\n\nShall I request a renewal through cert-manager now?",
    "Shall I request a renewal through cert-manager now?",
    note_a="asks for recalled account -> open",
    note_b="offers renewal -> yes_no/propose",
    pb=True,
)

add(
    95,
    "The pen test noted missing `SameSite=Strict` on the session cookie.\n\nWhat cookie attributes does production set today?",
    "What cookie attributes does production set today?",
    "The pen test noted missing `SameSite=Strict` on the session cookie.\n\nWant me to add `SameSite=Strict` in the auth middleware?",
    "Want me to add `SameSite=Strict` in the auth middleware?",
    note_a="asks for current attributes -> open",
    note_b="offers add attribute -> yes_no/propose",
    pb=True,
)

add(
    96,
    "SAST scan found a hardcoded token pattern in `scripts/deploy.sh`.\n\nCould you clarify whether that string is a real secret or a placeholder?",
    "Could you clarify whether that string is a real secret or a placeholder?",
    "SAST scan found a hardcoded token pattern in `scripts/deploy.sh`.\n\nCould you rotate the credential if it's real and redeploy?",
    "Could you rotate the credential if it's real and redeploy?",
    note_a="asks to clarify secret vs placeholder -> open",
    note_b="asks to rotate/redeploy -> yes_no",
)

add(
    97,
    "IAM policy simulation denies `s3:PutObject` on the artifacts bucket.\n\nWhich principal ARN are you testing with?",
    "Which principal ARN are you testing with?",
    "IAM policy simulation denies `s3:PutObject` on the artifacts bucket.\n\nCan you attach the `artifacts-writer` policy to that role?",
    "Can you attach the `artifacts-writer` policy to that role?",
    note_a="asks which ARN -> open",
    note_b="asks to attach policy -> yes_no",
)

add(
    98,
    "Rate limiter blocked your IP during the load test.\n\nWhat source IP did the edge see for your requests?",
    "What source IP did the edge see for your requests?",
    "Rate limiter blocked your IP during the load test.\n\nCan you whitelist your IP on staging for the next run?",
    "Can you whitelist your IP on staging for the next run?",
    note_a="asks for IP -> open",
    note_b="asks to whitelist -> yes_no",
)

add(
    99,
    "Dependabot security alert on `lodash` — fix available in 4.17.21.\n\nWhich services still pin lodash below 4.17.21?",
    "Which services still pin lodash below 4.17.21?",
    "Dependabot security alert on `lodash` — fix available in 4.17.21.\n\nWant me to open a bump PR across the monorepo?",
    "Want me to open a bump PR across the monorepo?",
    note_a="asks which services -> open",
    note_b="offers bump PR -> yes_no/propose",
    pb=True,
)

add(
    100,
    "Audit log shows `DELETE` on `users` without a matching ticket.\n\nCould you double-check the id or provide more details?",
    "Could you double-check the id or provide more details?",
    "Audit log shows `DELETE` on `users` without a matching ticket.\n\nCould you double-check the id and revert the delete if it was accidental?",
    "Could you double-check the id and revert the delete if it was accidental?",
    note_a="double-check or provide details -> open",
    note_b="double-check and revert -> yes_no",
    da="m",
    db="e",
)

# --- mobile ---
add(
    101,
    "Push notifications arrive on Android but not iOS.\n\nWhich APNs environment is the build using?",
    "Which APNs environment is the build using?",
    "Push notifications arrive on Android but not iOS.\n\nCan you reinstall the TestFlight build and accept notification permissions again?",
    "Can you reinstall the TestFlight build and accept notification permissions again?",
    note_a="asks which environment -> open",
    note_b="asks to reinstall -> yes_no",
)

add(
    102,
    "The React Native bundle fails code signing on device.\n\nCould you share the Xcode codesign error?",
    "Could you share the Xcode codesign error?",
    "The React Native bundle fails code signing on device.\n\nCould you clean the build folder and rebuild on device?",
    "Could you clean the build folder and rebuild on device?",
    note_a="asks for error -> open",
    note_b="asks to clean/rebuild -> yes_no",
)

add(
    103,
    "Deep link `myapp://invite/abc` opens the store instead of the app.\n\nWhat iOS version shows the wrong behavior?",
    "What iOS version shows the wrong behavior?",
    "Deep link `myapp://invite/abc` opens the store instead of the app.\n\nWant me to add the associated domain entitlement?",
    "Want me to add the associated domain entitlement?",
    note_a="asks for iOS version -> open",
    note_b="offers add entitlement -> yes_no/propose",
    pb=True,
)

add(
    104,
    "Offline sync queued 200 items but only 40 uploaded after reconnect.\n\nCan you paste the sync debug log from the device?",
    "Can you paste the sync debug log from the device?",
    "Offline sync queued 200 items but only 40 uploaded after reconnect.\n\nCan you toggle airplane mode and retry the sync?",
    "Can you toggle airplane mode and retry the sync?",
    note_a="asks for debug log -> open",
    note_b="asks to toggle/retry -> yes_no",
)

add(
    105,
    "Biometric unlock fails after OS update on Pixel 8.\n\nWhich Android security patch level is installed?",
    "Which Android security patch level is installed?",
    "Biometric unlock fails after OS update on Pixel 8.\n\nCan you enroll a new fingerprint and try unlock again?",
    "Can you enroll a new fingerprint and try unlock again?",
    note_a="asks for patch level -> open",
    note_b="asks to enroll/retry -> yes_no",
)

add(
    106,
    "App Store review rejected the build for missing privacy manifest.\n\nWhich SDKs in the binary lack privacy entries?",
    "Which SDKs in the binary lack privacy entries?",
    "App Store review rejected the build for missing privacy manifest.\n\nShall I generate a privacy manifest stub for the analytics SDK?",
    "Shall I generate a privacy manifest stub for the analytics SDK?",
    note_a="asks which SDKs -> open",
    note_b="offers generate manifest -> yes_no/propose",
    pb=True,
)

add(
    107,
    "Tablet layout shows two columns where design spec shows one.\n\nWhat device model and orientation are you testing?",
    "What device model and orientation are you testing?",
    "Tablet layout shows two columns where design spec shows one.\n\nCan you rotate to portrait and confirm whether it still splits?",
    "Can you rotate to portrait and confirm whether it still splits?",
    note_a="asks model/orientation -> open",
    note_b="asks to rotate/confirm -> yes_no",
)

add(
    108,
    "Crash on launch in release build only — debug is fine.\n\nWould you share the crash log from TestFlight?",
    "Would you share the crash log from TestFlight?",
    "Crash on launch in release build only — debug is fine.\n\nWould you install the latest release build and reproduce once?",
    "Would you install the latest release build and reproduce once?",
    note_a="asks for crash log -> open",
    note_b="asks to install/reproduce -> yes_no",
)

add(
    109,
    "In-app purchase restore returns empty on sandbox.\n\nWhich sandbox tester account are you signed in with?",
    "Which sandbox tester account are you signed in with?",
    "In-app purchase restore returns empty on sandbox.\n\nCan you sign out of the App Store and sign back into sandbox?",
    "Can you sign out of the App Store and sign back into sandbox?",
    note_a="asks which account -> open",
    note_b="asks to sign out/in -> yes_no",
)

add(
    110,
    "Location permission prompt never appears on first launch.\n\nWhat permission state does Settings show for the app?",
    "What permission state does Settings show for the app?",
    "Location permission prompt never appears on first launch.\n\nWant me to reset the permission flow and ship a new beta?",
    "Want me to reset the permission flow and ship a new beta?",
    note_a="asks for permission state -> open",
    note_b="offers reset/ship beta -> yes_no/propose",
    pb=True,
)

# --- performance ---
add(
    111,
    "Lighthouse performance score dropped from 92 to 71 on the homepage.\n\nWhich audit regressed the most in your run?",
    "Which audit regressed the most in your run?",
    "Lighthouse performance score dropped from 92 to 71 on the homepage.\n\nWant me to lazy-load the hero video?",
    "Want me to lazy-load the hero video?",
    note_a="asks which audit -> open",
    note_b="offers lazy-load -> yes_no/propose",
    pb=True,
)

add(
    112,
    "Server-Timing shows 800ms in `db.query` for `/api/search`.\n\nCould you share the slow query log entry?",
    "Could you share the slow query log entry?",
    "Server-Timing shows 800ms in `db.query` for `/api/search`.\n\nCould you add an index on `products(name)` and rerun the query?",
    "Could you add an index on `products(name)` and rerun the query?",
    note_a="asks for log entry -> open",
    note_b="asks to add index/rerun -> yes_no",
)

add(
    113,
    "Memory leak in the worker — RSS climbs 50 MB/hour.\n\nWhat does the heap snapshot top retainers list show?",
    "What does the heap snapshot top retainers list show?",
    "Memory leak in the worker — RSS climbs 50 MB/hour.\n\nCan you restart the worker pod and watch RSS for an hour?",
    "Can you restart the worker pod and watch RSS for an hour?",
    note_a="asks for retainers list -> open",
    note_b="asks to restart/watch -> yes_no",
)

add(
    114,
    "CDN cache hit ratio fell to 62% after the asset hash change.\n\nWhich paths are missing cache hits in the report?",
    "Which paths are missing cache hits in the report?",
    "CDN cache hit ratio fell to 62% after the asset hash change.\n\nWant me to extend cache TTL on immutable assets?",
    "Want me to extend cache TTL on immutable assets?",
    note_a="asks which paths -> open",
    note_b="offers extend TTL -> yes_no/propose",
    pb=True,
)

add(
    115,
    "GraphQL query `GetDashboard` returns 2.1 MB — N+1 on comments.\n\nCan you paste the field timing breakdown from Apollo Studio?",
    "Can you paste the field timing breakdown from Apollo Studio?",
    "GraphQL query `GetDashboard` returns 2.1 MB — N+1 on comments.\n\nCan you try batching comment loads with a DataLoader to see if you get more info?",
    "Can you try batching comment loads with a DataLoader to see if you get more info?",
    note_a="asks for timing paste -> open",
    note_b="asks to try batching -> yes_no",
    da="m",
    db="m",
)

add(
    116,
    "Cold start on Lambda hit 4.2s after adding the native dependency.\n\nWhat is the init duration in the latest CloudWatch report?",
    "What is the init duration in the latest CloudWatch report?",
    "Cold start on Lambda hit 4.2s after adding the native dependency.\n\nShall I move the native lib to a Lambda layer?",
    "Shall I move the native lib to a Lambda layer?",
    note_a="asks for init duration -> open",
    note_b="offers layer move -> yes_no/propose",
    pb=True,
)

add(
    117,
    "WebSocket fan-out latency p99 is 900ms under 5k connections.\n\nWhich region are the slow clients connecting from?",
    "Which region are the slow clients connecting from?",
    "WebSocket fan-out latency p99 is 900ms under 5k connections.\n\nCan you enable sticky sessions on the load balancer?",
    "Can you enable sticky sessions on the load balancer?",
    note_a="asks which region -> open",
    note_b="asks to enable sticky -> yes_no",
)

add(
    118,
    "Image pipeline outputs 400 KB PNGs where WebP would be 90 KB.\n\nWhat quality setting does the current encoder use?",
    "What quality setting does the current encoder use?",
    "Image pipeline outputs 400 KB PNGs where WebP would be 90 KB.\n\nWant me to switch the pipeline default to WebP?",
    "Want me to switch the pipeline default to WebP?",
    note_a="asks for quality setting -> open",
    note_b="offers switch format -> yes_no/propose",
    pb=True,
)

add(
    119,
    "GC pause spikes correlate with the hourly aggregation cron.\n\nCould you describe the heap pattern you see during the cron window?",
    "Could you describe the heap pattern you see during the cron window?",
    "GC pause spikes correlate with the hourly aggregation cron.\n\nCould you stagger the cron by 15 minutes and observe again?",
    "Could you stagger the cron by 15 minutes and observe again?",
    note_a="asks for heap description -> open",
    note_b="asks to stagger/observe -> yes_no",
)

add(
    120,
    "Frontend bundle grew 180 KB gzip after adding the chart library.\n\nWhich routes import the chart module today?",
    "Which routes import the chart module today?",
    "Frontend bundle grew 180 KB gzip after adding the chart library.\n\nShall I code-split charts onto the analytics route only?",
    "Shall I code-split charts onto the analytics route only?",
    note_a="asks which routes -> open",
    note_b="offers code-split -> yes_no/propose",
    pb=True,
)

# --- docs / refactors ---
add(
    121,
    "OpenAPI spec lists `POST /v1/refunds` as deprecated but clients still call it.\n\nWhich clients haven't migrated to `/v2/refunds`?",
    "Which clients haven't migrated to `/v2/refunds`?",
    "OpenAPI spec lists `POST /v1/refunds` as deprecated but clients still call it.\n\nWant me to add a sunset header on `/v1/refunds`?",
    "Want me to add a sunset header on `/v1/refunds`?",
    note_a="asks which clients -> open",
    note_b="offers sunset header -> yes_no/propose",
    pb=True,
)

add(
    122,
    "The ADR index links to ADR-014 but the file was renamed.\n\nWhat is the new filename for ADR-014?",
    "What is the new filename for ADR-014?",
    "The ADR index links to ADR-014 but the file was renamed.\n\nShall I fix the link in the ADR index?",
    "Shall I fix the link in the ADR index?",
    note_a="asks for new filename -> open",
    note_b="offers fix link -> yes_no/propose",
    pb=True,
)

add(
    123,
    "Extracting `BillingService` into its own package — 38 imports to update.\n\nCan you list the packages that import `BillingService` directly?",
    "Can you list the packages that import `BillingService` directly?",
    "Extracting `BillingService` into its own package — 38 imports to update.\n\nCan you try building with `--watch` after the move to see if you get more info?",
    "Can you try building with `--watch` after the move to see if you get more info?",
    note_a="asks for import list -> open",
    note_b="asks to try watch build -> yes_no",
    da="m",
    db="m",
)

add(
    124,
    "Runbook for `payments-outage` references a retired PagerDuty service.\n\nWhich on-call rotation should replace it?",
    "Which on-call rotation should replace it?",
    "Runbook for `payments-outage` references a retired PagerDuty service.\n\nWant me to update the runbook to point at the new rotation?",
    "Want me to update the runbook to point at the new rotation?",
    note_a="asks which rotation -> open",
    note_b="offers update runbook -> yes_no/propose",
    pb=True,
)

add(
    125,
    "Type rename from `UserDTO` to `UserView` left stale JSDoc in 12 files.\n\nWhich public APIs should still say `UserDTO` for compatibility?",
    "Which public APIs should still say `UserDTO` for compatibility?",
    "Type rename from `UserDTO` to `UserView` left stale JSDoc in 12 files.\n\nShall I run a codemod to rename remaining references?",
    "Shall I run a codemod to rename remaining references?",
    note_a="asks which APIs keep old name -> open",
    note_b="offers codemod -> yes_no/propose",
    pb=True,
)

add(
    126,
    "Contributing guide says to run `make test` but the target was removed.\n\nWhat command do you use to run the full suite locally?",
    "What command do you use to run the full suite locally?",
    "Contributing guide says to run `make test` but the target was removed.\n\nWant me to add a `make test` alias that calls `pnpm test:all`?",
    "Want me to add a `make test` alias that calls `pnpm test:all`?",
    note_a="asks for command -> open",
    note_b="offers add alias -> yes_no/propose",
    pb=True,
)

add(
    127,
    "The architecture diagram still shows the monolith calling MySQL directly.\n\nWhich datastore should the diagram show after the split?",
    "Which datastore should the diagram show after the split?",
    "The architecture diagram still shows the monolith calling MySQL directly.\n\nShall I redraw the diagram with the new services?",
    "Shall I redraw the diagram with the new services?",
    note_a="asks which datastore -> open",
    note_b="offers redraw -> yes_no/propose",
    pb=True,
)

add(
    128,
    "Inline TODO in `cache.ts` says \"fix before launch\" with no ticket.\n\nWhat was the launch blocker tied to that TODO?",
    "What was the launch blocker tied to that TODO?",
    "Inline TODO in `cache.ts` says \"fix before launch\" with no ticket.\n\nWant me to open a ticket and link it in the comment?",
    "Want me to open a ticket and link it in the comment?",
    note_a="asks what blocker -> open",
    note_b="offers open ticket -> yes_no/propose",
    pb=True,
)

add(
    129,
    "Generated protobuf stubs are out of date with `api.proto`.\n\nWhich proto fields did you add in the last commit?",
    "Which proto fields did you add in the last commit?",
    "Generated protobuf stubs are out of date with `api.proto`.\n\nCan you run `buf generate` and commit the updated stubs?",
    "Can you run `buf generate` and commit the updated stubs?",
    note_a="asks which fields -> open",
    note_b="asks to run generate -> yes_no",
)

add(
    130,
    "Style guide bans default exports but 40 files still use them.\n\nWhich directories should we migrate first?",
    "Which directories should we migrate first?",
    "Style guide bans default exports but 40 files still use them.\n\nWant me to start with `src/components/`?",
    "Want me to start with `src/components/`?",
    note_a="asks which directories -> open",
    note_b="offers start migration -> yes_no/propose",
    pb=True,
)

# --- longer status + question ---
add(
    131,
    """Afternoon update on the auth migration:

- Session store moved to Redis
- Refresh rotation implemented
- Logout revoke still TODO

The staging login flow fails after the second refresh.

Could you share the network trace for the failing refresh?""",
    "Could you share the network trace for the failing refresh?",
    """Afternoon update on the auth migration:

- Session store moved to Redis
- Refresh rotation implemented
- Logout revoke still TODO

The staging login flow fails after the second refresh.

Could you log out everywhere and walk through login again?""",
    "Could you log out everywhere and walk through login again?",
    note_a="asks for network trace -> open",
    note_b="asks to logout/walk through -> yes_no",
)

add(
    132,
    """PR checklist for the metrics overhaul:

1. Histogram buckets updated
2. Cardinality guard added
3. Dashboard JSON not imported yet

What Grafana folder should the new dashboard live in?""",
    "What Grafana folder should the new dashboard live in?",
    """PR checklist for the metrics overhaul:

1. Histogram buckets updated
2. Cardinality guard added
3. Dashboard JSON not imported yet

Want me to import the dashboard JSON into staging Grafana?""",
    "Want me to import the dashboard JSON into staging Grafana?",
    note_a="asks which folder -> open",
    note_b="offers import -> yes_no/propose",
    pb=True,
)

add(
    133,
    """Build log excerpt:

[CODE]
error: linking with `cc` failed: exit status: 1
  = note: ld: library not found for -lssl
[CODE]

Which OpenSSL package is installed on the builder image?""",
    "Which OpenSSL package is installed on the builder image?",
    """Build log excerpt:

[CODE]
error: linking with `cc` failed: exit status: 1
  = note: ld: library not found for -lssl
[CODE]

Can you rebuild the image with `openssl-dev` added to the Dockerfile?""",
    "Can you rebuild the image with `openssl-dev` added to the Dockerfile?",
    note_a="asks which package -> open",
    note_b="asks to rebuild image -> yes_no",
)

add(
    134,
    """Incident timeline (all times UTC):

- 14:02 — error rate spike
- 14:05 — auto-rollback triggered
- 14:11 — rate normalized

Which deploy SHA was live at 14:02?""",
    "Which deploy SHA was live at 14:02?",
    """Incident timeline (all times UTC):

- 14:02 — error rate spike
- 14:05 — auto-rollback triggered
- 14:11 — rate normalized

Want me to pin the rollback SHA in the deploy config?""",
    "Want me to pin the rollback SHA in the deploy config?",
    note_a="asks which SHA -> open",
    note_b="offers pin SHA -> yes_no/propose",
    pb=True,
)

add(
    135,
    """Review notes on the caching PR:

| Concern | Status |
|---------|--------|
| Stampede protection | done |
| TTL jitter | missing |
| Cache key versioning | unclear |

What TTL jitter range do you want?""",
    "What TTL jitter range do you want?",
    """Review notes on the caching PR:

| Concern | Status |
|---------|--------|
| Stampede protection | done |
| TTL jitter | missing |
| Cache key versioning | unclear |

Want me to add ±10% TTL jitter as a default?""",
    "Want me to add ±10% TTL jitter as a default?",
    note_a="asks for jitter range -> open",
    note_b="offers add jitter -> yes_no/propose",
    pb=True,
)

add(
    136,
    """Staging repro steps I tried:

1. Open settings
2. Toggle dark mode
3. Reload

Theme resets to light — can't match your report without more context.

Could you describe what you see after step 3?""",
    "Could you describe what you see after step 3?",
    """Staging repro steps I tried:

1. Open settings
2. Toggle dark mode
3. Reload

Theme resets to light — can't match your report without more context.

Could you clear site data and repeat those three steps?""",
    "Could you clear site data and repeat those three steps?",
    note_a="asks for description -> open",
    note_b="asks to clear/repeat -> yes_no",
)

add(
    137,
    """Data validation summary:

- 1.2M rows ingested
- 14k failed schema check
- Failures clustered on `event_date`

Which date format did the upstream export use?""",
    "Which date format did the upstream export use?",
    """Data validation summary:

- 1.2M rows ingested
- 14k failed schema check
- Failures clustered on `event_date`

Want me to quarantine the bad rows and re-ingest?""",
    "Want me to quarantine the bad rows and re-ingest?",
    note_a="asks which date format -> open",
    note_b="offers quarantine/re-ingest -> yes_no/propose",
    pb=True,
)

add(
    138,
    """Release candidate `rc.3` notes:

- Fixed race in checkout
- Known issue: Safari autofill
- Docs not updated

What should the Safari autofill workaround say in the release notes?""",
    "What should the Safari autofill workaround say in the release notes?",
    """Release candidate `rc.3` notes:

- Fixed race in checkout
- Known issue: Safari autofill
- Docs not updated

Shall I publish `rc.3` to the beta channel anyway?""",
    "Shall I publish `rc.3` to the beta channel anyway?",
    note_a="asks for workaround text -> open",
    note_b="offers publish beta -> yes_no/propose",
    pb=True,
)

add(
    139,
    """Customer report via support:

> Checkout button spins forever after applying coupon `SAVE20`

I can't find that coupon in staging.

Could you confirm the exact coupon code and cart total?""",
    "Could you confirm the exact coupon code and cart total?",
    """Customer report via support:

> Checkout button spins forever after applying coupon `SAVE20`

I can't find that coupon in staging.

Could you reproduce the flow with `SAVE20` on staging?""",
    "Could you reproduce the flow with `SAVE20` on staging?",
    note_a="asks to confirm code/total -> open",
    note_b="asks to reproduce -> yes_no",
)

add(
    140,
    """Migration dry-run results:

[CODE]
ALTER TABLE orders ADD COLUMN tax_cents INT;
-- would lock table for ~45s on prod
[CODE]

What maintenance window length can we use?""",
    "What maintenance window length can we use?",
    """Migration dry-run results:

[CODE]
ALTER TABLE orders ADD COLUMN tax_cents INT;
-- would lock table for ~45s on prod
[CODE]

Want me to schedule the migration for Saturday 02:00 UTC?""",
    "Want me to schedule the migration for Saturday 02:00 UTC?",
    note_a="asks for window length -> open",
    note_b="offers schedule -> yes_no/propose",
    pb=True,
)

# --- terse CLI + chatty markdown ---
add(
    141,
    "Fixed. Deploy green. One flaky e2e left.\n\nWhich scenario flakes?",
    "Which scenario flakes?",
    "Fixed. Deploy green. One flaky e2e left.\n\nWant me to mark it `@flaky`?",
    "Want me to mark it `@flaky`?",
    note_a="asks which scenario -> open",
    note_b="offers mark flaky -> yes_no/propose",
    pb=True,
)

add(
    142,
    "Cherry-picked `f8a2` onto `release/3.2`. Clean apply.\n\nWhat ticket does `f8a2` close?",
    "What ticket does `f8a2` close?",
    "Cherry-picked `f8a2` onto `release/3.2`. Clean apply.\n\nShall I push the release branch?",
    "Shall I push the release branch?",
    note_a="asks for ticket -> open",
    note_b="offers push -> yes_no/propose",
    pb=True,
)

add(
    143,
    """I've compared staging and prod configs side by side. Three diffs stand out:

- `MAX_UPLOAD_MB` (10 vs 50)
- `FEATURE_BETA` (off vs on)
- `LOG_LEVEL` (warn vs info)

**Which of those diffs is intentional for prod?**""",
    "Which of those diffs is intentional for prod?",
    """I've compared staging and prod configs side by side. Three diffs stand out:

- `MAX_UPLOAD_MB` (10 vs 50)
- `FEATURE_BETA` (off vs on)
- `LOG_LEVEL` (warn vs info)

**Could you try uploading a 30 MB file on staging to see if you get more info?**""",
    "Could you try uploading a 30 MB file on staging to see if you get more info?",
    note_a="asks which diffs intentional -> open",
    note_b="asks to try upload -> yes_no",
    da="m",
    db="m",
)

add(
    144,
    """Here's the failing curl from the ticket:

[CODE]
curl -H "Authorization: Bearer …" [URL]/api/v1/me
HTTP/2 403
[CODE]

What scopes does that token have?""",
    "What scopes does that token have?",
    """Here's the failing curl from the ticket:

[CODE]
curl -H "Authorization: Bearer …" [URL]/api/v1/me
HTTP/2 403
[CODE]

Can you regenerate the token and retry the request?""",
    "Can you regenerate the token and retry the request?",
    note_a="asks for scopes -> open",
    note_b="asks to regenerate/retry -> yes_no",
)

add(
    145,
    "Indexed 2.4k symbols. Broken xref on `ConfigLoader`.\n\nWhich doc page should `ConfigLoader` link to?",
    "Which doc page should `ConfigLoader` link to?",
    "Indexed 2.4k symbols. Broken xref on `ConfigLoader`.\n\nWant me to add a stub page for `ConfigLoader`?",
    "Want me to add a stub page for `ConfigLoader`?",
    note_a="asks which page -> open",
    note_b="offers stub page -> yes_no/propose",
    pb=True,
)

add(
    146,
    """Webpack bundle analyzer highlights:

- `moment` — 290 KB
- `lodash` — 110 KB
- `chart.js` — 85 KB

What is the bundle budget for the main chunk?""",
    "What is the bundle budget for the main chunk?",
    """Webpack bundle analyzer highlights:

- `moment` — 290 KB
- `lodash` — 110 KB
- `chart.js` — 85 KB

Want me to replace `moment` with `dayjs` on the critical path?""",
    "Want me to replace `moment` with `dayjs` on the critical path?",
    note_a="asks for budget -> open",
    note_b="offers replace moment -> yes_no/propose",
    pb=True,
)

add(
    147,
    "Spun up preview env at [URL]/pr-882.\n\nWhat account should I use to smoke-test checkout?",
    "What account should I use to smoke-test checkout?",
    "Spun up preview env at [URL]/pr-882.\n\nWant me to run the checkout smoke test against it?",
    "Want me to run the checkout smoke test against it?",
    note_a="asks for account -> open",
    note_b="offers run smoke test -> yes_no/propose",
    pb=True,
)

add(
    148,
    """Sentry issue grouped 400 events under:

> TypeError: Cannot read properties of undefined (reading 'id')

Which user action triggers it most often in your sessions?""",
    "Which user action triggers it most often in your sessions?",
    """Sentry issue grouped 400 events under:

> TypeError: Cannot read properties of undefined (reading 'id')

Want me to add a null guard at the read site?""",
    "Want me to add a null guard at the read site?",
    note_a="asks which action -> open",
    note_b="offers null guard -> yes_no/propose",
    pb=True,
)

add(
    149,
    "Could you build the native addon (linux-x64) and share the result?",
    "Could you build the native addon (linux-x64) and share the result?",
    "Could you build the native addon (linux-x64) on your machine?",
    "Could you build the native addon (linux-x64) on your machine?",
    note_a="build and share result -> open",
    note_b="build on machine without share -> yes_no",
    da="m",
    db="e",
)

add(
    150,
    "I'd like to confirm the rollout percentage before flipping traffic.\n\nWhat percentage of users should see the new checkout?",
    "What percentage of users should see the new checkout?",
    "I'd like to confirm the rollout percentage before flipping traffic.\n\nWant me to start a 5% canary on production?",
    "Want me to start a 5% canary on production?",
    note_a="asks for percentage -> open",
    note_b="offers canary -> yes_no/propose",
    pb=True,
)

assert len(PAIRS) == 100
assert [p["n"] for p in PAIRS] == list(range(51, 151))
