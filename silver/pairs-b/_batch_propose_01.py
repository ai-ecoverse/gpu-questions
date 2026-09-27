"""Handcrafted propose vs not-propose pairs pb0451–pb0525."""
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
    ka="y",
    kb="e",
    pa=True,
    pb=False,
    da="e",
    db="e",
    opts_a=None,
    opts_b=None,
    ms_a=False,
    ms_b=False,
    amb_a=False,
    amb_b=False,
):
    PAIRS.append(
        {
            "n": n,
            "boundary": "propose/not",
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
                        "opts": opts_a or [],
                    }
                ],
            },
            "b": {
                "text": text_b,
                "difficulty": db,
                "amb": amb_b,
                "contrast": note_b,
                "note": f"pair pb{n:04d}: {note_b}",
                "qs": [
                    {
                        "kind": kb,
                        "propose": pb,
                        "multi": ms_b,
                        "prompt": prompt_b,
                        "opts": opts_b or [],
                    }
                ],
            },
        }
    )


# --- database / migrations ---
add(
    451,
    "Migration `202503_add_vat` failed halfway on staging. The `invoices` table is half-altered.\n\n- **Roll back** using the down script\n- **Fix forward** with a patch migration\n\nShould I roll back using the down script?",
    "Should I roll back using the down script?",
    "Migration `202503_add_vat` failed halfway on staging. The `invoices` table is half-altered.\n\n- **Roll back** using the down script\n- **Fix forward** with a patch migration\n\nDo you want a rollback or a fix-forward migration?",
    "Do you want a rollback or a fix-forward migration?",
    note_a="agent offers rollback action -> yes_no/propose",
    note_b="user picks direction without agent commit -> either_or/not",
    opts_b=["a rollback", "a fix-forward migration"],
)

add(
    452,
    "Read-heavy dashboard queries hit Postgres on every page load.\n\n- **TTL cache** (5m) on aggregated metrics\n- **Write-through invalidation** when editors publish\n\nWant me to add TTL caching first?",
    "Want me to add TTL caching first?",
    "Read-heavy dashboard queries hit Postgres on every page load.\n\n- **TTL cache** (5m) on aggregated metrics\n- **Write-through invalidation** when editors publish\n\nWhich cache strategy do you prefer — TTL cache or write-through invalidation?",
    "Which cache strategy do you prefer — TTL cache or write-through invalidation?",
    note_a="agent offers to implement TTL -> yes_no/propose",
    note_b="preference between strategies -> either_or/not",
    opts_b=["TTL cache", "write-through invalidation"],
)

add(
    453,
    "Connection pool exhaustion shows up only under load tests.\n\n- **Raise** `max_connections` to 200\n- **PgBouncer** in transaction mode\n- **Read replica** for reporting queries\n\nWhich pool fix should I try first — raise max_connections, PgBouncer, or a read replica?",
    "Which pool fix should I try first — raise max_connections, PgBouncer, or a read replica?",
    "Connection pool exhaustion shows up only under load tests.\n\n- **Raise** `max_connections` to 200\n- **PgBouncer** in transaction mode\n- **Read replica** for reporting queries\n\nWhich pool fix do you prefer — raise max_connections, PgBouncer, or a read replica?",
    "Which pool fix do you prefer — raise max_connections, PgBouncer, or a read replica?",
    note_a="agent picks from menu -> multi_choice/propose",
    note_b="user preference across same options -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["raise max_connections", "PgBouncer", "a read replica"],
    opts_b=["raise max_connections", "PgBouncer", "a read replica"],
)

add(
    454,
    "Slow query log flags `SELECT * FROM events WHERE user_id = ?` with no index.\n\n```sql\nCREATE INDEX CONCURRENTLY idx_events_user_id ON events(user_id);\n```\n\nShall I add that concurrent index on staging?",
    "Shall I add that concurrent index on staging?",
    "Slow query log flags `SELECT * FROM events WHERE user_id = ?` with no index.\n\n```sql\nCREATE INDEX CONCURRENTLY idx_events_user_id ON events(user_id);\n```\n\nDo you want a concurrent index or a partial index on recent rows only?",
    "Do you want a concurrent index or a partial index on recent rows only?",
    note_a="agent offers to run DDL -> yes_no/propose",
    note_b="schema shape preference -> either_or/not",
    opts_b=["a concurrent index", "a partial index on recent rows only"],
    da="m",
)

add(
    455,
    "Replica lag spiked to 90s during the nightly ETL job.\n\nWant me to pause the ETL until replication catches up?",
    "Want me to pause the ETL until replication catches up?",
    "Replica lag spiked to 90s during the nightly ETL job.\n\nDo you want to pause ETL during peak hours or reschedule it to 03:00 UTC?",
    "Do you want to pause ETL during peak hours or reschedule it to 03:00 UTC?",
    note_a="agent offers pause -> yes_no/propose",
    note_b="scheduling preference -> either_or/not",
    opts_b=["pause ETL during peak hours", "reschedule it to 03:00 UTC"],
)

add(
    456,
    "Nullability drift: `users.phone` is `NOT NULL` in prod but nullable in staging.\n\n- **Align staging** to prod (add NOT NULL)\n- **Align prod** to staging (drop NOT NULL)\n\nWant me to align staging to prod?",
    "Want me to align staging to prod?",
    "Nullability drift: `users.phone` is `NOT NULL` in prod but nullable in staging.\n\n- **Align staging** to prod (add NOT NULL)\n- **Align prod** to staging (drop NOT NULL)\n\nWhich environment should be the source of truth — staging or prod?",
    "Which environment should be the source of truth — staging or prod?",
    note_a="agent offers staging alignment -> yes_no/propose",
    note_b="truth-source preference -> either_or/not",
    kb="e",
    opts_b=["staging", "prod"],
    da="m",
)

add(
    457,
    "Partition pruning fails on `events_2024` because the check constraint uses `timestamp` not `date`.\n\nShould I rewrite the constraint to use `date_trunc('day', created_at)`?",
    "Should I rewrite the constraint to use `date_trunc('day', created_at)`?",
    "Partition pruning fails on `events_2024` because the check constraint uses `timestamp` not `date`.\n\nDo you want daily partitions keyed on `date` or monthly partitions keyed on `year-month`?",
    "Do you want daily partitions keyed on `date` or monthly partitions keyed on `year-month`?",
    note_a="agent offers constraint rewrite -> yes_no/propose",
    note_b="partition granularity preference -> either_or/not",
    opts_b=["daily partitions keyed on `date`", "monthly partitions keyed on `year-month`"],
    da="m",
)

