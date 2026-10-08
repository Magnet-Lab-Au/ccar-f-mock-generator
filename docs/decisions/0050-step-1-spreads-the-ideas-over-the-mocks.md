# 0050: Step 1 spreads the ideas over the mocks

- Date: 8 October 2026
- Status: accepted
- Diagram: `docs/diagrams/02-step-1-plan-the-mock.html` (step 1)

## Question

Decision 0049 says that the program makes 5 mocks. The guide has 95 groups of points (ideas, decision 0047), and 5 mocks have 300 slots. So each idea comes in more than one mock. Without a rule, the seed decides alone: some ideas come in no mock, and others come in all 5. How does the program spread the ideas over the mocks?

## Options

1. A rule of step 1: the ideas that earlier mocks used least come first.
2. Step 1 plans all 5 mocks at one time.

## Decision

Option 1.

1. Before step 1 plans mock N, code reads the points of each built mock with a lower number, from `mocks/mock-NN.questions.json`. A mock that is not built does not count.
2. Code counts how many times each group was used in these mocks.
3. The seed sets the order of the points of a task statement, as before. Then code moves the points of the least-used groups to the front. Inside the same count, the order of the seed stays.
4. The rules of decisions 0047 and 0048 still apply: no two slots in one group, and each choice keeps a full plan possible.
5. The plan file has a new field `earlier_mocks`: the numbers of the mocks that code counted.
6. No model call. Mock 1 does not change. Code counts its final points.

## Reason

Plain reason: a participant who takes all 5 mocks should meet each idea about the same number of times, not one idea in each mock and another idea in none.

A simulation ran 20 series of mocks 2 to 5 after the real mock 1. On average, over the 5 mocks:

| Mocks that test one idea | Without the rule | With the rule |
|---|---|---|
| 0 | 4.8 ideas | 0 ideas |
| 1 | 13.6 ideas | 1.6 ideas |
| 2 or 3 | 35.8 ideas | 63.8 ideas |
| 4 or 5 | 33.1 ideas | 24.7 ideas |
| 6 or more | 7.8 ideas | 5.0 ideas |

A count of 6 or more comes from mock 1, which has more than one slot in some groups. About 7 ideas are in each mock with or without the rule, because a task statement with few groups must always take them (decision 0048).

Option 2 does not fit, because mock 1 exists already, and the owner checks each mock before the next one starts.

Not decided yet:

- How the program prevents the same scene in two mocks.
- How the program selects the scenarios across the mocks.

## How we decided

The assistant suggested this rule and a second rule for the writer (the earlier questions on the same idea, to avoid an old scene). The owner said: "It is getting so so complicated." The assistant suggested to drop both rules. The owner asked: "Is there no simple way to ensure that similar questions are spread out between mocks?" The assistant suggested this one rule in step 1, in code only. The owner said yes.

The assistant first said that each idea then comes in 3 or 4 of the 5 mocks. The simulation shows that this was too exact: most ideas come in 2 to 4 mocks.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
