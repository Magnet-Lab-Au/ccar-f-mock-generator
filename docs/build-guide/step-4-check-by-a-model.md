# Step 4: check by a model

Status: built. It ran in the test before the first full run, on 7 October 2026.

Diagram: [`06-step-4-check-by-a-model.html`](../diagrams/06-step-4-check-by-a-model.html)

## What the step does

Some rules need judgment, so a model checks them. The step has two calls, and code sits between them.

**Call 4a, the blind answer.** A new call answers the question as a second expert does. It gets the question, the line "Select N.", the options and the text of the guide, but not the marks and not the reasons. Code compares its letters with the marks of the writer. Different letters fail rule B1. Two calls with code between them make sure that the blind answer always comes first.

**Call 4b, the rule check.** A second call gets the complete question, with the marks and the reasons, and the text of the guide. It gives one result for each of the 9 rules B1 to B9: the marked options are correct, each wrong option is wrong for a reason that the guide gives, each reason is true, the question tests its point, the question is inside its story, no text depends on a feature that the guide does not name, each actor has one name and each sentence is clear, the question is not a close copy of a sample question of the guide, and the question is not a repeat of a question of an earlier mock on the same idea. For rule B8, the call also gets the 12 sample questions (decision 0055). For rule B9, it gets the questions of the built earlier mocks whose point is in the same group (decision 0056, diagram 11). In mock 2, before this rule, 13 questions repeated mock 1. In mock 1, before this rule, two questions were close copies of sample questions 1 and 12. The result is "pass", "fail" or "cannot decide".

For rule B6, the model lists each feature name. Code searches each name in the records of the guide, as a complete word. A name that the guide does not have fails the rule.

Code, not a model, makes the verdict. A question that fails, or that the checker cannot decide, goes to step 5 with its findings.

## The test run

- Call 4a answered the 12 sample questions of the guide. 12 of 12 were right.
- Call 4b checked the 9 questions that the owner marked good, and one copy of each that the build damaged on purpose. Each copy broke one rule. 18 of 18 results were as expected: each good question passed, and each damaged copy failed on its rule.
- After the owner marked a question bad for two names of one actor, rule B7 was added. Call 4b failed that question on B7. It also failed 3 of the 9 good questions on B7, each with a true finding. The rule stays strict.

## A deviation from the exam guide

The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call.

The reason: the newest Claude models reject it. The page "Define tools" of the Anthropic documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), section "Controlling Claude's output", subsection "Forcing tool use", has a table. Its row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". As the replacement it names "`auto` with strict tool use", or "structured outputs when you need a response in a fixed JSON shape". An older model, Claude Opus 5, still accepts a forced tool call, but this build keeps the choice of the model free for the test that selects it.

So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`. The page "Structured outputs" (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), section "Why use structured outputs", says: "Structured outputs guarantee schema-compliant responses through constrained decoding".

The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes. Copies of both pages, read on 7 October 2026, are in `docs/sources/`.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 4.6-K1 | "Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session" | Task statement 4.6: Design multi-instance and multi-pass review architectures | Written for the review of code. Here: the call that wrote a question does not check it. |
| 4.6-K2 | "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking" | Task statement 4.6: Design multi-instance and multi-pass review architectures | The same context. Here: a new call, with no reasoning of the writer, checks the question. |
| 4.3-S5 | "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for a schema for the extraction of data. Here: the result "cannot decide" for a case that the checker cannot decide. |
| 4.1-K1 | "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" | Task statement 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | Written for the review of code. Here: one result for each exact rule, not one total verdict. |
| 1.4-K2 | "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" | Task statement 1.4: Implement multi-step workflows with enforcement and handoff patterns | Written for the order of steps in the workflow of an agent. Here: "answer first, then see the key" is enforced by two calls, not by an instruction. |
| 4.3-K1 | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above). |
| 4.3-S3 | "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above). |
