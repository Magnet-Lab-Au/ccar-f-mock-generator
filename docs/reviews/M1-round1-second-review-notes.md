# Mock 1, round 1: notes of the second review

- Date: 8 October 2026
- Who: an assistant in a Cowork session. It is a Claude model, as the writer and the checkers are. It is not a person.
- File with the marks: `M1-round1.xlsx`. The owner asked for the same file name, so it replaces the marking file. It is the file of the owner with 7 marks changed from `good` to `bad`, each with a reason. The first state of the file had 60 marks `good`.

## How the review was made

1. The owner marked all 60 questions first, with no verdict in view. Result: 60 `good`.
2. The assistant read the 60 questions with the answer key and the reasons, but with the two columns of the owner hidden.
3. The assistant saved its marks. Only then it opened the columns of the owner.
4. The owner then asked the assistant to write its findings into the Excel file as bad marks.

So the 7 bad marks in the file are not blind marks of the owner. They come from a second review, after the blind marking. Record them in that way.

## The result

By the four checks of the marking, all 60 questions are good: no wrong answer key, no second correct option, no question that misses its point, no false reason. A script checked rules A4 to A11 on all 60, with no failure.

The problems are in the mock as a set.

## The 7 questions with a bad mark

| Question | Cause |
|---|---|
| M1-S09 | Repeat of M1-S07 in the same scenario |
| M1-S24 | Repeat of M1-S10 in a different scenario |
| M1-S28 | Repeat of M1-S21 in the same scenario |
| M1-S30 | Close copy of sample question 1 of the exam guide |
| M1-S47 | "Select 2.", but the two correct options are one action |
| M1-S49 | Ruling 2: a second and a third wrong option on the confidence of the model in scenario 5 |
| M1-S60 | Repeat of M1-S48 in the same scenario |

The full reason of each one is in the Excel file. Each reason describes the other question, because the writer of step 5 does not see it.

7 bad marks are more than the stop number of decision 0035 (more than 6 of 60). The owner decides if these 7 count as bad marks or as `rewrite` actions, which do not count (decision 0037, item 3).

## Findings that have no bad mark

### Groups of questions on one idea

| Idea | Questions |
|---|---|
| A prompt rule fails in a few percent of the runs, and code must enforce it. Wrong options: a stronger prompt, few-shot examples. | S13, S14, S18, S30 |
| A fixed sequence against a plan that adapts | S08, S21, S25, S28 |
| Review in the session that wrote the code against an independent instance | S31, S48, S60 |
| Few-shot examples when detailed rules give inconsistent output | S47, S57 |
| Continue a named session with `--resume` | S10, S24 |
| A keyword in the system prompt overrides the tool descriptions | S07, S09 |
| A semantic error against a schema error, and a retry with the exact error | S53, S54 |
| The error category and the retry of `process_refund` outside the return policy | S20, S22 |
| Plan mode before a change in many files | S34, S38 |
| Conventions for one directory | S33, S40 |

- M1-S13 is the same sample question as M1-S30, moved to scenario 3. It has no bad mark, but it is in the first group.
- M1-S33 and M1-S40 have the same problem and two different correct answers: a rules file with a path, and a `CLAUDE.md` in the directory. Each question does not offer the mechanism of the other.

### The longest option is often correct

In the 52 questions with one answer, the correct option is the longest by characters in 31. Chance is 13. Each question passes rule A7 (largest ratio 1.27), so that rule does not catch the pattern. A participant who always selects the longest option gets about 60%.

### Weak wrong options

In S03, S12, S17, S26, S27, S35, S37 and S50, the wrong options are plainly bad or are the opposite of the guide.

In S08, three wrong options start with "Keep the fixed sequence". The form points at the answer.

### "Select 2." questions

In S17, S35 and S47, the two correct options are two examples of one idea. Only S58 has two different needs with two different answers. A point of the guide that holds one idea does not give two different correct options.

### Weak fit with the story

S10 and S24 (a Claude Code session in the research scenario and in the support scenario), S27 (test files in the support scenario), S39 and S44 (document analysis and confidence scores in the code generation scenario).

### Numbers

- Letters of the correct option, questions with one answer: A 11, B 15, C 8, D 18. That is not far from chance for 52 questions.
- Tries: 49 questions are try 1, 10 are try 2, and S47 is try 4.

## The probable causes, for the pipeline

1. **Twin points.** The guide has pairs of points on one idea, often one "knowledge" point and one "skill" point of the same task statement. Examples: 1.7-K1 and 1.7-S1, 2.1-K4 and 2.1-S4, 4.6-K1 and 4.6-S1, 4.2-K1 and 4.2-S1. The plan selects points at random, so it selects twins. The writer of one slot does not see the other slot.
2. **Scenario 5 has 12 of its 15 questions from Domain 4.** Four of the 10 groups are there. This is the effect of the scenario limit of decision 0027.
3. **Step 6 compares questions inside one scenario only.** The pair S10 and S24 is in two scenarios.
4. **The writer got sample question 1 as an example and copied its structure** (S13 and S30).
5. **No rule looks at the set of 60 for the longest option.**

These causes are the opinion of the assistant. It did not see the plan, the code or the records of step 6.

## Not checked

- The plan file, the records of step 6, and the report of the run.
- If the program accepts a marking file with a different name, or a reason of this length.
- The 60 questions against the original exam guide. The assistant used `reference/guide-records.json`.
