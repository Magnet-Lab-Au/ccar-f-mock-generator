"""Step 1 of the pipeline: the plan of a mock (decisions 0009, 0027 and 0037, item 14,
and the point groups of decisions 0047 and 0048).

Code makes a list of 60 slots. No model works in this step. The seed controls
each selection, so the same seed gives the same plan.

Run from the folder ccar-f-mock-generator:
    python3 src/step1_plan.py --mock 1 --seed 1234

It writes runs/mock-01/plan.json. It does not write over a plan that exists.
"""
import argparse
import copy
import datetime
import itertools
import json
import os
import random
import sys

import point_groups

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS = os.path.join(ROOT, "reference", "guide-records.json")
TWO_ANSWER_POINTS = os.path.join(ROOT, "data", "two-answer-points.json")   # decision 0054

QUESTIONS = 60
PER_SCENARIO = 15
SCENARIOS_IN_MOCK = 4
MULTIPLE_RESPONSE_PER_SCENARIO = 2   # a guess with no source (decision 0027)
DOMAIN_COUNTS = {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}   # decision 0027, item 1
# Decision 0053: the slots on which the longest option may be correct. The chance
# numbers: 1 in 4 of the 52 slots with 1 answer, 2 in 5 of the 8 slots with 2 answers.
LONGEST_MAY_BE_CORRECT = {1: 13, 2: 3}


class PlanError(Exception):
    """The step cannot make a plan. The message names the cause."""


