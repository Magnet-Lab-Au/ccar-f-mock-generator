"""The command line of the owner (decisions 0033, 0038 and 0039).

Run from the folder ccar-f-mock-generator:

    python3 src/run.py run --mock 1                 start the program: the automatic work
    python3 src/run.py report --mock 1              show the state and what the mock waits for
    python3 src/run.py mark --mock 1                read the marking file of the open round
    python3 src/run.py decide --mock 1 more_tries M1-S05 --reason "..."
    python3 src/run.py decide --mock 1 rewrite M1-SC3-R1-F1 --question M1-S38-T1 --reason "..."
    python3 src/run.py accept --mock 1              step 8 builds the files, if the conditions hold

The steps 2, 4 and 6 call the Claude API. The key comes from the environment
(ANTHROPIC_API_KEY or a profile of `ant auth login`), never from a file of
the repository.
"""
import argparse
import json
import os
import sys

from control import Control, Refused, RunStopped
from model_call import cost
from steps import ROOT, RealSteps, guide_points, load_records


def make_control(mock, seed=None):
    folder = os.path.join(ROOT, "runs", "mock-%02d" % mock)
    plan_path = os.path.join(folder, "plan.json")
    if os.path.exists(plan_path):
        with open(plan_path, encoding="utf-8") as f:
            seed = json.load(f)["seed"]
    elif seed is None:
        raise Refused("Mock %d has no plan. Give --seed to make one." % mock)
    records = load_records()
    steps = RealSteps(folder, records=records)
    return Control(folder, mock, seed, steps, guide_points(records)), steps


def save_cost(c, steps):
    """Save the tokens and the cost of this run, one file for each run. Print the
    cost of this run and of the mock so far."""
    if not steps.model_call.usage or c.run_number is None:
        return
    folder = os.path.join(c.folder, "usage")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "run-%03d.json" % c.run_number)
    data = dict(cost(steps.model_call.usage), run=c.run_number, model=steps.model_call.model, effort=steps.model_call.effort)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    total = 0.0
    for name in sorted(os.listdir(folder)):
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            total += json.load(f)["dollars"]
    print("Cost of this run: $%.2f (%d calls). Cost of the mock so far: $%.2f." % (data["dollars"], data["calls"], total))


def show(report):
    print("State: %s" % report["state"])
    for line in report["waiting_for"]:
        print("  waits for: %s" % line)
    open_slots = [s for s in report["slots"] if s["status"] != "passed"]
    print("Slots: %d passed, %d not passed" % (len(report["slots"]) - len(open_slots), len(open_slots)))
    for s in open_slots:
        print("  %s %s %s" % (s["slot_id"], s["status"], ", ".join(s["open_reasons"])))
    for f in report["step6_findings"]:
        print("  finding %s (%s, %s): %s %s" % (f["id"], f["rule"], f["result"], ", ".join(f["question_ids"]), f["detail"]))
    for e in report["errors"]:
        print("  error %s: %s %s: %s" % (e["id"], e["step"], e["target"], e["cause"]))


def main(argv=None):
    p = argparse.ArgumentParser(description="The control of the mock builder.")
    p.add_argument("command", choices=["run", "report", "mark", "decide", "accept"])
    p.add_argument("action", nargs="?")
    p.add_argument("target", nargs="?")
    p.add_argument("--mock", type=int, required=True)
    p.add_argument("--seed", type=int)
    p.add_argument("--reason", default="")
    p.add_argument("--question")
    a = p.parse_args(argv)
    c = steps = None
    try:
        c, steps = make_control(a.mock, a.seed)
        if a.command == "run":
            try:
                show(c.run())
            finally:
                save_cost(c, steps)
        elif a.command == "report":
            show(c.report())
        elif a.command == "mark":
            report = c.read_marks()
            print("Bad marks:", json.dumps(steps.bad_marks_by_segment(c.marks())))
            show(report)
        elif a.command == "decide":
            if not a.action or not a.target:
                raise Refused("decide needs an action and a target.")
            d = c.decide(a.action, a.target, a.reason, question_id=a.question)
            print("Saved: %s" % json.dumps(d))
            show(c.report())
        elif a.command == "accept":
            show(c.accept(a.reason))
    except Refused as e:
        print("Refused: %s" % e)
        return 1
    except RunStopped as e:
        print("Stopped: %s" % e)
        print("Repair the cause, then start the program again.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
