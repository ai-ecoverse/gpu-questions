"""Handcrafted list_offered vs background_list pairs pb0351–pb0450."""
from __future__ import annotations

PAIRS = []


def add(n, text_a, prompt_a, opts_a, text_b, prompt_b, *, note_a, note_b,
        ka="m", kb="y", pa=False, pb=True, da="e", db="e", ms_a=False, amb_a=False, amb_b=False):
    PAIRS.append({
        "n": n, "boundary": "list_offered/background_list",
        "a": {"text": text_a, "difficulty": da, "amb": amb_a, "contrast": note_a,
              "note": f"pair pb{n:04d}: {note_a}",
              "qs": [{"kind": ka, "propose": pa, "multi": ms_a, "prompt": prompt_a, "opts": opts_a}]},
        "b": {"text": text_b, "difficulty": db, "amb": amb_b, "contrast": note_b,
              "note": f"pair pb{n:04d}: {note_b}",
              "qs": [{"kind": kb, "propose": pb, "prompt": prompt_b, "opts": []}]},
    })


add(
    351,
    'The API gateway security review surfaced three auth gaps:\n\n- **OAuth device flow** — PKCE missing on token exchange\n- **Session cookies** — `SameSite=None` without `Secure` on `/callback` and `/sso`\n- **JWT rotation** — refresh tokens never expire\n\nWhich fix should I tackle first?',
    'Which fix should I tackle first?',
    ['OAuth device flow', 'Session cookies', 'JWT rotation'],
    'The API gateway security review surfaced three auth gaps:\n\n- **OAuth device flow** — PKCE missing on token exchange\n- **Session cookies** — `SameSite=None` without `Secure` on `/callback` and `/sso`\n- **JWT rotation** — refresh tokens never expire\n\nWant me to open a tracking ticket for these findings?',
    'Want me to open a tracking ticket for these findings?',
    note_a='offered fix list -> multi_choice/propose',
    note_b='same list as review findings; ticket offer -> yes_no',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    352,
    'CSP violations in production cluster around two directives:\n\n- **script-src** — inline handlers from legacy checkout widget\n- **connect-src** — websocket to `analytics.example.com` blocked\n\nShould I tighten `script-src` with nonces or whitelist the checkout host?',
    'Should I tighten `script-src` with nonces or whitelist the checkout host?',
    ['tighten `script-src` with nonces', 'whitelist the checkout host'],
    'CSP violations in production cluster around two directives:\n\n- **script-src** — inline handlers from legacy checkout widget\n- **connect-src** — websocket to `analytics.example.com` blocked\n\nShall I deploy the CSP report-only header first and watch for a day?',
    'Shall I deploy the CSP report-only header first and watch for a day?',
    note_a='two remediation paths -> either_or/propose',
    note_b='diagnostic list; deploy report-only -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    353,
    'Secrets scan on `main` flagged four leaked patterns:\n\n- **AWS access key** — in `scripts/backup.sh` commit `f4a2`\n- **Stripe test key** — embedded in `fixtures/payments.json`\n- **Slack webhook** — hard-coded in `deploy/notify.ts`\n- **Private PEM** — checked into `certs/dev.pem`\n\nWhich credential should I rotate and purge from history first?',
    'Which credential should I rotate and purge from history first?',
    ['AWS access key', 'Stripe test key', 'Slack webhook', 'Private PEM'],
    'Secrets scan on `main` flagged four leaked patterns:\n\n- **AWS access key** — in `scripts/backup.sh` commit `f4a2`\n- **Stripe test key** — embedded in `fixtures/payments.json`\n- **Slack webhook** — hard-coded in `deploy/notify.ts`\n- **Private PEM** — checked into `certs/dev.pem`\n\nWant me to run `git filter-repo` on the affected paths after you confirm?',
    'Want me to run `git filter-repo` on the affected paths after you confirm?',
    note_a='selectable leak targets -> multi_choice',
    note_b='scan findings as background; filter-repo offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    354,
    "WAF rule tuning after last week's bot spike left two candidate blocks:\n\n- Geo block — deny ASNs from regions with no customers\n- Rate limit — cap `/login` at 20 req/min per IP\n\nWhich WAF change should I ship to staging first?",
    'Which WAF change should I ship to staging first?',
    ['Geo block', 'Rate limit'],
    "WAF rule tuning after last week's bot spike left two candidate blocks:\n\n- Geo block — deny ASNs from regions with no customers\n- Rate limit — cap `/login` at 20 req/min per IP\n\nShould I leave the WAF in count mode overnight and review the dashboard?",
    'Should I leave the WAF in count mode overnight and review the dashboard?',
    note_a='two WAF options -> either_or/propose',
    note_b='candidate rules as context; count mode -> yes_no',
    ka='e',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    355,
    'mTLS rollout plan for service mesh has three phases:\n\n- **Pilot** — enable strict mTLS on `payments` namespace only\n- **Expand** — add `auth` and `billing` with permissive mode\n- **Enforce** — reject plaintext sidecar traffic cluster-wide\n\nWhich phase do you want me to start implementing?',
    'Which phase do you want me to start implementing?',
    ['Pilot', 'Expand', 'Enforce'],
    'mTLS rollout plan for service mesh has three phases:\n\n- **Pilot** — enable strict mTLS on `payments` namespace only\n- **Expand** — add `auth` and `billing` with permissive mode\n- **Enforce** — reject plaintext sidecar traffic cluster-wide\n\nWant me to draft the runbook before we touch prod?',
    'Want me to draft the runbook before we touch prod?',
    note_a='phases offered as choices -> multi_choice/propose',
    note_b='phases as plan background; runbook offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    356,
    'SAST pipeline reported critical findings in the auth module:\n\n- **SQL injection** — `UserRepository.search` concatenates input\n- **Path traversal** — `/export` accepts unsanitized `filename`\n- **Hard-coded secret** — HMAC key in `token.rs`\n- **Insecure deserialization** — pickle load in admin import\n\nWhich finding(s) should I patch in this PR?',
    'Which finding(s) should I patch in this PR?',
    ['SQL injection', 'Path traversal', 'Hard-coded secret', 'Insecure deserialization'],
    'SAST pipeline reported critical findings in the auth module:\n\n- **SQL injection** — `UserRepository.search` concatenates input\n- **Path traversal** — `/export` accepts unsanitized `filename`\n- **Hard-coded secret** — HMAC key in `token.rs`\n- **Insecure deserialization** — pickle load in admin import\n\nShall I attach the SARIF export to the security channel?',
    'Shall I attach the SARIF export to the security channel?',
    note_a='multi-select from finding list -> multi_choice/ms/propose',
    note_b='findings inventory; share SARIF -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=True,
)

add(
    357,
    'Rate-limiting design for the public API offers:\n\n1. **Token bucket** — per API key with burst allowance\n2. **Sliding window** — per IP with Redis counters\n3. **Adaptive throttle** — slow down clients returning 429s\n\nWhich rate-limit strategy should I prototype?',
    'Which rate-limit strategy should I prototype?',
    ['Token bucket', 'Sliding window', 'Adaptive throttle'],
    'Rate-limiting design for the public API offers:\n\n1. **Token bucket** — per API key with burst allowance\n2. **Sliding window** — per IP with Redis counters\n3. **Adaptive throttle** — slow down clients returning 429s\n\nWant me to load-test the current endpoint to establish a baseline?',
    'Want me to load-test the current endpoint to establish a baseline?',
    note_a='strategy list as choices -> multi_choice/propose',
    note_b='design options as background; load-test offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    358,
    'Supply-chain audit flagged two dependency risks:\n\n- **Unpinned transitive** — `lodash` pulled at `^4.17.0` through `react-scripts`\n- **Abandoned package** — `request@2.88` with no maintainer\n\nShould I pin with lockfile overrides or replace `request` with `undici`?',
    'Should I pin with lockfile overrides or replace `request` with `undici`?',
    ['pin with lockfile overrides', 'replace `request` with `undici`'],
    'Supply-chain audit flagged two dependency risks:\n\n- **Unpinned transitive** — `lodash` pulled at `^4.17.0` through `react-scripts`\n- **Abandoned package** — `request@2.88` with no maintainer\n\nShall I open an SBOM diff PR so security can sign off?',
    'Shall I open an SBOM diff PR so security can sign off?',
    note_a='two remediation paths -> either_or/propose',
    note_b='audit items as context; SBOM PR -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    359,
    'Tracing gaps after the checkout latency spike:\n\n1. **Missing parent span** — `POST /pay` never links to Stripe call\n2. **High-cardinality tag** — `user.email` on every span\n3. **Sampler misconfig** — tail sampling drops error traces\n\nWhich tracing fix should I land first?',
    'Which tracing fix should I land first?',
    ['Missing parent span', 'High-cardinality tag', 'Sampler misconfig'],
    'Tracing gaps after the checkout latency spike:\n\n1. **Missing parent span** — `POST /pay` never links to Stripe call\n2. **High-cardinality tag** — `user.email` on every span\n3. **Sampler misconfig** — tail sampling drops error traces\n\nWant me to enable debug exporter locally and capture one checkout trace?',
    'Want me to enable debug exporter locally and capture one checkout trace?',
    note_a='fix menu -> multi_choice/propose',
    note_b='gap analysis background; debug trace -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    360,
    'Metrics cardinality review recommends trimming these labels:\n\n- **`pod_name`** — unique per replica on histograms\n- **`request_id`** — attached to counter `http_requests`\n- **`build_sha`** — changes every deploy on gauges\n\nWhich label(s) should I drop from the hot path metrics?',
    'Which label(s) should I drop from the hot path metrics?',
    ['`pod_name`', '`request_id`', '`build_sha`'],
    'Metrics cardinality review recommends trimming these labels:\n\n- **`pod_name`** — unique per replica on histograms\n- **`request_id`** — attached to counter `http_requests`\n- **`build_sha`** — changes every deploy on gauges\n\nShall I push the recording rules to staging and validate scrape size?',
    'Shall I push the recording rules to staging and validate scrape size?',
    note_a='multi-select label cleanup -> multi_choice/ms',
    note_b='review recommendations as background; push rules -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=True,
)

