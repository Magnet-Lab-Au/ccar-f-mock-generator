# 0033: One long page in practice

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none

## Question

The 1.1 samples are two short pages. Each tab is one long page with many parts (decision 0010). How are the figures numbered, where is the list of sources, and how do the IDs stay unique?

## Decision

1. Each part numbers its own figures with its own number: Fig. 1.1-1, 1.1-2 in task statement 1.1, and Fig. 5-1, 5-2 in step 5.
2. Each part lists its own sources at the end of its Depth. There is no single list at the end of the page.
3. Each ID on the page starts with the anchor of its part, such as `ts-1-1-` or `step-5-`. A script checks that no ID repeats.

## Reason

A part must make sense alone, because a link can open it directly (decision 0010). Its figure numbers and its sources then stay with it. A repeated ID breaks a link or a popup.

## How we decided

The independent review of the plan found that the long page was not planned. The assistant recommended the three rules. The owner accepted them.

## Known limits

- The anchors work in the prototypes. How they work under React Router in the portal is not checked.

## Exam guide points

none.
