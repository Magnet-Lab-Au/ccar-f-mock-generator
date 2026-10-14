# Figure plan (academy decision 0037)

- Date: 14 October 2026
- Status: accepted by the owner on 14 October 2026, with the 5 fixes of the plan review (`figure-plan-review.html`, made with the command plan-review of the plugin).
- Source: the 56 figures of `pages/exam-guide-breakdown.html` (34) and `pages/behind-the-mocks.html` (22), as built at commit 982c7c5. The assistant loaded the skill of the plugin visual-explainer (version 0.12.0) for this plan.

## How to read the plan

Each figure gets one claim in one sentence, and one type from the table of the plugin:

| Type | The plugin uses it for |
|---|---|
| Stepper | a process that changes over time. It opens on the full picture. The reader goes one step at a time with the arrows. Nothing plays by itself. |
| Small multiples | cases, options or failure modes: the same small drawing once for each case, so only the difference changes |
| Before / after | one drawing with a toggle, so the reader sees exactly what changes. With no script, both panels show. |
| Live figure | a setting that the reader can try. One control changes the picture. |
| Close-up | a claim that lives in one small part, such as the fields of one record, drawn large |
| Diagram | a still drawing of a structure or a data flow |
| Bars, waffle, dimension line | a number. A dimension line sits on the span that it measures. |
| Grid, table with chips | cards, or a matrix of many rows |

"Change" says what happens to the figure:

- **Redraw**: the type changes.
- **Add**: the figure stays, and a picture for a number is added (the plugin rule "every number gets a picture").
- **Keep**: the figure already has the right type. It still gets the checks of decision 0013 and screenshots in both modes.

The facts of each figure stay the same. A redraw changes the form, not the content. Each label still comes from the fact sheet of its part (decision 0011).

## Tab 1, Exam guide breakdown (34 figures)

