# 0054: Two-answer questions only on two-answer points

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html` (step 1). Diagram 04 shows the instruction to the writer.

## Question

Change 6 of decision 0046: "A "Select 2." slot needs a point with two ideas." In mock 1, the two correct options of M1-S17, M1-S35 and M1-S47 were two examples of one idea. Only M1-S58 had two different needs with two different answers. How does the plan prevent this?

## Options

1. A list of the points that can carry two different correct answers, a rule of step 1, and an instruction to the writer.
2. No change.

## Decision

Option 1.

1. **The list.** The file `data/two-answer-points.json` has the fields `guide_version` and `points` (point IDs). A point is on the list when its text holds two or more separate actions or facts, so that two correct options can test two different parts of it in one situation. A point that is one action with a list of examples is not on the list. The assistant drafts the list, a reviewer checks it, and the owner confirms it.
2. **Step 1.** The 2 multiple-response slots of each scenario go only to slots whose point is on the list. The seed selects them.
3. **Too few.** If a scenario has fewer than 2 questions on a listed point, code swaps the scenarios of two questions of the same domain, from a scenario that has more than 2. If no swap is possible, step 1 stops with an error that names the scenario. Then the owner uses another seed.
4. **Step 2.** For a slot with 2 answers, the writer gets: "The two correct options test two different parts of the point. They are not two examples of one idea."
5. Mock 1 does not change.

## Reason

Plain reason: a question with 2 answers tests two things. A point with one idea gives only one thing to test, so the writer makes two examples of it, as in mock 1.

The list has 78 points. A script ran step 1 over 2000 seeds (`python3 src/point_groups.py seeds 2000`): each seed gives a plan. With the first draft of the list, seed 734 stopped, because its scenario 6 got only 1 listed point.

Not decided yet:

- A code check of the two correct options. Only a model can judge if they are two parts or two examples.

## How we decided

The assistant suggested the list, the rule of step 1 and the instruction to the writer. The owner said yes.

The assistant drafted 85 points. An independent reviewer checked them against the exam guide. It found 2 points that are sure errors (3.6-K3 and 3.6-S5) and several judgment calls. The assistant removed 8 points and added 8. For 7 points that list the fields of one structure (1.4-K3, 1.4-S3, 2.1-K2, 2.1-S1, 2.2-S1, 5.3-K1, 5.3-S1), the assistant suggested to remove them, because two fields come close to two examples of one idea. The owner agreed.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
