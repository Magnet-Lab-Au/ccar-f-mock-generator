# 0031: The story of the three document checks

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none
- Changes: decisions 0010 and 0023, the story "the 26 document gaps"

## Question

Decision 0010 (and decision 0023 before this decision) names the story "the 26 document gaps that an independent agent found". Its only source is `docs/journal.md`, line 38, which is the lowest level of the order of trust (decision 0011). How do we tell this story?

## Decision

The story is three rounds of independent checks of all documents, and not "26 gaps":

1. The first check found gaps. The journal gives no count.
2. The second check found 26 gaps.
3. The third check found 20 smaller gaps.

Each round found fewer problems. The counts 26 and 20 come from `docs/journal.md`, lines 38 and 39. The errors that the checks found in confirmed decisions come from mock decision 0078, a higher source.

## Reason

The journal records three checks, not one. The story of three rounds is true to the sources, and it shows how independent checks find fewer problems each time.

## How we decided

The independent review of the plan found the weak source. The assistant read lines 37 to 39 of the journal and recommended the story of three rounds. The owner accepted it.

## Exam guide points

none.
