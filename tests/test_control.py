"""Tests of the control (decision 0038). No test makes a model call.

Run from the folder ccar-f-mock-generator:
    python3 -m unittest discover tests
"""
import json
import os
import shutil
import tempfile
import unittest

from fakes import FakeSteps, GUIDE_POINTS, fake_plan
from control import Control, Refused


class Base(unittest.TestCase):
    mock = 1

    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.steps = FakeSteps()

    def tearDown(self):
        shutil.rmtree(self.folder)

    def control(self, steps=None):
        return Control(self.folder, self.mock, 42, steps or self.steps, GUIDE_POINTS,
                       today=lambda: "2026-10-07")

    def read_text(self, name):
        with open(os.path.join(self.folder, name), encoding="utf-8") as f:
            return f.read()

    def status(self, c, slot_id):
        return c.slot_state(c._slot(slot_id))

    def run_to_marks(self, c):
        report = c.run()
        self.assertEqual(report["state"], "ready_to_mark", report["waiting_for"])
        return report

    def finding(self, rule, ids, result="fail"):
        results = [{"rule": r, "result": "pass", "findings": []}
                   for r in ("D1", "D2", "D3", "D4") if r != rule]
        results.append({"rule": rule, "result": result,
                        "findings": [{"question_ids": ids, "detail": "The same scene."}]})
        return results


class TestPathWithNoFailure(Base):
    def test_path_with_no_failure(self):
        c = self.control()
        report = self.run_to_marks(c)
        self.assertEqual(len(self.steps.requests), 60)
        self.assertEqual(len(self.steps.model_calls), 60)
        self.assertEqual(sorted(self.steps.scenario_calls), [1, 3, 5, 6])
        self.assertEqual(len(self.steps.marking_files[1]), 60)
        self.assertTrue(all(s["status"] == "passed" for s in report["slots"]))
        self.assertEqual(report["waiting_for"], ["marks of round 1"])

        report = c.read_marks()
        self.assertEqual(report["state"], "waits_for_owner")
        self.assertEqual(report["waiting_for"], ["accept the mock"])

        report = c.accept()
        self.assertEqual(report["state"], "built")
        self.assertEqual(len(self.steps.builds), 1)
        self.assertEqual(len(self.steps.builds[0]), 60)

    def test_each_request_is_step_2(self):
        self.control().run()
        self.assertTrue(all(r["step"] == 2 and r["shown_try"] is None for r in self.steps.requests))

    def test_a_record_is_never_written_over(self):
        c = self.control()
        c.run()
        with self.assertRaises(RuntimeError):
            c._write_new({}, "plan.json")


class TestCaseA(Base):
    """(a) Fail on try 1, "cannot decide" on tries 2 and 3."""

    def test_open_with_both_reasons(self):
        self.steps.model_script["M1-S05"] = ["fail", "cannot_decide", "cannot_decide"]
        c = self.control()
        report = c.run()
        s = self.status(c, "M1-S05")
        self.assertEqual(s["status"], "open")
        self.assertEqual(s["open_reasons"], ["three_tries", "cannot_decide_twice"])
        self.assertEqual(report["state"], "waits_for_owner")
        self.assertIn("open slot M1-S05: three_tries, cannot_decide_twice", report["waiting_for"])
        # Step 6 does not start while a slot is open.
        self.assertEqual(self.steps.scenario_calls, [])

    def test_tries_2_and_3_are_step_5_with_the_last_try(self):
        self.steps.model_script["M1-S05"] = ["fail", "fail", "pass"]
        self.control().run()
        requests = [r for r in self.steps.requests if r["slot"]["slot_id"] == "M1-S05"]
        self.assertEqual([r["step"] for r in requests], [2, 5, 5])
        self.assertEqual([r["shown_try"] for r in requests], [None, "M1-S05-T1", "M1-S05-T2"])
        self.assertEqual(requests[1]["findings"][0]["rule"], "B1")

    def test_more_tries_gives_3_new_tries(self):
        self.steps.model_script["M1-S05"] = ["fail", "fail", "fail", "fail", "pass"]
        c = self.control()
        c.run()
        c.decide("more_tries", "M1-S05", "Try again.")
        report = c.run()
        self.assertEqual(self.status(c, "M1-S05")["status"], "passed")
        self.assertEqual(self.status(c, "M1-S05")["tries"], 5)
        self.assertEqual(report["state"], "ready_to_mark")

    def test_a_decision_on_a_slot_that_is_not_open_is_refused(self):
        c = self.control()
        c.run()
        with self.assertRaises(Refused):
            c.decide("more_tries", "M1-S05", "")


