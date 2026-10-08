# Handoff: start here

Date: 5 October 2026. Updated on 7 October 2026, second session. This file gives a new session what it needs to continue.

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

The section of step 1 exists. The diagrams 02 to 10 in `docs/diagrams/` are the diagrams of steps 0 to 8. Rule 18 still applies to the portal page "How the Mocks Are Built New".

## Read these files first, in this sequence

1. `WORKING-RULES.md`: how the assistant works here. Part A has the rules of the owner. Part B has rules that the assistant suggested. The owner confirmed Part B on 6 October 2026. Part C has one change of rule 1.
2. `README.md`: what is in this folder.
3. `docs/journal.md`: the top entry.
4. `docs/decisions/`: decisions 0001 to 0046. Read decision 0038 before the step files: it changes the control. Read 0039 after 0038: it describes the control code. Read 0019 together with 0003 to 0018. Decisions 0027 to 0036 are the design of steps 0 to 8 and the rules for a good question. Decision 0037 has the answers to the 14 serious items of the first review. Read them completely.
5. `docs/diagrams/01-pipeline-overview.html`: the nine steps on one page. Then diagrams 02 to 10, one for each of the steps 0 to 8. Diagrams 09 and 10 have the visual form that the owner wants.

Read these only when you need them:

- `reference/guide-records.json`: the records of the exam guide for code. Step 0 made it on 6 October 2026. It is the one source of guide text for code and for scripts.
- `reference/exam-guide.md`: the exam guide. Section 3 has the exam details. Section 5 has the 6 scenarios. Section 6 has the 30 task statements. Section 9 has 12 sample questions.
- `reference/task-statements-and-points.md`: the 30 task statements and their 240 points, with IDs. It is the file for people.
- `docs/reviews/`: the reports of the independent reviewers. `review-decisions-0024-to-0037.md` is necessary for the next step. `review-decisions-0026-to-0036.md` is the first review of the step files.
- `reference/practice-audit-first-build.md`: History of the first build. Not a source for the design.

## Where we are

State on 7 October 2026, second session.

- Decisions 0001 to 0039 exist. The owner confirmed the text of each one. Rule 26 applies to all of them. The owner confirmed 0019 to 0036 and 0039 on 7 October 2026, after a summary of one line for each file.
- Decisions 0003 to 0008 set the form of a mock, its scope and its source of facts.
- Decisions 0009 to 0017 are the steps 0 to 8 of the pipeline. Decision 0018 sets two rules for the design of the steps. Decision 0019 corrects errors in the reasons of 0003 to 0018. Decisions 0020 to 0025 close open questions and confirm the list of steps.
- Decision 0026: the build guide does not show MCP, subagents, hooks or sessions at work.
- **Each of the 9 steps has a design decision and a diagram. The design is not complete.** A first review found 14 serious items in decisions 0026 to 0036. Decision 0037 (third session of 6 October 2026) has an answer to each one, and the owner confirmed its text. Decisions 0024, 0027 and 0029 to 0036 were changed and have those answers. Where decision 0037 and a step file disagree, tell the owner.
- **A second review checked the changed files.** Of the 14 items, 8 are closed and 6 are closed in part. The reviewers found 3 new errors and 10 new serious items. A programmer who has only the decision files still meets cases with no path. The report is `docs/reviews/review-decisions-0024-to-0037.md`. Read it before you continue. In the table below, "Designed" means: a decision and a diagram exist. It does not mean: ready for code.
- **Decision 0038 stops the cycle of reviews.** The fixes of the first review made the 10 new items. All of them are in the control. The theme: too much automatic repair, designed before one real run. So the control is simple for mock 1. One automatic loop stays: a question that fails step 3 or step 4 goes to step 5, with the limits of decisions 0033 and 0037. Each other failure waits for the owner. Step 6 sends no question back. The owner accepts a mock with a command before step 8 builds the files.
- **The control exists as code with tests** (decision 0039): `src/control.py`, `tests/fakes.py` and `tests/test_control.py`. 53 tests pass, and no test makes a model call. Two independent reviewers checked it. No reviewer checked the last round of fixes. Each step is a fake. The owner has no command line yet.
- Where decision 0038 and an older file disagree, decision 0038 is correct. Decisions 0024 and 0027 to 0036 were corrected on 7 October 2026 so that they describe the control. Diagrams 07 and 08 were made again. The other diagrams do not show decisions 0038 and 0039 yet.

