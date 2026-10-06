# 0001: Record decisions and diagrams as we go, in one repository folder

- Date: 5 October 2026
- Status: accepted
- Diagram: none

## Question

How do we document the build, so that nobody has to reconstruct it later?

## Options

1. Continue the folder `CCAR-F Mocks v2` and its file `DECISIONS.md`.
2. Start a new folder. Keep one file for each decision, one HTML file for each diagram and a journal. Keep the documents and the code in the same folder.

## Decision

Option 2. The folder is `mock-builder-v3`. The structure and the rules are in `README.md`.

Design method: first agree on the steps of the pipeline. Then design one step at a time and find the exam guide points that apply to it. At the end, a script checks that each of the 240 points has an answer.

## Reason

The record of the first build had to be reconstructed from files, and many decisions had no record that they ran. The owner wants to start clean, and wants each decision and each diagram to exist from the day it is made.

We discussed a different method: go through the 30 task statements first and mark each one. We rejected it as the starting point. The task statements are a list of practices, not a design. That method made the assistant assume a pipeline that nobody had agreed on. The list stays as the final check.

## Exam guide points

5.4-K2, 5.4-K4, 5.6-K2
