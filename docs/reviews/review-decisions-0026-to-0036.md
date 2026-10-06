# Review of decisions 0026 to 0036, diagrams 02 to 10 and `HANDOFF.md`

- Date: 6 October 2026
- Reviewers: two independent agents. They did not write the files. They worked at the same time and did not see the report of the other.
- Reviewer A: decisions 0026 to 0036 against the exam guide.
- Reviewer B: decisions 0026 to 0036 against each other, against decisions 0003 to 0025, against the diagrams and against `HANDOFF.md`.

The assistant wrote this file from the two reports. The text of the findings is shortened. No finding is left out.

## The result in short

- Each quoted exam guide text is exact. Each point ID exists. Each number about the guide that reviewer A checked is true.
- Reviewer A: 4 errors and 10 findings to consider. Of 47 uses of the guide: 17 agree, 17 agree in part with the context stated, 12 agree in part with the context not stated or with a claim that is too strong, 1 does not agree.
- Reviewer B: 10 contradictions, 13 gaps, 10 diagram errors, 5 handoff errors.
- The most important result: `HANDOFF.md` says that the design of all 9 steps is complete. Reviewer B says that this is too strong. A programmer who has only the decision files meets cases with no path.

## Reviewer A: the decisions against the exam guide

### Checked and true

- 19 quotes with a point ID are exact. 8 quotes of Sections 3, 4 and 5 are exact.
- The weights give 16, 11, 12, 12 and 9. Exactly 11 of 15 sets of scenarios fit. The 4 sets that decision 0027 names do not fit: 48 of 60 questions.
- 30 task statements, 240 points, 6 to 10 points for each task statement, 12 sample questions, 14 technologies.
- All 12 sample questions have 4 options and 1 correct answer. The correct answer is A 10 times and B 2 times.
- Decision 0031: questions 33 to 91 words, options 7 to 35 words, largest ratio 1.21. All 12 sample questions pass the limits.
- Decision 0034: 15 questions are about 1900 words. Decision 0032: 5255 words of guide text.
- The three JSON drafts in decisions 0029, 0032 and 0034 are the same as the files in `docs/diagrams/`.

### Errors (4)

The list "Exam guide points" does not agree with the Reason.

| File | The list says | The Reason also uses |
|---|---|---|
| 0030 | 4.1-K1 | 4.3-K3 |
| 0031 | none | 5.3-K4 |
| 0033 | 4.4-K1, 4.4-S1, 4.4-K2, 1.1-S3 | 4.3-K1 |
| 0035 | 5.5-K1 | 5.5-K2 and 5.5-S1 |

In each case the missing ID is used through an earlier decision. Decisions 0032 and 0034 list such IDs. So the files do not apply one rule.

### Findings to consider (10)

- **F1. 0029 and 0030, point 4.3-K3.** The files say that the form cannot check the number of options. The point says only that a schema does not prevent semantic errors. It says nothing on the number of items in a list. This is also a statement about a product with no source.
- **F2. 0032, point 4.6-S3.** The point teaches a check where the model reports confidence with each finding. The decision is "no confidence number". The file does not say that the design does the opposite of the point.
- **F3. 0034, point 4.6-K3.** The point divides a large review by scope. The file uses "attention dilution" for the number of jobs in one call. The guide does not say that.
- **F4. 0032, point 4.6-K2.** The file quotes "without prior reasoning context", but call 4b gets the reason of each option from the writer. The reason for the blind answer ("a checker that sees the marks tends to agree") applies to call 4b too.
- **F5. 0029, point 1.4-K2.** It supports "code controls the sequence". It does not support "not the Agent SDK". Point 1.4-K1 names hooks as enforcement by code. The context is not stated.
- **F6. 0032, point 4.1-K1.** The point is on exact criteria in a prompt, not on one result for each criterion.
- **F7. The context is not stated**, the same kind of error as in decision 0019: 5.3-K4 in 0031 and 0034, 5.5-K2 and 5.5-S1 in 0035, 4.3-S5 in 0032, 4.1-K1 in 0034.
- **F8. 0029, possible points for "the plain API, not the SDK".** Points 1.6-K1, 1.6-S1 and 1.1-K3 say what the reason says. Also: "Decision 0012 has the reason" is true only for the section "How we decided" of 0012, not for its Reason.
- **F9. 0029, the number of 3 examples has no reason.** Point 4.2-S1 says "2-4 targeted few-shot examples". Also: the status `cannot_write` is nearer to point 4.3-S5 than to 4.3-S4.
- **F10. 0029 against 0032.** 0029 says that the writer needs its one task statement "and no more". 0032 says that a wrong option often comes from a different task statement and that a slice is not sufficient. The writer gets rule B2 with only the slice.

