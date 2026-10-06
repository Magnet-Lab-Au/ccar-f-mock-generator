# 0017: Step 0 of the pipeline: prepare the guide records

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

Where do the steps get the text of the guide, and is that work a step?

## Options

1. Step 0: checked record files of the guide, made one time for each version of the guide. It is in the numbered sequence.
2. Prework: the same work, documented, outside the numbered steps.
3. No separate work. Each step reads what it needs from the guide file.

## Decision

Option 1. Step 0 is "prepare the guide records". It makes checked record files of the guide in `reference/`. It runs one time for each version of the guide, not one time for each mock.

The records are:

- The 30 task statements and their 240 points with IDs. This part is done: `reference/task-statements-and-points.md`, made on 5 October 2026. An independent reviewer confirmed it against the exam guide copy.
- The 6 scenarios with their primary domains, the 5 domain weights, the 12 sample questions and the lists of Section 17. This part is not done. It will be one new file. An independent reviewer checks it against the guide, the same way.

No step lets a model copy guide text. Each step takes the text from these files by ID.

## Reason

The guide describes the method: "Using structured data formats to separate content from metadata (source URLs, document names, page numbers) when passing context between agents to preserve attribution" (1.3-S2), and the risk: "source attribution is lost during summarization steps when findings are compressed without preserving claim-source mappings" (5.6-K1, also 5.6-K2).

The guide does not cover this: that the records are made one time and checked character for character, and that no model copies guide text.

Not decided yet: the format of the new file, and if code or a person makes it. One open item of the handoff belongs here: no code compared `reference/exam-guide.md` with the original, character for character.

## How we decided

The assistant first suggested a step 0 in which code reads the complete guide into records. The owner said that the guide was already divided into task statements. That was correct for the 240 points. The assistant then suggested to call the work an input and not a step. The owner said that it must be documented in each case, because a goal of the build is a record that a portal page can show. So the work has a number, a decision file and a box in the diagram.

## Exam guide points

1.3-S2, 5.6-K1, 5.6-K2
