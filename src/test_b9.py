"""The test of the stricter rule B9 on mock 3, before mock 4 (decision 0066).

Call 4b checks each of the 60 questions of the built mock 3, with the questions
of mocks 1 and 2 on the same idea, and the text of B9 of decision 0066. The
script saves the result of rule B9 for each question, and the cost. It changes
no record of mock 3.

Run from the folder ccar-f-mock-generator (the API key comes from the environment):
    python3 src/test_b9.py
It writes runs/test-b9/results.json.
"""
import json
import os
import sys

from control import CallFailed
from earlier import Earlier
from model_call import ModelCall, cost
from step4_check_model import ModelCheck
from steps import ROOT, load_records

FOLDER = os.path.join(ROOT, "runs", "test-b9")


def mock3_questions():
    """The 60 built questions of mock 3, in the form of a question record."""
    with open(os.path.join(ROOT, "mocks", "mock-03.questions.json"), encoding="utf-8") as f:
        built = json.load(f)
    with open(os.path.join(ROOT, "mocks", "mock-03.answers.json"), encoding="utf-8") as f:
        answers = {a["question_id"]: a for a in json.load(f)["answers"]}
    out = []
    for g in built["groups"]:
        for q in g["questions"]:
            a = answers[q["question_id"]]
            reasons = {r["letter"]: r["reason"] for r in a.get("options", []) if isinstance(r, dict)}
            out.append(({"question_id": q["question_id"], "point": q["point"], "question": q["question"],
                         "select": q["select"],
                         "options": [{"letter": o["letter"], "text": o["text"], "correct": o["letter"] in a["correct"],
                                      "reason": reasons.get(o["letter"], "")} for o in q["options"]]},
                        {"scenario": g["scenario"], "task_statement": q["task_statement"], "point": q["point"]}))
    return out


def main():
    records = load_records()
    call = ModelCall()
    earlier = Earlier(os.path.join(ROOT, "mocks"), 3)
    check = ModelCheck(records, call, earlier=earlier.on_idea)
    results = []
    for question, slot in mock3_questions():
        found = earlier.on_idea(question["point"])
        entry = {"question_id": question["question_id"], "point": question["point"],
                 "earlier": [q["question_id"] for q in found]}
        try:
            answer, model = check.rules(question, slot)
            b9 = next(r for r in answer["results"] if r["rule"] == "B9")
            entry.update(result=b9["result"], finding=b9.get("finding"), model=model)
        except (CallFailed, StopIteration) as e:
            entry.update(result="error", finding=str(e))
        results.append(entry)
        print(entry["question_id"], entry["result"], flush=True)
    os.makedirs(FOLDER, exist_ok=True)
    data = {"decision": "0066", "mock": 3, "results": results, "cost": cost(call.usage)}
    with open(os.path.join(FOLDER, "results.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    fails = [r for r in results if r["result"] == "fail"]
    print("B9 fails %d of %d. Cost: $%.2f." % (len(fails), len(results), data["cost"]["dollars"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
