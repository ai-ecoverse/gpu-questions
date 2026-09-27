"""Handcrafted propose vs preference pairs pb0526–pb0600."""
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


# --- security ---
add(
    526,
    "Dependabot opened twelve PRs overnight. The `lodash` bump in `packages/shared` is the only one touching production runtime code.\n\nWant me to merge that patch release and leave the devDependency bumps for Monday?",
    "Want me to merge that patch release and leave the devDependency bumps for Monday?",
    "Dependabot opened twelve PRs overnight. The `lodash` bump in `packages/shared` is the only one touching production runtime code.\n\nWhich merge strategy do you prefer for the rest — batch by ecosystem or review each PR individually?",
    "Which merge strategy do you prefer for the rest — batch by ecosystem or review each PR individually?",
    note_a="merge one patch -> yes_no/propose",
    note_b="strategy fork without agent action -> either_or",
    opts_b=["batch by ecosystem", "review each PR individually"],
)

add(
    527,
    "The container scan on `billing-api:2.14.0` flagged CVE-2024-3094 in `xz-utils`. Base image is `debian:bookworm-slim`.\n\nShall I rebuild from `bookworm-slim` with `--no-cache` and redeploy to staging?",
    "Shall I rebuild from `bookworm-slim` with `--no-cache` and redeploy to staging?",
    "The container scan on `billing-api:2.14.0` flagged CVE-2024-3094 in `xz-utils`. Base image is `debian:bookworm-slim`.\n\nWhich remediation path do you want — rebuild the image or pin `xz-utils` to a known-good digest in the Dockerfile?",
    "Which remediation path do you want — rebuild the image or pin `xz-utils` to a known-good digest in the Dockerfile?",
    note_a="rebuild and redeploy -> yes_no/propose",
    note_b="two fix routes; user picks, no agent commit -> either_or",
    opts_b=["rebuild the image", "pin `xz-utils` to a known-good digest"],
)

add(
    528,
    "[CODE]\n```python\n# middleware/rate_limit.py\nif request.headers.get(\"X-Api-Key\"):\n    bucket = f\"key:{request.headers['X-Api-Key']}\"\nelse:\n    bucket = f\"ip:{request.client.host}\"\n```\n\nAbuse spike is mostly shared-NAT office egress. Want me to tighten per-IP limits and leave key buckets unchanged?",
    "Want me to tighten per-IP limits and leave key buckets unchanged?",
    "[CODE]\n```python\n# middleware/rate_limit.py\nif request.headers.get(\"X-Api-Key\"):\n    bucket = f\"key:{request.headers['X-Api-Key']}\"\nelse:\n    bucket = f\"ip:{request.client.host}\"\n```\n\nAbuse spike is mostly shared-NAT office egress. Should rate limiting key off API keys or client IP for anonymous routes?",
    "Should rate limiting key off API keys or client IP for anonymous routes?",
    note_a="tighten IP limits -> yes_no/propose",
    note_b="bucket strategy preference -> either_or",
    opts_b=["API keys", "client IP"],
)

add(
    529,
    "SBOM export for the release candidate is empty for two transitive deps pulled via Git URL. Compliance wants SPDX JSON before sign-off.\n\nWant me to run Syft against the built image and attach the SPDX file to the release ticket?",
    "Want me to run Syft against the built image and attach the SPDX file to the release ticket?",
    "SBOM export for the release candidate is empty for two transitive deps pulled via Git URL. Compliance wants SPDX JSON before sign-off.\n\nWhich SBOM format should we standardize on — SPDX or CycloneDX?",
    "Which SBOM format should we standardize on — SPDX or CycloneDX?",
    note_a="generate and attach SBOM -> yes_no/propose",
    note_b="format preference only -> either_or",
    opts_b=["SPDX", "CycloneDX"],
)

add(
    530,
    "Pen test report landed. Critical: unauthenticated SSRF in `/api/preview?url=`. High: IDOR on invoice download.\n\nShall I hotfix the SSRF path with an allowlist and open a follow-up for the IDOR?",
    "Shall I hotfix the SSRF path with an allowlist and open a follow-up for the IDOR?",
    "Pen test report landed. Critical: unauthenticated SSRF in `/api/preview?url=`. High: IDOR on invoice download.\n\nWhich finding should engineering tackle first?",
    "Which finding should engineering tackle first?",
    note_a="hotfix SSRF now -> yes_no/propose",
    note_b="priority preference without agent plan -> either_or",
    opts_b=["unauthenticated SSRF in `/api/preview?url=`", "IDOR on invoice download"],
    kb="e",
)

add(
    531,
    "Hashicorp Vault lease on the DB credential is 24h but app pods restart every 6h — no rotation errors yet, but the runbook says 1h max.\n\nWant me to drop the lease TTL to 1h and roll the deployment?",
    "Want me to drop the lease TTL to 1h and roll the deployment?",
    "Hashicorp Vault lease on the DB credential is 24h but app pods restart every 6h — no rotation errors yet, but the runbook says 1h max.\n\nWhich rotation model do you prefer — dynamic secrets on every pod start or a sidecar that refreshes in place?",
    "Which rotation model do you prefer — dynamic secrets on every pod start or a sidecar that refreshes in place?",
    note_a="shorten TTL and roll -> yes_no/propose",
    note_b="architecture preference -> either_or",
    opts_b=["dynamic secrets on every pod start", "sidecar that refreshes in place"],
)

add(
    532,
    "Security champions asked for CT log monitoring on `*.example.com`. We already renew via Let's Encrypt but nothing alerts on rogue certs.\n\nShall I wire certstream alerts into the `#sec-ops` channel this week?",
    "Shall I wire certstream alerts into the `#sec-ops` channel this week?",
    "Security champions asked for CT log monitoring on `*.example.com`. We already renew via Let's Encrypt but nothing alerts on rogue certs.\n\nWhich CT feed do you want to rely on — crt.sh polling or a commercial CT monitor?",
    "Which CT feed do you want to rely on — crt.sh polling or a commercial CT monitor?",
    note_a="enable alerting -> yes_no/propose",
    note_b="feed preference, no setup offer -> either_or",
    opts_b=["crt.sh polling", "commercial CT monitor"],
)

# --- ML ---
add(
    533,
    "Offline eval shows the reranker dropped NDCG@10 from 0.41 to 0.36 after the catalog skew shift. Training data ends at June.\n\nWant a diff that adds the July–August backfill job and retrains the reranker tonight?",
    "Want a diff that adds the July–August backfill job and retrains the reranker tonight?",
    "Offline eval shows the reranker dropped NDCG@10 from 0.41 to 0.36 after the catalog skew shift. Training data ends at June.\n\nWhich recovery path do you prefer — refresh training data or roll back to the June checkpoint?",
    "Which recovery path do you prefer — refresh training data or roll back to the June checkpoint?",
    note_a="backfill and retrain -> yes_no/propose",
    note_b="recovery fork without agent schedule -> either_or",
    opts_b=["refresh training data", "roll back to the June checkpoint"],
)

