# 0029: The design of step 2: what the writer call gets and what it returns

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review.
- Diagram: `docs/diagrams/04-step-2-write-the-question.html`

## Question

Decision 0010 says that one API call writes one question for one slot. It left open the exact input of a call, the output format and the model. Decision 0027 left open the format of the plan file and the form of a multiple-response question. What is the design of step 2?

## Options

1. One proposal of the assistant with exact formats and fields. The owner accepts or changes each part.
2. A different design, for example a writer that is an agent with the Agent SDK and that starts its own reviewer.

## Decision

Option 1. The owner accepted each part.

### 1. What one writer call gets

Code builds the request from the records file of step 0 and the plan of step 1. The request has these parts:

1. The rules for a good question. This is fixed text, the same for each call. The list is in decision 0030. The checker uses the same list. The request also has one instruction that no step checks: the options of a question have the same form, for example all are actions (decision 0037, item 12).
2. 3 sample questions of the guide, as examples. Code takes them from scenarios that are not the scenario of the slot. Code prepares each example: it keeps the question and the 4 options, mixes the options, removes the letters, marks the correct option and leaves out the explanation (decision 0037, item 12).
3. The story of the scenario of the slot.
4. The task statement of the slot with all its points. The point of the slot is marked.
5. The list of 14 technologies of Section 17 of the guide.
6. The slot.
7. The form that the model must fill (part 3 below).

### 2. The slot

The plan of one mock is one file, for example `runs/mock-01/plan.json`. It has 60 slots. The slot number always has two digits, for example `M1-S04`.

| Field | Example |
|---|---|
| `slot_id` | `M1-S17` |
| `scenario` | `3` |
| `task_statement` | `1.2` |
| `point` | `1.2-K2` |
| `type` | `multiple_choice` or `multiple_response` |
| `options` | `4` or `5` |
| `select` | `1` or `2` |

A multiple-choice question has 4 options and 1 correct answer. A multiple-response question has 5 options and 2 correct answers.

### 3. The form of the answer

The model answers in a fixed form. The form is a JSON schema of a tool, and the request forces the model to call that tool. This is the draft of the schema. It is not tested against the API. The draft does not set the option `strict: true`. The Anthropic documentation (page "Structured outputs", read on 7 October 2026) says that this option guarantees "schema validation on tool names and inputs". Without it, the API does not guarantee that the answer agrees with the schema. So code checks that the answer is a complete form (the contract below).

```json
{
  "name": "submit_question",
  "description": "Return one exam question for the slot, or say that you cannot write it.",
  "input_schema": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["written", "cannot_write"]
      },
      "question": {
        "type": ["string", "null"],
        "description": "The text of the question. Null when status is cannot_write."
      },
      "options": {
        "type": "array",
        "description": "The answer options, with no letters. Empty when status is cannot_write.",
        "items": {
          "type": "object",
          "properties": {
            "text": { "type": "string" },
            "correct": { "type": "boolean" },
            "reason": {
              "type": "string",
              "description": "Why this option is correct or wrong."
            }
          },
          "required": ["text", "correct", "reason"]
        }
      },
      "cannot_write_reason": {
        "type": ["string", "null"],
        "description": "Why the slot cannot be written. Null when status is written."
      }
    },
    "required": ["status", "question", "options", "cannot_write_reason"]
  }
}
```

- `status` has two permitted values.
- `question` and `cannot_write_reason` can be empty (`null`).
- Each option has a text, a mark "correct" (yes or no) and a reason. The options have no letters.
- The model can answer `cannot_write` with a reason. Code saves that answer as a record with its try number. The slot gets the status `open` immediately, with no new try. The report names the slot, and the other slots continue (decision 0037, item 5).

### 4. What code does after the call

1. Code mixes the options and gives them the letters. The seed controls the sequence. The model does not select the letters. The record keeps the letters (decision 0037, item 11).
2. Code adds `question_id`, `slot_id`, `try`, `select`, `point`, `request`, `shown_try`, `status`, `model` and `date`. `point` is the point of the slot, or the new point of a decision `new_point`. `request` is 2 or 5, and `shown_try` is the ID of the failed try that the writer saw, or empty (decision 0039, items 7 and 8). A record with the status `cannot_write` has the field `cannot_write_reason` and no question. Code copies `select` from the slot. It is the number of the line "Select 1." or "Select 2." that each question has. The line is not a part of the question text (decision 0037, item 1). Example: `M1-S17-T1` is mock 1, slot 17, try 1.
3. Code saves the record as one JSON file for each try, for example `runs/mock-01/questions/M1-S17-T1.json`. A new try makes a new file.

### 5. Other parts

- The model is a setting. We select it at the test of decision 0024.
- Each model step is a call of the plain API. The Agent SDK is not used for step 2 or for the check of step 4.

### The contract of the step (decision 0018)

- It receives one slot, the records file and the fixed parts of the request.
- It returns one question record with one ID.
- It can fail when the API call fails or when the answer is not a complete form. Then code runs the same call again, at most 3 times. These are not tries of the slot. After that, no record of a question is saved. Code saves an error record, for example `runs/mock-01/errors/E001.json`, and the other slots continue. The report shows the errors of the last run. The owner starts the program again, and the new start runs the call again (decision 0039, item 9).

## Reason

