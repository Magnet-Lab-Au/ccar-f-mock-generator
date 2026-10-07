"""Step 0 of the pipeline: prepare the guide records (decisions 0017 and 0028).

It reads reference/exam-guide.md and writes reference/guide-records.json.
It copies each text with no change. It writes no file if a count is wrong
or if a text is not exactly in the guide.

Run from the folder ccar-f-mock-generator:
    python3 src/step0_prepare_guide_records.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE = os.path.join(ROOT, "reference", "exam-guide.md")
OUT = os.path.join(ROOT, "reference", "guide-records.json")

PAGE_LINE = re.compile(r"^<!-- Page \d+ \| .* -->$")
EXPECTED = {"domains": 5, "scenarios": 6, "task_statements": 30, "points": 240, "sample_questions": 12}


class GuideError(Exception):
    """The guide does not have the form that this script expects."""


def need(condition, message):
    if not condition:
        raise GuideError(message)


def section(lines, start_pattern, end_pattern):
    """The lines after the heading start_pattern, up to the heading end_pattern."""
    starts = [i for i, line in enumerate(lines) if re.match(start_pattern, line)]
    need(len(starts) == 1, "heading not found one time: " + start_pattern)
    for j in range(starts[0] + 1, len(lines)):
        if re.match(end_pattern, lines[j]):
            return lines[starts[0] + 1:j]
    raise GuideError("end of section not found: " + end_pattern)


def read_guide():
    with open(GUIDE, encoding="utf-8", newline="") as f:
        raw = f.read()
    # A page line is a mark of the PDF page. It is not guide text.
    lines = [ln for ln in raw.replace("\r\n", "\n").split("\n") if ln.strip() and not PAGE_LINE.match(ln)]
    return raw, lines


def parse_version(lines):
    found = [ln for ln in lines if ln.startswith("Version ")]
    need(len(found) == 1, "version line not found one time")
    return {"version": found[0]}


def parse_domains(lines):
    domains = []
    for ln in section(lines, r"^## 4\. ", r"^## 5\. "):
        m = re.match(r"^\| (\d) \| (.+?) \| (\d+)% \|$", ln)
        if m:
            domains.append({"id": int(m.group(1)), "name": m.group(2), "weight": int(m.group(3))})
    need([d["id"] for d in domains] == [1, 2, 3, 4, 5], "domain ids are not 1 to 5")
    need(sum(d["weight"] for d in domains) == 100, "domain weights do not add up to 100")
    return domains


def parse_scenarios(lines, domains):
    by_name = {d["name"]: d["id"] for d in domains}
    body = section(lines, r"^## 5\. ", r"^## 6\. ")
    scenarios = []
    i = 0
    while i < len(body):
        m = re.match(r"^### Scenario (\d): (.+)$", body[i])
        if m:
            story, primary = body[i + 1], body[i + 2]
            need(primary.startswith("Primary domains: "), "no primary domains for scenario " + m.group(1))
            names = primary[len("Primary domains: "):].split(", ")
            for name in names:
                need(name in by_name, "unknown domain name in scenario %s: %s" % (m.group(1), name))
            scenarios.append({"id": int(m.group(1)), "name": m.group(2), "story": story,
                              "primary_domains": [by_name[n] for n in names]})
            i += 3
        else:
            i += 1
    need([s["id"] for s in scenarios] == [1, 2, 3, 4, 5, 6], "scenario ids are not 1 to 6")
    return scenarios


def parse_task_statements(lines):
    body = section(lines, r"^## 6\. ", r"^## 7\. ")
    statements, current, kind, domain = [], None, None, None
    for ln in body:
        m_dom = re.match(r"^## Domain (\d): ", ln)
        m_ts = re.match(r"^### \*\*Task Statement (\d)\.(\d): (.+)\*\*$", ln)
        if m_dom:
            domain = int(m_dom.group(1))
        elif m_ts:
            need(int(m_ts.group(1)) == domain, "task statement in the wrong domain: " + ln)
            current = {"id": "%s.%s" % (m_ts.group(1), m_ts.group(2)), "domain": domain,
                       "title": m_ts.group(3), "points": []}
            statements.append(current)
            kind = None
        elif ln == "**Knowledge of:**":
            kind = "knowledge"
        elif ln == "**Skills in:**":
            kind = "skill"
        elif ln.startswith("- "):
            need(current is not None and kind is not None, "bullet with no heading: " + ln[:60])
            letter = "K" if kind == "knowledge" else "S"
            number = 1 + sum(1 for p in current["points"] if p["kind"] == kind)
            current["points"].append({"id": "%s-%s%d" % (current["id"], letter, number), "kind": kind, "text": ln[2:]})
        else:
            need(statements == [] and domain is None, "line that the script does not know: " + ln[:60])
    for ts in statements:
        kinds = [p["kind"] for p in ts["points"]]
        need("knowledge" in kinds and "skill" in kinds, "task statement with one kind of point only: " + ts["id"])
        need(kinds == sorted(kinds), "a knowledge point comes after a skill point: " + ts["id"])
    return statements


def parse_sample_questions(lines, scenarios):
    by_name = {s["name"]: s["id"] for s in scenarios}
    body = section(lines, r"^## 9\. ", r"^## 10\. ")
    questions, scenario, current = [], None, None
    for ln in body:
        m_sc = re.match(r"^### \*\*Scenario: (.+)\*\*$", ln)
        m_q = re.match(r"^\*\*Question (\d+):\*\* (.+)$", ln)
        m_opt = re.match(r"^\*\*([A-Z])\.\*\* (.+)$", ln)
        m_ans = re.match(r"^\*\*Correct Answer: ([A-Z])\.\*\* (.+)$", ln)
        if m_sc:
            need(m_sc.group(1) in by_name, "unknown scenario name: " + m_sc.group(1))
            scenario = by_name[m_sc.group(1)]
        elif m_q:
            need(scenario is not None, "question with no scenario")
            current = {"number": int(m_q.group(1)), "scenario": scenario, "question": m_q.group(2),
                       "options": {}, "correct_answer": None, "explanation": None}
            questions.append(current)
        elif m_opt:
            need(current is not None and current["correct_answer"] is None, "option in the wrong place: " + ln[:60])
            current["options"][m_opt.group(1)] = m_opt.group(2)
        elif m_ans:
            need(current is not None and current["correct_answer"] is None, "answer in the wrong place: " + ln[:60])
            current["correct_answer"] = [m_ans.group(1)]
            current["explanation"] = m_ans.group(2)
        else:
            need(not questions, "line that the script does not know: " + ln[:60])
    need([q["number"] for q in questions] == list(range(1, len(questions) + 1)), "question numbers are not in sequence")
    for q in questions:
        need(len(q["options"]) >= 2, "question %d has fewer than 2 options" % q["number"])
        need(q["correct_answer"] and q["correct_answer"][0] in q["options"], "question %d has no valid answer" % q["number"])
    return questions


def parse_section_17(lines):
    body = section(lines, r"^## 17\. ", r"^## 18\. ")
    names = {"### **Technologies and Concepts**": "technologies",
             "### **In-Scope Topics**": "in_scope",
             "### **Out-of-Scope Topics**": "out_of_scope"}
    lists, key = {v: [] for v in names.values()}, None
    for ln in body:
        if ln in names:
            key = names[ln]
        elif ln.startswith("- "):
            need(key is not None, "bullet with no heading in Section 17")
            lists[key].append(ln[2:])
        else:
            need(not ln.startswith("#"), "heading that the script does not know: " + ln)
    for k, v in lists.items():
        need(len(v) > 0, "empty list in Section 17: " + k)
    return lists


def all_texts(records):
    yield records["guide"]["version"]
    for d in records["domains"]:
        yield d["name"]
    for s in records["scenarios"]:
        yield s["name"]
        yield s["story"]
    for ts in records["task_statements"]:
        yield ts["title"]
        for p in ts["points"]:
            yield p["text"]
    for q in records["sample_questions"]:
        yield q["question"]
        yield q["explanation"]
        for text in q["options"].values():
            yield text
    for items in records["section_17"].values():
        for text in items:
            yield text


def build():
    raw, lines = read_guide()
    domains = parse_domains(lines)
    scenarios = parse_scenarios(lines, domains)
    records = {
        "guide": parse_version(lines),
        "domains": domains,
        "scenarios": scenarios,
        "task_statements": parse_task_statements(lines),
        "sample_questions": parse_sample_questions(lines, scenarios),
        "section_17": parse_section_17(lines),
    }
    counts = {
        "domains": len(records["domains"]),
        "scenarios": len(records["scenarios"]),
        "task_statements": len(records["task_statements"]),
        "points": sum(len(ts["points"]) for ts in records["task_statements"]),
        "sample_questions": len(records["sample_questions"]),
    }
    for name, expected in EXPECTED.items():
        need(counts[name] == expected, "count of %s is %d, expected %d" % (name, counts[name], expected))
    for text in all_texts(records):
        need(text and text in raw, "text is not exactly in the guide: " + text[:60])
    return records, counts


def main():
    try:
        records, counts = build()
    except (GuideError, OSError) as error:
        print("Step 0 failed. No file is written. Cause: %s" % error, file=sys.stderr)
        return 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Step 0 wrote", os.path.relpath(OUT, ROOT))
    for name, n in counts.items():
        print("  %-17s %d" % (name, n))
    for name, items in records["section_17"].items():
        print("  %-17s %d" % ("17 " + name, len(items)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
