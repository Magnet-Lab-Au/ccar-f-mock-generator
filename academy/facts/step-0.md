# Fact sheet: tab 2, step 0 "Prepare the guide records"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `1cbae17` (branch `main`, clean).
- Levels of trust (academy decisions 0011, 0014, 0029): 1 = code, tests and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "L" = level of trust. "(computed)" = this agent ran a script that reads files and writes nothing.
- A path such as `docs/decisions/0028-...md` means the one file in `docs/decisions/` whose name starts with `0028-`. For 0027, 0031 and 0037: the file that starts with `00NN-the-`.
- Line numbers are for the files at commit `1cbae17`.
- Scripts that this agent ran (none writes a file, none calls a model): `python3 src/check_guide_records.py` (prints "41 of 41 checks passed", exit 0); `step0_prepare_guide_records.build()` imported in Python, without `main()`, so no file is written; small read-only counts shown in section 4. The agent did not run `src/step0_prepare_guide_records.py` as a script, because that writes `reference/guide-records.json` (working rule 27).
- Not run: `academy/sources/compare-exam-guide.py`. The library `pypdf` is not installed here ("ModuleNotFoundError: No module named 'pypdf'").
- Files not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, the personal files of the owner, `claude-code-brand-kit/`, conversation transcripts.
- No Anthropic documentation page was needed: step 0 has no model call and uses no product feature (see section 9).

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | A script copies the parts of the exam guide that later steps need into one file. No model copies text. | `docs/build-guide/step-0-prepare-the-guide-records.md`, 9 | "Before the program plans a mock, a script copies the parts of the exam guide that the later steps need into one file, `reference/guide-records.json` (decision 0028). No model copies text." | 3 |
| O2 | The same, in the code. | `src/step0_prepare_guide_records.py`, 3-5 | "It reads reference/exam-guide.md and writes reference/guide-records.json. It copies each text with no change. It writes no file if a count is wrong or if a text is not exactly in the guide." | 1 |
| O3 | The file is the one source of guide text for the code. A later step takes a slice by ID. | `docs/build-guide/step-0-...md`, 9; `docs/decisions/0028-...md`, 23 | "The file is the one source of guide text for the code. A later step takes a slice of it by ID." / "Code takes a slice from it by ID and gives only that slice to a model call. A model call does not read the file." | 3 / 2 |
| O4 | It runs one time for each version of the guide, not for each mock. | `docs/decisions/0017-...md`, 20; `docs/diagrams/01-pipeline-overview.html`, 138 | "It runs one time for each version of the guide, not one time for each mock." / "Step 0 runs one time for each version of the exam guide." | 2 / 3 |
| O5 | Who: code. The step is a script. | `docs/decisions/0028-...md`, 22 | "**Who.** Step 0 is a script. It reads `reference/exam-guide.md` and writes the records. No model copies text." | 2 |
| O6 | Status: built, ran on 6 October 2026. It ran once. | `docs/build-guide/step-0-...md`, 3; `README.md`, 43 | "Status: built. It ran on 6 October 2026." / "Step 0 ran once, on 6 October 2026." | 3 / 4 |
| O7 | The records file did not change after the first commit. | git (computed) | `git diff 8cc3a24 HEAD --stat -- reference/guide-records.json reference/exam-guide.md` is empty. `8cc3a24` is "Initial Commit", 7 October 2026 09:41. | 1 |
| O8 | Diagram 03 title, the idea of the step. | `docs/diagrams/03-step-0-...html`, 122-123 | "Step 0: from the exam guide to records that code can read" / "The exam guide is a document for people. The program needs its text in small parts, each with an ID." | 3 |

## 2. Explanation facts: the mechanism

### 2.1 Input and output (the contract)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | Input: `reference/exam-guide.md`. Output: `reference/guide-records.json`. | `src/step0_prepare_guide_records.py`, 16-17; `docs/decisions/0028-...md`, 42-43 | `GUIDE = os.path.join(ROOT, "reference", "exam-guide.md")` / `OUT = os.path.join(ROOT, "reference", "guide-records.json")` | 1 / 2 |
| E2 | The contract: it can fail on a wrong count or a text that is not exactly in the guide. Then it writes no file and names the cause. | `docs/decisions/0028-...md`, 44; `src/step0_prepare_guide_records.py`, 221-225 | "It can fail when a count is wrong or when a text is not exactly in the guide. Then the script writes no file and names the cause." / `print("Step 0 failed. No file is written. Cause: %s" % error, file=sys.stderr)` | 2 / 1 |
| E3 | The file has 6 parts at the top level: guide, domains, scenarios, task statements, sample questions, Section 17. | `src/step0_prepare_guide_records.py`, 198-205; `src/check_guide_records.py`, 48 | `check("top level has 6 parts", sorted(REC) == ["domains", "guide", "sample_questions", "scenarios", "section_17", "task_statements"])` | 1 |
| E4 | The records and their fields. | `docs/decisions/0028-...md`, 26-34 | "Guide \| version \| 1", "Domain \| id, name, weight \| 5", "Scenario \| id, name, story, primary domains \| 6", "Task statement \| id, domain, title, points \| 30", "Point \| id, kind (knowledge or skill), text \| 240", "Sample question \| number, scenario, question, options, correct answer, explanation \| 12", "Section 17 \| technologies, topics in scope, topics out of scope \| 3 lists" | 2 |
| E5 | The sections of the guide that the script reads: 4 (domains), 5 (scenarios), 6 (task statements), 9 (sample questions), 17 (lists). | `src/step0_prepare_guide_records.py`, 58, 69, 90, 123, 155 | `section(lines, r"^## 4\. ", r"^## 5\. ")` ... `section(lines, r"^## 17\. ", r"^## 18\. ")` | 1 |
| E6 | Example of the file content: domain 1. | `reference/guide-records.json` (computed) | `(1, 'Agentic Architecture & Orchestration', 27)` | 1 |