# The Python documentation guarantees the same sequence of random() for the same
# seed in later versions of Python. It does not guarantee it for choice, shuffle
# and sample. So these three functions use only random().
def _shuffle(rng, items):
    for i in range(len(items) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        items[i], items[j] = items[j], items[i]


def _sample(rng, items, k):
    pool = list(items)
    _shuffle(rng, pool)
    return pool[:k]


def _choice(rng, items):
    return items[int(rng.random() * len(items))]


TASK_STATEMENTS = 30


def check_records(records):
    """Check the parts of the records file that step 1 reads. Raise PlanError
    with the cause for each problem."""
    if not isinstance(records, dict):
        raise PlanError("The records file is not a JSON object.")
    for key in ("domains", "scenarios", "task_statements"):
        if not records.get(key):
            raise PlanError("The records file has no %s." % key)
    if not isinstance(records.get("guide"), dict) or not records["guide"].get("version"):
        raise PlanError("The records file has no version of the guide.")
    domains = set()
    for d in records["domains"]:
        if not isinstance(d.get("id"), int) or not isinstance(d.get("weight"), (int, float)):
            raise PlanError("A domain has no number id or no number weight: %s" % d)
        domains.add(d["id"])
    for sc in records["scenarios"]:
        if not isinstance(sc.get("id"), int) or not sc.get("primary_domains"):
            raise PlanError("A scenario has no number id or no primary domains: %s" % sc.get("id"))
        unknown = [x for x in sc["primary_domains"] if x not in domains]
        if unknown:
            raise PlanError("Scenario %s has an unknown primary domain: %s" % (sc["id"], unknown))
    if len(records["task_statements"]) != TASK_STATEMENTS:
        raise PlanError("The records file has %d task statements, not %d."
                        % (len(records["task_statements"]), TASK_STATEMENTS))
    seen = set()
    for ts in records["task_statements"]:
        tid = ts.get("id")
        if not isinstance(tid, str) or not all(x.isdigit() for x in tid.split(".")):
            raise PlanError("A task statement has an id that is not like 1.2: %s" % tid)
        if ts.get("domain") not in domains:
            raise PlanError("Task statement %s has an unknown domain: %s" % (tid, ts.get("domain")))
        if not ts.get("points"):
            raise PlanError("Task statement %s has no points." % tid)
        for pt in ts["points"]:
            if not pt.get("id"):
                raise PlanError("Task statement %s has a point with no id." % tid)
            if pt["id"] in seen:
                raise PlanError("The point id %s is in the records two times." % pt["id"])
            seen.add(pt["id"])


def domain_counts(records):
    """The number of questions of each domain, from the weights of Section 4."""
    counts = {d["id"]: round(d["weight"] * QUESTIONS / 100) for d in records["domains"]}
    if sum(counts.values()) != QUESTIONS:
        raise PlanError("The domain counts add up to %d, not %d." % (sum(counts.values()), QUESTIONS))
    if counts != DOMAIN_COUNTS:
        raise PlanError("The domain counts %s are not those of decision 0027." % counts)
    return counts


def _rows(total, parts):
    """Each way to divide total into parts numbers, each at least 1."""
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for rest in _rows(total - first, parts - 1):
            yield (first,) + rest


_TABLES = {}


def tables(scenarios, primary, counts):
    """Each table that fits: 15 questions for each scenario, at least 1 for each
    primary domain, no question outside a primary domain, and the domain counts."""
    key = json.dumps([list(scenarios), {str(k): sorted(v) for k, v in primary.items()},
                      {str(k): v for k, v in counts.items()}], sort_keys=True)
    if key not in _TABLES:
        _TABLES[key] = _find_tables(scenarios, primary, counts)
    return [copy.deepcopy(t) for t in _TABLES[key]]


def _find_tables(scenarios, primary, counts):
    found = []

    def fill(index, left, table):
        if index == len(scenarios):
            if all(v == 0 for v in left.values()):
                found.append(dict(table))
            return
        s = scenarios[index]
        domains = sorted(primary[s])
        for row in _rows(PER_SCENARIO, len(domains)):
            if all(n <= left[d] for d, n in zip(domains, row)):
                new_left = dict(left)
                for d, n in zip(domains, row):
                    new_left[d] -= n
                table[s] = dict(zip(domains, row))
                fill(index + 1, new_left, table)
                del table[s]

    fill(0, dict(counts), {})
    return found


def _squares(table):
    return sum(n * n for row in table.values() for n in row.values())


def scenario_sets(records, counts):
    """The sets of 4 scenarios that have a table (decision 0027, item 2)."""
    primary = {s["id"]: s["primary_domains"] for s in records["scenarios"]}
    return [c for c in itertools.combinations(sorted(primary), SCENARIOS_IN_MOCK)
            if tables(c, primary, counts)]


def _possible(need, ts_groups, used):
    """True if each task statement can still get need[ts] points, each from a
    different group that is not in used (decision 0048). A matching of task
    statements to groups: each group serves at most one question."""
    owner = {}

    def place(ts, seen):
        for g in sorted(ts_groups[ts] - used):
            if g in seen:
                continue
            seen.add(g)
            if g not in owner or place(owner[g], seen):
                owner[g] = ts
                return True
        return False

    for ts in sorted(need):
        for _ in range(need[ts]):
            if not place(ts, set()):
                return False
    return True


def _extras(orders, need, ts_groups):
    """Give the extra questions of each domain (decision 0048, item 2). orders is a
    list of (domain, task statements in the order of the seed, number of extra
    questions). Return the first counts in the order of the seed that keep a full
    plan possible, or None if no such counts exist. A task statement gets at most
    one extra question."""
    if not orders:
        return need
    (d, order, left), rest = orders[0], orders[1:]
    if left > len(order):
        return None
    for chosen in itertools.combinations(order, left):
        more = dict(need)
        for ts in chosen:
            more[ts] += 1
        if _possible(more, ts_groups, frozenset()):
            found = _extras(rest, more, ts_groups)
            if found is not None:
                return found
    return None


def earlier_points(mocks_folder, mock):
    """The points of each built mock with a lower number (decision 0050): a map
    from the mock number to the list of its points. A mock is built when its file
    mock-NN.questions.json exists."""
    found = {}
    for n in range(1, mock):
        path = os.path.join(mocks_folder, "mock-%02d.questions.json" % n)
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    built = json.load(f)
                found[n] = [q["point"] for g in built["groups"] for q in g["questions"]]
            except (OSError, ValueError, KeyError, TypeError) as e:
                raise PlanError("The built mock file %s cannot be read: %s" % (path, e))
    return found


def load_two_answer_points(records, path=TWO_ANSWER_POINTS):
    """The points that can carry a question with 2 answers (decision 0054)."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise PlanError("The file of the two-answer points cannot be read: %s" % e)
    known = {p["id"] for ts in records["task_statements"] for p in ts["points"]}
    if not isinstance(data, dict) or data.get("guide_version") != records["guide"]["version"]:
        raise PlanError("The file of the two-answer points has another guide version.")
    points = data.get("points")
    if not isinstance(points, list) or not points or len(set(points)) != len(points) or not set(points) <= known:
        raise PlanError("The file of the two-answer points has no list of known points, each one time.")
    return set(points)


def make_plan(records, mock, seed, date, groups=None, earlier=None, two_answer=None):
    """Return the plan of one mock. Raise PlanError, and make no plan, if a record
    is missing, a count does not add up, or the groups allow no plan. groups is the
    content of data/point-groups.json. None reads that file. earlier is the result
    of earlier_points: the points of the built mocks before this one."""
    check_records(records)
    if groups is None:
        groups = point_groups.load()
    try:
        point_groups.check_groups(groups, records)
    except point_groups.GroupError as e:
        raise PlanError("The groups file is not correct: %s" % e)
    counts = domain_counts(records)
    primary = {s["id"]: s["primary_domains"] for s in records["scenarios"]}
    by_domain = {}
    for ts in records["task_statements"]:
        if not ts.get("points"):
            raise PlanError("Task statement %s has no points." % ts["id"])
        by_domain.setdefault(ts["domain"], []).append(ts)
    rng = random.Random(seed)

    # 1. The seed selects one of the sets, and the sequence of the 4 groups.
    sets = scenario_sets(records, counts)
    if not sets:
        raise PlanError("No set of 4 scenarios has a table.")
    scenarios = list(_choice(rng, sets))
    _shuffle(rng, scenarios)

    # 2. The most even table. The seed selects one when two are equal.
    found = tables(sorted(scenarios), primary, counts)
    least = min(_squares(t) for t in found)
    best = sorted((t for t in found if _squares(t) == least),
                  key=lambda t: json.dumps(t, sort_keys=True))
    table = _choice(rng, best)

    # 3. In each domain, the task statements share the questions equally. A task
    #    statement gets no more questions than it has groups (decision 0048).
    #    The seed sets the order in which task statements get the questions
    #    that are left. Each one gets at most one extra question. Code takes the
    #    first choice in that order that keeps a full plan possible, over all
    #    domains together.
    # 4. The seed sets the order of the points of each task statement, and the
    #    groups that earlier mocks used least come first (decision 0050). Code
    #    takes the first point whose group is free and that keeps a full plan
    #    possible.
    #    No two slots get points of the same group (decisions 0047 and 0048).
    if two_answer is None:
        two_answer = load_two_answer_points(records)
    of = point_groups.group_of(groups)
    earlier = earlier or {}
    use = {}
    for points in earlier.values():
        for p in points:
            if p not in of:
                raise PlanError("An earlier mock has the point %s, which is in no group." % p)
            use[of[p]["id"]] = use.get(of[p]["id"], 0) + 1
    ts_groups = {ts["id"]: frozenset(of[p["id"]]["id"] for p in ts["points"]) for ts in records["task_statements"]}
    statements = {}
    need = {}
    for d in sorted(counts):
        statements[d] = sorted(by_domain.get(d, []), key=lambda t: [int(x) for x in t["id"].split(".")])
        if not statements[d]:
            raise PlanError("Domain %d has no task statements." % d)
        share = counts[d] // len(statements[d])
        if share < 1:
            raise PlanError("Domain %d has more task statements than questions. Each task statement "
                            "must get at least 1 question." % d)
        for ts in statements[d]:
            need[ts["id"]] = min(share, len(ts_groups[ts["id"]]))
    if not _possible(need, ts_groups, frozenset()):
        start = {}
        for t in sorted(need, key=lambda x: [int(n) for n in x.split(".")]):
            start[t] = need[t]
            if not _possible(start, ts_groups, frozenset()):
                raise PlanError("No plan is possible with these groups, even with no extra questions. "
                                "Task statement %s cannot get its %d questions." % (t, need[t]))
    orders = []
    for d in sorted(counts):
        order = list(statements[d])
        _shuffle(rng, order)
        left = counts[d] - sum(need[ts["id"]] for ts in statements[d])
        share = counts[d] // len(statements[d])
        orders.append((d, [ts["id"] for ts in order if need[ts["id"]] == share
                           and share < len(ts_groups[ts["id"]])], left))
    found = _extras(orders, need, ts_groups)
    if found is None:
        raise PlanError("No plan is possible with these groups: the extra questions of domains %s "
                        "find no task statements with free groups."
                        % ", ".join(str(d) for d, _, left in orders if left))
    need = found
    used = set()
    picked = {}
    rest = dict(need)
    for d in sorted(counts):
        for ts in statements[d]:
            pool = list(ts["points"])
            _shuffle(rng, pool)
            # Decision 0050: the groups that earlier mocks used least come first.
            # The seed keeps the order inside the same count.
            pool.sort(key=lambda p: use.get(of[p["id"]]["id"], 0))
            picked[ts["id"]] = []
            for _ in range(need[ts["id"]]):
                rest[ts["id"]] -= 1
                for p in pool:
                    g = of[p["id"]]["id"]
                    if g not in used and _possible(rest, ts_groups, frozenset(used | {g})):
                        used.add(g)
                        picked[ts["id"]].append(p)
                        pool.remove(p)
                        break
                else:
                    raise PlanError("Task statement %s has no allowed point left." % ts["id"])

    # 5. The seed decides which scenario each question goes to.
    questions = []   # (scenario, task statement, point)
    for d in sorted(counts):
        items = [(ts["id"], p["id"]) for ts in statements[d] for p in picked[ts["id"]]]
        places = [s for s in sorted(table) for _ in range(table[s].get(d, 0))]
        if len(places) != len(items):
            raise PlanError("Domain %d: the table has %d places for %d questions." % (d, len(places), len(items)))
        _shuffle(rng, places)
        questions.extend([s, ts, p] for s, (ts, p) in zip(places, items))
    # Decision 0054: each scenario needs 2 questions on a two-answer point. If a
    # scenario has fewer, code swaps the scenarios of two questions of the same
    # domain with a scenario that has more than 2.
    domain_of = {ts["id"]: ts["domain"] for ts in records["task_statements"]}

    def listed(s):
        return [q for q in questions if q[0] == s and q[2] in two_answer]
    for s in sorted(table):
        while len(listed(s)) < MULTIPLE_RESPONSE_PER_SCENARIO:
            swap = None
            for give in sorted(table):
                if give == s or len(listed(give)) <= MULTIPLE_RESPONSE_PER_SCENARIO:
                    continue
                for q2 in listed(give):
                    q1 = next((q for q in questions if q[0] == s and q[2] not in two_answer
                               and domain_of[q[1]] == domain_of[q2[1]]), None)
                    if q1 is not None:
                        swap = (q1, q2)
                        break
                if swap:
                    break
            if swap is None:
                raise PlanError("Scenario %d has fewer than %d questions on a two-answer point (decision 0054)."
                                % (s, MULTIPLE_RESPONSE_PER_SCENARIO))
            swap[0][0], swap[1][0] = swap[1][0], swap[0][0]
    questions = [tuple(q) for q in questions]

    # 6. Two multiple-response slots in each scenario, on two-answer points
    #    (decision 0054). The seed selects them.
    # 7. The slots get the numbers 1 to 60, group by group. The seed sets the
    #    sequence inside a group.
    slots = []
    for s in scenarios:
        group = sorted((q for q in questions if q[0] == s), key=lambda q: q[2])
        if len(group) != PER_SCENARIO:
            raise PlanError("Scenario %d has %d questions, not %d." % (s, len(group), PER_SCENARIO))
        _shuffle(rng, group)
        multiple = set(_sample(rng, [i for i, q in enumerate(group) if q[2] in two_answer],
                               MULTIPLE_RESPONSE_PER_SCENARIO))
        for i, (_, ts, p) in enumerate(group):
            many = i in multiple
            slots.append({"slot_id": "M%d-S%02d" % (mock, len(slots) + 1), "scenario": s,
                          "task_statement": ts, "point": p,
                          "type": "multiple_response" if many else "multiple_choice",
                          "options": 5 if many else 4, "select": 2 if many else 1})
    if len(slots) != QUESTIONS:
        raise PlanError("The plan has %d slots, not %d." % (len(slots), QUESTIONS))
    # 8. The seed selects the slots on which the longest option may be correct
    #    (decision 0053). On the other slots, step 3 checks that a wrong option is
    #    the longest (rule A12).
    for select, number in sorted(LONGEST_MAY_BE_CORRECT.items()):
        group = [s for s in slots if s["select"] == select]
        allowed = {s["slot_id"] for s in _sample(rng, group, number)}
        for s in group:
            s["longest_may_be_correct"] = s["slot_id"] in allowed
    same = point_groups.conflicts([(x["slot_id"], x["point"]) for x in slots], groups)
    if same:
        raise PlanError("Two slots are in one group: %s" % "; ".join(
            "%s: %s" % (g["id"], ", ".join(x for x, _ in items)) for g, items in same))
    return {"mock": mock, "seed": seed, "guide_version": records["guide"]["version"], "date": date,
            "earlier_mocks": sorted(earlier),
            "scenarios": scenarios,
            "table": {str(s): {str(d): n for d, n in sorted(table[s].items())} for s in scenarios},
            "slots": slots}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Step 1: make the plan of one mock.")
    parser.add_argument("--mock", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--runs", default=os.path.join(ROOT, "runs"))
    parser.add_argument("--records", default=RECORDS)
    parser.add_argument("--groups", default=point_groups.GROUPS)
    parser.add_argument("--mocks", default=os.path.join(ROOT, "mocks"))
    args = parser.parse_args(argv)
    path = os.path.join(args.runs, "mock-%02d" % args.mock, "plan.json")
    if os.path.exists(path):
        print("A plan exists already: " + path)
        return 1
    try:
        with open(args.records, encoding="utf-8") as f:
            records = json.load(f)
    except (OSError, ValueError) as e:
        print("No plan: the records file cannot be read: %s" % e)
        return 1
    try:
        groups = point_groups.load(args.groups)
    except (OSError, ValueError) as e:
        print("No plan: the groups file cannot be read: %s" % e)
        return 1
    try:
        plan = make_plan(records, args.mock, args.seed, datetime.date.today().isoformat(), groups,
                         earlier_points(args.mocks, args.mock))
    except PlanError as e:
        print("No plan: " + str(e))
        return 1
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Written: " + path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
