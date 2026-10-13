# Fact sheet: tab 2, step 3 "Check by code"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `f714b83` (branch `main`, clean).
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = Anthropic documentation (academy decision 0014).
- Line numbers are for the files at commit `f714b83`. "L" = level of trust.
- The tests ran on 14 October 2026 with no API key in the environment: `python3 -m unittest discover -s tests` gives "Ran 228 tests ... OK". `tests/test_step3_check_code.py` has 28 tests (`grep -c "def test" tests/test_step3_check_code.py`).
- Files that this agent did not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, and all personal files of the owner. No model call was made. `src/run.py` was not run.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | Code checks each question against rules A1 to A12, which have an exact answer. No model works in this step. | `src/step3_check_code.py`, 3-4 | "Code checks the rules A1 to A12, which have an exact answer. No model works in this step." | 1 |
| O2 | The same, in the build guide: the check comes before a model looks at the question. | `docs/build-guide/step-3-check-by-code.md`, 9 | "Before a model looks at a question, code checks the 12 rules that have one exact answer (rules A1 to A12):" | 3 |
| O3 | The reason for the order: a question with a simple defect does not use a model call. | `docs/build-guide/step-3-check-by-code.md`, 18 | "The check is cheap and fast, so a question with a simple defect does not use a model call." | 3 |
| O4 | The first decision of the step: code checks the rules with an exact answer, before the model check. | `docs/decisions/0011-...`, 20 | "Step 3 is the code check. Code checks each question against the rules that have an exact answer. No model works in this step." | 2 |
| O5 | Status: built. It ran in the test of 7 October 2026 and in mocks 1 to 5 (7 to 9 October 2026). | `docs/build-guide/step-3-check-by-code.md`, 3 | "Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026." | 3 |
| O6 | Changed once after it was built: rule A12 on 8 October 2026. | `docs/build-guide/README.md`, 17 | "built (7 October 2026), changed on 8 October 2026 (rule A12)" | 3 |
| O7 | Step 3 is the one check step with no model. The control calls it directly, not through the retry wrapper `_call` that the model steps use. | `src/control.py`, 368-370 (step 3) against 372-373 (step 4) | `v = self.steps.check_code(question, slot)` / `v = self._call("check_model", ...)` | 1 |

## 2. Explanation facts: the mechanism

### 2.1 Inputs, outputs, the order of the checks

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | Input: one question record and its slot. Output: a verdict `pass` or `fail` with a list of findings. | `src/step3_check_code.py`, 77-78 | `def check(question, slot, rules=None):` / `"""Return {"verdict": "pass" or "fail", "findings": [...]}.` | 1 |
| E2 | The question record has `question`, `select` and `options`. Each option has `letter`, `text`, `correct`, `reason`. | `src/step3_check_code.py`, 7-8 | "A question record has `question`, `select` and `options`. Each option has `letter`, `text`, `correct` and `reason` (decision 0029)." | 1 |
| E3 | The control calls step 3 when a try has no step 3 verdict yet, and saves the verdict as a new record. | `src/control.py`, 368-370 | `if self.verdict(question["question_id"], 3) is None:` / `v = self.steps.check_code(question, slot)` / `self._save_verdict(question, 3, v)` | 1 |
| E4 | The verdict record has `question_id`, `step`, `verdict`, `findings`, `fingerprint`, `date`. It is written as a new file, never over an old one. | `src/control.py`, 394-401; 94-99 | `record = {"question_id": ..., "step": step, "verdict": v["verdict"], "findings": v["findings"], "fingerprint": fingerprint(question), "date": self.today()}` / `"""Write a record. A record is never written over."""` | 1 |
| E5 | A real record: `runs/mock-01/checks/M1-S01-T1-step3.json`. | that file, 1-8 | `"step": 3,` `"verdict": "pass",` `"findings": [],` `"fingerprint": "07e2e917..."` `"date": "2026-10-07"` | 1 |
| E6 | The fingerprint is a SHA-256 of what a participant sees: question ID, question, `select`, and each option with letter, text, mark and reason. | `src/control.py`, 52-66 | `"""SHA-256 of what a participant sees (decision 0036).` | 1 |
| E7 | Each finding has the same six fields as the findings of step 4: `step`, `rule`, `detail`, `letter`, `point`, `other_questions`. | `src/step3_check_code.py`, 35-37 | `return {"step": 3, "rule": rule, "detail": detail, "letter": letter, "point": None, "other_questions": []}` | 1 |
| E8 | A question that fails step 3 does not go to step 4. Step 4 runs only when step 3 says `pass`. | `src/control.py`, 206-213 | `if v3 is None or (v3["verdict"] == "pass" and v4 is None):` / `state["status"] = "to_check"` | 1 |
| E9 | Run files agree with E8: in mocks 1 to 5, no try that failed step 3 has a step 4 record (0 of 11). Step 4 records = step 3 passes in each mock (83, 91, 99, 107, 97). | section 4 | method in 4.1 | 1 (computed) |
| E10 | On a fail, the try goes to step 5: the writer gets the failed question and the findings of steps 3 and 4. | `src/control.py`, 288-294 | `for step in (3, 4): v = self.verdict(question["question_id"], step) ... findings.extend(v["findings"])` | 1 |
| E11 | A slot is `passed` only when steps 3 and 4 both say `pass` for the current try. | `src/control.py`, 211-213 | `if v3["verdict"] == "pass" and v4["verdict"] == "pass": state["status"] = "passed"` | 1 |
| E12 | Before step 8 builds, code checks again that each question has a valid pass of step 3 with the same fingerprint. | `src/control.py`, 743-746 | `if v is None or v["verdict"] != "pass" or v["fingerprint"] != fp:` / `"%s: no valid pass of step %d"` | 1 |
| E13 | A question with the status `cannot_write` does not go to step 3. The slot becomes `open`. | `src/control.py`, 202-205; `docs/decisions/0031-...`, 59 | `state["open_reasons"] = ["cannot_write"]` / "A question with the status `cannot_write` does not go to step 3." | 1 / 2 |
| E14 | `rules` can limit the check to some rules. Used for the 12 sample questions of the guide (rules A4 to A11, which need no slot and no reason). | `src/step3_check_code.py`, 79-81; `tests/test_step3_check_code.py`, 188-198 | "`rules` limits the check to some rules, for example A4 to A11 for the sample questions of the guide (decision 0024)." | 1 |
| E15 | The writer of step 2 gets the same A rules in its list, with the same numbers. | `src/step2_write.py`, 31-45 | "Rules for a good question. Code checks group A. A second model checks group B." | 1 |

### 2.2 The 12 rules (what each checks)

All from `src/step3_check_code.py` (L1). The short text agrees with `docs/decisions/0030-...`, 27-37 (A1 to A11) and `docs/decisions/0053-...`, 21-23 (A12) (L2).