| Fig. | Claim | Now | Type | Change |
|---|---|---|---|---|
| A | The 5 domains have different weights, and domain 1 has the largest share. | grid of cards with weight bars | Grid, with one weight bar for each domain | Keep |
| B | Each scenario has 2 or 3 primary domains. | list | Table with chips: 6 scenarios by 5 domains | Redraw |
| 1.1-1 | The loop continues on "tool_use" and stops on "end_turn". | stepper | Stepper | Keep |
| 1.1-2 | Three ways to stop the loop are wrong, and stop_reason is right. | small multiples | Small multiples | Keep |
| 1.1-3 | The guide names two stop reasons, and the API has seven. | chips | Close-up: the seven values, two marked | Keep |
| 1.2-1 | All communication goes through the coordinator, and no subagent talks to another. | diagram | Stepper: delegate, each final result returns, a gap, a targeted query again | Redraw |
| 1.3-1 | A subagent that is not a fork gets only the prompt of its call, and only its final message returns. | diagram | Stepper: three calls in one response, the prompt only, the final messages back | Redraw |
| 1.4-1 | A hook runs at a fixed point, so the model cannot skip the check. | diagram | Small multiples: the check passes, the check denies. The escalation and its handoff summary become a third card. | Redraw |
| 1.5-1 | Two hook events wrap each tool call, and PostToolUse can change the result before Claude sees it. | diagram | Stepper, with a close-up of the value that changes | Redraw |
| 1.6-1 | A fixed chain suits known steps, and a dynamic plan changes with what each step finds. | two panels | Small multiples (two panels) | Keep |
| 1.7-1 | Resume keeps the session ID, fork copies the history to a new ID, and a fresh start uses a summary. | diagram | Small multiples: resume, fork, fresh start | Redraw |
| 2.1-1 | A specific name and description send each request to one tool. | diagram | Before / after: the rename only. The split example moves to the caption, because the reader agent found that the figure mixes two examples (decision 0039, item 12). | Redraw |
| 2.2-1 | Each category of error needs a different response, and an empty result is not an error. | diagram | Small multiples: valid empty result, transient, validation, business, permission | Redraw |
| 2.3-1 | Each agent gets only the tools of its role. | diagram | Diagram, plus a waffle for the 85% of simple checks | Add |
| 2.4-1 | Team servers go in .mcp.json, personal servers in ~/.claude.json, and the agent gets the tools of both. | diagram | Diagram | Keep |
| 2.5-1 | Glob and Grep find the entry points and Read follows the imports, so the context does not fill. | diagram | Small multiples: read all files first, Glob and Grep then Read. The context is a box that is full or not full, with no measure. | Redraw |
| 3.1-1 | Claude Code joins all CLAUDE.md files that it finds, and no file overrides another. | diagram | Diagram | Keep |
| 3.2-1 | context: fork runs a skill in a subagent, so only a summary reaches the main conversation. | diagram | Before / after: without fork, with fork | Redraw |
| 3.3-1 | A paths pattern loads a rule only for the files that match. | diagram | Live figure: the reader selects a file, and the figure shows if the rule loads | Redraw |
| 3.4-1 | A big or unclear change goes through plan mode, and a small clear change goes direct. | diagram | Diagram | Keep |
| 3.5-1 | The tests come first, and the failures go back to Claude until all tests pass. | diagram | Stepper: interview, tests, implement, run, failures back | Redraw |
| 3.6-1 | claude -p runs in CI and returns JSON findings, and in the guide they become comments on the pull request. | diagram | Stepper: the trigger, the context, the JSON, the comments | Redraw |
| 4.1-1 | Explicit criteria decide what to report, not a filter on confidence. | diagram | Before / after: a filter on confidence, explicit criteria. The after panel keeps the category that is disabled for a time (4.1-S2). | Redraw |
| 4.2-1 | 2 to 4 targeted examples, each with its reason, make the output consistent. | close-up of the prompt, with a flow | Close-up: the parts of the prompt, plus a dimension line "2 to 4" on the block of examples | Add |
| 4.3-1 | auto can answer in text, any must call a tool, and a forced choice must call the named tool. | diagram | Small multiples: auto, any, forced. Under the cards, one strip: the schema stops syntax errors, and code still checks the values (4.3-K3). | Redraw |
| 4.4-1 | A retry with the specific errors can fix a wrong value, but not information that the source does not have. | diagram | Small multiples: a retry helps, a retry cannot help | Redraw |
| 4.5-1 | A batch suits work that can wait: half the price, results in up to 24 hours. | diagram | Diagram, plus a dimension line for the 24 hours and bars for the price | Add |
| 4.6-1 | A new instance without the reasoning of the writer finds what a review in the same session misses. | diagram, two ideas | Small multiples: the same session, a new instance. The passes for each file and across files stay as one strip. | Redraw |
| 5.1-1 | The case facts stay word for word in each request, and older turns become a summary. | diagram | Close-up of one request, plus bars "40+ fields" and "5 relevant" (the example of the guide) | Add |
| 5.2-1 | Three triggers send a case to a human, and sentiment and confidence are not triggers. | diagram | Small multiples: three triggers, two cases that are not triggers. The figure no longer shows "Several matches?", because the reader agent found that it is not an escalation. The question for one more identifier moves to the text. | Redraw |
| 5.3-1 | An access failure returns structured context, and an empty result is a success. | diagram | Small multiples: results, empty result, access failure | Redraw |
| 5.4-1 | Four techniques keep a long exploration reliable: subagents for the verbose output, a scratchpad file of key findings, a manifest for a resume after a crash, and /compact. | diagram, four ideas | Small multiples: one card for each technique | Redraw |
| 5.5-1 | Calibrated confidence for each field routes the review, and a sample checks the high-confidence items. | diagram | Diagram, plus one bar for "97% overall". No live figure and no bars for each segment, because no source gives those numbers. | Add |
| 5.6-1 | Each finding keeps its claim, source and date through the synthesis. | diagram, busy | Close-up of one claim-source record, plus a short flow | Redraw |

## Tab 2, Behind the mocks (22 figures)

