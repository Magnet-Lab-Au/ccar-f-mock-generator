# 0068: Three more narrow ideas

- Date: 9 October 2026
- Status: accepted
- Diagram: none. Diagram 11 shows the narrow ideas.

## Question

Decision 0066 confirmed a list of 20 narrow ideas: ideas with almost only one problem, which keep the copy rule of B9. In mock 4, three slots failed the stricter rule B9 three times, each time on the same problem as an earlier question: M4-S06 (G074, retry fails when the information is absent), M4-S50 (G060, one message for interacting issues) and M4-S54 (G059, the interview pattern). Do these ideas join the list?

## Options

1. Add G059, G060 and G074 to the list of narrow ideas, and give the three slots 3 more tries.
2. Keep the list, and give the slots new points. Each of these task statements has no free point outside the same idea, so a new point does not help.

## Decision

Option 1. The list `data/narrow-ideas.json` now has 24 groups. Added:

| Group | The one problem |
|---|---|
| G059 | A developer in an unfamiliar domain misses design considerations: the interview pattern before implementing |
| G060 | Several issues to fix: one message for interacting issues, a sequence for independent ones |
| G074 | A retry cannot help when the information is absent from the source |
| G041 | Callers behind a wrapper module: list the exported names, then search for each |

M4-S06, M4-S50 and M4-S54 get 3 more tries, with the copy rule. In the same round, the owner gave M4-S23 the new point 2.1-S1 (decision 0045), and M4-S27 3 more tries, because its last try failed on the form, not on B9.

**Addition, the same day.** M4-S27 then failed B9 three more times, each time on the problem of M2-S11 (a function changes behind a wrapper module, and the answer is to list the wrapper's exports and search for each). Its idea G041 has one point (2.5-S5) and almost only one problem. The owner added G041 to the list and gave M4-S27 3 more tries. The copy rule still holds: not the same scene, answer and wrong options as M2-S11.

This adds to the confirmed list of decision 0066.

## Reason

Plain reason: each of the three slots failed B9 three times on the same problem as an earlier question, and each idea has almost only one problem. For such an idea, the stricter rule cannot pass a new question, so only a copy should fail (decision 0066, item 6).

## How we decided

The assistant suggested to add the three ideas, the new point for M4-S23 and more tries for M4-S27. The owner agreed to all three. After the second failure of M4-S27, the assistant suggested G041 too, and the owner agreed. The owner also asked for a check of all point groups before mock 5: each group where one point gives both the scene and the answer, as for G041. The list waits for the owner.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
