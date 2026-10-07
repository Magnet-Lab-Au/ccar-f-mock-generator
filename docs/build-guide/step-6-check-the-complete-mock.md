# Step 6: check the complete mock

Status: built. It ran in the test before the first full run, on 7 October 2026.

Diagram: [`08-step-6-check-the-complete-mock.html`](../diagrams/08-step-6-check-the-complete-mock.html)

## What the step does

Steps 3 and 4 look at one question. Some defects show only when many questions are read together. Each writer call sees only its own slot, so two calls can write the same scene.

When each slot has a question that passed steps 3 and 4, code counts the mock against the plan. Then two model calls read the 15 questions of one scenario together. Each call has one job:

- **Call 6a, the scenes:** no two questions have the same scene (the same problem and the same correct action), and no question gives away the answer of a different question.
- **Call 6b, the wrong options:** no wrong idea is a wrong option in more than 2 questions of the scenario, and at most one wrong option of the scenario is the option in which a model rates its own confidence.

Step 6 sends no question back. Each finding gets an ID and waits for the owner. The owner first marks the questions, with no finding in view. Then the owner selects "ignore" or "rewrite" for each finding. A rewrite sends one question of the finding to step 5. Then step 6 runs again for that scenario only.

## The test run

The test put two questions with the same scene into a set of 15 questions of one scenario. Call 6a found them: yes. Step 6 also found real problems of the writer: one more pair of questions with the same scene, pairs of questions that give away an answer, and one wrong idea in three questions.

## A deviation from the exam guide

The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call.

The reason: the current Claude models reject it. The page "Define tools" of the Anthropic documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), section "Controlling Claude's output", subsection "Forcing tool use", has a table. Its row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". It says to use "structured outputs when you need a response in a fixed JSON shape".

So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`. The page "Structured outputs" (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), section "Why use structured outputs", says: "Structured outputs guarantee schema-compliant responses through constrained decoding".

The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes. Copies of both pages, read on 7 October 2026, are in `docs/sources/`.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 4.6-K3 | "Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings" | Task statement 4.6: Design multi-instance and multi-pass review architectures | Written for the review of code in many files. Here: steps 3 and 4 are the pass for each question, and this step is the pass across the questions. |
| 4.6-S2 | "Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis" | Task statement 4.6: Design multi-instance and multi-pass review architectures | The same context and the same use. |
| 4.1-K1 | "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" | Task statement 4.1: Design prompts with explicit criteria to improve precision and reduce false positives | Written for the review of code. Here: "the same scene" has an exact definition: the same problem and the same correct action. |
| 5.3-K4 | "Why silently suppressing errors (returning empty results as success) or terminating entire workflows on single failures are both anti-patterns" | Task statement 5.3: Implement error propagation strategies across multi-agent systems | Written for errors between agents. Here: a call that fails, or an answer that is not valid, never counts as a pass. |
| 4.3-K1 | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above). |
| 4.3-S3 | "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above). |
