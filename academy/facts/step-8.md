# Fact sheet: tab 2, step 8 "Build the files"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `5debc46` (branch `main`). Before this file, the only untracked file was `academy/facts/step-7.md` (another agent).
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`, `docs/portal-notes.md`. "L" = level of trust. "(computed)" = this agent ran a script that reads files (section 4.1).
- A path such as `docs/decisions/0036-...md` means the one file in `docs/decisions/` whose name starts with `0036-`.
- Line numbers are for the files at commit `5debc46`. The files of `src/`, `tests/`, `runs/`, `mocks/` and `docs/` that this sheet cites did not change after `a3c5414`.
- The tests ran on 14 October 2026 with no API key in the environment: `env -u ANTHROPIC_API_KEY python3 -m unittest discover -s tests` gives "Ran 228 tests in 16.242s" / "OK". `tests/test_step8_build_files.py` has 17 tests (`grep -c "def test"`).
- Files that this agent did not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, all personal files of the owner, `claude-code-brand-kit/`, conversation transcripts. No model call. `src/run.py` was not run.
- No Anthropic documentation page was needed: step 8 makes no model call and uses no product feature (section 3).

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | Code builds the two files of a mock, only from the plan, the question records and the guide records. Nobody edits the files by hand. | `src/step8_build_files.py`, 1-6 | "Step 8 of the pipeline: code builds the two files of a mock (decisions 0016 and 0036)." / "The step builds the files only from the plan, the question records and the guide records. Nobody edits the files by hand. The step does not write over files that exist." | 1 |
| O2 | The two files: questions with no answers, and answers with reasons. | `src/step8_build_files.py`, 8-9 | "mocks/mock-01.questions.json   the 60 questions, with no answers and no reasons" / "mocks/mock-01.answers.json     the correct letters, and the reason of each option" | 1 |
| O3 | It starts only on the command `accept` of the owner, and only when the conditions hold. | `src/control.py`, 765-766; `src/run.py`, 10 | `def accept(self, reason=""):` / "Command of the owner: accept the mock. Code checks the conditions, then step 8 builds." / "python3 src/run.py accept --mock 1              step 8 builds the files, if the conditions hold" | 1 |
| O4 | The first decision of the step: one true copy. | `docs/decisions/0016-...md`, 19 | "The stored question records are the one true copy. Code builds the mock file and the answer key from them. Nobody edits an output file by hand. To change a question, change its record, and code builds the files again." | 2 |
| O5 | The build guide summary. | `docs/build-guide/step-8-build-the-files.md`, 9 | "Code builds the two files of a mock from the stored question records. Nobody edits the files by hand. To change a question, the record changes, and code builds the files again." | 3 |
| O6 | Status: built; built mocks 1 to 5, 8 to 9 October 2026. It is the last step. | `docs/build-guide/step-8-build-the-files.md`, 3; `docs/diagrams/10-step-8-build-the-files.html`, 234 | "Status: built. It built mocks 1 to 5, from 8 to 9 October 2026." / "This is the last step." | 3 |
| O7 | Step 8 makes no model call. No usage record is written by `accept` (only `run` saves the cost). | `src/run.py`, 86-90 (`save_cost` only under `run`), 104-105; `src/steps.py`, 97-101 | `elif a.command == "accept":` / `show(c.accept(a.reason))` / `return step8_build_files.build(plan, questions, self.records, self.mocks_folder, self.today())` | 1 |

## 2. Explanation facts: the mechanism

### 2.1 The command

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | The owner types `accept`, with an optional `--reason`. | `src/run.py`, 73, 78, 104-105 | `p.add_argument("command", choices=["run", "report", "mark", "decide", "accept"])` / `p.add_argument("--reason", default="")` | 1 |
| E2 | A refusal prints "Refused: ..." and exits with 1. | `src/run.py`, 106-108 | `except Refused as e:` / `print("Refused: %s" % e)` / `return 1` | 1 |
| E3 | The report says "accept the mock" when only the accept is left. | `src/control.py`, 830-831 | `waiting.append("accept the mock")` | 1 |
| E4 | `accept` is refused when the mock is `stopped` or already `built`. | `src/control.py`, 767-768 | `if self.state()["state"] in ("stopped", "built"):` / `raise Refused("The mock is %s." % self.state()["state"])` | 1 |
| E5 | The order inside `accept`: conditions, then the build, then the decision `accept`, then `build.json`, then the report. | `src/control.py`, 769-781 | `causes = self.build_conditions()` ... `files = self.steps.build(self.plan(), questions)` ... `"action": "accept"` ... `self._write_new({"files": files, "fingerprints": ...}, "build.json")` / `return self.report()` | 1 |
| E6 | The decision `accept` is saved only after the build. A failed build saves no accept. | `docs/decisions/0039-...md`, 33, 91; `tests/test_control.py`, 601-611 | "Code saves it only after step 8 built the files." / "7. Code saves the decision `accept` only after step 8 built the files." / `def test_a_build_that_fails_saves_no_accept(self):` | 2 / 1 |
| E7 | After the build, the mock is `built`, and code refuses each later decision. | `src/control.py`, 791-792, 628-629; `tests/test_control.py`, 586-592 | `if self._exists("build.json"):` / `return {"state": "built", "waiting_for": []}` / `self.assertIn("The mock is built", str(e.exception))` | 1 |
| E8 | The real accept records of the 5 mocks. | `runs/mock-01/owner-decisions.json`, 347 (D044); `runs/mock-02/...`, 193 (D024); `runs/mock-03/...`, 132 (D018); `runs/mock-04/...`, 193 (D026); `runs/mock-05/...`, 154 (D021) | mock 1: `"reason": "The owner accepts mock 1 with the known limits of decision 0046."`, `"date": "2026-10-08"`. Mocks 2 to 5: `"reason": ""`. | 1 |

### 2.2 The six conditions (code checks them first)

The decision text (`docs/decisions/0039-...md`, 63-72, L2; the same in `docs/decisions/0036-...md`, 35-41):

> 1. Each of the 60 questions passed steps 3 and 4, and no question changed after its checks (the fingerprint).
> 2. Step 6 checked the current questions of each scenario.
> 3. Each finding of step 6 has a decision of the owner.
> 4. Each question that needs a mark has a mark. A bad mark sends the slot back, so the mark of each current question is `good`.
> 5. The bad marks are below the stop limit.
> 6. No call failed in the last run.
>
> If a condition is false, code builds no file and lists the causes.

The code (`src/control.py`, 733-763, `build_conditions`, L1), each cause text exact:

| Cond. | Code lines | Cause text in the code |
|---|---|---|
| 1 | 736-740 | `"%s: the status is %s"` (a slot that is not `passed`) |
| 1 | 741-746 | `"%s: no valid pass of step %d"` (no verdict `pass` of step 3 or 4, or `v["fingerprint"] != fp`) |
| 2 | 748-751 | `"scenario %s: step 6 did not check the current questions"` (`_step6_current`, 410-420: `return last if last["fingerprints"] == now else None`) |
| 3 | 752-753 | `"%s: the finding of step 6 has no decision"` |
| 4 | 754-755 | `"a marking file waits for marks"` |
| 4 | 756-757 | `"%s: no mark"` (`to_mark`, 500-517: a mark counts only with the same fingerprint: `if (q["question_id"], fingerprint(q)) not in marked:`) |
| 5 | 758-759 | `"the bad marks reached the limit that stops the mock"` (`stop_limit_reached`, 574-576; limits 7 of 60 for mocks 1 and 5, 2 of 20 for the other mocks, lines 34-36) |
| 6 | 760-762 | `"%s: a call failed 3 times"` (errors of the last run) |
| all | 770-771 | `raise Refused("Step 8 cannot start: " + "; ".join(causes))` |

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| C-a | Conditions 2, 3 and 4 are checked only when condition 1 gives no cause. So with a slot that is not passed, the list does not show the step 6 and mark causes. (Reading of the code; not in a decision.) | `src/control.py`, 747 | `if not causes:` | 1 |
| C-b | Tests of the conditions: no accept before the marks; no accept with an open finding; a record that changed after its check stops the build; 2 bad marks stop a later mock. | `tests/test_control.py`, 366-373, 375-383, 394-407, 385-392 | `self.assertIn("a marking file waits for marks", ...)` / `self.assertIn("M2-SC1-R1-F1: the finding of step 6 has no decision", ...)` / `self.assertIn("M2-S30-T1: no valid pass of step 3", ...)` / `self.assertEqual(self.steps.builds, [])` | 1 |
| C-c | A test runs the whole pipeline with a fake client, from the plan to the two files, and ends with `accept`. | `tests/test_model_steps.py`, 468-505; `docs/journal.md`, 191 | `self.assertEqual(c.accept()["state"], "built")` / "A test runs the whole pipeline with a fake client, from the plan to the two files." | 1 / 4 |

### 2.3 The last checks inside step 8 (beyond the six conditions)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | A last check of each record against its slot, "before a participant sees the file". | `src/step8_build_files.py`, 24-46 | "The record must agree with its slot. The control already checked steps 3 and 4 and the fingerprints. This is a last check before a participant sees the file." | 1 |
| B2 | What it checks: status `written`; the question belongs to the slot; a text; the number of options; each option complete; letters A to E in sequence; the number of correct options; `select` of the slot. | `src/step8_build_files.py`, 28-46 | `"%s has no written question."` / `"%s: the question %s does not belong to the slot."` / `"%s: the question does not have %d options."` / `"%s: the question does not have %d correct options."` | 1 |
| B3 | The 60 records must agree with the 60 slots, the slots must be in sequence 1 to 60, and the groups must agree with the scenarios of the plan. | `src/step8_build_files.py`, 52-57, 71-72, 85-86 | `"The questions do not agree with the 60 slots of the plan."` / `"The slots are not in the sequence 1 to 60."` / `"The groups do not agree with the scenarios of the plan."` | 1 |
| B4 | The step never writes over a file that exists. | `src/step8_build_files.py`, 63-65; `tests/test_step8_build_files.py`, 88-91 | `raise BuildError("The file exists already: %s" % p)` / `def test_no_file_is_written_over(self):` | 1 |
| B5 | Both files are written under a temporary name first, so a failure leaves no half mock. | `src/step8_build_files.py`, 91-105; `tests/test_step8_build_files.py`, 146-162 | "Write both files first with a temporary name. Only when both exist, give them their names. So a failure leaves no half mock." | 1 |
| B6 | A `BuildError` reaches the owner as a refusal. | `src/steps.py`, 97-101 | `except step8_build_files.BuildError as e:` / `raise Refused(str(e))` | 1 |

### 2.4 The two files and their fields

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| F1 | Questions file, top fields: `mock`, `guide_version`, `seed`, `date`, `minutes`, `groups`. | `src/step8_build_files.py`, 88-89 | `questions_file = {"mock": mock, "guide_version": plan["guide_version"], "seed": plan["seed"], "date": date, "minutes": MINUTES, "groups": groups}` | 1 |
| F2 | `minutes` is 120, from decision 0003. | `src/step8_build_files.py`, 17; `docs/decisions/0003-...md`, 22 | `MINUTES = 120   # decision 0003` / "60 questions and 120 minutes." | 1 / 2 |
| F3 | A group: `scenario`, `name`, `story`, `questions`. A new group starts when the scenario changes. | `src/step8_build_files.py`, 73-75 | `groups.append({"scenario": sc["id"], "name": sc["name"], "story": sc["story"], "questions": []})` | 1 |
| F4 | A question: `number`, `question_id`, `domain`, `task_statement`, `point`, `type`, `select`, `question`, `options` (each `letter`, `text` only). | `src/step8_build_files.py`, 76-80; `tests/test_step8_build_files.py`, 71-77 | `"options": [{"letter": o["letter"], "text": o["text"]} for o in q["options"]]` / `self.assertEqual(set(q["options"][0]), {"letter", "text"})` | 1 |
| F5 | The point comes from the record if it has one (a `new_point` decision), else from the slot. Domain, task statement, type and `select` come from the slot and the guide records. | `src/step8_build_files.py`, 77-79; `tests/test_step8_build_files.py`, 164-167 | `"point": q.get("point", slot["point"])` / `def test_the_point_of_a_new_point_decision_is_used(self):` | 1 |
| F6 | Answers file: `mock`, `answers`; each answer `number`, `question_id`, `correct` (the letters), `options` (each `letter`, `correct`, `reason`). | `src/step8_build_files.py`, 81-84, 90 | `"correct": [o["letter"] for o in q["options"] if o["correct"]]` / `answers_file = {"mock": mock, "answers": answers}` | 1 |
| F7 | A test proves the questions file has no answers. | `tests/test_step8_build_files.py`, 54-59 | `self.assertNotIn('"correct"', text)` / `self.assertNotIn('"reason"', text)` | 1 |
| F8 | The exact field names were not decided in decision 0036. The code chose them. | `src/step8_build_files.py`, 11-12; `docs/decisions/0036-...md`, 67 | "The exact field names were not decided in decision 0036. These are the names that the code uses." / "The exact names of the fields in the two files." (under "Not decided yet") | 1 / 2 |
| F9 | The sequence: the slot number is the question number; step 1 sets the sequence. | `docs/decisions/0036-...md`, 33; `src/step1_plan.py`, 427-435 | "The plan of step 1 sets the sequence: the slot number is the question number" / "7. The slots get the numbers 1 to 60, group by group. The seed sets the sequence inside a group." | 2 / 1 |
| F10 | Why two files: the portal can send the questions with no answers in the same file. | `docs/decisions/0036-...md`, 56 | "Plain reason: the portal can send the questions to a participant with no answers in the same file." | 2 |
| F11 | Our own format; the portal format and the converter are not known. No converter exists in `src/` (search "convert": no match). | `docs/decisions/0036-...md`, 45, 62, 66; `HANDOFF.md`, 129, 160 | "The two files have our own format. A converter for the portal comes later, when the format of the portal is known." / "Plain reason: the pipeline does not wait for the portal, and a converter is a small step." / "Not known. Step 8 writes our own two files. A converter comes later (decision 0036)." | 2 / 4 |
| F12 | The portal notes for the people who put the mocks on the portal (5 notes, one on the files). | `docs/portal-notes.md`, 3, 5, 9 | "The format of the portal is not known yet (decision 0036)." / "**Random order of the options.** Show the options of each question in a random order on each attempt. The correct letters in mocks 1 to 4 are not balanced (decision 0070). The converter must keep the link between each option and its reason." | 4 |

