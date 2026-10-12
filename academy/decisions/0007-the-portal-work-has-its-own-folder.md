# 0007: The portal work has its own folder

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

The records of the portal work (the brief, the decisions and the journal) are not about the mock generator. Where do they go?

## Options

1. Into the folders of the mock generator: `docs/decisions/` and `docs/journal.md`.
2. Into a separate folder `academy/` in this repository, with its own decision numbers from 0001.
3. Into a new repository.

## Decision

Option 2. The folder `academy/` has the brief (`brief.md`), the decisions (`decisions/`) and the journal (`journal.md`). Its decisions are numbered from 0001, separate from the decisions of the mock generator. A reference to a decision of the mock generator says "mock decision", for example "mock decision 0053".

## Reason

The owner's reason: separate concerns. The owner will later keep only the files for the mocks in this repository.

Against option 3: the portal work reads many files of the mock generator: the build guide, the diagrams, the decisions and the run records. In one repository, the assistant can read them and link to them directly. One folder with its own numbers is easy to move later. The portal is a separate project, so the folder can move to the code of the portal when that work starts.

## How we decided

The assistant first wrote the six decisions of 12 and 13 October 2026 into `docs/decisions/` as 0080 to 0085, and the brief as `docs/academy-mvp-brief.md`. The owner said that those folders are for the mock generator. The assistant suggested the folder `academy/`, and the owner agreed. Nobody had committed or confirmed the six files, so they moved and became 0001 to 0006.

## Exam guide points

none