add(
    458,
    "Flyway checksum mismatch on `V12__add_coupon.sql` blocks deploy.\n\n- **Repair** the checksum in the history table\n- **Replace** the migration with a new versioned file\n\nWant me to repair the checksum?",
    "Want me to repair the checksum?",
    "Flyway checksum mismatch on `V12__add_coupon.sql` blocks deploy.\n\n- **Repair** the checksum in the history table\n- **Replace** the migration with a new versioned file\n\nWhich remediation do you prefer — repair the checksum or replace the migration file?",
    "Which remediation do you prefer — repair the checksum or replace the migration file?",
    note_a="agent offers repair -> yes_no/propose",
    note_b="remediation preference -> either_or/not",
    opts_b=["repair the checksum", "replace the migration file"],
)

add(
    459,
    "Row-level security policy on `documents` lets service accounts read everything.\n\nShall I tighten the policy to owner-only reads?",
    "Shall I tighten the policy to owner-only reads?",
    "Row-level security policy on `documents` lets service accounts read everything.\n\nDo you want owner-only reads or team-scoped reads with shared folders?",
    "Do you want owner-only reads or team-scoped reads with shared folders?",
    note_a="agent offers policy tighten -> yes_no/propose",
    note_b="access model preference -> either_or/not",
    opts_b=["owner-only reads", "team-scoped reads with shared folders"],
)

add(
    460,
    "Backup restore test failed: WAL segments after `2025-03-01T04:00Z` are missing from S3.\n\nWant me to open a ticket with infra and pause restores until the gap is filled?",
    "Want me to open a ticket with infra and pause restores until the gap is filled?",
    "Backup restore test failed: WAL segments after `2025-03-01T04:00Z` are missing from S3.\n\nDo you want to pause restores now or proceed with a point-in-time recovery to the last good segment?",
    "Do you want to pause restores now or proceed with a point-in-time recovery to the last good segment?",
    note_a="agent offers ticket + pause -> yes_no/propose",
    note_b="restore strategy preference -> either_or/not",
    opts_b=["pause restores now", "proceed with a point-in-time recovery to the last good segment"],
    da="m",
)

# --- API / backend ---
add(
    461,
    "Breaking change landed in `/v2/users` — the `name` field split into `given_name` and `family_name`.\n\n- **Bump** to `/v3`\n- **Feature-flag** the old shape for 30 days\n\nWant me to bump to `/v3`?",
    "Want me to bump to `/v3`?",
    "Breaking change landed in `/v2/users` — the `name` field split into `given_name` and `family_name`.\n\n- **Bump** to `/v3`\n- **Feature-flag** the old shape for 30 days\n\nWhich versioning path do you prefer — bump to `/v3` or feature-flag the old shape?",
    "Which versioning path do you prefer — bump to `/v3` or feature-flag the old shape?",
    note_a="agent offers v3 bump -> yes_no/propose",
    note_b="versioning preference -> either_or/not",
    opts_b=["bump to `/v3`", "feature-flag the old shape"],
)

add(
    462,
    "Stripe webhook handler returns 500 on duplicate `event.id` deliveries.\n\n```python\n@router.post('/hooks/stripe')\ndef stripe_hook(payload: dict):\n    process_event(payload)  # not idempotent\n```\n\nWant me to add idempotency keys and return 200 on duplicates?",
    "Want me to add idempotency keys and return 200 on duplicates?",
    "Stripe webhook handler returns 500 on duplicate `event.id` deliveries.\n\n```python\n@router.post('/hooks/stripe')\ndef stripe_hook(payload: dict):\n    process_event(payload)  # not idempotent\n```\n\nDo you want idempotency keys on the handler or move webhook processing to a queue?",
    "Do you want idempotency keys on the handler or move webhook processing to a queue?",
    note_a="agent offers idempotency fix -> yes_no/propose",
    note_b="handler vs queue preference -> either_or/not",
    opts_b=["idempotency keys on the handler", "move webhook processing to a queue"],
    da="m",
)

add(
    463,
    "OpenAPI spec drift: clients expect `GET /invoices/{id}/pdf` but the route is undocumented.\n\nShall I add the route to the published spec and regenerate the TS client?",
    "Shall I add the route to the published spec and regenerate the TS client?",
    "OpenAPI spec drift: clients expect `GET /invoices/{id}/pdf` but the route is undocumented.\n\nDo you want the PDF route documented in OpenAPI or exposed only via an internal SDK?",
    "Do you want the PDF route documented in OpenAPI or exposed only via an internal SDK?",
    note_a="agent offers spec + regen -> yes_no/propose",
    note_b="public vs internal exposure preference -> either_or/not",
    opts_b=["the PDF route documented in OpenAPI", "exposed only via an internal SDK"],
)

add(
    464,
    "Rate limiter uses a global token bucket; one noisy tenant blocks everyone.\n\n- **Per-tenant** buckets keyed by API key\n- **Weighted** buckets by plan tier\n- **Sliding window** per IP for anonymous routes\n\nWhich limiter model should I implement first — per-tenant buckets, weighted buckets, or sliding window per IP?",
    "Which limiter model should I implement first — per-tenant buckets, weighted buckets, or sliding window per IP?",
    "Rate limiter uses a global token bucket; one noisy tenant blocks everyone.\n\n- **Per-tenant** buckets keyed by API key\n- **Weighted** buckets by plan tier\n- **Sliding window** per IP for anonymous routes\n\nWhich limiter model do you prefer — per-tenant buckets, weighted buckets, or sliding window per IP?",
    "Which limiter model do you prefer — per-tenant buckets, weighted buckets, or sliding window per IP?",
    note_a="agent picks from limiter menu -> multi_choice/propose",
    note_b="limiter preference -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["per-tenant buckets", "weighted buckets", "sliding window per IP"],
    opts_b=["per-tenant buckets", "weighted buckets", "sliding window per IP"],
    da="m",
)

add(
    465,
    "GraphQL N+1 on `Order.items` shows 240 queries per request in traces.\n\nWant me to add a DataLoader for line items?",
    "Want me to add a DataLoader for line items?",
    "GraphQL N+1 on `Order.items` shows 240 queries per request in traces.\n\nDo you want a DataLoader batching layer or a single SQL join in the resolver?",
    "Do you want a DataLoader batching layer or a single SQL join in the resolver?",
    note_a="agent offers DataLoader -> yes_no/propose",
    note_b="batching vs join preference -> either_or/not",
    opts_b=["a DataLoader batching layer", "a single SQL join in the resolver"],
)

add(
    466,
    "gRPC deadline exceeded errors cluster on `BillingService.Charge`.\n\nShould I raise the client timeout from 2s to 5s and add retry with backoff?",
    "Should I raise the client timeout from 2s to 5s and add retry with backoff?",
    "gRPC deadline exceeded errors cluster on `BillingService.Charge`.\n\nDo you want longer client timeouts or server-side queueing for charge calls?",
    "Do you want longer client timeouts or server-side queueing for charge calls?",
    note_a="agent offers timeout + retry -> yes_no/propose",
    note_b="client vs server mitigation preference -> either_or/not",
    opts_b=["longer client timeouts", "server-side queueing for charge calls"],
)

