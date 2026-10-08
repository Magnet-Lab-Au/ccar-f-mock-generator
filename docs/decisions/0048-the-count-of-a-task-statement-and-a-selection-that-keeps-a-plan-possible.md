# 0048: The count of a task statement, and a selection that keeps a plan possible

- Date: 8 October 2026
- Status: accepted
- Text confirmed by the owner: 8 October 2026
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html` (step 1)

## Question

Decision 0047, item 3, says: "No two slots of one mock get points of the same group. The seed selects from the points that are still allowed. If a task statement has no allowed point left, the plan stops with an error that names the task statement."

With the draft of `data/point-groups.json`, that rule can never make a plan:

- Task statement 3.3 is one group, because its 6 points have one correct answer (a rules file with a path). Decision 0027 gives each task statement of Domain 3 two questions.
- In Domain 1, task statements 1.5 and 1.6 have only 2 groups each, and other task statements share these groups. A script ran the rule over 2000 seeds: each seed failed.

How does step 1 make a plan with the groups?

## Options

1. Two changes of step 1: a cap on the count of a task statement, and a selection that keeps a full plan possible.
2. Smaller groups, so that each task statement has enough groups. Then the groups do not catch the known pair M1-S33 and M1-S43 (decision 0046).

## Decision

Option 1. It changes item 3 of decision 0047 and the equal share of decision 0027, item 3.

1. **The cap.** In each domain, the task statements share the questions equally, as before. But a task statement gets no more questions than its number of groups. The questions that are left go to other task statements of the same domain. Each domain keeps its count (decision 0027, item 1).
2. **The extra questions.** The seed sets an order of the task statements of each domain. Code takes the first choice in that order that keeps a full plan possible, over all domains together. A task statement gets at most one extra question.
3. **The points.** The seed sets an order of the points of each task statement. Code takes the first point in that order whose group is free and that keeps a full plan possible.
4. **"Possible"** means: each task statement can still get its count of points, each from a different free group. Code checks this with a matching of task statements to groups. No model makes this check.
5. **The error.** The plan stops with an error only if no plan exists at all. The error names the domains or the task statement.

## Reason

Plain reason: a group means one idea. Two questions on task statement 3.3 are two questions on one idea, which is the repeat that decision 0047 prevents. So the count must follow the groups, not the groups the count.

A prototype ran over 2000 seeds. Each seed gave a plan with 60 slots, the domain counts of decision 0027, and no two slots in one group. The 2000 plans took 4 seconds.

The cost: with the draft of the groups, 11 points never got a question, because a task statement with fewer groups always takes their group. Example: 1.6 must take the group "Per-file passes plus a cross-file integration pass", so 4.6-K3 and 4.6-S2 never get a slot. Another point of the same group still tests the idea of each of these points. After the second review of the groups, the number is 15.

After the second review of the groups, the owner agreed that the 9 points of 4.2 and three points of 3.5 are one group. So 4.2 also gets one question for each mock.

## How we decided

The assistant drafted the groups and ran the rule of decision 0047 over 2000 seeds. Each seed failed. The assistant suggested the two changes and showed the result of a prototype. The owner asked for a short explanation, and then said yes.

One independent reviewer checked this file, the code of step 1, diagram 02 and the build guide section on 8 October 2026. The assistant fixed its findings. The main fix: code gave the extra questions one domain at a time and never went back, so it could stop although a plan existed. Now it searches over all domains together. The owner confirmed the text of this file on 8 October 2026.

## Exam guide points

none
