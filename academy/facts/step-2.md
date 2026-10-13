# Fact sheet: tab 2, step 2 "Write the question"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `b24ea7f` (branch `main`, clean).
- Levels of trust (academy decisions 0011, 0014, 0029): 1 = code, tests, data and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = an outside documentation page. "L" = level. "Computed" = a number that a script of this agent made from level 1 files (method in section 4).
- A path such as `docs/decisions/0029-...md` means the one file in `docs/decisions/` whose name starts with `0029-`. Line numbers are for commit `b24ea7f`.
- Tests run on 14 October 2026 with no API key and no model call (the tests use a fake client): `python3 -m unittest tests.test_model_steps` gives "Ran 37 tests ... OK"; `python3 -m unittest tests.test_earlier` gives "OK" (12 tests, `grep -c "def test"`).
- Files that this agent did not read (working rules 19 and 28, academy decision 0028): `marking/*.xlsx`, `responses.json` and all personal files of the owner, `claude-code-brand-kit/`, conversation transcripts. No model call, no API key, `src/run.py` not run.
- Scripts of this agent were in its scratchpad, not in the repository. They read files only.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | One call of the Claude API writes one question for one slot. The call is new each time and does not know the other questions of the mock. | `docs/build-guide/step-2-write-the-question.md`, 9 | "For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock." | 3 |
| O2 | The decision that made step 2 (6 October 2026): one call, one question, one slot. 60 slots give 60 calls. | `docs/decisions/0010-...md`, 20 | "Option 1. Step 2 is the writer. For each slot of the plan (decision 0009), one API call writes one question. 60 slots give 60 calls." | 2 |
| O3 | The plain reason (no guide point). | `docs/decisions/0010-...md`, 24 | "One call makes one record with one ID, so each later verdict connects to exactly one question. If one question fails, the program writes that one again and the others do not change." | 2 |
| O4 | The rejected option: one call for the 15 questions of a scenario. | `docs/decisions/0010-...md`, 32 | "We rejected option 2. Its writer sees the other questions, but one bad output spoils about 15 questions." | 2 |
| O5 | The accepted cost of option 1: the writer cannot see the other questions of its scenario. Another step does that work. | `docs/decisions/0010-...md`, 30 | "We accepted one disadvantage: a writer that sees one slot does not see the other questions of its scenario. It cannot prevent two questions with the same scene" | 2 |
| O6 | The same writer code serves step 5 (a new try). | `src/step2_write.py`, 1-7 | "Step 2 writes the first question of a slot. Step 5 writes a new try: it is the request of step 2, plus the failed question with its letters and its findings" | 1 |
| O7 | Status: built; it ran in the test of 7 October 2026 and for mocks 1 to 5, 7 to 9 October 2026. Question record dates agree: mock 1 2026-10-07 (73) and 2026-10-08 (10); mock 2 2026-10-08; mock 3 2026-10-08 (99) and 2026-10-09 (2); mocks 4, 5 2026-10-09. | `docs/build-guide/step-2-write-the-question.md`, 3; field `date` of `runs/mock-0N/questions/*.json` | "Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026." | 3 / 1 |

## 2. Explanation facts: the mechanism

### 2.1 Who calls the step, and what it saves

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | The control calls the writer for a slot with the status `to_write`, through `steps.write`. | `src/control.py`, 350-360 | `answer = self._call("write", slot["slot_id"], self.steps.write, request)` | 1 |
| E2 | The control (code), not the writer, builds the request and decides if it is step 2 or step 5. A plain first try is `"step": 2` with no findings. | `src/control.py`, 229-239 | `request = {"slot": slot, "point": self.point_of(slot), "step": 2, "shown_try": None, "failed_question": None, "findings": [], "other_questions": []}` | 1 |
| E3 | A rewrite with a new point (decision 0045) is also a request of step 2, with the owner's reason and the other questions not to repeat. | `src/control.py`, 261-266; `src/step2_write.py`, 143-151 | `# Decision 0045: a rewrite with a new point is a request of step 2 on` / "A NEW QUESTION FOR THIS SLOT, ON THE POINT MARKED ABOVE. The owner asks for it:" | 1 |
| E4 | The real step gives the writer the seed of the plan, the earlier questions on the idea (0056) and the narrow-idea test (0066). | `src/steps.py`, 53-67 | `self.writer.seed = self._plan()["seed"]` / `self.writer.earlier = self._earlier()` / `self.writer.narrow = self._narrow_of` | 1 |
| E5 | A failed call (API error that a new call can repair, refusal, `max_tokens`, no valid JSON, incomplete form) runs again, at most 3 times. Then an error record; no question record. These runs are not tries. | `src/control.py`, 30, 309-322; `src/model_call.py`, 45-54, 130-142; `src/step2_write.py`, 168-180; `docs/decisions/0029-...md`, 116 | `CALL_RUNS = 3          # runs of a call that fails (decision 0037, item 10). A guess.` / "These are not tries of the slot." | 1 / 2 |
| E6 | An error that a new call cannot repair (for example 400, no key) stops the run at once. | `src/model_call.py`, 45-54; `docs/decisions/0041-...md`, 33 | "Each other error stops the run at once, with the cause." | 1 / 2 |
| E7 | No mock has an error record: no `runs/mock-0N/errors/` folder exists. | `ls runs/mock-0*/errors` (no match) | | 1 |
| E8 | The question record: one JSON file for each try, never written over. Fields `question_id`, `slot_id`, `try`, `point`, `select`, `request`, `shown_try`, `status`, `date`, `model`, then `question` and `options`, or `cannot_write_reason`. | `src/control.py`, 378-392; `docs/decisions/0029-...md`, 104-105 | `qid = "%s-T%d" % (slot["slot_id"], n)` / `self._write_new(record, "questions", qid + ".json")` | 1 / 2 |
| E9 | A real record: `runs/mock-01/questions/M1-S01-T1.json`, point 2.5-K3, `"request": 2`, `"model": "claude-opus-5-5"`, 4 options A to D, C correct ("Use Edit to replace the incorrect URL, since that string appears once and gives a unique match for the targeted change."). | that file | | 1 |
| E10 | The request text is not saved in the record. Only `request` (2 or 5) and `shown_try` say which request the writer got. | `src/control.py`, 378-392 | | 1 |

### 2.2 What the request holds, in order

The call (`src/model_call.py`, 108-120) sends: `system` = [the rules (cached block), the system text]; `messages` = one user message with the request text; `output_config` = effort and the form.

