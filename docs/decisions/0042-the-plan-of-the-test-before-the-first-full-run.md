# 0042: The plan of the test before the first full run

- Date: 7 October 2026
- Status: accepted
- Diagram: none

## Question

Decision 0024 says that a test of the writer and of the checker comes before the first full run. It left open: who damages the copies, how many copies there are, and what result is enough to start the full run. What is the plan of the test?

## Options

1. One proposal of the assistant with four parts.
2. A different plan.

## Decision

Option 1. The records of the test go to `runs/test-0024/`, not to `runs/mock-01/`, so that mock 1 starts clean. The script is `src/test_0024.py`. Each part is a separate command, and no part runs before the yes of the owner.

1. **Part 1, the writer.** The writer (step 2) makes one question for each of 10 slots of the plan of mock 1. The slots cover the 4 scenarios, the 5 domains and 2 multiple-response questions. Code selects them from the plan with a fixed method. Each question gets one writer call, with no new try, so that the result shows the first-pass quality. Step 3 checks each question. Code builds a marking file (step 7) for the owner, `marking/test-0024-round1.xlsx`. The owner marks each question good or bad.
2. **Part 2, call 4a on the guide.** Call 4a answers the 12 sample questions of the guide. Their correct answers are known. Enough: 12 of 12. The owner sees each miss before the full run.
3. **Part 3, call 4b.** Call 4b checks each question that the owner marked good. Each one must pass. For each such question, one damaged copy breaks one rule from B1 to B6. Each rule gets at least one copy. Code makes the damage of B1: it moves the mark "correct" to a wrong option. The assistant writes the other damages by hand in one file, `runs/test-0024/damaged.json`, which the owner can read. Each damaged copy must fail on its rule. Enough: each good question passes, and each damaged copy fails on its rule.
4. **Part 4, step 6.** Decision 0034, part 7, adds a test of call 6a with two questions of the same scene in a set of 15. It needs 15 questions, so it is a later, separate part.

The script prints the real numbers of input and output tokens of each part, and the cost at the prices of the page "Pricing" (https://platform.claude.com/docs/en/about-claude/pricing, section "Model pricing", read on 7 October 2026: Claude Opus 5.5, $4 per million input tokens and $20 per million output tokens).

## Reason

- **One call for each question in part 1.** Decision 0024 uses this point, for batch runs: "Using prompt refinement on a sample set before batch-processing large volumes to maximize first-pass success rates and reduce iterative resubmission costs" (4.5-S4). The first-pass result is what the test measures.
- **A separate folder.** Plain reason: the records of mock 1 are never written over. A test question in `runs/mock-01/` would become a try of mock 1.
- **12 of 12 in part 2.** Plain reason: the sample questions are the official questions of the guide. A checker that answers one of them wrong can mark a good question bad.
- **Damage by hand.** Plain reason: a damage that a model makes can be too weak or too clear. The owner can read each one.
- **The cost.** The assistant estimated $5 to $10 for parts 1 to 3, about 55 calls. That estimate is not checked. The script shows the real numbers.

Not decided yet:

- What happens if the test is not enough: a change of the prompts, of the model or of the effort. The owner decides with the results.

## How we decided

The assistant showed the plan with the cost. The owner said yes. The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

4.5-S4
