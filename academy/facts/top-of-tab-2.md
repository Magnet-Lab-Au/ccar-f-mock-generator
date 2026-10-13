# Fact sheet: the top of tab 2

- Part: the top of tab 2 (academy decision 0010, item 2 of tab 2): the fixed title and paragraph of the owner, and one diagram of the 9 steps (steps 0 to 8).
- Fact agent: a new agent (academy decision 0012). Date: 13 October 2026.
- Order of trust (academy decisions 0011, 0014, 0029): L1 code, tests and run files. L2 decisions. L3 build guide and diagrams. L4 journal, lessons, reviews, `HANDOFF.md`.
- The fixed text is in `academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md`, lines 27 to 29. This sheet does not repeat it or change it.
- A path such as `docs/decisions/0033-...md` means the one file in `docs/decisions/` whose name starts with `0033-` (for 0027, 0031 and 0037: the file that starts with `00NN-the-`).
- Line numbers: `docs/diagrams/01-pipeline-overview.html` has all 9 step boxes on line 141 and the step data (JSON) on line 191.
- Files not read: the personal files of the owner (working rules 19 and 28), `claude-code-brand-kit/`, conversation transcripts, and the Excel files in `marking/`. The marks come from the run files `runs/mock-NN/marks/`.

## 1. The 9 steps

### The control (not a step, but it moves every question)

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F-C1 | The control decides the next action for each slot and for the mock. It does not do the work of a step. | `src/control.py:3-4` | "The control decides what happens next to a slot and to a mock. It does not do the work of a step." | 1 |
| F-C2 | The control calls steps 1 to 8 through one object. Step 0 is not in this list. | `src/control.py:6-14`; `src/steps.py:1-2` | "It connects steps 1 to 8 to the calls that the control makes." | 1 |
| F-C3 | Code calculates the status of each slot and the state of the mock from the records each time. No file stores them. | `src/control.py:21-22` | "No file stores them (decision 0037, item 2)." | 1 |
| F-C4 | The owner has 5 commands. | `src/run.py:73` | `choices=["run", "report", "mark", "decide", "accept"]` | 1 |
| F-C5 | One `run` does the automatic work and then stops with a report. | `src/control.py:329-331` | "One run of the program. It does the automatic work, then it stops and writes the report." | 1 |
| F-C6 | The states of a mock are `in_work`, `ready_to_mark`, `waits_for_owner`, `stopped` and `built`. | `src/control.py:789-836`; `docs/decisions/0039-...md:24-28` | "`stopped`: the owner selected `new_plan`, or the bad marks reached the limit." | 1, 2 |
| F-C7 | A record is never written over. The exceptions are `owner-decisions.json` and `report.json`. | `src/control.py:94-98`; `docs/decisions/0039-...md:99` | "A record is never written over." | 1, 2 |

### Step 0: Prepare the guide records

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F0.1 | Name. | `docs/build-guide/README.md:14` | "0. Prepare the guide records" | 3 |
| F0.2 | Who: code (a script). No model copies text. | `docs/decisions/0028-...md:21`; `src/step0_prepare_guide_records.py:3` | "Step 0 is a script. It reads `reference/exam-guide.md` and writes the records. No model copies text." | 2, 1 |
| F0.3 | Gets: `reference/exam-guide.md`. Gives: `reference/guide-records.json`. | `docs/decisions/0028-...md:42-43` | "It receives `reference/exam-guide.md`." / "It returns `reference/guide-records.json`." | 2 |
| F0.4 | What it does: it copies the parts of the guide that the later steps need into one file. A later step takes a slice by ID. | `docs/build-guide/step-0-prepare-the-guide-records.md:9` | "A later step takes a slice of it by ID." | 3 |
| F0.5 | It runs one time for each version of the guide, not for each mock. | `docs/diagrams/01-pipeline-overview.html:138-139` | "Step 0 runs one time for each version of the exam guide." / "Steps 1 to 8 run for each mock." | 3 |
| F0.6 | It writes no file if a count is wrong or a text is not exactly in the guide. | `src/step0_prepare_guide_records.py:4-5` | "It writes no file if a count is wrong or if a text is not exactly in the guide." | 1 |
| F0.7 | A second script checks the file. It does not use the code of step 0. | `src/check_guide_records.py:3-5` | "It does not use the code of step 0." | 1 |
| F0.8 | The records file feeds steps 1, 2, 4, 7 and 8, not only step 1. | `src/steps.py:35,40-41,49,85,99` | `self.writer = Writer(self.records, self.model_call)` | 1 |