| # | Part, in the order of the code | Source, lines | Exact quote | L |
|---|---|---|---|---|
| R1 | System block 1: the list of rules, with a cache mark (`"cache_control": {"type": "ephemeral"}`). | `src/model_call.py`, 112-114; `src/step2_write.py`, 218-220 | `# Decision 0067: the rules come first as a cached block.` | 1 |
| R2 | The list has 21 rules: A1 to A12 (code checks them, step 3) and B1 to B9 (a model checks them, step 4), plus "Two more instructions" and the letters note. 3077 characters, 581 words (computed). | `src/step2_write.py`, 31-63 | "Rules for a good question. Code checks group A. A second model checks group B." / "Do not give letters to the options. Code gives the letters." | 1 |
| R3 | A narrow idea gets the same list with the copy rule B9 in place of the strict B9 (2788 characters, computed). So there are two cached lists. | `src/step2_write.py`, 109-111; `docs/decisions/0067-...md`, 23 | "A narrow idea has its own list, with the copy rule B9 (decision 0066), so it has its own cache." | 1 / 2 |
| R4 | System block 2: the role and the form description. | `src/step2_write.py`, 65-67 | "You write one exam question for a mock exam of the exam \"Claude Certified Architect - Foundations\". The question must follow the rules exactly, and it must use only facts that the exam guide states. Return the question in the form. Return one exam question for the slot, or say that you cannot write it." | 1 |
| R5 | User text, part 1: 3 sample questions of the guide, from scenarios that are not the slot's scenario. Code mixes their options, removes the letters, marks the correct option, leaves out the explanation. The slot ID seeds the choice, so the same slot always gets the same 3. | `src/step2_write.py`, 70-86, 123-124 | "Which samples, when more are possible, was not decided: the slot ID selects them, so the same slot gets the same examples." | 1 |
| R6 | Part 2: the story of the slot's scenario. | `src/step2_write.py`, 125-126 | `"The story of the scenario %d (%s):"` | 1 |
| R7 | Part 3: the task statement with all its points; the slot's point is marked `>>>`. | `src/step2_write.py`, 127-129 | "Its points (the point of the slot is marked with >>>):" | 1 |
| R8 | Part 4: the 14 technologies of Section 17 (14 = `len(records["section_17"]["technologies"])`, computed). | `src/step2_write.py`, 130-131 | "The technologies that the guide names (Section 17):" | 1 |
| R9 | Part 5: the slot (scenario, task statement, point, type, options, select, `longest_may_be_correct`), and the count line. The slot shown to the writer has no `slot_id` and no `correct_letters`. A plan with no field (mock 1) shows `longest_may_be_correct: true`. | `src/step2_write.py`, 132-136 | `"Write %d options. Mark exactly %d of them correct."` / `slot.get("longest_may_be_correct", True)` | 1 |
| R10 | Part 6, only when the idea is in an earlier built mock: the earlier questions with "CORRECT:"/"WRONG:" on each option, and the rule (strict or narrow). | `src/step2_write.py`, 89-106, 137-139 | "Write a question with a different problem, also if you change the setting" | 1 |
| R11 | Part 7, only for a two-answer slot. | `src/step2_write.py`, 140-142 | "The two correct options test two different parts of the point. They are not two examples of one idea." | 1 |
| R12 | Part 8, only for a rewrite with a new point (step 2) or a new try (step 5): the owner's reason, or the failed question with its letters and findings, and the other questions not to repeat. | `src/step2_write.py`, 143-164 | "A NEW TRY. The question below did not pass." | 1 |
| R13 | `output_config`: `{"effort": "high", "format": {"type": "json_schema", "schema": ...}}`; `max_tokens` 64000; the call streams. No `tools`, no `tool_choice`. | `src/model_call.py`, 20-26, 116-120; `tests/test_model_steps.py`, 105-112 | `self.assertNotIn("tool_choice", req)` | 1 |
| R14 | The model and effort are "first values, not decisions". All 488 question records of mocks 1 to 5 have `model` `claude-opus-5-5`; each usage file has effort `high` (computed). | `src/model_call.py`, 20-23 | "These are first values, not decisions." | 1 |
| R15 | The order of the parts in decision 0029: rules, 3 samples, story, task statement, technologies, slot, form. The decision left the exact order open. | `docs/decisions/0029-...md`, 27-33, 136 | "The exact text of the request and the sequence of its parts." (not decided yet) | 2 |

### 2.3 What the writer returns: the form

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| F1 | The form file: `docs/diagrams/04-form-schema-draft.json`, loaded by code, so decisions and code use one copy. Fields: `status` (enum `written`, `cannot_write`), `question` (string or null), `options` (array of `text`, `correct` boolean, `reason`), `cannot_write_reason` (string or null). All four required. | `docs/diagrams/04-form-schema-draft.json`, 1-38; `src/step2_write.py`, 16; `src/model_call.py`, 1-5, 75-81 | `"enum": ["written", "cannot_write"]` | 1 |
| F2 | Code adds `"additionalProperties": false` to each object before it sends the schema (the documentation requires it). | `src/model_call.py`, 57-72; `docs/decisions/0040-...md`, 23 | "Add \"additionalProperties\": false to each object of a schema. The documentation of structured outputs requires it (decision 0040)." | 1 / 2 |
| F3 | The `name` and `description` of the draft are not sent as a tool. The description goes into the system prompt. | `src/model_call.py`, 81; `src/step2_write.py`, 65-67; `docs/decisions/0044-...md`, 27 | "The code puts the description of each form into the system prompt of the call." | 1 / 2 |
| F4 | The reason of an option asks for "a short explanation" (decision 0041, after the documentation advice against asking for reasoning). | `docs/diagrams/04-form-schema-draft.json`, 25; `docs/decisions/0041-...md`, 21-25; `tests/test_model_steps.py`, 148-152 | "A short explanation of why this option is correct or wrong." | 1 / 2 |
| F5 | Code checks the answer after the schema: a valid status; a `cannot_write` with a reason; a `written` with a question and a non-empty list of options. Else the call failed. | `src/step2_write.py`, 168-180 | "The answer must be a complete form. Otherwise the call failed (decision 0029, the contract)." | 1 |
| F6 | Code writes each enum value in one fixed form ("Written" becomes "written"), because structured outputs do not guarantee capitals. | `src/model_call.py`, 146-166; `docs/decisions/0041-...md`, 37 | "Structured outputs don't guarantee the capitalization of string `enum` and `const` values" | 1 / 2 |
| F7 | A form stops format errors, not content errors. The count of options and of correct answers is checked by step 3, not by the form. | `docs/decisions/0029-...md`, 122; `docs/decisions/0040-...md`, 25 | "So the design does not rely on the form for a count. The code check of step 3 checks the number of options and the number of correct answers." | 2 |
| F8 | "Cannot write": the slot opens at once, no new try; the owner decides. | `docs/decisions/0029-...md`, 99; `src/control.py`, 202-204 | "The slot gets the status `open` immediately, with no new try." | 2 / 1 |
| F9 | "Cannot write" was never used: 0 of 488 tries have `status` `cannot_write` (computed). The build guide calls the purpose an assumption. | run files; `docs/build-guide/step-2-write-the-question.md`, 13 | "The design expects that, with this answer available, the model does not invent a question for a slot that does not fit. That is an assumption, not checked." | 1 / 3 |

### 2.4 Who mixes the options and gives the letters

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| L1 | Code, not the model, mixes the options and gives the letters. The seed is the plan's seed, the slot ID and the question text, so the same answer always gets the same letters. | `src/step2_write.py`, 183-202; `docs/decisions/0041-...md`, 41 | "Code mixes the options with the seed of the plan, the slot ID and the question text. So the same answer always gets the same letters." | 1 / 2 |
| L2 | The reason: the 12 sample questions have A correct 10 times (and B 2 times). Counted again by this agent: A 10, B 2 (`correct_answer` of `reference/guide-records.json`). | `docs/decisions/0029-...md`, 126 | "in the 12 sample questions of the guide, the correct answer is A 10 times and B 2 times. A model that sees those examples can copy that. This is an assumption of the assistant. It is not checked." | 2 / 1 |
| L3 | From mock 5: the correct options take the letters that the plan sets (`correct_letters`); the wrong options take the other letters in the mixed order. | `src/step2_write.py`, 191-199; `docs/decisions/0070-...md`, 22 | "**Step 2** (and step 5) puts the correct options at the letters of the slot. The wrong options take the other letters, in the mixed order of decision 0029." | 1 / 2 |
| L4 | Mock 5: in all 101 tries, the correct letters equal the plan's `correct_letters` (computed). | run files | | 1 |
| L5 | The model never learns the letter: `correct_letters` is not in the slot that the writer sees (R9). | `src/step2_write.py`, 132-135 | | 1 |

