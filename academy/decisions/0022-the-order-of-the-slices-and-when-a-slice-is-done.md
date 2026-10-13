# 0022: The order of the slices, and when a slice is done

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none

## Question

Decision 0015 defines a slice, but no decision gives the order of the slices or says when a slice is done. How many review rounds does a part get?

## Decision

The order of the slices:

1. The top of tab 2, plus step 5
2. Steps 0 to 4 and 6 to 8
3. The build in Claude Code
4. The top of tab 1 (the map and "How we broke it down"), plus domain 1 and its task statements
5. Domain 2
6. Domain 3
7. Domain 4
8. Domain 5

A slice is done when the review lists are empty, or when the owner accepts the items that are left. Each part gets at most 2 review rounds. After that, the owner decides. The owner says when a slice is done.

## Reason

The independent review of the plan found no order and no definition of done. It warned that the mock builder already had a review loop with no end (mock decision 0038). A limit of rounds and a decision by the owner stop that loop. Slice 1 tests the exploded view on real content before the other slices repeat it.

## How we decided

The independent review of the plan raised it. The assistant recommended the order and the limit of 2 rounds. The owner accepted it.

## Exam guide points

none.
