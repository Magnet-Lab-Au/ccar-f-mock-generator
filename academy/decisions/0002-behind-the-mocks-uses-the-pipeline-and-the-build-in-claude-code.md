# 0002: "Behind the mocks" uses the pipeline and how the project was built in Claude Code

- Date: 12 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

The tables of guide points in the build guide use points of only 12 of the 30 task statements: 1.1, 1.3, 1.4, 1.6, 4.1, 4.2, 4.3, 4.4, 4.6, 5.3, 5.5 and 5.6. It uses no task statement of domain 2 or domain 3. This is a deliberate choice. Not every task statement fits the mock generator. Where do the "Behind the mocks" entries get their examples?

## Options

1. Only from the pipeline: steps 0 to 8.
2. From the pipeline, and also from how the project was built in Claude Code: `CLAUDE.md`, the working rules, and the independent review agents.

## Decision

Option 2. Each entry says which source it uses: the pipeline, or the build in Claude Code. If neither source has an example for a task statement, the entry says so. It also says in one or two sentences why the build did not need it. Example: the pipeline uses no MCP server, because it calls only the Claude API and reads local files. The pipeline sends no tool definitions to the API. It sends its forms as structured outputs (mock decision 0040). The project uses no MCP server. So most entries of domain 2 will say that there is no example. A possible exception is task statement 2.5: the build in Claude Code uses the built-in tools of Claude Code.

## Reason

The owner's reason: not all task statements fit the mock generator. A good engineer knows what to use and what not to use. So the build used only the patterns that it needed.

The build in Claude Code is real work of this project, so its examples are honest. The label of the source stops a reader from thinking that the pipeline does a thing that it does not do.

## How we decided

The assistant read the 9 step files of the build guide and the 12 diagrams. It counted the task statements in the tables of guide points and found the gap. The assistant suggested the build in Claude Code as a second source. The owner said "why not both". The owner then corrected the reason: the unused task statements are a choice, not a gap. The assistant added that each entry with no example says why the build did not need it. The owner agreed.

## Exam guide points

none
