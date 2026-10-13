# Fact sheet: tab 2, step 4 "Check by a model"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `7c4604a` (branch `main`). Other agents had uncommitted changes in `academy/` at the time. No source file of this sheet was among them.
- Levels of trust (academy decision 0011): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = Anthropic documentation (academy decision 0014). "L" = level. "1 (computed)" = a number that this agent computed from level-1 files by script.
- The tests ran on 14 October 2026 with no API key in the environment: `env -u ANTHROPIC_API_KEY python3 -m unittest discover -s tests` gives "Ran 228 tests" and "OK". No model call was made. No script in `src/` that calls the API was run.
- Files that this agent did not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, and all personal files of the owner.
- Academy decision 0030 asks the fact agent to save a dated copy of each documentation page in `academy/sources/`. This agent was told to change no file except this sheet. So the live page "Prompt caching" (read 14 October 2026) has no saved copy. See section 9, item 1.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | Some rules need judgment, so a model checks them. The step has two calls, and code sits between them. | `docs/build-guide/step-4-check-by-a-model.md`, 9 | "Some rules need judgment, so a model checks them. The step has two calls, and code sits between them." | 3 |
| O2 | Code, not a model, makes the verdict. | `src/step4_check_model.py`, 3-8 | "Code checks each answer, searches the feature names in the records file, and makes the verdict. A model does not make the verdict." | 1 |
| O3 | Call 4a answers the question with no answer key. Call 4b checks rules B1 to B9 with the answer key. | `src/step4_check_model.py`, 3-6 | "Call 4a answers the question with no marks and no reasons. Call 4b checks the rules B1 to B9 with the complete record" | 1 |
| O4 | The step gets one question that passed step 3. Fail and cannot decide go to step 5. | `src/control.py`, 206-213, 371-376; `docs/build-guide/step-4-check-by-a-model.md`, 17 | "A question that fails, or that the checker cannot decide, goes to step 5 with its findings." | 1 / 3 |
| O5 | Why a new call: the guide says that a model that wrote a thing is less likely to question it. | `docs/decisions/0012-...md`, 20, 24 | "For each question that passed step 3, a new API call checks the question against the rules that need judgment." / "The call receives the question and the text of the guide. It does not receive the notes or the reasoning of the writer. The call is not a subagent." | 2 |
| O6 | Status: built. It ran in the test of 7 October 2026 and for mocks 1 to 5, 7 to 9 October 2026. | `docs/build-guide/step-4-check-by-a-model.md`, 3; run files: field `date` of `runs/mock-0N/checks/*-step4.json` is 2026-10-07 to 2026-10-09 | "Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026." | 3 / 1 |
| O7 | The model of each step 4 check in mocks 1 to 5 is `claude-opus-5-5` (477 of 477 records). | `src/model_call.py`, 22; field `model` of each `runs/mock-0N/checks/*-step4.json` | `MODEL = "claude-opus-5-5"` | 1 (computed) |

## 2. Explanation facts: the mechanism

### 2.1 Call 4a, the blind answer

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | Input, user text: the story of the scenario, then the question with the line "Select N." and the options. No marks, no reasons. | `src/step4_check_model.py`, 148; 38-46 | `text = "\n".join([story_text(...), "", "THE QUESTION:", show(question, with_key=False)])` / "With no key: the question, the line \"Select N.\" and the options with their letters." | 1 |
| A2 | Input, system: the guide block (30 task statements, 240 points, the three lists of Section 17) as the first block, with a cache mark. Then the instruction. | `src/step4_check_model.py`, 147-149, 55-64; `src/model_call.py`, 112-114 | "# Decision 0067: the guide comes first as a cached block. The story follows." / `{"type": "text", "text": c, "cache_control": {"type": "ephemeral"}}` | 1 |
| A3 | The instruction of call 4a. | `src/step4_check_model.py`, 32-33 | "You answer one exam question of the exam \"Claude Certified Architect - Foundations\", as a candidate does. Select the options that you think are correct. If you cannot decide, say so." | 1 |
| A4 | Output form: `status` (`answered` or `cannot_decide`), `selected` (letters), `reason`. | `docs/diagrams/06-forms-draft.json`, `call_4a`; `src/step4_check_model.py`, 17 | `"enum": ["answered", "cannot_decide"]` / "A short explanation of the selection, or of why you cannot decide." | 1 |
| A5 | Code checks the answer: a wrong count of letters, a repeated letter or a letter that the question does not have is a call that failed, not a finding. | `src/step4_check_model.py`, 150-158 | `raise CallFailed("Call 4a: %d letters selected, the line says %d." ...)` | 1 |
| A6 | A test checks that call 4a sees no marks and no reasons, and call 4b sees "Marked: correct". | `tests/test_model_steps.py`, 265-273 | `self.assertNotIn("Marked", blind_text)` | 1 |
| A7 | Why blind: an assumption of the assistant, not checked. | `docs/decisions/0032-...md`, 157 | "A checker that sees the marks can tend to agree with them. This is an assumption of the assistant. It is not checked." | 2 |
| A8 | Why two calls: an instruction "answer first, then look at the key" in one call is not enforced. Two calls with code between them enforce the order (1.4-K2). | `docs/decisions/0032-...md`, 158; `docs/build-guide/step-4-check-by-a-model.md`, 11 | "Two calls with code between them make sure that the blind answer always comes first." | 2 / 3 |

