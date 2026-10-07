# src

The program.

- `step0_prepare_guide_records.py`: step 0. It reads `reference/exam-guide.md` and writes `reference/guide-records.json` (decision 0028).
- `check_guide_records.py`: the check of step 0. It does not use the code of step 0.
- `step1_plan.py`: step 1. It makes the plan of one mock, `runs/mock-NN/plan.json`, from the records file and a seed (decision 0027). It uses only `random()` of Python, so the same seed gives the same plan also in a later Python version.
- `control.py`: the control (decisions 0038 and 0039). It decides what happens next to a slot and to a mock. It calls each step as a separate part. The real steps do not exist yet.

The tests of the control are in `tests/`. Run them from the folder `ccar-f-mock-generator`:

    python3 -m unittest discover tests

No test makes a model call.
