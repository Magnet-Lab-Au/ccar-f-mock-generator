"""Step 6: the check of the complete mock, one scenario at a time (decisions 0014, 0034, 0038, 0039 and 0040).

Code counts the questions of the scenario against the plan (rules C2 and C3).
The control already checked rule C1: it starts step 6 only when each slot has
the status passed. Then two model calls read the 15 questions together: call
6a (rules D1 and D4) and call 6b (rules D2 and D3). Step 6 sends no question
back. Each finding goes to the owner (decision 0038, part 3).
"""
from control import CallFailed
from model_call import load_form
from step4_check_model import show

DESCRIPTION, SCHEMA = load_form("08-form-draft.json")

RULES_6A = """D1. No two questions have the same scene. Two questions have the same scene when they have the same problem and the same correct action.
D4. No question gives away the answer of a different question."""
RULES_6B = """D2. No wrong idea is a wrong option in more than 2 questions of the scenario.
D3. At most one wrong option of the scenario is this option: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger. A use of model confidence that the exam guide teaches as correct does not count: field-level confidence scores calibrated with labeled validation sets, used to route review attention or to send items to human review. The option also does not count when it is the correct answer."""

SYSTEM = ("You check the 15 questions of one scenario of a mock exam together. Give one result for each rule of this call: "
          "pass, fail or cannot_decide. A finding names the questions by their IDs. " + DESCRIPTION)


def code_count(scenario, questions, slots):
    """Rules C2 and C3 for one scenario. C2 failing raises CallFailed: it is an
    error for the owner (decision 0034). C3 failing is a finding."""
    plan = [s for s in slots if s["scenario"] == scenario]
    by_slot = {q["slot_id"]: q for q in questions}
    if sorted(by_slot) != sorted(s["slot_id"] for s in plan):
        raise CallFailed("Rule C2: the questions of scenario %s do not agree with the plan." % scenario)
    for s in plan:
        q = by_slot[s["slot_id"]]
        if q.get("select") != s["select"] or len(q.get("options", [])) != s["options"]:
            raise CallFailed("Rule C2: %s does not agree with its slot." % q["question_id"])
    seen, results = {}, []
    for q in questions:
        key = " ".join(q["question"].lower().split())
        if key in seen:
            results.append({"rule": "C3", "result": "fail", "findings": [
                {"question_ids": [seen[key], q["question_id"]], "detail": "The two questions have the same text."}]})
        seen.setdefault(key, q["question_id"])
    return results


class ScenarioCheck:
    def __init__(self, plan, model_call):
        self.slots = plan["slots"]
        self.model_call = model_call

    def _call(self, rules, wanted, text):
        answer, model = self.model_call.ask(SYSTEM, "THE RULES OF THIS CALL\n%s\n\n%s" % (rules, text), SCHEMA)
        results = answer.get("results") if isinstance(answer, dict) else None
        if not isinstance(results, list) or sorted(r.get("rule") for r in results) != sorted(wanted):
            raise CallFailed("The answer does not have one result for each rule %s." % ", ".join(wanted))
        out = []
        for r in results:
            if r.get("result") not in ("pass", "fail", "cannot_decide"):
                raise CallFailed("Rule %s has no valid result." % r.get("rule"))
            out.append({"rule": r["rule"], "result": r["result"],
                        "findings": [{"question_ids": f.get("question_ids") or [], "detail": f.get("detail", "")}
                                     for f in (r.get("findings") or [])]})
        return out, model

    def check(self, scenario, questions):
        """Return the results of all rules for one scenario, in the form that the
        control expects. The control checks the findings (decision 0039, rule 11)."""
        results = code_count(scenario, questions, self.slots)
        scenes = "\n\n".join("QUESTION %s\n%s" % (q["question_id"], show(q, with_key=True)) for q in questions)
        wrong = "\n\n".join("QUESTION %s\n%s" % (q["question_id"], "\n".join(
            "%s. %s\n   Reason: %s" % (o["letter"], o["text"], o["reason"]) for o in q["options"] if not o["correct"]))
            for q in questions)
        a, _ = self._call(RULES_6A, ["D1", "D4"], "THE 15 QUESTIONS, with their options and marks:\n\n" + scenes)
        b, _ = self._call(RULES_6B, ["D2", "D3"], "THE WRONG OPTIONS of the 15 questions, with their reasons:\n\n" + wrong)
        return results + a + b