class TestCaseB(Base):
    """(b) `cannot_write` on a new try after step 6."""

    def setUp(self):
        super().setUp()
        self.steps.scenario_script[1] = [self.finding("D1", ["M1-S03-T1", "M1-S04-T1"])]
        self.c = self.control()
        self.run_to_marks(self.c)
        self.c.read_marks()
        self.c.decide("rewrite", "M1-SC1-R1-F1", "Write a new scene.", question_id="M1-S04-T1")
        self.steps.write_script["M1-S04"] = ["cannot_write"]
        self.c.run()

    def test_the_slot_is_open(self):
        s = self.status(self.c, "M1-S04")
        self.assertEqual(s["status"], "open")
        self.assertEqual(s["open_reasons"], ["cannot_write"])

    def test_the_rewrite_request_is_step_5_with_the_finding_and_the_other_question(self):
        r = self.steps.requests[-1]
        self.assertEqual(r["step"], 5)
        self.assertEqual(r["shown_try"], "M1-S04-T1")
        self.assertEqual([f["rule"] for f in r["findings"]], ["D1", "owner"])
        self.assertEqual(r["findings"][0]["other_questions"], ["M1-S03-T1"])
        self.assertEqual([q["question_id"] for q in r["other_questions"]], ["M1-S03-T1"])

    def test_more_tries_after_cannot_write_is_step_2(self):
        self.c.decide("more_tries", "M1-S04", "Try again.")
        self.c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"]), (2, None))
        self.assertEqual(self.status(self.c, "M1-S04")["status"], "passed")

    def test_new_point_after_cannot_write_is_step_2_with_the_new_point(self):
        d = self.c.decide("new_point", "M1-S04", "A different point.")
        self.c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"], r["point"]), (2, None, d["point"]))


class TestCaseC(Base):
    """(c) `new_point`."""

    def test_new_point(self):
        self.steps.write_script["M1-S07"] = ["cannot_write"]
        c = self.control()
        c.run()
        plan_before = self.read_text("plan.json")
        d = c.decide("new_point", "M1-S07", "The point does not fit.")
        # The point is in the decision. The plan does not change.
        self.assertEqual(d["point"], "1.7-K3")
        self.assertEqual(self.read_text("plan.json"), plan_before)
        c.run()
        q = c._question("M1-S07-T2")
        self.assertEqual(q["point"], "1.7-K3")
        # No other slot has the new point.
        points = [c.point_of(s) for s in c.slots()]
        self.assertEqual(len(points), len(set(points)))
        # The same seed still gives the same plan.
        self.assertEqual(json.loads(plan_before), fake_plan(1, 42))

    def test_no_free_point_is_refused(self):
        self.steps.write_script["M1-S07"] = ["cannot_write", "cannot_write"]
        c = self.control()
        c.run()
        c.decide("new_point", "M1-S07", "First.")
        c.run()
        with self.assertRaises(Refused):
            c.decide("new_point", "M1-S07", "Second.")


class TestCaseD(Base):
    """(d) Step 6 has a finding, and the owner selects `ignore`."""

    def test_ignore_then_accept(self):
        self.steps.scenario_script[3] = [self.finding("D2", ["M1-S20-T1", "M1-S21-T1"])]
        c = self.control()
        report = self.run_to_marks(c)
        # Step 6 sent no question back.
        self.assertEqual(len(self.steps.requests), 60)
        report = c.read_marks()
        self.assertEqual(report["waiting_for"], ["finding M1-SC3-R1-F1 of step 6: ignore or rewrite"])
        with self.assertRaises(Refused):
            c.accept()
        c.decide("ignore", "M1-SC3-R1-F1", "Two different scenes.")
        self.assertEqual(c.accept()["state"], "built")

    def test_cannot_decide_of_step_6_also_waits_for_the_owner(self):
        self.steps.scenario_script[3] = [self.finding("D1", ["M1-S20-T1", "M1-S21-T1"],
                                                      result="cannot_decide")]
        c = self.control()
        self.run_to_marks(c)
        report = c.read_marks()
        self.assertEqual(report["step6_findings"][0]["result"], "cannot_decide")

    def test_a_decision_before_the_marks_is_refused(self):
        self.steps.scenario_script[3] = [self.finding("D2", ["M1-S20-T1", "M1-S21-T1"])]
        c = self.control()
        self.run_to_marks(c)
        with self.assertRaises(Refused) as e:
            c.decide("ignore", "M1-SC3-R1-F1", "")
        self.assertIn("Mark the questions first", str(e.exception))


