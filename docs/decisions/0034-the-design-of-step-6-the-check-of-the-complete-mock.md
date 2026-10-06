# 0034: The design of step 6: code counts the mock, and two calls read each scenario

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Diagram: `docs/diagrams/08-step-6-check-the-complete-mock.html`

## Question

Decision 0014 says that step 6 checks the complete mock: a code count, and one model call for each scenario. It left open the definition of "the same scene" and the output of the model call. Decision 0023 left open if the model call of step 6 has the verdict "cannot decide". What is the design of step 6?

This decision adds to decision 0014. Decision 0014 has one model call for each scenario. This decision has two. It also changes two things. Decision 0014 sends back each question that the step names, and this decision sends back one question for each finding. Decision 0020 checks the complete mock again after a new try, and this decision checks that scenario again.

## Options

1. A code count, and one model call for each scenario with 4 rules.
2. A code count, and two model calls for each scenario. Each call has one job.

## Decision

Option 2.

### 1. When the step starts

The step starts when the current try of each of the 60 slots has the status `passed` (decisions 0033 and 0037, item 2).

### 2. Part 1: code counts the mock

| # | Rule |
|---|---|
| C1 | The current try of each of the 60 slots has the status `passed`. The current try is the try with the highest number. |
| C2 | The counts agree with the plan: for each scenario, each domain, each task statement and each question type. |
| C3 | No two questions have the same text. |

If rule C1 or C2 fails, the step stops with an error that names the cause. If rule C3 fails, the question that was written last goes to step 5.

### 3. Part 2: two model calls for each scenario

Each call reads the 15 questions of one scenario together. A mock has 4 scenarios, so a mock has 8 of these calls.

| Call | Looks at | Rules |
|---|---|---|
| 6a. The scenes | The 15 questions with their options and marks | D1 and D4 |
| 6b. The wrong options | The wrong options of the 15 questions, with their reasons | D2 and D3 |

| # | Rule |
|---|---|
| D1 | No two questions have the same scene. Two questions have the same scene when they have the same problem and the same correct action. |
| D2 | No wrong idea is a wrong option in more than 2 questions of the scenario. |
| D3 | Ruling 2: at most one wrong option of the scenario is the self-reported-confidence option, with the limits of decisions 0006 and 0019. |
| D4 | No question gives away the answer of a different question. |

### 4. The answer of a call

Each call answers in a fixed form. For each of its rules it returns `pass`, `fail` or `cannot_decide`. A finding names the questions by their IDs, and has a detail. This is the draft of the form. It is not tested against the API. The file is `docs/diagrams/08-form-draft.json`.

```json
{
  "name": "submit_scenario_check",
  "description": "Give one result for each rule of this call. Call 6a has the rules D1 and D4. Call 6b has the rules D2 and D3.",
  "input_schema": {
    "type": "object",
    "properties": {
      "results": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "rule": { "type": "string", "enum": ["D1", "D2", "D3", "D4"] },
            "result": { "type": "string", "enum": ["pass", "fail", "cannot_decide"] },
            "findings": {
              "type": "array",
              "description": "Empty when result is pass.",
              "items": {
                "type": "object",
                "properties": {
                  "question_ids": {
                    "type": "array",
                    "description": "The IDs of the questions that the finding names.",
                    "items": { "type": "string" }
                  },
                  "detail": { "type": "string" }
                },
                "required": ["question_ids", "detail"]
              }
            }
          },
          "required": ["rule", "result", "findings"]
        }
      }
    },
    "required": ["results"]
  }
}
```

### 5. What happens with a finding

- When a finding names two questions or more, the question that was written last goes to step 5. If the dates are the same, the question with the highest slot number goes back. Code selects it, not the model (decision 0037, item 7).
- The writer of step 5 gets the finding and the text of the other question.
- The new question goes through steps 3 and 4. Then step 6 checks that scenario again, with the code count and both calls.
- Step 6 runs at most 3 times for one scenario. If the third run still has a finding, the mock waits for the owner. For each finding the owner selects `ignore` or `rewrite` (decision 0037, item 7).
- A result `cannot_decide` goes into the field `step6_cannot_decide` of the report of the run. No question is written again for it. The owner sees it in step 7, after the marking, and selects `ignore` or `rewrite` (decisions 0035 and 0037, item 3). This closes the open item of decision 0023.
- A scenario passes step 6 when no rule has the result `fail`.

