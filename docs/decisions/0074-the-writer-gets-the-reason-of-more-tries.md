# 0074: The writer gets the reason of "more tries"

- Date: 9 October 2026
- Status: accepted
- Diagram: none. Diagram 07 (step 5) shows the request of a new try.

## Question

For the open slot M5-S38, the owner gave 3 more tries with an instruction: "use the second problem, custom_id to match answers to requests". The program sent the writer the last failed try and its findings, but not the reason of the owner (decision 0039). How does the instruction reach the writer?

## Options

1. The request of a new try after "more tries" also has the reason of the owner, as a finding of the owner.
2. No change. The owner uses a new point instead.

## Decision

Option 1. After a decision `more_tries`, the request of step 5 has the findings of the last try and the reason of the owner, as for a rewrite (decision 0045). A test checks it.

In the same round, the owner gave new points to three open slots of mock 5: M5-S28 the point 5.6-K3, M5-S29 the point 3.4-S3 and M5-S39 the point 4.1-S2. M5-S38 got 3 more tries with the instruction above.

## Reason

Plain reason: the owner's reason says what the next try must do differently. Without it, the writer repeats the same problem, as M5-S38 did three times.

## How we decided

The owner agreed to the four slot decisions and gave the instruction for M5-S38. The assistant found that the program did not pass the reason, and made the change so that the instruction reaches the writer.

The owner has not confirmed the text of this file. No independent reviewer checked this file.

## Exam guide points

none