add(
    534,
    "Production drift detector fired on `user_embedding_v3`: PSI 0.22 on `country_code`. No SLA breach yet.\n\nShall I shadow-deploy the last known-good model and compare latency for an hour?",
    "Shall I shadow-deploy the last known-good model and compare latency for an hour?",
    "Production drift detector fired on `user_embedding_v3`: PSI 0.22 on `country_code`. No SLA breach yet.\n\nDo you want to retrain on recent data or adjust the drift threshold before paging anyone?",
    "Do you want to retrain on recent data or adjust the drift threshold before paging anyone?",
    note_a="shadow deploy comparison -> yes_no/propose",
    note_b="response preference -> either_or",
    opts_b=["retrain on recent data", "adjust the drift threshold"],
)

add(
    535,
    "Embedding index for support tickets is 48h stale — incremental upserts lag during peak. Query latency is fine but recall dropped in eval.\n\nWant me to rebuild the FAISS index from Snowflake exports and swap aliases?",
    "Want me to rebuild the FAISS index from Snowflake exports and swap aliases?",
    "Embedding index for support tickets is 48h stale — incremental upserts lag during peak. Query latency is fine but recall dropped in eval.\n\nWhich index backend should we standardize on — self-hosted FAISS or managed Pinecone?",
    "Which index backend should we standardize on — self-hosted FAISS or managed Pinecone?",
    note_a="rebuild and swap -> yes_no/propose",
    note_b="backend preference -> either_or",
    opts_b=["self-hosted FAISS", "managed Pinecone"],
)

add(
    536,
    "Label audit sampled 500 rows from the fraud model set — 8% disagreements, mostly borderline `device_reuse` cases.\n\nShall I launch an active-learning round that surfaces uncertain rows to Label Studio?",
    "Shall I launch an active-learning round that surfaces uncertain rows to Label Studio?",
    "Label audit sampled 500 rows from the fraud model set — 8% disagreements, mostly borderline `device_reuse` cases.\n\nWhich cleanup approach do you prefer — relabel the disputed bucket or drop ambiguous rows from training?",
    "Which cleanup approach do you prefer — relabel the disputed bucket or drop ambiguous rows from training?",
    note_a="active-learning round -> yes_no/propose",
    note_b="cleanup strategy preference -> either_or",
    opts_b=["relabel the disputed bucket", "drop ambiguous rows from training"],
)

add(
    537,
    "GPU inference queue depth spiked to 400 during the flash sale. p99 latency hit 2.1s with batch size fixed at 32.\n\nWant me to enable dynamic batching in Triton and cap wait at 50ms?",
    "Want me to enable dynamic batching in Triton and cap wait at 50ms?",
    "GPU inference queue depth spiked to 400 during the flash sale. p99 latency hit 2.1s with batch size fixed at 32.\n\nWhich batching policy do you prefer — dynamic batching with a short wait or a larger fixed batch size?",
    "Which batching policy do you prefer — dynamic batching with a short wait or a larger fixed batch size?",
    note_a="enable dynamic batching -> yes_no/propose",
    note_b="batching preference -> either_or",
    opts_b=["dynamic batching with a short wait", "larger fixed batch size"],
)

add(
    538,
    "Fine-tune job for `support_summarizer` OOM'd on the A100 quota. Spot preemption killed two runs overnight.\n\nShall I resubmit on on-demand `a100-80gb` with gradient checkpointing enabled?",
    "Shall I resubmit on on-demand `a100-80gb` with gradient checkpointing enabled?",
    "Fine-tune job for `support_summarizer` OOM'd on the A100 quota. Spot preemption killed two runs overnight.\n\nWhich capacity mode should we use for this training run — spot instances or on-demand GPUs?",
    "Which capacity mode should we use for this training run — spot instances or on-demand GPUs?",
    note_a="resubmit on-demand -> yes_no/propose",
    note_b="capacity preference -> either_or",
    opts_b=["spot instances", "on-demand GPUs"],
)

add(
    539,
    "Imbalanced churn set: PR-AUC looks great but precision@100 is unusable for sales outreach. Product wants fewer false positives.\n\nWant me to switch the eval dashboard to precision@k and re-rank the champion list?",
    "Want me to switch the eval dashboard to precision@k and re-rank the champion list?",
    "Imbalanced churn set: PR-AUC looks great but precision@100 is unusable for sales outreach. Product wants fewer false positives.\n\nWhich metric should we optimize for in the next experiment — F1 or precision at top-k?",
    "Which metric should we optimize for in the next experiment — F1 or precision at top-k?",
    note_a="change dashboard metric -> yes_no/propose",
    note_b="metric preference -> either_or",
    opts_b=["F1", "precision at top-k"],
)

# --- mobile ---
add(
    540,
    "iOS push extension truncates the order-update payload when images attach — users see `…` mid tracking number.\n\nWant me to strip the hero image from the extension payload and keep full text?",
    "Want me to strip the hero image from the extension payload and keep full text?",
    "iOS push extension truncates the order-update payload when images attach — users see `…` mid tracking number.\n\nWhich delivery shape do you prefer — text-only pushes or silent pushes that open the in-app inbox?",
    "Which delivery shape do you prefer — text-only pushes or silent pushes that open the in-app inbox?",
    note_a="strip image from payload -> yes_no/propose",
    note_b="payload strategy preference -> either_or",
    opts_b=["text-only pushes", "silent pushes that open the in-app inbox"],
)

add(
    541,
    "Offline cart sync on Android conflicted when airplane mode toggled mid-checkout — local quantity 2, server quantity 1.\n\nShall I ship a hotfix that applies last-write-wins for line items until CRDT lands?",
    "Shall I ship a hotfix that applies last-write-wins for line items until CRDT lands?",
    "Offline cart sync on Android conflicted when airplane mode toggled mid-checkout — local quantity 2, server quantity 1.\n\nWhich conflict policy do you want long term — last-write-wins or CRDT merge for cart lines?",
    "Which conflict policy do you want long term — last-write-wins or CRDT merge for cart lines?",
    note_a="hotfix LWW -> yes_no/propose",
    note_b="long-term policy preference -> either_or",
    opts_b=["last-write-wins", "CRDT merge for cart lines"],
)

add(
    542,
    "App Store Connect warns the IPA is 212 MB — limit is 200 MB over cellular. Most bulk is unused 3x asset catalogs.\n\nWant me to enable on-demand resources for the seasonal sticker pack and rebuild?",
    "Want me to enable on-demand resources for the seasonal sticker pack and rebuild?",
    "App Store Connect warns the IPA is 212 MB — limit is 200 MB over cellular. Most bulk is unused 3x asset catalogs.\n\nWhich slimming approach do you prefer — on-demand resources or dropping @3x assets from the main bundle?",
    "Which slimming approach do you prefer — on-demand resources or dropping @3x assets from the main bundle?",
    note_a="enable ODR and rebuild -> yes_no/propose",
    note_b="size strategy preference -> either_or",
    opts_b=["on-demand resources", "dropping @3x assets from the main bundle"],
)

