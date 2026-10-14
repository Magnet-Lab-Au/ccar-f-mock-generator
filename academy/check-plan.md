# Reader check plan, from 14 October 2026

Status: proposed. The owner asked for this plan on 14 October 2026 and chose to run all checks.

An independent agent checked the first version and found 14 problems, 5 of them high. This version fixes all 14.

## Aim

Find the errors and the weak places of the two tabs before the owner reviews them. Most checks read the pages as a stranger would. Scripts do the checks that need no judgment.

The assistant works alone. The owner's yes to this plan covers each step in it (working rules 32 and 33). It also covers the push at the end.

## What the assistant changes, and what it only lists

| Kind of finding | Action |
|---|---|
| A clear error: a wrong fact, a wrong number, a broken link, a typo, two names for one thing | The assistant fixes it. |
| A change of text, a popup or a figure that no decision of the owner covers | The assistant puts it on the list for the owner. |
| A new design, a new figure type, a change of layout | The assistant puts it on the list for the owner. |

- Before the first fix, the assistant tags the commit that the owner reads now: `owner-review-2026-10-14`.
- A fix never changes an element ID, a figure number, a heading or a popup title. So the notes of the owner keep their places.
- Each fix gets one line in `academy/checks/changes.md`. The line gives the tab, the element ID, the finding and the source. It also gives the old text and the new text.
- A review agent checks each batch of fixes. It also checks that each fix is a clear error.
- A fix must not push a part over its word limit.
- If an item is possibly not a clear error, the assistant puts it on the list.

## The checks

Each check writes its result to `academy/checks/<ID>.md`. The list for the owner is `academy/checks/findings.md`.

Agents get the text of the pages as extracted files in the scratch folder, in slices. They do not get the HTML.

### A. Accuracy

| ID | Check | Who |
|---|---|---|
| A1 | Test each external link of both tabs. The links to the repository use the push of 14 October 2026. | Script |
| A2 | Compute each number of tab 2 again from its source, and compare. An agent lists the numbers and their sources in `mocks/`, `runs/`, `docs/` and `tests/`. | 1 agent, then script |
| A3 | Compare each fact that both tabs state. | 1 agent |
| A4 | Check each claim of parts 5.2, 2.2, 2.3, 4.3 and 4.6 against its source again. | 2 agents |

A2 does not read `marking/*.xlsx`.

### B. Learning

| ID | Check | Who |
|---|---|---|
| B1 | An agent reads the parts of one domain and answers the mock questions of that domain. A script scores the answers. | 5 agents, then script |
| B2 | For each part, name the wrong answer that tempts a candidate. Check if the page warns against it. | 2 agents |
| B3 | Explain each part back at each level: Overview, Explanation and Depth. | 3 agents |
| B4 | For each K and S point of the guide, judge if the page teaches it or only names it. | 2 agents |

B1 details:

- The agent gets two files only: the tab 1 text of its domain and the questions of its domain.
- The question file has the scenario story, the question, the options and the number to select. It has no point, no task statement and no answer.
- A script removes each question that a tab shows: by its ID, its question text or its option text.
- For each answer, the agent quotes the page sentence that supports it. A script checks that each quote is in the page.
- The score counts only the answers with a valid quote. This measures the page, not what the model already knows.
- A question with more than one correct answer scores only when the set matches exactly.
- The agent lists each file that it read.

### C. Reader types

| ID | Reader | Who |
|---|---|---|
| C1 | A beginner who never used the Claude API or Claude Code | 1 agent |
| C2 | A skimmer: the agent gets only the headings, the figures and the captions | 2 agents |
| C3 | A reader with English as a second language | 1 agent, and a script for sentence length |
| C4 | A phone reader, from pictures at 390 pixels | 1 agent |
| C5 | A sceptic of tab 2: does the tab convince, and does it show its weak points? | 1 agent |

### D. Figures and popups

| ID | Check | Who |
|---|---|---|
| D1 | The agent sees a figure without its captions and states its claim. A table gives the claim, the caption and the result: match, partial or miss. | 2 agents |
| D2 | List the boxes with no popup that raise a question. Check that each popup answers its question. | 2 agents |

