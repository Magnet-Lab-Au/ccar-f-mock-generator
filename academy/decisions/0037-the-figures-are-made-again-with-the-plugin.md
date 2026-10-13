# 0037: The figures are made again with the plugin

- Date: 14 October 2026
- Status: accepted
- Text confirmed by the owner: 14 October 2026, in the discussion (working rule 35)
- Diagram: none
- Names: decision 0013. Its text does not change (working rule 26).

## Question

Decision 0013 says that each figure goes through four stages, and that in the plan stage the assistant "picks the type of the figure from the table of the plugin: for example a stepper for a process, small multiples for cases, and bars for numbers."

At night, the assistant did not load the skill of the plugin visual-explainer. It drew the figures by hand in the build scripts, in the look of the fifth sample. The fact sheets name a mechanism for each figure, but no type from the table of the plugin. So 55 of the 56 figures of the two tabs are one static drawing. Only Fig. 1 of part 1.1, from the sample, is a stepper. The screenshots of tab 1 are in light mode at 1280 pixels only, but decision 0013 asks for both modes.

How are the figures made right?

## Decision

1. The assistant loads the skill of the plugin before it plans or draws a figure.
2. Plan: the assistant writes a figure plan for all 56 figures. Each figure gets a claim in one sentence and a type from the table of the plugin. The owner checks the plan before any figure is drawn.
3. Draw: the assistant draws again each figure whose type changes, with the rules of the plugin, in the look of decision 0008.
4. The stages "check by script" and "check by review" of decision 0013 apply to each new figure. The owner gets screenshots of each figure in light and dark mode.
5. These changes go with the figure redo, because they touch the same parts: the takeaway in each closed heading, the label "Guide only", the names of the documentation, the code popup of part 1.2, and Figs. 5.6-1, 2.1-1 and 5.2-1 (decision 0039).

## Reason

The owner asked for the plugin, and decision 0013 asks for its table. The figures of the night follow the rules of the plugin but do not use its range of types. So many processes that can go step by step are one static drawing.

## How we decided

The owner asked how many visuals have animations, and then if the figures were made with the plugin. The assistant said that the plugin was not loaded at night, and that half of the plan stage was not done. The owner asked: "Why did you not use the plugin I told you to". The assistant gave the reasons: it took the look of the plugin for the use of the plugin, and it put speed first. The morning report did not say this. The assistant recommended the figure plan first. The owner said to address the other issues of the night first, and then to do the figure plan.

## Exam guide points

None.
