# 0011: Step 3 of the pipeline: code checks each question

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What is the first check of a question that step 2 wrote?

## Options

1. Code checks each question against the rules that have an exact answer, before a model check.
2. No code check step. A model checks each question against all rules.
3. A different method.

## Decision

Option 1. Step 3 is the code check. Code checks each question against the rules that have an exact answer. No model works in this step. Examples of such rules:

- The record is complete and has the correct format.
- The question agrees with its slot: the scenario, the task statement, the question type.
- The number of correct answers agrees with the number that the question tells the participant to select.
- The length of the question text is in a set range.

## Reason

These rules have one correct answer each. The guide separates "programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance" (1.4-K1), and says that prompt instructions alone have a non-zero failure rate (1.4-K2).

A fixed output format is not sufficient. Strict schemas "eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)" (4.3-K3, also 4.4-K4). So code must check the content of a record.

An empty output must not pass as a success. The guide names "silently suppressing errors (returning empty results as success)" as an anti-pattern (5.3-K4).

The guide does not cover this: that the code check comes before the model check, to save model calls, and the rules on the quality of an exam question, for example a mark that shows the correct answer.

Not decided yet: the full list of rules, each limit, and what happens to a question that fails.

## How we decided

The assistant suggested this step. The rules that need judgment are a different step (decision 0012).

## Exam guide points

1.4-K1, 1.4-K2, 4.3-K3, 4.4-K4, 5.3-K4
