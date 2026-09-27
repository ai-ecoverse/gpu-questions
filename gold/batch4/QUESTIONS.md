# Batch 4 convention questions

- t4b:019b9d12-16e0-7ae0-b233-a6356d3c6d67:22 | “OK to bump packed version to v10 (hard switch), and should the web client expose the kind byte in results?” | One yes_no proposal span; both approvals are requested in the same sentence. Ambiguous because either clause could be answered separately.
- t4b:019bc745-ef1d-7981-99a9-df7cc17fa981:11 | “Do you want to define `Language.IsContextFree` (or reuse Mathlib’s) in this file, or just import it?” | Three named alternatives: define, reuse, import. Ambiguous because reuse and import may describe the same action.
- t4b:019b9ddd-922e-7622-80ba-50e858fa99db:6 | “Where do you want the logs (console vs on-page), and should they be always-on or behind a flag?” | One multi_choice span with four option spans. Ambiguous because the sentence requests two independent preferences without a clean sentence boundary.
- t4b:tandem:2026-09-05-shiftboard:0 | “approve this complete plan or request a revision.” | Direct imperative choice addressed to the human; either_or proposal even without a question mark. The compiler misses it.

Append `id | question | decision`.

t4a:0015 | one sentence holding two questions: "Which do you want — and do you genuinely want me to start X, or is Y the right stopping point?" after two numbered offers | t4-a: two records, "Which do you want" (either_or over the numbered offers, no '?' in the span) and the either/or proposal after the dash; amb
t4a:0027 | "Want me to move them there now?" … plan list … "Should I go ahead with that move?" | t4-a: two records (the batch-2 rule says differently worded questions are separate; the restatement rule covers only option lists); amb
t4a:0068/0075/0107 | Chinese "有什么我可以帮助你的吗？" / "有什么具体任务需要我帮忙吗？" ("Is there anything I can help with?") | t4-a: yes_no, by the "Is there anything …" precedent (a0200); the compiler reads them as open
t4a:0105 | Chinese "do you mind or not mind …?" whose answers map to options A/B listed below, closed by "你选哪个,我就开工。" (no '?') | t4-a: one either_or record over 介意 / 不介意; the closing line restates the choice and is not a separate record; amb
t4a:0128 | numbered list of three alternative readings, each a question with its own follow-up sub-questions, then "你期望看到什么？" | t4-a: one multi_choice span over the three bold arms (sub-questions not separate), plus the closing open question; amb
t4a:0155 | "Does she speak English, or do you know what language she'd need services in?" | t4-a: open (one named possibility plus a request to name the answer, per the CONVENTIONS escape-hatch rule)
t4a:0148 | "Want me to sketch X, or is that too prescriptive?" | t4-a: yes_no proposal; a hedge arm that names no deliverable is treated like "or adjust anything" (batch-3 d0766)
t4a:0120/0122 | "Want me to fix these?" followed by the statement "I can do all of it, a subset, or just one"; "Want me to wire one of these …?" with a stated lean in prose | t4-a: yes_no proposals (the scopes/approaches are not offered inside the question); amb
