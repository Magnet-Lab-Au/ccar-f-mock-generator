# C2 skim takeaways (headings, figure labels and captions only)

## Tab 1: Exam guide breakdown

- top: no point (title only).
- map: The guide has 5 weighted domains with 30 task statements, and 6 scenarios that each touch 2 or 3 domains.
- breakdown: no point (heading "How we broke it down" with nothing under it).
- domain-1: no point (divider).
- ts-1-1: The agent loop continues while stop_reason is "tool_use" and stops on "end_turn", not on words, counts or any text.
- ts-1-2: A coordinator sends tasks to subagents and receives every result, and subagents never talk to each other directly.
- ts-1-3: A subagent gets only the prompt of its own call (so the coordinator must put the findings in it), and only its final message comes back.
- ts-1-4: To force an order (verify the customer before a refund), use a PreToolUse hook in code, not an instruction in the prompt.
- ts-1-5: PreToolUse can deny a call before it runs, and PostToolUse can rewrite the result before Claude sees it.
- ts-1-6: Use a fixed chain of steps when the work is known, and a plan that changes with findings when it is open.
- ts-1-7: Resume a session when its context is mostly valid, fork it to compare approaches, and start fresh with a summary when tool results are stale.
- domain-2: no point (divider).
- ts-2-1: Claude picks a tool by its description, so two tools with vague, overlapping descriptions get confused.
- ts-2-2: A tool error must say its category (transient, validation, business, permission) and whether a retry helps, and an empty result is not an error.
- ts-2-3: Each agent gets only the tools of its role, plus a narrow shared tool such as verify_fact for a frequent simple need.
- ts-2-4: Team MCP servers go in the committed .mcp.json with secrets in environment variables, and personal servers go in ~/.claude.json.
- ts-2-5: Grep first for entry points and then Read along the imports, instead of reading every file (the Glob and Edit parts of the heading come only from the caption).
- domain-3: no point (divider).
- ts-3-1: Claude Code joins all CLAUDE.md and rules files without overrides, and only the project files reach the team through git.
- ts-3-2: A skill with context: fork runs in its own subagent and returns only a summary to the main conversation.
- ts-3-3: A rule file with a paths glob loads only for matching files anywhere in the repo, which a folder CLAUDE.md cannot do.
- ts-3-4: Use plan mode (explore, plan, approve) for big or unclear changes, and direct execution for small clear ones.
- ts-3-5: Write tests first, let Claude implement, and send the failures back, with interacting issues in one message.
- ts-3-6: In CI, run claude -p with --output-format json and --json-schema, give it context, and post the findings as inline PR comments.
- domain-4: no point (divider).
- ts-4-1: Explicit criteria for what to report beat a confidence filter, and a noisy category can be switched off while the prompt is fixed.
- ts-4-2: 2 to 4 examples of ambiguous cases, each with its reason, make the output consistent where instructions alone do not.
- ts-4-3: tool_choice has three settings, and a schema stops syntax errors but not wrong values, which code must check (the panel captions about models that reject settings blur this).
- ts-4-4: Retry with the document, the failed result and the exact errors, but stop when the information is not in the source.
- ts-4-5: Use Message Batches (half price, up to 24 hours) only for work nobody waits for, and resend only the failed items by custom_id.
- ts-4-6: A fresh instance reviews better than the writer, file by file and then across files, with a confidence on each finding.
- domain-5: no point (divider).
- ts-5-1: Keep exact facts in a case facts block outside the summary, and trim tool output to the relevant fields.
- ts-5-2: Escalate on a request for a human, a policy gap or no progress, not on sentiment or the model's own confidence.
- ts-5-3: A failing subagent returns structured error context (type, query, partial results), and an empty result is a success.
- ts-5-4: Send exploration to subagents, keep key findings in a scratchpad file, use a manifest to resume, and /compact a full context.
- ts-5-5: Confidence scores route review only after a labeled set calibrates them, and a stratified sample checks each segment.
- ts-5-6: Each claim keeps its source and date through synthesis, and conflicts keep both values in a "contested" section.

## Tab 2: Behind the mocks

- top: The mocks were built with the same principles that the exam tests.
- steps: no point (heading "The 9 steps" only).
- step-0: A script, not a model, copies the needed parts of the exam guide into one records file, checked by a second script.
- step-1: Code plans 60 slots (domain counts, scenarios, task statements, unused ideas) before any model writes, and this stopped repeated ideas after mock 1.
- step-2: Each question is written by one new Claude call from a request that code builds, and the call does not see the other questions.
- step-3: Code checks 12 exact rules before any model check, and the rule on the longest option cut a strong bias after mock 1.
- step-4: One Claude call answers blind, one checks 9 judgment rules, code makes the verdict, most failures were repeats of earlier questions (B9), and caching halved the cost from mock 4.
- step-5: A failed try returns to the writer with its findings, at most 3 tries per start, then the owner decides, and 488 tries made 300 questions.
- step-6: Two calls read each scenario's 15 questions together, and the owner decides each of 108 findings (4 rewrites).
- step-7: A reader marks each question good or bad in a file that hides the checkers' verdicts, and 2 of 209 marks were bad.
- step-8: Code builds the mock files only after the owner accepts and 6 conditions hold, and the answer letters became balanced by mock 5.
- cc-3-1: no point (a heading about one short file loading the rules, and an unexplained "A file that was not in git").
- cc-1-7: A new session starts from a summary that an earlier session wrote (but "The summary was not read" is unexplained).
- cc-4-6: Documents were checked by agents that did not write them, and the gaps fell from 26 to 20 before the owner stopped the checks.
- cc-3-4: The build used a "discuss first" rule instead of plan mode (the "not a block" heading is unexplained).