class TestCaseE(Base):
    """(e) A bad mark, and the round after it."""

    def test_bad_mark_round(self):
        self.steps.marks["M1-S20-T1"] = {"mark": "bad", "reason": "C is also correct."}
        c = self.control()
        self.run_to_marks(c)
        report = c.read_marks()
        self.assertEqual(self.status(c, "M1-S20")["status"], "to_write")
        self.assertEqual(report["state"], "in_work")
        report = c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"]), (5, "M1-S20-T1"))
        self.assertEqual(r["findings"][0]["rule"], "owner")
        self.assertEqual(r["findings"][0]["detail"], "C is also correct.")
        # Step 6 runs again only for scenario 3.
        self.assertEqual(self.steps.scenario_calls, [1, 3, 5, 6, 3])
        # Round 2 has only the new question.
        self.assertEqual(self.steps.marking_files[2], ["M1-S20-T2"])
        self.assertEqual(report["state"], "ready_to_mark")
        c.read_marks()
        self.assertEqual(c.accept()["state"], "built")

    def test_a_new_question_that_clashes_goes_to_the_owner(self):
        self.steps.marks["M1-S20-T1"] = {"mark": "bad", "reason": "C is also correct."}
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        self.steps.scenario_script[3] = [self.finding("D1", ["M1-S19-T1", "M1-S20-T2"])]
        c.run()
        c.read_marks()
        report = c.report()
        self.assertEqual(report["waiting_for"], ["finding M1-SC3-R2-F1 of step 6: ignore or rewrite"])

    def test_6_bad_marks_do_not_stop_mock_1(self):
        for n in range(1, 7):
            self.steps.marks["M1-S%02d-T1" % n] = {"mark": "bad", "reason": "Bad."}
        c = self.control()
        self.run_to_marks(c)
        self.assertNotEqual(c.read_marks()["state"], "stopped")

    def test_7_bad_marks_stop_mock_1(self):
        for n in range(1, 8):
            self.steps.marks["M1-S%02d-T1" % n] = {"mark": "bad", "reason": "Bad."}
        c = self.control()
        self.run_to_marks(c)
        self.assertEqual(c.read_marks()["state"], "stopped")
        c.run()
        self.assertEqual(len(self.steps.requests), 60)

    def test_a_mark_that_is_not_good_or_bad_is_named(self):
        self.steps.marks["M1-S04-T1"] = {"mark": "good.", "reason": ""}
        self.steps.marks["M1-S05-T1"] = {"mark": None, "reason": ""}
        c = self.control()
        self.run_to_marks(c)
        with self.assertRaises(Refused) as e:
            c.read_marks()
        self.assertIn('M1-S04-T1: the mark "good." is not good or bad', str(e.exception))
        self.assertIn("M1-S05-T1: no mark", str(e.exception))

    def test_an_incomplete_marking_file_is_refused(self):
        self.steps.marks["M1-S02-T1"] = {"mark": "bad", "reason": ""}
        self.steps.marks["M1-S03-T1"] = None
        c = self.control()
        self.run_to_marks(c)
        with self.assertRaises(Refused) as e:
            c.read_marks()
        self.assertIn("M1-S02-T1: a bad mark has no reason", str(e.exception))
        self.assertIn("M1-S03-T1: the row is missing", str(e.exception))


