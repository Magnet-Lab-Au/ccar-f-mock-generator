# Figure plan (academy decision 0037)

- Date: 14 October 2026
- Status: proposed. The owner checks it before any figure is drawn.
- Source: the 56 figures of `pages/exam-guide-breakdown.html` (34) and `pages/behind-the-mocks.html` (22), as built at commit 982c7c5. The skill of the plugin visual-explainer (version 0.12.0) was loaded for this plan.

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
| A | The 5 domains have different weights, and domain 1 has the largest share. | grid of cards | Grid, with one weight bar for each domain | Add |
| B | Each of the 6 scenarios draws on its primary domains. | list | Table with chips: 6 scenarios by 5 domains | Redraw |
| 1.1-1 | The loop continues on "tool_use" and stops on "end_turn". | stepper | Stepper | Keep |
| 1.1-2 | Three ways to stop the loop are wrong, and stop_reason is right. | small multiples | Small multiples | Keep |
| 1.1-3 | The guide names two stop reasons, and the API has seven. | chips | Close-up: the seven values, two marked | Keep |
| 1.2-1 | All communication goes through the coordinator, and no subagent talks to another. | diagram | Stepper: delegate, each final result returns, a gap, a targeted query again | Redraw |
| 1.3-1 | A subagent gets only the prompt of its call, and only its final message returns. | diagram | Stepper: three calls in one response, the prompt only, the final messages back | Redraw |
| 1.4-1 | A hook runs at a fixed point, so the model cannot skip the check. | diagram | Small multiples: the check passes, the check denies | Redraw |
| 1.5-1 | Two hook events wrap each tool call, and PostToolUse can change the result before Claude sees it. | diagram | Stepper, with a close-up of the value that changes | Redraw |
| 1.6-1 | A fixed chain suits known steps, and a dynamic plan changes with what each step finds. | two panels | Small multiples (two panels) | Keep |
| 1.7-1 | Resume keeps the session ID, fork copies the history to a new ID, and a fresh start uses a summary. | diagram | Small multiples: resume, fork, fresh start | Redraw |
| 2.1-1 | A specific name and description send each request to one tool. | diagram | Before / after: the rename only. The split example moves to the text (reader point, decision 0039 item 12). | Redraw |
| 2.2-1 | Each category of error needs a different response, and an empty result is not an error. | diagram | Small multiples: valid empty result, transient, validation, business, permission | Redraw |
| 2.3-1 | Each agent gets only the tools of its role. | diagram | Diagram, plus a waffle for the 85% of simple checks | Add |
| 2.4-1 | Team servers go in .mcp.json, personal servers in ~/.claude.json, and the agent gets the tools of both. | diagram | Diagram | Keep |
| 2.5-1 | Grep finds the entry points and Read follows the imports, so the context does not fill. | diagram | Small multiples: read all files first, Grep then Read, each with a bar of the context | Redraw |
| 3.1-1 | Claude Code joins all CLAUDE.md files that it finds, and no file overrides another. | diagram | Diagram | Keep |
| 3.2-1 | context: fork runs a skill in a subagent, so only a summary reaches the main conversation. | diagram | Before / after: without fork, with fork | Redraw |
| 3.3-1 | A paths pattern loads a rule only for the files that match. | diagram | Live figure: the reader selects a file, and the figure shows if the rule loads | Redraw |
| 3.4-1 | A big or unclear change goes through plan mode, and a small clear change goes direct. | diagram | Diagram | Keep |
| 3.5-1 | The tests come first, and the failures go back to Claude until all tests pass. | diagram | Stepper: interview, tests, implement, run, failures back | Redraw |
| 3.6-1 | claude -p runs in CI and returns JSON findings that become comments on the pull request. | diagram | Stepper: the trigger, the context, the JSON, the comments | Redraw |
| 4.1-1 | Explicit criteria decide what to report, not a filter on confidence. | diagram | Before / after: a filter on confidence, explicit criteria | Redraw |
| 4.2-1 | 2 to 4 targeted examples, each with its reason, make the output consistent. | diagram | Close-up: the parts of the prompt | Keep |
| 4.3-1 | auto can answer in text, any must call a tool, and a forced choice must call the named tool. | diagram | Small multiples: auto, any, forced | Redraw |
| 4.4-1 | A retry with the specific errors can fix a wrong value, but not information that the source does not have. | diagram | Small multiples: a retry helps, a retry cannot help | Redraw |
| 4.5-1 | A batch suits work that can wait: half the price, results in up to 24 hours. | diagram | Diagram, plus a dimension line for the 24 hours and bars for the price | Add |
| 4.6-1 | A new instance without the reasoning of the writer finds what a review in the same session misses. | diagram, two ideas | Small multiples: the same session, a new instance. The passes for each file and across files stay as one strip. | Redraw |
| 5.1-1 | The case facts stay word for word in each request, and older turns become a summary. | diagram | Close-up of one request, plus bars for the tool output cut from more than 40 fields | Add |
| 5.2-1 | Three triggers send a case to a human, and sentiment and confidence are not triggers. | diagram | Small multiples: three triggers, two cases that are not triggers. "Several matches?" is removed (reader point). | Redraw |
| 5.3-1 | An access failure returns structured context, and an empty result is a success. | diagram | Small multiples: results, empty result, access failure | Redraw |
| 5.4-1 | Subagents keep the verbose output, and the main agent keeps key findings in a scratchpad file. | diagram, four ideas | Stepper: one technique for each step (subagents, scratchpad, manifest, /compact) | Redraw |
| 5.5-1 | Calibrated confidence for each field routes the review, and a sample checks the high-confidence items. | diagram | Diagram. No live figure, because it would need numbers that no source gives. | Keep |
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
| 3-1 | Code checks 12 exact rules, and a try that fails one never reaches the model. | diagram | Diagram, plus a bar for 477 passed and 11 failed | Add |
| 3-2 | The correct option was the longest in 37 of 52 questions in mock 1, and at or below chance after that. | bars | Bars | Keep |
| 4-1 | Call 4a answers with no key, call 4b checks the rules with the key, and code makes the verdict. | diagram | Stepper: call 4a, call 4b, the verdict of code | Redraw |
| 4-2 | Most findings of step 4 were rule B9, a repeat of an earlier question. | bars | Bars | Keep |
| 4-3 | Mocks 4 and 5 used prompt caching and cost about half. | bars | Bars | Keep |
| 5-1 | A pass stops the loop, and after 3 failed tries the slot waits for the owner. | diagram | Stepper, plus a dimension line for the limit of 3 tries | Redraw |
| 5-2 | The 5 mocks needed 488 tries for 300 questions. | grid of squares | Waffle (one square for each slot) | Keep |
| 5-3 | The second design review found new items in the fixes of the first, so the rules became code. | diagram | Diagram | Keep |
| 5-4 | The reason of the owner reached try 4, but not try 5. | diagram | Stepper: tries 1 to 5 | Redraw |
| 6-1 | Two calls read the 15 questions of a scenario together, and each finding goes to the owner. | diagram | Diagram | Keep |
| 6-2 | Step 6 made 108 findings, and the owner rewrote a question for 4 of them. | bars | Bars | Keep |
| 7-1 | The marking file shows no verdict of a checker. | diagram | Close-up: the columns of the marking file | Redraw |
| 7-2 | Over the 5 mocks, 209 marks were given, and 2 were bad. | small multiples | Small multiples | Keep |
| 8-1 | Code builds the files only after the owner accepts and six conditions hold. | diagram | Diagram | Keep |
| 8-2 | The correct letters of each built mock, against the chance line of 13. | small multiples | Small multiples | Keep |
| C-4.6-1 | Check 2 found 26 gaps and check 3 found 20, and then the owner stopped the checks. | diagram | Diagram, plus bars for 26 and 20 gaps | Add |