### 6. The verdict record

Code saves one new file for each scenario and each run of the step. Example: `runs/mock-01/checks/M1-scenario-3-step6-run1.json`.

| Field | Content |
|---|---|
| `mock`, `scenario`, `run` | Which mock, which scenario, and the run number of the step |
| `code_count` | The results of rules C1 to C3 |
| `results` | The results of both calls, for rules D1 to D4 |
| `verdict` | `pass` or `fail` |
| `to_step_5` | The IDs of the questions that go to step 5 |
| `fingerprints` | One fingerprint for each of the 15 question records that the step read (decision 0036) |
| `model`, `date` | Which model checked, and when |

### 7. The test before the first full run

This adds one part to decision 0024: two questions with the same scene are put into a set of 15 on purpose. Call 6a must find them. If it does not, the call is divided more.

### The contract of the step (decision 0018)

- It receives the plan and the 60 question records that passed steps 3 and 4.
- It returns one verdict record for each scenario.
- It can fail when a slot has no question that passed, or when a call fails. Code runs a call that fails again, at most 3 times (decision 0037, item 10). Then the step reports an error. It never returns "pass" for a scenario that it did not check.

## Reason

- **A pass across the questions.** Decision 0014 has the reason. The guide wrote these points for the review of code in many files: "Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings" (4.6-K3). "Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis" (4.6-S2).
- **Two calls, each with one job.** The owner asked if one call is good enough for so many questions. The length is not the problem: 15 questions with their options are about 1900 words, if they have the length of the 12 sample questions of the guide. (The assistant said "about 2000 words" in the chat.) The risk is the number of jobs in one call. That is a plain reason. The guide does not say it: point 4.6-K3 divides a large review of code by its files, and names "attention dilution" there. So one call compares the scenes, and one call compares the wrong options. The cost is 8 calls for one mock, not 4.
- **C1 and C2.** Decision 0014 has them. Plain reason: after many new tries, code makes sure that the mock still agrees with its plan.
- **C3.** Plain reason: code finds an exact copy for no cost. A model finds a copy with different words (D1).
- **D1.** Decision 0014 names it. A writer call sees only its own slot (decision 0010), so two calls can write the same scene. The definition "the same problem and the same correct action" is an exact rule, not a vague one (4.1-K1, in decision 0030). The guide wrote that point for the review of code.
- **D2.** Decision 0014 names it. Plain reason: if the same wrong idea comes again and again, a participant can mark it wrong without thought. The number 2 is a guess of the assistant. It has no source.
- **D3.** Ruling 2 of the owner (decision 0006, with the correction of decision 0019).
- **D4.** Decision 0014 does not name it. It is new. Plain reason: one question must not answer another.
- **Code selects the question that goes back.** Plain reason: the rule "the question that was written last" has one exact answer, so code applies it. The newest question made the clash. The older question already passed step 6, and maybe the mark of the owner, without it.
- **At most 3 runs.** Plain reason: with no limit, the loop can run with no end. The number 3 is a guess of the assistant. It has no source.
- **"Cannot decide" goes to the report.** Plain reason: a finding of this step names two questions or more. If the call cannot decide, the program does not know which question to write again. So a person looks at it.
- **An error is not a pass.** Decision 0011 uses the guide for this (5.3-K4). The guide wrote that point for errors between the agents of a multi-agent system.

Not decided yet:

- If the correct letters are spread well over a mock, and what the program does if they are not.
- If the step compares questions of different scenarios.
- The exact text of the two requests, the guide text that each call gets, and the model.

## How we decided

The assistant showed a proposal with one model call for each scenario and 4 rules. The owner said: "I wonder if one api call is good enough? 60 questions and answers is long". The assistant said that it is 4 calls with 15 questions each, not one call with 60, and that the length is not the problem. But the doubt of the owner had a real point: one call had 4 jobs. The assistant changed the proposal to two calls for each scenario. The owner said yes.

The owner approved the proposal in the chat. The owner did not see the form and did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

4.6-K3, 4.6-S2, 4.1-K1, 5.3-K4