class TestCaseF(Base):
    """(f) A call fails 3 times."""

    def test_writer_call_fails_3_times_then_a_new_start(self):
        self.steps.write_script["M1-S10"] = ["call_fails"] * 3
        c = self.control()
        report = c.run()
        self.assertEqual(self.status(c, "M1-S10")["status"], "to_write")
        self.assertEqual(report["state"], "waits_for_owner")
        self.assertEqual(report["errors"][0]["target"], "M1-S10")
        self.assertEqual(report["errors"][0]["step"], "write")
        self.assertTrue(os.path.exists(os.path.join(self.folder, "errors", "E001.json")))
        calls = len(self.steps.requests)
        self.assertEqual(calls, 62)  # 59 slots, and 3 runs of the call that failed

        # A new start continues from the records.
        report = self.control().run()
        self.assertEqual(len(self.steps.requests), calls + 1)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["state"], "ready_to_mark")

    def test_model_check_fails_3_times(self):
        self.steps.model_script["M1-S10"] = ["call_fails"] * 3
        c = self.control()
        report = c.run()
        self.assertEqual(self.status(c, "M1-S10")["status"], "to_check")
        self.assertEqual(report["errors"][0]["target"], "M1-S10-T1")
        self.assertEqual(self.control().run()["state"], "ready_to_mark")

    def test_a_call_that_fails_less_than_3_times_is_not_an_error(self):
        self.steps.write_script["M1-S10"] = ["call_fails", "call_fails", "ok"]
        report = self.control().run()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["state"], "ready_to_mark")

    def test_step_6_call_fails_3_times(self):
        self.steps.scenario_script[5] = ["call_fails"] * 3
        c = self.control()
        report = c.run()
        self.assertEqual(report["state"], "waits_for_owner")
        self.assertEqual(report["errors"][0]["target"], "scenario-5")
        self.assertNotIn(1, self.steps.marking_files)
        self.assertEqual(self.control().run()["state"], "ready_to_mark")


class TestCaseJ(Base):
    """(j) Step 8 for a later mock."""
    mock = 2

    def test_sample_of_20(self):
        c = self.control()
        self.run_to_marks(c)
        ids = self.steps.marking_files[1]
        self.assertEqual(len(ids), 20)
        slots = {s["slot_id"]: s for s in c.slots()}
        for scenario in (1, 3, 5, 6):
            self.assertEqual(sum(1 for i in ids if slots[i[:-3]]["scenario"] == scenario), 5)
        domains = {slots[i[:-3]]["task_statement"][0] for i in ids}
        self.assertEqual(domains, {"1", "2", "3", "4", "5"})

    def test_no_accept_before_the_marks(self):
        c = self.control()
        self.run_to_marks(c)
        with self.assertRaises(Refused) as e:
            c.accept()
        self.assertIn("a marking file waits for marks", str(e.exception))
        c.read_marks()
        self.assertEqual(c.accept()["state"], "built")

    def test_no_accept_with_a_finding_that_has_no_decision(self):
        self.steps.scenario_script[1] = [self.finding("D1", ["M2-S03-T1", "M2-S04-T1"],
                                                      result="cannot_decide")]
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        with self.assertRaises(Refused) as e:
            c.accept()
        self.assertIn("M2-SC1-R1-F1: the finding of step 6 has no decision", str(e.exception))

    def test_2_bad_marks_stop_a_later_mock(self):
        c = self.control()
        self.run_to_marks(c)
        for qid in self.steps.marking_files[1][:2]:
            self.steps.marks[qid] = {"mark": "bad", "reason": "Bad."}
        self.assertEqual(c.read_marks()["state"], "stopped")
        with self.assertRaises(Refused):
            c.accept()

    def test_a_record_that_changed_after_its_check_stops_the_build(self):
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        path = os.path.join(self.folder, "questions", "M2-S30-T1.json")
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        record["question"] = "A changed question?"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f)
        with self.assertRaises(Refused) as e:
            c.accept()
        self.assertIn("M2-S30-T1: no valid pass of step 3", str(e.exception))
        self.assertEqual(self.steps.builds, [])

    def test_a_question_from_a_rewrite_gets_a_mark_also_outside_the_sample(self):
        c = self.control()
        # The sample depends only on the plan and the seed, so a second control finds it.
        probe = Control(tempfile.mkdtemp(), 2, 42, FakeSteps(), GUIDE_POINTS)
        probe.run()
        sample = probe.sample()
        shutil.rmtree(probe.folder)
        group = ["M2-S%02d" % n for n in range(1, 16)]
        outside = [s for s in group if s not in sample][:2]
        ids = [s + "-T1" for s in outside]
        self.steps.scenario_script[1] = [self.finding("D1", ids)]
        self.run_to_marks(c)
        self.assertNotIn(ids[1], self.steps.marking_files[1])
        c.read_marks()
        c.decide("rewrite", "M2-SC1-R1-F1", "Write a new scene.", question_id=ids[1])
        c.run()
        self.assertEqual(self.steps.marking_files[2], [outside[1] + "-T2"])


