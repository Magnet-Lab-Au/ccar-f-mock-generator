# Step 8: build the files

Status: built. It ran for mock 1 on 8 October 2026.

Diagram: [`10-step-8-build-the-files.html`](../diagrams/10-step-8-build-the-files.html)

## What the step does

Code builds the two files of a mock from the stored question records. Nobody edits the files by hand. To change a question, the record changes, and code builds the files again.

The build starts only after the owner accepts the mock. Then code checks six conditions: each question passed steps 3 and 4 and did not change after its checks, step 6 checked the current questions of each scenario, each finding of step 6 has a decision, each question that needs a mark has one, the bad marks are below the stop limit, and no call failed in the last run. If one condition is false, code builds no file and lists the causes.

To know that a question did not change after its checks, each check saves a fingerprint of the question: a code of 64 characters that code calculates from the text. Before the build, code calculates the fingerprint again and compares.

The questions file has the 60 questions in 4 groups, one for each scenario. Each group starts with the story of its scenario. The file has no answers. The answers file has the correct letters and the reason of each option, for after the mock.

## The run of mock 1

The owner accepted mock 1 on 8 October 2026, with known limits. Code checked the six conditions and built the two files: `mocks/mock-01.questions.json`, with 60 questions in 4 groups (scenarios 3, 1, 2, 5) and 120 minutes, and `mocks/mock-01.answers.json`, with 60 answers. The build saved 60 fingerprints. Mock 1 cost $17.17 for 265 model calls.

## The exam guide texts that the step uses

The step uses no point of a task statement. It uses three facts of the exam form.

| Section | Text of the guide | How the step uses it |
|---|---|---|
| 3 | "each item states how many responses to select" | Each question has the field "select", so the portal can show the line "Select 1." or "Select 2." The format of the portal is not decided yet. |
| 5 | "Each scenario presents a realistic production context that frames a set of questions." | The questions are in groups by scenario, each with its story. |
| 3 | "percent-correct by domain on the score report" | Each question has its domain, so the portal can show a result for each domain. |