### 2.5 The fingerprints and `build.json`

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| P1 | The fingerprint: SHA-256 of what a participant sees, as JSON with sorted keys, in UTF-8. Fields: question ID, question, `select`, and each option as letter, text, mark, reason. | `src/control.py`, 52-66 | `"""SHA-256 of what a participant sees (decision 0036).` / `The fields are written as JSON with sorted keys, in UTF-8 (decision 0039).` / `[o.get("letter"), o.get("text"), o.get("correct"), o.get("reason")]` / `return hashlib.sha256(text.encode("utf-8")).hexdigest()` | 1 |
| P2 | The design: 64 characters; date and model not in it; each check saves one; step 8 compares; a different fingerprint stops the build. | `docs/decisions/0036-...md`, 44 | "A fingerprint is a code of 64 characters that code calculates from the text of the record. The method is SHA-256. ... The date and the model are not in it, because they do not change what a participant sees. ... Step 8 calculates the fingerprint of each record again and compares. A different fingerprint stops the build. Then the record must pass the checks again." | 2 |
| P3 | Where the fingerprints are saved: the verdicts of steps 3 and 4 (`fingerprint`), the record of step 6 (`fingerprints`, one for each of 15 questions), each mark (`fingerprint`), each marking round (`fingerprints`). | `src/control.py`, 394-401, 410-420, 500-517; `docs/decisions/0036-...md`, 44; `docs/decisions/0039-...md`, 107 | "It adds the field `fingerprint` to the verdict records of steps 3 and 4 and to each mark, and the field `fingerprints`, one for each question, to the record of step 6" | 1 / 2 |
| P4 | `build.json` has `files`, `fingerprints` (one for each of the 60 questions) and `date`. It is written as a new record, never over an old one. | `src/control.py`, 778-780, 94-99; `docs/decisions/0039-...md`, 112 | `self._write_new({"files": files, "fingerprints": {q["question_id"]: fingerprint(q) for q in questions}, "date": self.today()}, "build.json")` / "`build.json` \| The files that step 8 built, and the fingerprints" | 1 / 2 |
| P5 | A real `build.json`. | `runs/mock-01/build.json`, 1-8, 66-68 | `"M1-S01-T1": "07e2e91762b4effff6cc390aaa1400225ee090c407116707adad04c7fc5cc6fd"` / `"date": "2026-10-08"` | 1 |
| P6 | Why a fingerprint: a rule alone does not make sure that nobody edits a record. | `docs/decisions/0036-...md`, 61 | "Decision 0016 says that nobody edits a file by hand. A rule alone does not make sure of that. The plain reason for the fingerprint: code can prove that the question in the mock is the question that the checks saw." | 2 |
| P7 | The comparison is in the control (`build_conditions`), before step 8 runs; `step8_build_files.py` does not calculate a fingerprint. | `src/control.py`, 741-746; `src/step8_build_files.py`, 25-26 | `fp = fingerprint(q)` / "The control already checked steps 3 and 4 and the fingerprints." | 1 |
| P8 | The fingerprint does not cover the `point`, `slot_id` or `status` of a record. The files take `point` from the record (F5). So a change of only the point after the checks would not change the fingerprint. (Reading of the code; no source discusses it.) | `src/control.py`, 58-63; `src/step8_build_files.py`, 78 | `data = {"question_id": ..., "question": ..., "select": ..., "options": [...]}` | 1 |
| P9 | `build.json` stored absolute paths of this computer. On 14 October 2026 the paths became paths from the root of the repository (academy decision 0039, item 20), so the quote now shows the new path. | `runs/mock-01/build.json`, 2-5 (same in mocks 2 to 5) | `"mocks/mock-01.questions.json"` | 1 |