class TestRuleC3OverTheMock(Base):
    """Decision 0052: rule C3 compares the whole mock, so its finding can name a
    question of another scenario. Another rule cannot."""

    def test_step6_gets_the_questions_of_the_other_scenarios(self):
        c = self.control()
        self.run_to_marks(c)
        self.assertEqual(len(self.steps.scenario_others), 45)
        self.assertEqual(len(self.steps.scenario_own), 15)
        self.assertFalse(set(self.steps.scenario_others) & set(self.steps.scenario_own))

    def test_a_c3_finding_can_name_a_question_of_another_scenario(self):
        self.steps.scenario_script[1] = [self.finding("C3", ["M1-S03-T1", "M1-S20-T1"])]
        c = self.control()
        self.run_to_marks(c)
        report = c.read_marks()
        self.assertEqual([f["question_ids"] for f in report["step6_findings"]], [["M1-S03-T1", "M1-S20-T1"]])

    def test_another_rule_cannot_name_a_question_of_another_scenario(self):
        self.steps.scenario_script[1] = [self.finding("D1", ["M1-S03-T1", "M1-S20-T1"])] * 3
        c = self.control()
        c.run()
        errors = [json.load(open(os.path.join(c.folder, "errors", f))) for f in sorted(os.listdir(os.path.join(c.folder, "errors")))]
        self.assertIn("unknown question: M1-S20-T1", errors[0]["cause"])


class TestNewPointOfTheOwner(Base):
    """An open slot can get a point that the owner gives (decisions 0039 and 0045)."""

    def test_the_owner_gives_the_point_of_an_open_slot(self):
        self.steps.model_script["M1-S05"] = ["fail", "fail", "fail"]
        c = self.control()
        c.run()
        slot = c._slot("M1-S05")
        free = [p for p in GUIDE_POINTS[slot["task_statement"]]
                if p != slot["point"] and all(c.point_of(s) != p for s in c.slots())]
        d = c.decide("new_point", "M1-S05", "A new point.", new_point=free[0])
        self.assertEqual(d["point"], free[0])
        with self.assertRaises(Refused):
            c.decide("more_tries", "M1-S05", "x", new_point=free[0])


