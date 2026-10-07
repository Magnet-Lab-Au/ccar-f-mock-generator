# 0021: A bad mark of the owner sends the question to step 5, and too many bad marks stop the mock

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Diagram: none

## Question

In step 7 the owner marks a question bad. What happens?

## Options

1. The program repairs that one question only.
2. The program repairs that question. If the sample has too many bad marks, the mock stops.
3. Each bad mark discards the mock.

## Decision

Option 2. A question with a bad mark goes to step 5, with the reason of the owner as the finding. If the sample has too many bad marks, the mock is not released. Then we correct the rules of the checker, and all 60 questions go through the checks again.

## Reason

The reason is plain. A bad mark says two things: this question is bad, and the checker passed a bad question. The owner reads a sample, so more bad questions can be in the part that the owner did not read. Option 1 does not use that fact.

The guide gives the purpose of a sample, in the context of data extraction: "Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns" (5.5-K2). A bad mark is such an error pattern.

The guide does not cover this: what to do with the complete set when the sample fails.

Not decided yet: the number for "too many bad marks".

## How we decided

The assistant showed three options and recommended option 2. The owner asked first how large the sample is (decision 0022), and then chose option 2.

## Exam guide points

5.5-K2