### Step 1: Plan the mock

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F1.1 | Name. | `docs/build-guide/README.md:15` | "1. Plan the mock" | 3 |
| F1.2 | Who: code. No model. | `docs/build-guide/step-1-plan-the-mock.md:9` | "No model works in this step." | 3 |
| F1.3 | Gets: the guide records, a mock number and a seed. Also the point groups and the points that earlier built mocks used. | `docs/decisions/0027-the-design-...md:60`; `src/steps.py:49-50`; `docs/build-guide/step-1-plan-the-mock.md:25,27` | "It receives the guide records (...), a mock number and a seed." / `earlier=step1_plan.earlier_points(self.mocks_folder, mock)` | 2, 1, 3 |
| F1.4 | Gives: one plan file, `runs/mock-NN/plan.json`, with 60 slots. Code writes it only if it does not exist. | `src/control.py:332-334`; `docs/decisions/0027-the-design-...md:61` | `plan = self.steps.plan(self.mock, self.seed)` | 1, 2 |
| F1.5 | What it does: makes 60 slots. Each slot says the scenario, the task statement, one point, the question type and the number of answers to select. The same seed gives the same plan. | `docs/build-guide/step-1-plan-the-mock.md:9,11` | "A seed controls each selection. The same seed gives the same plan." | 3 |
| F1.6 | A first run needs a seed. | `src/run.py:33` | "Mock %d has no plan. Give --seed to make one." | 1 |

### Step 2: Write the question

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F2.1 | Name. | `docs/build-guide/README.md:16` | "2. Write the question" | 3 |
| F2.2 | Who: one call of the Claude API for each try. The call does not know the other questions. | `docs/build-guide/step-2-write-the-question.md:9`; `src/run.py:12` | "The call is new each time, and it does not know the other questions of the mock." / "The steps 2, 4 and 6 call the Claude API." | 3, 1 |
| F2.3 | The model in all run records: `claude-opus-5-5`, effort `high`. The code calls these "first values, not decisions". | `src/model_call.py:20-23`; run files `runs/mock-0*/questions/*.json` field `model` (488 of 488) and `runs/mock-0*/usage/*.json` fields `model`, `effort` (17 of 17) | "These are first values, not decisions." | 1 |
| F2.4 | Gets: one slot and the request that code builds from the guide records and the plan. | `docs/build-guide/step-2-write-the-question.md:11`; `docs/decisions/0029-...md:114` | "It receives one slot, the records file and the fixed parts of the request." | 3, 2 |
| F2.5 | Gives: one question record (one file for each try), with status `written` or `cannot_write`. | `src/control.py:378-392`; `src/step2_write.py:170` | `self._write_new(record, "questions", qid + ".json")` | 1 |
| F2.6 | Code, not the model, mixes the options and gives the letters. | `docs/build-guide/step-2-write-the-question.md:21` | "Code then mixes the options and gives them their letters. The model does not select the letters." | 3 |

### Step 3: Check by code

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F3.1 | Name. | `docs/build-guide/README.md:17` | "3. Check by code" | 3 |
| F3.2 | Who: code. Rules A1 to A12. | `src/step3_check_code.py:3-4` | "Code checks the rules A1 to A12, which have an exact answer. No model works in this step." | 1 |
| F3.3 | Gets: one question and its slot. Gives: verdict `pass` or `fail` with findings, saved as `checks/<question>-step3.json`. | `src/control.py:368-370,394-401` | `v = self.steps.check_code(question, slot)` | 1 |
| F3.4 | A question with `cannot_write` does not go to step 3. The slot is `open`. | `src/control.py:202-205` | `state["open_reasons"] = ["cannot_write"]` | 1 |
| F3.5 | A question that fails step 3 does not go to step 4. It goes to the writer again. | `src/control.py:206-224` | `if v3 is None or (v3["verdict"] == "pass" and v4 is None):` | 1 |

### Step 4: Check by a model

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F4.1 | Name. | `docs/build-guide/README.md:18` | "4. Check by a model" | 3 |
| F4.2 | Who: two model calls (4a blind answer, 4b rule check), then code makes the verdict. | `src/step4_check_model.py:3-8,196-197` | "A model does not make the verdict." | 1 |
| F4.3 | Gets: a question that passed step 3, its slot and the records. | `docs/decisions/0032-...md:150`; `src/control.py:208,371-376` | "It receives one question record that passed step 3, its slot, and the records file." | 2, 1 |
| F4.4 | Gives: verdict `pass`, `fail` or `cannot_decide` with findings, saved as `checks/<question>-step4.json`. | `src/step4_check_model.py:214-219`; `src/control.py:376` | `verdict = "cannot_decide"` | 1 |
| F4.5 | Call 4a does not see the marks or the reasons. | `docs/build-guide/step-4-check-by-a-model.md:11` | "It gets the question, the line "Select N.", the options and the text of the guide, but not the marks and not the reasons." | 3 |
| F4.6 | Fail and cannot decide go to step 5. | `docs/build-guide/step-4-check-by-a-model.md:17` | "A question that fails, or that the checker cannot decide, goes to step 5 with its findings." | 3 |