### 2.2 How the script works

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E7 | The script removes the page marks of the PDF before it reads the lists. | `src/step0_prepare_guide_records.py`, 19, 45-46 | `PAGE_LINE = re.compile(r"^<!-- Page \d+ \| .* -->$")` / "# A page line is a mark of the PDF page. It is not guide text." | 1 |
| E8 | Why the page marks matter (diagram popup). | `docs/diagrams/03-step-0-...html`, 166 (JSON `stepdata`, box `script`); `docs/diagrams/03-make-diagram.py`, 78 | "The guide file has 39 page marks from the PDF. A page mark can be in the middle of a list. The script leaves the page marks out, so that no list is cut in two." | 3 |
| E9 | The script gives each point its ID: task statement, K or S, then the number of the bullet. | `src/step0_prepare_guide_records.py`, 107-111 | `letter = "K" if kind == "knowledge" else "S"` / `current["points"].append({"id": "%s-%s%d" % (current["id"], letter, number), "kind": kind, "text": ln[2:]})` | 1 |
| E10 | The IDs are ours. The guide does not number its bullets. | `docs/decisions/0028-...md`, 36; `docs/build-guide/step-0-...md`, 13 | "Example: `1.4-K2` is the second bullet below \"Knowledge of:\" in task statement 1.4. The IDs are ours. The guide does not number its bullets." | 2 / 3 |
| E11 | The script stops on a line that it does not know, in Sections 6, 9 and 17. | `src/step0_prepare_guide_records.py`, 113, 146, 167 | `need(statements == [] and domain is None, "line that the script does not know: " + ln[:60])` | 1 |
| E12 | The script checks the structure: domain IDs 1 to 5, weights add up to 100, scenario IDs 1 to 6, each task statement has knowledge and skill points, knowledge before skill, sample questions in sequence with a valid answer. | `src/step0_prepare_guide_records.py`, 62-63, 85, 116-117, 147-150 | `need(sum(d["weight"] for d in domains) == 100, "domain weights do not add up to 100")` | 1 |
| E13 | The five expected counts are in the code. | `src/step0_prepare_guide_records.py`, 20, 213-214 | `EXPECTED = {"domains": 5, "scenarios": 6, "task_statements": 30, "points": 240, "sample_questions": 12}` | 1 |
| E14 | Before it writes, the script checks that each text is exactly in the guide. | `src/step0_prepare_guide_records.py`, 215-216 | `need(text and text in raw, "text is not exactly in the guide: " + text[:60])` | 1 |
| E15 | Plain reason for a script, not a person and not a model. | `docs/decisions/0028-...md`, 50; diagram 03 popup `script` | "a script copies text with no change, and we can run it again for a new version of the guide." / "No model works in this step. A model can change a word when it copies. A script cannot." | 2 / 3 |
| E16 | Plain reason for one file. | `docs/decisions/0028-...md`, 52 | "one file has one version and one check. With many files, a file can be missing or old. The slices that a call gets are the same in each case." | 2 |
| E17 | Plain reason for JSON, and why task statement 4.3 is not used. | `docs/decisions/0028-...md`, 51 | "JSON: the plain reason is that code reads it directly. The guide teaches JSON schemas for the output of a model (task statement 4.3). That is a different context. This file is the output of a script." | 2 |
| E18 | The script is deterministic: run again today, `build()` gives the same content as the file. | computed: `import step0_prepare_guide_records as s; r, c = s.build(); r == json.load(open("reference/guide-records.json"))` | output: "build() equals file: True" | 1 (computed) |
| E19 | The old file for people stays. | `docs/decisions/0028-...md`, 38 | "**The old file.** `reference/task-statements-and-points.md` stays. It is a file for people." | 2 |

### 2.3 The three checks of the file (decision 0028, part 5)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E20 | Decision 0028 names three checks. | `docs/decisions/0028-...md`, 37 | "(1) A script compares `reference/exam-guide.md` with the original in the Claude project \"CPN Learning path\", character for character. (2) A script checks the counts, and checks that each text in the file is exactly in the guide. (3) An independent reviewer checks the file (rule 15)." | 2 |
| E21 | Check 2 is a second script that does not use the code of step 0. | `src/check_guide_records.py`, 1-5 | "It checks reference/guide-records.json against reference/exam-guide.md and against reference/task-statements-and-points.md. It does not use the code of step 0. It prints one line for each check." | 1 |
| E22 | Check 2 passes 41 of 41 today. | run of `python3 src/check_guide_records.py` on 14 October 2026 | "41 of 41 checks passed" (exit 0) | 1 (computed) |
| E23 | Check 2 also checks the other direction: the 240 bullets of Section 6 are the 240 points, in the same sequence. | `src/check_guide_records.py`, 82-85 | `check("Section 6 of the guide has 240 bullets, and they are the 240 points in the same sequence", ...)` | 1 |
| E24 | Check 2 compares the points with the file for people, which a reviewer confirmed on 5 October 2026. | `src/check_guide_records.py`, 100-102 | "# 5. The points agree with the file for people, which a reviewer confirmed on 5 October 2026" | 1 |
| E25 | Check 3: an independent reviewer with its own script found no errors. It did not see the code of step 0 or the check script. | `docs/reviews/review-guide-records.md`, 4, 12, 16 | "It did not make the file. It did not see the script of step 0 or the check script." / "No errors found." / "The reviewer wrote its own script and compared the two files record by record and character by character, in both directions." | 4 |
| E26 | The reviewer checked the page marks where they cut a list. | `docs/reviews/review-guide-records.md`, 25 | "Page marks: the guide has 39, and 18 of them are in Section 6. No page mark is in a text. No bullet is lost, moved or numbered wrong." | 4 |
| E27 | Check 1 was not done on 6 October 2026. | `docs/journal.md`, 279 (section "6 October 2026, second session") | "Check 1, the comparison of our copy of the guide with the original, is not done. The assistant can read the original only as text in the chat." | 4 |
| E28 | Check 1 was done on 13 October 2026, against the official PDF: 0 differences. | `academy/decisions/0027-...md`, 14, 18 | "The owner gave the PDF. It is `academy/sources/exam-guide-v1.0-official.pdf`, and the script is `academy/sources/compare-exam-guide.py`." / "The result on 13 October 2026: 11,157 words in each, and 0 places that differ." | 2 |
| E29 | The limit of that comparison: words, not characters. | `academy/decisions/0027-...md`, 30 | "The script compares words, not spaces, line breaks, the order of table cells or the layout." | 2 |
| E30 | Why a check that does not use the code of step 0 (diagram popup). | diagram 03 popup `c2`; `03-make-diagram.py`, 86 | "A check must not depend on the code that made the file." | 3 |