### 2.2 Call 4b, the rule check

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | Input, system: two cached blocks (the guide block, then the 12 sample questions with their correct answers), then the instruction. | `src/step4_check_model.py`, 167-176, 73-81 | "# Decision 0067: the guide and the 12 sample questions come first as two # cached blocks. The story and the rest follow." | 1 |
| B2 | Input, user text, in order: the story; the earlier questions on the same idea (or "None."); the rules; the slot (task statement, point, scenario); the question with marks and reasons. | `src/step4_check_model.py`, 169-174 | `"THE EARLIER QUESTIONS ON THE SAME IDEA (for rule B9):"`, `"THE RULES"`, `"THE SLOT: task statement %s, point %s, scenario %d."`, `"THE QUESTION, with the marks and the reasons of the writer:"` | 1 |
| B3 | The instruction of call 4b. | `src/step4_check_model.py`, 34-35 | "You check one exam question against nine rules. Use only the text of the exam guide below as the source of facts. Give one result for each rule: pass, fail or cannot_decide. A result that is not pass has a finding." | 1 |
| B4 | Output form: for each rule, `rule`, `result` (`pass`, `fail`, `cannot_decide`), `finding`, `letter`, `point`. Plus a list `features`. | `docs/diagrams/06-forms-draft.json`, `call_4b` | "Give one result for each of the rules B1 to B9." | 1 |
| B5 | Code checks the answer: one result for each rule B1 to B9, a finding for each result that is not pass, a letter that exists, a point ID that exists, a list of features. Else the call failed. | `src/step4_check_model.py`, 177-191 | `raise CallFailed("Call 4b: rule %s names the point %s, which does not exist." ...)` | 1 |
| B6 | Call 4b always runs, also when call 4a disagrees, so the writer gets all findings in one try. | `src/step4_check_model.py`, 196-197; `docs/decisions/0032-...md`, 41 | "Call 4b always runs, also when the blind answer of call 4a is different from the marks. Then the writer of step 5 gets all findings in one try." | 1 / 2 |
| B7 | The earlier questions come from the built mocks with a lower number, by the group of the point. With none, B9 passes. | `docs/decisions/0056-...md`, 23-24; `src/step4_check_model.py`, 164, 29 | "If there are none, B9 passes." | 2 / 1 |
| B8 | For a narrow idea (63 of the 95 groups in `data/narrow-ideas.json`), code swaps the strict B9 for the copy rule. | `src/step4_check_model.py`, 165-166; `data/narrow-ideas.json` (`len(groups)` = 63); `data/point-groups.json` (95) | `rules_text = RULES_TEXT.replace(B9_STRICT, B9_COPY) if narrow else RULES_TEXT` | 1 |
| B9 | No confidence number. | `docs/decisions/0032-...md`, 40, 167 | "The call gives no confidence number." / "We have no such labels before the owner marks mock 1 (decision 0022). Until then a number has no meaning." | 2 |
| B10 | A limit: only call 4a is blind. Call 4b gets the writer's reasons. | `docs/decisions/0032-...md`, 156 | "A limit: only call 4a is blind. Call 4b is not completely \"without prior reasoning context\", because it gets the reason of each option from the writer." | 2 |

### 2.3 The 9 rules, one line each (exact text sent to call 4b)

Source: `src/step4_check_model.py`, 21-30 (B9 text from `src/step2_write.py`, 26 and 28-30). L1.

| Rule | Text (shortened only where marked "...") |
|---|---|
| B1 | "Each option that is marked correct is correct, and no other option is correct." |
| B2 | "Each wrong option is wrong for a reason that the guide gives, and its reason says so." |
| B3 | "Each reason is true and agrees with the guide." |
| B4 | "The question tests the point of its slot." |
| B5 | "The question is inside the story of its scenario and does not contradict it." |
| B6 | "No text depends on a feature that the guide does not name. A feature is a thing of a Claude product or of MCP that has a name: a tool, a command, a flag, a parameter, a field, a file or a setting. ..." |
| B7 | "Each actor has one name in the question, the options and the reasons. A reader understands each sentence at the first reading." |
| B8 | "The question is not a close copy of a sample question of the exam guide: not the same scene with the same correct action." |
| B9 (strict, from mock 4) | "The question does not have the same problem as an earlier question on the same idea, also in another setting (another tool, team, product or data). ... At most one wrong option may repeat." |
| B9 (copy rule, narrow idea) | "The question is not a copy of an earlier question on the same idea: not the same scene with the same answer and the same set of wrong options. At most one wrong option may repeat. ..." |

When each rule was added (decision, and the run files): B1 to B6 decision 0032 (6 October). B7 decision 0043 (7 October). B8 decision 0055 (8 October). B9 decision 0056 (8 October), stricter text decision 0066 (9 October). Run files: mock 1 records have B1 to B7 (83 of 83). Mock 2 records have B1 to B8 (74) or B1 to B9 (17, the rewrites under decision 0056). Mocks 3 to 5 have B1 to B9. Method: section 4.1. L1 (computed), L2.

### 2.4 Code makes the verdict

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| V1 | A different blind answer adds a B1 finding. A blind "cannot decide" adds a B1 finding. Each rule result that is not pass adds its finding. | `src/step4_check_model.py`, 200-208 | "The blind answer selected %s. The writer marked %s. The reason of the blind answer: %s" | 1 |
| V2 | Rule B6 by code: the model lists the feature names, and code searches each name in the records file. A name that is not found adds a B6 finding. | `src/step4_check_model.py`, 209-212, 95-129 | "The feature \"%s\" is not in the exam guide." | 1 |
| V3 | `fail`: blind answer different, or a rule fails, or a feature is not found. `cannot_decide`: else, if the blind answer or a rule cannot decide. `pass`: else. | `src/step4_check_model.py`, 213-219 | `if (blind["status"] == "answered" and not same) or "fail" in results.values() or any(not f["found"] for f in features): verdict = "fail"` | 1 |
| V4 | Code saves one new file per check, with `verdict`, `findings`, `fingerprint`, `date`, `blind_answer`, `results`, `features`, `model`. | `src/control.py`, 394-401 | "# Step 4 adds its own fields: blind_answer, results, features, model (decision 0032)." | 1 |
| V5 | A call that fails runs again, at most 3 times. Then an error record. | `src/control.py`, 30, 309-322 | `CALL_RUNS = 3          # runs of a call that fails (decision 0037, item 10). A guess.` | 1 |
| V6 | Two "cannot decide" verdicts in one start of a slot open the slot for the owner. | `src/control.py`, 32, 215-223 | `CANNOT_DECIDE = 2      # "cannot decide" results that stop a slot (decision 0023)` | 1 |
| V7 | A new try is checked as a new question. The two calls do not see earlier findings. Reason: an assumption, not checked. | `src/step4_check_model.py`, 194; `docs/decisions/0032-...md`, 59, 168 | "A question from step 5 is checked as a new question. The two calls do not see the earlier findings." | 1 / 2 |
| V8 | Rule B6 search: capital letters do not count, a hyphen, an underscore and a space are the same, a name must be a complete word, a name of one character is never named, except a flag with its hyphens. | `src/step4_check_model.py`, 84-129 | "So \"Vision\" is not found inside \"provisions\". A name of one character is never named, except a flag with its hyphens (decision 0061)." | 1 |

### 2.5 Limits of the mechanism (facts)

