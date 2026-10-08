"""Tests of step 1, the plan of a mock (decision 0027). No test makes a model call.

Run from the folder ccar-f-mock-generator:
    python3 -m unittest discover tests
"""
import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import step1_plan  # noqa: E402
from step1_plan import PlanError, make_plan, scenario_sets, tables, domain_counts, DOMAIN_COUNTS  # noqa: E402
import point_groups  # noqa: E402

with open(step1_plan.RECORDS, encoding="utf-8") as f:
    RECORDS = json.load(f)
TS = {t["id"]: t for t in RECORDS["task_statements"]}
PRIMARY = {s["id"]: s["primary_domains"] for s in RECORDS["scenarios"]}
SEEDS = range(40)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = point_groups.load()
OF = point_groups.group_of(GROUPS)
TS_GROUPS = {t: {OF[p["id"]]["id"] for p in TS[t]["points"]} for t in TS}


def domain(slot):
    return TS[slot["task_statement"]]["domain"]


class TestPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plans = [make_plan(RECORDS, 1, seed, "2026-10-07") for seed in SEEDS]

    def test_11_sets_and_the_4_sets_that_do_not_fit(self):
        sets = scenario_sets(RECORDS, domain_counts(RECORDS))
        self.assertEqual(len(sets), 11)
        for bad in [(1, 2, 3, 4), (1, 2, 5, 6), (2, 3, 5, 6), (2, 4, 5, 6)]:
            self.assertNotIn(bad, sets)

    def test_the_counts(self):
        for plan in self.plans:
            slots = plan["slots"]
            self.assertEqual(len(slots), 60)
            self.assertEqual(Counter(domain(s) for s in slots), Counter({1: 16, 2: 11, 3: 12, 4: 12, 5: 9}))
            self.assertEqual(Counter(s["scenario"] for s in slots), Counter({s: 15 for s in plan["scenarios"]}))
            self.assertEqual(len(plan["scenarios"]), 4)
            self.assertIn(tuple(sorted(plan["scenarios"])), scenario_sets(RECORDS, domain_counts(RECORDS)))

    def test_each_task_statement_gets_its_share_up_to_its_groups(self):
        # Decision 0048: an equal share, but no more questions than groups, and at
        # most one extra question.
        for plan in self.plans:
            per_ts = Counter(s["task_statement"] for s in plan["slots"])
            self.assertEqual(set(per_ts), set(TS))
            for d in range(1, 6):
                names = [t for t in TS if TS[t]["domain"] == d]
                share = DOMAIN_COUNTS[d] // len(names)
                for t in names:
                    self.assertLessEqual(per_ts[t], min(share + 1, len(TS_GROUPS[t])))
                    self.assertGreaterEqual(per_ts[t], min(share, len(TS_GROUPS[t])))
            self.assertEqual(per_ts["3.3"], 1)

    def test_no_two_slots_in_one_group(self):
        for plan in self.plans:
            groups = [OF[s["point"]]["id"] for s in plan["slots"]]
            self.assertEqual(len(groups), len(set(groups)))

    def test_each_question_fits_a_primary_domain(self):
        for plan in self.plans:
            for s in plan["scenarios"]:
                got = {domain(x) for x in plan["slots"] if x["scenario"] == s}
                self.assertEqual(got, set(PRIMARY[s]))

    def test_the_table_agrees_with_the_slots_and_is_the_most_even(self):
        for plan in self.plans:
            for s in plan["scenarios"]:
                counted = Counter(domain(x) for x in plan["slots"] if x["scenario"] == s)
                self.assertEqual({str(d): n for d, n in counted.items()}, plan["table"][str(s)])
            found = tables(sorted(plan["scenarios"]), PRIMARY, domain_counts(RECORDS))
            least = min(sum(n * n for r in t.values() for n in r.values()) for t in found)
            mine = sum(n * n for r in plan["table"].values() for n in r.values())
            self.assertEqual(mine, least)

    def test_one_point_for_each_slot_and_no_point_two_times(self):
        for plan in self.plans:
            points = [s["point"] for s in plan["slots"]]
            self.assertEqual(len(points), len(set(points)))
            for s in plan["slots"]:
                self.assertIn(s["point"], [p["id"] for p in TS[s["task_statement"]]["points"]])

    def test_question_types(self):
        for plan in self.plans:
            for sc in plan["scenarios"]:
                group = [s for s in plan["slots"] if s["scenario"] == sc]
                self.assertEqual(sum(1 for s in group if s["type"] == "multiple_response"), 2)
            for s in plan["slots"]:
                expected = (5, 2) if s["type"] == "multiple_response" else (4, 1)
                self.assertEqual((s["options"], s["select"]), expected)

    def test_slot_numbers_follow_the_groups(self):
        for plan in self.plans:
            slots = plan["slots"]
            self.assertEqual([s["slot_id"] for s in slots], ["M1-S%02d" % n for n in range(1, 61)])
            for i, sc in enumerate(plan["scenarios"]):
                self.assertTrue(all(s["scenario"] == sc for s in slots[i * 15:(i + 1) * 15]))

    def test_the_slot_fields_of_decision_0029(self):
        for s in self.plans[0]["slots"]:
            self.assertEqual(set(s), {"slot_id", "scenario", "task_statement", "point", "type", "options", "select"})
        self.assertEqual(set(self.plans[0]), {"mock", "seed", "guide_version", "date", "earlier_mocks",
                                              "scenarios", "table", "slots"})

    def test_the_same_seed_gives_the_same_plan(self):
        step1_plan._TABLES.clear()
        self.assertEqual(make_plan(RECORDS, 1, 7, "2026-10-07"), self.plans[7])
        self.assertNotEqual(self.plans[1]["slots"], self.plans[2]["slots"])

    def test_the_seed_reaches_many_sets(self):
        reached = {tuple(sorted(p["scenarios"])) for p in self.plans}
        self.assertGreaterEqual(len(reached), 8)

    def test_the_seed_selects_between_equal_tables(self):
        # 7 of the 11 sets have two most even tables. Over many seeds, both appear.
        seen = {}
        for plan in self.plans:
            key = tuple(sorted(plan["scenarios"]))
            seen.setdefault(key, set()).add(json.dumps(plan["table"], sort_keys=True))
        self.assertTrue(any(len(v) == 2 for v in seen.values()))

    def test_no_function_of_random_other_than_random_is_used(self):
        with open(step1_plan.__file__, encoding="utf-8") as f:
            code = f.read()
        for name in ("rng.choice", "rng.shuffle", "rng.sample", "rng.randint", "rng.randrange",
                     "rng.uniform", "rng.getrandbits", "rng.choices"):
            self.assertNotIn(name, code)

    def test_a_later_mock_has_its_own_ids(self):
        plan = make_plan(RECORDS, 2, 5, "2026-10-07")
        self.assertEqual(plan["slots"][0]["slot_id"], "M2-S01")