## 3. Task statements and points of the step

Source: `docs/build-guide/step-8-build-the-files.md`, 25-33 (L3), academy decision 0024.

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| T1 | The table says: no point of a task statement; three facts of the exam form. | `docs/build-guide/step-8-build-the-files.md`, 27 | "The step uses no point of a task statement. It uses three facts of the exam form." | 3 |
| T2 | Decision 0036 agrees: no points, only Sections 3 and 5. | `docs/decisions/0036-...md`, 78-80 | "none. The decision uses Sections 3 and 5 of the guide." | 2 |
| T3 | Decision 0016 gives the reason in words: no point gives it, the reason is plain. | `docs/decisions/0016-...md`, 23, 31-33 | "No exam guide point gives this reason. The reason is plain. If a question exists in two places and a person can edit one of them, the two can disagree, and nobody knows which one the checks saw. With one true copy and files that code builds from it, a question in a mock is always the question that passed the checks." / "none" | 2 |
| T4 | Diagram 01 agrees. | `docs/diagrams/01-pipeline-overview.html`, 191 (JSON `stepdata`, key "8") | `"points": []` / `"ts": "Exam guide: no point. Plain engineering reason."` | 3 |
| T5 | Diagram 10 cites only the Sections, each marked "not a task statement point". | `docs/diagrams/10-step-8-build-the-files.html`, 284 (JSON `stepdata`, keys `qfile`, `seq`, `domains`) | `"ctx": "A fact about the exam. It is not a task statement point."` | 3 |
| T6 | An independent reviewer checked the "does not cover" claim of 0016. | `docs/reviews/review-decisions-0003-to-0018.md`, 101 | "**0003, 0015, 0016:** the \"does not cover\" statements are true. I found no point on the number of multiple-response items, on questions per scenario, on blind marking, or on one true copy." | 4 |
| T7 | The page heading "no task statement of the exam guide" agrees with T1 to T6. | `academy/pages/behind-the-mocks.html`, 240, part `#step-8` | "code, after the owner accepts the mock · no task statement of the exam guide" | (page) |

