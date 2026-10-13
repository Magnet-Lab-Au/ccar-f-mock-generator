# 0026: A reader agent and word limits

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none
- Changes: adds a fourth agent to decisions 0012 and 0015, for each slice

## Question

All checks of decisions 0011, 0013 and 0015 test accuracy, agreement and layout. Nothing checks that a page suits the audience: senior engineers, directors of engineering and senior product managers, with little time. The time targets of decision 0004 (30 seconds for an Overview, 3 minutes for an Explanation) are never measured. How do we check this?

## Decision

1. Word limits, which a script counts:
   - Overview: at most 100 words, plus its figure
   - Explanation: at most 500 words
   - Depth: no limit

   A part over its limit goes to the owner. The owner decides whether to cut it or keep it.
2. A reader agent after each slice. It is a new agent, separate from the whole-picture agent of decision 0015. It gets only the pages and a description of the audience, as a participant sees them. It does not get the sources or the decisions. It reads the slice as a senior engineer with little time, and lists each part that is hard to follow.

   Before the review, the assistant writes one intended takeaway for each part. The reader agent does not see it. For each part, the reader agent:

   1. reads only the Overview, and writes the main point in one sentence. The assistant compares it with the intended takeaway. If they differ, the part is flagged.
   2. looks only at each figure, and says what it shows. If that differs from the caption, the figure is flagged.
   3. lists each term that the part uses before it explains it.
   4. lists each sentence that it had to read twice.
   5. says whether each closed heading tells it if the part is worth opening.
   6. lists any code that is in the text and not in a popup (decision 0004).

   Each item gives a quote from the page, so the agent cannot give only an opinion.

The owner's yes to this decision covers the reader agent for each slice (working rule 32).

## Reason

A script measures only length, not clarity. The assistant first suggested that the whole-picture agent also judges clarity. The owner said that this needs another agent. One agent with one task gives a clearer check, and a reader that sees no sources reads like a participant.

## How we decided

The independent review of the plan found that nothing checks the pages for the audience. The assistant recommended the word limits. The owner asked if an independent agent or the same agent does the check. The assistant said a script, and suggested a task for the whole-picture agent. The owner asked for another agent. The assistant then moved on too soon. The owner asked how the agent checks and what the requirements are. The assistant proposed the six requirements and the intended takeaway. The owner accepted them.

## Exam guide points

none.
