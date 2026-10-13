# 0080: Each try of a new start gets the parts of the owner

- Date: 14 October 2026
- Status: proposed, chosen by the assistant at night (working rule 36). On the branch `fix-owner-reason`, not merged.
- Text confirmed by the owner: not yet
- Diagram: `docs/diagrams/07-step-5-try-again.html` (step 5)
- Names: decision 0074. Decision 0074 does not change (working rule 26).

## Question

Decision 0074 says: "After a decision `more_tries`, the request of step 5 has the findings of the last try and the reason of the owner". The code does this only for the first try of the new start. In `src/control.py`, `request_for`, the branch `if in_round:` returns before the branches of the events. So try 2 and try 3 of a new start get only the findings of steps 3 and 4 of the last try. The same gap applies after a bad mark and after a rewrite. The test of decision 0074 (`tests/test_control.py`) forces `in_round=[]`, so it checks only the first try.

The case in the run files: for the open slot M5-S38, the owner gave more tries with a reason. Try 4 got the reason and failed rule B9. Try 5 did not get the reason, wrote the old problem again, passed, and is the question in mock 5. A replay of `request_for` on a copy of `runs/mock-05/`, with no model call, shows the request of try 5 with the findings `['B9']` only.

The academy fact agent of step 5 found the gap (`academy/facts/step-5.md`, conflict C2). An independent agent confirmed it.

## Options

1. No change. The page of tab 2 tells the gap as a known limit.
2. Each try of the new start gets the reason of the owner only.
3. Each try of the new start gets all the parts that the first try gets: the reason of the owner (rule `owner`), and after a rewrite also the finding of step 6 and the other questions not to repeat.

## Decision

Option 3. A new method `_event_parts` returns the findings and the other questions that an event of the owner adds. `request_for` adds them to the request of each try of the new start. The first try of a start gets the same request as before.

Six new tests (class `TestOwnerPartsReachEachTryOfTheStart`) check try 2 and try 3 after `more_tries`, try 2 after a bad mark, try 2 after a rewrite of a finding of step 6, try 2 after a rewrite with a new point, try 2 after `more_tries` that followed `cannot_write`, and a slot with no event. No test makes a model call (decision 0038). All 234 tests pass.

The choice between options 2 and 3 is a choice for the owner. The assistant chose option 3 at night: a later try that does not see the other questions of a rewrite can write the same scene again.

## Known limits

- On try 2 and try 3 of a new start, the reason of the owner and the finding of step 6 appear next to the latest failed try of the start, not next to the question that the owner judged. A reason that names a letter, such as "C is also correct.", names an option of the judged question. The writer then sees a different option C. The independent review of the change found this. A fix would add the ID of the judged question to each of these findings. It is a choice for the owner.
- The result of decision 0074, "The instruction reached the writer, but the question did not follow it", is true only for try 4 of M5-S38. Try 5, the question in mock 5, did not get the instruction.

## Reason

The reason of the owner says what the next try must do differently (decision 0074). Without it, a later try can go back to the old problem, as M5-S38-T5 did.

## What does not change

- The 5 built mocks and the files in `runs/`. The program did not run, and no run file stores the text of a request.
- Mocks 1 to 5 were built without this fix. The build guide and diagram 07 keep that history.

## How we decided

The academy fact agent of step 5 found the gap while it read the code for tab 2 of the portal (`academy/facts/step-5.md`, conflict C2). An independent agent confirmed it in the code, the test and a replay. The owner accepted a night plan with this fix on a separate branch (`academy/night-plan.md`). The owner had not yet chosen between options 2 and 3, so the assistant chose option 3 at night under working rule 36. An independent agent reviewed the change: the first try of each start gets the same request as before, in 10 cases. It found the known limit above, a test class below the main guard of the test file, and paths with no test. The assistant moved the class and added two tests: a rewrite with a new point, and "more tries" after "cannot write". All 234 tests pass.

## Exam guide points

4.4-K1, 4.4-S1.
