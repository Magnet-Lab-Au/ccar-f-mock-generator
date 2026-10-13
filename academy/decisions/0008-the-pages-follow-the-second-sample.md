# 0008: The pages follow the second sample

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none

## Question

There are two samples of task statement 1.1. Which one is the model for the pages?

## Options

1. The first sample, `sample/1-1-agentic-loops.html`: text first, with one animated loop.
2. The second sample, `sample/1-1-agentic-loops-ve.html`, made with the plugin visual-explainer: figures lead, and the text is the caption of each figure.

## Decision

Option 2. The colors and the fonts can change later.

## Reason

The owner said that the second sample "looks better by a lot".

A later change of colors and fonts is small. In `sample/make-1-1-ve.py`, all colors and fonts are variables in three blocks: light, dark and print. The figures use these variables, so they follow a change. A change of the figures themselves is larger, because each page has its own drawn figures.

## How we decided

The owner asked for a second copy of the sample with the plugin visual-explainer. The assistant made it from the same checked data as the first sample. The owner compared the two pages and chose the second one. The owner asked if colors and looks can change later. The assistant checked the script and said yes, with the limit above.

## Exam guide points

none.
