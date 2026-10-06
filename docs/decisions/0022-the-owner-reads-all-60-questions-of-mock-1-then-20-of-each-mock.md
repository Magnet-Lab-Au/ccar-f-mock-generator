# 0022: The owner reads all 60 questions of mock 1, then 20 of each later mock

- Date: 6 October 2026
- Status: accepted
- Diagram: none

## Question

How many questions does the owner mark in step 7?

## Options

1. A small sample of each mock, for example 12.
2. All 60 questions of the first mock, then 20 of each later mock.
3. All 60 questions of each mock.

## Decision

Option 2. For mock 1 the owner marks all 60 questions. For each later mock the owner marks 20 questions, 5 from each scenario. The number goes lower only when the checker agrees with the marks of the owner.

## Reason

The reason is plain arithmetic. A sample with zero bad marks still permits bad questions in the part that the owner did not read. A script calculated the limits for a mock of 60 questions, with 95% confidence: a clean sample of 12 permits up to 11 bad questions, a clean sample of 20 permits up to 6, and a clean sample of 30 permits up to 4. The 60 marked questions of mock 1 also give a set to test the checker against.

The guide gives the rule to go lower, in the context of data extraction: "Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review" (5.5-S2).

Not decided yet: the measure for "the checker agrees with the marks of the owner".

## How we decided

The owner asked how many questions the sample has. The number was not decided. The assistant showed the table of limits and recommended option 2. The owner said yes.

## Exam guide points

5.5-S2