| Rule | What code checks | Lines | Exact quote of the code or its finding text |
|---|---|---|---|
| A1 | The form is complete: a question text, options, and each option has a text, a mark (`true`/`false`) and a reason. The letters are A, B, C... in sequence. | 40-74 | `"The question has no text."`, `"The question has no options."`, `"%s has no %s."`, `"The options do not have the letters A to %s in sequence."` |
| A2 | The number of options is the number of the slot (4 or 5). | 94-95 | `"The question has %d options. The slot needs %s."` |
| A3 | The number of options marked correct is the `select` of the slot (1 or 2). | 96-99 | `"%d options are marked correct. The slot needs %s."` |
| A4 | No two options have the same text (code ignores capital letters and extra spaces). | 100-107 | `key = " ".join(o["text"].lower().split())` / `"Options %s and %s have the same text."` |
| A5 | No question text, option text or reason names a letter or a different option: "Option B", "all of the above", "none of the above", "both A and C". | 19-22, 108-116 | `LETTER_WORDS = re.compile(r"\b((?i:option) [A-E]\b|(?i:all of the above)|(?i:none of the above)|(?i:both) [A-E] (?i:and) [A-E]\b)")` |
| A6 | The question has 25 to 110 words. Each option has 5 to 45 words. | 14-15, 117-124 | `QUESTION_WORDS = (25, 110)   # A6` / `OPTION_WORDS = (5, 45)       # A6` |
| A7 | The average words of the correct options are at most 1.3 times the average words of the wrong options. | 16, 125-131 | `LONGER_LIMIT = 1.3           # A7` |
| A8 | The question text ends with "?". | 132-133 | `"The question does not end with a question mark."` |
| A9 | The question text has 2 to 5 sentences. | 17, 134-137 | `SENTENCES = (2, 5)           # A9` |
| A10 | Each option is one sentence. | 138-141 | `"Option %s has more than one sentence."` |
| A11 | Not a negative question: no "NOT" or "EXCEPT" in capital letters in the question text, and no "not" or "except" in small letters in its last sentence. The options do not count. | 142-150 | `m = re.search(r"\b(NOT|EXCEPT)\b", text)` / `m = re.search(r"\b(not|except)\b", last)` / `# Decision 0038, part 8. The options do not count.` |
| A12 | When the slot has `longest_may_be_correct: false`, a wrong option must be longer (in characters) than each correct option. An equal length fails. A slot with no field (mock 1) does not get the rule. | 151-160 | `if right and wrong and max(right) >= max(wrong):` / `"The longest option is a correct option (%d characters). The slot needs a wrong option that is longer than each correct option."` |

Facts on the method:

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| R1 | How code counts a sentence, and its known limit. | `src/step3_check_code.py`, 29-32 | "A sentence ends with \".\", \"?\" or \"!\" and a space comes after it (decision 0031). Known limit: a dot and then a quote mark does not end a sentence." | 1 |
| R2 | A second known limit of the same method: an abbreviation with a dot. | `docs/decisions/0031-...`, 53 | "It can count wrong when a text has an abbreviation with a dot." | 2 |
| R3 | The limits of A6 and A7 are the range of the 12 sample questions of the guide, with a margin. The margin is a choice of the assistant with no source. | `docs/decisions/0031-...`, 43-47, 69 | "The size of the margin is a choice of the assistant. It has no source." | 2 |
| R4 | The measured range: questions 33 to 91 words, options 7 to 35 words, largest ratio 1.21. A8 to A11 true for 12 of 12. | `docs/decisions/0031-check-sample-lengths.py` and `docs/decisions/0037-check-sample-properties.py`, run on 14 October 2026 | output: "question words: 33 to 91", "option words: 7 to 35", "largest ratio: 1.21", "all 12 pass"; "A8 true for 12 of 12" ... "A11 true for 12 of 12" | 1 (computed) |
| R5 | A11 is weaker than what the script measured. | `docs/decisions/0031-...`, 69; `docs/build-guide/step-3-check-by-code.md`, 18 | "The limit of A11 is weaker than what the script measured: it permits \"not\" outside the last sentence." | 2 / 3 |
| R6 | A12 counts characters, A6 and A7 count words. The length in words for A12 is not decided. | `docs/decisions/0053-...`, 35 | "The length in words. Rule A12 counts characters." | 2 |
| R7 | The A5 word list is a first list, not decided. | `src/step3_check_code.py`, 19-20; `docs/decisions/0031-...`, 73 | "The exact list is not decided (decision 0031). This is the first list" | 1 / 2 |
| R8 | A5 needs a capital letter, so "the option a reviewer prefers" passes. | `src/step3_check_code.py`, 21; `tests/test_step3_check_code.py`, 162-164 | "The letter must be a capital letter, so that \"the option a reviewer prefers\" passes." | 1 |
| R9 | The other rules run also when A1 fails, on each option that has a text. | `src/step3_check_code.py`, 88-89 | "The other rules run on each option that has a text, also when A1 fails" | 1 |
| R10 | The line "Select N." is not part of the question text. Code copies it from the slot, so no rule checks it, and A6 does not count it. | `docs/decisions/0030-...`, 39 | "Code copies it from the slot. So no rule is necessary for that line, and rule A6 does not count it" | 2 |
| R11 | A12 slots: the seed sets `longest_may_be_correct: true` on 13 of 52 one-answer slots and 3 of 8 two-answer slots (the chance numbers). | `src/step1_plan.py`, 46-48, 446-453 | `LONGEST_MAY_BE_CORRECT = {1: 13, 2: 3}` | 1 |
| R12 | The plans agree with R11: mocks 2 to 5 each have 13 `true` of 52 and 3 `true` of 8. Mock 1 has no field (60 slots). | `runs/mock-0N/plan.json` | method 4.1 | 1 (computed) |

### 2.3 What happens on a fail, and when code cannot read

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| F1 | A fail goes to step 5 with the findings. | `docs/decisions/0031-...`, 60; `docs/build-guide/step-3-check-by-code.md`, 20 | "A question that fails goes to step 5 with its findings (decision 0013)." / "Each finding names the rule and the detail, so the writer of step 5 knows what to change." | 2 / 3 |
| F2 | The new try goes through step 3 again. | diagram 05, popup "fail" (`docs/diagrams/05-step-3-check-by-code.html`, 157) | "The new question goes through this check again." | 3 |
| F3 | A record that is not a question (not a JSON object) fails A1. It is not a pass. | `src/step3_check_code.py`, 44-45; `tests/test_step3_check_code.py`, 159-160 | `return [finding("A1", "The question record is not complete.")], []` / `self.assertEqual(rules_of(check("not a record", SLOT))[0], "A1")` | 1 |
| F4 | The design says: if the question file is missing or cannot be read, the step reports an error and never says "pass". | `docs/decisions/0031-...`, 28; `docs/build-guide/step-3-check-by-code.md`, 20 | "It can fail when the file of the question is missing or cannot be read. Then the step reports an error. It never returns \"pass\" for a question that it did not read." | 2 / 3 |
| F5 | In the code, the control reads the question file (`_question`, a plain `json.load`) before it calls step 3. No `try` catches a read error there, and `src/run.py` catches only `Refused` and `RunStopped`. So a missing or broken file stops the run with a Python error, and no verdict is saved. No pass is possible, but no error record is written either. (Reading of the code; not run.) | `src/control.py`, 296-297, 365; `src/run.py`, 106-112 | `def _question(self, question_id): return self._read("questions", question_id + ".json")` / `except Refused as e:` / `except RunStopped as e:` | 1 |
| F6 | No test covers a missing or unreadable question file (search of `tests/` for "missing", "cannot be read", "JSONDecode": no such test). | `tests/` | (none) | 1 |

