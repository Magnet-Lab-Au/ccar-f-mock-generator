# 0010: Step 2 of the pipeline: a model writes one question for one slot

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What writes the questions, and how many in one call?

## Options

1. One API call writes one question, for one slot.
2. One API call writes all questions of one scenario, about 15.
3. A different method.

## Decision

Option 1. Step 2 is the writer. For each slot of the plan (decision 0009), one API call writes one question. 60 slots give 60 calls. Each call receives its slot and the parts of the guide that the slot needs.

## Reason

No exam guide point gives this reason. The reason is plain. One call makes one record with one ID, so each later verdict connects to exactly one question. If one question fails, the program writes that one again and the others do not change. Each call gets the complete text that its one question needs.

Not decided yet: the exact input of a call, the output format, and which model.

## How we decided

The assistant suggested this step. We accepted one disadvantage: a writer that sees one slot does not see the other questions of its scenario. It cannot prevent two questions with the same scene, and it cannot count for ruling 2 (decision 0006). A different step does that work (decision 0014).

We rejected option 2. Its writer sees the other questions, but one bad output spoils about 15 questions.

## Exam guide points

none