### 2.4 Who uses the records (the later steps)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E31 | The program loads the file once and gives it to the steps and to the control. | `src/run.py`, 34-36; `src/steps.py`, 23-25, 35 | `records = load_records()` / `return Control(folder, mock, seed, steps, guide_points(records)), steps` | 1 |
| E32 | Step 1 reads domains (weights), scenarios (primary domains), task statements and points. It checks the parts that it reads first. | `src/step1_plan.py`, 77-79, 269 | `def check_records(records):` / "Check the parts of the records file that step 1 reads. Raise PlanError with the cause for each problem." | 1 |
| E33 | Step 2 (the writer) gets a slice: 3 sample questions of other scenarios (letters removed, no explanation), the story of the scenario, the task statement of the slot with its points (the point marked), and the 14 technologies of Section 17. | `src/step2_write.py`, 70-85, 119-131 | `"The task statement %s: %s. Its points (the point of the slot is marked with >>>):"` / `parts += ["- " + plain(t) for t in records["section_17"]["technologies"]]` | 1 |
| E34 | Step 4 gets the story, all 30 task statements with their 240 points, and the 3 lists of Section 17: the same text for each call, so that it can be cached. It also gets the 12 sample questions for rule B8. | `src/step4_check_model.py`, 55-58, 74-76 | "All 30 task statements with their 240 points, and the three lists of Section 17. The same text for each call, so it can be cached (decision 0067)." / "Decision 0055: the 12 sample questions of the guide, for rule B8, with the correct answer of each." | 1 |
| E35 | Step 4, rule B6: code (not a model) searches each feature name in all texts of the records file. | `src/step4_check_model.py`, 95-114 | "Decision 0030: \"named\" means that the name is in the text of the records file. Code searches each text of the file, without the backslash of the format." | 1 |
| E36 | Step 4 checks that each point ID in an answer exists in the records. | `src/step4_check_model.py`, 143; `docs/decisions/0032-...md`, 39 | `self.point_ids = {p["id"] for t in records["task_statements"] for p in t["points"]}` / "Code checks that each point ID exists in the records file." | 1 / 2 |
| E37 | Step 7 shows the text of each point in the marking file. | `src/step7_marking.py`, 49-51, 81 | `self.points = {p["id"]: p["text"] for t in records["task_statements"] for p in t["points"]}` | 1 |
| E38 | Step 8 copies the scenario name and story into the mock file, and the domain of each question. | `src/step8_build_files.py`, 58-59, 73-74 | `groups.append({"scenario": sc["id"], "name": sc["name"], "story": sc["story"], "questions": []})` | 1 |
| E39 | The control checks a new point of the owner against the records. | `src/control.py`, 700-702 | `if point not in self.guide_points.get(slot["task_statement"], []):` | 1 |
| E40 | Other files are tied to the guide version of the records: the plan of each mock, `data/point-groups.json`, `data/two-answer-points.json`. Code refuses a file with another version. | `src/step1_plan.py`, 255-256; `src/point_groups.py`, 46-48 | `raise PlanError("The file of the two-answer points has another guide version.")` | 1 |
| E41 | No model call reads the file. | `docs/decisions/0028-...md`, 23; diagram 03 popup `u1` | "A model call does not read the file." / "It is a small database for the code. No model call reads it." | 2 / 3 |
| E42 | The records file keeps a backslash from the Markdown of the guide in 5 texts. Code removes it before a model or a person sees the text. | `src/step2_write.py`, 19-21; `src/step7_marking.py`, 32-35 | "Remove the backslash that the records keep from the format of the guide." / "The records file keeps a backslash from the format of the guide, for example \"\\*\\*/\\*.test.tsx\". The owner reads the text without it." | 1 |

