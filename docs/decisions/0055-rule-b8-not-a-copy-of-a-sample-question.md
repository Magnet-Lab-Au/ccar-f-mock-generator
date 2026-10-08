# 0055: Rule B8: not a copy of a sample question

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/06-step-4-check-by-a-model.html` (step 4). Diagram 04 shows the list of rules of the writer.

## Question

Change 7 of decision 0046: "No rule compares a question with the 12 sample questions of the guide." In mock 1, M1-S30 was a close copy of sample question 1, and M1-S60-T2 was a close copy of sample question 12. How does the program find a copy?

## Options

1. A new rule for the model check, B8, with the 12 sample questions in call 4b.
2. A code check of the word overlap with each sample question.

## Decision

Option 1.

1. **Rule B8:** "The question is not a close copy of a sample question of the exam guide: not the same scene with the same correct action."
2. **Call 4b** gets the 12 sample questions of the guide, each with its correct answer, before the rules. The text of B8 says that a question on the same point as a sample question passes if its scene and its correct action are different.
3. **The writer** gets B8 in its list of rules, as each other rule. The list now has 20 rules: A1 to A12 and B1 to B8.
4. A question that fails B8 goes to step 5, as for each other rule of call 4b.
5. Mock 1 does not change.

## Reason

A script measured the word overlap of each question of mock 1 with the 12 sample questions. The known copy M1-S30-T1 had a lower overlap than M1-S40-T1, which is not a copy. A copy keeps the scene and the correct action, but it changes the words. So code does not find it, and a model must judge it.

The cost: about 18,000 characters more input for each call 4b, about 4,500 tokens. For 60 questions and some tries, that is about $1.20 more for each mock, at $4 for each million input tokens (decision 0042). This is an estimate. It is not measured.

Not decided yet:

- If the writer also gets the rule to use a different scene than the 3 sample questions that it sees as examples.

## How we decided

The assistant measured the word overlap and showed that a code check does not separate a copy. It suggested rule B8 in call 4b. The owner said yes.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
