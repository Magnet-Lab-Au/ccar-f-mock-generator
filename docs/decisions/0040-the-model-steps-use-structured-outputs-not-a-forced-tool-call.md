# 0040: The model steps use structured outputs, not a forced tool call

- Date: 7 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026
- Diagram: none. The diagrams of steps 2, 4 and 6 show it when those steps are built.

## Question

Decisions 0029, 0032 and 0034 say that each model step answers in a fixed form, and that the request forces the model to call one tool. Decision 0029, part 3, says: "The form is a JSON schema of a tool, and the request forces the model to call that tool." The current Claude models do not accept a forced tool call. How does a model step get its fixed form?

## Options

1. Keep the forced tool call, and use a model that still accepts it (Claude Opus 5).
2. Structured outputs: the request carries the JSON schema in `output_config.format`, and the API makes the answer agree with it. No tool.
3. A tool that the model is not forced to call (`tool_choice` `auto`), with `strict: true`, and an instruction in the prompt to call it.

## Decision

Option 2. Steps 2, 4 and 6 (and step 5, which uses the request of step 2) send their form as a JSON schema in `output_config.format`. The forms of decisions 0029, 0032 and 0034 keep their fields. Two things change:

- The schema is the part `input_schema` of each draft. The fields `name` and `description` of the tool are not sent as a tool. The description goes into the request text.
- Each object in a schema gets `"additionalProperties": false`. The documentation requires it (see the sources below).

Code still checks each answer (decisions 0031, 0032 and 0039). A schema does not check meaning. The guide says this, for the extraction of data, in point 4.3-K3 (quoted in decision 0029).

This replaces one sentence in each of three confirmed decisions (rule 26):

- Decision 0029, part 3: "The form is a JSON schema of a tool, and the request forces the model to call that tool."
- Decision 0032, part 7: "Each call answers in a fixed form, as in step 2 (decision 0029)." The form is now sent as structured outputs.
- Decision 0034, part 4: "Each call answers in a fixed form." The form is now sent as structured outputs.

### A deviation from the exam guide

The exam guide teaches a forced tool call for a fixed form. This build does not use it. Each build guide section of steps 2, 4 and 6 must show this deviation openly: what the guide teaches, what the current API documentation says, the page, the section, and the exact text.

The guide points:

- "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" (4.3-K1, task statement 4.3: Enforce structured output using tool use and JSON schemas)
- "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" (4.3-S3, task statement 4.3: Enforce structured output using tool use and JSON schemas)
- "The distinction between tool_choice: "auto" (model may return text instead of calling a tool), "any" (model must call a tool but can choose which), and forced tool selection (model must call a specific named tool)" (4.3-K2, task statement 4.3: Enforce structured output using tool use and JSON schemas)

### The sources

Both pages were downloaded on 7 October 2026. A copy of each is in `docs/sources/`.

1. Page "Define tools", https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, section "Controlling Claude's output", subsection "Forcing tool use". The table row for the current models says:

   | Model or setting | Restriction | What to use instead |
   |---|---|---|
   | Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://anthropic.com/glasswing) | `any` and `tool` return a [400 error](https://platform.claude.com/docs/en/api/errors#forced-tool-use-not-supported) | `auto` with [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) to guarantee schema-valid tool inputs, or [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) when you need a response in a fixed JSON shape. Prompting still influences which tool `auto` picks. `none` is also supported |

   The same table says about Claude Opus 5: "Adaptive thinking itself doesn't block forced tool use (Claude Opus 5 supports it with thinking on)".

2. Page "Structured outputs", https://platform.claude.com/docs/en/build-with-claude/structured-outputs.
   - Section "Why use structured outputs": "Structured outputs guarantee schema-compliant responses through constrained decoding".
   - Section "How it works": "The request carries the schema in `output_config.format` with `type: "json_schema"`."
   - Section "JSON Schema limitations", list "Supported features": "`required` and `additionalProperties` (must be set to `false` for objects)". The list "Not supported" includes "Numerical constraints (such as `minimum`, `maximum`, `multipleOf`)", "String constraints (`minLength`, `maxLength`)" and "Array constraints beyond `minItems` of 0 or 1". The draft forms use none of these.

## Reason

- **Not option 1.** The test of decision 0024 must select the model for the quality of the questions. A forced tool call would fix the model now. An older model also costs more and is retired earlier. Structured outputs work with each current model, so the model stays free.
- **Not option 3.** With `auto`, the model can answer with text and not call the tool. Then code must run the call again. The documentation recommends structured outputs "when you need a response in a fixed JSON shape", and a fixed form is all that these steps need.
- **The guide.** Point 4.3-K1 says that tool use with JSON schemas is the most reliable way to get output that agrees with a schema. Point 4.3-S3 forces one tool. The guide wrote both for the extraction of data, and the guide is Version 1.0, July 2026. The current API documentation gives a newer way with the same purpose: an answer that agrees with a schema. This build follows the current API, and it says so.

Not decided yet:

- If a later version of this build uses `strict: true` tools in place of structured outputs.

## How we decided

The assistant read the skill of the Claude API before it wrote the code of the model steps. The skill said that the current models reject a forced tool call. Rule 9 asks for a check in the documentation, so the assistant read the page "Define tools". It confirmed the fact and recommended structured outputs. The owner asked if a model that supports a forced tool call is better. The assistant recommended against it, for the three reasons in the Reason. The owner agreed, and asked that the deviation is shown openly, with the page and the section. So the two pages are saved in `docs/sources/`, and this file quotes them.

No independent reviewer checked this file.

## Exam guide points

4.3-K1, 4.3-S3, 4.3-K2, 4.3-K3