The three facts of the exam form (table rows, exact; each checked against `reference/exam-guide.md` by grep):

| Section | Line of the table | Text of the guide | Where in `reference/exam-guide.md` | How the step uses it (exact, from the table) | In the code |
|---|---|---|---|---|---|
| 3 | 31 | "each item states how many responses to select" | 41 ("Item format" row) | "Each question has the field \"select\", so the portal can show the line \"Select 1.\" or \"Select 2.\" The format of the portal is not decided yet." | `"select": slot["select"]` (`src/step8_build_files.py`, 79) |
| 5 | 32 | "Each scenario presents a realistic production context that frames a set of questions." | 67 | "The questions are in groups by scenario, each with its story." | groups, lines 73-75 |
| 3 | 33 | "percent-correct by domain on the score report" | 48 ("Result reporting" row) | "Each question has its domain, so the portal can show a result for each domain." | `"domain": domain_of[...]` (line 77) |

Other facts for section 3:
- T8: A fourth guide fact is in the files but not in the table: the time limit. `reference/exam-guide.md`, 43: "| Time limit | 120 minutes |". The code takes it from decision 0003 (F2), not from a table row. (L1 / L2; see Not found 4.)
- T9: The first build linked the "one source" lesson to point 2.5-K3, as history. `reference/practice-audit-first-build.md`, 253: "| 2.5-K3 | Read/Write for full file operations; Edit for targeted modifications using unique text matching | Applied in part | ... | P2 rewrote 28 option texts in the papers and left the bank as it was; the bank and the August papers differ for 23 questions." `HANDOFF.md`, 61, calls that file "History of the first build. Not a source for the design." No design file of step 8 cites 2.5-K3. (L4, history only.)
- T10: No diagram cites a point for step 8, so academy decision 0024 has no diagram-only point to list as a conflict for this step.

## 4. Numbers, per mock, with method

### 4.1 Method

Script `count8.py` (in the scratchpad of this agent, not in the repository). Run: `env -u ANTHROPIC_API_KEY python3 -I count8.py ~/ccar-f-mock-generator`. It reads `runs/mock-0N/plan.json`, `build.json`, `questions/*.json`, `checks/*.json`, `marks/round-*.json`, `mocks/mock-0N.*.json` and `reference/guide-records.json`. It imports `fingerprint` from `src/control.py` and `build` from `src/step8_build_files.py`. It makes no model call. The only thing it writes is a rebuild of each mock into a temporary folder in the scratchpad (deleted after the run), to compare with `mocks/` byte for byte.

```python
records = rd(ROOT + "/reference/guide-records.json")
for m in range(1, 6):
    F = ROOT + "/runs/mock-%02d" % m
    plan, b = rd(F + "/plan.json"), rd(F + "/build.json")
    qf = rd(ROOT + "/mocks/mock-%02d.questions.json" % m); af = rd(ROOT + "/mocks/mock-%02d.answers.json" % m)
    qs = [q for g in qf["groups"] for q in g["questions"]]
    # groups: len(qf["groups"]); per group: [len(g["questions"]) ...]; order: [g["scenario"] ...] vs plan["scenarios"]
    # numbers: [q["number"] for q in qs] == list(range(1, 61)); answers: len(af["answers"])
    # no answers in the questions file: '"correct"' / '"reason"' not in json.dumps(qf)
    fps = b["fingerprints"]; recs = {k: rd(F + "/questions/%s.json" % k) for k in fps}
    # fingerprint(recs[k]) == fps[k]; checks/<k>-step3.json and -step4.json "fingerprint" == fps[k]
    # last run of step 6 of each scenario: r["fingerprints"][k] == fps[k]
    # last mark of k (marks/round-*.json): mark == "good" and fingerprint == fps[k]
    # file == record: question, select, (letter, text) and (letter, correct, reason) of each option
    # rebuild: s8.build(plan, [recs[k] for k in sorted(fps)], records, tmp, qf["date"]); filecmp.cmp(..., shallow=False)
    # letters: Counter of af["answers"][i]["correct"] for one-answer and two-answer questions
```

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | File and method |
|---|---|---|---|---|---|---|
| Questions in the questions file | 60 | 60 | 60 | 60 | 60 | sum of `len(g["questions"])` over `groups` |
| Groups / questions per group | 4 / 15,15,15,15 | same | same | same | same | `groups` |
| Scenarios in file order (= `plan.json` `scenarios`) | 3, 1, 2, 5 | 3, 4, 5, 6 | 6, 1, 4, 2 | 6, 3, 1, 4 | 4, 2, 5, 1 | `g["scenario"]`; equal to the plan in 5 of 5 |
| Numbers 1 to 60 in sequence | yes | yes | yes | yes | yes | `number` |
| `minutes` | 120 | 120 | 120 | 120 | 120 | top field |
| `seed` (= plan seed) | 366341 | 167622 | 788092 | 445312 | 203660 | top field, `plan.json` |
| `date` of the questions file (= `build.json` date) | 2026-10-08 | 2026-10-08 | 2026-10-09 | 2026-10-09 | 2026-10-09 | top field |
| Answers in the answers file (numbers and IDs match the questions file) | 60 | 60 | 60 | 60 | 60 | `answers` |
| The questions file has `"correct"` or `"reason"` | no | no | no | no | no | text search |
| `select` 1 / 2 | 52 / 8 | 52 / 8 | 52 / 8 | 52 / 8 | 52 / 8 | `select` |
| Domains 1 to 5 | 16, 11, 12, 12, 9 | same | same | same | same | `domain` |
| Questions not from try 1 (`-T2` or later) | 18 | 27 | 28 | 29 | 21 | `question_id` |
| Fingerprints in `build.json` | 60 | 60 | 60 | 60 | 60 | `len(fingerprints)`; all 64 characters |
| ... equal to `fingerprint()` of the record today | 60 | 60 | 60 | 60 | 60 | `src/control.py` `fingerprint` |
| ... equal to the step 3 verdict | 60 | 60 | 60 | 60 | 60 | `checks/<id>-step3.json` |
| ... equal to the step 4 verdict | 60 | 60 | 60 | 60 | 60 | `checks/<id>-step4.json` |
| ... equal to the last run of step 6 | 60 | 60 | 60 | 60 | 60 | `checks/MN-scenario-*-step6-run*.json` |
| Built questions with a mark / mark `good` with the same fingerprint | 60 / 60 | 30 / 30 | 22 / 22 | 20 / 20 | 60 / 60 | `marks/round-*.json`, last mark of the ID |
| Questions in the files equal to their records | 60 | 60 | 60 | 60 | 60 | text, `select`, each option |
| Rebuild with today's code is byte-identical (questions, answers) | yes, yes | yes, yes | yes, yes | yes, yes | yes, yes | `filecmp.cmp(shallow=False)` |
| One-answer correct letters A, B, C, D | 10, 17, 7, 18 | 11, 13, 15, 13 | 12, 12, 18, 10 | 8, 8, 14, 22 | 13, 13, 13, 13 | `correct` of the 52 |
| Two-answer correct letters A to E | 3, 4, 6, 2, 1 | 6, 2, 2, 4, 2 | 3, 3, 2, 5, 3 | 5, 2, 2, 2, 5 | 4, 3, 3, 3, 3 | `correct` of the 8 |
| ID of the `accept` decision (decisions before it) | D044 (43) | D024 (23) | D018 (17) | D026 (25) | D021 (20) | `owner-decisions.json` |
| `report.json` state | built | built | built | built | built | field `state`; `errors` empty |
| File size, bytes (questions, answers) | 94879, 70486 | 100301, 72178 | 100023, 72890 | 102963, 73932 | 104111, 72052 | `os.path.getsize` |
| Commit that added the files (`git log -- mocks/`) | `26477e1` 2026-10-08 11:06 | `d97c686` 2026-10-08 20:56 | `4011959` 2026-10-09 10:20 | `a74fccd` 2026-10-09 17:22 | `f1e0904` 2026-10-09 22:36 | one commit for each file, no later commit |

