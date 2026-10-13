# Night plan, 14 October 2026, 00:30 to 09:30

The owner sleeps for 8 to 9 hours. The assistant works alone under `/goal`, in auto mode. The owner's yes to this plan covers each step in it (working rules 32 and 33). The owner reads only the morning report.

## Step 1. Check this plan (first, before any other work)

1. A new agent reads this plan, academy decisions 0001 to 0034, `WORKING-RULES.md`, `CLAUDE.md`, `HANDOFF.md` and the state of slice 1. It lists gaps, conflicts with the decisions or rules, and risks.
2. The assistant checks each item. It fixes this plan where a fix needs no decision of the owner. It records each change in the journal.
3. If an item needs the owner, the assistant takes the safer choice (usually: do less) and puts the item in the morning report.

## Step 2. Slice 2: steps 0 to 4 and 6 to 8 of tab 2

The same process as slice 1 (academy decisions 0011, 0012, 0013, 0015, 0019, 0022, 0026, 0030, 0033):

1. For each step: a fact agent writes `academy/facts/step-N.md`. It gets the order of trust and working rules 19 and 28.
2. The assistant writes the part in `academy/build/make-behind-the-mocks.py`, from the fact sheet only. Each number and each excerpt comes from its file by script. A figure only where the step has a mechanism (decision 0010). Diagrams 02 to 10 of the mock builder give the content, drawn again (decision 0013).
3. A review agent for each part checks each sentence and each label against the sources. At most 2 review rounds for each part (decision 0022).
4. After all 8 steps: one whole-picture agent and one reader agent read tab 2 (decisions 0015 and 0026). The assistant writes the intended takeaways in `academy/facts/takeaways-slice-2.md` before the reader agent starts.
5. `node academy/build/check-pages.js behind-the-mocks.html` prints "All checks passed." Screenshots go to `academy/screenshots/slice-2/`.
6. Commit on `main` after each part and after each round of fixes.

At most 2 agents run at the same time.

## Step 3. Slice 3: the build in Claude Code

The 6 entries of decision 0023 (3.1, 1.7, 4.6, 3.2, 2.5, and 3.4 with no example), the story of the three document checks (decision 0031), with the same process as step 2. The fact agent checks each task statement link against the K and S points first (decision 0023). A link that does not hold is removed, and the morning report names it.

## Step 4. The mock builder fix, on a branch

On the branch `fix-owner-reason`, made from `main`. `main` does not get this change. The owner decides in the morning whether to merge.

1. The gap: after "more tries", a bad mark or a rewrite, the reason of the owner reaches only the first try of the new start (`src/control.py`, the branch `if in_round:` runs first). Fact sheet `academy/facts/step-5.md`, conflict C2.
2. The fix: each try of the new start gets the reason of the owner as a finding with the rule "owner".
3. Tests: a test for try 2 and try 3 of a new start after each of the three events. No test makes a model call (decision 0038, `CLAUDE.md`). All tests pass: `python3 -m unittest discover -s tests` prints "OK".
4. A new mock decision in `docs/decisions/` (number 0080), with status "proposed". Decision 0074 does not change (working rule 26). Its status line changes only if the owner merges.
5. The build guide step 5 and diagram 07 get the change on the branch only (`CLAUDE.md`, checklist item 4).
6. An independent agent reviews the change against the code and the tests.
7. The 5 built mocks and the files in `runs/` do not change. The program does not run. No API key is used.

## Limits for the whole night

- No push to GitHub. No merge of the branch. No deletion of work.
- No model call through the API and no API cost. Only the agents of Claude Code.
- No change to the mock builder's code on `main`, to `reference/`, to the old folders or to the study packs (working rules 16 and 27).
- No change to tab 1. No new design: a part follows slice 1. If a part needs a new kind of figure, the assistant draws it with the rules of decision 0013 and lists it in the morning report.
- No file of the owner's personal material (working rules 19 and 28).
- A decision that needs the owner: the assistant takes its recommendation, writes the decision file with the status "proposed, chosen by the assistant at night", and puts it in the morning report.
- Text in Simplified Technical English. No semicolons, no em dashes.

## Order and time

Step 1 (about 15 minutes), step 2 (about 4 to 6 hours), step 4 (about 1 to 2 hours, while the agents of step 2 run where possible), then step 3 (about 2 hours). If the time ends first, the assistant stops at the end of a part, commits, and writes the report.

## The morning report

At the end, `HANDOFF.md` (section "The academy work") gets the morning report, and `academy/journal.md` gets the night's entry. The report has:

1. What is done, with the commits.
2. The decisions that the assistant chose at night, each with its question and its choice.
3. The items that the agents found and that wait for the owner.
4. The result of the checks and of the tests.
5. The screenshots to look at.

## Done when

Slices 2 and 3 are built, reviewed and committed on `main`. `check-pages.js` prints "All checks passed.". The fix is committed on `fix-owner-reason`, and all tests pass there. `HANDOFF.md` has the morning report. `git status` is clean. Or the time is 09:30.
