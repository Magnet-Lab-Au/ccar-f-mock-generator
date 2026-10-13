# Fact sheet: tab 2, step 7 "The questions are marked"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `7d1aa0c` (branch `main`, clean).
- Build guide name: "The owner marks the questions" (`docs/build-guide/step-7-the-owner-marks-the-questions.md`, line 1). Tab 2 name: "The questions are marked" (academy decision 0034, status "proposed", line 4).
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`, `docs/portal-notes.md`. Git commit messages are listed with "git" (they are records of the time, not in the order of trust).
- The tests ran on 14 October 2026 with no API key in the environment: `env -u ANTHROPIC_API_KEY python3 -m unittest discover -s tests` gives "Ran 228 tests ... OK". `tests/test_step7_marking.py` has 15 tests (`grep -c "def test"`).
- Files that this agent did not open (working rules 19 and 28): `marking/*.xlsx` (only their names and commit messages are used), `responses.json`, and all personal files of the owner. No Anthropic documentation page was used.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | The step shows if the checks before it are right: a reader marks the questions. | `docs/build-guide/step-7-the-owner-marks-the-questions.md`, 9 | "Each check before this step is code or a model. This step shows if those checks are right: a reader marks the questions." | 3 |
| O2 | Who the reader was: the owner for mocks 1 to 3, the second review in Cowork (a Claude model) for mocks 4 and 5. | same, 9; `HANDOFF.md`, 69 | "For mocks 1 to 3 the reader is the owner. For mocks 4 and 5 it is the second review in Cowork, also a Claude model, so in mocks 4 and 5 every check is a model or code (decision 0071)." / "So no person read the questions of mocks 4 and 5." | 3 / 4 |
| O3 | Code writes the marking file and reads it. The step does only that. The control decides which questions go in, checks the marks and saves them. | `src/step7_marking.py`, 3-9 | "Code builds one Excel file for each round of marking ... It shows no verdict of a checker. The owner fills two columns: \"Mark\" (good or bad) and \"Reason\". The control decides which questions go into a round, checks that each mark is complete, and saves the marks record (decision 0039). This step only writes and reads the file." | 1 |
| O4 | A bad mark sends the question back. Too many bad marks stop the mock. | build guide, 13 | "A bad mark sends the question to step 5, with the reason as the finding. Too many bad marks stop the mock" | 3 |
| O5 | Status: built, ran in the test of 7 October and in mocks 1 to 5. | build guide, 3 | "Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026." | 3 |
| O6 | The original question of the design: what shows if the model check is correct. | `docs/decisions/0015-...`, 10 | "What shows if the model check is correct?" | 2 |
| O7 | Known limit: no person reads the questions of mocks 4 and 5. | `docs/decisions/0071-...`, 24; `docs/portal-notes.md`, 7 | "**Known limit: no person reads the questions of mocks 4 and 5.** The writer, the checkers of steps 4 and 6, and the second review are all Claude models." | 2 / 4 |

## 2. Explanation facts: the mechanism

### 2.1 When a round starts, and which questions go in

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | A round is made at the end of a run, only when all 60 slots passed and step 6 ran. | `src/control.py`, 340-344 | `if all(self.slot_state(s)["status"] == "passed" for s in self.slots()):` ... `self._make_marking_round()` | 1 |
| E2 | No round while step 6 must still check a scenario, or while a round is open, or when no question needs a mark. | `src/control.py`, 527-534 | `if any(self._step6_needed(s) for s in self.plan()["scenarios"]): return` / `if self._open_round() is not None: return` / `if not ids: return` | 1 |
| E3 | The constants: 20 for a later mock, mocks 1 and 5 put all 60 in the file. | `src/control.py`, 33, 36 | `MARKS_LATER_MOCK = 20  # the sample of a later mock (decision 0022)` / `MARK_ALL = {1, 5}      # the mocks whose 60 questions are all in the marking file (decisions 0022 and 0073)` | 1 |
| E4 | The sample of a later mock: 5 slots from each scenario at random, with a seed. Code draws again (up to 1000 times) until each domain is in the sample. Domain is a condition of the draw, not a stratum. | `src/control.py`, 485-498 | `rng = random.Random("%s-sample" % self.seed)` / `chosen.extend(rng.sample(group, MARKS_LATER_MOCK // 4))` / `if {domain(s) for s in chosen} == domains:` / `raise RuntimeError("No sample has each domain.")` | 1 |
| E5 | A question also needs a mark when a `rewrite` or a bad mark sent its slot back, also outside the sample. `more_tries` and `new_point` do not add a mark. | `src/control.py`, 500-517; `docs/decisions/0039-...`, 88 | "A slot needs a mark when it is in the sample, or when it was sent back." / "Only a `rewrite` or a bad mark adds a question outside the sample to a marking round (decision 0038, part 9). `more_tries` and `new_point` do not." | 1 / 2 |
| E6 | A question is "marked" only if its mark has the same fingerprint as the current record. | `src/control.py`, 503, 515 | `marked = {(m["question_id"], m["fingerprint"]) for m in self.marks()}` | 1 |
| E7 | The round record: the question IDs with their fingerprints and the date, in `runs/mock-0N/marking-rounds/round-N.json`. | `src/control.py`, 535-541 | `self._write_new({"round": n, "question_ids": ids, "fingerprints": {...}, "date": self.today()}, "marking-rounds", "round-%d.json" % n)` | 1 |
| E8 | Tests: 20 questions, 5 from each scenario, all 5 domains; mock 5 gets 60, mock 4 gets 20; a rewrite outside the sample gets a mark; more tries and a new point outside the sample do not. | `tests/test_control.py`, 355-364, 473-478, 409, 695-699 | `def test_sample_of_20(self):` / `def test_mock_5_samples_all_60_and_mock_4_samples_20(self):` / `def test_a_question_from_a_rewrite_gets_a_mark_also_outside_the_sample(self):` / `def test_more_tries_outside_the_sample_does_not_add_a_mark(self):` | 1 |

### 2.2 The marking file (what the reader sees and fills)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E9 | The 15 columns of the file. 13 for reading, 2 for the reader. | `src/step7_marking.py`, 20-22 | `HEADERS = ["Question ID", "Scenario", "Point", "Point text", "Question", "Select", "A", "B", "C", "D", "E", "Correct answer", "Reasons of the options", "Mark", "Reason (needed for a bad mark)"]` | 1 |
| E10 | The file shows the correct answer and the reasons, but no verdict of a checker. A test checks that no header or cell has a verdict word. | `src/step7_marking.py`, 4-5; `tests/test_step7_marking.py`, 71-78 | "It shows no verdict of a checker." / `for word in ("verdict", "finding", "step 3", "step 4", "step 6"):` / `self.assertFalse(cells & {"pass", "fail", "cannot_decide", "cannot decide"})` | 1 |
| E11 | Why no verdict: a person who sees a verdict tends to agree with it. | `docs/diagrams/09-...html`, 232 (popup `owner`) | "The owner does not see the verdicts of the checkers during the marking. A person who sees a verdict tends to agree with it." | 3 |
| E12 | Why the point is in the file. | `docs/decisions/0035-...`, 45 | "Plain reason: the owner cannot judge if a question tests its point when the file does not show the point." | 2 |
| E13 | The two yellow columns. "Mark" has a list: good or bad. | `src/step7_marking.py`, 24, 114-117 | `FILL = PatternFill("solid", fgColor="FFF2CC")   # the yellow of the columns that the owner fills` / `formula1='"good,bad"'` / `error='Type "good" or "bad".'` | 1 |
| E14 | The sheet is protected with no password, and sorting is off, so a mark cannot move to a different question. | `src/step7_marking.py`, 101-106 | "The sheet is protected with no password. Only the two columns of the owner can change, and sorting is off, so that a mark cannot move to a different question. The owner can remove the protection on purpose." | 1 |
| E15 | Code never writes over a marking file. An empty file of the same round is used again after a stop. | `src/step7_marking.py`, 56-70; `tests/test_step7_marking.py`, 98, 104 | "Write the marking file of one round. Never write over a file." / `raise MarkingError("The marking file exists already: %s" % path)` | 1 |
| E16 | Why Excel. | `docs/decisions/0035-...`, 44 | "Plain reason: the owner can read and fill it with no tool." | 2 |
| E17 | The file is in `marking/`, not in `runs/`, because no person writes in `runs/`. | `docs/decisions/0035-...`, 33 | "The marking file is in the folder `marking/`, not in `runs/`. `README.md` says that no person writes in `runs/`." | 2 |

### 2.3 Code reads the marks

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E18 | The owner's command `mark` reads the file of the open round. | `src/run.py`, 7, 93-96 | `python3 src/run.py mark --mock 1                read the marking file of the open round` / `report = c.read_marks()` | 1 |
| E19 | Code refuses an incomplete file and names each row: a missing row, no mark, a mark that is not good or bad, a bad mark with no reason. | `src/control.py`, 549-561 | `problems.append("%s: no mark" % qid)` / `'%s: the mark "%s" is not good or bad'` / `problems.append("%s: a bad mark has no reason" % qid)` / `raise Refused("The marking file is not complete: " + "; ".join(problems))` | 1 |
| E20 | Code also refuses a formula in the two columns, a question in the file two times, and changed columns. | `src/step7_marking.py`, 136-150 | "The columns of the marking file changed. Use the file as code made it." / "The row of %s has a formula. Type the mark and the reason as text." | 1 |
| E21 | The marks record: one record per round, in `runs/mock-0N/marks/round-N.json`. Fields: `question_id`, `try`, `mark`, `reason`, `round`, `date`, `fingerprint`. No field says who marked. | `src/control.py`, 562-568 | `records.append({"question_id": qid, "try": q["try"], "mark": ..., "reason": ..., "round": r["round"], "date": self.today(), "fingerprint": r["fingerprints"][qid]})` | 1 |
| E22 | A record is never written over (`_write_new`). | `src/control.py`, 568; `docs/decisions/0035-...`, 28 | "A record is never written over (decision 0039)." | 1 / 2 |
| E23 | After `mark`, code prints the bad marks for each scenario and each domain. The print is not saved in a run file. | `src/run.py`, 95; `src/step7_marking.py`, 158-167 | `print("Bad marks:", json.dumps(steps.bad_marks_by_segment(c.marks())))` / "The bad marks for each scenario and each domain (decision 0035, part 4)." | 1 |
| E24 | The test of the per-segment count. | `tests/test_step7_marking.py`, 179 | `def test_bad_marks_for_each_scenario_and_each_domain(self):` | 1 |
| E25 | Code does not compare the marks with the verdicts. Decision 0035 changed decision 0015 on this. | `docs/decisions/0035-...`, 23; `docs/decisions/0015-...`, 21 | "It does not compare the marks with the verdicts in this step." / (0015) "Code then compares the marks with the verdicts" | 2 |

### 2.4 What a mark does

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E26 | A bad mark is a send-back event of its slot, after the try that was marked. | `src/control.py`, 171-173 | `if m["mark"] == "bad" and m["question_id"].startswith(slot_id + "-T"):` / `events.append({"kind": "bad_mark", "after_try": m["try"], "mark": m})` | 1 |
| E27 | After a bad mark, the writer gets a request of step 5 with the marked question. The finding is the reason of the reader, rule `owner`. | `src/control.py`, 244-248 | `finding = {"step": 7, "rule": "owner", "detail": event["mark"]["reason"], "letter": None, "point": None, "other_questions": []}` / `return self._step5(request, q, [finding])` | 1 |
| E28 | The new question goes through steps 3 and 4, step 6 runs again for its scenario, and the next round has only the new question. | `tests/test_control.py`, 238-256 | `# Step 6 runs again only for scenario 3.` / `# Round 2 has only the new question.` / `self.assertEqual(self.steps.marking_files[2], ["M1-S20-T2"])` | 1 |
| E29 | Why a bad mark needs a reason. | `docs/decisions/0035-...`, 46 | "A bad mark with no reason gives the writer nothing to change." | 2 |
| E30 | The stop numbers: 7 for 60 marks (mocks 1 and 5), 2 for 20 marks. Only bad marks of round 1 count. | `src/control.py`, 34-35, 571-576 | `STOP_MOCK_1 = 7        # bad marks of 60 that stop mock 1 (decision 0035): more than 6` / `STOP_LATER_MOCK = 2    # bad marks of 20 that stop a later mock (decision 0035)` / `return [m for m in self.marks() if m["round"] == 1 and m["mark"] == "bad"]` / `limit = STOP_MOCK_1 if self.mock in MARK_ALL else STOP_LATER_MOCK` | 1 |
| E31 | The state is then `stopped`, and code refuses each command of the owner. | `src/control.py`, 795-796, 628-629 | `return {"state": "stopped", "waiting_for": ["too many bad marks"]}` / `raise Refused("The mock is %s." % self.state()["state"])` | 1 |
| E32 | Tests: 6 bad marks of 60 do not stop mock 1, 7 do. 2 bad marks stop a later mock. | `tests/test_control.py`, 269-283, 385-392 | `def test_6_bad_marks_do_not_stop_mock_1(self):` / `def test_7_bad_marks_stop_mock_1(self):` / `def test_2_bad_marks_stop_a_later_mock(self):` | 1 |
| E33 | The two stop numbers are guesses with no source. | `docs/decisions/0035-...`, 48 | "**The two numbers that stop a mock.** They are guesses of the assistant. They have no source." | 2 |
| E34 | Why a stop: a bad mark says two things. | `docs/decisions/0021-...`, 24 | "A bad mark says two things: this question is bad, and the checker passed a bad question. The owner reads a sample, so more bad questions can be in the part that the owner did not read." | 2 |
| E35 | Why "only round 1 counts". | `docs/decisions/0039-...`, 77 | "Only the bad marks of round 1 count for the stop limit. This closes an open item of decision 0035." | 2 |
| E36 | Marks come before the findings of step 6. Code refuses a decision on a finding, or a rewrite, while marks wait. | `src/control.py`, 615-616, 645-648; `tests/test_control.py`, 226-232 | "Mark the questions first. Then decide on the findings of step 6." / `raise Refused("Mark the questions first.")` | 1 |
| E37 | The reason: the owner marks first, with no verdict in view. | `docs/decisions/0038-...`, 24 | "The owner marks first, with no verdict in view." | 2 |
| E38 | A `rewrite` is not a bad mark, because the owner saw a verdict before it. | `docs/decisions/0035-...`, 31; `docs/decisions/0037-...`, 58 | "A `rewrite` does not count as a bad mark, because the owner saw a verdict of a checker before the decision." / "A decision that the owner makes after a verdict is not a blind mark." | 2 |
| E39 | Step 8 needs a mark for each question that needs one, and the bad marks below the limit. | `src/control.py`, 754-759; `docs/decisions/0039-...`, 68-69 | `causes.append("a marking file waits for marks")` / `causes.append("the bad marks reached the limit that stops the mock")` | 1 / 2 |
| E40 | State while a file waits: `ready_to_mark`. | `src/control.py`, 822-824 | `return {"state": "ready_to_mark", "waiting_for": ["marks of round %d" % ...]}` | 1 |

### 2.5 Who marked, and who typed the marks (outside the code)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| W1 | The second review is outside the program: no file in `src/` names it. | `grep -rn -i "cowork\|second review" src/` gives no line | (no match) | 1 |
| W2 | Mock 5: the second review marks; the assistant does not wait for marks of the owner and records each mark as a mark of the second review. | `docs/decisions/0071-...`, 21-22 | "Step 7 makes the marking file as before. The assistant sends it to the owner, and the second review in Cowork marks it." / "It records each mark as a mark of the second review, not of the owner, in the commit and in the decision of the mock." | 2 |
| W3 | The assistant typed the marks of the second review into the files of mock 4 round 2 and mock 5 rounds 1 and 2, on the instruction of the owner. | `docs/decisions/0069-...`, 25; `0076-...`, 21; `0077-...`, 21 | "On the instruction of the owner, the assistant typed \"good\" for both in `marking/M4-round2.xlsx` and committed the file. The owner did not read them." / "On the instruction of the owner, the assistant typed them into `marking/M5-round1.xlsx` and committed the file." | 2 |
| W4 | The rule that a filled marking file is committed before anybody else reads it. | `CLAUDE.md` (end-of-session check, item 5); `docs/decisions/0071-...`, 23 | "A marking file that the owner filled is committed before anybody else reads it." / "The rule of the marking file stays: the file is committed before anybody else reads it." | project file / 2 |
| W5 | The owner agreed to mark mocks 1 and 2 only, then marked mock 3 too. | `docs/decisions/0071-...`, 25 | "**The owner agreed to mark mocks 1 and 2 only.** ... The owner marked mock 3 too (decision 0063). The owner did not read the questions of mock 4 (decision 0069)." | 2 |
| W6 | The second review is a Claude model, not a person. | `docs/reviews/M1-round1-second-review-notes.md`, 4 | "Who: an assistant in a Cowork session. It is a Claude model, as the writer and the checkers are. It is not a person." | 4 |
| W7 | `HANDOFF.md` defines Cowork. | `HANDOFF.md`, 25 | "Cowork \| The Claude desktop product that the discussions ran in until 7 October 2026" | 4 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-7-the-owner-marks-the-questions.md`, lines 21-28 (L3). One task statement: 5.5 "Design human review workflows and confidence calibration" (domain 5). The four texts agree with `reference/guide-records.json` (checked by script on 14 October 2026: each guide text, without the backslashes of the records file, is in the table).

| Point | Line | How the step uses it (exact, from the table) |
|---|---|---|
| 5.5-K2 | 25 | "Written for the extraction of data, where a person samples results that the system is sure of. Here: a person marks questions that passed all checks. For mock 1 the owner reads all 60, so that is not a sample." |
| 5.5-S1 | 26 | "The same context. Here: the sample of a later mock has questions from each scenario and each domain." |
| 5.5-K1 | 27 | "Written for the extraction of data. Here: the bad marks are shown for each scenario and each domain, because one total can hide a bad part." |
| 5.5-S2 | 28 | "The same context. Here: a sample below 20 questions comes only after the results are good in each scenario and each domain." |

Guide texts (from `reference/guide-records.json`):
- 5.5-K2: "Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns"
- 5.5-S1: "Implementing stratified random sampling of high-confidence extractions for ongoing error rate measurement and novel pattern detection"
- 5.5-K1: "The risk that aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields"
- 5.5-S2: "Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review"

Points in the diagrams (academy decision 0024 check):
- Diagram 09 (`docs/diagrams/09-...html`, line 232, JSON `stepdata`): popup `owner` 5.5-K2 and 5.5-S1, popup `read` 5.5-K1, popup `later` 5.5-S2. All four are in the table.
- Diagram 01 (`docs/diagrams/01-pipeline-overview.html`, line 191, popup "7"): 5.5-K2, 5.5-S1, 5.5-K1, 5.5-S2. All four are in the table.
- So no point appears only in a diagram. No conflict under academy decision 0024.
- The other points of 5.5 (K3, K4, S3, S4: confidence scores and routing) are not in the table. Decision 0035, line 43: "This design has no confidence number (decision 0032)."

Facts that support each use:
- T1 (5.5-K2, "not a sample"): mocks 1 and 5 put 60 of 60 in round 1 (section 4). So the sample applies only to mocks 2 to 4. Decision 0035, line 43: "The points apply to the 20 questions of a later mock." (L1, L2)
- T2 (5.5-K2, "high-confidence"): the build has no confidence number; "high-confidence" is read as "passed all checks". Diagram 09 popup `owner`: "Here each question in the file passed all checks. So each bad mark shows an error that the checks did not find." (L3)
- T3 (5.5-S1, "each scenario and each domain"): the code draws 5 from each scenario and redraws until each domain is present (E4). The run files agree: each round 1 of mocks 2 to 4 has 5 per scenario and all 5 domains (section 4.3). (L1)
- T4 (5.5-K1): the per-segment count exists only as a print of the command `mark` (E23). No run file keeps it. In the 5 mocks, only mock 5 had bad marks (2, both in scenario 5, domains 3 and 4; section 4.3). (L1)
- T5 (5.5-S2): the rule was never applied. No decision sets a sample below 20. Decision 0035, line 53, left it open: "The owner and the assistant decide the number after mock 3, with real results." The opposite happened: mock 5 went from 20 to 60 questions (decision 0073), and the owner stopped reading from mock 4 (decisions 0069, 0071). (L2)
- T6: decision 0022, line 26, gives 5.5-S2 as "the rule to go lower". Decision 0022, line 28: "Not decided yet: the measure for \"the checker agrees with the marks of the owner\"." (L2)

## 4. Numbers, per mock, with method

### 4.1 Method

Script 1 reads only the run files. It makes no model call. Run: `python3 -I count7.py ~/ccar-f-mock-generator` (copy in the scratchpad of this agent, not in the repository). It ran on 14 October 2026.

```python
import glob, json, os, sys
from collections import Counter
ROOT = sys.argv[1]
def rd(p):
    with open(p, encoding="utf-8") as f: return json.load(f)
for m in range(1, 6):
    F = os.path.join(ROOT, "runs", "mock-%02d" % m)
    for p in sorted(glob.glob(F + "/marking-rounds/round-*.json")):
        r = rd(p); print(r["round"], len(r["question_ids"]), r["date"])      # questions per round
    for p in sorted(glob.glob(F + "/marks/round-*.json")):
        ms = rd(p); print(Counter(x["mark"] for x in ms))                     # good and bad marks
    decs = rd(F + "/owner-decisions.json")
    print(Counter(d["action"] for d in decs))                                 # rewrites
```

Script 2 (sample check) copies `runs/mock-0N/` to a scratch folder, then for each mock: `c = Control(copy, N, plan["seed"], None, {})`, compares `sorted(c.sample())` with the slots of `marking-rounds/round-1.json`, and prints `c.state()`, `c.stop_limit_reached()` and `len(c.bad_marks_first_round())`. No step is called, so no model call. A third run sets `control.MARK_ALL = {1}` before the call, to get the sample of 20 that the old code would give mock 5 (section 4.4).

Script 3 (the 95% limits of decision 0022): for a mock of 60 and a clean sample of n, the largest K bad questions with `comb(60-K, n) / comb(60, n) >= 0.05`.

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Total | File and method |
|---|---|---|---|---|---|---|---|
| Marking rounds | 2 | 2 | 2 | 2 | 2 | 10 | files in `marking-rounds/` |
| Questions in round 1 | 60 | 20 | 20 | 20 | 60 | 180 | `len(question_ids)` of `round-1.json` |
| Questions in round 2 | 9 | 14 | 2 | 2 | 2 | 29 | `len(question_ids)` of `round-2.json` |
| Marks in all | 69 | 34 | 22 | 22 | 62 | 209 | records in `marks/round-*.json` |
| Good marks | 69 | 34 | 22 | 22 | 60 | 207 | `"mark": "good"` |
| Bad marks | 0 | 0 | 0 | 0 | 2 (round 1) | 2 | `"mark": "bad"` |
| Stop limit (round 1 bad marks) | 7 | 2 | 2 | 2 | 7 | | `src/control.py` 34-36, 575 |
| Stop limit reached | no | no | no | no | no (2 of 7) | | script 2 |
| Rewrites of the owner (after the marks) | 9 | 14 | 2 | 2 | 0 | 27 | action `rewrite` in `owner-decisions.json` |
| ... their question had a good mark in round 1 | 9 | 4 | 0 | 2 | 0 | 15 | target `question_id` found in `marks/round-1.json` with `good` |
| Round 2 = the slots sent back (rewrites + bad marks) | yes | yes | yes | yes | yes | | sorted slot IDs equal |
| Reader of round 1 (sources) | the owner, blind (0045 l.10) | the owner (0056 l.10) | the owner (0063 l.10) | not named: "the owner states that they did not read" (0069 l.24) | the second review (0076 l.10, 21) | | decisions |
| Reader of round 2 (sources) | the owner, blind (0046 l.10) | the owner (0059 l.10) | the owner (0063 l.10) | the second review, typed by the assistant (0069 l.25) | the second review, typed by the assistant (0077 l.10, 21) | | decisions |
| Date of the round file / of the marks | 7 Oct / 8 Oct, 8 Oct / 8 Oct | 8 Oct / 8 Oct, 8 Oct / 8 Oct | 8 Oct / 9 Oct, 9 Oct / 9 Oct | 9 Oct / 9 Oct (both rounds) | 9 Oct / 9 Oct (both rounds) | | field `date` |
| Final state | built | built | built | built | built | | script 2, `c.state()` |

Try numbers of the marked questions (field `try` of the marks), round 1: mock 1 {1: 49, 2: 10, 4: 1}; mock 2 {1: 14, 2: 6}; mock 3 {1: 14, 2: 4, 4: 2}; mock 4 {1: 14, 2: 5, 3: 1}; mock 5 {1: 40, 2: 13, 3: 1, 4: 2, 5: 3, 6: 1}.

### 4.3 Checks of the sample (script 2)

| Mock | Round 1 slots equal `sample()` | Per scenario (round 1) | Per domain (round 1) |
|---|---|---|---|
| 1 | yes (60) | 15, 15, 15, 15 | 1:16, 2:11, 3:12, 4:12, 5:9 |
| 2 | yes (20) | 5, 5, 5, 5 (scenarios 3, 4, 5, 6) | 1:3, 2:5, 3:6, 4:3, 5:3 |
| 3 | yes (20) | 5, 5, 5, 5 (scenarios 6, 1, 4, 2) | 1:5, 2:3, 3:5, 4:3, 5:4 |
| 4 | yes (20) | 5, 5, 5, 5 (scenarios 6, 3, 1, 4) | 1:8, 2:3, 3:4, 4:3, 5:2 |
| 5 | yes (60) | 15, 15, 15, 15 | 1:16, 2:11, 3:12, 4:12, 5:9 |

Bad marks by segment (mock 5, round 1, from `runs/mock-05/plan.json`): M5-S33 scenario 5, task statement 3.2 (domain 3); M5-S45 scenario 5, task statement 4.6 (domain 4). So scenario {5: 2}, domain {3: 1, 4: 1}.

### 4.4 Computed facts for the stories

- N1 (counterfactual, decision 0073): with the old code (`MARK_ALL = {1}`) and the same seed 203660, the sample of 20 of mock 5 is M5-S01, S02, S10, S13, S15, S17, S18, S24, S26, S29, S34, S40, S41, S42, S43, S47, S49, S55, S59, S60. Neither M5-S33 nor M5-S45 is in it. So both bad questions of mock 5 were outside the sample that the old code would have selected. (L1, computed)
- N2 (decision 0022, the 95% limits): script 3 gives 11 for a clean sample of 12, 6 for 20, 4 for 30. This agrees with decision 0022, line 24: "a clean sample of 12 permits up to 11 bad questions, a clean sample of 20 permits up to 6, and a clean sample of 30 permits up to 4." (L1 computed / L2)
- N3: in mocks 2 and 3, 12 of the 16 rewrites (10 of 14 and 2 of 2) were of questions outside the sample of 20, so no mark had looked at them. Decision 0062, line 21: "Neither question is in the sample of round 1." (L1 / L2)
- N4: 15 of the 27 rewrites changed a question that had a good mark in round 1 (all 9 of mock 1, 4 of mock 2, 2 of mock 4). (L1)
- N5: the test run (`runs/test-0024/part-b7.json`, field `checks`): 10 marks, 9 good and 1 bad (T-M1-S05). Agrees with the build guide, line 19, and `docs/decisions/0042-...`, 40. (L1)

### 4.5 Order in time (`git log --date=iso`)

| Time (+1100) | Commit | Event |
|---|---|---|
| 2026-10-07 09:41 | `8cc3a24` | Decisions 0015, 0021, 0022, 0035 first committed (their files are dated 6 October 2026). |
| 2026-10-07 12:31 | `326c542` | "Build step 7, the marking file, with tests" (an independent review found 3 serious and 6 minor items). |
| 2026-10-07 19:00 / 19:07 | `61dee25` / `fa48a42` | "The marks of the owner for the test of decision 0042" / "Update the marks of the owner for the test of decision 0042". |
| 2026-10-07 19:22 | `d086206` | Decision 0043 (rule B7) from the bad mark of T-M1-S05. |
| 2026-10-07 22:50 | `07d1c42` | Mock 1: round 1 ready to mark (60). |
| 2026-10-08 10:37 | `209898a` | "Mock 1, round 1: the blind marks of the owner, and the second review" (both files, notes, and the new rule in `CLAUDE.md`). |
| 2026-10-08 10:41 | `72262b1` | Decision 0045: the 7 problems are rewrites. |
| 2026-10-08 10:55 | `c587839` | Mock 1: marks of round 1 read (60 good), 9 rewrites ran, round 2 ready (9). |
| 2026-10-08 11:04 | `f450784`, `c5ec7dd` | Mock 1 round 2: 9 of 9 good; decision 0046. |
| 2026-10-08 16:56 to 20:52 | `d3a8cef` ... `de0aa0c` | Mock 2: round 1 (20 good), decision 0056 and 14 rewrites, round 2 (14 good). |
| 2026-10-08 22:59 to 2026-10-09 10:20 | `fd7b5d1` ... `4011959` | Mock 3: round 1 (20 good), 2 rewrites, round 2 (2 good). |
| 2026-10-09 13:00 | `8026a4a` | Mock 4: round 1 ready (20). |
| 2026-10-09 17:06 | `3fec57e` | "Mock 4: the marks of the owner, round 1, committed before anybody read them". |
| 2026-10-09 17:13 | `f873cf2` | "Mock 4: round 1 read (20 of 20 good); 2 rewrites from the second review". |
| 2026-10-09 17:21 | `15bf377` | "Mock 4: round 2 marks from the second review in Cowork (M4-S09 and M4-S43 good). The owner did not mark this round. The assistant typed the marks on the instruction of the owner." |
| 2026-10-09 17:22 | `a74fccd` | Mock 4 accepted; decisions 0069, 0070, 0071. |
| 2026-10-09 17:33 | `69d6878` | Decision 0073: `MARK_ALL = {1, 5}` and its test; the 4 questions of the stopped run (M5-S01-T1, M5-S02-T1, M5-S02-T2, M5-S03-T1). |
| 2026-10-09 20:33 | `f6f6c79` | "Mock 5: all 60 passed, step 6, marking file of 60 questions". |
| 2026-10-09 22:26 | `21b2dfa` | "Mock 5: round 1 marks of the second review in Cowork (58 good, 2 bad: M5-S33 and M5-S45). The owner did not mark. The assistant typed the marks on the instruction of the owner." |
| 2026-10-09 22:27 | `c92ac13`, `235960a` | Mock 5 round 1 read; decision 0076. |
| 2026-10-09 22:30 / 22:33 | `1d52627` / `00dcc31`, `2422bac` | The 2 rewrites; round 2 marks of the second review (2 good), read. |
| 2026-10-09 22:36 | `f1e0904` | Decision 0077: mock 5 accepted. |

## 5. Stories for the Depth

### 5.1 Story (a): the test run, one bad mark made rule B7 (7 October 2026)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | The owner marked 10 test questions: 9 good, 1 bad. | `docs/build-guide/step-7-...md`, "The test run", 19 | "The owner marked 9 good and 1 bad. The bad mark had a reason, and that reason led to a new rule of step 4." | 3 |
| A2 | The reason of the bad mark (the owner's words, with the owner's typing). | `docs/decisions/0043-...`, Question, 10 | "The question is confusing and needs calrification. I had to read the question more than one time. Use one name for the actor, not 'the subagent' and 'Claude'. Make the sentences shorter. Do not change what the question tests, and do not say directly that the search result is missing." / "No rule of decision 0030 covers it." | 2 |
| A3 | The fix: an instruction to the writer and rule B7 in call 4b. | `docs/decisions/0043-...`, 23 | "\"Each actor has one name in the question, the options and the reasons. A reader understands each sentence at the first reading.\"" | 2 |
| A4 | The owner's marks then tested the new rule: B7 failed T-M1-S05, and also 3 of the 9 good questions, with true findings. | `docs/decisions/0043-...`, 38 | "call 4b with B7 failed T-M1-S05 on B7. It also failed 3 of the 9 questions that the owner marked good, each with a true finding: two names for one actor." | 2 |
| A5 | The assistant first recommended an instruction only; the owner asked if that was enough. | `docs/decisions/0043-...`, How we decided, 42; `docs/journal.md`, 196 | "The assistant first recommended an instruction only. The owner asked if that is enough." | 2 / 4 |

### 5.2 Story (b): mock 1, the blind 60 good and the 7 problems as a set (decision 0045, 8 October 2026)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | The question of decision 0045. | `docs/decisions/0045-...`, Question, 10 | "The owner marked the 60 questions of mock 1 blind: 60 good. A second review by a Claude model after the blind marking found 7 problems of the mock as a set, and wrote them as 7 bad marks into a copy of the marking file. 7 bad marks reach the stop limit of decision 0035 (\"more than 6 bad marks of 60\")." | 2 |
| B2 | The two options. | same, Options, 14-15 | "1. The 7 are bad marks of round 1. The mock stops." / "2. Round 1 is the blind file of the owner (60 good). The 7 are rewrites, which do not count as bad marks." | 2 |
| B3 | The decision: two files; the blind file is round 1. | same, 21 | "The blind file of the owner is round 1: `marking/M1-round1.xlsx`, 60 good, SHA-256 a30c0145b79a727ae34c7a4feafec362e8dd6b59cc483cb8ceb85fe19cd7b0e5. The file with the 7 bad marks is a separate record: `marking/M1-round1-second-review.xlsx`" | 2 |
| B4 | The reason: a bad mark is a blind mark of the owner; steps 3 and 4 did not fail. | same, Reason, 44 | "A bad mark is a blind mark of the owner. ... Here the owner and the second review found each question good on its own, so steps 3 and 4 did not fail. The 7 are problems of the mock as a set." | 2 |
| B5 | The 7 problems: 4 repeats, 1 close copy of a guide sample, 1 "Select 2." with one action, 1 ruling 2. | same, 28-36; `docs/reviews/M1-round1-second-review-notes.md`, 24-32 | table rows M1-S09, S24, S28, S60 (repeats), S30 ("Close copy of sample question 1 of the guide"), S47 ("\"Select 2.\", but the two correct options are one action"), S49 ("Ruling 2") | 2 / 4 |
| B6 | How the second review worked: it marked with the owner's columns hidden, then compared. | `docs/reviews/M1-round1-second-review-notes.md`, 9-14 | "The assistant read the 60 questions with the answer key and the reasons, but with the two columns of the owner hidden." / "So the 7 bad marks in the file are not blind marks of the owner." | 4 |
| B7 | The second review also found all 60 good by the four checks. | same, 18 | "By the four checks of the marking, all 60 questions are good: no wrong answer key, no second correct option, no question that misses its point, no false reason." | 4 |
| B8 | Who proposed what. | `docs/decisions/0045-...`, How we decided, 53; `docs/journal.md`, 141 | "The assistant said that the program applies the stop limit, and suggested option 2. The owner agreed." | 2 / 4 |
| B9 | A second change came with it: a rewrite with no finding of step 6, and a new point that the owner gives. | `docs/decisions/0045-...`, 22-23, 53 | "The owner changed that: the owner gives the point, and code checks three conditions, because a random point can be a twin again" | 2 |
| B10 | The run file agrees: round 1 of mock 1 has 60 good. The 9 rewrites D002 to D010 all name a question with a good mark. 7 come from the second review (D002 to D008), 2 from findings of step 6 (D009 target `M1-SC1-R1-F1`, D010 target `M1-SC2-R1-F1`). | `runs/mock-01/marks/round-1.json`; `runs/mock-01/owner-decisions.json` | D010: "Same scene as S34 (plan mode for a large change). The slot gets the new point 3.4-K4: the Explore subagent." | 1 |
| B11 | Round 2: 9 of 9 good by the owner, blind. The second review found 3 weak questions, and the owner stopped the rewrites. | `docs/decisions/0046-...`, 10, 47 | "After the round of 9 rewrites (decision 0045), the owner marked round 2 blind: 9 of 9 good." / "'I do not want another rewrite round. Record them as known limits of mock 1.'" | 2 |
| B12 | A side story: the blind file was not in git at first. This made the new rule in `CLAUDE.md`. | `docs/journal.md`, 142-143 | "The blind file was not in git: only the empty file of the program was committed. The owner had sent the blind file to the Cowork session before the second review, and it came back from there unchanged" / "A new line in the check at the end of a session in `CLAUDE.md`: a marking file that the owner filled is committed before anybody else reads it." | 4 |
| B13 | Commit `209898a` (8 Oct, 10:37) has both files and the rule; `72262b1` (10:41) has decision 0045. | git | "marking/M1-round1-second-review.xlsx: the same file after a second review by a Claude model, with 7 bad marks. They do not count." | git |
| B14 | Decision 0045 was not checked by an independent reviewer. | `docs/decisions/0045-...`, 55 | "No independent reviewer checked this file." | 2 |

### 5.3 Story (c): mock 4, round 1 that nobody read (decision 0069, 9 October 2026)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| C1 | The question of decision 0069. | `docs/decisions/0069-...`, Question, 10 | "The marking file of round 1 of mock 4 has 20 of 20 good. The second review in Cowork found 2 questions to fix." | 2 |
| C2 | The owner did not read round 1; the marks are recorded as they are. | same, 24 | "**Round 1:** the owner states that they did not read the 20 questions of round 1. The marks in `marking/M4-round1.xlsx` (20 of 20 good) are recorded as they are." | 2 |
| C3 | The second review's 2 findings became rewrites, not bad marks. | same, 21-23; `runs/mock-04/owner-decisions.json` D007, D008 | "Finding of the second review in Cowork (not a mark of the owner): this question copies M3-S19 and repeats M4-S45 in the same scenario." | 2 / 1 |
| C4 | Both rewritten questions have the mark "good" in `runs/mock-04/marks/round-1.json` (M4-S43-T1, M4-S09-T1). | run file | `"mark": "good"` for both | 1 |
| C5 | Round 2: the owner did not mark; the assistant typed the second review's marks. | `docs/decisions/0069-...`, 25 | "The owner did not read them." | 2 |
| C6 | The owner's instruction. | same, How we decided, 41 | "\"Round 2: I do not mark. Use the second review in Cowork as the marks\"" | 2 |
| C7 | The plain reason. | same, Reason, 35 | "Plain reason: nobody read the 20 questions of round 1." | 2 |
| C8 | The commit of the round 1 file calls the marks "the marks of the owner". | git `3fec57e` (17:06) | "Mock 4: the marks of the owner, round 1, committed before anybody read them" | git |
| C9 | The journal of the same day. | `docs/journal.md`, 22 | "Round 1 of mock 4: the marking file has 20 of 20 good. The owner states that they did not read the 20 questions." | 4 |
| C10 | No source names who filled the 20 good marks of round 1 (see conflict X3). | | | |

### 5.4 Story (d): mock 5 is marked by the second review (decision 0071) and all 60 go in the file (decision 0073)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| D1 | The question of 0071. | `docs/decisions/0071-...`, 10 | "Decision 0035 says that the owner marks a sample of 20 questions of each later mock. For mock 4, the owner did not read the questions. Who marks mock 5?" | 2 |
| D2 | The owner's words. | same, How we decided, 33 | "\"For mock 5, I do not mark. Do not wait for my marks. Send me the marking file, and the second review in Cowork marks it.\"" | 2 |
| D3 | Why its marks are recorded as its own. | same, Reason, 29 | "In mock 1, it found 7 problems of the mock as a set that the owner had not marked (decision 0045). So the second review is not the same as the owner, and its marks are recorded as its own." | 2 |
| D4 | The question of 0073, and the owner's words. | `docs/decisions/0073-...`, 10, 33 | "How many questions of mock 5 go in the marking file?" / "The owner said: \"Put all 60 questions of mock 5 in the marking file.\"" | 2 |
| D5 | The reason for 60: the only reader reads all. | same, Reason, 27 | "Plain reason: no person reads the questions of mock 5 (decision 0071). So the second review, as the only reader, reads all of them, not a sample." | 2 |
| D6 | The stop limit for 60 came from mock 1; the owner did not name one. | same, 29 | "The stop limit for 60 marks is the limit of mock 1. The owner did not name a limit. The assistant used the one that the decisions already have for 60 marks." | 2 |
| D7 | The run had started with the old code; the assistant stopped it after 4 questions. | same, 23 | "The run of mock 5 had started with the old code, which picks a sample of 20. The assistant stopped the run after 4 questions, changed the code and started the run again. The control reads its records, so the 4 written questions stay." | 2 |
| D8 | The code change: `self.mock == 1` became `self.mock in MARK_ALL` in `sample` and in `stop_limit_reached`, with one new test. | `git show 69d6878 -- src/control.py tests/test_control.py` | `-        if self.mock == 1:` / `+        if self.mock in MARK_ALL:` | 1 |
| D9 | The result: 58 good, 2 bad, both in scenario 5. | `runs/mock-05/marks/round-1.json`; `docs/decisions/0076-...`, 10 | "The second review in Cowork marked all 60 questions of mock 5 (decisions 0071 and 0073): 58 good, 2 bad." | 1 / 2 |
| D10 | The two reasons, exact. | `runs/mock-05/marks/round-1.json`, records with `"mark": "bad"` (lines 293 and 401) | M5-S33-T1: "Copy of M2-S34: a CI test-generation skill ran a Bash command that deleted a fixture directory, the answer is allowed-tools, and the three wrong options are the same (context: fork, argument-hint, a CLAUDE.md rule). Keep point 3.2-K2, but make a different frontmatter field the answer, for example context: fork or argument-hint." M5-S45-T3: "Repeat of M5-S41 in the same scenario: both answers are 'the same session keeps its reasoning'. It also misses its point 4.6-S3. Keep the point. ..." | 1 |
| D11 | Below the stop limit. | `docs/decisions/0076-...`, 28 | "2 bad marks of 60 are below the stop limit of decision 0073 (more than 6)." | 2 |
| D12 | Both bad questions were outside the sample of 20 that the old code would have selected (N1). With a sample of 20, no mark would have reached them. | computed, section 4.4 | | 1 (computed) |
| D13 | After the 2 bad marks: each slot went back to the writer with the reason (E27). Round 2 had M5-S33-T2 and M5-S45-T5; the second review found both good. | `runs/mock-05/marking-rounds/round-2.json`; `docs/decisions/0077-...`, 10 | "The second review marked round 2 of mock 5: M5-S33 and M5-S45 good." | 1 / 2 |
| D14 | These are the only 2 bad marks of the 5 mocks, and the only marks that used the path "bad mark to step 5" in a mock. | section 4.2 | | 1 |
| D15 | The build guide tells participants that no person reads mocks 4 and 5. | `docs/decisions/0071-...`, 24; `docs/portal-notes.md`, 7 | "The build guide says this to the participants." | 2 / 4 |

### 5.5 Story (e): the sample (decisions 0022, 0073)

| # | Fact | Source | Exact quote | L |
|---|---|---|---|---|
| S1 | The size 20 came from arithmetic, not a guess. | `docs/decisions/0022-...`, Reason, 24 | "A sample with zero bad marks still permits bad questions in the part that the owner did not read. ... a clean sample of 20 permits up to 6" | 2 |
| S2 | The number agrees with a recomputation (N2). | script 3 | | 1 (computed) |
| S3 | The rule to go lower was never measured or applied (T5, T6). | `docs/decisions/0035-...`, 53 | "The owner and the assistant decide the number after mock 3, with real results." | 2 |
| S4 | The sample clean in mocks 2 to 4, but problems were found outside it by other means: 12 of 16 rewrites of mocks 2 and 3 were outside the sample (N3). | run files; `docs/decisions/0056-...`, 10; `0062-...`, 10, 21 | "A second review and an independent agent compared the 60 questions of mock 2 with the 60 of mock 1." / "An independent agent compared the 60 questions of mock 3 with mocks 1 and 2" | 1 / 2 |
| S5 | The mock 5 counterfactual (N1, D12). | computed | | 1 (computed) |
| S6 | Problems of the set get past a mark: 15 of 27 rewrites changed a question with a good mark (N4). The decisions name the reason: the marks judge each question on its own. | run files; `docs/decisions/0045-...`, 44 | "the owner and the second review found each question good on its own" | 1 / 2 |

### 5.6 Story (f): the build of step 7, sorting could move a mark (7 October 2026)

| # | Fact | Source | Exact quote | L |
|---|---|---|---|---|
| F1 | An independent reviewer of the code found that sorting one column moves marks to the wrong questions. The fix: a protected sheet. | `docs/journal.md`, 188 | "The main one: an owner who sorts only the column \"Mark\" moves marks to the wrong questions, and code cannot see it later. The sheet is now protected with no password, so only the two columns of the owner can change and sorting is off. This is not checked in real Excel." | 4 |
| F2 | The code of the fix. | `src/step7_marking.py`, 101-106 | (see E14) | 1 |
| F3 | Commit. | git `326c542` | "An independent review found 3 serious and 6 minor items. They are fixed. The control now names each cause of a bad marking file." | git |
| F4 | Still not checked in real Excel. | `docs/journal.md`, 207 | "The protection of the marking file is not checked in real Excel." | 4 |

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/control.py` | 33-36 | The four constants: 20, the stop numbers 7 and 2, `MARK_ALL = {1, 5}`. |
| `src/control.py` | 481-498 | `sample`: 5 per scenario at random with a seed, redrawn until each domain is in. |
| `src/control.py` | 500-517 | `to_mark`: the sample, plus each slot that a rewrite or a bad mark sent back. |
| `src/control.py` | 527-541 | `_make_marking_round`: when a round is made, and the round record with fingerprints. |
| `src/control.py` | 543-569 | `read_marks`: refuses an incomplete file and names each row, then saves the marks record. |
| `src/control.py` | 171-173 | A bad mark is a send-back event. |
| `src/control.py` | 244-248 | After a bad mark: request of step 5, the reason as a finding with rule "owner". |
| `src/control.py` | 571-576 | Only round 1 counts; the limit depends on `MARK_ALL`. |
| `src/control.py` | 795-796 | The state `stopped` after too many bad marks. |
| `src/control.py` | 615-616, 645-648 | Marks come first, then the findings of step 6 and rewrites. |
| `src/step7_marking.py` | 1-9 | The docstring: what the step does and does not do. |
| `src/step7_marking.py` | 20-22 | The 15 columns. |
| `src/step7_marking.py` | 101-117 | The protected sheet and the list "good, bad". |
| `src/step7_marking.py` | 158-167 | Bad marks for each scenario and each domain (5.5-K1). |
| `src/run.py` | 93-96 | The command `mark`, and the print of the bad marks by segment. |
| `tests/test_step7_marking.py` | 71-78 | The file shows no verdict. |
| `tests/test_control.py` | 238-256 | A bad mark, step 5 with the reason, and round 2 with only the new question. |
| `tests/test_control.py` | 269-283, 385-392 | 6 bad of 60 do not stop, 7 stop; 2 of 20 stop. |
| `tests/test_control.py` | 473-478 | Decision 0073: mock 5 samples 60, mock 4 samples 20. |
| `git show 69d6878 -- src/control.py` | | The diff of decision 0073 (3 changed lines and the constant). |
| `runs/mock-05/marks/round-1.json` | 290-298 (M5-S33-T1), 398-406 (M5-S45-T3) | Two real bad marks with their reasons. |
| `runs/mock-01/owner-decisions.json` | D002 to D008 | The 7 problems of the second review as rewrites. |

## 7. A figure

The mechanism (boxes and arrows with verbs):

1. [60 questions that passed steps 3, 4 and 6] --code selects--> (all 60 for mocks 1 and 5 / 20 for mocks 2 to 4, 5 per scenario, each domain) --code writes--> [marking file `Mx-roundN.xlsx`: question, point, options, correct answer, reasons; no verdict]
2. [marking file] --a reader fills "Mark" and "Reason"--> (the owner: mocks 1 to 3; the second review, a Claude model: mocks 4 and 5, typed by the assistant) --committed before anybody else reads it-->
3. --the command `mark`: code reads and checks--> (refuses a missing mark or a bad mark with no reason) --code saves--> [`runs/mock-0N/marks/round-N.json`]
4. Three exits: all good --> the owner decides the findings of step 6 --> `accept` --> step 8. / bad --> step 5 (reason = finding, rule "owner") --> steps 3, 4, 6 --> a new round with only the new question. / too many bad in round 1 (7 of 60, 2 of 20) --> mock `stopped`.
5. A side panel with the real counts: 10 rounds, 209 marks, 207 good, 2 bad (mock 5).

Facts behind each label: "code selects" E3-E5; "no verdict" E10; "a reader fills" E9, O2, W3; "committed before anybody else reads it" W4; "code reads and checks" E18-E20; "code saves" E21; "bad --> step 5" E26-E28; "too many" E30-E31; "all good --> findings --> accept" E36, E39; counts section 4.2.

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| X1 | Who does step 7 (known; academy decision 0034 is the answer for tab 2, status "proposed"). | `docs/build-guide/README.md`, 21: "7. The owner marks the questions" (L3). `docs/diagrams/01-pipeline-overview.html`, 110: legend "The owner" = "a person" (L3). `docs/diagrams/09-...html`, 188: "Step 7: a person is the last check"; 210: the box label "The owner" (L3). `src/step7_marking.py`, 5: "The owner fills two columns" (L1). | `docs/decisions/0071-...`, 24: "no person reads the questions of mocks 4 and 5." (L2). Build guide step 7, 9: "For mocks 4 and 5 it is the second review in Cowork, also a Claude model" (L3). |
| X2 | What happens after too many bad marks. | `docs/diagrams/09-...html`, 232, popup `stop`: "The mock is not released. We correct the rules of the checker. Then all 60 questions go through the checks again." (L3). `docs/decisions/0021-...`, 20 (same, L2). | `src/control.py`, 795-796 and 628-629: the state is `stopped`, and code refuses each decision. No code checks the 60 again (L1). `docs/decisions/0035-...`, 55-57: "Not decided yet: ... What \"we correct the rules of the checker\" means as a procedure. ... How \"all 60 questions go through the checks again\" works after a stop" (L2). |
| X3 | Who gave the 20 good marks of round 1 of mock 4. | Build guide step 7, 9: for mocks 4 and 5 the reader "is the second review in Cowork" (L3). `HANDOFF.md`, 69: "The second review in Cowork, a Claude model, marked mocks 4 and 5" (L4). `docs/decisions/0071-...`, 29: "The second review marked the rounds of mocks 1 to 4." (L2) | `docs/decisions/0069-...`, 24: "the owner states that they did not read the 20 questions of round 1. The marks ... (20 of 20 good) are recorded as they are." (L2). Git `3fec57e`: "Mock 4: the marks of the owner, round 1". The second review found M4-S43-T1 and M4-S09-T1 to fix, but both have `"mark": "good"` in `runs/mock-04/marks/round-1.json` (L1). No source names who typed the 20 marks. |
| X4 | The words "the owner marked" in decision 0069 itself. | `docs/decisions/0069-...`, 37: "In the 20 questions that the owner marked, B was never correct." | same decision, 24: "the owner states that they did not read the 20 questions of round 1." |
| X5 | Which mocks mark all 60, inside the code. | `src/control.py`, 482-483, docstring of `sample`: "Mock 1: all 60. A later mock: 20, 5 from each scenario, with each domain." Also line 34 comment: "bad marks of 60 that stop mock 1". | `src/control.py`, 36: `MARK_ALL = {1, 5}`, used in 485 and 575. Run file: mock 5 round 1 has 60 questions. |
| X6 | Where the second review's 7 bad marks of mock 1 are. | `docs/reviews/M1-round1-second-review-notes.md`, 5: "File with the marks: `M1-round1.xlsx`. The owner asked for the same file name, so it replaces the marking file." (L4) | `docs/decisions/0045-...`, 21: "The file with the 7 bad marks is a separate record: `marking/M1-round1-second-review.xlsx`" (L2). `docs/journal.md`, 142 agrees with 0045. `ls marking/` shows both files. |
| X7 | Does code compare the marks with the verdicts? | `docs/decisions/0015-...`, 21: "Code then compares the marks with the verdicts, and shows the result for each scenario and each domain." (L2; status line "accepted", names no later decision) | `docs/decisions/0035-...`, 23 (later): "It does not compare the marks with the verdicts in this step." (L2). Code: no such comparison (L1). |
| X8 | "The owner fills two columns" in the build guide. | `docs/build-guide/step-7-...md`, 11: "The owner fills two columns: \"good\" or \"bad\", and a reason for a bad mark." (L3) | `docs/decisions/0069-...`, 25; `0076-...`, 21; `0077-...`, 21: the assistant typed the marks of the second review for mock 4 round 2 and mock 5 rounds 1 and 2 (L2). |
| X9 | Who the reader of mock 2 round 1 was compared with. | `docs/decisions/0071-...`, 29: "In mocks 2 and 3, its marks agreed with the owner's marks." (L2) | `docs/decisions/0056-...`, 10: after the owner's 20 of 20 good, a second review and an independent agent found 17 repeats of mock 1 (L2). 3 of the rewritten repeats (M2-S08, M2-S32, M2-S59) had a good mark of the owner in round 1 (L1). No run file or review file has the marks of the second review for mock 2 round 1. |
| X10 | What follows "all marks good" in diagram 09. | `docs/diagrams/09-...html`, 218-219, segment "No bad mark": "Step 8 builds the files." (L3) | `src/control.py`, 752-757, 765-771: step 8 needs the findings of step 6 decided and the command `accept` (L1). The popup `good` of the same diagram says this. An omission in the visible label, not a direct contradiction. |

## 9. Not found

1. Who typed the 20 good marks of round 1 of mock 4 (X3). The marks record has no field for the marker (E21).
2. The marks of the second review for mock 2 round 1 and mock 3 round 1. Decision 0071, line 29 says it "marked the rounds of mocks 1 to 4", but only mock 1 round 1 has notes (`docs/reviews/M1-round1-second-review-notes.md`) and mock 1 round 2 has a summary (`docs/reviews/M1-round2-second-review.md`).
3. A comparison of the checker with the marks ("with them we can test the checker", decisions 0022 line 24, 0035 line 49, diagram 09 popup `m1`). No decision, review or script does it for mocks 1 to 5. The only use of the owner's marks to test a checker is the test run (decision 0043, line 38: B7 against the 10 test marks).
4. A decision on a sample below 20 (5.5-S2, T5). Open since decision 0035, line 53.
5. A procedure after a stop by too many bad marks (X2). No mock reached it (most: 2 of 60, mock 5).
6. A run file with the bad marks by segment: the command `mark` only prints them (E23).
7. Text of the second review's process for mocks 4 and 5 (how it read, what it saw). No review file exists for those rounds; the decisions give only the results.
8. The content of the Excel files was not read (working rules and the task). The marks come from `runs/mock-0N/marks/`. The SHA-256 values of the files in decision 0045 and the journal were not checked.
9. `docs/lessons.md` has no entry on step 7 of this build. Its lines 19, 28 and 107-108 are about the first build ("A person found it, not the verifier").
10. A product fact on Cowork in the Anthropic documentation (academy decision 0014). Only `HANDOFF.md`, 25 defines it. Not checked.
11. Why the test marking file was committed two times (`61dee25` "The marks of the owner for the test of decision 0042" and `fa48a42` "Update the marks of the owner"). No source says what changed.