### Step 5: Try again

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F5.1 | Name. | `docs/build-guide/README.md:19` | "5. Try again" | 3 |
| F5.2 | Who: one model call, the same writer code as step 2. Code (the control) selects the request: step 2 or step 5. | `src/README.md:12`; `src/control.py:229-230` | "`step2_write.py`: steps 2 and 5, the writer." / "Step 2 or step 5, and which try the writer sees." | 1 |
| F5.3 | Gets: the request of step 2, plus the failed question with its letters, plus the exact findings. Only the last failed try. | `docs/build-guide/step-5-try-again.md:9`; `src/control.py:283-286` | "The writer does not see older tries, so the request stays short." | 3, 1 |
| F5.4 | Gives: a new question record with the next try number. No file is written over. | `src/control.py:379-380`; `docs/build-guide/step-5-try-again.md:15` | `qid = "%s-T%d" % (slot["slot_id"], n)` | 1, 3 |
| F5.5 | The findings come from step 3, step 4, step 6 (a rewrite of the owner) or the owner in step 7. | `docs/decisions/0033-...md:25,29` | "The findings come from step 3, step 4, step 6 or the owner in step 7." | 2 |
| F5.6 | After "more tries", the writer also gets the reason of the owner. | `src/control.py:270-281`; `docs/decisions/0074-...md:19` | "Since decision 0074 the writer also gets the reason of the owner, as an instruction." (control.py:270-271) | 1, 2 |

### Step 6: Check the complete mock

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F6.1 | Name. | `docs/build-guide/README.md:20` | "6. Check the complete mock" | 3 |
| F6.2 | Who: code (rules C2 and C3) and two model calls for each scenario (6a: D1, D4. 6b: D2, D3). The control checks rule C1. | `src/step6_check_scenario.py:3-9,86-87` | "Then two model calls read the 15 questions together: call 6a (rules D1 and D4) and call 6b (rules D2 and D3)." | 1 |
| F6.3 | It runs only when all slots have the status `passed`. | `src/control.py:340-343` | `if all(self.slot_state(s)["status"] == "passed" for s in self.slots()):` | 1 |
| F6.4 | Gets: the current questions of one scenario, plus the passed questions of the other scenarios (for rule C3). | `src/control.py:425-434,455-458` | "rule C3 compares the whole mock, decision 0052" | 1 |
| F6.5 | Gives: one record for each run for each scenario, with findings that have IDs such as `M1-SC3-R1-F1`. | `src/control.py:461-477`; `docs/decisions/0039-...md:34` | "`M1-SC3-R1-F1` is mock 1, scenario 3, run 1 of step 6, finding 1." | 1, 2 |
| F6.6 | Step 6 sends no question back. Each finding goes to the owner. | `src/step6_check_scenario.py:8-9`; `docs/decisions/0038-...md:23` | "Step 6 sends no question back. Each finding goes to the owner (decision 0038, part 3)." | 1 |
| F6.7 | A failure of rule C2 stops the run with an error. A new call cannot repair it. | `src/step6_check_scenario.py:27-28,35` | "C2 failing stops the run with an error that names the cause" | 1 |
| F6.8 | Step 6 runs again for a scenario when a question of it changed (the fingerprints differ). | `src/control.py:410-423` | `return last if last["fingerprints"] == now else None` | 1 |

