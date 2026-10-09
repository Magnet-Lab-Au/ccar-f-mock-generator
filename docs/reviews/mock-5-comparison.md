# Mock 5 compared with mocks 1 to 4

- Date: 9 October 2026
- Made by: an independent agent (a Claude model) that read the 300 questions of mocks 1 to 5 and Section 9 of the exam guide. It did not open `marking/`. Each judgment is its own. No script checked it.
- Rule: decision 0060, item 5 (a comparison before the marking of a later mock).

## Totals

| Group | Questions of mock 5 |
|---|---|
| Copy (same scene, answer and wrong options) | 1 |
| Close (same idea and a similar scene, or the same scene with the cause instead of the fix) | 46 |
| Same idea only | 12 |
| New | 1 |

14 of the 46 close questions are near copies: the same scene and answer, with other wrong options.

## The copy

M5-S33 and M2-S34: a CI test-generation skill uses Bash and deletes a fixture folder. The answer is allowed-tools. The wrong ideas are the same: context: fork, argument-hint, a CLAUDE.md rule.

## Pairs inside mock 5

- M5-S41 and M5-S45: both are CI checks run in the generation session, with the answer "the same session keeps its reasoning". The strongest pair.
- M5-S02 and M5-S05: the correct option D of S02 is the answer of S05 (run the subagents in parallel).
- Smaller overlaps: S26 and S27, S16 and S17, S08 and S46.

## Sample questions of the guide

No copy. Close: M5-S56 and sample question 8 (the same three wrong ideas), M5-S01 and sample question 12, M5-S17 and sample question 5.

## The new question

M5-S10: "too many tools degrade tool selection" as the correct answer.

## Why so many close questions

The narrow list has 63 of the 95 ideas (decisions 0066, 0068, 0072 and 0075). For a narrow idea, only a copy fails rule B9. So most questions of mock 5 test the same problem as an earlier mock in a new setting. Some ideas are now in their fourth mock (for example "append the tool result": M1-S05, M2-S18, M4-S22, M5-S58).
