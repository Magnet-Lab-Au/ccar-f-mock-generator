# 0052: Rule C3 compares the whole mock

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/08-step-6-check-the-complete-mock.html` (step 6)

## Question

Change 4 of decision 0046: "Step 6 compares the questions of one scenario only." In mock 1, step 6 did not find M1-S10 and M1-S24, the same question in two scenarios. What does step 6 change?

## Options

1. A change in code only: rule C3 ("No two questions have the same text") compares all 60 questions of the mock.
2. A new model call that reads all 60 questions together.

## Decision

Option 1.

1. Rule C3 compares each question of the scenario with the other questions of the scenario, and with the current questions of the other 3 scenarios.
2. A finding of rule C3 can name a question of another scenario. A finding of another rule cannot. The control checks this.
3. No new model call. Calls 6a and 6b still read the 15 questions of one scenario.
4. The findings keep their IDs. The finding belongs to the scenario that step 6 checked.

## Reason

The point groups (decisions 0047 and 0048) now prevent the case of mock 1: 1.7-K1 and 1.7-S1 are in one group, so no mock gets both. Two questions in different scenarios on different ideas seldom have the same scene. The owner marks all 60 questions of a mock in step 7, so the owner sees the questions of all scenarios.

A copy of a question is a new question in the run of step 6 of its own scenario. So that run finds the copy, also when the other scenario does not run again.

Not decided yet:

- A copy with different words in two scenarios. Only a model call can find it.
- The same scene in two mocks.

## How we decided

The assistant said that the groups now catch the case of mock 1, and suggested the change in code only. The owner said yes.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
