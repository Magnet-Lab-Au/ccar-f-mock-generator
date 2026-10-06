# 0008: The exam guide is the only source of facts in the first version

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 6 October 2026
- Diagram: none

## Question

From what text does the program take the facts of a question?

## Options

1. The exam guide only. Documentation can be added by a later decision.
2. The exam guide plus saved copies of official pages, from a fixed list that the owner approves.
3. A different set of sources.

## Decision

Option 1. In the first version, the program reads the exam guide only (`reference/exam-guide.md`). A fact can decide a question only if the guide states it.

The program reads each source as a saved file in the repository. It does not read the live web. So a later decision can add documentation as more saved files, with no new design.

## Reason

The exam tests the guide. Where the documentation and the guide disagree, the answer of the guide is the answer of the exam. The guide alone is sufficient for its own sample questions: the assistant checked four of the twelve (1, 2, 3 and 10). Each added source adds a step that can fail and that becomes old.

The cost: a question cannot use detail that is finer than the guide. If a first run shows that the questions are too thin, a new decision adds a second source, with the evidence of that run.

Not decided yet: if the program can use the course lessons or the digests of the first build. Some of those files are personal notes of the owner (rule 28).

## How we decided

The owner asked how option 2 would work. The assistant suggested this form. It is not decided:

- No web search. A fixed list of page addresses that the owner approves. The program downloads each page once and saves a copy with the link and the date.
- Official sources only: the Anthropic documentation, and the official MCP specification. Code enforces the list.
- Three checks: the source list, an exact quote that code finds in the saved copy, and no question where a page and the guide disagree.
- A limit: the checks prove that the page said so on that date. They do not prove that the model understood the sentence, or that the page is still current.

This decision is different from decision 5 of the folder `CCAR-F Mocks v2` (two source tiers).

## Exam guide points

none.