| Fig. | Claim | Now | Type | Change |
|---|---|---|---|---|
| A | Code moves each try through the steps, and each way back except step 5 waits for the owner. | diagram | Stepper: a try that passes, a try that fails, the checks of the complete mock, the decisions of the owner | Redraw |
| 0-1 | A script, not a model, copies the guide into records, and a second script checks them. | diagram | Diagram | Keep |
| 1-1 | Code plans 60 slots by fixed rules before a model writes any question. | diagram | Diagram, plus bars for the questions of each domain (16, 11, 12, 12, 9) | Add |
| 1-2 | Step 1 is on the fixed side, because the work of a mock is known before it starts. | two panels | Small multiples (two panels) | Keep |
| 1-3 | Ideas with two or more slots in one plan: 12 in mock 1, then 0. | bars | Bars | Keep |
| 2-1 | Each question comes from one request that code builds for one slot. | diagram | Close-up: the blocks of the request | Keep |
| 3-1 | Code checks 12 exact rules, and a try that fails one never reaches step 4. | diagram | Diagram, plus a bar for 477 passed and 11 failed | Add |
| 3-2 | The correct option was the longest in 37 of 52 questions in mock 1, and at or below chance after that. | bars | Bars | Keep |
| 4-1 | Call 4a answers with no key, call 4b checks the rules with the key, and code makes the verdict. | diagram | Stepper: call 4a, call 4b, the verdict of code | Redraw |
| 4-2 | Most findings of step 4 were rule B9, a repeat of an earlier question. | bars | Bars, plus one bar for the 477 checks: 329 passed and 148 failed | Add |
| 4-3 | Mocks 4 and 5 used prompt caching and cost about half. | bars | Bars | Keep |
| 5-1 | A pass stops the loop, and after 3 failed tries in one start the slot waits for the owner. | diagram | Stepper, plus a dimension line for the limit of 3 tries | Redraw |
| 5-2 | The 5 mocks needed 488 tries for 300 questions. | grid of squares | Waffle (one square for each slot) | Keep |
| 5-3 | The second design review found new items, most of them in the rules that answered the first, so the rules became code. | diagram | Diagram | Keep |
| 5-4 | The reason of the owner reached try 4, but not try 5. | diagram | Stepper: tries 1 to 5 | Redraw |
| 6-1 | Two calls read the 15 questions of a scenario together, and each finding goes to the owner. | diagram | Diagram | Keep |
| 6-2 | Step 6 made 108 findings, and the owner rewrote a question for 4 of them. | bars | Bars | Keep |
| 7-1 | The marking file shows no verdict of a checker. | diagram | Close-up: the columns of the marking file | Redraw |
| 7-2 | Over the 5 mocks, 209 marks were given, and 2 were bad. | five cards of text | Small multiples with bars: for each mock, the marks of round 1, of round 2, and the bad marks | Redraw |
| 8-1 | Code builds the files only after the owner accepts and six conditions hold. | diagram | Diagram | Keep |
| 8-2 | The correct letters of each built mock, against the chance line of 13. | small multiples | Small multiples | Keep |
| C-4.6-1 | Check 2 found 26 gaps and check 3 found 20, and then the owner stopped the checks. | diagram | Diagram, plus bars for 26 and 20 gaps. Check 1 shows "no count", not a bar of zero. | Add |

## Totals

| Change | Tab 1 | Tab 2 | All |
|---|---|---|---|
| Redraw | 21 | 6 | 27 |
| Add | 5 | 4 | 9 |
| Keep | 8 | 12 | 20 |

New steppers: 9 (1.2, 1.3, 1.5, 3.5, 3.6, A of tab 2, 4-1, 5-1, 5-4). With Fig. 1.1-1, the pages then have 10 steppers. New small multiples: 11. Before / after: 3. Live figure: 1 (Fig. 3.3-1). New close-ups: 2 (5.6-1, 7-1).

## The changes that go with the redraw (decision 0037, item 5)

- The takeaway in each closed heading (decision 0039, item 4).
- The label "Guide only" (item 10) and the three names of the documentation (item 11).
- The code popup of part 1.2 (item 15).

## Rules for the new figures (plan review)