- **The form.** The guide wrote these points for the extraction of data from documents. Here they apply to a question. "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" (4.3-K1). "Forcing a specific tool with tool_choice: {"type": "tool", "name": "extract_metadata"} to ensure a particular extraction runs before enrichment steps" (4.3-S3). That point forces one tool so that one extraction runs before the others. A nearer point is: "The distinction between tool_choice: "auto" (model may return text instead of calling a tool), "any" (model must call a tool but can choose which), and forced tool selection (model must call a specific named tool)" (4.3-K2). Both points are for the extraction of data. Here a forced tool makes the model answer with the form, and not with free text.
- **Blanks that can stay empty, and "cannot write".** The guide wrote the next point for the extraction of data from documents: "Designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields" (4.3-S4). A model that must fill each blank invents a question for a slot that does not fit. This is an assumption of the assistant. It is not checked. This is the answer of step 2 to the open item of decision 0027 on a task statement that does not fit its scenario. The status `cannot_write` is also near a second point, which the guide wrote for a schema for the extraction of data: "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization" (4.3-S5).
- **What the form cannot check.** "That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)" (4.3-K3). The guide wrote this point for the extraction of data. The point does not say if a schema can limit the number of items in a list, and the assistant did not check that in the Anthropic documentation. So the design does not rely on the form for a count. The code check of step 3 checks the number of options and the number of correct answers.
- **The examples.** The guide wrote these points for output in a fixed format. "Few-shot examples as the most effective technique for achieving consistently formatted, actionable output when detailed instructions alone produce inconsistent results" (4.2-K1). "Including few-shot examples that demonstrate specific desired output format (location, issue, severity, suggested fix) to achieve consistency" (4.2-S2). The plain reason for "not from the scenario of the slot": the writer must not copy the scene of an example. The number 3 is a choice of the assistant. The guide gives a range, for a different purpose: "Creating 2-4 targeted few-shot examples for ambiguous scenarios that show reasoning for why one action was chosen over plausible alternatives" (4.2-S1). Our examples show the form of a question. They do not show reasoning. A limit: the prepared examples have no reason for each option, so they do not show the complete form that the writer must fill.
- **The rules.** The guide wrote this point for the review of code. "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" (4.1-K1).
- **The story, the task statement and the technologies.** Plain reason: the writer needs these for its one question. The list of technologies is for ruling 1 (decision 0005). A limit: a wrong option often comes from a different task statement (decision 0032), and the writer does not get those texts. Call 4b of step 4 has the complete guide text, and it checks the wrong options (rule B2).
- **The letters.** Plain reason, with a count by script: in the 12 sample questions of the guide, the correct answer is A 10 times and B 2 times. A model that sees those examples can copy that. This is an assumption of the assistant. It is not checked. Then a participant can guess the answer. For the same reason, code mixes the options of each example and removes the letters (decision 0037, item 12).
- **One reason for each option.** Plain reason: no reason names a letter, so the letters can change, and the checker can check each reason alone. The reviewer of step 0 found that the explanations of the sample questions name letters ("Option B").
- **4 options.** Each of the 12 sample questions has 4 options.
- **5 options and 2 correct answers.** A guess of the assistant. It has no source. The guide says only that each item states how many responses to select (Section 3).
- **One file for each try.** Plain reason: the record of each try stays, so we can see later how a question changed.
- **The plain API, not the Agent SDK.** The section "How we decided" of decision 0012 has the reason. In step 2 and step 4, code knows before the call what the model must read, and the answer is one filled form. That is a plain reason. The guide says, for the workflow of an agent, that prompt instructions alone have a non-zero failure rate (1.4-K2). That point supports one thing: code controls the sequence, so each question always gets each check. It does not say "not the Agent SDK". The guide also names hooks as enforcement by code (1.4-K1). The guide has two points on a fixed sequence: "When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings" (1.6-K1) and "Selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks" (1.6-S1). The work of this pipeline is known before it starts, so a fixed sequence fits.

Not decided yet:

- Which 3 sample questions code takes, when more than 3 are possible.
- The exact text of the request and the sequence of its parts.
- The model.
- An automatic path for a `cannot_write` slot. The test of decision 0024 shows if it is necessary (decision 0037).
- What to do with the 5 texts of the records file that have a backslash from the file format (review of step 0).
- The writer gets no example of a multiple-response question with 5 options and 2 correct answers. All 12 sample questions have 4 options and 1 correct answer.
- If the forms use the option `strict: true`.

## How we decided

The first proposal of the assistant said "the story of the scenario" and "a fixed form with fields", with no source and no fields. The owner said that this was not specific. Step 0 was then designed and run first (decision 0028).

The second proposal had exact fields. The owner did not understand it. The assistant then told it as the story of one question in four steps. The owner asked if this describes what is sent in the API call. The answer: it describes both directions, the request and the answer.

The owner asked to see the JSON schema, and accepted it.

The owner asked why a subagent in the same call does not review the output. The answer: one call is one model run, the review is step 4, and a separate call from code gives a separate context with more control. That answer is an assumption of the assistant. It is not checked. The owner asked if the API can have subagents in a call. The assistant read the Anthropic documentation on 6 October 2026. The Messages API is stateless and has no subagents. On 7 October 2026 the assistant found the source of "stateless": the page "Messages" of the API reference says "The Messages API can be used for either single queries or stateless multi-turn conversations." Subagents are a feature of the Agent SDK and of Claude Code. The owner asked why the build does not use the SDK. The answer is in the Reason. The assistant said that the cost is the one of decision 0026, and asked if the owner wants to change that. The owner said: "keep the simple api".

Product facts that the assistant did not check: the exact names of the API parameters that force the form. That check belongs to the code stage.

The owner approved each part in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

4.3-K1, 4.3-S3, 4.3-K2, 4.3-S4, 4.3-S5, 4.3-K3, 4.2-K1, 4.2-S2, 4.2-S1, 4.1-K1, 1.4-K2, 1.4-K1, 1.6-K1, 1.6-S1
