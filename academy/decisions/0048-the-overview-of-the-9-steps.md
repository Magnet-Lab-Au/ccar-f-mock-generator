# 0048: The overview of the 9 steps is one story paragraph and a short caption

- Date: 16 October 2026
- Status: accepted. Built in `academy/build/make-behind-the-mocks.py`.
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0046 (the bridge of the overview, and Fig. A, its caption and the section "The 9 steps" that stayed as they were)

## Question

The section "Then, we built it in 9 steps" had a bridge, then Fig. A, then a caption of 7 sentences. Is this the best overview of the steps for the goals and the story tone of tab 2?

## Decision

1. One story paragraph before Fig. A carries the design idea: "With the truth settled and the tools chosen, we built the pipeline. It makes a mock in 9 steps. We let code move each try through the steps, and a Claude model write and check. Only one way back is automatic: a try that fails step 3 or step 4 goes to step 5, where the writer tries again, up to 3 times. Every other way back waits for a decision of the owner, and the owner accepts the mock before step 8."
2. The caption of Fig. A is short: "The 9 steps. The form of each box shows who does the step: code, a Claude model, or the owner. Each box opens a short note."
3. The preview cards of the old caption move into the paragraph, with the same sources. "up to 3 times" gets the code card of the limit of tries.
4. Two details of the old caption move into the Depth of their step, each with its card: "Not drawn in Fig. A" (step 5) and "Rewrites after the marks", since mock decision 0045 (step 7). The build stops if either is missing.
5. The box popups of Fig. A do not change.

## Reason

The bridge and the old caption said the same thing twice. The caption listed exceptions and decision numbers in the tone of a manual. The design idea was hidden: only one way back is automatic, and every other way back needs the owner. A leader sees judgment in it, and a learner sees the exam idea of bounded retries and escalation.

## How we decided

The owner asked: "Base on our goals is this the best way to start the 9 steps?", about the old caption. The assistant first recommended a shorter caption and moving the details. The owner said that the question was about the whole overview: "In the 9 steps section we start with this paragrapgh "With the truth settled..." and then show figure A. After the diagram comes this paragrapgh "Code moves each try through the steps...."", and asked to pay attention to the preview cards. The assistant recommended one story paragraph before the figure and a short caption, with no card lost. The owner said: "yes, build it". The build first lost the card of the rewrites after the marks, because a marker did not match. The assistant found it by a comparison of the cards before and after, fixed it, and added a check.

## Exam guide points

None.
