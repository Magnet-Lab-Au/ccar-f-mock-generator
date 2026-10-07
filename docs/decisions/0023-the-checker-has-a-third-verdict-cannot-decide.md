# 0023: The checker has a third verdict: "cannot decide"

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Diagram: none

## Question

The checker of step 4 cannot decide if a question is good. What happens?

## Options

1. The checker has only "pass" and "fail". It must select one.
2. The checker has a third verdict, "cannot decide", with a reason. The question goes to step 5.
3. Each "cannot decide" goes to the owner immediately.

## Decision

Option 2. The checker of step 4 has three verdicts: "pass", "fail" and "cannot decide". "Cannot decide" has a reason. The question then goes to step 5 with that reason. If one slot gets "cannot decide" two times, the slot goes to the owner.

## Reason

The guide names the method, in the context of a schema for data extraction: "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization" (4.3-S5). With only two verdicts, the checker must guess, and a guess looks the same as a real verdict.

The plain reason for step 5 as the first action: if the checker cannot decide, a participant probably cannot decide. So the question is not clear, and a new try can repair it.

Not decided yet: if the model call of step 6 also has this verdict.

## How we decided

The assistant showed three options and recommended option 2. The owner chose option 2.

## Exam guide points

4.3-S5
