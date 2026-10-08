"""Tests of the point groups (decision 0047). No test makes a model call.

Run from the folder ccar-f-mock-generator:
    python3 -m unittest discover tests
"""
import copy
import itertools
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import point_groups  # noqa: E402
from point_groups import GroupError, check_groups, conflicts, group_of  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(point_groups.RECORDS, encoding="utf-8") as f:
    RECORDS = json.load(f)
GROUPS = point_groups.load()
with open(os.path.join(ROOT, "runs", "mock-01", "plan.json"), encoding="utf-8") as f:
    PLAN_1 = json.load(f)
POINT = {s["slot_id"][3:]: s["point"] for s in PLAN_1["slots"]}

# The known repeats of mock 1 (decision 0047, item 5). Each line is one idea and
# the slots that a source found on it, on the points of the plan.
# Sources: decision 0045 (the bad marks), decision 0046 (the known limits), and
# docs/reviews/M1-round1-second-review-notes.md ("Groups of questions on one idea").
KNOWN = [
    ("S13", "S14", "S18", "S30"),   # notes: a prompt rule fails, code must enforce it
    ("S08", "S21", "S25", "S28"),   # notes, and 0045 for S21 and S28
    ("S31", "S48", "S60"),          # notes, and 0045 for S48 and S60
    ("S47", "S57"),                 # notes
    ("S10", "S24"),                 # notes and 0045
    ("S07", "S09"),                 # notes and 0045
    ("S53", "S54"),                 # notes and 0046
    ("S20", "S22"),                 # notes
    ("S34", "S38"),                 # notes
    ("S33", "S40"),                 # notes
    ("S33", "S43"),                 # 0046
]
# 0046: M1-S38-T2 and M1-S45-T2. S38-T2 has the point 3.4-K4 of decision D010.
KNOWN_ON_REWRITE_POINTS = [("3.4-K4", "5.4-S1")]

# The pairs that the groups do not catch, with the reason.
NOT_CAUGHT = {
    # 0046: "The points 4.4-K1 and 4.4-K4 are not twins by their texts."
    ("S53", "S54"),
    # The notes: "two different correct answers: a rules file with a path, and a
    # CLAUDE.md in the directory". 3.1-K1 is the CLAUDE.md hierarchy.
    ("S33", "S40"),
}


def known_pairs():
    pairs = []
    for line in KNOWN:
        for a, b in itertools.combinations(line, 2):
            if (a, b) not in pairs:
                pairs.append((a, b))
    return pairs


class TestFile(unittest.TestCase):
    def test_the_file_is_correct(self):
        check_groups(GROUPS, RECORDS)

    def test_each_of_the_240_points_is_in_exactly_one_group(self):
        points = [p for g in GROUPS["groups"] for p in g["points"]]
        self.assertEqual(len(points), 240)
        self.assertEqual(len(set(points)), 240)

    def test_a_point_in_two_groups_is_an_error(self):
        bad = copy.deepcopy(GROUPS)
        bad["groups"][1]["points"].append(bad["groups"][0]["points"][0])
        with self.assertRaisesRegex(GroupError, "is in group G001 and in group G002"):
            check_groups(bad, RECORDS)

    def test_a_missing_point_is_an_error(self):
        bad = copy.deepcopy(GROUPS)
        lost = bad["groups"][0]["points"].pop()
        if not bad["groups"][0]["points"]:
            bad["groups"][0]["points"] = None
        with self.assertRaisesRegex(GroupError, "The point %s is in no group" % lost):
            check_groups(bad, RECORDS)

    def test_an_unknown_point_is_an_error(self):
        bad = copy.deepcopy(GROUPS)
        bad["groups"][0]["points"].append("9.9-K9")
        with self.assertRaisesRegex(GroupError, "9.9-K9"):
            check_groups(bad, RECORDS)

    def test_a_wrong_guide_version_is_an_error(self):
        bad = copy.deepcopy(GROUPS)
        bad["guide_version"] = "0.0"
        with self.assertRaisesRegex(GroupError, "guide version"):
            check_groups(bad, RECORDS)

    def test_ids_in_sequence(self):
        bad = copy.deepcopy(GROUPS)
        bad["groups"][2]["id"] = "G099"
        with self.assertRaisesRegex(GroupError, "Group number 3 has the id"):
            check_groups(bad, RECORDS)


class TestMock1(unittest.TestCase):
    """Decision 0047, item 5: the test against mock 1."""

    def test_each_known_pair_is_in_one_group_except_the_named_ones(self):
        of = group_of(GROUPS)
        for a, b in known_pairs():
            same = of[POINT[a]]["id"] == of[POINT[b]]["id"]
            self.assertEqual(same, (a, b) not in NOT_CAUGHT, (a, b, POINT[a], POINT[b]))
        for a, b in KNOWN_ON_REWRITE_POINTS:
            self.assertEqual(of[a]["id"], of[b]["id"])

    def test_the_rule_rejects_the_plan_of_mock_1_and_names_the_pairs(self):
        found = conflicts([(s["slot_id"][3:], s["point"]) for s in PLAN_1["slots"]], GROUPS)
        named = set()
        for _, items in found:
            for (a, _), (b, _) in itertools.combinations(items, 2):
                named.add((a, b))
        self.assertTrue(found)
        for pair in known_pairs():
            if pair not in NOT_CAUGHT:
                self.assertIn(pair, named)


if __name__ == "__main__":
    unittest.main()
