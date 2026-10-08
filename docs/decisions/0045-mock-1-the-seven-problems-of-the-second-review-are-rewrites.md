# 0045: Mock 1: the 7 problems of the second review are rewrites, and a rewrite can get a new point

- Date: 8 October 2026
- Status: accepted
- Text confirmed by the owner: 8 October 2026
- Diagram: none

## Question

The owner marked the 60 questions of mock 1 blind: 60 good. A second review by a Claude model after the blind marking found 7 problems of the mock as a set, and wrote them as 7 bad marks into a copy of the marking file. 7 bad marks reach the stop limit of decision 0035 ("more than 6 bad marks of 60"). How does the program handle the 7 problems?

## Options

1. The 7 are bad marks of round 1. The mock stops.
2. Round 1 is the blind file of the owner (60 good). The 7 are rewrites, which do not count as bad marks.

## Decision

Option 2.

1. **Round 1.** The blind file of the owner is round 1: `marking/M1-round1.xlsx`, 60 good, SHA-256 a30c0145b79a727ae34c7a4feafec362e8dd6b59cc483cb8ceb85fe19cd7b0e5. The file with the 7 bad marks is a separate record: `marking/M1-round1-second-review.xlsx`, with the notes `docs/reviews/M1-round1-second-review-notes.md`.
2. **A rewrite with no finding of step 6.** The owner names a question and gives a reason. The writer gets a request of step 5 with that question, and the reason as the finding (rule `owner`). This adds to decision 0037, item 3, and decision 0039, where a rewrite needs a finding of step 6.
3. **A rewrite with a new point.** The owner can give a point ID with the rewrite. Code checks three things and stops with a clear message if one fails: the point is in the same task statement as the slot, no other slot of the mock uses it, and this slot did not have it before. Then the writer gets a request of step 2 with the new point, and the text of the other question of the pair, with the instruction not to write that scene. Code saves the point in the decision, as for `new_point` (decision 0039, item 7). Code does not select the point: the owner selects it, because a point that code selects at random can be a twin again.
4. **The rest is as before.** A rewrite does not count as a bad mark. The slot gets 3 new tries, and step 6 runs again for its scenario.

The choices of the owner for mock 1:

| Slot | Problem (second review) | Action |
|---|---|---|
| M1-S09 | Repeat of S07, same scenario | Rewrite with the new point 2.1-K3 |
| M1-S24 | Repeat of S10, different scenario | Rewrite with the new point 1.7-K2 |
| M1-S28 | Repeat of S21, same scenario | Rewrite with the new point 1.1-S1 |
| M1-S60 | Repeat of S48, same scenario | Rewrite with the new point 4.6-K3 |
| M1-S30 | Close copy of sample question 1 of the guide | Rewrite on the same point, with the reason of the second review file |
| M1-S47 | "Select 2.", but the two correct options are one action | Rewrite on the same point, with the reason of the second review file |
| M1-S49 | Ruling 2: more than one wrong option on the confidence of the model in scenario 5 | Rewrite on the same point, with the reason of the second review file |

A script checked the four new points against the plan of mock 1. Each one is in the task statement of its slot, no other slot uses it, and the slot did not have it before. None is a twin of a point that another slot uses. The nearest is 2.1-S4 of S07, near to 2.1-K3 of S09: both are about tool selection, but with a different cause and a different correct action.

No rewrite runs before the owner has decided each of the 19 findings of step 6. Then all rewrites run in one round.

## Reason

- **The 7 are not bad marks.** A bad mark is a blind mark of the owner. Decision 0021 gives the reason for the stop limit: a bad mark shows that "the checker passed a bad question". Here the owner and the second review found each question good on its own, so steps 3 and 4 did not fail. The 7 are problems of the mock as a set. Decision 0037, item 3, already says that a decision after a verdict is a rewrite and not a bad mark.
- **A new point for the twin points.** Plain reason: when two points of one task statement describe one idea, a new scene on the same point is hard. A point that the owner selects can avoid a twin.

Not decided yet:

- The changes to the plan and the rules that the confirmed causes suggest: twin points, the 12 of 15 questions of scenario 5, step 6 inside one scenario, the longest option, and multiple-response slots on a point with one idea. The owner decides them one at a time after mock 1 is repaired.

## How we decided

The owner asked which rule the program applies. The assistant said that the program applies the stop limit, and suggested option 2. The owner agreed. The assistant first suggested that code selects the new point at random. The owner changed that: the owner gives the point, and code checks three conditions, because a random point can be a twin again (example: 4.6-K2 for S60 is the idea of S48). The owner selected the four points.

The owner confirmed the text of this file on 8 October 2026. No independent reviewer checked this file.

## Exam guide points

none