add(
    467,
    "Pagination cursor leaks internal monotonic IDs in `next_page_token`.\n\n- **Opaque** base64 blob with HMAC\n- **Keyset** pagination on `(created_at, id)`\n\nWant me to switch to opaque signed cursors?",
    "Want me to switch to opaque signed cursors?",
    "Pagination cursor leaks internal monotonic IDs in `next_page_token`.\n\n- **Opaque** base64 blob with HMAC\n- **Keyset** pagination on `(created_at, id)`\n\nWhich pagination style do you prefer — opaque signed cursors or keyset pagination?",
    "Which pagination style do you prefer — opaque signed cursors or keyset pagination?",
    note_a="agent offers opaque cursors -> yes_no/propose",
    note_b="pagination style preference -> either_or/not",
    opts_b=["opaque signed cursors", "keyset pagination"],
    da="m",
)

add(
    468,
    "SSE stream for live notifications drops events when the client sleeps on mobile Safari.\n\nShall I add a `Last-Event-ID` resume handshake?",
    "Shall I add a `Last-Event-ID` resume handshake?",
    "SSE stream for live notifications drops events when the client sleeps on mobile Safari.\n\nDo you want SSE resume via `Last-Event-ID` or fall back to polling on mobile?",
    "Do you want SSE resume via `Last-Event-ID` or fall back to polling on mobile?",
    note_a="agent offers resume handshake -> yes_no/propose",
    note_b="transport preference -> either_or/not",
    opts_b=["SSE resume via `Last-Event-ID`", "fall back to polling on mobile"],
)

add(
    469,
    "OAuth scope `billing:write` is requested on login but never used.\n\nWant me to drop it from the authorize URL?",
    "Want me to drop it from the authorize URL?",
    "OAuth scope `billing:write` is requested on login but never used.\n\nDo you want to remove unused scopes now or split login vs billing consent screens?",
    "Do you want to remove unused scopes now or split login vs billing consent screens?",
    note_a="agent offers scope removal -> yes_no/propose",
    note_b="consent UX preference -> either_or/not",
    opts_b=["remove unused scopes now", "split login vs billing consent screens"],
)

add(
    470,
    "Health check at [URL] returns 200 while Redis is down.\n\nShould I fail the check when Redis ping misses?",
    "Should I fail the check when Redis ping misses?",
    "Health check at [URL] returns 200 while Redis is down.\n\nDo you want a strict health check (fail on Redis) or a degraded status with details?",
    "Do you want a strict health check (fail on Redis) or a degraded status with details?",
    note_a="agent offers strict check -> yes_no/propose",
    note_b="health semantics preference -> either_or/not",
    opts_b=["a strict health check (fail on Redis)", "a degraded status with details"],
)

# --- frontend / UI ---
add(
    471,
    "Lighthouse flags CLS 0.18 on the checkout page — the promo banner shifts the pay button.\n\nWant me to reserve space for the banner with a min-height skeleton?",
    "Want me to reserve space for the banner with a min-height skeleton?",
    "Lighthouse flags CLS 0.18 on the checkout page — the promo banner shifts the pay button.\n\nDo you want a reserved banner slot or load the banner only after the pay button mounts?",
    "Do you want a reserved banner slot or load the banner only after the pay button mounts?",
    note_a="agent offers skeleton fix -> yes_no/propose",
    note_b="layout strategy preference -> either_or/not",
    opts_b=["a reserved banner slot", "load the banner only after the pay button mounts"],
)

add(
    472,
    "Dark mode toggle ships behind `feature.dark_mode`.\n\n- **Internal** rollout to `@company.com` emails\n- **10%** canary on production\n- **100%** GA for all tenants\n\nWhich rollout slice should I enable first — internal, 10% canary, or GA?",
    "Which rollout slice should I enable first — internal, 10% canary, or GA?",
    "Dark mode toggle ships behind `feature.dark_mode`.\n\n- **Internal** rollout to `@company.com` emails\n- **10%** canary on production\n- **100%** GA for all tenants\n\nWhich rollout slice do you want — internal, 10% canary, or GA?",
    "Which rollout slice do you want — internal, 10% canary, or GA?",
    note_a="agent enables a slice -> multi_choice/propose",
    note_b="rollout preference -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["internal", "10% canary", "GA"],
    opts_b=["internal", "10% canary", "GA"],
)

add(
    473,
    "React error boundary catches nothing — the crash is in an async `useEffect` fetch.\n\nShall I wrap the fetch in an error boundary helper and surface a retry UI?",
    "Shall I wrap the fetch in an error boundary helper and surface a retry UI?",
    "React error boundary catches nothing — the crash is in an async `useEffect` fetch.\n\nDo you want an inline retry panel or redirect to a dedicated error route?",
    "Do you want an inline retry panel or redirect to a dedicated error route?",
    note_a="agent offers boundary + retry UI -> yes_no/propose",
    note_b="error UX preference -> either_or/not",
    opts_b=["an inline retry panel", "redirect to a dedicated error route"],
)

add(
    474,
    "Bundle analyzer shows `moment` and `date-fns` both in the vendor chunk.\n\nWant me to migrate remaining `moment` calls to `date-fns`?",
    "Want me to migrate remaining `moment` calls to `date-fns`?",
    "Bundle analyzer shows `moment` and `date-fns` both in the vendor chunk.\n\nDo you want to standardize on `date-fns` or keep `moment` for legacy screens only?",
    "Do you want to standardize on `date-fns` or keep `moment` for legacy screens only?",
    note_a="agent offers migration -> yes_no/propose",
    note_b="library standard preference -> either_or/not",
    opts_b=["standardize on `date-fns`", "keep `moment` for legacy screens only"],
)

add(
    475,
    "Virtualized table stutters when row height is dynamic.\n\n- **Fixed row height** with ellipsis overflow\n- **Measure pass** with `ResizeObserver` cache\n\nWant me to implement the measure pass with `ResizeObserver`?",
    "Want me to implement the measure pass with `ResizeObserver`?",
    "Virtualized table stutters when row height is dynamic.\n\n- **Fixed row height** with ellipsis overflow\n- **Measure pass** with `ResizeObserver` cache\n\nWhich row-height strategy do you prefer — fixed height or measure pass?",
    "Which row-height strategy do you prefer — fixed height or measure pass?",
    note_a="agent offers measure pass -> yes_no/propose",
    note_b="row-height preference -> either_or/not",
    opts_b=["fixed height", "measure pass"],
    da="m",
)

