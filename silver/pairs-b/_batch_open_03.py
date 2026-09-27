"""Handcrafted open vs yes_no pairs pb0151–pb0250."""
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


# --- observability ---
add(
    151,
    "The p99 spike on `checkout-api` lines up with a deploy, but the trace IDs in Grafana don't match what I see in Tempo.\n\nWhich datasource UID is your dashboard using for traces?",
    "Which datasource UID is your dashboard using for traces?",
    "The p99 spike on `checkout-api` lines up with a deploy, but the trace IDs in Grafana don't match what I see in Tempo.\n\nWant me to repoint the dashboard at the staging Tempo datasource?",
    "Want me to repoint the dashboard at the staging Tempo datasource?",
    note_a="asks which datasource -> open",
    note_b="offers repoint dashboard -> yes_no/propose",
    pb=True,
)

add(
    152,
    "Log volume jumped 4× after the structured logging rollout. I can't tell if sampling changed.\n\nCould you share the current `OTEL_TRACES_SAMPLER` value from the pod env?",
    "Could you share the current `OTEL_TRACES_SAMPLER` value from the pod env?",
    "Log volume jumped 4× after the structured logging rollout. I can't tell if sampling changed.\n\nCould you restart one pod so the new env vars take effect?",
    "Could you restart one pod so the new env vars take effect?",
    note_a="asks for env value -> open",
    note_b="asks to restart pod -> yes_no",
)

add(
    153,
    "Alert `HighErrorRate` fired twice overnight then cleared on its own.\n\nDo you remember the exact UTC window when it was red?",
    "Do you remember the exact UTC window when it was red?",
    "Alert `HighErrorRate` fired twice overnight then cleared on its own.\n\nShall I silence that alert until Monday's deploy?",
    "Shall I silence that alert until Monday's deploy?",
    note_a="asks for recalled time window -> open",
    note_b="offers silence alert -> yes_no/propose",
    pb=True,
)

add(
    154,
    "The SLO burn chart shows green while customers report timeouts.\n\nWhat error budget threshold did you set for the 30-day window?",
    "What error budget threshold did you set for the 30-day window?",
    "The SLO burn chart shows green while customers report timeouts.\n\nCan you try opening the burn chart in an incognito session to see if you get more info?",
    "Can you try opening the burn chart in an incognito session to see if you get more info?",
    note_a="asks for threshold value -> open",
    note_b="asks to try incognito -> yes_no",
    da="m",
    db="m",
)

add(
    155,
    "Prometheus scrape targets for `worker-metrics` are flapping `DOWN`.\n\nWould you paste the last scrape error from the targets page?",
    "Would you paste the last scrape error from the targets page?",
    "Prometheus scrape targets for `worker-metrics` are flapping `DOWN`.\n\nWould you reload the Prometheus config without restarting?",
    "Would you reload the Prometheus config without restarting?",
    note_a="asks for pasted error -> open",
    note_b="asks to reload config -> yes_no",
)

add(
    156,
    "OpenTelemetry collector drops spans at the batch processor when queue fills.\n\nCould you describe what the collector logs show right before the drop?",
    "Could you describe what the collector logs show right before the drop?",
    "OpenTelemetry collector drops spans at the batch processor when queue fills.\n\nCould you bump `send_batch_max_size` and redeploy the collector?",
    "Could you bump `send_batch_max_size` and redeploy the collector?",
    note_a="asks for log description -> open",
    note_b="asks to bump/redeploy -> yes_no",
)

add(
    157,
    "Honeycomb query for `service.name=ingest` returns nothing after the namespace rename.\n\nWhich dataset should I query now?",
    "Which dataset should I query now?",
    "Honeycomb query for `service.name=ingest` returns nothing after the namespace rename.\n\nWant me to add a dataset alias for the old name?",
    "Want me to add a dataset alias for the old name?",
    note_a="asks which dataset -> open",
    note_b="offers alias -> yes_no/propose",
    pb=True,
)

add(
    158,
    "The runbook link in PagerDuty points to a deleted Notion page.\n\nWhat URL should on-call use instead?",
    "What URL should on-call use instead?",
    "The runbook link in PagerDuty points to a deleted Notion page.\n\nShall I update the PagerDuty service with a placeholder runbook?",
    "Shall I update the PagerDuty service with a placeholder runbook?",
    note_a="asks for replacement URL -> open",
    note_b="offers update service -> yes_no/propose",
    pb=True,
)

add(
    159,
    "Loki query `{app=\"api\"} |= \"timeout\"` returns zero lines for the incident window.\n\nCould you share the exact time range you searched?",
    "Could you share the exact time range you searched?",
    "Loki query `{app=\"api\"} |= \"timeout\"` returns zero lines for the incident window.\n\nCould you rerun the query with `{app=~\"api.*\"}`?",
    "Could you rerun the query with `{app=~\"api.*\"}`?",
    note_a="asks for time range -> open",
    note_b="asks to rerun query -> yes_no",
)

add(
    160,
    """Dashboard panel "Queue depth" flatlines at zero though RabbitMQ UI shows backlog.

Could you paste a screenshot of the RabbitMQ queue overview?""",
    "Could you paste a screenshot of the RabbitMQ queue overview?",
    """Dashboard panel "Queue depth" flatlines at zero though RabbitMQ UI shows backlog.

Can you try refreshing the Grafana panel with a 5-minute refresh interval?""",
    "Can you try refreshing the Grafana panel with a 5-minute refresh interval?",
    note_a="asks for screenshot -> open",
    note_b="asks to try refresh -> yes_no",
)

# --- ML training ---
add(
    161,
    "Training loss plateaued after epoch 40 on the vision run `run-7f2a`. I don't have your W&B project access.\n\nCould you share the learning-rate curve from that run?",
    "Could you share the learning-rate curve from that run?",
    "Training loss plateaued after epoch 40 on the vision run `run-7f2a`. I don't have your W&B project access.\n\nCould you resume training from epoch 38 with a lower LR?",
    "Could you resume training from epoch 38 with a lower LR?",
    note_a="asks for curve -> open",
    note_b="asks to resume training -> yes_no",
)

add(
    162,
    "GPU utilization sits at 12% while dataloader workers peg CPU.\n\nWhat batch size and `num_workers` are you using locally?",
    "What batch size and `num_workers` are you using locally?",
    "GPU utilization sits at 12% while dataloader workers peg CPU.\n\nWant me to bump `num_workers` to 8 in the config?",
    "Want me to bump `num_workers` to 8 in the config?",
    note_a="asks for hyperparams -> open",
    note_b="offers bump workers -> yes_no/propose",
    pb=True,
)

