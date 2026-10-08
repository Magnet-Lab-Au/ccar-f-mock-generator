# 0062: Mock 3: close repeats are known limits, and a stricter B9 from mock 4

- Date: 8 October 2026
- Status: accepted
- Diagram: none. The design of the stricter B9 comes with its own decision.

## Question

An independent agent compared the 60 questions of mock 3 with mocks 1 and 2 (decision 0060, item 5). It found 2 copies (M3-S34 with M2-S13, and M3-S49 with M1-S34) and 47 close repeats. About 26 questions have the same problem and the same answer as an earlier question, in another setting. Rule B9 should fail these, but the model judged a new setting as a new scene. What happens to mock 3, and to rule B9?

## Options

1. Mock 3: rewrite the 2 copies, and record the close repeats as known limits. Rule B9: stricter from mock 4.
2. Make B9 stricter now, and write mock 3 again.

## Decision

Option 1.

1. M3-S34 and M3-S49 get a rewrite with rule B9. The program accepts a rewrite only after the open marking round, so the owner marks round 1 first. Neither question is in the sample of round 1. The owner then marks the 2 new questions in round 2.
2. The close repeats of mock 3 are known limits (decision 0060). The list is in the report of the agent, recorded in `docs/journal.md`.
3. Rule B9 becomes stricter before mock 4: a question fails if it has the same problem as an earlier question on the same idea, also in another setting. The exact text and its cost come in a separate decision, before mock 4.

This changes the instruction of the owner "Do not change rule B9" (decision 0060, item 4) for mocks 4 and 5.

## Reason

Plain reason: a copy breaks decision 0060. The close repeats are allowed, but the count shows that B9 lets through more than its text says. Mock 3 is complete and checked, so a new run costs more than it gains. Mocks 4 and 5 can still profit.

## How we decided

The assistant showed the count and said that B9 is too weak, and asked the owner to look again at "Do not change rule B9". The owner decided: "for mock 4 we make it stricter but for now we accept mock 3 as it is with the 2 copies rewritten."

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
