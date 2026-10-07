# 0027: The design of step 1: the plan of a mock

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review.
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html`

## Question

Decision 0009 says that code makes the plan of a mock, a list of 60 slots. What does the plan contain, and what does step 1 receive and return?

## Options

1. One proposal of the assistant for all details of the step. The owner accepts or changes each detail.
2. A different design.

## Decision

Option 1. The owner accepted each detail.

1. **Domains.** A mock has 16 questions of Domain 1, 11 of Domain 2, 12 of Domain 3, 12 of Domain 4 and 9 of Domain 5.
2. **Scenarios.** The program selects 4 of the 6 scenarios at random. It selects only from the 11 sets of 4 scenarios in which each question fits a primary domain of its scenario. It does not use these 4 sets: scenarios 1, 2, 3, 4. Scenarios 1, 2, 5, 6. Scenarios 2, 3, 5, 6. Scenarios 2, 4, 5, 6.
3. **Questions for each scenario.** Each scenario has 15 questions.
4. **Task statements.** Each of the 30 task statements gets at least 1 question in each mock. The task statements of a domain share the questions of that domain equally. The seed selects which task statements get the questions that are left.
5. **Question types.** A mock has 52 multiple-choice questions and 8 multiple-response questions. Each scenario has 2 multiple-response questions.
6. **A slot.** A slot contains an ID, the scenario, the task statement, one point of that task statement, the question type, the number of options and the number of answers to select. The program selects the point at random. Two slots of one mock do not get the same point. Decision 0029 has the table of the fields.
7. **The seed.** A seed is a number that controls the random selections. The plan file has the seed. The same seed gives the same plan.
8. **A new point.** The owner can give an open slot a new point with the decision `new_point`. Code saves the new point in that decision. `plan.json` does not change, so the same seed still gives the same plan (decision 0039, item 7).

### The method (decision 0037, item 14)

Code makes the plan in this sequence. Where code must select, the seed decides.

1. The seed selects one of the 11 sets of 4 scenarios, and the sequence of the 4 groups in the mock.
2. Code makes the table of scenarios and domains. The table says how many questions of each domain each scenario gets. A table fits when each scenario has 15 questions, each primary domain of a scenario has at least 1 question, no question is outside a primary domain, and the domain counts are those of item 1. From all tables that fit, code takes the most even one: the table with the smallest sum of the squares of its numbers. If two tables are equal, the seed selects one.
3. In each domain, the task statements share the questions equally. The seed selects which task statements get the questions that are left. Example: Domain 1 has 16 questions and 7 task statements. Each one gets 2, and two of them get 3.
4. The seed decides which scenario of the table each of these questions goes to.
5. The seed selects one point for each slot.
6. The seed selects 2 slots of each scenario for multiple-response.
7. The slots get the numbers 1 to 60, group by group. Inside a group, the seed sets the sequence. The slot number is the question number in the finished mock (decision 0036). Example: `M1-S17` is question 17.

### The plan file

The plan of one mock is one file, for example `runs/mock-01/plan.json`. It has these top fields, and then the 60 slots.

| Field | Content |
|---|---|
| `mock` | The number of the mock |
| `seed` | The seed |
| `guide_version` | The version of the guide, from the records file |
| `date` | The date of the plan |
| `scenarios` | The 4 scenarios, in the sequence of the groups |
| `table` | The number of questions for each scenario and each domain |
| `slots` | The 60 slots |

The contract of the step (decision 0018):

- It receives the guide records (the scenarios with their primary domains, the domain weights, the task statements with their points), a mock number and a seed.
- It returns one plan file, `runs/mock-01/plan.json`.
- It can fail when a record is missing or when the counts do not add up to 60. Then it stops with an error that names the cause, and it writes no plan.

## Reason

The reason that code makes the plan is in decision 0009. This decision uses no new exam guide point. The guide has no point on the plan of an exam paper.

1. Domains. The weights are from Section 4 of the guide: 27%, 18%, 20%, 20% and 15%. "The percentages indicate the approximate proportion of scored items drawn from each domain." For 60 questions they give 16.2, 10.8, 12, 12 and 9. The five numbers are these values, rounded. They add up to 60.
2. Scenarios. Section 5 of the guide gives the primary domains of each scenario. The plain reason for the limit: a question on a domain that is not a primary domain of its scenario is forced into a story that does not fit it. This is a difference from the exam. The guide says: "During the exam, 4 scenarios are presented and picked at random from the full set of the 6 scenarios below." The exam can use all 15 sets. A mock uses 11.
3. Questions for each scenario. The guide gives no number. The plain reason: equal parts.
4. Task statements. The plain reason: each mock then covers the complete guide.
5. Question types. The guide gives no number. It says only: "Multiple-choice and multiple-response items; each item states how many responses to select" (Section 3). All 12 sample questions of Section 9 are multiple-choice with 4 options. The number 8 is a guess of the assistant. It has no source.
6. A slot. The plain reason for the point: the writer and the checker know exactly what the question must test. With no point, the writer selects a part of the task statement, and the same part can come again and again.
7. The seed. The plain reason: we can make the same plan again and compare it, for example after a change to the code.
8. The method. The plain reason for the most even table: no scenario gets more questions of one domain than is necessary. A script checked each set: `docs/decisions/0037-check-scenario-tables.py`. Each of the 11 sets has a table that fits. But in 9 of the 11 sets, a scenario gets 12 of its 15 questions from one domain. In 2 of these sets (scenarios 1, 2, 3, 6 and scenarios 1, 3, 4, 6), two scenarios get 12. The cause is the limit of item 2. Example: only scenarios 5 and 6 have Domain 4 as a primary domain. If a set has only one of them, that scenario gets all 12 questions of Domain 4. This explains 8 of the 9 sets. In the set 1, 3, 5, 6 the cause is Domain 3: scenario 5 gets all 12 questions of Domain 3. The limit stays for mock 1. If the check of the complete mock shows repeats, a new decision changes the limit with that evidence.

Not decided yet:

- A task statement can be a bad fit for a scenario, also when its domain is a primary domain of that scenario. Example: task statement 5.4 (large codebase exploration) in scenario 6 (structured data extraction). The plan does not prevent this. The writer can answer `cannot_write` for such a slot (decisions 0029 and 0037). The slot is then open, and the owner selects `new_point`, `more_tries` or `new_plan` (decision 0039).
- How the program selects the scenarios across more than one mock. That depends on the number of mocks.

## How we decided

The owner and the assistant agreed on a faster method for the design of the steps: the assistant shows one proposal for each step, and the owner accepts or changes it. For step 1, the owner then looked at each detail separately and said yes to each one.

The owner asked if the domain numbers are a best practice from the exam guide. The answer was no: the percentages are a fact about the exam (Section 4), and the numbers are arithmetic.

The owner did not understand the first explanation of the scenario limit. The assistant then showed the table of the scenarios and their primary domains, and the example of the 12 questions of Domain 4.

A script checked all 15 sets of 4 scenarios: 11 fit, and in 4 sets only 48 of 60 questions fit. The script is `docs/decisions/0027-check-scenario-sets.py`. It checks the domain counts and the 15 questions for each scenario. It does not check the fit of a task statement.

The assistant found the first "not decided yet" item after the proposal, and told the owner before this file was written.

The owner approved a short form of this text. The owner did not confirm the full text. No independent reviewer checked this file.

## Exam guide points

none. The decision uses Sections 3, 4, 5 and 9 of the guide.