Totals: 300 questions, 20 groups, 300 of 300 fingerprints match the records, the verdicts of steps 3 and 4 and the last run of step 6; 192 of 192 marks of built questions are `good` with the same fingerprint; 10 of 10 files rebuild byte-identical.

### 4.3 Checks of the numbers in other files

- `docs/build-guide/step-8-build-the-files.md`, 19: "60 questions in 4 groups (scenarios 3, 1, 2, 5) and 120 minutes ... with 60 answers. The build saved 60 fingerprints." Agrees.
- `docs/decisions/0070-...md`, 10: "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. ... Mock 1 had B 17 times and C 7 times." Agrees. Mock 5, 13 each and "3 or 4 each" for two-answer letters (0070, 21): agrees.
- `docs/decisions/0065-...md`, 10, 19: "The owner marked 22 questions good in two rounds" / "scenarios 1, 2, 4 and 6". Agrees (22; the file order is 6, 1, 4, 2).
- `academy/facts/top-of-tab-2.md`, 242: "Questions in the built mock file: 60 in 4 groups, each mock \| 300". Agrees.
- The 16, 11, 12, 12, 9 domain counts agree with `HANDOFF.md`, 114: "16, 11, 12, 12 and 9 questions for the 5 domains."

## 5. Stories for the Depth

Search: "step 8", "Step 8", "build.json", "fingerprint", "mocks-v", "rebuil", "build again", "converter", "cannot start", "refused", "accept" in `docs/decisions/`, `docs/journal.md`, `docs/lessons.md`, `docs/reviews/`, `HANDOFF.md`, `docs/portal-notes.md`; `git log` of `src/step8_build_files.py`, `mocks/`, `runs/mock-0*/build.json`, the step 8 docs; `git show 8cc3a24:` of decision 0036.

No source tells a failed real build: no record shows a refused `accept` (a refusal writes no file, E2), and the journal and decisions name none. No mock was ever rebuilt: each file in `mocks/` has exactly one commit, and `git diff aca8a23 HEAD -- mocks/ runs/mock-0*` is empty. The stories are design stories, one fault found in review, and two decisions after the build.

### Story (a): the conditions that could never be met, and why the owner accepts with a command

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| a1 | The first text of 0036 (6 October): the step starts when the questions passed steps 3, 4 and 6, and each marked question is good. | `git show 8cc3a24:docs/decisions/0036-...md`, 21, 33 | "1. **When the step starts.** The current try of each of the 60 slots passed steps 3, 4 and 6, and each question that the owner marked has the mark good." / "7. **The checks before the build.** Code checks that each slot has a question, that each question has its verdict records and the mark of the owner if the owner read it, and that no record changed after its check." | 2 (old text) |
| a2 | The assistant said the design of all 9 steps was complete; that was too early. Step 8 was the last design of that session. | `docs/journal.md`, 298-300 (section "6 October 2026, second session") | "Decided the design of step 8 (decision 0036): two JSON files for each mock, groups by scenario, and a fingerprint that stops the build when a record changed after its check." / "Each of the 9 steps now has a design decision and a diagram. The assistant told the owner that the design of all 9 steps is complete. That was too early." | 4 |
| a3 | The first review: the fingerprint had no method (serious), and the 120 minutes were in no output file (minor). | `docs/reviews/review-decisions-0026-to-0036.md`, 95, 99 (section "Gaps (13)") | "9. **Serious. The fingerprint.** No method, and no list of the fields that it covers. A record of step 6 covers 15 questions, so one field is not sufficient." / "The 120 minutes are in no output file." | 4 |
| a4 | The fix of the method: decision 0037, item 13. (The `minutes` field is in 0036 at the first commit; no source says which change added it.) | `docs/decisions/0037-...md`, 41 | "13. **The fingerprint.** SHA-256 of the question ID, the question, `select`, and each option with its letter, its mark and its reason. A record of step 6 has one fingerprint for each of its 15 questions. The marks record has one for each mark. Changes 0036." | 2 |
| a5 | The second review: after `ignore`, a scenario never passes step 6, "So the mock can never be built". | `docs/reviews/review-decisions-0024-to-0037.md`, 106 (section "New contradictions (7)") | "3. **Serious.** 0034: a scenario passes step 6 when no rule has the result `fail`. After `ignore`, the record still has a `fail`. 0036 needs \"passed steps 3, 4 and 6\". So the mock can never be built." | 4 |
| a6 | The second review: for a later mock, the condition is true with no marks. | same file, 132 (section "New gaps, from 10 cases ...") | "**(j) Step 8 for a later mock. Serious.** \"Each question that the owner marked has the mark good\" is true with no marks. No condition says that a marking round was accepted, that each \"cannot decide\" result of step 6 has a decision, or that the stop number was not reached." | 4 |
| a7 | The owner stopped the review cycle (decision 0038). Step 8 starts when the owner accepts; the exact conditions go to code and tests. | `docs/decisions/0038-...md`, 25, 38, 44, 62 | "5. **Step 8 starts when the owner accepts the mock.** Code checks the conditions before it builds." / "\| 4. After `ignore`, the scenario cannot pass \| Closed by parts 4 and 5 \|" / "\| 10. The exact conditions before step 8 \| Goes to the code and its tests \|" / "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." | 2 |
| a8 | The six conditions in decision 0039, item 10, which closes item 10. | `docs/decisions/0039-...md`, 61-72; `HANDOFF.md`, 139, 145 | (text in section 2.2) / "\| 4 \| After `ignore`, the scenario cannot pass step 6. \| Closed. The owner accepts the mock with a command. \|" / "\| 10 \| The exact conditions before step 8 builds the files \| Closed by decision 0039. \|" | 2 / 4 |
| a9 | 0036 was changed to describe the control. | `docs/decisions/0036-...md`, 7 | "Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review." | 2 |
| a10 | The conditions in the code (section 2.2). Each case of the review that the conditions answer has a test (C-b). | `src/control.py`, 733-763 | `if self._step6_current(scenario) is None:` ... `"%s: the finding of step 6 has no decision"` ... `"the bad marks reached the limit that stops the mock"` | 1 |

