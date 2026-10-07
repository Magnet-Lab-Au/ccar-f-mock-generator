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
| `docs/build-guide/` | The build guide "How the Mocks Are Built": one file for each pipeline step. The section of step 1 exists. |
| `docs/reviews/` | The reports of independent reviewers |
| `docs/journal.md` | What we did in each work session |
| `docs/coverage/task-statement-decisions.xlsx` | The 240 points of the exam guide. It is the final check that the design missed nothing. |
| `reference/exam-guide.md` | The exam guide, Version 1.0, July 2026 |
| `reference/task-statements-and-points.md` | The 30 task statements and their 240 points, exact text. An independent reviewer confirmed it on 5 October 2026. |
| `reference/practice-audit-first-build.md` and `.json` | The audit of the first build against the 240 points |
| `src/` | The program. It has the two scripts of step 0, steps 1, 3, 7 and 8, and the control. Steps 2, 4, 5 and 6 do not exist yet. |
| `runs/` | The run records. Empty until the first run. |

## Status

7 October 2026: each of the 9 steps has a design decision and a diagram (decisions 0026 to 0036, diagrams 02 to 10). Decision 0038 makes the control simple for mock 1 and writes it as code with tests. The control exists: `src/control.py`, with its tests in `tests/` (decision 0039). Step 1 is built, and it made the plan of mock 1. The other real steps do not exist yet, only fakes in the tests. Decisions 0024 and 0027 to 0036 and diagrams 07 and 08 describe the control. The other diagrams do not show decisions 0038 and 0039 yet. Step 0 ran: the file `reference/guide-records.json` exists, and it is the one source of guide text for code. The next steps are in `HANDOFF.md`.