### Step 7: The owner marks the questions

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F7.1 | Name. | `docs/build-guide/README.md:21` | "7. The owner marks the questions" | 3 |
| F7.2 | Who: code writes and reads an Excel file. A reader fills two columns. Mocks 1 to 3: the owner. Mocks 4 and 5: the second review in Cowork, a Claude model. | `src/step7_marking.py:3-5`; `docs/build-guide/step-7-the-owner-marks-the-questions.md:9`; `docs/decisions/0071-...md:21-24`; `HANDOFF.md:69` | "For mocks 4 and 5 it is the second review in Cowork, also a Claude model, so in mocks 4 and 5 every check is a model or code (decision 0071)." | 1, 3, 2, 4 |
| F7.3 | Code makes a marking round only after step 6 checked the current questions of each scenario, and when no round is open. | `src/control.py:527-531` | `if any(self._step6_needed(s) for s in self.plan()["scenarios"]):` | 1 |
| F7.4 | Gets: the questions to mark: all 60 for mocks 1 and 5. 20 for the other mocks, 5 from each scenario, with each domain. Also each question that a rewrite or a bad mark sent back. | `src/control.py:36,481-498,500-517` | `MARK_ALL = {1, 5}` | 1 |
| F7.5 | The file shows no verdict of a checker. | `src/step7_marking.py:4-5` | "It shows no verdict of a checker." | 1 |
| F7.6 | Gives: the marks record of the round, `runs/mock-NN/marks/round-N.json`, after the command `mark`. Code refuses a file with a missing mark or a bad mark with no reason. | `src/control.py:543-568`; `src/run.py:7` | "a bad mark has no reason" | 1 |
| F7.7 | The marks record has no field that says who marked. | `src/control.py:565-567` | `{"question_id": qid, "try": q["try"], "mark": ..., "reason": ..., "round": ..., "date": ..., "fingerprint": ...}` | 1 |

### Step 8: Build the files

| ID | Fact | Source | Quote | L |
|---|---|---|---|---|
| F8.1 | Name. | `docs/build-guide/README.md:22` | "8. Build the files" | 3 |
| F8.2 | Who: code, after the command `accept` of the owner. | `src/control.py:765-773`; `src/run.py:10` | "Command of the owner: accept the mock. Code checks the conditions, then step 8 builds." | 1 |
| F8.3 | Gets: the plan, the current question records and the guide records. | `src/step8_build_files.py:5-6`; `src/control.py:772-773` | "The step builds the files only from the plan, the question records and the guide records." | 1 |
| F8.4 | Gives: `mocks/mock-NN.questions.json` (no answers) and `mocks/mock-NN.answers.json`, and `build.json` with the fingerprints. | `src/step8_build_files.py:8-9`; `src/control.py:778-780` | "the 60 questions, with no answers and no reasons" | 1 |
| F8.5 | Code checks the conditions first. If one is false, it builds no file and lists the causes. | `src/control.py:733-763,770-771`; `docs/decisions/0039-...md:63-72` | "Step 8 cannot start: " | 1, 2 |
| F8.6 | Nobody edits the files by hand. | `docs/build-guide/step-8-build-the-files.md:9` | "Nobody edits the files by hand. To change a question, the record changes, and code builds the files again." | 3 |

## 2. The flow and the loops

Each arrow: from, to, a verb label, and the sources. "Owner" means the command of the owner (`decide`, `mark`, `accept`, `run`).

### The main path (top to bottom)

| ID | From | To | Label | Source | L |
|---|---|---|---|---|---|
| A1 | Step 0 | Step 1 (and steps 2, 4, 7, 8) | gives the guide records | `src/steps.py:23-25,35-41`; `docs/build-guide/step-0-...md:9` | 1, 3 |
| A2 | Step 1 | Step 2 | gives each slot (60) | `src/control.py:338-339` (`for slot in self.slots(): self._work_on_slot(slot)`) | 1 |
| A3 | Step 2 | Step 3 | gives a question record | `src/control.py:356-370` | 1 |
| A4 | Step 3 | Step 4 | passes | `src/control.py:208,371-376` | 1 |
| A5 | Step 4 | Step 6 | passes (when all 60 slots passed) | `src/control.py:211-213,340-343` | 1 |
| A6 | Step 6 | Step 7 | makes the marking file (when step 6 checked each scenario) | `src/control.py:344,527-541` | 1 |
| A7 | Step 7 | Step 8 | the owner accepts; code checks the conditions | `src/control.py:765-781`; `docs/build-guide/step-8-...md:11` | 1, 3 |

### The automatic loop (no owner)

| ID | From | To | Label | Source | L |
|---|---|---|---|---|---|
| L1 | Step 3 | Step 5 | fails | `src/control.py:206-224`; `docs/build-guide/step-5-try-again.md:9` | 1, 3 |
| L2 | Step 4 | Step 5 | fails or cannot decide | `src/control.py:211-224`; `docs/build-guide/step-4-...md:17` | 1, 3 |
| L3 | Step 5 | Step 3 | the new try is checked again (then step 4) | `docs/decisions/0033-...md:39`; `src/control.py:350-376` | 2, 1 |
| L4 | Step 5 (or step 2) | Open slot | 3 tries in one start, or 2 "cannot decide", or "cannot write" | `src/control.py:31-32,202-205,220-224` | 1 |

