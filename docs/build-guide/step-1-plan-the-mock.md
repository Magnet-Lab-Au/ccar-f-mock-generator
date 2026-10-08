# Step 1: plan the mock

Status: built. The step made the plan of mock 1 on 2026-10-07.

Diagram: [`02-step-1-plan-the-mock.html`](../diagrams/02-step-1-plan-the-mock.html)

## What the step does

Before a model writes a question, code makes the plan of the mock: a list of 60 slots. Each slot says what one question must be: the scenario, the task statement, one point of that task statement, the question type, and the number of answers to select. No model works in this step.

A seed controls each selection. The same seed gives the same plan. So we can make the same plan again and compare it, for example after a change to the code.

From the exam guide (Sections 3, 4, 5 and 9):

- 60 questions in 4 of the 6 scenarios.
- The domain weights. For 60 questions they give 16, 11, 12, 12 and 9 questions.
- Two question types: multiple-choice and multiple-response. Each question says how many answers to select.
- 4 options for a multiple-choice question, as in each of the 12 sample questions of the guide.

Not from the exam guide. Each part has a plain reason:

- 15 questions for each scenario: equal parts.
- Each of the 30 task statements gets at least 1 question, so that each mock covers the complete guide. In each domain, the task statements share the questions equally. But a task statement gets no more questions than its number of point groups (decision 0048). Example: task statement 3.3 has one group, so it gets 1 question.
- Each question is in a primary domain of its scenario, so that no question is forced into a story that does not fit it. So the step uses only 11 of the 15 possible sets of 4 scenarios. This is a difference from the exam, which can use all 15 sets.
- No two slots of one mock get points of the same group (decision 0047). The file `data/point-groups.json` puts each of the 240 points into one group, and two points in one group describe one idea. Mock 1 got repeats from two points on one idea (decision 0046).
- The seed sets the order of the task statements for the extra questions, and the order of the points. Code takes the first choice in that order that keeps a full plan possible. It checks this with a matching of task statements to free groups (decision 0048).
- 2 questions of each scenario are multiple-response, with 5 options and 2 answers to select. These numbers are a guess. They have no source.

If a record of the guide or the groups file is not valid, a count does not add up, or the groups allow no plan, the step stops with an error that names the cause. It writes no plan.

## Why code makes the plan

The counts of a mock must hold each time. A model that makes the plan can make an error in a count. The guide says this about instructions to a model, in the context of an agent workflow that must always run in the correct order. So code makes the plan, not a model.

The guide has points on the choice between a fixed sequence of steps (prompt chaining) and a decomposition that changes with what the work finds. It wrote them for a sequence of model calls, with reviews and investigations as examples. Step 1 has no model call. So these points support only one idea: the work of a mock is known before it starts, so the program can fix the plan before the writing starts.

The guide does not cover two parts of this step: a list of slots before the writing, and the balance of the 4 scenarios against the domain weights. Those come from the form of the exam in Sections 3, 4, 5 and 9 of the guide.

## The run of mock 1

| Fact | Value |
|---|---|
| Seed | 366341 |
| Scenarios, in the sequence of the groups | 3. Multi-Agent Research System, 1. Customer Support Resolution Agent, 2. Code Generation with Claude Code, 5. Claude Code for Continuous Integration |
| Questions for each domain | Domain 1: 16, Domain 2: 11, Domain 3: 12, Domain 4: 12, Domain 5: 9 |
| Multiple-response slots | 8 |
| Different points | 60 of 60 |
| The first slot | `{"slot_id": "M1-S01", "scenario": 3, "task_statement": "2.5", "point": "2.5-K3", "type": "multiple_choice", "options": 4, "select": 1}` |

The record is `runs/mock-01/plan.json`. Code writes it one time, and never writes over it.

Code made the plan of mock 1 before the point groups existed. The command `python3 src/point_groups.py plan runs/mock-01/plan.json` shows 9 groups with two or more slots of that plan. The command `python3 src/point_groups.py seeds 2000` runs step 1 over 2000 seeds with the groups: each seed gives a plan.

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 1.4-K2 | "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" | Task statement 1.4: Implement multi-step workflows with enforcement and handoff patterns | Written for an agent workflow. Here: a count must always hold, so code, not a model, makes the plan. |
| 1.6-K1 | "When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings" | Task statement 1.6: Design task decomposition strategies for complex workflows | Written for a sequence of model calls. Here only one idea is used: the work of a mock is known before it starts. Step 1 itself has no model call. |
| 1.6-S1 | "Selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks" | Task statement 1.6: Design task decomposition strategies for complex workflows | Written for the choice of a decomposition, with multi-aspect reviews and open-ended investigations as examples. Here it is used as 1.6-K1 is used. |
