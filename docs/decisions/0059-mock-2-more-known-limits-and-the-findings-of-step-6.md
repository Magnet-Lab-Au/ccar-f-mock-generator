# 0059: Mock 2: more known limits, and the findings of step 6

- Date: 8 October 2026
- Status: accepted
- Diagram: none

## Question

The owner marked round 2 of mock 2 (the 14 rewrites): 14 of 14 good. The second review also found 14 of 14 good. The reviewer of decisions 0056 to 0058 and the second review found that some new questions are still close to another question. Step 6 ran again and has 9 findings that wait for the owner. What happens to them before mock 2 is built?

## Options

1. No more rewrites. The close questions and some findings are known limits. The other findings are ignored.
2. Another round of rewrites.

## Decision

Option 1. Decision 0058 has the first 4 known limits. These are added:

| Known limit | Found by |
|---|---|
| M2-S35-T3 has the scene of M2-S31-T2 (plan mode for a choice between two ways with different infrastructure). Step 6 finding M2-SC5-R2-F1 (rule D1). | The reviewer, the second review and step 6 |
| M2-S31-T2 has the scene of M1-S34 (a migration of about 40 files with two approaches, plan mode first), now asked as a cause. | The reviewer and the second review |
| M2-S59-T2 has the same point and answer as M1-S39 (keep both values with their sources). | The reviewer and the second review |
| M2-S48-T2 has the scene of M1-S12 (a subagent timeout and the error report). | The second review |
| Scenario 6 has 5 wrong options on the model's own confidence: M2-S49, M2-S50, M2-S51, M2-S52 and M2-S56. Step 6 findings M2-SC6-R2-F1 (rule D2) and M2-SC6-R2-F2 (rule D3). | Step 6 |
| Scenario 5 has one wrong idea in 3 questions: an output schema controls the content of the output (M2-S37, M2-S41 and M2-S45). Step 6 finding M2-SC5-R2-F7 (rule D2). | Step 6 |

The 5 findings of rule D4 (a question that gives away the answer of another), M2-SC5-R2-F2 to F6, are ignored.

After these decisions (D015 to D023 in `runs/mock-02/owner-decisions.json`), the owner accepted mock 2. Step 8 built `mocks/mock-02.questions.json` and `mocks/mock-02.answers.json`.

## Reason

Plain reason: decision 0060 says that a close repeat is allowed and is recorded as a known limit. The owner and the second review found each question good. Another rewrite round costs a marking round and can make new close questions.

## How we decided

The owner decided: "Record these as known limits of mock 2, with no rewrites", "Ignore the 5 findings of rule D4", and "Accept mock 2 and build its files". The finding M2-SC5-R2-F7 was not in those instructions. The assistant suggested that it is a known limit too, and the owner agreed.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
