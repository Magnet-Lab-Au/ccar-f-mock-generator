# 0018: Each step has a contract, and the final script checks the step names

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: none

## Question

Two details were suggested in the session of 2 to 5 October 2026 and were in no decision file. Do they apply?

## Options

1. Both apply.
2. One of them applies.
3. None applies.

## Decision

Option 1.

1. For each pipeline step, we decide what it receives, what it returns and what can fail.
2. The final script of decision 0001 checks that each of the 240 points has an answer in the workbook `docs/coverage/task-statement-decisions.xlsx`. It also checks that each answer names a step that exists.

## Reason

A step gets only what the program gives it. The guide says this for subagents: "subagent context must be explicitly provided in the prompt" (1.3-K2). So the design of each step must say what the step receives.

A failure must have a form that the next step can use. The guide names "Structured error context (failure type, attempted query, partial results, alternative approaches) as enabling intelligent coordinator recovery decisions" (5.3-K1), and it names "silently suppressing errors (returning empty results as success)" as an anti-pattern (5.3-K4). So the design of each step must say what can fail.

The guide does not cover this: what a step returns when it succeeds, as a general rule, and the check of step names by the final script. The plain reason for that check: an answer that names a step that does not exist is an answer that nothing in the program does.

## How we decided

The session of 2 to 5 October 2026 suggested both details. `HANDOFF.md` said to ask the owner before use. The owner confirmed both on 6 October 2026.

## Exam guide points

1.3-K2, 5.3-K1, 5.3-K4