add(
    163,
    "Checkpoint `epoch_12.ckpt` fails to load on the inference box — shape mismatch on the head layer.\n\nWhich class count did you train with?",
    "Which class count did you train with?",
    "Checkpoint `epoch_12.ckpt` fails to load on the inference box — shape mismatch on the head layer.\n\nShall I strip the classification head and export embeddings only?",
    "Shall I strip the classification head and export embeddings only?",
    note_a="asks which class count -> open",
    note_b="offers strip head -> yes_no/propose",
    pb=True,
)

add(
    164,
    "Mixed-precision run NaN'd on step 903. The grad norm graph cuts off.\n\nCan you paste the last 20 lines of the training log around step 903?",
    "Can you paste the last 20 lines of the training log around step 903?",
    "Mixed-precision run NaN'd on step 903. The grad norm graph cuts off.\n\nCan you try rerunning with `--precision=32` to see if you get more info?",
    "Can you try rerunning with `--precision=32` to see if you get more info?",
    note_a="asks for log paste -> open",
    note_b="asks to try fp32 rerun -> yes_no",
    da="m",
    db="m",
)

add(
    165,
    "The eval set F1 dropped 6 points after label schema v3.\n\nWhich labels were merged or renamed in v3?",
    "Which labels were merged or renamed in v3?",
    "The eval set F1 dropped 6 points after label schema v3.\n\nWant me to roll eval back to schema v2 for comparison?",
    "Want me to roll eval back to schema v2 for comparison?",
    note_a="asks which label changes -> open",
    note_b="offers roll back eval -> yes_no/propose",
    pb=True,
)

add(
    166,
    "Distributed job hung at barrier on rank 3. NCCL logs aren't in the bundle I have.\n\nWould you share the NCCL debug output from rank 3?",
    "Would you share the NCCL debug output from rank 3?",
    "Distributed job hung at barrier on rank 3. NCCL logs aren't in the bundle I have.\n\nWould you kill the job and relaunch with `NCCL_DEBUG=INFO`?",
    "Would you kill the job and relaunch with `NCCL_DEBUG=INFO`?",
    note_a="asks for NCCL output -> open",
    note_b="asks to kill/relaunch -> yes_no",
)

add(
    167,
    "Feature store join returns null embeddings for 18% of users.\n\nWhat entity ID column does your offline table use?",
    "What entity ID column does your offline table use?",
    "Feature store join returns null embeddings for 18% of users.\n\nCan you run a backfill on the `user_embedding` feature group?",
    "Can you run a backfill on the `user_embedding` feature group?",
    note_a="asks which column -> open",
    note_b="asks to run backfill -> yes_no",
)

add(
    168,
    "Tokenizer vocab size in the saved config doesn't match the checkpoint weights.\n\nCould you clarify which tokenizer revision you fine-tuned on?",
    "Could you clarify which tokenizer revision you fine-tuned on?",
    "Tokenizer vocab size in the saved config doesn't match the checkpoint weights.\n\nCould you re-export the tokenizer from the base model and retry?",
    "Could you re-export the tokenizer from the base model and retry?",
    note_a="asks to clarify revision -> open",
    note_b="asks to re-export/retry -> yes_no",
)

add(
    169,
    """Hyperparameter sweep `sweep-019` finished but only 3 of 12 runs logged metrics.

Which three runs actually completed on your side?""",
    "Which three runs actually completed on your side?",
    """Hyperparameter sweep `sweep-019` finished but only 3 of 12 runs logged metrics.

Want me to mark the failed nine as cancelled in W&B?""",
    "Want me to mark the failed nine as cancelled in W&B?",
    note_a="asks which runs -> open",
    note_b="offers mark cancelled -> yes_no/propose",
    pb=True,
)

add(
    170,
    "ONNX export succeeded but ORT throws `INVALID_ARGUMENT` on the attention mask input.\n\nWhat input names does Netron show for that graph?",
    "What input names does Netron show for that graph?",
    "ONNX export succeeded but ORT throws `INVALID_ARGUMENT` on the attention mask input.\n\nCan you try running the same model through ORT with dynamic axes disabled?",
    "Can you try running the same model through ORT with dynamic axes disabled?",
    note_a="asks what Netron shows -> open",
    note_b="asks to try ORT run -> yes_no",
)

# --- mobile ---
add(
    171,
    "Push notifications arrive on Android but not iOS for the staging build.\n\nWhich APNs environment is the staging app pointed at?",
    "Which APNs environment is the staging app pointed at?",
    "Push notifications arrive on Android but not iOS for the staging build.\n\nWant me to flip the entitlements to production APNs for a test flight?",
    "Want me to flip the entitlements to production APNs for a test flight?",
    note_a="asks which APNs env -> open",
    note_b="offers flip entitlements -> yes_no/propose",
    pb=True,
)

add(
    172,
    "The bottom sheet jumps when the keyboard opens on Pixel 7.\n\nCould you describe how far the sheet shifts relative to the keyboard?",
    "Could you describe how far the sheet shifts relative to the keyboard?",
    "The bottom sheet jumps when the keyboard opens on Pixel 7.\n\nCould you reinstall the latest internal build and reproduce once?",
    "Could you reinstall the latest internal build and reproduce once?",
    note_a="asks for description -> open",
    note_b="asks to reinstall/reproduce -> yes_no",
)

add(
    173,
    "Crashlytics groups two distinct stacks under the same issue key.\n\nCan you share the full stack trace from the most recent iOS crash?",
    "Can you share the full stack trace from the most recent iOS crash?",
    "Crashlytics groups two distinct stacks under the same issue key.\n\nCan you force-quit the app and cold-launch it again?",
    "Can you force-quit the app and cold-launch it again?",
    note_a="asks for stack trace -> open",
    note_b="asks to force-quit/launch -> yes_no",
)

add(
    174,
    "Deep link `myapp://invite/abc` opens the store page instead of the invite screen.\n\nWhat URL does the marketing email actually use?",
    "What URL does the marketing email actually use?",
    "Deep link `myapp://invite/abc` opens the store page instead of the invite screen.\n\nShall I add a universal-link fallback in `apple-app-site-association`?",
    "Shall I add a universal-link fallback in `apple-app-site-association`?",
    note_a="asks what URL -> open",
    note_b="offers add fallback -> yes_no/propose",
    pb=True,
)

