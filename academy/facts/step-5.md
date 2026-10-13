# Fact sheet: tab 2, step 5 "Try again"

- Fact agent: a new agent (academy decision 0012). Date: 13 October 2026.
- Repository state: commit `d884cb4` (branch `main`, clean).
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = Anthropic documentation (academy decision 0014).
- Line numbers are for the files at commit `d884cb4`. "L" = level of trust.
- The tests ran on 13 October 2026 without an API key: `python3 -m unittest discover -s tests` gives "Ran 228 tests ... OK". `tests/test_control.py` has 66 tests (count with `grep -c "def test" tests/test_control.py`).
- Files that this agent did not read (working rules 19 and 28): the marking files `marking/*.xlsx`, `responses.json`, and all personal files of the owner.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | A question that fails step 3 or step 4 goes back to the writer with the failed question and the findings. | `docs/build-guide/step-5-try-again.md`, 9 | "A question that fails step 3 or step 4 goes back to the writer. The writer gets the request of step 2, plus the failed question with the letters that the checker saw, and the exact findings." | 3 |
| O2 | The same, in the code: steps 2 and 5 are one writer call. Step 5 is the request of step 2 plus the failed question and its findings. | `src/step2_write.py`, 3-5 | "Step 5 writes a new try: it is the request of step 2, plus the failed question with its letters and its findings" | 1 |
| O3 | The new try goes through steps 3 and 4 again. | `docs/build-guide/step-5-try-again.md`, 9; `docs/decisions/0020-...`, 19 | "The new try goes through steps 3 and 4 again, as a new question." / "A question from step 5 goes through step 3 and step 4 again." | 3 / 2 |
| O4 | The owner can also send a question back: a bad mark or a rewrite. | `docs/build-guide/step-5-try-again.md`, 11 | "A question also comes back when the owner sends it back: a bad mark, or a \"rewrite\"." | 3 |
| O5 | It is the one automatic loop of the builder. Each other failure waits for the owner. | `docs/decisions/0038-...`, 21-22 | "1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5." / "2. **Each other failure waits for the owner.**" | 2 |
| O6 | The main way to stop is a question that passes. The limit is not the main way. | `docs/build-guide/step-5-try-again.md`, 13 | "The limit is not the main way to stop. The main way to stop is a question that passes." | 3 |
| O7 | Status of the step: built, ran in mocks 1 to 5, 7 to 9 October 2026. | `docs/build-guide/step-5-try-again.md`, 3 | "Status: built. It ran in mocks 1 to 5, from 7 to 9 October 2026." | 3 |
| O8 | The writer of step 5 is a model call. The model of every try in mocks 1 to 5 is `claude-opus-5-5`. | `src/model_call.py`, 22; run files | `MODEL = "claude-opus-5-5"`. Count: field `model` of each `runs/mock-0N/questions/*.json` is `claude-opus-5-5` in all 488 files. | 1 |

## 2. Explanation facts: the mechanism

### 2.1 What the writer gets on a retry

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | The request of step 5 is the request of step 2 plus two parts: the failed question and its findings. | `docs/decisions/0033-...`, 23 | "It is the request of step 2 (decision 0029), plus two parts: the failed question and the list of its findings." | 2 |
| E2 | The code text that the writer gets for a new try. | `src/step2_write.py`, 152-159 | "A NEW TRY. The question below did not pass. Write a new question for the same slot. Correct each finding. The letters are the letters that the checker saw." | 1 |
| E3 | The failed question is shown with its options, letters, marks and reasons (fields `question`, `select`, `options`, `cannot_write_reason`). | `src/step2_write.py`, 153-155; `src/step2_write.py`, 202 | `shown = {"question": ..., "select": ..., "options": failed.get("options"), "cannot_write_reason": ...}`. Each option keeps `letter`, `text`, `correct`, `reason`. | 1 |
| E4 | The writer sees the letters that the checker saw, so a finding that names a letter is clear. | `docs/decisions/0033-...`, 23 | "Code shows the failed question with the letters that the checker saw. So a finding that names a letter is clear (decision 0037, item 11)." | 2 |
| E5 | The findings of the failed try are the findings of its step 3 and step 4 records. | `src/control.py`, 288-294 | `for step in (3, 4): v = self.verdict(question["question_id"], step) ... findings.extend(v["findings"])` | 1 |
| E6 | One form for each finding: `step`, `rule`, `detail`, `letter`, `point`, `other_questions`. | `docs/decisions/0033-...`, 25-34; `docs/diagrams/07-make-diagram.py`, 61 | "Each finding has the same fields: step, rule, detail, letter, point and other_questions." | 2 / 3 |
| E7 | The writer also gets all other parts of the request of step 2: the rules, 3 sample questions, the story, the task statement with the point marked, the technologies, the slot and the form. | `src/step2_write.py`, 122-136; `docs/diagrams/07-make-diagram.py`, 52 | "All parts of the request of step 2: the rules, the 3 sample questions, the story, the task statement, the 14 technologies, the slot and the form." | 1 / 3 |
| E8 | The writer also gets the earlier questions of the built mocks on the same idea (rule B9), on step 2 and on step 5. | `src/steps.py`, 52-67; `src/step2_write.py`, 137-139 | `# steps 2 and 5` ... `self.writer.earlier = self._earlier()`; `if request.get("earlier_questions"):` | 1 |
| E9 | After a rewrite of a step 6 finding, the writer also gets the text of the other questions that the finding names. | `src/step2_write.py`, 160-164; `src/control.py`, 249-269 | "The other questions that a finding names. Do not write the same scene:" | 1 |
| E10 | After a bad mark, the finding is the reason of the owner (`step` 7, `rule` "owner"). | `src/control.py`, 244-248 | `finding = {"step": 7, "rule": "owner", "detail": event["mark"]["reason"], ...}` | 1 |
| E11 | After `more_tries`, since decision 0074, the writer also gets the reason of the owner as a finding with the rule "owner". | `src/control.py`, 270-281 | "# more_tries: the last try before the decision. Since decision 0074 the # writer also gets the reason of the owner, as an instruction." | 1 |
| E12 | The answer of the writer has the same fixed form as in step 2, sent as structured outputs (JSON schema in `output_config.format`). | `docs/decisions/0040-...`, 20; `src/model_call.py`, 119 | "Steps 2, 4 and 6 (and step 5, which uses the request of step 2) send their form as a JSON schema in `output_config.format`." | 2 / 1 |
| E13 | Code mixes the options of the new try and gives the letters. The model does not select them. | `src/step2_write.py`, 183-202 | "Decision 0029, part 4.1: code mixes the options and gives the letters. The model does not select them." | 1 |
| E14 | From mock 5, the plan sets the letters of the correct options (decision 0070), also for step 5. | `src/step2_write.py`, 191-199; `docs/decisions/0070-...`, 22 | "**Step 2** (and step 5) puts the correct options at the letters of the slot." | 1 / 2 |

