# Lessons from the first build

Private history of the first build. Not a source for the design.

Lesson 3 leaves out the two limits of ruling 2. Decision 0006 is correct.

Each lesson is a rule. The line below it says where the lesson comes from.

"The first build" means two things together: an assistant made five mock papers in August 2026, and a review repaired them in September 2026. An audit on 2 October 2026 compared that work with the 240 points of the exam guide. "F" numbers are the failures in the record of the first build. The table at the end of this file lists them.

**Caution.** Lessons 5 to 21 use words such as "generator", "verifier" and "question bank". These are parts of the first build. They are not agreed steps of the new pipeline. The owner and the assistant have agreed on no step yet.

## Lessons for the design

1. **Design the steps of the pipeline first. Use the exam guide as the final check, not as the starting point.**
   The design of the first build connected its decisions to 14 of the 30 task statements. It had no decision for the other 16. (Audit, section 3.)

2. **A plan is not a record. A step counts as done only when a run record shows it.**
   In the first build, 40 guide points have a plan for the generation phase and no record that the step ran. Examples: the retry of a rejected question, and the review of a sample by the owner. (Audit, section 3.)

3. **Get the rulings of the owner before the build, not after it.**
   The owner gave two rulings on 29 September 2026, one month after the August work. Ruling 1: no question depends on a feature that the exam guide does not name. Ruling 2: at most one wrong option in each scenario uses a confidence value that the model reports about itself. In the first review of Mocks 2, 4 and 5, 32 questions failed on ruling 1 and 24 on ruling 2. The owner has not said if these rulings apply to the new build. Ask.

4. **Write the criteria before the first edit or the first run that they apply to.**
   The first 40 questions had zero rejections, because the list of rules was not complete (F5). In September, six editor runs changed 82 questions of Mocks 1 and 3 before the rubric existed, and 9 questions became worse.

5. **Measure against the sample questions of the exam guide before the first full run.**
   In Mock 3 the stems had a median of 120 words. The guide samples have a median of about 52 words (F6). In Mock 1, a punctuation pattern marked the correct answer. A person found it, not the verifier (F7).

6. **Do not make a rule from a fact that has no source and no date.**
   A note with no link and no date made Mocks 1 to 4 single-answer only. The exam has multiple-response questions (F4).

## Lessons for the pipeline

7. **Give each question an ID when a generator writes it. Connect each verdict, flag and edit to it by that ID.**
   The first build connected verdicts by position. In 10 groups each verdict was one record too late. 10 rejected questions entered Mocks 1 and 2, and 10 entered with no verdict (F2).

8. **Let code or the API enforce the format of each record. A sentence in a prompt does not enforce it.**
   The format was in the prompt only. 0 of 342 records have the domain in the designed form (F3). One flag had three field names, and the portal files then lost all 58 warning lines.

9. **Put a code check between steps. The code refuses an empty output, a missing verdict and a file that does not parse.**
   One run had the status "complete" when its output file had 0 bytes (F1). An append joined two records and damaged the question bank (F11).

10. **Give each agent the complete input that its task needs. Decide the input by relevance, not by length.**
    The verifier saw each earlier question cut at about 120 characters. 22 verifier notes say so. Nobody supplied the full text. The checked digests (files of exact quotes from the course material) were not in the list of what a generator receives (F10).

11. **When a checker says that information is missing, supply it and check again. Do not print a warning.**
    58 questions had a "needs review" flag. 35 flags had no reason. 16 of the 23 reasons were missing text. The questions entered the papers, and each got a warning line in the answer key.

12. **Send a failed question to a writer again, with the findings. Do not only drop it.**
    The design of the first build planned one retry. No record shows a retry of one question. The records show only new batches. In Mock 2, all three questions on task statement 1.6 were rejected, and the paper has no question on 1.6.

13. **Do not trust a confidence value before you compare it with labels from a person.**
    The flags did not predict defects. In the first review of Mocks 2, 4 and 5, 51% of the flagged questions failed and 55% of the others (F8).

14. **Show each result by segment: task statement, scenario, paper.**
    In the first review of Mocks 2, 4 and 5, 54% of the questions failed. By task statement the rate was 0% to 100%. Nobody divided the result. (Audit, section 5.)

15. **Check each paper as a whole before release: a count of questions for each task statement, and a search for repeated scenes.**
    Mock 2 had no question on task statement 1.6, and Mock 3 had none on 1.5. A script for a second check of repeated scenes did not work (F12).

16. **Keep the exact source text with each question to the end, and let code compare it with the source.**
    The field for the exact guide text was exact in 15 of 342 records. Later steps dropped the field.

17. **A reviewer gets the question, not the notes of the writer.**
    In the later review rounds the reviewer also received the notes of the editor.

18. **Each role has a saved definition with an enforced tool list.**
    No record shows an agent with a saved definition. Each limit on record was a sentence in a prompt.

## Lessons for the records

19. **Keep the prompts, the rules and the code in the repository.**
    The prompts and the generator code of the first build did not survive the session (F9).

20. **Keep a list of runs with the status of each run, in a place that survives the session.**
    The first build kept most of its state in a temporary workspace. The September review ran 82 agents with no list of runs. (Audit, theme "Run state and restart", 14 points.)

21. **Keep one source of data. Code makes each paper and each summary from it. Nobody edits an output file by hand.**
    For 23 questions the paper had an option text that was different from the question bank. The score table of the coverage matrix did not agree with its own rows.

22. **Write the record during the work.**
    The assistant made the record of the first build from files, weeks later. The assistant could not find many things.

## Lessons for how the assistant works

These three come from the session of 2 to 5 October 2026, not from the records of the first build.

23. **Do not mix what exists with what is only a plan on one page.**
    A portal page mixed work of August with a design of October. The owner rejected it.

24. **Do not show a design step as agreed if the owner did not agree to it.**
    The assistant started a review of task statement 1.1 with a pipeline sequence that nobody had agreed on. The owner stopped it.

25. **Say how many agents a job needs and how long you expect it to take, before you start it.**
    The audit used 11 agents and reached a usage limit. The owner did not expect the wait, and stopped the next agent.

## The failures F1 to F12 of the first build

| No. | Failure |
|---|---|
| F1 | One run had the status "complete". Its output file had 0 bytes. |
| F2 | The verdicts of 10 groups were one record too late. 10 rejected questions entered Mocks 1 and 2, and 10 entered with no verdict. |
| F3 | The format was in the prompt only. Field values did not follow the allowed lists. |
| F4 | A note with no link and no date made Mocks 1 to 4 single-answer only. |
| F5 | The first 40 questions had zero rejections, because the list of rules was not complete. |
| F6 | Stems grew to a median of 120 words in Mock 3. The guide samples have about 52. |
| F7 | A punctuation pattern marked the correct answer. A person found it, not the verifier. |
| F8 | The "needs review" flags did not predict which questions needed a correction. |
| F9 | Nobody kept the prompts and the generator code. |
| F10 | The digests were not in the design list of what a generator receives. |
| F11 | An append to the question bank joined two records and damaged the file. |
| F12 | A script for a second check of repeated scenes did not work. |

The full record with evidence is in `CCAR-F Mocks v2/reference/first-build/OLD PROCESS - exact steps.md`, in the folder next to this one.