- The loop L1 to L3 runs inside one `run`, with no owner. It ends when the slot is `passed` (`src/control.py:211-213`) or `open` (`src/control.py:220-224`). Source of the rule: `docs/decisions/0038-...md:21` "One automatic loop. A question that fails step 3 or step 4 goes to step 5." (L2)
- The main way to stop is a pass, not the limit: `docs/build-guide/step-5-try-again.md:13` "The limit is not the main way to stop. The main way to stop is a question that passes." (L3)
- An open slot waits for the owner: `src/control.py:805-806` `waiting.append("open slot %s: %s" % ...)` (L1).

### The loops through the owner

| ID | From | To | Label | Source | L |
|---|---|---|---|---|---|
| O1 | Open slot | Step 5 | owner: `more_tries` (3 new tries; the writer gets the reason of the owner) | `src/control.py:270-281,633-638`; `docs/decisions/0074-...md:19` | 1, 2 |
| O2 | Open slot (`cannot_write`) | Step 2 | owner: `more_tries` | `src/control.py:278-280`; `docs/decisions/0033-...md:73` | 1, 2 |
| O3 | Open slot | Step 2 | owner: `new_point` (a new point of the same task statement) | `src/control.py:242-243,639-643` | 1 |
| O4 | Open slot | Mock stopped | owner: `new_plan` | `src/control.py:667-671,793-794` | 1 |
| O5 | Step 6 finding | (closed) | owner: `ignore` | `src/control.py:584-594,654-660` | 1 |
| O6 | Step 6 finding | Step 5 | owner: `rewrite` (names one question of the finding, with a reason) | `src/control.py:249-269`; `docs/build-guide/step-6-...md:16` | 1, 3 |
| O7 | Step 6 finding, or a question with no finding | Step 2 | owner: `rewrite` with a new point | `src/control.py:261-266,645-653,682-683`; `docs/decisions/0045-...md:23` | 1, 2 |
| O8 | Step 7 | Step 5 | bad mark (the reason of the owner is the finding) | `src/control.py:171-173,244-248`; `docs/build-guide/step-7-...md:13` | 1, 3 |
| O9 | Step 7 | Mock stopped | too many bad marks in round 1 | `src/control.py:571-576,795-796` | 1 |
| O10 | A call that failed 3 times | Error record, then the same call | owner starts the program again | `src/control.py:309-322,808-810`; `docs/decisions/0039-...md:54-59` | 1, 2 |

- Order of the owner's work: marks first, then the findings of step 6. `src/control.py:615-616` "Mark the questions first. Then decide on the findings of step 6." (L1). `docs/decisions/0038-...md:24` "The owner marks first, with no verdict in view." (L2)
- After O1, O3, O6, O7 or O8, the slot gets a new start: 3 new tries, and the count of "cannot decide" starts at zero. `src/control.py:158-163`; `docs/decisions/0033-...md:41` (L1, L2)
- After O6, O7 or O8: the new question goes through steps 3 and 4. Then step 6 runs again for its scenario (F6.8), and a new marking round has the new question (`src/control.py:500-517`: "A slot needs a mark when it is in the sample, or when it was sent back."). L1.
- Each loop through the owner needs a new `run`: `src/control.py:835` `"waiting_for": waiting + ["start the program"]`. `docs/decisions/0038-...md:24` "No count limits these rounds, because the owner starts each one." (L1, L2)
- A `rewrite` can also name a question with no finding of step 6 (`docs/decisions/0045-...md:22`; `src/control.py:645-653`). L2, L1.

### Where the loops end

| Loop | Ends at | Source | L |
|---|---|---|---|
| Automatic loop (L1 to L3) | `passed`, or `open` (waits for the owner) | `src/control.py:211-224` | 1 |
| Owner loops (O1 to O3, O6 to O8) | Back in the automatic loop, then step 6, then step 7 again. They end when no finding waits and no question waits for a mark. Then the state waits for "accept the mock". | `src/control.py:821-831` | 1 |
| `ignore` (O5) | The finding is closed. | `src/control.py:587` | 1 |
| `accept` (A7) | State `built`. Code refuses each later decision. | `src/control.py:628-629,791-792` | 1 |
| `new_plan` (O4) | State `stopped`. How a new plan starts is not built. | `src/control.py:793-794`; `docs/decisions/0039-...md:79` | 1, 2 |
| Too many bad marks (O9) | State `stopped`. No path in code after that. | `src/control.py:795-796`; `docs/decisions/0035-...md:57` | 1, 2 |
| Call failed 3 times (O10) | Waits for a new `run`. | `src/control.py:808-810` | 1 |
| Rule C2 fails in step 6 | The run stops (`RunStopped`). | `src/step6_check_scenario.py:35`; `src/run.py:109-111` | 1 |