### 2.5 Limits

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E43 | What the guide does not cover in this step. | `docs/decisions/0017-...md`, 33 | "The guide does not cover this: that the records are made one time and checked character for character, and that no model copies guide text." | 2 |
| E44 | The reviewer did not check the copy of the guide, the content of the guide, or the script of step 0. | `docs/reviews/review-guide-records.md`, 45-49 | "If `reference/exam-guide.md` is a correct copy of the original guide." / "If the content of the guide is technically correct." / "The script of step 0." | 4 |
| E45 | The records leave out most sections of the guide (1 to 3, 7, 8, 10 to 16, 18). | `docs/reviews/review-guide-records.md`, 48 | "Sections 1 to 3, 7, 8, 10 to 16 and 18 of the guide. The records do not include them." | 4 |
| E46 | The guide's sample questions cover only scenarios 1, 2, 3 and 5. | `reference/guide-records.json` (computed); `docs/reviews/review-guide-records.md`, 26 | "Questions 1 to 3 are scenario 1, 4 to 6 are scenario 2, 7 to 9 are scenario 3, and 10 to 12 are scenario 5." | 1 / 4 |
| E47 | No unit test in `tests/` covers step 0 or its check script. The check script is the test. | computed: `grep -rn "step0\|check_guide" tests/` gives no line | (no output) | 1 (computed) |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-0-prepare-the-guide-records.md`, lines 23-31 (L3). Line 25: "Decision 0017 chose these points for step 0. Decision 0028 is the design of the step." A script checked on 14 October 2026 that each text and each title in the table is exactly the text of `reference/guide-records.json` (3 of 3 rows agree in point text, task statement ID and title).

| Point | Line | Task statement | Text of the guide | How the step uses it (exact, from the table) |
|---|---|---|---|---|
| 1.3-S2 | 29 | 1.3: Configure subagent invocation, context passing, and spawning | "Using structured data formats to separate content from metadata (source URLs, document names, page numbers) when passing context between agents to preserve attribution" | "Written for agents that pass context to other agents. Here: each record keeps its ID, so each later step and each question keeps the link to its source." |
| 5.6-K1 | 30 | 5.6: Preserve information provenance and handle uncertainty in multi-source synthesis | "How source attribution is lost during summarization steps when findings are compressed without preserving claim-source mappings" | "Written for the synthesis of findings. Here: the records keep the exact guide text, so no summary loses the source." |
| 5.6-K2 | 31 | 5.6 | "The importance of structured claim-source mappings that the synthesis agent must preserve and merge when combining findings" | "The same context. Here: the IDs of the points are the mapping between a question and the text of the guide." |

Facts that support the uses:

- T1: the same three points are the Reason of decision 0017 (`docs/decisions/0017-...md`, 31, 43: "1.3-S2, 5.6-K1, 5.6-K2"). Decision 0028 adds no point (line 48: "This decision uses no new exam guide point."; line 70: "none"). (L2)
- T2: the popups cite the same three points and no other. Diagram 01, line 191, popup "0": points 1.3-S2, 5.6-K1, 5.6-K2, and the line "Exam guide: task statements 1.3 and 5.6". Diagram 03, line 166, popup `script`: the same three. So no point appears only in a diagram (no conflict under academy decision 0024). (L3)
- T3: no other build guide table uses 1.3 or 5.6. Method: `grep -ln "1.3-S2\|5.6-K1\|5.6-K2" docs/build-guide/*.md docs/diagrams/*.html` gives only the step 0 section, diagram 01 and diagram 03. So in tab 1, task statements 1.3 and 5.6 link to step 0 only (for these points). (L3, computed)
- T4: the "Here" of 1.3-S2 is in the code: each question record, plan slot and mock question keeps the point ID. All 300 questions of `mocks/mock-0N.questions.json` have a `point` that is in the records, and all 20 scenario stories in the mock files are exactly the story of the records (section 4). (L1, computed)
- T5: an independent review called all three uses "agrees in part" (context). See story (d) in section 5. (L4)
- T6: the "Why here" text of the diagrams. Diagram 01 line 191 and diagram 03 line 166: "The guide wrote these points for agents that pass findings to other agents. Here they apply to record files: each later step takes guide text from these records by ID, so each question keeps the link to its source." (L3)

## 4. Numbers, with method

All counts were made on 14 October 2026 with Python `json` and `re`, reading files only.

| Number | Meaning | Source | How a script reads it |
|---|---|---|---|
| 5, 6, 30, 240, 12 | domains, scenarios, task statements, points, sample questions | `src/step0_prepare_guide_records.py`, 20; `reference/guide-records.json` | regex `^EXPECTED = (\{.*\})` on the script; or `len(R["domains"])`, `len(R["scenarios"])`, `len(R["task_statements"])`, `sum(len(t["points"]) for t in R["task_statements"])`, `len(R["sample_questions"])` |
| 14, 18, 16 (48 in all) | technologies, topics in scope, topics out of scope (Section 17) | `reference/guide-records.json` | `len(R["section_17"][k])` for each key; the check script prints "48 = 14 + 18 + 16" |
| 113 / 127 | knowledge points / skill points | `reference/guide-records.json` | count `p["kind"] == "knowledge"` / `"skill"` over all points |
| 3 or 4 / 3 to 6 | knowledge points per task statement / skill points per task statement | same | Counter of knowledge points per task statement: {3: 7, 4: 23}; skill: {3: 7, 4: 11, 5: 10, 6: 2}. Agrees with `docs/reviews/review-guide-records.md`, 39 |
| 7, 5, 6, 6, 6 | task statements in domains 1 to 5 | same; `src/check_guide_records.py`, 66 | count `t["domain"]` |
| 48, 43, 49, 47, 53 | points in domains 1 to 5 | same | count points by the domain of their task statement |
| 27, 18, 20, 20, 15 | domain weights (add up to 100) | same; `src/check_guide_records.py`, 107 | `[d["weight"] for d in R["domains"]]` |
| 408 | texts in the file | `src/check_guide_records.py`, 77 (prints "each of the 408 texts is exactly in the guide"); `docs/diagrams/03-make-diagram.py`, 38 (`assert n_texts == 408`) | the list `texts` of the check script, lines 69-75 |
| 7,958 (about 8,000) | words in the 408 texts | computed | `sum(len(t.split()) for t in texts)`; diagram 03 rounds it: `round(n_words, -2)` (line 97) → "about 8000 words" |
| 202 (about 200) | words of the example slice: story of scenario 3 and task statement 1.2 with its 8 points | computed; `docs/diagrams/03-make-diagram.py`, 33-34 | same word count over the slice texts; the diagram rounds to "about 200" |
| 39 | page marks of the PDF in `reference/exam-guide.md` | `docs/diagrams/03-make-diagram.py`, 35; `docs/reviews/review-guide-records.md`, 25 | `len(re.findall(r'^<!-- Page \d+ \|.*-->$', guide, flags=re.M))` |
| 41 | checks of the check script (all pass) | run `python3 src/check_guide_records.py` | last line "41 of 41 checks passed". (The file has 25 lines with `check(`; loops over the 6 scenarios and the 12 sample questions make 41.) |
| 12 of 12 | sample questions that call 4a of step 4 answered right in the test before the first full run | `runs/test-0024/part2.json` | fields `right` = 12, `of` = 12 (cost field: 12 calls, $0.79) |
| A 10, B 2 | correct letters of the 12 sample questions | `reference/guide-records.json`; `docs/decisions/0029-...md`, 125 | Counter of `q["correct_answer"][0]`. Decision 0029: "the correct answer is A 10 times and B 2 times" |
| 5 | texts of the records with a backslash from the Markdown of the guide | computed; `docs/reviews/review-guide-records.md`, 35 | count texts that contain `\\` (1.7-K1, 2.5-S2, 3.3-S1, 3.3-S2, the explanation of sample question 6) |
| 11,157 / 0 | words in the PDF and in the copy / places that differ | `academy/decisions/0027-...md`, 18 | regex `(\d{1,2},\d{3}) words in each, and (\d+) places that differ` on the decision. Not re-run by this agent (pypdf missing). |
| 1,073 | lines of `reference/exam-guide.md` | computed | `wc -l` |
| 1,741 | lines of `reference/guide-records.json` | computed | `wc -l` |
| 238 / 138 | lines of the step 0 script / the check script | computed | `wc -l src/step0_prepare_guide_records.py src/check_guide_records.py` |
| 300 of 300; 20 of 20 | mock questions whose `point` is in the records; scenario groups whose `story` is exactly the story in the records (mocks 1 to 5) | `mocks/mock-0N.questions.json` | for each group: `g["story"] == story[g["scenario"]]`; for each question: `q["point"] in point_ids` |
| 7 of 7 | files with a `guide_version` equal to the version in the records | `runs/mock-0N/plan.json` (5), `data/point-groups.json`, `data/two-answer-points.json` | `d["guide_version"] == R["guide"]["version"]` |
| 1 | runs of step 0 | `README.md`, 43; `docs/journal.md`, 278 | text "Step 0 ran once, on 6 October 2026". No run file of step 0 exists (section 9). |

The version string of the records (field `guide.version`): "Version 1.0 · Effective July 2026 · Exam code: CCAR-F · This guide is subject to change without notice."

## 5. Stories for the Depth

Searched: the "How we decided" sections of decisions 0017, 0028, 0029, 0032; `docs/journal.md` (sections "6 October 2026, first session" and "second session"); `docs/reviews/review-guide-records.md`; `docs/reviews/review-decisions-0003-to-0018.md`; `docs/reviews/review-decisions-0026-to-0036.md` and `-0024-to-0037.md` (no mention of step 0 points); `docs/lessons.md`; `HANDOFF.md`; `academy/journal.md`; academy decision 0027; git history of the step 0 files.

Result: no source records a failure of the step 0 script or of the records file itself (no wrong count, no wrong text, no rerun). The stories are about the design process and the checks. Story (a) is the strongest "what went wrong and the fix".

### Story (a): a proposal for step 2 had no source, so step 0 was designed first

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | What went wrong. | `docs/decisions/0028-...md`, How we decided, 58 | "The assistant showed a proposal for step 2 that said \"the story of the scenario\" and \"a fixed form with fields\". The owner asked where the story comes from, said that the task statements are not in separate records for code, and said that no output format and no fields were decided. The owner was right." | 2 |
| A2 | The cause. | same, 58 | "The cause: `HANDOFF.md` said to start with step 1, and each step reads the records of step 0. The assistant followed that sequence and did not say that it was wrong." | 2 |
| A3 | The fix: two changes. | same, 60 | "The owner and the assistant then agreed on two changes. Step 0 is designed before step 2. Each design names the exact file format and the exact fields." | 2 |
| A4 | The same in decision 0029 (step 2). | `docs/decisions/0029-...md`, How we decided, 145 | "The first proposal of the assistant said \"the story of the scenario\" and \"a fixed form with fields\", with no source and no fields. The owner said that this was not specific. Step 0 was then designed and run first (decision 0028)." | 2 |
| A5 | The journal of that session. | `docs/journal.md`, "6 October 2026, second session", 276 | "The owner said that it was not specific: no source for the story of the scenario, no records for code, no output format, no fields. The owner was right. Agreed: step 0 is designed before step 2, and each design names the exact file format and the exact fields." | 4 |
| A6 | The fix became a working rule. | `WORKING-RULES.md`, 60 (rule 30) | "for the design of a pipeline step, the assistant shows one proposal with all details of the step. The proposal names the exact file format and the exact fields." | (project file) |
| A7 | The questions of the owner on the design. | `docs/decisions/0028-...md`, 62, 64 | "The owner asked why all records are in one file, because different API calls get different slices. The answer: code takes the slice, and the model never sees the file. The owner accepted one file." / "The owner asked what a point is, and if \"Knowledge of\" and \"Skills in\" are in the original guide." | 2 |
| A8 | The result: the step 2 request now names its sources in the records (story, task statement, points, technologies, samples). | `src/step2_write.py`, 119-131; `docs/decisions/0029-...md`, 25 | "Code builds the request from the records file of step 0 and the plan of step 1." | 1 / 2 |
| A9 | Same day: design, run, checks. | `docs/journal.md`, 277-279 | "Step 0 ran. `src/step0_prepare_guide_records.py` made `reference/guide-records.json`: 5 domains, 6 scenarios, 30 task statements, 240 points, 12 sample questions and the 3 lists of Section 17." | 4 |

### Story (b): step 0 was first an "input", and the owner made it a step

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | The two corrections of the owner. | `docs/decisions/0017-...md`, How we decided, 39 | "The assistant first suggested a step 0 in which code reads the complete guide into records. The owner said that the guide was already divided into task statements. That was correct for the 240 points. The assistant then suggested to call the work an input and not a step. The owner said that it must be documented in each case, because a goal of the build is a record that a portal page can show. So the work has a number, a decision file and a box in the diagram." | 2 |
| B2 | The journal. | `docs/journal.md`, "6 October 2026, first session", 337 | "The owner corrected the assistant two times: the 240 points exist already, and the work must be documented as a step." | 4 |
| B3 | The three options of decision 0017. | `docs/decisions/0017-...md`, Options, 14-16 | "1. Step 0: checked record files of the guide, made one time for each version of the guide. It is in the numbered sequence." / "2. Prework: the same work, documented, outside the numbered steps." / "3. No separate work. Each step reads what it needs from the guide file." | 2 |
| B4 | Later, the script did read the complete guide (decision 0028), and the file for people became a check. | `src/step0_prepare_guide_records.py`, 89-118; `src/check_guide_records.py`, 100-104 | `check("the 240 points agree with task-statements-and-points.md, ID and text", ...)` | 1 |

### Story (c): the check of the copy against the original stayed open for a week

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| C1 | Decision 0017 already named the gap. | `docs/decisions/0017-...md`, 35 | "One open item of the handoff belongs here: no code compared `reference/exam-guide.md` with the original, character for character." | 2 |
| C2 | Not done on 6 October 2026. | `docs/journal.md`, 279, 311 | "The assistant can read the original only as text in the chat." / "Check 1 of the records file is not done. The assistant asked the owner if the original guide file is on the computer. The owner did not answer yet." | 4 |
| C3 | Why it matters (diagram popup). | diagram 03 popup `c1`; `03-make-diagram.py`, 95 | "The other two checks show that the records agree with our copy. Only this check shows that our copy agrees with the original." | 3 |
| C4 | Raised again for tab 1. | `academy/decisions/0027-...md`, Question, 10 | "`HANDOFF.md` lists as open: \"`reference/exam-guide.md` is not compared with the original, character for character.\" How do we know that the quotes are exact?" | 2 |
| C5 | The fix and the result. | `academy/decisions/0027-...md`, 14, 18 | (see E28) "11,157 words in each, and 0 places that differ." | 2 |
| C6 | How the script got to 0. | `academy/decisions/0027-...md`, How we decided, 26 | "The first runs listed only differences of format, such as list bullets, running headers, escaped marks and links. The assistant added a rule for each kind, and then no difference was left." | 2 |
| C7 | `HANDOFF.md` has the result. | `HANDOFF.md`, 161 | "Compared with the official PDF on 13 October 2026, word for word: 0 differences (academy decision 0027)." | 4 |
| C8 | The build guide and diagram 03 still say "not done". | see conflict X1 | | 3 |

### Story (d): the three guide points fit "in part"

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| D1 | The review of decisions 0003 to 0018 rated all three uses of step 0 "agrees in part". | `docs/reviews/review-decisions-0003-to-0018.md`, 47-49 | "0017 \| 1.3-S2 \| agrees in part \| Point is about \"passing context between agents\" (task 1.3, subagents). The Decision is a one-time preparation of record files" / "0017 \| 5.6-K1 \| agrees in part \| ... The Decision has no summarization step; the risk it guards is a model that copies guide text wrongly." | 4 |
| D2 | The overall result of that review. | same, 5 | "The weak spot is context transfer: 26 of 41 rows are \"agrees in part\" and 1 is \"does not agree\"." | 4 |
| D3 | Decision 0019 corrected other decisions after that review, but not decision 0017. | `docs/decisions/0019-...md`, 21-37 (items 1 to 9 name 0012, 0006, 0013, 0005, 0007, 0008, 0003, 0018) | (no item names 0017) | 2 |
| D4 | The build guide table now states the context of each point ("Written for ..."). | `docs/build-guide/step-0-...md`, 29-31 | "Written for agents that pass context to other agents. Here: ..." | 3 |
| D5 | The reviewer named a nearer point, which no file of step 0 uses. | `docs/reviews/review-decisions-0003-to-0018.md`, 99 | "**0017** (\"no model copies guide text\", \"made one time\"): partly covered by 5.1-S1 ... \"Checked character for character\" is not covered." | 4 |

### Story (e): the reviewer's observations reached later steps

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| R1 | The reviewer found no errors but listed 7 observations for later steps. | `docs/reviews/review-guide-records.md`, 31-33; `docs/journal.md`, 279 | "## Observations (not errors)" / "A later step must know these." | 4 |
| R2 | Observation 1: backslashes in 5 texts. | `docs/reviews/review-guide-records.md`, 35 | "**Markdown backslashes in 5 texts.** They are exact copies of the guide file. A step that shows the text to a person or to a model must decide what to do with them." | 4 |
| R3 | Decision 0029 left it open. | `docs/decisions/0029-...md`, 139 | "What to do with the 5 texts of the records file that have a backslash from the file format (review of step 0)." | 2 |
| R4 | The code removes the backslash for the writer, the checker and the marking file. | `src/step2_write.py`, 19-21; `src/step4_check_model.py`, 84-87, 95-97; `src/step7_marking.py`, 32-35 | `return re.sub(r"\\(.)", r"\1", text)` | 1 |
| R5 | Observation 7: the explanations name option letters. | `docs/reviews/review-guide-records.md`, 41 | "**The explanations name option letters.** An explanation says \"Option B\" or \"Option C\". If a later step changes the sequence of the options, these words become wrong." | 4 |
| R6 | Decision 0029 used it: one reason for each option, and no reason names a letter. | `docs/decisions/0029-...md`, 127 | "**One reason for each option.** Plain reason: no reason names a letter, so the letters can change, and the checker can check each reason alone. The reviewer of step 0 found that the explanations of the sample questions name letters (\"Option B\")." | 2 |
| R7 | The code: the examples for the writer leave out the explanation and the letters. | `src/step2_write.py`, 70-75 | "Code keeps the question and the options, mixes the options, removes the letters, marks the correct option and leaves out the explanation." | 1 |

### Minor facts for the Depth (small slips around the records)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| M1 | A wrong word count: the assistant said the checker gets about 8000 words; that was the whole records file. | `docs/decisions/0032-...md`, 45; `docs/journal.md`, 288 | "(The assistant said \"about 8000 words\" in the chat. That number was the complete records file, with the sample questions. A script counted 5255 words for this text, without the story.)" | 2 / 4 |
| M2 | Diagram 03 was made twice. | `docs/journal.md`, 280 | "The owner said that the first version was a copy of the form of diagram 02 and had elements that are not necessary. The assistant made it again with a different idea: a document for people becomes records for code. The owner accepted it. Diagrams 04 to 07 have this form." | 4 |
| M3 | Background from the first build (CAUTION: the file calls itself private, see section 9). Lesson 16. | `docs/lessons.md`, 3, 62-63 | "Private history of the first build. Not a source for the design." / "**Keep the exact source text with each question to the end, and let code compare it with the source.** The field for the exact guide text was exact in 15 of 342 records. Later steps dropped the field." | 4 |

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step0_prepare_guide_records.py` | 1-9 | The docstring: what the step reads and writes, and when it writes no file. |
| `src/step0_prepare_guide_records.py` | 19-20 | The page mark pattern and the five expected counts (`EXPECTED`). |
| `src/step0_prepare_guide_records.py` | 42-47 | `read_guide`: page marks of the PDF are left out. |
| `src/step0_prepare_guide_records.py` | 103-111 | How a point gets its ID: K or S, then the number of the bullet. |
| `src/step0_prepare_guide_records.py` | 206-217 | The checks before the file is written: the counts, and each text exactly in the guide. |
| `src/step0_prepare_guide_records.py` | 220-228 | `main`: on an error, "Step 0 failed. No file is written. Cause: ..."; else it writes the file. |
| `src/check_guide_records.py` | 1-5 | The second script does not use the code of step 0. |
| `src/check_guide_records.py` | 76-77 | Each of the 408 texts is exactly in the guide. |
| `src/check_guide_records.py` | 82-85 | The other direction: the 240 bullets of Section 6 are the 240 points, in sequence. |
| `src/check_guide_records.py` | 101-102 | The points agree with the file for people. |
| `reference/guide-records.json` | (one record) | A point record, for example `1.4-K2` (diagram 03 uses it: `03-make-diagram.py`, 44). |
| `src/steps.py` | 23-25, 35-41 | The program loads the records once and gives them to the writer and the checker. |
| `src/step2_write.py` | 119-131 | The slice that the writer gets: story, task statement with the point marked (`>>>`), technologies. |
| `src/step2_write.py` | 19-21 | `plain`: the backslash of the guide format is removed. |
| `src/step4_check_model.py` | 55-64 | `guide_core`: the same guide text for each call, so it can be cached. |
| `src/step4_check_model.py` | 95-114 | `FeatureSearch`: code searches a feature name in all texts of the records. |
| `src/step1_plan.py` | 77-112 | `check_records`: step 1 checks the parts it reads again. |
| `src/control.py` | 698-702 | A new point of the owner must be in the task statement, by the records. |

## 7. A figure

The mechanism (boxes and arrows with verbs):

```
[exam-guide.md: Sections 4, 5, 6, 9, 17; 39 page marks]
        | the script reads it, leaves out the page marks
        v
[step 0 script: copies each text, gives each point an ID (1.4-K2)]
        | checks 5 counts and that each of 408 texts is exactly in the guide
        |------ a check fails --> [no file; the cause is named]
        v
[guide-records.json: 1 file, 408 texts, ~8,000 words]
        ^ checked by: [second script, 41 of 41] [independent reviewer, no errors] [copy vs official PDF, 0 differences, 13 Oct]
        | code takes a slice by ID
        v
[steps 1, 2, 4, 7, 8 and the control]  -->  [a model call gets only its slice; no model reads the file]
```

Facts behind each label:
- "Sections 4, 5, 6, 9, 17": E5. "39 page marks": section 4, E7, E8.
- "copies each text": O2. "gives each point an ID": E9, E10.
- "5 counts": E13. "408 texts exactly in the guide": E14, section 4.
- "no file; the cause is named": E2.
- "1 file, 408 texts, ~8,000 words": E3, E16, section 4.
- "second script, 41 of 41": E21, E22. "independent reviewer, no errors": E25. "copy vs official PDF, 0 differences": E28, E29 (word for word, not character for character), and conflict X1.
- "code takes a slice by ID": O3. "steps 1, 2, 4, 7, 8 and the control": E31 to E39.
- "a model call gets only its slice; no model reads the file": E41, but see conflict X4 for step 4.
- "runs one time for each version of the guide": O4 (a band above the figure, as in diagram 01).

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| X1 | Is check 1 (our copy against the original) done? | `docs/build-guide/step-0-...md`, 19 (L3): "The comparison of `reference/exam-guide.md` with the original, character for character, is not done." Diagram 03, line 166, popup `c1` (L3): who "Not done yet", "Result: not done yet." Box on the figure: tag "Not done yet" (`03-make-diagram.py`, 138). `docs/journal.md`, 279 (L4). | `academy/decisions/0027-...md`, 18 (L2, later): "The result on 13 October 2026: 11,157 words in each, and 0 places that differ." `HANDOFF.md`, 161 (L4): "Compared with the official PDF on 13 October 2026, word for word: 0 differences". |
| X2 | What check 1 is. | `docs/decisions/0028-...md`, 37 (L2): "A script compares `reference/exam-guide.md` with the original in the Claude project \"CPN Learning path\", character for character." | `academy/decisions/0027-...md`, 14, 16, 30 (L2, later): the original is the official PDF `academy/sources/exam-guide-v1.0-official.pdf`; "The script makes both files into one list of words"; "The script compares words, not spaces, line breaks, the order of table cells or the layout." So the check that was done is word for word, not character for character. |
| X3 | One file or several record files. | `docs/decisions/0017-...md`, 20, 24-25 (L2): "It makes checked record files of the guide in `reference/`." The 240 points: "This part is done: `reference/task-statements-and-points.md`"; the other records "will be one new file". Its status line (line 4) says only "accepted". `docs/diagrams/01-pipeline-overview.html`, 191, popup "0" (L3): "Puts the text of the exam guide into checked files." / "into record files with IDs, and a reviewer checks each record against the guide." / "It returns checked record files." | `docs/decisions/0028-...md`, 23, 38 (L2, later): "The script writes one file, `reference/guide-records.json`." / "`reference/task-statements-and-points.md` stays. It is a file for people." Code (L1): one output file `OUT` (`src/step0_prepare_guide_records.py`, 17). |
| X4 | Does each model call get only a small, different slice? | Diagram 03, line 166, popups `u2` and `u3` (L3): "Each model call needs a different part of the guide. Code selects that part by ID." / "The call gets only its slice. It does not read the file. So each call gets what it needs and no more". `docs/decisions/0028-...md`, 23 (L2): "gives only that slice to a model call". | `src/step4_check_model.py`, 55-58 (L1): step 4 gets "All 30 task statements with their 240 points, and the three lists of Section 17. The same text for each call", plus the 12 sample questions (lines 74-80). `docs/decisions/0032-...md`, 45 (L2): "That is about 5300 words." The diagram example (about 200 words) is true for the writer of step 2 only. (No model reads the file itself: this part agrees.) |
| X5 | Where the sample questions are used. | Diagram 03, line 166, popup `sq` (L3): "Before the first full run, the checker must pass all 12 sample questions. We also compare the first new questions with them." | Code (L1): step 2 gives 3 sample questions to the writer as examples (`src/step2_write.py`, 70-85), and step 4 gives all 12 to call 4b for rule B8 (`src/step4_check_model.py`, 74-80, decision 0055). The diagram does not name these uses. This is an omission, not a direct contradiction. |
| X6 | The backslash of 5 texts: open in the decision, decided in the code. | `docs/decisions/0029-...md`, 139 (L2): under "Not decided yet": "What to do with the 5 texts of the records file that have a backslash from the file format (review of step 0)." No later decision text found with "backslash" (search of `docs/decisions/`: only 0029 and 0030, line 90, an open item of rule B6). | `src/step2_write.py`, 19-21; `src/step4_check_model.py`, 84-87, 95-97; `src/step7_marking.py`, 32-35 (L1): code removes the backslash before the writer, the checker and the owner see the text. (Added in commits `eb05725` and `326c542`, 7 October 2026.) |
| X7 | Did the owner confirm the text of decision 0028? | `docs/decisions/0028-...md`, 5: "Text confirmed by the owner: 7 October 2026, after a summary of one line for each file" | same file, 66: "The owner approved a short form of this text. The owner did not confirm the full text." (Line 66 may be older than the status line. Both are L2 in one file.) |

Points (academy decision 0024): no conflict. The points in the popups of diagrams 01 and 03 are the same three points as the build guide table (section 3, T2).

## 9. Not found

1. No failure of step 0 in any source: no record of a wrong count, a text not found, or a second run. The Depth has no story of the step's own output going wrong. The stories in section 5 are about the design and the checks.
2. No run file of step 0. The run of 6 October 2026 came before the git repository (`docs/journal.md`, 312: "The folder is not a git repository."). The output of that run is recorded only in the journal (line 278). The file is unchanged since commit `8cc3a24` (O7).
3. No test in `tests/` for step 0 or for the check script (E47). The check script is the only automatic check.
4. Step 0 never ran for a second version of the guide, so "one time for each version" is not shown by a run.
5. The comparison with the PDF was not re-run by this agent (`pypdf` is not installed). The result is from academy decision 0027 only.
6. No source links lesson 16 of `docs/lessons.md` (the exact guide text field of the first build) to the design of step 0. Decisions 0017 and 0028 do not cite it. Also, the owner decided on 6 October 2026 that `docs/lessons.md` "is private history of the first build. It is not a source for the design." (`docs/journal.md`, 343, "6 October 2026, first session"). The file is not in the list of personal files of working rule 19, but the owner should decide if a page may quote it (fact M3).
7. No decision records the choice to remove the backslash (conflict X6).
8. No decision answers the review's suggestion of point 5.1-S1 for step 0 (story D5).
9. No Anthropic documentation page was read: step 0 makes no model call and uses no product feature. No dated copy in `academy/sources/` is needed for this part.
10. The answer of the owner to "if the original guide file is on the computer" (`docs/journal.md`, 311) is not recorded. Academy decision 0027 shows that the owner later gave the PDF.