add(
    543,
    "Marketing link `example://promo/summer` opens the app but Android App Links verification fails on `/promo/*`.\n\nShall I publish the Digital Asset Links file and rerun verification?",
    "Shall I publish the Digital Asset Links file and rerun verification?",
    "Marketing link `example://promo/summer` opens the app but Android App Links verification fails on `/promo/*`.\n\nWhich deep-link route should be canonical — universal HTTPS links or the custom `example://` scheme?",
    "Which deep-link route should be canonical — universal HTTPS links or the custom `example://` scheme?",
    note_a="publish asset links -> yes_no/propose",
    note_b="link scheme preference -> either_or",
    opts_b=["universal HTTPS links", "custom `example://` scheme"],
)

add(
    544,
    "Battery report from TestFlight: background location for store pickup drains 4%/hr even when no active order.\n\nWant me to drop to `visit` monitoring and geofence only active pickups?",
    "Want me to drop to `visit` monitoring and geofence only active pickups?",
    "Battery report from TestFlight: background location for store pickup drains 4%/hr even when no active order.\n\nWhich location strategy do you prefer — visit monitoring or significant-change only?",
    "Which location strategy do you prefer — visit monitoring or significant-change only?",
    note_a="reduce location polling -> yes_no/propose",
    note_b="location mode preference -> either_or",
    opts_b=["visit monitoring", "significant-change only"],
)

add(
    545,
    "Widget timeline for order tracking refreshes every 15 minutes but couriers often batch scans — UI looks stale on lock screen.\n\nShall I extend the widget timeline with placeholder statuses and push-driven reloads?",
    "Shall I extend the widget timeline with placeholder statuses and push-driven reloads?",
    "Widget timeline for order tracking refreshes every 15 minutes but couriers often batch scans — UI looks stale on lock screen.\n\nWhich refresh model do you prefer — longer timeline entries or background URLSession pulls?",
    "Which refresh model do you prefer — longer timeline entries or background URLSession pulls?",
    note_a="extend timeline + push reloads -> yes_no/propose",
    note_b="refresh preference -> either_or",
    opts_b=["longer timeline entries", "background URLSession pulls"],
)

add(
    546,
    "Android 14 users deny `POST_NOTIFICATIONS` then miss delivery alerts. Current flow requests permission on first launch cold.\n\nWant me to move the permission prompt to after the first order is placed with a rationale sheet?",
    "Want me to move the permission prompt to after the first order is placed with a rationale sheet?",
    "Android 14 users deny `POST_NOTIFICATIONS` then miss delivery alerts. Current flow requests permission on first launch cold.\n\nWhich permission UX do you prefer — post-order rationale or progressive prompts per feature?",
    "Which permission UX do you prefer — post-order rationale or progressive prompts per feature?",
    note_a="relocate permission prompt -> yes_no/propose",
    note_b="UX preference -> either_or",
    opts_b=["post-order rationale", "progressive prompts per feature"],
)

# --- payments ---
add(
    547,
    "Stripe dispute `dp_8f2a` needs evidence in 48h — customer claims product not received but tracking shows delivered.\n\nWant me to auto-assemble the shipping proof pack and stage it for your review?",
    "Want me to auto-assemble the shipping proof pack and stage it for your review?",
    "Stripe dispute `dp_8f2a` needs evidence in 48h — customer claims product not received but tracking shows delivered.\n\nWhich chargeback workflow do you prefer — auto-submit when tracking exists or always manual review?",
    "Which chargeback workflow do you prefer — auto-submit when tracking exists or always manual review?",
    note_a="assemble evidence pack -> yes_no/propose",
    note_b="workflow preference -> either_or",
    opts_b=["auto-submit when tracking exists", "always manual review"],
)

add(
    548,
    "EU checkout conversion dipped after PSD2 step-up. Issuer supports TRA exemption on low-risk baskets under €30.\n\nShall I enable TRA for eligible carts and log exemption failures?",
    "Shall I enable TRA for eligible carts and log exemption failures?",
    "EU checkout conversion dipped after PSD2 step-up. Issuer supports TRA exemption on low-risk baskets under €30.\n\nWhich SCA route should we default to — TRA exemption or low-value exemption?",
    "Which SCA route should we default to — TRA exemption or low-value exemption?",
    note_a="enable TRA -> yes_no/propose",
    note_b="SCA preference -> either_or",
    opts_b=["TRA exemption", "low-value exemption"],
)

add(
    549,
    "Marketplace sellers asked for faster payouts. Current schedule aggregates weekly on Monday 06:00 UTC.\n\nWant me to flip the cron to daily payouts with a €1 minimum balance?",
    "Want me to flip the cron to daily payouts with a €1 minimum balance?",
    "Marketplace sellers asked for faster payouts. Current schedule aggregates weekly on Monday 06:00 UTC.\n\nWhich payout cadence do you prefer — daily transfers or keep weekly aggregation?",
    "Which payout cadence do you prefer — daily transfers or keep weekly aggregation?",
    note_a="switch to daily payouts -> yes_no/propose",
    note_b="cadence preference -> either_or",
    opts_b=["daily transfers", "weekly aggregation"],
)

add(
    550,
    "Multi-currency ledger shows €12k FX variance last month — Stripe rates vs internal ECB table.\n\nShall I wire live ECB feeds into the settlement report and backfill October?",
    "Shall I wire live ECB feeds into the settlement report and backfill October?",
    "Multi-currency ledger shows €12k FX variance last month — Stripe rates vs internal ECB table.\n\nWhich FX policy do you want — pass through processor rates or hedge with a fixed daily ECB rate?",
    "Which FX policy do you want — pass through processor rates or hedge with a fixed daily ECB rate?",
    note_a="wire ECB feeds and backfill -> yes_no/propose",
    note_b="FX policy preference -> either_or",
    opts_b=["pass through processor rates", "hedge with a fixed daily ECB rate"],
)

add(
    551,
    "Wallet adoption is 12% on iOS, 3% on Android. Product wants one wallet push before holiday code freeze.\n\nWant me to land Apple Pay first since the checkout webview already exposes `canMakePayments`?",
    "Want me to land Apple Pay first since the checkout webview already exposes `canMakePayments`?",
    "Wallet adoption is 12% on iOS, 3% on Android. Product wants one wallet push before holiday code freeze.\n\nWhich wallet should we prioritize — Apple Pay or Google Pay?",
    "Which wallet should we prioritize — Apple Pay or Google Pay?",
    note_a="ship Apple Pay first -> yes_no/propose",
    note_b="wallet priority preference -> either_or",
    opts_b=["Apple Pay", "Google Pay"],
)

add(
    552,
    "Partial refund on a mixed-tax order failed — Avalara expects line-level amounts but support issued a flat €20 credit.\n\nShall I patch the refund API to prorate tax per line and replay the stuck refund?",
    "Shall I patch the refund API to prorate tax per line and replay the stuck refund?",
    "Partial refund on a mixed-tax order failed — Avalara expects line-level amounts but support issued a flat €20 credit.\n\nWhich partial refund rule do you prefer — prorate tax per line or refund whole line items only?",
    "Which partial refund rule do you prefer — prorate tax per line or refund whole line items only?",
    note_a="prorate tax and replay -> yes_no/propose",
    note_b="refund rule preference -> either_or",
    opts_b=["prorate tax per line", "refund whole line items only"],
)

