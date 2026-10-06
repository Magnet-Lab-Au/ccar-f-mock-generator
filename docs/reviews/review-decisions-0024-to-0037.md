# Review of decisions 0024 and 0027 to 0037, after the changes of decision 0037

- Date: 6 October 2026, third session
- Reviewers: two independent agents. They did not write the files. They worked at the same time and did not see the report of the other.
- Reviewer A: decisions 0024, 0027 and 0029 to 0037 against the exam guide records.
- Reviewer B: the same files against each other, against decisions 0001 to 0026 and against the 14 serious items of the earlier review (`review-decisions-0026-to-0036.md`).

The assistant wrote this file from the two reports. The text of the findings is shortened. No finding is left out.

## The result in short

- Each of the 26 quotes with a point ID is exact. Each point ID exists. Each list "Exam guide points" agrees with its Reason.
- The 4 earlier errors on the lists are fixed. Of the earlier findings F1 to F10, 9 are fixed and F10 is fixed in part.
- Of the 14 serious items: 8 are closed and 6 are closed in part.
- Reviewer A found 3 new errors. Reviewer B found 10 new serious items. Most of them are cases that the new rules made.
- The design is not complete.

## Reviewer A: the decisions against the exam guide

### Checked and true

- 26 quotes with a point ID are exact. The 6 quotes of Sections 3, 4 and 5 (in 0027, 0030 and 0036) are not in the records file. The reviewer found them exact in the exam guide document.
- 30 task statements, divided 7, 5, 6, 6 and 6 by domain. 240 points, 6 to 10 for each task statement. 12 sample questions, each with 4 options and 1 answer. The correct answer is A 10 times and B 2 times. 14 technologies and 3 lists in Section 17.
- The weights give 16.2, 10.8, 12, 12 and 9. The example of 0027 is correct: 7 task statements with 2 questions, and 2 more, give 16.
- 0031: questions 33 to 91 words, options 7 to 35 words, largest ratio 1.21. All 12 pass the limits of A6 and A7.
- 0032: 5255 words of guide text. 0034: 15 questions are about 1870 words.
- Both scripts of 0037 run. 11 of 15 sets have a table, 9 sets have a 12, and rules A8 to A11 are true for 12 of 12.
- The reviewer checked more than the script: each fitting table of those 9 sets has the 12. So the cause is the limit, as 0027 says.
- Of 39 uses of a point in a Reason: 7 agree, 21 agree in part with the context stated, 11 agree in part with the context not stated or with a claim that is too strong, none does not agree.

### Errors (3)

1. **0037, Reason, item 8.** The file says that the guide says "that code must enforce a rule that must always hold (1.4-K2)". The point says only that prompt instructions alone have a non-zero failure rate. Enforcement by code is in 1.4-K1 and 1.4-S1.
2. **0031, table, rule A10.** "Each of the 48 options is one sentence." The script tests only that an option has no sentence break inside. 12 options (sample questions 4, 6 and 10) have no end mark. The 4 options of sample question 4 are phrases, not sentences.
3. **0031.** "Rules A8 to A11 have no margin." The limit of A11 is weaker than the measured property. The script finds no "not" or "except" in the complete question text, in capital or small letters. The limit of 0031 permits "not" in small letters outside the last sentence. It is also different from A11 in 0030 and 0037.

### Uses of a point with the context not stated, or with a claim that is too strong (11 uses)

- **0030, 1.4-K2.** The point is on the order of workflow steps. The file uses it for a text search by code. Call 4b still lists the names by prompt, so a name that it misses passes.
- **0032, 1.4-K2.** The context is not stated in this file. Decisions 0029, 0030 and 0037 state it.
- **0029, 4.3-S3.** "So the API forces the form." The point forces a tool so that one extraction runs before others. Point 4.3-K2 is nearer.
- **0029, 4.3-S4, and 0033, 4.4-K2.** The context is visible only inside the quote. Point 4.4-K2 supports `cannot_write`, not the limit of 3.
- **0029, 4.2-K1 and 4.2-S2.** The points are on the output format. The prepared examples have no reason for each option, so they do not show the form that the writer must fill.
- **0033, 4.3-K1.** "Each try must have the same form." The point does not say this. The sentence is a plain reason with an ID.
- **0035, 5.5-K2 and 5.5-S1.** The points sample "high-confidence extractions". The design has no confidence number, and the owner reads all 60 questions of mock 1. The file does not say this.

### Other findings (4)

