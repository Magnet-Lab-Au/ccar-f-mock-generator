# 0012: Two agents for each part

- Date: 13 October 2026
- Status: accepted. Decision 0015 adds a whole-picture review after each slice.
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

Decision 0011 needs a fact sheet and an independent review for each part. Which agents do this work?

## Decision

Two new agents for each part. Both use the same model as the assistant, Opus 5.5.

| Agent | Gets | Gives |
|---|---|---|
| Fact agent | the sources of the part, the order of trust (decision 0011), and working rules 19 and 28 | the fact sheet: each fact with its file and line, and each conflict |
| Review agent | the finished part, the fact sheet, and the sources. It does not get the notes of the assistant. | each sentence that the source does not support |

The assistant writes the part from the fact sheet. Two agents for each part is within working rule 32, so the assistant needs no new yes for each run.

A part is one closed section of a tab: in tab 2, the top, each of the 9 steps and each of the 5 entries of the build in Claude Code (about 15). In tab 1, the map and each of the 30 task statements (31). That is about 92 agent runs.

## Reason

The fact agent and the review agent are two different agents, and neither one wrote the part. So no check depends on the memory or the judgment of one agent (working rule 14). The review agent gets no notes of the assistant, so it judges the part only against its sources.

## How we decided

The assistant recommended the two agents, the model, and what each agent gets and gives. The owner accepted it.

## Exam guide points

none.
