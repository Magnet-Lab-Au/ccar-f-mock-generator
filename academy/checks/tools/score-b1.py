"""Scores check B1 (academy/check-plan.md). Run: python3 score-b1.py <b1-dir> <domain> [...]
An answer counts as correct only when its set of letters equals the set of the answer file.
A quote is valid when its normalized text is in the page file of its domain."""
import collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B1 = sys.argv[1]
key, meta = {}, {}
for f in glob.glob(os.path.join(ROOT, "mocks", "mock-*.answers.json")):
    for a in json.load(open(f))["answers"]:
        key[a["question_id"]] = set(a["correct"])
for f in glob.glob(os.path.join(ROOT, "mocks", "mock-*.questions.json")):
    for g in json.load(open(f))["groups"]:
        for q in g["questions"]:
            meta[q["question_id"]] = (q["task_statement"], q["point"])


def norm(s):
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip().lower().rstrip(".")


for d in sys.argv[2:]:
    page = norm(open(os.path.join(B1, "domain-%s.page.md" % d)).read())
    asked = re.findall(r"^### (M\d-S\d+-T\d+)", open(os.path.join(B1, "domain-%s.questions.md" % d)).read(), re.M)
    ans = {a["id"]: a for a in json.load(open(os.path.join(B1, "domain-%s.answers.json" % d)))}
    tot = collections.Counter()
    by_ts = collections.defaultdict(collections.Counter)
    wrong = []
    for qid in asked:
        a = ans.get(qid)
        ts = meta[qid][0]
        tot["asked"] += 1; by_ts[ts]["asked"] += 1
        if not a:
            tot["missing"] += 1; continue
        ok = set(a["answer"]) == key[qid]
        valid = bool(a.get("quote")) and norm(a["quote"]) in page
        tot["correct"] += ok; by_ts[ts]["correct"] += ok
        tot["valid quote"] += valid
        tot["correct, valid quote"] += ok and valid; by_ts[ts]["correct, valid quote"] += ok and valid
        tot["basis own"] += a.get("basis") == "own"
        if not ok:
            wrong.append((qid, ts, meta[qid][1], "".join(sorted(a["answer"])), "".join(sorted(key[qid])), a.get("basis"), valid))
    print("## Domain %s" % d)
    print(", ".join("%s %d" % kv for kv in tot.items()))
    print("By task statement (correct with a valid quote / asked): " + ", ".join(
        "%s %d/%d" % (ts, c["correct, valid quote"], c["asked"]) for ts, c in sorted(by_ts.items())))
    print("Wrong answers (ID, task statement, point, given, key, basis, valid quote):")
    for w in wrong:
        print("- %s %s %s given %s key %s basis %s quote %s" % w)
    print()
