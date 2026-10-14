# 0042: A box gives the exam answer and the product today

- Date: 14 October 2026
- Status: accepted
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0039, item 10 (the label "Guide only"). The label stays for the other places.

## Question

In some places of tab 1, a fact of the product differs from a point of the guide, and the page does not say which answer the exam expects. What does the page show there?

## Decision

1. A box follows the paragraph. It has two lines:
   - **For the exam:** the answer of the guide, in one line.
   - **The product today:** one line, and a link "Detail in the Depth".
2. The facts of the product, with their cards, move from the Explanation to a list "The product today" at the top of the Depth of the part. The list says that the facts come from the documentation of 14 October 2026, and that the exam answer is the answer of the guide.
3. The box says "The product today", not "changed since the guide". The guide is version 1.0, effective July 2026. Many of these facts were true before then. For most places, the documentation does not say when the product changed.
4. A box goes only where the product fact could lead a candidate to a different exam answer. Where the documentation only uses other words or says nothing, the label "Guide only" stays.
5. The top of tab 1 explains the box once, below the explanation of the label "Guide only".

## Reason

The checks B1, B2, B3, B4 and C1 of decision 0041 found the same weakness: a candidate who remembers the product fact can choose the wrong exam answer. The move to the Depth keeps each part inside the word limits of decision 0026. Before the change, the Explanations of 1.3, 2.3 and 3.6 had 497 to 500 of their 500 words. The move also follows the B3 result: the caveats of the product compete with the exam point in the 3-minute level.

## How we decided

The assistant recommended one line, "For the exam: answer as the guide says", in each place. The owner said: "yes, add it but is that we should say how the product has changed since the guide was written and this is the answer for the exam and this is the current product in reality". The assistant said that "changed since the guide" is mostly not true and cannot be checked for most places. It also said that three parts would go over the word limit. It recommended the box with the two lines, and the move of the detail to the Depth. The owner said: "yes, build it that way".

## The places

23 boxes in 15 parts: 1.3 (allowedTools and the Agent tool), 2.3 (three boxes: the number of tools, tool_choice in the Overview, and narrow tools against joined tools), 2.4 (the local scope, tool search, resources), 2.5 (Edit with text that is not unique, Grep and Glob), 3.1 (/memory and /context), 3.2 (commands and skills, allowed-tools and argument-hint), 3.3 (a read loads a path rule), 3.4 (the Plan subagent), 3.5 (2 or 3 examples), 3.6 (`--bare`), 4.1 (report everything, severity in prose), 4.2 (2 to 4 examples), 4.3 (two boxes: tool use against structured outputs, tool_choice), 4.5 (server tools in a batch), 4.6 (extended thinking). Fig. 4.3-1 says the same in its two notes. The Explanation of 2.3 has no second box for tool_choice, because the box of the Overview is above it, and a second box put the Explanation over its limit.

The review of this change found the boxes of 2.3 (narrow tools) and 2.4 (the local scope), and the assistant added them.

No box, because the product fact gives no different answer: 3.5-K1 and 4.2-K1 ("one of the most reliable ways"), 3.6-K2 ("validated"), 4.2-K3, and the exception of bypass permissions in 3.4.

## Exam guide points

1.3-K1, 2.3-K1, 2.3-S2, 2.3-S4, 2.3-S5, 2.4-K1, 2.4-K3, 2.4-K4, 2.4-S5, 2.5-K4, 3.1-S4, 3.2-K1, 3.2-S3, 3.2-S4, 3.3-K2, 3.4-K4, 3.4-S3, 3.5-S1, 3.6-K3, 4.1-K2, 4.1-S3, 4.2-S1, 4.3-K1, 4.3-K2, 4.3-S2, 4.3-S3, 4.5-K3, 4.6-K2.
