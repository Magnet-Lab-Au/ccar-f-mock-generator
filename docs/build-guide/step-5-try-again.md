# Step 5: try again

Status: built. It ran in mocks 1 to 5, from 7 to 9 October 2026.

Diagram: [`07-step-5-try-again.html`](../diagrams/07-step-5-try-again.html)

## What the step does

A question that fails step 3 or step 4 goes back to the writer. The writer gets the request of step 2, plus the failed question with the letters that the checker saw, and the exact findings. The writer does not see older tries, so the request stays short. The new try goes through steps 3 and 4 again, as a new question.

A question also comes back when the owner sends it back: a bad mark, or a "rewrite". A rewrite can name a finding of step 6, or only a reason of the owner. The owner can also give the slot a new point of the same task statement. Code then checks that the point is in that task statement, that no other slot uses it, and that the slot did not have it before.

Each start of a slot has at most 3 tries. Two results "cannot decide" also stop a slot. A slot that stops is open, and the owner decides: more tries, a new point, or a new plan. After "more tries", the writer also gets the reason of the owner as an instruction (decision 0074). In mocks 4 and 5, most open slots came from the stricter rule B9, and the owner gave new points or added the idea to the narrow list (decisions 0068 and 0075). The limit is not the main way to stop. The main way to stop is a question that passes.

Each try is a new file. No file is written over, so the history of each question stays.

## The run of mock 1

- 83 tries for 60 slots: 65 were a request of step 2 (a first question, or a rewrite on a new point), and 18 a request of step 5.
- 18 slots needed more than one try. The most tries for one slot: 6.
- Step 4 failed 14 tries. The findings by rule: B3 1, B4 1, B5 2, B6 3, B7 7.
- One slot stopped after 3 tries. Each try had corrected the last finding, and a new small finding came. The owner gave it more tries.
- The owner sent 9 questions back as rewrites after the marks, 5 of them with a new point.

## A deviation from the exam guide

The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call.

The reason: the newest Claude models reject it. The page "Define tools" of the Anthropic documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), section "Controlling Claude's output", subsection "Forcing tool use", has a table. Its row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". As the replacement it names "`auto` with strict tool use", or "structured outputs when you need a response in a fixed JSON shape". An older model, Claude Opus 5, still accepts a forced tool call, but this build keeps the choice of the model free for the test that selects it.

So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`. The page "Structured outputs" (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), section "Why use structured outputs", says: "Structured outputs guarantee schema-compliant responses through constrained decoding".

The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes. Copies of both pages, read on 7 October 2026, are in `docs/sources/`.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 4.4-K1 | "Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction" | Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality | Written for the extraction of data. Here: the findings of the checks go back to the writer with the failed question. |
| 4.4-S1 | "Implementing follow-up requests that include the original document, the failed extraction, and specific validation errors for model self-correction" | Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality | The same context. Here: the "document" is the request of step 2, the "failed extraction" is the failed question, and the "validation errors" are the findings. |
| 4.4-K2 | "The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)" | Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality | The same context. Here: the writer can answer "cannot write" for a slot that does not fit its scenario. The design expects that such a slot does not improve with a new try. That is an assumption, not checked. |
| 1.1-S3 | "Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator" | Task statement 1.1: Design and implement agentic loops for autonomous task execution | Written for agent loops. Here: the limit of 3 tries is a guard, not the main way to stop. The main way to stop is a question that passes. |
| 4.3-K1 | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. The new try answers in the same fixed form as step 2, sent as structured outputs (see the deviation above). |
| 4.3-S3 | "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above). |
