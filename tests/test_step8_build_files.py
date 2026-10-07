"""Tests of step 8, the files of a mock (decision 0036). No test makes a model call.

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

from step1_plan import make_plan, RECORDS as RECORDS_PATH  # noqa: E402
from step8_build_files import build, BuildError, MINUTES  # noqa: E402

with open(RECORDS_PATH, encoding="utf-8") as f:
    RECORDS = json.load(f)
PLAN = make_plan(RECORDS, 1, 11, "2026-10-07")


def question_for(slot, n_try=1):
    options = [{"letter": "ABCDE"[i], "text": "Option text %d of %s." % (i, slot["slot_id"]),
                "correct": i < slot["select"], "reason": "Reason %d of %s." % (i, slot["slot_id"])}
               for i in range(slot["options"])]
    return {"question_id": "%s-T%d" % (slot["slot_id"], n_try), "slot_id": slot["slot_id"], "try": n_try,
            "point": slot["point"], "select": slot["select"], "status": "written",
            "question": "Question of %s?" % slot["slot_id"], "options": options}


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.questions = [question_for(s) for s in PLAN["slots"]]

    def tearDown(self):
        shutil.rmtree(self.folder)

    def load(self, paths):
        out = []
        for p in paths:
            with open(p, encoding="utf-8") as f:
                out.append(json.load(f))
        return out

    def test_two_files(self):
        paths = build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08")
        self.assertEqual([os.path.basename(p) for p in paths], ["mock-01.questions.json", "mock-01.answers.json"])
        qf, af = self.load(paths)
        self.assertEqual((qf["mock"], qf["minutes"], qf["seed"], qf["date"]), (1, MINUTES, 11, "2026-10-08"))
        self.assertEqual(qf["guide_version"], RECORDS["guide"]["version"])

    def test_the_questions_file_has_no_answers(self):
        qf, _ = self.load(build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08"))
        text = json.dumps(qf)
        self.assertNotIn('"correct"', text)
        self.assertNotIn('"reason"', text)
        self.assertNotIn("Reason ", text)

    def test_four_groups_by_scenario_with_their_story(self):
        qf, _ = self.load(build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08"))
        stories = {s["id"]: s["story"] for s in RECORDS["scenarios"]}
        self.assertEqual([g["scenario"] for g in qf["groups"]], PLAN["scenarios"])
        for g in qf["groups"]:
            self.assertEqual(len(g["questions"]), 15)
            self.assertEqual(g["story"], stories[g["scenario"]])
        numbers = [q["number"] for g in qf["groups"] for q in g["questions"]]
        self.assertEqual(numbers, list(range(1, 61)))

    def test_each_question_has_its_fields(self):
        qf, _ = self.load(build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08"))
        q = qf["groups"][0]["questions"][0]
        self.assertEqual(set(q), {"number", "question_id", "domain", "task_statement", "point", "type",
                                  "select", "question", "options"})
        self.assertIn(q["select"], (1, 2))
        self.assertEqual(set(q["options"][0]), {"letter", "text"})

    def test_the_answers_file(self):
        _, af = self.load(build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08"))
        self.assertEqual(len(af["answers"]), 60)
        first = af["answers"][0]
        slot = PLAN["slots"][0]
        self.assertEqual(first["correct"], ["A", "B"][:slot["select"]])
        self.assertEqual(len(first["options"]), slot["options"])
        self.assertEqual(set(first["options"][0]), {"letter", "correct", "reason"})

    def test_no_file_is_written_over(self):
        build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08")
        with self.assertRaises(BuildError):
            build(PLAN, self.questions, RECORDS, self.folder, "2026-10-09")

    def test_a_missing_question_builds_nothing(self):
        with self.assertRaises(BuildError):
            build(PLAN, self.questions[:-1], RECORDS, self.folder, "2026-10-08")
        self.assertEqual(os.listdir(self.folder), [])

    def test_a_cannot_write_record_builds_nothing(self):
        self.questions[5] = {"question_id": "M1-S06-T1", "slot_id": "M1-S06", "status": "cannot_write"}
        with self.assertRaises(BuildError):
            build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08")
        self.assertEqual(os.listdir(self.folder), [])

    def refused(self, change, words):
        change(self.questions)
        with self.assertRaises(BuildError) as e:
            build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08")
        self.assertIn(words, str(e.exception))
        self.assertEqual(os.listdir(self.folder), [])

    def test_a_record_that_does_not_agree_with_its_slot_builds_nothing(self):
        self.refused(lambda qs: qs[0]["options"].pop(), "options")

    def test_wrong_correct_marks_build_nothing(self):
        def all_correct(qs):
            for o in qs[0]["options"]:
                o["correct"] = True
        self.refused(all_correct, "correct options")

    def test_a_mark_that_is_not_true_or_false_builds_nothing(self):
        self.refused(lambda qs: qs[0]["options"][1].update(correct="no"), "not complete")

    def test_wrong_letters_build_nothing(self):
        def same(qs):
            for o in qs[0]["options"]:
                o["letter"] = "A"
        self.refused(same, "letters")

    def test_a_question_of_another_slot_builds_nothing(self):
        self.refused(lambda qs: qs[0].update(question_id="M1-S02-T1"), "does not belong")

    def test_slots_out_of_sequence_build_nothing(self):
        plan = json.loads(json.dumps(PLAN))
        plan["slots"][0], plan["slots"][1] = plan["slots"][1], plan["slots"][0]
        with self.assertRaises(BuildError) as e:
            build(plan, self.questions, RECORDS, self.folder, "2026-10-08")
        self.assertIn("sequence", str(e.exception))

    def test_groups_that_do_not_agree_with_the_plan_build_nothing(self):
        plan = json.loads(json.dumps(PLAN))
        plan["scenarios"] = list(reversed(plan["scenarios"]))
        with self.assertRaises(BuildError) as e:
            build(plan, self.questions, RECORDS, self.folder, "2026-10-08")
        self.assertIn("groups", str(e.exception))

    def test_a_failed_write_leaves_no_half_mock(self):
        real = json.dump
        calls = []

        def broken(data, f, **kw):
            calls.append(1)
            if len(calls) == 2:
                raise OSError("disk full")
            return real(data, f, **kw)
        import step8_build_files
        step8_build_files.json.dump = broken
        try:
            with self.assertRaises(OSError):
                build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08")
        finally:
            step8_build_files.json.dump = real
        self.assertEqual(os.listdir(self.folder), [])

    def test_the_point_of_a_new_point_decision_is_used(self):
        self.questions[0]["point"] = "X-K9"
        qf, _ = self.load(build(PLAN, self.questions, RECORDS, self.folder, "2026-10-08"))
        self.assertEqual(qf["groups"][0]["questions"][0]["point"], "X-K9")


if __name__ == "__main__":
    unittest.main()
