# 0027: The copy of the exam guide matches the official PDF

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none

## Question

Tab 1 quotes the exam guide exactly, from `reference/exam-guide.md`. `HANDOFF.md` lists as open: "`reference/exam-guide.md` is not compared with the original, character for character." How do we know that the quotes are exact?

## Decision

A script compares the copy with the official PDF once, before tab 1 is built. The owner gave the PDF. It is `academy/sources/exam-guide-v1.0-official.pdf`, and the script is `academy/sources/compare-exam-guide.py`.

The script makes both files into one list of words and lists each place where the two lists differ. It removes only what is not text of the guide: the Markdown marks of the copy, and the running headers, the page numbers, the list bullets and the line breaks of the PDF. It replaces the "fi" and "fl" ligatures of the PDF.

The result on 13 October 2026: 11,157 words in each, and 0 places that differ.

## Reason

A quote that is not exact is a wrong fact. The copy is the source of each quote of tab 1 (decision 0011).

## How we decided

The independent review of the plan raised it. The assistant recommended a script and asked for the original. The owner put the PDF in the repository. The assistant moved it to `academy/sources/`, wrote the script and ran it. The first runs listed only differences of format, such as list bullets, running headers, escaped marks and links. The assistant added a rule for each kind, and then no difference was left.

## Known limits

- The script compares words, not spaces, line breaks, the order of table cells or the layout.
- It depends on the text that the library pypdf takes from the PDF.
- The script does not change `reference/` (working rule 27).

## Exam guide points

none.