add(
    476,
    "Form validation messages are English-only; locale files exist for ES and DE.\n\nShould I wire `react-hook-form` errors through `i18next`?",
    "Should I wire `react-hook-form` errors through `i18next`?",
    "Form validation messages are English-only; locale files exist for ES and DE.\n\nDo you want client-side i18n for validation or server-returned localized messages?",
    "Do you want client-side i18n for validation or server-returned localized messages?",
    note_a="agent offers i18n wiring -> yes_no/propose",
    note_b="validation i18n preference -> either_or/not",
    opts_b=["client-side i18n for validation", "server-returned localized messages"],
)

add(
    477,
    "Modal focus trap leaks to the browser chrome on Firefox 128.\n\nWant me to patch the focus loop to include the dialog title?",
    "Want me to patch the focus loop to include the dialog title?",
    "Modal focus trap leaks to the browser chrome on Firefox 128.\n\nDo you want a focus-trap patch or switch to the native `<dialog>` element?",
    "Do you want a focus-trap patch or switch to the native `<dialog>` element?",
    note_a="agent offers focus patch -> yes_no/propose",
    note_b="modal implementation preference -> either_or/not",
    opts_b=["a focus-trap patch", "switch to the native `<dialog>` element"],
)

add(
    478,
    "Storybook snapshot for `Button` differs only in class order.\n\nShall I normalize Tailwind class order in the test serializer?",
    "Shall I normalize Tailwind class order in the test serializer?",
    "Storybook snapshot for `Button` differs only in class order.\n\nDo you want serializer normalization or switch snapshots to visual regression?",
    "Do you want serializer normalization or switch snapshots to visual regression?",
    note_a="agent offers serializer fix -> yes_no/propose",
    note_b="snapshot strategy preference -> either_or/not",
    opts_b=["serializer normalization", "switch snapshots to visual regression"],
)

add(
    479,
    "Chart tooltip overlaps the legend on narrow viewports.\n\n- **Flip** tooltip above the point on mobile\n- **Collapse** legend into a drawer\n\nWant me to flip the tooltip above the point on mobile?",
    "Want me to flip the tooltip above the point on mobile?",
    "Chart tooltip overlaps the legend on narrow viewports.\n\n- **Flip** tooltip above the point on mobile\n- **Collapse** legend into a drawer\n\nWhich mobile layout do you prefer — flip tooltip or collapse legend?",
    "Which mobile layout do you prefer — flip tooltip or collapse legend?",
    note_a="agent offers tooltip flip -> yes_no/propose",
    note_b="mobile layout preference -> either_or/not",
    opts_b=["flip tooltip", "collapse legend"],
)

add(
    480,
    "SSR hydration mismatch on the pricing page — client renders `$9` while server sent `$9.00`.\n\nShould I format currency with `Intl.NumberFormat` on both sides?",
    "Should I format currency with `Intl.NumberFormat` on both sides?",
    "SSR hydration mismatch on the pricing page — client renders `$9` while server sent `$9.00`.\n\nDo you want fixed two-decimal formatting or locale-aware currency display?",
    "Do you want fixed two-decimal formatting or locale-aware currency display?",
    note_a="agent offers Intl formatting -> yes_no/propose",
    note_b="currency display preference -> either_or/not",
    opts_b=["fixed two-decimal formatting", "locale-aware currency display"],
)

# --- git / CI ---
add(
    481,
    "Large refactor spans 38 files across api, worker, and ui layers.\n\nWant me to split the PR by layer?",
    "Want me to split the PR by layer?",
    "Large refactor spans 38 files across api, worker, and ui layers.\n\nDo you want one PR or split by layer — api, worker, and ui?",
    "Do you want one PR or split by layer — api, worker, and ui?",
    note_a="agent offers split -> yes_no/propose",
    note_b="PR shape preference -> either_or/not",
    opts_b=["one PR", "split by layer — api, worker, and ui"],
)

add(
    482,
    "CI matrix is red on three jobs:\n\n- **lint** — ruff import order\n- **test** — flaky websocket case\n- **build** — missing `VITE_API_URL`\n\nWant me to open the lint log first?",
    "Want me to open the lint log first?",
    "CI matrix is red on three jobs:\n\n- **lint** — ruff import order\n- **test** — flaky websocket case\n- **build** — missing `VITE_API_URL`\n\nWhich failing job should we triage first — lint, test, or build?",
    "Which failing job should we triage first — lint, test, or build?",
    note_a="agent offers to open lint log -> yes_no/propose",
    note_b="triage priority preference -> multi_choice/not",
    kb="m",
    opts_b=["lint", "test", "build"],
)

add(
    483,
    "Remote history diverged after the rebase.\n\n- **Force-with-lease** push to update the PR branch\n- **New branch** `feature/cache-v2` and abandon the old remote\n\nShall I force-with-lease push to update the PR branch?",
    "Shall I force-with-lease push to update the PR branch?",
    "Remote history diverged after the rebase.\n\n- **Force-with-lease** push to update the PR branch\n- **New branch** `feature/cache-v2` and abandon the old remote\n\nWhich route do you prefer — force-with-lease or a new branch?",
    "Which route do you prefer — force-with-lease or a new branch?",
    note_a="agent offers force-with-lease -> yes_no/propose",
    note_b="git route preference -> either_or/not",
    opts_b=["force-with-lease", "a new branch"],
)

add(
    484,
    "Pre-commit blocked the commit on `ruff format`.\n\nWant me to run `ruff format` on `cli/main.py` and recommit?",
    "Want me to run `ruff format` on `cli/main.py` and recommit?",
    "Pre-commit blocked the commit on `ruff format`.\n\nDo you want to fix formatting locally or skip hooks just this once?",
    "Do you want to fix formatting locally or skip hooks just this once?",
    note_a="agent offers format + recommit -> yes_no/propose",
    note_b="hook failure preference -> either_or/not",
    opts_b=["fix formatting locally", "skip hooks just this once"],
)

add(
    485,
    "Deploy workflow needs a manual approval gate before production.\n\nShould I add a GitHub Environment with required reviewers?",
    "Should I add a GitHub Environment with required reviewers?",
    "Deploy workflow needs a manual approval gate before production.\n\nDo you want GitHub Environment approvals or a chatops `/deploy approve` step?",
    "Do you want GitHub Environment approvals or a chatops `/deploy approve` step?",
    note_a="agent offers Environment gate -> yes_no/propose",
    note_b="approval mechanism preference -> either_or/not",
    opts_b=["GitHub Environment approvals", "a chatops `/deploy approve` step"],
)

add(
    486,
    "Cache restore missed on `~/.cargo/registry` — builds are cold every run.\n\nWant me to bump the cache key suffix to `v3`?",
    "Want me to bump the cache key suffix to `v3`?",
    "Cache restore missed on `~/.cargo/registry` — builds are cold every run.\n\nDo you want to bump the cache key or split caches per crate group?",
    "Do you want to bump the cache key or split caches per crate group?",
    note_a="agent offers cache key bump -> yes_no/propose",
    note_b="cache strategy preference -> either_or/not",
    opts_b=["bump the cache key", "split caches per crate group"],
)