add(
    361,
    'Log correlation is broken between two services:\n\n- **Missing trace ID** — nginx strips `traceparent` header\n- **Timezone drift** — worker logs UTC, API logs local\n- **JSON parser errors** — multiline stack traces split events\n\nWhich correlation issue should I fix first?',
    'Which correlation issue should I fix first?',
    ['Missing trace ID', 'Timezone drift', 'JSON parser errors'],
    'Log correlation is broken between two services:\n\n- **Missing trace ID** — nginx strips `traceparent` header\n- **Timezone drift** — worker logs UTC, API logs local\n- **JSON parser errors** — multiline stack traces split events\n\nWant me to tail both log streams during the next deploy window?',
    'Want me to tail both log streams during the next deploy window?',
    note_a='selectable fixes -> multi_choice/propose',
    note_b='issue inventory; tail logs -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    362,
    'SLO burn alerts need tuning — current candidates:\n\n- **Fast burn** — 2% budget in 1 hour pages on-call\n- **Slow burn** — 10% budget in 6 hours opens ticket\n- **Multi-window** — combine 5m and 1h error rates\n\nWhich alert policy should I enable for checkout?',
    'Which alert policy should I enable for checkout?',
    ['Fast burn', 'Slow burn', 'Multi-window'],
    'SLO burn alerts need tuning — current candidates:\n\n- **Fast burn** — 2% budget in 1 hour pages on-call\n- **Slow burn** — 10% budget in 6 hours opens ticket\n- **Multi-window** — combine 5m and 1h error rates\n\nShould I silence the noisy `search` SLO while we tune?',
    'Should I silence the noisy `search` SLO while we tune?',
    note_a='alert policies as choices -> multi_choice/propose',
    note_b='tuning candidates as plan; silence offer -> yes_no',
    ka='m',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    363,
    'Dashboard refresh for the on-call board lists:\n\n- **Golden signals** — latency, traffic, errors, saturation per service\n- **Dependency map** — upstream/downstream health tiles\n- **Incident timeline** — deploy markers overlaid on error rate\n\nWhich panel should I add to the primary dashboard?',
    'Which panel should I add to the primary dashboard?',
    ['Golden signals', 'Dependency map', 'Incident timeline'],
    'Dashboard refresh for the on-call board lists:\n\n- **Golden signals** — latency, traffic, errors, saturation per service\n- **Dependency map** — upstream/downstream health tiles\n- **Incident timeline** — deploy markers overlaid on error rate\n\nWant me to snapshot the current dashboard JSON before editing?',
    'Want me to snapshot the current dashboard JSON before editing?',
    note_a='panel options -> multi_choice/propose',
    note_b='panel plan as background; snapshot offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    364,
    'Profiling the memory leak narrowed it to two hotspots:\n\n- gRPC buffer pool — retained slices after stream cancel\n- Image decode cache — unbounded map in thumbnail worker\n\nShould I profile with pprof heap or capture allocations with py-spy?',
    'Should I profile with pprof heap or capture allocations with py-spy?',
    ['profile with pprof heap', 'capture allocations with py-spy'],
    'Profiling the memory leak narrowed it to two hotspots:\n\n- gRPC buffer pool — retained slices after stream cancel\n- Image decode cache — unbounded map in thumbnail worker\n\nShall I leave continuous profiling enabled on the canary pod?',
    'Shall I leave continuous profiling enabled on the canary pod?',
    note_a='two profiling approaches -> either_or/propose',
    note_b='hotspot findings; enable continuous profiling -> yes_no',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    365,
    'Synthetic checks failing from three regions:\n\n- **us-east-1** — TLS handshake timeout to CDN\n- **eu-west-1** — 401 on health endpoint missing bearer\n- **ap-south-1** — DNS resolves to decommissioned LB\n\nWhich region failure should I investigate first?',
    'Which region failure should I investigate first?',
    ['us-east-1', 'eu-west-1', 'ap-south-1'],
    'Synthetic checks failing from three regions:\n\n- **us-east-1** — TLS handshake timeout to CDN\n- **eu-west-1** — 401 on health endpoint missing bearer\n- **ap-south-1** — DNS resolves to decommissioned LB\n\nWant me to rerun synthetics with verbose HAR capture?',
    'Want me to rerun synthetics with verbose HAR capture?',
    note_a='region list as selectable -> multi_choice/propose',
    note_b='failure summary; HAR rerun -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    366,
    'Error budget policy options for Q4:\n\n- **Freeze deploys** — when budget < 10% for tier-1\n- **Feature flags only** — block risky merges, allow fixes\n- **Auto rollback** — revert last deploy on burn spike\n\nWhich policy should I document in the SRE playbook?',
    'Which policy should I document in the SRE playbook?',
    ['Freeze deploys', 'Feature flags only', 'Auto rollback'],
    'Error budget policy options for Q4:\n\n- **Freeze deploys** — when budget < 10% for tier-1\n- **Feature flags only** — block risky merges, allow fixes\n- **Auto rollback** — revert last deploy on burn spike\n\nShall I schedule a review with product once the draft is ready?',
    'Shall I schedule a review with product once the draft is ready?',
    note_a='policy choices -> multi_choice',
    note_b='policy options as plan; schedule review -> yes_no/propose',
    ka='m',
    pa=False,
    pb=True,
    ms_a=False,
)

add(
    367,
    "Training pipeline failures from last night's run:\n\n1. **Data shard OOM** — batch size 512 on 16GB GPU\n2. **Label leakage** — validation split includes future timestamps\n3. **Checkpoint corruption** — partial write at epoch 40\n\nWhich blocker should I fix before retraining?",
    'Which blocker should I fix before retraining?',
    ['Data shard OOM', 'Label leakage', 'Checkpoint corruption'],
    "Training pipeline failures from last night's run:\n\n1. **Data shard OOM** — batch size 512 on 16GB GPU\n2. **Label leakage** — validation split includes future timestamps\n3. **Checkpoint corruption** — partial write at epoch 40\n\nWant me to resume from the last good checkpoint and log metrics?",
    'Want me to resume from the last good checkpoint and log metrics?',
    note_a='blocker list as choices -> multi_choice/propose',
    note_b='failure log; resume training -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    368,
    'Model registry promotion criteria still open:\n\n- **Offline AUC** — must beat champion by 0.02\n- **Latency p99** — under 120ms on T4\n- **Fairness audit** — demographic parity within 5%\n\nWhich gate should I implement in the CI promotion job?',
    'Which gate should I implement in the CI promotion job?',
    ['Offline AUC', 'Latency p99', 'Fairness audit'],
    'Model registry promotion criteria still open:\n\n- **Offline AUC** — must beat champion by 0.02\n- **Latency p99** — under 120ms on T4\n- **Fairness audit** — demographic parity within 5%\n\nShall I tag the current champion as `baseline-v3` before changes?',
    'Shall I tag the current champion as `baseline-v3` before changes?',
    note_a='gate options -> multi_choice/propose',
    note_b='criteria as background; tag champion -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    369,
    'Feature store drift detected on three columns:\n\n- **`user_tenure_days`** — mean shifted +18% week-over-week\n- **`cart_value`** — null rate jumped to 12%\n- **`device_os`** — new category `visionOS` unmapped\n\nWhich feature should I backfill and recompute first?',
    'Which feature should I backfill and recompute first?',
    ['`user_tenure_days`', '`cart_value`', '`device_os`'],
    'Feature store drift detected on three columns:\n\n- **`user_tenure_days`** — mean shifted +18% week-over-week\n- **`cart_value`** — null rate jumped to 12%\n- **`device_os`** — new category `visionOS` unmapped\n\nWant me to snapshot the offline store before backfill?',
    'Want me to snapshot the offline store before backfill?',
    note_a='feature pick list -> multi_choice/propose',
    note_b='drift report; snapshot offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    370,
    'Inference scaling options for the ranking model:\n\n- **Horizontal pods** — HPA on GPU utilization\n- **Batching server** — dynamic batch with 50ms wait\n- **Edge cache** — CDN for popular item embeddings\n\nWhich scaling approach should I benchmark?',
    'Which scaling approach should I benchmark?',
    ['Horizontal pods', 'Batching server', 'Edge cache'],
    'Inference scaling options for the ranking model:\n\n- **Horizontal pods** — HPA on GPU utilization\n- **Batching server** — dynamic batch with 50ms wait\n- **Edge cache** — CDN for popular item embeddings\n\nShould I run load tests against the staging endpoint tonight?',
    'Should I run load tests against the staging endpoint tonight?',
    note_a='scaling choices -> multi_choice/propose',
    note_b='options as design notes; load test -> yes_no',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    371,
    'Hyperparameter search budget can go to:\n\n1. **Learning rate sweep** — 1e-5 to 1e-3 log scale\n2. **Dropout grid** — 0.1, 0.2, 0.3 on attention layers\n\nShould I spend the next 20 GPU-hours on LR sweep or dropout grid?',
    'Should I spend the next 20 GPU-hours on LR sweep or dropout grid?',
    ['Learning rate sweep', 'Dropout grid'],
    'Hyperparameter search budget can go to:\n\n1. **Learning rate sweep** — 1e-5 to 1e-3 log scale\n2. **Dropout grid** — 0.1, 0.2, 0.3 on attention layers\n\nWant me to queue the job on the shared cluster with preemptible nodes?',
    'Want me to queue the job on the shared cluster with preemptible nodes?',
    note_a='two search arms -> either_or/propose',
    note_b='budget allocation background; queue job -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    372,
    'ONNX export blockers for the vision model:\n\n- **Dynamic axes** — batch dimension not marked\n- **Custom op** — `DeformConv` missing converter\n- **Quantization** — INT8 calibrator needs 500 images\n\nWhich export issue should I resolve first?',
    'Which export issue should I resolve first?',
    ['Dynamic axes', 'Custom op', 'Quantization'],
    'ONNX export blockers for the vision model:\n\n- **Dynamic axes** — batch dimension not marked\n- **Custom op** — `DeformConv` missing converter\n- **Quantization** — INT8 calibrator needs 500 images\n\nShall I pin the export to opset 17 and retry?',
    'Shall I pin the export to opset 17 and retry?',
    note_a='blocker menu -> multi_choice/propose',
    note_b='export status; retry offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    373,
    'Offline eval metrics disagree on the new ranker:\n\n- **NDCG@10** — +3.2% vs champion\n- **Coverage** — -8% long-tail items surfaced\n- **Calibration** — ECE worsened on mobile traffic\n\nWhich metric should drive the launch decision?',
    'Which metric should drive the launch decision?',
    ['NDCG@10', 'Coverage', 'Calibration'],
    'Offline eval metrics disagree on the new ranker:\n\n- **NDCG@10** — +3.2% vs champion\n- **Coverage** — -8% long-tail items surfaced\n- **Calibration** — ECE worsened on mobile traffic\n\nWant me to generate the side-by-side eval report PDF?',
    'Want me to generate the side-by-side eval report PDF?',
    note_a='metric choice -> multi_choice',
    note_b='eval summary; PDF offer -> yes_no/propose',
    ka='m',
    pa=False,
    pb=True,
    ms_a=False,
)

