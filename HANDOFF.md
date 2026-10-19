# Handoff: start here

Date: 5 October 2026. Updated on 9 October 2026, and on 13 and 14 October 2026 for the academy work. This file gives a new session what it needs to continue.

## The academy work (from 12 October 2026)

From 12 October 2026 the sessions build the teaching pages of the portal: "Exam guide breakdown" and "Behind the mocks". This work has its own records in `academy/` (academy decision 0007): `academy/README.md`, `academy/brief.md`, `academy/journal.md` and `academy/decisions/`. For this work, the records of the checklist in `CLAUDE.md` are the files in `academy/`, not `docs/journal.md` and `docs/decisions/`.

### State on 19 October 2026: the mocks of version 2 and the two tabs are live in the portal (academy decisions 0050 to 0057)

- The owner decided how the mocks of version 2, tab 1 and tab 2 go into the portal (`~/magnetlab-academy`, a private repository). The decisions are 0050 to 0057. `academy/` stays in this public repository. The portal gets a converted copy of the mocks and a copy of the built pages.
- Done here: the page build reads each file at a tag from GitHub, and all page links that pointed to `main` point to the tag `pages-v1` (decision 0054). `check-pages.js` checks each card's quote on its linked line at the tag. Both pages: "All checks passed.", reading from GitHub. `main` and `pages-v1` are on GitHub.
- The start note and the draft plan section for the portal: `academy/portal-plan.md`. An independent agent reviewed it, and its 15 points are fixed.
- The plan PR (#30) and PR 4 (the mocks of version 2, #31 to `staging` and #32 to `main`) are merged in the portal. The owner checked staging and production. The mocks of version 2 are live.
- The portal form of the two pages is built in `academy/pages/portal/` and checked (`academy/portal-plan.md`, "The portal form as built"). The tag `pages-v2` (commit ddbaf96) is on GitHub.
- PR 5 (the two pages) is live in the portal: #33 to `staging` and #34 to `main` (merge commit 4759b23). The owner checked staging and production. The 19 copied files in the portal are the same as the tag `pages-v2`.
- `pages-v3` (494a82e, on GitHub, decision 0058): the two highlight sentences have a faint tint, and the scroll to a part is fixed. The portal session found that the portal's `stop.open(id)` right after `start()` stopped the late scroll after the fonts load, so the portal did not take `pages-v3`. `pages-v4` (bdf7882) fixes this, and the checks now make the portal's call and load the fonts 2 seconds late. `pages-v4` is live in the portal (#35 and #36, checked by the owner on staging and production). The portal's CI now checks the landing on a part for each new tag.
- Next step: none is open. For a future update of the pages: keep the form, check, make a new tag, push it with the yes of the owner, and give the owner the tag name for the portal session.
- Done in `pages-v3`, kept for the record: `academy/build/academy.js` scrolls to the `#hash` only at the end of `academyStart()`, after it hides the rows and panels above the target. Today the portal calls `stop.open(id)` after `start()` to fix this, so nothing is broken. The fix needs a new tag `pages-v3` and a new copy into the portal.
- The portal session's handoff (19 October 2026): to take a new version, the owner gives the portal session the tag, and it runs `node scripts/copy-academy-pages.mjs <tag>` in `frontend/`. The script stops if a copied file changed in the portal, so all changes to the pages happen here. Keep the form: the file names, `export { academyStart as start }`, `export default data`, `stop()` and `stop.open(id)`, the class `academy-page ap-<tab>`, links as `/<tab>#id`, and images under `/academy/`. If the form changes, write down what changes for the portal session.
- Also for the next update, an open design item for the owner: on tab 1, part 1.1, the two sentences `<b class="ve-ref">` ("tool_use" and "end_turn") have the dotted underline of a card, so a reader expects a popup. They only light up a part of the figure. They are the only 2 on both pages.

- State on 13 October 2026: the plan is decided and confirmed in academy decisions 0001 to 0033. An independent review of the plan found 24 items, and all are decided or fixed. An independent agent checked the texts of 0016 to 0033 (working rule 35).

### State on 15 October 2026, evening: tab 2 version 3 (academy decision 0046, branch `behind-mocks-v3`)

- A fork of the main session works in the worktree `.claude/worktrees/behind-mocks-v3`, on the branch `behind-mocks-v3`. The main branch does not have this work yet.
- The owner and the assistant set the purpose of tab 2: first teach, then show leaders a careful design, then trust. Version 3 (`academy/pages/behind-the-mocks-v3.html`) adds a story under the paragraph of the owner: how we settled what is true (Fig. S), and what we chose to use (three choices and Fig. M, the map of the 30 task statements from `academy/facts/task-statement-use.json`).
- Tab 2 (`academy/pages/behind-the-mocks.html`, built by `academy/build/make-behind-the-mocks.py`) tells one story in 5 sections: the truth, the tools, the 9 steps, the build in Claude Code, and what we can claim, with jump links at the top. Each step and each Claude Code part shows an approved principle, an Overview with three beats (the risk, what we built, the result, decision 0049), and an Explanation that ends with "What this teaches for the exam" from the build guide tables. Independent agents checked each new sentence against its card. The old versions are `behind-the-mocks-v1-old.html` to `-v3-old` (decision 0047). Merged and pushed on 16 October 2026 (fafddcd).
- Next step: the owner reads tab 2 from top to bottom and writes notes. After that, the long-term goal of decision 0046, item 13: a tab that collects the differences between the guide and the products. Working rule 37: show the old and the new text before a text change, unless the owner says otherwise for a task. Left for later: the schema of the request to Claude, a chip for sentences with a code card, and the removal of the worktree `.claude/worktrees/behind-mocks-v3`.

### State on 14 October 2026, night: the exam box (academy decision 0042)

- The owner finds `academy/checks/findings.md` too long to read. The assistant brings its items one at a time, with one recommendation each. Item 1 is done: where a product fact could lead to a different exam answer, a box on tab 1 gives "For the exam" and "The product today", and the detail moved to a list in the Depth. 23 boxes in 15 parts.
- Decision 0043: the owner answered the other items of the short list, and all are built and reviewed: the Guide only popup, the primer before domain 1, phone drawings for 7 figures, the tab 2 section "What this shows and what it does not", the 45 popup items of check D2, role="group" on drawings with popups, facts moved between levels, and the long sentences split (151 to 34, the rest are false hits). `check-pages.js` prints "All checks passed." for both tabs.
- After decision 0043 (15 October 2026, morning): the dots of a fact show only under the pointer, the glossary is a side panel, the source lists are closed (decision 0044), marks of the owner next to four headings, and popups on the 10 boxes of Fig. A (switch FIG_A_POPUPS). The real cause of the dense paragraphs, text written as a chain of sourced facts, is not changed.
- Next step: the owner checks both tabs by hand and writes notes, on the version with the tag `owner-review-2026-10-15`. Then the assistant sorts the notes into fixes and new design decisions, one question at a time.

### State on 14 October 2026, evening: the reader checks (academy decision 0041)

- The owner chose to write notes on both tabs in one pass, on another day. Meanwhile the assistant ran the 23 checks of `academy/check-plan.md` alone, under `/goal`. Each check has its result in `academy/checks/<ID>.md`.
- The list for the owner is `academy/checks/findings.md`. Its main points: the facts hold (822 URLs: 819 links, 0 broken, and 3 URLs in code examples. 246 numbers of tab 2. A second fact check of the 5 hardest parts). Agents that read only the page answered 293 mock questions, all correct with a quote of the page, and 4 answers used the agent's own knowledge. B1 by domain: 78 of 78, 55 of 55, 60 of 60, 55 of 55, 45 of 45. The main weakness: in about 22 places the page states a product fact that goes against a guide point, and no line says which answer the exam expects. A beginner of domain 1 needs a primer and a glossary. On a phone, the sideways scroll hides the point of about 25 of 67 figure pictures. Tab 2 convinces about the process, less about the quality of the questions.
- The fixes: 41 lines in `academy/checks/changes.md`: clear errors, 3 fixes that add a reading or a fact (named in the log, the owner can take them back), 1 moved link and the check tools. They go from facts in 2.2, 2.3, 4.3, 4.6, 5.2 and 5.5 to four drawing faults (Fig. A, 0-1, 5-2, 6-1). No fix changed an element ID, a figure number, a heading or a popup title. The tag `owner-review-2026-10-14` (d938b71) marks the version that the owner reads, so the owner's notes keep their places. A review agent checked all fixes and found 7 problems, 1 high (a reused card ID). All are fixed, and the build now stops on two different cards with one ID.
- The tools of the checks are in `academy/checks/tools/`. `academy/build/check-pages.js` prints "All checks passed." for both tabs.
- The owner's yes to the plan covered one push at the end. `main` is pushed to GitHub after this report.
- G1 surveyed the portal for the move (decision 0017): three ways, and 7 decisions for the owner first (`academy/checks/G1.md`).
- Next step: the owner writes notes on both tabs, reads `academy/checks/findings.md`, and says which items to take. Then the assistant sorts the notes into fixes and new design decisions (one question at a time).

### State on 14 October 2026, morning: the answers to the morning report

- The owner answered all items of the morning report below, one question at a time. The 27 answers are in academy decision 0039. Academy decision 0040 corrects its item 12: section 17 is the appendix of the guide.
- Accepted: academy decisions 0035 and 0036, mock decision 0080 (merged into `main`, bec0418; the branch `fix-owner-reason` and its worktree are deleted). New: academy decisions 0037 (the figures are made again with the plugin), 0038 (a single name can appear in the running text), and mock decisions 0081 (ruling 2), 0082 (no path to build the files again) and 0083 (no more mocks for now).
- Done after the answers: the records, the paths without the user name, the build guide (step 2 line 45, step 6 table with 1.6-K2, step 8, the section of mock decision 0026), diagram 08, and the text fixes of both tabs. `check-pages.js` prints "All checks passed." The tests print "Ran 234 tests" and "OK".
- An independent check found that step 6 uses 1.6-K2 but not 5.2-K3. So only 1.6-K2 is in the step 6 table, and tab 2 shows no 5.2 chip on step 6.
- The figure plan of academy decision 0037 is built (14 October 2026, afternoon): 27 redraws and 9 additions, with steppers, small multiples, before/after, one live figure (3.3-1), moving dots on six figures, and growing bars. The text changes of decision 0039 are done too: the label "Guide only", the three names of the documentation, the code popup of part 1.2, and the takeaway in each closed heading of tab 2. Each domain and tab 2 had a review agent. Their items are fixed, except the few that the academy journal names as not changed. `check-pages.js` checks each step, panel and choice, and prints "All checks passed." for both tabs.
- Pictures for the owner: `academy/screenshots/tab-1-redraw/before-after-1.N.png` (domain 1) and `academy/screenshots/redraw/before-after-*.png` (the rest), dark mode in `academy/screenshots/redraw/dark/`. All were taken again after the last fixes.
- `main` was pushed to GitHub at 7b47e4d. The later commits are local.
- The missing reviews of decision 0036 are done: the top of tab 1, part 1.1, and the reader agent of decision 0026 for slices 5 to 8. Their items are fixed, except the few that the academy journal names as not changed.
- The popup plan (`academy/popup-plan.md`, accepted) is built: 95 new popups on the boxes of 40 figures (with the 6 earlier popups of Fig. 1.1-1, 41 of 56 figures have popups), from `academy/build/popups.py`, reviewed and fixed.
- Next step: the owner looks at the pages, says yes to a push (main is ahead of GitHub), and accepts slices 2 to 8 or names what to change (decision 0022).

### Morning report, night of 14 October 2026 (`academy/night-plan.md`)

Status of this report: answered by the owner on 14 October 2026 (academy decision 0039). The final version. An independent agent checked it against the commits at about 07:38 and found 8 problems. A second agent checked the fixes and decision 0036 and found 7 problems. A third agent checked the final version and found 5 problems, none high. All 20 are fixed. A fourth agent checked those last fixes and found no problems (see the journal).

**In short:** tab 1 is complete: all 30 task statements are written, reviewed and fixed (part 1.1 was reviewed before the night, see decision 0036). Tab 2 has slices 2 and 3. All work is in local commits on `main` and on the branch `fix-owner-reason`, from 1cbae17 to the commit of this report. Nothing is pushed. The work paused from about 03:50 to 06:30, probably at a usage limit, and then continued.

**Done on `main`, tab 2 "Behind the mocks"** (slices 2 and 3):

- Slice 2: steps 0 to 4 and 6 to 8 of tab 2 are written. Each step had a fact agent, a review agent and one round of fixes. Then a whole-picture agent (30 items, 26 fixed) and a reader agent. The reader's summaries agree with the intended takeaways of all 8 steps.
- Each closed heading of a step names its task statements (night plan choice, 1cbae17).
- Slice 3: the build in Claude Code, with 4 parts: 3.1, 1.7, 4.6 (with Fig. C-4.6-1, the three document checks) and 3.4 (no example). One review, one whole-picture agent (18 items, all fixed) and one reader agent (summaries agree with the takeaways of all 4 parts).
- The check `check-pages.js` prints "All checks passed." No part is over its word limit. The links to tab 1 now resolve, because tab 1 is built.
- Dated copies of 6 documentation pages are in `academy/sources/` (decision 0030).
- Screenshots to look at: `academy/screenshots/slice-2/` (steps 0 to 4 and 6 to 8) and `academy/screenshots/slice-3/`, in light and dark, at 1280 and 390 pixels. They are from 02:03. Tab 2 changed after that, for example the name Fig. C-4.6-1.

**Done on `main`, tab 1 "Exam guide breakdown"** (slices 4 to 8, the owner's words of 02:06: "Do as many slices as you can. Go all the way"):

- The script `academy/build/make-exam-guide-breakdown.py` writes `academy/pages/exam-guide-breakdown.html`. The top has the map of the guide (Fig. A, the domains and their task statements, and Fig. B, the scenarios) and "How we broke it down". Each domain has a summary.
- Each of the 30 parts has the three levels, one figure (part 1.1 has three), its K and S points, "The exam tests" with the count of mock questions, "Beyond the exam" and the links to tab 2. 28 parts have a code popup. Part 1.1 takes the checked content of the fifth sample, with its code in one popup of its figure. Part 1.2 has no code popup (item 16).
- A fact agent wrote a fact sheet for each part except 1.1, 29 in all (`academy/facts/ts-N-M.md`), with its conflicts and what it did not find. The night added 66 dated copies of documentation pages to `academy/sources/`.
- Review agents checked the parts, in most cases two parts for each agent. They found 245 items, and all are fixed. Most were cards that held only a near claim, facts without their product or condition, and claims of the guide that the page did not mark as the guide's.
- Whole-picture agents found 14 items (the top and domain 1, all fixed except one, which is item 8 below) and 17 items (domains 2 and 3, all fixed). A third one found 13 items (domains 4 and 5). Nine are fixed. Three are in items 9, 10 and 12. The assistant checked the last one (step 4 and its verdict) and found the two tabs consistent.
- Reader agents: their one-sentence summaries agree with the intended takeaways of all 30 parts (`academy/facts/takeaways-slice-4.md` and `takeaways-slices-5-to-8.md`). The unclear sentences that they found are fixed.
- The check `check-pages.js` prints "All checks passed." for both tabs. No part is over its word limit.
- Screenshots of the 30 figures: `academy/screenshots/tab-1/`.

**Choices of the night for tab 1 (working rule 36):** academy decision 0036 (proposed) records them. One review agent checks two parts, except part 3.6, which had its own, and part 1.1, which had no review agent at night. One whole-picture agent checks slices 5 and 6, and one checks slices 7 and 8. One reader agent reads slices 5 to 8, and it does not follow all of the method of decision 0026. The top of tab 1 has no fact agent and no review agent. These choices change how decisions 0012, 0015 and 0026 apply.

**Done on the branch `fix-owner-reason`** (worktree `../ccar-f-fix-owner-reason`, commits 46ed3fd and bd63ff7, not merged):

- In `src/control.py`, each try of a new start now gets the parts of the owner: the owner's reason, and after a rewrite also the step 6 finding and the other questions. Before, only the first try got them.
- 6 new tests. The test run prints "Ran 234 tests" and "OK". No test makes a model call. A replay with no model call shows that M5-S38-T5 now gets the rules B9 and owner. Before, it got only B9.
- The build guide step 5, diagram 07 and `docs/journal.md` are updated on the branch. An independent review found no bug.
- Mock decision number 0080 is used on the branch only.
- A known limit: the owner's reason now sits next to the latest failed try, not next to the question that the owner judged. A letter in the reason can point to the wrong option.
- If the owner merges: tab 2 step 5 says "The code still works this way." That sentence must change.

**Decisions of the night:**

- Academy decision 0034 (step 7 is named "The questions are marked" on tab 2) is now accepted. The owner accepted it before the night, and an agent checked its text (working rule 35).

**Decisions that the assistant chose at night (working rule 36):**

- Mock decision 0080: each try of a new start gets the parts of the owner (the fix above). The owner chooses whether to merge.
- Academy decision 0036: the reviews of tab 1 at night (see above).
- Academy decision 0035: tab 2 leaves out the entries of 3.2 (skills) and 2.5 (built-in tools), which decision 0023 named. For 2.5, no record says which tool did what. For 3.2, no record shows that the build used the two named skills, and they are outside the repository. The assistant recommends no 3.2 entry.

**Waiting for the owner:**

1. The reader agent of slice 2 proposes the takeaway in each closed heading. This is a new design.
2. The Depth label "what went wrong, and the fix" does not fit parts 1.7, 4.6 and 3.4 of slice 3, which show no fix of the process.
3. Slice 3 does not explain project words such as "the owner", "slice" and rule numbers inside the section.
4. Whole-picture items of slice 2 that are not fixed: the "Beyond the exam" label on two small product facts, "today" on the rule counts, one cross-reference, and the scheme of the popup IDs.
5. Found in the records of the mock builder, not changed at night:
   - The build guide, step 2 line 45, says "The current models accept only auto and none". The documentation says that four models return a 400 error for any and tool: Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1. Tab 2 corrects it in a popup.
   - Two cases apply ruling 2 in two ways on point 4.1-S3: M1-S49-T1 option D counted (rewrite D008), M5-S40-T1 option B did not (mock decision 0077).
   - No record names who filled the 20 good marks of round 1 of mock 4.
   - `runs/mock-0N/build.json` holds absolute paths with the user name. The repository becomes public.
   - The build guide and mock decision 0016 say that code builds the files again after a change. The code has no such path.
6. The commit message of f62b523 says that the links of 3.2 and 2.5 "do not hold". For 3.2 that is too strong. The journal and decision 0035 have the correct reason.
7. The open question from before: will more mocks be built?
8. Tab 1: API names such as updatedToolOutput, allowed_tools and --fork-session are in the running text. Decision 0032 does not say whether a name counts as code.
9. Tab 1: the sentence "The exam uses the guide" comes often (9 times in domain 1 alone). The idea "only the guide says this" has six different forms. The reader agent of slice 4 found that this slows the reading. The assistant suggests one fixed sentence.
10. Tab 1 says "the documentation", "the Claude API documentation" and "the Claude Code documentation". Tab 2 and the source lists say "Anthropic documentation". One name for each set of pages is needed in both tabs.
11. Points of the reader agent of slices 5 to 8:
    - The notes about the mock builder (step numbers, rule D3, call 4a) mean little to a candidate.
    - The page never explains "section 17" of the guide.
    - Fig. 5.6-1 is busy.
    - Fig. 2.1-1 mixes the rename example and the split example.
    - Fig. 5.2-1 shows "Several matches?" in the chain of escalation checks, but it is not an escalation.
12. Tab 2:
    - The chips of steps 2, 4, 5 and 6 show 4.3-S3 under the heading "How step N uses each point", but the text of 4.3-S3 says "This build does not use it". Tab 1 now says "names but does not use 4.3-S3".
    - Step 6 has no chip for 5.2, but rule D3 rests on 5.2-K3.
    - Three chip IDs of step 5 (`step-5-ts-44`, `step-5-ts-43`, `step-5-ts-11`) break the pattern `step-N-ts-X-Y`.
13. The links of the cards to files in `academy/` (sources, facts, decisions) point to `blob/main/...` on GitHub. They fail until a push.
14. Records of the mock builder, found by the fact agents of tab 1. None was changed at night:
    - Some diagrams and mock decisions name guide points that the tables of the build guide do not have. For example, diagram 08 cites 5.2-K3, and mock decision 0014 and diagram 01 cite 1.6-K2, but the step 6 table has neither. Also, mock decision 0040 (line 6) says that the diagrams of steps 2, 4 and 6 show the deviation, but diagram 08 does not. Tab 1 links only by the tables (academy decision 0024). The fact sheets in `academy/facts/` list each case under their conflicts.
    - Mock decision 0026 asks for a build guide section on why the mock builder uses no MCP, subagents, hooks or sessions. That section does not exist.
    - Mock decision 0001 links the decision files and the journal to 5.4. Academy decision 0023 links the same files to 1.7.
    - Step 6 stops the whole run when rule C2 fails. 5.3-K4 calls this an anti-pattern, but the stop names its cause and no retry can repair it. Should the Depth of 5.3 say so?
15. Part 5.6: the Claude API returns an error when citations and `output_config.format` are in one request. This academy did not check whether citations work with a forced tool call.
16. Part 1.2 has no code popup. Its fact sheet proposed the same code that part 1.3 shows, or a text popup. The assistant used neither for 1.2.

- Next step: the owner reads this report, decides items 1 to 16, decisions 0035 and 0036 and the merge of the fix, and accepts slices 2 to 8 or names what to change (decision 0022).

From 7 October 2026 the work continues in Claude Code. The owner moves this folder out of OneDrive, to a folder in WSL with a private repository on GitHub. The folder in OneDrive is then old.

## Words

| Word | Meaning |
|---|---|
| The owner | The person who directs this work. The owner passed the CCAR-F exam. |
| CCAR-F | The exam "Claude Certified Architect – Foundations" |
| Mock | A practice exam paper. "Mock" and "paper" are the same thing. |
| The portal | MagnetLab Academy, a learning site for people who prepare for the exam. A separate project builds it. |
| Participant | A person who uses the portal |
| The first build | Two things together: an assistant made five mocks in August 2026 in a chat session, and a review repaired them in September 2026 |
| `CCAR-F Mocks v2` | A second attempt, of 2 October 2026. It made decisions and records. It made no mocks. |
| Cowork | The Claude desktop product that the discussions ran in until 7 October 2026 |
| Claude Code | The Anthropic product that writes the program, from 7 October 2026 (decisions 0002 and 0038). It reads `CLAUDE.md` at the start of each session. |
| The control | The part of the program that decides what happens next to a slot or to a mock: the loop, the limits, the statuses and the decisions of the owner |
| Session | One chat with the assistant |
| The exam guide, or "the guide" | The official guide of the CCAR-F exam, `reference/exam-guide.md` |
| The build guide | "How the Mocks Are Built": the pages in `docs/build-guide/` that show participants how the program makes the mocks |

## The goal

1. Build a program that writes and checks mocks for the CCAR-F exam. The portal will launch with these mocks.
2. Document the build during the work: each decision, each diagram and each run. Later a portal page will show participants how the program makes the mocks, as a worked example of the exam guide.

## The build guide "How the Mocks Are Built"

The build guide is a product of this work. It has the same weight as the program. It is the portal page of goal 2.

- **Source.** The Reason section of each decision. Each Reason stands on the exam guide. The build guide does not use the section "How we decided", and it does not tell the history of the first build.
- **Structure.** One section for each pipeline step. Each section has a short explanation, one diagram, and a table of the exam guide points that the step uses. The sections are files in `docs/build-guide/`, one file for each pipeline step.
- **Status.** Each section has the status "planned" or "built". A section becomes "built" only when a run record shows the step.

All 9 sections exist, for steps 0 to 8. The diagrams 02 to 10 in `docs/diagrams/` are the diagrams of steps 0 to 8. Diagrams 11 (repeats across mocks) and 12 (the scenarios of the 5 mocks) show the rules across mocks. Rule 18 still applies to the portal page "How the Mocks Are Built New".

## Read these files first, in this sequence

1. `WORKING-RULES.md`: how the assistant works here. Part A has the rules of the owner. Part B has rules that the assistant suggested. The owner confirmed Part B on 6 October 2026. Part C has rules 30 to 33: the changes after 6 October 2026.
2. `README.md`: what is in this folder.
3. `docs/journal.md`: the top entry.
4. `docs/decisions/`: decisions 0001 to 0079. Read decision 0038 before the step files: it changes the control. Read 0039 after 0038: it describes the control code. Read 0019 together with 0003 to 0018. Decisions 0027 to 0036 are the design of steps 0 to 8 and the rules for a good question. Decision 0037 has the answers to the 14 serious items of the first review. Read them completely.
5. `docs/diagrams/01-pipeline-overview.html`: the nine steps on one page. Then diagrams 02 to 10, one for each of the steps 0 to 8, and diagrams 11 and 12 for the rules across mocks. Diagrams 09 to 12 have the visual form that the owner wants.

Read these only when you need them:

- `reference/guide-records.json`: the records of the exam guide for code. Step 0 made it on 6 October 2026. It is the one source of guide text for code and for scripts.
- `reference/exam-guide.md`: the exam guide. Section 3 has the exam details. Section 5 has the 6 scenarios. Section 6 has the 30 task statements. Section 9 has 12 sample questions.
- `reference/task-statements-and-points.md`: the 30 task statements and their 240 points, with IDs. It is the file for people.
- `docs/reviews/`: the reports of the independent reviewers. `review-decisions-0024-to-0037.md` is necessary for the next step. `review-decisions-0026-to-0036.md` is the first review of the step files.
- `reference/practice-audit-first-build.md`: History of the first build. Not a source for the design.

## Where we are

State on 9 October 2026.

- **All 5 mocks are built** in `mocks/`: `mock-0N.questions.json` and `mock-0N.answers.json`. The git tag `mocks-v2` marks this set (decision 0079). It is version 2, because the portal already has a version 1. The cost of the runs: mock 1 $17.17, mock 2 $20.73, mock 3 $23.85, mock 4 $12.83, mock 5 $11.68 (plus under $1 of a stopped run, decision 0073).
- **Decisions 0001 to 0079** record the design and each change. The owner confirmed the texts of 0001 to 0079. Decision 0078 corrects lines of the confirmed decisions 0045, 0046, 0047, 0049, 0051, 0058, 0059, 0061, 0064, 0068, 0069 and 0071.
- **The marks.** The owner read and marked mocks 1 to 3. For mock 4 the owner did not read the questions. The second review in Cowork, a Claude model, marked mocks 4 and 5 (decisions 0069, 0071 and 0073). So no person read the questions of mocks 4 and 5.
- **The rules across mocks.** Point groups (decisions 0047, 0048), the spread of ideas (0050), no repeat of an earlier question with rule B9 (0056, stricter in 0066), the narrow list of 63 of 95 ideas that keep the copy rule (0066, 0068, 0072, 0075), the fixed scenarios of mocks 3 to 5 (0057), and no copy across mocks (0060).
- **Other rules since mock 1:** rule A12 on the longest option (0053), two-answer points (0054), rule B8 against copies of the sample questions (0055), rule C3 over the whole mock (0052), prompt caching (0067), balanced correct letters from mock 5 (0070), the reason of the owner after more tries (0074).
- **Known limits** of each mock: decisions 0046 (mock 1), 0058 and 0059 (mock 2), 0063 (mock 3), 0069 (mock 4), 0076 and 0077 (mock 5). Mock 5 is a review mock: 46 of its 60 questions are close to an earlier mock.
- **The program:** `src/` with 228 tests in `tests/`. The command line is `src/run.py`. No test makes a model call.

| Step | Decisions | Diagram | State |
|---|---|---|---|
| 0. Prepare the guide records | 0017, 0028 | 03 | Ran on 6 October 2026. `reference/guide-records.json` exists. |
| 1. Plan the mock | 0027, 0047, 0048, 0050, 0053, 0054, 0056, 0057, 0070 | 02, 11, 12 | Built, ran for mocks 1 to 5 |
| 2. Write the question | 0029, 0053 to 0056, 0066, 0067, 0068, 0070, 0072, 0075 | 04 | Built, ran for mocks 1 to 5 |
| The rules for a good question (21 rules: A1 to A12, B1 to B9) | 0030, 0043, 0053, 0055, 0056, 0066 | 05, 06 | Decided |
| 3. Check by code | 0031, 0053 | 05 | Built, ran for mocks 1 to 5 |
| 4. Check by a model | 0032, 0055, 0056, 0061, 0066, 0067, 0068, 0072, 0075 | 06 | Built, ran for mocks 1 to 5 |
| 5. Try again | 0033, 0045, 0074 | 07 | Built, ran for mocks 1 to 5 |
| 6. Check the complete mock | 0034, 0052, 0059, 0064, 0069, 0077 | 08 | Built, ran for mocks 1 to 5 |
| 7. Mark the questions | 0035, 0071, 0073 | 09 | Built, ran for mocks 1 to 5 |
| 8. Build the files | 0036, 0039 | 10 | Built mocks 1 to 5 |

### How the owner wants the work (from the second session of 6 October)

- Short answers in the chat. Do not overload the owner. Write in Simplified Technical English.
- For the design of a step: one proposal with all details, with the exact file format and the exact fields. If the owner does not understand the proposal, tell it as the story of one question.
- Do not hand the owner a design that is not specific. The owner asked: where does this text come from, which file, which fields?
- A diagram of a step shows what a reader must understand, not a list of what the code does. It has hover popups with a real example from the files. It has no element that is not necessary. A script makes each one: `docs/diagrams/NN-make-diagram.py`.
- A diagram shows the thing itself, not a box with its name. Examples: a question card with options, a sheet with rows and the columns that the owner fills, 60 squares for the size of a sample, a bar with zones for a limit. The owner said "the visuals could be better" for diagrams 02 to 08, and "much better" for diagram 09. Diagrams 09 and 10 have this form. The owner said that the older diagrams do not have to be made again.
- Make the diagram of a step when its decision is made. Do not postpone it.
- From the third session of 6 October: make each explanation short, and tell it as the story of one question from the start. The owner asked for a more simple explanation of 4 of the 14 items. A table of fields is too much for the first explanation.
- The owner discussed the 14 items one at a time, with one question for each item. That worked well.
- Explain in plain words what code does. Do not show code to the owner if the owner did not ask for it.

## What a finished mock is

Decision 0003: a mock has the same form as the exam. These are the facts from the exam guide (Sections 3, 4 and 5):

- 60 questions and 120 minutes.
- 4 scenarios, from the 6 scenarios of the guide.
- Multiple-choice and multiple-response questions. Each question says how many answers to select.
- The approximate domain weights 27%, 18%, 20%, 20% and 15%.

Also decided:

- The program writes each question new. The build never reads the old questions (decision 0004).
- The two owner rulings of 29 September 2026 apply. Ruling 1 is in decisions 0005 and 0007. Ruling 2 is in decision 0006.
- The exam guide is the only source of facts in the first version (decision 0008).
- The numbers of one mock (decision 0027): 16, 11, 12, 12 and 9 questions for the 5 domains. 15 questions for each scenario. At least 1 question for each of the 30 task statements. 52 multiple-choice and 8 multiple-response questions, 2 in each scenario.
- The program selects the 4 scenarios at random, from 11 of the 15 possible sets (decision 0027). The owner fixed the sets of mocks 3 to 5 (decision 0057).
- A finished mock is two JSON files: the questions, and the answers with the reasons (decision 0036). The format that the portal reads is not known. A converter comes later.
- A multiple-choice question has 4 options and 1 correct answer. A multiple-response question has 5 options and 2 correct answers (decision 0029). The number 8 and the form "5 options, 2 correct" are guesses with no source.

Decided later:

- The program makes 5 mocks (decision 0049). Their scenarios (0057) and the rules against repeats (0056, 0060, 0066) are decided.

Not decided:

- If a later version can use other sources than the exam guide (decision 0008 covers the first version only).

## The next steps

1. A converter from the two files of each mock to the format of the portal, when that format is known (decision 0036). The notes for the portal are in `docs/portal-notes.md`.
2. The workbook `docs/coverage/task-statement-decisions.xlsx`: its three yellow columns are still empty (decision 0018).

### History: the 10 serious items of the second review, after decision 0038

| # | Item | Result |
|---|---|---|
| 1 | Rule A11 has three different texts. | Closed by decision 0038, part 8. Decisions 0030 and 0031 do not have the new text yet. |
| 2 | A slot that goes back keeps the status `passed`. | Closed by decision 0038, part 9 |
| 3 | Step 6 asks the owner before the marking. | Removed. Step 6 sends no question back, and the owner sees its findings after the marking. |
| 4 | After `ignore`, the scenario cannot pass step 6. | Closed. The owner accepts the mock with a command. |
| 5 | The count of the runs of step 6 | Removed. The owner starts each round. |
| 6 | The values of `state` have no meaning. `id` in `owner-decisions.json` has no definition, and a finding of step 6 has no ID. | Closed by decision 0039. |
| 7 | `new_point` has no place to store the new point. No file says if `plan.json` changes, or how the new point stays different from the points of the other slots. | Closed by decision 0039. |
| 8 | After `more_tries` or `new_point`, no file says if the next call is a request of step 2 or of step 5, or which failed try it shows. | Closed by decision 0039. |
| 9 | A call that fails 3 times leaves no record. So the report has no source for `errors` after a new start. | Closed by decision 0039. |
| 10 | The exact conditions before step 8 builds the files | Closed by decision 0039. |

For each new reason:

- Take each exam guide text from `reference/guide-records.json` with a script. Do not type it.
- The guide wrote many points for a different context, for example code review or data extraction. When a reason uses such a point, say the context in the same file. The second review found 11 uses where a file does not do that.
- Do not say that a design is complete before a reviewer has checked it.
- When you make one file more exact, make each file that has the same rule agree. Rule A11 is the example.

In the workbook, the owner completes the three yellow columns. The assistant can write agreed notes there after a discussion. The column "Suggested decision" is a first suggestion from the audit. It is not a decision, and it is not a source for the design.

## Things that are open

| Open item | Note |
|---|---|
| The format of the portal | Not known. Step 8 writes our own two files. A converter comes later (decision 0036). `docs/portal-notes.md` has the notes for it. |
| The copy of the exam guide | Compared with the official PDF on 13 October 2026, word for word: 0 differences (academy decision 0027). |
| A repeat with different words | Rule B9 is a judgment of a model. It can fail a good question or pass a close one (decision 0066). |
| Rule A11 and words like "cannot" | Step 3 follows decision 0038, part 8. A change needs a new decision. |
| The Agent SDK | Decision 0002 names it. No step uses it. A new decision must say so. |
| The portal pages | "How the Mocks Are Built New" shows a design of 2 October. Rule 18 applies. Tab 2 of the academy work will replace it (academy decision 0018). |

## Where the old material is

You do not need it for the design. It is here if the owner asks. Each folder is in OneDrive, in `C:\Users\<the owner>\OneDrive\Desktop\Learning\CPN Learning pathway\CCAR-F\`. After the move to WSL they are not next to this folder. Rule 27 applies: do not change them.

| Folder | Content |
|---|---|
| `CCAR-F Mocks v2/` | The second attempt: an older decision file, and the record of the first build in `reference/first-build/` |
| `Mocks/` | The five mocks of August 2026 and the question bank |
| `CCAR-F Portal Mocks/` | The five mocks after the review of September 2026 |
| `CCAR-F Study Pack/` and the numbered files in `CCAR-F/` | Study files of the owner, and some records of the first build (files 06, 10 and 11). Many of them are personal. |

## What the owner says to start

"Read `HANDOFF.md` in `ccar-f-mock-generator` and follow it."
