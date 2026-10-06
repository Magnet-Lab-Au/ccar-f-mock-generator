"""Check for decision 0037, item 14: the table of scenarios and domains.

For each set of 4 scenarios, the script finds each table that fits:
15 questions for each scenario, at least 1 question for each primary domain
of a scenario, no question outside a primary domain, and the domain counts
16, 11, 12, 12 and 9 (decision 0027).
It prints the number of tables, the most even table (the smallest sum of
squares), how many tables are equal to it, and the largest number in it.
The primary domains come from reference/guide-records.json.
Run: python3 0037-check-scenario-tables.py
"""
import itertools
import json
from pathlib import Path

RECORDS = Path(__file__).resolve().parents[2] / "reference" / "guide-records.json"
QUOTA = {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}
PER_SCENARIO = 15
MINIMUM = 1

records = json.loads(RECORDS.read_text(encoding="utf-8"))
PRIMARY = {s["id"]: sorted(s["primary_domains"]) for s in records["scenarios"]}


def rows(total, parts):
    """Each way to divide total into parts numbers, each at least MINIMUM."""
    if parts == 1:
        if total >= MINIMUM:
            yield (total,)
        return
    for first in range(MINIMUM, total + 1):
        for rest in rows(total - first, parts - 1):
            yield (first,) + rest


def tables(scenarios):
    found = []

    def fill(index, left, table):
        if index == len(scenarios):
            if all(value == 0 for value in left.values()):
                found.append(tuple(table))
            return
        domains = PRIMARY[scenarios[index]]
        for row in rows(PER_SCENARIO, len(domains)):
            if all(n <= left[d] for d, n in zip(domains, row)):
                new_left = dict(left)
                for d, n in zip(domains, row):
                    new_left[d] -= n
                fill(index + 1, new_left, table + [row])

    fill(0, dict(QUOTA), [])
    return found


def squares(table):
    return sum(n * n for row in table for n in row)


assert sum(QUOTA.values()) == 60
sets_that_fit = 0
sets_with_12 = 0
for scenarios in itertools.combinations(sorted(PRIMARY), 4):
    found = tables(scenarios)
    if not found:
        print(scenarios, "no table")
        continue
    sets_that_fit += 1
    least = min(squares(t) for t in found)
    best = [t for t in found if squares(t) == least]
    largest = max(n for row in best[0] for n in row)
    sets_with_12 += largest >= 12
    shown = {s: dict(zip(PRIMARY[s], row)) for s, row in zip(scenarios, best[0])}
    print(scenarios, "tables:", len(found), "| equal most even tables:", len(best),
          "| largest number:", largest, "|", shown)
print("sets that have a table:", sets_that_fit, "of 15")
print("sets where one scenario has 12 or more questions of one domain:", sets_with_12)