add(
    374,
    'Data labeling queue has three urgent buckets:\n\n- **Safety** — 2.1k toxic chat examples\n- **OCR** — receipt photos with skew\n- **Audio** — noisy call-center clips\n\nWhich bucket(s) should I send to the vendor this week?',
    'Which bucket(s) should I send to the vendor this week?',
    ['Safety', 'OCR', 'Audio'],
    'Data labeling queue has three urgent buckets:\n\n- **Safety** — 2.1k toxic chat examples\n- **OCR** — receipt photos with skew\n- **Audio** — noisy call-center clips\n\nShall I pause auto-labeling until QA signs off the guidelines?',
    'Shall I pause auto-labeling until QA signs off the guidelines?',
    note_a='multi-select buckets -> multi_choice/ms/propose',
    note_b='queue status; pause auto-label -> yes_no',
    ka='m',
    pa=True,
    pb=True,
    ms_a=True,
)

add(
    375,
    'Push notification delivery issues on Android:\n\n1. **FCM token rotation** — stale tokens after app restore\n2. **Channel config** — high-importance channel missing sound\n3. **Payload size** — data-only messages truncated at 4KB\n\nWhich push issue should I fix in the next release?',
    'Which push issue should I fix in the next release?',
    ['FCM token rotation', 'Channel config', 'Payload size'],
    'Push notification delivery issues on Android:\n\n1. **FCM token rotation** — stale tokens after app restore\n2. **Channel config** — high-importance channel missing sound\n3. **Payload size** — data-only messages truncated at 4KB\n\nWant me to pull delivery stats from Firebase for the last 7 days?',
    'Want me to pull delivery stats from Firebase for the last 7 days?',
    note_a='fix menu -> multi_choice/propose',
    note_b='issue list; stats pull -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    376,
    'Offline sync conflict strategy options:\n\n- **Last-write-wins** — simple timestamp merge\n- **CRDT cart** — merge line items without data loss\n- **Manual resolve** — prompt user on conflict\n\nWhich sync strategy should I prototype for the cart?',
    'Which sync strategy should I prototype for the cart?',
    ['Last-write-wins', 'CRDT cart', 'Manual resolve'],
    'Offline sync conflict strategy options:\n\n- **Last-write-wins** — simple timestamp merge\n- **CRDT cart** — merge line items without data loss\n- **Manual resolve** — prompt user on conflict\n\nShall I add an integration test that simulates airplane mode?',
    'Shall I add an integration test that simulates airplane mode?',
    note_a='strategy choices -> multi_choice/propose',
    note_b='design options; integration test -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    377,
    'Deep link routing bugs reported on iOS:\n\n- **Universal links** — Safari opens web instead of app\n- **Deferred deep links** — install attribution lost\n- **Custom scheme** — `myapp://` hijacked on iOS 18\n\nWhich deep link path should I debug first?',
    'Which deep link path should I debug first?',
    ['Universal links', 'Deferred deep links', 'Custom scheme'],
    'Deep link routing bugs reported on iOS:\n\n- **Universal links** — Safari opens web instead of app\n- **Deferred deep links** — install attribution lost\n- **Custom scheme** — `myapp://` hijacked on iOS 18\n\nWant me to capture a sysdiagnose while reproducing on device?',
    'Want me to capture a sysdiagnose while reproducing on device?',
    note_a='selectable bug areas -> multi_choice/propose',
    note_b='bug inventory; sysdiagnose -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    378,
    'App Store review rejection cited two items:\n\n- Privacy manifest — missing `NSPrivacyAccessedAPITypes` entries\n- Sign in with Apple — required for Google-only login flow\n\nShould I update the privacy manifest or add Sign in with Apple first?',
    'Should I update the privacy manifest or add Sign in with Apple first?',
    ['update the privacy manifest', 'add Sign in with Apple first'],
    'App Store review rejection cited two items:\n\n- Privacy manifest — missing `NSPrivacyAccessedAPITypes` entries\n- Sign in with Apple — required for Google-only login flow\n\nShall I submit a build to TestFlight while we wait for review?',
    'Shall I submit a build to TestFlight while we wait for review?',
    note_a='two compliance fixes -> either_or/propose',
    note_b='rejection reasons; TestFlight submit -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    379,
    'Biometric auth rollout plan:\n\n- **Face ID** — replace PIN on iOS checkout\n- **Fingerprint** — Android quick unlock for wallet\n- **Fallback PIN** — after three failed biometric attempts\n\nWhich biometric flow should I implement first?',
    'Which biometric flow should I implement first?',
    ['Face ID', 'Fingerprint', 'Fallback PIN'],
    'Biometric auth rollout plan:\n\n- **Face ID** — replace PIN on iOS checkout\n- **Fingerprint** — Android quick unlock for wallet\n- **Fallback PIN** — after three failed biometric attempts\n\nWant me to update the threat model doc with biometric storage?',
    'Want me to update the threat model doc with biometric storage?',
    note_a='flow options -> multi_choice/propose',
    note_b='rollout plan; threat model -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    380,
    'Background task limits hitting two features:\n\n- **Photo upload** — iOS suspends after 30s in background\n- **Location ping** — Android Doze delays beacons\n\nShould I move uploads to BGProcessingTask or reduce location frequency?',
    'Should I move uploads to BGProcessingTask or reduce location frequency?',
    ['move uploads to BGProcessingTask', 'reduce location frequency'],
    'Background task limits hitting two features:\n\n- **Photo upload** — iOS suspends after 30s in background\n- **Location ping** — Android Doze delays beacons\n\nShall I add battery metrics to the next beta build?',
    'Shall I add battery metrics to the next beta build?',
    note_a='two mitigation paths -> either_or/propose',
    note_b='limit findings; battery metrics -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    381,
    'React Native bridge errors after the upgrade:\n\n- **TurboModule** — `NativeSettings` fails lazy load\n- **Hermes** — bytecode mismatch on release builds\n- **Fabric** — layout flicker on nested ScrollViews\n\nWhich bridge issue should I bisect first?',
    'Which bridge issue should I bisect first?',
    ['TurboModule', 'Hermes', 'Fabric'],
    'React Native bridge errors after the upgrade:\n\n- **TurboModule** — `NativeSettings` fails lazy load\n- **Hermes** — bytecode mismatch on release builds\n- **Fabric** — layout flicker on nested ScrollViews\n\nWant me to run the upgrade helper and diff native deps?',
    'Want me to run the upgrade helper and diff native deps?',
    note_a='issue pick list -> multi_choice/propose',
    note_b='error summary; upgrade helper -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    382,
    'Crash reporting triage from Crashlytics:\n\n- **Null deref** — `HomeViewModel.onResume` 38% of sessions\n- **ANR** — main thread blocked on disk I/O\n- **OOM** — image cache unbounded on tablets\n\nWhich crash cluster should I prioritize for hotfix?',
    'Which crash cluster should I prioritize for hotfix?',
    ['Null deref', 'ANR', 'OOM'],
    'Crash reporting triage from Crashlytics:\n\n- **Null deref** — `HomeViewModel.onResume` 38% of sessions\n- **ANR** — main thread blocked on disk I/O\n- **OOM** — image cache unbounded on tablets\n\nShall I cut a hotfix branch from `release/4.2`?',
    'Shall I cut a hotfix branch from `release/4.2`?',
    note_a='cluster selection -> multi_choice/propose',
    note_b='triage stats; hotfix branch -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    383,
    'Stripe webhook failures in the last hour:\n\n1. **`invoice.paid`** — signature mismatch on rotated secret\n2. **`customer.subscription.updated`** — handler timeout at 25s\n3. **`charge.dispute.created`** — unhandled event type 400\n\nWhich webhook handler should I patch first?',
    'Which webhook handler should I patch first?',
    ['`invoice.paid`', '`customer.subscription.updated`', '`charge.dispute.created`'],
    'Stripe webhook failures in the last hour:\n\n1. **`invoice.paid`** — signature mismatch on rotated secret\n2. **`customer.subscription.updated`** — handler timeout at 25s\n3. **`charge.dispute.created`** — unhandled event type 400\n\nWant me to replay dead-letter events from the SQS queue?',
    'Want me to replay dead-letter events from the SQS queue?',
    note_a='handler pick list -> multi_choice/propose',
    note_b='failure log; replay offer -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    384,
    'Idempotency key collisions detected on checkout:\n\n- **Client reuse** — mobile SDK resends same key on retry\n- **TTL too short** — keys expire before async capture completes\n- **Hash collision** — UUID v4 truncated to 16 chars in logs only\n\nWhich idempotency issue should I fix first?',
    'Which idempotency issue should I fix first?',
    ['Client reuse', 'TTL too short', 'Hash collision'],
    'Idempotency key collisions detected on checkout:\n\n- **Client reuse** — mobile SDK resends same key on retry\n- **TTL too short** — keys expire before async capture completes\n- **Hash collision** — UUID v4 truncated to 16 chars in logs only\n\nShall I add a dashboard panel for duplicate key rate?',
    'Shall I add a dashboard panel for duplicate key rate?',
    note_a='issue menu -> multi_choice/propose',
    note_b='collision analysis; dashboard -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    385,
    'Refund workflow gaps after the policy change:\n\n- **Partial refunds** — no line-item allocation in ledger\n- **Store credit** — gift card balance not restored\n- **FX rounding** — currency conversion off by one cent\n\nWhich refund gap should I close in this sprint?',
    'Which refund gap should I close in this sprint?',
    ['Partial refunds', 'Store credit', 'FX rounding'],
    'Refund workflow gaps after the policy change:\n\n- **Partial refunds** — no line-item allocation in ledger\n- **Store credit** — gift card balance not restored\n- **FX rounding** — currency conversion off by one cent\n\nWant me to walk through a test refund on staging?',
    'Want me to walk through a test refund on staging?',
    note_a='gap selection -> multi_choice/propose',
    note_b='workflow gaps; staging test -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    386,
    'PCI scope reduction options:\n\n- **Hosted fields** — Stripe Elements for card entry\n- **Network tokenization** — issuer tokens via gateway\n- **Outsource vault** — move PAN storage to VGS\n\nWhich approach should I spike for PCI SAQ-A?',
    'Which approach should I spike for PCI SAQ-A?',
    ['Hosted fields', 'Network tokenization', 'Outsource vault'],
    'PCI scope reduction options:\n\n- **Hosted fields** — Stripe Elements for card entry\n- **Network tokenization** — issuer tokens via gateway\n- **Outsource vault** — move PAN storage to VGS\n\nShall I schedule a call with the QSA to review the diagram?',
    'Shall I schedule a call with the QSA to review the diagram?',
    note_a='scope options -> multi_choice/propose',
    note_b='reduction strategies; QSA call -> yes_no',
    ka='m',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    387,
    'Subscription dunning experiments ready:\n\n- **Email cadence** — day 1, 3, 7 reminders\n- **In-app banner** — soft block after failed charge\n- **Grace period** — 7-day access before cancel\n\nWhich dunning variant should I A/B test first?',
    'Which dunning variant should I A/B test first?',
    ['Email cadence', 'In-app banner', 'Grace period'],
    'Subscription dunning experiments ready:\n\n- **Email cadence** — day 1, 3, 7 reminders\n- **In-app banner** — soft block after failed charge\n- **Grace period** — 7-day access before cancel\n\nWant me to enable the experiment flag at 5% traffic?',
    'Want me to enable the experiment flag at 5% traffic?',
    note_a='experiment choices -> multi_choice/propose',
    note_b='experiment plan; enable flag -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    388,
    '3DS friction vs approval trade-offs:\n\n- **Challenge every txn** — maximize issuer approval\n- **Risk-based** — step-up only on high fraud score\n\nShould we challenge every transaction or use risk-based 3DS?',
    'Should we challenge every transaction or use risk-based 3DS?',
    ['Challenge every txn', 'Risk-based'],
    '3DS friction vs approval trade-offs:\n\n- **Challenge every txn** — maximize issuer approval\n- **Risk-based** — step-up only on high fraud score\n\nShall I pull approval rates from the last 30 days before deciding?',
    'Shall I pull approval rates from the last 30 days before deciding?',
    note_a='two 3DS modes -> either_or',
    note_b='trade-off summary; pull rates -> yes_no/propose',
    ka='e',
    pa=False,
    pb=True,
    ms_a=False,
)

