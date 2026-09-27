"""Minimal pairs pa0301–pa0450: yes_no vs either_or boundary.

a = either_or (two deliverables); b = yes_no (one change, attribute alternatives).
Some pairs omit propose (`Q e ::` / `Q y ::`) for preference-without-commitment.
"""

PAIRS = [
    {
        "n": 301,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Drafted a transactional receipt template with liquid placeholders for `order_id` and `total`.

[CODE]
Subject: Your order {{ order_id }}
Hi {{ name }}, …
[CODE]

Want me to draft the welcome email or write a deliverability checklist?""",
        "text_b": """Drafted a transactional receipt template with liquid placeholders for `order_id` and `total`.

[CODE]
Subject: Your order {{ order_id }}
Hi {{ name }}, …
[CODE]

Want me to use a different subject line or CTA wording?""",
        "ann_a": ['Q e p :: Want me to draft the welcome email or write a deliverability checklist?', 'O draft the welcome email', 'O write a deliverability checklist'],
        "ann_b": ['Q y p :: Want me to use a different subject line or CTA wording?'],
    },
    {
        "n": 302,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """The password-reset mail currently ships plain text only. I can add a multipart MIME body.

Shall I add the HTML multipart version or document the ESP setup steps?""",
        "text_b": """The password-reset mail currently ships plain text only. I can add a multipart MIME body.

Shall I use a different preheader or button color?""",
        "ann_a": ['Q e p :: Shall I add the HTML multipart version or document the ESP setup steps?', 'O add the HTML multipart version', 'O document the ESP setup steps'],
        "ann_b": ['Q y p :: Shall I use a different preheader or button color?'],
    },
    {
        "n": 303,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Unsubscribe footer is missing the required physical address line per CAN-SPAM.

Want a patched footer snippet or a full compliance walkthrough?""",
        "text_b": """Unsubscribe footer is missing the required physical address line per CAN-SPAM.

Want a different address format or link label?""",
        "ann_a": ['Q e p :: Want a patched footer snippet or a full compliance walkthrough?', 'O a patched footer snippet', 'O a full compliance walkthrough'],
        "ann_b": ['Q y p :: Want a different address format or link label?'],
    },
    {
        "n": 304,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """I sketched three A/B variants for the abandoned-cart nudge. Preview:

[URL]

Want me to wire the ESP experiment or export the HTML packages?""",
        "text_b": """I sketched three A/B variants for the abandoned-cart nudge. Preview:

[URL]

Want me to try a different discount amount or urgency tone?""",
        "ann_a": ['Q e p :: Want me to wire the ESP experiment or export the HTML packages?', 'O wire the ESP experiment', 'O export the HTML packages'],
        "ann_b": ['Q y p :: Want me to try a different discount amount or urgency tone?'],
    },
    {
        "n": 305,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two deliverables, not propose',
        "note_b": 'preference about attributes of one name, not propose',
        "text_a": """For the onboarding drip, I'm stuck between approaches.

Which do you prefer — a single long welcome email or a three-step drip?""",
        "text_b": """For the onboarding drip, I'm stuck between naming styles.

Do you prefer a shorter or warmer subject line?""",
        "ann_a": ['Q e :: Which do you prefer — a single long welcome email or a three-step drip?', 'O a single long welcome email', 'O a three-step drip'],
        "ann_b": ['Q y :: Do you prefer a shorter or warmer subject line?'],
    },
    {
        "n": 306,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Extracted 42 hard-coded strings from `CheckoutForm.tsx` into `en.json`.

Want me to add the German locale file or generate the ICU plural rules doc?""",
        "text_b": """Extracted 42 hard-coded strings from `CheckoutForm.tsx` into `en.json`.

Want me to use a different key naming scheme or nesting depth?""",
        "ann_a": ['Q e p :: Want me to add the German locale file or generate the ICU plural rules doc?', 'O add the German locale file', 'O generate the ICU plural rules doc'],
        "ann_b": ['Q y p :: Want me to use a different key naming scheme or nesting depth?'],
    },
    {
        "n": 307,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """RTL layout breaks the date picker in `he` locale — mirrored padding is wrong on the popup.

Shall I fix the RTL CSS or write a screenshot comparison checklist?""",
        "text_b": """RTL layout breaks the date picker in `he` locale — mirrored padding is wrong on the popup.

Shall I use a different padding token or mirror strategy?""",
        "ann_a": ['Q e p :: Shall I fix the RTL CSS or write a screenshot comparison checklist?', 'O fix the RTL CSS', 'O write a screenshot comparison checklist'],
        "ann_b": ['Q y p :: Shall I use a different padding token or mirror strategy?'],
    },
    {
        "n": 308,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`react-intl` FormattedMessage ids collide with the marketing site's namespace.

Want a namespace prefix migration or a conflict report spreadsheet?""",
        "text_b": """`react-intl` FormattedMessage ids collide with the marketing site's namespace.

Want a different prefix separator or case style?""",
        "ann_a": ['Q e p :: Want a namespace prefix migration or a conflict report spreadsheet?', 'O a namespace prefix migration', 'O a conflict report spreadsheet'],
        "ann_b": ['Q y p :: Want a different prefix separator or case style?'],
    },
    {
        "n": 309,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Pseudo-loc (`en-XA`) is ready in CI. Sample:

[CODE]
Ördéŕ #12345 — Çôñfîřɱéď
[CODE]

Want me to enable it on preview deploys or document how translators pull strings?""",
        "text_b": """Pseudo-loc (`en-XA`) is ready in CI. Sample:

[CODE]
Ördéŕ #12345 — Çôñfîřɱéď
[CODE]

Want me to use a different expansion factor or accent set?""",
        "ann_a": ['Q e p :: Want me to enable it on preview deploys or document how translators pull strings?', 'O enable it on preview deploys', 'O document how translators pull strings'],
        "ann_b": ['Q y p :: Want me to use a different expansion factor or accent set?'],
    },
    {
        "n": 310,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Date formatting still uses `toLocaleString` instead of the shared `formatDate` helper.

Want me to migrate the remaining call sites or add a lint rule that bans the raw API?""",
        "text_b": """Date formatting still uses `toLocaleString` instead of the shared `formatDate` helper.

Want me to switch to a different default locale or timezone source?""",
        "ann_a": ['Q e p :: Want me to migrate the remaining call sites or add a lint rule that bans the raw API?', 'O migrate the remaining call sites', 'O add a lint rule that bans the raw API'],
        "ann_b": ['Q y p :: Want me to switch to a different default locale or timezone source?'],
    },
    {
        "n": 311,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """axe flagged 6 contrast failures on the settings page (AA).

Want me to patch the failing color tokens or produce a WCAG audit table?""",
        "text_b": """axe flagged 6 contrast failures on the settings page (AA).

Want me to try a different contrast ratio or text weight?""",
        "ann_a": ['Q e p :: Want me to patch the failing color tokens or produce a WCAG audit table?', 'O patch the failing color tokens', 'O produce a WCAG audit table'],
        "ann_b": ['Q y p :: Want me to try a different contrast ratio or text weight?'],
    },
    {
        "n": 312,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two a11y approaches, not propose',
        "note_b": 'preference about attributes of one label, not propose',
        "text_a": """For the skip-link target, both patterns are valid.

Which approach do you prefer — a landmark-based skip or a first-heading skip?""",
        "text_b": """For the skip-link label, both phrasings work.

Do you prefer a shorter or more descriptive link text?""",
        "ann_a": ['Q e :: Which approach do you prefer — a landmark-based skip or a first-heading skip?', 'O a landmark-based skip', 'O a first-heading skip'],
        "ann_b": ['Q y :: Do you prefer a shorter or more descriptive link text?'],
    },
    {
        "n": 313,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Modal traps focus but Escape doesn't close it when a nested popover is open.

Shall I fix the focus trap nesting or write a keyboard test plan?""",
        "text_b": """Modal traps focus but Escape doesn't close it when a nested popover is open.

Shall I use a different Escape precedence or focus restore target?""",
        "ann_a": ['Q e p :: Shall I fix the focus trap nesting or write a keyboard test plan?', 'O fix the focus trap nesting', 'O write a keyboard test plan'],
        "ann_b": ['Q y p :: Shall I use a different Escape precedence or focus restore target?'],
    },
    {
        "n": 314,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Icon-only toolbar buttons lack accessible names.

Want aria-label attributes added now or a Storybook a11y checklist?""",
        "text_b": """Icon-only toolbar buttons lack accessible names.

Want a different aria-label wording or naming pattern?""",
        "ann_a": ['Q e p :: Want aria-label attributes added now or a Storybook a11y checklist?', 'O aria-label attributes added now', 'O a Storybook a11y checklist'],
        "ann_b": ['Q y p :: Want a different aria-label wording or naming pattern?'],
    },
    {
        "n": 315,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Screen reader announces the live region twice on filter apply.

Want me to dedupe the polite announcements or record a VoiceOver script?""",
        "text_b": """Screen reader announces the live region twice on filter apply.

Want me to use a different politeness level or announcement timing?""",
        "ann_a": ['Q e p :: Want me to dedupe the polite announcements or record a VoiceOver script?', 'O dedupe the polite announcements', 'O record a VoiceOver script'],
        "ann_b": ['Q y p :: Want me to use a different politeness level or announcement timing?'],
    },
    {
        "n": 316,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Reconnect logic drops the subscription list after a 30s idle timeout.

Want me to implement backoff with resume or draft the protocol notes?""",
        "text_b": """Reconnect logic drops the subscription list after a 30s idle timeout.

Want me to use a different idle timeout or backoff curve?""",
        "ann_a": ['Q e p :: Want me to implement backoff with resume or draft the protocol notes?', 'O implement backoff with resume', 'O draft the protocol notes'],
        "ann_b": ['Q y p :: Want me to use a different idle timeout or backoff curve?'],
    },
    {
        "n": 317,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Binary frames for cursor positions still go through JSON.stringify — wasteful.

Shall I switch the cursor channel to protobuf frames or keep JSON and add compression?""",
        "text_b": """Binary frames for cursor positions still go through JSON.stringify — wasteful.

Shall I use a different frame type or compression level?""",
        "ann_a": ['Q e p :: Shall I switch the cursor channel to protobuf frames or keep JSON and add compression?', 'O switch the cursor channel to protobuf frames', 'O keep JSON and add compression'],
        "ann_b": ['Q y p :: Shall I use a different frame type or compression level?'],
    },
    {
        "n": 318,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Heartbeat pings are client-only; the load balancer still kills quiet connections.

Want a server-side ping interval or an LB idle-timeout runbook?""",
        "text_b": """Heartbeat pings are client-only; the load balancer still kills quiet connections.

Want a different ping interval or payload size?""",
        "ann_a": ['Q e p :: Want a server-side ping interval or an LB idle-timeout runbook?', 'O a server-side ping interval', 'O an LB idle-timeout runbook'],
        "ann_b": ['Q y p :: Want a different ping interval or payload size?'],
    },
    {
        "n": 319,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Auth token refresh mid-socket leaves a window where messages 401.

Want me to pause the queue during refresh or document the race?""",
        "text_b": """Auth token refresh mid-socket leaves a window where messages 401.

Want me to use a different refresh trigger or queue drain order?""",
        "ann_a": ['Q e p :: Want me to pause the queue during refresh or document the race?', 'O pause the queue during refresh', 'O document the race'],
        "ann_b": ['Q y p :: Want me to use a different refresh trigger or queue drain order?'],
    },
    {
        "n": 320,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two WS strategies, not propose',
        "note_b": 'preference about attributes of one reconnect policy, not propose',
        "text_a": """For fan-out under load, both topologies work.

Which do you prefer — sticky sessions or a Redis pub/sub bridge?""",
        "text_b": """For the reconnect banner copy, both tones work.

Do you prefer a quieter or more urgent reconnect message?""",
        "ann_a": ['Q e :: Which do you prefer — sticky sessions or a Redis pub/sub bridge?', 'O sticky sessions', 'O a Redis pub/sub bridge'],
        "ann_b": ['Q y :: Do you prefer a quieter or more urgent reconnect message?'],
    },
    {
        "n": 321,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`UserProfile` gained `optional string display_name = 7` — need codegen.

Want me to regenerate the stubs or write a wire-compat checklist?""",
        "text_b": """`UserProfile` gained `optional string display_name = 7` — need codegen.

Want me to use a different field number or presence rule?""",
        "ann_a": ['Q e p :: Want me to regenerate the stubs or write a wire-compat checklist?', 'O regenerate the stubs', 'O write a wire-compat checklist'],
        "ann_b": ['Q y p :: Want me to use a different field number or presence rule?'],
    },
    {
        "n": 322,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """gRPC reflection is off in prod; clients can't discover methods.

Shall I enable reflection on the staging server or publish the `.proto` package?""",
        "text_b": """gRPC reflection is off in prod; clients can't discover methods.

Shall I use a different reflection ACL or package path?""",
        "ann_a": ['Q e p :: Shall I enable reflection on the staging server or publish the `.proto` package?', 'O enable reflection on the staging server', 'O publish the `.proto` package'],
        "ann_b": ['Q y p :: Shall I use a different reflection ACL or package path?'],
    },
    {
        "n": 323,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Oneof `payload` vs separate optional fields — schema debate in PR #412.

Want a oneof refactor PR or a decision memo for the API review?""",
        "text_b": """Oneof `payload` vs separate optional fields — schema debate in PR #412.

Want a different oneof name or field numbering?""",
        "ann_a": ['Q e p :: Want a oneof refactor PR or a decision memo for the API review?', 'O a oneof refactor PR', 'O a decision memo for the API review'],
        "ann_b": ['Q y p :: Want a different oneof name or field numbering?'],
    },
    {
        "n": 324,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """buf breaking change: deleted `legacy_id`. CI is red.

Want me to restore a reserved tag or generate a migration guide?""",
        "text_b": """buf breaking change: deleted `legacy_id`. CI is red.

Want me to use a different reserved range or deprecation comment?""",
        "ann_a": ['Q e p :: Want me to restore a reserved tag or generate a migration guide?', 'O restore a reserved tag', 'O generate a migration guide'],
        "ann_b": ['Q y p :: Want me to use a different reserved range or deprecation comment?'],
    },
    {
        "n": 325,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`bazel build //services/api` fails on hermetic Python toolchain mismatch.

Want me to pin the toolchain or document the local override flags?""",
        "text_b": """`bazel build //services/api` fails on hermetic Python toolchain mismatch.

Want me to use a different Python version or toolchain repo?""",
        "ann_a": ['Q e p :: Want me to pin the toolchain or document the local override flags?', 'O pin the toolchain', 'O document the local override flags'],
        "ann_b": ['Q y p :: Want me to use a different Python version or toolchain repo?'],
    },
    {
        "n": 326,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Remote cache hit rate is ~12% after the WORKSPACE → MODULE.bazel move.

Shall I retune the remote cache keys or write a migration retrospective?""",
        "text_b": """Remote cache hit rate is ~12% after the WORKSPACE → MODULE.bazel move.

Shall I use a different cache key salt or remote endpoint?""",
        "ann_a": ['Q e p :: Shall I retune the remote cache keys or write a migration retrospective?', 'O retune the remote cache keys', 'O write a migration retrospective'],
        "ann_b": ['Q y p :: Shall I use a different cache key salt or remote endpoint?'],
    },
    {
        "n": 327,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`select()` for macOS vs Linux linkopts is duplicated across 9 targets.

Want a shared `.bzl` macro or a graphviz of the dependency edges?""",
        "text_b": """`select()` for macOS vs Linux linkopts is duplicated across 9 targets.

Want a different select key or default linkopt set?""",
        "ann_a": ['Q e p :: Want a shared `.bzl` macro or a graphviz of the dependency edges?', 'O a shared `.bzl` macro', 'O a graphviz of the dependency edges'],
        "ann_b": ['Q y p :: Want a different select key or default linkopt set?'],
    },
    {
        "n": 328,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Bazel layouts, not propose',
        "note_b": 'preference about attributes of one target name, not propose',
        "text_a": """Package boundaries aren't settled.

Which layout do you prefer — flat `//lib/...` or service-scoped `//services/*/lib`?""",
        "text_b": """Target naming isn't settled.

Do you prefer a shorter or more explicit target name?""",
        "ann_a": ['Q e :: Which layout do you prefer — flat `//lib/...` or service-scoped `//services/*/lib`?', 'O flat `//lib/...`', 'O service-scoped `//services/*/lib`'],
        "ann_b": ['Q y :: Do you prefer a shorter or more explicit target name?'],
    },
    {
        "n": 329,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`nix develop` pulls an old openssl; CI flake.lock is ahead.

Want me to bump the flake inputs or write a `nix flake update` runbook?""",
        "text_b": """`nix develop` pulls an old openssl; CI flake.lock is ahead.

Want me to pin a different nixpkgs rev or openssl overlay?""",
        "ann_a": ['Q e p :: Want me to bump the flake inputs or write a `nix flake update` runbook?', 'O bump the flake inputs', 'O write a `nix flake update` runbook'],
        "ann_b": ['Q y p :: Want me to pin a different nixpkgs rev or openssl overlay?'],
    },
    {
        "n": 330,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """direnv + nix-direnv works locally but agents without flakes fail.

Shall I add a classic `shell.nix` shim or document the flake-only path?""",
        "text_b": """direnv + nix-direnv works locally but agents without flakes fail.

Shall I use a different shellHook or direnv watch pattern?""",
        "ann_a": ['Q e p :: Shall I add a classic `shell.nix` shim or document the flake-only path?', 'O add a classic `shell.nix` shim', 'O document the flake-only path'],
        "ann_b": ['Q y p :: Shall I use a different shellHook or direnv watch pattern?'],
    },
    {
        "n": 331,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Binary cache auth expired; builds pull from source again.

Want me to rotate the cache token or publish a cold-build time report?""",
        "text_b": """Binary cache auth expired; builds pull from source again.

Want me to use a different cache URL or signing key?""",
        "ann_a": ['Q e p :: Want me to rotate the cache token or publish a cold-build time report?', 'O rotate the cache token', 'O publish a cold-build time report'],
        "ann_b": ['Q y p :: Want me to use a different cache URL or signing key?'],
    },
    {
        "n": 332,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Android 14: notification permission prompt fires too late on first launch.

Want me to move the prompt into onboarding or draft the Play policy notes?""",
        "text_b": """Android 14: notification permission prompt fires too late on first launch.

Want me to use a different prompt timing or copy tone?""",
        "ann_a": ['Q e p :: Want me to move the prompt into onboarding or draft the Play policy notes?', 'O move the prompt into onboarding', 'O draft the Play policy notes'],
        "ann_b": ['Q y p :: Want me to use a different prompt timing or copy tone?'],
    },
    {
        "n": 333,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """iOS deep link from universal link opens cold but loses query params.

Shall I fix the SceneDelegate routing or write a TestFlight repro script?""",
        "text_b": """iOS deep link from universal link opens cold but loses query params.

Shall I use a different URL scheme or query encoding?""",
        "ann_a": ['Q e p :: Shall I fix the SceneDelegate routing or write a TestFlight repro script?', 'O fix the SceneDelegate routing', 'O write a TestFlight repro script'],
        "ann_b": ['Q y p :: Shall I use a different URL scheme or query encoding?'],
    },
    {
        "n": 334,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kotlin Multiplatform shared module builds, but iOS XCFramework is stale.

Want a CI job that regenerates the XCFramework or a local `./scripts/kmp-ios.sh`?""",
        "text_b": """Kotlin Multiplatform shared module builds, but iOS XCFramework is stale.

Want a different framework name or deployment target?""",
        "ann_a": ['Q e p :: Want a CI job that regenerates the XCFramework or a local `./scripts/kmp-ios.sh`?', 'O a CI job that regenerates the XCFramework', 'O a local `./scripts/kmp-ios.sh`'],
        "ann_b": ['Q y p :: Want a different framework name or deployment target?'],
    },
    {
        "n": 335,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two mobile stacks, not propose',
        "note_b": 'preference about attributes of one screen title, not propose',
        "text_a": """For the new settings screen, both stacks are on the table.

Which do you prefer — Compose Multiplatform or separate SwiftUI/Compose UIs?""",
        "text_b": """For the settings screen title, both phrasings work.

Do you prefer a shorter or more formal title?""",
        "ann_a": ['Q e :: Which do you prefer — Compose Multiplatform or separate SwiftUI/Compose UIs?', 'O Compose Multiplatform', 'O separate SwiftUI/Compose UIs'],
        "ann_b": ['Q y :: Do you prefer a shorter or more formal title?'],
    },
    {
        "n": 336,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Play Console rejected the AAB: 16 KB page size warning on native libs.

Want me to rebuild with the NDK flag or prepare an appeal note?""",
        "text_b": """Play Console rejected the AAB: 16 KB page size warning on native libs.

Want me to use a different NDK version or linker flag?""",
        "ann_a": ['Q e p :: Want me to rebuild with the NDK flag or prepare an appeal note?', 'O rebuild with the NDK flag', 'O prepare an appeal note'],
        "ann_b": ['Q y p :: Want me to use a different NDK version or linker flag?'],
    },
    {
        "n": 337,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Notebook still embeds 40 MB of PNG outputs — repo bloat.

Want me to clear outputs and add nbstripout or write a data-pipeline notebook instead?""",
        "text_b": """Notebook still embeds 40 MB of PNG outputs — repo bloat.

Want me to use a different figure DPI or output format?""",
        "ann_a": ['Q e p :: Want me to clear outputs and add nbstripout or write a data-pipeline notebook instead?', 'O clear outputs and add nbstripout', 'O write a data-pipeline notebook instead'],
        "ann_b": ['Q y p :: Want me to use a different figure DPI or output format?'],
    },
    {
        "n": 338,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kernel dies on the Spark session cell — memory limit too low in Binder.

Shall I raise the Binder memory or convert the notebook to a script?""",
        "text_b": """Kernel dies on the Spark session cell — memory limit too low in Binder.

Shall I use a different memory limit or executor count?""",
        "ann_a": ['Q e p :: Shall I raise the Binder memory or convert the notebook to a script?', 'O raise the Binder memory', 'O convert the notebook to a script'],
        "ann_b": ['Q y p :: Shall I use a different memory limit or executor count?'],
    },
    {
        "n": 339,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Papermill parameters aren't declared in the first cell.

Want parameterized tags added or a papermill CLI example doc?""",
        "text_b": """Papermill parameters aren't declared in the first cell.

Want a different parameter name or default value?""",
        "ann_a": ['Q e p :: Want parameterized tags added or a papermill CLI example doc?', 'O parameterized tags added', 'O a papermill CLI example doc'],
        "ann_b": ['Q y p :: Want a different parameter name or default value?'],
    },
    {
        "n": 340,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Shuffle spill is huge on the join — skew on `user_id`.

Want me to add a salted skew join or produce an explain-plan dump?""",
        "text_b": """Shuffle spill is huge on the join — skew on `user_id`.

Want me to use a different salt cardinality or join hint?""",
        "ann_a": ['Q e p :: Want me to add a salted skew join or produce an explain-plan dump?', 'O add a salted skew join', 'O produce an explain-plan dump'],
        "ann_b": ['Q y p :: Want me to use a different salt cardinality or join hint?'],
    },
    {
        "n": 341,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Delta table OPTIMIZE hasn't run in 3 weeks; small files everywhere.

Shall I schedule OPTIMIZE+ZORDER or write the ops playbook?""",
        "text_b": """Delta table OPTIMIZE hasn't run in 3 weeks; small files everywhere.

Shall I use a different ZORDER column or optimize interval?""",
        "ann_a": ['Q e p :: Shall I schedule OPTIMIZE+ZORDER or write the ops playbook?', 'O schedule OPTIMIZE+ZORDER', 'O write the ops playbook'],
        "ann_b": ['Q y p :: Shall I use a different ZORDER column or optimize interval?'],
    },
    {
        "n": 342,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Spark APIs, not propose',
        "note_b": 'preference about attributes of one job name, not propose',
        "text_a": """For the daily aggregate, both APIs work.

Which do you prefer — DataFrame SQL or the Dataset typed API?""",
        "text_b": """For the Spark job display name, both styles work.

Do you prefer a shorter or more descriptive job name?""",
        "ann_a": ['Q e :: Which do you prefer — DataFrame SQL or the Dataset typed API?', 'O DataFrame SQL', 'O the Dataset typed API'],
        "ann_b": ['Q y :: Do you prefer a shorter or more descriptive job name?'],
    },
    {
        "n": 343,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`spark.sql.shuffle.partitions=200` is too high for this cluster size.

Want me to lower shuffle partitions or add an adaptive-query note?""",
        "text_b": """`spark.sql.shuffle.partitions=200` is too high for this cluster size.

Want me to use a different partition count or AQE setting?""",
        "ann_a": ['Q e p :: Want me to lower shuffle partitions or add an adaptive-query note?', 'O lower shuffle partitions', 'O add an adaptive-query note'],
        "ann_b": ['Q y p :: Want me to use a different partition count or AQE setting?'],
    },
    {
        "n": 344,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """DAG `ingest_events` still uses `schedule_interval`; Airflow 2 wants `schedule`.

Want me to migrate the DAG params or write the 1→2 upgrade checklist?""",
        "text_b": """DAG `ingest_events` still uses `schedule_interval`; Airflow 2 wants `schedule`.

Want me to use a different timetable or catchup policy?""",
        "ann_a": ['Q e p :: Want me to migrate the DAG params or write the 1→2 upgrade checklist?', 'O migrate the DAG params', 'O write the 1→2 upgrade checklist'],
        "ann_b": ['Q y p :: Want me to use a different timetable or catchup policy?'],
    },
    {
        "n": 345,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Task `load_dim` retries forever on a bad credential — no `on_failure_callback`.

Shall I add Slack alerting or document the retry policy?""",
        "text_b": """Task `load_dim` retries forever on a bad credential — no `on_failure_callback`.

Shall I use a different retry count or backoff delay?""",
        "ann_a": ['Q e p :: Shall I add Slack alerting or document the retry policy?', 'O add Slack alerting', 'O document the retry policy'],
        "ann_b": ['Q y p :: Shall I use a different retry count or backoff delay?'],
    },
    {
        "n": 346,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """XCom pulls a 12 MB JSON — metastore is unhappy.

Want me to switch that payload to S3 or draft an XCom best-practices note?""",
        "text_b": """XCom pulls a 12 MB JSON — metastore is unhappy.

Want me to use a different XCom backend or serialization format?""",
        "ann_a": ['Q e p :: Want me to switch that payload to S3 or draft an XCom best-practices note?', 'O switch that payload to S3', 'O draft an XCom best-practices note'],
        "ann_b": ['Q y p :: Want me to use a different XCom backend or serialization format?'],
    },
    {
        "n": 347,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Consumer lag on `orders.v2` jumped after the key change.

Want me to rebalance with a sticky assignor or produce a lag dashboard query?""",
        "text_b": """Consumer lag on `orders.v2` jumped after the key change.

Want me to use a different partition count or assignor strategy?""",
        "ann_a": ['Q e p :: Want me to rebalance with a sticky assignor or produce a lag dashboard query?', 'O rebalance with a sticky assignor', 'O produce a lag dashboard query'],
        "ann_b": ['Q y p :: Want me to use a different partition count or assignor strategy?'],
    },
    {
        "n": 348,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Schema Registry SUBJECT strategy is TopicName; new topics break avro readers.

Shall I migrate to RecordNameStrategy or write a compatibility matrix?""",
        "text_b": """Schema Registry SUBJECT strategy is TopicName; new topics break avro readers.

Shall I use a different subject strategy or compatibility level?""",
        "ann_a": ['Q e p :: Shall I migrate to RecordNameStrategy or write a compatibility matrix?', 'O migrate to RecordNameStrategy', 'O write a compatibility matrix'],
        "ann_b": ['Q y p :: Shall I use a different subject strategy or compatibility level?'],
    },
    {
        "n": 349,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Exactly-once producer is configured but transactions aren't fencing properly.

Want me to fix the transactional.id setup or document the EOS caveats?""",
        "text_b": """Exactly-once producer is configured but transactions aren't fencing properly.

Want me to use a different transactional.id prefix or timeout?""",
        "ann_a": ['Q e p :: Want me to fix the transactional.id setup or document the EOS caveats?', 'O fix the transactional.id setup', 'O document the EOS caveats'],
        "ann_b": ['Q y p :: Want me to use a different transactional.id prefix or timeout?'],
    },
    {
        "n": 350,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Kafka patterns, not propose',
        "note_b": 'preference about attributes of one topic name, not propose',
        "text_a": """For DLQ handling, both patterns are common.

Which do you prefer — a shared DLQ topic or per-consumer DLQs?""",
        "text_b": """For the DLQ topic name, both styles work.

Do you prefer a shorter or more namespaced topic name?""",
        "ann_a": ['Q e :: Which do you prefer — a shared DLQ topic or per-consumer DLQs?', 'O a shared DLQ topic', 'O per-consumer DLQs'],
        "ann_b": ['Q y :: Do you prefer a shorter or more namespaced topic name?'],
    },
    {
        "n": 351,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OIDC callback rejects `state` after the IdP round-trip — cookie SameSite is Strict.

Want me to fix the state cookie flags or write an Auth0 troubleshooting guide?""",
        "text_b": """OIDC callback rejects `state` after the IdP round-trip — cookie SameSite is Strict.

Want me to use a different SameSite mode or cookie path?""",
        "ann_a": ['Q e p :: Want me to fix the state cookie flags or write an Auth0 troubleshooting guide?', 'O fix the state cookie flags', 'O write an Auth0 troubleshooting guide'],
        "ann_b": ['Q y p :: Want me to use a different SameSite mode or cookie path?'],
    },
    {
        "n": 352,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """PKCE is missing on the public SPA client; security review flagged it.

Shall I enable PKCE on the SPA or draft the OAuth threat model notes?""",
        "text_b": """PKCE is missing on the public SPA client; security review flagged it.

Shall I use a different code_challenge method or redirect URI pattern?""",
        "ann_a": ['Q e p :: Shall I enable PKCE on the SPA or draft the OAuth threat model notes?', 'O enable PKCE on the SPA', 'O draft the OAuth threat model notes'],
        "ann_b": ['Q y p :: Shall I use a different code_challenge method or redirect URI pattern?'],
    },
    {
        "n": 353,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Refresh tokens rotate but the old one isn't revoked — replay window.

Want a revoke-on-rotate patch or a token lifecycle diagram?""",
        "text_b": """Refresh tokens rotate but the old one isn't revoked — replay window.

Want a different rotation interval or reuse detection window?""",
        "ann_a": ['Q e p :: Want a revoke-on-rotate patch or a token lifecycle diagram?', 'O a revoke-on-rotate patch', 'O a token lifecycle diagram'],
        "ann_b": ['Q y p :: Want a different rotation interval or reuse detection window?'],
    },
    {
        "n": 354,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Audience claim mismatch: API expects `api://orders`, tokens have `api://default`.

Want me to align the audience config or produce a JWT claim dump helper?""",
        "text_b": """Audience claim mismatch: API expects `api://orders`, tokens have `api://default`.

Want me to use a different audience string or issuer URL?""",
        "ann_a": ['Q e p :: Want me to align the audience config or produce a JWT claim dump helper?', 'O align the audience config', 'O produce a JWT claim dump helper'],
        "ann_b": ['Q y p :: Want me to use a different audience string or issuer URL?'],
    },
    {
        "n": 355,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two auth flows, not propose',
        "note_b": 'preference about attributes of one claim name, not propose',
        "text_a": """For first-party mobile, both flows are acceptable.

Which do you prefer — Authorization Code + PKCE or the device code flow?""",
        "text_b": """For the custom claim name, both styles work.

Do you prefer a shorter or more namespaced claim name?""",
        "ann_a": ['Q e :: Which do you prefer — Authorization Code + PKCE or the device code flow?', 'O Authorization Code + PKCE', 'O the device code flow'],
        "ann_b": ['Q y :: Do you prefer a shorter or more namespaced claim name?'],
    },
    {
        "n": 356,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Gateway returns 429 without `Retry-After`; clients hammer.

Want me to add Retry-After headers or write a client backoff recipe?""",
        "text_b": """Gateway returns 429 without `Retry-After`; clients hammer.

Want me to use a different Retry-After unit or jitter policy?""",
        "ann_a": ['Q e p :: Want me to add Retry-After headers or write a client backoff recipe?', 'O add Retry-After headers', 'O write a client backoff recipe'],
        "ann_b": ['Q y p :: Want me to use a different Retry-After unit or jitter policy?'],
    },
    {
        "n": 357,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Per-IP limit is too coarse for NAT'd enterprise users.

Shall I switch to per-API-key quotas or document the current buckets?""",
        "text_b": """Per-IP limit is too coarse for NAT'd enterprise users.

Shall I use a different quota window or burst size?""",
        "ann_a": ['Q e p :: Shall I switch to per-API-key quotas or document the current buckets?', 'O switch to per-API-key quotas', 'O document the current buckets'],
        "ann_b": ['Q y p :: Shall I use a different quota window or burst size?'],
    },
    {
        "n": 358,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two limiter backends, not propose',
        "note_b": 'preference about attributes of one error body, not propose',
        "text_a": """Rate-limit storage choice is still open.

Which do you prefer — Redis token buckets or in-process sliding windows?""",
        "text_b": """Rate-limit error payload shape is still open.

Do you prefer a shorter or more detailed 429 body?""",
        "ann_a": ['Q e :: Which do you prefer — Redis token buckets or in-process sliding windows?', 'O Redis token buckets', 'O in-process sliding windows'],
        "ann_b": ['Q y :: Do you prefer a shorter or more detailed 429 body?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 359,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """GraphQL resolvers share one global RPM — mutations starve under reads.

Want me to split read/write budgets or sketch a cost-analysis table?""",
        "text_b": """GraphQL resolvers share one global RPM — mutations starve under reads.

Want me to use a different RPM split or cost weight?""",
        "ann_a": ['Q e p :: Want me to split read/write budgets or sketch a cost-analysis table?', 'O split read/write budgets', 'O sketch a cost-analysis table'],
        "ann_b": ['Q y p :: Want me to use a different RPM split or cost weight?'],
    },
    {
        "n": 360,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """CDN still caches `/api/me` — `Cache-Control` is missing on that route.

Want me to set no-store on private routes or write a caching matrix?""",
        "text_b": """CDN still caches `/api/me` — `Cache-Control` is missing on that route.

Want me to use a different Cache-Control directive or max-age?""",
        "ann_a": ['Q e p :: Want me to set no-store on private routes or write a caching matrix?', 'O set no-store on private routes', 'O write a caching matrix'],
        "ann_b": ['Q y p :: Want me to use a different Cache-Control directive or max-age?'],
    },
    {
        "n": 361,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """ETag generation hashes the whole JSON body — expensive on large lists.

Shall I switch to a weak ETag from `updated_at` or document the current cost?""",
        "text_b": """ETag generation hashes the whole JSON body — expensive on large lists.

Shall I use a different ETag source or hash algorithm?""",
        "ann_a": ['Q e p :: Shall I switch to a weak ETag from `updated_at` or document the current cost?', 'O switch to a weak ETag from `updated_at`', 'O document the current cost'],
        "ann_b": ['Q y p :: Shall I use a different ETag source or hash algorithm?'],
    },
    {
        "n": 362,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`stale-while-revalidate` is set but the CDN vendor ignores it.

Want a vendor-specific surrogate-control patch or a fallback polling note?""",
        "text_b": """`stale-while-revalidate` is set but the CDN vendor ignores it.

Want a different SWR window or stale-if-error value?""",
        "ann_a": ['Q e p :: Want a vendor-specific surrogate-control patch or a fallback polling note?', 'O a vendor-specific surrogate-control patch', 'O a fallback polling note'],
        "ann_b": ['Q y p :: Want a different SWR window or stale-if-error value?'],
    },
    {
        "n": 363,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Icon sprite still inlines 80 SVGs — first paint is heavy.

Want me to switch to an external sprite sheet or produce a size breakdown?""",
        "text_b": """Icon sprite still inlines 80 SVGs — first paint is heavy.

Want me to use a different sprite packing or icon size?""",
        "ann_a": ['Q e p :: Want me to switch to an external sprite sheet or produce a size breakdown?', 'O switch to an external sprite sheet', 'O produce a size breakdown'],
        "ann_b": ['Q y p :: Want me to use a different sprite packing or icon size?'],
    },
    {
        "n": 364,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """CurrentColor isn't inherited in the nested `<use>` icons.

Shall I flatten the SVGs or write a theming guide for designers?""",
        "text_b": """CurrentColor isn't inherited in the nested `<use>` icons.

Shall I use a different fill strategy or stroke width?""",
        "ann_a": ['Q e p :: Shall I flatten the SVGs or write a theming guide for designers?', 'O flatten the SVGs', 'O write a theming guide for designers'],
        "ann_b": ['Q y p :: Shall I use a different fill strategy or stroke width?'],
    },
    {
        "n": 365,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two icon pipelines, not propose',
        "note_b": 'preference about attributes of one icon name, not propose',
        "text_a": """Icon delivery is undecided.

Which do you prefer — SVG sprites or individual React icon components?""",
        "text_b": """Icon naming is undecided.

Do you prefer a shorter or more descriptive icon name?""",
        "ann_a": ['Q e :: Which do you prefer — SVG sprites or individual React icon components?', 'O SVG sprites', 'O individual React icon components'],
        "ann_b": ['Q y :: Do you prefer a shorter or more descriptive icon name?'],
    },
    {
        "n": 366,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Button stories lack dark-mode and RTL variants.

Want me to add those stories or write a Storybook contribution guide?""",
        "text_b": """Button stories lack dark-mode and RTL variants.

Want me to use a different viewport preset or background color?""",
        "ann_a": ['Q e p :: Want me to add those stories or write a Storybook contribution guide?', 'O add those stories', 'O write a Storybook contribution guide'],
        "ann_b": ['Q y p :: Want me to use a different viewport preset or background color?'],
    },
    {
        "n": 367,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Chromatic baselines drifted after the token rename — 40 diffs.

Shall I accept the new baselines or produce a visual-diff triage list?""",
        "text_b": """Chromatic baselines drifted after the token rename — 40 diffs.

Shall I use a different diff threshold or capture delay?""",
        "ann_a": ['Q e p :: Shall I accept the new baselines or produce a visual-diff triage list?', 'O accept the new baselines', 'O produce a visual-diff triage list'],
        "ann_b": ['Q y p :: Shall I use a different diff threshold or capture delay?'],
    },
    {
        "n": 368,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """CSF3 args aren't typed; `as const` missing on the meta.

Want typed CSF meta now or a Storybook TS cookbook section?""",
        "text_b": """CSF3 args aren't typed; `as const` missing on the meta.

Want a different argType control or default arg?""",
        "ann_a": ['Q e p :: Want typed CSF meta now or a Storybook TS cookbook section?', 'O typed CSF meta now', 'O a Storybook TS cookbook section'],
        "ann_b": ['Q y p :: Want a different argType control or default arg?'],
    },
    {
        "n": 369,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OpenAPI `Pedido` schema still says `additionalProperties: true` — codegen is loose.

Want me to tighten the schema or regenerate the client with warnings?""",
        "text_b": """OpenAPI `Pedido` schema still says `additionalProperties: true` — codegen is loose.

Want me to use a different additionalProperties setting or required set?""",
        "ann_a": ['Q e p :: Want me to tighten the schema or regenerate the client with warnings?', 'O tighten the schema', 'O regenerate the client with warnings'],
        "ann_b": ['Q y p :: Want me to use a different additionalProperties setting or required set?'],
    },
    {
        "n": 370,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`/v2/orders` isn't in the published OpenAPI — SDK users can't see it.

Shall I add the path to the spec or publish a changelog of undocumented routes?""",
        "text_b": """`/v2/orders` isn't in the published OpenAPI — SDK users can't see it.

Shall I use a different operationId or tag grouping?""",
        "ann_a": ['Q e p :: Shall I add the path to the spec or publish a changelog of undocumented routes?', 'O add the path to the spec', 'O publish a changelog of undocumented routes'],
        "ann_b": ['Q y p :: Shall I use a different operationId or tag grouping?'],
    },
    {
        "n": 371,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Discriminated union for `PaymentMethod` is wrong in the OAS oneOf.

Want a corrected oneOf patch or an example payloads appendix?""",
        "text_b": """Discriminated union for `PaymentMethod` is wrong in the OAS oneOf.

Want a different discriminator property or mapping key?""",
        "ann_a": ['Q e p :: Want a corrected oneOf patch or an example payloads appendix?', 'O a corrected oneOf patch', 'O an example payloads appendix'],
        "ann_b": ['Q y p :: Want a different discriminator property or mapping key?'],
    },
    {
        "n": 372,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two OpenAPI tooling paths, not propose',
        "note_b": 'preference about attributes of one schema title, not propose',
        "text_a": """Spec authoring workflow isn't locked.

Which do you prefer — hand-written OAS or codegen from Go structs?""",
        "text_b": """Schema titles aren't locked.

Do you prefer a shorter or more qualified schema title?""",
        "ann_a": ['Q e :: Which do you prefer — hand-written OAS or codegen from Go structs?', 'O hand-written OAS', 'O codegen from Go structs'],
        "ann_b": ['Q y :: Do you prefer a shorter or more qualified schema title?'],
    },
    {
        "n": 373,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """v2.4.0 ships breaking rename of `fetchUser` → `getUser`.

Want me to draft the Keep-a-Changelog entry or write a migration snippet?""",
        "text_b": """v2.4.0 ships breaking rename of `fetchUser` → `getUser`.

Want me to use a different section heading or severity label?""",
        "ann_a": ['Q e p :: Want me to draft the Keep-a-Changelog entry or write a migration snippet?', 'O draft the Keep-a-Changelog entry', 'O write a migration snippet'],
        "ann_b": ['Q y p :: Want me to use a different section heading or severity label?'],
    },
    {
        "n": 374,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Conventional commits aren't parsing — CHANGELOG generation skipped 3 PRs.

Shall I fix the commit parser config or manually backfill those entries?""",
        "text_b": """Conventional commits aren't parsing — CHANGELOG generation skipped 3 PRs.

Shall I use a different commit type set or footer format?""",
        "ann_a": ['Q e p :: Shall I fix the commit parser config or manually backfill those entries?', 'O fix the commit parser config', 'O manually backfill those entries'],
        "ann_b": ['Q y p :: Shall I use a different commit type set or footer format?'],
    },
    {
        "n": 375,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Release notes buried the security fix under Features.

Want me to promote it to a Security section or add a CVE advisory link block?""",
        "text_b": """Release notes buried the security fix under Features.

Want me to use a different section order or callout style?""",
        "ann_a": ['Q e p :: Want me to promote it to a Security section or add a CVE advisory link block?', 'O promote it to a Security section', 'O add a CVE advisory link block'],
        "ann_b": ['Q y p :: Want me to use a different section order or callout style?'],
    },
    {
        "n": 376,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Vendored crate is GPL-3; our repo is Apache-2.0 — license scan failed.

Want me to replace the dependency or draft a license exception request?""",
        "text_b": """Vendored crate is GPL-3; our repo is Apache-2.0 — license scan failed.

Want me to use a different license scanner rule or allowlist entry?""",
        "ann_a": ['Q e p :: Want me to replace the dependency or draft a license exception request?', 'O replace the dependency', 'O draft a license exception request'],
        "ann_b": ['Q y p :: Want me to use a different license scanner rule or allowlist entry?'],
    },
    {
        "n": 377,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """LICENSE file still says MIT; package.json says Apache-2.0.

Shall I align LICENSE to Apache-2.0 or produce a NOTICE file for attributions?""",
        "text_b": """LICENSE file still says MIT; package.json says Apache-2.0.

Shall I use a different SPDX identifier or copyright year range?""",
        "ann_a": ['Q e p :: Shall I align LICENSE to Apache-2.0 or produce a NOTICE file for attributions?', 'O align LICENSE to Apache-2.0', 'O produce a NOTICE file for attributions'],
        "ann_b": ['Q y p :: Shall I use a different SPDX identifier or copyright year range?'],
    },
    {
        "n": 378,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Third-party fonts need OFL attribution in the about screen.

Want the about-screen attribution UI or a licenses.json export?""",
        "text_b": """Third-party fonts need OFL attribution in the about screen.

Want a different attribution layout or link style?""",
        "ann_a": ['Q e p :: Want the about-screen attribution UI or a licenses.json export?', 'O the about-screen attribution UI', 'O a licenses.json export'],
        "ann_b": ['Q y p :: Want a different attribution layout or link style?'],
    },
    {
        "n": 379,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two licenses, not propose',
        "note_b": 'preference about attributes of one copyright line, not propose',
        "text_a": """New shared library needs a license pick.

Which do you prefer — Apache-2.0 or MIT?""",
        "text_b": """Copyright line wording needs a pick.

Do you prefer a shorter or more formal copyright line?""",
        "ann_a": ['Q e :: Which do you prefer — Apache-2.0 or MIT?', 'O Apache-2.0', 'O MIT'],
        "ann_b": ['Q y :: Do you prefer a shorter or more formal copyright line?'],
    },
    {
        "n": 380,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables buried in soft wording -> either_or',
        "note_b": 'attribute alternatives sound like choices -> yes_no',
        "text_a": """Email template PR is green. Reviewer asked for one more pass before merge.

Would you like me to tighten the transactional templates, or would you rather I prepare the ESP handoff notes?""",
        "text_b": """Email template PR is green. Reviewer asked for one more pass before merge.

Would you like me to tighten the templates with a different voice or length?""",
        "ann_a": ['Q e p :: Would you like me to tighten the transactional templates, or would you rather I prepare the ESP handoff notes?', 'O tighten the transactional templates', 'O prepare the ESP handoff notes'],
        "ann_b": ['Q y p :: Would you like me to tighten the templates with a different voice or length?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 381,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """i18n coverage report:

| locale | missing |
| en | 0 |
| de | 18 |
| fr | 41 |

Want me to fill the German gaps or export a Crowdin CSV?""",
        "text_b": """i18n coverage report:

| locale | missing |
| en | 0 |
| de | 18 |
| fr | 41 |

Want me to use a different fallback locale or missing-key behavior?""",
        "ann_a": ['Q e p :: Want me to fill the German gaps or export a Crowdin CSV?', 'O fill the German gaps', 'O export a Crowdin CSV'],
        "ann_b": ['Q y p :: Want me to use a different fallback locale or missing-key behavior?'],
    },
    {
        "n": 382,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """axe + VoiceOver both complain about the tablist roles on settings.

Want a role fix PR or a recorded VO walkthrough link?""",
        "text_b": """axe + VoiceOver both complain about the tablist roles on settings.

Want a different role mapping or aria-orientation?""",
        "ann_a": ['Q e p :: Want a role fix PR or a recorded VO walkthrough link?', 'O a role fix PR', 'O a recorded VO walkthrough link'],
        "ann_b": ['Q y p :: Want a different role mapping or aria-orientation?'],
    },
    {
        "n": 383,
        "boundary": "yes_no/either_or",
        "note_a": "two deliverables with 'or would you like' -> either_or",
        "note_b": 'single adjustment with attribute or -> yes_no',
        "text_a": """WebSocket client recovers, but the UI still shows "Connecting…" for 8s after open.

Want me to fix the connection state machine, or would you like a sequence diagram of the handshake?""",
        "text_b": """WebSocket client recovers, but the UI still shows "Connecting…" for 8s after open.

Want me to tweak the connection banner with a different delay or copy?""",
        "ann_a": ['Q e p :: Want me to fix the connection state machine, or would you like a sequence diagram of the handshake?', 'O fix the connection state machine', 'O a sequence diagram of the handshake'],
        "ann_b": ['Q y p :: Want me to tweak the connection banner with a different delay or copy?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 384,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """buf lint found `PACKAGE_DIRECTORY_MATCH` on `orders/v1`.

Shall I rename the proto package or add a lint ignore with justification?""",
        "text_b": """buf lint found `PACKAGE_DIRECTORY_MATCH` on `orders/v1`.

Shall I use a different package path or file layout?""",
        "ann_a": ['Q e p :: Shall I rename the proto package or add a lint ignore with justification?', 'O rename the proto package', 'O add a lint ignore with justification'],
        "ann_b": ['Q y p :: Shall I use a different package path or file layout?'],
    },
    {
        "n": 385,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Bazel query for `somepath(//app, //lib:legacy)` is empty — unexpected.

Want me to chase the missing edge or dump a `bazel cquery` report?""",
        "text_b": """Bazel query for `somepath(//app, //lib:legacy)` is empty — unexpected.

Want me to use a different query expression or output format?""",
        "ann_a": ['Q e p :: Want me to chase the missing edge or dump a `bazel cquery` report?', 'O chase the missing edge', 'O dump a `bazel cquery` report'],
        "ann_b": ['Q y p :: Want me to use a different query expression or output format?'],
    },
    {
        "n": 386,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """NixOS module for the agent sets `services.foo.enable` but the package is impure.

Want me to hermeticize the package or write a module options reference?""",
        "text_b": """NixOS module for the agent sets `services.foo.enable` but the package is impure.

Want me to use a different store path or buildInputs set?""",
        "ann_a": ['Q e p :: Want me to hermeticize the package or write a module options reference?', 'O hermeticize the package', 'O write a module options reference'],
        "ann_b": ['Q y p :: Want me to use a different store path or buildInputs set?'],
    },
    {
        "n": 387,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Android Room migration 12→13 fails on devices that skipped 11.

Shall I add a fallback destructive migration path or document the upgrade ladder?""",
        "text_b": """Android Room migration 12→13 fails on devices that skipped 11.

Shall I use a different migration version or fallback strategy?""",
        "ann_a": ['Q e p :: Shall I add a fallback destructive migration path or document the upgrade ladder?', 'O add a fallback destructive migration path', 'O document the upgrade ladder'],
        "ann_b": ['Q y p :: Shall I use a different migration version or fallback strategy?'],
    },
    {
        "n": 388,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two notebook formats, not propose',
        "note_b": 'preference about attributes of one cell tag, not propose',
        "text_a": """Sharing format for the analysis notebook is open.

Which do you prefer — `.ipynb` with clear outputs or a rendered Quarto `.qmd`?""",
        "text_b": """Cell tagging convention is open.

Do you prefer a shorter or more hierarchical tag name?""",
        "ann_a": ['Q e :: Which do you prefer — `.ipynb` with clear outputs or a rendered Quarto `.qmd`?', 'O `.ipynb` with clear outputs', 'O a rendered Quarto `.qmd`'],
        "ann_b": ['Q y :: Do you prefer a shorter or more hierarchical tag name?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 389,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Spark UI shows stage 4 skew: one task 40× slower.

Want me to apply salting on that key or export the stage metrics CSV?""",
        "text_b": """Spark UI shows stage 4 skew: one task 40× slower.

Want me to use a different repartition count or skew hint?""",
        "ann_a": ['Q e p :: Want me to apply salting on that key or export the stage metrics CSV?', 'O apply salting on that key', 'O export the stage metrics CSV'],
        "ann_b": ['Q y p :: Want me to use a different repartition count or skew hint?'],
    },
    {
        "n": 390,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Airflow pool `heavy_etl` is saturated; new DAGs queue forever.

Want me to raise the pool slots or write a capacity-planning note?""",
        "text_b": """Airflow pool `heavy_etl` is saturated; new DAGs queue forever.

Want me to use a different pool size or priority weight?""",
        "ann_a": ['Q e p :: Want me to raise the pool slots or write a capacity-planning note?', 'O raise the pool slots', 'O write a capacity-planning note'],
        "ann_b": ['Q y p :: Want me to use a different pool size or priority weight?'],
    },
    {
        "n": 391,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kafka mirror-maker lag to DR is 12 minutes — SLA is 2.

Shall I tune MM2 throughput or draft an incident timeline?""",
        "text_b": """Kafka mirror-maker lag to DR is 12 minutes — SLA is 2.

Shall I use a different fetch size or commit interval?""",
        "ann_a": ['Q e p :: Shall I tune MM2 throughput or draft an incident timeline?', 'O tune MM2 throughput', 'O draft an incident timeline'],
        "ann_b": ['Q y p :: Shall I use a different fetch size or commit interval?'],
    },
    {
        "n": 392,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OIDC silent renew iframe is blocked by COOP on the new app shell.

Want me to adjust COOP/COEP or move renew to a top-level redirect?""",
        "text_b": """OIDC silent renew iframe is blocked by COOP on the new app shell.

Want me to use a different COOP value or renew interval?""",
        "ann_a": ['Q e p :: Want me to adjust COOP/COEP or move renew to a top-level redirect?', 'O adjust COOP/COEP', 'O move renew to a top-level redirect'],
        "ann_b": ['Q y p :: Want me to use a different COOP value or renew interval?'],
    },
    {
        "n": 393,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Rate limit headers use `X-RateLimit-*`; RFC 6585 prefers `RateLimit-*`.

Want me to dual-write both header sets or update the client SDK docs?""",
        "text_b": """Rate limit headers use `X-RateLimit-*`; RFC 6585 prefers `RateLimit-*`.

Want me to use a different header prefix or remaining-count field?""",
        "ann_a": ['Q e p :: Want me to dual-write both header sets or update the client SDK docs?', 'O dual-write both header sets', 'O update the client SDK docs'],
        "ann_b": ['Q y p :: Want me to use a different header prefix or remaining-count field?'],
    },
    {
        "n": 394,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`Cache-Control: public, max-age=3600` on HTML — users see stale nav after deploys.

Shall I switch HTML to `no-cache` with ETag or write a purge runbook?""",
        "text_b": """`Cache-Control: public, max-age=3600` on HTML — users see stale nav after deploys.

Shall I use a different max-age or must-revalidate combo?""",
        "ann_a": ['Q e p :: Shall I switch HTML to `no-cache` with ETag or write a purge runbook?', 'O switch HTML to `no-cache` with ETag', 'O write a purge runbook'],
        "ann_b": ['Q y p :: Shall I use a different max-age or must-revalidate combo?'],
    },
    {
        "n": 395,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two SVG approaches, not propose',
        "note_b": 'preference about attributes of one viewBox, not propose',
        "text_a": """Icon system direction is still fuzzy.

Which do you prefer — inline SVGs with CSS vars or a masked icon font?""",
        "text_b": """viewBox conventions are still fuzzy.

Do you prefer a tighter or more padded viewBox?""",
        "ann_a": ['Q e :: Which do you prefer — inline SVGs with CSS vars or a masked icon font?', 'O inline SVGs with CSS vars', 'O a masked icon font'],
        "ann_b": ['Q y :: Do you prefer a tighter or more padded viewBox?'],
    },
    {
        "n": 396,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Storybook 8 migration: `storiesOf` still in 11 files.

Want me to convert them to CSF3 or list the blockers per file?""",
        "text_b": """Storybook 8 migration: `storiesOf` still in 11 files.

Want me to use a different story title or hierarchy separator?""",
        "ann_a": ['Q e p :: Want me to convert them to CSF3 or list the blockers per file?', 'O convert them to CSF3', 'O list the blockers per file'],
        "ann_b": ['Q y p :: Want me to use a different story title or hierarchy separator?'],
    },
    {
        "n": 397,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OpenAPI example for `422` uses the wrong error envelope.

Want a corrected example block or a Spectral rule that catches it?""",
        "text_b": """OpenAPI example for `422` uses the wrong error envelope.

Want a different error code or message field name?""",
        "ann_a": ['Q e p :: Want a corrected example block or a Spectral rule that catches it?', 'O a corrected example block', 'O a Spectral rule that catches it'],
        "ann_b": ['Q y p :: Want a different error code or message field name?'],
    },
    {
        "n": 398,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """CHANGELOG.md has unreleased items older than two months.

Shall I cut a patch release notes draft or reorganize Unreleased sections?""",
        "text_b": """CHANGELOG.md has unreleased items older than two months.

Shall I use a different date format or version bump policy?""",
        "ann_a": ['Q e p :: Shall I cut a patch release notes draft or reorganize Unreleased sections?', 'O cut a patch release notes draft', 'O reorganize Unreleased sections'],
        "ann_b": ['Q y p :: Shall I use a different date format or version bump policy?'],
    },
    {
        "n": 399,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """REUSE.toml missing for two SVG assets — license CI fails.

Want me to add SPDX headers or generate the REUSE compliance report?""",
        "text_b": """REUSE.toml missing for two SVG assets — license CI fails.

Want me to use a different SPDX license or copyright holder line?""",
        "ann_a": ['Q e p :: Want me to add SPDX headers or generate the REUSE compliance report?', 'O add SPDX headers', 'O generate the REUSE compliance report'],
        "ann_b": ['Q y p :: Want me to use a different SPDX license or copyright holder line?'],
    },
    {
        "n": 400,
        "boundary": "yes_no/either_or",
        "note_a": 'tricky adjust-X-or-ship-Y -> either_or',
        "note_b": 'attribute reading of adjust wording -> yes_no',
        "text_a": """Accessibility pass left one open question on the toast component.

Want me to adjust the toast timing, or ship a focus-management fix instead?""",
        "text_b": """Accessibility pass left one open question on the toast component.

Want me to adjust the toast with a different timing or animation?""",
        "ann_a": ['Q e p :: Want me to adjust the toast timing, or ship a focus-management fix instead?', 'O adjust the toast timing', 'O ship a focus-management fix instead'],
        "ann_b": ['Q y p :: Want me to adjust the toast with a different timing or animation?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 401,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Transactional email: the liquid `if` for gift orders never renders.

[CODE]
{% if order.gift %}…{% endif %}
[CODE]

Want me to fix the gift branch or add a preview fixture set?""",
        "text_b": """Transactional email: the liquid `if` for gift orders never renders.

[CODE]
{% if order.gift %}…{% endif %}
[CODE]

Want me to use a different gift flag or branch condition?""",
        "ann_a": ['Q e p :: Want me to fix the gift branch or add a preview fixture set?', 'O fix the gift branch', 'O add a preview fixture set'],
        "ann_b": ['Q y p :: Want me to use a different gift flag or branch condition?'],
    },
    {
        "n": 402,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """ICU MessageFormat for plurals in `cart.items` is English-only.

Want me to add `one`/`other`/`few` for Polish or export the raw ICU for translators?""",
        "text_b": """ICU MessageFormat for plurals in `cart.items` is English-only.

Want me to use a different plural category set or message id?""",
        "ann_a": ['Q e p :: Want me to add `one`/`other`/`few` for Polish or export the raw ICU for translators?', 'O add `one`/`other`/`few` for Polish', 'O export the raw ICU for translators'],
        "ann_b": ['Q y p :: Want me to use a different plural category set or message id?'],
    },
    {
        "n": 403,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Focus order jumps past the dismiss button when the drawer opens from the right.

Shall I reorder the tab sequence or capture a before/after a11y video?""",
        "text_b": """Focus order jumps past the dismiss button when the drawer opens from the right.

Shall I use a different tab order or initial focus target?""",
        "ann_a": ['Q e p :: Shall I reorder the tab sequence or capture a before/after a11y video?', 'O reorder the tab sequence', 'O capture a before/after a11y video'],
        "ann_b": ['Q y p :: Shall I use a different tab order or initial focus target?'],
    },
    {
        "n": 404,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """WebSocket subprotocol negotiation fails on the canary ingress.

Want me to align the `Sec-WebSocket-Protocol` list or write a curl repro?""",
        "text_b": """WebSocket subprotocol negotiation fails on the canary ingress.

Want me to use a different subprotocol name or negotiation order?""",
        "ann_a": ['Q e p :: Want me to align the `Sec-WebSocket-Protocol` list or write a curl repro?', 'O align the `Sec-WebSocket-Protocol` list', 'O write a curl repro'],
        "ann_b": ['Q y p :: Want me to use a different subprotocol name or negotiation order?'],
    },
    {
        "n": 405,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two proto styles, not propose',
        "note_b": 'preference about attributes of one field name, not propose',
        "text_a": """For the public events API, both styles are on the table.

Which do you prefer — proto3 optional fields or explicit wrappers?""",
        "text_b": """For the event type field name, both styles work.

Do you prefer a shorter or more qualified field name?""",
        "ann_a": ['Q e :: Which do you prefer — proto3 optional fields or explicit wrappers?', 'O proto3 optional fields', 'O explicit wrappers'],
        "ann_b": ['Q y :: Do you prefer a shorter or more qualified field name?'],
    },
    {
        "n": 406,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`bazel run //tools:gazelle` rewrote 200 BUILD files overnight — noisy.

Want me to reinstate the intentional tags or produce a gazelle diff summary?""",
        "text_b": """`bazel run //tools:gazelle` rewrote 200 BUILD files overnight — noisy.

Want me to use a different gazelle directive or visibility default?""",
        "ann_a": ['Q e p :: Want me to reinstate the intentional tags or produce a gazelle diff summary?', 'O reinstate the intentional tags', 'O produce a gazelle diff summary'],
        "ann_b": ['Q y p :: Want me to use a different gazelle directive or visibility default?'],
    },
    {
        "n": 407,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Flake `devShell` lacks `postgresql` — onboarding docs assume it's there.

Shall I add it to `buildInputs` or update the README prerequisites?""",
        "text_b": """Flake `devShell` lacks `postgresql` — onboarding docs assume it's there.

Shall I use a different postgres package or version pin?""",
        "ann_a": ['Q e p :: Shall I add it to `buildInputs` or update the README prerequisites?', 'O add it to `buildInputs`', 'O update the README prerequisites'],
        "ann_b": ['Q y p :: Shall I use a different postgres package or version pin?'],
    },
    {
        "n": 408,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """iOS App Store screenshot set is still 6.5" only — 6.7" required now.

Want me to regenerate the 6.7" set or draft the ASC metadata checklist?""",
        "text_b": """iOS App Store screenshot set is still 6.5" only — 6.7" required now.

Want me to use a different device frame or screenshot locale?""",
        "ann_a": ['Q e p :: Want me to regenerate the 6.7" set or draft the ASC metadata checklist?', 'O regenerate the 6.7" set', 'O draft the ASC metadata checklist'],
        "ann_b": ['Q y p :: Want me to use a different device frame or screenshot locale?'],
    },
    {
        "n": 409,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Jupyter notebook uses `%matplotlib inline` — breaks in VS Code web.

Want me to switch to `widget` backend or document the VS Code caveat?""",
        "text_b": """Jupyter notebook uses `%matplotlib inline` — breaks in VS Code web.

Want me to use a different matplotlib backend or figure size?""",
        "ann_a": ['Q e p :: Want me to switch to `widget` backend or document the VS Code caveat?', 'O switch to `widget` backend', 'O document the VS Code caveat'],
        "ann_b": ['Q y p :: Want me to use a different matplotlib backend or figure size?'],
    },
    {
        "n": 410,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Spark storage formats, not propose',
        "note_b": 'preference about attributes of one table name, not propose',
        "text_a": """Fact table format decision is pending.

Which do you prefer — Delta Lake or Iceberg?""",
        "text_b": """Fact table naming decision is pending.

Do you prefer a shorter or more qualified table name?""",
        "ann_a": ['Q e :: Which do you prefer — Delta Lake or Iceberg?', 'O Delta Lake', 'O Iceberg'],
        "ann_b": ['Q y :: Do you prefer a shorter or more qualified table name?'],
    },
    {
        "n": 411,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Airflow `KubernetesExecutor` pods OOM on the feature-store DAG.

Want me to bump the pod memory request or write an executor comparison?""",
        "text_b": """Airflow `KubernetesExecutor` pods OOM on the feature-store DAG.

Want me to use a different memory request or executor type?""",
        "ann_a": ['Q e p :: Want me to bump the pod memory request or write an executor comparison?', 'O bump the pod memory request', 'O write an executor comparison'],
        "ann_b": ['Q y p :: Want me to use a different memory request or executor type?'],
    },
    {
        "n": 412,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kafka compaction topic grows unbounded — tombstones never land.

Shall I emit tombstones on soft-delete or document the compaction config?""",
        "text_b": """Kafka compaction topic grows unbounded — tombstones never land.

Shall I use a different cleanup.policy or min.cleanable.dirty.ratio?""",
        "ann_a": ['Q e p :: Shall I emit tombstones on soft-delete or document the compaction config?', 'O emit tombstones on soft-delete', 'O document the compaction config'],
        "ann_b": ['Q y p :: Shall I use a different cleanup.policy or min.cleanable.dirty.ratio?'],
    },
    {
        "n": 413,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OIDC IdP metadata URL returns HTML intermittently — discovery fails.

Want me to cache the JWKS aggressively or add a fallback static metadata file?""",
        "text_b": """OIDC IdP metadata URL returns HTML intermittently — discovery fails.

Want me to use a different metadata URL or cache TTL?""",
        "ann_a": ['Q e p :: Want me to cache the JWKS aggressively or add a fallback static metadata file?', 'O cache the JWKS aggressively', 'O add a fallback static metadata file'],
        "ann_b": ['Q y p :: Want me to use a different metadata URL or cache TTL?'],
    },
    {
        "n": 414,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Edge rate limiter counts OPTIONS preflight against the budget.

Want me to exempt OPTIONS or publish the current budget spreadsheet?""",
        "text_b": """Edge rate limiter counts OPTIONS preflight against the budget.

Want me to use a different exempt method list or budget key?""",
        "ann_a": ['Q e p :: Want me to exempt OPTIONS or publish the current budget spreadsheet?', 'O exempt OPTIONS', 'O publish the current budget spreadsheet'],
        "ann_b": ['Q y p :: Want me to use a different exempt method list or budget key?'],
    },
    {
        "n": 415,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Asset pipeline sets `immutable` on hashed CSS but forgets `max-age`.

Shall I add long-cache headers or write a CDN invalidation playbook?""",
        "text_b": """Asset pipeline sets `immutable` on hashed CSS but forgets `max-age`.

Shall I use a different max-age or immutable pairing?""",
        "ann_a": ['Q e p :: Shall I add long-cache headers or write a CDN invalidation playbook?', 'O add long-cache headers', 'O write a CDN invalidation playbook'],
        "ann_b": ['Q y p :: Shall I use a different max-age or immutable pairing?'],
    },
    {
        "n": 416,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """SVG logo still has embedded raster — fails the crispness check on 2x.

Want me to redraw as pure vectors or attach a before/after PNG?""",
        "text_b": """SVG logo still has embedded raster — fails the crispness check on 2x.

Want me to use a different path precision or stroke alignment?""",
        "ann_a": ['Q e p :: Want me to redraw as pure vectors or attach a before/after PNG?', 'O redraw as pure vectors', 'O attach a before/after PNG'],
        "ann_b": ['Q y p :: Want me to use a different path precision or stroke alignment?'],
    },
    {
        "n": 417,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Storybook interactions test flakes on the async Modal open.

Want me to stabilize with `waitFor` or skip the interaction test for now?""",
        "text_b": """Storybook interactions test flakes on the async Modal open.

Want me to use a different wait timeout or play-function delay?""",
        "ann_a": ['Q e p :: Want me to stabilize with `waitFor` or skip the interaction test for now?', 'O stabilize with `waitFor`', 'O skip the interaction test for now'],
        "ann_b": ['Q y p :: Want me to use a different wait timeout or play-function delay?'],
    },
    {
        "n": 418,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OpenAPI `servers` still lists localhost only — public SDK wrong.

Want me to add the prod server URL or generate an environments table?""",
        "text_b": """OpenAPI `servers` still lists localhost only — public SDK wrong.

Want me to use a different server description or variable default?""",
        "ann_a": ['Q e p :: Want me to add the prod server URL or generate an environments table?', 'O add the prod server URL', 'O generate an environments table'],
        "ann_b": ['Q y p :: Want me to use a different server description or variable default?'],
    },
    {
        "n": 419,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Unreleased CHANGELOG section mixes Added/Fixed without bullets consistency.

Shall I normalize the Unreleased formatting or cut notes for 2.5.0-rc1?""",
        "text_b": """Unreleased CHANGELOG section mixes Added/Fixed without bullets consistency.

Shall I use a different bullet style or section casing?""",
        "ann_a": ['Q e p :: Shall I normalize the Unreleased formatting or cut notes for 2.5.0-rc1?', 'O normalize the Unreleased formatting', 'O cut notes for 2.5.0-rc1'],
        "ann_b": ['Q y p :: Shall I use a different bullet style or section casing?'],
    },
    {
        "n": 420,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two license overlays, not propose',
        "note_b": 'preference about attributes of one NOTICE wording, not propose',
        "text_a": """Dual-licensing the CLI plugin is on the table.

Which do you prefer — Apache-2.0 only or Apache-2.0 OR MIT?""",
        "text_b": """NOTICE file tone is on the table.

Do you prefer a shorter or more lawyerly NOTICE blurb?""",
        "ann_a": ['Q e :: Which do you prefer — Apache-2.0 only or Apache-2.0 OR MIT?', 'O Apache-2.0 only', 'O Apache-2.0 OR MIT'],
        "ann_b": ['Q y :: Do you prefer a shorter or more lawyerly NOTICE blurb?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 421,
        "boundary": "yes_no/either_or",
        "note_a": 'soft two-arm propose -> either_or',
        "note_b": 'different-X-or-Y attributes -> yes_no',
        "text_a": """Email ESP sandbox accepted the template; production still needs approval.

Would you like me to submit the production template, or would you rather I pause and draft the approval email to ops?""",
        "text_b": """Email ESP sandbox accepted the template; production still needs approval.

Would you like me to tweak the template with a different from-name or reply-to?""",
        "ann_a": ['Q e p :: Would you like me to submit the production template, or would you rather I pause and draft the approval email to ops?', 'O submit the production template', 'O pause and draft the approval email to ops'],
        "ann_b": ['Q y p :: Would you like me to tweak the template with a different from-name or reply-to?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 422,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`next-intl` middleware locale detection fights the CDN's `Accept-Language`.

Want me to force cookie-based locale or document the detection order?""",
        "text_b": """`next-intl` middleware locale detection fights the CDN's `Accept-Language`.

Want me to use a different cookie name or detection priority?""",
        "ann_a": ['Q e p :: Want me to force cookie-based locale or document the detection order?', 'O force cookie-based locale', 'O document the detection order'],
        "ann_b": ['Q y p :: Want me to use a different cookie name or detection priority?'],
    },
    {
        "n": 423,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """aria-live region announces every keystroke in the search box — too chatty.

Want me to debounce announcements or switch to an assertive status only on submit?""",
        "text_b": """aria-live region announces every keystroke in the search box — too chatty.

Want me to use a different debounce ms or live politeness?""",
        "ann_a": ['Q e p :: Want me to debounce announcements or switch to an assertive status only on submit?', 'O debounce announcements', 'O switch to an assertive status only on submit'],
        "ann_b": ['Q y p :: Want me to use a different debounce ms or live politeness?'],
    },
    {
        "n": 424,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Protobuf `map<string, string>` for labels blows up codegen size.

Shall I replace maps with repeated `KeyValue` or keep maps and bump the size budget?""",
        "text_b": """Protobuf `map<string, string>` for labels blows up codegen size.

Shall I use a different map value type or repeated message shape?""",
        "ann_a": ['Q e p :: Shall I replace maps with repeated `KeyValue` or keep maps and bump the size budget?', 'O replace maps with repeated `KeyValue`', 'O keep maps and bump the size budget'],
        "ann_b": ['Q y p :: Shall I use a different map value type or repeated message shape?'],
    },
    {
        "n": 425,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Bazel remote setups, not propose',
        "note_b": 'preference about attributes of one platform string, not propose',
        "text_a": """Remote execution setup is still a product call.

Which do you prefer — BuildBuddy or a self-hosted REAPI farm?""",
        "text_b": """Platform string naming is still a product call.

Do you prefer a shorter or more specific platform string?""",
        "ann_a": ['Q e :: Which do you prefer — BuildBuddy or a self-hosted REAPI farm?', 'O BuildBuddy', 'O a self-hosted REAPI farm'],
        "ann_b": ['Q y :: Do you prefer a shorter or more specific platform string?'],
    },
    {
        "n": 426,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Android deep link scheme `app://o/{id}` collides with Next.js marketing routes.

Want me to narrow the intent filters or coordinate a path prefix with web?""",
        "text_b": """Android deep link scheme `app://o/{id}` collides with Next.js marketing routes.

Want me to use a different path prefix or host allowlist?""",
        "ann_a": ['Q e p :: Want me to narrow the intent filters or coordinate a path prefix with web?', 'O narrow the intent filters', 'O coordinate a path prefix with web'],
        "ann_b": ['Q y p :: Want me to use a different path prefix or host allowlist?'],
    },
    {
        "n": 427,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Spark Structured Streaming checkpoint dir is on ephemeral disk — bad idea.

Want me to move checkpoints to durable storage or write a recovery drill?""",
        "text_b": """Spark Structured Streaming checkpoint dir is on ephemeral disk — bad idea.

Want me to use a different checkpoint path or trigger interval?""",
        "ann_a": ['Q e p :: Want me to move checkpoints to durable storage or write a recovery drill?', 'O move checkpoints to durable storage', 'O write a recovery drill'],
        "ann_b": ['Q y p :: Want me to use a different checkpoint path or trigger interval?'],
    },
    {
        "n": 428,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Airflow Variable `db_url` is stored plaintext in the metastore UI.

Shall I migrate it to a Secret or document the rotation procedure?""",
        "text_b": """Airflow Variable `db_url` is stored plaintext in the metastore UI.

Shall I use a different Variable key or Secret backend?""",
        "ann_a": ['Q e p :: Shall I migrate it to a Secret or document the rotation procedure?', 'O migrate it to a Secret', 'O document the rotation procedure'],
        "ann_b": ['Q y p :: Shall I use a different Variable key or Secret backend?'],
    },
    {
        "n": 429,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kafka consumer `enable.auto.commit=true` fights manual offset commits.

Want me to disable auto-commit or diagram the current commit paths?""",
        "text_b": """Kafka consumer `enable.auto.commit=true` fights manual offset commits.

Want me to use a different auto.commit.interval or commit strategy?""",
        "ann_a": ['Q e p :: Want me to disable auto-commit or diagram the current commit paths?', 'O disable auto-commit', 'O diagram the current commit paths'],
        "ann_b": ['Q y p :: Want me to use a different auto.commit.interval or commit strategy?'],
    },
    {
        "n": 430,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OIDC `prompt=login` forces reauth every time — product hates it.

Want me to drop to `prompt=none` with fallback or write the UX tradeoff note?""",
        "text_b": """OIDC `prompt=login` forces reauth every time — product hates it.

Want me to use a different prompt value or max_age?""",
        "ann_a": ['Q e p :: Want me to drop to `prompt=none` with fallback or write the UX tradeoff note?', 'O drop to `prompt=none` with fallback', 'O write the UX tradeoff note'],
        "ann_b": ['Q y p :: Want me to use a different prompt value or max_age?'],
    },
    {
        "n": 431,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Rate limit redis key includes raw IP — IPv6 length blows the key size.

Want me to hash the IP in the key or switch to a compact encoding?""",
        "text_b": """Rate limit redis key includes raw IP — IPv6 length blows the key size.

Want me to use a different key prefix or hash algorithm?""",
        "ann_a": ['Q e p :: Want me to hash the IP in the key or switch to a compact encoding?', 'O hash the IP in the key', 'O switch to a compact encoding'],
        "ann_b": ['Q y p :: Want me to use a different key prefix or hash algorithm?'],
    },
    {
        "n": 432,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """`Vary: Accept-Encoding` missing — gzip and br variants collide in cache.

Shall I add the Vary header or purge and document the incident?""",
        "text_b": """`Vary: Accept-Encoding` missing — gzip and br variants collide in cache.

Shall I use a different Vary set or encoding preference?""",
        "ann_a": ['Q e p :: Shall I add the Vary header or purge and document the incident?', 'O add the Vary header', 'O purge and document the incident'],
        "ann_b": ['Q y p :: Shall I use a different Vary set or encoding preference?'],
    },
    {
        "n": 433,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """SVG icon `stroke-width` looks thinner in Safari than Chrome.

Want me to normalize with `vector-effect` or file a cross-browser matrix?""",
        "text_b": """SVG icon `stroke-width` looks thinner in Safari than Chrome.

Want me to use a different stroke-width or vector-effect setting?""",
        "ann_a": ['Q e p :: Want me to normalize with `vector-effect` or file a cross-browser matrix?', 'O normalize with `vector-effect`', 'O file a cross-browser matrix'],
        "ann_b": ['Q y p :: Want me to use a different stroke-width or vector-effect setting?'],
    },
    {
        "n": 434,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Storybook MDX docs page imports a missing design-token story.

Want me to restore that story or convert the MDX to autodocs?""",
        "text_b": """Storybook MDX docs page imports a missing design-token story.

Want me to use a different MDX layout or docs title?""",
        "ann_a": ['Q e p :: Want me to restore that story or convert the MDX to autodocs?', 'O restore that story', 'O convert the MDX to autodocs'],
        "ann_b": ['Q y p :: Want me to use a different MDX layout or docs title?'],
    },
    {
        "n": 435,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two OpenAPI review gates, not propose',
        "note_b": 'preference about attributes of one operation summary, not propose',
        "text_a": """API review process isn't settled.

Which do you prefer — Spectral in CI or a human OAS checklist?""",
        "text_b": """Operation summary style isn't settled.

Do you prefer a shorter or more verb-heavy summary?""",
        "ann_a": ['Q e :: Which do you prefer — Spectral in CI or a human OAS checklist?', 'O Spectral in CI', 'O a human OAS checklist'],
        "ann_b": ['Q y :: Do you prefer a shorter or more verb-heavy summary?'],
    },
    {
        "n": 436,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Keep-a-Changelog link to compare view 404s after the tag rename.

Want me to fix the compare URLs or drop the compare links entirely?""",
        "text_b": """Keep-a-Changelog link to compare view 404s after the tag rename.

Want me to use a different tag prefix or compare base?""",
        "ann_a": ['Q e p :: Want me to fix the compare URLs or drop the compare links entirely?', 'O fix the compare URLs', 'O drop the compare links entirely'],
        "ann_b": ['Q y p :: Want me to use a different tag prefix or compare base?'],
    },
    {
        "n": 437,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """LICENSE header script skipped `.tsx` — new files lack SPDX.

Shall I extend the header globs or backfill headers on the last 20 files?""",
        "text_b": """LICENSE header script skipped `.tsx` — new files lack SPDX.

Shall I use a different header template or SPDX tag style?""",
        "ann_a": ['Q e p :: Shall I extend the header globs or backfill headers on the last 20 files?', 'O extend the header globs', 'O backfill headers on the last 20 files'],
        "ann_b": ['Q y p :: Shall I use a different header template or SPDX tag style?'],
    },
    {
        "n": 438,
        "boundary": "yes_no/either_or",
        "note_a": 'tricky either_or with soft second arm -> either_or',
        "note_b": 'yes_no with different attributes -> yes_no',
        "text_a": """Nix flake check fails on aarch64-darwin for the protobuf plugin.

Want me to fix the aarch64 overlay, or would you rather I mark that system unsupported for now?""",
        "text_b": """Nix flake check fails on aarch64-darwin for the protobuf plugin.

Want me to tweak the overlay with a different derivation name or version?""",
        "ann_a": ['Q e p :: Want me to fix the aarch64 overlay, or would you rather I mark that system unsupported for now?', 'O fix the aarch64 overlay', 'O mark that system unsupported for now'],
        "ann_b": ['Q y p :: Want me to tweak the overlay with a different derivation name or version?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 439,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """JupyterLab extension for our theme conflicts with `@jupyterlab/toc`.

Want me to vendor a patched toc or disable our theme on that page?""",
        "text_b": """JupyterLab extension for our theme conflicts with `@jupyterlab/toc`.

Want me to use a different theme class prefix or z-index?""",
        "ann_a": ['Q e p :: Want me to vendor a patched toc or disable our theme on that page?', 'O vendor a patched toc', 'O disable our theme on that page'],
        "ann_b": ['Q y p :: Want me to use a different theme class prefix or z-index?'],
    },
    {
        "n": 440,
        "boundary": "yes_no/either_or",
        "note_a": 'preference between two Airflow deferrable styles, not propose',
        "note_b": 'preference about attributes of one task_id, not propose',
        "text_a": """Long-running sensor style is undecided.

Which do you prefer — classic sensors or deferrable operators?""",
        "text_b": """task_id naming is undecided.

Do you prefer a shorter or more hierarchical task_id?""",
        "ann_a": ['Q e :: Which do you prefer — classic sensors or deferrable operators?', 'O classic sensors', 'O deferrable operators'],
        "ann_b": ['Q y :: Do you prefer a shorter or more hierarchical task_id?'],
    },
    {
        "n": 441,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Kafka ACL still grants `*` on the staging cluster — audit finding.

Want me to tighten ACLs to service principals or export the current ACL dump?""",
        "text_b": """Kafka ACL still grants `*` on the staging cluster — audit finding.

Want me to use a different principal pattern or resource pattern?""",
        "ann_a": ['Q e p :: Want me to tighten ACLs to service principals or export the current ACL dump?', 'O tighten ACLs to service principals', 'O export the current ACL dump'],
        "ann_b": ['Q y p :: Want me to use a different principal pattern or resource pattern?'],
    },
    {
        "n": 442,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OIDC group claim is a string; we expected an array — authz breaks.

Shall I normalize the claim in middleware or ask IdP to emit arrays?""",
        "text_b": """OIDC group claim is a string; we expected an array — authz breaks.

Shall I use a different claim name or separator?""",
        "ann_a": ['Q e p :: Shall I normalize the claim in middleware or ask IdP to emit arrays?', 'O normalize the claim in middleware', 'O ask IdP to emit arrays'],
        "ann_b": ['Q y p :: Shall I use a different claim name or separator?'],
    },
    {
        "n": 443,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Storybook a11y addon fails on color-contrast for the warning badge.

Want me to fix the badge tokens or waive that rule with a comment?""",
        "text_b": """Storybook a11y addon fails on color-contrast for the warning badge.

Want me to use a different badge contrast or font weight?""",
        "ann_a": ['Q e p :: Want me to fix the badge tokens or waive that rule with a comment?', 'O fix the badge tokens', 'O waive that rule with a comment'],
        "ann_b": ['Q y p :: Want me to use a different badge contrast or font weight?'],
    },
    {
        "n": 444,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """OpenAPI webhook callback schema lacks `x-amazon-apigateway` bits we need.

Want me to add the vendor extensions or keep a separate SAM template?""",
        "text_b": """OpenAPI webhook callback schema lacks `x-amazon-apigateway` bits we need.

Want me to use a different extension key or callback path?""",
        "ann_a": ['Q e p :: Want me to add the vendor extensions or keep a separate SAM template?', 'O add the vendor extensions', 'O keep a separate SAM template'],
        "ann_b": ['Q y p :: Want me to use a different extension key or callback path?'],
    },
    {
        "n": 445,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """CHANGELOG generator double-counts squash merges.

Want me to fix the generator filters or hand-edit this release's notes?""",
        "text_b": """CHANGELOG generator double-counts squash merges.

Want me to use a different merge filter or commit matcher?""",
        "ann_a": ["Q e p :: Want me to fix the generator filters or hand-edit this release's notes?", 'O fix the generator filters', "O hand-edit this release's notes"],
        "ann_b": ['Q y p :: Want me to use a different merge filter or commit matcher?'],
    },
    {
        "n": 446,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """WebSocket gzip permessage-deflate negotiated but client doesn't decompress.

Want me to disable deflate on the server or patch the client inflater?""",
        "text_b": """WebSocket gzip permessage-deflate negotiated but client doesn't decompress.

Want me to use a different compression window or memLevel?""",
        "ann_a": ['Q e p :: Want me to disable deflate on the server or patch the client inflater?', 'O disable deflate on the server', 'O patch the client inflater'],
        "ann_b": ['Q y p :: Want me to use a different compression window or memLevel?'],
    },
    {
        "n": 447,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """Bazel `rules_python` pip.parse locked an old `protobuf` wheel.

Shall I bump the lock or document why we pin that wheel?""",
        "text_b": """Bazel `rules_python` pip.parse locked an old `protobuf` wheel.

Shall I use a different protobuf version or python platform?""",
        "ann_a": ['Q e p :: Shall I bump the lock or document why we pin that wheel?', 'O bump the lock', 'O document why we pin that wheel'],
        "ann_b": ['Q y p :: Shall I use a different protobuf version or python platform?'],
    },
    {
        "n": 448,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """iOS push entitlement missing on the Notification Service Extension target.

Want me to add the entitlement or write a TestFlight push checklist?""",
        "text_b": """iOS push entitlement missing on the Notification Service Extension target.

Want me to use a different entitlement key or team ID?""",
        "ann_a": ['Q e p :: Want me to add the entitlement or write a TestFlight push checklist?', 'O add the entitlement', 'O write a TestFlight push checklist'],
        "ann_b": ['Q y p :: Want me to use a different entitlement key or team ID?'],
    },
    {
        "n": 449,
        "boundary": "yes_no/either_or",
        "note_a": 'soft preference-looking but propose either_or vs attribute yes_no',
        "note_b": 'attribute alternatives -> yes_no',
        "text_a": """Email template lint found bare insecure tracking pixels.

Want me to rewrite them as protocol-relative links, or would you rather I remove tracking pixels entirely?""",
        "text_b": """Email template lint found bare insecure tracking pixels.

Want me to rewrite the pixels with a different host or path pattern?""",
        "ann_a": ['Q e p :: Want me to rewrite them as protocol-relative links, or would you rather I remove tracking pixels entirely?', 'O rewrite them as protocol-relative links', 'O remove tracking pixels entirely'],
        "ann_b": ['Q y p :: Want me to rewrite the pixels with a different host or path pattern?'],
        "diff_a": 'm',
        "diff_b": 'm',
    },
    {
        "n": 450,
        "boundary": "yes_no/either_or",
        "note_a": 'two deliverables -> either_or',
        "note_b": 'one change attributes -> yes_no',
        "text_a": """LICENSE CI: `cargo deny` flags `unicode-ident` as dual-licensed — fine, but noisy.

Want me to allowlist it in deny.toml or silence that advisory class?""",
        "text_b": """LICENSE CI: `cargo deny` flags `unicode-ident` as dual-licensed — fine, but noisy.

Want me to use a different allowlist severity or advisory id?""",
        "ann_a": ['Q e p :: Want me to allowlist it in deny.toml or silence that advisory class?', 'O allowlist it in deny.toml', 'O silence that advisory class'],
        "ann_b": ['Q y p :: Want me to use a different allowlist severity or advisory id?'],
    },
]

