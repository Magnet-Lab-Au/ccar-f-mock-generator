# 0023: The task statements of the build in Claude Code

- Date: 13 October 2026
- Status: accepted. Decision 0035 (proposed) leaves out the entries of 3.2 and 2.5.
- Text confirmed by the owner: 13 October 2026 (working rule 35)
- Diagram: none
- Changes: decision 0010, the table of the build in Claude Code

## Question

Decision 0010 links each entry of "the build in Claude Code" to a task statement, to be checked against the K and S points of the guide. The independent review of the plan found that two links are stretched. Which links hold?

## Decision

| Entry | Task statement |
|---|---|
| CLAUDE.md, which imports WORKING-RULES.md | 3.1 |
| HANDOFF.md, the journal and the decision files carry the work from one session to the next | 1.7 |
| A new agent reviews each file. Story: the three document checks (decision 0031) | 4.6 (not 1.3) |
| Skills, such as ste-writing and discussion-and-brainstorming | 3.2. The preview card says that the skills are outside the repository. |
| The built-in tools of Claude Code | 2.5 (new) |
| "Discuss first", before any code | 3.4: no example. The entry says that the build used a "discuss first" rule, not plan mode. |

The fact agent still checks each link against the K and S points before the part is written (decision 0011). For 3.4, it also checks whether the build used the Explore subagent (3.4-K4, 3.4-S3) before the entry says "no example". For the review agents, it also checks 1.3-K2: a subagent gets its context only in its prompt.

## Reason

- 4.6-S1 says: "Using a second independent Claude instance to review generated code without the generator's reasoning context". The part review (decision 0012) plus the whole-picture review (decision 0015) also match 4.6-K3: per-file passes plus cross-file integration passes. Task statement 1.3 is about the Task tool and the context that a coordinator passes.
- The build did not use plan mode, so 3.4 has no example. Decision 0002 says that such an entry says why the build did not need it.
- Decision 0002 named 2.5 as a possible exception: the build in Claude Code uses the built-in tools of Claude Code.
- The skills are in the folder of the owner's user settings, not in the repository. So their preview card cannot link to the repository (decision 0005).

## How we decided

The independent review of the plan raised it. The assistant checked the points of 3.4 and 4.6 in `reference/task-statements-and-points.md` and recommended the table. The owner accepted it.

## Exam guide points

3.1, 1.7, 4.6-K2, 4.6-K3, 4.6-S1, 3.2, 2.5, 3.4.