add(
    389,
    'Nightly reconciliation mismatches:\n\n- **Unsettled captures** — 12 orders pending > 48h\n- **Fee drift** — Stripe fees differ from internal model\n- **Currency FX** — EUR settlements off by €43\n\nWhich mismatch bucket should I reconcile first?',
    'Which mismatch bucket should I reconcile first?',
    ['Unsettled captures', 'Fee drift', 'Currency FX'],
    'Nightly reconciliation mismatches:\n\n- **Unsettled captures** — 12 orders pending > 48h\n- **Fee drift** — Stripe fees differ from internal model\n- **Currency FX** — EUR settlements off by €43\n\nWant me to export the ledger diff CSV for finance?',
    'Want me to export the ledger diff CSV for finance?',
    note_a='bucket selection -> multi_choice/propose',
    note_b='mismatch report; CSV export -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    390,
    'Tax calculation integration choices:\n\n- **Stripe Tax** — automatic rate lookup\n- **Avalara** — existing ERP integration\n- **Manual tables** — static rates per state\n\nWhich tax engine should I wire into checkout?',
    'Which tax engine should I wire into checkout?',
    ['Stripe Tax', 'Avalara', 'Manual tables'],
    'Tax calculation integration choices:\n\n- **Stripe Tax** — automatic rate lookup\n- **Avalara** — existing ERP integration\n- **Manual tables** — static rates per state\n\nShall I hold deploy until tax QA signs off on test invoices?',
    'Shall I hold deploy until tax QA signs off on test invoices?',
    note_a='engine choices -> multi_choice/propose',
    note_b='integration options; hold deploy -> yes_no',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    391,
    'DNS cutover checklist for `api.example.com`:\n\n1. **A/AAAA records** — point to new anycast IPs\n2. **TTL reduction** — drop to 60s 24h before switch\n3. **Health checks** — Route53 failover to secondary\n\nWhich cutover step should I execute first?',
    'Which cutover step should I execute first?',
    ['A/AAAA records', 'TTL reduction', 'Health checks'],
    'DNS cutover checklist for `api.example.com`:\n\n1. **A/AAAA records** — point to new anycast IPs\n2. **TTL reduction** — drop to 60s 24h before switch\n3. **Health checks** — Route53 failover to secondary\n\nWant me to monitor resolver caches during the change window?',
    'Want me to monitor resolver caches during the change window?',
    note_a='step selection -> multi_choice/propose',
    note_b='cutover checklist; monitor caches -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    392,
    'CNAME flattening options at the apex:\n\n- **ALIAS record** — provider-native flattening\n- **ANAME** — DNS Made Easy proprietary\n- **A record sync** — script updates from CDN API\n\nWhich apex strategy should I configure?',
    'Which apex strategy should I configure?',
    ['ALIAS record', 'ANAME', 'A record sync'],
    'CNAME flattening options at the apex:\n\n- **ALIAS record** — provider-native flattening\n- **ANAME** — DNS Made Easy proprietary\n- **A record sync** — script updates from CDN API\n\nShall I lower TTL on the apex now before the migration?',
    'Shall I lower TTL on the apex now before the migration?',
    note_a='strategy pick -> multi_choice/propose',
    note_b='options as plan; lower TTL -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    393,
    'Geo DNS routing for compliance:\n\n- **EU-only pool** — GDPR data residency\n- **US default** — lowest latency for NA users\n- **Failover to EU** — when US pool unhealthy\n\nWhich geo route should I attach to `app.example.com`?',
    'Which geo route should I attach to `app.example.com`?',
    ['EU-only pool', 'US default', 'Failover to EU'],
    'Geo DNS routing for compliance:\n\n- **EU-only pool** — GDPR data residency\n- **US default** — lowest latency for NA users\n- **Failover to EU** — when US pool unhealthy\n\nWant me to run `dig` from three vantage points after the change?',
    'Want me to run `dig` from three vantage points after the change?',
    note_a='route choices -> multi_choice/propose',
    note_b='routing plan; dig verification -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    394,
    'DNSSEC rollout steps remaining:\n\n- **KSK rollover** — publish new trust anchor\n- **NSEC3** — enable hashed denial of existence\n- **DS update** — registrar still on SHA-1 DS\n\nWhich DNSSEC task should I complete first?',
    'Which DNSSEC task should I complete first?',
    ['KSK rollover', 'NSEC3', 'DS update'],
    'DNSSEC rollout steps remaining:\n\n- **KSK rollover** — publish new trust anchor\n- **NSEC3** — enable hashed denial of existence\n- **DS update** — registrar still on SHA-1 DS\n\nShall I schedule maintenance with the registrar for DS swap?',
    'Shall I schedule maintenance with the registrar for DS swap?',
    note_a='task menu -> multi_choice/propose',
    note_b='remaining steps; registrar maintenance -> yes_no',
    ka='m',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    395,
    'Split-horizon DNS for internal services:\n\n- **Private zone** — Route53 assoc with VPC\n- **Views on BIND** — internal vs external answers\n- **Split DNS proxy** — forward corp queries to AD\n\nWhich split-horizon approach fits the mesh services?',
    'Which split-horizon approach fits the mesh services?',
    ['Private zone', 'Views on BIND', 'Split DNS proxy'],
    'Split-horizon DNS for internal services:\n\n- **Private zone** — Route53 assoc with VPC\n- **Views on BIND** — internal vs external answers\n- **Split DNS proxy** — forward corp queries to AD\n\nWant me to document the resolver paths for SRE?',
    'Want me to document the resolver paths for SRE?',
    note_a='approach selection -> multi_choice/propose',
    note_b='design options; document paths -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    396,
    'Health-checked record failures:\n\n- Primary LB — fails HTTPS check on `/healthz`\n- Secondary region — passes but higher latency\n\nShould I fail over to the secondary region or fix the primary health check?',
    'Should I fail over to the secondary region or fix the primary health check?',
    ['fail over to the secondary region', 'fix the primary health check'],
    'Health-checked record failures:\n\n- Primary LB — fails HTTPS check on `/healthz`\n- Secondary region — passes but higher latency\n\nShall I page infra once failover completes?',
    'Shall I page infra once failover completes?',
    note_a='two incident paths -> either_or/propose',
    note_b='health status; page on failover -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    397,
    'SPF alignment failures on marketing mail:\n\n1. **Too many lookups** — 10 DNS lookups exceeded\n2. **Softfail** — `~all` allows spoofed forwards\n3. **Include chain** — third-party ESP not authorized\n\nWhich SPF issue should I fix first?',
    'Which SPF issue should I fix first?',
    ['Too many lookups', 'Softfail', 'Include chain'],
    'SPF alignment failures on marketing mail:\n\n1. **Too many lookups** — 10 DNS lookups exceeded\n2. **Softfail** — `~all` allows spoofed forwards\n3. **Include chain** — third-party ESP not authorized\n\nWant me to send test messages through mail-tester.com?',
    'Want me to send test messages through mail-tester.com?',
    note_a='SPF fix menu -> multi_choice/propose',
    note_b='alignment report; test send -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    398,
    'DKIM key rotation plan:\n\n- **2048-bit key** — publish new selector `s2`\n- **Dual signing** — sign with old and new for 7 days\n- **Revoke old** — remove `s1` after DMARC passes\n\nWhich rotation step should I run tonight?',
    'Which rotation step should I run tonight?',
    ['2048-bit key', 'Dual signing', 'Revoke old'],
    'DKIM key rotation plan:\n\n- **2048-bit key** — publish new selector `s2`\n- **Dual signing** — sign with old and new for 7 days\n- **Revoke old** — remove `s1` after DMARC passes\n\nShall I notify support before the rotation window?',
    'Shall I notify support before the rotation window?',
    note_a='step choices -> multi_choice/propose',
    note_b='rotation plan; notify support -> yes_no',
    ka='m',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    399,
    'DMARC policy escalation options:\n\n- **p=none** — monitor only with aggregate reports\n- **p=quarantine** — pct=25 on suspicious mail\n- **p=reject** — block outright after confidence\n\nWhich DMARC policy should I publish for `example.com`?',
    'Which DMARC policy should I publish for `example.com`?',
    ['p=none', 'p=quarantine', 'p=reject'],
    'DMARC policy escalation options:\n\n- **p=none** — monitor only with aggregate reports\n- **p=quarantine** — pct=25 on suspicious mail\n- **p=reject** — block outright after confidence\n\nWant me to parse the latest aggregate XML reports?',
    'Want me to parse the latest aggregate XML reports?',
    note_a='policy selection -> multi_choice/propose',
    note_b='policy options; parse reports -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    400,
    'Bounce handling improvements:\n\n- **Hard bounces** — suppress after first 5xx\n- **Soft bounces** — retry with exponential backoff\n- **Complaints** — auto-unsubscribe on FBL signal\n\nWhich bounce rule should I deploy first?',
    'Which bounce rule should I deploy first?',
    ['Hard bounces', 'Soft bounces', 'Complaints'],
    "Bounce handling improvements:\n\n- **Hard bounces** — suppress after first 5xx\n- **Soft bounces** — retry with exponential backoff\n- **Complaints** — auto-unsubscribe on FBL signal\n\nShall I backfill suppression lists from last month's bounces?",
    "Shall I backfill suppression lists from last month's bounces?",
    note_a='rule pick -> multi_choice/propose',
    note_b='improvement list; backfill -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    401,
    'Transactional email template i18n gaps:\n\n- **Missing `pt-BR`** — order shipped template\n- **RTL layout** — Arabic password reset broken\n- **Plural rules** — Polish item count wrong\n\nWhich template locale should I fix first?',
    'Which template locale should I fix first?',
    ['Missing `pt-BR`', 'RTL layout', 'Plural rules'],
    'Transactional email template i18n gaps:\n\n- **Missing `pt-BR`** — order shipped template\n- **RTL layout** — Arabic password reset broken\n- **Plural rules** — Polish item count wrong\n\nWant me to run Litmus previews across clients?',
    'Want me to run Litmus previews across clients?',
    note_a='locale fix menu -> multi_choice/propose',
    note_b='gap inventory; Litmus previews -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    402,
    'List hygiene before the campaign:\n\n- **Remove role accounts** — `admin@`, `info@`\n- **Re-confirm inactive** — no opens in 180 days\n- **Block disposable domains** — update denylist\n\nWhich hygiene step(s) should I run on the main list?',
    'Which hygiene step(s) should I run on the main list?',
    ['Remove role accounts', 'Re-confirm inactive', 'Block disposable domains'],
    'List hygiene before the campaign:\n\n- **Remove role accounts** — `admin@`, `info@`\n- **Re-confirm inactive** — no opens in 180 days\n- **Block disposable domains** — update denylist\n\nShall I pause the campaign send until hygiene completes?',
    'Shall I pause the campaign send until hygiene completes?',
    note_a='multi-select hygiene tasks -> multi_choice/ms/propose',
    note_b='hygiene checklist; pause campaign -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=True,
)

