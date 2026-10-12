# Diagrams

One HTML file for each diagram. The file name starts with a number, for example `01-pipeline-overview.html`.

A diagram for participants uses plain words and no decision numbers. The decision file names its diagram.

| File | What it shows |
|---|---|
| `01-pipeline-overview.html` | The 9 steps of the pipeline on one page, with the path of a question that fails. Each box opens a popup with the exam guide points of its step and its status. Corrected on 7 October 2026: step 6 sends no question back. |
| `02-step-1-plan-the-mock.html` | Step 1 in 5 parts: what the plan of a mock receives, does and returns, and what can fail. Each box opens a popup with the detail and the exam guide text. |
| `03-step-0-prepare-the-guide-records.html` | Step 0: how a script copies 5 sections of the exam guide into the records file, the three checks of the file, and how a later step takes a slice from it. Each box opens a popup with an example from the file. |
| `04-step-2-write-the-question.html` | Step 2: what code sends in one API call, the two answers that the model can give, and what code does after the call. Each box opens a popup with an example. |
| `05-step-3-check-by-code.html` | Step 3: one question goes through the 12 exact rules (A1 to A12), the two results, and the verdict record. Each rule opens a popup with an example of a finding. |
| `06-step-4-check-by-a-model.html` | Step 4: the blind answer without the answer key, the check of the 9 rules (B1 to B9) with the answer key, and the three verdicts. Each rule opens a popup with an example of a finding. |
| `07-step-5-try-again.html` | Step 5, in the new visual form (7 October 2026): the four ways a question comes back, what the writer gets for the new try, the limit of 3 tries for each start of a slot, the open slot, the three actions of the owner, and a new start. Each part opens a popup. |
| `08-step-6-check-the-complete-mock.html` | Step 6, in the new visual form (7 October 2026): the code count of all 60 questions, the two model calls that read the 15 questions of one scenario together, and a finding that waits for the owner, who selects `ignore` or `rewrite`. Each part opens a popup. |
| `09-step-7-the-owner-marks-the-questions.html` | Step 7, in the new visual form: a question card, the marking sheet with the two columns that the owner fills, 60 squares for the size of the sample, and two bars for what the marks decide. Each part opens a popup. |
| `10-step-8-build-the-files.html` | Step 8, in the new visual form: the question records with their checks, the three checks and the fingerprint before the build, the two files, the 4 scenario groups, and what a participant gets during and after the mock. Each part opens a popup. |
| `11-repeats-across-mocks.html` | The rule against repeats across mocks (decisions 0056, 0066 and the narrow list of 0068, 0072 and 0075), in the visual form of diagrams 09 and 10, with a real question of mock 1, its repeat in mock 2, and the rewrite. |
| `12-scenarios-of-the-mocks.html` | A grid of the 5 mocks and the 6 scenarios (decision 0057). It reads the state of each mock from the files. |

On 7 October 2026 the text of diagrams 01, 02 and 04 to 10 was corrected to describe the built steps and decisions 0038 to 0043. On 8 October 2026 diagrams 01 and 02 got the point groups of step 1 (decisions 0047, 0048 and 0050), and diagrams 02, 04 to 08 got the changes of decisions 0052 to 0055. Diagram 11 shows the rule against repeats across mocks (decision 0056), and diagram 12 shows the scenarios of the 5 mocks (decision 0057). Both have the visual form of diagrams 09 and 10. On 9 October 2026, diagrams 01 to 12 got the changes of decisions 0066 to 0077: the stricter rule B9 and the narrow list, prompt caching, the balanced correct letters, the reason of the owner after more_tries, and the second review that marks mocks 4 and 5. Diagram 08 got the rule of the owner for the findings of step 6 (decisions 0059, 0064, 0069 and 0077). Diagram 03 and diagram 10 got their status. Diagram 12 shows all 5 mocks as built. Each diagram says its status in its footer.

## The check of the popups

`check-popups.py` opens each diagram in a headless browser with the script `check-popups.js`. It checks that each part opens its popup, that the popup stays in the window, and that Escape closes it. It changes no diagram. The comment at the top of `check-popups.py` has the command and the browser that it needs. Run it after each change of a diagram. On 12 October 2026 all 12 diagrams passed.
