# 0063: Tab names in place of "tab 1" and "tab 2"

- Date: 20 October 2026
- Status: accepted
- Text confirmed by the owner: 20 October 2026, after the full review of the portal (item 17). The owner saw each old and new text below and said yes.
- Diagram: none
- Changes: none. It follows decision 0061 (the tab bar in the owner's order).

## Question

The portal now has five Academy tabs, in the order Start here, Exam guide breakdown, Study with Claude, Exam traps, Behind the mocks (decision 0061). The text of the two tabs made here still says "tab 1" for the Exam guide breakdown and "tab 2" for Behind the mocks. In the portal, the Exam guide breakdown is the second tab and Behind the mocks the fifth. What do these words become?

## Decision

1. The text names the tab. Both forms change, the page that opens alone and the portal form:

   | Tab | Old | New |
   |---|---|---|
   | Exam guide breakdown | "(tab 2)" | "(Behind the mocks)" |
   | Exam guide breakdown | "Step 2 of tab 2 tells why" | "Step 2 in Behind the mocks tells why" |
   | Exam guide breakdown | "leaves 2.5 out of tab 2" | "leaves 2.5 out of Behind the mocks" |
   | Exam guide breakdown | "the build in Claude Code on tab 2" | "the build in Claude Code in Behind the mocks" |
   | Exam guide breakdown | "Tab 2 shows them under 1.7" | "Behind the mocks shows them under 1.7" |
   | Exam guide breakdown | "use the words of tab 2" | "use the words of Behind the mocks" |
   | Exam guide breakdown | "Glossary of tab 2 →" | "Glossary of Behind the mocks →" |
   | Behind the mocks | "on tab 1 give the answer" | "in the Exam guide breakdown give the answer" |
   | Behind the mocks | "Tab 1 explains them →" | "The Exam guide breakdown explains them →" |
   | Behind the mocks (popup) | "We compared each part of tab 1 with a copy of the documentation of 14 October 2026." | "We compared each part of the Exam guide breakdown with a copy of the documentation of 14 October 2026." |
   | Behind the mocks (popup) | "Tab 1 has 23 boxes in 15 parts." | "The Exam guide breakdown has 23 boxes in 15 parts." |
   | Behind the mocks (30 links) | "Task statement 1.1 on tab 1 →" | "Task statement 1.1 in the Exam guide breakdown →" |

2. Code comments, the records and the old page builders (`-v1-old` to `-v3-old`) keep "tab 1" and "tab 2". Readers do not see them.
3. The change goes to the portal as the tag `pages-v10`.

## Reason

A number no longer says which tab is meant: the portal has five tabs, and the numbers 1 and 2 match neither their place in the tab bar nor the names a reader sees.

## How we decided

The full review of the portal on 20 October 2026 (four agents) found the tab numbers. The portal session listed each place with its old and new text, and the owner said yes to the text. The search covered the visible text of both forms, with tags and scripts taken out. Three more texts with "tab 1" are in the script of Behind the mocks: two popup sentences and the links "Task statement N.N on tab 1 →". They were not in the first list, so the portal session showed them to the owner separately, as rule 37 asks. The owner said yes to them too, the same day.

## Exam guide points

None.
