# 0013: Four stages for each figure

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none

## Question

How do we make sure that the figures and animations are the best that the plugin visual-explainer can make?

## Decision

Each figure goes through four stages.

1. Plan. For each part, the assistant writes the claim of each figure in one sentence. It picks the type of the figure from the table of the plugin: for example a stepper for a process, small multiples for cases, and bars for numbers. A part gets a figure only when it has a mechanism to show (decision 0010).
2. Draw. The assistant draws each figure with the rules of the plugin, in the look of decision 0008. Diagrams 01 to 12 of the mock generator give the content. The assistant draws them again, because they have layout defects.
3. Check by script. A headless browser checks each figure in light mode and in dark mode, at 1280 and 390 pixels wide: no sideways overflow, no console errors, a text contrast of at least 4.5 to 1, and labels of at least 12 pixels.
4. Check by review. A figure states facts, so the review agent (decision 0012) checks each label against the fact sheet. The owner gets screenshots of each figure in both modes.

## Reason

The owner wants the best figures that the plugin can make, and the plugin has rules for this. A check by script finds faults of layout and contrast that a person can miss. A label of a figure is a fact, so it gets the same check as a sentence (decision 0011).

## How we decided

After the agents were decided, the owner said that the figures and animations also need a plan. The assistant recommended the four stages. The owner accepted them.

## Known limits

- The K and S letters in light mode are about 2 to 1 (decision 0009), and the warning yellow is 1.6 to 1 on white (decision 0008). The contrast check reports them as known exceptions. It does not fail on them.

## Exam guide points

none.
