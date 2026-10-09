# The build guide "How the Mocks Are Built"

The build guide shows participants how the program makes the mocks, as a worked example of the exam guide. It is a product of this work, with the same weight as the program.

- One file for each pipeline step, in this folder.
- Each file has a short explanation, one diagram, and a table of the exam guide points that the step uses.
- The source of each file is the Reason section of the decisions for its step. A file does not use the section "How we decided", and it does not tell the history of the first build.
- Each file has a status: "planned" or "built". A file becomes "built" only when a run record shows the step.

Sections:

| Step | File | Status |
|---|---|---|
| 0. Prepare the guide records | `step-0-prepare-the-guide-records.md` | built (6 October 2026), section written on 9 October 2026 |
| 1. Plan the mock | `step-1-plan-the-mock.md` | built (7 October 2026), changed on 8 October 2026 (point groups, the spread over the mocks, the fixed scenarios of mocks 3 to 5) and 9 October 2026 (balanced correct letters) |
| 2. Write the question | `step-2-write-the-question.md` | built (7 October 2026), changed on 8 October 2026 (rules A12, B8 and B9, two-answer slots, the earlier questions on the same idea) and 9 October 2026 (stricter B9, narrow ideas, cached rules, balanced letters) |
| 3. Check by code | `step-3-check-by-code.md` | built (7 October 2026), changed on 8 October 2026 (rule A12) |
| 4. Check by a model | `step-4-check-by-a-model.md` | built (7 October 2026), changed on 8 October 2026 (rules B8 and B9) and 9 October 2026 (stricter B9, narrow ideas, prompt caching, the cost of all 5 mocks) |
| 5. Try again | `step-5-try-again.md` | built (8 October 2026), changed on 9 October 2026 (the reason of the owner after more tries) |
| 6. Check the complete mock | `step-6-check-the-complete-mock.md` | built (7 October 2026), changed on 8 October 2026 (rule C3 over the whole mock) and 9 October 2026 (the rule for the findings) |
| 7. The owner marks the questions | `step-7-the-owner-marks-the-questions.md` | built (7 October 2026), changed on 9 October 2026 (the second review marks mocks 4 and 5, all 60 of mock 5) |
| 8. Build the files | `step-8-build-the-files.md` | built (8 October 2026), built mocks 1 to 5 by 9 October 2026 |

A script makes each section: `make-section-step-0.py` makes step 0, `make-section-step-1.py` makes step 1, and `make-sections.py` makes steps 2 to 8.

## What participants should know about the mocks

- **Mocks 4 and 5 often test the same problem as mocks 1 to 3, in a new setting.** The guide has 95 ideas, and 5 mocks have 300 questions, so each idea comes back. For most ideas the guide gives almost only one problem and one answer. The program blocks only copies: a question with the same scene, the same answer and the same wrong options as an earlier one (decisions 0060, 0066, 0068, 0072 and 0075).
- **Mock 5 is a review mock.** It mostly revisits problems of mocks 1 to 4 in new settings. 46 of its 60 questions are close to a question of an earlier mock (decision 0076). Use it to review, not as a new test.
- **No person reads the questions of mocks 4 and 5.** The writer, the checkers and the second review are all Claude models. The owner read and marked the questions of mocks 1 to 3 (decisions 0069 and 0071).

A deviation from the exam guide is shown openly in its section: what the guide teaches, what the build does instead, and the source with its page, section and exact text. Decision 0040 is the first case: the model steps use structured outputs, not a forced tool call.