## 3. Numbers

Each number with its source and how a script reads it. "Run-file script" means: read the JSON files of `runs/mock-01` to `runs/mock-05` with Python `json` and `glob`.

### Fixed numbers (code constants and decisions)

| Number | Meaning | Source | How a script reads it |
|---|---|---|---|
| 9 | steps, 0 to 8 | `docs/build-guide/README.md:14-22` | count files `docs/build-guide/step-*.md` (9) |
| 5 | mocks | `docs/decisions/0049-...md:18`; `mocks/` | count files `mocks/mock-*.questions.json` (5) |
| 60 | slots (questions) per mock | `src/step1_plan.py:41` | regex `^QUESTIONS = (\d+)`; or `len(plan["slots"])` in `runs/mock-NN/plan.json` |
| 4, 15 | scenarios per mock, questions per scenario | `src/step1_plan.py:42-43` | regex `^SCENARIOS_IN_MOCK = (\d+)`, `^PER_SCENARIO = (\d+)` |
| 16, 11, 12, 12, 9 | questions for domains 1 to 5 | `src/step1_plan.py:45` | regex `^DOMAIN_COUNTS = (.*)` |
| 3 | tries for each start of a slot | `src/control.py:31` | regex `^TRIES = (\d+)` |
| 2 | "cannot decide" results that stop a slot | `src/control.py:32` | regex `^CANNOT_DECIDE = (\d+)` |
| 3 | runs of a call that fails | `src/control.py:30` | regex `^CALL_RUNS = (\d+)` |
| 12 | rules of step 3 (A1 to A12) | `src/step3_check_code.py:3` | regex `rules A1 to A(\d+)` |
| 9 | rules of step 4 (B1 to B9) | `src/step4_check_model.py:19` | `len(RULES_B)` by regex on line 19 |
| 2 | model calls of step 4 for each try | `src/step4_check_model.py:196-197` | count lines with `self.blind(` and `self.rules(` in `check` |
| 2 | model calls of step 6 for each scenario | `src/step6_check_scenario.py:86-87` | count `self._call(` in `check` |
| 60 / 20 | questions in the marking file: mocks 1 and 5 / mocks 2 to 4 | `src/control.py:33,36` | regex `^MARKS_LATER_MOCK = (\d+)`, `^MARK_ALL = \{(.*)\}` |
| 7 / 2 | bad marks in round 1 that stop the mock (60 marks / 20 marks) | `src/control.py:34-35` | regex `^STOP_MOCK_1 = (\d+)`, `^STOP_LATER_MOCK = (\d+)`. Note: 7 means "more than 6". |
| 6 | conditions before step 8 | `docs/decisions/0039-...md:65-70` | count lines matching `^\d\. ` under "### Item 10" |
| 120 | minutes of a mock | `src/step8_build_files.py:17` | regex `^MINUTES = (\d+)`; or field `minutes` in `mocks/mock-NN.questions.json` |
| 5 | commands of the owner | `src/run.py:73` | parse the list `choices=[...]` |
| 228 | tests; all pass (run on 13 October 2026, no model call) | `tests/*.py` | count `def test` in `tests/*.py`; or `python3 -m unittest discover tests` prints "Ran 228 tests" |

### Run numbers (run-file script, read on 13 October 2026)