add(
    175,
    "Battery drain report shows location updates every 30s in background.\n\nWhich screen were you on when the drain spiked?",
    "Which screen were you on when the drain spiked?",
    "Battery drain report shows location updates every 30s in background.\n\nWant me to gate background location behind a new permission prompt?",
    "Want me to gate background location behind a new permission prompt?",
    note_a="asks which screen -> open",
    note_b="offers permission gate -> yes_no/propose",
    pb=True,
)

add(
    176,
    "React Native Hermes crash only on release builds.\n\nWould you paste the `metro` bundle map entry for `src/screens/Feed.tsx`?",
    "Would you paste the `metro` bundle map entry for `src/screens/Feed.tsx`?",
    "React Native Hermes crash only on release builds.\n\nWould you try a release build with Hermes disabled?",
    "Would you try a release build with Hermes disabled?",
    note_a="asks for bundle map paste -> open",
    note_b="asks to try Hermes off -> yes_no",
)

add(
    177,
    "Offline sync replayed the same mutation twice after reconnect.\n\nDo you remember whether airplane mode was toggled mid-request?",
    "Do you remember whether airplane mode was toggled mid-request?",
    "Offline sync replayed the same mutation twice after reconnect.\n\nCan you toggle airplane mode once and retry the checkout flow?",
    "Can you toggle airplane mode once and retry the checkout flow?",
    note_a="asks for recalled fact -> open",
    note_b="asks to toggle/retry -> yes_no",
)

add(
    178,
    """TestFlight build 412 shows a blank WebView on the help tab.

What does Safari Web Inspector report for the embedded page?""",
    "What does Safari Web Inspector report for the embedded page?",
    """TestFlight build 412 shows a blank WebView on the help tab.

Can you try loading the help URL in mobile Safari directly?""",
    "Can you try loading the help URL in mobile Safari directly?",
    note_a="asks what inspector reports -> open",
    note_b="asks to try Safari -> yes_no",
    da="m",
    db="m",
)

# --- security ---
add(
    179,
    "Semgrep flagged `eval()` in `scripts/migrate.js` but the path looks generated.\n\nCould you share who last edited that file and when?",
    "Could you share who last edited that file and when?",
    "Semgrep flagged `eval()` in `scripts/migrate.js` but the path looks generated.\n\nCould you revert that commit until we review it?",
    "Could you revert that commit until we review it?",
    note_a="asks for author/when -> open",
    note_b="asks to revert -> yes_no",
)

add(
    180,
    "OAuth callback returns `invalid_state` for one tenant only.\n\nWhich IdP issuer URL is that tenant configured with?",
    "Which IdP issuer URL is that tenant configured with?",
    "OAuth callback returns `invalid_state` for one tenant only.\n\nWant me to rotate the OAuth state signing key for that tenant?",
    "Want me to rotate the OAuth state signing key for that tenant?",
    note_a="asks which issuer -> open",
    note_b="offers rotate key -> yes_no/propose",
    pb=True,
)

add(
    181,
    "Vault lease renewal fails with `403` on the CI runner.\n\nWhat role name is the pipeline using in `VAULT_ROLE`?",
    "What role name is the pipeline using in `VAULT_ROLE`?",
    "Vault lease renewal fails with `403` on the CI runner.\n\nCan you re-authenticate the runner against Vault and retry the job?",
    "Can you re-authenticate the runner against Vault and retry the job?",
    note_a="asks for role name -> open",
    note_b="asks to re-auth/retry -> yes_no",
)

add(
    182,
    "CSP report-only shows repeated violations for an inline script on `/admin`.\n\nCould you paste one full CSP report payload?",
    "Could you paste one full CSP report payload?",
    "CSP report-only shows repeated violations for an inline script on `/admin`.\n\nCould you switch `/admin` to enforcing CSP for an hour?",
    "Could you switch `/admin` to enforcing CSP for an hour?",
    note_a="asks for report payload -> open",
    note_b="asks to switch to enforcing -> yes_no",
    da="h",
    db="e",
)

add(
    183,
    "Pen test noted missing `Strict-Transport-Security` on the CDN edge.\n\nWhat max-age did security ask for on static assets?",
    "What max-age did security ask for on static assets?",
    "Pen test noted missing `Strict-Transport-Security` on the CDN edge.\n\nShall I add HSTS at the CDN with a 1-year max-age?",
    "Shall I add HSTS at the CDN with a 1-year max-age?",
    note_a="asks for max-age requirement -> open",
    note_b="offers add HSTS -> yes_no/propose",
    pb=True,
)

add(
    184,
    "JWT `aud` claim mismatch between the mobile client and the BFF.\n\nWhich audience string is the mobile SDK sending today?",
    "Which audience string is the mobile SDK sending today?",
    "JWT `aud` claim mismatch between the mobile client and the BFF.\n\nCan you try logging out and back in to see if you get more info?",
    "Can you try logging out and back in to see if you get more info?",
    note_a="asks which audience -> open",
    note_b="asks to try logout/login -> yes_no",
    da="m",
    db="m",
)

add(
    185,
    "Dependabot security PR bumps `openssl` but breaks the FIPS build.\n\nWhich compliance mode does prod require?",
    "Which compliance mode does prod require?",
    "Dependabot security PR bumps `openssl` but breaks the FIPS build.\n\nWant me to pin OpenSSL to the last FIPS-validated version?",
    "Want me to pin OpenSSL to the last FIPS-validated version?",
    note_a="asks which compliance mode -> open",
    note_b="offers pin version -> yes_no/propose",
    pb=True,
)

add(
    186,
    """SAST scan blocked merge on `src/upload.ts`:

[CODE]
Potential path traversal in user-supplied filename
[CODE]

Could you clarify whether user filenames are ever used on disk?""",
    "Could you clarify whether user filenames are ever used on disk?",
    """SAST scan blocked merge on `src/upload.ts`:

[CODE]
Potential path traversal in user-supplied filename
[CODE]

Can you try uploading a file with `../` in the name to see if you get more info?""",
    "Can you try uploading a file with `../` in the name to see if you get more info?",
    note_a="asks to clarify behavior -> open",
    note_b="asks to try upload test -> yes_no",
)

# --- payments ---
add(
    187,
    "Stripe webhook `payment_intent.succeeded` hits our endpoint twice for the same intent.\n\nCould you share the two event IDs from the dashboard?",
    "Could you share the two event IDs from the dashboard?",
    "Stripe webhook `payment_intent.succeeded` hits our endpoint twice for the same intent.\n\nCould you disable webhook retries on the test endpoint?",
    "Could you disable webhook retries on the test endpoint?",
    note_a="asks for event IDs -> open",
    note_b="asks to disable retries -> yes_no",
)