add(
    553,
    "Fraud velocity alerts tripped on 200 signups from two ASNs — mostly disposable emails, no charge attempts yet.\n\nWant me to enable device fingerprint blocking for those ASNs and page fraud on charge attempts?",
    "Want me to enable device fingerprint blocking for those ASNs and page fraud on charge attempts?",
    "Fraud velocity alerts tripped on 200 signups from two ASNs — mostly disposable emails, no charge attempts yet.\n\nWhich signal should drive the first blocking rule — device fingerprint or IP velocity?",
    "Which signal should drive the first blocking rule — device fingerprint or IP velocity?",
    note_a="enable fingerprint block -> yes_no/propose",
    note_b="signal preference -> either_or",
    opts_b=["device fingerprint", "IP velocity"],
)

# --- DNS ---
add(
    554,
    "Resolver logs show EDNS Client Subnet leaking office prefixes to authoritative NS for `cdn.example.com`.\n\nShall I disable ECS on the forwarding zone and purge cached answers?",
    "Shall I disable ECS on the forwarding zone and purge cached answers?",
    "Resolver logs show EDNS Client Subnet leaking office prefixes to authoritative NS for `cdn.example.com`.\n\nDo you prefer ECS enabled for latency or disabled for privacy on public zones?",
    "Do you prefer ECS enabled for latency or disabled for privacy on public zones?",
    note_a="disable ECS and purge -> yes_no/propose",
    note_b="ECS preference -> either_or",
    opts_b=["enabled for latency", "disabled for privacy"],
)

add(
    555,
    "Corporate laptops will use DNS-over-HTTPS by policy next quarter. Current split-tunnel sends `.corp` to BIND, everything else to ISP.\n\nWant me to pilot DoH to Cloudflare Gateway on the IT VLAN this sprint?",
    "Want me to pilot DoH to Cloudflare Gateway on the IT VLAN this sprint?",
    "Corporate laptops will use DNS-over-HTTPS by policy next quarter. Current split-tunnel sends `.corp` to BIND, everything else to ISP.\n\nWhich public DoH resolver should we standardize on — Cloudflare or Quad9?",
    "Which public DoH resolver should we standardize on — Cloudflare or Quad9?",
    note_a="pilot DoH on IT VLAN -> yes_no/propose",
    note_b="resolver preference -> either_or",
    opts_b=["Cloudflare", "Quad9"],
)

add(
    556,
    "New staging cluster needs TLS for `*.staging.example.com` plus apex `staging.example.com` on the same cert.\n\nShall I request a cert covering apex, wildcard, and the legacy `api-staging` SAN?",
    "Shall I request a cert covering apex, wildcard, and the legacy `api-staging` SAN?",
    "New staging cluster needs TLS for `*.staging.example.com` plus apex `staging.example.com` on the same cert.\n\nWhich SAN coverage do you want on the staging cert — apex + wildcard only or include `api-staging` too?",
    "Which SAN coverage do you want on the staging cert — apex + wildcard only or include `api-staging` too?",
    note_a="request expanded cert -> yes_no/propose",
    note_b="SAN scope preference -> either_or",
    opts_b=["apex + wildcard only", "include `api-staging` too"],
)

add(
    557,
    "Incident playbook says drop TTL before rollback, but `shop.example.com` is still at 3600s from last month's migration.\n\nWant me to lower TTL to 60s now and schedule the rollback window for tonight?",
    "Want me to lower TTL to 60s now and schedule the rollback window for tonight?",
    "Incident playbook says drop TTL before rollback, but `shop.example.com` is still at 3600s from last month's migration.\n\nDuring incidents do you prefer aggressive 30s TTL or keep 300s for resolver stability?",
    "During incidents do you prefer aggressive 30s TTL or keep 300s for resolver stability?",
    note_a="lower TTL and schedule rollback -> yes_no/propose",
    note_b="TTL policy preference -> either_or",
    opts_b=["aggressive 30s TTL", "keep 300s for resolver stability"],
)

add(
    558,
    "Mesh services still hard-code `redis.internal` in ConfigMaps — moving clusters means grep-and-replace.\n\nShall I stand up CoreDNS stub zones that CNAME to the new service entries?",
    "Shall I stand up CoreDNS stub zones that CNAME to the new service entries?",
    "Mesh services still hard-code `redis.internal` in ConfigMaps — moving clusters means grep-and-replace.\n\nWhich service discovery backend should we adopt — CoreDNS stub zones or Consul service catalog?",
    "Which service discovery backend should we adopt — CoreDNS stub zones or Consul service catalog?",
    note_a="deploy CoreDNS stubs -> yes_no/propose",
    note_b="discovery backend preference -> either_or",
    opts_b=["CoreDNS stub zones", "Consul service catalog"],
)

add(
    559,
    "CA offers DANE TLSA records for the new cert chain but the registrar DNS panel is still manual.\n\nWant me to publish TLSA `3 1 1` hashes for the leaf and intermediate?",
    "Want me to publish TLSA `3 1 1` hashes for the leaf and intermediate?",
    "CA offers DANE TLSA records for the new cert chain but the registrar DNS panel is still manual.\n\nDo you want to publish DANE now or wait until automated DNS API access lands?",
    "Do you want to publish DANE now or wait until automated DNS API access lands?",
    note_a="publish TLSA records -> yes_no/propose",
    note_b="timing preference -> either_or",
    opts_b=["publish DANE now", "wait until automated DNS API access lands"],
)

add(
    560,
    "[URL] shows conflicting SPF includes after the Mailgun migration.\n\nShall I flatten the SPF record to stay under ten lookups?",
    "Shall I flatten the SPF record to stay under ten lookups?",
    "[URL] shows conflicting SPF includes after the Mailgun migration.\n\nWhich SPF maintenance approach do you prefer — automated flattening or manual TXT consolidation?",
    "Which SPF maintenance approach do you prefer — automated flattening or manual TXT consolidation?",
    note_a="flatten SPF now -> yes_no/propose",
    note_b="maintenance preference -> either_or",
    opts_b=["automated flattening", "manual TXT consolidation"],
)

# --- email ---
add(
    561,
    "Brand team uploaded a BIMI SVG but mailbox providers want a VMC before showing the logo in Gmail.\n\nWant me to open the VMC purchase request with DigiCert and park the SVG in DNS?",
    "Want me to open the VMC purchase request with DigiCert and park the SVG in DNS?",
    "Brand team uploaded a BIMI SVG but mailbox providers want a VMC before showing the logo in Gmail.\n\nWhich rollout order do you prefer — VMC first or publish BIMI DNS now without logo display?",
    "Which rollout order do you prefer — VMC first or publish BIMI DNS now without logo display?",
    note_a="start VMC purchase -> yes_no/propose",
    note_b="rollout order preference -> either_or",
    opts_b=["VMC first", "publish BIMI DNS now without logo display"],
)

add(
    562,
    "New dedicated IP warmed to 5k/day but Yahoo deferrals spiked after yesterday's promo blast.\n\nShall I throttle today's marketing send to 2k and spread the remainder across the week?",
    "Shall I throttle today's marketing send to 2k and spread the remainder across the week?",
    "New dedicated IP warmed to 5k/day but Yahoo deferrals spiked after yesterday's promo blast.\n\nWhich warm-up strategy do you prefer — gradual volume ramp or separate subdomain isolation?",
    "Which warm-up strategy do you prefer — gradual volume ramp or separate subdomain isolation?",
    note_a="throttle send volume -> yes_no/propose",
    note_b="warm-up preference -> either_or",
    opts_b=["gradual volume ramp", "separate subdomain isolation"],
)

