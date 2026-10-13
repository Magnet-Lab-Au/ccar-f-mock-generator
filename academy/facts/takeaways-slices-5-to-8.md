# Intended takeaways of slices 5 to 8 (academy decision 0026)

The reader agent does not see this file. The assistant compares the one-sentence summary of the reader agent with these takeaways. Each line is the heading of the part and the first sentence of its Overview.

## Domain 2

- **2.1 The description decides which tool Claude picks:** Claude chooses among tools mainly by their descriptions.
- **2.2 Errors must say what failed and whether a retry helps:** Mark a failed tool call with the error flag, and say the category, whether a new try can help, and what went wrong, so the agent can retry, fix its input, explain or escalate.
- **2.3 Give each agent only the tools that its role needs:** Each agent gets a small set of tools for its role, plus a narrow shared tool for a frequent need, and the coordinator handles the rest.
- **2.4 Share MCP servers in .mcp.json, with secrets in variables:** A team commits its shared MCP servers in .mcp.json and writes each token as an environment variable.
- **2.5 Grep finds content, Glob finds files, Edit needs unique text:** Search first: Glob finds files by name, Grep finds text inside files, and Read then follows only the files that matter.

## Domain 3

- **3.1 Team instructions live in the project CLAUDE.md, split into files:** Claude Code joins the CLAUDE.md files of the user, the project and its subdirectories, and only the project files reach teammates through git.
- **3.2 Share skills through the repository, and set how they run:** A command or a skill in the .claude/ folder of the project reaches the team through git.
- **3.3 A rule with a glob loads only for matching files:** A file in .claude/rules/ with a paths list of glob patterns loads into the context only when Claude edits a file that matches (the guide).
- **3.4 Plan first when the change is big or unclear:** In plan mode, Claude reads the code and proposes a plan, and in most sessions the edits wait until you approve it.
- **3.5 Refine with examples, failing tests and an interview:** When prose gives mixed results, show Claude 2 or 3 input and output examples, or write the tests first and let the failures drive the next try.
- **3.6 In CI, run claude -p with a schema and context:** In a pipeline, claude -p runs with no interaction, and --output-format json with --json-schema gives structured findings, which the guide posts as comments on the pull request (PR).

## Domain 4

- **4.1 Name what to report, not how careful to be:** A review prompt gets precise when it names the categories to report and to skip, and gives a code example for each severity level.
- **4.2 Few-shot examples fix what instructions alone leave inconsistent:** When detailed instructions still give inconsistent output, add 2 to 4 targeted examples that show the exact output format and the hard cases, each with the reason for the choice.
- **4.3 A schema guarantees the form, not the values:** Give Claude a JSON schema with structured outputs or a strict tool, and the output parses.
- **4.4 Retry with the exact errors, but not for missing facts:** When an extraction fails a check, send the document, the failed result and the specific errors back, so that the model can correct it.
- **4.5 Batch only the work that can wait a day:** The Message Batches API costs half, but a batch can take up to 24 hours with no promised time, so use it only for work that nobody waits for.
- **4.6 A new instance reviews each file, then the files together:** The session that wrote the work keeps its reasoning, so it is less likely to question its own choices.

## Domain 5

- **5.1 Pin exact facts outside the summary, and trim the rest:** A summary of a long conversation blurs numbers, dates and promises, so keep these facts in a separate block that each request carries word for word.
- **5.2 Escalate on explicit criteria, not on mood or confidence:** Write the escalation criteria and a few examples into the system prompt: a request for a human, a gap in the policy, and no progress.
- **5.3 A failed subagent reports what failed, never a silent empty:** A subagent retries a transient failure itself.
- **5.4 Keep findings in files, keep exploration in subagents:** A long exploration fills the context, and then the answers get worse.
- **5.5 Trust confidence scores only after labeled data calibrates them:** One total accuracy can hide a weak document type or field, so measure each segment before you cut human review.
- **5.6 Each claim keeps its source, date and conflicts:** Each subagent returns its findings as structured records: the claim, the excerpt, the source and the date.