add(
    403,
    'WCAG audit findings on the checkout flow:\n\n1. **Focus order** — modal traps keyboard on step 2\n2. **Color contrast** — CTA button 3.2:1 on gray\n3. **Error announcements** — validation errors not in live region\n\nWhich accessibility issue should I fix first?',
    'Which accessibility issue should I fix first?',
    ['Focus order', 'Color contrast', 'Error announcements'],
    'WCAG audit findings on the checkout flow:\n\n1. **Focus order** — modal traps keyboard on step 2\n2. **Color contrast** — CTA button 3.2:1 on gray\n3. **Error announcements** — validation errors not in live region\n\nWant me to run axe-core in CI on the checkout pages?',
    'Want me to run axe-core in CI on the checkout pages?',
    note_a='fix selection -> multi_choice/propose',
    note_b='audit findings; axe CI -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    404,
    'Screen reader testing notes from NVDA:\n\n- **Unlabeled icon buttons** — cart and wishlist\n- **Duplicate landmarks** — two `navigation` regions\n- **Hidden headings** — skipped levels in footer\n\nWhich screen reader issue should I patch in this PR?',
    'Which screen reader issue should I patch in this PR?',
    ['Unlabeled icon buttons', 'Duplicate landmarks', 'Hidden headings'],
    'Screen reader testing notes from NVDA:\n\n- **Unlabeled icon buttons** — cart and wishlist\n- **Duplicate landmarks** — two `navigation` regions\n- **Hidden headings** — skipped levels in footer\n\nShall I record a VoiceOver walkthrough for QA?',
    'Shall I record a VoiceOver walkthrough for QA?',
    note_a='issue pick -> multi_choice/propose',
    note_b='testing notes; VoiceOver recording -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    405,
    "Keyboard navigation gaps on the data table:\n\n- **Skip link** — missing jump to main content\n- **Row focus** — arrow keys don't move between rows\n- **Escape closes** — filter popover ignores Esc\n\nWhich keyboard fix should I prioritize?",
    'Which keyboard fix should I prioritize?',
    ['Skip link', 'Row focus', 'Escape closes'],
    "Keyboard navigation gaps on the data table:\n\n- **Skip link** — missing jump to main content\n- **Row focus** — arrow keys don't move between rows\n- **Escape closes** — filter popover ignores Esc\n\nWant me to add a keyboard-only test in Playwright?",
    'Want me to add a keyboard-only test in Playwright?',
    note_a='fix menu -> multi_choice/propose',
    note_b='gap list; Playwright test -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    406,
    'Live region strategy for toast notifications:\n\n- **polite** — non-critical save confirmations\n- **assertive** — payment failure alerts\n\nShould toasts use `aria-live="polite"` or `assertive` for errors?',
    'Should toasts use `aria-live="polite"` or `assertive` for errors?',
    ['`aria-live="polite"`', '`assertive`'],
    'Live region strategy for toast notifications:\n\n- **polite** — non-critical save confirmations\n- **assertive** — payment failure alerts\n\nShall I verify with NVDA before merging?',
    'Shall I verify with NVDA before merging?',
    note_a='two ARIA modes -> either_or/propose',
    note_b='strategy notes; NVDA verify -> yes_no',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    407,
    'Skip link placement options:\n\n- **First focusable** — before header logo\n- **Visible on focus** — high-contrast bar\n- **Skip to search** — alternative target for power users\n\nWhich skip link pattern should I implement?',
    'Which skip link pattern should I implement?',
    ['First focusable', 'Visible on focus', 'Skip to search'],
    'Skip link placement options:\n\n- **First focusable** — before header logo\n- **Visible on focus** — high-contrast bar\n- **Skip to search** — alternative target for power users\n\nWant me to add it to the design system Storybook?',
    'Want me to add it to the design system Storybook?',
    note_a='pattern choices -> multi_choice/propose',
    note_b='placement options; Storybook -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    408,
    'Form labeling inconsistencies:\n\n- **Missing `<label>`** — coupon field uses placeholder only\n- **aria-describedby** — hint text not linked\n- **Required indicator** — asterisk without text alternative\n\nWhich labeling issue(s) should I fix on the billing form?',
    'Which labeling issue(s) should I fix on the billing form?',
    ['Missing `<label>`', 'aria-describedby', 'Required indicator'],
    'Form labeling inconsistencies:\n\n- **Missing `<label>`** — coupon field uses placeholder only\n- **aria-describedby** — hint text not linked\n- **Required indicator** — asterisk without text alternative\n\nShall I run the automated contrast check after the patch?',
    'Shall I run the automated contrast check after the patch?',
    note_a='multi-select fixes -> multi_choice/ms/propose',
    note_b='labeling audit; contrast check -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=True,
)