add(
    563,
    "Product wants interactive checkout reminders in Gmail. AMP HTML passes lint but fallback MIME part is untested in Outlook.\n\nWant me to enable AMP for the receipt template behind a 1% holdout?",
    "Want me to enable AMP for the receipt template behind a 1% holdout?",
    "Product wants interactive checkout reminders in Gmail. AMP HTML passes lint but fallback MIME part is untested in Outlook.\n\nWhich email format should be canonical — AMP with static fallback or static HTML only?",
    "Which email format should be canonical — AMP with static fallback or static HTML only?",
    note_a="enable AMP holdout -> yes_no/propose",
    note_b="format preference -> either_or",
    opts_b=["AMP with static fallback", "static HTML only"],
)

add(
    564,
    "Gmail one-click unsubscribe is live but List-Unsubscribe-Post returns 405 on our legacy endpoint.\n\nShall I deploy the RFC 8058 POST handler and backfill headers on queued campaigns?",
    "Shall I deploy the RFC 8058 POST handler and backfill headers on queued campaigns?",
    "Gmail one-click unsubscribe is live but List-Unsubscribe-Post returns 405 on our legacy endpoint.\n\nWhich unsubscribe mechanism should we treat as primary — List-Unsubscribe-Post or mailto fallback?",
    "Which unsubscribe mechanism should we treat as primary — List-Unsubscribe-Post or mailto fallback?",
    note_a="deploy POST handler -> yes_no/propose",
    note_b="mechanism preference -> either_or",
    opts_b=["List-Unsubscribe-Post", "mailto fallback"],
)

add(
    565,
    "Dark-mode clients render our receipt template with navy text on charcoal — contrast fails in Apple Mail night mode.\n\nWant me to add `@media (prefers-color-scheme: dark)` overrides and resync the template?",
    "Want me to add `@media (prefers-color-scheme: dark)` overrides and resync the template?",
    "Dark-mode clients render our receipt template with navy text on charcoal — contrast fails in Apple Mail night mode.\n\nWhich dark-mode approach do you prefer — CSS media queries or separate dark HTML templates?",
    "Which dark-mode approach do you prefer — CSS media queries or separate dark HTML templates?",
    note_a="add dark CSS overrides -> yes_no/propose",
    note_b="dark-mode strategy preference -> either_or",
    opts_b=["CSS media queries", "separate dark HTML templates"],
)

add(
    566,
    "Inbound parse webhook from SendGrid failed HMAC verification on 14 messages — all from the same forwarding rule.\n\nShall I rotate the signing secret and replay those 14 payloads from the event log?",
    "Shall I rotate the signing secret and replay those 14 payloads from the event log?",
    "Inbound parse webhook from SendGrid failed HMAC verification on 14 messages — all from the same forwarding rule.\n\nWhich inbound trust model do you prefer — HMAC signature verification or IP allowlisting?",
    "Which inbound trust model do you prefer — HMAC signature verification or IP allowlisting?",
    note_a="rotate secret and replay -> yes_no/propose",
    note_b="trust model preference -> either_or",
    opts_b=["HMAC signature verification", "IP allowlisting"],
)

add(
    567,
    "Deliverability tanked after yesterday's win-back blast — complaints tripped Yahoo's bulk threshold.\n\nWant me to pause the win-back drip until reputation recovers?",
    "Want me to pause the win-back drip until reputation recovers?",
    "Deliverability tanked after yesterday's win-back blast — complaints tripped Yahoo's bulk threshold.\n\nShould we pause the win-back drip or switch to transactional-only sends?",
    "Should we pause the win-back drip or switch to transactional-only sends?",
    note_a="pause drip -> yes_no/propose",
    note_b="send strategy preference -> either_or",
    opts_b=["pause the win-back drip", "transactional-only sends"],
)

# --- a11y ---
add(
    568,
    "Hero carousel autoplay ignores `prefers-reduced-motion` — vestibular disorder report from beta.\n\nWant me to disable autoplay when reduced motion is requested and expose manual controls?",
    "Want me to disable autoplay when reduced motion is requested and expose manual controls?",
    "Hero carousel autoplay ignores `prefers-reduced-motion` — vestibular disorder report from beta.\n\nWhich motion policy do you prefer — honor reduced motion or remove autoplay entirely?",
    "Which motion policy do you prefer — honor reduced motion or remove autoplay entirely?",
    note_a="disable autoplay on PRM -> yes_no/propose",
    note_b="motion policy preference -> either_or",
    opts_b=["honor reduced motion", "remove autoplay entirely"],
)

add(
    569,
    "Keyboard users on Safari can't see focus rings on ghost buttons — `:focus-visible` polyfill isn't loaded on marketing pages.\n\nShall I add the polyfill bundle and a `:focus-visible` utility in Tailwind?",
    "Shall I add the polyfill bundle and a `:focus-visible` utility in Tailwind?",
    "Keyboard users on Safari can't see focus rings on ghost buttons — `:focus-visible` polyfill isn't loaded on marketing pages.\n\nWhich focus styling approach do you prefer — `:focus-visible` polyfill or always-on outline utilities?",
    "Which focus styling approach do you prefer — `:focus-visible` polyfill or always-on outline utilities?",
    note_a="add polyfill bundle -> yes_no/propose",
    note_b="focus styling preference -> either_or",
    opts_b=["`:focus-visible` polyfill", "always-on outline utilities"],
)

add(
    570,
    "Analytics dashboard charts have no non-visual alternative — screen reader users hear silence on the revenue widget.\n\nWant me to add a visually hidden data table mirror for each chart?",
    "Want me to add a visually hidden data table mirror for each chart?",
    "Analytics dashboard charts have no non-visual alternative — screen reader users hear silence on the revenue widget.\n\nWhich chart accessibility pattern do you prefer — data table fallback or sonified summaries?",
    "Which chart accessibility pattern do you prefer — data table fallback or sonified summaries?",
    note_a="add data table mirror -> yes_no/propose",
    note_b="chart a11y preference -> either_or",
    opts_b=["data table fallback", "sonified summaries"],
)

add(
    571,
    "Kanban drag-and-drop has no keyboard path — audit flagged WCAG 2.2 drag alternative.\n\nShall I add move-up/move-down buttons on each card for keyboard reorder?",
    "Shall I add move-up/move-down buttons on each card for keyboard reorder?",
    "Kanban drag-and-drop has no keyboard path — audit flagged WCAG 2.2 drag alternative.\n\nWhich drag alternative do you prefer — explicit move buttons or a keyboard-only reorder dialog?",
    "Which drag alternative do you prefer — explicit move buttons or a keyboard-only reorder dialog?",
    note_a="add move buttons -> yes_no/propose",
    note_b="alternative preference -> either_or",
    opts_b=["explicit move buttons", "keyboard-only reorder dialog"],
)

