# Fact sheet: tab 2, step 6 "Check the complete mock"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `88d0dba` (branch `main`, clean before this file).
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = Anthropic documentation (academy decision 0014).
- Line numbers are for the files at commit `88d0dba`. "L" = level of trust.
- The tests ran on 14 October 2026 with no API key in the environment: `python3 -m unittest discover -s tests` gives "Ran 228 tests ... OK". `tests/test_control.py` has 66 tests (`grep -c "def test" tests/test_control.py`).
- Files that this agent did not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, and all personal files of the owner. No model call. `src/run.py` was not run.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | Steps 3 and 4 look at one question. Step 6 looks for the defects that show only when many questions are read together. | `docs/build-guide/step-6-check-the-complete-mock.md`, 9 | "Steps 3 and 4 look at one question. Some defects show only when many questions are read together. Each writer call sees only its own slot, so two calls can write the same scene." | 3 |
| O2 | Code checks the mock (C2, C3), then two model calls read the 15 questions of one scenario together. | `src/step6_check_scenario.py`, 1-9 | "Step 6: the check of the complete mock, one scenario at a time" / "Then two model calls read the 15 questions together: call 6a (rules D1 and D4) and call 6b (rules D2 and D3)." | 1 |
| O3 | Step 6 sends no question back. Each finding goes to the owner. | `src/step6_check_scenario.py`, 8-9 | "Step 6 sends no question back. Each finding goes to the owner (decision 0038, part 3)." | 1 |
| O4 | Why a separate step: the writer sees only its own slot, so it cannot prevent a repeated scene and cannot count for ruling 2. | `docs/decisions/0010-...`, 30 | "a writer that sees one slot does not see the other questions of its scenario. It cannot prevent two questions with the same scene, and it cannot count for ruling 2 (decision 0006). A different step does that work (decision 0014)." | 2 |
| O5 | Status: built; ran in the test of 7 October 2026 and for mocks 1 to 5, 7 to 9 October 2026. | `docs/build-guide/step-6-check-the-complete-mock.md`, 3 | "Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026." | 3 |
| O6 | The model of each call of step 6 in mocks 1 to 5 is `claude-opus-5-5`. | `src/model_call.py`, 22; run files | `MODEL = "claude-opus-5-5"`. Count: field `model` of each result D1 to D4 in the 33 files `runs/mock-0N/checks/*step6*.json` is `claude-opus-5-5` (132 of 132). | 1 |

## 2. Explanation facts: the mechanism

### 2.1 When the step starts, and its inputs

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | Step 6 starts only when every slot has the status `passed`. This is rule C1, checked by the control, not by step 6. | `src/control.py`, 340-343; `src/step6_check_scenario.py`, 6-7 | `if all(self.slot_state(s)["status"] == "passed" for s in self.slots()):` / "The control already checked rule C1: it starts step 6 only when each slot has the status passed." | 1 |
| E2 | It runs again for a scenario only when a question of that scenario changed (fingerprints differ). | `src/control.py`, 410-423 | `return last if last["fingerprints"] == now else None` | 1 |
| E3 | Input: the 15 current questions of one scenario, plus the passed questions of the other scenarios (only for C3). | `src/control.py`, 425-434, 455-458 | "The current questions of the other scenarios, of each slot that passed (rule C3 compares the whole mock, decision 0052)." | 1 |
| E4 | Call 6a sees each question with its options, the marks and the reasons. | `src/step6_check_scenario.py`, 82, 86; `src/step4_check_model.py`, 38-46 | `show(q, with_key=True)` / "Marked: %s. Reason: %s" | 1 |
| E5 | Call 6b sees only the wrong options of the 15 questions, with their reasons. No question text, no correct option. | `src/step6_check_scenario.py`, 83-87; `tests/test_model_steps.py`, 429 | "THE WRONG OPTIONS of the 15 questions, with their reasons" / `self.assertNotIn("RIGHT option", client.requests[1]["messages"][0]["content"])` | 1 |
| E6 | Neither call gets text of the exam guide. The request is the system text, the rules of the call and the questions. | `src/step6_check_scenario.py`, 22-23, 64 | `"THE RULES OF THIS CALL\n%s\n\n%s" % (rules, text)` | 1 |
| E7 | 4 scenarios in a mock, so 8 calls per full run of step 6. | `docs/decisions/0034-...`, 41 | "A mock has 4 scenarios, so a mock has 8 of these calls." | 2 |

### 2.2 The rules, one line each

| Rule | Who | Text (exact) | Source, lines | L |
|---|---|---|---|---|
| C1 | Control (code) | "The current try of each of the 60 slots has the status `passed`." | `docs/decisions/0034-...`, 33; code: `src/control.py`, 342 | 2 / 1 |
| C2 | Code | Code: the slot IDs of the scenario agree with the plan, and each question has the `select` and the number of options of its slot. "Rule C2: the questions of scenario %s do not agree with the plan." | `src/step6_check_scenario.py`, 32-39 | 1 |
| C3 | Code | "No two questions have the same text." Compares lower-case text with whitespace joined, across the whole mock. | `docs/decisions/0034-...`, 35; `src/step6_check_scenario.py`, 40-55 | 2 / 1 |
| D1 (6a) | Model | "D1. No two questions have the same scene. Two questions have the same scene when they have the same problem and the same correct action." | `src/step6_check_scenario.py`, 17 | 1 |
| D4 (6a) | Model | "D4. No question gives away the answer of a different question." | `src/step6_check_scenario.py`, 18 | 1 |
| D2 (6b) | Model | "D2. No wrong idea is a wrong option in more than 2 questions of the scenario." | `src/step6_check_scenario.py`, 19 | 1 |
| D3 (6b) | Model | "D3. At most one wrong option of the scenario is this option: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger. A use of model confidence that the exam guide teaches as correct does not count: field-level confidence scores calibrated with labeled validation sets, used to route review attention or to send items to human review. The option also does not count when it is the correct answer." | `src/step6_check_scenario.py`, 20 | 1 |

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E8 | The number 2 of rule D2 is a guess. | `docs/decisions/0034-...`, 141 | "The number 2 is a guess of the assistant. It has no source." | 2 |
| E9 | D4 is new: decision 0014 did not name it. | `docs/decisions/0034-...`, 143 | "D4. Decision 0014 does not name it. It is new. Plain reason: one question must not answer another." | 2 |
| E10 | C3 is a cheap exact check; a copy with other words is for the model (D1). An assumption. | `docs/decisions/0034-...`, 139 | "Plain reason: code finds an exact copy for no cost. A model finds a copy with different words (D1). This is an assumption of the assistant. It is not checked." | 2 |
| E11 | Why two calls: the owner doubted one call; the risk was the number of jobs, not the length. | `docs/decisions/0034-...`, 137, 156 | "I wonder if one api call is good enough? 60 questions and answers is long" / "But the doubt of the owner had a real point: one call had 4 jobs." | 2 |