| Number per mock (1, 2, 3, 4, 5) | Total | How a script reads it |
|---|---|---|
| Tries: 83, 92, 101, 111, 101 | 488 | count `runs/mock-NN/questions/*.json` |
| Requests of step 2: 65, 60, 61, 61, 64 | 311 | field `request` == 2 in each question record |
| Requests of step 5: 18, 32, 40, 50, 37 | 177 | field `request` == 5 |
| Slots with more than 1 try: 18, 27, 28, 29, 21 | | count `slot_id` values with 2 or more question records |
| Most tries for one slot: 6, 3, 6, 7, 6 | | max of the count above |
| Step 3 fails: 0, 1, 2, 4, 4 | 11 | field `verdict` == "fail" in `checks/*-step3.json` |
| Step 4 fails: 14, 17, 37, 45, 35 | 148 | field `verdict` == "fail" in `checks/*-step4.json` |
| Step 4 "cannot decide": 0 in each mock | 0 | field `verdict` == "cannot_decide" in `checks/*-step4.json` |
| Tries with "cannot write": 0 in each mock | 0 | field `status` == "cannot_write" in question records |
| Slots that the owner opened again (`more_tries` or `new_point`): 1, 0, 4, 5, 6 | 16 | distinct `target` of those actions in `owner-decisions.json` |
| Rewrites: 9, 14, 2, 2, 0 | 27 | `action` == "rewrite" in `owner-decisions.json` |
| Runs of step 6 (all scenarios): 8, 8, 6, 6, 5 | 33 | count `checks/*step6*.json` |
| Findings of step 6: 35, 18, 13, 23, 19 | 108 | sum of `len(findings)` in `checks/*step6*.json` |
| `ignore` decisions: 33, 9, 11, 17, 14 | 84 | `action` == "ignore" |
| Marking rounds (questions in each): [60, 9], [20, 14], [20, 2], [20, 2], [60, 2] | | `len(question_ids)` in `marking-rounds/round-N.json` |
| Bad marks: 0, 0, 0, 0, 2 (both round 1 of mock 5) | 2 | `mark` == "bad" in `marks/round-N.json` |
| Program runs: 5, 2, 4, 4, 6 | 21 | count `runs/mock-NN/runs/*.json` |
| Error records: 0 in each mock | 0 | count `runs/mock-NN/errors/*.json` |
| Model calls: 265, 290, 313, 337, 295 | 1500 | sum of field `calls` in `usage/*.json` |
| Cost in dollars: 17.17, 20.73, 23.85, 12.83, 11.68 | 86.26 | sum of field `dollars` in `usage/*.json` |
| Questions in the built mock file: 60 in 4 groups, each mock | 300 | sum of `len(g["questions"])` over `groups` in `mocks/mock-NN.questions.json` |
| State of each mock: `built` | | field `state` in `runs/mock-NN/report.json` |

Notes on the numbers:

- Mock 5 cost: `docs/decisions/0073-...md:23` says a stopped run of mock 5 is not in `usage/` ("under $1"). So 11.68 and 86.26 do not include it. (L2)
- Mock 1 rewrites: 9, and 5 of them have a field `point` (a new point). This agrees with `docs/build-guide/step-5-try-again.md:23` "The owner sent 9 questions back as rewrites after the marks, 5 of them with a new point." (L1, L3)
- Mock 1 tries, requests and step 4 fails agree with `docs/build-guide/step-5-try-again.md:19-21` (83, 65, 18, 14). (L3)

## 4. Conflicts