add(
    572,
    "Training video captions drift 300ms late on module 4 — auto-sync confidence was low.\n\nWant me to re-run forced alignment and publish corrected VTT?",
    "Want me to re-run forced alignment and publish corrected VTT?",
    "Training video captions drift 300ms late on module 4 — auto-sync confidence was low.\n\nWhich caption fix do you prefer — auto-sync realignment or manual offset adjustment?",
    "Which caption fix do you prefer — auto-sync realignment or manual offset adjustment?",
    note_a="realign captions -> yes_no/propose",
    note_b="caption fix preference -> either_or",
    opts_b=["auto-sync realignment", "manual offset adjustment"],
)

add(
    573,
    "Windows high-contrast mode strips our custom focus colors — buttons disappear against the background.\n\nShall I add `@media (forced-colors: active)` overrides for primary actions?",
    "Shall I add `@media (forced-colors: active)` overrides for primary actions?",
    "Windows high-contrast mode strips our custom focus colors — buttons disappear against the background.\n\nWhich high-contrast strategy do you prefer — forced-colors media queries or a dedicated high-contrast theme toggle?",
    "Which high-contrast strategy do you prefer — forced-colors media queries or a dedicated high-contrast theme toggle?",
    note_a="add forced-colors CSS -> yes_no/propose",
    note_b="high-contrast strategy preference -> either_or",
    opts_b=["forced-colors media queries", "dedicated high-contrast theme toggle"],
)

add(
    574,
    "Modal traps focus but returns to `<body>` on close instead of the launch button — disorienting in NVDA.\n\nWant me to patch the dialog hook to restore focus to the triggering control?",
    "Want me to patch the dialog hook to restore focus to the triggering control?",
    "Modal traps focus but returns to `<body>` on close instead of the launch button — disorienting in NVDA.\n\nWhich focus restoration behavior do you prefer — return to trigger or stay inside the page landmark?",
    "Which focus restoration behavior do you prefer — return to trigger or stay inside the page landmark?",
    note_a="restore focus to trigger -> yes_no/propose",
    note_b="restoration preference -> either_or",
    opts_b=["return to trigger", "stay inside the page landmark"],
)

# --- i18n ---
add(
    575,
    "Product list sorted by raw UTF-8 codepoints — Swedish `Å` entries appear after `Z`.\n\nShall I switch catalog sorting to `Intl.Collator` with locale-aware options?",
    "Shall I switch catalog sorting to `Intl.Collator` with locale-aware options?",
    "Product list sorted by raw UTF-8 codepoints — Swedish `Å` entries appear after `Z`.\n\nWhich collation approach do you prefer — locale-aware sort or normalized Unicode sort keys?",
    "Which collation approach do you prefer — locale-aware sort or normalized Unicode sort keys?",
    note_a="enable Intl.Collator -> yes_no/propose",
    note_b="collation preference -> either_or",
    opts_b=["locale-aware sort", "normalized Unicode sort keys"],
)

add(
    576,
    "Checkout shows `$12.00 USD` but EU users expect `12,00 €` with narrow symbol placement.\n\nWant me to update price formatting to use narrow currency symbols per CLDR?",
    "Want me to update price formatting to use narrow currency symbols per CLDR?",
    "Checkout shows `$12.00 USD` but EU users expect `12,00 €` with narrow symbol placement.\n\nWhich currency display do you prefer — narrow symbol or ISO code suffix?",
    "Which currency display do you prefer — narrow symbol or ISO code suffix?",
    note_a="apply narrow symbols -> yes_no/propose",
    note_b="currency display preference -> either_or",
    opts_b=["narrow symbol", "ISO code suffix"],
)

add(
    577,
    "Translators keep misinterpreting `{count}` in `items_in_cart` — English comment says \"devices\" but UI is generic.\n\nShall I add Crowdin context screenshots for that key and push string notes?",
    "Shall I add Crowdin context screenshots for that key and push string notes?",
    "Translators keep misinterpreting `{count}` in `items_in_cart` — English comment says \"devices\" but UI is generic.\n\nWhere should translation context live — Crowdin screenshots or in-file developer comments?",
    "Where should translation context live — Crowdin screenshots or in-file developer comments?",
    note_a="add Crowdin context -> yes_no/propose",
    note_b="context location preference -> either_or",
    opts_b=["Crowdin screenshots", "in-file developer comments"],
)

add(
    578,
    "Pseudolocale QA caught truncated German strings but not padding issues — `en-XA` isn't enabled in staging.\n\nWant me to turn on pseudolocale builds in staging and wire them to Percy?",
    "Want me to turn on pseudolocale builds in staging and wire them to Percy?",
    "Pseudolocale QA caught truncated German strings but not padding issues — `en-XA` isn't enabled in staging.\n\nWhich pseudolocale strategy do you prefer — full `en-XA` accents or lengthen-only padding?",
    "Which pseudolocale strategy do you prefer — full `en-XA` accents or lengthen-only padding?",
    note_a="enable pseudolocale in staging -> yes_no/propose",
    note_b="pseudolocale preference -> either_or",
    opts_b=["full `en-XA` accents", "lengthen-only padding"],
)

add(
    579,
    "Compact view shows `1.2M` views but Japanese locale expects `120万` notation.\n\nShall I migrate number formatting to `Intl.NumberFormat` with compact notation?",
    "Shall I migrate number formatting to `Intl.NumberFormat` with compact notation?",
    "Compact view shows `1.2M` views but Japanese locale expects `120万` notation.\n\nWhich number format do you prefer — compact notation or full grouping with separators?",
    "Which number format do you prefer — compact notation or full grouping with separators?",
    note_a="migrate to Intl.NumberFormat -> yes_no/propose",
    note_b="number format preference -> either_or",
    opts_b=["compact notation", "full grouping with separators"],
)

add(
    580,
    "Timezone picker lists 600 flat offsets — users in Sydney miss `Australia/Sydney` when searching \"Sydney\".\n\nWant me to group zones by region with CLDR display names?",
    "Want me to group zones by region with CLDR display names?",
    "Timezone picker lists 600 flat offsets — users in Sydney miss `Australia/Sydney` when searching \"Sydney\".\n\nWhich timezone picker layout do you prefer — region groups or sort by UTC offset?",
    "Which timezone picker layout do you prefer — region groups or sort by UTC offset?",
    note_a="group zones by region -> yes_no/propose",
    note_b="picker layout preference -> either_or",
    opts_b=["region groups", "sort by UTC offset"],
)

add(
    581,
    "Marketing wants a Canadian French site — routing work is blocked until we pick the BCP-47 tag.\n\nWant me to register `fr-CA` in the i18n config and wire the fallback chain?",
    "Want me to register `fr-CA` in the i18n config and wire the fallback chain?",
    "Marketing wants a Canadian French site — routing work is blocked until we pick the BCP-47 tag.\n\nWhat should we name the locale — `fr-CA` or `fr-CA-u-ca-gregory`?",
    "What should we name the locale — `fr-CA` or `fr-CA-u-ca-gregory`?",
    note_a="register locale in config -> yes_no/propose",
    note_b="locale tag naming -> open/not",
    kb="o",
)