- **The script `0037-check-sample-properties.py`.** It does not divide a sentence that ends with a dot and then a quote mark. Sample question 7 has 4 sentences, and the script counts 3. This is important for "the last sentence" in A11.
- **The same script, A11.** It tests the question text only. Option C of sample question 7 has "not".
- **0024 and 0037, item 12.** "That explanation names letters." True for 11 of 12. The explanation of sample question 10 names no letter.
- **0027 and 0037.** "One scenario gets 12 of its 15 questions." In the sets 1, 2, 3, 6 and 1, 3, 4, 6, two scenarios get 12. The example of Domain 4 explains 8 of the 9 sets. In the set 1, 3, 5, 6 the cause is Domain 3.

### Statements about a product with no source and with no words "assumption" or "not checked" (7)

- 0029, "How we decided": "one call is one model run", and a separate call "gives a separate context with more control".
- 0029: "The Messages API is stateless and has no subagents." The source is "the Anthropic documentation", with no page.
- 0029, Decision, part 3: "the API forces the model to answer in that schema". The guide names "strict" schemas. The draft sets no strict option.
- 0029: "A model that must fill each blank invents a question."
- 0033 and 0037: "The same request with the same slot probably gets the same answer."
- 0034: "The length is not the problem", "The risk is the number of jobs in one call", and "A model finds a copy with different words".
- 0024: "If a prompt is wrong, all 60 have the same error."

### The earlier findings

- Errors 1 to 4 (the lists in 0030, 0031, 0033 and 0035): fixed.
- F1 to F9: fixed. F7 is fixed for the five uses that it named, and the same fault is new in 0032 (1.4-K2).
- F10: fixed in part. The limit is stated, but the writer still gets rule B2 with only its slice.
- Product statement 1 (the form and the counts): fixed. Statement 2 ("one model run", "more control"): not fixed. Statements 3, 4 and 5: fixed, each is marked as an assumption.

## Reviewer B: the design as a whole

### The 14 serious items

| Item | Status | What still disagrees or has no path |
|---|---|---|
| 1. The line "Select N." | Closed in part | Minor. 0037 says that step 6 sees the line. 0034 does not give the line to calls 6a and 6b. The "one function of code" is in no step file. |
| 2. The current try | Closed in part | **Serious.** A slot that step 6 or a bad mark sends back keeps the status `passed` until the new try exists. So the start condition of step 6 is true again immediately. |
| 3. Marking with no verdict in view | Closed in part | **Serious.** After run 3 of step 6 the owner selects `ignore` or `rewrite`. That is before step 7. 0035 says that the owner marks first. |
| 4. One form of a finding | Closed | Minor. 0034 does not name `other_questions`, and its verdict record has no list of findings. |
| 5. `cannot_write` | Closed | |
| 6. Two rules that stop a slot | Closed | |
| 7. The limits | Closed in part | **Serious.** No rule says if the count of 3 runs of step 6 starts again after a `rewrite` or a bad mark. |
| 8. Rule B6 | Closed | The list of words of rule A5 is still open (0031). |
| 9. Call 4a and the count | Closed | Minor. An answer `cannot_decide` has 0 letters. Read exactly, the count rule makes it an error. |
| 10. The report and the way back | Closed in part | **Serious.** The meaning of each value of `state` is not decided. `id` in `owner-decisions.json` has no definition, and a finding of step 6 has no ID. |
| 11. Letters | Closed | |
| 12. The sample questions | Closed in part | Minor. 0024 says that step 3 checks the 12 sample questions. They have no slot and no reason for each option, so A1 to A3 cannot run. |
| 13. The fingerprint | Closed | Minor. No rule for the sequence and the encoding of the fields. |
| 14. The method of step 1 | Closed | Minor. 0027, item 4, says "at random". The method says "equally". |

### Answers of 0037 that are missing or different in the step files (5)

- **Item 12, rule A11. Serious.** Three texts. See new gap (i).
- **Item 1.** Missing in 0034. The "one function" is in no step file.
- **Item 3.** "A `rewrite` names one question and has a reason" is in 0035 only. 0034 does not say it for the findings of run 3.
- **Item 4.** 0037 says that it changes 0034. 0034 has none of the six field names.
- **Item 13.** Minor. 0036 says that one field `fingerprint` is added to the record of step 6. 0034 names it `fingerprints`.

Items 2, 5 to 11 and 14 are in the step files with the same content.

### New contradictions (7)

