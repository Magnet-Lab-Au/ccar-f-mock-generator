# 0075: G042 joins the narrow list

- Date: 9 October 2026
- Status: accepted
- Diagram: none. Diagram 11 shows the narrow ideas.

## Question

The open slot M5-S37 (point 3.3-S3, idea G042, path-scoped rules) failed three tries: once on rule A12, and twice on the stricter rule B9 against M1-S43. Path-scoped rules are in every earlier mock (M1-S33, M1-S43, M2-S32, M3-S58, M4-S59). Task statement 3.3 has only this one idea. What happens to the slot?

## Options

1. Keep the slot on task statement 3.3, add G042 to the narrow list, and give the slot 3 more tries.
2. Move the slot to another task statement with a less-used idea (for example 3.2-S4, argument-hint). Then mock 5 has no question on 3.3, against decision 0027, and the program must change.

## Decision

Option 1.

1. G042 joins the narrow list `data/narrow-ideas.json`, which now has 63 of the 95 groups.
2. M5-S37 stays on point 3.3-S3 and gets 3 more tries.
3. The copy rule still holds: no copy of sample question 6 of the guide (rule B8), and no copy of a question of an earlier mock (rule B9).
4. Decision 0027 holds: each task statement gets at least 1 question. The program does not change.

In the same round, the open slot M5-S60 (point 2.2-S3, idea G029, a judgment call that keeps the stricter rule) failed B9 twice, on the problems of M3-S24 and M2-S07, and once on the form. The owner gave it the new point 2.2-S1 (idea G028, structured error information), which no mock had used.

## Reason

Plain reason: task statement 3.3 has one idea with almost only one problem. The stricter rule cannot pass a new question on it, and moving the slot breaks the rule that each mock covers each task statement.

## How we decided

The assistant suggested to move the slot to 3.2-S4 with an exception to decision 0027. The owner said no: "Keep M5-S37 on task statement 3.3, so decision 0027 holds and the program does not change. Add G042 to the narrow list in a new decision, and give M5-S37 3 more tries."

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
