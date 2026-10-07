"""Step 4: a blind answer, then a rule check (decisions 0012, 0023, 0030, 0032, 0037 and 0040).

Call 4a answers the question with no marks and no reasons. Call 4b checks the
rules B1 to B6 with the complete record and the guide text. Code checks each
answer, searches the feature names in the records file, and makes the verdict.
A model does not make the verdict.
"""
import json
import re

from control import CallFailed
from model_call import load_form
from step2_write import plain

DESC_4A, SCHEMA_4A = load_form("06-forms-draft.json", "call_4a")
DESC_4B, SCHEMA_4B = load_form("06-forms-draft.json", "call_4b")
RULES_B = ["B1", "B2", "B3", "B4", "B5", "B6"]

RULES_TEXT = """B1. Each option that is marked correct is correct, and no other option is correct.
B2. Each wrong option is wrong for a reason that the guide gives, and its reason says so.
B3. Each reason is true and agrees with the guide.
B4. The question tests the point of its slot.
B5. The question is inside the story of its scenario and does not contradict it.
B6. No text depends on a feature that the guide does not name. A feature is a thing of a Claude product or of MCP that has a name: a tool, a command, a flag, a parameter, a field, a file or a setting. A name that the question invents for its story is not a feature. General technology, for example Python, is not a feature. List in "features" each feature name that the question, the options and the reasons use."""

SYSTEM_4A = ("You answer one exam question of the exam \"Claude Certified Architect - Foundations\", as a candidate does. "
             "Select the options that you think are correct. If you cannot decide, say so. " + DESC_4A)
SYSTEM_4B = ("You check one exam question against six rules. Use only the text of the exam guide below as the source of facts. "
             "Give one result for each rule: pass, fail or cannot_decide. A result that is not pass has a finding. " + DESC_4B)


def show(question, with_key):
    """Decision 0037, item 1: the one function that shows a question. With no
    key: the question, the line "Select N." and the options with their letters."""
    lines = [question["question"], "Select %d." % question["select"]]
    for o in question["options"]:
        lines.append("%s. %s" % (o["letter"], o["text"]))
        if with_key:
            lines.append("   Marked: %s. Reason: %s" % ("correct" if o["correct"] else "wrong", o["reason"]))
    return "\n".join(lines)


def guide_text(records, scenario):
    """Decision 0032, part 3: the story of the scenario, all 30 task statements
    with their 240 points, and the three lists of Section 17."""
    sc = next(s for s in records["scenarios"] if s["id"] == scenario)
    parts = ["THE EXAM GUIDE", "", "The story of scenario %d (%s):" % (sc["id"], sc["name"]), plain(sc["story"]), ""]
    for t in records["task_statements"]:
        parts.append("Task statement %s: %s" % (t["id"], t["title"]))
        parts += ["  %s: %s" % (p["id"], plain(p["text"])) for p in t["points"]]
    for key, title in (("technologies", "Technologies"), ("in_scope", "Topics in scope"), ("out_of_scope", "Topics out of scope")):
        parts += ["", "Section 17, %s:" % title] + ["- " + plain(x) for x in records["section_17"][key]]
    return "\n".join(parts)


def _norm(text):
    """Decision 0037, item 8: ignore capital letters, and treat a hyphen, an
    underscore and a space as the same."""
    return re.sub(r"[-_\s]+", " ", plain(text).lower()).strip()


class FeatureSearch:
    """Decision 0030: "named" means that the name is in the text of the records
    file. Code searches each text of the file, without the backslash of the format."""

    def __init__(self, records):
        texts = []

        def walk(node):
            if isinstance(node, str):
                texts.append(node)
            elif isinstance(node, dict):
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(records)
        self.text = " | ".join(_norm(t) for t in texts)

    def named(self, name):
        n = _norm(name)
        return bool(n) and n in self.text


def finding(rule, detail, letter=None, point=None):
    return {"step": 4, "rule": rule, "detail": detail, "letter": letter, "point": point, "other_questions": []}


