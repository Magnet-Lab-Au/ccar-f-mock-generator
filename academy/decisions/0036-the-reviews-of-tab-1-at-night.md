# 0036: The reviews of tab 1 at night

- Date: 14 October 2026
- Status: proposed, chosen by the assistant at night (working rule 36)
- Text confirmed by the owner: not yet
- Diagram: none
- Changes: decision 0012 (a review agent for each part), decision 0015 (a whole-picture agent after each slice), decision 0026 (a reader agent after each slice, and how it reads)

## Question

The owner said at 02:06: "Do as many slices as you can. Go all the way". Slices 4 to 8 are all of tab 1: the map and 30 task statements. With the agents of decisions 0012, 0015 and 0026 for each part and each slice, the night could not finish them. How does the night review tab 1?

## Decision

1. A fact agent writes the fact sheet of each task statement, as decision 0012 says. Part 1.1 is the exception: it takes the checked content of the fifth sample, so it has no new fact sheet.
2. One review agent checks two parts, not one (from 02:28).
3. One whole-picture agent checks slices 5 and 6 together (03:40), and one checks slices 7 and 8 together (07:15). Slice 4 had its own.
4. One reader agent reads slices 5 to 8 together (07:15). Slice 4 had its own. The reader of slices 5 to 8 reads all three levels of each part and writes one sentence for each part, as a candidate for the exam. It does not read the Overview alone, and it does not judge each figure alone, which decision 0026 asks for.
5. The top of tab 1 (the map, "How we broke it down" and the summaries of the domains) has no fact agent and no review agent. The whole-picture agents of slice 4 and of slices 7 and 8 read it.

## Reason

The night had about 7 hours and a pause of about 2.5 hours at a usage limit. Each review agent still checked each sentence of its two parts against the sources. The fixes of each review are in the commit messages. The night plan allows at most 2 agents at a time.

## Options for the owner

- Accept the reviews as they are.
- Ask for the missing agents: a review of the top of tab 1, and a reader agent that follows decision 0026 for slices 5 to 8 (Overview alone, and each figure alone).

## How we decided

The assistant chose step 2 at 02:28 and steps 3 to 5 after the pause, under working rule 36. The independent check of the morning report found that no file recorded these choices.

## Exam guide points

None.
