# Review: the text of academy decision 0046 (after version 4)

- Date: 15 October 2026
- Reviewer: an independent agent that did not write the file (working rule 35)
- File: `academy/decisions/0046-tab-2-tells-a-story-before-the-steps.md`
- Files read: the decision, decision 0010 (tab 2, items 1 to 4), decisions 0042 and 0045 (format), `academy/build/make-behind-the-mocks-v4.py` (docstring, CC_PRINCIPLE, PRINCIPLE, ts_of, map_tile, the counts, LIMITS, the overview), the headings and texts of `academy/pages/behind-the-mocks-v3.html` and `behind-the-mocks-v4.html`, the links `#cc-*` in `behind-the-mocks-v4.js`, `academy/facts/task-statement-use.json` (states and "where"), the tables of guide points in `docs/build-guide/step-*.md`.
- Not checked: the quotes of the owner, the claims of item 10 and item 16 again (the earlier review `review-v3-top-of-tab-2.md` covered them), the 13 changed entries and 8 weaker claims of line 43, the layout in a browser.

## What agrees

- Counts: the JSON has 11 "used", 10 "idea", 9 "not-used". The caption of Fig. M on both pages says "used 11, used 10 in part, and did not use 9". The key says "in part, or in another way than the guide names". Lines 45 and 47 agree.
- Headings on both pages: "First, we settled what is true", "Next, we used only what the job needed", "Then, we built it in 9 steps". The bridge of line 49 is on both pages word for word.
- "Code runs only 4 of the 9 steps alone": WHO_LONG gives code alone for steps 0, 1, 3 and 8. Correct.
- The 4 principles of line 53, their task statements and states agree with CC_PRINCIPLE and the map. The bridge agrees with the page. The tiles 3.1, 1.7, 4.6 and 3.4 link to `#cc-3-1`, `#cc-1-7`, `#cc-4-6`, `#cc-3-4` through their popups.
- The short line has at most 10 words (an assert in the builder).
- The last section: the heading and the bridge agree with v4. The old lead of v3 follows in the same paragraph. The two boxes are still there.
- 1.3 is "used" and 1.2 is "idea", both at the level of the build in Claude Code. The footnote of choice 1 says that the build used subagents.

## High

None.

## Medium

M1. Line 22, item 5. The page heading is "Next, we used only what the job needed", not "Then, ...". Line 49 changes the word without saying that it changes item 5.
Replace item 5 with:
`5. "Next, we used only what the job needed": three choices, and a map of the 30 task statements. (Line 49 changed "Then" to "Next".)`
If item 5 is a confirmed text that must not change, add to line 49 instead: `This changes the word "Then" of item 5 to "Next".`

M2. Line 4, status. It names only version 3. Version 4 is built and approved by the owner. A change of the status line is permitted (rule 26).
Replace with:
`- Status: accepted. Built as version 3, `academy/pages/behind-the-mocks-v3.html`, and version 4, `academy/pages/behind-the-mocks-v4.html`. The original tab 2 and version 2 do not change.`

M3. Line 7, "Changes". Version 4 changes the closed state of each step (decision 0010, tab 2, item 3: "Closed: the step name and its place in the 9-step diagram") and of each part of the build in Claude Code (item 4). The header names only item 1.
Replace with:
`- Changes: decision 0010, tab 2, item 1 (what comes under the title and the paragraph of the owner). In version 4, decision 0010, tab 2, items 3 and 4 (the closed state of each step and of each part of the build in Claude Code).`

M4. Line 51. "its principle with the task statements of its build guide table" is not exact. The builder shows only the task statements of the principle, a subset of the table: step 2 shows 4.3 and 4.2 of 4.3, 4.2, 4.1, 1.4. Step 8 shows none. The line also does not say that the takeaway of each step leaves the page in version 4 (builder comment at the PRINCIPLE table, and `_take` is not used).
Replace the first sentence with:
`Version 4 (owner, 15 October 2026) is built by `academy/build/make-behind-the-mocks-v4.py` as `academy/pages/behind-the-mocks-v4.html`. Each closed step shows its principle and the task statements of that principle, taken from the table of the step in the build guide. Step 8 has none. Under the principle, a short line of at most 10 words says what the step does. The last line gives the name of the step and who does it. The takeaway of each step leaves the page.`

## Low

L1. Line 49, last sentence. "Fig. A, its caption and the section "The 9 steps" stay as they are." Version 4 (line 51) changes the closed steps.
Replace with: `In version 3, Fig. A, its caption and the section "The 9 steps" stay as they are. Version 4 changes the closed steps (see below).`

L2. Line 24, item 7. "each step heading becomes a principle with its task statement". Step 2 has two task statements and step 8 has none. "The owner wants to see it before a decision on the words" is now history, because line 51 records the approval. Item 7 is a decision item, so do not change it. Line 51 with the text of M4 makes the exact form clear. No change needed if M4 is done.

L3. Line 31, item 10, second sentence, has about 37 words.
Replace with: `They became the benchmark. The guide alone answers 4 that the assistant checked (mock decision 0008). Call 4a answered all 12 right before mock 1. Rule B8 stops a close copy of one of them.`

L4. Passive voice: line 4 "Built as version 3", line 34 "It is not built yet", line 55 "is not added".
Replace line 34 end with `We did not build it yet.` Replace line 55 end with `We did not add the concept "Where the process failed" of the document of mock v1, because the Depth of each step holds its failures.` Line 4 follows the form of the other status lines, so keep it.

L5. Line 53. "Each part has the same form as the 9 steps" is almost exact: a step shows its task statement chips and who does it, and a part shows its state on the map instead.
Replace with: `Each part has the form of the 9 steps: a principle, a short teal line, and its name. In place of who does it, the part gives its state on the map.`

L6. Outside the file (no change to 0046): the docstring of `make-behind-the-mocks-v4.py`, lines 4 to 8, says that version 3 and version 2 write `behind-the-mocks-v4.html`. They write the v3 and v2 files.

## Format and style

- The header lines and the sections (Question, Decision, Reason, How we decided, Exam guide points) agree with 0042 and 0045.
- No semicolons, em dashes or contractions outside the quotes of the owner.
- Item numbers 1 to 16 are in sequence. Line 43 ("items 3 to 6 and 8 to 16") agrees with them.
- No stale "not approved yet" remains. The first count of line 43 (10, 11, 9) is corrected by line 45, and line 45 says so.