1. **Serious.** Rule A11 has three texts.
2. **Serious.** 0034, run 3, against 0035 and 0015 (item 3 above).
3. **Serious.** 0034: a scenario passes step 6 when no rule has the result `fail`. After `ignore`, the record still has a `fail`. 0036 needs "passed steps 3, 4 and 6". So the mock can never be built.
4. Minor. Code builds the report from the records. After 3 failed calls no record is saved. So `errors` has no source after a new start.
5. Minor. 0034: "the question that was written last", then "if the dates are the same". The record has only `date`. If that is a day, the highest slot number is the usual rule.
6. Minor. One check file for each try (0031 and 0032). 0035: "all 60 questions go through the checks again". 0031: no file is written over.
7. Minor. The slot ID `M1-S17` (0029) against `M1-S04-T1` (0033). No rule for the zero.

### Old statements (6)

- 0029, part 2: "This closes one open item of decision 0027" and "a second open item". 0027 does not list them now.
- 0032, part 8: "This adds one part to decision 0024." 0024 has it now.
- 0033, item 7: "3 tries for one slot: the first question and 2 new tries." Item 8 makes this false after a send-back.
- 0033, the contract: it leaves out the text of the other questions.
- 0031, Question: "those rules: A1 to A7". It is history, but a programmer reads it first.
- The file name of 0030 says "the-13-rules".

### New gaps, from 10 cases that the reviewer followed through the files

- **(a) Fail on try 1, "cannot decide" on tries 2 and 3.** Has a path. The slot is `open` with both causes.
- **(b) `cannot_write` on a new try after step 6. Serious.** The slot becomes `open`. After `more_tries` or `new_point`, no file says if the next call is a request of step 2 or of step 5, or which failed try it shows.
- **(c) `new_point`. Serious.** No place stores the new point. `owner-decisions.json` has only `id`, `action`, `reason` and `date`. No file says if `plan.json` changes. If it changes, "the same seed gives the same plan" is false. No rule keeps the new point different from the points of the other slots. The question record has no field `point`.
- **(d) Run 3 of step 6 has a finding, and the owner selects `ignore`. Serious.** The scenario does not pass. See contradiction 3.
- **(e) A new question after a bad mark clashes with a question that the owner marked good.** The new question goes back. No path if the scenario already had its 3 runs. Also, a question from a `rewrite` gets no new marking file, so "mock 1: all 60" can fail.
- **(f) A call fails 3 times. Serious.** The slot stays `to_write` or `to_check`. The `state` of the mock is not defined. A new start has no rule for that call.
- **(g) A feature name with a different spelling.** No rule for a part of a word against a complete word, for `--`, for a plural, or for the 5 texts with a backslash. The search covers the complete file, with the list "out of scope" of Section 17 and the explanations of the sample questions. A feature on that list counts as named.
- **(h) A multiple-response question.** Rule A7 and the count of call 4a work. The writer gets no example with 5 options and 2 correct answers. The test of call 4a covers questions with one answer only. No rule for the letter E from call 4a on 4 options. A finding of call 4b has one `letter`.
- **(i) Rule A11. Serious.** 0037 and 0030: no "NOT" and no "EXCEPT". 0031: capital letters in the text, and "not" or "except" in the last sentence. The script: capital or small letters, in the complete question text. No file says if the options count.
- **(j) Step 8 for a later mock. Serious.** "Each question that the owner marked has the mark good" is true with no marks. No condition says that a marking round was accepted, that each "cannot decide" result of step 6 has a decision, or that the stop number was not reached.

### Checked and consistent

- The JSON forms in 0029, 0032 and 0034 are valid and agree with their text. The forms of 0032 are the same as `06-forms-draft.json`.
- 60 slots, 16, 11, 12, 12 and 9, 15 for each scenario, 52 and 8, 4 or 5 options.
- 188 model calls for one mock with no failure. No file states the total.
- The statuses, the values of `state`, `open_reasons`, the actions of the owner and "3 runs of a call that fails" are the same in each file.
- Rules A1 to A11 and B1 to B6 have the same numbers in 0030, 0031 and 0032.
- The slot number is the question number in 0027 and 0036.

## Not checked by the reviewers

- Any statement about a product against the Anthropic documentation. The forms against the API.
- The diagrams, `08-form-draft.json`, `HANDOFF.md`, `README.md`, `docs/journal.md` and `src/`.
- The scripts `0027-check-scenario-sets.py` and `0031-check-sample-lengths.py`. The reviewers did not get them. Reviewer A calculated their numbers again.
- The records file against the original guide.
- The sections "How we decided", except for statements about a product.
- If the design is good.