add(
    409,
    'RTL layout bugs after enabling Arabic:\n\n1. **Mirrored icons** — chevrons point wrong direction\n2. **Padding flip** — card gutters not logical\n3. **Modal alignment** — close button off-screen on mobile\n\nWhich RTL issue should I fix first?',
    'Which RTL issue should I fix first?',
    ['Mirrored icons', 'Padding flip', 'Modal alignment'],
    'RTL layout bugs after enabling Arabic:\n\n1. **Mirrored icons** — chevrons point wrong direction\n2. **Padding flip** — card gutters not logical\n3. **Modal alignment** — close button off-screen on mobile\n\nWant me to snapshot visual diffs in Percy for `ar-SA`?',
    'Want me to snapshot visual diffs in Percy for `ar-SA`?',
    note_a='RTL fix menu -> multi_choice/propose',
    note_b='bug list; Percy diffs -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    410,
    'Plural rule failures in ICU messages:\n\n- **Polish** — `one/few/many` mismatches in cart count\n- **Russian** — genitive plural on `{count}` items\n- **Arabic** — dual form missing for `{count}` days\n\nWhich locale pluralization should I correct first?',
    'Which locale pluralization should I correct first?',
    ['Polish', 'Russian', 'Arabic'],
    'Plural rule failures in ICU messages:\n\n- **Polish** — `one/few/many` mismatches in cart count\n- **Russian** — genitive plural on `{count}` items\n- **Arabic** — dual form missing for `{count}` days\n\nShall I export the ICU strings for translator review?',
    'Shall I export the ICU strings for translator review?',
    note_a='locale pick -> multi_choice/propose',
    note_b='failure inventory; export strings -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    411,
    'Locale fallback chain options:\n\n- **en-GB → en** — collapse regional variants\n- **zh-Hans → zh** — simplified to macro language\n- **pt → pt-BR** — prefer Brazilian Portuguese\n\nWhich fallback rule should I add to the i18n config?',
    'Which fallback rule should I add to the i18n config?',
    ['en-GB → en', 'zh-Hans → zh', 'pt → pt-BR'],
    'Locale fallback chain options:\n\n- **en-GB → en** — collapse regional variants\n- **zh-Hans → zh** — simplified to macro language\n- **pt → pt-BR** — prefer Brazilian Portuguese\n\nWant me to add unit tests for each fallback path?',
    'Want me to add unit tests for each fallback path?',
    note_a='fallback choices -> multi_choice/propose',
    note_b='chain options; unit tests -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    412,
    'Date formatting inconsistencies:\n\n- **Short date** — `MM/DD` vs `DD/MM` by locale\n- **Timezone labels** — missing offset in emails\n- **Relative time** — `3 hours ago` not localized\n\nWhich date format should I standardize first?',
    'Which date format should I standardize first?',
    ['Short date', 'Timezone labels', 'Relative time'],
    'Date formatting inconsistencies:\n\n- **Short date** — `MM/DD` vs `DD/MM` by locale\n- **Timezone labels** — missing offset in emails\n- **Relative time** — `3 hours ago` not localized\n\nShall I run the locale snapshot tests before release?',
    'Shall I run the locale snapshot tests before release?',
    note_a='format pick -> multi_choice/propose',
    note_b='inconsistency list; snapshot tests -> yes_no',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    413,
    'Translation workflow tooling:\n\n- **Crowdin sync** — auto PR on string updates\n- **Lokalise OTA** — hotfix strings without app release\n- **Manual JSON** — commit locale files in repo\n\nWhich translation workflow should we adopt?',
    'Which translation workflow should we adopt?',
    ['Crowdin sync', 'Lokalise OTA', 'Manual JSON'],
    'Translation workflow tooling:\n\n- **Crowdin sync** — auto PR on string updates\n- **Lokalise OTA** — hotfix strings without app release\n- **Manual JSON** — commit locale files in repo\n\nWant me to draft the vendor comparison doc?',
    'Want me to draft the vendor comparison doc?',
    note_a='workflow choices -> multi_choice',
    note_b='tooling options; comparison doc -> yes_no/propose',
    ka='m',
    pa=False,
    pb=True,
    ms_a=False,
)

add(
    414,
    'ICU message extraction gaps:\n\n- Hard-coded strings — 142 in React components\n- Concatenation — word order breaks in Japanese\n\nShould I run the codemod for extraction or fix concatenation manually first?',
    'Should I run the codemod for extraction or fix concatenation manually first?',
    ['run the codemod for extraction', 'fix concatenation manually first'],
    'ICU message extraction gaps:\n\n- Hard-coded strings — 142 in React components\n- Concatenation — word order breaks in Japanese\n\nShall I enable the ESLint rule to block new hard-coded copy?',
    'Shall I enable the ESLint rule to block new hard-coded copy?',
    note_a='two remediation paths -> either_or/propose',
    note_b='gap summary; ESLint rule -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    415,
    'Turbo cache misses after the upgrade:\n\n1. **Env hash** — `NODE_ENV` differs local vs CI\n2. **Output globs** — `dist/**` too broad invalidates\n3. **Remote cache** — token expired on Vercel\n\nWhich cache issue should I fix first?',
    'Which cache issue should I fix first?',
    ['Env hash', 'Output globs', 'Remote cache'],
    'Turbo cache misses after the upgrade:\n\n1. **Env hash** — `NODE_ENV` differs local vs CI\n2. **Output globs** — `dist/**` too broad invalidates\n3. **Remote cache** — token expired on Vercel\n\nWant me to warm the cache on main before the next PR?',
    'Want me to warm the cache on main before the next PR?',
    note_a='cache fix menu -> multi_choice/propose',
    note_b='miss analysis; warm cache -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    416,
    'Nx module boundary violations:\n\n- **`ui` → `api`** — shared components import server code\n- **Circular deps** — `billing` ↔ `auth` through utils\n- **Lazy routes** — feature lib imports app shell\n\nWhich boundary violation should I refactor first?',
    'Which boundary violation should I refactor first?',
    ['`ui` → `api`', 'Circular deps', 'Lazy routes'],
    'Nx module boundary violations:\n\n- **`ui` → `api`** — shared components import server code\n- **Circular deps** — `billing` ↔ `auth` through utils\n- **Lazy routes** — feature lib imports app shell\n\nShall I enable `enforce-module-boundaries` in CI?',
    'Shall I enable `enforce-module-boundaries` in CI?',
    note_a='violation pick -> multi_choice/propose',
    note_b='violation report; enforce rule -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    417,
    'Shared dependency version drift:\n\n- **React** — 18.2 in apps, 17.0 in packages\n- **TypeScript** — 5.4 vs 4.9 across libs\n- **ESLint** — flat config only in root\n\nWhich dependency should I align across the workspace?',
    'Which dependency should I align across the workspace?',
    ['React', 'TypeScript', 'ESLint'],
    'Shared dependency version drift:\n\n- **React** — 18.2 in apps, 17.0 in packages\n- **TypeScript** — 5.4 vs 4.9 across libs\n- **ESLint** — flat config only in root\n\nWant me to run `pnpm dedupe` and open a sync PR?',
    'Want me to run `pnpm dedupe` and open a sync PR?',
    note_a='dependency pick -> multi_choice/propose',
    note_b='drift inventory; dedupe PR -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    418,
    'Independent versioning strategy:\n\n- **Changesets** — per-package semver bumps\n- **Fixed group** — single version for all `@acme/*`\n- **Canary tags** — `@acme/ui@0.0.0-canary` on main\n\nWhich versioning model should I configure?',
    'Which versioning model should I configure?',
    ['Changesets', 'Fixed group', 'Canary tags'],
    'Independent versioning strategy:\n\n- **Changesets** — per-package semver bumps\n- **Fixed group** — single version for all `@acme/*`\n- **Canary tags** — `@acme/ui@0.0.0-canary` on main\n\nShall I document the release process in `CONTRIBUTING.md`?',
    'Shall I document the release process in `CONTRIBUTING.md`?',
    note_a='model choices -> multi_choice/propose',
    note_b='strategy options; CONTRIBUTING doc -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    419,
    'CI graph optimization for the monorepo:\n\n- **Affected only** — run tests for changed projects\n- **Shard by package** — parallelize `apps/*` matrix\n- **Merge queue** — batched merges with required checks\n\nWhich CI optimization should I implement first?',
    'Which CI optimization should I implement first?',
    ['Affected only', 'Shard by package', 'Merge queue'],
    'CI graph optimization for the monorepo:\n\n- **Affected only** — run tests for changed projects\n- **Shard by package** — parallelize `apps/*` matrix\n- **Merge queue** — batched merges with required checks\n\nWant me to benchmark pipeline duration before/after?',
    'Want me to benchmark pipeline duration before/after?',
    note_a='optimization pick -> multi_choice/propose',
    note_b='CI plan; benchmark -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    420,
    'Package publishing pipeline choices:\n\n1. **GitHub Packages** — private npm registry\n2. **npm org** — public scoped packages\n\nShould we publish to GitHub Packages or the public npm org?',
    'Should we publish to GitHub Packages or the public npm org?',
    ['GitHub Packages', 'npm org'],
    'Package publishing pipeline choices:\n\n1. **GitHub Packages** — private npm registry\n2. **npm org** — public scoped packages\n\nShall I set up provenance signing on publish?',
    'Shall I set up provenance signing on publish?',
    note_a='two registry options -> either_or',
    note_b='publishing options; provenance -> yes_no/propose',
    ka='e',
    pa=False,
    pb=True,
    ms_a=False,
)

