"""Check for decision 0027: which sets of 4 scenarios fit the domain counts.

A set fits when all 60 questions can be in a primary domain of their scenario,
with 15 questions for each scenario and the domain counts 16, 11, 12, 12, 9.
The primary domains are from the exam guide, Section 5.
Run: python3 0027-check-scenario-sets.py
"""
import collections
import itertools

PRIMARY = {1: {1, 2, 5}, 2: {3, 5}, 3: {1, 2, 5}, 4: {1, 2, 3}, 5: {3, 4}, 6: {4, 5}}
QUOTA = {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}
PER_SCENARIO = 15


def max_fit(scenarios):
    """Largest number of questions that fit a primary domain (maximum flow)."""
    cap = collections.defaultdict(int)
    for s in scenarios:
        cap[("S", ("s", s))] = PER_SCENARIO
        for d in PRIMARY[s]:
            cap[(("s", s), ("d", d))] = 999
    for d, q in QUOTA.items():
        cap[(("d", d), "T")] = q
    nodes = {n for edge in list(cap) for n in edge}
    flow = 0
    while True:
        parent = {"S": None}
        queue = ["S"]
        while queue and "T" not in parent:
            u = queue.pop(0)
            for v in nodes:
                if v not in parent and cap[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)
        if "T" not in parent:
            return flow
        push, v = 999, "T"
        while parent[v] is not None:
            push = min(push, cap[(parent[v], v)])
            v = parent[v]
        v = "T"
        while parent[v] is not None:
            cap[(parent[v], v)] -= push
            cap[(v, parent[v])] += push
            v = parent[v]
        flow += push


assert sum(QUOTA.values()) == 60
fits = 0
for combo in itertools.combinations(sorted(PRIMARY), 4):
    n = max_fit(combo)
    fits += n == 60
    print(combo, n, "fits" if n == 60 else "does not fit")
print("sets that fit:", fits, "of 15")
