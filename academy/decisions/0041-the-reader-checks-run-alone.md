# 0041: The reader checks run alone, after the plan of 14 October 2026

- Date: 14 October 2026
- Status: accepted. The owner accepted the plan by starting `/goal` with its condition.
- Text confirmed by the owner: not yet. An independent agent checks it with the report (working rule 35).
- Diagram: none
- Changes: none. Working rules 32 and 33 apply.

## Question

The owner will review the two tabs and write notes. While the owner does not review, what can the assistant check?

## Decision

The assistant runs `academy/check-plan.md` alone, from start to end. The plan has 23 checks: 29 check agents and 7 scripts. The assistant fixes only clear errors and lists all other items for the owner in `academy/checks/findings.md`. No fix changes an element ID, a figure number, a heading or a popup title. The tag `owner-review-2026-10-14` marks the version that the owner reads. The mocks and the mock builder do not change. The yes to the plan covers one push to GitHub at the end.

## Reason

The owner said that a loop of small corrections is not efficient. The owner wants one full pass of notes. Checks that read the pages as a stranger would find the weak places before that pass.

## How we decided

The assistant proposed a list of checks. The owner liked all of them and asked for more checks from the side of the reader ("Read the pages as an exam candidate"). The assistant added 13 more, and the owner said: "Okay all of it. You will be doing it autonomously like before." The assistant wrote the plan. An independent agent found 14 problems, 5 of them high, and the assistant fixed all 14. The owner asked if the mocks and the mock builder change. They do not, and the plan now names each folder that the checks only read. The assistant proposed the `/goal` condition. The owner asked if it was good enough. The assistant named three gaps and gave a better condition, and the owner started `/goal` with it.

## Exam guide points

None.