add(
    487,
    "Signed release artifacts fail cosign verification in the deploy job.\n\n- **Rotate** the cosign key\n- **Pin** the digest in the workflow\n\nWant me to pin the digest in the workflow?",
    "Want me to pin the digest in the workflow?",
    "Signed release artifacts fail cosign verification in the deploy job.\n\n- **Rotate** the cosign key\n- **Pin** the digest in the workflow\n\nWhich remediation do you prefer — rotate the cosign key or pin the digest?",
    "Which remediation do you prefer — rotate the cosign key or pin the digest?",
    note_a="agent offers digest pin -> yes_no/propose",
    note_b="remediation preference -> either_or/not",
    opts_b=["rotate the cosign key", "pin the digest"],
)

add(
    488,
    "Concurrency group blocked two workflow runs on `deploy-staging`.\n\nShall I cancel the older run and let the latest finish?",
    "Shall I cancel the older run and let the latest finish?",
    "Concurrency group blocked two workflow runs on `deploy-staging`.\n\nWhich concurrency policy do you prefer — cancel the older run or queue until in-flight finishes?",
    "Which concurrency policy do you prefer — cancel the older run or queue until in-flight finishes?",
    note_a="agent offers cancel -> yes_no/propose",
    note_b="concurrency policy preference -> either_or/not",
    opts_b=["cancel the older run", "queue until in-flight finishes"],
)

add(
    489,
    "Tag `v2.4.0` is ready. Release checklist:\n\n1. **Annotated tag** with signed message\n2. **Lightweight tag** on HEAD\n\nShall I create the annotated tag?",
    "Shall I create the annotated tag?",
    "Tag `v2.4.0` is ready. Release checklist:\n\n1. **Annotated tag** with signed message\n2. **Lightweight tag** on HEAD\n\nDo you want an annotated tag or a lightweight tag on HEAD?",
    "Do you want an annotated tag or a lightweight tag on HEAD?",
    note_a="agent offers annotated tag -> yes_no/propose",
    note_b="tag style preference -> either_or/not",
    opts_b=["an annotated tag", "a lightweight tag on HEAD"],
)

add(
    490,
    "Fork sync is 41 commits behind upstream.\n\nWant me to merge `upstream/main` into our default branch?",
    "Want me to merge `upstream/main` into our default branch?",
    "Fork sync is 41 commits behind upstream.\n\nDo you want to merge upstream/main or rebase our feature branches onto upstream?",
    "Do you want to merge upstream/main or rebase our feature branches onto upstream?",
    note_a="agent offers merge -> yes_no/propose",
    note_b="sync strategy preference -> either_or/not",
    opts_b=["merge upstream/main", "rebase our feature branches onto upstream"],
)

# --- security / auth ---
add(
    491,
    "JWT access tokens live 24 hours with no refresh rotation.\n\nShould I shorten access tokens to 15 minutes and add refresh rotation?",
    "Should I shorten access tokens to 15 minutes and add refresh rotation?",
    "JWT access tokens live 24 hours with no refresh rotation.\n\nDo you want shorter access tokens or step-up MFA on sensitive routes?",
    "Do you want shorter access tokens or step-up MFA on sensitive routes?",
    note_a="agent offers token rotation -> yes_no/propose",
    note_b="auth hardening preference -> either_or/not",
    opts_b=["shorter access tokens", "step-up MFA on sensitive routes"],
)

add(
    492,
    "CSP report-only mode shows inline script violations on the admin panel.\n\nWant me to move inline handlers to external bundles and flip CSP to enforce?",
    "Want me to move inline handlers to external bundles and flip CSP to enforce?",
    "CSP report-only mode shows inline script violations on the admin panel.\n\nDo you want to enforce CSP now or whitelist admin inline scripts temporarily?",
    "Do you want to enforce CSP now or whitelist admin inline scripts temporarily?",
    note_a="agent offers CSP enforce -> yes_no/propose",
    note_b="CSP rollout preference -> either_or/not",
    opts_b=["enforce CSP now", "whitelist admin inline scripts temporarily"],
)

add(
    493,
    "Secrets scanner flagged a test API key committed in `fixtures/keys.json`.\n\nShall I rotate the key in Vault and replace the fixture with a placeholder?",
    "Shall I rotate the key in Vault and replace the fixture with a placeholder?",
    "Secrets scanner flagged a test API key committed in `fixtures/keys.json`.\n\nDo you want to rotate the key in Vault or scrub history with a filter-repo pass?",
    "Do you want to rotate the key in Vault or scrub history with a filter-repo pass?",
    note_a="agent offers rotate + placeholder -> yes_no/propose",
    note_b="incident response preference -> either_or/not",
    opts_b=["rotate the key in Vault", "scrub history with a filter-repo pass"],
    da="m",
)

add(
    494,
    "SAML metadata expired for the Okta IdP — logins fail with `InvalidSignature`.\n\nWant me to fetch fresh metadata from [URL] and update the config?",
    "Want me to fetch fresh metadata from [URL] and update the config?",
    "SAML metadata expired for the Okta IdP — logins fail with `InvalidSignature`.\n\nDo you want to refresh metadata from Okta or switch to OIDC for this tenant?",
    "Do you want to refresh metadata from Okta or switch to OIDC for this tenant?",
    note_a="agent offers metadata refresh -> yes_no/propose",
    note_b="IdP protocol preference -> either_or/not",
    opts_b=["refresh metadata from Okta", "switch to OIDC for this tenant"],
)

add(
    495,
    "RBAC matrix grants `editor` role delete on published content.\n\nShould I remove delete from `editor` and leave it admin-only?",
    "Should I remove delete from `editor` and leave it admin-only?",
    "RBAC matrix grants `editor` role delete on published content.\n\nDo you want delete admin-only or soft-delete with a 30-day retention window?",
    "Do you want delete admin-only or soft-delete with a 30-day retention window?",
    note_a="agent offers permission tighten -> yes_no/propose",
    note_b="delete policy preference -> either_or/not",
    opts_b=["delete admin-only", "soft-delete with a 30-day retention window"],
)

add(
    496,
    "Dependency audit shows `lodash@4.17.15` with a known prototype pollution CVE.\n\nWant me to bump to `4.17.21` and open a patch PR?",
    "Want me to bump to `4.17.21` and open a patch PR?",
    "Dependency audit shows `lodash@4.17.15` with a known prototype pollution CVE.\n\nDo you want a direct bump PR or replace lodash usages with native utilities?",
    "Do you want a direct bump PR or replace lodash usages with native utilities?",
    note_a="agent offers bump PR -> yes_no/propose",
    note_b="dependency fix preference -> either_or/not",
    opts_b=["a direct bump PR", "replace lodash usages with native utilities"],
)

