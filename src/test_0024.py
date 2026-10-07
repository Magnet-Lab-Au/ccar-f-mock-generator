"""The test before the first full run (decisions 0024 and 0042).

Run from the folder ccar-f-mock-generator, one part at a time:

    python3 src/test_0024.py part1     the writer makes 10 questions, step 3 checks them, a marking file
    python3 src/test_0024.py part2     call 4a answers the 12 sample questions of the guide
    python3 src/test_0024.py part3     call 4b checks the good questions and the damaged copies

Parts 1 to 3 call the Claude API and cost money. The records go to
runs/test-0024/. Nothing goes to runs/mock-01/.
"""
import argparse
import copy
import json
import os
import sys

import step3_check_code
from control import CallFailed, RunStopped
from model_call import ModelCall, cost as usage_cost
from step2_write import Writer
from step4_check_model import ModelCheck
from step6_check_scenario import ScenarioCheck
from step7_marking import Marking, MarkingError
from steps import ROOT, load_records

FOLDER = os.path.join(ROOT, "runs", "test-0024")
MARKING = os.path.join(ROOT, "marking")
PRICE = {"input": 4.0, "output": 20.0}   # US dollars per million tokens, Claude Opus 5.5 (decision 0042)
CALL_RUNS = 3


def save(name, data):
    os.makedirs(FOLDER, exist_ok=True)
    path = os.path.join(FOLDER, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def load(name):
    with open(os.path.join(FOLDER, name), encoding="utf-8") as f:
        return json.load(f)


def cost(model_call):
    return usage_cost(model_call.usage)


def retry(function, *args):
    """A call that fails runs again, at most 3 times (decision 0037, item 10)."""
    cause = None
    for _ in range(CALL_RUNS):
        try:
            return function(*args), None
        except CallFailed as e:
            cause = str(e)
    return None, cause


def select_slots(plan, records, count=10):
    """Decision 0042: 10 slots that cover the 4 scenarios, the 5 domains and 2
    multiple-response questions. A fixed method: walk the slots in their
    sequence, and take a slot when it adds a scenario, a domain or a needed
    multiple-response question. Then fill up in sequence."""
    domain = {t["id"]: t["domain"] for t in records["task_statements"]}
    chosen, scen, dom, mr = [], set(), set(), 0
    for s in plan["slots"]:
        many = s["type"] == "multiple_response"
        adds = (s["scenario"] not in scen) or (domain[s["task_statement"]] not in dom) or (many and mr < 2)
        if adds and (not many or mr < 2):
            chosen.append(s)
            scen.add(s["scenario"])
            dom.add(domain[s["task_statement"]])
            mr += many
        if len(chosen) == count:
            break
    for s in plan["slots"]:
        if len(chosen) == count:
            break
        if s not in chosen and (s["type"] == "multiple_choice" or mr < 2):
            chosen.append(s)
            mr += s["type"] == "multiple_response"
    return sorted(chosen, key=lambda s: s["slot_id"])


def part1(records, plan, model_call):
    writer = Writer(records, model_call, plan["seed"])
    slots = select_slots(plan, records)
    out = []
    for slot in slots:
        request = {"slot": slot, "point": slot["point"], "step": 2, "shown_try": None,
                   "failed_question": None, "findings": [], "other_questions": []}
        answer, cause = retry(writer.write, request)
        entry = {"slot": slot, "error": cause}
        if answer is not None:
            q = {"question_id": "T-%s" % slot["slot_id"], "slot_id": slot["slot_id"], "try": 1,
                 "point": slot["point"], "select": slot["select"], **answer}
            entry["question"] = q
            if answer["status"] == "written":
                entry["step3"] = step3_check_code.check(q, slot)
        out.append(entry)
        print("%s: %s %s" % (slot["slot_id"], "error" if cause else entry["question"]["status"],
                              entry.get("step3", {}).get("verdict", "")))
    written = [e["question"] for e in out if e.get("question", {}).get("status") == "written"]
    marking = Marking(plan, records, MARKING)
    marking.prefix = "test-0024"
    path = marking.make(1, written)
    result = {"questions": out, "marking_file": path, "cost": cost(model_call)}
    save("part1.json", result)
    print("Marking file: %s" % path)
    return result


def sample_as_question(sample):
    return {"question_id": "SAMPLE-%d" % sample["number"], "select": len(sample["correct_answer"]),
            "question": sample["question"],
            "options": [{"letter": k, "text": v, "correct": k in sample["correct_answer"], "reason": ""}
                        for k, v in sorted(sample["options"].items())]}


def part2(records, model_call):
    check = ModelCheck(records, model_call)
    out = []
    for sample in records["sample_questions"]:
        q = sample_as_question(sample)
        answer, cause = retry(check.blind, q, {"scenario": sample["scenario"]})
        right = answer is not None and answer[0]["status"] == "answered" and \
            sorted(answer[0]["selected"]) == sorted(sample["correct_answer"])
        out.append({"number": sample["number"], "correct": sample["correct_answer"],
                    "answer": answer[0] if answer else None, "error": cause, "right": right})
        print("Sample %d: %s" % (sample["number"], "right" if right else "NOT right"))
    result = {"answers": out, "right": sum(e["right"] for e in out), "of": len(out), "cost": cost(model_call)}
    save("part2.json", result)
    print("Right: %d of %d" % (result["right"], result["of"]))
    return result


def damage_b1(question):
    """Code moves the mark "correct" to a wrong option (decision 0042)."""
    q = copy.deepcopy(question)
    right = [o for o in q["options"] if o["correct"]]
    wrong = [o for o in q["options"] if not o["correct"]]
    right[0]["correct"], wrong[0]["correct"] = False, True
    right[0]["reason"], wrong[0]["reason"] = wrong[0]["reason"], right[0]["reason"]
    return q


def rules_verdict(check, question, slot):
    """Call 4b alone, with the feature search, as decision 0032 part 4 makes the
    verdict without the blind answer."""
    answer, _ = check.rules(question, slot)
    results = {r["rule"]: r["result"] for r in answer["results"]}
    missing = [n for n in answer["features"] if not check.features.named(n)]
    failed = sorted(set([r for r, v in results.items() if v == "fail"] + (["B6"] if missing else [])))
    verdict = "fail" if failed else ("cannot_decide" if "cannot_decide" in results.values() else "pass")
    return {"verdict": verdict, "failed_rules": failed, "results": answer["results"], "features": answer["features"],
            "not_named": missing}


def part3(records, model_call):
    p1 = load("part1.json")
    by_id = {e["question"]["question_id"]: e for e in p1["questions"] if e.get("question")}
    marking = Marking(load_plan(), records, MARKING)
    marking.prefix = "test-0024"
    marks = {m["question_id"]: m for m in marking.read(1)}
    good = [qid for qid, m in marks.items() if m["mark"] == "good"]
    damaged = {d["question_id"]: d for d in load("damaged.json")}
    check = ModelCheck(records, model_call)
    out = []
    for qid in good:
        entry = by_id[qid]
        q, slot = entry["question"], entry["slot"]
        v, cause = retry(rules_verdict, check, q, slot)
        out.append({"question_id": qid, "copy": "good", "expected": "pass", "error": cause, "verdict": v})
        d = damaged.get(qid)
        if d is None:
            continue
        broken = damage_b1(q) if d["rule"] == "B1" else dict(q, **d["question"])
        v, cause = retry(rules_verdict, check, broken, slot)
        out.append({"question_id": qid, "copy": "damaged", "rule": d["rule"], "damage": d.get("what"),
                    "expected": "fail on %s" % d["rule"], "error": cause, "verdict": v})
    for e in out:
        v = e["verdict"] or {}
        e["as_expected"] = (v.get("verdict") == "pass") if e["copy"] == "good" else (e["rule"] in v.get("failed_rules", []))
        print("%s %s: %s %s" % (e["question_id"], e["copy"], v.get("verdict"), "ok" if e["as_expected"] else "NOT as expected"))
    result = {"checks": out, "as_expected": sum(e["as_expected"] for e in out), "of": len(out), "cost": cost(model_call)}
    save("part3.json", result)
    print("As expected: %d of %d" % (result["as_expected"], result["of"]))
    return result


def part_b7(records, model_call):
    """Decision 0043: call 4b with rule B7 on the 9 good questions and on the
    question that the owner marked bad for clarity (T-M1-S05). Each good
    question must pass. T-M1-S05 must fail on B7."""
    p1 = load("part1.json")
    by_id = {e["question"]["question_id"]: e for e in p1["questions"] if e.get("question")}
    marking = Marking(load_plan(), records, MARKING)
    marking.prefix = "test-0024"
    marks = {m["question_id"]: m["mark"] for m in marking.read(1)}
    check = ModelCheck(records, model_call)
    out = []
    for qid, mark in sorted(marks.items()):
        entry = by_id[qid]
        v, cause = retry(rules_verdict, check, entry["question"], entry["slot"])
        expected = "pass" if mark == "good" else "fail on B7"
        ok = v is not None and (v["verdict"] == "pass" if mark == "good" else "B7" in v["failed_rules"])
        out.append({"question_id": qid, "mark": mark, "expected": expected, "error": cause, "verdict": v, "as_expected": ok})
        print("%s (%s): %s %s %s" % (qid, mark, v and v["verdict"], v and v["failed_rules"], "ok" if ok else "NOT as expected"))
    result = {"checks": out, "as_expected": sum(e["as_expected"] for e in out), "of": len(out), "cost": cost(model_call)}
    save("part-b7.json", result)
    print("As expected: %d of %d" % (result["as_expected"], result["of"]))
    return result


# Part 4 (decisions 0034 part 7 and 0042): a copy that the assistant wrote by hand.
# It has the same scene as T-M1-S06: the same problem (find every caller of a
# deprecated function in a local repository) and the same correct action (Grep).
SAME_SCENE = {
    "question_id": "T-M1-S15", "slot_id": "M1-S15", "try": 1, "select": 1, "status": "written",
    "question": ("The research team must find out which modules of a locally cloned open-source project still call the "
                 "deprecated function load_old_settings. The document analysis subagent can use the built-in tools. "
                 "Its first step is to list every place in the code that calls this function. "
                 "Which tool should the document analysis subagent use for this first step?"),
    "options": [
        {"letter": "A", "text": "Use Grep to search the contents of the project files for load_old_settings and list each matching call.",
         "correct": True, "reason": "Grep searches file contents, so it finds each caller of a function by its name."},
        {"letter": "B", "text": "Use Glob with the pattern **/*load_old_settings* to find each file that calls the function.",
         "correct": False, "reason": "Glob matches file paths by name or extension patterns. It does not search file contents."},
        {"letter": "C", "text": "Use Read to load each source file of the project first, and then look in each file for the calls.",
         "correct": False, "reason": "The guide advises to start with Grep and read files selectively, not to read all files first."},
        {"letter": "D", "text": "Use Write to add a log line to the function so that each call reports its caller during a run.",
         "correct": False, "reason": "Write is for full file operations. It changes the code and does not search for the callers."},
    ],
}


def part4(records, plan, model_call):
    """Step 6 on a set of 15 questions of scenario 3 with two questions of the same
    scene: T-M1-S06 and the copy T-M1-S15. Call 6a must name both (rule D1)."""
    p1 = load("part1.json")
    have = {e["slot"]["slot_id"]: e["question"] for e in p1["questions"] if e.get("question")}
    writer = Writer(records, model_call, plan["seed"])
    scenario = plan["scenarios"][0]
    questions = []
    for slot in [s for s in plan["slots"] if s["scenario"] == scenario]:
        if slot["slot_id"] in have:
            questions.append(have[slot["slot_id"]])
        elif slot["slot_id"] == SAME_SCENE["slot_id"]:
            questions.append(dict(SAME_SCENE, point=slot["point"]))
        else:
            request = {"slot": slot, "point": slot["point"], "step": 2, "shown_try": None,
                       "failed_question": None, "findings": [], "other_questions": []}
            answer, cause = retry(writer.write, request)
            if answer is None or answer["status"] != "written":
                raise RunStopped("The writer gave no question for %s: %s" % (slot["slot_id"], cause))
            questions.append({"question_id": "T-%s" % slot["slot_id"], "slot_id": slot["slot_id"], "try": 1,
                              "point": slot["point"], "select": slot["select"], **answer})
            print("%s: written" % slot["slot_id"])
    results, cause = retry(ScenarioCheck(plan, model_call).check, scenario, questions)
    found = False
    for r in results or []:
        for f in r["findings"]:
            if r["rule"] == "D1" and {"T-M1-S06", "T-M1-S15"} <= set(f["question_ids"]):
                found = True
    result = {"scenario": scenario, "questions": questions, "results": results, "error": cause,
              "same_scene_found": found, "cost": cost(model_call)}
    save("part4.json", result)
    for r in results or []:
        print("%s %s %s" % (r["rule"], r["result"], [(f["question_ids"], f["detail"][:120]) for f in r["findings"]]))
    print("Same scene of T-M1-S06 and T-M1-S15 found: %s" % found)
    return result


def load_plan():
    with open(os.path.join(ROOT, "runs", "mock-01", "plan.json"), encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    p = argparse.ArgumentParser(description="The test of decisions 0024 and 0042.")
    p.add_argument("part", choices=["part1", "part2", "part3", "b7", "part4"])
    a = p.parse_args(argv)
    records = load_records()
    model_call = ModelCall()
    try:
        if a.part == "part1":
            r = part1(records, load_plan(), model_call)
        elif a.part == "part2":
            r = part2(records, model_call)
        elif a.part == "part3":
            r = part3(records, model_call)
        elif a.part == "b7":
            r = part_b7(records, model_call)
        else:
            r = part4(records, load_plan(), model_call)
    except RunStopped as e:
        print("Stopped: %s" % e)
        print("Cost so far: %s" % json.dumps(cost(model_call)))
        return 1
    except MarkingError as e:
        print("Refused: %s" % e)
        return 1
    print("Cost: %s" % json.dumps(r["cost"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