class TestReviewFindings(Base):
    """The cases of the independent review of 7 October 2026."""

    def test_the_report_hides_the_findings_while_marks_wait(self):
        self.steps.scenario_script[3] = [self.finding("D2", ["M1-S20-T1", "M1-S21-T1"])]
        c = self.control()
        report = self.run_to_marks(c)
        self.assertEqual(report["step6_findings"], [])
        report = c.read_marks()
        self.assertEqual([f["id"] for f in report["step6_findings"]], ["M1-SC3-R1-F1"])

    def test_a_rewrite_does_not_hide_the_other_findings(self):
        two = [{"rule": "D1", "result": "fail", "findings": [
                   {"question_ids": ["M1-S20-T1", "M1-S21-T1"], "detail": "Same scene."},
                   {"question_ids": ["M1-S22-T1", "M1-S23-T1"], "detail": "Same scene."}]}]
        self.steps.scenario_script[3] = [two]
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.decide("rewrite", "M1-SC3-R1-F1", "New scene.", question_id="M1-S21-T1")
        self.assertEqual([f["id"] for f in c.open_findings()], ["M1-SC3-R1-F2"])
        c.decide("ignore", "M1-SC3-R1-F2", "Different scenes.")
        c.run()
        c.read_marks()
        self.assertEqual(c.accept()["state"], "built")

    def test_a_second_rewrite_of_the_same_question_is_refused(self):
        two = [{"rule": "D1", "result": "fail", "findings": [
                   {"question_ids": ["M1-S20-T1", "M1-S21-T1"], "detail": "Same scene."},
                   {"question_ids": ["M1-S21-T1", "M1-S22-T1"], "detail": "Same scene."}]}]
        self.steps.scenario_script[3] = [two]
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.decide("rewrite", "M1-SC3-R1-F1", "New scene.", question_id="M1-S21-T1")
        with self.assertRaises(Refused) as e:
            c.decide("rewrite", "M1-SC3-R1-F2", "New scene.", question_id="M1-S21-T1")
        self.assertIn("not the current try", str(e.exception))

    def test_step_6_that_names_an_unknown_or_old_question_runs_again(self):
        self.steps.model_script["M1-S16"] = ["fail", "pass"]
        self.steps.scenario_script[3] = [self.finding("D1", ["M1-S99-T1", "M1-S17-T1"]),
                                         self.finding("D1", ["M1-S16-T1", "M1-S17-T1"])]
        c = self.control()
        report = self.run_to_marks(c)
        # Two answers were not valid. The third call gave a valid answer.
        self.assertEqual(self.steps.scenario_calls.count(3), 3)
        self.assertEqual(report["errors"], [])

    def test_step_6_that_names_unknown_questions_3_times_is_an_error(self):
        bad = self.finding("D1", ["M1-S99-T1", "M1-S17-T1"])
        self.steps.scenario_script[3] = [bad, bad, bad]
        c = self.control()
        report = c.run()
        self.assertEqual(report["errors"][0]["target"], "scenario-3")
        self.assertIn("M1-S99-T1", report["errors"][0]["cause"])

    def test_a_fail_of_step_6_with_no_finding_runs_again(self):
        empty = [{"rule": "D1", "result": "fail", "findings": []}]
        self.steps.scenario_script[3] = [empty, empty, empty]
        report = self.control().run()
        self.assertEqual(report["errors"][0]["target"], "scenario-3")

    def test_findings_are_hidden_while_a_slot_is_in_work(self):
        self.steps.marks["M1-S22-T1"] = {"mark": "bad", "reason": "Bad."}
        self.steps.scenario_script[3] = [self.finding("D2", ["M1-S20-T1", "M1-S21-T1"])]
        c = self.control()
        self.run_to_marks(c)
        report = c.read_marks()
        self.assertEqual(report["step6_findings"], [])
        self.assertEqual(report["waiting_for"], ["start the program"])
        with self.assertRaises(Refused) as e:
            c.decide("ignore", "M1-SC3-R1-F1", "")
        self.assertIn("Start the program", str(e.exception))

    def test_no_marking_file_after_step_6_fails_gives_the_correct_refusal(self):
        self.steps.scenario_script[3] = [self.finding("D2", ["M1-S20-T1", "M1-S21-T1"])]
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.decide("rewrite", "M1-SC3-R1-F1", "New scene.", question_id="M1-S21-T1")
        self.steps.scenario_script[3] = ["call_fails"] * 3
        c.run()
        self.assertEqual(c.steps.marking_files.get(2), None)
        with self.assertRaises(Refused) as e:
            c.decide("ignore", "M1-SC3-R1-F1", "")
        self.assertIn("Step 6 must check the new questions first", str(e.exception))

    def test_the_report_of_a_stopped_mock_has_no_errors(self):
        # In the same run, slot 7 becomes open and a call for slot 10 fails 3 times.
        self.steps.write_script["M1-S07"] = ["cannot_write"]
        self.steps.write_script["M1-S10"] = ["call_fails"] * 3
        c = self.control()
        self.assertEqual(len(c.run()["errors"]), 1)
        c.decide("new_plan", "M1", "Stop.")
        self.assertEqual(c.report()["errors"], [])

    def test_the_rounds_are_in_the_sequence_of_their_numbers(self):
        c = self.control()
        c.run()
        for n in (10, 2):
            c._write_new({"round": n, "question_ids": [], "fingerprints": {}, "date": ""},
                         "marking-rounds", "round-%d.json" % n)
        self.assertEqual([r["round"] for r in c.marking_rounds()], [1, 2, 10])

    def test_a_decision_after_the_build_is_refused(self):
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.accept()
        with self.assertRaises(Refused) as e:
            c.decide("more_tries", "M1-S05", "Too late.")
        self.assertIn("The mock is built", str(e.exception))

    def test_new_plan_without_an_open_slot_is_refused(self):
        c = self.control()
        c.run()
        with self.assertRaises(Refused):
            c.decide("new_plan", "M1", "No reason.")

    def test_a_build_that_fails_saves_no_accept(self):
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()

        def broken(plan, questions):
            raise RuntimeError("the build failed")
        self.steps.build = broken
        with self.assertRaises(RuntimeError):
            c.accept()
        self.assertEqual([d for d in c.decisions() if d["action"] == "accept"], [])

    def test_after_a_bad_mark_the_owner_is_told_to_start_the_program(self):
        self.steps.marks["M1-S20-T1"] = {"mark": "bad", "reason": "C is also correct."}
        c = self.control()
        self.run_to_marks(c)
        self.assertEqual(c.read_marks()["waiting_for"], ["start the program"])