add(
    188,
    "PayPal capture succeeds but our ledger shows `PENDING` for six hours.\n\nWhich merchant account ID should the webhook map to?",
    "Which merchant account ID should the webhook map to?",
    "PayPal capture succeeds but our ledger shows `PENDING` for six hours.\n\nWant me to replay the stuck webhooks from yesterday?",
    "Want me to replay the stuck webhooks from yesterday?",
    note_a="asks which merchant ID -> open",
    note_b="offers replay webhooks -> yes_no/propose",
    pb=True,
)

add(
    189,
    "3-D Secure challenge loops on Visa but not Mastercard in sandbox.\n\nWhat test card number are you using for Visa?",
    "What test card number are you using for Visa?",
    "3-D Secure challenge loops on Visa but not Mastercard in sandbox.\n\nCan you try the Visa flow in an incognito window?",
    "Can you try the Visa flow in an incognito window?",
    note_a="asks for test card -> open",
    note_b="asks to try incognito -> yes_no",
)

add(
    190,
    "Refund API returns `amount_too_large` though the capture was partial.\n\nWould you paste the capture and refund amounts from the admin UI?",
    "Would you paste the capture and refund amounts from the admin UI?",
    "Refund API returns `amount_too_large` though the capture was partial.\n\nWould you retry the refund after voiding the pending partial?",
    "Would you retry the refund after voiding the pending partial?",
    note_a="asks for pasted amounts -> open",
    note_b="asks to void/retry -> yes_no",
)

add(
    191,
    "Subscription proration math differs by a cent between invoice preview and charge.\n\nWhich timezone should billing periods anchor on?",
    "Which timezone should billing periods anchor on?",
    "Subscription proration math differs by a cent between invoice preview and charge.\n\nShall I add a rounding adjustment line item?",
    "Shall I add a rounding adjustment line item?",
    note_a="asks which timezone -> open",
    note_b="offers adjustment line -> yes_no/propose",
    pb=True,
)

add(
    192,
    "Apple IAP receipt validation fails with status `21002`.\n\nCan you share the base64 receipt blob you're posting?",
    "Can you share the base64 receipt blob you're posting?",
    "Apple IAP receipt validation fails with status `21002`.\n\nCan you restore purchases on the device and retry validation?",
    "Can you restore purchases on the device and retry validation?",
    note_a="asks for receipt blob -> open",
    note_b="asks to restore/retry -> yes_no",
)

add(
    193,
    "ACH micro-deposit verification never marks the bank account verified.\n\nWhat amounts did the customer report seeing?",
    "What amounts did the customer report seeing?",
    "ACH micro-deposit verification never marks the bank account verified.\n\nWant me to trigger a fresh micro-deposit pair?",
    "Want me to trigger a fresh micro-deposit pair?",
    note_a="asks what amounts -> open",
    note_b="offers trigger deposits -> yes_no/propose",
    pb=True,
)

add(
    194,
    """Checkout totals mismatch between cart and confirmation email:

| Line | Cart | Email |
|------|------|-------|
| Tax  | $4.20 | $4.19 |

Which total is the source of truth for finance?""",
    "Which total is the source of truth for finance?",
    """Checkout totals mismatch between cart and confirmation email:

| Line | Cart | Email |
|------|------|-------|
| Tax  | $4.20 | $4.19 |

Want me to regenerate the confirmation template from cart totals?""",
    "Want me to regenerate the confirmation template from cart totals?",
    note_a="asks which total -> open",
    note_b="offers regenerate template -> yes_no/propose",
    pb=True,
)

# --- DNS ---
add(
    195,
    "`api.example.test` resolves to the old load balancer from your office network.\n\nWhat A record does `dig api.example.test` return on your laptop?",
    "What A record does `dig api.example.test` return on your laptop?",
    "`api.example.test` resolves to the old load balancer from your office network.\n\nCan you flush your local DNS cache and query again?",
    "Can you flush your local DNS cache and query again?",
    note_a="asks what dig returns -> open",
    note_b="asks to flush/requery -> yes_no",
)

add(
    196,
    "ACM certificate validation stuck on `_acme-challenge.www`.\n\nWhich DNS provider hosts the `www` CNAME today?",
    "Which DNS provider hosts the `www` CNAME today?",
    "ACM certificate validation stuck on `_acme-challenge.www`.\n\nShall I recreate the validation CNAME in Route53?",
    "Shall I recreate the validation CNAME in Route53?",
    note_a="asks which provider -> open",
    note_b="offers recreate CNAME -> yes_no/propose",
    pb=True,
)

add(
    197,
    "Split-horizon DNS serves different answers inside the VPC.\n\nCould you share the answer you get from a pod in `staging`?",
    "Could you share the answer you get from a pod in `staging`?",
    "Split-horizon DNS serves different answers inside the VPC.\n\nCould you restart CoreDNS in the staging cluster?",
    "Could you restart CoreDNS in the staging cluster?",
    note_a="asks for answer from pod -> open",
    note_b="asks to restart CoreDNS -> yes_no",
)

add(
    198,
    "Email DKIM fails alignment because the signing domain changed.\n\nWhat selector name is Postmark using now?",
    "What selector name is Postmark using now?",
    "Email DKIM fails alignment because the signing domain changed.\n\nWant me to publish a new TXT record for selector `pm2024`?",
    "Want me to publish a new TXT record for selector `pm2024`?",
    note_a="asks what selector -> open",
    note_b="offers publish TXT -> yes_no/propose",
    pb=True,
)

add(
    199,
    "GeoDNS routes EU users to the US PoP during the failover drill.\n\nWhich health check failed first in your dashboard?",
    "Which health check failed first in your dashboard?",
    "GeoDNS routes EU users to the US PoP during the failover drill.\n\nCan you try failing over the EU PoP manually to see if you get more info?",
    "Can you try failing over the EU PoP manually to see if you get more info?",
    note_a="asks which check failed -> open",
    note_b="asks to try manual failover -> yes_no",
)

add(
    200,
    "Internal zone `svc.cluster.local` intermittently NXDOMAIN from one node pool.\n\nWould you paste `nslookup redis.svc.cluster.local` from an affected node?",
    "Would you paste `nslookup redis.svc.cluster.local` from an affected node?",
    "Internal zone `svc.cluster.local` intermittently NXDOMAIN from one node pool.\n\nWould you cordon the affected nodes and drain workloads?",
    "Would you cordon the affected nodes and drain workloads?",
    note_a="asks for nslookup paste -> open",
    note_b="asks to cordon/drain -> yes_no",
)