add(
    497,
    "Session cookies ship without `SameSite=Strict` on the marketing subdomain.\n\nShall I set `SameSite=Strict` and `Secure` on all auth cookies?",
    "Shall I set `SameSite=Strict` and `Secure` on all auth cookies?",
    "Session cookies ship without `SameSite=Strict` on the marketing subdomain.\n\nDo you want `SameSite=Strict` everywhere or `Lax` on marketing and `Strict` on app?",
    "Do you want `SameSite=Strict` everywhere or `Lax` on marketing and `Strict` on app?",
    note_a="agent offers Strict + Secure -> yes_no/propose",
    note_b="SameSite policy preference -> either_or/not",
    opts_b=["`SameSite=Strict` everywhere", "`Lax` on marketing and `Strict` on app"],
)

add(
    498,
    "PII export endpoint lacks audit logging.\n\n- **Append-only** audit table\n- **Stream** events to the SIEM\n\nWhich audit sink should I wire up first — append-only table or SIEM stream?",
    "Which audit sink should I wire up first — append-only table or SIEM stream?",
    "PII export endpoint lacks audit logging.\n\n- **Append-only** audit table\n- **Stream** events to the SIEM\n\nWhich audit sink do you prefer — append-only table or SIEM stream?",
    "Which audit sink do you prefer — append-only table or SIEM stream?",
    note_a="agent picks audit sink -> either_or/propose",
    note_b="audit sink preference -> either_or/not",
    ka="e",
    kb="e",
    opts_a=["append-only table", "SIEM stream"],
    opts_b=["append-only table", "SIEM stream"],
)

add(
    499,
    "Pen test noted missing HSTS on the marketing site.\n\nShould I add a 31536000-second HSTS header with includeSubDomains?",
    "Should I add a 31536000-second HSTS header with includeSubDomains?",
    "Pen test noted missing HSTS on the marketing site.\n\nDo you want HSTS with includeSubDomains or preload registration first?",
    "Do you want HSTS with includeSubDomains or preload registration first?",
    note_a="agent offers HSTS header -> yes_no/propose",
    note_b="HSTS rollout preference -> either_or/not",
    opts_b=["HSTS with includeSubDomains", "preload registration first"],
)

add(
    500,
    "MFA enrollment rate is 62% for admin accounts.\n\nWant me to enforce TOTP enrollment on next login for admins?",
    "Want me to enforce TOTP enrollment on next login for admins?",
    "MFA enrollment rate is 62% for admin accounts.\n\nDo you want mandatory TOTP on next login or a grace period until April 1?",
    "Do you want mandatory TOTP on next login or a grace period until April 1?",
    note_a="agent offers enforced enrollment -> yes_no/propose",
    note_b="MFA rollout preference -> either_or/not",
    opts_b=["mandatory TOTP on next login", "a grace period until April 1"],
)

# --- devops / infra ---
add(
    501,
    "Docker image is 1.8GB — mostly dev dependencies in the runtime layer.\n\nWant me to convert the Dockerfile to a multi-stage build?",
    "Want me to convert the Dockerfile to a multi-stage build?",
    "Docker image is 1.8GB — mostly dev dependencies in the runtime layer.\n\nWhich slimming approach do you prefer — multi-stage build or strip dev deps in the final layer?",
    "Which slimming approach do you prefer — multi-stage build or strip dev deps in the final layer?",
    note_a="agent offers multi-stage conversion -> yes_no/propose",
    note_b="image slimming preference -> either_or/not",
    opts_b=["multi-stage build", "strip dev deps in the final layer"],
)

add(
    502,
    "Kubernetes pod OOMKilled on `worker-export` during large CSV jobs.\n\n- **Raise** memory limit to 4Gi\n- **Stream** rows instead of buffering\n- **Shard** export by date range\n\nWhich fix should I apply first — raise memory, stream rows, or shard by date?",
    "Which fix should I apply first — raise memory, stream rows, or shard by date?",
    "Kubernetes pod OOMKilled on `worker-export` during large CSV jobs.\n\n- **Raise** memory limit to 4Gi\n- **Stream** rows instead of buffering\n- **Shard** export by date range\n\nWhich fix do you prefer — raise memory, stream rows, or shard by date?",
    "Which fix do you prefer — raise memory, stream rows, or shard by date?",
    note_a="agent picks fix from menu -> multi_choice/propose",
    note_b="OOM fix preference -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["raise memory", "stream rows", "shard by date"],
    opts_b=["raise memory", "stream rows", "shard by date"],
    da="m",
)

add(
    503,
    "Terraform plan wants to replace the RDS instance because `engine_version` drifted.\n\nShall I pin `engine_version` and import the live version into state?",
    "Shall I pin `engine_version` and import the live version into state?",
    "Terraform plan wants to replace the RDS instance because `engine_version` drifted.\n\nDo you want to pin engine version in Terraform or upgrade the instance to match the code?",
    "Do you want to pin engine version in Terraform or upgrade the instance to match the code?",
    note_a="agent offers pin + import -> yes_no/propose",
    note_b="drift resolution preference -> either_or/not",
    opts_b=["pin engine version in Terraform", "upgrade the instance to match the code"],
    da="m",
)

add(
    504,
    "ALB health checks pass while the app returns 503 on `/ready`.\n\nWant me to point the target group health check at `/ready`?",
    "Want me to point the target group health check at `/ready`?",
    "ALB health checks pass while the app returns 503 on `/ready`.\n\nDo you want health checks on `/ready` or keep `/health` and fix readiness separately?",
    "Do you want health checks on `/ready` or keep `/health` and fix readiness separately?",
    note_a="agent offers health check path change -> yes_no/propose",
    note_b="health check semantics preference -> either_or/not",
    opts_b=["health checks on `/ready`", "keep `/health` and fix readiness separately"],
)

add(
    505,
    "CloudFront cache hit ratio is 12% for static assets — `Cache-Control` is missing.\n\nShould I add `Cache-Control: public, max-age=31536000, immutable` on hashed assets?",
    "Should I add `Cache-Control: public, max-age=31536000, immutable` on hashed assets?",
    "CloudFront cache hit ratio is 12% for static assets — `Cache-Control` is missing.\n\nDo you want long-lived cache headers on hashed assets or shorter TTL with manual purge?",
    "Do you want long-lived cache headers on hashed assets or shorter TTL with manual purge?",
    note_a="agent offers cache headers -> yes_no/propose",
    note_b="CDN TTL preference -> either_or/not",
    opts_b=["long-lived cache headers on hashed assets", "shorter TTL with manual purge"],
)