# --- wasm ---
add(
    582,
    "[CODE]\n```rust\n// lib.rs\n#[cfg(target_feature = \"simd128\")]\nfn dot_product(a: &[f32], b: &[f32]) -> f32 { /* simd */ }\n```\n\nWasm build without `-C target-feature=+simd128` leaves the scalar path on Apple Silicon.\n\nShall I enable SIMD128 in the release profile and rebuild the module?",
    "Shall I enable SIMD128 in the release profile and rebuild the module?",
    "[CODE]\n```rust\n// lib.rs\n#[cfg(target_feature = \"simd128\")]\nfn dot_product(a: &[f32], b: &[f32]) -> f32 { /* simd */ }\n```\n\nWasm build without `-C target-feature=+simd128` leaves the scalar path on Apple Silicon.\n\nWhich wasm CPU feature set do you prefer — SIMD128 enabled or scalar-only for maximum compatibility?",
    "Which wasm CPU feature set do you prefer — SIMD128 enabled or scalar-only for maximum compatibility?",
    note_a="enable SIMD and rebuild -> yes_no/propose",
    note_b="feature set preference -> either_or",
    opts_b=["SIMD128 enabled", "scalar-only for maximum compatibility"],
)

add(
    583,
    "Image filter plugin uses `SharedArrayBuffer` but COOP/COEP headers aren't on the CDN — threads fall back to single-core.\n\nWant me to add `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` on `/wasm/*`?",
    "Want me to add `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` on `/wasm/*`?",
    "Image filter plugin uses `SharedArrayBuffer` but COOP/COEP headers aren't on the CDN — threads fall back to single-core.\n\nWhich threading approach do you prefer — COOP/COEP for SharedArrayBuffer or stay single-threaded?",
    "Which threading approach do you prefer — COOP/COEP for SharedArrayBuffer or stay single-threaded?",
    note_a="add COOP/COEP headers -> yes_no/propose",
    note_b="threading preference -> either_or",
    opts_b=["COOP/COEP for SharedArrayBuffer", "stay single-threaded"],
)

add(
    584,
    "Rust wasm-pack bundle bloat: `wee_alloc` saves 12 KB but leaks in long sessions per profiling.\n\nShall I switch back to the default allocator and accept the size hit?",
    "Shall I switch back to the default allocator and accept the size hit?",
    "Rust wasm-pack bundle bloat: `wee_alloc` saves 12 KB but leaks in long sessions per profiling.\n\nWhich allocator strategy do you prefer — `wee_alloc` for size or default for stability?",
    "Which allocator strategy do you prefer — `wee_alloc` for size or default for stability?",
    note_a="revert to default allocator -> yes_no/propose",
    note_b="allocator preference -> either_or",
    opts_b=["`wee_alloc` for size", "default for stability"],
)

add(
    585,
    "Editor wants sandboxed plugins — Node wasm runner works but startup is 800ms cold on M2.\n\nWant me to prototype the same API on Wasmtime with AOT compile cached on disk?",
    "Want me to prototype the same API on Wasmtime with AOT compile cached on disk?",
    "Editor wants sandboxed plugins — Node wasm runner works but startup is 800ms cold on M2.\n\nWhich wasm runtime should we standardize on — Wasmtime or Wasmer?",
    "Which wasm runtime should we standardize on — Wasmtime or Wasmer?",
    note_a="prototype Wasmtime AOT -> yes_no/propose",
    note_b="runtime preference -> either_or",
    opts_b=["Wasmtime", "Wasmer"],
)

add(
    586,
    "JS↔WASM boundary serializes large matrices through JSON — 40ms marshaling on 4k textures.\n\nShall I move the buffer exchange to shared linear memory views instead?",
    "Shall I move the buffer exchange to shared linear memory views instead?",
    "JS↔WASM boundary serializes large matrices through JSON — 40ms marshaling on 4k textures.\n\nWhich interop style do you prefer — JSON serialization or shared linear memory?",
    "Which interop style do you prefer — JSON serialization or shared linear memory?",
    note_a="switch to linear memory -> yes_no/propose",
    note_b="interop preference -> either_or",
    opts_b=["JSON serialization", "shared linear memory"],
)

add(
    587,
    "Main wasm module is 1.8 MB gzipped — Lighthouse flags it on first paint.\n\nWant me to run `wasm-opt -Oz` and split the parser into a lazy-loaded chunk?",
    "Want me to run `wasm-opt -Oz` and split the parser into a lazy-loaded chunk?",
    "Main wasm module is 1.8 MB gzipped — Lighthouse flags it on first paint.\n\nWhich size strategy do you prefer — aggressive `wasm-opt` or lazy-loaded split modules?",
    "Which size strategy do you prefer — aggressive `wasm-opt` or lazy-loaded split modules?",
    note_a="wasm-opt and split chunk -> yes_no/propose",
    note_b="size strategy preference -> either_or",
    opts_b=["aggressive `wasm-opt`", "lazy-loaded split modules"],
)

# --- gamedev ---
add(
    588,
    "Physics sim stutters when tab backgrounded — fixed 60Hz tick piles up catch-up steps.\n\nShall I cap catch-up ticks and switch to variable timestep for the demo build?",
    "Shall I cap catch-up ticks and switch to variable timestep for the demo build?",
    "Physics sim stutters when tab backgrounded — fixed 60Hz tick piles up catch-up steps.\n\nWhich simulation clock do you prefer — fixed 60Hz or variable timestep?",
    "Which simulation clock do you prefer — fixed 60Hz or variable timestep?",
    note_a="cap catch-up and switch timestep -> yes_no/propose",
    note_b="clock preference -> either_or",
    opts_b=["fixed 60Hz", "variable timestep"],
)

add(
    589,
    "Multiplayer prototype shows rubber-banding on 120ms RTT — client prediction overshoots corners.\n\nWant me to add server rewind reconciliation for player positions?",
    "Want me to add server rewind reconciliation for player positions?",
    "Multiplayer prototype shows rubber-banding on 120ms RTT — client prediction overshoots corners.\n\nWhich netcode model do you prefer — client-side prediction or server rewind?",
    "Which netcode model do you prefer — client-side prediction or server rewind?",
    note_a="add server rewind -> yes_no/propose",
    note_b="netcode preference -> either_or",
    opts_b=["client-side prediction", "server rewind"],
)

add(
    590,
    "Open-world demo hitches when entering the forest biome — all LOD0 textures load at once.\n\nShall I stream mips by priority queue and defer flora assets?",
    "Shall I stream mips by priority queue and defer flora assets?",
    "Open-world demo hitches when entering the forest biome — all LOD0 textures load at once.\n\nWhich asset streaming policy do you prefer — mip priority queue or distance-based LOD bands?",
    "Which asset streaming policy do you prefer — mip priority queue or distance-based LOD bands?",
    note_a="stream mips with priority -> yes_no/propose",
    note_b="streaming policy preference -> either_or",
    opts_b=["mip priority queue", "distance-based LOD bands"],
)

