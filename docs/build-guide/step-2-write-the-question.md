# Step 2: write the question

Status: built. It ran in the test before the first full run, on 7 October 2026, and for mocks 1 to 5, from 7 to 9 October 2026.

Diagram: [`04-step-2-write-the-question.html`](../diagrams/04-step-2-write-the-question.html)

## What the step does

For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock.

Code builds the request from the records of the guide and from the plan. The request has the rules for a good question, 3 sample questions of the guide as examples of the form, the story of the scenario, the task statement of the slot with its point marked, the 14 technologies of Section 17 of the guide, and the slot.

The model fills a form: the question, and each option with a mark ("correct" or "wrong") and a reason. The model can also answer "cannot write", with a reason. Then the slot is open, and the owner decides. The design expects that, with this answer available, the model does not invent a question for a slot that does not fit. That is an assumption, not checked.

The slot also tells the writer two things (decisions 0053 and 0054). If the field `longest_may_be_correct` is false, a wrong option must be longer than each correct option (rule A12). For a slot with 2 answers, the two correct options must test two different parts of the point.

When the idea of the slot is in an earlier built mock, the writer also gets those earlier questions, with the rule: a different problem, also in another setting (the cause, the fix, or a choice between two rules), and not the same set of wrong options. At most one wrong option may repeat (decisions 0056 and 0066). For a narrow idea, with almost only one problem (63 of the 95 ideas), the writer gets the copy rule instead: the same problem may come back in a new setting, but not the same set of wrong options (decisions 0066, 0068, 0072 and 0075).

The list of rules comes first in the request, as a cached block, so that a repeated list costs less (decision 0067).

Code then mixes the options and gives them their letters. The model does not select the letters. From mock 5, the correct options take the letters that the plan sets, so the letters are balanced over the mock (decision 0070). In the 12 sample questions of the guide the correct answer is A 10 times, and a model that sees them can copy that (an assumption, not checked). Code saves one file for each try. No file is written over.

Step 5 uses the same request when a question must be written again. It adds the failed question and the exact findings.

## The test run

The writer made 10 questions for 10 slots of the plan of mock 1, one call for each, with no new try. 10 of 10 passed the code check of step 3 at the first try. The owner read the 10 questions and marked 9 good and 1 bad. The bad mark said that the question used two names for one actor and was hard to read. That mark gave a new instruction to the writer and a new rule for the checker (rule B7, see step 4).

## A deviation from the exam guide

The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call.

The reason: the newest Claude models reject it. The page "Define tools" of the Anthropic documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), section "Controlling Claude's output", subsection "Forcing tool use", has a table. Its row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". As the replacement it names "`auto` with strict tool use", or "structured outputs when you need a response in a fixed JSON shape". An older model, Claude Opus 5, still accepts a forced tool call, but this build keeps the choice of the model free for the test that selects it.

So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`. The page "Structured outputs" (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), section "Why use structured outputs", says: "Structured outputs guarantee schema-compliant responses through constrained decoding".

The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes. Copies of both pages, read on 7 October 2026, are in `docs/sources/`.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 4.3-K1 | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Here: the writer fills a form, so code can read each answer. The method is structured outputs (see the deviation above). |
| 4.3-S3 | "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above). |
| 4.3-K2 | "The distinction between tool_choice: "auto" (model may return text instead of calling a tool), "any" (model must call a tool but can choose which), and forced tool selection (model must call a specific named tool)" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | The same context. It names the three settings of a tool call. The Claude API documentation (Define tools) says that Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 return a 400 error for "any" and "tool". "auto" and "none" still work. |
| 4.3-S4 | "Designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Here: the question can be empty when the answer is "cannot write", so the model does not invent a question for a slot that does not fit. |
| 4.3-S5 | "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for a schema for the extraction of data. Here: the status "cannot_write" is an answer for a case that does not fit. |
| 4.3-K3 | "That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Here: a form stops format errors, but not content errors. So step 3 checks the content. |
| 4.2-K1 | "Few-shot examples as the most effective technique for achieving consistently formatted, actionable output when detailed instructions alone produce inconsistent results" | Task statement 4.2: Apply few-shot prompting to improve output consistency and quality | Written for output in a fixed format. Here: 3 sample questions show the writer the form of a good question. |
| 4.2-S2 | "Including few-shot examples that demonstrate specific desired output format (location, issue, severity, suggested fix) to achieve consistency" | Task statement 4.2: Apply few-shot prompting to improve output consistency and quality | The same context. A limit: the examples have no reason for each option, so they do not show the complete form. |
| 4.1-K1 | "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" | Task statement 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | Written for the review of code. Here: the writer gets exact rules, not vague ones. |
| 1.4-K2 | "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" | Task statement 1.4: Implement multi-step workflows with enforcement and handoff patterns | Written for the workflow of an agent. Here: an instruction to the writer can fail, so each rule that the writer gets is also checked, by code or by a model. |
