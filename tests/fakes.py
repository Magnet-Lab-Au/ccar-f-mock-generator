"""Fake steps for the tests of the control. No fake makes a model call.

A test tells each fake what to answer. A fake that has no instruction gives
the answer of the path with no failure.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from control import CallFailed  # noqa: E402

SCENARIOS = [1, 3, 5, 6]
# 30 task statements: 7, 5, 6, 6 and 6 for the 5 domains.
TASK_STATEMENTS = (["1.%d" % i for i in range(1, 8)] + ["2.%d" % i for i in range(1, 6)]
                   + ["3.%d" % i for i in range(1, 7)] + ["4.%d" % i for i in range(1, 7)]
                   + ["5.%d" % i for i in range(1, 7)])
# Each task statement has 3 points in the fake guide. The plan uses K1 and K2.
GUIDE_POINTS = {ts: ["%s-K%d" % (ts, k) for k in (1, 2, 3)] for ts in TASK_STATEMENTS}


def fake_plan(mock, seed):
    slots = []
    for n in range(1, 61):
        ts = TASK_STATEMENTS[(n - 1) % 30]
        point = "%s-K%d" % (ts, 1 if n <= 30 else 2)
        scenario = SCENARIOS[(n - 1) // 15]
        multiple = (n - 1) % 15 in (0, 1)
        slots.append({"slot_id": "M%d-S%02d" % (mock, n), "scenario": scenario,
                      "task_statement": ts, "point": point,
                      "type": "multiple_response" if multiple else "multiple_choice",
                      "options": 5 if multiple else 4, "select": 2 if multiple else 1})
    return {"mock": mock, "seed": seed, "guide_version": "1.0", "date": "2026-10-07",
            "scenarios": SCENARIOS, "table": {}, "slots": slots}


class FakeSteps:
    def __init__(self):
        self.write_script = {}      # slot_id -> list of "ok", "cannot_write", "call_fails"
        self.code_script = {}       # slot_id -> list of "pass", "fail"
        self.model_script = {}      # slot_id -> list of "pass", "fail", "cannot_decide", "call_fails"
        self.scenario_script = {}   # scenario -> list of result lists
        self.marks = {}             # question_id -> {"mark": ..., "reason": ...}
        self.requests = []
        self.model_calls = []
        self.scenario_calls = []
        self.marking_files = {}
        self.builds = []

    @staticmethod
    def _next(script, key, default):
        queue = script.get(key)
        if queue:
            return queue.pop(0)
        return default

    def plan(self, mock, seed):
        return fake_plan(mock, seed)

    def write(self, request):
        slot = request["slot"]
        self.requests.append(request)
        action = self._next(self.write_script, slot["slot_id"], "ok")
        if action == "call_fails":
            raise CallFailed("the API call failed")
        if action == "cannot_write":
            return {"status": "cannot_write", "question": None, "options": [],
                    "cannot_write_reason": "The task statement does not fit the scenario."}
        n = len(self.requests)
        options = []
        for i in range(slot["options"]):
            options.append({"letter": "ABCDE"[i], "text": "Option text %d of call %d." % (i, n),
                            "correct": i < slot["select"], "reason": "Reason %d." % i})
        return {"status": "written", "question": "Question of call %d for %s?" % (n, slot["slot_id"]),
                "options": options, "cannot_write_reason": None}

    def check_code(self, question, slot):
        result = self._next(self.code_script, slot["slot_id"], "pass")
        findings = [] if result == "pass" else [
            {"step": 3, "rule": "A6", "detail": "The question is too long.", "letter": None,
             "point": None, "other_questions": []}]
        return {"verdict": result, "findings": findings}

    def check_model(self, question, slot):
        self.model_calls.append(question["question_id"])
        result = self._next(self.model_script, slot["slot_id"], "pass")
        if result == "call_fails":
            raise CallFailed("the API call failed")
        findings = [] if result == "pass" else [
            {"step": 4, "rule": "B1", "detail": "Option C is also correct (%s)." % result,
             "letter": "C", "point": None, "other_questions": []}]
        return {"verdict": result, "findings": findings}

    def check_scenario(self, scenario, questions, others=()):
        self.scenario_calls.append(scenario)
        self.scenario_others = [q["question_id"] for q in others]
        self.scenario_own = [q["question_id"] for q in questions]
        results = self._next(self.scenario_script, scenario, None)
        if results == "call_fails":
            raise CallFailed("the API call failed")
        if results is None:
            results = [{"rule": r, "result": "pass", "findings": []}
                       for r in ("D1", "D2", "D3", "D4")]
        return results

    def make_marking_file(self, round_number, questions):
        self.marking_files[round_number] = [q["question_id"] for q in questions]

    def read_marking_file(self, round_number):
        result = []
        for qid in self.marking_files[round_number]:
            m = self.marks.get(qid, {"mark": "good", "reason": ""})
            if m is not None:
                result.append(dict(m, question_id=qid))
        return result

    def build(self, plan, questions):
        self.builds.append([q["question_id"] for q in questions])
        return ["mocks/mock-%02d.questions.json" % plan["mock"],
                "mocks/mock-%02d.answers.json" % plan["mock"]]
