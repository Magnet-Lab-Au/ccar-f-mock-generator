# 0071: Mock 5 is marked by the second review

- Date: 9 October 2026
- Status: accepted. Decision 0078 corrects one line of this file.
- Text confirmed by the owner: 9 October 2026
- Diagram: none. Step 7 does not change in code.

## Question

Decision 0035 says that the owner marks a sample of 20 questions of each later mock. For mock 4, the owner did not read the questions. Who marks mock 5?

## Options

1. The second review in Cowork marks mock 5. The owner does not mark it.
2. The owner marks mock 5, as before.

## Decision

Option 1.

1. Step 7 makes the marking file as before. The assistant sends it to the owner, and the second review in Cowork marks it.
2. The assistant does not wait for marks of the owner. It records each mark as a mark of the second review, not of the owner, in the commit and in the decision of the mock.
3. The rule of the marking file stays: the file is committed before anybody else reads it.
4. **Known limit: no person reads the questions of mocks 4 and 5.** The writer, the checkers of steps 4 and 6, and the second review are all Claude models. The build guide says this to the participants.
5. **The owner agreed to mark mocks 1 and 2 only.** This is different from decision 0035, which says that the owner marks all 60 questions of mock 1 and a sample of 20 of each later mock. The owner marked mock 3 too (decision 0063). The owner did not read the questions of mock 4 (decision 0069).

## Reason

Plain reason: the owner decided not to mark mock 5. The second review marked the rounds of mocks 1 to 4. In mocks 2 and 3, its marks agreed with the owner's marks. In mock 4, the owner did not read the questions of either round. In mock 1, it found 7 problems of the mock as a set that the owner had not marked (decision 0045). So the second review is not the same as the owner, and its marks are recorded as its own.

## How we decided

The owner said: "For mock 5, I do not mark. Do not wait for my marks. Send me the marking file, and the second review in Cowork marks it."

The owner confirmed the text of this file on 9 October 2026. The second review in Cowork checked it. No independent reviewer of Claude Code checked this file.

## Exam guide points

none