class TestItem8Rows(Base):
    """Each row of the table of item 8 (decision 0039)."""

    def open_after_three_tries(self):
        self.steps.model_script["M1-S05"] = ["fail", "fail", "fail"]
        c = self.control()
        c.run()
        self.assertEqual(self.status(c, "M1-S05")["open_reasons"], ["three_tries"])
        return c

    def test_more_tries_after_three_tries_is_step_5_with_the_last_try(self):
        c = self.open_after_three_tries()
        c.decide("more_tries", "M1-S05", "Try again.")
        c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"]), (5, "M1-S05-T3"))
        self.assertEqual(r["findings"][0]["rule"], "B1")

    def test_new_point_after_three_tries_is_step_2(self):
        c = self.open_after_three_tries()
        d = c.decide("new_point", "M1-S05", "A different point.")
        c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"], r["point"]), (2, None, d["point"]))


class TestLimits(Base):
    def test_cannot_decide_twice_in_2_tries(self):
        self.steps.model_script["M1-S05"] = ["cannot_decide", "cannot_decide"]
        c = self.control()
        c.run()
        s = self.status(c, "M1-S05")
        self.assertEqual((s["status"], s["tries"], s["open_reasons"]),
                         ("open", 2, ["cannot_decide_twice"]))

    def test_the_count_of_cannot_decide_starts_at_zero_after_a_send_back(self):
        # One "cannot decide" before the bad mark, and one after it: the slot stays in the loop.
        self.steps.model_script["M1-S05"] = ["cannot_decide", "pass", "cannot_decide", "pass"]
        self.steps.marks["M1-S05-T2"] = {"mark": "bad", "reason": "Bad."}
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.run()
        s = self.status(c, "M1-S05")
        self.assertEqual((s["status"], s["tries"]), ("passed", 4))

    def test_a_slot_sent_back_twice_and_a_bad_mark_in_round_2(self):
        self.steps.marks["M1-S05-T1"] = {"mark": "bad", "reason": "First."}
        self.steps.marks["M1-S05-T2"] = {"mark": "bad", "reason": "Second."}
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        c.run()
        self.assertEqual(self.steps.marking_files[2], ["M1-S05-T2"])
        report = c.read_marks()
        self.assertNotEqual(report["state"], "stopped")
        c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"]), (5, "M1-S05-T2"))
        self.assertEqual(r["findings"][0]["detail"], "Second.")
        self.assertEqual(self.steps.marking_files[3], ["M1-S05-T3"])
        c.read_marks()
        self.assertEqual(c.accept()["state"], "built")


class TestLaterMockSample(Base):
    mock = 2

    def outside_slot(self):
        probe = Control(tempfile.mkdtemp(), 2, 42, FakeSteps(), GUIDE_POINTS)
        probe.run()
        outside = next(s["slot_id"] for s in probe.slots() if s["slot_id"] not in probe.sample())
        shutil.rmtree(probe.folder)
        return outside

    def test_more_tries_outside_the_sample_does_not_add_a_mark(self):
        self.check_action("more_tries")

    def test_new_point_outside_the_sample_does_not_add_a_mark(self):
        self.check_action("new_point")

    def check_action(self, action):
        outside = self.outside_slot()
        self.steps.write_script[outside] = ["cannot_write"]
        c = self.control()
        c.run()
        c.decide(action, outside, "Try again.")
        c.run()
        self.assertEqual(len(self.steps.marking_files[1]), 20)


