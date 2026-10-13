# 0015: A whole-picture review after each slice

- Date: 13 October 2026
- Status: accepted. Decision 0026 adds a reader agent for each slice. Decision 0028 gives rules 19 and 28 to each agent.
- Text confirmed by the owner: 13 October 2026
- Diagram: none
- Changes: adds a third agent to decision 0012, for each slice

## Question

The review of decision 0012 checks each part against its sources. It does not check how the parts fit together. How do we make sure that the parts agree with the whole picture as we build slice after slice?

## Decision

A whole-picture review after each slice. A slice is a group of parts that the assistant builds and shows to the owner together, such as the top of tab 2 with step 5.

1. A script checks:
   - each link and each anchor between the two tabs works
   - each step in the 9-step diagram has its part
   - each number has the same value everywhere on both tabs
2. A new agent reads both tabs as they are so far, and decisions 0001 to 0015 (and the later decisions). It lists:
   - one thing with two names
   - two parts that disagree
   - a part that does not follow the decisions
   - text that repeats another part

The owner's yes to this decision covers the third agent for each slice (working rule 32).

## Reason

The owner asked for an overall review, to see if everything agrees with the whole picture as the slices are built. A part can be correct against its sources and still use a different name, or repeat another part.

## How we decided

The assistant proposed to start the first slice. The owner asked for a review of the whole picture after each slice. The assistant recommended a script and a new agent. The owner accepted it.

## Exam guide points

none.
