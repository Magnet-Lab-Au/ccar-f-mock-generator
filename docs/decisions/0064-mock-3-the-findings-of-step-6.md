# 0064: Mock 3: the findings of step 6

- Date: 9 October 2026
- Status: accepted. Decision 0078 corrects one line of this file.
- Text confirmed by the owner: 9 October 2026
- Diagram: none. No step changes.

## Question

Step 6 found 11 findings in mock 3 that wait for the owner. What happens to each one?

## Options

1. The same treatment as for mock 2: ignore the findings of rule D4, and record the findings of rules D2 and D3 as known limits.
2. A rewrite for some of them.

## Decision

Option 1. Each finding gets "ignore" (owner decisions D007 to D017 in `runs/mock-03/owner-decisions.json`):

| Findings | Rule | Decision |
|---|---|---|
| M3-SC6-R1-F1 to F5, M3-SC1-R1-F1, M3-SC4-R2-F1 | D4: a question gives away the answer of another | Ignore |
| M3-SC6-R1-F6, F7, F8, M3-SC1-R1-F2 | D2 and D3: one wrong idea in too many questions | Ignore. They are known limits (decision 0063) |

The run of step 6 after the 2 rewrites replaced the findings of scenario 4 (M3-SC4-R2) and found none in scenario 2. Before that run, scenario 4 had one more D4 finding (M3-S42 and M3-S43). It is not in the last run.

## Reason

Plain reason: the owner and the second review marked each question good. For mock 2, the owner ignored the D4 findings and recorded the D2 and D3 findings as known limits (decision 0059). A rewrite for each would cost a marking round and can make new findings.

## How we decided

The assistant suggested the same treatment as for mock 2. The owner said "agree".

The owner confirmed the text of this file on 9 October 2026. No independent reviewer checked this file.

## Exam guide points

none
