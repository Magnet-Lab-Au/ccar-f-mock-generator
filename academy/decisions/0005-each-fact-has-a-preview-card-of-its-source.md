# 0005: Each fact has a preview card of its source

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

The repository becomes public (decision 0003). A reader who goes deep can check the work in it. How does a page show where each fact comes from?

## Options

1. A table of links at the end of each entry.
2. A short link in brackets after each fact, for example "[decision 0053]".
3. A plain hyperlink on the fact.
4. A preview card on the fact.

## Decision

Option 4. A fact, for example "37 of 52", has a light dotted underline and no other mark. On hover, or on a tap on a phone, a small card opens. The card shows a short excerpt from the source: the sentence of the decision, a few lines of code, or the number from the run record. At the bottom, the card has one link: "Open in the repository". A link to code goes to the exact lines.

A script takes each excerpt from its source file, so the excerpt always agrees with the source.

## Reason

The owner rejected option 1: people glance at a table and do not read it, and a column "what it proves" sounds like a sales pitch. The owner rejected option 2: the brackets distract.

Against option 3: a plain link opens a raw file. A run record is a JSON file in the folder `runs/`, with 1,573 files in its subfolders. The reader leaves the page and gets nothing readable.

For option 4: the reader sees the evidence without leaving the page, and the excerpt is readable. The raw file is there for the reader who wants it. The diagrams already use popups, so the reader learns one pattern for the whole portal.

The cost: somebody must choose and check the excerpt of each card.

## How we decided

The owner preferred hyperlinks, and asked the assistant to think and not only take that solution. The assistant looked at where a link goes, and suggested the preview card. The owner said "Yes. I suppose so." The first real page tests the cards. If they do not work on a real page, the owner and the assistant change them.

## Exam guide points

none