| Step | Decision | Diagram | State |
|---|---|---|---|
| 0. Prepare the guide records | 0028 | 03 | Designed, and the step ran. The file `reference/guide-records.json` exists. |
| 1. Plan the mock | 0027 | 02 | Built and ran: `src/step1_plan.py`, 20 tests. The plan of mock 1 exists: `runs/mock-01/plan.json`, seed 366341. Build guide section: `docs/build-guide/step-1-plan-the-mock.md`. Diagram 02 is corrected. |
| 2. Write the question | 0029 | 04 | Built, ran in the test and in mock 1. Build guide section exists. |
| The rules for a good question (17 rules) | 0030 | none | Decided |
| 3. Check by code | 0031 | 05 | Built, ran in the test and in mock 1. Build guide section exists. |
| 4. Check by a model | 0032 | 06 | Built, ran in the test and in mock 1. Build guide section exists. |
| 5. Try again | 0033 | 07 | Built, ran in mock 1. Build guide section exists. |
| 6. Check the complete mock | 0034 | 08 | Built, ran in the test and in mock 1. Build guide section exists. |
| 7. The owner marks the questions | 0035 | 09 | Built, ran in the test and in mock 1. Build guide section exists. |
| 8. Build the files | 0036 | 10 | Built, built mock 1 on 8 October 2026. Build guide section exists. |

- Code that exists: `src/step0_prepare_guide_records.py`, `src/check_guide_records.py` and `src/control.py`, with the tests in `tests/`. No real step from 1 to 8 exists. Four check scripts are in `docs/decisions/`, for decisions 0027, 0031 and 0037.
- The checks of the records file: a second script passed 41 of 41 checks. An independent reviewer found no errors (`docs/reviews/review-guide-records.md`). The comparison of `reference/exam-guide.md` with the original guide is not done.
- No agreed step uses a subagent, MCP or the Agent SDK. Each model step is a call of the plain API with a fixed answer form (decisions 0029 and 0032). The owner asked why, and said: "keep the simple api".
- One mock needs these model calls when no question fails: 60 writer calls, 60 blind answers, 60 rule checks, and 8 calls of step 6 (2 for each scenario).
- The design names three folders that do not exist yet. The program makes them: `runs/mock-01/` (the plan, the question records, the verdict records, the marks record, the decisions of the owner and the report), `marking/` (the Excel files that the owner fills) and `mocks/` (the two files of each mock).
- `docs/lessons.md` is private history of the first build. It is not a source for the design.

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
- The program selects the 4 scenarios at random, from 11 of the 15 possible sets (decision 0027).
- A finished mock is two JSON files: the questions, and the answers with the reasons (decision 0036). The format that the portal reads is not known. A converter comes later.
- A multiple-choice question has 4 options and 1 correct answer. A multiple-response question has 5 options and 2 correct answers (decision 0029). The number 8 and the form "5 options, 2 correct" are guesses with no source.

Not decided:

- How many mocks the program makes.
- If a later version can use other sources than the exam guide (decision 0008 covers the first version only).

## The next steps

1. Mock 1 is built (`mocks/mock-01.questions.json` and `mocks/mock-01.answers.json`), with the known limits of decision 0046. It cost $17.17. Next: the owner confirms the text of decision 0046. Then the 7 changes before mock 2 of decision 0046, one at a time, each with its own decision file. Then mock 2.
2. A script checks the workbook `docs/coverage/task-statement-decisions.xlsx`: each of the 240 points has an answer, and each answer names a step that exists (decision 0018). The three yellow columns of the workbook are still empty.
3. Set up the API key. It must not be in a file of the repository. Then the test of decision 0024, and then mock 1. Before mock 1, the real steps and a command line for the owner must exist.

