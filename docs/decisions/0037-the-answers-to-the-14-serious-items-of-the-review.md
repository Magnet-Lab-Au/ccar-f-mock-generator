# 0037: The answers to the 14 serious items of the review

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: none. The diagrams of the steps change together with the step files.

## Question

Two independent reviewers found 14 serious items in decisions 0026 to 0036 (`docs/reviews/review-decisions-0026-to-0036.md`). What is the answer to each item?

## Options

1. One new decision file with the 14 answers. It names each decision that it changes.
2. Change decisions 0027 to 0036 directly, with no new file.

## Decision

Option 1. Where this file and an older file disagree, this file is correct. The step files 0027 to 0036 are changed after this file, so that each one is complete again.

1. **The line "Select N."** Each of the 60 questions has the line: "Select 1." or "Select 2." It is the field `select` of the question record. It is not a part of the question text. Code copies it from the slot. One function of code shows a question to a model or to the owner: the question, the line, the options with their letters. Steps 4, 6 and 7 see the line. Rule A6 counts the question text only. Changes 0030 and 0036.
2. **The current try.** The current try of a slot is the try with the highest number. Older tries are history. Code calculates the status of a slot from the records: `to_write`, `to_check`, `passed` or `open`. No file stores the status. Rule C1 becomes: the current try of each of the 60 slots has the status `passed`. Changes 0034.
3. **"Cannot decide" in step 6.** The owner marks first, with no verdict in view. After code accepts the marking file, code shows these results. For each result the owner selects `ignore` or `rewrite`. A `rewrite` names one question and has a reason. It does not count as a bad mark. Changes 0034 and 0035.
4. **One form of a finding.** Code converts each finding into these fields: `step`, `rule`, `detail`, `letter`, `point`, `other_questions`. The rule of a bad mark is `owner`. `letter` and `point` can be empty. Only step 6 fills `other_questions`. Code adds the text of each question in `other_questions` to the request of step 5. Changes 0031, 0032, 0033 and 0034.
5. **`cannot_write`.** Code saves the answer as a record with its try number and its reason. The slot gets the status `open` immediately, with no new try. The other slots continue. Changes 0029 and 0033.
6. **Two rules that stop a slot.** Both stay: 3 tries with no pass, and "cannot decide" two times. The rule that applies first stops the slot. The two "cannot decide" results do not have to come one after the other. The field `open_reasons` names each cause: `three_tries`, `cannot_decide_twice` or `cannot_write`.
7. **Limits.** Each time step 6, step 7 or the owner sends a slot back, the slot gets 3 new tries, and the count of "cannot decide" starts at zero. The try numbers continue. Step 6 runs at most 3 times for one scenario. Then the mock waits for the owner, with the actions `ignore` and `rewrite`. When a finding names two questions or more, the question that was written last goes back. If the dates are the same, the highest slot number goes back. Changes 0033 and 0034.
8. **Rule B6.** A feature is a thing of a Claude product or of MCP that has a name: a tool, a command, a flag, a parameter, a field, a file or a setting. A name that the question invents for its story is not a feature. General technology, for example Python, is not a feature. Call 4b gets one new field, `features`: each feature name that the question, the options and the reasons use. Code searches each name in `reference/guide-records.json`. Code ignores capital letters, and treats a hyphen, an underscore and a space as the same. A name that is not found makes B6 fail, and the finding gives the name. Changes 0030 and 0032.
9. **Call 4a.** Code counts the selected letters before it compares them. A count that is not the number of the line is an error of the call. It is not a finding. Code runs the call again (item 10). Changes 0032.
10. **The report, a call that fails, the way back.**
    - Code builds `runs/mock-01/report.json` from the records at the end of each run. Fields: `mock`, `date`, `state`, `slots`, `step6_cannot_decide`, `errors`. Each slot has `slot_id`, `status`, the current question ID, the number of tries and `open_reasons`.
    - `state` is `in_work`, `waits_for_owner`, `ready_to_mark`, `stopped` or `built`.
    - Code runs a call that fails again, at most 3 times. These are not tries of the slot. Then the call goes into `errors`, and the other slots continue. A new start of the program continues from the records.
    - The owner answers with one command. Code saves the decision in `runs/mock-01/owner-decisions.json`: `id`, `action`, `reason`, `date`. The actions for an open slot are `new_point`, `more_tries` and `new_plan`. The actions `ignore` and `rewrite` go into the same file.