### 2.4 Why code for group A and a model for group B

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| W1 | The two groups. | `docs/decisions/0030-...`, 21, 73 | "The code check of step 3 checks group A. The model check of step 4 checks group B." / "code checks a rule that has one correct answer, and a model checks a rule that needs judgment." | 2 |
| W2 | The rules that need judgment are step 4. | `docs/decisions/0011-...`, 41; `docs/decisions/0012-...`, 20 | "The rules that need judgment are a different step (decision 0012)." / "For each question that passed step 3, a new API call checks the question against the rules that need judgment." | 2 |
| W3 | Reason in decision 0011: 1.4-K1, 1.4-K2. | `docs/decisions/0011-...`, 29 | "The guide separates \"programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance\" (1.4-K1), and says that prompt instructions alone have a non-zero failure rate (1.4-K2)." | 2 |
| W4 | Reason in decision 0011: a schema does not stop content errors (4.3-K3, 4.4-K4). | `docs/decisions/0011-...`, 31 | "A fixed output format is not sufficient. ... So code must check the content of a record." | 2 |
| W5 | Reason in decision 0011: an empty output must not pass (5.3-K4). | `docs/decisions/0011-...`, 33 | "An empty output must not pass as a success." | 2 |
| W6 | What the guide does not cover: the order (code before model, to save calls) and the rules on the quality of a question. | `docs/decisions/0011-...`, 35 | "The guide does not cover this: that the code check comes before the model check, to save model calls, and the rules on the quality of an exam question" | 2 |
| W7 | The writer's form cannot count the options, so the design does not rely on it. Step 3 counts. | `docs/decisions/0029-...`, 122 | "So the design does not rely on the form for a count. The code check of step 3 checks the number of options and the number of correct answers." | 2 |
| W8 | Docs check: structured outputs do not support array length limits beyond `minItems` 0 or 1. So the schema cannot say "exactly 4 options". | https://platform.claude.com/docs/en/build-with-claude/structured-outputs, section "JSON Schema limitations", list "Not supported", read live on 14 October 2026 | "Array constraints beyond `minItems` of 0 or 1"; list "Supported features": "Array `minItems` (only values 0 and 1 supported)". Agrees with `docs/sources/2026-10-07-anthropic-docs-structured-outputs.md`, 2628 and 2637, and `docs/decisions/0040-...`, 58. | Docs |
| W9 | The writer's schema has no count on `options`. | `docs/diagrams/04-form-schema-draft.json`, 15-29 (loaded by `src/step2_write.py`, 16) | `"options": { "type": "array", ... "items": {...} }` (no `minItems`, no `maxItems`) | 1 |
| W10 | The writer is told the count in words only. | `src/step2_write.py`, 136 | `"Write %d options. Mark exactly %d of them correct."` | 1 |
| W11 | Also a code part in step 4: rule B6 ("named" in the guide) is decided by a code search, not by the model. | `docs/decisions/0030-...`, 57-58 | "\"Named\" means: the name is in the text of `reference/guide-records.json`. Code decides this, not the model." | 2 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-3-check-by-code.md`, lines 28-34 (L3). A script on 14 October 2026 checked each guide text and each task statement title of the table against `reference/guide-records.json`: all 5 texts and all 4 titles are exact.

| Point | Line | Task statement | How the step uses it (exact, from the table) |
|---|---|---|---|
| 1.4-K1 | 30 | 1.4: Implement multi-step workflows with enforcement and handoff patterns | "Written for the order of the steps of an agent workflow. Here: a rule with one exact answer is checked by code, not by a model." |
| 1.4-K2 | 31 | 1.4 | "The same context. Here: an instruction to a model can fail, so code checks the rules that code can check." |
| 4.3-K3 | 32 | 4.3: Enforce structured output using tool use and JSON schemas | "Written for the extraction of data. Here: the form of the answer does not stop content errors, so code checks the content." |
| 4.4-K4 | 33 | 4.4: Implement validation, retry, and feedback loops for extraction quality | "The same context. Here: the same difference between errors of format and errors of meaning." |
| 5.3-K4 | 34 | 5.3: Implement error propagation strategies across multi-agent systems | "Written for errors between agents. Here: an error must never look like a pass." |

Guide texts (from `reference/guide-records.json`, same as the table):
- 1.4-K1: "The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering"
- 1.4-K2: "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate"
- 4.3-K3: "That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)"
- 4.4-K4: "The difference between semantic validation errors (values don't sum, wrong field placement) and schema syntax errors (eliminated by tool use)"
- 5.3-K4: "Why silently suppressing errors (returning empty results as success) or terminating entire workflows on single failures are both anti-patterns"

Decision 0011 lists the same 5 points (`docs/decisions/0011-...`, 45: "1.4-K1, 1.4-K2, 4.3-K3, 4.4-K4, 5.3-K4"). Diagram 01, popup "3", has the same 5 (`docs/diagrams/01-pipeline-overview.html`, JSON `stepdata`). The page summary line already says "task statements 1.4, 4.3, 4.4, 5.3" (`academy/pages/behind-the-mocks.html`, part `#step-3`).

Facts from the runs that support the uses:
- T1 (1.4-K2, 4.3-K3): the writer was told "Write 5 options" and wrote 6 options twice: M4-S27-T3 and M5-S60-T2 (section 4.3). The schema could not stop it (W8, W9). Step 3 failed both on A2 (and A1). (L1)
- T2 (5.3-K4): no try in mocks 1 to 5 lacks a step 3 record: 488 tries, 488 step 3 records (section 4.2). (L1)
- T3: 4.4-K1 is in a popup of diagram 05 but not in this table. See conflict C1.

## 4. Numbers, per mock, with method

### 4.1 Method

The script reads only the run files and the code of step 3. It makes no model call. Run: `python3 -I count3.py ~/ccar-f-mock-generator`. It ran on 14 October 2026 (a copy was in the scratchpad of this agent, not in the repository).

