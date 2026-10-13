# Night plan, 14 October 2026, 00:45 to 09:30

The owner sleeps for 8 to 9 hours. The assistant works alone under `/goal`, in auto mode, in Claude Code 2.1.296. The owner's yes to this plan covers each step in it (working rules 32, 33 and 36). The owner reads only the morning report.

An independent agent checked the first version of this plan and found 20 items. This version fixes them (see the journal).

## The rules for the night

- Working rule 36 (one night only) lets the assistant choose a design decision that needs the owner. It takes its recommendation, writes the decision file with the status "proposed, chosen by the assistant at night", and puts it in the morning report.
- Two choices are already made with the owner's yes to this plan:
  - Slice 2 copies the form of slice 1. Each closed heading of a step also names the task statements that the step uses, for example "Task statements 4.4, 1.1, 4.3" (the reader agent of slice 1 found that the headings do not show why a step matters). The assistant adds this to step 5 too.
  - The fix of step 4 gives each try of a new start all the parts that the first try gets: the owner's reason, the step 6 finding and the other questions not to repeat. Decision 0080 lists this as a choice for the owner.
- Never end a turn with a question to the owner or with "waiting". If a part cannot continue, record why, skip it, and start the next part.
- Each turn ends with the output of `date`.

## Step 1. Before the work (done before the owner sleeps)

1. An independent agent checked the first version of this plan. The assistant fixed it. Done.
2. Rule 36 is in `WORKING-RULES.md`. Done.

## Step 2. Slice 2: steps 0 to 4 and 6 to 8 of tab 2 (in the main folder, on `main`)

The same process as slice 1 (academy decisions 0011, 0012, 0013, 0015, 0019, 0022, 0026, 0030, 0033, 0034):

1. For each step: a fact agent writes `academy/facts/step-N.md`. It gets the order of trust and working rules 19 and 28.
2. The assistant writes the part in `academy/build/make-behind-the-mocks.py`, from the fact sheet only. Each number and each excerpt comes from its file by script. A figure only where the step has a mechanism (decision 0010). Diagrams 02 to 10 of the mock builder give the content, drawn again (decision 0013).
3. A review agent for each part checks each sentence and each label against the sources. At most 2 review rounds for each part (decision 0022).
4. After all 8 steps: the assistant writes the intended takeaways in `academy/facts/takeaways-slice-2.md`. Then one whole-picture agent and one reader agent read tab 2 (decisions 0015 and 0026). The whole-picture agent also checks the text of decision 0034.
5. The checks, with the full command:
   `NODE_PATH=<scratchpad>/pw/node_modules CHROME=$HOME/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell LD_LIBRARY_PATH=$HOME/.cache/ccar-chrome-libs node academy/build/check-pages.js behind-the-mocks.html`
   The result is "All checks passed.", or failures that are only word limits. A part over its word limit is not cut at night. It goes to the owner (decision 0026), and the morning report names it.
6. Screenshots: the assistant copies them to `academy/screenshots/slice-2/`.
7. Commit on `main` after each part and after each round of fixes.

## Step 3. The mock builder fix, in a separate folder

The fix lives in a separate worktree, so that the main folder never leaves `main` and the agents of step 2 never see the change:

    git worktree add ../ccar-f-fix-owner-reason -b fix-owner-reason main

All work of this step happens in `../ccar-f-fix-owner-reason`. The owner decides in the morning whether to merge.

