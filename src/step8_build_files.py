"""Step 8 of the pipeline: code builds the two files of a mock (decisions 0016 and 0036).

The control checks the six conditions of decision 0039, item 10, before it calls
this step. The step builds the files only from the plan, the question records
and the guide records. Nobody edits the files by hand. The step does not write
over files that exist.

    mocks/mock-01.questions.json   the 60 questions, with no answers and no reasons
    mocks/mock-01.answers.json     the correct letters, and the reason of each option

The exact field names were not decided in decision 0036. These are the names
that the code uses.
"""
import json
import os

MINUTES = 120   # decision 0003


class BuildError(Exception):
    """The step cannot build the files. The message names the cause."""


def check_record(q, slot):
    """The record must agree with its slot. The control already checked steps 3 and
    4 and the fingerprints. This is a last check before a participant sees the file."""
    sid = slot["slot_id"]
    if not isinstance(q, dict) or q.get("status") != "written":
        raise BuildError("%s has no written question." % sid)
    if not str(q.get("question_id", "")).startswith(sid + "-T"):
        raise BuildError("%s: the question %s does not belong to the slot." % (sid, q.get("question_id")))
    if not isinstance(q.get("question"), str) or not q["question"].strip():
        raise BuildError("%s: the question has no text." % sid)
    options = q.get("options")
    if not isinstance(options, list) or len(options) != slot["options"]:
        raise BuildError("%s: the question does not have %d options." % (sid, slot["options"]))
    for o in options:
        if not (isinstance(o, dict) and isinstance(o.get("text"), str) and isinstance(o.get("reason"), str)
                and isinstance(o.get("correct"), bool)):
            raise BuildError("%s: an option is not complete." % sid)
    if [o["letter"] for o in options] != list("ABCDE"[:len(options)]):
        raise BuildError("%s: the options do not have the letters A to E in sequence." % sid)
    if sum(o["correct"] for o in options) != slot["select"]:
        raise BuildError("%s: the question does not have %d correct options." % (sid, slot["select"]))
    if q.get("select") != slot["select"]:
        raise BuildError("%s: the question and the slot have a different number to select." % sid)


def build(plan, questions, records, folder, date):
    """Build the two files. `questions` are the 60 current question records, one
    for each slot. Return the two paths."""
    if any(not isinstance(q, dict) or "slot_id" not in q for q in questions):
        raise BuildError("A question record has no slot.")
    by_slot = {q["slot_id"]: q for q in questions}
    slots = plan["slots"]
    if len(by_slot) != len(questions) or set(by_slot) != {s["slot_id"] for s in slots}:
        raise BuildError("The questions do not agree with the 60 slots of the plan.")
    scenarios = {s["id"]: s for s in records["scenarios"]}
    domain_of = {t["id"]: t["domain"] for t in records["task_statements"]}
    mock = plan["mock"]
    paths = [os.path.join(folder, "mock-%02d.questions.json" % mock),
             os.path.join(folder, "mock-%02d.answers.json" % mock)]
    for p in paths:
        if os.path.exists(p):
            raise BuildError("The file exists already: %s" % p)

    groups, answers = [], []
    for number, slot in enumerate(slots, start=1):
        q = by_slot[slot["slot_id"]]
        check_record(q, slot)
        if int(slot["slot_id"].split("-S")[1]) != number:
            raise BuildError("The slots are not in the sequence 1 to 60.")
        if not groups or groups[-1]["scenario"] != slot["scenario"]:
            sc = scenarios[slot["scenario"]]
            groups.append({"scenario": sc["id"], "name": sc["name"], "story": sc["story"], "questions": []})
        groups[-1]["questions"].append({
            "number": number, "question_id": q["question_id"], "domain": domain_of[slot["task_statement"]],
            "task_statement": slot["task_statement"], "point": q.get("point", slot["point"]),
            "type": slot["type"], "select": slot["select"], "question": q["question"],
            "options": [{"letter": o["letter"], "text": o["text"]} for o in q["options"]]})
        answers.append({
            "number": number, "question_id": q["question_id"],
            "correct": [o["letter"] for o in q["options"] if o["correct"]],
            "options": [{"letter": o["letter"], "correct": o["correct"], "reason": o["reason"]} for o in q["options"]]})
    if len(groups) != len(plan["scenarios"]) or [g["scenario"] for g in groups] != plan["scenarios"]:
        raise BuildError("The groups do not agree with the scenarios of the plan.")

    questions_file = {"mock": mock, "guide_version": plan["guide_version"], "seed": plan["seed"],
                      "date": date, "minutes": MINUTES, "groups": groups}
    answers_file = {"mock": mock, "answers": answers}
    # Write both files first with a temporary name. Only when both exist, give
    # them their names. So a failure leaves no half mock.
    os.makedirs(folder, exist_ok=True)
    temporary = [p + ".tmp" for p in paths]
    try:
        for path, data in zip(temporary, (questions_file, answers_file)):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        for tmp, path in zip(temporary, paths):
            os.replace(tmp, path)
    finally:
        for tmp in temporary:
            if os.path.exists(tmp):
                os.remove(tmp)
    return paths
