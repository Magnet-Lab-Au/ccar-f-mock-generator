# The test of the stricter rule B9 on mock 3

- Date: 9 October 2026
- Decision: 0066
- Script: `src/test_b9.py`. Results: `runs/test-b9/results.json`.
- Cost: $6.33 for 60 calls of call 4b. The estimate of the assistant was $3 to $4. Each call takes the full text of the guide and the 12 sample questions.

## What the test did

Call 4b checked each of the 60 built questions of mock 3 with the new text of rule B9 (decision 0066), against the questions of mocks 1 and 2 on the same idea. Mock 3 did not change.

## The result

The new B9 fails 24 of the 60 questions and passes 36.

| Failed question | Earlier questions on the same idea |
|---|---|
| M3-S07-T4 | M2-S54-T1 |
| M3-S08-T1 | M1-S31-T2, M1-S48-T1, M2-S38-T3 |
| M3-S09-T1 | M1-S50-T1 |
| M3-S10-T2 | M2-S41-T2 |
| M3-S13-T2 | M2-S49-T2 |
| M3-S17-T1 | M1-S17-T2 |
| M3-S22-T3 | M1-S26-T1, M2-S19-T3 |
| M3-S23-T1 | M2-S21-T1 |
| M3-S24-T1 | M2-S07-T1 |
| M3-S26-T1 | M1-S06-T1 |
| M3-S27-T1 | M2-S55-T1 |
| M3-S30-T2 | M1-S08-T1, M1-S21-T1, M1-S25-T2, M2-S29-T1 |
| M3-S35-T1 | M1-S24-T3 |
| M3-S39-T2 | M2-S03-T1 |
| M3-S40-T2 | M1-S27-T1 |
| M3-S42-T1 | M1-S28-T2, M2-S08-T2 |
| M3-S44-T2 | M1-S11-T1 |
| M3-S46-T1 | M2-S47-T1 |
| M3-S48-T6 | M1-S44-T1 |
| M3-S51-T1 | M1-S42-T1 |
| M3-S53-T4 | M2-S20-T2 |
| M3-S54-T1 | M2-S04-T1 |
| M3-S57-T2 | M2-S57-T1 |
| M3-S58-T1 | M1-S33-T1, M1-S40-T2, M1-S43-T1, M2-S32-T3 |

## Agreement with the independent agent

Before the marking of mock 3, an independent agent compared the questions (decision 0062). It named about 26 questions with the same problem and the same answer as an earlier question.

| | Questions |
|---|---|
| The rule fails them, and the agent named them | 12 |
| The rule fails them, but the agent did not name them | 12 |
| The agent named them, but the rule passes them | 14 |

So the rule and the agent agree on about half. Both are judgments of a model.

## Five examples

| Mock 3 | Earlier | The reason of B9, in short |
|---|---|---|
| M3-S51 | M1-S42 | The same problem in the same setting: a long Claude Code session, compaction blurs exact values, and the answer is a facts block outside the summary. Only the data changes. |
| M3-S24 | M2-S07 | A subagent's tool times out on a short outage. The answer is a local retry, then partial results and what was tried. Another subagent and tool, but the same problem. |
| M3-S10 | M2-S41 | A vague instruction causes false positives. The answer is explicit categories to flag and to skip. Invoices instead of code review. |
| M3-S26 | M1-S06 | A text pattern in hundreds of files whose names do not show it. The answer is Grep, not Glob or Read. Only the pattern changes. |
| M3-S42 | M1-S28, M2-S08 | The loop gets stop_reason "tool_use". The answer is to run the tool, send the result back, and continue. |

The assistant judged the first three fair fails, and the last two a risk: those ideas have almost only one problem, so a strict rule can make their slots fail three times.

## The decision of the owner

The owner decided: use the stricter B9 for mock 4, with one exception. Some ideas have almost only one problem, for example "find text across many files, so use Grep" and "run the requested tool and send the result back". For those, the old rule stays: only a copy fails. The assistant drafts the list of these narrow ideas from the point groups, and the owner confirms it once (decision 0066, `data/narrow-ideas.json`).