### 2.5 Limits stated by the sources

| # | Limit | Source, lines | Exact quote | L |
|---|---|---|---|---|
| X1 | The examples have no reason for each option, so they do not show the whole form. | `docs/build-guide/step-2-write-the-question.md`, 50 | "A limit: the examples have no reason for each option, so they do not show the complete form." | 3 |
| X2 | No example of a two-answer question (all 12 samples have 4 options and 1 answer). | `docs/decisions/0029-...md`, 140 | "The writer gets no example of a multiple-response question with 5 options and 2 correct answers." | 2 |
| X3 | The writer gets only its own task statement; a wrong option often comes from another one. Call 4b has the whole guide. | `docs/decisions/0029-...md`, 125 | "A limit: a wrong option often comes from a different task statement (decision 0032), and the writer does not get those texts." | 2 |
| X4 | Two instructions have no check by any step: "the same form" for the options, and "two different parts of the point" for two-answer slots. `grep -n -i "two different\|same form" src/*.py` finds them only in `src/step2_write.py` (60, 141-142). | `docs/decisions/0054-...md`, 35; `docs/decisions/0029-...md`, 27 | "A code check of the two correct options. Only a model can judge if they are two parts or two examples." (not decided yet) | 2 / 1 |
| X5 | Plain API, not the Agent SDK; the owner's words. | `docs/decisions/0029-...md`, 131, 151 | "The owner said: \"keep the simple api\"." | 2 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-2-write-the-question.md`, lines 41-52 (L3). 10 points in 4 task statements: 4.3, 4.2, 4.1, 1.4. The page heading (`academy/pages/behind-the-mocks.html`, closed heading of `#step-2`) says "task statements 4.3, 4.2, 4.1, 1.4". Agrees. The guide texts agree with `reference/guide-records.json`.

| Point | Line | Task statement | How the step uses it (exact, from the table) |
|---|---|---|---|
| 4.3-K1 | 43 | 4.3: Enforce structured output using tool use and JSON schemas | "Written for the extraction of data. Here: the writer fills a form, so code can read each answer. The method is structured outputs (see the deviation above)." |
| 4.3-S3 | 44 | 4.3 | "Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above)." |
| 4.3-K2 | 45 | 4.3 | "The same context. It names the three settings of a tool call. The current models accept only \"auto\" and \"none\"." |
| 4.3-S4 | 46 | 4.3 | "Written for the extraction of data. Here: the question can be empty when the answer is \"cannot write\", so the model does not invent a question for a slot that does not fit." |
| 4.3-S5 | 47 | 4.3 | "Written for a schema for the extraction of data. Here: the status \"cannot_write\" is an answer for a case that does not fit." |
| 4.3-K3 | 48 | 4.3 | "Written for the extraction of data. Here: a form stops format errors, but not content errors. So step 3 checks the content." |
| 4.2-K1 | 49 | 4.2: Apply few-shot prompting to improve output consistency and quality | "Written for output in a fixed format. Here: 3 sample questions show the writer the form of a good question." |
| 4.2-S2 | 50 | 4.2 | "The same context. A limit: the examples have no reason for each option, so they do not show the complete form." |
| 4.1-K1 | 51 | 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | "Written for the review of code. Here: the writer gets exact rules, not vague ones." |
| 1.4-K2 | 52 | 1.4: Implement multi-step workflows with enforcement and handoff patterns | "Written for the workflow of an agent. Here: an instruction to the writer can fail, so each rule that the writer gets is also checked, by code or by a model." |

The deviation (build guide 29-37, L3): "The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call." / "So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`." / "The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes."

Checks of the points in other files:
- Diagram 04 popups (`docs/diagrams/04-step-2-write-the-question.html`, 166): "rules" 4.1-K1; "examples" 4.2-K1, 4.2-S2; "form" 4.3-K1, 4.3-S3, 4.3-K3; "cannot" 4.3-S4. All 7 are in the table. No point only in the diagram (academy decision 0024): no conflict. The table has 3 points that diagram 04 does not show: 4.3-K2, 4.3-S5, 1.4-K2.
- Diagram 01 (`docs/diagrams/01-pipeline-overview.html`, 141 box, 191 popup "2"): box "Exam guide: no point. Plain engineering reason."; popup "the decision of the step uses no point. Its design uses task statements 4.1, 4.2 and 4.3." See conflict C5.
- Decision 0029, "Exam guide points", 159 (L2): "4.3-K1, 4.3-S3, 4.3-K2, 4.3-S4, 4.3-S5, 4.3-K3, 4.2-K1, 4.2-S2, 4.2-S1, 4.1-K1, 1.4-K2, 1.4-K1, 1.6-K1, 1.6-S1". It has 4 points that the table does not have: 4.2-S1 (cited only for the number 3, "for a different purpose"), 1.4-K1, 1.6-K1, 1.6-S1 (cited for "the plain API, not the Agent SDK"). Not a conflict under academy decision 0024 (the table is the source); listed for the owner.
- Decision 0040, 78: "4.3-K1, 4.3-S3, 4.3-K2, 4.3-K3". Decision 0044, 57, adds 4.3-S2 for the deviation (see conflict C1). Decision 0043, 48: "1.4-K2" (the B7 story, section 5 b).
- Guide text of 4.3-S2 (`reference/guide-records.json`), not in the table: "Setting tool_choice: \"any\" to guarantee structured output when multiple extraction schemas exist and the document type is unknown".

Product facts (academy decision 0014):
- Dated copy, L1-equivalent source for the decision: `docs/sources/2026-10-07-anthropic-docs-define-tools.md`, 553-564, page "Define tools", https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, section "Controlling Claude's output", subsection "Forcing tool use", row: "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 | `any` and `tool` return a 400 error | `auto` with strict tool use to guarantee schema-valid tool inputs, or structured outputs when you need a response in a fixed JSON shape."
- Live read of the same page by this agent, 14 October 2026: the row for Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 is unchanged. The row above it changed (see conflict C3): "models with thinking on by default, such as Claude Opus 5 and Claude Haiku 5.5, accept it, but a forced call skips thinking: the response starts with the tool call and has no `thinking` block". The page now also says: "Forcing a tool also skips thinking on every model that accepts forced tool use". No dated copy of the 14 October read is saved (this agent may write only this sheet).
- `docs/sources/2026-10-07-anthropic-docs-structured-outputs.md`, 44-53, page "Structured outputs", https://platform.claude.com/docs/en/build-with-claude/structured-outputs, section "Why use structured outputs": "Structured outputs guarantee schema-compliant responses through constrained decoding". Lines 66-67: "The request carries the schema in `output_config.format` with `type: \"json_schema\"`." Line 2730 ("Invalid outputs", "Enum value casing"): "Structured outputs don't guarantee the capitalization of string `enum` and `const` values". Not read live by this agent.
- What the exam expects: the guide's answer is tool use with a JSON schema (4.3-K1) and `tool_choice` "any" or a forced tool (4.3-K2, 4.3-S2, 4.3-S3). The documentation of today says that the newest models reject `any` and `tool`, and names structured outputs or `auto` with strict tool use. Both are in the sources above; the exam guide is "Version 1.0, July 2026" (`docs/decisions/0040-...md`, 64).

## 4. Numbers, per mock, with method

### 4.1 Method

