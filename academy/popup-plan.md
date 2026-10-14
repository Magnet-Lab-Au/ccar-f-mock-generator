# Popup plan for the figures

- Date: 14 October 2026
- Status: proposed. The owner checks it before any popup is built.
- Source: two drafts by agents, one for each tab, with the five rules below. The assistant merged them and kept only the popups that answer the first question a reader has about a box.

## Why popups

A figure shows the shape of an idea at a glance. A reader who wants more about one box gets it there, on demand, without a long text and without leaving the figure. The overview stays clean, and the detail waits for the reader who asks for it. Fig. 1.1-1 already works this way. The other figures lost their box popups at night, with no decision (the owner's question, 14 October 2026).

## The five rules (accepted by the owner)

1. A box gets a popup only if it raises a question that the figure and its caption do not answer.
2. Each popup answers that one question, in 1 to 3 short sentences (about 50 words at most), with the guide point that it shows.
3. A popup never repeats the caption or the text of the part.
4. Every sentence comes from the fact sheet of the part, so that a review agent can check it.
5. One design for all, as in 1.1. Code or an example only when it shows something that words cannot.

## How the plan chose

The two drafts had 140 popups. The assistant kept a popup only when it answers the first question that a reader has about that box: what it is, what it gets, what it does or what it returns. It dropped side questions, popups that the caption or the label already answers, and popups on a line instead of a box. The list of the dropped ones is at the end.

## Totals

| | Figures with popups | New popups |
|---|---|---|
| Tab 1 | 27 of 34 | 54 |
| Tab 2 | 13 of 22 | 41 |
| All | 40 of 56 | 95 |

Fig. 1.1-1 keeps its 6 popups. Bars, waffles, tables and most cards get none.

## Points for the owner

- Part 1.1 has no fact sheet. Its 7 popups (Figs. 1.1-2 and 1.1-3) cite the dated copies in `academy/sources/` directly. The assistant suggests that this is acceptable, because a review agent can check those copies in the same way.
- Some popups say "the documentation". At build time each one takes its name: the Claude API documentation or the Claude Code documentation (academy decision 0039, item 11).
- Boxes that repeat one idea share one popup: Subagents A to C in 1.3, the file passes in 1.6, the two "before" tools in 2.1.
- The text of each popup is a draft. When the assistant builds them, a review agent checks each one against its source, domain by domain, as for the figures.

## The popups, figure by figure

## Tab 1, Exam guide breakdown

### Fig. A (top, a map of the 5 domains with links)
No popup. Each task statement is a link to its part, and each weight opens its card of the guide.

### Fig. B (top, a table of the 6 scenarios)
No popup. Each scenario name already opens a card with the full text of the scenario (cards `m-s1` to `m-s6`).

### Fig. 1.1-1 (part 1.1, a stepper of the loop)

### Fig. 1.1-2 (part 1.1, four cards: three anti-patterns and the correct check)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Stops mainly at a count | So is a limit of turns wrong? | The guide rejects a limit only as the main way to stop. The Agent SDK has max_turns as a safety limit: its example sets max_turns=30 to "prevent runaway sessions". | 1.1-S3 | GUIDE 127. `academy/sources/2026-10-14-claude-code-docs-agent-sdk-agent-loop.md` 46, 395 (no fact sheet, see point 1) |
| Looks for text | Why does text not mean that the work is done? | A response can hold text blocks before its tool_use block. So text can come while Claude still asks for a tool. | 1.1-S3 | `academy/sources/2026-10-14-anthropic-docs-build-a-tool-using-agent.md` 81 (no fact sheet, see point 1) |

No popup: Reads the words, Checks the field (the line under each card answers it).

### Fig. 1.1-3 (part 1.1, a grid of the 7 stop_reason values)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| "max_tokens" | What does it mean, and what do I do? | The response reached your max_tokens limit. Raise max_tokens, or continue the response. | 1.1-K1 (beyond the guide) | `academy/sources/2026-10-14-anthropic-docs-handling-stop-reasons.md` 16 |
| "stop_sequence" | Same | Claude wrote one of your stop sequences. Read the field stop_sequence to see which one. | 1.1-K1 (beyond the guide) | same copy, 17 |
| "pause_turn" | Same | A loop of server tools reached its limit of iterations. Send the assistant content back to continue. | 1.1-K1 (beyond the guide) | same copy, 19 |
| "refusal" | Same | Claude declined to respond. Read stop_details, and retry on a fallback model. | 1.1-K1 (beyond the guide) | same copy, 20 |
| "model_context_window_exceeded" | Same | The response filled the context window of the model. Treat the response as cut off. | 1.1-K1 (beyond the guide) | same copy, 21 |

No popup: "end_turn", "tool_use" (Fig. 1.1-1 and the Overview explain them).

### Fig. 1.2-1 (part 1.2, a hub and spoke stepper)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Coordinator | How does it choose a subagent, and what does it pass on? | It decides from the task and from the description of each subagent. It passes the results of one subagent to the next, for example the findings of the search to the synthesis. | 1.2-K3, 1.2-S1 | ts-1-2 F7, F12 |
| Web search | What does it get, do and return? | It gets only the prompt of its task, with its own subtopic or source type. It searches the web. Its tool calls stay inside it, and only its final message returns. | 1.2-K2, 1.2-S2 | ts-1-2 F5, F1, F4, GUIDE 144 |
| Document analysis | What does it get, do and return? | It gets only its task prompt, not the system prompt of the coordinator. It analyzes documents. When the synthesis has a gap, it gets a targeted query. | 1.2-K2, 1.2-S3 | ts-1-2 F6, F1, GUIDE 145 |
| Synthesis | What does it get, do and return? | It gets the findings of the search and the analysis, which the coordinator passes on. It joins them. Its output goes back to the coordinator, not straight to the report subagent. | 1.2-K1, 1.2-K3 | ts-1-2 F12, F1, GUIDE 133 |
| Report | What does it get, do and return? | It gets the synthesis through the coordinator. It writes the report: in scenario 3, the system produces comprehensive, cited reports. | 1.2-K1 | ts-1-2 F12, F1 (GUIDE 85) |

No popup: the arrows "task prompt", "result", "no direct path" and "gaps? targeted queries again" (the caption and the Explanation answer them).

### Fig. 1.3-1 (part 1.3, a stepper of one coordinator and three subagents)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| findings + sources (arrow) | What does such a prompt look like? | Put each document in document tags, with the text in document_content and the metadata in source. Example below. | 1.3-S2 | ts-1-3 F16 |
| Task calls (arrow) | Why several calls in one response? | Subagents can run at the same time. Independent subtasks then finish in the time of the slowest one, not of all together. | 1.3-S3 | ts-1-3 F15 |



No popup: Coordinator "allowedTools has Task" (the Explanation covers it in full), "only the final message of each comes back" (the caption says it).

### Fig. 1.4-1 (part 1.4, three cards: allowed, denied, escalation)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| deny + reason to the agent | What exactly goes back? | The hook returns permissionDecision "deny" and a permissionDecisionReason. The reason tells the model why, so that it does not retry the same call. If any hook denies, the call stops, whatever the other hooks return. | 1.4-S1 | ts-1-4 F6, F5 |
| escalate_to_human | What makes the agent escalate here? | In the guide exercise, a hook enforces a business rule, such as a limit on the amount, and redirects to an escalation workflow when the rule triggers. escalate_to_human is a tool of scenario 1. | 1.4-K3 | ts-1-4 F12, GUIDE 71 |

No popup: Agent, "your state: ID returned?", process_refund runs, handoff summary (the card lines and the Explanation answer them).

### Fig. 1.5-1 (part 1.5, a stepper of two hooks around one tool call)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| PreToolUse, your code | What can the hook answer? | It sets permissionDecision to allow, deny, ask or defer. It can also change the input of the call with updatedInput. | 1.5-K2 | ts-1-5 F8 |

No popup: Claude asks for a tool, the labels Unix time and ISO 8601 (the example values in the fact sheet have no source).

### Fig. 1.6-1 (part 1.6, two flows side by side)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| File 1, 2, N, local pass (one key) | What goes wrong in one pass over all files? | In sample question 12, one pass over 14 files gave detailed feedback on some files and superficial comments on others. Separate files can be analyzed at the same time. | 1.6-S2 | GUIDE 888, ts-1-6 F8 |
| Integration pass, across the files | What does it look at? | It examines the data flow across the files, which no pass of one file can see. The Claude Code documentation gives all the findings to one agent that ranks them and removes duplicates. | 1.6-K2 | GUIDE 890, 900, ts-1-6 F7 |
| Map the structure | Why map before the plan? | Without a map, the work can solve the wrong problem. For tests, the Claude Code recipe starts by finding the code that has no tests. | 1.6-S3 | ts-1-6 F13, F14 |

No popup: High-impact areas, Prioritized plan (their names say it).

### Fig. 1.7-1 (part 1.7, three cards: resume, fork, fresh start)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| New session, fresh context + summary | What goes into the summary? | Capture what you need, such as the analysis output, the decisions and the file diffs. Put it into the prompt of the new session. | 1.7-K4, 1.7-S3 | ts-1-7 F10 |

No popup: "same ID + the changed files", "results stale" (the caption and the Explanation answer them).

### Fig. 2.1-1 (part 2.1, before and after)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| analyze_content and analyze_document, before (one key) | Why does Claude pick the wrong one? | Both say only "analyzes content", so Claude has nothing to tell them apart. The documentation names two more causes of a wrong choice: a collision of tool names, and a schema that is too generic. | 2.1-K3 | GUIDE 764, ts-2-1 F8 |
| extract_web_results, after | What makes a description web-specific? | It also says what the tool does not do. The good example of the documentation ends: "It will not provide any other information about the stock or company." | 2.1-K2 | ts-2-1 F6, GUIDE 236 |

No popup: the request "Get the results of this web page" (the figure shows it).

### Fig. 2.2-1 (part 2.2, five cards: one success and four categories of error)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Not an error, a valid empty result | What does it look like? | A normal tool result, with no error flag. The Claude API documentation shows a tool_result with no content and no is_error. | 2.2-S4 | ts-2-2 section 6 (HANDLE 141-151) |
| Business, explain it | What does the agent say? | Claude reads the error and explains the limit. In the tutorial of the documentation, it answers that "the calendar only allows 10 attendees per event", and offers two ways forward. | 2.2-S2 | ts-2-2 F9 (TUT 2932, 4011) |

No popup: Transient, Validation, Permission (the card lines and the Explanation answer them).

### Fig. 2.3-1 (part 2.3, the tools of each agent)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| verify_fact | What problem does it solve, and why not all web tools? | Before, each check went back through the coordinator: 2 or 3 round trips for each task, and 40% more latency. verify_fact covers the simple checks of dates, names and statistics. All web search tools would over-provision the synthesis agent. | 2.3-S3 | GUIDE 848, 858 |

No popup: Coordinator, Web search, Document analysis load_document, Synthesis, Report, the split bar (the caption and the Explanation answer them).

### Fig. 2.4-1 (part 2.4, where MCP servers are set and what the agent gets)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| The agent, tools of all servers | All servers, always? | Only the connected ones. The tools of a server that has not connected yet are absent. | 2.4-K3 | ts-2-4 F10 |
| Resources | How does a resource reach the agent? | In Claude Code, a user can name a resource with @, as for a file. Claude Code then fetches it and adds it as an attachment, with no tool call by Claude. | 2.4-K4, 2.4-S5 | ts-2-4 F12, F14 |

No popup: .mcp.json, ~/.claude.json, Claude Code connects to each (the caption and the Explanation answer them).

### Fig. 2.5-1 (part 2.5, two cards: read all first, Grep then Read)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Grep, then Read | What does Grep return? | By default, only the paths of the matching files, not the lines. It can limit a search to a file pattern such as **/*.tsx, or to a language such as py. | 2.5-K1, 2.5-S1 | ts-2-5 F2, F3 |

No popup: Read every file first, the context bars (the card lines answer them).

### Fig. 3.1-1 (part 3.1, the levels of CLAUDE.md)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Context of the session | In what order, and what if two files disagree? | The files join in load order, from broad to specific, so a project instruction comes after a user instruction. If two files give different guidance for the same behavior, Claude may choose either one. | 3.1-K1, 3.1-S4 | ts-3-1 F1, F18 |
| .claude/rules/*.md | When does a rule file load? | A rule file with no paths field loads at launch, with the same priority as .claude/CLAUDE.md. Claude Code finds each .md file in the folder, also in its subfolders. | 3.1-K4 | ts-3-1 F13, F12 |

No popup: ~/.claude/CLAUDE.md, ./CLAUDE.md, /memory and /context (the caption and the Explanation answer them).

### Fig. 3.2-1 (part 3.2, before and after: a skill without and with context: fork)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| The skill, the body of SKILL.md (without fork) | Does the body stay in the context? | Yes. The content of SKILL.md enters the conversation as one message and stays there in later turns. Claude Code does not read the skill file again. | 3.2-K3 | ts-3-2 section 6 (SK 590) |
| no conversation history | Is context: fork a fork of the conversation? | No. Despite its name, a skill with context: fork does not run in a fork of the current conversation. | 3.2-K3 | ts-3-2 F11 |

No popup: Main conversation, "only a summary returns" (the caption says it).

### Fig. 3.3-1 (part 3.3, one rule with a glob against a directory CLAUDE.md)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|

No popup: the file names, "no match", Context, src/ui/CLAUDE.md (the figure, the caption and the Explanation answer them).

### Fig. 3.4-1 (part 3.4, a decision and two paths)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Explore, read, no edits | What can Claude do here, and how do I start it? | Claude reads files and runs shell commands to explore. You enter plan mode with Shift+Tab, or with /plan in front of one prompt. | 3.4-K3, 3.4-K1 | ts-3-4 F4, F11 |
| Approve, you decide | What happens when I approve? | Plan mode ends. The session changes to the permission mode that the chosen approve option names, and Claude starts to edit. | 3.4-S4 | ts-3-4 F10 |

No popup: A change, Big or unclear?, Plan, Direct execution (the Explanation answers them).

### Fig. 3.5-1 (part 3.5, a stepper of the test-driven loop)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| 2 or 3 input and output examples | What makes a good example? | Make the examples diverse. Cover edge cases, and vary them enough that Claude does not copy a pattern that you did not intend. | 3.5-S1 | ts-3-5 F2 |
| Interview | How does Claude ask? | With the tool AskUserQuestion. It asks multiple-choice questions, and by default each question stays open until you answer. | 3.5-K3 | ts-3-5 F12 |
| Write tests, before the code | What does a test case in a prompt look like? | Give example inputs and their expected outputs as test cases in the prompt. Example below. | 3.5-S4 | ts-3-5 F4 |
| Run the tests | Why must Claude run them? | Without a check that Claude can run, "looks done" is the only signal, and you become the verification loop. | 3.5-K2 | ts-3-5 F7 |


No popup: Claude implements, Done, the labels "interacting" and "independent" (the caption answers them).

### Fig. 3.6-1 (part 3.6, a stepper of Claude Code in a CI pipeline)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|

No popup: PR or new commit, JSON fits --json-schema, Inline PR comments, Existing tests, CLAUDE.md not with --bare (the caption and the Explanation answer them).

### Fig. 4.1-1 (part 4.1, before and after: filter on confidence, explicit criteria)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Explicit criteria, report bugs, skip style | What does an explicit criterion look like? | It can ask for evidence. An example from Code Review: "behavior claims need a file:line citation in the source, not an inference from naming". | 4.1-K1 | ts-4-1 F3 |
| Severity, code examples | Which levels? | Code Review uses three: Important (a bug to fix before the merge), Nit (a minor issue that does not block) and Pre-existing (a bug that the PR did not add). | 4.1-S3 | ts-4-1 F11 |
| A noisy category? | How do I know that a category is noisy? | In Code Review, developers mark each finding as useful, or as wrong or noisy. Anthropic uses the counts to tune the reviewer. | 4.1-K3 | ts-4-1 F7 |

No popup: Candidate findings, Posted findings, Filter on confidence (the Explanation answers them).

### Fig. 4.2-1 (part 4.2, the parts of a few-shot prompt)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| reason: why this choice | How do I write the reason? | With thinking on, give each example as a problem, the method to apply and the expected answer. Claude then uses that method in its own thinking for similar problems. | 4.2-S1 | ts-4-2 F6 |

No popup: Instructions, input, output, Claude, New input, Consistent output (the caption and the Explanation answer them).

### Fig. 4.3-1 (part 4.3, three cards of tool_choice and the check after the call)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| one tool, Claude picks which (card any) | What do I use on the models that reject it? | On models that accept it, any with strict tools guarantees both a call and a valid input. On the four models that reject it, use auto with strict tool use, or structured outputs. | 4.3-S2 | ts-4-3 F11, F10 |
| Code checks the values | Which values can the schema not check? | A strict schema cannot hold rules on numbers, such as minimum, maximum or multipleOf. Compare enum values without regard to case. | 4.3-K3 | ts-4-3 F13, F16 |

No popup: the auto card, the forced card, tool_use input (the card lines and the Explanation answer them).

### Fig. 4.4-1 (part 4.4, three cards: pass, retry, stop)
No popup. Each card line, the caption and the Explanation answer the question of each box. The facts that remain are in the Depth or in the popups of 4.3.

### Fig. 4.5-1 (part 4.5, a flow and a bar of the price)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Failed only, fixed if needed | Which failures need a fix? | An invalid request must be fixed first. A request with a server error can go again as it is. A batch cannot change after you submit it, so the failed requests go in a new batch. | 4.5-S3 | ts-4-5 section 6 (BATCH 768-771), F15 |

No popup: Does anybody wait?, Messages API, Message Batches, Results, Use, the price bars (the caption and the Explanation answer them).

### Fig. 4.6-1 (part 4.6, two cards and a row of passes)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| new reviewer, code and criteria only | How do I get a new instance? | In the Claude API, each new call is one: the Messages API is stateless and sees only what you send. In Claude Code, a subagent starts with a fresh, isolated context. | 4.6-S1 | ts-4-6 F7, F6 |
| Verification, confidence each | Why a separate pass? | The review first reports every finding, and a separate pass filters them. A prompt that says "be conservative" can make the model report less. | 4.6-S3 | ts-4-6 F15 |

No popup: Writer, the file passes, Integration pass, Route (the caption, the Explanation and Fig. 1.6-1 answer them).

### Fig. 5.1-1 (part 5.1, the stack of one request and a bar)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Case facts | In what form? | Keep them in a structured format, such as JSON, as the documentation advises for state data. In Claude Code, the project CLAUDE.md does this job: Claude reads it again from disk after /compact. | 5.1-S1 | ts-5-1 F6, F5 |
| keep 5 (the filter) | Where does the cut happen? | In the Agent SDK, a PostToolUse hook can make the cut: updatedToolOutput replaces the tool output before Claude sees it. | 5.1-S3 | ts-5-1 F15 |

No popup: System prompt, Summary of older turns, Recent turns, Claude, the bar (the caption, the Explanation and the Depth answer them).

### Fig. 5.2-1 (part 5.2, five cards: three triggers and two non-triggers)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| The agent, low confidence of its own | Why not escalate on low confidence? | In sample question 3, the agent is already wrongly confident on hard cases. So a limit on its own confidence does not catch them. | 5.2-K3 | GUIDE 776 |

No popup: Asks for a human, No progress, escalate_to_human (the card lines and the Explanation answer them).

### Fig. 5.3-1 (part 5.3, three cards and the path after a failure)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| Synthesis, gaps marked | How is a gap marked? | Name each source or topic that the run could not cover. An example prompt of Managed Agents: if an agent fails to read a contract, list that contract as not covered. | 5.3-S4 | ts-5-3 F9 |

No popup: Results, No matches, the access failure card, Coordinator (the card lines and the Overview answer them).

### Fig. 5.4-1 (part 5.4, four cards)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| scratchpad file, key findings | Why a file and not the conversation? | A file on disk survives a compaction. The conversation history may not. The memory tool prompt tells the agent to assume that its context can reset at any moment. | 5.4-K2 | ts-5-4 F6, F5 |

No popup: subagent test files, manifest (no source says what a manifest holds), the context.

### Fig. 5.5-1 (part 5.5, a routing flow and a bar of 97%)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|

No popup: Extraction, Review thresholds, Labeled set, Human review, Automated, the bar (the Explanation and the Depth answer them. No source defines "stratified").

### Fig. 5.6-1 (part 5.6, a finding from the subagents to the report)
| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point | Source |
|---|---|---|---|---|
| source URL or document name | What can the source be? | Any stable string: a URL, or an internal identifier such as kb://article-1234. | 5.6-S1 | ts-5-6 F7 |

No popup: claim, evidence excerpt, publication date, Synthesis, Report sections (the caption and the Explanation answer them).






## Tab 2, Behind the mocks

### Fig. A (top of the tab, a stepper of the 9 steps)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| open slot (waits for owner) | Does a slot open only after 3 tries? | A slot also opens after 2 results "cannot decide" of step 4 in one start, or at once when the writer answers "cannot write". Neither happened in the 5 mocks: each opening came after 3 failed tries. | Mock decisions 0023 and 0033 | top-of-tab-2.md L4, N5, step-5.md T2 |

No popup: the 9 step boxes (each one links to its step), the legend (it explains itself).

### Fig. 0-1 (step 0, a flow of the script and its checks)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| exam guide (the copy, .md) | Which parts of the guide does the script read? | The script reads five sections of the guide: 4 (domains), 5 (scenarios), 6 (task statements), 9 (sample questions) and 17 (the lists of technologies and topics). The records leave out the other sections. | Mock decision 0028 | step-0.md E5, E45 |
| steps (1, 2, 4, 5, 7, 8) | Does each step get the same part? | No model call reads the file. Code takes a slice by ID: the writer gets its scenario and its own task statement, but step 4 gets all 30 task statements, the same text in each call, so that it can be cached. | Mock decisions 0028 and 0067 | step-0.md E33, E34, E41, X4 |
| second script (41 of 41 checks) | What does it check that the script of step 0 does not? | It also checks the other direction: the 240 bullets of Section 6 of the guide are the 240 points, in the same sequence. It compares the points with the older file for people too. No test in `tests/` covers step 0, so this script is its only automatic check. | Mock decision 0028 | step-0.md E23, E24, E47 |

No popup: none left. Each box raises a question that the caption and the text do not answer.

### Fig. 1-1 (step 1, inputs, the rules box and the plan, with a small bar chart)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| ideas (95 groups of points) | What does one idea look like? | Example: idea G003, "Fixed sequence against a plan that adapts", holds the points 1.1-K3, 1.6-K1, 1.6-K3, 1.6-S1 and 1.6-S3. Of the 95 ideas, 65 have 2 or more points and 30 have 1. | Mock decision 0047 | step-1.md section 3 (last bullet), R13 |
| earlier mocks (built only) | Which mocks count, and what does code read? | Code counts how often each idea came in each built mock with a lower number. A mock counts only when its file `mocks/mock-NN.questions.json` exists. So the plan of mock 1 had no earlier mocks. | Mock decision 0050 | step-1.md R14, R15, section 4.2 (`earlier_mocks`) |
| a seed (a number) | Does the same seed always give the same plan? | The seed controls each random choice. The code uses only `random()` of Python, because Python guarantees its sequence for the same seed. But with today's code the seed of mock 2 no longer gives its plan, because a later rule changed the order of the points. | Mock decision 0056 | step-1.md R21, R22, C2, C-10 |
| the plan (60 slots) | What is in one slot? | Each slot is one record in `plan.json`. Code writes the plan once and never writes over it. A new point of the owner does not change it. Example below. | Mock decision 0027 | step-1.md E2, E3, E15, E11 |


No popup: guide records (the caption and the text say what step 1 takes), rule lines 1, 3, 4 and 5 (the text and the Depth explain them), the bar chart.

### Fig. 1-2 (step 1, two cards: dynamic decomposition against a fixed sequence)

No popup. Two cards with one contrast. The caption names 1.6-K1, and the chip of task statement 1.6 below gives the guide texts.

### Fig. 1-3 (step 1, bar chart)

No popup. A bar chart with its numbers. The caption explains it.

### Fig. 2-1 (step 2, the request built by code, the call and the form)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| row "3 sample questions of the guide" | Which samples, and in which form? | The 3 samples come from scenarios other than the scenario of the slot, so that the writer does not copy the scene of an example. Code removes their letters and their explanations. So they do not show the whole form: an option has no reason. | 4.2-K1, 4.2-S2 | step-2.md R5, D5, X1, section 3 |
| row "the slot: type, options, answers" | Does the writer see the correct letters? | The writer sees the scenario, the task statement, the point, the type, the number of options and answers, and if the longest option may be correct. It does not see the letters that the plan sets from mock 5, so the model never chooses a letter. | Mock decision 0070 | step-2.md R9, L5 |
| row "if any: earlier questions on the idea" | How many earlier questions, and with what instruction? | For most ideas, from mock 4, the writer is told: "Write a question with a different problem, also if you change the setting". In mock 5, each of the 101 tries got earlier questions: 2.88 on average, 7 at most. | Mock decisions 0056 and 0066 | step-2.md R10, A12, A14, section 4.2 |
| the form (question, options) | What exactly does the writer fill? | Code adds `"additionalProperties": false` to each object before it sends the schema, because the documentation of structured outputs requires it. The form stops format errors, not content errors, so step 3 checks the content. Example below. | 4.3-K3, mock decision 0040 | step-2.md F1, F2, section 3 (4.3-K3) |


No popup: rows "the rules" (the text covers the cached block and the 21 rules), "the role and the form" (the box "the form" covers it), "the story of the scenario" (trivial), "the 14 technologies" (no source gives a reason), "step 5: the failed try and its findings" (step 5 explains it).

### Fig. 3-1 (step 3, a box of 12 rule cells, two exits, small bars)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| A5 "no 'Option B'" | Which words, and why? | No text and no reason may name a letter or another option, for example "Option B", "all of the above" or "both A and C". Code gives the letters after the writer, so such words could become wrong. | Mock decision 0029 | step-3.md rule table A5, step-0.md R6 |
| A6 "word limits" | Which limits, and from where? | A question has 25 to 110 words, and an option 5 to 45. The limits are the range of the 12 sample questions of the guide, with a margin that the assistant chose with no source. | Mock decision 0031 | step-3.md rule table A6, R3 |
| A7 "not much longer" | How much longer? | The correct options may have at most 1.3 times the average words of the wrong options. The largest ratio in the 12 sample questions of the guide is 1.21, and in the 488 tries 1.29. | Mock decision 0031 | step-3.md rule table A7, R4, section 4.2 (note) |
| A9 "2 to 5 sentences" | How does code count a sentence? | Code ends a sentence at ".", "?" or "!" and a space. So M5-S43-T1 failed with 6 sentences: "9 a.m." ended a sentence. The next try wrote "09:00" and passed. | Mock decision 0031 | step-3.md R1, d2, d3, d4 |
| step 5 (with the findings) | What does a finding look like? | Each finding names the rule, the detail and, where it fits, the letter. Example from M2-S02-T1: "The longest option is a correct option (191 characters). The slot needs a wrong option that is longer than each correct option." Each of the 11 tries that failed step 3 passed it at the next try. | Mock decision 0031 | step-3.md E7, section 4.3, section 4.2 (note) |

No popup: A2, A3 and A12 (the text and the Depth explain them), A4, A8 and A10 (trivial), step 4 (it has its own part), the small bars.

### Fig. 3-2 (step 3, bar chart)

No popup. A bar chart with its numbers and the chance line. The caption explains it.

### Fig. 4-1 (step 4, a stepper of the two calls and the verdict)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| call 4a (no answer key) | What does call 4a see? | Call 4a gets the guide, the story and the question with its options, but no marks and no reasons. It answers as a candidate does. That a checker who sees the marks tends to agree with them is an assumption of the assistant, not checked. | Mock decision 0032 | step-4.md A1, A2, A3, A7 |
| call 4b (9 rules, the key) | What does call 4b give back? | Call 4b gives one result for each rule B1 to B9: pass, fail or cannot decide, with a finding for each result that is not a pass. It also gets the 12 sample questions of the guide for rule B8, and the earlier questions on the same idea for rule B9. | 4.1-K1 | step-4.md B1, B2, B3, B5, section 3 (4.1-K1) |
| code (makes the verdict) | When is it a fail? | A fail: the letters of call 4a differ from the marks, a rule fails, or code does not find a feature name in the guide records. If not, "cannot decide" when call 4a or a rule cannot decide. If not, a pass. | Mock decision 0032 | step-4.md V3 |
| fail or cannot decide (to step 5) | Why a result "cannot decide"? | "Cannot decide" is a value of the form, so the checker does not have to guess. No check of mocks 1 to 5 gave it: 0 of 477. | 4.3-S5 | step-4.md section 3 (4.3-S5), X3 |

No popup: question (passed step 3) and pass (slot passed), both trivial.

### Fig. 4-2 (step 4, bar chart)

No popup. A bar chart with its numbers. The caption explains it.

### Fig. 4-3 (step 4, bar chart of the cost)

No popup. A bar chart with its numbers and a legend line.

### Fig. 5-1 (step 5, a stepper of the loop of one slot)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| new request of step 5 | What does the writer read? | The request tells the writer: "Correct each finding. The letters are the letters that the checker saw." After a bad mark, a rewrite or "more tries", each try of the new start also gets the reason of the owner, as a finding with the rule "owner". | 4.4-K1, mock decision 0080 | step-5.md E2, E10, E11, `src/control.py`, lines 236-242 |
| dimension line "at most 3 tries in one start" | Why 3? | The number 3 is a guess of the assistant: the guide gives no number. A limit exists because, with no limit, a slot that cannot pass makes the program try with no end. | 1.1-S3, mock decision 0033 | step-5.md L1, L15, L16, section 3 (1.1-S3) |

No popup: Writer (Fig. A and the text say that it is the writer of step 2), Step 3 (it has its own part), passed (trivial).

### Fig. 5-2 (step 5, grids of squares, one for each slot)

No popup. Each square already has a native tooltip with its slot and its tries.

### Fig. 5-3 (step 5, three boxes of the review loop)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| the rules are code (with tests) | How can a test run with no model call? | A fake writer and fake checkers give the answers that each test tells them to give. Each case is one test, and the 10 cases of the second review were the first tests. | Mock decision 0038 | step-5.md A8 |

No popup: none left.

### Fig. 5-4 (step 5, a stepper of the tries of slot M5-S38)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| Try 1 (fails B9) | Which earlier question did it repeat? | Try 1 had the same problem as M3-S12-T1 of mock 3: it resubmits the failed requests of a batch. The point of the slot is 4.5-S3. | 4.5-S3 | step-5.md B12, B2 |
| dimension line "a new start" | What does a new start change? | A new start gives the slot 3 new tries, and the count of "cannot decide" starts at zero. The try numbers continue, so the new start begins at try 4. | Mock decision 0033 | step-5.md L8 |

No popup: Try 4 and Try 5 (each opens a card already), Try 2 (the Depth tells it), Try 3 (the same finding as Try 1), the label line of B9 (it explains itself).

### Fig. 6-1 (step 6, a flow of code, two calls and the owner)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| code (plan, copies) | What does code check? | Rule C2 checks the slot IDs and the number of options against the plan, and a failure stops the run. Rule C3 looks for two questions with the same text in the whole mock. C3 found none in the 5 mocks: a copy in other words is for call 6a. | Mock decisions 0034 and 0052 | step-6.md rule table C2 and C3, E10, E17, section 4.2 |
| call 6a (D1 scene, D4 answer) | What is "the same scene"? | "The same scene" has an exact definition: the same problem and the same correct action. Call 6a sees each question with its marks and reasons, but no text of the exam guide. | 4.1-K1 | step-6.md rule table D1, E4, E6, section 3 (4.1-K1) |
| call 6b (D2, D3: wrong options) | How many repeats are too many? | Rule D2 fails a wrong idea that is a wrong option in more than 2 questions of the scenario. The number 2 is a guess of the assistant with no source, and no decision changed it after the 5 mocks. | Mock decision 0034 | step-6.md rule table D2, E8, X10 |
| the owner (ignore or rewrite) | When does the owner see the findings? | The owner sees the findings only after the marks of step 7, so the marks come with no verdict in view. Step 8 cannot start while a finding has no decision. | Mock decision 0038, part 4 | step-6.md E20, E25, step-7.md E37 |

No popup: none left.

### Fig. 6-2 (step 6, bar chart)

No popup. A bar chart with its numbers. The caption explains it.

### Fig. 7-1 (step 7, the columns of the marking file, then a flow)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| column "Point" | Why does the reader see the point? | The file shows the ID and the text of the point, because a reader cannot judge if a question tests its point without it. | Mock decision 0035 | step-7.md E9, E12 |
| column "Reason (for a bad mark)" | Why must a bad mark have a reason? | A bad mark with no reason gives the writer nothing to change. A real reason, from mock 5: "Keep point 3.2-K2, but make a different frontmatter field the answer". | Mock decision 0035 | step-7.md E29, D10 |
| box "no column for the verdict of a checker" | How does the build make sure of it? | A test checks that no header and no cell of the file has a verdict word, such as "pass" or "fail". For the same reason, a rewrite never counts as a bad mark: the owner saw a verdict before it. | Mock decisions 0035 and 0037 | step-7.md E10, E38 |
| too many bad (the mock stops) | How many is too many, and what then? | More than 6 bad marks of 60, or 2 of 20, in round 1 stop the mock. Both numbers are guesses of the assistant. After a stop, code refuses each command, and no procedure for the next step is decided. | Mock decisions 0035 and 0039 | step-7.md E30, E31, E33, X2 |

No popup: columns "Question", "Correct answer" and "Reasons of the options" (they explain themselves), good (kept) (trivial), bad (to step 5) (the text says it).

### Fig. 7-2 (step 7, small bar charts for each mock)

No popup. Bar charts with their numbers and a line for each mock.

### Fig. 8-1 (step 8, the owner, the conditions box and the files)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| the owner (accept) | What does accept save, and when? | Code saves the decision `accept` only after step 8 built the files, so a failed build saves no accept. Then the mock is `built`, and code refuses each later decision. The code has no path to build the files again. | Mock decisions 0039 and 0082 | step-8.md E5, E6, E7, `docs/decisions/0082-the-code-has-no-path-to-build-the-files-again.md` |
| questions file (no answers) | What is in it? | Each question keeps its point and its task statement, and each option has only a letter and a text. A test checks that the file has no key "correct" and no key "reason". The file also gives the time of the mock: 120 minutes. | Mock decisions 0003 and 0036 | step-8.md F2, F4, F7 |
| answers file (letters, reasons) | Why a separate file? | A separate file lets the portal send the questions to a participant with no answers in the same file. Both files have the format of this build. A converter for the portal comes later, when its format is known. | Mock decision 0036 | step-8.md F10, F11 |
| fingerprints | What does a fingerprint cover? | It covers what a participant sees: the question ID, the question, the field `select`, and each option with its letter, text, mark and reason. The date and the model are not in it, because they do not change what a participant sees. | Mock decisions 0036 and 0039 | step-8.md P1, P2 |

No popup: condition lines 1, 2, 3, 5 and 6 (the text, step 6 and step 7 explain them).

### Fig. 8-2 (step 8, small bar charts of the letters)

No popup. Bar charts with their numbers and the chance line. The caption explains it.

### Fig. C-4.6-1 (part 4.6 of "The build in Claude Code", four boxes of the document checks, small bars)

| Box | The question it raises | The popup (draft, 1 to 3 sentences) | Guide point or decision | Source |
|---|---|---|---|---|
| check 1 (gaps, no count) | What did check 1 find? | It found errors in three confirmed decisions: 0047, 0068 and 0071. Working rule 26 keeps a confirmed text, so mock decision 0078 names each error. | 4.6-S1, mock decision 0078 | claude-code.md entry 3 (c), row 1 and line 201 |
| check 2 (26 gaps, more files) | Which more files? | It also read diagrams 03, 05, 08 and 10 and the build guide sections of steps 0, 1, 3 and 6. Because its scope was wider, its 26 gaps cannot be compared with check 1, which has no count. | 4.6-S1 | claude-code.md entry 3 (c), row 2, C3.1 |
| check 3 (20 smaller gaps) | What kind of gaps? | One kind that the records name: some status lines did not name mock decision 0078. No source lists the 20 gaps one by one. | Mock decision 0078 | claude-code.md entry 3 (c), row 3, (f) |

No popup: the small bars (numbers with labels).







## Dropped from the drafts

- Fig. 1.3-1, conversation history of the coordinator (not passed): a side question
- Fig. 1.3-1, Subagent A, B, C (one key): a side question
- Fig. 1.4-1, PreToolUse hook (one key, cards Allowed and Denied): a side question
- Fig. 1.5-1, PostToolUse, your code: a side question
- Fig. 1.5-1, The tool runs, an MCP tool: a side question
- Fig. 1.6-1, Next subtask: a side question
- Fig. 1.7-1, Session A, name: auth-refactor (card Resume): a side question
- Fig. 2.1-1, analyze_document, after: the caption has it
- Fig. 2.4-1, environment, the secret, not in git: a side question
- Fig. 3.1-1, sub/CLAUDE.md: a side question
- Fig. 3.2-1, SKILL.md content = the task: a side question
- Fig. 3.2-1, New subagent: a side question
- Fig. 3.3-1, .claude/rules/testing.md, paths: "**/*.test.tsx": a side question (the live figure answers the box)
- Fig. 3.4-1, Explore subagent, outside plan mode: a side question
- Fig. 3.6-1, claude -p, in the CI job: a side question
- Fig. 3.6-1, Prior findings, report only new: a side question
- Fig. 5.2-1, Customer message, the policy is silent: a side question
- Fig. 5.2-1, Customer message, frustrated: a side question
- Fig. 5.4-1, /compact, makes it smaller: a side question
- Fig. 5.5-1, Accuracy by segment, document type and field: a side question
- Fig. 5.6-1, Coordinator, decides how to reconcile: a side question
- Fig. 0-1, script of step 0 (code, no model): the caption has it
- Fig. 0-1, guide records (one JSON file): a side question
- Fig. 0-1, no file (and the cause): a side question
- Fig. 1-1, rule line 2: "4 scenarios, 15 questions each": a line, not a box
- Fig. 1-1, rule line 6: "2 two-answer slots in each scenario": a line, not a box
- Fig. 2-1, row "the task statement, its point flagged": a side question
- Fig. 2-1, Claude (one new call): a side question
- Fig. 2-1, code (mixes, gives letters): a side question
- Fig. 3-1, A1 "complete form": the label answers it
- Fig. 3-1, A11 "not negative": the label answers it
- Fig. 5-1, Step 4 (check by a model): a side question
- Fig. 5-1, band "after the last failed try: an open slot, the owner dec: a side question
- Fig. 5-3, first design review (14): a side question
- Fig. 5-3, second design review (10 new): a side question
- Fig. 5-4, owner: more tries: a side question
- Fig. 6-1, all 60 passed (each scenario): a side question
- Fig. 7-1, column "Mark": a side question
- Fig. 7-1, marking file (no verdict shown): a side question
- Fig. 7-1, a reader (good or bad): a side question
- Fig. 7-1, code (reads the file): a side question
- Fig. 8-1, condition line 4: "each question that needs a mark has one": a line, not a box
- Fig. 8-1, no file, causes: the caption has it
- Fig. C-4.6-1, stopped (by the owner): a side question
- Fig. 1.7-1, --resume … --fork-session: a side question