add(
    421,
    'Wasm memory growth errors in the browser module:\n\n1. **Initial pages** — 16MB too small for image buffer\n2. **Max cap** — 256MB limit hit on large PDFs\n3. **Shared memory** — threaded build needs COOP/COEP\n\nWhich memory setting should I tune first?',
    'Which memory setting should I tune first?',
    ['Initial pages', 'Max cap', 'Shared memory'],
    'Wasm memory growth errors in the browser module:\n\n1. **Initial pages** — 16MB too small for image buffer\n2. **Max cap** — 256MB limit hit on large PDFs\n3. **Shared memory** — threaded build needs COOP/COEP\n\nWant me to rebuild with `-sALLOW_MEMORY_GROWTH` and measure?',
    'Want me to rebuild with `-sALLOW_MEMORY_GROWTH` and measure?',
    note_a='tuning menu -> multi_choice/propose',
    note_b='error analysis; rebuild measure -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    422,
    'SIMD optimization opportunities in the codec:\n\n- **v128 loads** — replace scalar RGBA unpack\n- **FMA** — dot product in color transform\n- **Tail handling** — scalar fallback for remainder pixels\n\nWhich SIMD path should I implement first?',
    'Which SIMD path should I implement first?',
    ['v128 loads', 'FMA', 'Tail handling'],
    'SIMD optimization opportunities in the codec:\n\n- **v128 loads** — replace scalar RGBA unpack\n- **FMA** — dot product in color transform\n- **Tail handling** — scalar fallback for remainder pixels\n\nShall I add a benchmark comparing scalar vs SIMD builds?',
    'Shall I add a benchmark comparing scalar vs SIMD builds?',
    note_a='SIMD options -> multi_choice/propose',
    note_b='optimization list; benchmark -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    423,
    'WASI preview2 migration blockers:\n\n- **Filesystem** — `preopen` paths differ in component model\n- **Sockets** — TCP still experimental in runtime\n- **Clocks** — monotonic vs wall clock APIs renamed\n\nWhich WASI surface should I port first?',
    'Which WASI surface should I port first?',
    ['Filesystem', 'Sockets', 'Clocks'],
    'WASI preview2 migration blockers:\n\n- **Filesystem** — `preopen` paths differ in component model\n- **Sockets** — TCP still experimental in runtime\n- **Clocks** — monotonic vs wall clock APIs renamed\n\nWant me to spike the migration on a branch?',
    'Want me to spike the migration on a branch?',
    note_a='surface pick -> multi_choice/propose',
    note_b='blocker list; spike branch -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    424,
    'Bundler integration for the wasm pkg:\n\n- **vite-plugin-wasm** — ESM import with top-level await\n- **webpack async** — dynamic `import()` chunk\n- **CDN instantiate** — fetch `.wasm` separately\n\nWhich bundler integration should I ship?',
    'Which bundler integration should I ship?',
    ['vite-plugin-wasm', 'webpack async', 'CDN instantiate'],
    'Bundler integration for the wasm pkg:\n\n- **vite-plugin-wasm** — ESM import with top-level await\n- **webpack async** — dynamic `import()` chunk\n- **CDN instantiate** — fetch `.wasm` separately\n\nShall I add a size budget check to CI?',
    'Shall I add a size budget check to CI?',
    note_a='integration choices -> multi_choice/propose',
    note_b='integration options; size budget -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    425,
    'Threading support for wasm workers:\n\n1. **Pthreads pool** — 4 workers for image tiles\n2. **Atomics wait** — backpressure on job queue\n\nShould I enable pthreads or keep single-threaded with SIMD only?',
    'Should I enable pthreads or keep single-threaded with SIMD only?',
    ['enable pthreads', 'keep single-threaded with SIMD only'],
    'Threading support for wasm workers:\n\n1. **Pthreads pool** — 4 workers for image tiles\n2. **Atomics wait** — backpressure on job queue\n\nWant me to verify COOP/COEP headers on staging?',
    'Want me to verify COOP/COEP headers on staging?',
    note_a='two threading modes -> either_or/propose',
    note_b='threading plan; header verify -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    426,
    'Wasm binary size reduction tactics:\n\n- `-Oz` compile — smaller but slower\n- Strip debug — remove name section\n- Feature detection — ship slim + full builds\n\nWhich size tactic should I apply first?',
    'Which size tactic should I apply first?',
    ['`-Oz` compile', 'Strip debug', 'Feature detection'],
    'Wasm binary size reduction tactics:\n\n- `-Oz` compile — smaller but slower\n- Strip debug — remove name section\n- Feature detection — ship slim + full builds\n\nShall I publish the before/after sizes in the PR description?',
    'Shall I publish the before/after sizes in the PR description?',
    note_a='tactic menu -> multi_choice/propose',
    note_b='size tactics; PR metrics -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    427,
    'Physics timestep instability in the platformer:\n\n1. **Fixed 60Hz** — deterministic but stutter on 120Hz displays\n2. **Variable delta** — smooth but tunneling on fast falls\n3. **Substepping** — 4 substeps with capped delta\n\nWhich timestep approach should I ship?',
    'Which timestep approach should I ship?',
    ['Fixed 60Hz', 'Variable delta', 'Substepping'],
    'Physics timestep instability in the platformer:\n\n1. **Fixed 60Hz** — deterministic but stutter on 120Hz displays\n2. **Variable delta** — smooth but tunneling on fast falls\n3. **Substepping** — 4 substeps with capped delta\n\nWant me to record a slow-motion replay to verify?',
    'Want me to record a slow-motion replay to verify?',
    note_a='timestep choices -> multi_choice/propose',
    note_b='physics options; replay verify -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    428,
    'Asset LOD pipeline gaps:\n\n- **Mesh decimation** — no auto-LOD for props\n- **Texture streaming** — 4K albedos loaded upfront\n- **Impostors** — distant trees still full geometry\n\nWhich LOD improvement should I prioritize?',
    'Which LOD improvement should I prioritize?',
    ['Mesh decimation', 'Texture streaming', 'Impostors'],
    'Asset LOD pipeline gaps:\n\n- **Mesh decimation** — no auto-LOD for props\n- **Texture streaming** — 4K albedos loaded upfront\n- **Impostors** — distant trees still full geometry\n\nShall I profile GPU frame time on the forest scene?',
    'Shall I profile GPU frame time on the forest scene?',
    note_a='LOD pick -> multi_choice/propose',
    note_b='pipeline gaps; GPU profile -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    429,
    'Netcode prediction mismatches:\n\n- **Input buffer** — 3 frames of lag compensation\n- **Reconciliation** — snap on divergence > 0.5m\n- **Rollback** — GGPO-style for fighting mode\n\nWhich netcode strategy should I prototype?',
    'Which netcode strategy should I prototype?',
    ['Input buffer', 'Reconciliation', 'Rollback'],
    'Netcode prediction mismatches:\n\n- **Input buffer** — 3 frames of lag compensation\n- **Reconciliation** — snap on divergence > 0.5m\n- **Rollback** — GGPO-style for fighting mode\n\nWant me to simulate 150ms latency in the test harness?',
    'Want me to simulate 150ms latency in the test harness?',
    note_a='strategy menu -> multi_choice/propose',
    note_b='netcode options; latency sim -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    430,
    'Save system corruption reports:\n\n- **Checksum** — missing on slot 2 saves\n- **Cloud sync** — Steam conflict on quit\n- **Autosave spam** — disk thrash every 30s\n\nWhich save issue should I fix first?',
    'Which save issue should I fix first?',
    ['Checksum', 'Cloud sync', 'Autosave spam'],
    'Save system corruption reports:\n\n- **Checksum** — missing on slot 2 saves\n- **Cloud sync** — Steam conflict on quit\n- **Autosave spam** — disk thrash every 30s\n\nShall I add a migration for existing player saves?',
    'Shall I add a migration for existing player saves?',
    note_a='issue pick -> multi_choice/propose',
    note_b='bug list; save migration -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    431,
    'Shader variant explosion:\n\n- **Keyword stripping** — remove unused multi_compile\n- **Shader LOD** — fallback for low spec\n- **Warmup collection** — precompile on load screen\n\nWhich shader optimization should I apply?',
    'Which shader optimization should I apply?',
    ['Keyword stripping', 'Shader LOD', 'Warmup collection'],
    'Shader variant explosion:\n\n- **Keyword stripping** — remove unused multi_compile\n- **Shader LOD** — fallback for low spec\n- **Warmup collection** — precompile on load screen\n\nWant me to capture a RenderDoc frame on min-spec GPU?',
    'Want me to capture a RenderDoc frame on min-spec GPU?',
    note_a='optimization choices -> multi_choice/propose',
    note_b='variant analysis; RenderDoc -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    432,
    'Audio bank loading hitches:\n\n1. **Stream music** — decode on background thread\n2. **Split banks** — combat SFX separate from UI\n\nShould I stream music or split the audio banks first?',
    'Should I stream music or split the audio banks first?',
    ['Stream music', 'Split banks'],
    'Audio bank loading hitches:\n\n1. **Stream music** — decode on background thread\n2. **Split banks** — combat SFX separate from UI\n\nShall I profile audio thread ms during scene transitions?',
    'Shall I profile audio thread ms during scene transitions?',
    note_a='two loading fixes -> either_or/propose',
    note_b='hitch findings; audio profile -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    433,
    'Canary deployment knobs for v2.8:\n\n1. **5% traffic** — route canary on ingress weight\n2. **Error gate** — auto-rollback if 5xx > 1%\n3. **Duration** — 30-minute bake before full promote\n\nWhich canary setting should I configure first?',
    'Which canary setting should I configure first?',
    ['5% traffic', 'Error gate', 'Duration'],
    'Canary deployment knobs for v2.8:\n\n1. **5% traffic** — route canary on ingress weight\n2. **Error gate** — auto-rollback if 5xx > 1%\n3. **Duration** — 30-minute bake before full promote\n\nWant me to wire the rollback hook to PagerDuty?',
    'Want me to wire the rollback hook to PagerDuty?',
    note_a='canary settings -> multi_choice/propose',
    note_b='deployment plan; PagerDuty hook -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    434,
    'Blue-green cutover checklist:\n\n- **Warm green** — preload caches on green stack\n- **DNS flip** — swap weighted record to green\n- **Drain blue** — graceful connection drain 5 min\n\nWhich cutover step should I execute next?',
    'Which cutover step should I execute next?',
    ['Warm green', 'DNS flip', 'Drain blue'],
    'Blue-green cutover checklist:\n\n- **Warm green** — preload caches on green stack\n- **DNS flip** — swap weighted record to green\n- **Drain blue** — graceful connection drain 5 min\n\nShall I run smoke tests against green before the flip?',
    'Shall I run smoke tests against green before the flip?',
    note_a='step selection -> multi_choice/propose',
    note_b='checklist; smoke tests -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    435,
    'Feature flag rollout for checkout redesign:\n\n- **Internal only** — dogfood on `@corp` accounts\n- **Percentage** — ramp 1% → 10% → 50%\n- **Geo gate** — enable in CA before US\n\nWhich rollout stage should I enable now?',
    'Which rollout stage should I enable now?',
    ['Internal only', 'Percentage', 'Geo gate'],
    'Feature flag rollout for checkout redesign:\n\n- **Internal only** — dogfood on `@corp` accounts\n- **Percentage** — ramp 1% → 10% → 50%\n- **Geo gate** — enable in CA before US\n\nWant me to attach flag metrics to the release dashboard?',
    'Want me to attach flag metrics to the release dashboard?',
    note_a='rollout choices -> multi_choice/propose',
    note_b='flag plan; dashboard metrics -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    436,
    'Semver bump policy for the breaking API change:\n\n- **Major** — v3.0.0 for removed endpoints\n- **Minor** — v2.9.0 with deprecation warnings only\n- **Pre-release** — v3.0.0-beta.1 for early adopters\n\nWhich version bump should I tag?',
    'Which version bump should I tag?',
    ['Major', 'Minor', 'Pre-release'],
    'Semver bump policy for the breaking API change:\n\n- **Major** — v3.0.0 for removed endpoints\n- **Minor** — v2.9.0 with deprecation warnings only\n- **Pre-release** — v3.0.0-beta.1 for early adopters\n\nShall I generate the changelog from conventional commits?',
    'Shall I generate the changelog from conventional commits?',
    note_a='version choices -> multi_choice/propose',
    note_b='semver options; changelog gen -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    437,
    'Changelog sections still empty for RC1:\n\n- **Features** — 12 commits since last tag\n- **Fixes** — 9 bugfix commits\n- **Breaking** — 3 API removals\n\nWhich section should I flesh out first in CHANGELOG.md?',
    'Which section should I flesh out first in CHANGELOG.md?',
    ['Features', 'Fixes', 'Breaking'],
    'Changelog sections still empty for RC1:\n\n- **Features** — 12 commits since last tag\n- **Fixes** — 9 bugfix commits\n- **Breaking** — 3 API removals\n\nWant me to open the RC1 release draft on GitHub?',
    'Want me to open the RC1 release draft on GitHub?',
    note_a='section pick -> multi_choice/propose',
    note_b='changelog status; release draft -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    438,
    'Rollback options after the bad deploy:\n\n- Revert commit — git revert merge SHA on main\n- Redeploy previous — helm rollback to revision 412\n- Feature kill switch — disable new parser via flag\n\nWhich rollback path should I take?',
    'Which rollback path should I take?',
    ['Revert commit', 'Redeploy previous', 'Feature kill switch'],
    'Rollback options after the bad deploy:\n\n- Revert commit — git revert merge SHA on main\n- Redeploy previous — helm rollback to revision 412\n- Feature kill switch — disable new parser via flag\n\nShall I notify #incidents once rollback starts?',
    'Shall I notify #incidents once rollback starts?',
    note_a='rollback menu -> multi_choice/propose',
    note_b='incident options; notify channel -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    439,
    'Hotfix branch strategy:\n\n1. **Branch from tag** — `hotfix/4.2.1` off `v4.2.0`\n2. **Cherry-pick to main** — forward-port after patch\n\nShould I branch from the tag or cherry-pick to main first?',
    'Should I branch from the tag or cherry-pick to main first?',
    ['Branch from tag', 'Cherry-pick to main'],
    'Hotfix branch strategy:\n\n1. **Branch from tag** — `hotfix/4.2.1` off `v4.2.0`\n2. **Cherry-pick to main** — forward-port after patch\n\nWant me to cut the branch and open a draft PR?',
    'Want me to cut the branch and open a draft PR?',
    note_a='two hotfix flows -> either_or/propose',
    note_b='strategy notes; cut branch -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    440,
    'Artifact signing for container releases:\n\n- **Cosign keyless** — OIDC signing in CI\n- **Notary v1** — Docker Content Trust\n- **Sigstore bundle** — attach attestations to GHCR\n\nWhich signing approach should I enable?',
    'Which signing approach should I enable?',
    ['Cosign keyless', 'Notary v1', 'Sigstore bundle'],
    'Artifact signing for container releases:\n\n- **Cosign keyless** — OIDC signing in CI\n- **Notary v1** — Docker Content Trust\n- **Sigstore bundle** — attach attestations to GHCR\n\nShall I update the deploy policy to verify signatures?',
    'Shall I update the deploy policy to verify signatures?',
    note_a='signing choices -> multi_choice/propose',
    note_b='signing options; policy update -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    441,
    'SBOM generation gaps in the pipeline:\n\n- **Syft** — SPDX JSON on every build\n- **CycloneDX** — merge deps from monorepo\n- **VEX** — attach exploitability statements\n\nWhich SBOM artifact should I add to CI?',
    'Which SBOM artifact should I add to CI?',
    ['Syft', 'CycloneDX', 'VEX'],
    'SBOM generation gaps in the pipeline:\n\n- **Syft** — SPDX JSON on every build\n- **CycloneDX** — merge deps from monorepo\n- **VEX** — attach exploitability statements\n\nWant me to upload the first SBOM to the security portal?',
    'Want me to upload the first SBOM to the security portal?',
    note_a='SBOM options -> multi_choice/propose',
    note_b='generation plan; portal upload -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    442,
    'Deployment window constraints:\n\n- **Freeze** — no prod deploys Friday after 3pm\n- **Maintenance** — DB migration Sunday 2–4am UTC\n- **Exception** — hotfix only with VP approval\n\nWhich window rule should I codify in the runbook?',
    'Which window rule should I codify in the runbook?',
    ['Freeze', 'Maintenance', 'Exception'],
    'Deployment window constraints:\n\n- **Freeze** — no prod deploys Friday after 3pm\n- **Maintenance** — DB migration Sunday 2–4am UTC\n- **Exception** — hotfix only with VP approval\n\nShall I add a calendar reminder for the next freeze?',
    'Shall I add a calendar reminder for the next freeze?',
    note_a='rule selection -> multi_choice/propose',
    note_b='window policies; calendar reminder -> yes_no',
    ka='m',
    pa=True,
    pb=False,
    ms_a=False,
)

