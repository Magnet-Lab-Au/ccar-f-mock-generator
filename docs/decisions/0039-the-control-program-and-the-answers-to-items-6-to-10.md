# 0039: The control program, and the answers to items 6 to 10 of the second review

- Date: 7 October 2026
- Status: accepted
- Changed: 7 October 2026, after two independent reviews of the code. The owner said yes to each change.
- Diagram: none

## Question

Decision 0038 says that the control is written as code with tests, and that the code and its tests give the answers to items 6 to 10 of the second review. What does the control do, and what are the answers?

## Options

1. The control as one part of the program, `src/control.py`. Each step is a separate part that the control calls. In the tests, each step is a fake.
2. A different design.

## Decision

Option 1. The tests are in `tests/`. They use `unittest` of Python. No test makes a model call. 53 tests pass. They cover the path with no failure, the cases (a) to (f) and (j) of the second review, each row of the table of item 8, the limits, `new_plan`, a new start, and the findings of the two independent reviews.

### Item 6: the values of `state`, and the IDs

- `in_work`: the program still has automatic work. `waiting_for` then says "start the program".
- `ready_to_mark`: a marking file waits for the marks of the owner.
- `waits_for_owner`: only the owner can move the mock on: an open slot, a call that failed 3 times, a finding of step 6, or the accept of the mock.
- `stopped`: the owner selected `new_plan`, or the bad marks reached the limit.
- `built`: step 8 made the files.
- The report gets a new field, `waiting_for`. It says what the mock waits for.
- The report field `step6_cannot_decide` becomes `step6_findings`, because a `fail` of step 6 also waits for the owner (decision 0038, part 3).
- A decision of the owner has the ID `D001`, `D002`, and so on, and a new field `target`: a slot (`M1-S05`), a finding (`M1-SC3-R1-F1`) or the mock (`M1`).
- Code adds two more fields to a decision. `after_try` (for `new_point`, `more_tries` and `rewrite`) is the try number when the owner decided. Each try with a higher number belongs to the new start of the slot. `question_id` (for `rewrite`) is the question that the owner names.
- The command `accept` is also saved as a decision, with the action `accept` and the target `M1`. Code saves it only after step 8 built the files.
- A finding of step 6 has an ID. Example: `M1-SC3-R1-F1` is mock 1, scenario 3, run 1 of step 6, finding 1.

### Item 7: `new_point`

- Code selects a point of the same task statement that no slot uses now, and that this slot did not have before. The seed selects from the free points. If no point is free, code refuses the command.
- Code saves the point in the decision, in the new field `point`. `plan.json` does not change, so the same seed still gives the same plan.
- Each question record gets the new field `point`.

### Item 8: the request after a decision

| Event | Request | The try that the writer sees |
|---|---|---|
| `new_point` | Step 2 | None |
| `more_tries` after `three_tries` or `cannot_decide_twice` | Step 5 | The last try, with its findings |
| `more_tries` after `cannot_write` | Step 2 | None |
| A bad mark | Step 5 | The marked question. The finding is the reason of the owner. |
| `rewrite` of a finding of step 6 | Step 5 | The named question, the finding, the reason of the owner, and the text of the other questions of the finding |

Each question record gets two new fields: `request` (2 or 5) and `shown_try`.

### Item 9: a call that fails 3 times

- Code saves an error record, for example `runs/mock-01/errors/E001.json`, with `id`, `run`, `step`, `target`, `cause` and `date`.
- Each start of the program saves a run record, for example `runs/mock-01/runs/run-002.json`.
- The report shows the error records of the last run.
- The action of the owner: start the program again. The new start runs the failed call again.

### Item 10: the conditions before step 8

Step 8 starts only after the command `accept` of the owner, and only when:

1. Each of the 60 questions passed steps 3 and 4, and no question changed after its checks (the fingerprint).
2. Step 6 checked the current questions of each scenario.
3. Each finding of step 6 has a decision of the owner.
4. Each question that needs a mark has a mark. A bad mark sends the slot back, so the mark of each current question is `good`.
5. The bad marks are below the stop limit.
6. No call failed in the last run.

If a condition is false, code builds no file and lists the causes.

### Four more choices of the code

1. The fingerprint uses the fields as JSON with sorted keys, in UTF-8. This closes an open item of decision 0036.
2. Only the bad marks of round 1 count for the stop limit. This closes an open item of decision 0035.
3. The marks go into one file for each round, for example `runs/mock-01/marks/round-1.json`, not into one file `marks.json`. A record is never written over.
4. `new_plan` stops the mock. How a new plan then starts is not built yet.

### Rules that the independent review added

Two independent reviewers checked the code on 7 October 2026. The first found 4 serious and 6 minor bugs. The second found 1 serious and 3 minor bugs in the fixes. Each fix makes the code agree with a decision that the owner already made. Each fix has a test, and the assistant checked that each test fails without its fix.

