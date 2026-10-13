# 0024: The build guide tables say which task statements a step uses

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none

## Question

Two files say which task statements a step uses, and they differ. The tables of guide points in the build guide list 12 task statements. The popups of the diagrams also cite two more task statements, 3.6 (point 3.6-K4 in diagram 01) and 5.2 (point 5.2-K3 in diagram 08). Diagram 01 also cites three points that no table has: 1.6-K2, 4.4-S2 and 4.6-S1. Which file is the source for the links of a step?

## Decision

The tables of guide points in the build guide (`docs/build-guide/step-*.md`) are the source. If a point appears only in a diagram, the fact agent lists it as a conflict, and the owner decides.

## Reason

Each row of a build guide table says how the step uses the point. A popup of a diagram only names the point.

## How we decided

The independent review of the plan raised it. The assistant checked that diagrams 01 and 08 cite these points. The assistant recommended the build guide tables. The owner accepted it.

## Exam guide points

none.
