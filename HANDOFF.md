# Handoff: start here

Date: 5 October 2026. Updated on 9 October 2026. This file gives a new session what it needs to continue.

From 7 October 2026 the work continues in Claude Code. The owner moves this folder out of OneDrive, to a folder in WSL with a private repository on GitHub. The folder in OneDrive is then old.

## Words

| Word | Meaning |
|---|---|
| The owner | The person who directs this work. The owner passed the CCAR-F exam. |
| CCAR-F | The exam "Claude Certified Architect – Foundations" |
| Mock | A practice exam paper. "Mock" and "paper" are the same thing. |
| The portal | MagnetLab Academy, a learning site for people who prepare for the exam. A separate project builds it. |
| Participant | A person who uses the portal |
| The first build | Two things together: an assistant made five mocks in August 2026 in a chat session, and a review repaired them in September 2026 |
| `CCAR-F Mocks v2` | A second attempt, of 2 October 2026. It made decisions and records. It made no mocks. |
| Cowork | The Claude desktop product that the discussions ran in until 7 October 2026 |
| Claude Code | The Anthropic product that writes the program, from 7 October 2026 (decisions 0002 and 0038). It reads `CLAUDE.md` at the start of each session. |
| The control | The part of the program that decides what happens next to a slot or to a mock: the loop, the limits, the statuses and the decisions of the owner |
| Session | One chat with the assistant |
| The exam guide, or "the guide" | The official guide of the CCAR-F exam, `reference/exam-guide.md` |
| The build guide | "How the Mocks Are Built": the pages in `docs/build-guide/` that show participants how the program makes the mocks |

## The goal

1. Build a program that writes and checks mocks for the CCAR-F exam. The portal will launch with these mocks.
2. Document the build during the work: each decision, each diagram and each run. Later a portal page will show participants how the program makes the mocks, as a worked example of the exam guide.

## The build guide "How the Mocks Are Built"

The build guide is a product of this work. It has the same weight as the program. It is the portal page of goal 2.

- **Source.** The Reason section of each decision. Each Reason stands on the exam guide. The build guide does not use the section "How we decided", and it does not tell the history of the first build.
- **Structure.** One section for each pipeline step. Each section has a short explanation, one diagram, and a table of the exam guide points that the step uses. The sections are files in `docs/build-guide/`, one file for each pipeline step.
- **Status.** Each section has the status "planned" or "built". A section becomes "built" only when a run record shows the step.

All 8 sections exist, for steps 1 to 8. The diagrams 02 to 10 in `docs/diagrams/` are the diagrams of steps 0 to 8. Diagrams 11 (repeats across mocks) and 12 (the scenarios of the 5 mocks) show the rules across mocks. Rule 18 still applies to the portal page "How the Mocks Are Built New".

## Read these files first, in this sequence

1. `WORKING-RULES.md`: how the assistant works here. Part A has the rules of the owner. Part B has rules that the assistant suggested. The owner confirmed Part B on 6 October 2026. Part C has one change of rule 1.
2. `README.md`: what is in this folder.
3. `docs/journal.md`: the top entry.
4. `docs/decisions/`: decisions 0001 to 0078. Read decision 0038 before the step files: it changes the control. Read 0039 after 0038: it describes the control code. Read 0019 together with 0003 to 0018. Decisions 0027 to 0036 are the design of steps 0 to 8 and the rules for a good question. Decision 0037 has the answers to the 14 serious items of the first review. Read them completely.
5. `docs/diagrams/01-pipeline-overview.html`: the nine steps on one page. Then diagrams 02 to 10, one for each of the steps 0 to 8, and diagrams 11 and 12 for the rules across mocks. Diagrams 09 to 12 have the visual form that the owner wants.

Read these only when you need them:

- `reference/guide-records.json`: the records of the exam guide for code. Step 0 made it on 6 October 2026. It is the one source of guide text for code and for scripts.
- `reference/exam-guide.md`: the exam guide. Section 3 has the exam details. Section 5 has the 6 scenarios. Section 6 has the 30 task statements. Section 9 has 12 sample questions.
- `reference/task-statements-and-points.md`: the 30 task statements and their 240 points, with IDs. It is the file for people.
- `docs/reviews/`: the reports of the independent reviewers. `review-decisions-0024-to-0037.md` is necessary for the next step. `review-decisions-0026-to-0036.md` is the first review of the step files.
- `reference/practice-audit-first-build.md`: History of the first build. Not a source for the design.

## Where we are

State on 9 October 2026.