1. The owner sees and decides the findings of step 6 only when the automatic work is done, step 6 checked the current questions, and no question waits for a mark (decision 0038, part 4). Otherwise code refuses the decision and says why.
2. A `rewrite` of one finding does not hide the other findings of the same run of step 6. A slot that waits only for the new try of a `rewrite` of the owner does not hide them. The owner decides each finding of the last run of step 6 of each scenario.
3. A `rewrite` must name the current try of a slot that has the status `passed`, and a question that exists. Otherwise code refuses the command.
4. Only a `rewrite` or a bad mark adds a question outside the sample to a marking round (decision 0038, part 9). `more_tries` and `new_point` do not.
5. `new_plan` is an action for an open slot (decision 0033). Code refuses it when no slot is open.
6. Code refuses each decision after the mock is `stopped` or `built`.
7. Code saves the decision `accept` only after step 8 built the files.
8. The report of a mock that is `stopped` or `built` shows no errors.
9. The marking rounds are in the sequence of their numbers.
10. After a bad mark, `waiting_for` says "start the program".
11. Code checks the answer of step 6. A result `fail` or `cannot_decide` must have a finding, and each finding must name only current questions of its scenario. Otherwise the answer is not valid, and code runs the call again, as for step 4 (decision 0032). After 3 answers that are not valid, code saves an error record.

### The records of the control

All are in the run folder, for example `runs/mock-01/`. Code writes each record one time, and never writes over it. The exceptions are `owner-decisions.json`, to which code adds each decision, and `report.json`, which code builds again each time.

| Record | Content |
|---|---|
| `plan.json` | The plan of step 1 |
| `questions/M1-S17-T1.json` | One try |
| `checks/M1-S17-T1-step3.json`, `-step4.json` | The verdicts of steps 3 and 4 |
| `checks/M1-scenario-3-step6-run1.json` | One run of step 6 for one scenario |
| `marking-rounds/round-1.json` | The questions of one marking round, with their fingerprints |
| `marks/round-1.json` | The marks of one round |
| `owner-decisions.json` | The decisions of the owner |
| `errors/E001.json` | A call that failed 3 times |
| `runs/run-001.json` | One start of the program |
| `build.json` | The files that step 8 built, and the fingerprints |
| `report.json` | The report |

### Step 6 in the control

The record of one run of step 6 has the fields `mock`, `scenario`, `run`, `results`, `findings` (each with its ID), `verdict`, `fingerprints` and `date`. It does not have `to_step_5`, because step 6 sends no question back (decision 0038, part 3). The fields `code_count` and `model` of decision 0034 belong to the real step 6, which is not built.

Rules C2 and C3 of decision 0034 are a part of step 6, not of the control. The fake of step 6 does not have them.

## Reason

- **Code with tests.** Decision 0038 has the reason.
- **Each step is a separate part.** Plain reason: a test can replace each step with a fake, so the tests check only the control.
- **The answers.** Plain reasons. Each answer is the path that the tests run. A test shows that a case has a path. It does not show that the path is good (decision 0038).
- **`waiting_for`.** Plain reason: the owner sees what to do without a search in the records.
- **A new point that the slot did not have before.** Plain reason: the owner selects `new_point` because the old point did not work. A test found that a second `new_point` could go back to the first point.
- **Step 2 after `new_point`.** Plain reason: the old tries tested a different point.
- **The error record.** Plain reason: the report is built from the records, so each error needs a record (contradiction 4 of the second review).
- **The start of the program as the action of the owner.** Decision 0038, part 4: the owner starts each round.

Not decided yet:

- How a new plan starts after `new_plan`.
- The command line of the owner. The control has the functions, but no command line exists yet.
- The real steps. Each one is a fake now.

## How we decided

The owner agreed to the plan for the control. The assistant first gave the plan before it read all files that `HANDOFF.md` names. The owner asked if the assistant had read them. It had not. It read them, and changed six points of the plan.

The plan said that the assistant stops at each of items 6 to 10. It wrote the code for all five in one pass, and told the owner. Then it showed each answer. The owner said yes to each one. The owner asked for shorter questions: 1 to 3 sentences.

The owner asked if the values of `state` were already decided. The answer: the names were decided in decision 0037, item 10. The meanings were open in decision 0033.

An independent reviewer checked the code, the tests and this file against decisions 0033 to 0038. It found 4 serious and 6 minor bugs, and 8 differences between this file and the code. The assistant fixed them, and the owner said yes before. The reviewer said that one test does not guard the rule "this slot did not have the point before". The assistant checked: that test fails without the rule.

A second independent reviewer checked the fixes. Eight were complete. It found 1 serious and 3 minor bugs, 3 differences in this file and 3 weak tests. The owner said yes, and the assistant fixed them. One fix (rule 1) first conflicted with rule 2. The assistant kept both, with the exception for a slot that waits for a `rewrite`. No reviewer checked this last round of fixes.

## Exam guide points

none