# --- email ---
add(
    201,
    "Postmark bounce webhook fires but the suppression list stays empty.\n\nCould you share the raw bounce payload from the webhook log?",
    "Could you share the raw bounce payload from the webhook log?",
    "Postmark bounce webhook fires but the suppression list stays empty.\n\nCould you resend the bounce test message through Postmark?",
    "Could you resend the bounce test message through Postmark?",
    note_a="asks for raw payload -> open",
    note_b="asks to resend test -> yes_no",
)

add(
    202,
    "Gmail clips the newsletter below the fold; Litmus shows full height.\n\nHow many KB is the HTML before send?",
    "How many KB is the HTML before send?",
    "Gmail clips the newsletter below the fold; Litmus shows full height.\n\nWant me to split the hero into a linked landing page?",
    "Want me to split the hero into a linked landing page?",
    note_a="asks for HTML size -> open",
    note_b="offers split hero -> yes_no/propose",
    pb=True,
)

add(
    203,
    "Double opt-in link expires in 15 minutes but legal wants 48 hours.\n\nWhat expiry did legal approve in the spec?",
    "What expiry did legal approve in the spec?",
    "Double opt-in link expires in 15 minutes but legal wants 48 hours.\n\nShall I bump the token TTL to 48 hours in config?",
    "Shall I bump the token TTL to 48 hours in config?",
    note_a="asks what expiry legal approved -> open",
    note_b="offers bump TTL -> yes_no/propose",
    pb=True,
)

add(
    204,
    "Transactional template `order-shipped` renders `{tracking_url}` literally.\n\nCan you paste the template JSON from SendGrid?",
    "Can you paste the template JSON from SendGrid?",
    "Transactional template `order-shipped` renders `{tracking_url}` literally.\n\nCan you try sending a test with a hard-coded tracking URL?",
    "Can you try sending a test with a hard-coded tracking URL?",
    note_a="asks for template JSON -> open",
    note_b="asks to try test send -> yes_no",
)

add(
    205,
    "DMARC aggregate reports show SPF fail on the marketing subdomain.\n\nWhich envelope-from domain are campaigns using?",
    "Which envelope-from domain are campaigns using?",
    "DMARC aggregate reports show SPF fail on the marketing subdomain.\n\nWant me to add an SPF include for the ESP?",
    "Want me to add an SPF include for the ESP?",
    note_a="asks which envelope-from -> open",
    note_b="offers SPF include -> yes_no/propose",
    pb=True,
)

add(
    206,
    """Inbox placement test: Outlook shows broken images, Gmail fine.

What image host URL appears in the broken `<img src>`?""",
    "What image host URL appears in the broken `<img src>`?",
    """Inbox placement test: Outlook shows broken images, Gmail fine.

Can you try opening the same message in Outlook on the web?""",
    "Can you try opening the same message in Outlook on the web?",
    note_a="asks what image URL -> open",
    note_b="asks to try Outlook web -> yes_no",
)

# --- accessibility ---
add(
    207,
    "Axe reports `color-contrast` failures on the pricing table in dark mode only.\n\nWhich tier label fails contrast in your audit?",
    "Which tier label fails contrast in your audit?",
    "Axe reports `color-contrast` failures on the pricing table in dark mode only.\n\nWant me to bump the muted text token to `#B8B8B8`?",
    "Want me to bump the muted text token to `#B8B8B8`?",
    note_a="asks which label -> open",
    note_b="offers token bump -> yes_no/propose",
    pb=True,
)

add(
    208,
    "Screen reader skips the modal title on VoiceOver.\n\nCould you describe what VoiceOver announces when the dialog opens?",
    "Could you describe what VoiceOver announces when the dialog opens?",
    "Screen reader skips the modal title on VoiceOver.\n\nCould you toggle VoiceOver off and on, then reopen the modal?",
    "Could you toggle VoiceOver off and on, then reopen the modal?",
    note_a="asks for announcement description -> open",
    note_b="asks to toggle/reopen -> yes_no",
)

add(
    209,
    "Focus trap leaks to the browser chrome on Firefox.\n\nWhat Firefox version are you testing with?",
    "What Firefox version are you testing with?",
    "Focus trap leaks to the browser chrome on Firefox.\n\nCan you try the same flow in Firefox ESR?",
    "Can you try the same flow in Firefox ESR?",
    note_a="asks for version -> open",
    note_b="asks to try ESR -> yes_no",
)

add(
    210,
    "Live region politeness is set to `assertive` and interrupts every cart update.\n\nWhich updates should be polite vs assertive?",
    "Which updates should be polite vs assertive?",
    "Live region politeness is set to `assertive` and interrupts every cart update.\n\nShall I downgrade cart count changes to `polite`?",
    "Shall I downgrade cart count changes to `polite`?",
    note_a="asks which updates -> open",
    note_b="offers downgrade -> yes_no/propose",
    pb=True,
)

add(
    211,
    "Keyboard users can't reach the toast dismiss button.\n\nWould you share a short screen recording of Tab order through checkout?",
    "Would you share a short screen recording of Tab order through checkout?",
    "Keyboard users can't reach the toast dismiss button.\n\nWould you try tabbing from the cart button with `prefers-reduced-motion` enabled?",
    "Would you try tabbing from the cart button with `prefers-reduced-motion` enabled?",
    note_a="asks for recording -> open",
    note_b="asks to try tabbing -> yes_no",
)

add(
    212,
    "PDF export tags are missing alt text on chart images.\n\nWhat alt strings should the three charts use?",
    "What alt strings should the three charts use?",
    "PDF export tags are missing alt text on chart images.\n\nWant me to add placeholder alt text from the chart titles?",
    "Want me to add placeholder alt text from the chart titles?",
    note_a="asks for alt strings -> open",
    note_b="offers placeholder alt -> yes_no/propose",
    pb=True,
)

# --- i18n ---
add(
    213,
    "German plural rules render `1 Artikel` as `1 Artikeln` in the cart badge.\n\nCould you paste the `.po` entry for `cart.item_count`?",
    "Could you paste the `.po` entry for `cart.item_count`?",
    "German plural rules render `1 Artikel` as `1 Artikeln` in the cart badge.\n\nCould you rebuild the locale bundle and reload the page?",
    "Could you rebuild the locale bundle and reload the page?",
    note_a="asks for po entry -> open",
    note_b="asks to rebuild/reload -> yes_no",
)