add(
    443,
    'Post-deploy smoke test suite:\n\n- **Health endpoints** — GET `/healthz` on all services\n- **Synthetic checkout** — place $0 auth-only order\n- **Auth login** — resource-owner password grant in staging mirror\n\nWhich smoke test should I add to the deploy job?',
    'Which smoke test should I add to the deploy job?',
    ['Health endpoints', 'Synthetic checkout', 'Auth login'],
    'Post-deploy smoke test suite:\n\n- **Health endpoints** — GET `/healthz` on all services\n- **Synthetic checkout** — place $0 auth-only order\n- **Auth login** — resource-owner password grant in staging mirror\n\nWant me to wire failures to block the promote step?',
    'Want me to wire failures to block the promote step?',
    note_a='test pick -> multi_choice/propose',
    note_b='smoke plan; block promote -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    444,
    'Staged rollout gates for mobile release:\n\n- **Internal track** — 100% `@corp` testers\n- **Closed beta** — 5% Play Console staged\n- **Production** — phased 10% → 100%\n\nWhich store track should I promote to next?',
    'Which store track should I promote to next?',
    ['Internal track', 'Closed beta', 'Production'],
    'Staged rollout gates for mobile release:\n\n- **Internal track** — 100% `@corp` testers\n- **Closed beta** — 5% Play Console staged\n- **Production** — phased 10% → 100%\n\nShall I pause auto-promote until crash-free > 99.5%?',
    'Shall I pause auto-promote until crash-free > 99.5%?',
    note_a='track selection -> multi_choice/propose',
    note_b='rollout stages; pause auto-promote -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    445,
    'Config drift between staging and prod:\n\n1. **Feature flags** — 12 flags differ\n2. **Rate limits** — prod 2× staging thresholds\n3. **DB pool size** — prod connections maxed\n\nWhich config drift should I reconcile first?',
    'Which config drift should I reconcile first?',
    ['Feature flags', 'Rate limits', 'DB pool size'],
    'Config drift between staging and prod:\n\n1. **Feature flags** — 12 flags differ\n2. **Rate limits** — prod 2× staging thresholds\n3. **DB pool size** — prod connections maxed\n\nWant me to export a diff report from the config service?',
    'Want me to export a diff report from the config service?',
    note_a='drift pick -> multi_choice/propose',
    note_b='drift inventory; diff export -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    446,
    'Environment promotion pipeline:\n\n- **Dev → staging** — auto on main merge\n- **Staging → prod** — manual approval gate\n- **Prod → DR** — nightly sync job\n\nWhich promotion step should I automate next?',
    'Which promotion step should I automate next?',
    ['Dev → staging', 'Staging → prod', 'Prod → DR'],
    'Environment promotion pipeline:\n\n- **Dev → staging** — auto on main merge\n- **Staging → prod** — manual approval gate\n- **Prod → DR** — nightly sync job\n\nShall I add a Slack approval button for prod?',
    'Shall I add a Slack approval button for prod?',
    note_a='promotion choices -> multi_choice/propose',
    note_b='pipeline stages; Slack approval -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    447,
    'Release notes audience variants:\n\n- **Customer-facing** — highlights + upgrade steps\n- **Internal** — commit list + risk notes\n- **Partner API** — breaking changes only\n\nWhich release notes template should I draft for v2.8?',
    'Which release notes template should I draft for v2.8?',
    ['Customer-facing', 'Internal', 'Partner API'],
    'Release notes audience variants:\n\n- **Customer-facing** — highlights + upgrade steps\n- **Internal** — commit list + risk notes\n- **Partner API** — breaking changes only\n\nWant me to publish the draft to Confluence for review?',
    'Want me to publish the draft to Confluence for review?',
    note_a='template pick -> multi_choice/propose',
    note_b='audience variants; Confluence draft -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    448,
    'Tag signing policy options:\n\n- GPG signed tags — require maintainer key\n- GitHub verified — auto-sign via Actions\n\nShould release tags be GPG-signed or GitHub-verified?',
    'Should release tags be GPG-signed or GitHub-verified?',
    ['GPG signed tags', 'GitHub verified'],
    'Tag signing policy options:\n\n- GPG signed tags — require maintainer key\n- GitHub verified — auto-sign via Actions\n\nShall I update the release workflow to enforce signing?',
    'Shall I update the release workflow to enforce signing?',
    note_a='two signing policies -> either_or/propose',
    note_b='policy options; workflow enforce -> yes_no/propose',
    ka='e',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    449,
    'Pre-release channel strategy:\n\n- **Alpha** — nightly from main\n- **Beta** — weekly RC from release branch\n- **Stable** — monthly tagged release\n\nWhich channel should get the current build?',
    'Which channel should get the current build?',
    ['Alpha', 'Beta', 'Stable'],
    'Pre-release channel strategy:\n\n- **Alpha** — nightly from main\n- **Beta** — weekly RC from release branch\n- **Stable** — monthly tagged release\n\nWant me to bump the channel manifest and notify subscribers?',
    'Want me to bump the channel manifest and notify subscribers?',
    note_a='channel selection -> multi_choice/propose',
    note_b='channel plan; manifest bump -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

add(
    450,
    'Post-deploy verification checklist:\n\n- **Metrics** — error rate flat for 15m\n- **Traces** — no new latency outliers\n- **Support queue** — no spike in billing tickets\n\nWhich verification signal should I watch first?',
    'Which verification signal should I watch first?',
    ['Metrics', 'Traces', 'Support queue'],
    'Post-deploy verification checklist:\n\n- **Metrics** — error rate flat for 15m\n- **Traces** — no new latency outliers\n- **Support queue** — no spike in billing tickets\n\nShall I mark the deploy complete in the release tracker?',
    'Shall I mark the deploy complete in the release tracker?',
    note_a='signal pick -> multi_choice/propose',
    note_b='verification checklist; mark complete -> yes_no/propose',
    ka='m',
    pa=True,
    pb=True,
    ms_a=False,
)

assert len(PAIRS) == 100
assert [p["n"] for p in PAIRS] == list(range(351, 451))