| ID | Topic | Source A (quote, level) | Source B (quote, level) |
|---|---|---|---|
| X1 | Who does step 7 | `docs/diagrams/01-pipeline-overview.html:141`, box 7 tag: "The owner" (L3). Also the step name "The owner marks the questions", `docs/build-guide/README.md:21` (L3). | `docs/build-guide/step-7-...md:9`: "For mocks 4 and 5 it is the second review in Cowork, also a Claude model" (L3). `docs/decisions/0071-...md:24`: "no person reads the questions of mocks 4 and 5." (L2). `docs/journal.md:22`: "the assistant typed the 2 marks on the instruction of the owner." (L4). The popup data of diagram 01 (line 191) says it too. |
| X2 | What happens after too many bad marks | `docs/diagrams/01-pipeline-overview.html:172`: "Too many bad marks of the owner stop the mock. The rules of the checker are corrected, and all 60 questions are checked again." (L3). `docs/decisions/0021-...md:20` says the same (L2). | `src/control.py:793-796` and `628-629`: the state is `stopped`, and code refuses each decision. No code checks the 60 questions again (L1). `docs/decisions/0035-...md:57`: "Not decided yet: ... How "all 60 questions go through the checks again" works after a stop" (L2). |
| X3 | Where a `rewrite` goes | `docs/build-guide/step-6-...md:16`: "A rewrite sends one question of the finding to step 5." (L3). `docs/decisions/0033-...md:75` and `0039-...md:50`: rewrite gets request "Step 5" (L2). | `src/control.py:261-266`: a rewrite with a new point is "a request of step 2 on the new point" (L1). `docs/decisions/0045-...md:23` (later): "Then the writer gets a request of step 2 with the new point" (L2). |
| X4 | What the writer gets after `more_tries` | `docs/decisions/0033-...md:72` and `0039-...md:47`: "The last try, with its findings" (L2). The status lines of 0033 and 0039 say only "accepted". | `docs/decisions/0074-...md:19` (later): "the request of step 5 has the findings of the last try and the reason of the owner" (L2). `src/control.py:270-281` agrees with 0074 (L1). |
| X5 | Does step 6 send questions back | `docs/decisions/0014-...md:25`: "A question that this step names goes back to step 5 (decision 0013)." Its status line (line 4) says only "accepted" (L2). | `docs/decisions/0038-...md:23` (later): "Step 6 sends no question back." (L2). `src/step6_check_scenario.py:8-9` (L1). |
| X6 | Which mocks mark all 60 (inside the code) | `src/control.py:483`, docstring of `sample`: "Mock 1: all 60. A later mock: 20, 5 from each scenario, with each domain." (L1) | `src/control.py:36`: `MARK_ALL = {1, 5}` (L1). `docs/decisions/0073-...md:21` (L2). Run files: mock 5 round 1 has 60 questions. |
| X7 | Do the real steps exist | `src/README.md:15`: "The real steps do not exist yet." (L1). `docs/decisions/0039-...md:136`: "The real steps. Each one is a fake now." (L2) | `src/steps.py:1-2` connects the real steps (L1). `src/README.md:12-13` lists them (L1). All 5 mocks are `built` in `runs/mock-NN/report.json` (L1). |
| X8 | Task statements shown in the box of each step (diagram 01 against the build guide) | `docs/diagrams/01-pipeline-overview.html:141`: step 2 "Exam guide: no point. Plain engineering reason."; step 4 "task statements 4.6 and 3.6"; step 5 "task statement 4.4"; step 6 "task statements 4.6 and 1.6" (L3). Line 191, step 2: "the decision of the step uses no point. Its design uses task statements 4.1, 4.2 and 4.3." (L3) | Build guide tables (L3): step 2 (`step-2-...md:41-52`) uses 4.3, 4.2, 4.1, 1.4. Step 4 (`step-4-...md:56-64`) uses 4.6, 4.3, 4.1, 1.4, and not 3.6. Step 5 (`step-5-...md:37-44`) uses 4.4, 1.1, 4.3. Step 6 (`step-6-...md:36-43`) uses 4.6, 4.1, 5.3, 4.3, and not 1.6. Decision 0033 line 135 (L2): "4.4-K1, 4.4-S1, 4.4-K2, 1.1-S3". |
| X9 | What step 8 waits for | `docs/diagrams/01-pipeline-overview.html:191`, step 8: "It receives the stored question records of a mock that passed step 7." (L3) | `src/control.py:733-771`: step 8 waits for the command `accept` and six conditions, also that each finding of step 6 has a decision (L1). `docs/build-guide/step-8-...md:11` (L3). This is an omission in diagram 01, not a direct contradiction. |
| X10 | The number of tests | `docs/decisions/0039-...md:20`: "53 tests pass." (L2). `docs/journal.md:25`: "226 tests pass." (L4) | `tests/*.py`: 228 `def test`. `python3 -m unittest discover tests` on 13 October 2026: "Ran 228 tests", "OK" (L1). The counts are from different dates. |

## 5. Not found

| ID | What the diagram needs | What the sources say |
|---|---|---|
| N1 | Who types the commands of the program (`run`, `decide`, `accept`, `mark`). | `src/run.py:1` calls it "The command line of the owner." But `docs/decisions/0073-...md:23` says "The assistant stopped the run after 4 questions, changed the code and started the run again." No source says in general who ran the commands. |
| N2 | Who filled the 20 "good" marks of round 1 of mock 4. | `docs/decisions/0069-...md:24`: "the owner states that they did not read the 20 questions of round 1. The marks ... (20 of 20 good) are recorded as they are." No source names who typed them. The marks record has no field for the marker (F7.7). |
| N3 | The path after `new_plan`. | `docs/decisions/0039-...md:79`: "How a new plan then starts is not built yet." No run used `new_plan`. |
| N4 | The path after the stop by too many bad marks. | See X2. No code and no decision gives the procedure. No mock reached the limit (most bad marks in round 1: 2 of 60, mock 5). |
| N5 | A run in which the loops "cannot write" and "cannot decide" happened. | The code has both paths (`src/control.py:202-205,215-223`), but the run files have 0 of each in all 5 mocks (section 3). So the diagram can show them only as paths of the code. |
| N6 | Arrows in diagram 01 for: owner decisions on an open slot back to step 2 or 5, a `rewrite` with a new point to step 2, `accept` to step 8, and the two stops. | Diagram 01 (`docs/diagrams/01-pipeline-overview.html:123-135,143-149`) has 7 arrows down and 6 failure arrows: "fails", "fails or cannot decide", "rewrite", "too many tries", "the new question is checked again", "bad mark". The open-slot box (data-step "L") has no outgoing arrow. The facts for the missing arrows are in the code (section 2), but no diagram shows them. |
| N7 | A place of the second review in Cowork in the program. | It is outside the code: no file in `src/` names it. The decisions (0045, 0069, 0071, 0073) and `HANDOFF.md:69` describe it. In mock 1 it also found 7 problems of the mock as a set (`docs/decisions/0045-...md:10`). |
