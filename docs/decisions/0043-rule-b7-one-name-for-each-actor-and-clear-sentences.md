# 0043: Rule B7: one name for each actor, and clear sentences

- Date: 7 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026
- Diagram: none

## Question

In the test of decision 0042, the owner marked one question bad (T-M1-S05) with this reason: "The question is confusing and needs calrification. I had to read the question more than one time. Use one name for the actor, not 'the subagent' and 'Claude'. Make the sentences shorter. Do not change what the question tests, and do not say directly that the search result is missing." No rule of decision 0030 covers it. How does the build prevent this defect?

## Options

1. An instruction to the writer only.
2. An instruction to the writer, and a code rule A12 with a word limit for each sentence.
3. An instruction to the writer, and a new rule B7 that call 4b checks.

## Decision

Option 3.

1. **The instruction to the writer** (step 2, and so also step 5): "Use one name for one actor. Write each sentence so that a reader understands it at the first reading."
2. **Rule B7** in group B of decision 0030, checked by call 4b of decision 0032: "Each actor has one name in the question, the options and the reasons. A reader understands each sentence at the first reading." A result `fail` or `cannot_decide` works as for the rules B1 to B6.
3. The form of call 4b (`docs/diagrams/06-forms-draft.json`) gets the value "B7" in the list of rules.

So the list of rules has 18 rules: A1 to A11 and B1 to B7. This adds to decisions 0030 and 0032. It does not change their text (rule 26).

## Reason

- **Not an instruction only.** The guide says, in the context of an agent workflow: "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" (1.4-K2). The owner asked: "but is that enough? Only in the prompt?" An instruction alone fails sometimes, so a check comes after it.
- **Not a code rule for the length of a sentence.** A script measured the sentences. In the 12 sample questions of the guide, the longest sentence of a question has up to 42 words. In the test, T-M1-S05 (marked bad) has a longest sentence of 27 words, and T-M1-S07 and T-M1-S16 (marked good) have 38 and 34. So a limit from the sample questions does not catch T-M1-S05. A limit of 25 words fails 6 of the 9 questions that the owner marked good and 5 of the 12 sample questions. The defect is clarity, not length, and clarity needs judgment.
- **A model rule.** Plain reason: a check that needs judgment is a rule of group B (decision 0011 and 0012). The owner marks all 60 questions of mock 1, so the marks of the owner check the rule B7 itself.

Not decided yet:

- How often B7 gives a false fail in mock 1.

The check of B7 (7 October 2026, `runs/test-0024/part-b7.json`): call 4b with B7 failed T-M1-S05 on B7. It also failed 3 of the 9 questions that the owner marked good, each with a true finding: two names for one actor. The owner said that cost is not a concern and asked what is best. Agreed: B7 stays strict for mock 1, and the report of mock 1 shows how often it fails.

## How we decided

The assistant first recommended an instruction only. The owner asked if that is enough. The assistant said no, with point 1.4-K2, and suggested a code rule for length and a model rule. A script then measured the sentences, and the result showed that length was not the cause. The assistant changed the recommendation to an instruction and rule B7. The owner said: "Yes, add both".

No independent reviewer checked this file.

## Exam guide points

1.4-K2