Time order (`git log --date=iso`; the dates inside the files for what is before git): review of 0026-0036 (6 October) -> decision 0037 and the changed 0036 (6 October, third session) -> review of 0024-0037 (6 October, third session) -> decision 0038 (7 October) — all in the first commit `8cc3a24` (2026-10-07 09:41:04) -> control and decision 0039 `ed742b7` (2026-10-07 11:11:12) -> 0036 changed to describe the control `73d9fba` (2026-10-07 11:25:36) -> the confirmation of 0036 and 0039 `938d0db` (2026-10-07 11:43:08) -> code of step 8 `fa7e9cd` (2026-10-07 12:22:46). `git log -L733,782:src/control.py` shows only `ed742b7`: the accept code did not change after it was written.

### Story (b): the review of the code found that step 8 built files from a record that did not agree with its slot

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| b1 | An independent reviewer of steps 3 and 8 found 4 serious and 6 minor items; one real fault was in step 8. | `docs/journal.md`, 185 (section "7 October 2026, second session") | "An independent reviewer found 4 serious and 6 minor items. The assistant fixed them. Two were real faults: the control crashed when it saved the verdict of a question with an incomplete option, and step 8 built files from a record that did not agree with its slot. 116 tests pass. For each fix, a test fails without it." | 4 |
| b2 | The fix in the code: `check_record`. | `src/step8_build_files.py`, 24-46 | "The record must agree with its slot. ... This is a last check before a participant sees the file." | 1 |
| b3 | The tests of the fix. | `tests/test_step8_build_files.py`, 98-130 | `def test_a_record_that_does_not_agree_with_its_slot_builds_nothing(self):` / `def test_wrong_correct_marks_build_nothing(self):` / `def test_a_mark_that_is_not_true_or_false_builds_nothing(self):` / `def test_wrong_letters_build_nothing(self):` / `def test_a_question_of_another_slot_builds_nothing(self):` | 1 |
| b4 | `src/README.md` names it. | `src/README.md`, 10 | "`step8_build_files.py`: step 8. It builds the two files of a mock in `mocks/` (decision 0036). It checks each record against its slot first." | 1 |
| b5 | The code and its tests are one commit; the fault and the fix are not separate in git. No review file in `docs/reviews/` covers the code of steps 3 and 8. | `git log -- src/step8_build_files.py`: only `fa7e9cd` 2026-10-07 12:22:46 "Build steps 3 and 8, with tests" | | 1 |
| b6 | Steps 3 and 8 had no build guide section until they ran on a real question. | `docs/journal.md`, 186 | "Steps 3 and 8 did not run on a real question, so they have no build guide section yet." | 4 |

### Story (c): one true copy, from the first build (background of decision 0016)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| c1 | The first build: papers and the question bank disagreed. | `docs/lessons.md`, 79-80 (file note, line 3: "Private history of the first build. Not a source for the design.") | "21. **Keep one source of data. Code makes each paper and each summary from it. Nobody edits an output file by hand.**" / "For 23 questions the paper had an option text that was different from the question bank." | 4 |
| c2 | The audit of the first build gives the detail. | `reference/practice-audit-first-build.md`, 98 | "5. For 23 questions the August paper has a rewritten option text (28 texts) and the bank holds the old text. For 7 more questions the order of the options differs. So the bank is not the source of the papers." | 4 (history) |
| c3 | The owner did not understand the first form of the question; the assistant used an invoice example. | `docs/decisions/0016-...md`, 29 (How we decided) | "The assistant suggested this step. The owner did not understand the first form of the question. The assistant then explained it with an example: an invoice from accounting software. You correct the entry in the software and print again. You do not write on the printed invoice." | 2 |
| c4 | Journal entry. | `docs/journal.md`, 336 (section "6 October 2026, first session") | "Decided step 8 of the pipeline: code builds the mock files from the question records, and nobody edits an output file by hand (decision 0016)." | 4 |
| c5 | The proof in the runs: 300 of 300 fingerprints match, 300 of 300 questions in the files equal their records, and the 10 files rebuild byte-identical (section 4.2). | `count8.py` | | 1 (computed) |

### Story (d): the letters of mocks 1 to 4 were not balanced; the files were not rebuilt, the portal gets a note

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| d1 | The problem, counted after mock 4 was built. | `docs/decisions/0070-...md`, 10 | "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. Chance is 13. Mock 1 had B 17 times and C 7 times. A participant can learn to guess a letter." | 2 |
| d2 | The fix is in steps 1 and 2 from mock 5. Mocks 1 to 4 do not change. | `docs/decisions/0070-...md`, 19, 23 | "Option 1, from mock 5." / "3. A plan with no field (mocks 1 to 4) keeps the mixed order. Mocks 1 to 4 do not change." | 2 |
| d3 | The owner added the note for the portal. | `docs/decisions/0070-...md`, 24, 32 | "4. **A note for the portal:** the portal shows the options in a random order on each attempt, because the letters in mocks 1 to 4 are not balanced. ... The converter must keep the link between each option and its reason." / "The owner agreed, and added the note for the portal." | 2 |
| d4 | The note in `docs/portal-notes.md`. | `docs/portal-notes.md`, 5 | "**Random order of the options.** Show the options of each question in a random order on each attempt." | 4 |
| d5 | Mock 5 is balanced: 13, 13, 13, 13 (section 4.2). | `mocks/mock-05.answers.json` | | 1 (computed) |

