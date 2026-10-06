# 0033: The design of step 5: the new try, its request and the limit of 3 tries

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Diagram: `docs/diagrams/07-step-5-try-again.html`

## Question

Decision 0013 says that a failed question goes back to the writer with the findings, up to a limit of tries. It left open the limit and who decides on an open slot. What is the design of step 5?

## Options

1. One proposal of the assistant with the exact request, the limit and the report.
2. A different design.

## Decision

Option 1.

1. **The request.** It is the request of step 2 (decision 0029), plus two parts: the failed question and the list of its findings. Code shows the failed question with the letters that the checker saw. So a finding that names a letter is clear (decision 0037, item 11).
2. **The answer.** The model answers in the same fixed form as in step 2. It can also answer `cannot_write`. Then the slot gets the status `open` immediately (decision 0037, item 5).
3. **A finding.** Code converts each finding into one form before the writer gets it (decision 0037, item 4). The findings come from step 3, step 4, step 6 or the owner in step 7.

| Field | Content | Example |
|---|---|---|
| `step` | 3, 4, 6 or 7 | `4` |
| `rule` | The rule that failed. For a bad mark or a `rewrite` of the owner: `owner` | `B1` |
| `detail` | What is wrong | "Option C is also correct." |
| `letter` | The option that the finding is about, or empty | `C` |
| `point` | The guide point that the finding uses, or empty | `1.2-K2` |
| `other_questions` | The IDs of other questions that the finding names. Only step 6 fills it. | `M1-S04-T1` |

   When `other_questions` has an ID, code adds the text of that question to the request.
4. **Which try the writer sees.** Only the last failed try and its findings. It does not see the tries before that.
5. **The new record.** A new question record with the next try number. Example: `M1-S17-T2`. The record of the earlier try stays. Code mixes the options of the new try and gives them new letters. The new letters have no connection with the old letters.
6. **After the new try.** The question goes through steps 3 and 4 again (decision 0020).
7. **The limit.** 3 tries for one slot: the first question and 2 new tries. A second rule also stops a slot: the checker says "cannot decide" two times (decision 0023). The two results do not have to come one after the other. The rule that applies first stops the slot (decision 0037, item 6).
8. **A slot that comes back.** Each time step 6, step 7 or the owner sends a slot back, the slot gets 3 new tries, and the count of "cannot decide" starts at zero. The try numbers continue: T3, T4, T5 (decision 0037, item 7).
9. **An open slot.** A slot that a rule stops gets the status `open`. The report of the run names the slot, the number of its tries and the field `open_reasons`. That field names each cause that applies: `three_tries`, `cannot_decide_twice` or `cannot_write`. The records of the tries and of their checks have the findings. The mock is not complete, and the other slots continue.
10. **The decision of the owner.** The owner answers with one command. Code saves the decision in `runs/mock-01/owner-decisions.json`, with the fields `id`, `action`, `reason` and `date`. The owner does not edit a file in `runs/`. The actions for an open slot:

| Action | What the program does |
|---|---|
| `new_point` | Code selects a different point of the same task statement. The slot gets 3 new tries. |
| `more_tries` | The same slot gets 3 new tries. |
| `new_plan` | This mock stops. A new seed makes a new plan. |

    The actions `ignore` and `rewrite` of steps 6 and 7 go into the same file (decisions 0034 and 0035).

### The status of a slot (decision 0037, item 2)

The current try of a slot is the try with the highest number. Older tries are history, and no step uses them again. Code calculates the status of a slot from the records each time. No file stores it.

| Status | Meaning |
|---|---|
| `to_write` | The slot has no question yet. |
| `to_check` | The current try has not passed steps 3 and 4. |
| `passed` | The current try passed steps 3 and 4. |
| `open` | A rule stopped the slot, and the owner decides. |

### The report of the run (decision 0037, item 10)

Code builds `runs/mock-01/report.json` from the records at the end of each run. Nobody edits it.

| Field | Content |
|---|---|
| `mock`, `date` | Which mock, and when code built the report |
| `state` | `in_work`, `waits_for_owner`, `ready_to_mark`, `stopped` or `built` |
| `slots` | For each slot: `slot_id`, `status`, the current question ID, the number of tries and `open_reasons` |
| `step6_cannot_decide` | The results "cannot decide" of step 6 (decision 0034) |
| `errors` | For each call that failed 3 times: the step, the ID and the cause |

A new start of the program continues from the records. It does not start the mock from zero.

### The contract of the step (decision 0018)

- It receives the slot, the question record of the last failed try and its findings.
- It returns one new question record.
- It can fail in the same way as step 2: the API call fails, or the answer is not a complete form. Then code runs the same call again, at most 3 times. These are not tries of the slot. After that, no record is saved, the call goes into the list `errors` of the report, and the other slots continue (decision 0037, item 10).

## Reason

- **The failed question and the exact findings go back to the writer.** Decision 0013 has the reason. The guide wrote these points for the extraction of data: "Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction" (4.4-K1). "Implementing follow-up requests that include the original document, the failed extraction, and specific validation errors for model self-correction" (4.4-S1).
- **The same form.** Plain reason: steps 3 and 4 check each try in the same way, so each try must have the same form (4.3-K1, in decision 0029).
- **Only the last failed try.** The guide names three parts for a new try: the original, the failed result and the errors (4.4-S1). It does not name the complete history. The plain reason: the request stays short, and the writer corrects the question that is on the table.
- **The limit of 3.** The guide gives no number. The number 3 is a guess of the assistant. It has no source. It can change after the test of decision 0024. Decision 0019 has the reason for a limit: with no limit, a slot that cannot pass makes the program try with no end. The guide says that some errors do not go away with a new try: "The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)" (4.4-K2).
- **The limit is not the main way to stop.** The main way to stop is a question that passes the checks. The guide names the opposite as an error, in the context of agent loops: "setting arbitrary iteration caps as the primary stopping mechanism" (1.1-S3).
- **The report and the owner.** Plain reason: a slot that the program cannot fill needs a decision of a person, and the person needs each try and its findings to decide.
- **One form of a finding.** Plain reason: the writer can correct only what it can see, and one form needs one piece of code.
- **The status is calculated.** One true copy, as in decision 0016. A stored status can disagree with the records.
- **`cannot_write` opens the slot.** Plain reason: the same request with the same slot probably gets the same answer.
- **A call that fails is not a try.** Plain reason: the question did nothing wrong. The number 3 for these runs is a guess of the assistant. It has no source.

Not decided yet:

- The exact meaning of each value of `state` in the report.
- The name of the command of the owner.
- An automatic path for a `cannot_write` slot. The test of decision 0024 shows if it is necessary.

## How we decided

The assistant showed the proposal. The owner said yes, and asked if the answer of step 5 is also structured output. The answer: yes, it is the same fixed form as in step 2.

The owner approved the proposal in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

4.4-K1, 4.4-S1, 4.4-K2, 1.1-S3, 4.3-K1