### 2.3 What each call returns, and what code does with it

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E12 | Each call returns one result for each of its rules: `pass`, `fail` or `cannot_decide`. A finding names question IDs and has a detail. | `src/step6_check_scenario.py`, 22-23, 63-75 | "Give one result for each rule of this call: pass, fail or cannot_decide. A finding names the questions by their IDs." | 1 |
| E13 | The form is sent as structured outputs (JSON schema in `output_config.format`). | `src/model_call.py`, 3, 119; `src/step6_check_scenario.py`, 15 | `output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}}` / `load_form("08-form-draft.json")` | 1 |
| E14 | An answer without one result for each rule, or with an invalid result, is a failed call. | `src/step6_check_scenario.py`, 66-71 | "The answer does not have one result for each rule %s." | 1 |
| E15 | The control also checks the answer: a `fail` or `cannot_decide` needs a finding, and each finding must name only questions of the scenario. Only C3 may name another scenario. | `src/control.py`, 436-453 | "Only a finding of rule C3 can name a question of another scenario (decision 0052)." / `raise CallFailed("rule %s has the result %s and no finding" ...)` | 1 |
| E16 | A failed call runs again, at most 3 times; then an error record, and the scenario waits. | `src/control.py`, 30; `docs/decisions/0034-...`, 132 | `CALL_RUNS = 3` / "It never returns \"pass\" for a scenario that it did not check." | 1 / 2 |
| E17 | C2 failing stops the run with an error; a new call cannot repair it. | `src/step6_check_scenario.py`, 27-28, 35, 39 | "C2 failing stops the run with an error that names the cause (decision 0034): a new call cannot repair it." | 1 |
| E18 | Each finding gets an ID `M{mock}-SC{scenario}-R{run}-F{n}`. One record file for each scenario and each run. | `src/control.py`, 461-477 | `"%s-SC%s-R%d-F%d" % (self.prefix, scenario, run, len(findings) + 1)` / `"%s-scenario-%s-step6-run%d.json"` | 1 |
| E19 | The record fields: `mock`, `scenario`, `run`, `results`, `findings`, `verdict`, `fingerprints`, `date`. | `src/control.py`, 471-475; all 33 run files have exactly these 8 keys (script) | `"verdict": "pass" if not findings else "fail"` | 1 |

### 2.4 What happens to a finding

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E20 | The owner marks first. Findings are visible only when the automatic work is done and no mark waits. | `src/control.py`, 596-624 | "Mark the questions first. Then decide on the findings of step 6." / "The owner sees the findings only when the automatic work is done and no marking waits (decision 0038, part 4)." | 1 |
| E21 | For each finding the owner selects `ignore` or `rewrite`. A rewrite names one question of the finding and needs a reason. | `src/control.py`, 654-663, 674-675 | "A rewrite names one question of the finding." / "A rewrite must have a reason." | 1 |
| E22 | A rewrite sends that question to step 5 with the finding, the reason and the other questions; then steps 3, 4 and step 6 for that scenario only. | `src/control.py`, 249-269; `docs/build-guide/step-6-check-the-complete-mock.md`, 16 | "A rewrite sends one question of the finding to step 5. Then step 6 runs again for that scenario only." | 1 / 3 |
| E23 | A rewrite of one finding does not hide the other findings of the run. Only the last run of each scenario counts. | `src/control.py`, 584-594 | "A rewrite of one finding does not hide the others." / `records[-1]["findings"]` | 1 |
| E24 | No limit counts the rounds; the owner starts each one. | `docs/decisions/0038-...`, 24 | "No count limits these rounds, because the owner starts each one." | 2 |
| E25 | Step 8 waits until each finding of step 6 has a decision. | `src/control.py`, 752-753 | `causes.append("%s: the finding of step 6 has no decision" % f["id"])` | 1 |
| E26 | Why the owner decides: a finding names two or more questions, so a person picks which one, or none. | `docs/decisions/0034-...`, 144 | "A finding of this step names two questions or more, so a person selects which one to write again, or none." | 2 |
| E27 | The rule of the owner for mocks 2 to 5 (build guide). | `docs/build-guide/step-6-check-the-complete-mock.md`, 18 | "A finding of rule D4, a question that gives away the answer of another, is ignored. A finding of rule D2 or D3, one wrong idea in too many questions, is recorded as a known limit of the mock. A finding of any other kind, for example rule D1 (the same scene twice in one scenario), goes to the owner, who decides it." | 3 |
| E28 | Tests (no model call): ignore then accept; `cannot_decide` also waits for the owner; a decision before the marks is refused; C3 may name another scenario, D1 may not. | `tests/test_control.py`, 202-231, 428-452; `tests/test_model_steps.py`, 431-447 | "(d) Step 6 has a finding, and the owner selects `ignore`." / "unknown question: M1-S20-T1" | 1 |

