# 0013: Step 5 of the pipeline: a failed question goes back to the writer with the findings

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What happens to a question that fails step 3 or step 4?

## Options

1. It goes back to the writer with the findings, up to a limit of tries.
2. It is discarded, and a new call writes a question for the slot with no findings.
3. A different method.

## Decision

Option 1. Step 5 is the new try. A new call writes the question for that slot again. It receives the slot, the failed question and the exact findings. The number of tries has a limit. If the limit is reached, the slot stays open, the program reports it, and the mock is not complete.

## Reason

The guide names the method: "appending specific validation errors to the prompt on retry to guide the model toward correction" (4.4-K1), with "the original document, the failed extraction, and specific validation errors" (4.4-S1).

The guide names the limit: "retries are ineffective when the required information is simply absent from the source document" (4.4-K2, also 4.4-S2). So the tries have a limit, and an open slot goes to a person.

Not decided yet: the limit, and who decides on an open slot.

## How we decided

The assistant suggested this step. We rejected option 2. Its writer does not know what was wrong, so it can make the same error again.

## Exam guide points

4.4-K1, 4.4-S1, 4.4-K2, 4.4-S2
