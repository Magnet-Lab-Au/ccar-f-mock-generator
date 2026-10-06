# 0031: The design of step 3: the code check and its verdict record

- Date: 6 October 2026
- Status: accepted
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Diagram: `docs/diagrams/05-step-3-check-by-code.html`

## Question

Decision 0011 says that code checks each question against the rules that have an exact answer. Decision 0030 gives those rules: A1 to A7. What does step 3 receive and return, and what are the numbers of rules A6 and A7?

## Options

1. One proposal of the assistant with the exact record and the exact numbers.
2. A different design.

## Decision

Option 1.

### The contract of the step (decision 0018)

- It receives one question record and its slot.
- It checks rules A1 to A11 of decision 0030. Decision 0037 added rules A8 to A11.
- It returns one verdict record, as a new file. Example: `runs/mock-01/checks/M1-S17-T1-step3.json`.
- It can fail when the file of the question is missing or cannot be read. Then the step reports an error. It never returns "pass" for a question that it did not read.

### The verdict record

| Field | Example |
|---|---|
| `question_id` | `M1-S17-T1` |
| `step` | `3` |
| `verdict` | `pass` or `fail` |
| `findings` | A list. Each finding has the form of decision 0037, item 4: `step`, `rule`, `detail`, `letter`, `point`, `other_questions`. Example: step `3`, rule `A6`, detail "The question has 140 words. The limit is 110." |
| `fingerprint` | The fingerprint of the question record that the step checked (decision 0036) |
| `date` | The date of the check |

### The numbers

| Rule | In the 12 sample questions of the guide | Limit |
|---|---|---|
| A6, the question | 33 to 91 words | 25 to 110 words |
| A6, each option | 7 to 35 words | 5 to 45 words |
| A7, the average number of words of the correct options against the average number of words of the wrong options | At most 1.21 times | At most 1.3 times |
| A8, the end of the question text | Each of the 12 ends with a question mark | The text ends with a question mark |
| A9, the sentences of the question text | 2 to 5 sentences | 2 to 5 sentences |
| A10, the sentences of an option | Each of the 48 options is one sentence | Each option is one sentence |
| A11, a negative question | No sample question has the word "not" or "except" | The text does not have "NOT" or "EXCEPT" in capital letters. The last sentence does not have the word "not" or "except" |

The method for sentences is simple: a sentence ends with ".", "?" or "!" and a space comes after it. It can count wrong when a text has an abbreviation with a dot.

Rule A6 counts the question text only. It does not count the line "Select N." (decision 0037, item 1).

### Other parts

- A question with the status `cannot_write` does not go to step 3. The slot gets the status `open` (decision 0037, item 5).
- A question that fails goes to step 5 with its findings (decision 0013).

## Reason

The reason for a code check is in decision 0011. This decision uses no new exam guide point.

- **A new file for the verdict.** Plain reason: no file is written over, so the record of each check stays (the same reason as for one file for each try, decision 0029).
- **The findings name the rule and the detail.** Decision 0013: the writer of step 5 gets the exact findings. A finding with no detail does not tell the writer what to change.
- **An error is not a pass.** Decision 0011 uses the guide for this (5.3-K4): an empty result must not pass as a success. The guide wrote that point for errors between the agents of a multi-agent system.
- **The numbers.** Each limit is the range of the 12 sample questions of the guide, with a small margin. The sample questions show the form of the exam (Section 9). A script measured them, and all 12 pass the limits: `docs/decisions/0031-check-sample-lengths.py`. The size of the margin is a choice of the assistant. It has no source. Rules A8 to A11 have no margin: a second script measured the four properties, and each one is true for all 12 sample questions (`docs/decisions/0037-check-sample-properties.py`).

Not decided yet:

- The exact list of words for rule A5. The check script uses a first list.
- If the numbers change after the test of decision 0024.

## How we decided

The assistant showed the proposal with the numbers from the script. The owner said yes.

The owner approved the proposal in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

5.3-K4
