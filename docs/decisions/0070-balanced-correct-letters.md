# 0070: Balanced correct letters

- Date: 9 October 2026
- Status: accepted. Academy decision 0055 changes item 4: the converter mixes the options once, and a random order on each attempt is later work.
- Text confirmed by the owner: 9 October 2026
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html` (step 1). Diagram 04 (step 2) shows how the writer's options get their letters.

## Question

Code mixes the options of each question at random (decision 0029, part 4.1). No rule balances the letters over a mock. In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. Chance is 13. Mock 1 had B 17 times and C 7 times. A participant can learn to guess a letter. How does the program balance the letters?

## Options

1. The plan sets the correct letter of each slot, balanced over the mock. Code puts the correct option at that letter.
2. No change.

## Decision

Option 1, from mock 5.

1. **Step 1** gives each slot a new field `correct_letters`. Each of A, B, C and D is the answer of 13 of the 52 slots with one answer. The 16 answers of the 8 slots with two answers spread over A to E, 3 or 4 each, two different letters in each slot. The seed sets which slot gets which letter.
2. **Step 2** (and step 5) puts the correct options at the letters of the slot. The wrong options take the other letters, in the mixed order of decision 0029.
3. A plan with no field (mocks 1 to 4) keeps the mixed order. Mocks 1 to 4 do not change.
4. **A note for the portal:** the portal shows the options in a random order on each attempt, because the letters in mocks 1 to 4 are not balanced. Then the letter of an answer does not help a participant. The format of the portal is not known yet (decision 0036). The converter must keep the link between each option and its reason.

## Reason

Plain reason: in the exam, a participant must not gain from a letter. A balanced count removes the pattern in a mock. A random order in the portal also removes it in mocks 1 to 4.

## How we decided

The assistant counted the letters of mock 4 on the request of the owner and suggested the rule for mock 5. The owner agreed, and added the note for the portal.

The owner confirmed the text of this file on 9 October 2026. The second review in Cowork checked it. No independent reviewer of Claude Code checked this file.

## Exam guide points

none
