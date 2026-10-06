# 0028: The design of step 0: a script makes one JSON file of guide records

- Date: 6 October 2026
- Status: accepted
- Diagram: `docs/diagrams/03-step-0-prepare-the-guide-records.html`

## Question

Decision 0017 says that step 0 prepares the guide records. It left three things open: the format of the new file, if code or a person makes it, and the comparison of our copy of the guide with the original. What is the design of step 0?

## Options

1. A script makes one JSON file with all records. Checks by script and by an independent reviewer.
2. A script makes separate files, for example one file for each task statement.
3. A person makes the file.

## Decision

Option 1.

1. **Who.** Step 0 is a script. It reads `reference/exam-guide.md` and writes the records. No model copies text.
2. **The file.** The script writes one file, `reference/guide-records.json`. It is the one source of guide text for the code. Code takes a slice from it by ID and gives only that slice to a model call. A model call does not read the file.
3. **The records and their fields.**

| Record | Fields | Count |
|---|---|---|
| Guide | version | 1 |
| Domain | id, name, weight | 5 |
| Scenario | id, name, story, primary domains | 6 |
| Task statement | id, domain, title, points | 30 |
| Point | id, kind (knowledge or skill), text | 240 |
| Sample question | number, scenario, question, options, correct answer, explanation | 12 |
| Section 17 | technologies, topics in scope, topics out of scope | 3 lists |

4. **The ID of a point.** The task statement, then K (knowledge) or S (skill), then the number of the bullet. Example: `1.4-K2` is the second bullet below "Knowledge of:" in task statement 1.4. The IDs are ours. The guide does not number its bullets.
5. **The checks.** (1) A script compares `reference/exam-guide.md` with the original in the Claude project "CPN Learning path", character for character. (2) A script checks the counts, and checks that each text in the file is exactly in the guide. (3) An independent reviewer checks the file (rule 15).
6. **The old file.** `reference/task-statements-and-points.md` stays. It is a file for people.

The contract of the step (decision 0018):

- It receives `reference/exam-guide.md`.
- It returns `reference/guide-records.json`.
- It can fail when a count is wrong or when a text is not exactly in the guide. Then the script writes no file and names the cause.

## Reason

The reason for checked records is in decision 0017. This decision uses no new exam guide point.

- A script, not a person and not a model: the plain reason is that a script copies text with no change, and we can run it again for a new version of the guide.
- JSON: the plain reason is that code reads it directly. The guide teaches JSON schemas for the output of a model (task statement 4.3). That is a different context. This file is the output of a script.
- One file: the plain reason is that one file has one version and one check. With many files, a file can be missing or old. The slices that a call gets are the same in each case.

Not decided yet: nothing for this step.

## How we decided

The assistant showed a proposal for step 2 that said "the story of the scenario" and "a fixed form with fields". The owner asked where the story comes from, said that the task statements are not in separate records for code, and said that no output format and no fields were decided. The owner was right. The cause: `HANDOFF.md` said to start with step 1, and each step reads the records of step 0. The assistant followed that sequence and did not say that it was wrong.

The owner and the assistant then agreed on two changes. Step 0 is designed before step 2. Each design names the exact file format and the exact fields.

The owner asked why all records are in one file, because different API calls get different slices. The answer: code takes the slice, and the model never sees the file. The owner accepted one file.

The owner asked what a point is, and if "Knowledge of" and "Skills in" are in the original guide. The answer: yes, each task statement in the guide has these two headings. The assistant read them in our copy of the guide.

The owner approved a short form of this text. The owner did not confirm the full text.

## Exam guide points

none
