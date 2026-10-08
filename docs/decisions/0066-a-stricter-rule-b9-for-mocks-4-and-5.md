# 0066: A stricter rule B9 for mocks 4 and 5

- Date: 9 October 2026
- Status: accepted
- Text confirmed by the owner: 9 October 2026
- Diagram: `docs/diagrams/11-repeats-across-mocks.html`. Diagram 06 (step 4) shows the new text of B9.

## Question

Decision 0062 says that rule B9 becomes stricter before mock 4. In mock 3, about 26 questions had the same problem and the same answer as an earlier question, in another setting, and B9 let them pass. What is the new text, and how does the owner know that it is fair?

## Options

1. A new text of B9 and of the writer instruction, with a test on mock 3 first.
2. The new text with no test.

## Decision

Option 1.

1. **The new text of rule B9:** "The question does not have the same problem as an earlier question on the same idea, also in another setting (another tool, team, product or data). The same problem means that the same thing goes wrong, or the team must make the same choice, so the same reasoning leads to the answer. A question on the same idea passes only with a different problem: for example the cause against the fix, a different failure, or a choice between two rules. Not the same set of wrong options as an earlier question on the same idea. At most one wrong option may repeat."
2. **The writer** gets the same rule in its own words: "Write a question with a different problem, also if you change the setting: a different thing goes wrong, or the team must make a different choice. For example the cause against the fix, a different failure, or a choice between two rules. The correct action may be the same, if the idea has only one. Do not use the same set of wrong options as an earlier question. At most one wrong option may repeat."
3. **A slot that fails B9 three times** opens for the owner, as before. The owner gives a new point or more tries.
4. **A test before mock 4:** call 4b checks the 60 built questions of mock 3 with the new text, against mocks 1 and 2 (`src/test_b9.py`, results in `runs/test-b9/results.json`). The owner sees 5 of the questions that the new rule fails, each with the earlier question and the reason, and decides if the rule is fair.
5. **Step 1 does not change.** It already takes first the ideas that the earlier mocks used least (decision 0050), and inside a group a point that they did not use (decision 0056).
6. **The exception for narrow ideas.** Some ideas have almost only one problem, for example "find text across many files, so use Grep" and "run the requested tool and send the result back". For an idea on the list `data/narrow-ideas.json`, the copy rule stays: "B9. The question is not a copy of an earlier question on the same idea: not the same scene with the same answer and the same set of wrong options. At most one wrong option may repeat." The writer gets: "This idea has almost only one problem, so the same problem and answer may come back. Use a different setting and scene. Do not use the same set of wrong options as an earlier question. At most one wrong option may repeat." The assistant drafted the list from the point groups (21 groups). The owner confirmed it on 9 October 2026, without G078 (custom_id): it has two problems, matching batch results and resubmitting only the failed requests, so it gets the stricter rule. The confirmed list has 20 groups:

| Group | The one problem |
|---|---|
| G001 | The loop stops too early or never stops: control it by stop_reason |
| G002 | The model repeats a step: the tool result is not sent back in the next request |
| G010 | The coordinator cannot start subagents: Task is not in allowedTools |
| G012 | Two approaches must start from one shared analysis: fork the session |
| G014 | Subagents run one after another: emit several Task calls in one response |
| G021 | Continue a named earlier session: --resume with its name |
| G027 | The agent does not see that a tool failed: set isError in the MCP result |
| G034 | Which MCP tools the agent has: all servers' tools, found at connection |
| G037 | Find text inside many files: Grep |
| G038 | Find files by name or extension: Glob |
| G039 | Edit fails on text that is not unique: Read, then Write |
| G044 | Each package needs its own standards file: @import in its CLAUDE.md |
| G046 | Which memory files are loaded: the /memory command |
| G047 | Share a command with the team: .claude/commands/ in the repository |
| G051 | A skill must not use some tools: allowed-tools in its frontmatter |
| G052 | A skill runs with a missing argument: argument-hint |
| G061 | Claude Code hangs in CI waiting for input: the -p flag |
| G062 | CI needs machine-readable output: --output-format json with --json-schema |
| G077 | A batch request needs tool calls in the middle: the Batch API cannot do that |
| G083 | Findings in the middle of a long input are missed: key findings first, with headers |


**The result of the test** (report: `docs/reviews/test-b9-mock-3.md`): the new B9 fails 24 of the 60 questions of mock 3. 12 of them the independent agent also named. 12 the agent did not name. 14 that the agent named pass the rule. The test cost $6.33, not $3 to $4. It agreed with the independent agent on 12. It also failed 12 that the agent did not call the same problem, and passed 14 that the agent did. So the rule is a judgment, and it will sometimes fail a good question or pass a close one.

This changes item 4 of decision 0060 ("Rule B9 does not change") from mock 4, as decision 0062 says.

## Reason

Plain reason: a participant who meets the same problem in a new setting meets the same question. The first text of B9 let a new setting count as a new scene.

The owner changed the first suggestion of the assistant: "No wrong option of an earlier question" became "Not the same set of wrong options. At most one wrong option may repeat." The reason of the owner: the standard mistakes that the guide names make the strongest wrong options, and the owner wants harder questions in mocks 4 and 5.

The cost of mock 4: mocks 2 and 3 cost about $0.23 for each written try, with all its checks and step 6. Mock 3 had 101 tries for 60 slots. With the stricter rule, the assistant expects about 130 to 160 tries and some open slots, so about $32 to $40. This is an estimate of the assistant. It is not measured. The owner accepted this estimate.

## How we decided

The assistant suggested the text, the test and the cost. The owner agreed with three changes: the rule on the wrong options, a check that the preference for unused groups is built (it is), and 5 failed questions from the test for the owner to judge. After the test, the owner decided: use the stricter B9 for mock 4, with the exception for narrow ideas. The stricter rule was proposed by Claude Code. The change to the wrong options and the exception for narrow ideas came from the second review in Cowork. The owner decided each one.

The owner confirmed the text of this file on 9 October 2026, with the two additions above. No independent reviewer checked this file.

## Exam guide points

none
