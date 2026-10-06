# 0035: The design of step 7: the marking file, the marks record and the numbers that stop a mock

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Diagram: `docs/diagrams/09-step-7-the-owner-marks-the-questions.html`

## Question

Decisions 0015, 0021 and 0022 say that the owner marks all 60 questions of mock 1 and 20 questions of each later mock, with no verdict in view, and that a bad mark sends the question to step 5. They left open what the owner gets, what the owner fills, and how many bad marks stop a mock. What is the design of step 7?

## Options

1. One proposal of the assistant with the exact file, the record and the numbers.
2. A different design.

## Decision

Option 1.

Two parts are different from decision 0015. Only a bad mark has a reason. And code shows the bad marks for each scenario and each domain. It does not compare the marks with the verdicts in this step.

1. **The marking file.** Code builds one Excel file for each round of marking. Example: `marking/M1-round1.xlsx`. It has one row for each question: the question ID, the scenario, the point that the question must test, the question, the line "Select N.", the options with their letters, the correct answer and the reason of each option. It shows no verdict of a checker.
2. **What the owner fills.** Two columns: "Mark" (`good` or `bad`) and "Reason". A bad mark must have a reason.
3. **Which questions.** Mock 1: all 60. A later mock: 20 questions, 5 from each scenario, with questions from each domain. Code selects them at random, with a seed (decisions 0015 and 0022).
4. **What code does with the file.** Code reads it. If a mark is missing, or a bad mark has no reason, code does not accept the file and names the rows. Code saves the marks as a record, for example `runs/mock-01/marks.json`. Each mark has the question ID, the mark, the reason, the round, the date and the fingerprint of the question record (decision 0036). Code shows the bad marks for each scenario and each domain.
5. **After a bad mark.** The question goes to step 5 with the reason of the owner as the finding. The finding has the rule `owner`, and the slot gets 3 new tries (decisions 0033 and 0037). The new question goes through steps 3, 4 and 6. The owner then gets a new marking file with only the new questions.
6. **What stops a mock.** Mock 1: more than 6 bad marks of 60. A later mock: 2 or more bad marks of 20. Then decision 0021 applies: the mock is not released, we correct the rules of the checker, and all 60 questions go through the checks again.
7. **The open findings of step 6.** The results "cannot decide" of step 6 are in the report of the run (decision 0034). The owner marks first, with no verdict in view. After code accepted the marking file, code shows these results with the questions that each one names. For each result the owner selects `ignore` or `rewrite`. A `rewrite` names one question and has a reason. That question goes to step 5. A `rewrite` does not count as a bad mark, because the owner saw a verdict of a checker before the decision. In a later mock, a result can name a question that the owner did not mark. Then the owner reads that question at this point. Code saves each action in `runs/mock-01/owner-decisions.json` (decision 0037, items 3 and 10).

The marking file is in the folder `marking/`, not in `runs/`. `README.md` says that no person writes in `runs/`.

### The contract of the step (decision 0018)

- It receives the question records of a mock that passed step 6.
- It returns the marks record.
- It can fail when the marking file is not complete. Then code does not accept the file and names the rows.

## Reason

- **A person marks a sample.** Decision 0015 has the reason (5.5-K2, 5.5-S1). The guide wrote those points for the extraction of data.
- **An Excel file.** Plain reason: the owner can read and fill it with no tool. The owner already fills a workbook in this folder.
- **The point of the slot is in the file.** Plain reason: the owner cannot judge if a question tests its point when the file does not show the point.
- **A bad mark must have a reason.** Decision 0015 says "with one reason". The reason is the finding for the writer of step 5 (decision 0021). A bad mark with no reason gives the writer nothing to change.
- **The bad marks for each scenario and each domain.** The guide wrote this point for the extraction of data: "The risk that aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields" (5.5-K1). One total can hide a bad part.
- **The two numbers that stop a mock.** They are guesses of the assistant. They have no source. Decision 0021 has the reason for a stop: many bad marks show that the checker is wrong, and in a sample more bad questions are probably in the part that the owner did not read.
- **The 60 marks of mock 1 are labels from a person.** Decision 0022 has this. With them we can test the checker.

Not decided yet:

- When the sample goes below 20. Decision 0022 says "only when the checker agrees with the marks of the owner". The owner and the assistant decide the number after mock 3, with real results.
- The exact columns of the Excel file, and the sequence of the questions in it.
- What "we correct the rules of the checker" means as a procedure.
- If the two numbers that stop a mock change after mock 1.
- If a bad mark of a later round counts for the number that stops a mock.

## How we decided

The assistant showed the proposal. The owner said yes. The assistant did not suggest a number for a smaller sample, and said why.

The folder `marking/` was not in the proposal that the owner saw. The assistant added it when it wrote this file, because of the rule of `README.md` for the folder `runs/`.

The owner approved the proposal in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

5.5-K1, 5.5-K2, 5.5-S1
