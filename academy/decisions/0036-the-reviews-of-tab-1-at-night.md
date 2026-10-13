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
2. One review agent checks two parts, not one (from 02:28). Part 3.6 had its own review agent, because it was the last part of domain 3. Part 1.1 had no review agent at night. Its content had an independent check before the night (academy journal, 13 October), and the night changed its IDs and some of its text.
3. One whole-picture agent checks slices 5 and 6 together (03:40), and one checks slices 7 and 8 together (07:15). Slice 4 had its own.
4. One reader agent reads slices 5 to 8 together (07:15). Slice 4 had its own. The reader of slices 5 to 8 got the role of a candidate for the exam, not the audience of decision 0026 (a senior engineer with little time). It wrote one sentence for each part from all three levels, not from the Overview alone. It listed the sentences that it had to read twice and the terms used before they are explained (points 3 and 4 of decision 0026). It also listed the parts that seem to disagree and up to 5 figures that did not help. It did not compare each figure with its caption, did not say whether each closed heading tells it if the part is worth opening, and did not list code in the text (points 2, 5 and 6).
5. The top of tab 1 (the map, "How we broke it down" and the summaries of the domains) has no fact agent and no review agent. The whole-picture agents of slice 4 and of slices 7 and 8 read it.

## Reason

The work on tab 1 ran from 02:06 to about 07:30, with a pause of about 2.5 hours at a usage limit (03:50 to 06:30). Each review agent still checked each sentence of its parts against the sources. The fixes of each review are in the commit messages. The night plan allows at most 2 agents at a time.

## Options for the owner

- Accept the reviews as they are.
- Ask for the missing agents: a review of the top of tab 1 and of part 1.1, and a reader agent that follows decision 0026 for slices 5 to 8 (points 1, 2, 5 and 6).

The assistant recommends the second option before tab 1 goes to the cohort. The top of tab 1 is the first thing that a reader sees, and no review agent checked its facts.

## How we decided

The assistant chose steps 2 and 5 during slice 4 (02:13 to 02:28), the joint whole-picture agent of slices 5 and 6 at 03:40, and the rest of steps 3 and 4 after the pause (06:32 to 07:15), under working rule 36. The independent check of the morning report found that no file recorded these choices.

## Exam guide points

None.