### 2.5 The test before the first full run (7 October 2026)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E29 | A planted copy with the same scene was found by call 6a. | `runs/test-0024/part4.json`, field `same_scene_found`; `docs/journal.md`, 199 | `"same_scene_found": true` / "Call 6a found the copy (D1). Step 6 also found real problems of the writer: one more pair with the same scene, and four pairs that give away an answer (D4)." | 1 / 4 |
| E30 | Cost of part 4: 9 calls, $0.40. | `runs/test-0024/part4.json`, field `cost` | `{"calls": 9, ... "dollars": 0.4}` | 1 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-6-check-the-complete-mock.md`, lines 36-43 (L3). Guide texts agree with `reference/guide-records.json` (checked by script on 14 October 2026).

| Point | Line | Task statement | How the step uses it (exact, from the table) |
|---|---|---|---|
| 4.6-K3 | 38 | 4.6: Design multi-instance and multi-pass review architectures | "Written for the review of code in many files. Here: steps 3 and 4 are the pass for each question, and this step is the pass across the questions." |
| 4.6-S2 | 39 | 4.6 | "The same context and the same use." |
| 4.1-K1 | 40 | 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | "Written for the review of code. Here: \"the same scene\" has an exact definition: the same problem and the same correct action." |
| 5.3-K4 | 41 | 5.3: Implement error propagation strategies across multi-agent systems | "Written for errors between agents. Here: a call that fails, or an answer that is not valid, never counts as a pass." |
| 4.3-K1 | 42 | 4.3: Enforce structured output using tool use and JSON schemas | "Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above)." |
| 4.3-S3 | 43 | 4.3 | "Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above)." |

Guide texts (`reference/guide-records.json`):
- 4.6-K3: "Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings"
- 4.6-S2: "Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis"
- 4.1-K1: "The importance of explicit criteria over vague instructions (e.g., \"flag comments only when claimed behavior contradicts actual code behavior\" vs \"check that comments are accurate\")"
- 5.3-K4: "Why silently suppressing errors (returning empty results as success) or terminating entire workflows on single failures are both anti-patterns"
- 4.3-K1: "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors"
- 4.3-S3: "Forcing a specific tool with tool_choice: {\"type\": \"tool\", \"name\": \"extract_metadata\"} to ensure a particular extraction runs before enrichment steps"

Facts that support the uses:
- T1 (5.3-K4): in code, a result `fail`/`cannot_decide` with no finding, or a finding with an unknown question, raises `CallFailed` (`src/control.py`, 444-452). No run file of mocks 1 to 5 has `cannot_decide` (0 of 132 results), and no `errors` folder exists under `runs/mock-0N/`, so no call of step 6 failed 3 times. (L1)
- T2 (4.3-S3, the deviation): `docs/build-guide/step-6-check-the-complete-mock.md`, 26-32. The saved copy `docs/sources/2026-10-07-anthropic-docs-define-tools.md`, line 564: "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1] ... `any` and `tool` return a [400 error] ... `auto` with [strict tool use] ... or [structured outputs] when you need a response in a fixed JSON shape". Live page: not checked by this agent (the step 5 fact sheet, T3, checked it live on 13 October 2026). (Docs, saved copy)
- T3: diagram 08 popups cite 4.6-K3 and 4.6-S2 (popup `c6a`) and 5.2-K3 (popup `D3`). 5.2-K3 is not in the table: see conflict X1.
- T4: decision 0014 (line 43) also lists 1.6-K2; decision 0034 (line 162) lists "4.6-K3, 4.6-S2, 4.1-K1, 5.3-K4". The table has no 1.6-K2: see conflict X2.

## 4. Numbers, per mock, with method

### 4.1 Method

Script (run on 14 October 2026 from the scratchpad of this agent, not in the repository). Run: `python3 -I s6.py ~/ccar-f-mock-generator`. It reads only run files and makes no model call.

```python
import json, glob, os, collections, sys
root = sys.argv[1]
for m in range(1, 6):
    d = os.path.join(root, "runs/mock-0%d" % m)
    files = sorted(glob.glob(d + "/checks/*step6*.json"))            # runs of step 6
    decs = json.load(open(d + "/owner-decisions.json"))
    bytarget = {x["target"]: x for x in decs}                       # decision on each finding ID
    last = {}
    for f in files:
        r = json.load(open(f)); last[r["scenario"]] = max(last.get(r["scenario"], 0), r["run"])
    for f in files:
        r = json.load(open(f))
        for x in r["results"]:            # (rule, result) per run
            ...
        for fd in r["findings"]:          # rule of each finding, and the owner action
            action = bytarget.get(fd["id"], {}).get("action", "NO DECISION")
            is_last = r["run"] == last[r["scenario"]]
