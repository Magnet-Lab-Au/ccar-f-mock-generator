"""Step 1 of the pipeline: the plan of a mock (decisions 0009, 0027 and 0037, item 14).

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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS = os.path.join(ROOT, "reference", "guide-records.json")

QUESTIONS = 60
PER_SCENARIO = 15
SCENARIOS_IN_MOCK = 4
MULTIPLE_RESPONSE_PER_SCENARIO = 2   # a guess with no source (decision 0027)
DOMAIN_COUNTS = {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}   # decision 0027, item 1


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


def make_plan(records, mock, seed, date):
    """Return the plan of one mock. Raise PlanError, and make no plan, if a record
    is missing or a count does not add up."""
    check_records(records)
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

    # 3. In each domain, the task statements share the questions equally.
    #    The seed selects which task statements get the questions that are left.
    # 4. The seed decides which scenario each of these questions goes to.
    # 5. The seed selects one point for each slot. No two slots get the same point.
    questions = []   # (scenario, task statement, point)
    for d in sorted(counts):
        statements = sorted(by_domain.get(d, []), key=lambda t: [int(x) for x in t["id"].split(".")])
        if not statements:
            raise PlanError("Domain %d has no task statements." % d)
        share, left = divmod(counts[d], len(statements))
        if share < 1:
            raise PlanError("Domain %d has more task statements than questions. Each task statement "
                            "must get at least 1 question." % d)
        extra = set(t["id"] for t in _sample(rng, statements, left))
        items = []
        for ts in statements:
            n = share + (1 if ts["id"] in extra else 0)
            if n > len(ts["points"]):
                raise PlanError("Task statement %s has fewer points than questions." % ts["id"])
            for p in _sample(rng, ts["points"], n):
                items.append((ts["id"], p["id"]))
        places = [s for s in sorted(table) for _ in range(table[s].get(d, 0))]
        if len(places) != len(items):
            raise PlanError("Domain %d: the table has %d places for %d questions." % (d, len(places), len(items)))
        _shuffle(rng, places)
        questions.extend((s, ts, p) for s, (ts, p) in zip(places, items))

    # 6. Two multiple-response slots in each scenario.
    # 7. The slots get the numbers 1 to 60, group by group. The seed sets the
    #    sequence inside a group.
    slots = []
    for s in scenarios:
        group = sorted((q for q in questions if q[0] == s), key=lambda q: q[2])
        if len(group) != PER_SCENARIO:
            raise PlanError("Scenario %d has %d questions, not %d." % (s, len(group), PER_SCENARIO))
        _shuffle(rng, group)
        multiple = set(_sample(rng, range(PER_SCENARIO), MULTIPLE_RESPONSE_PER_SCENARIO))
        for i, (_, ts, p) in enumerate(group):
            many = i in multiple
            slots.append({"slot_id": "M%d-S%02d" % (mock, len(slots) + 1), "scenario": s,
                          "task_statement": ts, "point": p,
                          "type": "multiple_response" if many else "multiple_choice",
                          "options": 5 if many else 4, "select": 2 if many else 1})
    if len(slots) != QUESTIONS:
        raise PlanError("The plan has %d slots, not %d." % (len(slots), QUESTIONS))
    return {"mock": mock, "seed": seed, "guide_version": records["guide"]["version"], "date": date,
            "scenarios": scenarios,
            "table": {str(s): {str(d): n for d, n in sorted(table[s].items())} for s in scenarios},
            "slots": slots}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Step 1: make the plan of one mock.")
    parser.add_argument("--mock", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--runs", default=os.path.join(ROOT, "runs"))
    parser.add_argument("--records", default=RECORDS)
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
        plan = make_plan(records, args.mock, args.seed, datetime.date.today().isoformat())
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