### 2.2 What the writer does not get

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| N1 | The writer sees only the last failed try, not the older tries. The request stays short. | `docs/decisions/0033-...`, 37; `docs/build-guide/step-5-try-again.md`, 9 | "Only the last failed try and its findings. It does not see the tries before that." / "The writer does not see older tries, so the request stays short." | 2 / 3 |
| N2 | Code: the request shows only `in_round[-1]`, the current failed try. | `src/control.py`, 236-239 | `failed = in_round[-1]` / `return self._step5(request, failed, self._check_findings(failed))` | 1 |
| N3 | The reason for "only the last failed try": guide point 4.4-S1 names three parts, not the history. | `docs/decisions/0033-...`, 113 | "The guide names three parts for a new try: the original, the failed result and the errors (4.4-S1). It does not name the complete history." | 2 |
| N4 | The reason of the owner (after `more_tries`, a bad mark or a rewrite) reaches only the first try of the new start. On a later try of the same start, the request has only the findings of steps 3 and 4 of the last try. | `src/control.py`, 236-239 (the branch for a failed try of the start runs before the branch for the owner's event, 240-281) | `if in_round:` ... `return self._step5(request, failed, self._check_findings(failed))` | 1 |
| N5 | Replay of N4 on a copy of `runs/mock-05/` (no model call, current code): the request of M5-S38-T4 has the findings `B9` and `owner`. The request of M5-S38-T5 has only `B9`. | method in section 4.6 | output: "status to_write step 5 shown M5-S38-T3 findings rules ['B9', 'owner']" and "status to_write step 5 shown M5-S38-T4 findings rules ['B9']" | 1 (computed) |
| N6 | The checker of step 4 does not see earlier findings. A new try is checked as a new question. | `src/step4_check_model.py`, 194 (`def check(self, question, slot):` gets no findings); `docs/decisions/0032-...`, 59 | "A question from step 5 is checked as a new question. The two calls do not see the earlier findings. This closes the open item of decision 0020." | 1 / 2 |
| N7 | The reason for N6 is an assumption, not checked. | `docs/decisions/0032-...`, 168 | "Plain reason: a checker that sees the earlier findings can look only for those findings. This is an assumption of the assistant. It is not checked." | 2 |
| N8 | After `new_point`, the writer gets a request of step 2 with no failed try, because the old tries tested a different point. | `src/control.py`, 242-243; `docs/decisions/0039-...`, 46, 128 | "Step 2 after `new_point`. Plain reason: the old tries tested a different point." | 1 / 2 |
| N9 | A rewrite with a new point is a request of step 2 on the new point, with the other questions not to repeat (decision 0045). | `src/control.py`, 261-266; `docs/decisions/0045-...`, 23 | "# Decision 0045: a rewrite with a new point is a request of step 2 on # the new point." | 1 / 2 |
| N10 | After `more_tries` on a `cannot_write` slot, the writer gets a request of step 2, because no question exists to show. | `src/control.py`, 278-280; `docs/diagrams/07-make-diagram.py`, 105 | "After cannot_write, the writer gets a request of step 2, because no question exists to show." | 1 / 3 |

### 2.3 Limits, what stops a slot, who decides

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| L1 | The limit of tries is 3, and the code calls it a guess. | `src/control.py`, 31 | `TRIES = 3              # tries for one slot (decision 0033). A guess.` | 1 |
| L2 | Two "cannot decide" results stop a slot. | `src/control.py`, 32 | `CANNOT_DECIDE = 2      # "cannot decide" results that stop a slot (decision 0023)` | 1 |
| L3 | A pass stops the loop first: the code checks for a pass before it checks the limits. | `src/control.py`, 211-224 | `if v3["verdict"] == "pass" and v4["verdict"] == "pass": state["status"] = "passed"; return state` then "# The current try failed. Check the two limits (decision 0037, item 6)." | 1 |
| L4 | The limits count only the tries of the current start (`in_round`: tries after the last send-back event). | `src/control.py`, 192-194, 215-224 | `start = events[-1]["after_try"] if events else 0` / `in_round = [t for t in tries if t["try"] > start]` / `if len(in_round) >= TRIES:` | 1 |
| L5 | Both reasons can apply at once. The field `open_reasons` lists each one. | `src/control.py`, 220-224; `tests/test_control.py`, 84-94 | `self.assertEqual(s["open_reasons"], ["three_tries", "cannot_decide_twice"])` | 1 |
| L6 | The two "cannot decide" results need not be one after the other. The rule that applies first stops the slot. | `docs/decisions/0033-...`, 40 | "The two results do not have to come one after the other. The rule that applies first stops the slot (decision 0037, item 6)." | 2 |
| L7 | The answer `cannot_write` makes the slot open at once. | `src/control.py`, 202-205; `docs/decisions/0033-...`, 24 | "It can also answer `cannot_write`. Then the slot gets the status `open` immediately" | 1 / 2 |
| L8 | Each start of a slot has at most 3 tries. A start is the first question, `more_tries`, `new_point`, a bad mark or a rewrite. The count of "cannot decide" starts at zero. The try numbers continue. | `src/control.py`, 158-174; `docs/decisions/0033-...`, 40-41; `tests/test_control.py`, 655-665 | "Each event that gives the slot a new start: 3 new tries, and the count of \"cannot decide\" at zero" | 1 / 2 |
| L9 | An open slot waits for the owner. The other slots continue. | `docs/decisions/0033-...`, 42 | "The mock is not complete, and the other slots continue." | 2 |
| L10 | The owner decides on an open slot with one command: `new_point`, `more_tries` or `new_plan`. | `docs/build-guide/step-5-try-again.md`, 13; `src/run.py`, 8 | "A slot that stops is open, and the owner decides: more tries, a new point, or a new plan." / `python3 src/run.py decide --mock 1 more_tries M1-S05 --reason "..."` | 3 / 1 |
| L11 | Code refuses `more_tries` or `new_point` for a slot that is not open. | `src/control.py`, 633-638 | `raise Refused("The slot %s is not open." % target)` | 1 |
| L12 | `new_point`: code checks that the point is in the task statement of the slot, that no other slot uses it, and that the slot did not have it before. | `src/control.py`, 698-711; `docs/build-guide/step-5-try-again.md`, 11 | "Code then checks that the point is in that task statement, that no other slot uses it, and that the slot did not have it before." | 1 / 3 |
| L13 | `new_plan` stops the mock. How the new plan starts is not built. | `docs/decisions/0033-...`, 61; `docs/diagrams/07-make-diagram.py`, 107 | "How the new plan starts is not built yet." | 2 / 3 |
| L14 | A call that fails 3 times is not a try. Code saves an error record. | `src/control.py`, 30, 309-322; `docs/decisions/0033-...`, 107 | `CALL_RUNS = 3          # runs of a call that fails (decision 0037, item 10). A guess.` / "These are not tries of the slot." | 1 / 2 |
| L15 | The number 3 has no source in the guide. | `docs/decisions/0033-...`, 114 | "The guide gives no number. The number 3 is a guess of the assistant. It has no source." | 2 |
| L16 | The reason for a limit at all. | `docs/decisions/0033-...`, 114 | "with no limit, a slot that cannot pass makes the program try with no end." | 2 |
| L17 | The reason why two "cannot decide" go to the owner. | `docs/decisions/0023-...`, 133; `docs/diagrams/07-make-diagram.py`, 87 | "If the checker cannot decide two times, a participant probably cannot decide either. The owner looks at it." | 2 / 3 |
| L18 | In mocks 4 and 5, most open slots came from the stricter rule B9. | `docs/build-guide/step-5-try-again.md`, 13 | "In mocks 4 and 5, most open slots came from the stricter rule B9, and the owner gave new points or added the idea to the narrow list (decisions 0068 and 0075)." The run files agree (section 4.4). | 3 |

### 2.4 Each try is a new file

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| F1 | Each try is a new file. No file is written over. | `docs/build-guide/step-5-try-again.md`, 15 | "Each try is a new file. No file is written over, so the history of each question stays." | 3 |
| F2 | The code refuses to write over a record. | `src/control.py`, 94-99 | `"""Write a record. A record is never written over."""` ... `raise RuntimeError("The record exists already: " + path)` | 1 |
| F3 | A test checks F2. | `tests/test_control.py`, 74-77 | `def test_a_record_is_never_written_over(self):` | 1 |
| F4 | The new record gets the next try number, the request number (2 or 5) and the try that the writer saw (`shown_try`). | `src/control.py`, 378-392 | `qid = "%s-T%d" % (slot["slot_id"], n)` ... `"request": request["step"], "shown_try": request["shown_try"]` | 1 |
| F5 | Example of a real record: `runs/mock-01/questions/M1-S05-T2.json` has `"try": 2`, `"request": 5`, `"shown_try": "M1-S05-T1"`. | `runs/mock-01/questions/M1-S05-T2.json`, 4, 7, 8 | `"request": 5,` `"shown_try": "M1-S05-T1",` | 1 |
| F6 | The status of a slot is calculated from the records each time. No file stores it. | `src/control.py`, 21-22 | "The control calculates the status of each slot and the state of the mock from the records each time. No file stores them" | 1 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-5-try-again.md`, lines 35-44 (L3). The texts agree with `reference/guide-records.json` (checked by script on 13 October 2026).

| Point | Line | Task statement | How the step uses it (exact, from the table) |
|---|---|---|---|
| 4.4-K1 | 39 | 4.4: Implement validation, retry, and feedback loops for extraction quality | "Written for the extraction of data. Here: the findings of the checks go back to the writer with the failed question." |
| 4.4-S1 | 40 | 4.4 | "The same context. Here: the \"document\" is the request of step 2, the \"failed extraction\" is the failed question, and the \"validation errors\" are the findings." |
| 4.4-K2 | 41 | 4.4 | "The same context. Here: the writer can answer \"cannot write\" for a slot that does not fit its scenario. The design expects that such a slot does not improve with a new try. That is an assumption, not checked." |
| 1.1-S3 | 42 | 1.1: Design and implement agentic loops for autonomous task execution | "Written for agent loops. Here: the limit of 3 tries is a guard, not the main way to stop. The main way to stop is a question that passes." |
| 4.3-K1 | 43 | 4.3: Enforce structured output using tool use and JSON schemas | "Written for the extraction of data. The new try answers in the same fixed form as step 2, sent as structured outputs (see the deviation above)." |
| 4.3-S3 | 44 | 4.3 | "Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above)." |

Guide texts (from `reference/guide-records.json`):
- 4.4-K1: "Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction"
- 4.4-S1: "Implementing follow-up requests that include the original document, the failed extraction, and specific validation errors for model self-correction"
- 4.4-K2: "The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)"
- 1.1-S3: "Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator"
- 4.3-K1: "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors"
- 4.3-S3: "Forcing a specific tool with tool_choice: {\"type\": \"tool\", \"name\": \"extract_metadata\"} to ensure a particular extraction runs before enrichment steps"

Points in the popups of diagram 07 (`docs/diagrams/07-step-5-try-again.html`, line 279, JSON `stepdata`): `failed` 4.4-S1, `findings` 4.4-K1, `open` 1.1-S3 and 4.4-K2. All four are in the table. The table also has 4.3-K1 and 4.3-S3, which diagram 07 does not cite (not a conflict under academy decision 0024).

Facts that support the uses:
- T1 (4.4-K2, "not checked"): in mocks 1 to 5, no try has the status `cannot_write` (all 488 question records have `"status": "written"`, section 4.1). So the case that 4.4-K2 supports never happened in a run. (L1)
- T2 (1.1-S3): all 17 open-slot events of mocks 1 to 5 came from `three_tries`. No slot stopped on `cannot_decide_twice`, and step 4 never gave the verdict `cannot_decide` (section 4.4). (L1)
- T3 (4.3-S3, the deviation): the build guide says the newest models reject a forced tool call (`docs/build-guide/step-5-try-again.md`, 27-31). Docs check: page "Define tools", https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, section "Controlling Claude's output" > "Forcing tool use", read live on 13 October 2026. The table row "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says "`any` and `tool` return a 400 error" and names as the replacement "`auto` with strict tool use to guarantee schema-valid tool inputs, or structured outputs when you need a response in a fixed JSON shape". This agrees with the saved copy `docs/sources/2026-10-07-anthropic-docs-define-tools.md`, line 564. (Docs)
- T4: the reasons of decision 0033 (lines 111, 115, 119) quote 4.4-K1, 4.4-S1, 1.1-S3 and 4.4-K2. Decision 0013 (line 26) also names 4.4-S2 (see conflict C1).

## 4. Numbers, per mock, with method

### 4.1 Method

The script below reads only the run files. It makes no model call. Run: `python3 -I count5.py ~/ccar-f-mock-generator`. It ran on 13 October 2026 (a copy was in the scratchpad of this agent, not in the repository).

```python
import glob, json, os, sys
from collections import Counter
ROOT = sys.argv[1]
def rd(p):
    with open(p, encoding="utf-8") as f: return json.load(f)
for m in range(1, 6):
    F = os.path.join(ROOT, "runs", "mock-%02d" % m)
    qs = [rd(p) for p in sorted(glob.glob(F + "/questions/M%d-S*-T*.json" % m))]
    per = Counter(q["slot_id"] for q in qs)                                  # tries per slot
    chk = {}
    for p in glob.glob(F + "/checks/M%d-S*-T*-step[34].json" % m):
        r = rd(p); chk[(r["question_id"], r["step"])] = r
    failed = lambda q: any(chk.get((q["question_id"], s), {}).get("verdict") not in (None, "pass") for s in (3, 4))
    more = {s for s, v in per.items() if v > 1}
    failed_slots = {q["slot_id"] for q in qs if failed(q)}
    decs = rd(F + "/owner-decisions.json")
    # tries: len(qs); slots: len(per); more than one try: len(more)
    # after a failed check: len(more & failed_slots); only after a send-back of the owner: len(more - failed_slots)
    # request of step 2 or 5: Counter(q["request"] for q in qs); failed tries: sum(failed(q) for q in qs)
    # step 4 finding rules: Counter(f["rule"] for (q, s), r in chk.items() if s == 4 and r["verdict"] != "pass" for f in r["findings"])
    # open-slot events: decisions with action more_tries or new_point (each one needs an open slot, src/control.py 633-638)
```

The reasons of each open-slot event were rebuilt from the tries of the start that ended at `after_try` (the same rule as `src/control.py` 215-224).

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Total | File and method |
|---|---|---|---|---|---|---|---|
| Tries (question files) | 83 | 92 | 101 | 111 | 101 | 488 | count `runs/mock-0N/questions/MN-S*-T*.json` |
| Slots | 60 | 60 | 60 | 60 | 60 | 300 | distinct `slot_id`; `plan.json` has 60 slots each |
| Slots with more than one try | 18 | 27 | 28 | 29 | 21 | 123 | slots with more than one file |
| ... of them with a failed check | 11 | 17 | 26 | 28 | 20 | 102 | slot has a try whose `checks/*-step3.json` or `-step4.json` verdict is not `pass` |
| ... of them only after a send-back of the owner | 7 | 10 | 2 | 1 | 1 | 21 | difference |
| Slots with 1 try | 42 | 33 | 32 | 31 | 39 | 177 | tries-per-slot distribution |
| Most tries for one slot | 6 (M1-S47) | 3 (5 slots) | 6 (M3-S48) | 7 (M4-S27) | 6 (M5-S39) | | max of tries per slot |
| Distribution {tries: slots} | {1:42, 2:16, 3:1, 6:1} | {1:33, 2:22, 3:5} | {1:32, 2:21, 3:3, 4:3, 6:1} | {1:31, 2:17, 3:7, 4:2, 5:2, 7:1} | {1:39, 2:14, 4:2, 5:4, 6:1} | | Counter of tries per slot |
| Requests of step 2 (field `request` = 2) | 65 | 60 | 61 | 61 | 64 | 311 | field `request` of each question file |
| Requests of step 5 (field `request` = 5) | 18 | 32 | 40 | 50 | 37 | 177 | same |
| Tries that failed step 3 or step 4 | 14 | 18 | 39 | 49 | 39 | 159 | verdict not `pass` |
| Step 3 verdict `fail` | 0 | 1 | 2 | 4 | 4 | 11 | `checks/*-step3.json` |
| Step 4 verdict `fail` | 14 | 17 | 37 | 45 | 35 | 148 | `checks/*-step4.json` |
| Step 4 verdict `cannot_decide` | 0 | 0 | 0 | 0 | 0 | 0 | `checks/*-step4.json` |
| Tries with status `cannot_write` | 0 | 0 | 0 | 0 | 0 | 0 | field `status` of question files |
| Open-slot events (`more_tries` + `new_point`) | 1 | 0 | 4 | 6 | 6 | 17 | `owner-decisions.json` |
| ... `more_tries` | 1 | 0 | 3 | 5 | 2 | 11 | same |
| ... `new_point` | 0 | 0 | 1 | 1 | 4 | 6 | same |
| ... reason `three_tries` | 1 | 0 | 4 | 6 | 6 | 17 | rebuilt (4.1) |
| `new_plan` | 0 | 0 | 0 | 0 | 0 | 0 | same |
| Rewrites of the owner | 9 | 14 | 2 | 2 | 0 | 27 | action `rewrite` |
| ... with a new point | 5 | 0 | 0 | 0 | 0 | 5 | `rewrite` with field `point` |
| Bad marks | 0 | 0 | 0 | 0 | 2 | 2 | `runs/mock-0N/marks/round-*.json`, `"mark": "bad"` |
| Final state | built | built | built | built | built | | `report.json`, field `state` |

Step 4 finding rules of the failed tries (count of findings; one failed try can have more than one finding):

| Mock | Step 3 rules | Step 4 rules |
|---|---|---|
| 1 | none | B3 1, B4 1, B5 2, B6 3, B7 7 |
| 2 | A12 1 | B1 1, B2 1, B3 2, B5 1, B6 8, B7 5, B8 2 |
| 3 | A12 2 | B1 1, B6 3, B7 11, B9 24 |
| 4 | A1 1, A2 1, A12 3 | B3 2, B6 1, B7 4, B8 1, B9 39 |
| 5 | A1 1, A2 1, A9 2, A12 1 | B3 2, B7 2, B8 1, B9 31 |

### 4.3 Checks of the numbers in other files

- Build guide, `docs/build-guide/step-5-try-again.md` 19-23 (mock 1): "83 tries for 60 slots: 65 were a request of step 2 ... and 18 a request of step 5", "18 slots needed more than one try. The most tries for one slot: 6", "Step 4 failed 14 tries. The findings by rule: B3 1, B4 1, B5 2, B6 3, B7 7", "The owner sent 9 questions back as rewrites after the marks, 5 of them with a new point." All agree with the run files.
- The tab 2 sample, Fig. 3: "83", "18 of 60 slots had more than one try: 11 after a failed check, 7 only after a rewrite", "9 tries were rewrites that the owner asked for". 83, 18, 11 and 7 agree. "9" agrees with the 9 decisions `rewrite` in `runs/mock-01/owner-decisions.json` (D002 to D010). The sample card counts the same file (`academy/sample/make-1-1.py`, 88).
- The sample methods (`academy/sample/make-1-1.py`, 84-93) give the same values for mock 1: TRIES 83, SLOTS 60, MORE 18, FAILED 11, RWONLY 7, MAX 6, REWRITES 9.
- Decision 0066, line 62: "Mock 3 had 101 tries for 60 slots." Agrees.

### 4.4 The open-slot events

| Mock | Decision | Slot | Action | after_try | Cause in the reason of the owner (`owner-decisions.json`) |
|---|---|---|---|---|---|
| 1 | D001 | M1-S47 | more_tries | 3 | "Each try corrected the last finding. The findings are small." |
| 3 | D001 | M3-S01 | new_point 4.4-S4 | 3 | "Three tries repeated the scene of M2-S52 (rule B9)." |
| 3 | D002 | M3-S07 | more_tries | 3 | "Three tries repeated the scene of M2-S54 (rule B9)." |
| 3 | D003 | M3-S48 | more_tries | 3 | "Two tries failed rule B6 on \"-p\", which was a fault of B6 (decision 0061)." |
| 3 | D004 | M3-S53 | more_tries | 3 | "The tries failed on rules B7 and B1." |
| 4 | D001-D003 | M4-S06, M4-S50, M4-S54 | more_tries | 3 | "B9 failed three times on the same problem. The idea has almost only one problem, so it joins the narrow list (decision 0068)." |
| 4 | D004 | M4-S23 | new_point 2.1-S1 | 3 | "B9 failed three times." |
| 4 | D005 | M4-S27 | more_tries | 3 | "The last try failed on the form (rules A1 and A2), not on B9." |
| 4 | D006 | M4-S27 | more_tries | 6 | "B9 failed three more times on the problem of M2-S11. G041 joins the narrow list (decision 0068)." |
| 5 | D001-D003 | M5-S28, M5-S29, M5-S39 | new_point 5.6-K3, 3.4-S3, 4.1-S2 | 3 | "B9 failed three times on the problem of an earlier question." |
| 5 | D004 | M5-S38 | more_tries | 3 | see story (b) |
| 5 | D005 | M5-S37 | more_tries | 3 | "G042 joins the narrow list (decision 0075)." |
| 5 | D006 | M5-S60 | new_point 2.2-S1 | 3 | "B9 failed twice on the problem of M3-S24 and M2-S07, and once the form failed." |

Each slot that opened passed later. `report.json` of each mock has the state `built` and no slot that is not `passed`.

### 4.5 The reason of the owner before and after decision 0074

- The code change of decision 0074 is commit `e9b1e6b` (9 October 2026, 19:17:35 +1100). It changes `src/control.py` and adds the test `test_more_tries_gives_the_reason_of_the_owner_to_the_writer`. `git log e9b1e6b..HEAD -- src/control.py src/step2_write.py` is empty, so the code did not change after it. (L1)
- Before that commit, the `more_tries` branch was `return self._step5(request, last, self._check_findings(last))`: no reason of the owner (`git show e9b1e6b -- src/control.py`). (L1)
- 9 `more_tries` decisions came before the commit (mock 1 D001, mock 3 D002 to D004, mock 4 D001 to D003, D005, D006). Their reasons did not reach the writer. 2 came after it (mock 5 D004 M5-S38, D005 M5-S37). Method: `git log --format="%h %ad %s" --date=iso -- runs/mock-0N/owner-decisions.json`. The mock 4 decisions are in commits `ea2529a` (12:48) and `5aaca92` (12:57) of 9 October 2026, before `e9b1e6b`. (L1)

### 4.6 Method of the replay (fact N5)

Copy `runs/mock-05/` to a scratch folder twice. In copy 1, delete `questions/M5-S38-T5.json` and `checks/M5-S38-T5-step*.json`. In copy 2, also delete the files of T4. For each copy: `c = Control(folder, 5, 0, None, {})`, `s = c._slot("M5-S38")`, `r = c.request_for(s, c.slot_state(s))`, print `r["step"]`, `r["shown_try"]` and the rules of `r["findings"]`. No step is called, so no model call.

## 5. Story (a): the review loop that ended when the control became code

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | The counts: 14 serious items, then 10 new ones, most from the rules of decision 0037. | `docs/decisions/0038-...`, Question, 10 | "The first review found 14 serious items. Decision 0037 answered them. The second review found 10 new serious items, and most of them come from the rules of decision 0037. How do we stop this cycle?" | 2 |
| A2 | The quote of the owner. | `docs/decisions/0038-...`, How we decided, 62 | "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." | 2 |
| A3 | The theme of the problems. | `docs/decisions/0038-...`, How we decided, 62 | "The owner asked what the theme of the problems is: too many rules, or too much control. The answer: too much automatic repair, designed before one real run." | 2 |
| A4 | The two options. | `docs/decisions/0038-...`, Options, 14-15 | "1. Answer the 10 new items in words, change the files, and review again." / "2. Make the control simple for mock 1, and write the control as code with tests." | 2 |
| A5 | The fix, part 1: one automatic loop, with the limits of 0033 and 0037. | `docs/decisions/0038-...`, Decision, 21 | "1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5. The limits of decisions 0033 and 0037 stay: 3 tries, and \"cannot decide\" two times." | 2 |
| A6 | The fix, part 2: each other failure waits for the owner. | `docs/decisions/0038-...`, Decision, 22 | "2. **Each other failure waits for the owner.** A slot that is `open`, a finding of step 6, a bad mark, and a call that fails 3 times. The program does no automatic repair for them." | 2 |
| A7 | The fix, part 4: the owner is the limit of the rounds. | `docs/decisions/0038-...`, Decision, 24 | "No count limits these rounds, because the owner starts each one." | 2 |
| A8 | The fix, part 6: the control is code, with tests that make no model call. | `docs/decisions/0038-...`, Decision, 26 | "6. **The control is code.** It is one part of the program, with tests that make no model call. A fake writer and fake checkers give the answers that a test tells them to give. Each case is one test. The 10 cases of the second review are the first tests." | 2 |
| A9 | What happened to the 10 items: 3 closed (items 1, 2, 4), 2 removed (items 3, 5), 5 to the code and its tests (items 6 to 10). | `docs/decisions/0038-...`, 33-44; `docs/journal.md`, 223 | "It closes 3 of the 10 items, removes 2, and gives 5 to the code and its tests." | 2 / 4 |
| A10 | A correction of the assistant. | `docs/decisions/0038-...`, How we decided, 64 | "The assistant said first that the simple control removes most of the 10 items. That was too strong. It removes 2." | 2 |
| A11 | The reason for code with tests. | `docs/decisions/0038-...`, Reason, 51 | "a rule in words can clash with a rule in a different file, and a reviewer finds that only by following one case through all files. A test runs the case. A case with no path makes the test fail." | 2 |
| A12 | The limit of the tests. | `docs/decisions/0038-...`, Reason, 52 | "A test shows that a case has a path. It does not show that the path is good. The owner decides that." | 2 |
| A13 | No independent reviewer checked decision 0038. | `docs/decisions/0038-...`, 66 | "No independent reviewer checked this file." | 2 |
| A14 | The second review: "Most of them are cases that the new rules made." | `docs/reviews/review-decisions-0024-to-0037.md`, 14-15 | "Of the 14 serious items: 8 are closed and 6 are closed in part." / "Reviewer B found 10 new serious items. Most of them are cases that the new rules made." | 4 |
| A15 | The journal has the same quote and the counts. | `docs/journal.md`, 221 (section "7 October 2026") | "The assistant agreed: the first review found 14 items, and the fixes made 10 new ones." | 4 |
| A16 | The control program that followed: `src/control.py`, tests in `tests/`, 53 tests at the time. | `docs/decisions/0039-...`, 20 | "The tests are in `tests/`. They use `unittest` of Python. No test makes a model call. 53 tests pass." | 2 |
| A17 | Two independent reviews of the code found bugs, each fix with a test that fails without it. | `docs/decisions/0039-...`, 83 | "The first found 4 serious and 6 minor bugs. The second found 1 serious and 3 minor bugs in the fixes." / "the assistant checked that each test fails without its fix." | 2 |
| A18 | Today: 66 tests in `tests/test_control.py`, 228 tests in all, all pass without an API key. | run on 13 October 2026 | "Ran 228 tests ... OK" | 1 |
| A19 | The test file says no test makes a model call. | `tests/test_control.py`, 1; `src/control.py`, 19 | "Tests of the control (decision 0038). No test makes a model call." / "In the tests, `steps` is a fake. No test makes a model call." | 1 |
| A20 | `CLAUDE.md` keeps the rule. | `CLAUDE.md` ("Two more rules for code") | "A test of the control makes no model call (decision 0038)." | (project file) |
| A21 | The first real run: one slot of mock 1 stopped at the guard, and the owner gave it more tries. | `docs/build-guide/step-5-try-again.md`, 22; `docs/journal.md`, 138 | "One slot stopped after 3 tries. Each try had corrected the last finding, and a new small finding came. The owner gave it more tries." / "One slot (M1-S47) failed 3 tries. The owner selected `more_tries` ... and it passed on its fourth try." | 3 / 4 |
| A22 | The run files of M1-S47: T1 fail B7, T2 fail B7, T3 fail B5, D001 `more_tries`, T4 pass, rewrite D007 (after try 4), T5 fail B4, T6 pass. | `runs/mock-01/questions/M1-S47-T*.json`, `runs/mock-01/checks/M1-S47-T*-step4.json`, `runs/mock-01/owner-decisions.json` | T1 B7: "Option E says \"Make the few-shot examples cover…\". The definite article points to examples that the stem never introduces"; T2 B7: "The reviewing actor has more than one name."; T3 B5. | 1 |
| A23 | The reason of D001 (M1-S47) did not reach the writer, because the code passed the reason only from commit `e9b1e6b` on (section 4.5). | `runs/mock-01/owner-decisions.json`; `git show e9b1e6b` | "Each try corrected the last finding. The findings are small." | 1 |

## 6. Story (b): the reason of the owner did not reach the writer (mock decision 0074)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | The question of decision 0074. | `docs/decisions/0074-...`, Question, 10 | "For the open slot M5-S38, the owner gave 3 more tries with an instruction: \"use the second problem, custom_id to match answers to requests\". The program sent the writer the last failed try and its findings, but not the reason of the owner (decision 0039). How does the instruction reach the writer?" | 2 |
| B2 | The exact reason in the run file. | `runs/mock-05/owner-decisions.json`, D004 (line 30 is `"id": "D004"`) | "B9 failed three times on the problem of resubmitting failed requests. Use the second problem of the point instead: custom_id to match each answer to its request, because batch results do not come back in the order of the requests." | 1 |
| B3 | The decision. | `docs/decisions/0074-...`, Decision, 19 | "Option 1. After a decision `more_tries`, the request of step 5 has the findings of the last try and the reason of the owner, as for a rewrite (decision 0045). A test checks it." | 2 |
| B4 | The test. | `tests/test_control.py`, 114-122 | `def test_more_tries_gives_the_reason_of_the_owner_to_the_writer(self):` / `# Decision 0074: the reason of the owner goes to the writer.` | 1 |
| B5 | The code. | `src/control.py`, 270-281 | `owner = [{"step": 7, "rule": "owner", "detail": event["decision"]["reason"], ...}]` / `return self._step5(request, last, self._check_findings(last) + owner)` | 1 |
| B6 | The plain reason. | `docs/decisions/0074-...`, Reason, 27 | "Plain reason: the owner's reason says what the next try must do differently. Without it, the writer repeats the same problem, as M5-S38 did three times." | 2 |
| B7 | How it was found. | `docs/decisions/0074-...`, How we decided, 31 | "The assistant found that the program did not pass the reason, and made the change so that the instruction reaches the writer." | 2 |
| B8 | The result in the decision: the final question did not follow the instruction. | `docs/decisions/0074-...`, Decision, 23 | "The result: the final M5-S38 still answers \"resubmit only the failed requests\" (option A, with option B). Matching answers to requests by custom_id appears only as a wrong option (option D). The instruction reached the writer, but the question did not follow it." | 2 |
| B9 | The final question in the built mock is M5-S38-T5, correct A and B. | `mocks/mock-05.questions.json`, 1085; `mocks/mock-05.answers.json`, 1109 | `"question_id": "M5-S38-T5"`, `"correct": ["A", "B"]` | 1 |
| B10 | M5-S38-T5, option A (correct). | `runs/mock-05/questions/M5-S38-T5.json` | "The retry step resubmits every request instead of only the failed ones identified by their custom_id, so successful reviews are paid for twice." | 1 |
| B11 | M5-S38-T5, option D (wrong). | same | "The retry step matches each result to its file by custom_id, which links the reviews of the retried files to the wrong source files." | 1 |
| B12 | The try history of M5-S38 (point 4.5-S3): T1 (request 2), T2, T3, T4, T5 (request 5). T1 to T4 failed step 4 on B9. T5 passed. | `runs/mock-05/questions/M5-S38-T*.json`, `runs/mock-05/checks/M5-S38-T*-step4.json` | T1: "Earlier question M3-S12-T1 has the same problem"; T2: "Earlier question M1-S46-T1 uses the same scene"; T3: "Same problem as M3-S12-T1."; T4: "The question repeats the problems of both earlier questions and adds no new one." | 1 |
| B13 | What happened after the fix: T4, the first try after the instruction, did follow it. Its two correct options are about custom_id. | `runs/mock-05/questions/M5-S38-T4.json` | A (correct): "Select the files to resubmit by reading the custom_id of each failed result, which maps directly to the source file path." B (correct): "Give each chunk request a custom_id that combines its file's original custom_id with a chunk index, so the results can be regrouped by file." | 1 |
| B14 | T4 failed B9: matching by custom_id was already the answer of M1-S46-T1 (point 4.5-K4) in mock 1. | `runs/mock-05/checks/M5-S38-T4-step4.json`; `runs/mock-01/questions/M1-S46-T1.json` | "M1-S46-T1 is the same scene: a nightly batch generating tests per source file, a custom_id set from the file path, and attaching each suite to the right file." / M1-S46-T1 correct option B: "Assign each request a custom_id derived from its source file path, then match each returned result to its file by that custom_id." | 1 |
| B15 | T5 did not get the reason of the owner. Its request had only the B9 finding of T4 (replay, fact N5). T5 went back to "resubmit only the failed requests" and passed. | `src/control.py`, 236-239; replay 4.6 | (see N4, N5) | 1 |
| B16 | T2 (before the instruction) already tried custom_id matching, and failed B9 on M1-S46-T1. | `runs/mock-05/questions/M5-S38-T2.json`, `runs/mock-05/checks/M5-S38-T2-step4.json` | T2 correct B: "Identify the failed files by reading the custom_id on each failed result instead of relying on the position of that result in the list." | 1 |
| B17 | Timing: code change and decision in commit `e9b1e6b` (19:17:35). T4 and T5 are in commit `18fc105` "Mock 5: run 3" (19:34:28). | `git log` | | 1 |
| B18 | In the same round, three other open slots got new points. | `docs/decisions/0074-...`, 21 | "In the same round, the owner gave new points to three open slots of mock 5: M5-S28 the point 5.6-K3, M5-S29 the point 3.4-S3 and M5-S39 the point 4.1-S2." | 2 |
| B19 | The second review in Cowork checked the decision, and the owner confirmed it. | `docs/decisions/0074-...`, 33 | "The second review in Cowork checked this file. The owner confirmed the text of this file on 9 October 2026." | 2 |
| B20 | The journal: the owner asked for the sentence "did not follow". | `docs/journal.md`, 41 | "In 0074 the final M5-S38 did not follow the instruction of the owner. The assistant checked the two question texts in `mocks/mock-05.questions.json`." | 4 |
| B21 | The build guide and diagram 07 show the fix. | `docs/build-guide/step-5-try-again.md`, 13; `docs/diagrams/07-make-diagram.py`, 104 | "After \"more tries\", the writer also gets the reason of the owner as an instruction (decision 0074)." / "The writer also gets the reason of the owner as an instruction, for example \"use the second problem of the point\" (decision 0074)." | 3 |
| B22 | Decision 0016 (academy) permits the page to show M5-S38 with its answer. | `academy/decisions/0016-...`, Decision | "A page can show a real mock question with its answer, where the story needs it." | 2 |

## 7. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/control.py` | 30-32 | The three limits: `CALL_RUNS = 3`, `TRIES = 3` "A guess.", `CANNOT_DECIDE = 2`. |
| `src/control.py` | 158-174 | `send_backs`: each event that gives a slot a new start. |
| `src/control.py` | 188-225 | `slot_state`: the whole status of a slot. |
| `src/control.py` | 211-224 | A pass stops the loop first, then the two limits and `open_reasons`. (The sample uses this range.) |
| `src/control.py` | 229-239 | `request_for`: a failed try of this start gives a request of step 5 with that try. |
| `src/control.py` | 270-281 | The fix of decision 0074: the reason of the owner as a finding with the rule "owner". |
| `src/control.py` | 283-294 | `_step5` and `_check_findings`: what goes into the request. |
| `src/control.py` | 94-99 | A record is never written over. |
| `src/control.py` | 378-392 | `_save_try`: the new file with the next try number, `request` and `shown_try`. |
| `src/control.py` | 633-644 | `decide` for `new_point` and `more_tries`: only for an open slot. |
| `src/control.py` | 698-711 | The three checks of a new point (decision 0045). |
| `src/step2_write.py` | 152-159 | The text "A NEW TRY ..." that the writer gets, with the failed question and the findings. |
| `src/step4_check_model.py` | 194 | `def check(self, question, slot):` the checker gets no findings. |
| `tests/test_control.py` | 96-102 | Tries 2 and 3 are requests of step 5 with the last try. |
| `tests/test_control.py` | 114-122 | The test of decision 0074. |
| `tests/test_control.py` | 84-94 | A slot open with both reasons. |
| `tests/test_control.py` | 630-636 | More tries after three tries is step 5 with the last try. (The sample uses line 630.) |
| `tests/test_control.py` | 647-665 | Two "cannot decide" stop a slot, and the count starts at zero after a send-back. |
| `git show e9b1e6b -- src/control.py` | | The diff of the fix of decision 0074 (10 lines). |
| `runs/mock-05/owner-decisions.json` | D004 (from line 29) | The decision record with the reason of the owner. |
| `runs/mock-01/questions/M1-S05-T2.json` | 1-9 | A real record of a try of step 5. |
| `docs/diagrams/07-make-diagram.py` | 31 | An example open slot of the diagram (invented): `open_reasons: ['three_tries']`. |

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| C1 | Point 4.4-S2 is in the popups of diagram 01 for step 5, but not in the build guide table of step 5 (academy decision 0024). | `docs/diagrams/01-pipeline-overview.html`, 191, popup "5" (Try again) and popup "L" (The limit of tries is reached): point "4.4-S2", "Identifying when retries will be ineffective (e.g., information exists only in an external document not provided) versus when they will succeed (format mismatches, structural output errors)". Decision 0013, line 36, also lists "4.4-K1, 4.4-S1, 4.4-K2, 4.4-S2". | `docs/build-guide/step-5-try-again.md`, 37-44: the table has 4.4-K1, 4.4-S1, 4.4-K2, 1.1-S3, 4.3-K1, 4.3-S3, and not 4.4-S2. Academy decision 0024 already names 4.4-S2 as a point of diagram 01 that no table has. |
| C2 | Does the reason of the owner reach each try of the new start, or only the first? | `docs/decisions/0074-...`, 19: "After a decision `more_tries`, the request of step 5 has the findings of the last try and the reason of the owner". `docs/build-guide/step-5-try-again.md`, 13: "After \"more tries\", the writer also gets the reason of the owner as an instruction". `docs/diagrams/07-make-diagram.py`, 104 (same). | `src/control.py`, 236-239: when a try of the start failed, `return self._step5(request, failed, self._check_findings(failed))`, with no reason of the owner. Replay (N5): the request of M5-S38-T5 has only the finding `B9`. The test (`tests/test_control.py`, 121) forces `in_round=[]`, so it checks only the first try. |
| C3 | "The question did not follow it": true for the final question, but the first try after the fix did follow the instruction. | `docs/decisions/0074-...`, 23: "The instruction reached the writer, but the question did not follow it." | `runs/mock-05/questions/M5-S38-T4.json`: both correct options use custom_id (B13). T4 failed B9 against M1-S46-T1 (B14). T5, which did not get the reason (C2), is the final question. |
| C4 | Number of open slots of mock 5. | `docs/journal.md`, 30: "7 slots opened on B9 or the form: new points for M5-S28, S29, S39 and S60, more tries for M5-S38 ... and M5-S37". | `runs/mock-05/owner-decisions.json`: 6 open-slot decisions (D001 to D006) for 6 slots. The rebuilt history (4.4) finds 6 open events and no other slot with 3 failed tries in one start. The journal sentence also names only 6 slots. |
| C5 | Letters of a new try in mock 5. | `docs/decisions/0033-...`, 38: "Code mixes the options of the new try and gives them new letters. The new letters have no connection with the old letters." `docs/diagrams/07-make-diagram.py`, 71: "Code mixes the options again and gives new letters." | `docs/decisions/0070-...`, 22: "**Step 2** (and step 5) puts the correct options at the letters of the slot." `src/step2_write.py`, 191-199. In mock 5, each try of a slot has the same correct letters (example: M5-S38-T1 to T5 all have A and B correct). |
| C6 | Request after a rewrite of a step 6 finding. | `docs/decisions/0033-...`, 75 (and `docs/decisions/0039-...`, 50): "`rewrite` of a finding of step 6 \| Step 5 \| The named question, the finding, the reason of the owner, and the text of the other questions of the finding". | `docs/decisions/0045-...`, 23 (later) and `src/control.py`, 261-266: a rewrite with a new point is a request of step 2. Run: `runs/mock-01/owner-decisions.json` D010, a rewrite of finding M1-SC2-R1-F1 with point 3.4-K4. |
| C7 | Where the tab 2 sample says the 10 new items came from. Small wording difference. | `academy/sample/1-1-split-behind-the-mocks.html`, Fig. 4: "most of them came from the answers to the first." | `docs/decisions/0038-...`, 10: "most of them come from the rules of decision 0037." `docs/reviews/review-decisions-0024-to-0037.md`, 15: "Most of them are cases that the new rules made." (Decision 0037 is the answer to the first review, so the meaning is close.) |

## 9. Not found

1. No run file stores the text of a request that the writer got. The records keep only `request` (2 or 5) and `shown_try`. So "the instruction reached the writer" (decision 0074) is shown by the code, the test and the replay (N5), not by a saved request.
2. No case of `cannot_decide` (step 4) or `cannot_write` in mocks 1 to 5. So no real example exists for the guard "two cannot decide" or for an open slot with `cannot_write`.
3. No `new_plan` in mocks 1 to 5. How a new plan starts is not built (`docs/decisions/0033-...`, 61).
4. No source measures whether the findings help the writer (for example, a pass rate of step 5 tries against first tries). Only counts exist.
5. No record of the owner's reasons for the number 3 beyond "a guess" (`src/control.py`, 31; decision 0033, 114). The test of decision 0024 did not change it (not checked in the files of `runs/test-0024/`).
6. `docs/lessons.md` has no entry on step 5, decision 0038 or decision 0074 (search for "0038", "0074", "more tries", "cycle", "guard": no match).
7. A dated copy of the documentation page "Define tools" of 13 October 2026 in `academy/sources/` (academy decision 0030) was not saved: this agent may change no file except this fact sheet. The copy of 7 October 2026 is in `docs/sources/2026-10-07-anthropic-docs-define-tools.md`, and its row (line 564) agrees with the live page.
8. Diagram 07 has no drawing of the M5-S38 case or of the fact that the reason reaches only the first try.
