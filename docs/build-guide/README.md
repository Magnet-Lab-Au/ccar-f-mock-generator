# The build guide "How the Mocks Are Built"

The build guide shows participants how the program makes the mocks, as a worked example of the exam guide. It is a product of this work, with the same weight as the program.

- One file for each pipeline step, in this folder.
- Each file has a short explanation, one diagram, and a table of the exam guide points that the step uses.
- The source of each file is the Reason section of the decisions for its step. A file does not use the section "How we decided", and it does not tell the history of the first build.
- Each file has a status: "planned" or "built". A file becomes "built" only when a run record shows the step.

Sections:

| Step | File | Status |
|---|---|---|
| 1. Plan the mock | `step-1-plan-the-mock.md` | built (7 October 2026), changed on 8 October 2026 (point groups) |
| 2. Write the question | `step-2-write-the-question.md` | built (7 October 2026) |
| 3. Check by code | `step-3-check-by-code.md` | built (7 October 2026) |
| 4. Check by a model | `step-4-check-by-a-model.md` | built (7 October 2026) |
| 5. Try again | `step-5-try-again.md` | built (8 October 2026) |
| 6. Check the complete mock | `step-6-check-the-complete-mock.md` | built (7 October 2026) |
| 7. The owner marks the questions | `step-7-the-owner-marks-the-questions.md` | built (7 October 2026) |
| 8. Build the files | `step-8-build-the-files.md` | built (8 October 2026) |

A script makes each section: `make-section-step-1.py` makes step 1, and `make-sections.py` makes steps 2 to 8. Step 0 has no section yet: it ran before the build guide existed.

A deviation from the exam guide is shown openly in its section: what the guide teaches, what the build does instead, and the source with its page, section and exact text. Decision 0040 is the first case: the model steps use structured outputs, not a forced tool call.
