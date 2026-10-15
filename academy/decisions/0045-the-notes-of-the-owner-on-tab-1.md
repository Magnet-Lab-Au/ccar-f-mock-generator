# 0045: The notes of the owner on tab 1

- Date: 15 October 2026
- Status: accepted
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0043, item 2 (the primer has a new heading). Decision 0010 (each part starts closed), for the 5 domains, "How we broke it down" and "Before you start". The task statements still start closed.

## Question

The owner checked tab 1 by hand and gave notes in batches. What changes on the page?

## Decision

Text:
1. The lead of tab 1: "This page breaks the CCAR-F exam guide into its 5 domains and 30 task statements. For each task statement, it explains what the exam expects, quotes the guide's own words, and shows where the product goes further. Use it to study one task statement at a time."
2. Two short sentences introduce the domains, and one paragraph introduces the scenarios and the two axes of a question.
3. Two paragraphs explain "Knowledge of" and "Skills in", each name in the colour of its label, with 4.3-K2 and 4.3-S2 as examples. The guide, not the page, puts each point in one of the two lists.
4. The three levels, the two marks ("Guide only" and the box), the block "The exam tests", and the three products and the protocol of the primer are lists. The sentence on the labels of the points has its own line.
5. A box for "New to the Claude API or Claude Code?".
6. The caption of Fig. B says what the table shows. The chip "primary" opens a popup. It says that the guide does not define the word. The reading of the page is that the questions of the scenario come mainly from these domains.
7. The primer heading: "Before you start: who runs the tools in each product".

Figures:
8. Fig. A: the exam, "Claude Certified Architect – Foundations", with the CCAR-F badge of the owner, on top. One thin trunk and one bar lead to a drop to each domain column, as thick as the weight of the domain. Each column has a line icon, its weight, its name and a one-line summary.
9. Fig. B: each scenario row opens the text of the guide under it, word for word, in paragraphs, with a dropdown arrow. A live graph of the two axes comes first. A large dot marks each primary domain, and a button for each scenario lights its primary domains. Each dot opens a small popup.
10. Fig. C: the drawings are in the middle of their cards. The five boxes that run the tools open a popup each, with a link to the part that teaches it.
11. Each Overview: the heading "Overview" in the style of the Explanation and the Depth, then the answer in body size, then the title of the guide, small.

Layout:
12. The hero image of the owner for each domain stands on the right of the summary of the domain, all at one height, with a transparent background. Dark mode shows a copy with cream outlines. `academy/build/make-dark-heroes.py` makes all copies from the originals.
13. Each domain, "How we broke it down" and "Before you start" open and close. The heading is plain text with a large orange chevron, and each starts open. "The exam guide on one page" stays as it is.
14. Marks next to headings: the notepad of the owner (tilted, with fewer and thicker lines) and the puzzle of the owner (solid cream in dark mode). A toolbox drawn for the primer goes next to its heading.

## Reason

The owner checked the page by hand and wanted it easier to read: fewer long paragraphs, pictures that break up the text, and controls that are clear.

## How we decided

The owner gave notes in batches, for example: "Before the scenario table, we need to introduce what scenarios are and explain how they sit on a second axis", "Each domain needs it's own tab and drop down with the v arrow like we did for the scenarios", and "I want it to not have borders and just be text on the page like before". For each note that needed a design, the assistant gave one recommendation and the owner answered. Some choices changed after the owner saw them. The lines of Fig. A were first curves, then right angles with their own heights, and then one trunk and one bar after a sketch of the owner. The domain images were first full width, then on the right at one height. The domains first started closed: the assistant recommended open, because Fig. A gives the overview and three clicks to the text is too many, and the owner said "yes, start them open". The first dark mode of the images had a white background, which looked bad, and the dark copies replaced it.

## Exam guide points

None.
