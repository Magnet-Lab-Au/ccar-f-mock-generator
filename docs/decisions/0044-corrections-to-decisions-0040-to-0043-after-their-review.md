# 0044: Corrections to decisions 0040 to 0043 after their review

- Date: 7 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026
- Diagram: none

## Question

An independent reviewer checked decisions 0040 to 0043 on 7 October 2026. It found no error, one serious item in the code, and 10 minor items in the text. The owner confirmed the text of the four files, so a correction needs a new file (rule 26). What are the corrections?

## Options

1. One file with each correction.
2. No correction.

## Decision

Option 1. Where this file and decisions 0040 to 0043 disagree, this file is correct.

**The code.** The system prompt of call 4b said "against six rules", but the rules are B1 to B7. The code now says "seven rules", and a test keeps the number equal to the number of rules. The check of rule B7 of decision 0043 ran with the old sentence. Code requires one result for each of the 7 rules, so each answer of that check had a result for B7.

**Decision 0040.**

1. "The exam guide teaches a forced tool call for a fixed form" is too strong. Point 4.3-S3 forces one tool so that one extraction runs before the others. A different point uses a tool call to get structured output: "Setting tool_choice: "any" to guarantee structured output when multiple extraction schemas exist and the document type is unknown" (4.3-S2, task statement 4.3, for the extraction of data). Both points use a tool call that the current models do not force.
2. "The guide wrote both for the extraction of data" is true for 4.3-S3. Point 4.3-K1 is a general point of task statement 4.3, "Enforce structured output using tool use and JSON schemas".
3. "The description goes into the request text" is not exact. The code puts the description of each form into the system prompt of the call.
4. The names of the parts of the page "Structured outputs": "JSON Schema limitations" and "Invalid outputs" are subsections of the section "Important considerations".
5. "An older model ... is retired earlier" is a prediction of the assistant. It is not checked. "Costs more" is true: the page "Pricing" gives Claude Opus 5 at $5 and $25 per million tokens, and Claude Opus 5.5 at $4 and $20.

**Decision 0041.**

6. Item 8: "The results of rules C2 and C3 are in the same list." Rule C2 gives no result: it passes with no entry, or it stops the run. Only a failure of rule C3 adds an entry.
7. How we decided: "Rule 32 permits fixes that make the code agree with decisions and with the documentation." Rule 32 names only fixes that agree with decisions of the owner. Items 2, 3 and 4 of decision 0041 were new design choices. The owner later confirmed the text of decision 0041.
8. Items 1 and 5 name sections of the page "Structured outputs". The enum quote is under the bold heading "Enum value casing", in the subsection "Invalid outputs" of the section "Important considerations".

**Decision 0042.**

9. "The test cost $3.86" includes the check of rule B7 of decision 0043 ($0.82). Parts 1 to 4 of the test cost $3.04.

**Decision 0043.**

10. The guide wrote point 1.4-K2 for deterministic compliance in an agent workflow, for example identity verification before financial operations. Decision 0043 uses only its general idea: an instruction alone can fail. The clarity of a question is a different context.

**Style.** Some sentences of decisions 0040 and 0042 have more than 25 words, and two sentences of decision 0040 use the passive voice. The text stays (rule 26). New files follow the style rules.

## Reason

Plain reason: a record that does not agree with its source is an error in the record, and the build guide takes its content from the decisions.

## How we decided

Rule 32 lets the assistant record corrections. No independent reviewer checked this file.

## Exam guide points

4.3-S2, 4.3-S3, 4.3-K1, 1.4-K2
