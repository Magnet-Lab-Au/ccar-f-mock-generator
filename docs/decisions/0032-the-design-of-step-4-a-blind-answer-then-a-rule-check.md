# 0032: The design of step 4: a blind answer, then a rule check

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review.
- Diagram: `docs/diagrams/06-step-4-check-by-a-model.html`

## Question

Decision 0012 says that an independent model call checks each question against the rules that need judgment. Decision 0030 gives those rules: B1 to B6. What does step 4 get and return?

This decision adds to decision 0012. It does not replace it. Decision 0012 has one call for each question. This decision has two. It also changes one sentence of decision 0012: call 4b gets the reasons of the options (see the Reason).

## Options

1. Two calls for each question: a blind answer, then a rule check.
2. One call that sees the complete question record and checks the rules.

## Decision

Option 1.

### 1. Call 4a: the blind answer

- Code gives the call the question, the line "Select N." and the options with their letters. Code leaves out the marks and the reasons (decision 0037, item 1).
- One function of code shows a question to a model or to the owner: the question, the line "Select N." and the options with their letters. Call 4a uses it alone. Call 4b, the calls of step 6 and the marking file of step 7 use it, and add the marks and the reasons. This makes decision 0037, item 1, more exact.
- The call selects the options that it thinks are correct, and gives its reason. It can also answer "cannot decide".
- Code counts the selected letters before it compares them. The count applies only to an answer with the status `answered`. An answer `cannot_decide` has no letters, and it is not an error. A count that is not the number of the line is an error of the call. It is not a finding about the question. Code runs the call again (decision 0037, items 9 and 10).
- A letter that the question does not have makes the answer not valid. Example: the letter E for a question with 4 options. Code runs the call again.
- Code compares the selected letters with the marks of the writer. If they are different, rule B1 fails. The finding has the answer and the reason of the call.

### 2. Call 4b: the rule check

- Code gives the call the complete question record: the question, the options, the marks and the reasons.
- The call returns one result for each rule B1 to B6: `pass`, `fail` or `cannot_decide`. A result that is not `pass` has a finding. A finding names its option by the letter, when it is about one option. A finding names the guide point that it uses, by its ID, when a point applies. Both can be empty.
- The call also returns the field `features`: each name of a feature that the question, the options and the reasons use. Code searches each name in the records file. A name that is not found makes rule B6 fail, and the finding gives the name. Decision 0030 has the definition of a feature (decision 0037, item 8).
- Code checks that each point ID exists in the records file. An answer that is not valid runs again, as a call that fails. Examples: a point ID that does not exist, the letter E for a question with 4 options, or a rule with no result.
- The call gives no confidence number.
- Call 4b always runs, also when the blind answer of call 4a is different from the marks. Then the writer of step 5 gets all findings in one try.

### 3. The guide text for both calls

The story of the scenario, all 30 task statements with their 240 points, and the three lists of Section 17. That is about 5300 words. (The assistant said "about 8000 words" in the chat. That number was the complete records file, with the sample questions. A script counted 5255 words for this text, without the story.)

### 4. The verdict

Code makes the verdict of the question. A model does not make it.

- `fail`: the blind answer is different from the marks, or one rule or more has the result `fail`, or code does not find a name of `features` in the records file.
- `cannot_decide`: no rule fails, and the blind answer or one rule or more has the result `cannot_decide`.
- `pass`: all other cases.

A question with the verdict `fail` or `cannot_decide` goes to step 5 with its findings (decisions 0013 and 0023). A slot that gets `cannot_decide` two times goes to the owner (decision 0023). Decisions 0033 and 0037 say how this rule works together with the limit of 3 tries.

### 5. A new try

A question from step 5 is checked as a new question. The two calls do not see the earlier findings. This closes the open item of decision 0020.

### 6. The verdict record

Code saves one new file for each check. Example: `runs/mock-01/checks/M1-S17-T1-step4.json`.

| Field | Content |
|---|---|
| `question_id` | `M1-S17-T1` |
| `step` | `4` |
| `blind_answer` | The selected letters, the reason, and if they agree with the marks |
| `results` | The result of each rule B1 to B6, with its finding and its point |
| `verdict` | `pass`, `fail` or `cannot_decide` |
| `features` | The names that call 4b listed, and for each one if code found it in the records file |
| `findings` | The list that the writer of step 5 gets, in the form of decision 0037, item 4 |
| `fingerprint` | The fingerprint of the question record that the step checked (decision 0036) |
| `model`, `date` | Which model checked, and when |

### 7. The two forms

Each call answers in a fixed form, as in step 2 (decision 0029). These are drafts. They are not tested against the API. The file is `docs/diagrams/06-forms-draft.json`.