add(
    591,
    "Save files are plain JSON on disk — players can edit currency in casual mode but competitors want tamper resistance.\n\nWant me to AES-encrypt saves with a device-derived key?",
    "Want me to AES-encrypt saves with a device-derived key?",
    "Save files are plain JSON on disk — players can edit currency in casual mode but competitors want tamper resistance.\n\nWhich save protection level do you prefer — AES encryption or lightweight XOR obfuscation?",
    "Which save protection level do you prefer — AES encryption or lightweight XOR obfuscation?",
    note_a="AES-encrypt saves -> yes_no/propose",
    note_b="protection level preference -> either_or",
    opts_b=["AES encryption", "lightweight XOR obfuscation"],
)

add(
    592,
    "Character mesh is 180k tris at LOD0 — auto decimation to 45k looks fine in stills but shimmers in motion.\n\nShall I bake authored LODs from the art team's Maya exports instead?",
    "Shall I bake authored LODs from the art team's Maya exports instead?",
    "Character mesh is 180k tris at LOD0 — auto decimation to 45k looks fine in stills but shimmers in motion.\n\nWhich LOD pipeline do you prefer — automatic mesh decimation or hand-authored LODs?",
    "Which LOD pipeline do you prefer — automatic mesh decimation or hand-authored LODs?",
    note_a="bake authored LODs -> yes_no/propose",
    note_b="LOD pipeline preference -> either_or",
    opts_b=["automatic mesh decimation", "hand-authored LODs"],
)

add(
    593,
    "Aimbots reported in the beta — client trusts hit detection locally.\n\nWant me to move damage adjudication to the dedicated server this sprint?",
    "Want me to move damage adjudication to the dedicated server this sprint?",
    "Aimbots reported in the beta — client trusts hit detection locally.\n\nWhich anti-cheat posture do you prefer — full server authority or client heuristics with bans?",
    "Which anti-cheat posture do you prefer — full server authority or client heuristics with bans?",
    note_a="server-side damage adjudication -> yes_no/propose",
    note_b="anti-cheat preference -> either_or",
    opts_b=["full server authority", "client heuristics with bans"],
)

# --- observability ---
add(
    594,
    "Trace volume doubled after the GraphQL migration — Jaeger storage costs up 35% with 100% head sampling.\n\nShall I drop head sampling to 1% and keep error spans at 100%?",
    "Shall I drop head sampling to 1% and keep error spans at 100%?",
    "Trace volume doubled after the GraphQL migration — Jaeger storage costs up 35% with 100% head sampling.\n\nWhich sampling strategy do you prefer — head-based 1% or tail-based on latency outliers?",
    "Which sampling strategy do you prefer — head-based 1% or tail-based on latency outliers?",
    note_a="reduce head sampling -> yes_no/propose",
    note_b="sampling preference -> either_or",
    opts_b=["head-based 1%", "tail-based on latency outliers"],
)

add(
    595,
    "Log index cardinality exploded — `user_id` labels on debug lines created 40k series overnight.\n\nWant me to drop debug logs in prod and aggregate request counts at the edge?",
    "Want me to drop debug logs in prod and aggregate request counts at the edge?",
    "Log index cardinality exploded — `user_id` labels on debug lines created 40k series overnight.\n\nWhich cardinality fix do you prefer — drop debug logs or aggregate metrics at ingest?",
    "Which cardinality fix do you prefer — drop debug logs or aggregate metrics at ingest?",
    note_a="drop debug and aggregate -> yes_no/propose",
    note_b="cardinality fix preference -> either_or",
    opts_b=["drop debug logs", "aggregate metrics at ingest"],
)

add(
    596,
    "SLO burn alert fired on API availability — single-window 2h burn page woke everyone for a blip.\n\nShall I switch to multi-window burn rates (5m + 1h) before the next deploy?",
    "Shall I switch to multi-window burn rates (5m + 1h) before the next deploy?",
    "SLO burn alert fired on API availability — single-window 2h burn page woke everyone for a blip.\n\nWhich alert policy do you prefer — multi-window burn rates or a single long threshold?",
    "Which alert policy do you prefer — multi-window burn rates or a single long threshold?",
    note_a="adopt multi-window burn -> yes_no/propose",
    note_b="alert policy preference -> either_or",
    opts_b=["multi-window burn rates", "single long threshold"],
)

add(
    597,
    "[URL] [URL] shows p99 regression but OTLP gRPC exporter queues are backing up.\n\nWant me to flip the collector to OTLP/HTTP and raise the batch timeout?",
    "Want me to flip the collector to OTLP/HTTP and raise the batch timeout?",
    "[URL] [URL] shows p99 regression but OTLP gRPC exporter queues are backing up.\n\nWhich OpenTelemetry exporter do you prefer — OTLP gRPC or OTLP HTTP/protobuf?",
    "Which OpenTelemetry exporter do you prefer — OTLP gRPC or OTLP HTTP/protobuf?",
    note_a="switch exporter settings -> yes_no/propose",
    note_b="exporter preference -> either_or",
    opts_b=["OTLP gRPC", "OTLP HTTP/protobuf"],
)

add(
    598,
    "Dashboard sprawl: 40 copies of the same Redis panel across team folders — on-call can't find the canonical board.\n\nShall I consolidate into a service-centric folder and archive duplicates?",
    "Shall I consolidate into a service-centric folder and archive duplicates?",
    "Dashboard sprawl: 40 copies of the same Redis panel across team folders — on-call can't find the canonical board.\n\nWhich dashboard ownership model do you prefer — team folders or service-centric boards?",
    "Which dashboard ownership model do you prefer — team folders or service-centric boards?",
    note_a="consolidate dashboards -> yes_no/propose",
    note_b="ownership model preference -> either_or",
    opts_b=["team folders", "service-centric boards"],
)

add(
    599,
    "Sentry events show `Script error.` on minified bundles — source maps weren't uploaded for `web-v3.2.1`.\n\nWant me to upload source maps for that release and backfill symbolicated stack traces?",
    "Want me to upload source maps for that release and backfill symbolicated stack traces?",
    "Sentry events show `Script error.` on minified bundles — source maps weren't uploaded for `web-v3.2.1`.\n\nWhich error-tracking release workflow do you prefer — CI source map upload or runtime deobfuscation in prod?",
    "Which error-tracking release workflow do you prefer — CI source map upload or runtime deobfuscation in prod?",
    note_a="upload source maps -> yes_no/propose",
    note_b="release workflow preference -> either_or",
    opts_b=["CI source map upload", "runtime deobfuscation in prod"],
)

# --- release ---
add(
    600,
    "Blue-green deploy scripts are ready — new pool passed smoke tests. Traffic is still 100% on blue.\n\nReady for me to proceed with the cutover plan — swap to green and watch error rates for fifteen minutes?",
    "Ready for me to proceed with the cutover plan — swap to green and watch error rates for fifteen minutes?",
    "Blue-green deploy scripts are ready — new pool passed smoke tests. Traffic is still 100% on blue.\n\nWhich cutover style do you prefer — instant swap or gradual weight shift?",
    "Which cutover style do you prefer — instant swap or gradual weight shift?",
    note_a="swap traffic to green -> yes_no/propose",
    note_b="cutover style preference -> either_or",
    opts_b=["instant swap", "gradual weight shift"],
)

assert [p["n"] for p in PAIRS] == list(range(526, 601))