add(
    214,
    "RTL layout mirrors icons but not the progress bar fill direction.\n\nWhich locale were you viewing when the bar looked wrong?",
    "Which locale were you viewing when the bar looked wrong?",
    "RTL layout mirrors icons but not the progress bar fill direction.\n\nWant me to flip the progress bar gradient for `ar` and `he`?",
    "Want me to flip the progress bar gradient for `ar` and `he`?",
    note_a="asks which locale -> open",
    note_b="offers flip gradient -> yes_no/propose",
    pb=True,
)

add(
    215,
    "Date picker shows `MM/DD/YYYY` for French users.\n\nWhat date format does the FR locale file specify?",
    "What date format does the FR locale file specify?",
    "Date picker shows `MM/DD/YYYY` for French users.\n\nCan you switch your profile locale to `fr-FR` and reopen settings?",
    "Can you switch your profile locale to `fr-FR` and reopen settings?",
    note_a="asks what format -> open",
    note_b="asks to switch locale -> yes_no",
)

add(
    216,
    "Crowdin export dropped 12 keys that still exist in `en.json`.\n\nWhich keys are missing from the latest export?",
    "Which keys are missing from the latest export?",
    "Crowdin export dropped 12 keys that still exist in `en.json`.\n\nShall I trigger a fresh Crowdin sync from `main`?",
    "Shall I trigger a fresh Crowdin sync from `main`?",
    note_a="asks which keys -> open",
    note_b="offers trigger sync -> yes_no/propose",
    pb=True,
)

add(
    217,
    "Currency formatting shows `US$` instead of `$` for en-CA.\n\nWhat currency code is the checkout API returning for Canada?",
    "What currency code is the checkout API returning for Canada?",
    "Currency formatting shows `US$` instead of `$` for en-CA.\n\nCan you try checking out with a Canadian test address?",
    "Can you try checking out with a Canadian test address?",
    note_a="asks what currency code -> open",
    note_b="asks to try checkout -> yes_no",
)

add(
    218,
    """Pseudo-localization stretched the nav and clipped "Settings".

Could you share a screenshot with pseudo-locale enabled?""",
    "Could you share a screenshot with pseudo-locale enabled?",
    """Pseudo-localization stretched the nav and clipped "Settings".

Can you try widening the nav min-width locally to see if you get more info?""",
    "Can you try widening the nav min-width locally to see if you get more info?",
    note_a="asks for screenshot -> open",
    note_b="asks to try widen locally -> yes_no",
    da="m",
    db="m",
)

# --- monorepo ---
add(
    219,
    "`pnpm --filter @pkg/ui build` still compiles `@pkg/icons` twice.\n\nWhat does `pnpm why @pkg/icons` print in the ui package?",
    "What does `pnpm why @pkg/icons` print in the ui package?",
    "`pnpm --filter @pkg/ui build` still compiles `@pkg/icons` twice.\n\nWant me to add `@pkg/icons` as an explicit dependency in ui?",
    "Want me to add `@pkg/icons` as an explicit dependency in ui?",
    note_a="asks what pnpm why prints -> open",
    note_b="offers add dependency -> yes_no/propose",
    pb=True,
)

add(
    220,
    "Changeset preview lists four packages but only two actually changed.\n\nWhich two packages did you intend to version?",
    "Which two packages did you intend to version?",
    "Changeset preview lists four packages but only two actually changed.\n\nShall I trim the changeset to `@app/web` and `@app/api` only?",
    "Shall I trim the changeset to `@app/web` and `@app/api` only?",
    note_a="asks which packages -> open",
    note_b="offers trim changeset -> yes_no/propose",
    pb=True,
)

add(
    221,
    "Nx affected graph includes `@lib/auth` though you only touched docs.\n\nCould you share the `nx print-affected` output from your machine?",
    "Could you share the `nx print-affected` output from your machine?",
    "Nx affected graph includes `@lib/auth` though you only touched docs.\n\nCould you clear the Nx cache and rerun affected?",
    "Could you clear the Nx cache and rerun affected?",
    note_a="asks for print-affected output -> open",
    note_b="asks to clear/rerun -> yes_no",
)

add(
    222,
    "Workspace protocol `workspace:*` resolves to an old `@pkg/utils` locally.\n\nWhich commit hash does your `packages/utils/package.json` version field show?",
    "Which commit hash does your `packages/utils/package.json` version field show?",
    "Workspace protocol `workspace:*` resolves to an old `@pkg/utils` locally.\n\nCan you run `pnpm install --force` at the repo root?",
    "Can you run `pnpm install --force` at the repo root?",
    note_a="asks which hash -> open",
    note_b="asks to force install -> yes_no",
)

add(
    223,
    "Lerna publish skipped `@pkg/telemetry` because of a private flag mismatch.\n\nWhat does the `private` field say in that package.json?",
    "What does the `private` field say in that package.json?",
    "Lerna publish skipped `@pkg/telemetry` because of a private flag mismatch.\n\nWant me to flip `private` to false for a canary publish?",
    "Want me to flip `private` to false for a canary publish?",
    note_a="asks what private says -> open",
    note_b="offers flip private -> yes_no/propose",
    pb=True,
)

add(
    224,
    """Turbo remote cache hit rate dropped to 12% after the VPN change.

What remote cache URL is your laptop using now?""",
    "What remote cache URL is your laptop using now?",
    """Turbo remote cache hit rate dropped to 12% after the VPN change.

Can you try disconnecting VPN and running `turbo run build` once?""",
    "Can you try disconnecting VPN and running `turbo run build` once?",
    note_a="asks what cache URL -> open",
    note_b="asks to try without VPN -> yes_no",
)

# --- wasm ---
add(
    225,
    "Wasm module loads but `instantiateStreaming` fails with wrong MIME type.\n\nWhat `Content-Type` header does your dev server send for `.wasm`?",
    "What `Content-Type` header does your dev server send for `.wasm`?",
    "Wasm module loads but `instantiateStreaming` fails with wrong MIME type.\n\nWant me to add `application/wasm` to the static file middleware?",
    "Want me to add `application/wasm` to the static file middleware?",
    note_a="asks what Content-Type -> open",
    note_b="offers add MIME -> yes_no/propose",
    pb=True,
)