Time order: mock 4 built `a74fccd` 2026-10-09 17:22:34 (same commit adds 0070); `docs/portal-notes.md` first written `235960a` 2026-10-09 22:27:10; mock 5 built `f1e0904` 2026-10-09 22:36:01.

### Story (e): the tag of the set, `mocks-v1` renamed to `mocks-v2`

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| e1 | The decision. | `docs/decisions/0079-...md`, 19 | "Option 1. The tag `mocks-v2`, with the message \"Mocks 1 to 5 built and accepted\", marks commit aca8a23 on GitHub. The first tag `mocks-v1` on the same commit is deleted, on this computer and on GitHub." | 2 |
| e2 | Why. | `docs/decisions/0079-...md`, 23, 27 | "Plain reason: the portal already has a version 1. The same name for two different sets of mocks confuses the readers of the portal." / "The owner asked for the tag `mocks-v1`. Then the owner asked to rename it to `mocks-v2`, because the portal already has a version 1." | 2 |
| e3 | The local tag: annotated, tagger date 2026-10-09 23:31:44, on `aca8a23` (2026-10-09 23:28:09, "Decisions 0073 to 0078: fixes of the owner and the second review, confirmed by the owner"). | `git for-each-ref refs/tags`; `git rev-list -n1 mocks-v2` | "mocks-v2 2026-10-09 23:31:44 +1100 aca8a23 Mocks 1 to 5 built and accepted" | 1 |
| e4 | Journal. | `docs/journal.md`, 42 (section "9 October 2026, mocks 4 and 5, and the check of the documents") | "The owner had the commit aca8a23 tagged as `mocks-v2` ... A first tag `mocks-v1` on the same commit was deleted, on this computer and on GitHub." | 4 |

Time order: `aca8a23` 23:28:09 -> tag 23:31:44 -> journal `4f544dd` 23:31:55 -> decision 0079 `cbc05a5` 23:33:16 -> confirmed `c05cbf4` 23:39:22 (all 2026-10-09).

### Other Depth facts

- The build guide table row on `select` got "The format of the portal is not decided yet." in a review fix: `79c6059` (2026-10-08 11:10:47, "Fix the findings of the review of steps 5, 8 and decision 0046"). (L1, git)
- The acceptance of each mock is in a decision: 0059, 32 (mock 2); 0065, 19 (mock 3: "Step 8 checked the six conditions of decision 0039 and built ..."); 0069, 31 (mock 4); 0077, 25 (mock 5); mock 1 in the D044 reason and `docs/journal.md`, 151: "The owner accepted mock 1. Step 8 checked the 6 conditions and built `mocks/mock-01.questions.json` and `mocks/mock-01.answers.json`: 60 questions in 4 groups, 120 minutes." (L2 / L1 / L4)
- Decision 0065, How we decided, 31: the owner made the accept wait for the records: "Accept mock 3 and build its files, after the known limits and the step 6 findings from my earlier message are recorded." (L2)

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/control.py` | 765-781 | `accept`: refuse if stopped or built, the conditions, the build, then the decision and `build.json`. |
| `src/control.py` | 733-763 | `build_conditions`: each cause text of the six conditions. |
| `src/control.py` | 52-66 | `fingerprint`: SHA-256 of what a participant sees, sorted keys, UTF-8. |
| `src/control.py` | 741-746 | The fingerprint compare against the verdicts of steps 3 and 4. |
| `src/control.py` | 410-420 | Step 6 counts only when its fingerprints equal the current questions. |
| `src/control.py` | 94-99 | `_write_new`: a record is never written over (used for `build.json`). |
| `src/step8_build_files.py` | 1-13 | The docstring: what the step builds, nobody edits by hand, the field names are the code's. |
| `src/step8_build_files.py` | 24-46 | `check_record`: the last check against the slot (story b). |
| `src/step8_build_files.py` | 67-90 | The groups, the questions with no answers, the answers file. |
| `src/step8_build_files.py` | 91-105 | Temporary names first: no half mock. |
| `src/steps.py` | 97-101 | A `BuildError` becomes a refusal to the owner. |
| `src/run.py` | 10, 104-108 | The command line `accept` and "Refused:". |
| `tests/test_step8_build_files.py` | 54-59 | The questions file has no answers. |
| `tests/test_step8_build_files.py` | 88-91 | No file is written over. |
| `tests/test_step8_build_files.py` | 111-130 | Records that do not agree with the slot build nothing (story b). |
| `tests/test_control.py` | 394-407 | A record changed after its check stops the build. |
| `tests/test_control.py` | 601-611 | A failed build saves no accept. |
| `runs/mock-01/build.json` | 1-8, 66-68 | A real `build.json`: the files and the fingerprints. |
| `runs/mock-01/owner-decisions.json` | 345-351 | The real accept record D044. |
| `mocks/mock-01.questions.json` | 1-30 | The top fields and the first group and question. |
| `mocks/mock-01.answers.json` | 1-30 | The first answer with its reasons. |
| `docs/decisions/0039-...md` | 61-72 | The six conditions (decision text). |
| `git show 8cc3a24:docs/decisions/0036-...md` | 21, 33 | The first conditions that could never be met (story a). |

## 7. A figure: the mechanism

```
[Owner: "accept"] --starts--> [Code: checks 6 conditions] --any false--> [Refused: lists the causes, no file]
                                      |
                                  all true
                                      v
[Question records (one true copy)] --read by--> [Step 8 code: last check against the slot]
                                                      |
                                    writes (temporary names, then renames)
                                      v                               v
                         [mock-0N.questions.json]           [mock-0N.answers.json]
                          4 groups x 15, story,              correct letters,
                          no answers, 120 minutes            reason of each option
                                      |
                              then saves
                                      v
                    [accept decision] + [build.json: 60 fingerprints]  --> state "built"