class TestEarlierMocks(unittest.TestCase):
    """Decision 0050: the groups that earlier mocks used least come first."""

    def groups_of(self, plan):
        return {OF[s["point"]]["id"] for s in plan["slots"]}

    def test_a_plan_shares_fewer_ideas_with_the_earlier_mock(self):
        with_rule, without = 0, 0
        for seed in range(10):
            first = make_plan(RECORDS, 1, 100 + seed, "2026-10-08")
            earlier = {1: [s["point"] for s in first["slots"]]}
            with_rule += len(self.groups_of(first) & self.groups_of(make_plan(RECORDS, 2, seed, "2026-10-08", None, earlier)))
            without += len(self.groups_of(first) & self.groups_of(make_plan(RECORDS, 2, seed, "2026-10-08")))
        self.assertLess(with_rule, without - 50)

    def test_the_plan_names_the_earlier_mocks(self):
        plan = make_plan(RECORDS, 3, 1, "2026-10-08", None, {1: ["1.1-K1"], 2: ["1.1-K2"]})
        self.assertEqual(plan["earlier_mocks"], [1, 2])
        self.assertEqual(make_plan(RECORDS, 1, 1, "2026-10-08")["earlier_mocks"], [])

    def test_an_unknown_earlier_point_makes_no_plan(self):
        with self.assertRaises(PlanError) as e:
            make_plan(RECORDS, 2, 1, "2026-10-08", None, {1: ["9.9-K9"]})
        self.assertIn("9.9-K9", str(e.exception))

    def test_earlier_points_reads_the_built_mocks_before_this_one(self):
        folder = tempfile.mkdtemp()
        try:
            for n, point in ((1, "1.1-K1"), (3, "1.1-K2")):
                built = {"groups": [{"questions": [{"point": point}]}]}
                with open(os.path.join(folder, "mock-%02d.questions.json" % n), "w", encoding="utf-8") as f:
                    json.dump(built, f)
            self.assertEqual(step1_plan.earlier_points(folder, 3), {1: ["1.1-K1"]})
            self.assertEqual(step1_plan.earlier_points(folder, 4), {1: ["1.1-K1"], 3: ["1.1-K2"]})
            self.assertEqual(step1_plan.earlier_points(folder, 1), {})
        finally:
            shutil.rmtree(folder)

    def test_the_real_mock_1_is_read(self):
        found = step1_plan.earlier_points(os.path.join(ROOT, "mocks"), 2)
        self.assertEqual(list(found), [1])
        self.assertEqual(len(found[1]), 60)


