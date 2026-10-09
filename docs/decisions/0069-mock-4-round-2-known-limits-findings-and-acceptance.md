# 0069: Mock 4: round 2, known limits, the findings of step 6, and acceptance

- Date: 9 October 2026
- Status: accepted
- Diagram: none. No step changes.

## Question

The owner marked round 1 of mock 4: 20 of 20 good. The second review in Cowork found 2 questions to fix. After the 2 rewrites, round 2 had 2 questions, and step 6 had findings. How is mock 4 finished?

## Options

1. The marks of round 2 come from the second review, the findings follow the rule of mocks 2 and 3, and the owner accepts mock 4.
2. The owner marks round 2.

## Decision

Option 1.

1. **The findings of the second review** (not marks of the owner):
   - M4-S43: a rewrite. It copied M3-S19 and repeated M4-S45 in the same scenario: one customer message with several concerns. The new question keeps point 1.2-K4 with a broad investigation (decision D007 in `runs/mock-04/owner-decisions.json`).
   - M4-S09: a new option C. The old option C was the second wrong option on the model's own confidence in scenario 6 (ruling 2). The program cannot change one option only, so the writer got the question with the instruction to keep everything and replace option C (D008). The new question has the same text and three of the same options.
2. **Round 2 was not marked by the owner.** The second review in Cowork found M4-S09-T2 and M4-S43-T3 good. On the instruction of the owner, the assistant typed "good" for both in `marking/M4-round2.xlsx` and committed the file. The owner did not read them.
3. **Known limits of mock 4:**
   - M4-S43 is close to sample question 7 of the guide: the same structure, but a new setting, and it asks for the fix instead of the cause.
   - The comparison with mocks 1 to 3 (an independent agent): 19 questions are close to an earlier question (the same idea and a similar scene), and 40 share only the idea. The one copy, M4-S43, was rewritten.
   - The findings of rules D2 and D3 of step 6 (D009 to D012, D014, D019 and D020): one wrong idea in too many questions, in scenarios 6, 3 and 1. Finding M4-SC6-R2-F4 (rule D3) still names M4-S03 and M4-S04 after the rewrite of M4-S09.
4. **The findings of rule D4 are ignored** (D013, D015 to D018, D021 to D025), as for mocks 2 and 3.
5. **The owner accepted mock 4.** Step 8 built `mocks/mock-04.questions.json` and `mocks/mock-04.answers.json`. Mock 4 cost $12.83.

## Reason

Plain reason: the owner and the second review found each marked question good. The rule for the findings is the rule of decisions 0059 and 0064.

The correct letters of mock 4 are not balanced: in the 52 questions with one answer, D is correct 22 times and B 8 times (chance is 13). In the 20 questions that the owner marked, B was never correct. The letters stay, because a change after the checks breaks the fingerprints of the build. Decision 0070 balances the letters from mock 5.

## How we decided

The owner gave one instruction for all points: "Round 2: I do not mark. Use the second review in Cowork as the marks", the known limit of M4-S43, "the step 6 findings of mock 4 follow the rule of mocks 2 and 3", and "Accept and build mock 4, and push to GitHub."

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
