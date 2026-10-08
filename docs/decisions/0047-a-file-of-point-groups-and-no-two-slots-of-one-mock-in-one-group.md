# 0047: A file of point groups, and no two slots of one mock in one group

- Date: 8 October 2026
- Status: accepted
- Diagram: none. Diagram 02 (step 1) changes when the rule is built.

## Question

Changes 1 and 2 of decision 0046: two points of one task statement often describe one idea, and twin points also exist across task statements. The plan of step 1 selects points at random, so one mock can get two questions on one idea. How does the plan prevent that?

## Options

1. A file that groups the 240 points by idea, and a rule of step 1: no two slots of one mock get points of the same group.
2. No change of the plan. Step 6 finds the repeats later.

## Decision

Option 1. It answers changes 1 and 2 of decision 0046 together.

1. **The file** `data/point-groups.json` has the field `guide_version` and a list `groups`. Each group has `id` (G001, G002, ...), `idea` (a few words) and `points` (point IDs). Each of the 240 points is in exactly one group. A point with no twin is a group of one. A group can hold points of different task statements. The file is in a new folder, `data/`, because rule 27 protects the files in `reference/`.
2. **Who makes it.** The assistant drafts the groups from the 240 texts. A script checks that each point exists and is in exactly one group. An independent reviewer checks the groups. The owner confirms the file. No model call of the program makes it.
3. **The rule of step 1.** No two slots of one mock get points of the same group. The seed selects from the points that are still allowed. If a task statement has no allowed point left, the plan stops with an error that names the task statement.
4. **Checks.** A script runs the rule over many seeds and shows that a plan is always possible. Tests check the rule.
5. **A test against mock 1.** Each known repeat pair of mock 1 (decisions 0045 and 0046, and the notes of the second review) must be in one group. The plan of mock 1 goes through the new rule. The rule must reject it and name those pairs. The result shows which known pairs the groups catch and which they do not.
6. **For the confirmation of the owner,** the assistant shows only the groups with two or more points, as a short table (the idea and the point IDs), and the number of groups with one point.
7. Mock 1 does not change. The rule applies to new plans.

## Reason

Plain reason: the second review of mock 1 found that most repeats come from two points on one idea, inside one task statement and across task statements (decision 0046). The plan is code, so code can prevent this before any question is written. A check after the writing (step 6) costs a rewrite, and it compares only one scenario.

Not decided yet:

- If the rule also applies across mocks, so that mock 2 does not repeat an idea of mock 1. That depends on the number of mocks.

## How we decided

The assistant suggested the file and the rule, and to treat changes 1 and 2 as one decision. The owner agreed, and added the test against mock 1 and the form of the table for the confirmation.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
