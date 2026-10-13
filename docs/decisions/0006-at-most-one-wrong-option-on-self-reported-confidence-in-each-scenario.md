# 0006: At most one wrong option on self-reported confidence in each scenario

- Date: 6 October 2026
- Status: accepted. Decision 0081 says how ruling 2 reads an option that acts only when the model is highly confident.
- Text confirmed by the owner: 6 October 2026
- Diagram: none

## Question

Does ruling 2 of the owner, of 29 September 2026, apply to the new build?

## Options

1. Yes, with the two limits of the original text.
2. Yes, with a change.
3. No.

## Decision

Option 1. In one scenario of one mock, at most one wrong option is the self-reported-confidence option. That option is: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger.

Two limits:

1. Calibrated confidence for each field, used to send items to human review, does not count. The guide endorses it (5.5).
2. The option does not count when it is the correct answer.

## Reason

This is ruling 2 of the owner, of 29 September 2026. The owner confirmed on 6 October 2026 that it applies, with the two limits.

The guide says that self-reported confidence scores are "unreliable proxies for actual case complexity" (5.2-K3), and sample question 3 in Section 9 uses such an option as a wrong option. So it is a fair wrong option. The plain reason for the limit of one: if the option appears many times, a participant can mark it wrong without thought.

The first limit comes from the guide: "Field-level confidence scores calibrated using labeled validation sets for routing review attention" (5.5-K3) is a practice that the guide teaches, so it does not count.

Not decided yet: how the program finds and counts this option.

## How we decided

The owner asked where the rulings are. The assistant then read the briefs of September 2026 in `CCAR-F Mocks v2/reference/first-build/rubric/` (`EDITOR.md`, `REVIEW2.md`, `REVIEW3.md`, `REVIEW4.md`). The assistant wrote those briefs. No file has the words of the owner. An earlier summary of the ruling did not have the two limits. The assistant suggested a general rule for repeated wrong options. That is not decided.

## Exam guide points

5.2-K3, 5.5-K3
