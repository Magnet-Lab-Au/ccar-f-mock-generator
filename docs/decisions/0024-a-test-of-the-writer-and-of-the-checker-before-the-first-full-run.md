# 0024: A test of the writer and of the checker before the first full run

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review.
- Diagram: none

## Question

Does the program run a small test before the first full mock?

## Options

1. No test.
2. A test of the writer.
3. A test of the writer and of the checker.

## Decision

Option 3. Before the first full run:

- The writer makes about 10 questions. We compare them with the 12 sample questions of the exam guide (Section 9), for example the length. The owner reads the 10 questions.
- The checker is tested in two parts (decision 0037, item 12). Part 1: call 4a of step 4 answers the 12 sample questions of the exam guide. Their correct answers are known. Step 3 also checks the 12 sample questions, with the rules that need no slot and no reason for each option: A4 to A11. A sample question has no slot and no reason for each option, so rules A1 to A3 cannot run. Part 2: call 4b of step 4 checks the questions that the writer made for this test and that the owner marked, and copies of them that we damage on purpose. Call 4b must pass a question that the owner marked good, and it must fail a damaged copy.

## Reason

The guide names the method for the writer, in the context of batch runs: "Using prompt refinement on a sample set before batch-processing large volumes to maximize first-pass success rates and reduce iterative resubmission costs" (4.5-S4). A full run makes 60 questions. If a prompt is wrong, all 60 have the same error. This is an assumption of the assistant. It is not checked.

The test of the checker has a plain reason. The checker is the weakest part of the pipeline. If call 4a gives a wrong answer to an official sample question, or call 4b passes a damaged copy, the checker is wrong, and we know that before it judges a real question.

The plain reason for the two parts: a sample question has one explanation for the complete question, and 11 of the 12 explanations name letters. It has no reason for each option. Call 4b checks the reason of each option, so it cannot check a sample question.

Not decided yet: who damages the copies, how many there are, and what result is sufficient to start the full run. Decision 0004 applies: no question of the first build is used.

## How we decided

The assistant showed three options and recommended option 3. The owner said yes.

## Exam guide points

4.5-S4
