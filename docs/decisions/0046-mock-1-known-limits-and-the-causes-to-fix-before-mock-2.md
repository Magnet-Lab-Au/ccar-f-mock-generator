# 0046: Mock 1: its known limits, and the causes to fix before mock 2

- Date: 8 October 2026
- Status: accepted
- Diagram: none

## Question

After the round of 9 rewrites (decision 0045), the owner marked round 2 blind: 9 of 9 good. A second review by a Claude model also found 9 of 9 good by the four checks, but found three weak questions (record: `docs/reviews/M1-round2-second-review.md`). Does mock 1 get another round of rewrites?

## Options

1. Another round of rewrites for the three questions.
2. No more rewrites. The three weak questions are known limits of mock 1. Their causes go to the list of changes before mock 2.

## Decision

Option 2. The owner also decided: each of the 16 findings of the second run of step 6 is `ignore`. The 3 findings of rule D1 among them are known limits too.

The known limits of mock 1:

| Question | Weakness |
|---|---|
| M1-S60-T2 | It is a close copy of sample question 12 of the guide: the same scene and the same four options. |
| M1-S47-T6 | After 6 tries, its two correct options are still one idea. The slot is "Select 2." on a point with one idea. |
| M1-S33-T1 and M1-S43-T1 | The same scene (finding M1-SC2-R2-F1, rule D1): conventions that load only for some files. Twin points 3.3-S1 and 3.3-S2. |
| M1-S38-T2 and M1-S45-T2 | The same scene, found by the second review and by step 6 (finding M1-SC2-R2-F2, rule D1): verbose discovery output fills the context. Twin points 3.4-K4 and 5.4-S1, in two different task statements. |
| M1-S53-T2 and M1-S54-T1 | The same scene (finding M1-SC5-R2-F1, rule D1): output that passes the schema but has a semantic error. The points 4.4-K1 and 4.4-K4 are not twins by their texts (a retry with the exact errors, and a semantic error against a schema error). The probable cause is that scenario 5 has 12 questions of Domain 4. |

The list of changes before mock 2 (from decision 0045 and from this file). Each one gets its own decision file:

1. Twin points: two points of one task statement often describe one idea, and the plan selects them at random.
2. Twin points also exist across task statements (new).
3. Scenario 5 has 12 of its 15 questions from Domain 4 (the scenario limit of decision 0027).
4. Step 6 compares the questions of one scenario only.
5. No rule looks at the longest option in the set of 60.
6. A "Select 2." slot needs a point with two ideas (new, it replaces "multiple-response slots on a point with one idea").
7. No rule compares a question with the 12 sample questions of the guide (new).

## Reason

Plain reason: the owner and the second review found each question good by the four checks. The three weaknesses come from the plan and from missing rules, so another rewrite on the same plan can repeat them. The changes before mock 2 address their causes.

## How we decided

The owner decided: "I do not want another rewrite round. Record them as known limits of mock 1." The owner named the three new causes.

The owner has not confirmed the text of this file. One independent reviewer checked this file on 8 October 2026, and the assistant fixed its findings.

## Exam guide points

none
