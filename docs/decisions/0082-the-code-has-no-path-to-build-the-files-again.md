# 0082: The code has no path to build the files of a mock again

- Date: 14 October 2026
- Status: accepted
- Text confirmed by the owner: 14 October 2026, in the discussion (working rule 35)
- Diagram: none
- Names: decision 0016. Its text does not change (working rule 26).

## Question

Decision 0016 says: "To change a question, change its record, and code builds the files again." The build guide, step 8, says the same. The code has no path for this:

- `src/step8_build_files.py` stops with "The file exists already" when a mock file exists.
- `src/control.py` refuses the commands `decide` and `accept` of the owner when the state of the mock is `built`.

No rebuild ever happened. Each file in `mocks/` has one commit. The academy fact agent of step 8 found this (`academy/facts/step-8.md`, conflict C1).

Does the code get the path, or do the records change?

## Options

1. Add the path to the code now.
2. Correct the build guide, and record that the code has no path.

## Decision

Option 2. The build guide, step 8, says that the code builds the files of a mock once. The code gives no command to change a question of a built mock.

## Reason

Decision 0083 says that no more mocks are built for now. A path that nobody uses now does not need code now. If more mocks are built, this decision is the place to start.

## How we decided

The morning report of the night of 14 October 2026 named the gap (item 5). The assistant recommended option 2. The owner said: "yes, correct the build guide".

## Exam guide points

None.
