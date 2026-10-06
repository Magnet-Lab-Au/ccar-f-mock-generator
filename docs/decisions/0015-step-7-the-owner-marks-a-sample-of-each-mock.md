# 0015: Step 7 of the pipeline: the owner marks a sample of each mock

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What shows if the model check is correct?

## Options

1. The owner marks a sample of each mock before its release.
2. The owner marks a sample of the first mock only.
3. No person step.
4. A different method.

## Decision

Option 1. Step 7 is the sample of the owner. For each mock, the program selects a sample at random, with questions from each scenario and each domain. The owner marks each question good or bad, with one reason. The owner does not see the verdict of the checker during the marking. Code then compares the marks with the verdicts, and shows the result for each scenario and each domain.

## Reason

The guide names the method: "Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns" (5.5-K2, also 5.5-S1).

The result is shown for each segment, because of the "risk that aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields" (5.5-K1).

The rule to reduce the work of the owner later: "verify consistent performance across all segments before reducing human review" (5.5-S2).

The guide does not cover one detail of the decision: the owner marks with no verdict in view.

Not decided yet: the size of the sample, and what happens when the owner marks a question bad.

## How we decided

The assistant suggested this step. The cost is the time of the owner for each mock. The assistant suggested a sample for each mock at the start, and a smaller one later if the evidence permits.

## Exam guide points

5.5-K2, 5.5-S1, 5.5-K1, 5.5-S2