add(
    226,
    "Emscripten build links but exported `_malloc` is missing at runtime.\n\nCould you paste the `EXPORTED_FUNCTIONS` line from your link flags?",
    "Could you paste the `EXPORTED_FUNCTIONS` line from your link flags?",
    "Emscripten build links but exported `_malloc` is missing at runtime.\n\nCould you rebuild with `-s EXPORTED_RUNTIME_METHODS=cwrap`?",
    "Could you rebuild with `-s EXPORTED_RUNTIME_METHODS=cwrap`?",
    note_a="asks for link flags paste -> open",
    note_b="asks to rebuild with flag -> yes_no",
)

add(
    227,
    "Rust `wasm-pack` output is 2.1MB gzipped — over the budget.\n\nWhich features are enabled in your `Cargo.toml` for the wasm target?",
    "Which features are enabled in your `Cargo.toml` for the wasm target?",
    "Rust `wasm-pack` output is 2.1MB gzipped — over the budget.\n\nShall I disable default features and rebuild?",
    "Shall I disable default features and rebuild?",
    note_a="asks which features -> open",
    note_b="offers disable/rebuild -> yes_no/propose",
    pb=True,
)

add(
    228,
    "SharedArrayBuffer is unavailable in the embedded iframe.\n\nWhat COOP/COEP headers does the parent page send?",
    "What COOP/COEP headers does the parent page send?",
    "SharedArrayBuffer is unavailable in the embedded iframe.\n\nCan you try loading the wasm page top-level instead of in an iframe?",
    "Can you try loading the wasm page top-level instead of in an iframe?",
    note_a="asks what headers -> open",
    note_b="asks to try top-level -> yes_no",
)

add(
    229,
    "WASI preview build can't read `/tmp` in the browser shim.\n\nCould you describe which filesystem calls fail first in the console?",
    "Could you describe which filesystem calls fail first in the console?",
    "WASI preview build can't read `/tmp` in the browser shim.\n\nCould you remount the shim with preopened `/tmp`?",
    "Could you remount the shim with preopened `/tmp`?",
    note_a="asks for call description -> open",
    note_b="asks to remount shim -> yes_no",
)

add(
    230,
    """Go wasm export panics on string return:

[CODE]
runtime.errorString: invalid memory address
[CODE]

Could you share the `js.Value` wrapper you're using on the JS side?""",
    "Could you share the `js.Value` wrapper you're using on the JS side?",
    """Go wasm export panics on string return:

[CODE]
runtime.errorString: invalid memory address
[CODE]

Can you try calling the export with a shorter test string?""",
    "Can you try calling the export with a shorter test string?",
    note_a="asks for JS wrapper -> open",
    note_b="asks to try shorter string -> yes_no",
)

# --- gamedev ---
add(
    231,
    "Frame time spikes to 40ms when the particle pool exceeds 2k instances.\n\nWhat GPU and driver version are you on?",
    "What GPU and driver version are you on?",
    "Frame time spikes to 40ms when the particle pool exceeds 2k instances.\n\nWant me to cap the pool at 1500 until we profile?",
    "Want me to cap the pool at 1500 until we profile?",
    note_a="asks for GPU/driver -> open",
    note_b="offers cap pool -> yes_no/propose",
    pb=True,
)

add(
    232,
    "Netcode desync shows divergent RNG seeds after the third respawn.\n\nCan you paste the host and client seed logs from that match?",
    "Can you paste the host and client seed logs from that match?",
    "Netcode desync shows divergent RNG seeds after the third respawn.\n\nCan you host a private lobby and reproduce with logging enabled?",
    "Can you host a private lobby and reproduce with logging enabled?",
    note_a="asks for seed logs -> open",
    note_b="asks to host/reproduce -> yes_no",
)

add(
    233,
    "Save file from build 0.9.4 won't load in 0.9.5 — schema version mismatch.\n\nWhich save slot were you loading?",
    "Which save slot were you loading?",
    "Save file from build 0.9.4 won't load in 0.9.5 — schema version mismatch.\n\nShall I add a one-time migration for slot 2 saves?",
    "Shall I add a one-time migration for slot 2 saves?",
    note_a="asks which slot -> open",
    note_b="offers migration -> yes_no/propose",
    pb=True,
)

add(
    234,
    "Audio crackle only when Bluetooth headphones connect mid-combat.\n\nCould you describe whether crackle happens on menu music too?",
    "Could you describe whether crackle happens on menu music too?",
    "Audio crackle only when Bluetooth headphones connect mid-combat.\n\nCould you disconnect and reconnect the headphones during a menu screen?",
    "Could you disconnect and reconnect the headphones during a menu screen?",
    note_a="asks for audio description -> open",
    note_b="asks to disconnect/reconnect -> yes_no",
)

add(
    235,
    "Steam overlay breaks input when using the in-game map.\n\nWhat resolution and fullscreen mode are you running?",
    "What resolution and fullscreen mode are you running?",
    "Steam overlay breaks input when using the in-game map.\n\nCan you try borderless windowed and open the map again?",
    "Can you try borderless windowed and open the map again?",
    note_a="asks for resolution/mode -> open",
    note_b="asks to try borderless -> yes_no",
)

add(
    236,
    """Physics tunneling reported on the fast dash move.

Could you share a replay file from a run where it happened?""",
    "Could you share a replay file from a run where it happened?",
    """Physics tunneling reported on the fast dash move.

Can you try reproducing with vsync forced off?""",
    "Can you try reproducing with vsync forced off?",
    note_a="asks for replay file -> open",
    note_b="asks to try vsync off -> yes_no",
)

# --- mixed / longer / edge patterns ---
add(
    237,
    "The incident ticket references run `[URL]` but I get a 404.\n\nCould you double-check the id or provide more details?",
    "Could you double-check the id or provide more details?",
    "The incident ticket references run `[URL]` but I get a 404.\n\nCould you double-check the id and open it again?",
    "Could you double-check the id and open it again?",
    note_a="double-check or provide details -> open",
    note_b="double-check and open again -> yes_no",
    da="m",
    db="e",
)

add(
    238,
    "Native addon build for `linux-arm64` needs a cross toolchain I don't have here.\n\nCould you build it on `linux-arm64` and share the resulting `.node` artifact?",
    "Could you build it on `linux-arm64` and share the resulting `.node` artifact?",
    "Native addon build for `linux-arm64` needs a cross toolchain I don't have here.\n\nCould you try building with `--target=linux-arm64` locally to see if you get more info?",
    "Could you try building with `--target=linux-arm64` locally to see if you get more info?",
    note_a="build and share artifact -> open",
    note_b="try building locally -> yes_no",
    da="m",
    db="m",
)

