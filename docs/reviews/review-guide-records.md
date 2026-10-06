# Review of `reference/guide-records.json`

- Date: 6 October 2026
- Reviewer: one independent agent. It did not make the file. It did not see the script of step 0 or the check script.
- Subject: `reference/guide-records.json`, compared with `reference/exam-guide.md`
- Decision: 0028 (check 3)

The assistant wrote this file from the report of the reviewer. The text of the findings is shortened. No finding is left out.

## Verdict

No errors found.

## The checks of the reviewer

The reviewer wrote its own script and compared the two files record by record and character by character, in both directions.

1. Structure: the top level has the 6 parts. No duplicate key.
2. `guide.version`: 1 of 1 agrees with line 7 of the guide.
3. Domains: 5 of 5 agree with the table of Section 4 (ID, name, weight). The weights add up to 100.
4. Scenarios: 6 of 6 agree (ID, name, story, primary domains). The sequence of the primary domains agrees with the guide. Scenario 4 is `[2, 3, 1]` in the guide.
5. Task statements: 30 of 30 agree (ID, domain, title).
6. Points: 240 of 240 agree in ID, kind and text.
7. The other direction: the 240 bullets of Section 6 of the guide are the 240 texts of the file, in the same sequence. Sections 5, 6 and 9 have no line that the script of the reviewer could not classify.
8. Page marks: the guide has 39, and 18 of them are in Section 6. No page mark is in a text. No bullet is lost, moved or numbered wrong. 12 marks are in the middle of a list, 3 are immediately before "Skills in:" (3.3, 4.2, 4.5), and 3 are immediately before a task statement heading (1.4, 1.6, 5.6).
9. Sample questions: 12 of 12 agree (number, scenario, question, options A to D, answer, explanation). Questions 1 to 3 are scenario 1, 4 to 6 are scenario 2, 7 to 9 are scenario 3, and 10 to 12 are scenario 5. The answer is B for questions 2 and 7, and A for the other 10. The reviewer read all 12 explanations. Each one argues for the letter in the file.
10. Section 17: 14 of 14 technologies, 18 of 18 topics in scope, 16 of 16 topics out of scope, with exact text and sequence.
11. Read by eye: task statements 1.2, 3.3 and 4.3, scenarios 2 and 4, sample questions 2, 6, 8 and 10, and all of Section 17. All agree.
12. 930 strings: no empty string, no space at the start or the end, no double space, no line break, no `**`, no duplicate ID. The fields `id`, `domain`, `weight`, `number` and `scenario` are integers where the specification says so.

## Observations (not errors)

A later step must know these.

1. **Markdown backslashes in 5 texts.** They are exact copies of the guide file. A step that shows the text to a person or to a model must decide what to do with them. The texts: `1.7-K1` (`\<session-name\>`), `2.5-S2` (`\*\*/\*.test.tsx`), `3.3-S1` (`["terraform/\*\*/\*"]`), `3.3-S2` (`\*\*/\*.test.tsx`), and the explanation of sample question 6 (`\*\*/\*.test.tsx`).
2. **Two characters outside ASCII.** The middle dot, 3 times in `guide.version`. The long dash, 27 times in 25 strings.
3. **Characters that a template or an HTML page must handle.** Option C of sample question 10 has `<`. Point `4.3-S3` has braces and double quotes. Many texts have double quotes.
4. **Options with no full stop.** The options of sample questions 4, 6 and 10 do not end with a full stop. The others do. The guide is the same.
5. **Lists of different length.** A task statement has 3 or 4 Knowledge points and 3 to 6 Skills points. A program must not assume one fixed number.
6. **Content of the guide, copied correctly.** The "Total" row of the domain table has a defect in the guide file, and it is not in the records. The explanation of sample question 11 quotes "often faster", which is in no option. The story of scenario 4 lists the built-in tools without Edit.
7. **The explanations name option letters.** An explanation says "Option B" or "Option C". If a later step changes the sequence of the options, these words become wrong.

## Not checked by the reviewer

- `reference/task-statements-and-points.md`.
- If `reference/exam-guide.md` is a correct copy of the original guide.
- If the content of the guide is technically correct.
- Sections 1 to 3, 7, 8, 10 to 16 and 18 of the guide. The records do not include them.
- The script of step 0.
