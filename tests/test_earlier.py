"""Tests of the rule against repeats across mocks (decision 0056). No test makes a model call.

Run from the folder ccar-f-mock-generator:
    python3 -m unittest discover tests
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import point_groups  # noqa: E402
import step1_plan  # noqa: E402
from earlier import Earlier, EarlierError  # noqa: E402
from model_call import ModelCall  # noqa: E402
from step2_write import EARLIER_RULE, Writer, request_text  # noqa: E402
from step4_check_model import ModelCheck  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCKS = os.path.join(ROOT, "mocks")
with open(step1_plan.RECORDS, encoding="utf-8") as f:
    RECORDS = json.load(f)
OF = point_groups.group_of(point_groups.load())


class TestEarlier(unittest.TestCase):
    def test_mock_1_has_no_earlier_mock(self):
        self.assertEqual(Earlier(MOCKS, 1).questions, [])

    def test_mock_2_reads_the_60_questions_of_mock_1_with_their_marks(self):
        e = Earlier(MOCKS, 2)
        self.assertEqual(len(e.questions), 60)
        for q in e.questions:
            self.assertGreaterEqual(sum(o["correct"] for o in q["options"]), 1)

    def test_on_idea_gives_the_questions_of_the_same_group(self):
        e = Earlier(MOCKS, 2)
        found = e.on_idea("1.1-S3")   # group G001, with 1.1-S1 of M1-S28
        self.assertIn("M1-S28-T2", [q["question_id"] for q in found])
        self.assertTrue(all(OF[q["point"]]["id"] == OF["1.1-S3"]["id"] for q in found))

    def test_a_bad_built_file_is_an_error(self):
        folder = tempfile.mkdtemp()
        try:
            with open(os.path.join(folder, "mock-01.questions.json"), "w", encoding="utf-8") as f:
                f.write("{}")
            with self.assertRaises(EarlierError):
                Earlier(folder, 2)
        finally:
            shutil.rmtree(folder)


class TestStep1(unittest.TestCase):
    def test_a_point_that_mock_1_used_is_taken_only_when_its_group_has_no_unused_point(self):
        earlier = step1_plan.earlier_points(MOCKS, 2)
        used = set(earlier[1])
        ts_points = {t["id"]: [p["id"] for p in t["points"]] for t in RECORDS["task_statements"]}
        for seed in range(10):
            plan = step1_plan.make_plan(RECORDS, 2, seed, "2026-10-08", None, earlier)
            for s in plan["slots"]:
                if s["point"] in used:
                    group = OF[s["point"]]["id"]
                    free = [p for p in ts_points[s["task_statement"]] if OF[p]["id"] == group and p not in used]
                    self.assertEqual(free, [], (seed, s["slot_id"], s["point"], free))


class FakeCall:
    def __init__(self, answer):
        self.answer = answer
        self.texts = []

    def ask(self, system, text, schema):
        self.texts.append(text)
        return self.answer, "claude-x"


class TestWriterAndCheck(unittest.TestCase):
    def setUp(self):
        self.plan = json.load(open(os.path.join(ROOT, "runs", "mock-02", "plan.json"), encoding="utf-8"))
        self.slot = next(s for s in self.plan["slots"] if s["point"] == "1.1-S3")
        self.earlier = Earlier(MOCKS, 2).on_idea

    def request(self):
        return {"slot": self.slot, "point": self.slot["point"], "step": 2, "shown_try": None,
                "failed_question": None, "findings": [], "other_questions": []}

    def test_the_writer_gets_the_earlier_questions_and_the_rule(self):
        call = FakeCall({"status": "cannot_write", "question": "", "options": [], "cannot_write_reason": "x"})
        try:
            Writer(RECORDS, call, earlier=self.earlier).write(self.request())
        except Exception:
            pass
        self.assertIn(EARLIER_RULE, call.texts[0])
        self.assertIn("M1-S28-T2", call.texts[0])
        self.assertIn("B9. The question does not have the same problem", call.texts[0])
        self.assertIn("At most one wrong option may repeat.", call.texts[0])

    def test_no_earlier_question_no_section(self):
        self.assertNotIn(EARLIER_RULE, request_text(self.request(), RECORDS))

    def test_call_4b_gets_the_earlier_questions(self):
        q = {"question_id": "M2-S08-T9", "point": "1.1-S3", "question": "Q?", "select": 1,
             "options": [{"letter": "A", "text": "a", "correct": True, "reason": "r"},
                         {"letter": "B", "text": "b", "correct": False, "reason": "r"}]}
        call = FakeCall({"results": [], "features": []})
        check = ModelCheck(RECORDS, call, earlier=self.earlier)
        with self.assertRaises(Exception):
            check.rules(q, self.slot)
        self.assertIn("THE EARLIER QUESTIONS ON THE SAME IDEA (for rule B9):", call.texts[0])
        self.assertIn("M1-S28-T2", call.texts[0])
        call2 = FakeCall({"results": [], "features": []})
        with self.assertRaises(Exception):
            ModelCheck(RECORDS, call2).rules(q, self.slot)
        self.assertIn("(for rule B9):\nNone.", call2.texts[0])


class TestRealSteps(unittest.TestCase):
    """The review of 8 October 2026: the real steps must give the earlier
    questions to the writer and to call 4b."""

    def test_the_real_steps_pass_the_earlier_questions(self):
        from steps import RealSteps
        steps = RealSteps(os.path.join(ROOT, "runs", "mock-02"), records=RECORDS, model_call=FakeCall({}))
        plan = json.load(open(os.path.join(ROOT, "runs", "mock-02", "plan.json"), encoding="utf-8"))
        slot = next(s for s in plan["slots"] if s["point"] == "1.1-S3")
        seen = {}
        steps.writer.write = lambda request: seen.setdefault("writer", steps.writer.earlier)
        steps.checker.check = lambda q, s: seen.setdefault("checker", steps.checker.earlier)
        steps.write({"slot": slot, "point": slot["point"], "step": 2})
        steps.check_model({"point": "1.1-S3"}, slot)
        for who in ("writer", "checker"):
            self.assertIsNotNone(seen[who], who)
            self.assertIn("M1-S28-T2", [q["question_id"] for q in seen[who]("1.1-S3")])


if __name__ == "__main__":
    unittest.main()
