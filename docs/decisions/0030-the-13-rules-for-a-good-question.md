# 0030: The rules for a good question (13 rules, and 17 after decision 0037)

- Date: 6 October 2026
- Status: accepted. Decisions 0043, 0053 and 0055 add rules B7, A12 and B8.
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Changed: 6 October 2026, with the answers of decision 0037 and the corrections of the review. No independent reviewer checked the changed text.
- Changed: 7 October 2026, to describe the control of decisions 0038 and 0039, and with the corrections of the second review.
- Diagram: none. The diagrams of steps 3 and 4 will show the rules.

## Question

Decision 0029 says that the writer gets a list of rules for a good question, and that the checker uses the same list. Decisions 0011 and 0012 left the list open. What are the rules?

## Options

1. One list in two groups: rules with an exact answer, and rules that need judgment.
2. A different list.

## Decision

Option 1. The list had 13 rules. Decision 0037 added rules A8 to A11, so the list has 17 rules. The writer of step 2 gets all 17. The code check of step 3 checks group A. The model check of step 4 checks group B.

### Group A: rules with an exact answer

| # | Rule |
|---|---|
| A1 | The form is complete: a question, and each option has a text, a mark and a reason. |
| A2 | The number of options agrees with the slot (4 or 5). |
| A3 | The number of correct options agrees with the slot (1 or 2). |
| A4 | No two options have the same text. |
| A5 | No text names a letter or a different option: no "Option B", no "all of the above", no "none of the above". |
| A6 | The length of the question and of each option is in a range. A script takes the range from the 12 sample questions of the guide. |
| A7 | The correct option is not much longer than the wrong options. |
| A8 | The text of the question ends with a question mark. |
| A9 | The text of the question has 2 to 5 sentences. |
| A10 | Each option is one sentence. |
| A11 | The question is not a negative question. The question text does not have "NOT" or "EXCEPT" in capital letters. The last sentence of the question text does not have "not" or "except" in small letters. The options do not count (decision 0038, part 8). |

Each of the 60 questions has the line that says how many answers to select: "Select 1." or "Select 2." The line is the field `select` of the question record. It is not a part of the question text. Code copies it from the slot. So no rule is necessary for that line, and rule A6 does not count it (decision 0037, item 1).

### Group B: rules that need judgment

| # | Rule |
|---|---|
| B1 | Each option that is marked correct is correct, and no other option is correct. |
| B2 | Each wrong option is wrong for a reason that the guide gives, and its reason says so. |
| B3 | Each reason is true and agrees with the guide. |
| B4 | The question tests the point of its slot. |
| B5 | The question is inside the story of its scenario and does not contradict it. |
| B6 | No text depends on a feature that the guide does not name (ruling 1). |

### Rule B6 in detail (decision 0037, item 8)

- A feature is a thing of a Claude product or of MCP that has a name: a tool, a command, a flag, a parameter, a field, a file or a setting. Examples: `tool_choice`, `CLAUDE.md`.
- A name that the question invents for its story is not a feature. Example: a tool `get_customer` of the company in the scenario.
- General technology is not a feature. Example: Python.
- "Named" means: the name is in the text of `reference/guide-records.json`. Code decides this, not the model.
- The model check of step 4 lists each feature name that the question, the options and the reasons use. Code searches each name in the records file. Code ignores capital letters, and it treats a hyphen, an underscore and a space as the same. A name that is not found makes rule B6 fail.
- The rule is more strict than the words of ruling 1. The ruling says "depends on". This rule fails a text that only uses such a name. That agrees with decision 0007.

### One instruction with no check

The writer gets one more instruction: the options of a question have the same form. Example: all are actions, or all are places, or all are causes. It needs judgment, and no step checks it. The owner sees it in step 7 (decision 0037, item 12).

### Not in the list

- Ruling 2 (at most one wrong option on self-reported confidence in each scenario) and a scene that repeats. One question cannot show them. Step 6 checks them (decision 0014).
- Vague rules, for example "the question is plausible" or "the question has the right level".

## Reason

- **Exact rules, not vague rules.** The guide wrote this point for the review of code: "The importance of explicit criteria over vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate")" (4.1-K1). Here it applies to the rules for a question.
- **Two groups.** Decisions 0011 and 0012 have the reason: code checks a rule that has one correct answer, and a model checks a rule that needs judgment.
- **A1 to A3.** They follow from the form and the slot of decision 0029. The design does not rely on the form for a count (decision 0029).
- **A4.** Plain reason: two equal options are one option.
- **A5.** Plain reason: code mixes the options and gives the letters (decision 0029). A text that names a letter or the position of an option becomes wrong.
- **A6.** Decision 0011 names a length range as an example of a code rule. The range comes from the sample questions, because they show the form of the exam (Section 9 of the guide).
- **A7.** Plain reason: a participant can guess the answer from its length.
- **A8 to A11.** A script measured the 12 sample questions of the guide: `docs/decisions/0037-check-sample-properties.py`. Each of the four properties is true for all 12. The sample questions show the form of the exam (Section 9). A limit: 12 questions are a small set.
- **The line "Select N."** The guide says: "each item states how many responses to select" (Section 3). Code copies the line from the slot, so it cannot be missing or wrong.
- **B1 and B2.** Decision 0012 names them as examples of rules that need judgment.
- **B3.** Decision 0007: a participant learns most from the explanation. In this build the explanation is the reasons of the options (decision 0029).
- **B4 and B5.** Each slot names one point and one scenario (decision 0027). A question that does not test its point, or that is outside its story, does not fill its slot.
- **B6.** Ruling 1 of the owner (decisions 0005 and 0007). The plain reason that code decides "named": a false fail costs one new try, and a false pass puts a bad question into a mock. The guide says, for the workflow of an agent, that prompt instructions alone have a non-zero failure rate (1.4-K2, in decision 0009). The guide wrote that point for the order of the steps of a workflow, for example identity verification before financial operations. Here it supports a text search by code. A limit: call 4b lists the names by prompt, so a name that call 4b does not list passes. Code does not know if two names are related. It only reports that a name is not in the guide. The writer of step 5 finds the word of the guide.

Not decided yet:

- If rules A8 to A11 change after the test of decision 0024.
- How often the exact search of rule B6 gives a false fail.
- Rule B6: a part of a word against a complete word, a plural, the characters `--`, and the 5 texts of the records file with a backslash. Also if a name on the list "out of scope" of Section 17 counts as named. The search covers the complete records file, so now it counts as named.

## How we decided

The assistant showed the 13 rules in one proposal, with the source of each rule. The owner said yes.

The owner approved the rules in the chat. The owner did not confirm the full text of this file. No independent reviewer checked this file.

## Exam guide points

4.1-K1, 1.4-K2