1. The gap: after "more tries", a bad mark or a rewrite, the reason of the owner reaches only the first try of the new start. In `src/control.py`, `request_for`, the branch `if in_round:` returns before the event branches. Fact sheet `academy/facts/step-5.md`, conflict C2. An independent agent confirmed it.
2. The fix: each try of the new start gets the same parts as the first try: the owner's reason as a finding with the rule "owner", and after a rewrite also the step 6 finding and the other questions.
3. Tests: try 2 and try 3 of a new start, after each of the three events. No test makes a model call (decision 0038, `CLAUDE.md`). All tests pass: `python3 -B -m unittest discover -s tests` prints "OK".
4. A proof with no model call: the replay of fact sheet section 4.6 on a scratch copy of `runs/mock-05/`. The request for M5-S38-T5 must show the rules `['B9', 'owner']`.
5. Mock decision 0080 in `docs/decisions/`, status "proposed". It names decision 0074 (working rule 26). Decision 0074 does not change.
6. On the branch: build guide step 5 and diagram 07 get the change, and they keep the history: mocks 1 to 5 were built without this fix. `docs/journal.md` gets an entry (`CLAUDE.md`, checklist items 1 and 4).
7. An independent agent reviews the change against the code and the tests.
8. The 5 built mocks and the files in `runs/` do not change. The program does not run. No API key is used.

## Step 4. Slice 3: the build in Claude Code (optional, only if time is left)

The 6 entries of decision 0023 and the story of the three document checks (decision 0031), with the process of step 2. The fact agent checks each task statement link against the K and S points first (decision 0023). 3.4 has no example unless the fact agent finds that the build used the Explore subagent (decision 0023). For entry 3.2, the agents read only the two skills ste-writing and discussion-and-brainstorming in the owner's settings folder, and no other skill (working rules 19 and 28).

## When things go wrong

- An agent with no result after 45 minutes: stop it and run it again once. A second failure: skip the part and name it in the report.
- A check that still fails after 3 rounds of fixes: stop that part, commit what works, name it in the report.
- A review finds a high item that needs the owner: choose the safer way (usually: show less), and name it in the report.
- Long context: the journal entry of the night has a short progress list. The assistant updates and commits it after each part, and reads it again after a compaction or a pause.
- A usage limit pauses the goal. Claude Code continues when the limit resets. The work then continues from the progress list.

## Limits for the whole night

- No push to GitHub. No merge of the branch. No deletion of work.
- No model call through the API and no API cost. Only the agents of Claude Code.
- No change to the mock builder's code on `main`, to `reference/`, to the old folders or to the study packs (working rules 16 and 27). No change to the page "How the Mocks Are Built New" (working rule 18). No change in the portal folders `~/magnetlab-academy` and `~/magnetlab-portal`.
- No change to tab 1. No new design beyond the two choices above: a part follows slice 1. If a part needs a new kind of figure, the assistant draws it with the rules of decision 0013 and names it in the report.
- No file of the owner's personal material, and no conversation transcript (working rules 19 and 28).
- At most 2 agents at the same time. About 45 agents in all, all Opus 5.5 (decision 0012): 2 or 3 for each of about 15 parts, 4 for the two slices, 2 for the fix and 1 for the report.
- Text in Simplified Technical English. No semicolons, no em dashes.

## Order and time

Step 2 (about 5 to 6 hours), with step 3 in the gaps while agents of step 2 run (about 1 to 2 hours), then step 4 if time is left. At 08:45 at the latest, the assistant starts the morning report.

## The morning report

1. `HANDOFF.md` (section "The academy work") gets the report, and `academy/journal.md` gets the night's entry. The report has:
   - What is done, with the commits, on `main` and on `fix-owner-reason`.
   - The decisions that the assistant chose at night, each with its question and its choice.
   - The items that the agents found and that wait for the owner, also parts over their word limits.
   - The result of the checks and of the tests.
   - The screenshots to look at.
   - That a merge of the fix also needs the sentence "The code still works this way." of tab 2 step 5 changed.
   - That mock decision number 0080 is used on the branch.
2. A new agent checks the report and the journal entry against the commits (working rule 15). The assistant fixes what it finds.
3. Final commit. The main folder is on `main`, and `git status` is clean in both folders.

## Done when (the `/goal` condition)

The evaluator sees only the conversation, so the assistant shows each check as output.

(a) The output of `git log --oneline` shows the commits of slice 2, the check prints "All checks passed." (or only word-limit failures), and in the worktree the test run prints "OK". Or the output of `date` shows 09:30 or later.
And in both cases:
(b) `HANDOFF.md` has the morning report, its check by an independent agent is done, `git branch --show-current` in the main folder prints `main`, and `git status` is clean in both folders.