Script `count2.py` (scratchpad), run on 14 October 2026 with `python3 -I count2.py /home/triggger/ccar-f-mock-generator`. It reads with `json`: `runs/mock-0N/plan.json`, `runs/mock-0N/questions/*.json`, `runs/mock-0N/checks/<id>-step3.json` and `-step4.json`, `data/narrow-ideas.json`, and it calls `earlier.Earlier(mocks, N).on_idea(point)` of `src/earlier.py` (reads `mocks/mock-0K.*.json`, K < N). No model call.

```python
Q = [json of each runs/mock-0N/questions/*.json]
len(Q); Counter(q["request"]); Counter(q["status"]); Counter(q["model"]); Counter(q["date"])
per_slot = Counter(q["slot_id"] for q in Q)                      # tries per slot
[q for q in Q if q["request"] == 2 and q["try"] > 1]                  # new point or rewrite with a new point
t1 = [q for q in Q if q["try"] == 1]; pass3 = verdict(id, 3) == "pass"; pass34 = pass3 and verdict(id, 4) == "pass"
mock 5: sorted(o["letter"] for o in q["options"] if o["correct"]) == sorted(slot["correct_letters"])
Earlier(R + "/mocks", N).on_idea(q["point"])                           # earlier questions on the idea, built mocks today
len(q["question"].split()); len(o["text"].split())                     # words
```

Script `b8.py`: for each `runs/mock-0N/checks/*-step4.json`, the results with `rule` "B8" and a result that is not "pass"; the sample numbers named in the finding (regex `[Ss]ample question (\d+)`); and the 3 examples that the writer got, recomputed with the code of `examples()` (`random.Random("examples-%s" % slot_id).sample(pool, 3)`, pool = samples of other scenarios). `git log -L` shows that `examples()` has not changed since commit `eb05725` (7 October 2026), so the replay holds for each mock.

Usage: `runs/mock-0N/usage/run-NNN.json`, fields `calls`, `dollars` (written by `src/run.py`, 42-47, from `model_call.cost`). The usage files hold all model calls of a run (steps 2, 4, 5, 6) together. They do not separate the writer.