```json
{
  "call_4a": {
    "name": "submit_answer",
    "description": "Answer the exam question. Select the options that are correct.",
    "input_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["answered", "cannot_decide"] },
        "selected": {
          "type": "array",
          "description": "The letters of the options that you select. Empty when status is cannot_decide.",
          "items": { "type": "string", "enum": ["A", "B", "C", "D", "E"] }
        },
        "reason": {
          "type": "string",
          "description": "Why you select these options, or why you cannot decide."
        }
      },
      "required": ["status", "selected", "reason"]
    }
  },
  "call_4b": {
    "name": "submit_check",
    "description": "Give one result for each of the rules B1 to B6.",
    "input_schema": {
      "type": "object",
      "properties": {
        "results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "rule": { "type": "string", "enum": ["B1", "B2", "B3", "B4", "B5", "B6"] },
              "result": { "type": "string", "enum": ["pass", "fail", "cannot_decide"] },
              "finding": {
                "type": ["string", "null"],
                "description": "What is wrong and which option. Null when result is pass."
              },
              "letter": {
                "type": ["string", "null"],
                "description": "The letter of the option that the finding is about. Null when the finding is not about one option."
              },
              "point": {
                "type": ["string", "null"],
                "description": "The ID of the guide point that the finding uses, for example 1.2-K2. Null when no point applies."
              }
            },
            "required": ["rule", "result", "finding", "letter", "point"]
          }
        },
        "features": {
          "type": "array",
          "description": "Each name of a feature of a Claude product or of MCP that the question, the options or the reasons use. Empty when they use none.",
          "items": { "type": "string" }
        }
      },
      "required": ["results", "features"]
    }
  }
}
```

### 8. The test before the first full run

Decision 0024 has this part: call 4a must answer the 12 sample questions of the guide. Their correct answers are known. Call 4b is not tested with the sample questions, because they have no reason for each option. It is tested with the questions of the writer that the owner marks, and with damaged copies of them (decision 0037, item 12).

### The contract of the step (decision 0018)

- It receives one question record that passed step 3, its slot, and the records file.
- It returns one verdict record.
- It can fail when a call fails or when an answer is not a complete form. Then code runs the same call again, at most 3 times. After that, code saves an error record, and the question stays unchecked. The owner starts the program again, and the new start runs the call again (decision 0039, item 9). It never returns `pass` for a question that it did not check.

## Reason

- **An independent call.** Decision 0012 has the reason. The guide wrote these points for the review of code: "Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session" (4.6-K1). "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking" (4.6-K2). A limit: only call 4a is blind. Call 4b is not completely "without prior reasoning context", because it gets the reason of each option from the writer.
- **The blind answer.** No exam guide point gives this reason. The reason is plain. A wrong answer key is the worst defect of a mock. A checker that sees the marks can tend to agree with them. This is an assumption of the assistant. It is not checked. A checker that does not see them must find the answer alone.
- **Code controls the sequence and compares.** The guide says that prompt instructions alone have a non-zero failure rate (1.4-K2, in decision 0009). The guide wrote that point for the order of the steps in the workflow of an agent. Here the order is: answer first, then see the key. An instruction "answer first, then look at the key" in one call is such an instruction. Two calls with code between them enforce it.
- **The cost of an error of call 4a.** If the question is good and call 4a is wrong, the question is written again. That is a false alarm, and it is cheap. If the question is bad and call 4a makes the same error as the writer, the question passes this part. So call 4b and the marks of the owner in step 7 come after it.
- **One result for each rule.** The guide wrote this point for the review of code, and it is about exact criteria in a prompt (4.1-K1, in decision 0030). It does not say "one result for each criterion". That part has a plain reason: one total verdict from the model hides which rule failed.
- **The count of the letters.** Plain reason: a finding must say something about the question. A wrong count says something only about the checker (decision 0037, item 9).
- **Rule B6.** Decision 0030 has the reason: the model finds the names, and code decides "named".
- **"Cannot decide".** Decision 0023 has the reason (4.3-S5). The guide wrote that point for a schema for the extraction of data.
- **The point ID in a finding, and the check by code.** Plain reason: a finding that names a point can be checked against the guide by the writer and by the owner. A point ID that does not exist shows that the checker invented a source.
- **The complete guide text.** Plain reason: a wrong option often comes from a different task statement than the one of the slot, and rule B6 asks what the complete guide names (decision 0005). A slice is not sufficient for that.
- **The reasons of the options go to call 4b.** Decision 0012 says that the checker does not get the notes or the reasoning of the writer. This part is a change of decision 0012, not an addition. The reasons of the options are not private notes. They are a part of the answer key that a participant reads (decision 0029), and rule B3 checks them.
- **No confidence number.** Decision 0019 said that the design of step 4 must decide this (4.6-S3). That point teaches a check in which the model reports confidence with each finding. For now, this design does the opposite of the point. The guide calibrates confidence with "labeled validation sets": "Field-level confidence scores calibrated using labeled validation sets for routing review attention" (5.5-K3). The guide wrote that point for the extraction of data. We have no such labels before the owner marks mock 1 (decision 0022). Until then a number has no meaning. The verdict "cannot decide" already shows doubt.
- **A new try is checked fresh.** Plain reason: a checker that sees the earlier findings can look only for those findings. This is an assumption of the assistant. It is not checked.

Not decided yet:

- The exact text of the two requests.
- The model of each call, and if it is the same model as the writer.
- A finding of call 4b has one `letter`. A question with 2 correct answers can need two.
- The test of call 4a covers questions with one answer only, because all 12 sample questions have one answer.
- If a confidence number is added after the owner marked mock 1.

## How we decided

The assistant showed the proposal. The owner did not understand it. The assistant then told it as the story of one question: a model answers as a student does, code compares, a second call checks as a teacher does, and code makes the verdict.

The owner asked: the model that answers as a student can be wrong, as a student who does not know the answer. What then? The answer is in the Reason: the two kinds of error and their cost, and the test with the 12 sample questions. The owner then accepted the two calls.

The assistant then asked if call 4b runs when the blind answer is already different from the marks, and suggested yes. The owner said yes.

The owner approved the proposal in the chat. The owner did not see the two forms and did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

4.6-K1, 4.6-K2, 5.5-K3, 4.6-S3, 4.3-S5, 4.1-K1, 1.4-K2
