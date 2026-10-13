# 0081: Ruling 2 counts an option that acts only when the model is highly confident

- Date: 14 October 2026
- Status: accepted
- Text confirmed by the owner: 14 October 2026, in the discussion (working rule 35)
- Diagram: none
- Names: decisions 0006, 0045 and 0077. Their texts do not change (working rule 26).

## Question

Decision 0006 (ruling 2) says: "In one scenario of one mock, at most one wrong option is the self-reported-confidence option. That option is: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger."

Two almost identical options on point 4.1-S3 got opposite answers:

- M1-S49-T1, option D: "Instruct Claude to be conservative and assign a higher severity level only when it is highly confident about the finding." Step 6 counted it as a confidence trigger (`runs/mock-01/checks/M1-scenario-5-step6-run1.json`). The owner rewrote the question (decision 0045, owner decision D008).
- M5-S40-T1, option B: "Tell Claude to be careful and conservative, and to assign the blocker level only when it is highly confident about the risk of the finding." Decision 0077 says that the second review counts it "as the general instruction "be conservative" of point 4.1-K2, not as a self-reported confidence option."

Which reading is correct?

## Options

1. The reading of M1-S49: an option that acts only when the model is highly confident counts for ruling 2.
2. The reading of M5-S40: such an option is a general instruction and does not count.

## Decision

Option 1. An option that lets the model act only when it is highly confident uses its own confidence as a trigger. It counts for ruling 2, also when it also says "be conservative".

Mock 5 does not change. M5-S40 stays in mock 5 as a known limit: scenario 5 of mock 5 has two wrong options on self-reported confidence (options A and B of M5-S40). No question is written again, so this decision has no API cost.

## Reason

The two options have the same trigger, "only when it is highly confident". The words "be conservative" do not remove the trigger. One rule must give one answer for the same text.

## How we decided

The academy fact agent of step 6 found the two cases. The morning report of the night of 14 October 2026 named them (item 5). The assistant recommended option 1 with no rewrite. The owner said: "yes, M1-S49 reading is correct".

## Exam guide points

4.1-S3, 4.1-K2.