class TestIncompleteQuestion(Base):
    def test_an_option_with_no_reason_is_saved_as_a_failure_of_step_3(self):
        real_write = self.steps.write

        def write(request):
            answer = real_write(request)
            if request["slot"]["slot_id"] == "M1-S05" and request["step"] == 2:
                answer["options"][1].pop("reason")
                answer["options"][2] = "an option that is not a record"
            return answer
        self.steps.write = write
        self.steps.code_script["M1-S05"] = ["fail"]
        c = self.control()
        c.run()
        v = c.verdict("M1-S05-T1", 3)
        self.assertEqual(v["verdict"], "fail")
        self.assertEqual(len(v["fingerprint"]), 64)
        self.assertEqual(self.status(c, "M1-S05")["status"], "passed")


class TestRewriteOfDecision0045(Base):
    """A rewrite with no finding of step 6, and a rewrite with a new point."""

    def marked(self):
        c = self.control()
        self.run_to_marks(c)
        c.read_marks()
        return c

    def test_a_rewrite_with_no_finding_is_step_5_with_the_reason(self):
        c = self.marked()
        d = c.decide("rewrite", "M1-S05-T1", "The two correct options are one action.")
        self.assertEqual((d["target"], d["question_id"], d["after_try"]), ("M1-S05-T1", "M1-S05-T1", 1))
        report = c.run()
        r = self.steps.requests[-1]
        self.assertEqual((r["step"], r["shown_try"]), (5, "M1-S05-T1"))
        self.assertEqual(r["findings"][-1]["detail"], "The two correct options are one action.")
        self.assertEqual(self.steps.marking_files[2], ["M1-S05-T2"])
        self.assertEqual(report["state"], "ready_to_mark")
        self.assertEqual(c.bad_marks_first_round(), [])

    def test_a_rewrite_with_a_new_point_is_step_2_on_that_point(self):
        c = self.marked()
        d = c.decide("rewrite", "M1-S11-T1", "Repeat of S07.", new_point="2.4-K3", other_questions=["M1-S10-T1"])
        self.assertEqual(d["point"], "2.4-K3")
        self.assertEqual(c.point_of(c._slot("M1-S11")), "2.4-K3")
        c.run()
        r = [x for x in self.steps.requests if x["slot"]["slot_id"] == "M1-S11"][-1]
        self.assertEqual((r["step"], r["point"], r["shown_try"]), (2, "2.4-K3", None))
        self.assertEqual([q["question_id"] for q in r["other_questions"]], ["M1-S10-T1"])
        self.assertEqual(c._question("M1-S11-T2")["point"], "2.4-K3")

    def test_the_three_checks_of_a_new_point(self):
        c = self.marked()
        with self.assertRaises(Refused) as e:
            c.decide("rewrite", "M1-S11-T1", "x", new_point="1.1-K3")
        self.assertIn("not in the task statement", str(e.exception))
        with self.assertRaises(Refused) as e:
            c.decide("rewrite", "M1-S11-T1", "x", new_point="2.4-K2")
        self.assertIn("used by the slot M1-S41", str(e.exception))
        with self.assertRaises(Refused) as e:
            c.decide("rewrite", "M1-S11-T1", "x", new_point="2.4-K1")
        self.assertIn("had the point", str(e.exception))

    def test_a_rewrite_with_a_new_point_through_a_finding(self):
        self.steps.scenario_script[1] = [self.finding("D1", ["M1-S03-T1", "M1-S04-T1"])]
        c = self.marked()
        c.decide("rewrite", "M1-SC1-R1-F1", "Same scene.", question_id="M1-S04-T1", new_point="1.4-K3")
        c.run()
        r = [x for x in self.steps.requests if x["slot"]["slot_id"] == "M1-S04"][-1]
        self.assertEqual((r["step"], r["point"]), (2, "1.4-K3"))
        self.assertEqual([q["question_id"] for q in r["other_questions"]], ["M1-S03-T1"])

    def test_a_rewrite_before_the_marks_is_refused(self):
        c = self.control()
        self.run_to_marks(c)
        with self.assertRaises(Refused):
            c.decide("rewrite", "M1-S05-T1", "x")


class TestNewPlan(Base):
    def test_new_plan_stops_the_mock(self):
        self.steps.write_script["M1-S07"] = ["cannot_write"]
        c = self.control()
        c.run()
        c.decide("new_plan", "M1", "The plan does not work.")
        report = c.run()
        self.assertEqual(report["state"], "stopped")


if __name__ == "__main__":
    unittest.main()
