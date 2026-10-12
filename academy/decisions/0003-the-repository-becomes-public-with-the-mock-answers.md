# 0003: The repository becomes public, with the mock answers in it

- Date: 12 October 2026
- Status: accepted
- Diagram: none

## Question

The owner will make this repository public, and the portal will link to it. The repository has the answers of the 5 mocks in three places. Do the answers stay in the public repository?

The three places, checked on 12 October 2026:

- `mocks/`: 5 answers files, separate from the 5 questions files.
- `runs/`: 488 question files, one for each try. Each option has its mark `"correct"` and its reason, next to the question.
- `marking/`: 12 marking sheets with a column for the correct answer.

Diagram 11 also shows two real questions of mocks 1 and 2 with the correct option marked.

## Options

1. Keep the answers. Accept that a participant can see answers before a mock.
2. Keep the mock content out of the public repository: a separate public repository, or a cleaned copy of the history.

## Decision

Option 1, for now. The owner accepts the risk. The owner can decide again before the repository is made public.

## Reason

The owner's reason: a person who wants to cheat can paste the questions into another AI chat anyway.

The objection that we discussed: the concern is not cheating. It is an honest participant who explores the repository and sees answers before a mock. Then the first-attempt score means less, and the readiness view of the brief depends on first-attempt scores. The answers are easy to find: one run file has the question and its answer together.

A limit: the choice can change only before the repository becomes public. After that, anybody can copy or fork it, and a private repository does not remove those copies.

## How we decided

The assistant named the risk. The owner said that the answers are in JSON files, separate from the questions. The assistant checked the files and showed that the run files and the marking sheets also have the answers. The owner then accepted the risk for now.

## Exam guide points

none
