# 0014: Step 6 of the pipeline: the program checks the complete mock

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What checks the things that a check of one question cannot see?

## Options

1. A check of the complete mock: a code count, and one model call for each scenario.
2. A code count only.
3. A different method.

## Decision

Option 1. Step 6 is the check of the complete mock. It starts when all 60 slots have a question that passed steps 3 and 4. It has two parts:

- Code counts. Each slot is full. The counts for each scenario, each domain, each task statement and each question type agree with the plan (decision 0009).
- One model call for each scenario reads all questions of that scenario together. It looks for two questions with the same scene, a wrong option that repeats, and the count for ruling 2 (decision 0006).

A question that this step names goes back to step 5 (decision 0013).

## Reason

The guide describes the structure: "splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings" (4.6-K3, also 4.6-S2 and 1.6-K2). Steps 3 and 4 are the pass for each question. This step is the pass across the questions.

The guide does not cover this: the code count against the plan, and the search for a wrong option that repeats.

Not decided yet: the definition of "the same scene", and the output of the model call.

## How we decided

The assistant suggested this step. In decision 0010 we accepted that the writer does not see the other questions of its scenario. This step does that work.

A limit: this step looks at one mock. It does not find a scene that repeats in two different mocks. That depends on how many mocks the program makes, which is not decided.

## Exam guide points

4.6-K3, 4.6-S2, 1.6-K2
