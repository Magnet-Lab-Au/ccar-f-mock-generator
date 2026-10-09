# Step 0: prepare the guide records

Status: built. It ran on 6 October 2026.

Diagram: [`03-step-0-prepare-the-guide-records.html`](../diagrams/03-step-0-prepare-the-guide-records.html)

## What the step does

Before the program plans a mock, a script copies the parts of the exam guide that the later steps need into one file, `reference/guide-records.json` (decision 0028). No model copies text. The file is the one source of guide text for the code. A later step takes a slice of it by ID.

The file has the version of the guide, 5 domains with their weights, 6 scenarios with their stories and primary domains, 30 task statements with their 240 points, 12 sample questions, and the three lists of Section 17.

Each point gets an ID that the guide does not have: the task statement, then K (knowledge) or S (skill), then the number of the bullet. Example: `1.4-K2` is the second bullet below "Knowledge of:" in task statement 1.4.

## The checks

- A second script checks the counts, and checks that each text in the file is exactly in the guide. It passed 41 of 41 checks.
- An independent reviewer checked the file and found no errors (`docs/reviews/review-guide-records.md`).
- The comparison of `reference/exam-guide.md` with the original, character for character, is not done.

If a count is wrong or a text is not exactly in the guide, the script writes no file and names the cause.

## The exam guide points that the step uses

Decision 0017 chose these points for step 0. Decision 0028 is the design of the step.

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 1.3-S2 | "Using structured data formats to separate content from metadata (source URLs, document names, page numbers) when passing context between agents to preserve attribution" | Task statement 1.3: Configure subagent invocation, context passing, and spawning | Written for agents that pass context to other agents. Here: each record keeps its ID, so each later step and each question keeps the link to its source. |
| 5.6-K1 | "How source attribution is lost during summarization steps when findings are compressed without preserving claim-source mappings" | Task statement 5.6: Preserve information provenance and handle uncertainty in multi-source synthesis | Written for the synthesis of findings. Here: the records keep the exact guide text, so no summary loses the source. |
| 5.6-K2 | "The importance of structured claim-source mappings that the synthesis agent must preserve and merge when combining findings" | Task statement 5.6: Preserve information provenance and handle uncertainty in multi-source synthesis | The same context. Here: the IDs of the points are the mapping between a question and the text of the guide. |
