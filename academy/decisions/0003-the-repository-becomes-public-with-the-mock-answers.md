# 0003: The repository becomes public, with the mock answers in it

- Date: 12 October 2026
- Status: accepted
- Diagram: none

## Question

The owner will make this repository public, and the portal will link to it. The repository has the answers of the 5 mocks in four places. Do the answers stay in the public repository?

The four places, checked on 12 and 13 October 2026:

- `mocks/`: 5 answers files, separate from the 5 questions files.
- `runs/*/questions/`: 488 question files, one for each try. Each option has its mark `"correct"` and its reason, next to the question.
- `runs/*/checks/`: 477 files of step 4. Each has the blind answer of the checker and if it agrees with the marks, so it also gives the key.
- `marking/`: 11 marking sheets of the mocks and 1 test sheet, each with a column for the correct answer.

Diagram 11 also shows three real questions with the correct option marked: M1-S28-T2 and M2-S08-T2 of the built mocks, and M2-S08-T1, a try that failed.

## Options

1. Keep the answers. Accept that a participant can see answers before a mock.
2. Keep the mock content out of the public repository: a separate public repository, or a cleaned copy of the history.

## Decision

Option 1, for now. The owner accepts the risk. The owner can decide again before the repository becomes public.

## Reason

The owner's reason: a person who wants to cheat can paste the questions into another AI chat anyway.

The objection that we discussed: the concern is not cheating. It is an honest participant who explores the repository and sees answers before a mock. Then the first-attempt score means less, and the readiness view of the brief depends on first-attempt scores. The answers are easy to find: one run file has the question and its answer together.

The brief (`academy/brief.md`) has three lines about mock content after the MVP: "No mock questions or answers in any downloadable file", links to mock questions "shown only after the person has sat that mock", and a public version that "stays separate from the portal". A public repository with the answers does not agree with the first two lines. This decision accepts that difference for now. The third line is about a public version of the portal, not about this repository.

A limit: the choice can change only before the repository becomes public. After that, anybody can copy or fork it, and a private repository does not remove those copies.

## How we decided

The assistant named the risk. The owner said that the answers are in JSON files, separate from the questions. The assistant checked the files and showed that the run files and the marking sheets also have the answers. The owner then accepted the risk for now.

## Exam guide points

none
