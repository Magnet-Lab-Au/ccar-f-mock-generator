"""Check of step 0 (decision 0028, check 2).

It checks reference/guide-records.json against reference/exam-guide.md and
against reference/task-statements-and-points.md. It does not use the code of
step 0. It prints one line for each check.

Run from the folder mock-builder-v3:
    python3 src/check_guide_records.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "reference")

with open(os.path.join(REF, "exam-guide.md"), encoding="utf-8") as f:
    GUIDE = f.read()
with open(os.path.join(REF, "task-statements-and-points.md"), encoding="utf-8") as f:
    POINTS_MD = f.read()
with open(os.path.join(REF, "guide-records.json"), encoding="utf-8") as f:
    REC = json.load(f)

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))


def between(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]


statements = REC["task_statements"]
points = [p for ts in statements for p in ts["points"]]
questions = REC["sample_questions"]

# 1. Counts
check("5 domains", len(REC["domains"]) == 5, str(len(REC["domains"])))
check("6 scenarios", len(REC["scenarios"]) == 6, str(len(REC["scenarios"])))
check("30 task statements", len(statements) == 30, str(len(statements)))
check("240 points", len(points) == 240, str(len(points)))
check("12 sample questions", len(questions) == 12, str(len(questions)))
check("top level has 6 parts", sorted(REC) == ["domains", "guide", "sample_questions", "scenarios", "section_17", "task_statements"])

# 2. IDs
ids = [p["id"] for p in points]
check("each point ID is different", len(set(ids)) == 240)
bad = [p["id"] for ts in statements for p in ts["points"]
       if not re.fullmatch(re.escape(ts["id"]) + r"-[KS]\d+", p["id"])
       or (p["id"].split("-")[1][0] == "K") != (p["kind"] == "knowledge") or p["kind"] not in ("knowledge", "skill")]
check("each point ID has the form of its task statement and its kind", not bad, ", ".join(bad))
bad = []
for ts in statements:
    for letter in "KS":
        nums = [int(p["id"].split("-")[1][1:]) for p in ts["points"] if p["id"].split("-")[1][0] == letter]
        if nums != list(range(1, len(nums) + 1)) or not nums:
            bad.append(ts["id"] + letter)
check("point numbers start at 1 and have no gap, for K and S of each task statement", not bad, ", ".join(bad))
check("each task statement is in the domain of its ID", all(ts["id"].split(".")[0] == str(ts["domain"]) for ts in statements))
per_domain = [sum(1 for ts in statements if ts["domain"] == d) for d in (1, 2, 3, 4, 5)]
check("task statements for each domain are 7, 5, 6, 6, 6", per_domain == [7, 5, 6, 6, 6], str(per_domain))

# 3. Each text is exactly in the guide
texts = [REC["guide"]["version"]]
texts += [d["name"] for d in REC["domains"]]
texts += [s[k] for s in REC["scenarios"] for k in ("name", "story")]
texts += [ts["title"] for ts in statements] + [p["text"] for p in points]
texts += [q[k] for q in questions for k in ("question", "explanation")]
texts += [t for q in questions for t in q["options"].values()]
texts += [t for items in REC["section_17"].values() for t in items]
missing = [t[:50] for t in texts if not t or t not in GUIDE]
check("each of the %d texts is exactly in the guide" % len(texts), not missing, " | ".join(missing))
edge = [t[:50] for t in texts if t != t.strip()]
check("no text starts or ends with a space", not edge, " | ".join(edge))

# 4. Nothing of the guide is left out
sec6 = between(GUIDE, "## 6. Detailed Objectives by Domain", "## 7. How to Prepare")
bullets6 = [ln[2:] for ln in sec6.split("\n") if ln.startswith("- ")]
check("Section 6 of the guide has 240 bullets, and they are the 240 points in the same sequence",
      bullets6 == [p["text"] for p in points], "guide bullets: %d" % len(bullets6))
titles6 = re.findall(r"^### \*\*Task Statement (\d\.\d): (.+)\*\*$", sec6, flags=re.M)
check("the 30 task statement headings of the guide are the 30 records", titles6 == [(ts["id"], ts["title"]) for ts in statements])
sec17 = between(GUIDE, "## 17. Appendix", "## 18. Document Control")
bullets17 = [ln[2:] for ln in sec17.split("\n") if ln.startswith("- ")]
s17 = REC["section_17"]
check("Section 17 of the guide has the same bullets as the 3 lists, in the same sequence",
      bullets17 == s17["technologies"] + s17["in_scope"] + s17["out_of_scope"],
      "%d = %d + %d + %d" % (len(bullets17), len(s17["technologies"]), len(s17["in_scope"]), len(s17["out_of_scope"])))
sec9 = between(GUIDE, "## 9. Sample Questions", "## 10. How the Exam Is Scored")
check("Section 9 of the guide has 12 questions and 12 answers",
      len(re.findall(r"^\*\*Question \d+:\*\*", sec9, flags=re.M)) == 12 and len(re.findall(r"^\*\*Correct Answer: ", sec9, flags=re.M)) == 12)
n_opts = len(re.findall(r"^\*\*[A-Z]\.\*\* ", sec9, flags=re.M))
check("Section 9 of the guide has the same number of options as the records", n_opts == sum(len(q["options"]) for q in questions), str(n_opts))

# 5. The points agree with the file for people, which a reviewer confirmed on 5 October 2026
md_points = re.findall(r"^- \*\*(\d\.\d-[KS]\d+)\*\* (.+)$", POINTS_MD, flags=re.M)
check("the 240 points agree with task-statements-and-points.md, ID and text", md_points == [(p["id"], p["text"]) for p in points], "file has %d" % len(md_points))
md_titles = re.findall(r"^### Task Statement (\d\.\d): (.+)$", POINTS_MD, flags=re.M)
check("the 30 titles agree with task-statements-and-points.md", md_titles == [(ts["id"], ts["title"]) for ts in statements])

# 6. Domains and scenarios
check("domain weights are 27, 18, 20, 20, 15", [d["weight"] for d in REC["domains"]] == [27, 18, 20, 20, 15])
check("domain IDs are 1 to 5 and scenario IDs are 1 to 6",
      [d["id"] for d in REC["domains"]] == [1, 2, 3, 4, 5] and [s["id"] for s in REC["scenarios"]] == [1, 2, 3, 4, 5, 6])
names = {d["id"]: d["name"] for d in REC["domains"]}
bad = [str(s["id"]) for s in REC["scenarios"]
       if ("### Scenario %d: %s\n" % (s["id"], s["name"])) not in GUIDE
       or ("Primary domains: " + ", ".join(names[i] for i in s["primary_domains"]) + "\n") not in GUIDE]
check("each scenario heading and each line of primary domains is in the guide", not bad, ", ".join(bad))
for s in REC["scenarios"]:
    part = between(GUIDE, "### Scenario %d: " % s["id"], "### Scenario %d: " % (s["id"] + 1) if s["id"] < 6 else "## 6. ")
    ok = s["story"] in part and ("Primary domains: " + ", ".join(names[i] for i in s["primary_domains"])) in part
    check("scenario %d: the story and the primary domains %s are below its heading" % (s["id"], s["primary_domains"]), ok)

# 7. Sample questions
scen_names = {s["id"]: s["name"] for s in REC["scenarios"]}
for q in questions:
    start = "**Question %d:** " % q["number"]
    end = "**Question %d:** " % (q["number"] + 1) if q["number"] < 12 else "## 10. "
    part = between(GUIDE, start, end)
    head = GUIDE[:GUIDE.index(start)]
    last_scenario = re.findall(r"^### \*\*Scenario: (.+)\*\*$", head, flags=re.M)[-1]
    ok = (part.startswith(start + q["question"] + "\n")
          and sorted(q["options"]) == ["A", "B", "C", "D"]
          and all(("**%s.** %s\n" % (k, v)) in part for k, v in q["options"].items())
          and len(q["correct_answer"]) == 1
          and ("**Correct Answer: %s.** %s\n" % (q["correct_answer"][0], q["explanation"])) in part
          and scen_names[q["scenario"]] == last_scenario)
    check("sample question %d: question, 4 options, answer %s, explanation and scenario %d agree with the guide"
          % (q["number"], q["correct_answer"][0], q["scenario"]), ok)

print("%d of %d checks passed" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