```

A finding with "NO DECISION" is a finding of a run that a later run of the same scenario replaced (the control uses only `records[-1]`, `src/control.py`, 593). All such findings were checked: each is in a replaced run.

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Total | Method |
|---|---|---|---|---|---|---|---|
| Run files of step 6 | 8 | 8 | 6 | 6 | 5 | 33 | count `runs/mock-0N/checks/*step6*.json` |
| Scenarios (run 1, run 2) | 1,2,3,5 (each 2) | 3,4,5,6 (each 2) | 1,2,4,6 (2 and 4 twice) | 1,3,4,6 (1 and 6 twice) | 1,2,4,5 (5 twice) | | field `scenario`, `run` |
| Model calls of step 6 (2 per run file, minimum) | 16 | 16 | 12 | 12 | 10 | 66 | 2 × run files (`src/step6_check_scenario.py`, 86-87). The usage files do not split calls by step. |
| All findings | 35 | 18 | 13 | 23 | 19 | 108 | sum of `len(findings)` |
| D1 findings | 8 | 2 | 0 | 0 | 2 | 12 | field `rule` |
| D2 findings | 10 | 4 | 3 | 9 | 4 | 30 | field `rule` |
| D3 findings | 1 | 3 | 1 | 2 | 2 | 9 | field `rule` |
| D4 findings | 16 | 9 | 9 | 12 | 11 | 57 | field `rule` |
| C3 findings | 0 | 0 | 0 | 0 | 0 | 0 | no `"C3"` in any step 6 file (`grep -l '"C3"' runs/*/checks/*step6*`) |
| Results `cannot_decide` | 0 | 0 | 0 | 0 | 0 | 0 | field `results[].result` |
| Run files with verdict `pass` | 1 | 3 | 2 | 0 | 0 | 6 | field `verdict` |
| Findings decided `ignore` | 33 | 9 | 11 | 17 | 14 | 84 | `owner-decisions.json`, `action` for `target` = finding ID |
| Findings decided `rewrite` | 2 | 2 | 0 | 0 | 0 | 4 | same |
| Findings with no decision (replaced run) | 0 | 7 | 2 | 6 | 5 | 20 | same |
| Findings in the last run of each scenario | 16 | 9 | 11 | 17 | 14 | 67 | findings with `run` = highest run of the scenario |
| Of these: D1 / D2 / D3 / D4 | 3/5/0/8 | 1/2/1/5 | 0/3/1/7 | 0/6/1/10 | 1/3/1/9 | 5/19/4/39 | same |
| Last-run findings decided `ignore` | 16 | 9 | 11 | 17 | 14 | 67 | all ignore |

Per rule and action (all runs):
- Mock 1: D1 ignore 6, rewrite 2 (D009 on M1-SC1-R1-F1, D010 on M1-SC2-R1-F1); D2 ignore 10; D3 ignore 1; D4 ignore 16. All 35 findings of both runs were decided (mock 1 decided run 1 and run 2).
- Mock 2: D1 ignore 1, rewrite 1 (D013 on M2-SC5-R1-F1); D3 ignore 1, rewrite 1 (D014 on M2-SC5-R1-F6), no decision 1; D2 ignore 2, no decision 2; D4 ignore 5, no decision 4.
- Mock 3: D2 ignore 3; D3 ignore 1; D4 ignore 7, no decision 2.
- Mock 4: D2 ignore 6, no decision 3; D3 ignore 1, no decision 1; D4 ignore 10, no decision 2.
- Mock 5: D1 ignore 1, no decision 1; D2 ignore 3, no decision 1; D3 ignore 1, no decision 1; D4 ignore 9, no decision 2.

Dates of the runs (field `date`): mock 1 run 1 on 2026-10-07, run 2 on 2026-10-08; mock 2 all 2026-10-08; mock 3 run 1 2026-10-08, run 2 2026-10-09; mocks 4 and 5 all 2026-10-09.

### 4.3 Checks of the numbers in other files

| Number in a file | Source | Agrees? |
|---|---|---|
| "each of the 19 findings of step 6" (mock 1, run 1) | `docs/decisions/0045-...`, 40 | Yes: 8+4+3+4 = 19 in the run 1 files. |
| "each of the 16 findings of the second run of step 6 is `ignore`. The 3 findings of rule D1 among them" | `docs/decisions/0046-...`, 19 | Yes: 5+8+0+3 = 16; D1 = 3. |
| "9 rewrites and 17 ignore (decisions D002 to D027)" | `docs/journal.md`, 147 | Yes: 17 ignore on run 1 findings; 9 rewrites = 7 of decision 0045 + D009 and D010. |
| "Step 6 ran again and has 9 findings" (mock 2) | `docs/decisions/0059-...`, 10 | Yes: 9 in the last runs. |
| "Step 6 found 11 findings in mock 3" | `docs/decisions/0064-...`, 10 | Yes: 11 in the last runs. |
| Mock 4: D2/D3 decisions D009 to D012, D014, D019, D020 (7); D4 D013, D015 to D018, D021 to D025 (10) | `docs/decisions/0069-...`, 29-30 | Yes: last runs D2 6 + D3 1 = 7; D4 10. |
| "The findings of rule D4 (9) ... D2 and D3 (4)", one D1 | `docs/decisions/0077-...`, 22-23 | Yes: 9, 3+1, 1. |
| "Runs of step 6 (all scenarios): 8, 8, 6, 6, 5"; "Findings of step 6: 35, 18, 13, 23, 19" | `academy/facts/top-of-tab-2.md`, 233-234 | Yes. |

### 4.4 Step 6 and the 7 problems of the second review of mock 1 (computed)

The 7 problems of decision 0045 (lines 30-36). Step 6 run 1 also named 5 of them: S09 (M1-SC3-R1-F1, D1), S28 (M1-SC1-R1-F2, D1), S30 (M1-SC1-R1-F3, D1), S60 (M1-SC5-R1-F2, D4), S49 (M1-SC5-R1-F4, D3). It did not name S24 (a repeat in another scenario; step 6 then compared one scenario only) or S47 (one question, two correct options that are one idea). Method: owner decisions with the reason "Covered by the rewrite of S.. (decision 0045)" in `runs/mock-01/owner-decisions.json`, matched to the findings of the run 1 files. (L1)

## 5. Stories for the Depth

### 5.1 Story (a): the confidence options that ruling 2 had to limit (rule D3, call 6b)

Origin and rule:

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | "Ruling 2" is one of two rulings of the owner of 29 September 2026, from the first build. In the first build's review, 24 questions failed on it. | `docs/lessons.md`, 22 (label line 3: "Private history of the first build. Not a source for the design.") | "Ruling 2: at most one wrong option in each scenario uses a confidence value that the model reports about itself. In the first review of Mocks 2, 4 and 5, 32 questions failed on ruling 1 and 24 on ruling 2." (These are the mocks of the first build.) | 4 |
| A2 | Decision 0006 (6 October 2026): ruling 2 applies to the new build, with two limits. | `docs/decisions/0006-...`, Decision, 20-25 | "In one scenario of one mock, at most one wrong option is the self-reported-confidence option. That option is: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger." / "1. Calibrated confidence for each field, used to send items to human review, does not count. The guide endorses it (5.5)." / "2. The option does not count when it is the correct answer." | 2 |
| A3 | Why the limit of one. | `docs/decisions/0006-...`, Reason, 31 | "The guide says that self-reported confidence scores are \"unreliable proxies for actual case complexity\" (5.2-K3), and sample question 3 in Section 9 uses such an option as a wrong option. So it is a fair wrong option. The plain reason for the limit of one: if the option appears many times, a participant can mark it wrong without thought." | 2 |
| A4 | No file has the words of the owner; an earlier summary lost the two limits. | `docs/decisions/0006-...`, How we decided, 39; `docs/lessons.md`, 5 | "The assistant wrote those briefs. No file has the words of the owner. An earlier summary of the ruling did not have the two limits." / "Lesson 3 leaves out the two limits of ruling 2. Decision 0006 is correct." | 2 / 4 |
| A5 | Decision 0019 widens limit 1 to four uses that the guide teaches (5.5-K3, 5.5-S3, 5.5-S4, 4.6-S3). | `docs/decisions/0019-...`, 23 | "The first limit is wider. A use of model confidence that the guide teaches as correct does not count as the wrong option. The guide teaches four such uses" | 2 |
| A6 | The writer does not get ruling 2. Its 21 rules (A1 to A12, B1 to B9) have no rule on confidence options; only step 6 checks it. | `src/step2_write.py`, 24-62 (no "confiden" in any `src/*.py` except `step6_check_scenario.py`, by `grep -rn -i confiden src/`); `docs/decisions/0030-...`, 67 | "Ruling 2 (at most one wrong option on self-reported confidence in each scenario) and a scene that repeats. One question cannot show them. Step 6 checks them (decision 0014)." | 1 / 2 |
| A7 | D3 is in call 6b. | `docs/decisions/0034-...`, 52, 142 | "D3 \| Ruling 2: at most one wrong option of the scenario is the self-reported-confidence option, with the limits of decisions 0006 and 0019." | 2 |

What happened, mock by mock (all D3 findings, 9 in all):

| # | Fact | Source | Exact quote | L |
|---|---|---|---|---|
| A8 | Mock 1, run 1 (2026-10-07): D3 fails in scenario 5. Three options: M1-S49 B and D, M1-S56 C. | `runs/mock-01/checks/M1-scenario-5-step6-run1.json`, finding at line 96 | "M1-S49-T1 B outputs a confidence score per finding and drops findings below a fixed threshold. M1-S49-T1 D lets a higher severity be assigned only when the model is highly confident, which is a confidence trigger. M1-S56-T1 C tells Claude to report only high-confidence findings" | 1 |
| A9 | The second review of mock 1 found the same problem (one of the 7). | `docs/reviews/M1-round1-second-review-notes.md`, 31; `docs/decisions/0045-...`, 36 | "M1-S49 \| Ruling 2: a second and a third wrong option on the confidence of the model in scenario 5" | 4 / 2 |
| A10 | Fix: owner decision D008, rewrite of M1-S49 that keeps the question and replaces options B and D. The finding itself got `ignore`, "Covered by the rewrite of S49". | `runs/mock-01/owner-decisions.json`, D008 at line 84; finding decision at line 229 | "Ruling 2 of the owner: in one scenario of one mock, at most one wrong option uses the confidence that the model reports about itself as a filter, a threshold or a trigger. This scenario already has that option in question M1-S56, option C ('only report high-confidence findings'). In this question, option B (a confidence score for each finding, with a threshold) is a second one. Option D ('only when it is highly confident') is a third one." | 1 |
| A11 | Before and after (point 4.1-S3). T1 option B: "Ask Claude to output a confidence score with each finding and drop any finding whose score falls below a fixed threshold." T1 option D: "Instruct Claude to be conservative and assign a higher severity level only when it is highly confident about the finding." T2 options A and D: "Add a concrete code example for the critical level only and leave the major and minor levels without criteria or examples." / "Write one general sentence that defines severity as the impact of an issue and use it for all three levels without examples." T2 is in the built mock. | `runs/mock-01/questions/M1-S49-T1.json`, `M1-S49-T2.json`; `mocks/mock-01.questions.json`, 1408 | (quotes in the fact) | 1 |
| A12 | Mock 1, run 2 (2026-10-08): D3 passes in scenario 5. | `runs/mock-01/checks/M1-scenario-5-step6-run2.json` | `D3=pass` (field `results`) | 1 |
| A13 | Mock 2, run 1: D3 fails on M2-S41 (options B and C). The owner rewrote it (D014): the only rewrite of a D3 finding in mocks 1 to 5. | `runs/mock-02/checks/M2-scenario-5-step6-run1.json`, finding at line 129; `runs/mock-02/owner-decisions.json`, D014 at line 120 | "Option B has Claude assign a confidence score to each finding and posts only findings above a fixed threshold. Option C tells Claude to report only high-confidence findings" / D014: "Ruling 2 of the owner: at most one wrong option of the scenario uses the model's own confidence as a filter. Options B and C both do. Write a new question on the same point. Use at most one wrong option on model confidence, and only if this scenario has no other one." | 1 |
| A14 | Mock 2, run 2 of scenario 5: D3 passes. M2-S41-T2 is in the built mock. | `runs/mock-02/checks/M2-scenario-5-step6-run2.json`; `mocks/mock-02.questions.json`, 1165 | `D3=pass` | 1 |
| A15 | Mock 2, scenario 6: 5 confidence options in 5 questions (S49, S50, S51, S52, S56), in run 1 and run 2. Recorded as a known limit, no rewrite. | `runs/mock-02/checks/M2-scenario-6-step6-run2.json`, finding at line 68; `docs/decisions/0059-...`, 27; `runs/mock-02/owner-decisions.json`, D022 at line 178 | "At least 5 wrong options use a model's own confidence rating as a filter, threshold or trigger. Only one is allowed." / "Scenario 6 has 5 wrong options on the model's own confidence: M2-S49, M2-S50, M2-S51, M2-S52 and M2-S56." / "Known limit of mock 2 (decision 0059): the findings of step 6 on model confidence. The owner decided no rewrite." | 1 / 2 |
| A16 | Mock 3, scenario 6: 4 confidence options (S07, S10, S13, S14). Known limit. | `runs/mock-03/checks/M3-scenario-6-step6-run1.json`, finding at line 170; `docs/decisions/0063-...`, 25; `docs/decisions/0064-...`, 24 | "The limit is one." / "the wrong idea \"a model's own confidence works as a filter\" is a wrong option in 4 questions (M3-S07, M3-S10, M3-S13, M3-S14)" | 1 / 2 |
| A17 | Mock 4, scenario 6: D3 names S04 B and S09 C. The second review in Cowork found S09 C; rewrite D008 replaced only option C. Run 2 still names S04 and S03; known limit. | `runs/mock-04/owner-decisions.json`, D008 at line 64; `runs/mock-04/checks/M4-scenario-6-step6-run2.json`, finding at line 99; `docs/decisions/0069-...`, 23, 29 | D008: "option C is the second wrong option about the model's own confidence in scenario 6 (ruling 2 of the owner). Option B of M4-S04 is the first." / "The program cannot change one option only, so the writer got the question with the instruction to keep everything and replace option C (D008)." / "Finding M4-SC6-R2-F4 (rule D3) still names M4-S03 and M4-S04 after the rewrite of M4-S09." | 1 / 2 |
| A18 | M4-S09 option C before: "The output schema has no confidence field, so Claude has nowhere to record its certainty and cannot filter its flags by that value." After (T2, built): "The output is not produced through tool_use with a JSON schema, so syntax errors in the responses corrupt the flag values that the lawyers receive." | `runs/mock-04/questions/M4-S09-T1.json`, `M4-S09-T2.json`; `mocks/mock-04.questions.json`, 243 | (quotes in the fact) | 1 |
| A19 | Mock 5: the rewrite of M5-S45 (a bad mark of the second review) was told to use no confidence option, because S40 already had one. | `docs/decisions/0076-...`, 23 | "No same-session idea, and no wrong option on self-reported confidence, because scenario 5 already has one in M5-S40." | 2 |
| A20 | Mock 5, run 2 of scenario 5: D3 still names M5-S40 options A and B. The owner (with the second review) ruled that option B is the "be conservative" instruction of 4.1-K2, so ruling 2 holds. | `runs/mock-05/checks/M5-scenario-5-step6-run2.json`, finding at line 109; `docs/decisions/0077-...`, 22 | "Option A has Claude report a 1-10 confidence score and downgrades blockers below seven, which is a threshold. Option B lets Claude assign the blocker level only when it is highly confident, which is a self-rated confidence trigger." / "The second review counts option B of M5-S40 (be careful and conservative) as the general instruction \"be conservative\" of point 4.1-K2, not as a self-reported confidence option. So ruling 2 holds in scenario 5: only option A is on self-reported confidence." | 1 / 2 |
| A21 | M5-S40-T1 option B (built mock): "Tell Claude to be careful and conservative, and to assign the blocker level only when it is highly confident about the risk of the finding." Same point (4.1-S3) and same kind of option as M1-S49-T1 option D, which mock 1 counted as a confidence option. See conflict X7. | `runs/mock-05/questions/M5-S40-T1.json`; `mocks/mock-05.questions.json`, 1145 | (quote in the fact) | 1 |
| A22 | Guide text of 4.1-K2 names both phrases as general instructions. | `reference/guide-records.json`, 931 | "How general instructions like \"be conservative\" or \"only report high-confidence findings\" fail to improve precision compared to specific categorical criteria" | 1 |
| A23 | Points of the questions that D3 findings named (computed): M1 4.1-S3, 4.1-S2; M2 4.1-S1; 4.6-S3, 4.2-S3, 5.2-K4, 4.4-K3, 5.5-S2; M3 4.4-S2, 4.1-K1, 4.6-S3, 4.1-S3; M4 5.2-K2, 4.1-K2, 4.1-K3; M5 4.1-S3, 4.6-S3. | field `point` of each named `runs/mock-0N/questions/*.json` | | 1 |

Summary of the fixes (computed from A8 to A21): 3 rewrites removed a second confidence option (M1-S49 D008, M2-S41 D014, M4-S09 D008); one rewrite instruction avoided a new one (M5-S45, decision 0076); 3 scenarios kept more than one and were recorded as known limits (M2 scenario 6, M3 scenario 6, M4 scenario 6); 1 finding was ruled not a violation (M5-S40). (L1/L2)

Order in time (`git log --date=iso`):

| When | Event | Commit |
|---|---|---|
| 29 September 2026 | Ruling 2 of the owner (first build) | `docs/decisions/0006-...`, 29 (no commit; before the repository) |
| 6 October 2026 | Decisions 0006, 0010, 0014, 0019, 0034 (dates in the files) | first commit `8cc3a24`, 2026-10-07 09:41:04 |
| 2026-10-07 12:51:37 | Step 6 built | `eb05725` "Build the model steps 2, 4, 5 and 6, the adapter and the command line" |
| 2026-10-07 22:50:29 | Mock 1 step 6 run 1 (D3 fails in scenario 5) | `07d1c42` |
| 2026-10-08 10:41:29 | Decision 0045 (rewrite of M1-S49 among the 7) | `72262b1` |
| 2026-10-08 10:55:43 | Rewrites ran, mock 1 step 6 run 2 (D3 passes) | `c587839` |
| 2026-10-08 20:22:56 | Mock 2: D014 rewrite of M2-S41 (ruling 2) | `eac2f0b` |
| 2026-10-08 20:52 to 20:56 | Mock 2: scenario 6 confidence findings as known limits, decision 0059 | `de0aa0c`, `d97c686` |
| 2026-10-09 10:20:12 | Mock 3: decisions 0063, 0064 (known limit) | `4011959` |
| 2026-10-09 17:13:20 | Mock 4: rewrite of M4-S09 option C (D008) | `f873cf2` |
| 2026-10-09 17:22:34 | Decision 0069 | `a74fccd` |
| 2026-10-09 22:33 to 22:36 | Mock 5: findings decided, decision 0077 (M5-S40 ruled not a violation) | `2422bac`, `f1e0904` |

### 5.2 Story (b): the rule for the findings of step 6

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | Decision 0038, part 3 only says that step 6 sends no question back. It does not say how to decide the findings. | `docs/decisions/0038-...`, 23 | "3. **Step 6 sends no question back.** It runs when all 60 slots have the status `passed`. Each of its findings goes into the report: `fail` and `cannot_decide`." | 2 |
| B2 | Mock 1, run 1: the owner's rule for the 19 findings. | `docs/journal.md`, 147 | "The owner set a rule for the 19 findings of step 6: ignore a finding that the 7 cover, rewrite the newer question of a D1 finding that the 7 do not cover, ignore the rest." | 4 |
| B3 | The same rule in the run file. | `runs/mock-01/owner-decisions.json`, line 153 (and others) | "Rule of the owner: a finding that is not D1 and that the rewrites do not cover is ignored." | 1 |
| B4 | A D4 finding ignored with a reason: the fact is only in a wrong option. | `runs/mock-01/owner-decisions.json` (target M1-SC3-R1-F2); `runs/mock-01/checks/M1-scenario-3-step6-run1.json`, 66 | "The fact is in a wrong option of S02, so a participant cannot know that it is true." | 1 |
| B5 | Mock 1, run 2: all 16 findings ignored; the 3 D1 findings are known limits. | `docs/decisions/0046-...`, 19, 47 | "The owner also decided: each of the 16 findings of the second run of step 6 is `ignore`. The 3 findings of rule D1 among them are known limits too." / "'I do not want another rewrite round. Record them as known limits of mock 1.'" | 2 |
| B6 | Mock 2: the rule first appears: D4 ignored, D2 and D3 known limits. | `docs/decisions/0059-...`, 30, 40 | "The 5 findings of rule D4 (a question that gives away the answer of another), M2-SC5-R2-F2 to F6, are ignored." / "The owner decided: \"Record these as known limits of mock 2, with no rewrites\", \"Ignore the 5 findings of rule D4\", and \"Accept mock 2 and build its files\"." | 2 |
| B7 | Mock 3: the same treatment, suggested by the assistant. | `docs/decisions/0064-...`, 14, 34 | "The same treatment as for mock 2: ignore the findings of rule D4, and record the findings of rules D2 and D3 as known limits." / "The assistant suggested the same treatment as for mock 2. The owner said \"agree\"." | 2 |
| B8 | The reason given (mock 3). | `docs/decisions/0064-...`, 30 | "Plain reason: the owner and the second review marked each question good. ... A rewrite for each would cost a marking round and can make new findings." | 2 |
| B9 | Mock 4: the same rule. | `docs/decisions/0069-...`, 41 | "\"the step 6 findings of mock 4 follow the rule of mocks 2 and 3\"" | 2 |
| B10 | Mock 5: the rule, and "another kind" goes to the owner first. | `docs/decisions/0077-...`, 35 | "The owner said: \"use the same rule as mocks 2 to 4 ... If a finding is of another kind, show it to me first.\" The assistant showed the D1 finding and suggested a known limit. The owner said yes" | 2 |
| B11 | The D1 finding of mock 5, a known limit. | `docs/decisions/0077-...`, 23 | "Option D of M5-S02 (spawn the subagents at the same time) is the answer of M5-S05 (emit all Task calls in one response)." | 2 |
| B12 | The rule went into diagram 08 and the build guide after mock 5. | `git log`: `5244bf6` 2026-10-09 22:47:19; `docs/journal.md`, 38 | "The rule for the step 6 findings in diagram 08 and step 6; the build guide section of step 0" | 1 / 4 |
| B13 | Decision 0078 records the diagram lines of 0059, 0064, 0069. | `docs/decisions/0078-...`, 27 | "Diagram 08 (step 6) now shows the rule of the owner for the findings that these decisions used: D4 ignored, D2 and D3 recorded as known limits, any other kind to the owner." | 2 |
| B14 | Result (computed, section 4.2): of the 67 findings in the last runs, all 67 got `ignore`. Rewrites came only from run 1 of mocks 1 and 2 (4 in all: 3 D1, 1 D3). | run files | | 1 |

### 5.3 Story (c): rule C3 over the whole mock (decision 0052)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| C1 | The cause: step 6 did not find M1-S10 and M1-S24, the same question in two scenarios. | `docs/decisions/0052-...`, Question, 10 | "In mock 1, step 6 did not find M1-S10 and M1-S24, the same question in two scenarios. What does step 6 change?" | 2 |
| C2 | It was change 4 of decision 0046. | `docs/decisions/0046-...`, 36 | "4. Step 6 compares the questions of one scenario only." | 2 |
| C3 | The second review found it; the owner rewrote M1-S24 (D003). | `runs/mock-01/owner-decisions.json`, D003 | "Repeat of a question in a different scenario. Question M1-S10 (scenario 3) is the same question: yesterday an investigation in a named Claude Code session, nothing has changed since then, continue it today." | 1 |
| C4 | The decision: code only; C3 compares all 60; no new model call. | `docs/decisions/0052-...`, 21-23 | "1. Rule C3 compares each question of the scenario with the other questions of the scenario, and with the current questions of the other 3 scenarios." / "3. No new model call. Calls 6a and 6b still read the 15 questions of one scenario." | 2 |
| C5 | The reason: the point groups now prevent the case of mock 1. | `docs/decisions/0052-...`, 28 | "The point groups (decisions 0047 and 0048) now prevent the case of mock 1: 1.7-K1 and 1.7-S1 are in one group, so no mock gets both." | 2 |
| C6 | Left open: a copy with other words in two scenarios. | `docs/decisions/0052-...`, 34 | "A copy with different words in two scenarios. Only a model call can find it." | 2 |
| C7 | Code before and after: the docstring said "Known limit: C3 compares the questions of one scenario only." | `git show 8e8b3b4 -- src/step6_check_scenario.py` (2026-10-08 14:32:21) | `-    is a finding. Known limit: C3 compares the questions of one scenario only."""` | 1 |
| C8 | Computed: the exact-text C3 would not have found the mock 1 case. The texts of M1-S10-T1 and M1-S24-T1 differ (normalized as in code). | `runs/mock-01/questions/M1-S10-T1.json`, `M1-S24-T1.json`; `src/step6_check_scenario.py`, 40-41 | S10: "Yesterday you investigated why the synthesis subagent in your multi-agent research system drops citations from web search results. ..." / S24: "Yesterday you used Claude Code to investigate why your support agent calls escalate_to_human for simple refund requests. ..." | 1 |
| C9 | Computed: C3 found nothing in mocks 2 to 5 (0 C3 findings in 33 run files; mock 1 ran before the change). | run files | | 1 |
| C10 | From mock 2, repeats across scenarios and mocks are checked in step 4 (rule B9), not in step 6. | `docs/journal.md`, 91 | "The assistant suggested the check in step 4, not in step 6, and the owner agreed." | 4 |
| C11 | Order: mock 1 built 2026-10-08 11:06:10 (`26477e1`); decision 0046 11:04:46 (`c5ec7dd`); decision 0052 and code 14:32:21 (`8e8b3b4`); mock 2 run 1 16:56:24 (`d3a8cef`). | `git log --date=iso` | | 1 |

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step6_check_scenario.py` | 1-9 | The docstring: the whole step in 9 lines. |
| `src/step6_check_scenario.py` | 17-20 | The exact texts of D1, D4 (call 6a) and D2, D3 (call 6b). Line 20 is rule D3 (ruling 2). |
| `src/step6_check_scenario.py` | 26-55 | `code_count`: C2 stops the run, C3 compares the text over the whole mock. |
| `src/step6_check_scenario.py` | 77-88 | `check`: the two calls, 6a with all of each question, 6b with only the wrong options. |
| `src/control.py` | 340-344 | Step 6 runs only when all slots passed, and before the marking round. |
| `src/control.py` | 410-423 | `_step6_current`: runs again only when the fingerprints changed. |
| `src/control.py` | 436-453 | `_checked_scenario`: an answer that is not valid is a failed call; only C3 may name another scenario. |
| `src/control.py` | 455-477 | `_run_step6`: the finding IDs and the record. |
| `src/control.py` | 584-594 | `open_findings`: only the last run counts; a rewrite does not hide the others. |
| `src/control.py` | 596-617 | `findings_wait`: "Mark the questions first. Then decide on the findings of step 6." |
| `src/control.py` | 654-663 | `decide` for `ignore` and `rewrite`. |
| `tests/test_control.py` | 202-231 | Test (d): ignore then accept; `cannot_decide` waits; a decision before the marks is refused. |
| `tests/test_control.py` | 428-452 | Tests of decision 0052 (C3 over the mock). |
| `tests/test_model_steps.py` | 431-447 | Tests of C2 and C3 in `code_count`. |
| `git show 8e8b3b4 -- src/step6_check_scenario.py` | | The diff of decision 0052. |
| `runs/mock-01/checks/M1-scenario-5-step6-run1.json` | 96 onward | The real D3 finding M1-SC5-R1-F4. |
| `runs/mock-01/owner-decisions.json` | 84 onward | D008, the rewrite of M1-S49 under ruling 2. |
| `docs/diagrams/08-form-draft.json` | 1-30 | The form of the answer of a call. |

## 7. A figure

One figure could show (boxes and arrows with verbs):

1. [60 questions, all `passed`] --control starts--> [Code: C2 counts against the plan; C3 compares the text with all 60] (`src/control.py`, 340-343; `src/step6_check_scenario.py`, 26-55)
2. [15 questions of one scenario] --all text, marks, reasons--> [Call 6a: D1 same scene, D4 gives away] (`src/step6_check_scenario.py`, 82, 86)
3. [15 questions of one scenario] --only wrong options + reasons--> [Call 6b: D2 wrong idea in >2 questions, D3 >1 confidence option] (lines 83-87)
4. [C2 fails] --stops--> [run stops with an error] (line 35, 39)
5. [results] --code checks the answer--> [invalid: run the call again, at most 3] (`src/control.py`, 30, 436-453)
6. [fail / cannot_decide] --gets an ID--> [finding M1-SC5-R1-F4] --waits--> [owner, after the marks] (`src/control.py`, 461-477, 596-617)
7. [owner] --ignore--> [closed / known limit]; --rewrite--> [step 5 → steps 3, 4 → step 6 for that scenario only] (`src/control.py`, 249-269, 654-663)

A real example for the figure: M1-SC5-R1-F4 (D3) → rewrite D008 of M1-S49 → run 2: D3 pass (section 5.1, A8 to A12).

Numbers a figure could carry (section 4.2): 33 runs, 108 findings, 57 of them D4; 67 findings in last runs, all `ignore`; 4 rewrites; 0 C3 findings.

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| X1 | Point 5.2-K3 is in a popup of diagram 08, not in the build guide table (academy decision 0024). | `docs/diagrams/08-step-6-check-the-complete-mock.html`, 273, popup `D3`: `"id": "5.2-K3", "text": "Why sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity"` (L3) | `docs/build-guide/step-6-check-the-complete-mock.md`, 36-43: 4.6-K3, 4.6-S2, 4.1-K1, 5.3-K4, 4.3-K1, 4.3-S3 only (L3). Decision 0006, line 43, lists "5.2-K3, 5.5-K3" (L2). |
| X2 | Point 1.6-K2 for step 6. | `docs/decisions/0014-...`, 43: "4.6-K3, 4.6-S2, 1.6-K2" (L2). `academy/facts/top-of-tab-2.md`, conflict X8: diagram 01 says "task statements 4.6 and 1.6" for step 6 (L3). | `docs/build-guide/step-6-check-the-complete-mock.md`, 36-43: no 1.6-K2 (L3). `docs/decisions/0034-...`, 162: "4.6-K3, 4.6-S2, 4.1-K1, 5.3-K4" (L2). |
| X3 | What rule C2 checks. | `docs/decisions/0034-...`, 34: "The counts agree with the plan: for each scenario, each domain, each task statement and each question type." (L2). Diagram 08 popup `C2`: "Code counts the questions for each scenario, each domain, each task statement and each question type." (L3) | `src/step6_check_scenario.py`, 32-39: compares the slot IDs of the scenario with the plan, and `select` and the number of options of each question with its slot. No count by domain or task statement (L1). |
| X4 | Rule C1: a finding or an error? | `docs/decisions/0034-...`, 37: "If rule C1 or C2 fails, the step stops with an error that names the cause" (L2). Diagram 08 popup `C1`: example finding "Slot M1-S41 has no question that passed." (L3) | `src/step6_check_scenario.py`, 6-7: "The control already checked rule C1: it starts step 6 only when each slot has the status passed." `src/control.py`, 342: step 6 does not start; no error, no finding (L1). |
| X5 | Fields of the step 6 record. | `docs/decisions/0034-...`, 117, 122: fields `code_count` ("The results of rules C1 to C3") and `model` (L2). | All 33 run files have only `date, findings, fingerprints, mock, results, run, scenario, verdict`; `model` is inside each result; C3 is in `results` only when it fails (`src/control.py`, 471-475) (L1). |
| X6 | "For mocks 2 to 5 the owner decided the findings by one rule" (D2/D3 = known limit). | `docs/build-guide/step-6-check-the-complete-mock.md`, 18 (L3); diagram 08 popup `finding`: "The rule of the owner since mock 2" (L3). | `runs/mock-02/owner-decisions.json`, D014 (line 120): a `rewrite` of the D3 finding M2-SC5-R1-F6, and D013 a rewrite of the D1 finding M2-SC5-R1-F1, in round 1 of mock 2 (L1). The rule of decision 0059 covers the 9 findings of the last runs only. |
| X7 | Is "assign the higher level only when highly confident" a ruling 2 option? | `runs/mock-01/owner-decisions.json`, D008: "Option D ('only when it is highly confident') is a third one." M1-S49-T1 D: "Instruct Claude to be conservative and assign a higher severity level only when it is highly confident about the finding." (L1) | `docs/decisions/0077-...`, 22: "The second review counts option B of M5-S40 (be careful and conservative) as the general instruction \"be conservative\" of point 4.1-K2, not as a self-reported confidence option." M5-S40-T1 B: "Tell Claude to be careful and conservative, and to assign the blocker level only when it is highly confident about the risk of the finding." (L2 / L1). Both questions are on point 4.1-S3. |
| X8 | Decision 0014 sends a named question back; later decisions do not. (Resolved in the records by a later decision; listed for completeness.) | `docs/decisions/0014-...`, 25: "A question that this step names goes back to step 5 (decision 0013)." Status line 4: "accepted" (L2). | `docs/decisions/0038-...`, 23: "Step 6 sends no question back." `docs/decisions/0034-...`, 14 names the change (L2). Code `src/step6_check_scenario.py`, 8 (L1). |
| X9 | The control check named in diagram 08 popup `valid`. | Diagram 08 popup `valid`: "each finding must name only current questions of this scenario." (L3) | `src/control.py`, 442: for C3 the allowed IDs are `own \| {q["question_id"] for q in others}` (L1). Diagram 08 popup `C3` states the exception, so the popups agree with each other only together. |
| X10 | Diagram 08 says the number 2 of D2 "can change after the first runs". | Diagram 08 popup `D2`: "The number 2 is a guess. It can change after the first runs." (L3) | `src/step6_check_scenario.py`, 19: still "more than 2" after 5 mocks; no decision changes it (`grep -n '\bD2\b' docs/decisions/*.md` finds only uses of the rule in 0034, 0059, 0063, 0064, 0069, 0077, 0078) (L1). Not a contradiction; the diagram text is out of date only if read as a plan. |

## 9. Not found

1. The words of the owner for ruling 2 (29 September 2026). Decision 0006, line 39: "No file has the words of the owner." The first-build briefs in `CCAR-F Mocks v2/reference/first-build/rubric/` were not opened by this agent (outside the source list).
2. A decision file for the owner's rule on the 19 findings of mock 1 run 1 ("rewrite the newer question of a D1 finding that the 7 do not cover, ignore the rest"). It is only in `docs/journal.md`, 147 and in the reasons of `runs/mock-01/owner-decisions.json`. Decision 0045, line 40 names the 19 findings but not the rule.
3. A reason why D4 findings are ignored as a class. Decisions 0059, 0064, 0069, 0077 give a general reason (each question marked good; a rewrite costs a marking round). Only one D4 finding has its own reason (M1-SC3-R1-F2, section 5.2 B4).
4. A per-step count of model calls or cost for step 6. The usage files (`runs/mock-0N/usage/run-*.json`) have only totals per run (`calls`, `dollars`). The figure 66 calls is 2 × run files, a minimum; retries of a call that succeeded are not recorded.
5. A case of `cannot_decide`, a C2 failure, a C3 finding, or a step 6 error record in mocks 1 to 5. None exists.
6. A measure of how often the step 6 findings were right. No source checks the D4 or D2 findings against a person, except the mock 1 overlap with the second review (section 4.4).
7. A rule or instruction to the writer about ruling 2 in `src/step2_write.py`. None; the writer learns of it only through a rewrite reason (D008, D014, decision 0076).
8. A dated copy of the documentation pages in `academy/sources/` (academy decision 0030) for the deviation of section 3. Only `docs/sources/2026-10-07-*.md` exist. This agent may change no other file.
9. `docs/lessons.md` has no lesson on step 6 or D3 from the new build (`grep -n -i 'step 6\|D3' docs/lessons.md`: no match). Its only mention of ruling 2 is first-build lesson 3 (lines 5, 21-22, 112).
