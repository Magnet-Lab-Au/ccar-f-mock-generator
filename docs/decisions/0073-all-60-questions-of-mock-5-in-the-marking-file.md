# 0073: All 60 questions of mock 5 in the marking file

- Date: 9 October 2026
- Status: accepted
- Text confirmed by the owner: 9 October 2026
- Diagram: `docs/diagrams/09-step-7-the-owner-marks-the-questions.html` (step 7) shows it.

## Question

Decision 0022 says that a later mock puts a sample of 20 questions in the marking file. Decision 0071 says that the second review in Cowork marks mock 5. How many questions of mock 5 go in the marking file?

## Options

1. All 60, as for mock 1.
2. A sample of 20, as for mocks 2 to 4.

## Decision

Option 1.

1. The marking file of mock 5 has all 60 questions. The code has a set of the mocks that mark all 60: mocks 1 and 5.
2. The stop limit of mock 1 applies: more than 6 bad marks of 60 stop the mock (decision 0035).
3. The run of mock 5 had started with the old code, which picks a sample of 20. The assistant stopped the run after 4 questions, changed the code and started the run again. The control reads its records, so the 4 written questions stay. The cost of the stopped run is not in `runs/mock-05/usage/`, because the program saves the cost at the end of a run. It was about 4 written questions and their checks, under $1.

## Reason

Plain reason: no person reads the questions of mock 5 (decision 0071). So the second review, as the only reader, reads all of them, not a sample.

The stop limit for 60 marks is the limit of mock 1. The owner did not name a limit. The assistant used the one that the decisions already have for 60 marks.

## How we decided

The owner said: "Put all 60 questions of mock 5 in the marking file." The assistant chose the stop limit of mock 1 for 60 marks.

The second review in Cowork checked this file. The owner confirmed the text of this file on 9 October 2026.

## Exam guide points

none
