# Hand-label conventions

Apply these rules to the assistant's full final-turn `text`. Label what the assistant asks the user to answer, not what a tagger might extract. A question's `prompt` is its exact Q span; `options` are exact OPT spans normalized by `build_gold.py`. Keep the original item ID.

## Addressed question

Label a direct request for the user's answer, choice, approval, or instruction. A question mark alone is insufficient: headings, jokes, quoted user text, sample output, rhetorical questions answered by the assistant, and advice are not questions to the user. A standalone offer without a question ("If you want, I can…") is also negative. Example: `Do you mean a git fast-forward (e.g., …), or something else?` is addressed to the user; `What does a "smart task" look like?` inside a proposed plan is not. A direct interrogative lead-in with a choice list can count without `?`: `Would you like me to:` followed by `Create a new GitHub repo` and `Add an existing remote` is a question. Use the exact question sentence from its first word through `?` when present; exclude a preceding list number or label. Include a second sentence only when it continues the same choice ("Shall I…? Or would you rather…?").

## Kind and alternatives

An explicit choice between two distinct answers or deliverables is `either_or`; three or more is `multi_choice`. This includes offers phrased as yes/no questions: `Want a diff or a walkthrough of any section?` is `either_or`, with `a diff` and `a walkthrough of any section`. A single proposed adjustment with several possible attributes remains `yes_no`: `Want the \`!\` indicator to use a different color or label?` asks whether to change it, without supplying two distinct changes. `Want a different filename or speed?` follows that rule. An open information request is `open`, even when it begins `Could you`, `Can you`, or `Do you remember`: `Could you clarify what you need help with?` and `Do you remember the repo directory (e.g. pi-mono) or approximate date so I can narrow it further?` need information rather than yes/no. `Could you build it now (osx-arm64) and share the result?` is `open` because the result is the answer; `Can you try running it directly … to see if you get more info?` remains `yes_no` because it asks the user to try an action without explicitly requesting the output. A genuine confirmation of a supplied fact remains `yes_no`.

## Escape hatches and examples

Do not count `or something else`, `or do you have a preference`, and similar open-ended escape hatches as options. `Which git operation do you want—fast-forward merge, pull with \`--ff-only\`, or something else?` has two options. `Do you mean a git fast-forward …, or something else?` has one named possibility, so it is `yes_no`. A `Which…?` request to name an unspecified other answer is `open`: `Which naming do you prefer — Auto / Confirm, or one of the others?` does not name the other choices in that message. Examples marked `e.g.` or `for example` inside a question illustrate possibilities; they are not options: `Could you clarify what “this” is—e.g., a specific file, directory, error message, or something else you’d like explained?` is `open`. If a later list explicitly offers selectable answers, label that list under the list rule below.

## Lists and option boundaries

Use a nearby list before or after a question as options only when the question asks the user to choose from that list. Background inventories, task plans, examples of possible requests, and diagnostic checklists do not automatically become choices. `Which module(s) would you like to work on today?` after a list of Pi packages selects from its package labels. `For example: … What can I help you with?` is open because those examples illustrate possible requests. A list cut off by the stored tail cannot supply a faithful option set: `Want me to implement one of these options?` after truncated Option 1 remains `yes_no`. In a choice list, take each bold heading or text before a dash/colon that separates a short label from its explanation; omit bullets, numbering, trailing parentheticals, and explanatory prose. Preserve a parenthetical that is part of the actual answer, such as `Modified C` versus `A`, or a substantive scope qualifier needed to distinguish choices. Inline choices use the shortest complete parallel phrases: `Want a diff or a walkthrough of any section?` yields `a diff` and `a walkthrough of any section`. In `For example:` diagnostic subquestions after `Could you describe what specifically looks different between the two?`, take each full diagnostic phrase without its question mark as an option because the list supplies selectable observations. `For example, do you want to:` followed by three concrete uses for `3000` likewise introduces actual selectable actions.

## Multiple questions

Record each independent addressed question in reading order. A list of distinct questions is multiple Q spans, not one choice list: `Do you want strict scoring …?` followed by `Should the game pause …?` has two records. When consecutive interrogative sentences present the two arms of one choice, use one Q span covering both sentences: `Shall I proceed with that lineup …? Or would you rather trim to a tighter set …?`. `expected` preserves this order, so the last record is the last question in the message; later explanatory text without a question does not replace it. A broad follow-up such as `Let me know…` is not a new Q.

## Propose

Set `propose: true` when the answer authorizes or requests an action the assistant offers to take, including `Want me to…?`, `Shall I…?`, `Want a diff?`, and confirmation of an agent plan. `Want me to build Snake … or dive into a Mario platformer …?` is a proposal. Set it false for information gathering or a preference question whose wording does not itself commit the agent: `Which git operation do you want…?` and `Which route do you prefer?` are not proposals.

## Multi-select

Set `multiSelect: true` only when multiple listed answers may be chosen together, signaled by `(s)`, `any of these`, `and/or`, `some or all`, or an explicit offer to combine choices. `Which module(s) would you like to work on today?` is multi-select. `Want me add some or all as Rules 8+?` is still a single yes/no proposal with no enumerated options, so its `multiSelect` is false.

## Default

Set a zero-based `default` only for an explicit recommendation or stated lean among the options, such as `I'd lean toward **A**` before `What's your read?`. A `REC` span may mark `(recommended)` or `(my lean)` after an option. Do not infer a default merely from option order, detailed explanation, or the assistant saying both choices are viable.

## Review and residual ambiguity

Preserve labels on items listed in `gold/review.jsonl` with a `human_review`/human verdict, even if a convention suggests a different reading; report disagreements. Remove `amb` when these rules settle an item. Keep it only when the full message supports two equally valid readings after applying the rules, and explain both in the annotation note.
