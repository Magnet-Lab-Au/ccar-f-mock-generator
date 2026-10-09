# 0058: Mock 2: its known limits

- Date: 8 October 2026
- Status: accepted. Decision 0078 corrects one line of this file.
- Text confirmed by the owner: 9 October 2026
- Diagram: none

## Question

An independent agent compared the 60 questions of mock 2 with the 60 of mock 1. It found 13 strong repeats and 4 close repeats. The owner decided to rewrite the 13 strong repeats with the rule of decision 0056. What happens to the 4 close repeats?

## Options

1. They stay. They are known limits of mock 2.
2. A rewrite for them too.

## Decision

Option 1. The 4 close repeats stay in mock 2 as known limits:

| Mock 2 | Mock 1 | Shared scene and answer |
|---|---|---|
| M2-S18 | M1-S05 | The loop throws away the tool output, and the model repeats a search. The answer: append the output as a tool result. Only one wrong option is the same. |
| M2-S05 | M1-S06 | Unfamiliar code. The answer: Grep first, then trace. The wrong options are similar. |
| M2-S06 | M1-S09 | Two tools with near-identical descriptions. Mock 1 asks for the cause, mock 2 for the fix. The wrong options are different. |
| M2-S50 | M1-S57 | Written rules fail on ambiguous cases. The answer: few-shot examples with the reasoning. The wrong options are different. |

## Reason

Plain reason: a close repeat has the same scene and answer, but different wrong options or a different angle. That is the line of decision 0056: a shared idea with a different angle is allowed. These 4 are near that line, so they are known limits, not errors.

The second review named M2-S26 and M1-S36 as close too. The independent agent did not agree: the two share only the topic (skills), with a different question. So that pair is not a known limit.

## How we decided

The owner decided: "Keep the 4 close repeats as known limits of mock 2."

The owner confirmed the text of this file on 9 October 2026. One independent reviewer checked decisions 0056 to 0058, diagrams 11 and 12 and the code on 8 October 2026, and the assistant fixed its findings.

## Exam guide points

none
