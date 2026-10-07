# 0041: Corrections to the model steps after the review of the code

- Date: 7 October 2026
- Status: accepted
- Diagram: none

## Question

An independent reviewer checked the code of steps 2, 4, 5 and 6 (`src/model_call.py`, `src/step2_write.py`, `src/step4_check_model.py`, `src/step6_check_scenario.py`). It found 3 serious and several minor items. Some fixes go beyond the text of confirmed decisions. Which fixes change what a decision says?

## Options

1. Record each fix that changes or adds to a confirmed decision in this file (rule 26).
2. Change the confirmed decisions.

## Decision

Option 1. These fixes are in the code, each with a test.

1. **The "reason" fields of the forms ask for a short explanation.** The draft forms in `docs/diagrams/04-form-schema-draft.json` and `06-forms-draft.json` change one description each:
   - The reason of an option (decision 0029, part 3): "Why this option is correct or wrong." becomes "A short explanation of why this option is correct or wrong."
   - The reason of call 4a (decision 0032, part 7): "Why you select these options, or why you cannot decide." becomes "A short explanation of the selection, or of why you cannot decide."

   The source: page "Define tools", https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, section "Specifying client tools", subsection "Best practices for tool definitions" (saved copy: `docs/sources/2026-10-07-anthropic-docs-define-tools.md`): "**Ask for an explanation, not reasoning.** If a parameter asks Claude why it is making the call, ask for a short explanation or the supporting evidence. A parameter that asks for the model's thinking or step-by-step reasoning may lead to a `reasoning_extraction` refusal."

2. **Rule B6: a name must be a complete word or words.** Decision 0037, item 8, says: "Code ignores capital letters, and treats a hyphen, an underscore and a space as the same." Code now also:
   - finds a name only when no letter or digit comes directly before it or after it. So "Vision" is not found inside "provisions".
   - removes quotes and backticks around a name.
   - never finds a name of one character.
   - tells call 4b to list the bare name, with no value: "tool_choice", not "tool_choice: any".

3. **An error that a new call cannot repair stops the run.** Decision 0037, item 10, says: "Code runs a call that fails again, at most 3 times." That stays for the errors that a new call can repair: 429, 5xx and network errors, a refusal, an answer that reached `max_tokens`, and an answer that is not valid. Each other error stops the run at once, with the cause. Examples: no key, a request that the API rejects (400), the package `anthropic` not installed. The owner repairs the cause and starts the program again. The source of the two groups: the Claude API skill, file `shared/error-codes.md` ("retryable (429, >=500, network) vs. non-retryable (4xx)"). Not checked on a page of the documentation.

4. **A failure of rule C2 stops the run.** Decision 0034 says: "If rule C1 or C2 fails, the step stops with an error that names the cause." A new call cannot repair a wrong count, so it now stops the run at once.

5. **Code writes each enum value in one form before it compares.** "Pass" becomes "pass", and "b1" becomes "B1". The source: page "Structured outputs", section "Invalid outputs" (saved copy: `docs/sources/2026-10-07-anthropic-docs-structured-outputs.md`): "Structured outputs don't guarantee the capitalization of string `enum` and `const` values". The same section says: "Compare enum values case-insensitively".

6. **Each call streams, with `max_tokens` 64000.** Thinking is always on in Claude Opus 5.5, and its tokens count toward `max_tokens`. With 16000, call 4b could stop before its answer is complete. The source: the Claude API skill (streaming for a high `max_tokens`, and thinking always on in Claude Opus 5.5). Not checked on a page of the documentation.

7. **The letters.** Decision 0029, part 4.1, says: "The seed controls the sequence." Code mixes the options with the seed of the plan, the slot ID and the question text. So the same answer always gets the same letters.

8. **Step 6 keeps the model.** Each result of calls 6a and 6b has the field `model`. The results of rules C2 and C3 are in the same list as the results of the calls. A separate field `code_count` (decision 0034, part 6) does not exist.

9. **The first values of the settings.** The model is `claude-opus-5-5` and the effort is `high`. These are not decisions. The test of decision 0024 decides them.

## Reason

- Items 1, 5 and 6 follow the documentation of the API.
- Item 2: a search inside other words passes a name that the guide does not name. That is the error that rule B6 must prevent (decision 0030: "a false pass puts a bad question into a mock").
- Items 3 and 4: three runs of a call that cannot succeed cost money and give the owner 60 error records in place of one clear cause.
- Items 7 and 8 make the code agree with decisions 0029 and 0034.

Not decided yet:

- Rule B6: if a name on the list "out of scope" of Section 17 counts as named. Now it counts, because it is in the records file. Also a name in another form than the guide, for example "is_error" against "isError", is not found.
- Rule C3 compares the questions of one scenario only. Decision 0034 says "No two questions have the same text" for the mock. A copy in two scenarios is not found.
- If the calls use the server-side refusal fallback that the Claude API skill recommends. It is not used now, because a fallback changes the model that answers.

## How we decided

The owner said yes to the plan to build steps 2, 4 and 6. Rule 32 permits fixes that make the code agree with decisions and with the documentation, without a yes before. The owner has not confirmed the text of this file. No independent reviewer checked this file. No real call to the API has run yet.

## Exam guide points

none
