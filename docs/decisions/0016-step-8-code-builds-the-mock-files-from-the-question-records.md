# 0016: Step 8 of the pipeline: code builds the mock files from the question records

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

Who makes the files of a mock that the portal shows?

## Options

1. Code builds the mock file and the answer key from the stored question records. Nobody edits an output file by hand.
2. A person or an assistant can correct an output file directly.

## Decision

Option 1. Step 8 is the build of the files. The stored question records are the one true copy. Code builds the mock file and the answer key from them. Nobody edits an output file by hand. To change a question, change its record, and code builds the files again.

## Reason

No exam guide point gives this reason. The reason is plain. If a question exists in two places and a person can edit one of them, the two can disagree, and nobody knows which one the checks saw. With one true copy and files that code builds from it, a question in a mock is always the question that passed the checks.

Not decided yet: the file format of a mock and of its answer key, and if a changed record must pass the checks again.

## How we decided

The assistant suggested this step. The owner did not understand the first form of the question. The assistant then explained it with an example: an invoice from accounting software. You correct the entry in the software and print again. You do not write on the printed invoice.

## Exam guide points

none
