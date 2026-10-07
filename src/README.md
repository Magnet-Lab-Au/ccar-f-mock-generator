# src

The program.

- `step0_prepare_guide_records.py`: step 0. It reads `reference/exam-guide.md` and writes `reference/guide-records.json` (decision 0028).
- `check_guide_records.py`: the check of step 0. It does not use the code of step 0.
- `step1_plan.py`: step 1. It makes the plan of one mock, `runs/mock-NN/plan.json`, from the records file and a seed (decision 0027). It uses only `random()` of Python, so the same seed gives the same plan also in a later Python version.
- `step3_check_code.py`: step 3. It checks a question against rules A1 to A11 (decisions 0030, 0031 and 0038, part 8).
- `step8_build_files.py`: step 8. It builds the two files of a mock in `mocks/` (decision 0036). It checks each record against its slot first.
- `control.py`: the control (decisions 0038 and 0039). It decides what happens next to a slot and to a mock. It calls each step as a separate part. The real steps do not exist yet.

The tests of the control are in `tests/`. Run them from the folder `ccar-f-mock-generator`:

    python3 -m unittest discover tests

No test makes a model call.