- Each stepper has the form of Fig. 1.1-1: it opens on the full picture, the arrows go one step at a time, and each step adds at most one new part. It has no Play button and no slider (the choice of the owner, academy journal, 13 October 2026).
- The toggle of a before / after figure and the control of the live figure are new shared code in `build/academy.js`. A page has no inline script, because the security policy of the portal allows only scripts from the portal itself (`build/lib.py`, CSP). The move into the portal (decision 0017) ports this code too.
- The stepper of Fig. A of tab 2 keeps `data-figure="builder"`, the ID `top-fig-a` and the links to steps 0 to 8 in the full picture, because `check-pages.js` needs them.

## Motion (the owner, 14 October 2026)

The owner likes motion that keeps the reader interested and releases information step by step, but not too much. Three kinds, all from `references/diagrams.md` of the plugin:

- **Stepper**: the 10 steppers of this plan.
- **Moving dots** (the plugin calls them flow dots) on the full picture of a figure where something flows. The plugin says "One moving layer per page". So by default each tab has one figure with dots: Fig. 1.1-1 (the loop) on tab 1 and Fig. A (the 9 steps) on tab 2. Fig. 1.1-1 had dots in the sample, and the built page lost them, because the page script has no code for them.
- **Charts that grow and numbers that count up** when the reader scrolls to them, on each chart.

Nothing plays by itself. Dots move only while the figure is on the screen and shows its full picture. With reduced motion in the settings of the device, the page shows the final picture with no motion.

A test in domain 1: Fig. 1.2-1 (the coordinator) also gets dots, so tab 1 has two figures with dots. The owner looks at both. If the second helps, each tab can have 2 or 3 figures with dots. If not, the dots of 1.2-1 go, and the pages follow the plugin exactly.

The result of the test (the owner, 14 October 2026): "keep the dots on 1.2, add them where reasonable". So the pages do not follow the rule "One moving layer per page" of the plugin. A figure gets dots only where something flows along its arrows. The figures with dots: 1.1-1 (the loop), 1.2-1 (the coordinator), 3.5-1 (the test loop) and 3.6-1 (the CI pipeline) on tab 1, and Fig. A (the 9 steps) and 5-1 (the retry loop) on tab 2. Each figure still moves only while it is on the screen and shows its full picture.

## Order of the work

1. Tab 1, domain 1 (9 figures), as a test of the new types. The owner looks at the screenshots before the rest.
2. The other figures of tab 1, one domain at a time.
3. Tab 2.
4. The checks of decision 0013 for each figure, a review agent for each pair of parts, and screenshots in light and dark mode.
5. Before step 1: `check-pages.js` gets the visit of each step of each stepper, each state of each toggle and each choice of the live figure, in both modes and at both widths. Today it skips hidden text, so it checks only the first step.

## Facts that move out of a figure

A redraw keeps each fact of the current figure. Where a fact leaves the drawing, it goes to the caption, the text of the part, or a popup:

- 1.4-1: the escalation and its handoff summary become a third card of the same figure.
- 2.1-1: the split of analyze_document goes to the caption. The Explanation of 2.1 has 498 of 500 words, and a caption does not count.
- 2.5-1: the fallback from Edit to Read and Write (2.5-K4) goes to the caption.
- 4.1-1: the disabled category (4.1-S2) stays in the after panel.
- 4.3-1: the limit of a schema (4.3-K3) becomes a strip under the cards.
- 5.2-1: the question for one more identifier goes to the Explanation of 5.2 in one short sentence. It has 28 words left.
- 5.6-1: the parts that the close-up leaves out (the reconcile step of the coordinator, the content types) go to the caption. The Explanation of 5.6 has 500 of 500 words.

## Limits

- Each label of a figure is a checked fact (decision 0011). A close-up shows single names only (decision 0038). A line of code or a JSON example goes into a popup (decision 0032).
- Some numbers stay in the caption with no picture, because they compare with nothing: "ran 33 times" (6-2) and "17 cases" (5-2).
- The live figure of 3.3 is illustrative. It matches only the example file paths of the fact sheet of 3.3, and it does not copy the matcher of Claude Code.

- A stepper hides the steps that are not current. The full picture shows first, and with no script, the full picture shows.
- Not checked yet: the word limits of the parts after the redraw.