For D1, `shot-figure.js` gets a mode that hides the caption and the step captions. The batch review agent checks the D1 table.

### E. Finding things

| ID | Check | Who |
|---|---|---|
| E1 | A script picks 20 points from `reference/guide-records.json` at random and records the seed. The agent finds where the page explains each point and reports its wrong turns. | 1 agent |
| E2 | Find each term that the page uses before it explains the term. | 1 agent |
| E3 | Find two names for one thing across both tabs. | Script |

E3 searches for three kinds of pairs. The first are the three names of the documentation (decision 0039, item 11). The second are spelling forms of one name, for example "subagent" and "sub-agent". The third are the pairs that the agents find.

### F. Layout and use

| ID | Check | Who |
|---|---|---|
| F1 | Check contrast and labels with axe-core in light and dark mode. Check keyboard order with a script that presses the Tab key. | Script |
| F2 | Take a picture of each figure at 390 pixels. C4 uses them. | Script |
| F3 | Measure the load time of each tab and find the large parts. | Script |

axe-core goes into the scratch folder, not into the repository. The known exceptions of decisions 0009 and 0013 are listed apart.

### G. Portal and records

| ID | Check | Who |
|---|---|---|
| G1 | Read `~/magnetlab-academy` and list what the move of the tabs needs (decision 0017). Read only. | 1 agent |
| G2 | In `academy/popup-plan.md` and `HANDOFF.md`, say that 40 figures have new popups. With Fig. 1.1-1, 41 of 56 figures have popups. A script gives the counts. | The assistant |

## Order and time

1. An independent agent checked this plan before the owner saw it. The assistant fixed it.
2. The journal entry and its progress list start before the first check.
3. Scripts first: A1, E3, F1, F2, F3, G2.
4. Agents, in this order of priority: B1, A4, A2, A3, D2, C1, B2, B4, D1, C2, C3, C4, C5, B3, E1, E2, G1.
5. Fixes in batches. After each batch, `check-pages.js` runs, and a review agent checks the batch.
6. The report.

Agents: 29 for the checks, 1 for this plan, 1 for the report, and 1 for each batch of fixes. With about 4 batches, the total is about 35. At most 2 run at the same time, all Opus 5.5.

Time: 6 to 8 hours. A usage limit can add hours. If the time runs out, the order of priority above says which checks stay.

## When things go wrong

- An agent has no result after 45 minutes: stop it and run it again once. After a second failure, skip the check and name it in the report.
- A check fails after 3 rounds of fixes: stop, commit what works, and name it in the report.
- A usage limit pauses the work: continue from the progress list in `academy/journal.md`.
- After each check, update the progress list. After a compaction, read it again.

## Limits

- No new design. No change to a decision text that the owner confirmed.
- No model call through the API, and no API cost. Only the agents of Claude Code.
- No change to the mocks or the mock builder: `mocks/`, `runs/`, `src/`, `tests/`, `docs/` and `marking/`. The checks only read them.
- No change to `reference/`, the old folders, the study packs or the portal folders.
- No personal file of the owner and no conversation transcript, also not in a prompt (rules 19 and 28).
- At most 2 agents at the same time.
- Commit after each check and after each batch of fixes.
- Never end a turn with a question to the owner. If a check cannot continue, record why. Then start the next check.
- Text in Simplified Technical English. No semicolons, no em dashes.

## The report

1. `academy/checks/findings.md` gives the list for the owner, sorted by part, with the most important items first.
2. `HANDOFF.md` and `academy/journal.md` get the result: the checks done and skipped, the fixes, and the B1 scores for each domain.
3. Academy decision 0041 records the owner's yes to this plan.
4. A new agent checks the report against the commits. The assistant fixes what it finds.
5. Final commit and push. `git status` is clean.

## Done when

The report is checked, `check-pages.js` prints "All checks passed." for both tabs, and GitHub has the last commit.
