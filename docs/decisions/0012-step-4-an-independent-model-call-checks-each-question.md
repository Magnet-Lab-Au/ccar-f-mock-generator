# 0012: Step 4 of the pipeline: an independent model call checks each question

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: `docs/diagrams/01-pipeline-overview.html`

## Question

What checks a question against the rules that need judgment?

## Options

1. A second model call that did not write the question. It is a plain API call.
2. The writer checks its own question in the same call.
3. A different method.

## Decision

Option 1. Step 4 is the model check. For each question that passed step 3, a new API call checks the question against the rules that need judgment. Examples: only the marked answer is correct, each wrong option is wrong for a reason that the guide gives, the question tests its task statement.

The call receives the question and the text of the guide. It does not receive the notes or the reasoning of the writer. The call is not a subagent.

## Reason

"a model retains reasoning context from generation, making it less likely to question its own decisions in the same session" (4.6-K1). "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking" (4.6-K2, also 4.6-S1 and 3.6-K4). So a new call checks the question, and it does not get the notes of the writer.

The doubt of the checker is not proof. Self-reported confidence scores are "unreliable proxies for actual case complexity" (5.2-K3). This step alone does not show that a question is good.

Not decided yet: the list of rules, the input and the output of the call, and which model.

## How we decided

The assistant suggested this step. The owner asked if the pipeline needs subagents, because single calls are independent already. That is correct. A subagent gives a separate context (1.2-K2) and a loop with tools. A plain API call already has a separate context: the Messages API is stateless, and each call sees only what the program sends (Anthropic documentation, read on 6 October 2026). A subagent is necessary only for a step in which code cannot know before the call what the model must read. Steps 1 to 4 have no such step. It is possible that no step needs the Agent SDK. Decision 0002 permits that. If no step needs it at the end, a new decision will say so.

A comparison of the checker with labels from a person is a different step (decision 0015).

## Exam guide points

4.6-K1, 4.6-K2, 4.6-S1, 3.6-K4, 5.2-K3, 1.2-K2