## Totals

| Change | Tab 1 | Tab 2 | All |
|---|---|---|---|
| Redraw | 21 | 5 | 26 |
| Add | 4 | 3 | 7 |
| Keep | 9 | 14 | 23 |

New steppers: 10 (1.2, 1.3, 1.5, 3.5, 3.6, 5.4, A of tab 2, 4-1, 5-1, 5-4). With Fig. 1.1-1, the pages then have 11 steppers. New small multiples: 9. Before / after: 3. Live figure: 1 (Fig. 3.3-1).

## The changes that go with the redraw (decision 0037, item 5)

- The takeaway in each closed heading (decision 0039, item 4).
- The label "Guide only" (item 10) and the three names of the documentation (item 11).
- The code popup of part 1.2 (item 15).

## Order of the work

1. Tab 1, domain 1 (9 figures), as a test of the new types. The owner looks at the screenshots before the rest.
2. The other figures of tab 1, one domain at a time.
3. Tab 2.
4. The checks of decision 0013 for each figure, a review agent for each pair of parts, and screenshots in light and dark mode.

## Limits

- A stepper hides the steps that are not current. The full picture shows first, and with no script, the full picture shows.
- The live figure of 3.3 shows example file paths. They are the examples of the current figure, from the fact sheet of 3.3.
- Not checked yet: the word limits of the parts after the redraw.
