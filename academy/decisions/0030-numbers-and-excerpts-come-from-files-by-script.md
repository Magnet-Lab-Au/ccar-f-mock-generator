# 0030: Numbers and excerpts come from files, by script

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none
- Changes: decision 0011 (check 2), decision 0005 (the excerpts of documentation pages), decision 0014 (a dated copy of each documentation page)

## Question

Two rules cannot hold as written:

1. Decision 0011, check 2: "The page script reads each count from the run files." Some numbers are not in run files. Examples: "14 serious items" is in mock decision 0038, and "27%" is in the guide.
2. Decision 0005: a script takes each excerpt of a card from its source file. A documentation page that the fact agent reads live (decision 0014) is not a file of the repository.

## Decision

1. The page script reads each number from its source file: a run file, a decision, the guide or another file of the order of trust. Nobody types a number by hand.
2. The fact agent saves a dated copy of each documentation page that a part uses, in `academy/sources/`, as `docs/sources/` already does. The script takes the excerpt from that copy.

## Reason

The aim of both rules stays: no number and no excerpt is typed by hand. The new words make the rules possible for all sources.

## How we decided

The independent review of the plan found both items. The assistant recommended the two changes. The owner accepted them.

## Exam guide points

none.
