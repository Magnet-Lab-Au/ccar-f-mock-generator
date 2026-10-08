# 0066: A stricter rule B9 for mocks 4 and 5

- Date: 9 October 2026
- Status: accepted
- Diagram: `docs/diagrams/11-repeats-across-mocks.html`. Diagram 06 (step 4) shows the new text of B9.

## Question

Decision 0062 says that rule B9 becomes stricter before mock 4. In mock 3, about 26 questions had the same problem and the same answer as an earlier question, in another setting, and B9 let them pass. What is the new text, and how does the owner know that it is fair?

## Options

1. A new text of B9 and of the writer instruction, with a test on mock 3 first.
2. The new text with no test.

## Decision

Option 1.

1. **The new text of rule B9:** "The question does not have the same problem as an earlier question on the same idea, also in another setting (another tool, team, product or data). The same problem means that the same thing goes wrong, or the team must make the same choice, so the same reasoning leads to the answer. A question on the same idea passes only with a different problem: for example the cause against the fix, a different failure, or a choice between two rules. Not the same set of wrong options as an earlier question on the same idea. At most one wrong option may repeat."
2. **The writer** gets the same rule in its own words: "Write a question with a different problem, also if you change the setting: a different thing goes wrong, or the team must make a different choice. For example the cause against the fix, a different failure, or a choice between two rules. The correct action may be the same, if the idea has only one. Do not use the same set of wrong options as an earlier question. At most one wrong option may repeat."
3. **A slot that fails B9 three times** opens for the owner, as before. The owner gives a new point or more tries.
4. **A test before mock 4:** call 4b checks the 60 built questions of mock 3 with the new text, against mocks 1 and 2 (`src/test_b9.py`, results in `runs/test-b9/results.json`). The owner sees 5 of the questions that the new rule fails, each with the earlier question and the reason, and decides if the rule is fair.
5. **Step 1 does not change.** It already takes first the ideas that the earlier mocks used least (decision 0050), and inside a group a point that they did not use (decision 0056).

This changes item 4 of decision 0060 ("Rule B9 does not change") from mock 4, as decision 0062 says.

## Reason

Plain reason: a participant who meets the same problem in a new setting meets the same question. The first text of B9 let a new setting count as a new scene.

The owner changed the first suggestion of the assistant: "No wrong option of an earlier question" became "Not the same set of wrong options. At most one wrong option may repeat." The reason of the owner: the standard mistakes that the guide names make the strongest wrong options, and the owner wants harder questions in mocks 4 and 5.

The cost: more tries for mock 4, perhaps $30 to $35 instead of about $24. This is an estimate of the assistant. It is not measured.

## How we decided

The assistant suggested the text, the test and the cost. The owner agreed with three changes: the rule on the wrong options, a check that the preference for unused groups is built (it is), and 5 failed questions from the test for the owner to judge.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
