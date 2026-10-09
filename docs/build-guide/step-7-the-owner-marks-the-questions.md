# Step 7: the owner marks the questions

Status: built. It ran in the test before the first full run, on 7 October 2026.

Diagram: [`09-step-7-the-owner-marks-the-questions.html`](../diagrams/09-step-7-the-owner-marks-the-questions.html)

## What the step does

Each check before this step is code or a model. This step shows if those checks are right: a person reads the questions and marks them.

The owner read and marked the questions of mocks 1 to 3. For mocks 4 and 5, no person reads the questions: the second review, also a Claude model, marks them (decision 0071). So in mocks 4 and 5, every check is a model or code.

Code builds one Excel file for each round of marking. It has one row for each question: the question, the point that it must test, the options, the correct answer and the reasons. It shows no verdict of a checker. The owner fills two columns: "good" or "bad", and a reason for a bad mark. The sheet is protected, so that only those two columns can change and a mark cannot move to a different question. (Not checked in real Excel yet.)

For mock 1 the owner marks all 60 questions. For mocks 2 to 4 the file has a random sample of 20, 5 from each scenario. For mock 5 the file has all 60 questions again (decision 0073). The owner marked mocks 1 to 3. For mocks 4 and 5 the second review in Cowork, a Claude model, marks the questions, and no person reads them (decision 0071). A bad mark sends the question to step 5, with the reason as the finding. Too many bad marks stop the mock: more than 6 of 60 for mocks 1 and 5, and 2 or more of 20 for mocks 2 to 4.

Code saves the marks, and shows the bad marks for each scenario and each domain.

## The test run

Code built a marking file for the 10 questions of the test. The owner marked 9 good and 1 bad. The bad mark had a reason, and that reason led to a new rule of step 4.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 5.5-K2 | "Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns" | Task statement 5.5: Design human review workflows and confidence calibration | Written for the extraction of data, where a person samples results that the system is sure of. Here: a person marks questions that passed all checks. For mock 1 the owner reads all 60, so that is not a sample. |
| 5.5-S1 | "Implementing stratified random sampling of high-confidence extractions for ongoing error rate measurement and novel pattern detection" | Task statement 5.5: Design human review workflows and confidence calibration | The same context. Here: the sample of a later mock has questions from each scenario and each domain. |
| 5.5-K1 | "The risk that aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields" | Task statement 5.5: Design human review workflows and confidence calibration | Written for the extraction of data. Here: the bad marks are shown for each scenario and each domain, because one total can hide a bad part. |
| 5.5-S2 | "Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review" | Task statement 5.5: Design human review workflows and confidence calibration | The same context. Here: a sample below 20 questions comes only after the results are good in each scenario and each domain. |