Side box: fingerprint of the record now = fingerprint saved by each check (steps 3, 4, 6, mark)?  equal -> build / different -> stop
```

| Label | Fact behind it |
|---|---|
| "accept" | E1, E3, O3 |
| "checks 6 conditions" | section 2.2, `src/control.py` 733-763 |
| "Refused: lists the causes, no file" | E2, `src/control.py` 770-771; C-b |
| "one true copy" | O4 |
| "last check against the slot" | B1, B2 (story b) |
| "temporary names, then renames" | B5 |
| "4 groups x 15, story, no answers, 120 minutes" | F1 to F4, F7; 4.2 |
| "correct letters, reason of each option" | F6 |
| "then saves accept + build.json" | E5, E6, P4 |
| "state built" | E7 |
| fingerprint side box | P1, P2, P3, P7 |
| Number on the figure | 300 of 300 fingerprints match; 10 of 10 files rebuild byte-identical (4.2) |

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| C1 | "Code builds the files again" after a change: no path for it exists in the code. | `docs/decisions/0016-...md`, 19 (L2): "To change a question, change its record, and code builds the files again." `docs/build-guide/step-8-build-the-files.md`, 9 (L3): "To change a question, the record changes, and code builds the files again." | `src/control.py`, 767-768 (L1): `accept` is refused when the state is `built`; 628-629: each `decide` is refused; `src/step8_build_files.py`, 63-65: `raise BuildError("The file exists already: %s" % p)`; `_write_new` refuses an existing `build.json` (94-99). No rebuild ever happened (each file in `mocks/` has one commit). |
| C2 | The answers file example in diagram 10 uses the key `reasons`; the code uses `options`. | `docs/diagrams/10-make-diagram.py`, 25-26, shown in `docs/diagrams/10-step-8-build-the-files.html`, 284, popup `afile` (L3): `"reasons": [ { "letter": "A", "correct": false, "reason": "(why A is wrong)" } ...` | `src/step8_build_files.py`, 84 (L1): `"options": [{"letter": o["letter"], "correct": o["correct"], "reason": o["reason"]} ...]`; `mocks/mock-01.answers.json`: keys `number`, `question_id`, `correct`, `options`. (The footer, line 281, says the files are drawings that "show the form".) |
| C3 | The box of the gate in diagram 10 is named "Three checks" and shows three lines; its popup and the decisions say six conditions. | `docs/diagrams/10-step-8-build-the-files.html`, 255 (L3): `aria-label="Three checks before the build"`, box lines "Each question passed its checks." / "Each finding and mark is settled." / "No record changed after its check." (from `10-make-diagram.py`, 107) | Same file, 284, popup `gate`: "Six conditions before the build"; `docs/decisions/0039-...md`, 61-72 (L2). |
| C4 | The example question ID of diagram 10 is a real ID with other fields. | `docs/diagrams/10-make-diagram.py`, 21 (L3): `'question_id': 'M1-S17-T2', 'domain': 1, 'task_statement': '1.2', 'point': '1.2-K2'`, 4 options, `select` 1 | `mocks/mock-01.questions.json` (L1), number 17: `M1-S17-T2`, domain 2, task statement 2.4, point 2.4-K4, `multiple_response`, `select` 2, correct C and D. |
| C5 | What step 8 receives, in diagram 01. (Also X9 in `academy/facts/top-of-tab-2.md`.) | `docs/diagrams/01-pipeline-overview.html`, 191, step "8" (L3): "It receives the stored question records of a mock that passed step 7." | `src/control.py`, 765-771 (L1): step 8 waits for `accept` and the six conditions, including the findings of step 6. |
| C6 | The date that step 8 was built. | `docs/build-guide/README.md`, 22 (L3): "built (8 October 2026), built mocks 1 to 5 by 9 October 2026" | `git log -- src/step8_build_files.py` (L1): `fa7e9cd` 2026-10-07 12:22:46 "Build steps 3 and 8, with tests". (8 October is the first real build, mock 1, `26477e1`.) The same README gives step 3, from the same commit, "built (7 October 2026)". |
| C7 | Decision 0036: confirmed or not. | `docs/decisions/0036-...md`, 5 (L2): "Text confirmed by the owner: 7 October 2026, after a summary of one line for each file" | Same file, 76: "The owner approved the proposal in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file." (The second sentence is from before the confirmation; `docs/journal.md`, 178: "The owner confirmed the text of decisions 0019 to 0036 and 0039.") |
| C8 | Who compares the fingerprints. | `docs/decisions/0036-...md`, 44 (L2): "Step 8 calculates the fingerprint of each record again and compares." | `src/control.py`, 741-746 (L1): the control compares before it calls step 8; `src/step8_build_files.py`, 25-26: "The control already checked steps 3 and 4 and the fingerprints." Small: the build guide, 13, says "code calculates the fingerprint again". |
| C9 | The fields of the fingerprint in words. | `docs/decisions/0036-...md`, 44 and `docs/decisions/0037-...md`, 41 (L2): "each option with its letter, its mark and its reason" (the option text is not named) | `src/control.py`, 62 (L1): `[o.get("letter"), o.get("text"), o.get("correct"), o.get("reason")]` (the text is in it). Small: "each option" can include its text. |

## 9. Not found

1. No real refusal of `accept` in any source: a refusal writes no record (E2), and no journal entry or decision mentions one. Each of the 5 accepts in `owner-decisions.json` is a success.
2. No rebuild of a mock: each file in `mocks/` has one commit, and nothing in `mocks/` or `runs/mock-0N/` changed after the tag commit `aca8a23` (`git diff aca8a23 HEAD` is empty for those paths).
3. No review file for the code review of steps 3 and 8 (story b). Only the journal line 185 tells it. The fault and its fix are not separate in git.
4. The build guide table of step 8 does not list the time limit ("120 minutes", guide Section 3, line 43), though the file has `minutes` 120 (from decision 0003). No source says if this omission is on purpose.
5. No source says which change put the field `minutes` into decision 0036 after the review gap "The 120 minutes are in no output file" (both are before the first commit).
6. Not checked: that the tag `mocks-v2` is on GitHub (no network call). Checked only on this computer (e3).
7. No source discusses that the fingerprint does not cover the point of a record (P8) or that `build.json` held absolute local paths until 14 October 2026 (P9), in a repository that becomes public (academy decision 0003).
8. No converter to the portal format exists (F11), and the portal format is not known. No source says how the portal will show "Select N." or a result for each domain.
9. No independent reviewer checked decision 0016 or 0036 (0036, 76: "No independent reviewer checked this file."); decision 0039's code had two reviews (0039, 83).
10. `docs/lessons.md` has no entry on step 8 of this build. Its item 21 is on the first build.