```python
import glob, json, os, sys
from collections import Counter
ROOT = sys.argv[1]
sys.path.insert(0, os.path.join(ROOT, "src"))
from control import fingerprint
import step3_check_code as s3
def rd(p):
    with open(p, encoding="utf-8") as f: return json.load(f)
for m in range(1, 6):
    F = os.path.join(ROOT, "runs", "mock-%02d" % m)
    qs = {q["question_id"]: q for q in (rd(p) for p in sorted(glob.glob(F + "/questions/M%d-S*-T*.json" % m)))}
    c3 = {r["question_id"]: r for r in (rd(p) for p in glob.glob(F + "/checks/M%d-S*-T*-step3.json" % m))}
    c4 = {r["question_id"]: r for r in (rd(p) for p in glob.glob(F + "/checks/M%d-S*-T*-step4.json" % m))}
    slots = {s["slot_id"]: s for s in rd(F + "/plan.json")["slots"]}
    fails = {k: r for k, r in c3.items() if r["verdict"] != "pass"}
    # verdicts: Counter(r["verdict"] for r in c3.values())
    # findings per rule: Counter(f["rule"] for r in fails.values() for f in r["findings"])
    # step 4 after a step 3 fail: [k for k in fails if k in c4]
    # fingerprint check: [k for k, r in c3.items() if r["fingerprint"] != fingerprint(qs[k])]
    # re-run of today's code: [k for k, r in c3.items() if s3.check(qs[k], slots[qs[k]["slot_id"]])["verdict"] != r["verdict"]]
    # A12 field: Counter((s["select"], s.get("longest_may_be_correct")) for s in slots.values())
```

A second script (`longest.py`, same scratchpad) reads `mocks/mock-0N.questions.json` and `.answers.json` (the built mocks) and counts, for each mock, the questions where a correct option is the longest by characters or ties with the longest (the A12 test `max(right) >= max(wrong)`).

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Total | File and method |
|---|---|---|---|---|---|---|---|
| Tries (question files) | 83 | 92 | 101 | 111 | 101 | 488 | count `runs/mock-0N/questions/MN-S*-T*.json` |
| Step 3 records | 83 | 92 | 101 | 111 | 101 | 488 | count `checks/*-step3.json` |
| Verdict `pass` | 83 | 91 | 99 | 107 | 97 | 477 | field `verdict` |
| Verdict `fail` | 0 | 1 | 2 | 4 | 4 | 11 | same |
| Findings A12 | 0 | 1 | 2 | 3 | 1 | 7 | field `rule` of each finding of a failed record |
| Findings A1 | 0 | 0 | 0 | 1 | 1 | 2 | same |
| Findings A2 | 0 | 0 | 0 | 1 | 1 | 2 | same |
| Findings A9 | 0 | 0 | 0 | 0 | 2 | 2 | same |
| Findings A3 to A8, A10, A11 | 0 | 0 | 0 | 0 | 0 | 0 | same |
| Step 4 records | 83 | 91 | 99 | 107 | 97 | 477 | count `checks/*-step4.json`; equals the passes of step 3 |
| Step 4 record after a step 3 fail | 0 | 0 | 0 | 0 | 0 | 0 | question IDs in both sets |
| Fingerprint of the record differs from the question | 0 | 0 | 0 | 0 | 0 | 0 | `fingerprint(question)` from `src/control.py` |
| Verdict differs when today's code runs again on the try | 0 | 0 | 0 | 0 | 0 | 0 | `step3_check_code.check(question, slot)` |
| Slots with `longest_may_be_correct` true / false / no field | 0 / 0 / 60 | 16 / 44 / 0 | 16 / 44 / 0 | 16 / 44 / 0 | 16 / 44 / 0 | | `plan.json` (true = 13 one-answer + 3 two-answer) |
| Built mock, one-answer questions where a correct option is the longest or tied (A12 test) | 37 of 52 | 11 of 52 | 11 of 52 | 5 of 52 | 12 of 52 | | `longest.py` |
| Built mock, two-answer questions, the same | 6 of 8 | 2 of 8 | 3 of 8 | 1 of 8 | 3 of 8 | | `longest.py` |
| ... of them on a slot with `longest_may_be_correct: false` | (no field) | 0 | 0 | 0 | 0 | 0 | `longest.py` |

- 11 failed tries, 13 findings (M4-S27-T3 and M5-S60-T2 each have A1 and A2).
- Each of the 11 failed tries was repaired by the next try: the next try of the slot passed step 3 (11 of 11). Method: the step 3 verdict of try N+1 of the same slot (section 4.3).
- Over all 488 tries (method: `step3_check_code.words`, `sentences` on each try): question 44 to 103 words, options 12 to 35 words, largest A7 ratio 1.29 (limit 1.3), 3 to 6 sentences.
- Mock 1 for A12 by the strict test (correct option longer than each wrong option, no tie): 33 of 52 in the built mock, 31 of 52 in the 60 questions of marking round 1 (`runs/mock-01/marks/round-1.json`). By words with ties: 30 of 52 built, 29 of 52 round 1. See conflict C6.

### 4.3 Each failed try of step 3

| Try | Request | Rule | Letter | Detail (exact) | Next try | Date |
|---|---|---|---|---|---|---|
| M2-S02-T1 | 2 | A12 | A | "The longest option is a correct option (191 characters). The slot needs a wrong option that is longer than each correct option." | T2 passed 3 and 4 | 2026-10-08 |
| M3-S31-T1 | 2 | A12 | A | "... (136 characters) ..." | T2 passed 3 and 4 | 2026-10-08 |
| M3-S57-T1 | 2 | A12 | B | "... (167 characters) ..." | T2 passed 3 and 4 | 2026-10-08 |
| M4-S22-T1 | 2 | A12 | B | "... (158 characters) ..." | T2 passed 3 and 4 | 2026-10-09 |
| M4-S27-T3 | 5 | A1, A2 | none | "The options do not have the letters A to E in sequence." / "The question has 6 options. The slot needs 5." | T4 passed 3, failed 4 | 2026-10-09 |
| M4-S43-T2 | 5 | A12 | A | "... (159 characters) ..." | T3 passed 3 and 4 | 2026-10-09 |
| M4-S56-T1 | 2 | A12 | C | "... (185 characters) ..." | T2 passed 3, failed 4; T3 passed | 2026-10-09 |
| M5-S37-T1 | 2 | A12 | A | "... (169 characters) ..." | T2 passed 3, failed 4 | 2026-10-09 |
| M5-S43-T1 | 2 | A9 | none | "The question has 6 sentences. The limit is 2 to 5." | T2 passed 3 and 4 | 2026-10-09 |
| M5-S58-T1 | 2 | A9 | none | "The question has 6 sentences. The limit is 2 to 5." | T2 passed 3 and 4 | 2026-10-09 |
| M5-S60-T2 | 5 | A1, A2 | none | "The options do not have the letters A to E in sequence." / "The question has 6 options. The slot needs 5." | T3 passed 3, failed 4 | 2026-10-09 |

