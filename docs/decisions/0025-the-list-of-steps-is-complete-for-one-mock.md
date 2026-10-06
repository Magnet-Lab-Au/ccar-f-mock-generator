# 0025: The list of steps is complete for one mock

- Date: 6 October 2026
- Status: accepted
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

Is the list of pipeline steps complete?

## Options

1. Yes, for one mock.
2. No. A step is missing or must change.

## Decision

Option 1. The pipeline for one mock is steps 0 to 8 (decisions 0009 to 0017), with the rules of decisions 0018 to 0024. The design of each step can start.

## Reason

No exam guide point gives this reason. The reason is plain. The assistant looked for a case with no path: a question that fails, a question that the checker cannot decide, a question that the owner marks bad, and a first run with a wrong prompt. Each case now has a path.

Not decided yet: how the program prevents the same scene in two different mocks. That depends on how many mocks the program makes.

## How we decided

The owner did not confirm the list at the first question, and asked if everything was covered. The owner and the assistant then closed four open questions (decisions 0020 to 0024). The owner then confirmed the list.

## Exam guide points

none
