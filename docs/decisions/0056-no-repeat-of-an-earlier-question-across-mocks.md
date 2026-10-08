# 0056: No repeat of an earlier question across mocks

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html` (step 1), `docs/diagrams/04-step-2-write-the-question.html` (step 2), `docs/diagrams/06-step-4-check-by-a-model.html` (step 4)

## Question

The owner marked mock 2: 20 of 20 good. A second review and an independent agent compared the 60 questions of mock 2 with the 60 of mock 1. 17 questions of mock 2 repeat mock 1: 13 strong (the same scene, the same answer and the same wrong options) and 4 close. Decisions 0047 and 0050 prevent two questions on one idea inside one mock, and they spread the ideas over the mocks. They do not prevent the same question in two mocks. How does the program prevent it?

## Options

1. A rule in steps 1, 2 and 4: a shared idea is allowed, the same question is not.
2. No shared idea across mocks. This is not possible: the guide has 95 ideas, and 5 mocks have 300 slots (decision 0049).

## Decision

Option 1. A shared idea is allowed. The same question is not.

1. **Step 1.** Inside a group, code takes first a point that the earlier mocks used less. The seed keeps the order inside the same counts. This is code only.
2. **Step 2.** When the idea of a slot is in an earlier mock, the writer gets the earlier questions on that idea, with the mark of each option, and this instruction: "Use a different scene and a different angle: the cause, the fix, or a choice between rules. The correct action may be the same, if the idea has only one. Do not use a wrong option of an earlier question."
3. **Step 4.** New rule B9 in call 4b: "The question is not a repeat of an earlier question on the same idea: not the same scene with the same answer, and no wrong option of an earlier question." Call 4b gets the earlier questions on the same idea. With none, B9 passes. A failure goes to step 5, as for each other rule.
4. **The earlier questions** are the questions of the built mocks with a lower number (`mocks/mock-NN.questions.json` and `mocks/mock-NN.answers.json`). The idea of a question is the group of its point (decision 0047). Code: `src/earlier.py`.
5. The list of rules for a good question now has 21 rules: A1 to A12 and B1 to B9.
6. Step 6 does not change. A check in step 4 sends a failure back to the writer automatically. A finding of step 6 waits for the owner after the marking.

## Reason

In mock 2, the writer did not know mock 1. On a shared idea it wrote the most obvious scene again, often with the same wrong options. 7 slots of mock 2 even had the same point as mock 1, although their group had a point that mock 1 did not use.

The owner changed the first suggestion of the assistant: the writer must use a different scene and a different angle, not a different correct action, because some ideas have only one correct action. The wrong options must never be the same.

Not decided yet:

- A repeat with different words that call 4b does not see. The owner marks a sample of each later mock.

## How we decided

The assistant counted the repeats of mock 2 with an independent agent, and explained why the plan did not stop them. It suggested the rule. The owner agreed with one change (a different angle, not a different correct action, and never the same wrong options). The assistant suggested the check in step 4, not in step 6, and the owner agreed.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