Source: `runs/mock-0N/checks/<try>-step3.json` and `-step4.json`, `runs/mock-0N/questions/<try>.json` (fields `request`, `date`). All L1.

### 4.4 Checks of the numbers in other files

- `academy/facts/top-of-tab-2.md`, run numbers: "Step 3 fails: 0, 1, 2, 4, 4 | 11". Agrees.
- `academy/facts/step-5.md`, 4.2: "Step 3 verdict `fail` | 0 | 1 | 2 | 4 | 4 | 11" and "Step 3 rules ... 2: A12 1; 3: A12 2; 4: A1 1, A2 1, A12 3; 5: A1 1, A2 1, A9 2, A12 1". Agrees.
- `docs/build-guide/step-3-check-by-code.md`, 16: "The plan lets the longest option be correct on 13 of the 52 slots with 1 answer and on 3 of the 8 slots with 2 answers ... In mock 1, before this rule, the correct option was the longest in 37 of 52 questions." Agrees with R12 and with the A12 test (longest or tied) on the built mock 1.
- `docs/decisions/0053-...`, 10: "37 of the 52 questions with 1 answer ... In the 8 questions with 2 answers, the longest option is correct in 6." Agrees (with ties counted, as A12 counts them).
- `docs/build-guide/step-3-check-by-code.md`, 24, the test run: "All 10 questions of the writer passed the 11 rules of that time". `runs/test-0024/part1.json`: 10 entries, each `step3.verdict` = "pass". Agrees.
- The 12 sample questions pass A4 to A11: test `test_the_12_sample_questions_pass_a4_to_a11` (`tests/test_step3_check_code.py`, 192-198) passes.

## 5. Stories for the Depth

### Story (a): the 6 options that the form could not stop (why A2 is code)