A rule for each of these steps, so that nobody has to reconstruct the build guide later: when a pipeline step is built and a run record shows it, write its build guide section in `docs/build-guide/` and correct its diagram, before the next pipeline step starts. The section "The build guide" above gives the source and the structure. The control program is not a pipeline step. It gets a decision file and a journal entry.

### The 10 serious items of the second review, after decision 0038

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
| Decision 0040: structured outputs | The model steps 2, 4, 5 and 6 send their form as structured outputs, because the current models reject a forced tool call. This deviates from the exam guide (4.3-K1, 4.3-S3). The build guide sections of these steps must show the deviation, with the page, the section and the exact text. The pages are saved in `docs/sources/`. |
| Rule A11 and words like "cannot" | Step 3 follows the text of decision 0038, part 8: "not" or "except" in small letters, or "NOT" or "EXCEPT" in capital letters. So "cannot", "doesn't", and "Not" or "Except" at the start of the last sentence pass. Also, an abbreviation with a dot can hide the last sentence. A change needs a new decision. |
| Decision 0009, points 1.6-K1 and 1.6-S1 | Its Reason uses these points for a plan that code makes. The guide wrote them for a sequence of model calls (prompt chaining), and step 1 has no model call. The build guide section of step 1 states the limit. The owner confirmed the text of 0009, so a correction needs a new decision file (rule 26). Ask the owner. |
| The real steps | Each step has code and tests. Steps 0 to 4, 6 and 7 ran (step 0 on 6 October, the others in the test of 7 October 2026). Steps 5 and 8 have not run yet. |
| The command line of the owner | `src/run.py`, with the commands `run`, `report`, `mark`, `decide` and `accept`. It has not run on a real mock yet. |
| Review | Two reviewers checked decisions 0024 and 0027 to 0037 on 6 October 2026, after the changes. No independent reviewer checked decision 0038, decisions 0001, 0002, 0019 to 0023, 0025 and 0026, or diagram 01. Nobody reviewed this file or `CLAUDE.md`. Two reviewers checked `src/control.py` and decision 0039 on 7 October 2026. One reviewer checked the corrected decisions 0024 and 0027 to 0036, and one checked diagrams 07 and 08. Later on 7 October, one reviewer checked decisions 0040 to 0043 (corrections in decision 0044), and one checked the build guide sections of steps 2, 3, 4, 6 and 7 and the corrected diagrams. Nobody checked the last fixes or decision 0044. |
| The other findings of the second review | Corrected on 7 October 2026 in decisions 0024 and 0027 to 0036. Open parts are now in the lists "Not decided yet" of those files, for example rule B6 (0030) and case (h) (0032). |
| Decision 0037, one sentence | Its Reason says that point 1.4-K2 tells us that code must enforce a rule. The point says only that an instruction can fail. The owner confirmed the text, so the correction needs a new file (rule 26). |
| The findings of the first review on the diagrams | 10 diagram errors of the first review are not corrected. Diagrams 02 to 10 also show the design before decision 0037. |
| Items that the decisions list as "not decided yet" | Each decision from 0027 to 0036 has a list "Not decided yet". The review said that this table does not have each of those items. Read those lists in the decision files. |
| A false sentence in diagram 06 | Corrected on 7 October 2026. |
| The copy of the exam guide | `reference/exam-guide.md` is a copy of a file in the Claude project "CPN Learning path". The comparison with the original, character for character, is not done. The assistant can read the original only as text in the chat, not as a file. The assistant asked the owner if the original file is on the computer. The owner did not answer yet. |
| The number of mocks | Not decided. It also decides how the program selects the scenarios across mocks, and how it prevents the same scene in two different mocks. |
| A task statement that does not fit its scenario | The plan does not prevent it (decision 0027). The writer can answer `cannot_write`. Then the slot gets the status `open`, and the owner decides (decision 0037). An automatic path is decided after the test of decision 0024. |
| Numbers | Decided, but each one is a guess or has a margin with no source, and can change after the test: 3 tries for one slot (decision 0033), 3 runs of step 6 for one scenario and 3 runs of a call that fails (decision 0037), the limits of rules A6 and A7 (decision 0031), at most 2 questions with the same wrong idea (decision 0034), and the bad marks that stop a mock: more than 6 of 60 for mock 1, 2 or more of 20 for a later mock (decision 0035). Not decided: when the sample of the owner goes below 20. |
| Rule B6 | Decided in decision 0037: the model lists the feature names, and code searches them in the records file. Not decided: a part of a word against a complete word, a plural, and if a name on the list "out of scope" of Section 17 counts as named. |
| Rule A5 | The exact list of words is not decided (decision 0031). |
| The 5 texts with a backslash | 5 texts of the records file have a backslash from the file format. A step that shows them must handle it (`docs/reviews/review-guide-records.md`). |
| The models and the cost | First values, not decisions: Claude Opus 5.5 at effort "high" (decision 0041). Price checked on 7 October 2026: $4 per million input tokens and $20 per million output tokens. The test cost $3.86. Estimate for mock 1: $12 to $16. |
| The format of the portal | Not known. Step 8 writes our own two files. A converter for the portal comes later (decision 0036). |
| The fingerprint | Decided in decisions 0036, 0037 and 0039: the fields as JSON with sorted keys, in UTF-8. |
| The correct letters | Not decided: if the correct letters are spread well over a mock (decisions 0034 and 0036). |
| The answer forms | The JSON schemas of decisions 0029, 0032 and 0034 are sent as structured outputs (decision 0040). They worked in the test of 7 October 2026. Decision 0041 changed the description of the "reason" fields, and decision 0043 added "B7". |
| The Agent SDK | Decision 0002 names it. The design of all 9 steps is complete, and no step uses it (decisions 0012, 0029, 0032 and 0034). So a new decision must say so. It is not written yet. |
| Version control | Decided on 7 October 2026: a folder in WSL with a private repository on GitHub. The owner makes it. Check it at the start (next step 1). |
| Which product writes the code | Decided on 7 October 2026: the work moves to Claude Code now (decisions 0002 and 0038). The two scripts of step 0 and the four check scripts were written in Cowork. |
| The audit | 52 of its 240 rows had one check, not two. These are the rows with a weak fit or no fit. |
| The portal pages | Two prototype pages exist on claude.ai. "How the Mocks Are Built Old" shows the first build and the audit. "How the Mocks Are Built New" shows a design of 2 October that is not the design of this folder. |
| Diagram 01 | Corrected on 7 October 2026: step 6 sends no question back, and each popup shows the status of its step. Some box texts of the older form are a little too long for their boxes. |
| Diagrams 02 to 06 | They have an older form: boxes of text with popups. The owner said that they do not have to be made again. Diagrams 07 to 10 have the form that the owner wants. On 7 October 2026 the text of each diagram was corrected to describe the built steps. |

## Where the old material is

You do not need it for the design. It is here if the owner asks. Each folder is in OneDrive, in `C:\Users\shekh\OneDrive\Desktop\Learning\CPN Learning pathway\CCAR-F\`. After the move to WSL they are not next to this folder. Rule 27 applies: do not change them.

| Folder | Content |
|---|---|
| `CCAR-F Mocks v2/` | The second attempt: an older decision file, and the record of the first build in `reference/first-build/` |
| `Mocks/` | The five mocks of August 2026 and the question bank |
| `CCAR-F Portal Mocks/` | The five mocks after the review of September 2026 |
| `CCAR-F Study Pack/` and the numbered files in `CCAR-F/` | Study files of the owner, and some records of the first build (files 06, 10 and 11). Many of them are personal. |

## What the owner says to start

"Read `HANDOFF.md` in `ccar-f-mock-generator` and follow it."
