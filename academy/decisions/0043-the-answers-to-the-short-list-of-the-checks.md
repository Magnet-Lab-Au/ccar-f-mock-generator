# 0043: The answers to the short list of the checks

- Date: 14 October 2026
- Status: accepted
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0039, item 10 (the label "Guide only" gets a popup). The choice of 14 October 2026 that wide figures scroll sideways on a phone (academy journal, 14 October 2026), for 7 figures.

## Question

The list of the checks (`academy/checks/findings.md`) is too long for the owner to read. Which of its items does the assistant build?

## Decision

The owner answered one item at a time. The assistant builds all of them after the last answer.

1. The guide and the product. Done in decision 0042.
2. A primer at the top of tab 1: one picture of the products (Claude API, Claude Code, Agent SDK, MCP) that shows who runs the tools, and a glossary of about 10 terms. The JSON example of a tool call that check C1 also asked for is not part of it.
3. The phone layout. On a phone, 4 figures stack vertically: 2.1-1, 3.2-1 and 4.1-1 (before and after) and 3.3-1 (live). The bar charts 4-2, 4-3 and 6-2 of tab 2 shrink to the width of the screen. The other figures still scroll sideways.
4. Tab 2 gets a short section near its end, "What this shows and what it does not": what was checked, what was not, the known limits, and the total cost. The assistant makes two of its own claims weaker. The top paragraph of the owner stays.
5. The popups: all 45 items of check D2. 18 new popups, and 27 weak popups written again so that each answers the question that D2 named.
6. Screen readers: a drawing with popups is a group, not one picture.
7. Facts at the wrong level: the facts of check B3 that crowd the Explanation move to the Depth, if decision 0042 did not move them already. Three exam points move up to the Overview: 1.5 (a PostToolUse hook cannot undo an action), 3.1 (CLAUDE.md does not enforce), 4.1 (turn off a noisy category).
8. Plain English: the 135 sentences of more than 25 words (85 on tab 1, 50 on tab 2) are split into shorter sentences with the same meaning. The top paragraph of the owner stays.
9. The label "Guide only" opens a popup that explains it, so that a reader who goes straight to a part understands it.

The work runs in six batches. After each batch: a build, `check-pages.js`, and one independent review agent. A push to GitHub needs a new yes.

After the eight items: the paragraphs that read as one long underline. Each sentence is a fact with its own card, and the parts have almost no sentences in their own words between the facts. The owner said to take this next.

## Built (15 October 2026)

All nine items are built, in six batches. After each batch, `check-pages.js` printed "All checks passed." for both tabs, and an independent agent reviewed the batch. The journal of the academy lists the review findings and their fixes.

- Item 4: a review found that the assistant had misread a test. `runs/test-0024/part3.json` gave two questions with a wrong answer key to call 4b alone, not to call 4a. So call 4a was never tested with a wrong answer key, as check C5 said. The section says so.
- Item 8: the count script finds 34 sentences over 25 words after the splits, against 151 before. The 34 are joins of table cells, captions and quotes, sentences that start with a number, and the paragraph of the owner.
- Not done: the Overview of 3.2 does not name context: fork (check B3). It is not one of the three points of item 7.

## Reason

The checks of decision 0041 found these items. The owner does not read the long list, so the assistant gave one recommendation for each item.

## How we decided

For each item, the assistant gave the context and one recommendation, and the owner answered:

- The popup of "Guide only": "yes, add the popup. But before you do that Take my decsions first for the rest of the items before implementing."
- The primer: "yes, add the primer section".
- The phone layout: "yes, change those 8 figures". The assistant then said that it had counted wrong: the check named 3 bar charts, not 4, so 7 figures change.
- Tab 2: "yes, add that section".
- The popups: "yes, fix all 45 popups".
- Screen readers: "yes, make the screen reader change".
- Facts at the wrong level: "yes, make those moves".
- Plain English: "yes, split all 135 sentences".

The assistant then gave the plan: six batches, about 8 agents, 4 to 6 hours. The owner asked why most paragraphs are underlined from start to end. The assistant said that the cause is mostly that each sentence is a fact with its own card, not STE. The owner said: "OKAY WE TACKLE THIS STRAIGHT AFTER THE 8 DECIDE ITEMS".

## Exam guide points

None.