### 4.2 Per mock

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Method |
|---|---|---|---|---|---|---|
| Tries (question records) = successful writer calls | 83 | 92 | 101 | 111 | 101 | count files in `questions/` (total 488) |
| Requests of step 2 / step 5 | 65 / 18 | 60 / 32 | 61 / 40 | 61 / 50 | 64 / 37 | field `request` |
| Step 2 requests that are not a first try (new point, or rewrite with a new point) | 5 (M1-S09-T2, S24-T3, S28-T2, S38-T2, S60-T2) | 0 | 1 (M3-S01-T4) | 1 (M4-S23-T4) | 4 (M5-S28-T4, S29-T4, S39-T4, S60-T4) | `request` == 2 and `try` > 1 |
| Status `cannot_write` | 0 | 0 | 0 | 0 | 0 | field `status` |
| Model in the records | claude-opus-5-5 (83) | (92) | (101) | (111) | (101) | field `model` |
| Slots with 1 try | 42 | 33 | 32 | 31 | 39 | Counter of `slot_id` |
| Most tries for one slot | 6 | 3 | 6 | 7 | 6 | max of the same |
| First tries (T1) that passed step 3 | 60 of 60 | 59 | 58 | 58 | 57 | `checks/<id>-step3.json` verdict |
| First tries that passed steps 3 and 4 | 49 of 60 | 46 | 34 | 33 | 40 | both verdicts "pass" |
| Tries on a two-answer slot | 14 | 13 | 16 | 21 | 17 | field `select` == 2 |
| Tries whose idea is in an earlier built mock (with today's `mocks/`) | 0 | 35 (but see note a) | 93 of 101 | 111 of 111 | 101 of 101 | `Earlier.on_idea(point)` not empty |
| Earlier questions shown for such a try: mean / max | | 1.69 / 4 | 1.38 / 5 | 1.90 / 6 | 2.88 / 7 | length of `on_idea` |
| ... of them on a narrow idea (today's list of 63) | | 18 | 59 | 72 | 52 | group in `data/narrow-ideas.json` (see note b) |
| Words of a question: min / mean / max | 48 / 61.7 / 85 | 46 / 64.7 / 90 | 44 / 67.2 / 89 | 52 / 73.0 / 91 | 46 / 75.1 / 103 | words of `question`, written tries (rule A6: 25 to 110) |
| Words of an option: min / max | 12 / 28 | 15 / 34 | 16 / 35 | 12 / 33 | 16 / 34 | (rule A6: 5 to 45) |
| B8 results that are not "pass" | 0 (no rule yet) | 2 | 0 | 1 | 1 | `b8.py` |
| Mock 5: tries whose correct letters equal the plan | | | | | 101 of 101 | compare per try |
| All model calls of the mock (all steps) | 265 | 290 | 313 | 337 | 295 | sum of `calls` in `usage/*.json` |
| Dollars of the mock (all steps) | 17.17 | 20.73 | 23.85 | 12.83 | 11.68 | sum of `dollars` |
| Usage files | run-002, 004, 005 | run-001, 002 | run-001, 003, 004 | run-001 to 004 | run-002 to 006 | `ls usage` |

Notes:
- a. Mock 2: decision 0056 was committed at 20:22 on 8 October 2026 (`ab70bd4`). Mock 2 run 1 (commit `d3a8cef`, 16:56) added 75 tries with no earlier questions. Run 2 (commit `f5d89c0`, 20:36, "14 rewrites under decision 0056") added 17 tries; 15 of them have earlier questions on the idea (computed with `git show --name-only --diff-filter=A f5d89c0`). Mocks 3 to 5 ran after `ab70bd4`. The rule text of 0056 was used for mock 3; the stricter text of 0066 (`b3c46ec`, 9 October 10:29) for mocks 4 and 5 (`git show ab70bd4:src/step2_write.py`, lines 84-86).
- b. The narrow list grew while mocks 4 and 5 ran: 20 groups (`310ea19`, 10:49), 23 (`ea2529a`, 12:48), 24 (`5aaca92`, 12:57), 62 (`74c0047`, 17:30), 63 (`c14e096`, 19:22), all 9 October 2026 (`git show <commit>:data/narrow-ideas.json`). Mock 4 run commits: 12:16, 12:55, 13:00; mock 5 run commits from 17:33. The "narrow" row above uses today's list of 63, not the list of each run.
- c. Words of a question grew from mean 61.7 (mock 1) to 75.1 (mock 5). No source gives a cause.
- d. The B8 failures, with the 3 examples of the writer (b8.py): M2-S25-T1 copied sample 9, and sample 9 was one of its examples (4, 9, 10). M2-S35-T2 (sample 5; examples 1, 3, 9), M4-S23-T2 (sample 2; examples 3, 5, 10), M5-S53-T1 (sample 2; examples 4, 6, 8): the copied sample was not an example. So 1 of 4.
- e. "First tries that passed steps 3 and 4" mixes the writer with the rules of each mock (B9 stricter from mock 4). It is not a measure of the writer alone.

### 4.3 The writer alone: the test of 7 October 2026

| Number | Value | Source |
|---|---|---|
| Writer calls of part 1 | 10, one for each of 10 slots of the plan of mock 1, no new try | `runs/test-0024/part1.json`, field `cost`; `docs/decisions/0042-...md`, 21 |
| Tokens and cost of part 1 (writer only, no cache, before rules B7 to B9 and A12) | 37,854 input, 14,248 output, $0.44 | `runs/test-0024/part1.json` `cost` |
| Per writer call (computed: divide by 10) | about 3,785 input and 1,425 output tokens, $0.044 | same |
| Step 3 result | 10 of 10 "pass" (T-M1-S01 to S07, S16, S31, S46) | `part1.json`, `questions[*].step3.verdict` |
| Owner marks | 9 good, 1 bad (T-M1-S05) | `docs/decisions/0042-...md`, 40; build guide, 27 |
| Part 4: the writer made more questions of scenario 3 | 9 calls, $0.40 (the file holds 15 questions of the scenario) | `runs/test-0024/part4.json` `cost` |

This is the only place where the writer's tokens and dollars are separate from the checks.

### 4.4 Fixed numbers

| Number | Meaning | Source | How a script reads it |
|---|---|---|---|
| 21 | rules in the list (A1-A12, B1-B9) | `src/step2_write.py`, 31-63 | lines of `RULES` that match `^[AB]\d+\.` |
| 3 | sample questions as examples | `src/step2_write.py`, 70 | `def examples(records, slot, count=3)` |
| 12 | sample questions in the guide | `reference/guide-records.json` | `len(sample_questions)` |
| 10 / 2 | correct letter A / B in the 12 samples | same | Counter of `correct_answer` |
| 14 | technologies of Section 17 | same | `len(section_17["technologies"])` |
| 63 of 95 | narrow ideas | `data/narrow-ideas.json` | `len(groups)`; the file's `status`: "decisions 0066, 0068, 0072 and 0075" |
| 3 | runs of a failed call | `src/control.py`, 30 | regex `^CALL_RUNS = (\d+)` |
| 64000 | `max_tokens` | `src/model_call.py`, 26 | regex `^MAX_TOKENS = (\d+)` |
| "high" | effort | `src/model_call.py`, 23 | regex `^EFFORT = "(\w+)"` |
| 4.0 / 20.0 | dollars per million input / output tokens (Claude Opus 5.5, read 7 October 2026) | `src/model_call.py`, 28 | regex `^PRICE = (.*)` |
| 1.25 / 0.05 | cache write / cache read factors (read 9 October 2026) | `src/model_call.py`, 32-33 | regex `^CACHE_WRITE = `, `^CACHE_READ = ` |
| 3077 / 2788 | characters of the strict / narrow list of rules | `src/step2_write.py` | `len(RULES)`, `len(rules_for({"narrow": True}))` |
| about 800 tokens | the writer's rules, stated by decision 0067 | `docs/decisions/0067-...md`, 25 | "the writer's rules (about 800 tokens) are above it" (512-token minimum). Not counted again: no tokenizer without a model call. |

## 5. Stories for the Depth

Sources searched: decisions 0010, 0029, 0030 (status), 0037 (items 5, 11, 12), 0040 to 0045, 0053 to 0056, 0062, 0066 to 0068, 0070, 0072, 0074, 0075; `docs/journal.md` (grep "writer", "forced tool", "structured output", "cannot write", "usage limit", "sample question"); `docs/reviews/` (grep "the writer"); `HANDOFF.md`; diagrams 04, 11; `docs/sources/`. Six stories found. Story (a) is the strongest: it starts with a real repeat in a built mock, shows the real records, and ends with code, a test and the rule in two steps. Note: the caching story (mock decision 0067) belongs to step 4 (academy decision 0010); section (f) lists only what is specific to the writer.

### Story (a): the writer did not know the earlier mocks, so it wrote the same question again

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | Mock 2 had 17 repeats of mock 1. | `docs/decisions/0056-...md`, Question, 10 | "17 questions of mock 2 repeat mock 1: 13 strong (the same scene, the same answer and the same wrong options) and 4 close." | 2 |
| A2 | The writer's part of the cause. | `docs/decisions/0056-...md`, Reason, 30 | "In mock 2, the writer did not know mock 1. On a shared idea it wrote the most obvious scene again, often with the same wrong options." | 2 |
| A3 | The earlier question (built, mock 1), M1-S28-T2, point 1.1-S1: "Your support agent's loop code sends one request to Claude, runs the tool that Claude requests, and then replies to the customer. ..." Correct D: "Check stop_reason after each response, execute the requested tools and send their results back while it is \"tool_use\", and end the loop when it is \"end_turn\"." Wrong: a phrase match (A), "text means Claude has finished" (B), "exactly five iterations" (C). | `mocks/mock-01.questions.json`, `mocks/mock-01.answers.json` | | 1 |
| A4 | The repeat, M2-S08-T1, point 1.1-S3, request 2, 8 October 2026: "Your coordinator agent's loop ends whenever a response from Claude contains any assistant text. ..." Correct C: "Continue the loop while stop_reason is \"tool_use\" and end the loop only when stop_reason is \"end_turn\"." Wrong: long text as the final answer (A), "a fixed cap of 15 iterations" (B), a completion phrase (D). | `runs/mock-02/questions/M2-S08-T1.json` | | 1 |
| A5 | Both are in one idea: 1.1-S1 and 1.1-S3 are both in group G001 (`point_groups.group_of`, computed). G001 is a narrow idea today (it was on the first list of 20). | `docs/diagrams/11-make-diagram.py`, 25-26; `data/narrow-ideas.json`; `docs/decisions/0066-...md` (table, G001) | `GROUP = G['1.1-S3']` | 1 / 3 |
| A6 | The owner's rewrite. | `runs/mock-02/owner-decisions.json`, D001 | "Repeat of M1-S28 of mock 1 (decision 0056): the same scene, the same answer and the same wrong options. Write a new question on the same point. Use a different scene and a different angle: the cause, the fix, or a choice between rules. Do not use a wrong option of the earlier question." | 1 |
| A7 | The new try, M2-S08-T2 (request 5, shown M2-S08-T1): it asks for the cause. "...the logs show that the loop exited right after the 12th response from Claude. That response had stop_reason \"tool_use\" ... What is the most likely cause of this failure?" Correct B: "The loop uses a fixed cap of 12 iterations as its main stopping rule, so it exits even while Claude is still requesting tools." B9 in call 4b: "pass". | `runs/mock-02/questions/M2-S08-T2.json`; `runs/mock-02/checks/M2-S08-T2-step4.json` | | 1 |
| A8 | The fix for step 2: the writer gets the earlier questions on the idea, with the marks, and an instruction. | `docs/decisions/0056-...md`, 22; `src/earlier.py`, 1-7, 55-58; `src/step2_write.py`, 89-106, 137-139 | "When the idea of a slot is in an earlier mock, the writer gets the earlier questions on that idea, with the mark of each option" | 2 / 1 |
| A9 | The owner changed the first suggestion. | `docs/decisions/0056-...md`, Reason, 32 | "The owner changed the first suggestion of the assistant: the writer must use a different scene and a different angle, not a different correct action, because some ideas have only one correct action. The wrong options must never be the same." | 2 |
| A10 | An instruction alone was not enough: step 4 got rule B9 to check it. | `docs/decisions/0056-...md`, 23 | "**Step 4.** New rule B9 in call 4b" | 2 |
| A11 | Mock 3, with the writer seeing earlier questions, still had about 26 questions with the same problem in another setting. | `docs/decisions/0062-...md`, Question, 10 | "About 26 questions have the same problem and the same answer as an earlier question, in another setting. Rule B9 should fail these, but the model judged a new setting as a new scene." | 2 |
| A12 | The stricter text for the writer (mocks 4 and 5). | `docs/decisions/0066-...md`, 22; `src/step2_write.py`, 89-93 | "Write a question with a different problem, also if you change the setting: a different thing goes wrong, or the team must make a different choice." | 2 / 1 |
| A13 | The owner's change on the wrong options, and the reason. | `docs/decisions/0066-...md`, Reason, 60 | "\"No wrong option of an earlier question\" became \"Not the same set of wrong options. At most one wrong option may repeat.\" The reason of the owner: the standard mistakes that the guide names make the strongest wrong options, and the owner wants harder questions in mocks 4 and 5." | 2 |
| A14 | The exception: a narrow idea keeps the copy rule (20 groups first, 63 today). | `docs/decisions/0066-...md`, 26; `docs/decisions/0068-...md`, 10; `docs/decisions/0072-...md`; `docs/decisions/0075-...md` | "For an idea on the list `data/narrow-ideas.json`, the copy rule stays" | 2 |
| A15 | Why the list grew: in mock 4, slots failed the stricter rule three times on ideas with one problem. | `docs/decisions/0068-...md`, 10 | "In mock 4, three slots failed the stricter rule B9 three times, each time on the same problem as an earlier question" | 2 |
| A16 | Run files: the share of tries with earlier questions grew from 0 (mock 1) to 101 of 101 (mock 5), and the mean number shown from 1.38 (mock 3) to 2.88 (mock 5) (section 4.2). | run files | | 1 (computed) |
| A17 | Tests: the writer gets the earlier questions and the rule; no earlier question gives no section; the narrow idea gets the copy rule. | `tests/test_earlier.py`, 90, 101, 136 | `def test_the_writer_gets_the_earlier_questions_and_the_rule(self):` | 1 |
| A18 | Open limit. | `docs/decisions/0066-...md`, 52 | "So the rule is a judgment, and it will sometimes fail a good question or pass a close one." | 2 |

### Story (b): the first bad mark became a writer instruction and a check (1.4-K2)

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | In the writer test, the owner marked T-M1-S05 bad (owner's words, typo kept). | `docs/decisions/0043-...md`, Question, 10 | "The question is confusing and needs calrification. I had to read the question more than one time. Use one name for the actor, not 'the subagent' and 'Claude'. Make the sentences shorter." | 2 |
| B2 | The test result: 10 of 10 passed step 3; owner marked 9 good, 1 bad. | `runs/test-0024/part1.json`; `docs/build-guide/step-2-write-the-question.md`, 27 | "The bad mark said that the question used two names for one actor and was hard to read. That mark gave a new instruction to the writer and a new rule for the checker (rule B7, see step 4)." | 1 / 3 |
| B3 | The assistant first recommended an instruction only; the owner asked if that is enough. | `docs/decisions/0043-...md`, How we decided, 42; Reason, 30 | "The owner asked: \"but is that enough? Only in the prompt?\" An instruction alone fails sometimes, so a check comes after it." | 2 |
| B4 | A measure showed length was not the cause. | `docs/decisions/0043-...md`, 31 | "So a limit from the sample questions does not catch T-M1-S05." / "The defect is clarity, not length, and clarity needs judgment." | 2 |
| B5 | The fix: the writer instruction and rule B7. | `docs/decisions/0043-...md`, 22-23; `src/step2_write.py`, 55, 61 | "Use one name for one actor. Write each sentence so that a reader understands it at the first reading." | 2 / 1 |
| B6 | The check of B7 found the same defect in 3 of the 9 good questions. | `docs/decisions/0043-...md`, 38 | "It also failed 3 of the 9 questions that the owner marked good, each with a true finding: two names for one actor." | 2 |
| B7 | The owner's words for the decision. | `docs/decisions/0043-...md`, 42 | "The owner said: \"Yes, add both\"." | 2 |
| B8 | This is the guide point 1.4-K2 of the build guide table (section 3); decision 0044 limits it to its general idea. | `docs/decisions/0044-...md`, 43 (item 10) | "Decision 0043 uses only its general idea: an instruction alone can fail. The clarity of a question is a different context." | 2 |

### Story (c): the design forced a tool call; the newest models reject it, so the form goes as structured outputs

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| C-1 | The confirmed design of 0029 forced a tool call. | `docs/decisions/0029-...md`, 53 | "The form is a JSON schema of a tool, and the request forces the model to call that tool." | 2 |
| C-2 | 0029 left the parameter names unchecked for the code stage. | `docs/decisions/0029-...md`, 153 | "Product facts that the assistant did not check: the exact names of the API parameters that force the form. That check belongs to the code stage." | 2 |
| C-3 | How it was found: before writing code, from the Claude API skill, then the documentation. | `docs/decisions/0040-...md`, How we decided, 72 | "The assistant read the skill of the Claude API before it wrote the code of the model steps. The skill said that the current models reject a forced tool call. Rule 9 asks for a check in the documentation, so the assistant read the page \"Define tools\"." | 2 |
| C-4 | The owner's question and request. | `docs/decisions/0040-...md`, 72 | "The owner asked if a model that supports a forced tool call is better. The assistant recommended against it ... The owner agreed, and asked that the deviation is shown openly, with the page and the section." | 2 |
| C-5 | The three options and the choice. | `docs/decisions/0040-...md`, 14-16, 20 | "Option 2. Steps 2, 4 and 6 (and step 5, which uses the request of step 2) send their form as a JSON schema in `output_config.format`." | 2 |
| C-6 | Why not an older model; why not `auto`. | `docs/decisions/0040-...md`, Reason, 62-63 | "A forced tool call would fix the model now." / "With `auto`, the model can answer with text and not call the tool. Then code must run the call again." | 2 |
| C-7 | The code never had a forced tool call: the first build of the model steps (`eb05725`, 7 October 2026) already sends `output_config` (`git show eb05725:src/model_call.py`, line 80). So nothing failed in a run; the error was in the design text. | git history | `output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}})` | 1 |
| C-8 | Two more fixes from the documentation for the same form: enum capitals (F6) and "a short explanation" in place of reasoning (F4). | `docs/decisions/0041-...md`, 21-25, 37 | "A parameter that asks for the model's thinking or step-by-step reasoning may lead to a `reasoning_extraction` refusal." | 2 |
| C-9 | A correction of the deviation text (see conflict C1). | `docs/decisions/0044-...md`, 25 | "\"The exam guide teaches a forced tool call for a fixed form\" is too strong." | 2 |
| C-10 | Test: no `tools` and no `tool_choice` in the request. | `tests/test_model_steps.py`, 105-112 | `def test_the_form_is_sent_as_structured_outputs_with_no_tool(self):` | 1 |

### Story (d): the few-shot examples, and a cause that was half true

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| D1 | The second review of mock 1 named a cause. | `docs/reviews/M1-round1-second-review-notes.md`, "The probable causes", 86, 89 | "**The writer got sample question 1 as an example and copied its structure** (S13 and S30)." / "These causes are the opinion of the assistant." | 4 |
| D2 | The journal checked it for S30 only. | `docs/journal.md`, 144 | "False as written: the writer of S30 did not get sample question 1 as an example. The probable cause is the point 1.4-K2 itself." | 4 |
| D3 | Replay of `examples()` (unchanged since `eb05725`): M1-S30 (scenario 1, point 1.4-K2) got samples 8, 10, 12. M1-S13 (scenario 3, point 1.4-S1) got samples 1, 4 and 12: it did see sample 1. So the review was right for S13 and wrong for S30. | `src/step2_write.py`, 70-86; `runs/mock-01/plan.json`; scratchpad `ex2.py` | | 1 (computed) |
| D4 | The two texts: sample 1, "Production data shows that in 12% of cases, your agent skips get_customer entirely and calls lookup_order ..."; M1-S13-T1, "Logs show that in 8% of runs, the coordinator agent skips verify_citations and calls generate_report directly ...". | `reference/guide-records.json` sample 1; `mocks/mock-01.questions.json` M1-S13-T1 | | 1 |
| D5 | The writer cannot copy the scene of an example from its own scenario: the examples come from other scenarios. Sample 1 is scenario 1; M1-S13 is scenario 3. | `docs/decisions/0029-...md`, 123; diagram 04 popup "examples" | "The plain reason for \"not from the scenario of the slot\": the writer must not copy the scene of an example." | 2 / 3 |
| D6 | Copies of samples that the writer never saw also happened: M1-S30 (sample 1) and M1-S60-T2 (sample 12; its examples were 2, 4, 8). | `docs/decisions/0055-...md`, 10; replay | "In mock 1, M1-S30 was a close copy of sample question 1, and M1-S60-T2 was a close copy of sample question 12." | 2 / 1 |
| D7 | The fix: rule B8, in the writer's list and checked by call 4b. A code check of word overlap failed. | `docs/decisions/0055-...md`, 21, 23, 29 | "A copy keeps the scene and the correct action, but it changes the words. So code does not find it, and a model must judge it." | 2 |
| D8 | After B8: 4 B8 failures in mocks 2 to 5; in 1 of them (M2-S25-T1, sample 9) the copied sample was one of the writer's 3 examples (section 4.2, note d). | `b8.py` | | 1 (computed) |
| D9 | Open item. | `docs/decisions/0055-...md`, 35 | "If the writer also gets the rule to use a different scene than the 3 sample questions that it sees as examples." | 2 |

### Story (e): patterns over 60 questions that one writer call cannot see

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| P1 | Letters: mock 4 had D correct 22 times of 52. Code now places the correct options at the plan's letters (mock 5). | `docs/decisions/0070-...md`, 10, 22 | "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. Chance is 13." | 2 |
| P2 | Mock 5: 101 of 101 tries have the plan's letters (L4). | run files | | 1 (computed) |
| P3 | Longest option: mock 1, 37 of 52. The writer gets rule A12 and the slot field; step 3 checks it. | `docs/decisions/0053-...md`, 10, 22 | "**Step 2.** The writer gets the field in the slot, and a new rule in its list" | 2 |
| P4 | Two-answer slots: mock 1 had two examples of one idea. The writer gets an instruction, with no check (X4). | `docs/decisions/0054-...md`, 10, 24, 35 | "In mock 1, the two correct options of M1-S17, M1-S35 and M1-S47 were two examples of one idea." | 2 |
| P5 | The test of 7 October already showed the cost of O5: in part 4, step 6 found "one more pair with the same scene, and four pairs that give away an answer (D4)" among the writer's questions of scenario 3. | `docs/journal.md`, 199 | "Step 6 also found real problems of the writer" | 4 |

These are step 1 and step 3 stories as much as step 2 stories (the plan sets the fields, code checks A12). Step 1's sheet (`academy/facts/step-1.md`, story e) already has P1, P3, P4.

### (f) Caching: what is specific to the writer (the story itself is for step 4)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| K1 | The writer sends its rules first as a cached block; a narrow idea has its own list and cache. | `docs/decisions/0067-...md`, 23; `src/step2_write.py`, 218-220 | "**The writer** sends its list of rules as a cached block first." | 2 / 1 |
| K2 | The writer's block is about 800 tokens, above the 512-token minimum. | `docs/decisions/0067-...md`, 25 | "the writer's rules (about 800 tokens) are above it" | 2 |
| K3 | The measured saving (66%) is for calls 4a and 4b only. `src/test_cache.py` checks 10 questions with calls 4a and 4b; it does not call the writer. | `docs/decisions/0067-...md`, 31 | "calls 4a and 4b checked 10 questions of mock 3 again" | 2 / 1 |
| K4 | The test that the cached blocks are identical covers calls 4a and 4b, not the writer. No test checks the writer's `cached` text across calls. | `tests/test_model_steps.py`, 287-300; `docs/decisions/0067-...md`, 27 | "A test checks that the cached blocks are identical in each call, for each scenario." | 1 / 2 |

No "what went wrong" story is specific to the writer's cache.

### Smaller items (for the Explanation, not stories)

- "Cannot write" was never used in 488 tries (F9). The open item of decision 0027 (a task statement that is a bad fit) was the reason for it (`docs/decisions/0029-...md`, 121: "This is the answer of step 2 to the open item of decision 0027"). No source says if the writer ever wrote a question that did not fit. (L1, L2)
- The design history of step 2: the owner rejected the first proposal as not specific, and step 0 was designed first (`docs/decisions/0029-...md`, 145; `docs/journal.md`, 276: "The owner said that it was not specific: no source for the story of the scenario, no records for code, no output format, no fields. The owner was right."). (L2, L4)
- The owner asked why a subagent in the same call does not review the output (`docs/decisions/0029-...md`, 151). The answer leads to step 4.
- Decision 0074 (the owner's reason reaches the writer after "more tries") belongs to step 5 (`academy/facts/step-5.md`).

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step2_write.py` | 1-7 | The docstring: one file for steps 2 and 5. |
| `src/step2_write.py` | 31-63 | The 21 rules as the writer gets them (long; lines 33-45 for group A, 47-57 for group B). |
| `src/step2_write.py` | 26, 28-30 | B9 strict and B9 copy. |
| `src/step2_write.py` | 65-67 | The system text. |
| `src/step2_write.py` | 70-86 | `examples()`: 3 samples from other scenarios, letters removed. |
| `src/step2_write.py` | 89-99 | The two instructions for earlier questions (strict and narrow). |
| `src/step2_write.py` | 114-142 | `request_text()`: the order of the parts. |
| `src/step2_write.py` | 168-180 | `check_answer()`: the contract after the schema. |
| `src/step2_write.py` | 183-202 | `give_letters()`: code mixes; the plan's letters from mock 5. |
| `src/step2_write.py` | 213-227 | `Writer.write()`: earlier questions, narrow, the call with the cached rules. |
| `src/model_call.py` | 108-120 | `ask()`: cached system blocks, `output_config` with effort and `json_schema`, streaming. |
| `src/model_call.py` | 57-72 | `strict()`: `additionalProperties: false`. |
| `src/model_call.py` | 150-166 | `lower_enums()` with the documentation quote. |
| `src/model_call.py` | 20-26 | The model and effort: "first values, not decisions". |
| `docs/diagrams/04-form-schema-draft.json` | 1-38 | The form. |
| `src/earlier.py` | 55-58 | `on_idea()`: earlier questions of the same group. |
| `src/control.py` | 229-239 | The plain request of step 2. |
| `src/control.py` | 378-392 | `_save_try()`: one file for each try. |
| `tests/test_model_steps.py` | 105-112 | No tool, no `tool_choice`. |
| `tests/test_model_steps.py` | 184-198 | The correct option gets the plan's letter. |
| `tests/test_model_steps.py` | 200-209 | 3 examples from other scenarios, no letters. |
| `tests/test_earlier.py` | 90-99 | The writer gets M1-S28-T2 and the rule. |
| `runs/mock-02/questions/M2-S08-T1.json`, `-T2.json` | whole | The repeat and the new try (story a). |
| `runs/test-0024/part1.json` | `cost` | The writer's own cost (section 4.3). |
| `git show eb05725:src/model_call.py` | 80 | Structured outputs from the first build (C-7). |

## 7. A figure

Diagram 04 (`docs/diagrams/04-step-2-write-the-question.html`) is the base: panel 1 "Code builds the request, and the model fills the form" (7 inputs, the writer, two answers), panel 2 "Code completes the record of the question" (letters, IDs, one file). A figure of the mechanism, suggested in boxes and arrows:

```
[plan.json: one slot] [guide records] [built mocks 1..N-1] [narrow list]
        \                 |                 | "finds questions on the same idea"
         v                v                 v
   [Code: builds the request]
        system:  [rules A1-A12, B1-B9 | cached] [role + form description]
        user:    [3 samples, other scenarios, no letters] [story] [task statement, point >>>]
                 [14 technologies] [slot] (+ earlier questions + rule) (+ two-answer line)
        output_config: [form as JSON schema]  -- no tool, no tool_choice --
        |  "one call, new each time"
        v
   [Claude: fills the form]  --"written"--> [question + options, each correct/wrong + reason, no letters]
                             --"cannot write"--> [reason] --> [slot open: the owner decides]
        |  "checks the form; else runs the call again, at most 3 times"
        v
   [Code: mixes options, gives letters (plan's letters from mock 5)] --> [adds IDs] --> [saves M?-S??-T?.json] --> [step 3]
```

Facts behind the labels: inputs E4, R9; "finds questions on the same idea" A8, `src/earlier.py`; "cached" R1, K1; role R4; samples R5; story, task statement, technologies R6-R8; earlier questions R10; two-answer line R11; form F1-F3; "no tool, no tool_choice" R13, C-10; "one call, new each time" O1; "written" / "cannot write" F1, F8; "slot open" F8; "checks the form ... 3 times" F5, E5; "mixes, gives letters" L1, L3; "adds IDs, saves" E8; "step 3" diagram 04 popup "save".

A second, small figure for the Depth (story a): M1-S28-T2 against M2-S08-T1 (same scene, same answer, same wrong options) and M2-S08-T2 (the cause, B9 pass). Diagram 11 already draws it from the real files (`docs/diagrams/11-make-diagram.py`, 19-24).

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| C1 | What the guide teaches for a fixed form. | `docs/build-guide/step-2-write-the-question.md`, 31 (L3): "The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below)." Diagram 04 popup "form" (L3): "The guide teaches a forced tool call for this (4.3-S3, below)." | `docs/decisions/0044-...md`, 25 (L2, later than 0040): "\"The exam guide teaches a forced tool call for a fixed form\" is too strong. Point 4.3-S3 forces one tool so that one extraction runs before the others. A different point uses a tool call to get structured output: \"Setting tool_choice: \"any\" to guarantee structured output when multiple extraction schemas exist and the document type is unknown\" (4.3-S2...)." 4.3-S2 is not in the build guide table. |
| C2 | Context of 4.3-K1. | Build guide, 43 (L3): "Written for the extraction of data." | `docs/decisions/0044-...md`, 26 (L2): "Point 4.3-K1 is a general point of task statement 4.3, \"Enforce structured output using tool use and JSON schemas\"." |
| C3 | Which models accept a forced tool call. | Build guide, 33 (L3): "An older model, Claude Opus 5, still accepts a forced tool call". Build guide, 45 (L3, 4.3-K2 row): "The current models accept only \"auto\" and \"none\"." Dated copy `docs/sources/2026-10-07-...define-tools.md`, 563: "(Claude Opus 5 supports it with thinking on)". | Live page "Define tools", read 14 October 2026 (Docs): "models with thinking on by default, such as Claude Opus 5 and Claude Haiku 5.5, accept it, but a forced call skips thinking". Claude Haiku 5.5 is also a model that accepts it, so "the current models accept only auto and none" is true only for the four models of the row. |
| C4 | Status line of decision 0029. | `docs/decisions/0029-...md`, 4 (L2): "Status: accepted". Its part 3, 53: "the request forces the model to call that tool." | `docs/decisions/0040-...md`, 27-29 (L2, later) replaces that sentence. The status line of 0029 does not name 0040, 0041 or 0044. (Compare 0030, whose status line names its later decisions.) |
| C5 | Task statements of step 2 in diagram 01. | `docs/diagrams/01-pipeline-overview.html`, 141 (L3), box: "Exam guide: no point. Plain engineering reason." Line 191, popup "2": "Its design uses task statements 4.1, 4.2 and 4.3." | Build guide table, 41-52 (L3): 4.3, 4.2, 4.1 and 1.4 (point 1.4-K2). The page heading also has 1.4. Already listed as X8 in `academy/facts/top-of-tab-2.md`. |
| C6 | How many writer instructions have no check. | Diagram 04 popup "rules" (L3): "One instruction has no rule of its own: the options of a question have the same form." Build guide, 52 (L3, 1.4-K2): "each rule that the writer gets is also checked, by code or by a model." | `src/step2_write.py`, 140-142 (L1) and `docs/decisions/0054-...md`, 35 (L2): the two-answer instruction ("two different parts of the point") also has no rule and no check ("A code check of the two correct options" is not decided). The build guide sentence holds for the 21 rules, not for the two instructions. |
| C7 | Did the writer copy sample question 1? | `docs/reviews/M1-round1-second-review-notes.md`, 86 (L4): "The writer got sample question 1 as an example and copied its structure (S13 and S30)." | `docs/journal.md`, 144 (L4): "False as written: the writer of S30 did not get sample question 1 as an example." Replay (L1, computed, D3): S30 did not get it; S13 did (samples 1, 4, 12). Both L4 sources are half right. |
| C8 | Diagram 04 popup "examples" (L3): "So the writer cannot copy the scene of an example." | | Run files (L1): M2-S25-T1 failed B8 as a copy of sample 9, which was one of its 3 examples (D8). The sentence is true for the scene of the slot's own scenario only; a sample of another scenario can still be copied. A difference of scope, for the owner. |
| C9 | Decisions of step 2 in `HANDOFF.md`. | `HANDOFF.md`, 79 (L4): "0029, 0053 to 0056, 0066, 0067, 0068, 0070, 0072, 0075". | Code and decisions (L1, L2): the step also rests on 0010, 0040, 0041, 0043 and 0044 (`src/step2_write.py`, 1; `src/model_call.py`, 1). A gap in a list, not a disagreement of fact. |
| C10 | Exam guide points of the step. | `docs/decisions/0029-...md`, 159 (L2): also 4.2-S1, 1.4-K1, 1.6-K1, 1.6-S1. | Build guide table (L3): not these four. Academy decision 0024 makes the table the source; listed so the owner knows. |

## 9. Not found

1. The writer's own share of tokens and dollars in mocks 1 to 5. The usage files hold all calls of a run together (section 4.1). Only the test of 7 October 2026 separates the writer (section 4.3).
2. A measured saving of the cache for the writer. `src/test_cache.py` measures calls 4a and 4b only (K3). The token size of the writer's rules (about 800) is stated by decision 0067 and not counted again (no tokenizer without a model call).
3. The request text that each try got. The question record does not save it (E10). The parts can be rebuilt by code, but the earlier questions and the narrow list depend on the time of the run (section 4.2, notes a and b).
4. Which narrow list each run of mocks 4 and 5 used. Commit times give an order, not the run times.
5. Any case where the writer answered "cannot write" (0 of 488), or any source that says the writer forced a question into a slot that did not fit.
6. Any test or check of the instructions "the same form" and "two different parts of the point" (X4).
7. A test that the writer's cached block is the same in each call (K4).
8. A dated copy of the live read of the page "Define tools" (14 October 2026). This agent may write only this sheet. The 7 October copy is in `docs/sources/`.
9. A cause for the growth of the question length from mock 1 to mock 5 (section 4.2, note c).
10. No failure of step 2 in a real run of the program: no error record in any mock (E7). Each story is a failure that the questions showed (repeats, copies, unclear text, patterns) or a design error found before the code ran (story c).
