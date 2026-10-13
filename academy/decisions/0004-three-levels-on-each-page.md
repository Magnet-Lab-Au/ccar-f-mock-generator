# 0004: Three levels on each page

- Date: 12 October 2026
- Status: accepted. Decision 0010 changes the levels of "Behind the mocks" and the one visual in each Overview. Decision 0032 says where code appears. Decision 0019 says what each level holds.
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

The participants are senior engineers, directors of engineering and senior product managers. They have full-time jobs and little time. The cohort has 10 to 15 people now, and it grows. How much does a page show at first, and how does a reader get more?

## Options

1. One full page for each task statement.
2. Levels: a short overview first, and more detail only for the reader who wants it.

## Decision

Option 2. Each page of both sections has three levels:

| Level | Exam guide breakdown | Behind the mocks |
|---|---|---|
| 1. Overview, about 30 seconds | What the task statement is about, and one visual | The story in one or two sentences, and one visual |
| 2. Explanation, about 3 minutes | A plain explanation, the exact guide text, and what the exam tests | What happened, what went wrong, and the fix |
| 3. Depth, optional | Code and schemas in hover popups on the diagram | The decision text, the full diagram, and code in hover popups |

The pages show no code in the text. Code and schemas appear only in a hover popup on a diagram.

Each fact links to its source (decision 0005).

## Reason

The owner's reasons: the pages must hook the readers with things that interest them. The ideas must be simple, with many visuals, some of them animated. A reader who wants depth gets it step by step. A reader who does not gets an overview. Nobody can expect these readers to read lines of code.

A second reason of the owner: the portal also shows these readers the technical competence of the owner, if they choose to go deep.

The objection that we discussed: the brief makes the Exam guide breakdown required reading, 30 pages. That is too much for these readers if each page is long. With level 1, all 30 overviews take about 15 minutes. In the discussion the assistant said "about one hour". The independent review found that error.

## How we decided

The owner described the audience. The assistant suggested three levels. The owner added that code and schemas appear only in a hover popup, and asked if three levels are enough to show competence. The assistant suggested a fourth level, a table of links to the evidence. The owner said that such a table is hard to read and that its words sounded like a sales pitch. So the evidence became links on each fact (decision 0005), and the levels stayed at three.

## Exam guide points

none
