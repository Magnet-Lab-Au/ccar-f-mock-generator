# 0077: Mock 5: the findings of step 6, and acceptance

- Date: 9 October 2026
- Status: accepted
- Diagram: `docs/diagrams/12-scenarios-of-the-mocks.html` shows mock 5 as built. Diagram 08 (step 6) shows the rule for the findings.

## Question

The second review marked round 2 of mock 5: M5-S33 and M5-S45 good. Step 6 had 14 findings. How is mock 5 finished?

## Options

1. The rule of mocks 2 to 4 for the findings, the one finding of another kind as a known limit, and the acceptance.
2. More rewrites.

## Decision

Option 1.

1. **Round 2:** marks of the second review, not of the owner. On the instruction of the owner, the assistant typed them into `marking/M5-round2.xlsx` and committed the file.
2. **The findings of rule D4 (9)** are ignored. The findings of rules D2 and D3 (4) are known limits. One of them, M5-SC5-R2-F5 (rule D3), names M5-S40: two wrong options of one question use the model's own confidence as a gate.
3. **The finding of rule D1, M5-SC4-R1-F1, is a known limit.** Option D of M5-S02 (spawn the subagents at the same time) is the answer of M5-S05 (emit all Task calls in one response). The point 1.4-S2 of M5-S02 names parallel investigation itself, and M5-S05 tests the Task tool mechanism.
4. The decisions are D007 to D020 in `runs/mock-05/owner-decisions.json`.
5. **The owner accepted mock 5.** Step 8 built `mocks/mock-05.questions.json` and `mocks/mock-05.answers.json`. Mock 5 cost $11.68 in its run records, plus under $1 of a stopped run (decision 0073).

The other known limits of mock 5 are in decision 0076 (46 of 60 questions close to earlier mocks, a review mock).

## Reason

Plain reason: the second review found each question good after the 2 rewrites, and the rule for the findings is the rule of decisions 0059, 0064 and 0069. The D1 finding repeats a part of a point, not a copy.

## How we decided

The owner said: "use the same rule as mocks 2 to 4 ... If a finding is of another kind, show it to me first." The assistant showed the D1 finding and suggested a known limit. The owner said yes, and asked to accept and build mock 5.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