add(
    506,
    "Secrets in ECS task defs still reference plaintext env vars.\n\nWant me to migrate them to AWS Secrets Manager references?",
    "Want me to migrate them to AWS Secrets Manager references?",
    "Secrets in ECS task defs still reference plaintext env vars.\n\nDo you want Secrets Manager references or SSM Parameter Store secure strings?",
    "Do you want Secrets Manager references or SSM Parameter Store secure strings?",
    note_a="agent offers Secrets Manager migration -> yes_no/propose",
    note_b="secret storage preference -> either_or/not",
    opts_b=["Secrets Manager references", "SSM Parameter Store secure strings"],
)

add(
    507,
    "Log volume exceeded the Datadog ingestion quota.\n\n- **Sample** debug logs at 10%\n- **Drop** health-check access lines\n- **Raise** quota with finance approval\n\nWhich cost control should I implement first — sample debug logs, drop health checks, or raise quota?",
    "Which cost control should I implement first — sample debug logs, drop health checks, or raise quota?",
    "Log volume exceeded the Datadog ingestion quota.\n\n- **Sample** debug logs at 10%\n- **Drop** health-check access lines\n- **Raise** quota with finance approval\n\nWhich cost control do you prefer — sample debug logs, drop health checks, or raise quota?",
    "Which cost control do you prefer — sample debug logs, drop health checks, or raise quota?",
    note_a="agent implements cost control -> multi_choice/propose",
    note_b="cost control preference -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["sample debug logs", "drop health checks", "raise quota"],
    opts_b=["sample debug logs", "drop health checks", "raise quota"],
)

add(
    508,
    "Blue/green deploy script leaves old tasks running for 30 minutes.\n\nShall I drain connections and terminate old tasks after the smoke test passes?",
    "Shall I drain connections and terminate old tasks after the smoke test passes?",
    "Blue/green deploy script leaves old tasks running for 30 minutes.\n\nDo you want immediate teardown after smoke tests or a 30-minute rollback window?",
    "Do you want immediate teardown after smoke tests or a 30-minute rollback window?",
    note_a="agent offers drain + terminate -> yes_no/propose",
    note_b="teardown timing preference -> either_or/not",
    opts_b=["immediate teardown after smoke tests", "a 30-minute rollback window"],
)

add(
    509,
    "IAM policy on the CI role grants `s3:*` on `arn:aws:s3:::*`.\n\nWant me to scope it to the artifacts bucket only?",
    "Want me to scope it to the artifacts bucket only?",
    "IAM policy on the CI role grants `s3:*` on `arn:aws:s3:::*`.\n\nDo you want bucket-scoped permissions or move uploads to an OIDC-assumed role?",
    "Do you want bucket-scoped permissions or move uploads to an OIDC-assumed role?",
    note_a="agent offers policy scope -> yes_no/propose",
    note_b="IAM model preference -> either_or/not",
    opts_b=["bucket-scoped permissions", "move uploads to an OIDC-assumed role"],
    da="m",
)

add(
    510,
    "Prometheus alert `HighErrorRate` fires every deploy during rolling restarts.\n\nShould I add a 5-minute `for:` clause and exclude canary pods?",
    "Should I add a 5-minute `for:` clause and exclude canary pods?",
    "Prometheus alert `HighErrorRate` fires every deploy during rolling restarts.\n\nDo you want a longer `for:` window or silence alerts during deploy windows?",
    "Do you want a longer `for:` window or silence alerts during deploy windows?",
    note_a="agent offers alert tuning -> yes_no/propose",
    note_b="alert noise preference -> either_or/not",
    opts_b=["a longer `for:` window", "silence alerts during deploy windows"],
)

# --- testing / QA ---
add(
    511,
    "Flaky test `auth/session.spec.ts` fails 1-in-20 on CI.\n\nWant me to quarantine it with `@flaky` and open a tracking issue?",
    "Want me to quarantine it with `@flaky` and open a tracking issue?",
    "Flaky test `auth/session.spec.ts` fails 1-in-20 on CI.\n\nDo you want to quarantine the test or rewrite it with fake timers?",
    "Do you want to quarantine the test or rewrite it with fake timers?",
    note_a="agent offers quarantine -> yes_no/propose",
    note_b="flaky test strategy preference -> either_or/not",
    opts_b=["quarantine the test", "rewrite it with fake timers"],
)

add(
    512,
    "E2E suite runtime hit 42 minutes — over the 30-minute gate.\n\n- **Shard** across four workers\n- **Trim** to smoke paths only\n- **Parallelize** setup with global fixtures\n\nWhich speedup should I implement first — shard workers, trim to smoke, or parallelize setup?",
    "Which speedup should I implement first — shard workers, trim to smoke, or parallelize setup?",
    "E2E suite runtime hit 42 minutes — over the 30-minute gate.\n\n- **Shard** across four workers\n- **Trim** to smoke paths only\n- **Parallelize** setup with global fixtures\n\nWhich speedup do you prefer — shard workers, trim to smoke, or parallelize setup?",
    "Which speedup do you prefer — shard workers, trim to smoke, or parallelize setup?",
    note_a="agent picks speedup -> multi_choice/propose",
    note_b="speedup preference -> multi_choice/not",
    ka="m",
    kb="m",
    opts_a=["shard workers", "trim to smoke", "parallelize setup"],
    opts_b=["shard workers", "trim to smoke", "parallelize setup"],
)

add(
    513,
    "Coverage gate failed at 78% — threshold is 80% on `src/parsers/`.\n\nShall I add tests for the uncovered `parse_date` edge cases?",
    "Shall I add tests for the uncovered `parse_date` edge cases?",
    "Coverage gate failed at 78% — threshold is 80% on `src/parsers/`.\n\nDo you want new tests for `parse_date` or lower the threshold for this package?",
    "Do you want new tests for `parse_date` or lower the threshold for this package?",
    note_a="agent offers new tests -> yes_no/propose",
    note_b="coverage strategy preference -> either_or/not",
    opts_b=["new tests for `parse_date`", "lower the threshold for this package"],
)

add(
    514,
    "Contract test against the billing API fails on optional field `tax_id`.\n\nWant me to update the Pact fixture to allow null `tax_id`?",
    "Want me to update the Pact fixture to allow null `tax_id`?",
    "Contract test against the billing API fails on optional field `tax_id`.\n\nDo you want the fixture relaxed or the API to always return an empty string?",
    "Do you want the fixture relaxed or the API to always return an empty string?",
    note_a="agent offers fixture update -> yes_no/propose",
    note_b="contract mismatch preference -> either_or/not",
    opts_b=["the fixture relaxed", "the API to always return an empty string"],
)

