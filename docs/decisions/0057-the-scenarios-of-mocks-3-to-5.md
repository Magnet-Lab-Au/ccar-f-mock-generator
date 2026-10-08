# 0057: The scenarios of mocks 3 to 5

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/12-scenarios-of-the-mocks.html`. Diagram 02 (step 1) shows the change in its step.

## Question

Decision 0027 lets the seed select the set of 4 scenarios of a mock. Mock 1 has scenarios 1, 2, 3 and 5. Mock 2 has 3, 4, 5 and 6. With a seed for each later mock, some scenarios can come much more often than others. How does the program select the scenarios of mocks 3 to 5?

## Options

1. The owner fixes the sets now.
2. The seed selects each set, as before.

## Decision

Option 1.

| Mock | Scenarios |
|---|---|
| 3 | 1, 2, 4, 6 |
| 4 | 1, 3, 4, 6 |
| 5 | 1, 2, 4, 5 |

1. The file `data/mock-scenarios.json` holds these sets. Step 1 reads it. The seed still sets the sequence of the 4 groups in the mock.
2. Step 1 stops with an error if a fixed set is not one of the 11 sets that decision 0027 permits.
3. Mocks 1 and 2 do not change.

## Reason

Plain reason: each scenario appears about equally. Over the 5 mocks, scenarios 1 and 4 come 4 times, and scenarios 2, 3, 5 and 6 come 3 times.

A script checked that each set is one of the 11 sets of decision 0027. Step 1 made a plan for 300 seeds of each of mocks 3, 4 and 5, with the rules of decisions 0047 to 0056: each seed gave a plan.

## How we decided

The owner gave the sets and asked for the check. The assistant checked them.

The owner has not confirmed the text of this file. One independent reviewer checked decisions 0056 to 0058, diagrams 11 and 12 and the code on 8 October 2026, and the assistant fixed its findings.

## Exam guide points

none
