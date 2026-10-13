# The brief of a fact agent for a task statement of tab 1

The assistant gives this brief to each fact agent of tab 1 (academy decisions 0011, 0012 and 0021). The agent writes one fact sheet: `academy/facts/ts-N-M.md` for task statement N.M.

## What tab 1 shows for a task statement (decisions 0004, 0010 and 0019)

- Closed: the takeaway heading only, such as "The loop runs while Claude asks for tools".
- Overview, about 30 seconds: the takeaway heading, the title of the task statement as a quote of the guide, a short answer of 1 or 2 sentences, and a figure only if the task statement has a mechanism to show.
- Explanation, about 3 minutes: a short text that explains the points, figures that support the text, the K and S points of the guide, and "The exam tests".
- Depth: "Beyond the exam" (decision 0006), code only in popups (decisions 0004 and 0032), and the links to the steps of tab 2 that use the task statement. If no step uses it, the Depth says so and says why the build did not need it (decision 0002).

The reader is a senior engineer, a director of engineering or a senior product manager, with little time.

## The sources and their order of trust (decisions 0011 and 0014)

- R = the exam guide: `reference/exam-guide.md` (the copy that matches the official PDF, decision 0027) and `reference/guide-records.json`. The guide is the source for what the exam tests.
- D = the official Anthropic documentation, for each fact about a product: the Claude API, Claude Code and the Agent SDK. Read the page live, as Markdown (add `.md` to the URL of the page, and follow redirects with `curl -sL`). Indexes: `https://platform.claude.com/llms.txt` and `https://code.claude.com/docs/llms.txt`. Save each page that the sheet cites as a dated copy in `academy/sources/`, named `2026-10-14-anthropic-docs-<page>.md` (platform pages) or `2026-10-14-claude-code-docs-<page>.md` (Claude Code pages), if that file does not exist yet (decision 0030). The line numbers in the sheet are lines of that copy.
- Levels 1 to 4 = the records of the mock builder: 1 code, tests and run files, 2 decisions, 3 build guide and diagrams, 4 journal and other notes. Use them for the links to tab 2.
- If the documentation and the guide disagree, record both, and say which one the exam uses (decision 0014).

## The fact sheet

1. **The guide text.** The title and each K and S point with its ID, exact.
2. **The takeaway.** A proposed takeaway heading (a claim of at most 10 words) and a short answer (1 or 2 sentences), each with the facts that support it.
3. **Facts for the Explanation.** A table: number, fact, source file and lines, exact quote, level. Cover each K and S point. Prefer the documentation for how a product works.
4. **The exam tests.** The lines of section 17 of the guide (in-scope topics, technologies) that belong to this task statement, exact, with lines. Each sample question of the guide that tests this task statement, with its number and why. The number of questions in `mocks/mock-0N.questions.json` (N = 1 to 5) whose point starts with N.M, computed.
5. **Beyond the exam.** Up to 3 product facts from the documentation that go beyond the guide and that a reader in production needs, each with its quote. Mark each place where the documentation and the guide differ.
6. **A mechanism for one figure**, or "none". A figure only where the task statement has a mechanism: a loop, a flow, a structure. Describe the boxes, the arrows and the labels, each with its source.
7. **Code for a popup**, or "none": a short example from the documentation, exact, with its lines.
8. **Links to tab 2.** Each step of the mock builder whose table of guide points (`docs/build-guide/step-*.md`, decision 0024) uses a point of this task statement: the step, the points and the use, with lines. Also the parts of `academy/pages/behind-the-mocks.html` that name this task statement (ids such as `step-5` or `cc-4-6`). If no step uses it, say so, and give any record that says why the build did not need it.
9. **Conflicts.** Each place where two sources disagree, or where a claim is weak.
10. **Not found.** What you looked for and did not find.

## Rules

- Each fact has its source and an exact quote. Do not write a fact from memory. If you cannot check a fact, write "not checked".
- Write in Simplified Technical English: short sentences, active voice, no contractions, no semicolons, no em dashes. Write "the owner", not a name.
- Change no file except your fact sheet and new dated copies in `academy/sources/`. Run no git command that changes the repository. Make no call to a model API.
- Do not open: `marking/*.xlsx`, the folder `claude-code-brand-kit/`, any conversation transcript, or a personal file of the owner (`responses.json`, the Study Edition, study notes, the progress tracker, the error log, the refresher, exam scores). Do not copy text from them (working rules 19 and 28).
- Keep the sheet under about 2,500 words.
