# 0028: Corrections from the review of the plan

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none
- Changes: decision 0011 (two counts), decisions 0012, 0015 and 0026 (what each agent gets)

## Question

The independent review of the plan found two errors of fact in decision 0011, and a rule that only one agent gets. The texts of 0011, 0012 and 0015 are confirmed, so a new decision corrects them (working rule 26).

## Decision

1. The counts of decision 0011. `docs/decisions/` has 79 mock decisions, 0001 to 0079, not 84. The other 5 files are `TEMPLATE.md` and 4 scripts. The status lines show 19 mock decisions that later decisions changed, not 24. So the build has 89 decisions in all with the 10 academy decisions 0001 to 0010, not 94.
2. Working rules 19 and 28 (no personal files of the owner) go to each agent: the fact agent, the review agent (decision 0012), the whole-picture agent (decision 0015) and the reader agent (decision 0026). Decision 0012 gave them only to the fact agent.

## Reason

A wrong count in a decision can reach a page. Each agent can open a file, so each agent must know which files it must not read or quote.

## How we decided

The independent review of the plan found both items. The assistant checked them: `ls docs/decisions` shows 79 numbered decision files and 5 other files, and 19 status lines name a later decision. The counts are corrections of fact. Item 2 adds to the confirmed decision 0012, so this decision waits for the confirmation of the owner.

## Exam guide points

none.
