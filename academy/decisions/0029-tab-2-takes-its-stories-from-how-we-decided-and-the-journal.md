# 0029: Tab 2 takes its stories from "How we decided" and the journal

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none

## Question

`HANDOFF.md` says: "The build guide does not use the section 'How we decided', and it does not tell the history of the first build." Tab 2 promises to show "where the design failed, what we learned, and how the system improved". Can tab 2 use the "How we decided" sections and the journal?

## Decision

Yes. Tab 2 takes its stories from the "How we decided" sections of the decisions and from the journal. If a fact of a story is also in a higher source of the order of trust (decision 0011), such as the code, a run file or the decision text, the page uses the higher source.

The rule of `HANDOFF.md` stays for the build guide only.

## Reason

The build guide describes how the builder works today, so it leaves out the history. Tab 2 tells the history, and it is written only in these two places. Example: the review loop story of the 1.1 sample quotes the owner: "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." The quote is in the "How we decided" section of mock decision 0038. Its counts, 14 serious items and then 10 new ones, are in the Question section of the same decision, a higher source.

## How we decided

The independent review of the plan found the conflict. The owner found the first question hard to understand. The assistant explained it with the example of mock decision 0038. The owner accepted it.

## Exam guide points

none.
