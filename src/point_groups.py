"""The point groups of decision 0047.

The file data/point-groups.json puts each of the 240 points of the guide into
exactly one group. Two points in one group describe one idea. No two slots of
one mock get points of the same group.

Run from the folder ccar-f-mock-generator:
    python3 src/point_groups.py check
        Checks the file and prints the groups with two or more points.
    python3 src/point_groups.py plan runs/mock-01/plan.json
        Prints each group that has two or more slots of the plan.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS = os.path.join(ROOT, "reference", "guide-records.json")
GROUPS = os.path.join(ROOT, "data", "point-groups.json")


class GroupError(Exception):
    """The groups file is not correct. The message names each problem."""


def load(path=GROUPS):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_groups(groups, records):
    """Raise GroupError with each problem. Return nothing if the file is correct."""
    problems = []
    if not isinstance(groups, dict) or not isinstance(groups.get("groups"), list):
        raise GroupError("The groups file has no list 'groups'.")
    if groups.get("guide_version") != records["guide"]["version"]:
        problems.append("The guide version is %r, not %r."
                        % (groups.get("guide_version"), records["guide"]["version"]))
    points = [p["id"] for ts in records["task_statements"] for p in ts["points"]]
    known = set(points)
    seen = {}
    for i, g in enumerate(groups["groups"], 1):
        gid = g.get("id")
        if gid != "G%03d" % i:
            problems.append("Group number %d has the id %r, not G%03d." % (i, gid, i))
        if not isinstance(g.get("idea"), str) or not g["idea"].strip():
            problems.append("Group %s has no idea." % gid)
        if not isinstance(g.get("points"), list) or not g["points"]:
            problems.append("Group %s has no points." % gid)
            continue
        for p in g["points"]:
            if p not in known:
                problems.append("Group %s has the point %r, which is not in the guide." % (gid, p))
            elif p in seen:
                problems.append("The point %s is in group %s and in group %s." % (p, seen[p], gid))
            else:
                seen[p] = gid
    for p in points:
        if p not in seen:
            problems.append("The point %s is in no group." % p)
    if problems:
        raise GroupError("\n".join(problems))


def group_of(groups):
    """A map from each point to its group."""
    return {p: g for g in groups["groups"] for p in g["points"]}


def conflicts(slots, groups):
    """Each group that has two or more of the slots. slots is a list of
    (slot ID, point ID). The result is a list of (group, [(slot, point), ...])."""
    of = group_of(groups)
    found = {}
    for slot, point in slots:
        found.setdefault(of[point]["id"], []).append((slot, point))
    by_id = {g["id"]: g for g in groups["groups"]}
    return [(by_id[gid], items) for gid, items in sorted(found.items()) if len(items) > 1]


def _sort_key(point):
    return [int(x) for x in re.findall(r"\d+", point)]


def table(groups):
    """The text for the confirmation of the owner (decision 0047, item 6)."""
    many = [g for g in groups["groups"] if len(g["points"]) > 1]
    lines = ["| Group | Idea | Points |", "|---|---|---|"]
    for g in many:
        lines.append("| %s | %s | %s |" % (g["id"], g["idea"], ", ".join(g["points"])))
    lines.append("")
    lines.append("%d groups have two or more points. %d groups have one point."
                 % (len(many), len(groups["groups"]) - len(many)))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check the point groups (decision 0047).")
    parser.add_argument("command", choices=["check", "plan"])
    parser.add_argument("plan", nargs="?")
    parser.add_argument("--groups", default=GROUPS)
    parser.add_argument("--records", default=RECORDS)
    args = parser.parse_args(argv)
    with open(args.records, encoding="utf-8") as f:
        records = json.load(f)
    groups = load(args.groups)
    try:
        check_groups(groups, records)
    except GroupError as e:
        print("The groups file is not correct:\n" + str(e))
        return 1
    if args.command == "check":
        print("The groups file is correct: %d groups, %d points.\n"
              % (len(groups["groups"]), sum(len(g["points"]) for g in groups["groups"])))
        print(table(groups))
        return 0
    if not args.plan:
        parser.error("plan needs the path of a plan file")
    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    found = conflicts([(s["slot_id"], s["point"]) for s in plan["slots"]], groups)
    if not found:
        print("No two slots of the plan are in one group.")
        return 0
    print("%d groups have two or more slots of the plan:" % len(found))
    for g, items in found:
        print("%s (%s): %s" % (g["id"], g["idea"], ", ".join("%s %s" % i for i in items)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
