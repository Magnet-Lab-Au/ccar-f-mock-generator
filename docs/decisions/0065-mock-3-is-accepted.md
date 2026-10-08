# 0065: Mock 3 is accepted

- Date: 9 October 2026
- Status: accepted
- Diagram: `docs/diagrams/12-scenarios-of-the-mocks.html` shows mock 3 as built.

## Question

Each of the 60 slots of mock 3 passed steps 3, 4 and 6. The owner marked 22 questions good in two rounds, with no bad mark. Each finding of step 6 has a decision (decision 0064). Does the owner accept mock 3?

## Options

1. Accept mock 3, and step 8 builds its files.
2. Wait.

## Decision

Option 1. The owner accepted mock 3. Step 8 checked the six conditions of decision 0039 and built `mocks/mock-03.questions.json` and `mocks/mock-03.answers.json`: 60 questions in 4 groups (scenarios 1, 2, 4 and 6, decision 0057).

Mock 3 cost $23.85 for its runs. Its known limits are in decision 0063.

Mock 4 does not start until the owner says so. Before mock 4, rule B9 becomes stricter (decision 0062).

## Reason

Plain reason: each condition of the build holds, and the owner found each marked question good.

## How we decided

The owner said: "Accept mock 3 and build its files, after the known limits and the step 6 findings from my earlier message are recorded." The assistant recorded decisions 0063 and 0064 first.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
