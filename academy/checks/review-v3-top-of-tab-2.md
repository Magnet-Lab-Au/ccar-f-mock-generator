# Review: the top of tab 2, version 3 (#truth, #tools) and academy decision 0046

- Date: 15 October 2026
- Reviewer: an independent agent that did not make the files.
- Files read: `academy/build/make-behind-the-mocks-v3.py` (section "VERSION 3", lines 2090 to 2240), the built `academy/pages/behind-the-mocks-v3.html` (text of #truth and #tools), the `v3-` popups in `academy/pages/behind-the-mocks-v3.js`, `academy/decisions/0046`, 0042, 0045, 0010, mock decisions 0001, 0008, 0012, 0019 (item 5), 0026, 0027, 0067, `academy/journal.md` line 9, `academy/facts/task-statement-use.json` (states only, not reviewed again), and the source lines of the cards (exam guide line 152, sub-agents copy line 490, batch copy line 82).
- Not checked: the quotes of the owner in 0046, the content of the mock v1 document (not in the repository), and the layout of the page in a browser.
- Script checks on the visible text of the two sections and the `v3-` popups: 0 semicolons, 0 em dashes, 0 en dashes, 0 contractions. One prose sentence has more than 25 words (L5). No personal file of the owner and no quote of the CCAR-F course appear.

Counts: 3 high, 6 medium, 6 low.

## High

**H1. The opening paragraph of #truth puts a 14 October fact before the first question.**
Place: #truth, paragraph 1 (builder, `TRUTH`, "Before we wrote a single question ... A candidate who learned the product could choose the wrong answer in the exam.").
What is wrong: The paragraph says that before any question we read the guide, the documentation and the course side by side, and then gives the Task/Agent difference as what we observed. The Task/Agent example comes from the documentation copy of 14 October 2026 (card `v3-docs13`), after mocks 1 to 5. For the present builder, mock decision 0008 records no side-by-side reading. It records only that the assistant checked four sample questions against the guide alone. The side-by-side reading has its only source in the mock v1 document, which is not in the repository. A reader takes the paragraph as a recorded fact of the present build.
Fix: Tie the reading to mock v1 and the example to the academy check. Suggested text: "Before we wrote a question, we had to know what a correct answer is. For mock v1, we used three sources: the exam guide, the Claude documentation and the CCAR-F course. Our notes from that time say that they did not always agree. Later, a check of the documentation of 14 October 2026 showed one example. The guide names [fact v3-guide13]. [fact v3-docs13] A candidate who learned the product could choose the wrong answer in the exam."

**H2. "These marks show what has changed since the guide was written" goes against academy decision 0042.**
Place: #truth, last paragraph, sentence 3 ("Anthropic changes its products fast, and these marks show what has changed since the guide was written.").
What is wrong: Decision 0042, item 3, says that the box says "The product today", not "changed since the guide", because many of these facts were true before the guide, and the documentation does not say when the product changed. In "How we decided", the assistant told the owner that "changed since the guide" "is mostly not true and cannot be checked for most places". The page now makes that claim.
Fix: "Anthropic changes its products often. The boxes show how the product differs from the guide on 14 October 2026. For most of them, the documentation does not say when the product changed."

**H3. #tools says that we asked about each of the 30 task statements, and calls the map "30 choices".**
Place: #tools, paragraph 1, sentence 3 ("For each one, we asked whether this job needed it."), and paragraph 2, sentence 1 ("The map shows the result of all 30 choices. An empty tile is a choice too: the job did not need it.").
What is wrong: No record shows a question for each task statement at design time. Mock decision 0001 says the opposite: "We discussed a different method: go through the 30 task statements first and mark each one. We rejected it as the starting point. ... The list stays as the final check." The map itself was drafted on 15 October 2026 from the records by an agent (decision 0046, item 15). Only some tiles rest on a recorded choice (for example 0012, 0026, 0067). This is the overclaim the owner fears most for senior leaders.
Fix: Paragraph 1: "The guide teaches 30 task statements. We did not try to use them all. We designed each step for its job, and then checked which task statements it used. Three choices show how we decided." Paragraph 2: "The map shows, for all 30 task statements, what the records show that the build used. We made it from the records on 15 October 2026, and an independent agent checked it. A grey tile means that the job did not need the task statement."

## Medium

**M1. Stage 1 of Fig. S has no source on the page, and only the popup says so.**
Place: Fig. S, stage "September 2026, Mock v1" ("We compared all three, and saw that they disagree.") and its popup `v3-s1`, sentence 2 ("A separate agent checked each quote ... we removed it.").
What is wrong: The stage and the figure caption state stage 1 as fact. The note "They are not in this repository" is the third sentence of a popup, and the "Sources of the truth" list has no entry for stage 1. Decision 0046, "How we decided", says that the owner shared the document as "a prototype from mock v1" and "said that it may be inaccurate". The page does not say that. The detail about one sentence that no source contained is precise, but nobody can check it.
Fix: (a) Add to the figure caption: "Stage 1 comes from our notes of mock v1, which are not in this repository." (b) Add one line to "Sources of the truth": "Mock v1, How These Mocks Were Made, 30 September 2026. Not in this repository. Not checked." (c) In popup `v3-s1`, either remove sentence 2, or begin it with "Our notes of mock v1 say that".

**M2. The heading "No MCP, no hooks, no sessions" disagrees with the map.**
Place: #tools, choice 2, bold heading, and Fig. M, tile 1.7.
What is wrong: Fig. M shows 1.7 "Session state" as "Used, Claude Code". Decision 0026 is about the pipeline only. A reader sees "no sessions" and then a tile that says that sessions were used.
Fix: Bold heading "In the builder: no MCP, no hooks, no sessions." Add after the last sentence: "The build in Claude Code is different: it kept its state across sessions (task statement 1.7)."

**M3. The heading "No subagents" disagrees with the map in the same way.**
Place: #tools, choice 1, bold heading, and Fig. M, tiles 1.2 and 1.3.
What is wrong: Tiles 1.2 and 1.3 say that the assistant started fact agents and review agents in the build in Claude Code. The choice is about the pipeline (mock decision 0012).
Fix: Bold heading "In the builder: no subagents." The sentence that follows already names the pipeline.

**M4. Fact span `v3-0026` changes "uses" to "needed".**
Place: #tools, choice 2, fact `v3-0026`: "The pipeline needed no MCP, no subagent, no hook and no session." Card quote: "The pipeline uses no MCP, no subagent, no hook and no session."
What is wrong: The span adds a judgment of need that the quoted sentence does not make. The rule is that a span says what its card quote says and no more.
Fix: "The pipeline used no MCP, no subagent, no hook and no session." The next sentences already give the reason.

**M5. Fact span `v3-0026b` covers hooks and sessions, but its quote covers only MCP and subagents.**
Place: #tools, choice 2, fact `v3-0026b`: "So we accepted none of them." Card quote: "The owner said: \"I accept no MCP and subagents\"."
What is wrong: "none of them" points back to MCP, subagents, hooks and sessions. The quote names only MCP and subagents. Decision 0026 records hooks and sessions as a separate "Sure". Also "accepted none of them" can be read as "rejected the proposal".
Fix: Span text: "We decided to add no MCP and no subagents." Then a plain sentence without a card: "We decided the same for hooks and sessions." Or change the card quote to cover lines 67 with "The owner said: \"Sure\"" as well.

**M6. Decision 0046, item 9, says "mark each difference". Decision 0042 says a box marks only a difference that changes the exam answer.**
Place: `academy/decisions/0046-tab-2-tells-a-story-before-the-steps.md`, line 30 ("The academy pages check the documentation of a fixed date and mark each difference (academy decision 0042)."). The same idea is on the page, Fig. S stage 3: "We check the product, and mark each gap with its date."
What is wrong: Decision 0042, item 4: "A box goes only where the product fact could lead a candidate to a different exam answer. Where the documentation only uses other words or says nothing, the label 'Guide only' stays." So not each difference has a box. The stage-3 popup says it correctly.
Fix: 0046 line 30: "... and give a box where a difference could change the exam answer (academy decision 0042)." Fig. S stage 3: "We check the product on a fixed date, and mark each gap that could change an answer." Under working rule 26, the text of 0046 is not yet confirmed, so it can still change.

## Low

**L1. "a whole batch" adds to the quote.**
Place: #tools, choice 3, fact `v3-0067a`. Quote: "the rounds of the pipeline would wait for each batch".
Fix: "We rejected it, because each round of the pipeline would wait for its batch."

**L2. Fact span `v3-0067b` adds "In a test on 10 questions", which its card quote does not contain.**
Place: #tools, choice 3. The fact is true (0067, Reason, line 102), but it is outside the quoted text.
Fix: Extend the card quote to start at "calls 4a and 4b checked 10 questions of mock 3 again." Or move "In a test on 10 questions," out of the span. Optional, for balance: 0067 also records that 2 of the 10 verdicts changed. The page claims only the cost, so this is not an overclaim.

**L3. "So each check is a plain call" is wider than decision 0012.**
Place: #tools, choice 1, last sentence. Step 3 checks are code, not model calls.
Fix: "So each model check is a plain call with a fresh context, and no subagent was needed."

**L4. "The old name still works" is wider than the source.**
Place: #truth, box "One difference, side by side", line "The product today". Source line 490: "Existing `Task(...)` references in settings and agent definitions still work as aliases."
Fix: "The Task tool is now called Agent. The old name still works in settings and agent definitions."

**L5. One sentence has 28 words.**
Place: popup `v3-s3`, sentence 2 ("Where a product fact could lead to a different exam answer, a box gives the answer of the guide and the product today: 23 boxes in 15 parts.").
Fix: "Tab 1 has 23 boxes in 15 parts. Each box stands where a product fact could lead to a different exam answer. It gives the answer of the guide and the product today."

**L6. Decision 0046 names the stage-1 source in two ways.**
Place: `academy/decisions/0046-...md`, line 32 ("the build notes of mock v1, 30 September 2026") and line 56 ("a prototype from mock v1, 'How These Mocks Were Made' (30 September 2026) ... may be inaccurate"). `academy/journal.md` line 9 calls it a prototype too. The page uses "build notes".
Fix: Use one name in 0046, item 11, and on the page: "the document 'How These Mocks Were Made' of mock v1, 30 September 2026", and add to item 11: "The owner said that it may be inaccurate."

## Decision 0046: other points checked

- Format: the header lines (Date, Status, Text confirmed, Diagram, Changes) and the sections Question, Decision, Reason, How we decided, Exam guide points match 0042 and 0045. The extra section "Built (15 October 2026)" is like "The places" in 0042, and is acceptable.
- "Changes: decision 0010, tab 2, item 1" is correct: item 1 of tab 2 in 0010 sets the title and the paragraph at the top.
- The counts 10 used, 11 idea only, 9 not used agree with `task-statement-use.json` and with the caption of Fig. M.
- Items 3 to 6, 8, 10, 13 and 14 agree with the page. Item 11 ("the page says so") is true only in a popup (see M1).
- The two open points for the owner (1.2 and 1.3, and 2.5 and 3.2 against decision 0035) are stated clearly.

## Other statements checked and found correct

- The three dates of Fig. S: 6 October 2026 is the date of mock decision 0008. 14 October 2026 is the date of academy decision 0042 and of the documentation copies. September 2026 has no source in the repository (M1).
- "We chose one source of truth: the guide" and popup `v3-s2` agree with 0008 ("the program reads the exam guide only"). 0008 limits this to "the first version", and no later mock decision found adds a source for the facts of a question. Mock decision 0019, item 5, confirms that the rule "the answer of the guide is the answer of the exam" is a choice of the owner, and the page presents it as a choice ("we chose one rule").
- "23 boxes in 15 parts" matches 0042, The places, line 33.
- The fact spans `v3-guide13`, `v3-docs13`, `v3-0008a`, `v3-0008b`, `v3-0042`, `v3-0012`, `v3-0012b` and `v3-batch` say what their quotes say. Each quote is on its stated file and line.
