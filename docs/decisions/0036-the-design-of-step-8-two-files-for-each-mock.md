# 0036: The design of step 8: two files for each mock, built only from checked records

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Diagram: `docs/diagrams/10-step-8-build-the-files.html`

## Question

Decision 0016 says that code builds the mock file and the answer key from the stored question records, and that nobody edits an output file by hand. It left open the file format, and if a changed record must pass the checks again. What is the design of step 8?

## Options

1. One proposal of the assistant with the exact files and the checks before the build.
2. A different design.

## Decision

Option 1.

1. **When the step starts.** The current try of each of the 60 slots passed steps 3, 4 and 6, and each question that the owner marked has the mark good.
2. **Two files for each mock**, in a new folder `mocks/`:

| File | Content |
|---|---|
| `mocks/mock-01.questions.json` | The 60 questions with their options and letters. No answers and no reasons. |
| `mocks/mock-01.answers.json` | For each question: the correct letters, and the reason of each option |

3. **The questions file.** It has the mock number, the version of the guide, the seed, the date and the field `minutes` with the value 120. Then 4 groups, one for each scenario. Each group has the scenario, its name, its story and its 15 questions. Each question has its number (1 to 60), which is its slot number, its question ID, its domain, its task statement, its point, its type, the number of answers to select, the question and the options with their letters.
4. **The answers file.** It has the mock number, and one entry for each question: the number, the question ID, the correct letters, and for each option its letter, its mark and its reason.
5. **The sequence.** The questions are in groups by scenario. Each group starts with the story of its scenario. The plan of step 1 sets the sequence: the slot number is the question number (decisions 0027 and 0037, item 14).
6. **The line "Select N."** Each of the 60 questions has the field `select`, with the value 1 or 2. The portal shows it as the line "Select 1." or "Select 2." (decisions 0030 and 0037, item 1).
7. **The checks before the build.** Code checks that each slot has a question, that each question has its verdict records and the mark of the owner if the owner read it, and that no record changed after its check.
8. **The fingerprint.** Each check saves a fingerprint of the question record that it checked. A fingerprint is a code of 64 characters that code calculates from the text of the record. The method is SHA-256. Code calculates it from the question ID, the question, `select`, and each option with its letter, its mark and its reason. The date and the model are not in it, because they do not change what a participant sees. A record of step 6 has one fingerprint for each of its 15 questions. The marks record has one for each mark (decision 0037, item 13). Step 8 calculates the fingerprint of each record again and compares. A different fingerprint stops the build. Then the record must pass the checks again. This closes the open item of decision 0016. It adds one field, `fingerprint`, to the verdict records of steps 3, 4 and 6 and to the marks record (decisions 0031, 0032, 0034 and 0035).
9. **The portal.** The two files have our own format. A converter for the portal comes later, when the format of the portal is known.

### The contract of the step (decision 0018)

- It receives the question records, the verdict records and the marks record of one mock.
- It returns the two files.
- It can fail when a slot is open, a verdict is missing, or a record changed after its check. Then code builds no file and names the cause.

## Reason

- **Code builds the files from the records.** Decision 0016 has the reason: one true copy.
- **Two files.** Plain reason: the portal can send the questions to a participant with no answers in the same file.
- **Groups by scenario, each with its story.** The guide says: "Each scenario presents a realistic production context that frames a set of questions." (Section 5).
- **The domain of each question.** The exam reports a result for each domain: "Pass/fail with scaled score (100–1,000), plus percent-correct by domain on the score report" (Section 3). With the domain in the file, the portal can show the same.
- **The line "Select N."** The guide says: "each item states how many responses to select" (Section 3).
- **The 120 minutes.** Decision 0003: a mock has 120 minutes. The file has the number, so the portal does not have to know it.
- **The fingerprint.** Decision 0016 says that nobody edits a file by hand. A rule alone does not make sure of that. The plain reason for the fingerprint: code can prove that the question in the mock is the question that the checks saw.
- **Our own format.** The assistant does not know the file format that the portal reads. Plain reason: the pipeline does not wait for the portal, and a converter is a small step.

Not decided yet:

- The format that the portal reads, and the converter.
- The exact names of the fields in the two files.
- If the portal shows the point of a question to a participant.
- How the portal calculates a score. The exam uses a scaled score (Section 3). The guide does not say how it is calculated.
- If the correct letters are spread well over a mock (also open in decision 0034).

## How we decided

The assistant showed the proposal. The owner first asked for better visuals in the diagrams. After the new form of diagram 09, the owner said: "step 8 is good".

The owner approved the proposal in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

none. The decision uses Sections 3 and 5 of the guide.
