# MagnetLab Academy: MVP brief (from the Cowork discussion, 12 October 2026)

Do not write code or page content yet. We are still in discussion.

## How to work with the owner
- Discussion first. Raise one question at a time: a short context, your recommendation, then the question.
- Push back directly when you disagree. Do not draft anything until the owner asks.
- Plain, simple English. No em dashes. In documents, write "the owner", not a name.

## The outcomes, in order
1. The build guide works as a case study of the exam. The mock builder uses the exam's own patterns, so it teaches the exam on a real system. This is the MVP.
2. Every cohort member passes CCA-F. This comes after the MVP.

## MVP scope
Two sections, linked both ways: each task statement page links to its case study entry, and each entry links back.

1. Exam guide breakdown (required reading for everyone)
- A short introduction: what the exam guide is, the 5 domains and their weights, and how to read a task statement.
- 5 domain pages, each listing its task statements.
- 30 task statement pages (1.1 to 1.7, 2.1 to 2.5, 3.1 to 3.6, 4.1 to 4.6, 5.1 to 5.6). Each page has the guide's own text, quoted exactly, and a plain-language explanation.
- Diagrams only where there is a mechanism to show: about one per domain, plus 8 to 10 for task statements such as the agentic loop and stop_reason (1.1), hub and spoke (1.2), when a hook runs (1.5), the CLAUDE.md hierarchy (3.1) and the batch timing arithmetic (4.5). Use the visual form of diagrams 09 and 10.

2. Case study (optional depth)
- One entry per task statement: where the mock builder uses it (step, diagram, decision), and what went wrong and how it was fixed.
- Where the builder has no example, say so. Do not stretch an example to fit.
- Real stories to use: the reason the program did not pass to the writer (decision 0074), the confidence options that ruling 2 had to limit, prompt caching missed in the design and added later, the review loop that ended when the control was written as code, and the 26 document gaps that an independent agent found.

How the page content is made
- The pages are written in the portal's code (the owner's decision for the MVP).
- Claude writes each explanation only from the exam guide's text: nothing the guide does not say.
- An independent agent checks each page against the guide and lists every sentence the guide does not support.
- The owner reads only the flagged pages, plus 3 or 4 at random.

## Not in the MVP (post-MVP, do not build now)
- Markdown downloads for use with AI, and skill files per domain so a participant's Claude can tutor them. Rule for later: the Markdown holds what both people and AI need, the code holds what only people need, and the skill file holds what only the AI needs. Each diagram gets a short text description.
- No mock questions or answers in any downloadable file.
- Links from each task statement to its mock questions, shown only after the person has sat that mock.
- A readiness view: first-attempt scores per domain on mocks 1 to 4. Mock 5 is the final review before booking.
- A public version as a portfolio showcase. It stays separate from the portal.

## Where the material is (this repository)
- docs/build-guide/: "How the Mocks Are Built", the index and steps 0 to 8.
- docs/diagrams/: diagrams 01 to 12.
- docs/decisions/: decisions 0001 to 0079.
- docs/portal-notes.md: the notes for the portal.
- reference/guide-records.json: the exam guide as records (task statements and points).
- mocks/: the 5 mocks, version 2 (tag mocks-v2). The portal already has a version 1.
- The old build guide in the Cowork folder (mock-builder-v3) is out of date. Do not use it.

## The open question to resume
Should the existing build guide go into the portal as it is, with each case study entry kept short and linking into it? Before deciding, read docs/build-guide/ step 4 and tell the owner whether it reads well for participants or only for the builder.
