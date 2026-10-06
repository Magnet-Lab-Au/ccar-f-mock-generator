# 0038: A simple control for mock 1, written as code with tests

- Date: 7 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026
- Diagram: none

## Question

The first review found 14 serious items. Decision 0037 answered them. The second review found 10 new serious items, and most of them come from the rules of decision 0037. How do we stop this cycle?

## Options

1. Answer the 10 new items in words, change the files, and review again.
2. Make the control simple for mock 1, and write the control as code with tests.

## Decision

Option 2.

1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5. The limits of decisions 0033 and 0037 stay: 3 tries, and "cannot decide" two times.
2. **Each other failure waits for the owner.** A slot that is `open`, a finding of step 6, a bad mark, and a call that fails 3 times. The program does no automatic repair for them.
3. **Step 6 sends no question back.** It runs when all 60 slots have the status `passed`. Each of its findings goes into the report: `fail` and `cannot_decide`. This changes decisions 0014 and 0034, and items 3 and 7 of decision 0037.
4. **The owner is the limit.** The owner marks first, with no verdict in view. Then the owner sees the findings of step 6 and selects `ignore` or `rewrite` for each one. A bad mark is a `rewrite`. Each new question goes through the automatic loop. Then step 6 runs again for its scenario, and the owner marks the new questions. No count limits these rounds, because the owner starts each one.
5. **Step 8 starts when the owner accepts the mock.** Code checks the conditions before it builds.
6. **The control is code.** It is one part of the program, with tests that make no model call. A fake writer and fake checkers give the answers that a test tells them to give. Each case is one test. The 10 cases of the second review are the first tests. This changes the method of decision 0001: the design of the control is not completed in words first.
7. **The files follow the code.** When the tests pass, decisions 0027 to 0036 are corrected so that they describe what the code does.
8. **Rule A11.** The question text does not have "NOT" or "EXCEPT" in capital letters. The last sentence of the question text does not have "not" or "except" in small letters. The options do not count.
9. **A slot that goes back.** A question is sent back when a later record names it: a `rewrite` or a bad mark of the owner. The slot then has the status `to_write` until the new try exists.

The 10 new serious items of the second review (`docs/reviews/review-decisions-0024-to-0037.md`):

| Item | Result |
|---|---|
| 1. Rule A11 | Closed by part 8 |
| 2. The status of a slot that goes back | Closed by part 9 |
| 3. Step 6 asks the owner before the marking | Removed by part 3 |
| 4. After `ignore`, the scenario cannot pass | Closed by parts 4 and 5 |
| 5. The count of the runs of step 6 | Removed by part 4 |
| 6. The values of `state`, and the IDs | Goes to the code and its tests |
| 7. Where `new_point` stores the point | Goes to the code and its tests |
| 8. The request after `more_tries` or `new_point` | Goes to the code and its tests |
| 9. A call that fails 3 times | Goes to the code and its tests |
| 10. The exact conditions before step 8 | Goes to the code and its tests |

A correction of decision 0037, Reason, item 8. The sentence on point 1.4-K2 is too strong. The point says only: "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate". Enforcement by code is in a different point: "The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering" (1.4-K1). The guide wrote both points for the workflow of an agent.

## Reason

- **The simple control.** Plain reason: the path with no failure is simple. The 10 new items are all cases where a failure follows a failure. Each automatic path for such a case has a limit, a status and an action, and these parts multiply. Each number in them is a guess. The owner reads all 60 questions of mock 1 in each case, so a decision of the owner costs little there. After mock 1 we know which failures occur, and we automate only those.
- **Code with tests.** Plain reason: a rule in words can clash with a rule in a different file, and a reviewer finds that only by following one case through all files. A test runs the case. A case with no path makes the test fail.
- **A limit.** A test shows that a case has a path. It does not show that the path is good. The owner decides that.

Not decided yet:

- Where the git repository is.
- Which automatic paths come back after mock 1.
- The answers to items 6 to 10. The code and its tests give them, and the owner sees each one before it is final.

## How we decided

The owner and the assistant started to close the 10 new items one at a time. After item 2 the owner said: "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." The assistant agreed. The owner asked what the theme of the problems is: too many rules, or too much control. The answer: too much automatic repair, designed before one real run.

The assistant said first that the simple control removes most of the 10 items. That was too strong. It removes 2.

No independent reviewer checked this file.

## Exam guide points

1.4-K1, 1.4-K2