| # | Fact | Source | L |
|---|---|---|---|
| X1 | In mocks 1 to 5, call 4a never disagreed with the marks and never said "cannot decide": 0 of 477 checks. All B1 findings in the mocks came from call 4b (2: M2-S49-T1, M3-S53-T2). In both, call 4a had selected the marked letters. | field `blind_answer` of `runs/mock-0N/checks/*-step4.json`; method 4.1 | 1 (computed) |
| X2 | Example, M3-S53-T2 (call 4a selected A, B, the marks; call 4b failed B1): "Option B is marked correct, but it does not explain the missed problems." | `runs/mock-03/checks/M3-S53-T2-step4.json`, field `findings[0].detail` | 1 |
| X3 | "Cannot decide" never happened in a real run: 0 verdicts, 0 rule results. | field `verdict` and `results[].result`; method 4.1 | 1 (computed) |
| X4 | In the test, the damaged copies with a moved mark (B1) were caught by call 4b alone. Part 3 of the test ran call 4b only. Each B1 copy failed B1, B2 and B3. | `runs/test-0024/part3.json`, field `checks[].verdict.failed_rules`; `runs/test-0024/damaged.json` ("Code moves the mark 'correct' from the correct option to a wrong option, and swaps their reasons.") | 1 |
| X5 | Call 4a was tested only on the 12 sample questions, which have one answer each: 12 of 12 right. | `runs/test-0024/part2.json` (`right` 12, `of` 12); `docs/decisions/0032-...md`, 175 | 1 / 2 |
| X6 | B6 still fails a name in another form than the guide. Run files: "tool description" (guide: "tool descriptions"), M2-S06-T1; "~/.claude/" (guide: "~/.claude/CLAUDE.md"), M4-S46-T2; "tool call interception hook", M1-S14-T1. This agent re-ran `FeatureSearch.named` on these names (no model call): all three `False`, `-p` `True`. | `features` fields of those records; `src/step4_check_model.py`, 116-129; `docs/decisions/0041-...md`, 56 ("Also a name in another form than the guide, for example \"is_error\" against \"isError\", is not found.") | 1 (computed) / 2 |
| X7 | A name on the list "out of scope" counts as named for B6. Example in a test: "Vision". | `tests/test_model_steps.py`, 404-410; `docs/decisions/0041-...md`, 56 | 1 / 2 |
| X8 | The instruction of call 4b says "the exam guide below". Since decision 0067 the guide is a system block before the instruction. | `src/step4_check_model.py`, 34 and 175-176; `src/model_call.py`, 112-114 | 1 |
| X9 | Each check of step 4 is a judgment of a model. Two of 10 verdicts changed in the cache test with the same rule text (section 5, story a). The stricter B9 agreed with an independent agent on only 12 of about 26 (story b). | `docs/decisions/0067-...md`, 33-43; `docs/decisions/0066-...md`, 52 | 2 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-4-check-by-a-model.md`, 56-64 (L3). This agent checked each quote and each task statement title against `reference/guide-records.json` by script: 7 of 7 texts and titles agree.

| Line | Point | Text of the guide | Task statement | How the step uses it (exact) |
|---|---|---|---|---|
| 58 | 4.6-K1 | "Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session" | 4.6: Design multi-instance and multi-pass review architectures | "Written for the review of code. Here: the call that wrote a question does not check it." |
| 59 | 4.6-K2 | "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking" | 4.6 | "The same context. Here: a new call, with no reasoning of the writer, checks the question." |
| 60 | 4.3-S5 | "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization" | 4.3: Enforce structured output using tool use and JSON schemas | "Written for a schema for the extraction of data. Here: the result "cannot decide" for a case that the checker cannot decide." |
| 61 | 4.1-K1 | "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" | 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | "Written for the review of code. Here: one result for each exact rule, not one total verdict." |
| 62 | 1.4-K2 | "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" | 1.4: Implement multi-step workflows with enforcement and handoff patterns | "Written for the order of steps in the workflow of an agent. Here: "answer first, then see the key" is enforced by two calls, not by an instruction." |
| 63 | 4.3-K1 | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" | 4.3 | "Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above)." |
| 64 | 4.3-S3 | "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" | 4.3 | "Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above)." |

Task statements: 4.6, 4.3, 4.1, 1.4 (the page summary line already shows "task statements 4.6, 4.3, 4.1, 1.4", `academy/pages/behind-the-mocks.html`, 104).

The deviation (build guide, 44-52, L3): "The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call." Reason, quoting the page "Define tools": the row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". Saved copy: `docs/sources/2026-10-07-anthropic-docs-define-tools.md` (Docs). For the exam, the answer is the forced tool call that the guide teaches.

Where the code uses each point:

| Point | Code |
|---|---|
| 4.6-K1, 4.6-K2 | `src/step4_check_model.py`, 145-149: a new call; the writer's call is a different request (`src/step2_write.py`, 218-220). |
| 4.3-S5 | `docs/diagrams/06-forms-draft.json`: enum `cannot_decide` in both forms; `src/step4_check_model.py`, 216-217. |
| 4.1-K1 | `src/step4_check_model.py`, 179-180: one result for each rule B1 to B9. |
| 1.4-K2 | `src/step4_check_model.py`, 196-197: call 4a runs and returns before call 4b is sent. |
| 4.3-K1, 4.3-S3 | `src/model_call.py`, 116-119: `output_config={"effort": ..., "format": {"type": "json_schema", "schema": schema}}`, no `tools`, no `tool_choice`. |

Exam guide facts on caching (for the Depth; not in the table):

- Section 17, "Out-of-Scope Topics": "Prompt caching implementation details (beyond knowing it exists)". `reference/exam-guide.md`, 1064 (L: exam guide). So the exam expects only that prompt caching exists.
- The cost lever that the guide teaches is the Message Batches API: 4.5-K1 "The Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed latency SLA". 4.5-K2: batch is "inappropriate for blocking workflows". `reference/guide-records.json`. Decision 0067 rejected the Batches API: "the rounds of the pipeline would wait for each batch" (`docs/decisions/0067-...md`, 15). Decision 0067 lists "Exam guide points: none" (57). No source links 0067 to 4.5-K2.

## 4. Numbers, per mock, with method

### 4.1 Method

Script (kept outside the repository, at the scratchpad path `s4.py`; it reads only run files and makes no model call). For each mock N in 1 to 5:

- Step 4 records: `glob("runs/mock-0N/checks/*-step4.json")`.
- Verdicts: count field `verdict`.
- Model "fail" results per rule: count `results[i].result == "fail"` by `results[i].rule`.
- Findings per rule: count `findings[i].rule`. (A B6 finding can come from the model result or from code. A B1 finding can come from call 4a or call 4b.)
- Blind disagreement: `blind_answer.status == "answered" and not blind_answer.agrees`. Blind cannot decide: `blind_answer.status == "cannot_decide"`.
- Features not found: `features[i].found == False`.
- Usage: sum of `calls`, `input_tokens`, `output_tokens`, `cache_write_tokens`, `cache_read_tokens`, `dollars` over `runs/mock-0N/usage/*.json`.
- Cost recomputed with the prices of `src/model_call.py`, 28-33: `(input + 1.25 x cache_write + 0.05 x cache_read) x $4/M + output x $20/M`.
- Cost without caching (a counterfactual for the same tokens): `(input + cache_write + cache_read) x $4/M + output x $20/M`.
- Expected calls: tries (`runs/mock-0N/questions/*.json`) + 2 x step 4 records + 2 x step 6 records (`checks/*step6*.json`).

### 4.2 Step 4 verdicts and findings

| Mock | Step 4 checks | pass | fail | cannot decide | Rules in each check |
|---|---|---|---|---|---|
| 1 | 83 | 69 | 14 | 0 | B1-B7 (83) |
| 2 | 91 | 74 | 17 | 0 | B1-B8 (74), B1-B9 (17) |
| 3 | 99 | 62 | 37 | 0 | B1-B9 |
| 4 | 107 | 62 | 45 | 0 | B1-B9 |
| 5 | 97 | 62 | 35 | 0 | B1-B9 |
| All | 477 | 329 | 148 | 0 | |

Checks = tries minus the tries that failed step 3 (83-0, 92-1, 101-2, 111-4, 101-4). The fails agree with `academy/facts/top-of-tab-2.md` (14, 17, 37, 45, 35).

Findings per rule (each check has at most one finding per rule in these runs, so this is also the number of checks with that finding):

| Mock | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 1 | 1 | 2 | 3 | 7 | - | - |
| 2 | 1 | 1 | 2 | 0 | 1 | 8 | 5 | 2 | 0 |
| 3 | 1 | 0 | 0 | 0 | 0 | 3 | 11 | 0 | 24 |
| 4 | 0 | 0 | 2 | 0 | 0 | 1 | 4 | 1 | 39 |
| 5 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 1 | 31 |
| All | 2 | 1 | 7 | 1 | 3 | 15 | 29 | 4 | 94 |

- B6: every B6 finding came from code (feature not found). The model's own B6 result was never "fail" (model fail counts per rule in the script output have no B6).
- B1: both B1 findings came from call 4b. Call 4a: 0 disagreements, 0 "cannot decide" in all mocks.
- Fails with findings of 2 or more rules: 0, 3, 2, 2, 1.
- B9 share of the fails: mock 3 24 of 37, mock 4 39 of 45, mock 5 31 of 35 (B9 alone: 22, 37, 30).

Features (rule B6) listed by call 4b and not found:

| Mock | Features listed | Not found | Of these, "-p" |
|---|---|---|---|
| 1 | 218 | 3 | 2 (M1-S24-T1, M1-S51-T1) |
| 2 | 216 | 8 | 7 (M2-S32-T2, S35-T2, S37-T1, S38-T2, S43-T1, S44-T1, S45-T1) |
| 3 | 276 | 3 | 3 (M3-S48-T1, M3-S48-T3, M3-S56-T1) |
| 4 | 225 | 1 | 0 |
| 5 | 263 | 0 | 0 |

### 4.3 Calls and cost per mock (whole mock: writer, step 4 and step 6)

| Mock | Calls | Input tokens | Cache write | Cache read | Output tokens | Dollars (files) | Recomputed | Without caching | Saved |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 265 | 3,155,135 | 0 | 0 | 227,309 | 17.17 | 17.17 | 17.17 | 0 |
| 2 | 290 | 3,820,272 | 0 | 0 | 272,378 | 20.73 | 20.73 | 20.73 | 0 |
| 3 | 313 | 4,260,060 | 0 | 0 | 340,675 | 23.85 | 23.85 | 23.85 | 0 |
| 4 | 337 | 816,640 | 114,690 | 3,727,309 | 412,234 | 12.83 | 12.83 | 26.88 | 14.05 (52%) |
| 5 | 295 | 771,454 | 114,844 | 3,257,489 | 368,531 | 11.68 | 11.68 | 23.95 | 12.26 (51%) |
| All | 1500 | | | | | 86.26 | | | |

More computed numbers:

- Cache reads were 80.0% (mock 4) and 78.6% (mock 5) of all input tokens.
- Input cost against output cost: mock 3 $17.04 input, $6.81 output. Mock 4 $4.59 input, $8.24 output. Mock 5 $4.31 input, $7.37 output. After caching, output is the larger part.
- Cost per try: $0.207, $0.225, $0.236, $0.116, $0.116. Cost per call: $0.065, $0.072, $0.076, $0.038, $0.040.
- Calls of step 4 per mock (2 per check): 166, 182, 198, 214, 194. The usage files do not split the cost by step (section 9, item 2).
- Expected calls against the usage files: mock 1 265 = 265, mock 2 290 = 290, mock 3 311 against 313 (2 more), mock 4 337 = 337, mock 5 305 against 295 (10 fewer). Mock 5: the stopped run is not in `usage/` (`docs/decisions/0073-...md`, 23: "The cost of the stopped run is not in `runs/mock-05/usage/`, because the program saves the cost at the end of a run."). Mock 3: no source explains the 2 extra calls (a retried call would make one; `errors/` is empty).
- Usage files exist for runs 2, 4, 5 of mock 1; 1, 2 of mock 2; 1, 3, 4 of mock 3; 1 to 4 of mock 4; 2 to 6 of mock 5.

### 4.4 The cache test (`runs/test-cache/results.json`)

| Number | Value | How a script reads it |
|---|---|---|
| Questions | 10 (every 6th of mock 3: `mock3_questions()[::6]`, `src/test_cache.py`, 42) | `len(results)` |
| Calls | 20 | `cost.calls` |
| Dollars with caching | 0.58 | `cost.dollars` |
| Without caching, same tokens | 1.72 (1.7196) | formula 4.1 over `results[].usage` |
| Saving | 66.4% | `1 - 0.5786/1.7196` |
| Input tokens / cache write / cache read / output | 22,731 / 34,369 / 309,321 / 12,698 | `cost.*` |
| Size of the cached block of call 4a | 15,327 tokens | `results[0].usage[0].cache_write` |
| Size of the cached blocks of call 4b | 19,042 tokens | `results[0].usage[1].cache_write` |
| Reads from the second question on | 15,327 (4a), 19,042 (4b) per call | `results[1..9].usage[*].cache_read` |
| Verdicts that changed | 2 of 10: M3-S31-T2 pass to fail (B9), M3-S49-T2 pass to fail (B8) | `stored != new` |

Call 4b wrote its full 19,042 tokens to the cache on the first question. It did not read the 15,327-token guide block that call 4a had just written. Decision 0067 line 31: "Calls 4a and 4b keep separate caches, probably because their answer forms differ." The page "Structured outputs" supports this: "Changing the `output_config.format` parameter will invalidate any [prompt cache] for that conversation thread" (`docs/sources/2026-10-07-anthropic-docs-structured-outputs.md`, 2613, Docs).

Text sizes, computed by this agent from the code with no model call: `guide_core(records)` = 44,073 characters, 5,650 words split on white space (with IDs and headings). `sample_text(records)` = 11,011 characters, 1,637 words.

### 4.5 The B9 test (`runs/test-b9/results.json`)

| Number | Value | How a script reads it |
|---|---|---|
| Questions of mock 3 checked by call 4b | 60 | `len(results)` |
| B9 fail / pass | 24 / 36 | count `result` |
| Questions with earlier questions on the same idea | 53 | count non-empty `earlier` |
| Fails with no earlier question | 0 | |
| Calls, input tokens, output tokens, dollars | 60, 1,257,489, 64,873, 6.33 | `cost.*` (no cache fields: the test ran before decision 0067) |

### 4.6 The test before the first full run (`runs/test-0024/`)

| Part | Result | Cost | Field |
|---|---|---|---|
| Part 2: call 4a on the 12 sample questions | 12 of 12 right | $0.79, 12 calls | `right`, `of`, `cost` in `part2.json` |
| Part 3: call 4b on 9 good questions and 9 damaged copies | 18 of 18 as expected | $1.41, 18 calls | `as_expected`, `of` in `part3.json` |
| Part B7: call 4b with rule B7 on the 10 questions | 7 of 10 as expected; 3 good questions (T-M1-S01, S02, S04) failed B7; the bad one (T-M1-S05) failed B7 | $0.82, 10 calls | `part-b7.json` |

Damaged rules in `damaged.json`: B1 (2), B2 (2), B3 (2), B4, B5, B6 (1 each).

### 4.7 Fixed numbers

| Number | Meaning | Source | How a script reads it |
|---|---|---|---|
| 9 | rules of call 4b | `src/step4_check_model.py`, 19 | `len(RULES_B)` |
| 2 | model calls per check | `src/step4_check_model.py`, 196-197 | |
| 3 | runs of a call that fails | `src/control.py`, 30 | regex `^CALL_RUNS = (\d+)` |
| 2 | "cannot decide" results that open a slot | `src/control.py`, 32 | regex `^CANNOT_DECIDE = (\d+)` |
| 4.0 / 20.0 | dollars per million input / output tokens | `src/model_call.py`, 28 | `PRICE` |
| 1.25 / 0.05 | cache write / cache read factor | `src/model_call.py`, 32-33 | regex `^CACHE_WRITE = `, `^CACHE_READ = ` |
| 64000 | `max_tokens` | `src/model_call.py`, 26 | regex `^MAX_TOKENS = (\d+)` |
| "high" | effort | `src/model_call.py`, 23 | regex `^EFFORT = ` |
| 240 | points in the guide block | `tests/test_model_steps.py`, 284 | `len(re.findall(r"^  \d\.\d-[KS]\d+:", text, re.M))` |
| 12 | sample questions in call 4b | `tests/test_model_steps.py`, 307-308 | |
| 63 of 95 | narrow ideas of 95 point groups | `data/narrow-ideas.json`, `data/point-groups.json` | `len(d["groups"])` |
| 228 | tests, all pass | `tests/*.py` | `unittest discover` (14 October 2026) |

## 5. Stories for the Depth

Sources searched: decisions 0012, 0023, 0032, 0037 (item 8), 0040, 0041, 0043, 0044, 0055, 0056, 0060 to 0068, 0072, 0073, 0075, 0078; `docs/journal.md` (grep "cach", "batch", "-p", "B6", "B9", "4a", "4b", "serious"); `docs/lessons.md`, `HANDOFF.md`, `docs/portal-notes.md` (grep "cach", "blind", "checker"); `docs/reviews/test-b9-mock-3.md`; `git log --date=iso` of the files named below.

### Story (a): prompt caching, missed in the design and added before mock 4 (mock decision 0067)

Order in time (commit times from `git log --date=iso`, +1100):

| # | When | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|---|
| a1 | 6-8 Oct | No decision before 0067 names caching. A search for "cach" in `docs/decisions/` (except 0067), `docs/reviews/`, `docs/lessons.md`, and in `src/` and `tests/` before commit `53b2fd4`, finds nothing. | grep (method) | - | 2 (search) |
| a2 | 7 Oct 22:50 to 9 Oct 10:15 | Mocks 1 to 3 ran with no caching: $17.17, $20.73, $23.85. | `runs/mock-0{1,2,3}/usage/*.json` (no cache fields); `git log` of the usage files; build guide, 21-27 | "Until mock 3, each call sent it at the full input price, with no caching" | 1 / 3 |
| a3 | 9 Oct, about 10:30 to 10:51 | The B9 test cost $6.33, not the $3 to $4 estimated. Each call takes the full guide and the 12 samples. | `docs/reviews/test-b9-mock-3.md`, 6; `runs/test-b9/results.json` `cost` | "Cost: $6.33 for 60 calls of call 4b. The estimate of the assistant was $3 to $4. Each call takes the full text of the guide and the 12 sample questions." | 4 / 1 |
| a4 | 9 Oct | The cost estimate of mock 4 without caching: $32 to $40. | `docs/decisions/0066-...md`, 62; `docs/journal.md`, 51 | "so about $32 to $40. This is an estimate of the assistant. It is not measured." | 2 |
| a5 | 9 Oct, before mock 4 | The owner stopped and asked about the cost. | `docs/journal.md`, 13 | "The plan of mock 4 was made (seed 445312). Before the run, the owner stopped and asked about the cost." | 4 |
| a6 | 9 Oct | The owner asked if the program uses caching. The assistant said no. | `docs/decisions/0067-...md`, 51 | "The owner asked if the program uses prompt caching. The assistant said no, estimated a saving of about $10 for each mock from the run records of mock 3, and showed the change." | 2 |
| a7 | 9 Oct | The problem, with the numbers of mock 3. | `docs/decisions/0067-...md`, 10 | "The program did not use prompt caching. Each check call sent the full text of the guide again, at the full input price. Mock 3 sent 3.84 million input tokens ($15.34) and cost $23.85 in total." (See conflict C1.) | 2 |
| a8 | 9 Oct | The owner rejected the Message Batches API. | `docs/decisions/0067-...md`, 15 | "The Message Batches API. The owner rejected it: the rounds of the pipeline would wait for each batch." | 2 |
| a9 | 9 Oct 11:00 | The fix: the guide first, the same in each call, with a cache mark. The story moves to the user text. Call 4b adds the samples as a second cached block. The writer caches its rules. | `docs/decisions/0067-...md`, 21-23; commit `53b2fd4` (2026-10-09 11:00:30) | "The story of the scenario moves from the guide block to the user text, so the guide block is the same for each scenario." | 2 / 1 |
| a10 | 9 Oct | Prices and minimum size, read on 9 October 2026. | `docs/decisions/0067-...md`, 24-25; `src/model_call.py`, 29-33 | "a 5-minute cache write costs 1.25 times the input price, and a cache hit on Claude Opus 5.5 costs 0.05 times the input price ($0.20 per million tokens)" / "The minimum cacheable size for Claude Opus 5.5 is 512 tokens" | 2 / 1 |
| a11 | 9 Oct | The test, 10 questions of mock 3: $0.58 with caching, $1.72 without, about 66% less. | `docs/decisions/0067-...md`, 31; `runs/test-cache/results.json` | "The calls cost $0.58 with caching. The same tokens with no caching cost $1.72. That is about 66% less on the check calls." | 2 / 1 |
| a12 | 9 Oct | 2 of 10 verdicts changed, both pass to fail, causes not separated. A recheck with no cache passed both. Mock 3 stays accepted. | `docs/decisions/0067-...md`, 33-47 | "M3-S31: rule B9, the same scene and answer as M1-S10 (a named session, continue it with --resume)." / "M3-S49: rule B8, the scene of sample question 5." / "The same 2 questions, checked once more with no cache and the guide in the user text, both passed." / "Possible causes, not separated" | 2 |
| a13 | 9 Oct | The owner named the stricter B9 as a cause. It does not apply: the test used the old B9 text. | `docs/decisions/0067-...md`, 45; `src/test_cache.py`, 8-9, 28-29, 38 | "The test script used the text of B9 that checked mock 3 (decision 0056), not the stricter text, so that cause does not apply to this test." | 2 / 1 |
| a14 | 9 Oct 11:09 | The owner confirmed 0067 and gave the go for mock 4. | commit `1facb17` (2026-10-09 11:09:30); `docs/decisions/0067-...md`, 5 | "The owner confirmed decision 0067 and gave the go for mock 4" | 1 |
| a15 | 9 Oct 12:16 to 17:15 | Mock 4 with caching: $12.83 for 337 calls (run 1 $10.39). Mock 5: $11.68 for 295 calls. | `runs/mock-04/usage/*.json`, `runs/mock-05/usage/*.json`; build guide, 33-34 | "Mock 4 also had the stricter rule B9 and more tries than mock 3, and it still cost about half of mock 3." (build guide, 36) | 1 / 3 |
| a16 | 9 Oct | Journal: an estimate with caching of $20 to $26 for mock 4. | `docs/journal.md`, 18 | "Mock 4 cost $12.16 for 326 calls: 3.69 million input tokens came from the cache. The estimate with caching was $20 to $26." | 4 |
| a17 | - | A test checks that the cached blocks are identical in each call, for each scenario, and that the cost counts the cached tokens. | `tests/test_model_steps.py`, 287-299, 316-321 | `self.assertEqual(len(firsts), 1)` | 1 |
| a18 | - | No independent reviewer checked decision 0067. | `docs/decisions/0067-...md`, 53 | "No independent reviewer checked this file." | 2 |

Product facts (Docs), page "Prompt caching", https://platform.claude.com/docs/en/build-with-claude/prompt-caching, read live on 14 October 2026 (no saved copy, see the header):

- "5-minute cache write tokens are 1.25 times the base input tokens price". "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)".
- Table row: "Claude Opus 5.5 | $4 / MTok | $5 / MTok | $8 / MTok | $0.20 / MTok | $20 / MTok". Footnote: "Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are priced at 0.05x the base input price." So the code's 0.05 is right for this model. The general rule is 0.1.
- "512 tokens for ... Claude Opus 5.5". "By default, the cache has a 5-minute lifetime."
- "Prompt caching references the entire prompt: `tools`, `system`, and `messages` (in that order), up to and including the block designated with `cache_control`." "Cache hits require 100% identical prompt segments".
- The exam guide: caching details are out of scope "beyond knowing it exists" (section 3 above).

### Story (b): rule B9 let the same problem pass, so it became stricter (mock decisions 0056, 0062, 0066)

| # | When | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|---|
| b1 | 8 Oct | In mock 2, 13 questions repeated mock 1 strongly and 4 closely. | `docs/decisions/0056-...md`, 10 | "17 questions of mock 2 repeat mock 1: 13 strong (the same scene, the same answer and the same wrong options) and 4 close." | 2 |
| b2 | 8 Oct 20:22 | The first B9. | `docs/decisions/0056-...md`, 23; commit `ab70bd4` | "New rule B9 in call 4b: \"The question is not a repeat of an earlier question on the same idea: not the same scene with the same answer, and no wrong option of an earlier question.\"" | 2 |
| b3 | 8 Oct 21:57 | Mock 3 run 1: B9 failed 24 checks at step 4. | `runs/mock-03/checks/*-step4.json`; journal, 74 | "Rule B9 failed many tries that repeated mock 2, mostly in scenario 6. 4 slots reached the limit of 3 tries." | 1 / 4 |
| b4 | 8 Oct | An independent agent still found about 26 same-problem repeats in the built mock 3. | `docs/decisions/0062-...md`, 10 | "About 26 questions have the same problem and the same answer as an earlier question, in another setting. Rule B9 should fail these, but the model judged a new setting as a new scene." | 2 |
| b5 | 8 Oct 23:28 | The owner: stricter from mock 4, mock 3 accepted. | `docs/decisions/0062-...md`, 33 | "for mock 4 we make it stricter but for now we accept mock 3 as it is with the 2 copies rewritten." | 2 |
| b6 | 9 Oct 10:29 | The new text, and a test on mock 3 first. | `docs/decisions/0066-...md`, 21, 24; `src/test_b9.py` | "A question on the same idea passes only with a different problem: for example the cause against the fix, a different failure, or a choice between two rules." | 2 / 1 |
| b7 | 9 Oct | The owner changed the wrong-options part. | `docs/decisions/0066-...md`, 60 | "\"No wrong option of an earlier question\" became \"Not the same set of wrong options. At most one wrong option may repeat.\" The reason of the owner: the standard mistakes that the guide names make the strongest wrong options, and the owner wants harder questions in mocks 4 and 5." | 2 |
| b8 | 9 Oct | The test: 24 of 60 fail. Agreement with the agent on 12. | `docs/decisions/0066-...md`, 52; `runs/test-b9/results.json` | "So the rule is a judgment, and it will sometimes fail a good question or pass a close one." | 2 / 1 |
| b9 | 9 Oct 10:48 | The exception: narrow ideas keep the copy rule. First list 20 groups. | `docs/decisions/0066-...md`, 26 | "Some ideas have almost only one problem, for example \"find text across many files, so use Grep\"" | 2 |
| b10 | 9 Oct | Who proposed what. | `docs/decisions/0066-...md`, 66 | "The stricter rule was proposed by Claude Code. The change to the wrong options and the exception for narrow ideas came from the second review in Cowork. The owner decided each one." | 2 |
| b11 | 9 Oct | The list grew: 24 (0068, after three mock 4 slots failed B9 three times), 62 (0072), 63 (0075). | `docs/decisions/0068-...md`, 10, 19; `0072-...md`, 20; `0075-...md`, 21 | "now has 63 of the 95 groups" | 2 |
| b12 | - | The result for participants: mocks 4 and 5 often repeat a problem in a new setting. | build guide, 13 | "So mocks 4 and 5 often test the same problem as mocks 1 to 3, in a new setting, and only copies are blocked." | 3 |

Example of a B9 finding from the test (real, mock 3): M3-S26-T1 against M1-S06-T1: "A text pattern must be found across hundreds of Python files whose names do not reveal it, and the answer is a Grep content search rather than Glob on file names or Read." (`runs/test-b9/results.json`). This idea (G037, Grep) is on the narrow list (`docs/decisions/0066-...md`, 38).

### Story (c): rule B6 failed the flag "-p", which the guide names (mock decision 0061)

| # | When | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|---|
| c1 | 7 Oct 13:01 | The cause: a review fix made B6 never find a name of one character, and code treats a hyphen as a space. | `docs/decisions/0041-...md`, 27-31; commit `0cbff92` | "never finds a name of one character." | 2 / 1 |
| c2 | - | The guide names "-p". | `reference/guide-records.json`, point 3.6-K1 | "The -p (or --print) flag for running Claude Code in non-interactive mode in automated pipelines" | exam guide |
| c3 | 7 Oct to 8 Oct | The run files: 12 checks in mocks 1 to 3 failed B6 on "-p" (2, 7, 3). In 10 of them it was the only finding. | section 4.2; `features` and `findings` fields | `{"name": "-p", "found": false}` / "The feature \"-p\" is not in the exam guide." | 1 (computed) |
| c4 | 8 Oct | The decision names only mock 3, slot M3-S48. | `docs/decisions/0061-...md`, 10 | "Code removed the hyphen and searched \"p\", so a question that used \"-p\" always failed B6. In mock 3, slot M3-S48 failed two of its three tries for this reason only." | 2 |
| c5 | 8 Oct | M3-S48: T1 and T3 failed B6 on "-p". T2 failed B9. The slot opened. | `runs/mock-03/checks/M3-S48-T{1,2,3}-step4.json` | - | 1 |
| c6 | 8 Oct | The assistant found it in the open slot. | `docs/decisions/0061-...md`, 29; journal, 75 | "The assistant found the fault in the open slot M3-S48 and suggested option 1. The owner said yes." | 2 / 4 |
| c7 | 8 Oct 22:52 | The fix: a flag is searched with its hyphens, as a complete flag. A test. | `src/step4_check_model.py`, 113-125; commit `0847fe5`; `tests/test_model_steps.py`, 331-339 | "A flag such as -p or --print is searched with its hyphens, as a complete flag." | 1 |
| c8 | 8 Oct | The owner gave the slot 3 more tries with the reason. | `runs/mock-03/owner-decisions.json`, D003 | "Two tries failed rule B6 on \"-p\", which was a fault of B6 (decision 0061). Try again." | 1 |
| c9 | 8 Oct 22:59 | After the fix, M3-S48-T5 and T6 used "-p" and code found it (`"found": true`). T6 passed. | `runs/mock-03/checks/M3-S48-T5-step4.json`, `-T6-step4.json` | `{"name": "-p", "found": true}` | 1 |
| c10 | - | The reason for the fix. | `docs/decisions/0061-...md`, 23 | "B6 must pass a feature that the guide names, and fail one that it does not. \"-p\" is named in the guide, so a fail is wrong." | 2 |

### Smaller items (for the Explanation, not stories)

| # | Fact | Source | L |
|---|---|---|---|
| s1 | Before any run, a reviewer found that call 4a had no guide text. The first code (`eb05725`, 7 Oct 12:51) called `blind(question)` with no guide. The fix (`0cbff92`, 13:01) added the guide text. | `docs/journal.md`, 191 ("An independent reviewer found 3 serious items: call 4a had no guide text, the B6 search found names inside other words, and each API error was retried."); `git show 0cbff92 -- src/step4_check_model.py` | 4 / 1 |
| s2 | A reviewer found that the prompt of call 4b said "six rules". A test now checks the number word. | `docs/journal.md`, 202; `tests/test_model_steps.py`, 311-314 | 4 / 1 |
| s3 | The enum of the form must have each rule, or each real call 4b fails. A test checks it. | `tests/test_model_steps.py`, 323-329 ("The review of 8 October 2026: the enum of the form must have each rule, or each real call 4b fails.") | 1 |
| s4 | B7 came from one bad mark of the owner in the test. B7 then failed 3 of 9 good questions, each with a true finding. The rule stays strict. | build guide, 42; `runs/test-0024/part-b7.json` | 3 / 1 |
| s5 | B8 came from two close copies of sample questions 1 and 12 in mock 1. | build guide, 13; diagram 06 popup B8 | 3 |

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step4_check_model.py` | 145-159 | `blind()`: call 4a, the cached guide, the question with no key, the checks of the letters. |
| `src/step4_check_model.py` | 161-176 | `rules()`: call 4b, the narrow swap of B9, the user text, two cached blocks. |
| `src/step4_check_model.py` | 194-219 | `check()`: code compares and makes the verdict. The core of the step. |
| `src/step4_check_model.py` | 21-30 | The text of the 9 rules. |
| `src/step4_check_model.py` | 116-129 | `named()`: the B6 search, with the flag fix of decision 0061 (121-125). |
| `src/model_call.py` | 108-114 | `ask()`: cached texts become system blocks with `cache_control`. |
| `src/model_call.py` | 27-43 | Prices, cache factors with their source line, and `cost()`. |
| `src/test_cache.py` | 37-58 | The cache test: old B9 text, 10 questions, stored against new verdict. |
| `tests/test_model_steps.py` | 287-299 | The test that the cached blocks are identical. |
| `tests/test_model_steps.py` | 331-339 | The test of decision 0061 (named: -p, --print; not named: -x, p, --printx). |
| `git show 0847fe5 -- src/step4_check_model.py` | diff | The before and after of the "-p" fix (a docstring line changed, 8 lines added). |

## 7. A figure

### Figure 1: the mechanism

```
 question (passed step 3)
   | code removes marks and reasons            | code keeps marks and reasons
   v                                           v
 [guide | cached] + story + question     [guide | cached][12 samples | cached]
   --> CALL 4a (Claude) "answers blind"         + story + earlier questions + rules + slot + question
   --> letters + reason                        --> CALL 4b (Claude) "checks B1..B9, lists features"
                                               --> 9 results + feature names
          \                                    /
           v                                  v
        CODE: compares letters | searches each feature name in the records | checks each answer
           --> verdict: pass -> next slot (step 6 when all 60 pass)
                         fail / cannot decide -> step 5 (writer, with findings)
```

Facts behind the labels: "removes marks and reasons" A1, A6. "guide cached" A2, a9. "12 samples cached" B1. "earlier questions" B2, B7. "rules" 2.3, B8. "answers blind" A3, A4. "checks B1..B9" B3-B5. "compares letters" V1. "searches each feature" V2, V8. "checks each answer" A5, B5. "verdict" V3. "step 5" O4. Real numbers that could sit on the arrows: 477 checks, 329 pass, 148 fail, 0 cannot decide (4.2). Call 4a disagreed 0 times (X1).

### Figure 2: the caching story

Bars of cost per mock (dollars, from `usage/*.json`): 17.17, 20.73, 23.85 (no caching), then 12.83, 11.68 (caching). A ghost bar for mocks 4 and 5 without caching: 26.88, 23.95 (counterfactual, section 4.1). A marker between mocks 3 and 4: "decision 0067, 9 October".

A small inset for the test: 10 questions, $0.58 with caching against $1.72 without (66% less). Per call: 4a reads 15,327 tokens from the cache, 4b reads 19,042 (4.4).

A second inset: where the input tokens of mock 4 went: 3,727,309 read from the cache (80%), 816,640 normal input, 114,690 cache write. After caching, output cost ($8.24) is bigger than input cost ($4.59).

## 8. Conflicts

| ID | Topic | Source A (quote, level) | Source B (quote, level) |
|---|---|---|---|
| C1 | Mock 3 input tokens | `docs/decisions/0067-...md`, 10: "Mock 3 sent 3.84 million input tokens ($15.34) and cost $23.85 in total." (L2) | `runs/mock-03/usage/*.json`: all runs 4,260,060 input tokens ($17.04). Run 1 alone: 3,835,197 ($15.34). The $23.85 is all runs. (L1) |
| C2 | Points of step 4 in diagram 01 | `docs/diagrams/01-pipeline-overview.html`, 191, popup "4": points 4.6-K1, 4.6-K2, 4.6-S1, 3.6-K4. Box: "Exam guide: task statements 4.6 and 3.6" (141). (L3) | Build guide table, 56-64: no 4.6-S1, no 3.6-K4, no task statement 3.6 (L3). By academy decision 0024, the table is the source. Decision 0012, 40, lists "4.6-K1, 4.6-K2, 4.6-S1, 3.6-K4, 5.2-K3, 1.2-K2" (L2). Already recorded as X8 in `academy/facts/top-of-tab-2.md`. |
| C3 | Points of the design decision | `docs/decisions/0032-...md`, 190: "4.6-K1, 4.6-K2, 5.5-K3, 4.6-S3, 4.3-S5, 4.1-K1, 1.4-K2" (L2). 5.5-K3 and 4.6-S3 are reasons for "no confidence number". | Build guide table: no 5.5-K3, no 4.6-S3; it has 4.3-K1 and 4.3-S3 (L3). Not a diagram-only point, so not a conflict by decision 0024. Listed for the owner. |
| C4 | The text of decision 0032 against the code | `docs/decisions/0032-...md`, 37, 45, 70: "one result for each rule B1 to B6"; the guide text has "The story of the scenario" in it. Status line (4): "Decision 0055 adds rule B8 to call 4b." only. (L2) | Code: B1 to B9 (`src/step4_check_model.py`, 19); the story is outside the cached guide block since 0067 (147-148). Later decisions 0043, 0056, 0066, 0067 win, but the status line of 0032 does not name them. (L1) |
| C5 | Words of the guide text | `docs/decisions/0032-...md`, 45 and diagram 06 popup "guide": "about 5300 words" ("A script counted 5255 words for this text, without the story."). (L2, L3) | This agent: `guide_core(records)` = 5,650 words split on white space, 44,073 characters. The methods differ (IDs and headings). (L1, computed) |
| C6 | "A fail has the point ID" | Diagram 06 popup "c4b": "A \"fail\" has a finding, and the ID of the guide point that the finding uses." (L3) | `docs/decisions/0032-...md`, 37: "Both can be empty." Form: `point` is `["string", "null"]`. Run files have fails with `"point": null`. (L2, L1) |
| C7 | "Below" | `src/step4_check_model.py`, 34: "Use only the text of the exam guide below as the source of facts." (L1) | `src/model_call.py`, 112-114 and `src/step4_check_model.py`, 175-176: the guide is a system block before this instruction (L1). The code disagrees with itself. No source says if this matters. |
| C8 | Cost of mock 3 and mock 5 in the journal | `docs/journal.md`, 76: "Mock 3 cost $23.15." Line 30: "Mock 5 cost $11.02". (L4) | `runs/mock-03/usage/*.json`: $23.85. `runs/mock-05/usage/*.json`: $11.68 (L1). The journal values are earlier points in time (23.15 = runs 1 and 3; 11.02 = runs 2 to 5). Later journal lines and the build guide have $23.85 and $11.68. |
| C9 | What the cost table of step 4 measures | Build guide, 21-34: under "The cost, with and without caching" of step 4, "Cost, no caching": $17.17, $20.73, $23.85 (L3). | `runs/mock-0N/usage/*.json`: these are the whole mock (writer, step 4, step 6). The usage files do not split by step (L1). The table does not say "whole mock". |
| C10 | Which mocks had the "-p" fault | `docs/decisions/0061-...md`, 10, names only mock 3, slot M3-S48 (L2). | Run files: also 2 checks in mock 1 and 7 in mock 2, and M3-S56-T1 (L1, computed, 4.2). Not a contradiction: the decision does not say "only". |
| C11 | Diagram 06 popup has no point that the table lacks | Popup "c4b" cites 4.6-K1, 4.6-K2, 4.3-S5 (L3). | All three are in the table. No diagram-only point in diagram 06. (No conflict; checked.) |

## 9. Not found

1. A saved dated copy of the page "Prompt caching". Decision 0067 read it on 9 October 2026 but `docs/sources/` has only "Define tools" and "Structured outputs". This agent read it live on 14 October 2026 and did not save a copy (instruction: change no other file). Academy decision 0030 needs a copy in `academy/sources/` before the page quotes it.
2. The cost of step 4 alone per mock. `usage/*.json` has one total per run. Only the cache test (`runs/test-cache/`) has usage per call.
3. A run file for the recheck of M3-S31 and M3-S49 "with no cache and the guide in the user text" (`docs/decisions/0067-...md`, 38). `runs/test-cache/` has only `results.json`.
4. The cause of the 2 calls of mock 3 that the records do not explain (313 against 311).
5. The source of the journal estimate "$20 to $26" with caching (`docs/journal.md`, 18). No decision has it.
6. Whether a B9 fail in mocks 4 and 5 used the strict text or the copy rule. Step 4 records do not store `narrow`, and the narrow list changed during the runs (20, 24, 62, 63 groups).
7. A source that says why caching was not in the design. Decision 0067 says only "The program did not use prompt caching." The "missed in the design" part rests on absence (a1).
8. A source that says the B9 test cost (a3) caused the owner's question about cost (a5). They are in order in time on 9 October. No record links them.
9. Evidence that call 4a ever caught a wrong key in a real run (X1). The test of call 4a covered only the 12 one-answer sample questions.