No decision, journal entry or review tells this as a story. The facts are in the run files and the decisions on the form. Search: "6 options", "six options", "M4-S27-T3", "M5-S60-T2" in `docs/` and `HANDOFF.md` (no match outside the owner's decision records below).

| # | Fact | Source | Exact quote | L |
|---|---|---|---|---|
| a1 | The design: the form cannot count, so step 3 counts. | `docs/decisions/0029-...`, Reason, 122 | "The point does not say if a schema can limit the number of items in a list, and the assistant did not check that in the Anthropic documentation. So the design does not rely on the form for a count." | 2 |
| a2 | The docs: array limits beyond `minItems` 0 or 1 are not supported. | W8 | "Array constraints beyond `minItems` of 0 or 1" | Docs |
| a3 | The instruction to the writer. | `src/step2_write.py`, 136 | `"Write %d options. Mark exactly %d of them correct."` | 1 |
| a4 | M4-S27-T3 (a "Select 2." slot of 5 options, a retry of step 5): the writer gave 6 options, A to F. | `runs/mock-04/questions/M4-S27-T3.json` | 6 options; correct C and E. Option F: "Use Edit now to change score_credibility in both wrapper modules, with Read and Write as the fallback if Edit finds non-unique text." | 1 |
| a5 | Step 3 found it. | `runs/mock-04/checks/M4-S27-T3-step3.json` | "The question has 6 options. The slot needs 5." | 1 |
| a6 | The owner's record names it. | `runs/mock-04/owner-decisions.json`, D005 (M4-S27, `more_tries`, after try 3) | "The last try failed on the form (rules A1 and A2), not on B9." | 1 |
| a7 | M5-S60-T2: the same, 6 options for a slot of 5. | `runs/mock-05/questions/M5-S60-T2.json`; `runs/mock-05/checks/M5-S60-T2-step3.json` | "The question has 6 options. The slot needs 5." | 1 |
| a8 | The owner's record. | `runs/mock-05/owner-decisions.json`, D006 (M5-S60, `new_point` 2.2-S1) | "B9 failed twice on the problem of M3-S24 and M2-S07, and once the form failed." | 1 |
| a9 | Both 6-option tries were requests of step 5 (retries), not first tries. | field `request` = 5, `shown_try` M4-S27-T2 / M5-S60-T1 | `"request": 5` | 1 |
| a10 | The A1 finding on these tries is a side effect: code compares the letters with "ABCDE" cut to the number of options, so 6 letters never match. The finding text says "A to E" for a question with A to F. | `src/step3_check_code.py`, 71-73; `src/step2_write.py`, 200 (`for letter, o in zip("ABCDEFGHIJ", options)`) | `if letters != list("ABCDE"[:len(options)]):` | 1 |
| a11 | Without step 3, a 6-option question would have gone to step 4 (a model call). Step 4 runs only after a pass of step 3 (E8). | `src/control.py`, 206-213 | | 1 |

Time order (`git log --date=iso`): decision 0029 and the build of step 3 are before mock 1 (`fa7e9cd`, 2026-10-07 12:22). M4-S27-T3 is in commit `e378e37` "Mock 4: run 1" (2026-10-09 12:16) or a later run commit of mock 4; M5-S60-T2 was added in `7819677` / `18fc105` (9 October 2026). The exact commit of each try file was not separated (see Not found 5).

### Story (b): rule A12, the longest option (decision 0053)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| b1 | Found by the second review of mock 1 (a Claude model in Cowork, not a person). | `docs/reviews/M1-round1-second-review-notes.md`, 58-60 | "In the 52 questions with one answer, the correct option is the longest by characters in 31. Chance is 13. Each question passes rule A7 (largest ratio 1.27), so that rule does not catch the pattern. A participant who always selects the longest option gets about 60%." | 4 |
| b2 | The assistant checked the cause against the plan and the code. | `docs/journal.md`, 144 (section "8 October 2026") | "no rule on the longest option in the set (29 of 52 by words, 34 of 52 by characters, chance about 13)" | 4 |
| b3 | Decision 0046 lists it as a cause to fix before mock 2. | `docs/decisions/0046-...`, 37 | "5. No rule looks at the longest option in the set of 60." | 2 |
| b4 | The question of decision 0053. | `docs/decisions/0053-...`, Question, 10 | "In the built mock 1, the correct option is the longest option (by characters) in 37 of the 52 questions with 1 answer. Chance is 13. In the 8 questions with 2 answers, the longest option is correct in 6. Chance is about 3. Rule A7 looks at one question only, and each question passed it. How does the program prevent this pattern?" | 2 |
| b5 | The rejected option. | `docs/decisions/0053-...`, Options, 15 | "2. A rule that the correct option is never the longest. Then a participant learns that the longest option is always wrong." | 2 |
| b6 | The decision: a field of the slot (step 1), an instruction to the writer (step 2), a rule in code (step 3). | `docs/decisions/0053-...`, Decision, 21-24 | "1. **Step 1.** Each slot gets the field `longest_may_be_correct` ... 13 of the 52 slots with 1 answer, and for 3 of the 8 slots with 2 answers. These are the chance numbers: 1 in 4, and 2 in 5." / "3. **Step 3.** Code checks rule A12. ... An equal length fails too." / "4. A slot with no field (the plan of mock 1) does not get rule A12. Mock 1 does not change." | 2 |
| b7 | The plain reason and the cost. | `docs/decisions/0053-...`, Reason, 29, 31 | "a participant who always selects the longest option must not gain from it." / "The cost: some questions need one more try." | 2 |
| b8 | How we decided. | `docs/decisions/0053-...`, 39, 41 | "The assistant counted the longest options in the built mock 1 and suggested the field, the instruction and the rule. The owner said yes." / "No independent reviewer checked this file." | 2 |
| b9 | The code. | `src/step3_check_code.py`, 151-160 | `if right and wrong and max(right) >= max(wrong):` | 1 |
| b10 | The tests: a tie fails, two correct options, a plan before 0053 passes. | `tests/test_step3_check_code.py`, 93-124 | `def test_a12_a_tie_fails(self):` / `def test_a12_with_two_correct_options(self):` / `self.assertEqual(check(GOOD, SLOT)["verdict"], "pass")   # a plan before decision 0053` | 1 |
| b11 | The result in the runs: A12 failed 7 tries in mocks 2 to 5, each repaired by the next try. In the built mocks 2 to 5, no question on a slot with `false` has a correct option as the longest. One-answer questions with the correct option longest: 11, 11, 5, 12 of 52 (chance 13). | section 4.2, 4.3 | | 1 (computed) |
| b12 | A real repair: M2-S02-T1 failed (correct option A 191 characters, longest wrong 183). In M2-S02-T2 the correct option has 167 characters, and the longest wrong option 183. T2 is in the built mock 2. | `runs/mock-02/questions/M2-S02-T1.json`, `-T2.json`; `mocks/mock-02.questions.json`, 43 | T1 A (correct): "Have the MCP search tool return isError true with a transient errorCategory and isRetryable true on timeouts, and return a successful empty result only when the query ran and matched nothing." T2 C (correct): "Have the MCP search tool flag timeouts with isError and a retryable transient category, and return a normal empty result only for queries that ran and matched nothing." | 1 |

Time order (`git log --date=iso`): mock 1 built `26477e1` 2026-10-08 11:06; decision 0046 `c5ec7dd` 11:04; decision 0053 and the code `288ad2c` 15:00; owner confirmed `066490d` 15:14; plan of mock 2 with the field `793d277` 16:20; mock 2 run 1 `d3a8cef` 16:56 (the first A12 fail, M2-S02-T1, is dated 2026-10-08).

### Story (c): rule A11 had three texts, and words like "cannot"

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| c1 | Origin: the owner's question on how the properties of the sample questions stay. That gave A8 to A11. | `docs/decisions/0037-...`, How we decided, 82 | "For item 12, the owner asked how the properties of the sample questions stay in the new questions. That question gave rules A8 to A11." | 2 |
| c2 | The first text of A11 in decision 0037. | `docs/decisions/0037-...`, 39 | "A11: the question has no \"NOT\" and no \"EXCEPT\"." | 2 |
| c3 | The assistant then wrote a more exact method in decision 0031, and did not make 0030 and 0037 agree. | `docs/journal.md`, 252, 254 (section "6 October 2026, third session") | "rule A11 got an exact method in decision 0031" / "One of the new serious items is an error of the assistant: it wrote a more exact method for rule A11 in decision 0031, and did not make decisions 0030 and 0037 agree." | 4 |
| c4 | The second review found three texts (serious). | `docs/reviews/review-decisions-0024-to-0037.md`, 131 | "**(i) Rule A11. Serious.** 0037 and 0030: no \"NOT\" and no \"EXCEPT\". 0031: capital letters in the text, and \"not\" or \"except\" in the last sentence. The script: capital or small letters, in the complete question text. No file says if the options count." | 4 |
| c5 | Reviewer A also found A11 weaker than the measurement. | same file, 35 | "The limit of A11 is weaker than the measured property. ... The limit of 0031 permits \"not\" in small letters outside the last sentence." | 4 |
| c6 | It was item 1 of the 10 new serious items. The owner agreed to it first. Then the owner stopped the cycle (decision 0038). | `docs/journal.md`, 220-221 (section "7 October 2026") | "The owner agreed to item 1 (rule A11) and saw a suggestion for item 2." / "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." | 4 |
| c7 | The fix: one text, in decision 0038, part 8. | `docs/decisions/0038-...`, Decision, 28 and 35 | "8. **Rule A11.** The question text does not have \"NOT\" or \"EXCEPT\" in capital letters. The last sentence of the question text does not have \"not\" or \"except\" in small letters. The options do not count." / "1. Rule A11 \| Closed by part 8" | 2 |
| c8 | Decisions 0030 and 0031 now carry the same text. | `docs/decisions/0030-...`, 37; `docs/decisions/0031-...`, 51 | "The options do not count (decision 0038, part 8)." | 2 |
| c9 | The lesson in `HANDOFF.md`. | `HANDOFF.md`, 152 | "When you make one file more exact, make each file that has the same rule agree. Rule A11 is the example." | 4 |
| c10 | The code follows part 8. | `src/step3_check_code.py`, 142-150 | `# Decision 0038, part 8. The options do not count.` | 1 |
| c11 | The open item "words like cannot", first text (when the code was built). | `git show fa7e9cd:HANDOFF.md`, 162 (2026-10-07 12:22) | "Step 3 follows the text of decision 0038, part 8: \"not\" or \"except\" in small letters, or \"NOT\" or \"EXCEPT\" in capital letters. So \"cannot\", \"doesn't\", and \"Not\" or \"Except\" at the start of the last sentence pass. Also, an abbreviation with a dot can hide the last sentence. A change needs a new decision." | 4 |
| c12 | The open item today (shortened in commit `edcd332`, 2026-10-09 22:43). | `HANDOFF.md`, 163 | "Rule A11 and words like \"cannot\" \| Step 3 follows decision 0038, part 8. A change needs a new decision." | 4 |
| c13 | The journal records it as open. | `docs/journal.md`, 208 (section "7 October 2026, second session") | "Rule A11 passes \"cannot\" and \"doesn't\" (see `HANDOFF.md`)." | 4 |
| c14 | Check by this agent with today's code (no model call): last sentences "Which change cannot help the team?", "Which change doesn't help the team?" and "Not every change helps; which one is best?" pass A11. "Which change does not help the team?" and "Which change is NOT useful here?" fail. "Which change does not help, e.g. for the team?" passes, because "e.g." splits the sentence and the last sentence becomes "for the team?". | `step3_check_code.check(..., rules={"A11"})`, run 14 October 2026 | output: `pass`, `pass`, `pass`, `fail`, `fail`, `pass` | 1 (computed) |
| c15 | The gap never happened in the runs: no try of 488 has "not", "cannot", "n't" or "except" (any case) in the last sentence of its question text. In the built mocks, 7 to 13 question texts per mock have such a word, but none in the last sentence. | script over `runs/mock-0N/questions/*.json` and `mocks/*.questions.json`, last sentence by `step3_check_code.sentences` | 0 of 488 | 1 (computed) |
| c16 | No new decision changed A11 after decision 0038 (status lines of 0030 and 0031 name no later A11 change; `git log -S"A11" -- src/step3_check_code.py` shows only `fa7e9cd`). | | | 1 / 2 |

Time order: decisions 0030, 0031, 0037 and 0038 are dated 6 and 7 October 2026 and are in the first commit `8cc3a24` (2026-10-07 09:41). The order inside that time comes from the dates in the files and the journal: 0037 (6 October, third session) -> 0031 changed with an exact A11 (same session) -> review (6 October, third session) -> 0038 (7 October, after midnight) -> code `fa7e9cd` (7 October 12:22).

### Story (d): the false fail of A9 ("9 a.m.")

No decision, journal entry or review mentions it. Search: "a.m.", "M5-S43", "abbreviation" in `docs/` and `HANDOFF.md` (only the known limit in decision 0031 and the old `HANDOFF.md` text). The facts are in the run files.

| # | Fact | Source | Exact quote | L |
|---|---|---|---|---|
| d1 | The known limit was written before the run. | `docs/decisions/0031-...`, 53; `git show fa7e9cd:HANDOFF.md`, 162 | "It can count wrong when a text has an abbreviation with a dot." / "an abbreviation with a dot can hide the last sentence." | 2 / 4 |
| d2 | M5-S43-T1 failed A9 with 6 sentences. | `runs/mock-05/checks/M5-S43-T1-step3.json` | "The question has 6 sentences. The limit is 2 to 5." | 1 |
| d3 | The question has 5 sentences. Code split "well before the 9 a.m. team review." into two, because "a.m." is followed by a space. | `runs/mock-05/questions/M5-S43-T1.json`; `step3_check_code.sentences` (run 14 October 2026) | sentence 2: "A scheduled job submits the batch at 1 a.m., and the generated tests usually return within an hour, well before the 9 a.m." / sentence 3: "team review." | 1 (computed) |
| d4 | The writer's next try avoided the abbreviation and passed steps 3 and 4. It is in the built mock 5. | `runs/mock-05/questions/M5-S43-T2.json`; `mocks/mock-05.questions.json`, 1229 | "A scheduled job submits the batch at 01:00, and the generated tests usually return within an hour, well before the 09:00 team review. Last night the batch finished at 15:00, so the team missed the review, and a developer opened a bug ticket against the batch job." | 1 |
| d5 | The other A9 fail was true: M5-S58-T1 has 6 real sentences. The next try joined two sentences and passed. | `runs/mock-05/questions/M5-S58-T1.json`, `-T2.json` | T2: "A customer asks for a refund, and Claude requests lookup_order, which the loop code runs correctly and saves to an audit log for the support team." | 1 |
| d6 | Cost: one more writer call for M5-S43. No model call of step 4 for T1 (E8). | section 4.3 | | 1 |

### Other Depth facts

- The longer history of "an error is not a pass" comes from the first build: `docs/lessons.md`, 41-42: "9. **Put a code check between steps. The code refuses an empty output, a missing verdict and a file that does not parse.**" / "One run had the status \"complete\" when its output file had 0 bytes (F1)." The file says of itself (line 3): "Private history of the first build. Not a source for the design." (L4)
- The test before mock 1: all 10 questions passed step 3 at the first try (`docs/journal.md`, 195: "the writer made 10 questions, and all 10 passed step 3 at the first try"; `runs/test-0024/part1.json`). (L4 / L1)
- Mock 1: 0 fails of step 3 in 83 tries (section 4.2). The rule that mock 1 needed (A12) came only after mock 1 was built. (L1)
- No story found for rules A3 to A8, A10 and A11 in the runs: they never failed (section 4.2).

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step3_check_code.py` | 1-9 | The docstring: code checks A1 to A12, no model works in this step. |
| `src/step3_check_code.py` | 12-22 | The limits of A6, A7, A9 (from decision 0031) and the A5 word list. |
| `src/step3_check_code.py` | 29-32 | The sentence method and its known limit. |
| `src/step3_check_code.py` | 35-37 | One finding: six fields, the same form as step 4. |
| `src/step3_check_code.py` | 94-99 | A2 and A3: code counts against the slot. |
| `src/step3_check_code.py` | 125-131 | A7: the ratio of average words. |
| `src/step3_check_code.py` | 142-150 | A11 as decision 0038, part 8. |
| `src/step3_check_code.py` | 151-160 | A12, decision 0053: `max(right) >= max(wrong)`. |
| `src/step3_check_code.py` | 71-73 | The A1 letter check (story a, a10). |
| `src/control.py` | 206-213 | Step 4 runs only after a pass of step 3; a slot passes only with both. |
| `src/control.py` | 365-370 | The control calls step 3 and saves the verdict. |
| `src/control.py` | 394-401 | The verdict record, with the fingerprint, as a new file. |
| `src/control.py` | 743-746 | Before step 8: each question needs a valid pass of step 3. |
| `src/steps.py` | 69-71 | Step 3 is a plain function call (no model, no retry). |
| `src/step1_plan.py` | 46-48, 446-453 | The slot field `longest_may_be_correct` (13 and 3). |
| `src/step2_write.py` | 136 | "Write %d options." The count is only an instruction. |
| `docs/diagrams/04-form-schema-draft.json` | 15-29 | The `options` array of the writer's schema: no count. |
| `tests/test_step3_check_code.py` | 93-124 | The three A12 tests. |
| `tests/test_step3_check_code.py` | 140-149 | A11: capital NOT fails, small "not" in the last sentence fails, outside it passes. |
| `tests/test_step3_check_code.py` | 192-198 | The 12 sample questions of the guide pass A4 to A11. |
| `runs/mock-04/checks/M4-S27-T3-step3.json` | all | A real fail: 6 options (A1, A2). |
| `runs/mock-02/checks/M2-S02-T1-step3.json` | all | A real fail of A12. |
| `runs/mock-05/checks/M5-S43-T1-step3.json` | all | The false fail of A9 ("9 a.m."). |
| `git show 288ad2c -- src/step3_check_code.py` | | The diff that added A12. |

## 7. A figure: the mechanism

One figure could show the gate between the writer and the model check:

```
[Writer, Claude] --writes a try--> [Step 3: code checks A1-A12]
     ^                                   |                 \
     |                                 pass               fail (rule + detail)
     |                                   v                   \
     |                         [Step 4: model checks B1-B9]   [verdict record, new file]
     +---- request of step 5: the failed try + findings <-----+
```

| Label | Fact behind it |
|---|---|
| "writes a try" | `src/control.py`, 356-363 (`self.steps.write(request)`) |
| "code checks A1-A12" | O1, section 2.2 |
| "pass" -> step 4 | E8, E9 |
| "fail (rule + detail)" | E7, F1; real details in 4.3 |
| "verdict record, new file" | E4, E5 |
| "the failed try + findings" | E10 |
| A side box "the form cannot count: 6 options" | story (a), W8-W10 |
| A number on the arrows | 477 pass, 11 fail of 488 (section 4.2) |

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| C1 | Point 4.4-K1 is in a popup of diagram 05 but not in the build guide table of step 3 (academy decision 0024). | `docs/diagrams/05-step-3-check-by-code.html`, 157, popup "finding" (from `docs/diagrams/05-make-diagram.py`, 119): `"points": [{"id": "4.4-K1", "text": "Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction"...` | `docs/build-guide/step-3-check-by-code.md`, 28-34: the table has 1.4-K1, 1.4-K2, 4.3-K3, 4.4-K4, 5.3-K4, and not 4.4-K1. (4.4-K1 is in the table of step 5.) |
| C2 | What happens when the question file is missing or cannot be read. | `docs/decisions/0031-...`, 28: "Then the step reports an error. It never returns \"pass\" for a question that it did not read." `docs/build-guide/step-3-check-by-code.md`, 20: "If code cannot read a question, it reports an error." Diagram 05, popup "err": "If the file of the question is missing or cannot be read, the step reports an error." | `src/control.py`, 296-297 and 365: the control reads the file with `json.load` before step 3, with no `try`. `src/run.py`, 106-112 catches only `Refused` and `RunStopped`. So the run stops with an uncaught Python error, and no error record is saved (F5). No test (F6). A record that is readable but not a question fails A1 (F3). No pass is possible in either case. |
| C3 | `HANDOFF.md` says decisions 0030 and 0031 do not have the new A11 text. They have it. | `HANDOFF.md`, 136: "Closed by decision 0038, part 8. Decisions 0030 and 0031 do not have the new text yet." | `docs/decisions/0030-...`, 37 and `docs/decisions/0031-...`, 51: both have "The options do not count (decision 0038, part 8)." Their status lines say "Changed: 7 October 2026, to describe the control of decisions 0038 and 0039". (`HANDOFF.md` line 136 is in the section "History".) |
| C4 | The A11 text that the writer gets differs from the code. | `src/step2_write.py`, 44: "The last sentence of the question text does not have \"not\" or \"except\"." (no "in small letters", no "The options do not count"). Line 25 says: "rule A11 of decision 0038, part 8". | `src/step3_check_code.py`, 148 (small letters only); `docs/decisions/0038-...`, 28: "does not have \"not\" or \"except\" in small letters. The options do not count." (Both L1. The writer's text is stricter in words.) |
| C5 | The example findings in the popups of diagram 05 do not have the words of the code. | `docs/diagrams/05-make-diagram.py`, 58, 62, 66, 74, 79, 84: "Option C has no reason.", "The question has 5 options. The slot says 4.", "2 options are marked correct. The slot says 1.", "The reason of option A has the words \"Option B\".", "The question has 140 words. The limit is 110.", "The correct option has 40 words. The wrong options have 18 words on average. The limit is 1.3 times." Decision 0031, 37, has the same A6 example. | `src/step3_check_code.py`: "Option C has no a reason." (line 68, with `missing.append("a reason")`, checked by a run on 14 October 2026), "The slot needs 4." (95), "The slot needs 1." (99), 'The reason of option A names a letter or an option: "Option B".' (116), "The limit is 25 to 110." (120), "The correct options are %.2f times as long as the wrong options. The limit is 1.3." (131). Also the popup "rec" example has no `fingerprint` field; the real records have it (E4). |
| C6 | Counts of "the correct option is the longest" in mock 1 differ by source. | `docs/reviews/M1-round1-second-review-notes.md`, 60: "by characters in 31". `docs/journal.md`, 144: "29 of 52 by words, 34 of 52 by characters". | `docs/decisions/0053-...`, 10, and `docs/build-guide/step-3-check-by-code.md`, 16: "37 of the 52". This agent's count (4.2): round 1 by characters 31 strict / 35 with ties; built mock 1 by characters 33 strict / 37 with ties; by words with ties 29 (round 1) / 30 (built). So 31 = round 1 strict, 37 = built with ties (the A12 test), 29 = round 1 by words with ties. The journal's "34 by characters" matches none of these methods. |
| C7 | Decision 0011 names a slot check that step 3 does not do. | `docs/decisions/0011-...`, 23: "The question agrees with its slot: the scenario, the task statement, the question type." (an example; line 37: "Not decided yet: the full list of rules") | `src/step3_check_code.py`: no rule compares the scenario or the task statement. A2 and A3 compare only the counts. Decision 0030 (later) gives the full list A1 to A11, and B4 and B5 (step 4) check the point and the scenario. A later decision wins (academy decision 0011). |
| C8 | The box of A11 in diagram 05 shows only half of the rule. | `docs/diagrams/05-step-3-check-by-code.html`, 144, box A11: "No \"NOT\" or \"EXCEPT\" in capital letters." | The popup of the same box (line 157) and the code (142-150) also check "not" or "except" in the last sentence. (Small; the box is a summary.) |

## 9. Not found

1. No decision, journal entry, lesson or review mentions the two 6-option tries (M4-S27-T3, M5-S60-T2) as a story, or why the writer wrote 6 options. Only the owner's reasons in `owner-decisions.json` name "the form (rules A1 and A2)".
2. No source mentions the false fail of A9 on M5-S43-T1 ("9 a.m."). Only the general known limit (decision 0031, 53) exists.
3. No run of a missing or unreadable question file, and no test of it (C2, F6). What the program prints in that case was not run by this agent.
4. No count of how often step 3 saved a model call. Only the number of tries that failed step 3 and so had no step 4 call: 11 (section 4.2). The cost of one step 4 call is not in the run files of step 3.
5. The commit that added each failed try file was not separated (several run commits of 9 October 2026). The dates in the records (field `date`) are days only.
6. No independent reviewer checked decisions 0011, 0031, 0038 or 0053 (each file says so: 0031, 80; 0038, 66; 0053, 41). Decision 0011 has no such line.
7. No source measures whether the A rules are the right rules (for example, a question that passed step 3 but the owner marked bad for an A-type reason). Not searched in the marking files (rule: do not open `marking/*.xlsx`).
8. A dated copy of the documentation page "Structured outputs" of 14 October 2026 in `academy/sources/` (academy decision 0030) was not saved: this agent may change no file except this fact sheet. The copy of 7 October 2026 is `docs/sources/2026-10-07-anthropic-docs-structured-outputs.md`, and its lines 2628 and 2637 agree with the live page.
9. `docs/lessons.md` has no entry on step 3, A11 or A12 of this build (search "A11", "A12", "longest", "step 3": no match). Its item 9 is on the first build.
