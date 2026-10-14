# The reader agent of decision 0026, domains 2 to 5 (14 October 2026, afternoon)

The reader agent got only the page `pages/exam-guide-breakdown.html`, its data file and screenshots of the figures, and the description of the audience. It did not see the sources, the decisions or `takeaways-slices-5-to-8.md`. This file copies the main parts of its report. The assistant compared point 1 with the intended takeaways in `takeaways-slices-5-to-8.md`.

## Point 1: the main point of each Overview, in one sentence

| Part | The sentence of the reader agent | Agrees with the intended takeaway |
|---|---|---|
| 2.1 | Claude picks a tool by its description, so each description must say its purpose, inputs, output and when to use it. Rename or split tools that overlap. | yes |
| 2.2 | Mark a failed call with the error flag, its category and whether a retry helps. An empty successful result is not an error. | yes |
| 2.3 | Give each agent only the tools of its role, plus a narrow shared tool. tool_choice has options, but current models reject two of them. | yes |
| 2.4 | Commit shared MCP servers in .mcp.json with tokens as variables, and keep personal servers in ~/.claude.json. | yes |
| 2.5 | Search first (Glob for file names, Grep for content), then Read only what matters. Edit needs text that occurs once. | yes |
| 3.1 | Claude Code joins the CLAUDE.md files of the user, the project and subdirectories. Only the project files reach teammates. | yes |
| 3.2 | Commands and skills in the project .claude/ reach the team, and those in ~/.claude/ stay personal. | yes |
| 3.3 | A rule file with a paths glob loads only for matching files, in every folder. | yes |
| 3.4 | Use plan mode for big, multi-file or unclear changes, and execute small, clear changes directly. | yes |
| 3.5 | When prose gives mixed results, give 2 or 3 input and output examples, write the tests first, and let Claude interview you in an unfamiliar domain. | yes |
| 3.6 | In CI, claude -p runs with no interaction, and a JSON schema gives findings that the guide posts as PR comments. | yes |
| 4.1 | Precision comes from naming the categories to report and to skip, with a code example for each severity, not from "be conservative". | yes |
| 4.2 | When instructions give inconsistent output, add 2 to 4 targeted examples, each with its reason. | yes |
| 4.3 | A schema (structured outputs or a strict tool) makes the output parse. Code still checks the values. | yes |
| 4.4 | When a check fails, send back the document, the failed result and the exact errors. A retry fixes format, not missing information. | yes |
| 4.5 | Batches cost half but take up to 24 hours, so use them only for work nobody waits for. | yes |
| 4.6 | The writer is biased, so give the review to a new instance with only the work and the criteria. Split a large review into passes. | yes |
| 5.1 | Keep exact facts in a block that each request carries word for word. Send the history, and trim tool results. | yes |
| 5.2 | Escalate on explicit criteria (a request for a human, a policy gap, no progress), not on sentiment or self-confidence. | yes |
| 5.3 | A subagent retries transient failures. If it cannot fix one, it returns the type, the query, the partial results and the alternatives. | yes |
| 5.4 | Long exploration degrades the answers. Use subagents and files of findings, and resume from the files. | yes |
| 5.5 | Measure accuracy for each segment before you cut human review. | yes |
| 5.6 | Subagents return claim, excerpt, source and date, and the synthesis keeps them and shows both values in a conflict. | yes |

## Point 2: figures that the reader agent flagged

- 2.2-1: the caption says "is not an access failure", and the figure says "Not an error". Not changed: both are true.
- 2.5-1: the caption says that the guide starts with Grep, and the figure said "Glob + Grep". Fixed: "Grep, then Read".
- 3.4-1: a box "Explore subagent" has no arrow, and the figure says "edits wait for approval (usually)". Not changed.
- 3.5-1: the note on 2 or 3 examples is not in the caption. Not changed.
- 4.3-1: the card note did not name the setting. Fixed.
- 4.5-1 and 5.5-1: the bars had no heading. Fixed.
- 4.6-1: the last two boxes were not explained. Fixed in the caption.
- 5.1-1: the arrow seems to come only from the summary. Not changed.
- 5.6-1: "a point of 5.3-S4" is cryptic. Fixed: "also in 5.3-S4".

## The two contradictions of wording (point 4), both fixed

- 2.2: "Its three categories do not include business errors" against "the four categories of errors are those of the guide".
- 5.2: "the agent escalates at once" against "it escalates only if the customer asks again for a human".

## Points for all parts

- Point IDs appear before "The guide's own text" explains them. Not changed (decision 0019).
- Field names were plain text. Fixed: code font by a step of the build (decision 0038).
- The label "Guide only" often follows a sentence about the documentation. Not changed. "How we broke it down" explains it.
- Some Depth sections use project words: "mock builder", "tab 2". The top of tab 1 explains the mock builder.

## The 5 parts that were hardest to follow

5.2, 2.2, 2.3, 4.3 and 4.6.
