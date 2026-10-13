# Fact sheet: tab 2, step 1 "Plan the mock"

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `1cbae17` (branch `main`, clean).
- Levels of trust (academy decisions 0011, 0014, 0029): 1 = code, tests, data and run files. 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`. "Docs" = an outside documentation page. "L" = level.
- A path such as `docs/decisions/0048-...md` means the one file in `docs/decisions/` whose name starts with `0048-` (for 0027 and 0037: the file that starts with `00NN-the-`). Line numbers are for commit `1cbae17`.
- The step 1 tests ran on 14 October 2026 with no API key and no model call: `python3 -m unittest tests.test_step1_plan tests.test_point_groups` gives "Ran 48 tests ... OK" (39 in `tests/test_step1_plan.py`, 9 in `tests/test_point_groups.py`; count with `grep -c "def test"`).
- Files that this agent did not read (working rules 19 and 28, academy decision 0028): `marking/*.xlsx`, `responses.json` and all personal files of the owner, `claude-code-brand-kit/`, conversation transcripts. No model call, no API key, `src/run.py` not run.
- Scripts of this agent were in its scratchpad, not in the repository. They read files only. Each method is in section 4.

---

## 1. Overview facts (what the step does)

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| O1 | Before a model writes a question, code makes the plan: a list of 60 slots. | `docs/build-guide/step-1-plan-the-mock.md`, 9 | "Before a model writes a question, code makes the plan of the mock: a list of 60 slots." | 3 |
| O2 | Each slot says what one question must be. | same, 9 | "Each slot says what one question must be: the scenario, the task statement, one point of that task statement, the question type, and the number of answers to select. No model works in this step." | 3 |
| O3 | The same in the code. | `src/step1_plan.py`, 4-5 | "Code makes a list of 60 slots. No model works in this step. The seed controls each selection, so the same seed gives the same plan." | 1 |
| O4 | The decision that made step 1 (6 October 2026). | `docs/decisions/0009-...md`, 20 | "Option 1. Step 1 is the plan. Code makes a list of 60 slots for one mock. Each slot says what one question must be." | 2 |
| O5 | The rejected option: a model writes many questions first, and a later step selects 60. | `docs/decisions/0009-...md`, 15, 34 | "2. A model writes many questions first. A later step selects 60 of them for a mock." / "We rejected option 2 because its gaps show only at the end." | 2 |
| O6 | Status: built, made the plans of mocks 1 to 5, 7 to 9 October 2026. | `docs/build-guide/step-1-plan-the-mock.md`, 3 | "Status: built. The step made the plans of mocks 1 to 5, from 7 to 9 October 2026." | 3 |
| O7 | The plan dates in the run files agree: 2026-10-07 (mock 1), 2026-10-08 (mocks 2, 3), 2026-10-09 (mocks 4, 5). | `runs/mock-0N/plan.json`, field `date` | | 1 |

## 2. Explanation facts: the mechanism

### 2.1 Inputs, output, who does what

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| E1 | Who: code only. No model call. | `src/step1_plan.py`, 4; `docs/diagrams/02-step-1-plan-the-mock.html`, 177 (popup "S") | "No model works in this step." | 1 / 3 |
| E2 | The control calls step 1 when the mock has no plan file, and writes the plan one time. | `src/control.py`, 332-334 | `if not self._exists("plan.json"):` / `plan = self.steps.plan(self.mock, self.seed)` / `self._write_new(plan, "plan.json")` | 1 |
| E3 | A record is never written over (so the plan is never written over). | `src/control.py`, 94-99 | `"""Write a record. A record is never written over."""` | 1 |
| E4 | The real step gets the guide records, the mock number, the seed and the points of the earlier built mocks. | `src/steps.py`, 48-50 | `return step1_plan.make_plan(self.records, mock, seed, self.today(), earlier=step1_plan.earlier_points(self.mocks_folder, mock))` | 1 |
| E5 | The first run of a mock needs a seed from the owner's command. Later runs read the seed from the plan. | `src/run.py`, 28-33 | `seed = json.load(f)["seed"]` / `"Mock %d has no plan. Give --seed to make one."` | 1 |
| E6 | Inputs that the code reads from files: `reference/guide-records.json`, `data/point-groups.json`, `data/two-answer-points.json` (decision 0054), `data/mock-scenarios.json` (decision 0057), and `mocks/mock-NN.questions.json` of each lower built mock (decision 0050). | `src/step1_plan.py`, 24-26, 230-244, 270-271; `src/point_groups.py`, 28-29 | `TWO_ANSWER_POINTS = os.path.join(ROOT, "data", "two-answer-points.json")   # decision 0054` / `MOCK_SCENARIOS = os.path.join(ROOT, "data", "mock-scenarios.json")         # decision 0057` | 1 |
| E7 | The inputs as the diagram lists them (it names the guide records, the point groups, the earlier mocks, the mock number and the seed). | `docs/diagrams/02-step-1-plan-the-mock.html`, 177 (popup "IN") | "A seed. A seed is a number that controls the random selections." | 3 |
| E8 | Output: one file `runs/mock-NN/plan.json` with the top fields `mock`, `seed`, `guide_version`, `date`, `earlier_mocks`, `scenarios`, `table`, `slots`. | `src/step1_plan.py`, 481-485; `tests/test_step1_plan.py`, 167-168 | `return {"mock": mock, "seed": seed, "guide_version": ..., "date": date, "earlier_mocks": sorted(earlier), "scenarios": scenarios, "table": ..., "slots": slots}` | 1 |
| E9 | A slot has the fields `slot_id`, `scenario`, `task_statement`, `point`, `type`, `options`, `select`, `longest_may_be_correct`, `correct_letters`. | `src/step1_plan.py`, 440-443, 453, 463, 476; `tests/test_step1_plan.py`, 165-166 | `"type": "multiple_response" if many else "multiple_choice", "options": 5 if many else 4, "select": 2 if many else 1` | 1 |
| E10 | The first slot of mock 1 (real). | `runs/mock-01/plan.json`; `docs/build-guide/step-1-plan-the-mock.md`, 52 | `{"slot_id": "M1-S01", "scenario": 3, "task_statement": "2.5", "point": "2.5-K3", "type": "multiple_choice", "options": 4, "select": 1}` | 1 / 3 |
| E11 | The first slot of mock 5 (real, with the two later fields). | `runs/mock-05/plan.json` | `{"slot_id": "M5-S01", "scenario": 4, "task_statement": "1.6", "point": "1.6-K2", "type": "multiple_choice", "options": 4, "select": 1, "longest_may_be_correct": true, "correct_letters": ["B"]}` | 1 |
| E12 | The fields grew over the mocks: mock 1 has no `earlier_mocks`, `longest_may_be_correct` or `correct_letters`. Mocks 2 to 4 have `earlier_mocks` and `longest_may_be_correct`. Only mock 5 has `correct_letters`. | run files `runs/mock-0N/plan.json` (keys of the top object and of `slots[0]`) | Diagram 02 popup "OUT": "Mocks 1 to 4 have no such field." | 1 / 3 |
| E13 | Who uses the plan: step 2 writes one question for each slot; the later checks compare each question with its slot. | `docs/diagrams/02-step-1-plan-the-mock.html`, 177 (popup "OUT") | "Step 2 writes one question for each slot. The later checks compare each question with its slot." | 3 |
| E14 | The slot number is the question number of the finished mock. | `src/step1_plan.py`, 428-429; `docs/decisions/0027-the-...md`, 42 | "The slots get the numbers 1 to 60, group by group. The seed sets the sequence inside a group." | 1 / 2 |
| E15 | A new point of the owner (`new_point`) does not change `plan.json`. The control reads the point from the decisions. | `src/control.py`, 176-186; `docs/decisions/0027-the-...md`, 30 | "`plan.json` does not change, so the same seed still gives the same plan (decision 0039, item 7)." | 1 / 2 |

### 2.2 The rules of the plan, in the order of the code

The code has 9 numbered stages (`src/step1_plan.py`, comments 285, 302, 309-319, 390, 426-429, 446, 454). Diagram 02 shows them as 5 parts.

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| R1 | Domain counts 16, 11, 12, 12, 9: the weights 27, 18, 20, 20, 15 per cent of 60, rounded. Code stops if the rounded counts are not these. | `src/step1_plan.py`, 45, 118-125; `docs/decisions/0027-the-...md`, 23, 68 | `DOMAIN_COUNTS = {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}   # decision 0027, item 1` / "For 60 questions they give 16.2, 10.8, 12, 12 and 9." | 1 / 2 |
| R2 | 4 scenarios, 15 questions each. 15 is "equal parts", not from the guide. | `src/step1_plan.py`, 41-43; `docs/decisions/0027-the-...md`, 70 | "The guide gives no number. The plain reason: equal parts." | 1 / 2 |
| R3 | Only the 11 sets of 4 scenarios in which each question fits a primary domain of its scenario. The 4 sets not used: 1-2-3-4, 1-2-5-6, 2-3-5-6, 2-4-5-6. | `src/step1_plan.py`, 178-182; `docs/decisions/0027-the-...md`, 24; `tests/test_step1_plan.py`, 41 | "It does not use these 4 sets: scenarios 1, 2, 3, 4. Scenarios 1, 2, 5, 6. Scenarios 2, 3, 5, 6. Scenarios 2, 4, 5, 6." | 1 / 2 |
| R4 | This is a difference from the exam, which can use all 15 sets. | `docs/build-guide/step-1-plan-the-mock.md`, 24; `docs/decisions/0027-the-...md`, 69 | "This is a difference from the exam, which can use all 15 sets." | 3 / 2 |
| R5 | The guide quote for the exam: 4 of 6 scenarios at random. | `docs/decisions/0027-the-...md`, 69; diagram 02 popup "1" | "During the exam, 4 scenarios are presented and picked at random from the full set of the 6 scenarios below." | 2 |
| R6 | The example for the limit: no scenario of 1, 2, 3, 4 has Domain 4 as a primary domain. | diagram 02, 177 (popup "1") | "none of the scenarios 1, 2, 3 and 4 has Domain 4 as a primary domain, but a mock needs 12 questions of Domain 4. Those questions would be forced into a story that does not fit them." | 3 |
| R7 | Mocks 1 and 2: the seed selected the set. Mocks 3 to 5: the owner fixed the set in `data/mock-scenarios.json`. The seed still sets the sequence of the 4 groups. A fixed set outside the 11 stops the step. | `src/step1_plan.py`, 289-300; `data/mock-scenarios.json`, 4-6; `docs/decisions/0057-...md`, 23-28 | `# Decision 0057: the owner fixed the set of mocks 3 to 5. The seed still` / `# sets the sequence of the 4 groups.` | 1 / 2 |
| R8 | The table of scenarios and domains: code takes the most even table (smallest sum of squares). The seed selects between equal tables. | `src/step1_plan.py`, 302-307; `docs/decisions/0027-the-...md`, 37 | `# 2. The most even table. The seed selects one when two are equal.` | 1 / 2 |
| R9 | Each of the 30 task statements gets at least 1 question. Share equal in a domain, but no more than its number of point groups (decision 0048). At most one extra question. | `src/step1_plan.py`, 309-314, 335-344; `docs/decisions/0048-...md`, 28-29 | "But a task statement gets no more questions than its number of groups." | 1 / 2 |
| R10 | Task statements 3.3 and 4.2 each have one group, so each gets 1 question (mocks 2 to 5). | `tests/test_step1_plan.py`, 68; `docs/build-guide/step-1-plan-the-mock.md`, 23; computed (section 4.3) | `self.assertEqual(per_ts["3.3"], 1)` / "Example: task statement 3.3 has one group, so it gets 1 question." | 1 / 3 |
| R11 | "Possible" is a matching of task statements to free groups, checked by code. | `src/step1_plan.py`, 185-205; `docs/decisions/0048-...md`, 31 | "Code checks this with a matching of task statements to groups. No model makes this check." | 1 / 2 |
| R12 | No two slots of one mock get points of the same group. Code checks it again at the end and stops if two slots share a group. | `src/step1_plan.py`, 319, 477-480; `src/point_groups.py`, 80-88 | `raise PlanError("Two slots are in one group: %s" ...` | 1 |
| R13 | The groups file: 95 groups, 240 points, each point in one group. 65 groups have 2 or more points, 30 have 1. The largest group (G057) has 12 points. | `data/point-groups.json`; `src/point_groups.py`, 3-5 | `python3 src/point_groups.py check` prints "The groups file is correct: 95 groups, 240 points." | 1 |
| R14 | Point order: the seed shuffles, then code moves first the groups that earlier built mocks used least (0050), then inside a group the point that they used less (0056). | `src/step1_plan.py`, 371-376 | `pool.sort(key=lambda p: (use.get(of[p["id"]]["id"], 0), point_use.get(p["id"], 0)))` | 1 |
| R15 | The earlier mocks are only built mocks: a mock counts when `mocks/mock-NN.questions.json` exists. | `src/step1_plan.py`, 230-244; `docs/decisions/0050-...md`, 21 | "A mock that is not built does not count." | 1 / 2 |
| R16 | The seed decides which scenario of the table each question goes to. | `src/step1_plan.py`, 390-398 | `# 5. The seed decides which scenario each question goes to.` | 1 |
| R17 | 2 multiple-response slots in each scenario, only on a point of `data/two-answer-points.json` (78 points). If a scenario has fewer than 2, code swaps two questions of one domain between scenarios. If no swap, the step stops. | `src/step1_plan.py`, 44, 399-423, 426-437; `docs/decisions/0054-...md`, 22-23, 31 | `MULTIPLE_RESPONSE_PER_SCENARIO = 2   # a guess with no source (decision 0027)` | 1 / 2 |
| R18 | The number of multiple-response questions (8) is a guess with no source. All 12 sample questions of the guide are multiple-choice. | `docs/decisions/0027-the-...md`, 72; diagram 02 popup "5" | "The number 8 is a guess of the assistant. It has no source." | 2 / 3 |
| R19 | `longest_may_be_correct`: true on 13 of the 52 one-answer slots and 3 of the 8 two-answer slots (the chance numbers). Step 3 rule A12 checks the other slots. | `src/step1_plan.py`, 46-48, 446-453; `docs/decisions/0053-...md`, 21 | `LONGEST_MAY_BE_CORRECT = {1: 13, 2: 3}` | 1 / 2 |
| R20 | `correct_letters` (from mock 5): each of A to D is the answer of 13 of the 52 one-answer slots; 16 answers of the 8 two-answer slots spread over A to E. | `src/step1_plan.py`, 454-476; `docs/decisions/0070-...md`, 21 | "Each of A, B, C and D is the answer of 13 of the 52 slots with one answer." | 1 / 2 |
| R21 | Reproducibility: the step uses only `random()` of Python, because the Python documentation guarantees the same sequence only for `random()`. A test checks that no other function of `random` is used. | `src/step1_plan.py`, 55-71; `tests/test_step1_plan.py`, 187-192; `docs/journal.md`, 181 | "The Python documentation guarantees the same sequence of random() for the same seed in later versions of Python. It does not guarantee it for choice, shuffle and sample." | 1 / 4 |
| R22 | Docs check of R21 (Python, not an Anthropic product): page "random", section "Notes on Reproducibility", https://docs.python.org/3/library/random.html, read live on 14 October 2026. It guarantees: "The generator's random() method will continue to produce the same sequence when the compatible seeder is given the same seed." No dated copy saved (this agent may write only this sheet). | live page | "Most of the random module's algorithms and seeding functions are subject to change across Python versions, but two aspects are guaranteed not to change" | Docs |
| R23 | When the step stops: a guide record is missing or not valid, a count does not add up, or the groups allow no plan. It names the cause and writes no plan. | `src/step1_plan.py`, 51-52, 77-125, 345-364; `docs/build-guide/step-1-plan-the-mock.md`, 33 | "the step stops with an error that names the cause. It writes no plan." | 1 / 3 |
| R24 | The command line also refuses to write over a plan. | `src/step1_plan.py`, 497-500; `tests/test_step1_plan.py`, 362 | `print("A plan exists already: " + path)` | 1 |

### 2.3 Why code, not a model

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| W1 | The counts must hold each time; a model can make an error in a count. | `docs/build-guide/step-1-plan-the-mock.md`, 37 | "The counts of a mock must hold each time. A model that makes the plan can make an error in a count." | 3 |
| W2 | The same reason in the decision, with the guide quote 1.4-K2. | `docs/decisions/0009-...md`, 24 | "The counts of a mock must hold each time. ... So code makes the plan, not a model." | 2 |
| W3 | The work is known before it starts, so a fixed plan fits (1.6-S1, 1.6-K1). | `docs/decisions/0009-...md`, 26; build guide, 39 | "the work of a mock is known before it starts, so the program can fix the plan before the writing starts" | 2 / 3 |
| W4 | The guide does not cover a list of slots or the balance of scenarios against weights. These come from the form of the exam (Sections 3, 4, 5, 9). | build guide, 41; `docs/decisions/0009-...md`, 28 | "The guide does not cover two parts of this step: a list of slots before the writing, and the balance of the 4 scenarios against the domain weights." | 3 / 2 |

## 3. Task statements and points of the step (build guide table)

Source: `docs/build-guide/step-1-plan-the-mock.md`, lines 58-64 (L3). The point texts agree with `reference/guide-records.json` (checked by script on 14 October 2026).

| Point | Line | Task statement | How the step uses it (exact, from the table) |
|---|---|---|---|
| 1.4-K2 | 62 | 1.4: Implement multi-step workflows with enforcement and handoff patterns | "Written for an agent workflow. Here: a count must always hold, so code, not a model, makes the plan." |
| 1.6-K1 | 63 | 1.6: Design task decomposition strategies for complex workflows | "Written for a sequence of model calls. Here only one idea is used: the work of a mock is known before it starts. Step 1 itself has no model call." |
| 1.6-S1 | 64 | 1.6: Design task decomposition strategies for complex workflows | "Written for the choice of a decomposition, with multi-aspect reviews and open-ended investigations as examples. Here it is used as 1.6-K1 is used." |

Guide texts (`reference/guide-records.json`):
- 1.4-K2: "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate"
- 1.6-K1: "When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings"
- 1.6-S1: "Selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks"

Checks of the points in other files:
- Diagram 02 (`docs/diagrams/02-step-1-plan-the-mock.html`, line 177, popup "S"): 1.4-K2, 1.6-K1, 1.6-S1. The same three. Popups "1", "2", "5" also cite "Section 5", "Section 4", "Section 3" of the guide as facts about the exam, "not a task statement point". No conflict (L3).
- Diagram 01 (`docs/diagrams/01-pipeline-overview.html`, line 191, step "1"): 1.4-K2, 1.6-S1, 1.6-K1; box: "Exam guide: task statements 1.4 and 1.6". No conflict (L3).
- Decision 0009, line 38: "1.4-K2, 1.6-S1, 1.6-K1". Decision 0027, line 98: "none. The decision uses Sections 3, 4, 5 and 9 of the guide." (L2)
- The page `academy/pages/behind-the-mocks.html`, line 50: closed heading "code · task statements 1.4, 1.6". Agrees.
- The tab 2 sample Fig. 2 cites 1.1-K3 for this mechanism: see conflict C1.
- Fact for the links: in `data/point-groups.json`, 1.6-K1 and 1.6-S1 are in group G003 "Fixed sequence against a plan that adapts" with 1.1-K3, 1.6-K3, 1.6-S3. 1.4-K2 is in G016 "Code enforcement (hooks, gates) against prompt guidance" (7 points). Both groups are in all 5 built mocks (section 4.5). (L1)

## 4. Numbers, per mock, with method

### 4.1 Method

Script 1 (plans and built mocks), run on 14 October 2026 with `python3 -I count1.py ~/ccar-f-mock-generator`. It reads `runs/mock-0N/plan.json`, `mocks/mock-0N.questions.json`, `mocks/mock-0N.answers.json`, `data/point-groups.json`, `data/two-answer-points.json` and `reference/guide-records.json` with `json`. No model call.

```python
P = rd("runs/mock-%02d/plan.json" % m); S = P["slots"]
of = {p: g["id"] for g in groups["groups"] for p in g["points"]}
dom = {ts["id"]: ts["domain"] for ts in records["task_statements"]}
len(S); Counter(dom[s["task_statement"]] for s in S); Counter(s["scenario"] for s in S)
len({s["task_statement"] for s in S}); Counter(Counter(s["task_statement"] for s in S).values())
len({of[s["point"]] for s in S}); groups with Counter(of[s["point"]]) > 1
Counter(s["select"] for s in S); sum(s["point"] in two for s in S if s["select"] == 2)
sum(s["longest_may_be_correct"] for s in S if s["select"] == k)        # k = 1, 2
built points: [q["point"] for g in B["groups"] for q in g["questions"]]   # B = mocks/mock-0N.questions.json
```

Script 2 (letters and the longest option of the built mocks): for each question of `mocks/mock-0N.questions.json`, the correct letters come from `mocks/mock-0N.answers.json` (`correct`). "Longest is correct" = a correct option has the largest number of characters of `text` (ties count).

Script 3 (replay): `step1_plan.make_plan(records, m, plan["seed"], plan["date"], earlier=step1_plan.earlier_points("mocks", m))` with the code of today, and for mocks 1 and 2 also with the code of the commit of the plan (`git archive a6067fc src reference` and `git archive 793d277 src data reference mocks`, extracted in the scratchpad). Compare field by field. No step writes a file. No model call.

Read-only commands of the repository, run on 14 October 2026: `python3 src/point_groups.py plan runs/mock-01/plan.json`, `python3 src/point_groups.py check`, `python3 src/point_groups.py seeds 2000` (13.9 s), `python3 src/point_groups.py series 20`.

### 4.2 Per mock (plans)

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Method |
|---|---|---|---|---|---|---|
| Seed | 366341 | 167622 | 788092 | 445312 | 203660 | `plan.json` field `seed` |
| Date of the plan | 2026-10-07 | 2026-10-08 | 2026-10-08 | 2026-10-09 | 2026-10-09 | field `date` |
| `earlier_mocks` | (no field) | [1] | [1, 2] | [1, 2, 3] | [1, 2, 3, 4] | field `earlier_mocks` |
| Scenarios, in the sequence of the groups | 3, 1, 2, 5 | 3, 4, 5, 6 | 6, 1, 4, 2 | 6, 3, 1, 4 | 4, 2, 5, 1 | field `scenarios` |
| Who selected the set | seed | seed | owner (0057) | owner (0057) | owner (0057) | `data/mock-scenarios.json` has mocks 3, 4, 5 |
| Slots | 60 | 60 | 60 | 60 | 60 | `len(slots)` |
| Domains 1-5 | 16, 11, 12, 12, 9 | same | same | same | same | domain of each slot's task statement |
| Questions per scenario | 15 each | 15 each | 15 each | 15 each | 15 each | Counter of `scenario` |
| Task statements covered | 30 | 30 | 30 | 30 | 30 | distinct `task_statement` |
| Task statements with 1 / 2 / 3 questions | 3 / 24 / 3 | 5 / 20 / 5 | 5 / 20 / 5 | 5 / 20 / 5 | 5 / 20 / 5 | Counter of the counts |
| Questions of 3.3 / 4.2 | 2 / 2 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | count `task_statement` |
| Distinct points | 60 | 60 | 60 | 60 | 60 | distinct `point` |
| Distinct groups (ideas) | 41 | 60 | 60 | 60 | 60 | distinct group of `point` |
| Groups with 2 or more slots | 12 | 0 | 0 | 0 | 0 | same; also `python3 src/point_groups.py plan runs/mock-01/plan.json` prints "12 groups have two or more slots of the plan" |
| A scenario with 12 questions of one domain | sc. 5, D4 | none (max 10) | sc. 6, D4 | sc. 6, D4 and sc. 4, D3 | sc. 5, D4 | field `table` |
| Multiple-choice / multiple-response | 52 / 8 | 52 / 8 | 52 / 8 | 52 / 8 | 52 / 8 | Counter of `select` |
| Multiple-response slots on a two-answer point | 3 of 8 | 8 of 8 | 8 of 8 | 8 of 8 | 8 of 8 | `point` in `data/two-answer-points.json` |
| `longest_may_be_correct` true (1-answer / 2-answer slots) | (no field) | 13 / 3 | 13 / 3 | 13 / 3 | 13 / 3 | sum of the field |
| `correct_letters` (1-answer slots) | (no field) | (no field) | (no field) | (no field) | A 13, B 13, C 13, D 13 | Counter |
| `correct_letters` (2-answer slots) | | | | | A 4, B 3, C 3, D 3, E 3 | Counter |
| Plan points that differ from the built mock | 5 | 0 | 1 | 1 | 4 | plan `point` against built `point`, slot by slot |
| Plan points already used in an earlier built mock | | 7 | 13 | 31 | 48 | plan point in the points of `mocks/mock-0K` for K < N |
| ... of them with an unused point of the same group and the same task statement | | 7 | 0 | 0 | 0 | the order of decision 0056 (after mock 2) |

Notes:
- The 5 / 1 / 1 / 4 differences come from owner decisions: mock 1 has 5 rewrites with a new point; mock 3 D001, mock 4 D004 and mock 5 D001-D003 and D006 are `new_point` (see `academy/facts/step-5.md`, section 4.4). Not computed again here for each decision.
- Mock 1 plan: 3.3 got 2 questions (M1-S33 3.3-S1 and M1-S43 3.3-S2), both group G042, and 1.6 got 3 questions with 2 groups. Both are not possible after decision 0048.

### 4.3 Fixed numbers (code and data)

| Number | Meaning | Source | How a script reads it |
|---|---|---|---|
| 60, 15, 4 | slots, questions per scenario, scenarios | `src/step1_plan.py`, 41-43 | regex `^QUESTIONS = (\d+)`, `^PER_SCENARIO = (\d+)`, `^SCENARIOS_IN_MOCK = (\d+)` |
| 16, 11, 12, 12, 9 | domain counts | `src/step1_plan.py`, 45 | regex `^DOMAIN_COUNTS = (.*)` |
| 27, 18, 20, 20, 15 | domain weights (%) | `reference/guide-records.json` | `[d["weight"] for d in records["domains"]]` |
| 2 | multiple-response slots per scenario ("a guess with no source") | `src/step1_plan.py`, 44 | regex `^MULTIPLE_RESPONSE_PER_SCENARIO = (\d+)` |
| 13, 3 | slots where the longest option may be correct | `src/step1_plan.py`, 48 | regex `^LONGEST_MAY_BE_CORRECT = (.*)` |
| 30, 240 | task statements, points | `reference/guide-records.json` | `len(task_statements)`, sum of `len(points)` |
| 95, 65, 30 | groups; groups with 2+ points; groups with 1 point | `data/point-groups.json` | `len(groups)`; count `len(points) > 1` |
| 78 | two-answer points | `data/two-answer-points.json` | `len(points)` |
| 11 of 15 | sets of 4 scenarios with a table | `step1_plan.scenario_sets(records, counts)` | computed: 11; the 4 others (1,2,3,4), (1,2,5,6), (2,3,5,6), (2,4,5,6) |
| 9 of 11 | sets where one scenario gets 12 questions of one domain | `step1_plan.tables` + `_squares` | computed; agrees with `docs/decisions/0051-...md`, 23 "This happens in 9 of the 11 sets." |
| 6 of 11 | sets with two most even tables | same | computed: (1,2,3,5), (1,2,3,6), (1,2,4,5), (1,3,4,5), (1,3,5,6), (2,3,4,5). See conflict C3. |
| 2 | groups of 1.5, of 1.6, of 5.2 | `data/point-groups.json` + records | distinct groups of the points of each task statement |
| 1 | groups of 3.3 and of 4.2 | same | same |
| 2000 of 2000 | seeds of `seeds 2000` that give a plan today | `python3 src/point_groups.py seeds 2000` | prints "Seeds: 2000. Plans: 2000. Failed: 0." |

### 4.4 Scenarios over the 5 mocks

| Scenario | Mocks | Count |
|---|---|---|
| 1. Customer Support Resolution Agent | 1, 3, 4, 5 | 4 |
| 2. Code Generation with Claude Code | 1, 3, 5 | 3 |
| 3. Multi-Agent Research System | 1, 2, 4 | 3 |
| 4. Developer Productivity with Claude | 2, 3, 4, 5 | 4 |
| 5. Claude Code for Continuous Integration | 1, 2, 5 | 3 |
| 6. Structured Data Extraction | 2, 3, 4 | 3 |

Method: field `scenarios` of the 5 plans. Agrees with `docs/decisions/0057-...md`, 33 ("scenarios 1 and 4 come 4 times, and scenarios 2, 3, 5 and 6 come 3 times") and diagram 12. (L1)

### 4.5 Ideas over the 5 mocks

| Mocks that have the idea | Built mocks (real) | Plans (before new points) | Simulation of decision 0050 (with the rule) | `series 20` today (with the rule) | `series 20` today (without) |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0.0 | 5.2 |
| 1 | 1 | 1 | 1.9 | 2.0 | 12.8 |
| 2 | 35 | 36 | 34.5 | 35.1 | 18.0 |
| 3 | 32 | 32 | 31.4 | 29.6 | 18.9 |
| 4 | 17 | 18 | 16.1 | 17.3 | 20.9 |
| 5 | 10 | 8 | 11.1 | 10.9 | 19.1 |
| 2 to 4 | 84 | 86 | 82 | 82.0 | |

- Method (real): the group of each `point` of `mocks/mock-0N.questions.json`; count the mocks per group over the 95 groups. Simulation: `docs/decisions/0050-...md`, 36-41 (table) and 43. Today: `python3 src/point_groups.py series 20` (the code and mock 1 of today, so it can differ from the table of 0050).
- The idea in 1 mock: G052 "argument-hint asks for missing arguments" (1 point).
- The 10 ideas in all 5 mocks: G001, G002, G003, G016, G017, G020, G031, G042, G057, G064. G003 holds 1.6-K1 and 1.6-S1; G016 holds 1.4-K2 (the points of step 1 itself).
- Mock 1 built has 7 questions in G003 or G016 (M1-S08, S13, S14, S18, S21, S25, S30). Mocks 2 to 5 have one of each.

### 4.6 Patterns in the set of 60 (built mocks)

| Number | Mock 1 | Mock 2 | Mock 3 | Mock 4 | Mock 5 | Method |
|---|---|---|---|---|---|---|
| Correct letter of the 52 one-answer questions | A 10, B 17, C 7, D 18 | A 11, B 13, C 15, D 13 | A 12, B 12, C 18, D 10 | A 8, B 8, C 14, D 22 | A 13, B 13, C 13, D 13 | `correct` in `mocks/mock-0N.answers.json` |
| Correct letters of the 8 two-answer questions | A 3, B 4, C 6, D 2, E 1 | A 6, B 2, C 2, D 4, E 2 | A 3, B 3, C 2, D 5, E 3 | A 5, B 2, C 2, D 2, E 5 | A 4, B 3, C 3, D 3, E 3 | same |
| Longest option is correct (1-answer, by characters, ties count) | 37 of 52 | 11 | 11 | 5 | 12 | script 2 |
| Longest option is correct (2-answer) | 6 of 8 | 2 | 3 | 1 | 3 | script 2 |
| Mock 5 built letters equal to the plan's `correct_letters` | | | | | 60 of 60 | compare per slot |

Checks: decision 0070, line 10: "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. ... Mock 1 had B 17 times and C 7 times." Agrees. Decision 0053, line 10: "37 of the 52 ... In the 8 questions with 2 answers, the longest option is correct in 6." Agrees (ties counted; strict longest: 33; by words with ties: 30). See conflict C4.

### 4.7 Replay of the plans (does the same seed give the same plan?)

| Mock | Today's code and today's `mocks/` | Code of the plan's commit |
|---|---|---|
| 1 | scenarios and table the same; 59 of 60 points differ | identical plan (code of `a6067fc`, 7 October 2026) |
| 2 | scenarios and table the same; 19 of 60 points differ | identical plan (code and data of `793d277`, 8 October 2026 16:20) |
| 3 | all slot fields the same (only `correct_letters` is new) | not needed |
| 4 | all slot fields the same (only `correct_letters` is new) | not needed |
| 5 | identical in each field | not needed |

- Cause for mock 1: the groups rule (decisions 0047, 0048) came after the plan. Cause for mock 2: the point order of decision 0056 (commit `ab70bd4`, 8 October 2026 20:22) came after the plan (commit `793d277`, 16:20). Decision 0056, line 34, says so: "seed 167622 no longer makes it again. The stored plan stays the record of mock 2." (L1, L2)
- Git history of `src/step1_plan.py`: 10 commits from `ba5b572` (7 October 2026, "Build step 1, the plan of a mock, with tests") to `a74fccd` (9 October 2026, "balanced correct letters for mock 5"). Method: `git log --format="%h %ad %s" --date=iso -- src/step1_plan.py`. (L1)
- Each `runs/mock-0N/plan.json` has exactly one commit in `git log` (written one time). (L1)

## 5. Stories for the Depth

Sources searched: decisions 0009, 0027, 0037 (item 14 via 0027), 0045 to 0057, 0070, 0078; `docs/journal.md` (grep "step 1", "plan", "seed", "point group", "0047", "0048", "0050", "0057", "twin"); `docs/lessons.md` (the first build only); `docs/reviews/M1-round1-second-review-notes.md`, `M1-round2-second-review.md`; `HANDOFF.md`; diagrams 02, 11, 12. Five stories found. Story (a) is the strongest: it starts with a real failure in a built mock and ends with code and a test.

### Story (a): mock 1 got repeats from two points on one idea, so the plan got point groups

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| A1 | The cause named by the second review of mock 1: twin points, and the plan selects at random. | `docs/reviews/M1-round1-second-review-notes.md`, "The probable causes", 83 | "**Twin points.** The guide has pairs of points on one idea ... The plan selects points at random, so it selects twins. The writer of one slot does not see the other slot." | 4 |
| A2 | The review says these causes are an opinion. | same, 89 | "These causes are the opinion of the assistant. It did not see the plan, the code or the records of step 6." | 4 |
| A3 | The known limits of mock 1 that came from the plan. | `docs/decisions/0046-...md`, Decision, 27-29 | "M1-S33-T1 and M1-S43-T1 \| The same scene ... Twin points 3.3-S1 and 3.3-S2." / "M1-S38-T2 and M1-S45-T2 \| ... Twin points 3.4-K4 and 5.4-S1, in two different task statements." | 2 |
| A4 | The list of changes before mock 2: changes 1 and 2 are about the plan. | `docs/decisions/0046-...md`, 33-34 | "1. Twin points: two points of one task statement often describe one idea, and the plan selects them at random." / "2. Twin points also exist across task statements (new)." | 2 |
| A5 | The reason why another rewrite does not help. | `docs/decisions/0046-...md`, Reason, 43 | "The three weaknesses come from the plan and from missing rules, so another rewrite on the same plan can repeat them." | 2 |
| A6 | The two options: groups in the plan, or step 6 finds repeats later. | `docs/decisions/0047-...md`, Options, 14-15 | "1. A file that groups the 240 points by idea, and a rule of step 1: no two slots of one mock get points of the same group." / "2. No change of the plan. Step 6 finds the repeats later." | 2 |
| A7 | The reason for option 1. | `docs/decisions/0047-...md`, Reason, 31 | "The plan is code, so code can prevent this before any question is written. A check after the writing (step 6) costs a rewrite, and it compares only one scenario." | 2 |
| A8 | The owner added a test against mock 1. | `docs/decisions/0047-...md`, 25, 39 | "The rule must reject it and name those pairs." / "The owner agreed, and added the test against mock 1 and the form of the table for the confirmation." | 2 |
| A9 | The test result: 9 of 11 known pairs caught, and one new group found. | `docs/journal.md`, "8 October 2026, later session", 108 | "The test against mock 1: the rule rejects the plan of mock 1. It catches 9 of the 11 known pairs. ... It also finds S12 with S20 and S22 (generic error messages), which no earlier review listed." | 4 |
| A10 | The test in code. | `tests/test_point_groups.py`, 115-124 | `def test_the_rule_rejects_the_plan_of_mock_1_and_names_the_pairs(self):` | 1 |
| A11 | The run file today: 12 groups have 2 or more slots of the mock 1 plan (example G042: M1-S33 3.3-S1, M1-S40 3.1-K1, M1-S43 3.3-S2). | command `python3 src/point_groups.py plan runs/mock-01/plan.json`; build guide, 56 | "12 groups have two or more slots of the plan:" | 1 / 3 |
| A12 | Mocks 2 to 5: 0 groups with 2 or more slots (section 4.2). | run files | | 1 |
| A13 | Mock 1 did not change. | `docs/decisions/0047-...md`, 27 | "7. Mock 1 does not change. The rule applies to new plans." | 2 |
| A14 | One repeat of mock 1 had a different cause: 12 questions of Domain 4 in scenario 5. The owner decided no new rule, because the groups prevent the harm. | `docs/decisions/0051-...md`, 23, 25-30, 32 | "The points 4.4-K1 and 4.4-K4 are now in one group, so no mock gets both. A scenario with 12 questions of Domain 4 still gets 12 different ideas." | 2 |
| A15 | Any limit below 12 removes sets: 10 or 11 leaves 2 of 11 sets and never uses scenario 2. | `docs/decisions/0051-...md`, 29-30 | "\| 11 or 10 \| 2 of 11: 1-4-5-6 and 3-4-5-6 \| Scenario 2 \|" | 2 |

### Story (b): the groups rule could never make a plan

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| B1 | The rule of 0047 failed for every seed. | `docs/decisions/0048-...md`, Question, 12, 14-15 | "With the draft of `data/point-groups.json`, that rule can never make a plan:" / "Task statement 3.3 is one group, because its 6 points have one correct answer (a rules file with a path)." / "A script ran the rule over 2000 seeds: each seed failed." | 2 |
| B2 | The journal says the same. | `docs/journal.md`, 110 | "The rule of decision 0047 could not make a plan: task statement 3.3 is one group, and Domain 1 failed for each of 2000 seeds." | 4 |
| B3 | The fix: a cap, extra questions in the order of the seed, and a matching. | `docs/decisions/0048-...md`, Decision, 28-31 | "1. **The cap.** ... a task statement gets no more questions than its number of groups." / "4. **\"Possible\"** means: each task statement can still get its count of points, each from a different free group. Code checks this with a matching of task statements to groups. No model makes this check." | 2 |
| B4 | The plain reason. | `docs/decisions/0048-...md`, Reason, 36 | "So the count must follow the groups, not the groups the count." | 2 |
| B5 | The rejected option: smaller groups, which miss a known pair. | `docs/decisions/0048-...md`, 22 | "2. Smaller groups, so that each task statement has enough groups. Then the groups do not catch the known pair M1-S33 and M1-S43 (decision 0046)." | 2 |
| B6 | The independent review of the code found a real bug. | `docs/decisions/0048-...md`, How we decided, 48 | "The main fix: code gave the extra questions one domain at a time and never went back, so it could stop although a plan existed. Now it searches over all domains together." | 2 |
| B7 | The cost: some points never get a question. | `docs/decisions/0048-...md`, 40 | "with the draft of the groups, 11 points never got a question ... After the second review of the groups, the number is 15." | 2 |
| B8 | The code of the fix: `_possible` (a matching with augmenting paths) and `_extras` (backtracking over all domains). | `src/step1_plan.py`, 185-227 | `"""True if each task statement can still get need[ts] points, each from a different group that is not in used (decision 0048). A matching of task statements to groups: each group serves at most one question."""` | 1 |
| B9 | A test that the extras go back to an earlier domain (the bug of B6). | `tests/test_step1_plan.py`, 335 | `def test_extras_go_back_to_an_earlier_domain(self):` | 1 |
| B10 | Today: 2000 of 2000 seeds give a plan. | `python3 src/point_groups.py seeds 2000`, run 14 October 2026 | "Seeds: 2000. Plans: 2000. Failed: 0." | 1 |

### Story (c): mock 2 repeated mock 1, so step 1 spreads the ideas and prefers an unused point

| # | Fact | Source, section, lines | Exact quote | L |
|---|---|---|---|---|
| C-1 | Before mock 2: the number of mocks forces shared ideas. | `docs/decisions/0049-...md`, 26-27 | "5 mocks have 300 slots. The guide has 95 groups (ideas). So each idea comes in about 3 of the 5 mocks." / "A rule \"no idea in two mocks\" is not possible." | 2 |
| C-2 | The owner's words for 0050. | `docs/decisions/0050-...md`, How we decided, 54 | "The owner said: \"It is getting so so complicated.\" ... The owner asked: \"Is there no simple way to ensure that similar questions are spread out between mocks?\" The assistant suggested this one rule in step 1, in code only." | 2 |
| C-3 | The rule: the least-used groups first. | `docs/decisions/0050-...md`, 21-23 | "Before step 1 plans mock N, code reads the points of each built mock with a lower number" | 2 |
| C-4 | A correction of the assistant. | `docs/decisions/0050-...md`, 56 | "The assistant first said that each idea then comes in 3 or 4 of the 5 mocks. The simulation shows that this was too exact" | 2 |
| C-5 | After mock 2: 17 repeats of mock 1. | `docs/decisions/0056-...md`, Question, 10 | "17 questions of mock 2 repeat mock 1: 13 strong (the same scene, the same answer and the same wrong options) and 4 close." | 2 |
| C-6 | Part of the cause was in step 1. | `docs/decisions/0056-...md`, Reason, 30; `docs/journal.md`, 90 | "7 slots of mock 2 even had the same point as mock 1, although their group had a point that mock 1 did not use." / "The cause: the plan checks groups only inside one mock, step 1 did not prefer an unused point inside a group, and the writer did not know mock 1." | 2 / 4 |
| C-7 | Run files confirm 7: the mock 2 plan has 7 points of built mock 1 (1.6-K1, 3.3-S2, 3.5-K3, 3.4-S1, 4.6-S1, 4.1-S2, 5.6-S3). Each had an unused point in the same group and the same task statement. In mocks 3, 4, 5: 0 such points. | section 4.2 | | 1 |
| C-8 | The example of diagram 11: M2-S32 got 3.3-S2, the point of M1-S43. Run files agree (`runs/mock-02/plan.json` M2-S32 point 3.3-S2; `mocks/mock-01.questions.json` M1-S43-T1 point 3.3-S2). | `docs/diagrams/11-make-diagram.py`, 51; `docs/diagrams/11-repeats-across-mocks.html`, 257 (popup "step1") | "Example: in mock 2, slot M2-S32 got point 3.3-S2, the point of M1-S43, although 3.3-K1, 3.3-K2, 3.3-K3 and 3.3-S3 were unused." | 3 / 1 |
| C-9 | The step 1 part of the fix (steps 2 and 4 got rule B9, not step 1). | `docs/decisions/0056-...md`, 21 | "Code sorts the points of a task statement: first by the use of their group in the earlier mocks (decision 0050), then by the use of the point itself." | 2 |
| C-10 | The cost of the fix: the seed of mock 2 no longer gives its plan. | `docs/decisions/0056-...md`, 34; section 4.7 | "The new sort changes the plan that a seed gives." | 2 / 1 |
| C-11 | The result over 5 mocks: 0 ideas left out, 84 in 2 to 4 mocks, 10 in all 5 (section 4.5). | run files | | 1 |
| C-12 | Diagram 11 states its scope: "It changes step 1 (the plan), step 2 (the writer) and step 4 (the check)." | `docs/diagrams/11-repeats-across-mocks.html` (header text) | "Across mocks: the same idea may come back, the same question may not" | 3 |

### Story (d): the owner fixed the scenarios of mocks 3 to 5

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| D1 | The question. | `docs/decisions/0057-...md`, 10 | "With a seed for each later mock, some scenarios can come much more often than others." | 2 |
| D2 | The decision and the file. | `docs/decisions/0057-...md`, 23-27; `data/mock-scenarios.json`, 4-6 | "\| 3 \| 1, 2, 4, 6 \|" / "\| 4 \| 1, 3, 4, 6 \|" / "\| 5 \| 1, 2, 4, 5 \|" | 2 / 1 |
| D3 | Who decided. | `docs/decisions/0057-...md`, 39 | "The owner gave the sets and asked for the check. The assistant checked them." | 2 |
| D4 | The check. | `docs/decisions/0057-...md`, 35 | "Step 1 made a plan for 300 seeds of each of mocks 3, 4 and 5, with the rules of decisions 0047 to 0056: each seed gave a plan." | 2 |
| D5 | The test. | `tests/test_step1_plan.py`, 257, 268 | `def test_mocks_3_to_5_get_their_sets(self):` / `def test_a_set_that_decision_0027_does_not_permit_makes_no_plan(self):` | 1 |
| D6 | Diagram 12 shows the 5 sets and the count per scenario. | `docs/diagrams/12-scenarios-of-the-mocks.html` | "Blue: a set that the seed selected. Green: a set that the owner fixed." | 3 |

This is a decision without a failure. It is not a "what went wrong" story.

### Story (e): patterns in the set of 60 that no check of one question sees

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| P1 | Mock 1: two-answer questions with two examples of one idea. | `docs/decisions/0054-...md`, 10 | "In mock 1, the two correct options of M1-S17, M1-S35 and M1-S47 were two examples of one idea. Only M1-S58 had two different needs with two different answers." | 2 |
| P2 | Fix in step 1: two-answer slots only on listed points; first draft failed one seed. | `docs/decisions/0054-...md`, 22, 31 | "With the first draft of the list, seed 734 stopped, because its scenario 6 got only 1 listed point." | 2 |
| P3 | Run files: mock 1 had 3 of 8 two-answer slots on a listed point; mocks 2 to 5: 8 of 8. | section 4.2 | | 1 |
| P4 | Mock 1: the longest option was correct in 37 of 52. Step 1 now sets `longest_may_be_correct`. | `docs/decisions/0053-...md`, 10, 21 | "In the built mock 1, the correct option is the longest option (by characters) in 37 of the 52 questions with 1 answer. Chance is 13." | 2 |
| P5 | Mock 4: D correct 22 times, B 8. Step 1 sets `correct_letters` from mock 5. | `docs/decisions/0070-...md`, 10, 21 | "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. Chance is 13." | 2 |
| P6 | Run files: mock 5 has 13 of each letter and its built letters equal the plan in 60 of 60 slots (section 4.6). | run files | | 1 |
| P7 | Mocks 1 to 4 keep unbalanced letters; the portal note. | `docs/decisions/0070-...md`, 24 | "the portal shows the options in a random order on each attempt, because the letters in mocks 1 to 4 are not balanced." | 2 |

### Smaller items (for the Explanation, not stories)

- The build of step 1: `docs/journal.md`, 181: "Step 1 is built: `src/step1_plan.py`, with 20 tests. An independent reviewer found 1 serious and 7 minor items, and the assistant fixed them." (L4) Today 39 tests (L1).
- Decision 0027 "How we decided", 88: "The owner did not understand the first explanation of the scenario limit. The assistant then showed the table of the scenarios and their primary domains, and the example of the 12 questions of Domain 4." (L2)
- Decision 0027, 94: "The owner approved a short form of this text. The owner did not confirm the full text. No independent reviewer checked this file." (L2) The status line, 4, says "Text confirmed by the owner: 7 October 2026, after a summary of one line for each file".
- Open item that the plan does not prevent: `docs/decisions/0027-the-...md`, 79: "A task statement can be a bad fit for a scenario, also when its domain is a primary domain of that scenario. Example: task statement 5.4 (large codebase exploration) in scenario 6 (structured data extraction). The plan does not prevent this." In mocks 1 to 5, no try has `cannot_write` (`academy/facts/step-5.md`, section 4.2), so this case never stopped a slot. (L2, L1)
- `docs/lessons.md` is "Private history of the first build. Not a source for the design." (line 3). Lesson 12, line 51, says that in the first build "the paper has no question on 1.6". No source links it to the rule "each task statement gets at least 1 question". Not used.

## 6. Code that a popup could show

| File | Lines | What it shows |
|---|---|---|
| `src/step1_plan.py` | 1-11 | The docstring: "Code makes a list of 60 slots. No model works in this step." |
| `src/step1_plan.py` | 41-48 | The fixed numbers, with "a guess with no source" on the 2 multiple-response slots. |
| `src/step1_plan.py` | 55-71 | Only `random()`, for reproducibility, with the reason. |
| `src/step1_plan.py` | 118-125 | Domain counts from the weights, and the stop if they differ. |
| `src/step1_plan.py` | 185-205 | `_possible`: the matching of task statements to free groups (decision 0048). |
| `src/step1_plan.py` | 230-244 | `earlier_points`: only built mocks count (decision 0050). |
| `src/step1_plan.py` | 289-300 | Fixed scenarios of mocks 3 to 5, and the stop for a set that is not permitted. |
| `src/step1_plan.py` | 302-307 | The most even table. |
| `src/step1_plan.py` | 335-344 | The cap: a share, but no more than the groups. |
| `src/step1_plan.py` | 371-388 | The point order (0050, 0056) and the first free group that keeps a plan possible. |
| `src/step1_plan.py` | 446-453 | `longest_may_be_correct` on 13 and 3 slots. |
| `src/step1_plan.py` | 454-476 | `correct_letters`, balanced. |
| `src/step1_plan.py` | 477-480 | The last check: no two slots in one group. |
| `src/control.py` | 332-334 | The control makes the plan one time. |
| `src/steps.py` | 48-50 | The real step: records, mock, seed, earlier points. |
| `src/point_groups.py` | 80-88 | `conflicts`: groups with two or more slots. |
| `data/point-groups.json` | group G003 | The group of 1.6-K1, 1.6-S1 and 1.1-K3: "Fixed sequence against a plan that adapts". |
| `data/mock-scenarios.json` | 1-8 | The 3 fixed sets (8 lines). |
| `runs/mock-01/plan.json` | first slot | A real slot (E10). |
| `runs/mock-05/plan.json` | first slot | A real slot with the later fields (E11). |
| `tests/test_step1_plan.py` | 68 | `self.assertEqual(per_ts["3.3"], 1)`. |
| `tests/test_step1_plan.py` | 170-173 | The same seed gives the same plan. |
| `tests/test_point_groups.py` | 115-124 | The rule rejects the plan of mock 1 and names the pairs. |
| output of `python3 src/point_groups.py plan runs/mock-01/plan.json` | | The 12 groups of mock 1 (A11). |

## 7. A figure

The tab 2 sample figure "Code makes a plan of 60 slots" (`academy/sample/1-1-split-behind-the-mocks.html`, lines 280-292, Fig. 2) moves to the Explanation of step 1 (academy decision 0020). It shows two small boxes: "Claude decides next step (which tool)" against "code / the owner decide next step (set in advance)". Its caption: "The work of a mock is known before it starts: code makes a plan of 60 slots before a model writes any question. So the builder uses the other side of the distinction in 1.1-K3." Its two cards quote build guide lines 39 and 9 (`academy/sample/make-1-1.py`, 97, 110, 112). The two quotes are correct at commit `1cbae17`. See conflict C1 for 1.1-K3.

A figure of the mechanism, suggested in boxes and arrows:

```
[guide records: 6 scenarios, 5 weights, 30 task statements, 240 points]
[point groups: 95 ideas]   [built mocks 1..N-1]   [seed]   [fixed sets, mocks 3-5]
        \                     |  "counts used ideas"   |  "orders each choice"  /
         v                    v                        v                       v
   [Code: step 1]  --1 selects 4 scenarios--> --2 shares 60: 15 each, 16/11/12/12/9-->
                   --3 gives each task statement 1-3 questions (cap = its groups)-->
                   --4 picks one point per slot: least-used idea first, no idea twice-->
                   --5 sets type, longest_may_be_correct, correct_letters-->
        |  "writes once"                 \  "stops with the cause, writes nothing"
        v                                 v
   [plan.json: 60 slots]  --each slot to--> [Step 2: the writer]       [error]
```

Facts behind the labels: inputs E4, E6; "counts used ideas" R14, R15; "orders each choice" R21, O3; "selects 4 scenarios" R3, R7; "shares 60" R1, R2, R8; "1-3 questions (cap)" R9, R10 and section 4.2; "no idea twice" R12; "least-used idea first" R14; "sets type ..." R17, R19, R20; "writes once" E2, E3, R24; "stops" R23; "each slot to step 2" E13.

A second, small figure for the Depth (story a): the 12 groups of the mock 1 plan against 0 in mocks 2 to 5 (section 4.2), or the ideas table of section 4.5.

## 8. Conflicts

| # | Conflict | Source 1 (quote) | Source 2 (quote) |
|---|---|---|---|
| C1 | Fig. 2 of the tab 2 sample, which moves to step 1, cites point 1.1-K3. The build guide table of step 1 does not have 1.1-K3 (academy decision 0024: a point only in a figure is a conflict). | `academy/sample/1-1-split-behind-the-mocks.html`, 292: "So the builder uses the other side of the distinction in 1.1-K3." 1.1-K3: "The distinction between model-driven decision-making (Claude reasons about which tool to call next based on context) and pre-configured decision trees or tool sequences". | `docs/build-guide/step-1-plan-the-mock.md`, 62-64: 1.4-K2, 1.6-K1, 1.6-S1 only. Note: `data/point-groups.json` puts 1.1-K3 in group G003 with 1.6-K1 and 1.6-S1 (one idea). The figure is about the whole builder ("code and the owner decide the next step"), not only step 1. |
| C2 | "The same seed gives the same plan." | `docs/build-guide/step-1-plan-the-mock.md`, 11: "The same seed gives the same plan. So we can make the same plan again and compare it, for example after a change to the code." Also `docs/decisions/0027-the-...md`, 29, `src/step1_plan.py`, 4-5, diagram 02 popup "IN". | `docs/decisions/0056-...md`, 34: "seed 167622 no longer makes it again." Replay (4.7): with today's code, the plans of mocks 1 and 2 are not made again (59 and 19 points differ). Each plan is made again only with the code and data of its commit. The plan also depends on `data/`, and on the built files in `mocks/` (R15). |
| C3 | Number of sets with two most even tables. | `tests/test_step1_plan.py`, 180: "# 7 of the 11 sets have two most even tables." | Computed with `step1_plan.tables` and `_squares` (same code): 6 of 11 (section 4.3). The test asserts only "any", so it passes. |
| C4 | Mock 1: in how many one-answer questions is the longest option correct? | `docs/decisions/0053-...md`, 10: "37 of the 52". | `docs/journal.md`, 144: "29 of 52 by words, 34 of 52 by characters, chance about 13". `docs/reviews/M1-round1-second-review-notes.md`, 60: "the correct option is the longest by characters in 31." Built file today: 37 with ties, 33 strict, 30 by words with ties (4.6). The counts are from different dates (round 1, before and after rewrites) and methods. |
| C5 | Inputs of the step. | `docs/decisions/0027-the-...md`, 60: "It receives the guide records (...), a mock number and a seed." Diagram 02 popup "IN" lists 5 inputs and not `data/two-answer-points.json` or `data/mock-scenarios.json` (they appear only in popups "5" and "1"). | `src/step1_plan.py`, 24-26, 264: the code also reads both data files (E6). The status line of 0027 names the later decisions (0047, 0048, 0050, 0053, 0054), but not 0057 or 0070, which also add to the plan. |
| C6 | Number of parts of the method. | Diagram 02 popup "S": "Code makes the plan of one mock, in 5 parts." Decision 0027 method: 7 numbered steps (36-42). | `src/step1_plan.py`: 9 numbered stages in the comments. A difference of grouping, not of fact. |

## 9. Not found

1. No source records why the seed of each mock is the number it is (366341, 167622, 788092, 445312, 203660), or who chose it. `docs/journal.md`, 182 says only "With the yes of the owner, step 1 made the real plan of mock 1". Not checked further.
2. No run file or test shows that a plan ever stopped with `PlanError` in a real run. `docs/decisions/0054-...md`, 31 names one failed seed (734) in a check, with the first draft of the list.
3. No measure of whether the plan rules improved the questions, except the counts in section 4 (repeats inside a mock 12 to 0 groups; letters; longest option; two-answer points).
4. No source for the number 15 points "never got a question" (`docs/decisions/0048-...md`, 40) in a run file. Today's `seeds 2000` prints 95 points that no plan uses, but it plans mock 2 after the built mock 1 with the order of 0056, so it is not the same measure. Not computed again.
5. Decision 0049, 28 ("Over 200 seeds, two plans share about 44 of their 60 ideas (36 to 51)") was not computed again.
6. No academy or `docs/sources/` copy of the Python page "random" (R22). This agent may write only this sheet.
7. No story in the sources about a failure of step 1 in a real run of the program. All stories are failures that the plan caused in the questions (repeats, patterns), found after a mock was built, and fixed in the plan of the next mock.