Two small notes: 0032 says "labels from a person", and point 5.5-K3 says only "labeled validation sets". The guide says that each item states how many responses to select, and the design adds the line only to multiple-response questions.

### Statements about products with no source

- 0029: the form cannot check the number of options.
- 0029: "one call is one model run", and a separate call "gives a separate context with more control".
- 0029: a model that sees the examples copies the letter A.
- 0032: a checker that sees the marks tends to agree with them.
- 0032: a checker that sees the earlier findings looks only for those findings.

## Reviewer B: the design as a whole

### Contradictions (10)

1. **Serious. The line "Select N."** Decision 0003 says that each question says how many answers to select. Decisions 0030 and 0036 add the line only to a multiple-response question. Decision 0030 treats the line as a part of the question, and decision 0036 lists it as work of step 8. So it is not clear if steps 3, 4, 6 and 7 see the line, or if rule A6 counts it.
2. **Serious. "Exactly one question that passed."** After a new try from step 6 or step 7, the older try also passed steps 3 and 4. No file defines the current try of a slot, or a status of a slot.
3. **Serious. Marking with no verdict in view.** The marking file shows no verdict. But the owner sees the "cannot decide" results of step 6 in step 7. It is not stated if that is before or after the marking, and the owner has no defined action.
4. **Serious. Three forms of a finding.** 0033: step, rule, detail. 0032: rule, result, finding, point. 0034: question IDs and detail. Step 7 has no rule. And 0034 adds a third part to the request of step 5, the text of the other question, which 0033 does not have.
5. Minor. 0032 says that a finding names its guide point. The form says that `point` can be null.
6. Minor. 0014: a question that step 6 names goes back. 0034: only the question with the highest slot number. 0020: step 6 checks the complete mock again. 0034: that scenario again. The changes are not stated.
7. Minor. 0012: the checker does not get the reasoning of the writer. 0032 gives call 4b the reasons of the options. It is a change, and the file calls it an addition.
8. Minor. 0015: "good or bad, with one reason", and code compares the marks with the verdicts. 0035: only a bad mark has a reason, and code only shows the bad marks.
9. Minor. 0011 names "agrees with its slot: the scenario, the task statement" as a code rule. In 0030 only the counts are code rules.
10. Minor. Old statements in the new files: 0027 still lists the form of multiple-response and the plan file format as not decided, and its slot has no `options` field. 0029 says that the rules are written in the design of step 4. 0033 lists the form of a finding from step 6 as open.

### Gaps (13)

Listed by the files as not decided, but they block the build:

1. **Serious. `cannot_write`.** The slot stays empty, so step 6 can never start. It is not stated if a record file is saved.
2. **Serious. Two rules that stop a slot.** "Cannot decide" two times, and 3 tries. After the second "cannot decide" on try 2, both apply.
3. **Serious. The limit of tries against new tries from steps 6 and 7.** Step 6 has run numbers but no limit, so the loop can run with no end. A new try from step 7 can make step 6 send back a different question that the owner marked good.
4. **Serious. Rule B6** has no definition of "feature" and "named". Also open: the words of rule A5, the request texts, the models.

Not noticed by the files:

5. **Serious. Call 4a does not know how many answers to select.** On a multiple-response question, a different count makes rule B1 fail with no real cause.
6. **Serious. The report and the paths to the owner.** `report.json` has no format. Four different things go into it. "The slot goes to the owner" has no file. No file gives a way back from the owner into the pipeline, or a new try for an API call that failed.
7. **Serious. Letters in a new try.** Findings name letters. The writer returns options with no letters, and code mixes them again. No file says how the letters of a finding map to the new options.
8. **Serious. The sample questions do not have the form of a question record.** They have one explanation that names letters, no point and no reason for each option. So the test of decision 0024 cannot run through rules A1 and A5 or through call 4b as designed. And the 3 examples for the writer break rule A5 and show the correct answer at A or B.
9. **Serious. The fingerprint.** No method, and no list of the fields that it covers. A record of step 6 covers 15 questions, so one field is not sufficient.
10. **Serious. Step 1 has no method.** How the domain counts are shared among the 4 scenarios, how task statements go to scenarios, the sequence of the slot numbers, and the top fields of `plan.json`.
11. Minor. Step 6: the record has no table of fields and no verdict field. "Passed step 6" is not defined when a result is "cannot decide". The guide text for calls 6a and 6b is not given. No path when rules C1 to C3 fail.
12. Minor. Step 7: if bad marks of round 2 count for the stop, and how `marks.json` holds more than one round.
13. Minor. What code does with a point ID that does not exist, with the letter E on 4 options, or with a missing rule result. The unit of rule A7. The 120 minutes are in no output file.

Rule A7 is defined for 2 correct options.

### Diagram errors (10)

1. **Serious. Diagram 10, popup of the records:** it says that each record has the results of its checks. The decisions save verdicts and marks as separate files.
2. **Serious. Diagram 02.** "Not decided yet" shows two items that decision 0029 closed. One popup says "selects 2 or more answers", and 0029 says exactly 2. The slot has no `options`.
3. **Serious. Diagram 07.** One popup says that the design of step 6 is not complete. The picture always shows 3 tries and leaves out the stop after two "cannot decide". One popup says that a slot with a passed question is full, but steps 6 and 7 can still send it back.
4. **Serious. Diagram 06.** The popup of rule B4 says: "The plan gives each point of the guide its share of questions." That is false: 60 slots, 240 points, selected at random. The diagram leaves out that call 4b always runs, and the error path.
5. Minor. Diagram 04: a popup says that the list of rules is not written yet. The page says "A to D", and a multiple-response question has A to E.
6. Minor. Diagram 03: "about 200 words" for the slice. The writer call also gets the examples, the rules and the technologies.
7. Minor. Diagram 05: the popup of rule A7 says "the correct option", and 0031 uses the average of the correct options. "No text is empty" is in no decision.
8. Minor. Diagram 09: the sheet shows slot IDs, and 0035 says question ID. It leaves out the results of step 6 and the folder `marking/`. One sentence on mock 1 can mislead.
9. Minor. Diagram 08: it leaves out the verdict record and the error path.
10. Minor. Diagram 10: it leaves out the head of the questions file, and the marks of step 7.

### Handoff errors (5)

1. **Serious.** "The design of all 9 steps is complete", and "Designed" for each step. Gaps 1 to 10 leave cases with no path.
2. **Serious.** "Things that are open" leaves out items that the decisions list as not decided.
3. Minor. It reports old content only for diagram 01. Diagrams 02, 04 and 07 also have old statements.
4. Minor. The next step reviews 0026 to 0036 only. Decisions 0019 to 0025 have no review.
5. Minor. "The owner confirmed the text of 0001 to 0018." Files 0001 and 0002 do not have the line "Text confirmed by the owner".

### Checked and consistent

- The three JSON forms are valid and agree with their descriptions.
- The numbers of the design: 60, 15 for each scenario, 52 and 8, 4 or 5 options, 8 calls in step 6, the sample of 20, and 188 calls for one mock with no failure.
- The ID formats and the paths are the same in 0029, 0031, 0032 and 0033.
- The verdict values. Code gives the letters in step 2, and each later step uses them.

## Not checked by the reviewers

- Any statement about a product against the Anthropic documentation.
- `README.md`, `WORKING-RULES.md`, `docs/journal.md`, `src/`, the workbook, diagram 01, the diagram scripts and the two check scripts. The reviewers did not get these files.
- The diagrams in a browser. Reviewer B read only their text.
- `reference/exam-guide.md` against the original guide.
- The sections "How we decided".
- If the design is good.