- **All 5 mocks are built** in `mocks/`: `mock-0N.questions.json` and `mock-0N.answers.json`. The cost of the runs: mock 1 $17.17, mock 2 $20.73, mock 3 $23.85, mock 4 $12.83, mock 5 $11.68 (plus under $1 of a stopped run, decision 0073).
- **Decisions 0001 to 0078** record the design and each change. The owner confirmed the texts of 0001 to 0072. Decisions 0073 to 0078 wait for the confirmation of the owner. Decision 0078 corrects three lines of the confirmed decisions 0047, 0068 and 0071.
- **The marks.** The owner read and marked mocks 1 to 3. For mock 4 the owner did not read the questions. The second review in Cowork, a Claude model, marked mocks 4 and 5 (decisions 0069, 0071 and 0073). So no person read the questions of mocks 4 and 5.
- **The rules across mocks.** Point groups (decisions 0047, 0048), the spread of ideas (0050), no repeat of an earlier question with rule B9 (0056, stricter in 0066), the narrow list of 63 of 95 ideas that keep the copy rule (0066, 0068, 0072, 0075), the fixed scenarios of mocks 3 to 5 (0057), and no copy across mocks (0060).
- **Other rules since mock 1:** rule A12 on the longest option (0053), two-answer points (0054), rule B8 against copies of the sample questions (0055), rule C3 over the whole mock (0052), prompt caching (0067), balanced correct letters from mock 5 (0070), the reason of the owner after more tries (0074).
- **Known limits** of each mock: decisions 0046 (mock 1), 0058 and 0059 (mock 2), 0063 (mock 3), 0069 (mock 4), 0076 and 0077 (mock 5). Mock 5 is a review mock: 46 of its 60 questions are close to an earlier mock.
- **The program:** `src/` with 228 tests in `tests/`. The command line is `src/run.py`. No test makes a model call.

| Step | Decisions | Diagram | State |
|---|---|---|---|
| 0. Prepare the guide records | 0028 | 03 | Ran on 6 October 2026. `reference/guide-records.json` exists. |
| 1. Plan the mock | 0027, 0047, 0048, 0050, 0053, 0054, 0056, 0057, 0070 | 02, 11, 12 | Built, ran for mocks 1 to 5 |
| 2. Write the question | 0029, 0053 to 0056, 0066, 0067, 0070 | 04 | Built, ran for mocks 1 to 5 |
| The rules for a good question (21 rules: A1 to A12, B1 to B9) | 0030, 0043, 0053, 0055, 0056, 0066 | 05, 06 | Decided |
| 3. Check by code | 0031, 0053 | 05 | Built, ran for mocks 1 to 5 |
| 4. Check by a model | 0032, 0055, 0056, 0061, 0066, 0067 | 06 | Built, ran for mocks 1 to 5 |
| 5. Try again | 0033, 0045, 0074 | 07 | Built, ran for mocks 1 to 5 |
| 6. Check the complete mock | 0034, 0052 | 08 | Built, ran for mocks 1 to 5 |
| 7. Mark the questions | 0035, 0071, 0073 | 09 | Built, ran for mocks 1 to 5 |
| 8. Build the files | 0036 | 10 | Built mocks 1 to 5 |

### How the owner wants the work (from the second session of 6 October)

- Short answers in the chat. Do not overload the owner. Write in Simplified Technical English.
- For the design of a step: one proposal with all details, with the exact file format and the exact fields. If the owner does not understand the proposal, tell it as the story of one question.
- Do not hand the owner a design that is not specific. The owner asked: where does this text come from, which file, which fields?
- A diagram of a step shows what a reader must understand, not a list of what the code does. It has hover popups with a real example from the files. It has no element that is not necessary. A script makes each one: `docs/diagrams/NN-make-diagram.py`.
- A diagram shows the thing itself, not a box with its name. Examples: a question card with options, a sheet with rows and the columns that the owner fills, 60 squares for the size of a sample, a bar with zones for a limit. The owner said "the visuals could be better" for diagrams 02 to 08, and "much better" for diagram 09. Diagrams 09 and 10 have this form. The owner said that the older diagrams do not have to be made again.
- Make the diagram of a step when its decision is made. Do not postpone it.
- From the third session of 6 October: make each explanation short, and tell it as the story of one question from the start. The owner asked for a more simple explanation of 4 of the 14 items. A table of fields is too much for the first explanation.
- The owner discussed the 14 items one at a time, with one question for each item. That worked well.
- Explain in plain words what code does. Do not show code to the owner if the owner did not ask for it.

## What a finished mock is

Decision 0003: a mock has the same form as the exam. These are the facts from the exam guide (Sections 3, 4 and 5):

- 60 questions and 120 minutes.
- 4 scenarios, from the 6 scenarios of the guide.
- Multiple-choice and multiple-response questions. Each question says how many answers to select.
- The approximate domain weights 27%, 18%, 20%, 20% and 15%.

Also decided:

- The program writes each question new. The build never reads the old questions (decision 0004).
- The two owner rulings of 29 September 2026 apply. Ruling 1 is in decisions 0005 and 0007. Ruling 2 is in decision 0006.
- The exam guide is the only source of facts in the first version (decision 0008).
- The numbers of one mock (decision 0027): 16, 11, 12, 12 and 9 questions for the 5 domains. 15 questions for each scenario. At least 1 question for each of the 30 task statements. 52 multiple-choice and 8 multiple-response questions, 2 in each scenario.
- The program selects the 4 scenarios at random, from 11 of the 15 possible sets (decision 0027). The owner fixed the sets of mocks 3 to 5 (decision 0057).
- A finished mock is two JSON files: the questions, and the answers with the reasons (decision 0036). The format that the portal reads is not known. A converter comes later.
- A multiple-choice question has 4 options and 1 correct answer. A multiple-response question has 5 options and 2 correct answers (decision 0029). The number 8 and the form "5 options, 2 correct" are guesses with no source.

Decided later:

- The program makes 5 mocks (decision 0049). Their scenarios (0057) and the rules against repeats (0056, 0060, 0066) are decided.

Not decided:

- If a later version can use other sources than the exam guide (decision 0008 covers the first version only).

## The next steps

1. The owner confirms the texts of decisions 0073 to 0078.
2. A converter from the two files of each mock to the format of the portal, when that format is known (decision 0036). The notes for the portal are in `docs/portal-notes.md`.
3. The workbook `docs/coverage/task-statement-decisions.xlsx`: its three yellow columns are still empty (decision 0018).

### History: the 10 serious items of the second review, after decision 0038

| # | Item | Result |
|---|---|---|
| 1 | Rule A11 has three different texts. | Closed by decision 0038, part 8. Decisions 0030 and 0031 do not have the new text yet. |
| 2 | A slot that goes back keeps the status `passed`. | Closed by decision 0038, part 9 |
| 3 | Step 6 asks the owner before the marking. | Removed. Step 6 sends no question back, and the owner sees its findings after the marking. |
| 4 | After `ignore`, the scenario cannot pass step 6. | Closed. The owner accepts the mock with a command. |
| 5 | The count of the runs of step 6 | Removed. The owner starts each round. |
| 6 | The values of `state` have no meaning. `id` in `owner-decisions.json` has no definition, and a finding of step 6 has no ID. | Closed by decision 0039. |
| 7 | `new_point` has no place to store the new point. No file says if `plan.json` changes, or how the new point stays different from the points of the other slots. | Closed by decision 0039. |
| 8 | After `more_tries` or `new_point`, no file says if the next call is a request of step 2 or of step 5, or which failed try it shows. | Closed by decision 0039. |
| 9 | A call that fails 3 times leaves no record. So the report has no source for `errors` after a new start. | Closed by decision 0039. |
| 10 | The exact conditions before step 8 builds the files | Closed by decision 0039. |

For each new reason:

- Take each exam guide text from `reference/guide-records.json` with a script. Do not type it.
- The guide wrote many points for a different context, for example code review or data extraction. When a reason uses such a point, say the context in the same file. The second review found 11 uses where a file does not do that.
- Do not say that a design is complete before a reviewer has checked it.
- When you make one file more exact, make each file that has the same rule agree. Rule A11 is the example.

In the workbook, the owner completes the three yellow columns. The assistant can write agreed notes there after a discussion. The column "Suggested decision" is a first suggestion from the audit. It is not a decision, and it is not a source for the design.

## Things that are open

| Open item | Note |
|---|---|
| The texts of decisions 0073 to 0078 | Not confirmed by the owner yet |
| The format of the portal | Not known. Step 8 writes our own two files. A converter comes later (decision 0036). `docs/portal-notes.md` has the notes for it. |
| The copy of the exam guide | `reference/exam-guide.md` is not compared with the original, character for character. |
| A repeat with different words | Rule B9 is a judgment of a model. It can fail a good question or pass a close one (decision 0066). |
| Rule A11 and words like "cannot" | Step 3 follows decision 0038, part 8. A change needs a new decision. |
| The Agent SDK | Decision 0002 names it. No step uses it. A new decision must say so. |
| The portal pages | "How the Mocks Are Built New" shows a design of 2 October. Rule 18 applies. |

## Where the old material is

You do not need it for the design. It is here if the owner asks. Each folder is in OneDrive, in `C:\Users\<the owner>\OneDrive\Desktop\Learning\CPN Learning pathway\CCAR-F\`. After the move to WSL they are not next to this folder. Rule 27 applies: do not change them.

| Folder | Content |
|---|---|
| `CCAR-F Mocks v2/` | The second attempt: an older decision file, and the record of the first build in `reference/first-build/` |
| `Mocks/` | The five mocks of August 2026 and the question bank |
| `CCAR-F Portal Mocks/` | The five mocks after the review of September 2026 |
| `CCAR-F Study Pack/` and the numbered files in `CCAR-F/` | Study files of the owner, and some records of the first build (files 06, 10 and 11). Many of them are personal. |

## What the owner says to start

"Read `HANDOFF.md` in `ccar-f-mock-generator` and follow it."