class ModelCheck:
    def __init__(self, records, model_call):
        self.records = records
        self.model_call = model_call
        self.features = FeatureSearch(records)
        self.point_ids = {p["id"] for t in records["task_statements"] for p in t["points"]}

    def blind(self, question):
        """Call 4a. Raise CallFailed for an answer that is not valid (decision 0032)."""
        answer, model = self.model_call.ask(SYSTEM_4A, show(question, with_key=False), SCHEMA_4A)
        letters = {o["letter"] for o in question["options"]}
        if not isinstance(answer, dict) or answer.get("status") not in ("answered", "cannot_decide"):
            raise CallFailed("Call 4a: the answer has no valid status.")
        selected = answer.get("selected") or []
        if answer["status"] == "answered":
            if len(selected) != question["select"] or len(set(selected)) != len(selected):
                raise CallFailed("Call 4a: %d letters selected, the line says %d." % (len(selected), question["select"]))
            if any(x not in letters for x in selected):
                raise CallFailed("Call 4a: a selected letter is not an option of the question.")
        return answer, model

    def rules(self, question, slot):
        """Call 4b. Raise CallFailed for an answer that is not valid (decision 0032)."""
        text = "\n".join([guide_text(self.records, slot["scenario"]), "", "THE RULES", RULES_TEXT, "",
                          "THE SLOT: task statement %s, point %s, scenario %d." % (slot["task_statement"], question.get("point", slot["point"]), slot["scenario"]),
                          "", "THE QUESTION, with the marks and the reasons of the writer:", show(question, with_key=True)])
        answer, model = self.model_call.ask(SYSTEM_4B, text, SCHEMA_4B)
        letters = {o["letter"] for o in question["options"]}
        results = answer.get("results") if isinstance(answer, dict) else None
        if not isinstance(results, list) or sorted(r.get("rule") for r in results) != RULES_B:
            raise CallFailed("Call 4b: the answer does not have one result for each rule B1 to B6.")
        for r in results:
            if r.get("result") not in ("pass", "fail", "cannot_decide"):
                raise CallFailed("Call 4b: rule %s has no valid result." % r.get("rule"))
            if r["result"] != "pass" and not (r.get("finding") or "").strip():
                raise CallFailed("Call 4b: rule %s has the result %s and no finding." % (r["rule"], r["result"]))
            if r.get("letter") is not None and r["letter"] not in letters:
                raise CallFailed("Call 4b: rule %s names the letter %s, which the question does not have." % (r["rule"], r["letter"]))
            if r.get("point") is not None and r["point"] not in self.point_ids:
                raise CallFailed("Call 4b: rule %s names the point %s, which does not exist." % (r["rule"], r["point"]))
        if not isinstance(answer.get("features"), list):
            raise CallFailed("Call 4b: the answer has no list of features.")
        return answer, model

    def check(self, question, slot):
        """Return the verdict of step 4 with its fields (decision 0032, part 6)."""
        blind, model_a = self.blind(question)
        check, model_b = self.rules(question, slot)
        marked = sorted(o["letter"] for o in question["options"] if o["correct"])
        found = []
        same = blind["status"] == "answered" and sorted(blind["selected"]) == marked
        if blind["status"] == "answered" and not same:
            found.append(finding("B1", "The blind answer selected %s. The writer marked %s. The reason of the blind answer: %s"
                                 % (", ".join(sorted(blind["selected"])), ", ".join(marked), blind.get("reason", ""))))
        if blind["status"] == "cannot_decide":
            found.append(finding("B1", "The blind answer could not decide: %s" % blind.get("reason", "")))
        for r in check["results"]:
            if r["result"] != "pass":
                found.append(finding(r["rule"], r["finding"], r.get("letter"), r.get("point")))
        features = [{"name": n, "found": self.features.named(n)} for n in check["features"]]
        for f in features:
            if not f["found"]:
                found.append(finding("B6", 'The feature "%s" is not in the exam guide.' % f["name"]))
        results = {r["rule"]: r["result"] for r in check["results"]}
        if (blind["status"] == "answered" and not same) or "fail" in results.values() or any(not f["found"] for f in features):
            verdict = "fail"
        elif blind["status"] == "cannot_decide" or "cannot_decide" in results.values():
            verdict = "cannot_decide"
        else:
            verdict = "pass"
        return {"verdict": verdict, "findings": found,
                "blind_answer": {"status": blind["status"], "selected": blind.get("selected") or [],
                                 "reason": blind.get("reason", ""), "agrees": same},
                "results": check["results"], "features": features,
                "model": model_a if model_a == model_b else "%s, %s" % (model_a, model_b)}
