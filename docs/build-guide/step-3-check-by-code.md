# Step 3: check by code

Status: built. It ran in the test before the first full run, on 7 October 2026.

Diagram: [`05-step-3-check-by-code.html`](../diagrams/05-step-3-check-by-code.html)

## What the step does

Before a model looks at a question, code checks the 12 rules that have one exact answer (rules A1 to A12):

- The form is complete, and the numbers of options and of correct options agree with the slot.
- No two options have the same text, and no text names a letter or a different option ("Option B", "all of the above").
- The question has 25 to 110 words and each option 5 to 45 words. The correct option is not much longer than the wrong options.
- The question ends with a question mark and has 2 to 5 sentences. Each option is one sentence.
- The question is not a negative question.
- On most slots, a wrong option is the longest option (rule A12, decision 0053). The plan lets the longest option be correct on 13 of the 52 slots with 1 answer and on 3 of the 8 slots with 2 answers, the chance numbers. In mock 1, before this rule, the correct option was the longest in 37 of 52 questions.

A script measured the 12 sample questions of the guide. The length limits (A6 and A7) are their range with a small margin. Rules A8 to A10 are true for all 12 with no margin. The limit of A11 is weaker than what the script measured: it permits "not" outside the last sentence. The check is cheap and fast, so a question with a simple defect does not use a model call.

Each finding names the rule and the detail, so the writer of step 5 knows what to change. If code cannot read a question, it reports an error. It never says "pass" for a question that it did not read.

## The test run

All 10 questions of the writer passed the 11 rules of that time (rule A12 came later). A test of the code also showed that the 12 sample questions of the guide pass the rules A4 to A11 (the rules that need no slot and no reason for each option).

## The exam guide points that the step uses

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
| 1.4-K1 | "The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering" | Task statement 1.4: Implement multi-step workflows with enforcement and handoff patterns | Written for the order of the steps of an agent workflow. Here: a rule with one exact answer is checked by code, not by a model. |
| 1.4-K2 | "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate" | Task statement 1.4: Implement multi-step workflows with enforcement and handoff patterns | The same context. Here: an instruction to a model can fail, so code checks the rules that code can check. |
| 4.3-K3 | "That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)" | Task statement 4.3: Enforce structured output using tool use and JSON schemas | Written for the extraction of data. Here: the form of the answer does not stop content errors, so code checks the content. |
| 4.4-K4 | "The difference between semantic validation errors (values don't sum, wrong field placement) and schema syntax errors (eliminated by tool use)" | Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality | The same context. Here: the same difference between errors of format and errors of meaning. |
| 5.3-K4 | "Why silently suppressing errors (returning empty results as success) or terminating entire workflows on single failures are both anti-patterns" | Task statement 5.3: Implement error propagation strategies across multi-agent systems | Written for errors between agents. Here: an error must never look like a pass. |
