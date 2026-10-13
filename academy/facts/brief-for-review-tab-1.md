# The brief of a review agent for tab 1

The assistant gives this brief to each review agent of tab 1 (academy decisions 0011 and 0012). The agent did not write the parts. It gets no notes of the assistant.

## What to check

The page is `academy/pages/exam-guide-breakdown.html`. Its popups and preview cards are data in `academy/pages/exam-guide-breakdown.js`. The page is made by `academy/build/make-exam-guide-breakdown.py`. A part of a task statement N.M is `<details class="part" id="ts-N-M">`. Its fact sheet is `academy/facts/ts-N-M.md`. The sources are the files that the fact sheet and the cards name, mainly `reference/exam-guide.md` and the dated copies of the Anthropic documentation in `academy/sources/`.

For each part that the assistant names:

1. Each sentence of the part, each label of its figure and each popup: does its source support it? Each underlined fact has a preview card. Check that the card text holds the claim of the sentence, not only a near claim.
2. Each claim about a product (the Claude API, Claude Code, the Agent SDK) must come from the documentation, not from memory. Where the guide and the documentation differ, the part must show both and say which one the exam uses (decision 0014).
3. The figure: does it draw a mechanism that the sources describe? Does a label claim more than its source?
4. The conflicts of the fact sheet (section 9): does the part handle each one, or avoid the claim?
5. The text: Simplified Technical English, no semicolons, no em dashes, "the owner" and not a name. A term that the part uses before it explains it.
6. The links to tab 2: do they hold? Does the part say that the mock builder does something that it does not do?

## The output

A numbered list, most serious first. Each item: the part, a quote from the page, the source that you checked (file and line), what is wrong, and a fix in one sentence. Mark each item high, medium or low. End with the count and with what you did not check. Under 800 words.

## Rules

- Do not edit any file. Run no git command that changes the repository. Make no call to a model API.
- Do not open: `marking/*.xlsx`, the folder `claude-code-brand-kit/`, any conversation transcript, or a personal file of the owner (`responses.json`, the Study Edition, study notes, the progress tracker, the error log, the refresher, exam scores) (working rules 19 and 28).