add(
    239,
    """Morning triage on the observability board:

- Traces: sampling change merged
- Logs: index lag cleared
- Metrics: one stale target

Which dashboard panel still looks wrong to you?""",
    "Which dashboard panel still looks wrong to you?",
    """Morning triage on the observability board:

- Traces: sampling change merged
- Logs: index lag cleared
- Metrics: one stale target

Want me to pin the stale-target alert to the top of the board?""",
    "Want me to pin the stale-target alert to the top of the board?",
    note_a="asks which panel -> open",
    note_b="offers pin alert -> yes_no/propose",
    pb=True,
)

add(
    240,
    "Feature store backfill job `fs-441` shows success but row counts differ by 3%.\n\nWhat row count does your warehouse query return for `user_features`?",
    "What row count does your warehouse query return for `user_features`?",
    "Feature store backfill job `fs-441` shows success but row counts differ by 3%.\n\nCan you rerun the validation query with yesterday's snapshot?",
    "Can you rerun the validation query with yesterday's snapshot?",
    note_a="asks for row count -> open",
    note_b="asks to rerun query -> yes_no",
)

add(
    241,
    "Mobile crash report mentions `JNI DETECTED ERROR` only on Samsung One UI 6.\n\nDo you remember the device model from the beta channel?",
    "Do you remember the device model from the beta channel?",
    "Mobile crash report mentions `JNI DETECTED ERROR` only on Samsung One UI 6.\n\nWant me to disable the native blur path on Samsung builds?",
    "Want me to disable the native blur path on Samsung builds?",
    note_a="asks for recalled model -> open",
    note_b="offers disable blur -> yes_no/propose",
    pb=True,
)

add(
    242,
    "Security scan flagged a leaked test API key in `fixtures/payments.json`.\n\nWhich fixture key should replace it in docs examples?",
    "Which fixture key should replace it in docs examples?",
    "Security scan flagged a leaked test API key in `fixtures/payments.json`.\n\nShall I rotate the staging key and update the fixture?",
    "Shall I rotate the staging key and update the fixture?",
    note_a="asks which fixture key -> open",
    note_b="offers rotate/update -> yes_no/propose",
    pb=True,
)

add(
    243,
    "Webhook replay from `[URL]` returns `409` for half the events.\n\nWould you paste one failing event body and its `Idempotency-Key` header?",
    "Would you paste one failing event body and its `Idempotency-Key` header?",
    "Webhook replay from `[URL]` returns `409` for half the events.\n\nWould you pause the replay job until we dedupe the queue?",
    "Would you pause the replay job until we dedupe the queue?",
    note_a="asks for pasted event -> open",
    note_b="asks to pause job -> yes_no",
)

add(
    244,
    "DNS failover page still serves the old status message during the drill.\n\nWhat status copy should visitors see during partial outage?",
    "What status copy should visitors see during partial outage?",
    "DNS failover page still serves the old status message during the drill.\n\nWant me to publish the new status banner to the failover bucket?",
    "Want me to publish the new status banner to the failover bucket?",
    note_a="asks what copy -> open",
    note_b="offers publish banner -> yes_no/propose",
    pb=True,
)

add(
    245,
    "Screen reader testing on the checkout flow skipped the discount field entirely.\n\nCould you clarify whether the discount is applied before or after tax in your market?",
    "Could you clarify whether the discount is applied before or after tax in your market?",
    "Screen reader testing on the checkout flow skipped the discount field entirely.\n\nCould you walk through checkout again with NVDA and note where focus lands?",
    "Could you walk through checkout again with NVDA and note where focus lands?",
    note_a="asks to clarify tax order -> open",
    note_b="asks to walk through again -> yes_no",
    da="m",
    db="e",
)

add(
    246,
    "Locale fallback shows English error strings inside the Japanese bundle.\n\nWhich error keys still lack `ja` translations?",
    "Which error keys still lack `ja` translations?",
    "Locale fallback shows English error strings inside the Japanese bundle.\n\nShall I copy missing keys from `en` with a `TODO` marker?",
    "Shall I copy missing keys from `en` with a `TODO` marker?",
    note_a="asks which keys -> open",
    note_b="offers copy with TODO -> yes_no/propose",
    pb=True,
)

add(
    247,
    "Monorepo CI runs `build` on every package though only `@app/docs` changed.\n\nWhat path filters does your fork use in GitHub Actions?",
    "What path filters does your fork use in GitHub Actions?",
    "Monorepo CI runs `build` on every package though only `@app/docs` changed.\n\nCan you try pushing an empty commit to see if you get more info?",
    "Can you try pushing an empty commit to see if you get more info?",
    note_a="asks what path filters -> open",
    note_b="asks to try empty commit -> yes_no",
    da="m",
    db="m",
)

add(
    248,
    "Wasm worker thread pool deadlocks when importing two modules from the same bundle.\n\nWhat order do the two `import()` calls happen in your app?",
    "What order do the two `import()` calls happen in your app?",
    "Wasm worker thread pool deadlocks when importing two modules from the same bundle.\n\nWant me to serialize module init behind a single promise queue?",
    "Want me to serialize module init behind a single promise queue?",
    note_a="asks what order -> open",
    note_b="offers serialize init -> yes_no/propose",
    pb=True,
)

add(
    249,
    "Boss fight phase transition soft-locks if a player dies during the cutscene.\n\nWhich difficulty were you on when it stuck?",
    "Which difficulty were you on when it stuck?",
    "Boss fight phase transition soft-locks if a player dies during the cutscene.\n\nCan you try skipping the cutscene with the debug flag enabled?",
    "Can you try skipping the cutscene with the debug flag enabled?",
    note_a="asks which difficulty -> open",
    note_b="asks to try skip flag -> yes_no",
)

add(
    250,
    """Cross-team handoff for the payments v2 rollout:

1. Ledger dual-write verified in staging
2. Webhook signatures aligned
3. Mobile SDK still on v1 endpoints

Would you like to share details on which mobile builds still hit v1?""",
    "Would you like to share details on which mobile builds still hit v1?",
    """Cross-team handoff for the payments v2 rollout:

1. Ledger dual-write verified in staging
2. Webhook signatures aligned
3. Mobile SDK still on v1 endpoints

Want me to block v1 traffic at the gateway once you confirm?""",
    "Want me to block v1 traffic at the gateway once you confirm?",
    note_a="share details on builds -> open",
    note_b="offers block v1 traffic -> yes_no/propose",
    pb=True,
)

assert len(PAIRS) == 100
assert [p["n"] for p in PAIRS] == list(range(151, 251))
