# 0009: Step 1 of the pipeline: code makes the plan of a mock

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What is the first step of the pipeline?

## Options

1. Code makes the plan of a mock before a model writes a question.
2. A model writes many questions first. A later step selects 60 of them for a mock.
3. A different first step.

## Decision

Option 1. Step 1 is the plan. Code makes a list of 60 slots for one mock. Each slot says what one question must be. Example: "Slot 17: scenario 3, task statement 1.2, multiple-choice." No model works in this step.

## Reason

The counts of a mock must hold each time. "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" (1.4-K2). So code makes the plan, not a model.

The work is known before it starts. The guide says to choose "prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks" (1.6-S1, also 1.6-K1). A fixed plan fits.

The guide does not cover this: a list of slots before the writing, and the balance of the 4 scenarios against the domain weights. Those come from the exam form in Sections 3 to 5 (decision 0003).

Not decided yet: what a slot contains exactly, and how the plan selects the 4 scenarios.

## How we decided

The assistant suggested this step. We rejected option 2 because its gaps show only at the end.

## Exam guide points

1.4-K2, 1.6-S1, 1.6-K1