11. **Letters.** The question record keeps the letters that code gave. Step 5 shows the failed question with them. Code gives new letters to the new try. Changes 0029 and 0033.
12. **The sample questions.**
    - The 12 sample questions test call 4a and step 3 only. Call 4b is tested with the 10 questions of the writer that the owner marks, and with damaged copies of them. Changes 0024 and 0032.
    - For a writer example, code keeps the question and the 4 options, mixes the options, removes the letters, marks the correct option and leaves out the explanation. Changes 0029.
    - Four new code rules. A8: the text ends with a question mark. A9: the text has 2 to 5 sentences. A10: each option is one sentence. A11: the question has no "NOT" and no "EXCEPT". Changes 0030 and 0031.
    - One instruction for the writer, with no check: the options of a question have the same form.
13. **The fingerprint.** SHA-256 of the question ID, the question, `select`, and each option with its letter, its mark and its reason. A record of step 6 has one fingerprint for each of its 15 questions. The marks record has one for each mark. Changes 0036.
14. **The method of step 1.**
    - The seed selects one of the 11 sets and the sequence of the 4 groups.
    - Code makes the table of scenarios and domains: 15 questions for each scenario, at least 1 for each primary domain. Code takes the most even table. The seed decides when two tables are equal.
    - In each domain, the task statements share the questions equally. The seed decides which ones get the questions that are left, and which scenario each one goes to.
    - The seed selects one point for each slot. Two slots of one mock do not get the same point.
    - The seed selects 2 multiple-response slots in each scenario.
    - The slots get the numbers 1 to 60, group by group. The slot number is the question number in the finished mock.
    - The top fields of the plan file: `mock`, `seed`, `guide_version`, `date`, `scenarios`, `table`.
    - Changes 0027 and 0036.

## Reason

Most reasons are plain.

- **Items 1 and 9.** Decision 0003 says that each question states how many answers to select. It uses Section 3 of the guide.
- **Item 2.** One true copy, as in decision 0016. A stored status can disagree with the records.
- **Item 3.** A decision that the owner makes after a verdict is not a blind mark.
- **Items 4 and 11.** The writer of step 5 can correct only what it can see.
- **Item 5.** The same request with the same slot probably gets the same answer.
- **Items 6 and 7.** With no limit, a loop can run with no end. The newest question made the clash.
- **Item 8.** A false fail costs one new try. A false pass puts a bad question into a mock. So code decides "named". The guide says, in the context of agent workflows, that an instruction to a model can fail and that code must enforce a rule that must always hold (1.4-K2, in decision 0009).
- **Item 9.** A finding must say something about the question, not about the checker.
- **Item 12.** The explanations of the sample questions name letters. A script measured the 12 sample questions: each of the four properties of A8 to A11 is true for all 12.
- **Item 14.** A script checked that each of the 11 sets has a table. In 9 of the 11 sets, one scenario gets 12 of its 15 questions from one domain. The cause is the limit of decision 0027. The limit stays for mock 1.

Numbers that are guesses of the assistant, with no source: 3 runs of step 6, and 3 runs of a call that fails.

Not decided yet:

- An automatic path for `cannot_write`. The test of decision 0024 shows if it is necessary.
- The name of the command of the owner.
- How often the exact search of item 8 gives a false fail.
- The items that decisions 0027 to 0036 list as not decided, if this file does not close them.

## How we decided

The assistant showed one proposal with 14 answers. The owner asked to discuss them one at a time, and said yes to each one. The owner asked for a more simple explanation of items 8, 10, 12 and 14.

For item 8, the owner asked if code or a model must do the search, and how code knows that two names are related. The answer: code does not know. It only reports that a name is not in the guide. The writer finds the word of the guide.

For item 12, the owner asked how the properties of the sample questions stay in the new questions. That question gave rules A8 to A11.

The assistant said first that 6 of the 11 sets have a scenario with 12 questions from one domain. The correct number is 9.

No independent reviewer checked this file.

## Exam guide points

1.4-K2