add(
    515,
    "Load test at 500 RPS showed p99 latency 2.1s — SLO is 800ms.\n\nShould I profile the hot path and attach flamegraphs to the ticket?",
    "Should I profile the hot path and attach flamegraphs to the ticket?",
    "Load test at 500 RPS showed p99 latency 2.1s — SLO is 800ms.\n\nDo you want a profiling pass first or scale horizontally before optimizing?",
    "Do you want a profiling pass first or scale horizontally before optimizing?",
    note_a="agent offers profiling -> yes_no/propose",
    note_b="performance strategy preference -> either_or/not",
    opts_b=["a profiling pass first", "scale horizontally before optimizing"],
)

add(
    516,
    "Visual regression caught a 3px shift on the navbar logo.\n\nWant me to update the Percy baseline for desktop Chrome?",
    "Want me to update the Percy baseline for desktop Chrome?",
    "Visual regression caught a 3px shift on the navbar logo.\n\nDo you want to accept the new baseline or revert the logo CSS change?",
    "Do you want to accept the new baseline or revert the logo CSS change?",
    note_a="agent offers baseline update -> yes_no/propose",
    note_b="visual diff preference -> either_or/not",
    opts_b=["accept the new baseline", "revert the logo CSS change"],
)

add(
    517,
    "Mutation testing survived 40% of mutants in `discount.py`.\n\nShall I add property-based tests for coupon stacking rules?",
    "Shall I add property-based tests for coupon stacking rules?",
    "Mutation testing survived 40% of mutants in `discount.py`.\n\nDo you want property-based tests or table-driven cases for each stacking rule?",
    "Do you want property-based tests or table-driven cases for each stacking rule?",
    note_a="agent offers property tests -> yes_no/propose",
    note_b="test style preference -> either_or/not",
    opts_b=["property-based tests", "table-driven cases for each stacking rule"],
    da="m",
)

add(
    518,
    "Playwright trace from the failed checkout run is 180MB.\n\nWant me to trim traces to on-failure only in CI config?",
    "Want me to trim traces to on-failure only in CI config?",
    "Playwright trace from the failed checkout run is 180MB.\n\nDo you want on-failure traces only or retain full traces for one nightly job?",
    "Do you want on-failure traces only or retain full traces for one nightly job?",
    note_a="agent offers trace trim -> yes_no/propose",
    note_b="trace retention preference -> either_or/not",
    opts_b=["on-failure traces only", "retain full traces for one nightly job"],
)

add(
    519,
    "Snapshot test updated 14 files after the icon font swap.\n\nShould I accept all 14 snapshot updates in this PR?",
    "Should I accept all 14 snapshot updates in this PR?",
    "Snapshot test updated 14 files after the icon font swap.\n\nWhich snapshots did you expect to change — navigation, billing, or settings?",
    "Which snapshots did you expect to change — navigation, billing, or settings?",
    note_a="agent offers bulk accept -> yes_no/propose",
    note_b="expected change areas -> multi_choice/not",
    kb="m",
    opts_b=["navigation", "billing", "settings"],
    db="m",
)

add(
    520,
    "Chaos experiment killed a Redis pod — sessions survived but queue depth spiked.\n\nWant me to add an alert on queue depth > 1000?",
    "Want me to add an alert on queue depth > 1000?",
    "Chaos experiment killed a Redis pod — sessions survived but queue depth spiked.\n\nDo you want a queue-depth alert or automatic consumer scaling?",
    "Do you want a queue-depth alert or automatic consumer scaling?",
    note_a="agent offers alert -> yes_no/propose",
    note_b="resilience preference -> either_or/not",
    opts_b=["a queue-depth alert", "automatic consumer scaling"],
)

# --- docs / naming / misc ---
add(
    521,
    "I'd like to confirm the product name before the rename lands in strings and docs.\n\nWant me to rename it to **Pulse** everywhere?",
    "Want me to rename it to **Pulse** everywhere?",
    "I'd like to confirm the product name before the rename lands in strings and docs.\n\nWhat should we call the feature in the UI?",
    "What should we call the feature in the UI?",
    note_a="agent offers rename -> yes_no/propose",
    note_b="asks for name -> open/not",
    kb="o",
)

add(
    522,
    "README install steps reference `pnpm` but the repo ships a `package-lock.json`.\n\nShall I rewrite the install section for npm and drop pnpm mentions?",
    "Shall I rewrite the install section for npm and drop pnpm mentions?",
    "README install steps reference `pnpm` but the repo ships a `package-lock.json`.\n\nDo you want npm-first docs or document both npm and pnpm workflows?",
    "Do you want npm-first docs or document both npm and pnpm workflows?",
    note_a="agent offers npm rewrite -> yes_no/propose",
    note_b="docs scope preference -> either_or/not",
    opts_b=["npm-first docs", "document both npm and pnpm workflows"],
)

add(
    523,
    "I can show the refactor diff as a unified patch or walk through each hunk.\n\nWant a unified patch or a walkthrough of each hunk?",
    "Want a unified patch or a walkthrough of each hunk?",
    "I can show the refactor diff as a unified patch or walk through each hunk.\n\nWhich format do you prefer for the summary — unified patch or hunk-by-hunk walkthrough?",
    "Which format do you prefer for the summary — unified patch or hunk-by-hunk walkthrough?",
    note_a="agent offers deliverable choice -> either_or/propose",
    note_b="format preference without agent commit -> either_or/not",
    ka="e",
    opts_a=["a unified patch", "a walkthrough of each hunk"],
    opts_b=["unified patch", "hunk-by-hunk walkthrough"],
)

add(
    524,
    "Release notes draft covers March fixes but not the billing migration.\n\nWant me to add a **Billing migration** section with rollback steps?",
    "Want me to add a **Billing migration** section with rollback steps?",
    "Release notes draft covers March fixes but not the billing migration.\n\nDo you want billing called out in release notes or a separate runbook link?",
    "Do you want billing called out in release notes or a separate runbook link?",
    note_a="agent offers section add -> yes_no/propose",
    note_b="documentation placement preference -> either_or/not",
    opts_b=["billing called out in release notes", "a separate runbook link"],
)

add(
    525,
    "Search index lag is ~4 minutes after publish.\n\nWant me to wire up binlog tail indexing or schedule a batch rebuild every 15 minutes?",
    "Want me to wire up binlog tail indexing or schedule a batch rebuild every 15 minutes?",
    "Search index lag is ~4 minutes after publish.\n\nWhich indexing model do you prefer — near-real-time via binlog or batch rebuild every 15 minutes?",
    "Which indexing model do you prefer — near-real-time via binlog or batch rebuild every 15 minutes?",
    note_a="agent offers either deliverable -> either_or/propose",
    note_b="indexing model preference -> either_or/not",
    ka="e",
    opts_a=["wire up binlog tail indexing", "schedule a batch rebuild every 15 minutes"],
    opts_b=["near-real-time via binlog", "batch rebuild every 15 minutes"],
    da="m",
)

assert len(PAIRS) == 75
assert [p["n"] for p in PAIRS] == list(range(451, 526))
