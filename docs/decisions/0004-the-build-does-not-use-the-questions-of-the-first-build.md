# 0004: The build does not use the questions of the first build

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: none

## Question

Can the program use question content from the first build?

## Options

1. No old question goes into a new mock. A use of the old questions as test data stays open for a later decision.
2. No old question goes into a new mock, and the build never reads the old questions.
3. The program can take questions from the first build or from the repaired mocks.

## Decision

Option 2. The program writes each question new. No prompt, no example, no test and no check of this build reads a question of the first build or of the repaired mocks. If a check needs test questions with known defects, we write them new.

"The old questions" are the questions in the folder `Mocks` (the five mocks and the question bank) and in the folder `CCAR-F Portal Mocks`.

The file `reference/practice-audit-first-build.md` stays in the folder as history. It is not a source of questions.

## Reason

No exam guide point gives the complete reason. The reason is plain, in three parts. A question that the program did not write has no run record in the program, so nobody can show how it was made. A model that writes questions and sees old questions copies their style and their defects. A check that is tuned on the old verdicts learns to agree with the old reviewer.

The guide calibrates a checker with "labeled validation sets" (5.5-K3). The old verdicts are not labels from a person.

Not decided yet: if the program can use the source files of the first build, for example the digests of the course material.

## How we decided

The assistant first recommended option 1. The owner asked if old questions in the context make a bias. The answer was yes, for the writer and for the check. The assistant had said that a person marked the old questions in the review of September 2026. That was wrong. Agents made the old verdicts, and the owner read 7 of 300 questions. The correction removed the reason for option 1.

## Exam guide points

5.5-K3
