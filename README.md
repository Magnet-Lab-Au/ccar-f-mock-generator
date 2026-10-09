# ccar-f-mock-generator

A program that writes and checks mock exam questions for the CCAR-F exam (Claude Certified Architect – Foundations).

This folder is the third attempt. It starts clean. The first build (August 2026) and the folder `CCAR-F Mocks v2` are history. We do not continue them.

## Rules of this folder

1. Record each decision on the day we make it, in `docs/decisions/`. One file for each decision.
2. Make each diagram when we make its decision, in `docs/diagrams/`. One HTML file for each diagram. Each diagram names its decision.
3. Write one entry in `docs/journal.md` for each work session.
4. The files in `reference/` are read only.
5. The program writes a record of each run in `runs/`. No person writes there.

## Where to find things

| Folder or file | Content |
|---|---|
| `HANDOFF.md` | Start here. What a new session reads, where the work stopped, and the next step. |
| `WORKING-RULES.md` | How the assistant works in this folder |
| `CLAUDE.md` | The file that Claude Code reads at the start of each session. It imports `WORKING-RULES.md`. |
| `docs/lessons.md` | Private history of the first build. Not a source for the design. |
| `docs/decisions/` | The decisions, in sequence. `TEMPLATE.md` shows the form. |
| `docs/diagrams/` | The diagrams, as HTML files |
| `docs/build-guide/` | The build guide "How the Mocks Are Built": one file for each pipeline step. All 8 sections exist (steps 1 to 8). |
| `docs/reviews/` | The reports of independent reviewers |
| `docs/journal.md` | What we did in each work session |
| `docs/portal-notes.md` | Notes for the people who put the mocks on the portal |
| `docs/sources/` | Saved pages of the Anthropic documentation that decisions cite |
| `docs/coverage/task-statement-decisions.xlsx` | The 240 points of the exam guide. It is the final check that the design missed nothing. |
| `reference/exam-guide.md` | The exam guide, Version 1.0, July 2026 |
| `reference/task-statements-and-points.md` | The 30 task statements and their 240 points, exact text. An independent reviewer confirmed it on 5 October 2026. |
| `reference/practice-audit-first-build.md` and `.json` | The audit of the first build against the 240 points |
| `src/` | The program: the code of each step, the control, the command line `src/run.py`, the point groups (`point_groups.py`), the earlier questions across mocks (`earlier.py`), and two test scripts that call the API (`test_b9.py`, `test_cache.py`). |
| `tests/` | The tests of the program. No test makes a model call. |
| `data/` | Data that the owner confirmed: the point groups, the two-answer points, the narrow ideas and the scenarios of mocks 3 to 5 |
| `marking/` | The Excel files of each marking round. A marked file is committed before anybody else reads it. |
| `mocks/` | The built mocks: `mock-0N.questions.json` and `mock-0N.answers.json` for mocks 1 to 5 |
| `runs/` | The run records of each mock and of each test: plans, questions, checks, marks, decisions of the owner and cost |

## Status

9 October 2026: all 5 mocks are built, in `mocks/`. The program ran each of the 9 steps for each mock. Decisions 0001 to 0078 record the design and each change. The cost of the runs: mock 1 $17.17, mock 2 $20.73, mock 3 $23.85, mock 4 $12.83 and mock 5 $11.68. The owner read and marked mocks 1 to 3. The second review in Cowork, a Claude model, marked mocks 4 and 5. The next steps are in `HANDOFF.md`.
