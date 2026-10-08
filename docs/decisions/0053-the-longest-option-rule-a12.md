# 0053: The longest option (rule A12)

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/05-step-3-check-by-code.html` (step 3). Diagrams 02 and 04 show the field of the slot and the instruction to the writer.

## Question

Change 5 of decision 0046: "No rule looks at the longest option in the set of 60." In the built mock 1, the correct option is the longest option (by characters) in 37 of the 52 questions with 1 answer. Chance is 13. In the 8 questions with 2 answers, the longest option is correct in 6. Chance is about 3. Rule A7 looks at one question only, and each question passed it. How does the program prevent this pattern?

## Options

1. A field of the slot, an instruction to the writer, and a rule of step 3 in code.
2. A rule that the correct option is never the longest. Then a participant learns that the longest option is always wrong.

## Decision

Option 1.

1. **Step 1.** Each slot gets the field `longest_may_be_correct` (true or false). The seed sets it to true for 13 of the 52 slots with 1 answer, and for 3 of the 8 slots with 2 answers. These are the chance numbers: 1 in 4, and 2 in 5.
2. **Step 2.** The writer gets the field in the slot, and a new rule in its list: "A12. When the slot has "longest_may_be_correct": false, at least one wrong option is longer (in characters) than each correct option."
3. **Step 3.** Code checks rule A12. When the field is false and no wrong option is longer than each correct option, the question fails. An equal length fails too. The question goes to step 5 with the finding.
4. A slot with no field (the plan of mock 1) does not get rule A12. Mock 1 does not change.
5. The list of rules for a good question now has 19 rules: A1 to A12 and B1 to B7.

## Reason

Plain reason: a participant who always selects the longest option must not gain from it. With the field, the longest option is correct about as often as chance.

The cost: some questions need one more try. Step 5 already has the limit of 3 tries (decision 0033).

Not decided yet:

- The length in words. Rule A12 counts characters.

## How we decided

The assistant counted the longest options in the built mock 1 and suggested the field, the instruction and the rule. The owner said yes.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