class TestPlanFails(unittest.TestCase):
    def test_a_missing_record_makes_no_plan(self):
        broken = copy.deepcopy(RECORDS)
        del broken["scenarios"]
        with self.assertRaises(PlanError) as e:
            make_plan(broken, 1, 1, "2026-10-07")
        self.assertIn("scenarios", str(e.exception))

    def test_counts_that_do_not_add_up_make_no_plan(self):
        broken = copy.deepcopy(RECORDS)
        broken["domains"][0]["weight"] = 40
        with self.assertRaises(PlanError) as e:
            make_plan(broken, 1, 1, "2026-10-07")
        self.assertIn("domain counts", str(e.exception))

    def broken(self, change, words):
        records = copy.deepcopy(RECORDS)
        change(records)
        with self.assertRaises(PlanError) as e:
            make_plan(records, 1, 1, "2026-10-07")
        self.assertIn(words, str(e.exception))

    def test_bad_records_give_an_error_that_names_the_cause(self):
        self.broken(lambda r: r["task_statements"][0].pop("id"), "not like 1.2")
        self.broken(lambda r: r["scenarios"][0].pop("primary_domains"), "no primary domains")
        self.broken(lambda r: r["scenarios"][0]["primary_domains"].append(7), "unknown primary domain")
        self.broken(lambda r: r["domains"][0].update(weight="27"), "number weight")
        self.broken(lambda r: r["task_statements"][0].update(id="1.1a"), "not like 1.2")
        self.broken(lambda r: r["guide"].pop("version"), "version of the guide")
        self.broken(lambda r: r["task_statements"][0].update(domain=9), "unknown domain")
        self.broken(lambda r: r["task_statements"].pop(), "29 task statements")
        self.broken(lambda r: r["task_statements"][1]["points"][0].update(id="1.1-K1"), "two times")

    def test_each_task_statement_must_get_a_question(self):
        def crowd(r):
            for t in r["task_statements"][:4]:
                t["domain"] = 5
        self.broken(crowd, "more task statements than questions")

    def test_groups_that_allow_no_plan_make_no_plan(self):
        groups = copy.deepcopy(GROUPS)
        one = [p["id"] for t in ("1.4", "1.5", "1.6") for p in TS[t]["points"]]
        for g in groups["groups"]:
            g["points"] = [p for p in g["points"] if p not in one]
        groups["groups"] = [g for g in groups["groups"] if g["points"]]
        groups["groups"].append({"id": "", "idea": "test", "points": one})
        for i, g in enumerate(groups["groups"], 1):
            g["id"] = "G%03d" % i
        with self.assertRaises(PlanError) as e:
            make_plan(RECORDS, 1, 1, "2026-10-07", groups)
        self.assertIn("No plan is possible", str(e.exception))
        self.assertIn("Task statement 1.", str(e.exception))

    def test_possible_is_a_matching(self):
        ts_groups = {"a": frozenset({"G1", "G2"}), "b": frozenset({"G1"}), "c": frozenset({"G2", "G3"})}
        self.assertTrue(step1_plan._possible({"a": 1, "b": 1, "c": 1}, ts_groups, frozenset()))
        self.assertTrue(step1_plan._possible({"a": 1, "b": 1, "c": 1}, ts_groups, frozenset({"G4"})))
        self.assertFalse(step1_plan._possible({"a": 2, "b": 1}, ts_groups, frozenset()))
        self.assertFalse(step1_plan._possible({"b": 1}, ts_groups, frozenset({"G1"})))
        self.assertFalse(step1_plan._possible({"a": 1, "b": 1, "c": 2}, ts_groups, frozenset()))

    def test_extras_go_back_to_an_earlier_domain(self):
        # Domain 1 has one extra question for x or y. y takes the group that z of
        # domain 2 needs. The seed order puts y first, so code must go back.
        ts_groups = {"x": frozenset({"G1", "G2"}), "y": frozenset({"G3", "G4"}), "z": frozenset({"G4", "G5"})}
        need = {"x": 1, "y": 1, "z": 1}
        found = step1_plan._extras([(1, ["y", "x"], 1), (2, ["z"], 1)], need, ts_groups)
        self.assertEqual(found, {"x": 2, "y": 1, "z": 2})
        self.assertIsNone(step1_plan._extras([(1, ["y"], 1), (2, ["z"], 1)], need, ts_groups))

    def test_a_bad_groups_file_makes_no_plan(self):
        groups = copy.deepcopy(GROUPS)
        groups["groups"][0]["points"].append("9.9-K9")
        with self.assertRaises(PlanError) as e:
            make_plan(RECORDS, 1, 1, "2026-10-07", groups)
        self.assertIn("groups file is not correct", str(e.exception))

    def test_the_command_reports_a_bad_records_file(self):
        folder = tempfile.mkdtemp()
        try:
            bad = os.path.join(folder, "records.json")
            with open(bad, "w", encoding="utf-8") as f:
                f.write("{ not json")
            self.assertEqual(step1_plan.main(["--mock", "1", "--seed", "3", "--runs", folder, "--records", bad]), 1)
            self.assertFalse(os.path.exists(os.path.join(folder, "mock-01", "plan.json")))
        finally:
            shutil.rmtree(folder)

    def test_the_command_writes_no_plan_over_a_plan(self):
        folder = tempfile.mkdtemp()
        try:
            self.assertEqual(step1_plan.main(["--mock", "1", "--seed", "3", "--runs", folder]), 0)
            path = os.path.join(folder, "mock-01", "plan.json")
            with open(path, encoding="utf-8") as f:
                first = f.read()
            self.assertEqual(step1_plan.main(["--mock", "1", "--seed", "4", "--runs", folder]), 1)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), first)
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main()
