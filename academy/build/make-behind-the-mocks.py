"""Make tab 2, "Behind the mocks": academy/pages/behind-the-mocks.html and behind-the-mocks.js.

Slice 1 (academy decision 0022): the top of the tab and step 5. The other steps and the build in
Claude Code are closed parts that say which slice brings them.

The facts come from the fact sheets academy/facts/top-of-tab-2.md and academy/facts/step-5.md
(decisions 0011 and 0012). Each number is read from its source file here, and each excerpt of a
preview card is taken from its file (decision 0030). The script stops if a text is not in its file.

Run from the folder ccar-f-mock-generator:
    python3 academy/build/make-behind-the-mocks.py
"""
import glob
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (BRANCH, group_roles, REPO, ROOT, TAG, add_popups, code_block, code_font, e, excerpt, fact, lines_of, link, number, page, read,  # noqa: E402
                 script_file, write)

TAB1 = "exam-guide-breakdown.html"
GUIDE = json.loads(read("reference/guide-records.json"))
POINTS = {p["id"]: (p["text"], t) for t in GUIDE["task_statements"] for p in t["points"]}
TS = {t["id"]: t for t in GUIDE["task_statements"]}

# ----- the files -----

S5 = "docs/build-guide/step-5-try-again.md"
S7 = "docs/build-guide/step-7-the-owner-marks-the-questions.md"
D33 = glob.glob(os.path.join(ROOT, "docs/decisions/0033-*.md"))[0][len(ROOT) + 1:]
D38 = "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md"
D45 = glob.glob(os.path.join(ROOT, "docs/decisions/0045-*.md"))[0][len(ROOT) + 1:]
D66 = glob.glob(os.path.join(ROOT, "docs/decisions/0066-*.md"))[0][len(ROOT) + 1:]
D74 = glob.glob(os.path.join(ROOT, "docs/decisions/0074-*.md"))[0][len(ROOT) + 1:]
CONTROL = "src/control.py"
OWNER5 = "runs/mock-05/owner-decisions.json"

# ----- numbers, read from their source files -----

SLOTS = number("src/step1_plan.py", r"(?m)^QUESTIONS = (\d+)")
TRIES = number(CONTROL, r"(?m)^TRIES = (\d+)")
CANNOT = number(CONTROL, r"(?m)^CANNOT_DECIDE = (\d+)")
STEPS = len(glob.glob(os.path.join(ROOT, "docs/build-guide/step-*.md")))
TESTS = sum(len(re.findall(r"(?m)^\s*def test", read(os.path.relpath(f, ROOT)))) for f in glob.glob(os.path.join(ROOT, "tests/*.py")))
assert STEPS == 9 and SLOTS == 60


def jread(path):
    return json.loads(read(path))


MOCKS = []
for m in range(1, 6):
    folder = "runs/mock-%02d" % m
    qs = [jread(os.path.relpath(p, ROOT)) for p in sorted(glob.glob(os.path.join(ROOT, folder, "questions", "M%d-S*-T*.json" % m)))]
    per = Counter(q["slot_id"] for q in qs)
    verdicts = {}
    for p in glob.glob(os.path.join(ROOT, folder, "checks", "M%d-S*-T*-step[34].json" % m)):
        r = jread(os.path.relpath(p, ROOT))
        verdicts[(r["question_id"], r["step"])] = r["verdict"]
    cannot = sum(1 for v in verdicts.values() if v == "cannot_decide")
    first = sum(1 for sid in per if verdicts.get((sid + "-T1", 3)) == "pass" and verdicts.get((sid + "-T1", 4)) == "pass")
    decisions = jread(folder + "/owner-decisions.json")
    opened = sum(1 for d in decisions if d["action"] in ("more_tries", "new_point"))
    MOCKS.append({"mock": m, "tries": len(qs), "slots": len(per), "per": per, "more": sum(1 for v in per.values() if v > 1),
                  "max": max(per.values()), "first": first, "cannot": cannot, "cannot_write": sum(1 for q in qs if q["status"] == "cannot_write"),
                  "opened": opened})
TOTAL_TRIES = sum(x["tries"] for x in MOCKS)
TOTAL_OPENED = sum(x["opened"] for x in MOCKS)
TOTAL_CANNOT = sum(x["cannot"] + x["cannot_write"] for x in MOCKS)
assert all(x["slots"] == SLOTS for x in MOCKS)
assert TOTAL_CANNOT == 0   # the text says that the guards "cannot decide" and "cannot write" never stopped a slot
REVIEW1 = number(D38, r"The first review found (\d+) serious items")
REVIEW2 = number(D38, r"The second review found (\d+) new serious items")

# M5-S38: the story of decision 0074, from the run files
S38 = {t: jread("runs/mock-05/questions/M5-S38-T%d.json" % t) for t in range(1, 6)}
S38V = {t: jread("runs/mock-05/checks/M5-S38-T%d-step4.json" % t)["verdict"] for t in range(1, 6)}
D004 = next(d for d in jread(OWNER5) if d["id"] == "D004")
assert D004["target"] == "M5-S38" and D004["after_try"] == 3 and D004["action"] == "more_tries"
assert [S38V[t] for t in range(1, 6)] == ["fail", "fail", "fail", "fail", "pass"]
T4A = next(o["text"] for o in S38[4]["options"] if o["letter"] == "A")
T5A = next(o["text"] for o in S38[5]["options"] if o["letter"] == "A")
T4F = jread("runs/mock-05/checks/M5-S38-T4-step4.json")["findings"][0]["detail"]
T2F = jread("runs/mock-05/checks/M5-S38-T2-step4.json")["findings"][0]["detail"]
M1S46 = next(o["text"] for o in jread("runs/mock-01/questions/M1-S46-T1.json")["options"] if o["correct"])

# ----- the preview cards -----


def jexcerpt(path, text, title):
    """An excerpt of a JSON file: the text as it is written in the file."""
    lines_of(path, json.dumps(text, ensure_ascii=False)[1:-1])
    a, b = lines_of(path, json.dumps(text, ensure_ascii=False)[1:-1])
    return {"title": title, "kind": "excerpt", "text": text, "src": "%s, line %d" % (path, a), "href": link(path, a, b)}


CARD = {
    "c-auto": excerpt(D38, "1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5.", "Mock decision 0038, Decision"),
    "c-wait": excerpt(D38, "2. **Each other failure waits for the owner.** A slot that is `open`, a finding of step 6, a bad mark, and a call that fails 3 times. The program does no automatic repair for them.", "Mock decision 0038, Decision"),
    "c-rw": excerpt(D45, "2. **A rewrite with no finding of step 6.** The owner names a question and gives a reason. The writer gets a request of step 5 with that question, and the reason as the finding (rule `owner`).", "Mock decision 0045, Decision"),
    "c-rwp": excerpt(D45, "Then the writer gets a request of step 2 with the new point", "Mock decision 0045, Decision"),
    "c-acc": code_block(CONTROL, "def accept(self", '"""Command of the owner: accept the mock.', "The command accept of the owner"),
    "w-slot": excerpt("docs/build-guide/step-1-plan-the-mock.md", "Before a model writes a question, code makes the plan of the mock: a list of 60 slots. Each slot says what one question must be", "Build guide, step 1"),
    "w-owner": excerpt("HANDOFF.md", "| The owner | The person who directs this work. The owner passed the CCAR-F exam. |", "HANDOFF.md, the words of the project"),
    "w-b9": excerpt(D66, "The question does not have the same problem as an earlier question on the same idea, also in another setting (another tool, team, product or data).", "Mock decision 0066, the text of rule B9"),
    "w-forced": excerpt("docs/sources/2026-10-07-anthropic-docs-define-tools.md", "| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://anthropic.com/glasswing)", "Claude API documentation, Define tools, copy of 7 October 2026 (the live page agreed on 13 October 2026)", kind="docs"),
    "w-guide": excerpt("reference/exam-guide.md", "Using tool_choice forced selection to ensure a specific tool is called first", "Exam guide, task statement 4.3", kind="guide"),
    "c-s6": excerpt("src/step6_check_scenario.py", "Step 6 sends no question\nback. Each finding goes to the owner (decision 0038, part 3).", "The code of step 6", kind="code"),
    "c-s7": excerpt(S7, "For mocks 1 to 3 the reader is the owner. For mocks 4 and 5 it is the second review in Cowork, also a Claude model", "Build guide, step 7"),
    "c-slots": code_block("src/step1_plan.py", "QUESTIONS = ", "QUESTIONS = ", "The number of slots in the code of step 1"),
    "s5-what": excerpt(S5, "A question that fails step 3 or step 4 goes back to the writer. The writer gets the request of step 2, plus the failed question with the letters that the checker saw, and the exact findings.", "Build guide, step 5"),
    "s5-again": excerpt(S5, "The new try goes through steps 3 and 4 again, as a new question.", "Build guide, step 5"),
    "s5-short": excerpt(S5, "The writer does not see older tries, so the request stays short.", "Build guide, step 5"),
    "s5-three": excerpt(D33, "The guide names three parts for a new try: the original, the failed result and the errors (4.4-S1). It does not name the complete history.", "Mock decision 0033, Reason"),
    "s5-pass": excerpt(S5, "The limit is not the main way to stop. The main way to stop is a question that passes.", "Build guide, step 5"),
    "s5-open": excerpt(S5, "A slot that stops is open, and the owner decides: more tries, a new point, or a new plan.", "Build guide, step 5"),
    "s5-file": excerpt(S5, "Each try is a new file. No file is written over, so the history of each question stays.", "Build guide, step 5"),
    "s5-guard": code_block(CONTROL, "TRIES = ", "CANNOT_DECIDE = ", "The two limits in the code"),
    "s5-counts": {"title": "The run records of mocks 1 to 5", "kind": "count",
                  "text": "Tries for %d slots, counted from the question files: %s. Slots with more than one try: %s. "
                          "Times that a slot opened at the limit and waited for the owner: %s. Results \"cannot decide\" and answers "
                          "\"cannot write\": %d in all. The script of this page counted the files."
                          % (SLOTS, ", ".join("mock %d %d" % (x["mock"], x["tries"]) for x in MOCKS),
                             ", ".join(str(x["more"]) for x in MOCKS), ", ".join(str(x["opened"]) for x in MOCKS), TOTAL_CANNOT),
                  "src": "runs/mock-01/ to runs/mock-05/: questions/, checks/ and owner-decisions.json",
                  "href": "%s/tree/%s/runs" % (REPO, TAG)},
    # story (a)
    "a-reviews": excerpt(D38, "The first review found 14 serious items. Decision 0037 answered them. The second review found 10 new serious items, and most of them come from the rules of decision 0037.", "Mock decision 0038, Question"),
    "a-quote": excerpt(D38, "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue.", "Mock decision 0038, How we decided"),
    "a-code": excerpt(D38, "6. **The control is code.** It is one part of the program, with tests that make no model call.", "Mock decision 0038, Decision"),
    "a-limit": excerpt(D38, "A test shows that a case has a path. It does not show that the path is good. The owner decides that.", "Mock decision 0038, Reason"),
    "a-passfirst": code_block(CONTROL, 'if v3["verdict"] == "pass" and v4["verdict"] == "pass":', 'state["status"] = "open" if state["open_reasons"] else "to_write"', "The code: a pass stops the loop first"),
    "a-tests": {"title": "The tests of the program", "kind": "count",
                "text": "The folder tests/ has %d tests (each line that starts with \"def test\"). No test makes a model call. "
                        "The script of this page counted them." % TESTS,
                "src": "tests/", "href": "%s/tree/%s/tests" % (REPO, TAG)},
    # story (b)
    "b-q": excerpt(D74, "The program sent the writer the last failed try and its findings, but not the reason of the owner (decision 0039).", "Mock decision 0074, Question"),
    "b-reason": jexcerpt(OWNER5, D004["reason"], "The decision of the owner on M5-S38"),
    "b-fix": code_block(CONTROL, "# more_tries: the last try before the decision.", "return self._step5(request, last, self._check_findings(last) + owner)", "The fix of decision 0074, in the code that built the 5 mocks", ref=TAG),
    "b-first": code_block(CONTROL, "if in_round:", "return self._step5(request, failed, self._check_findings(failed))", "The branch that runs first: a failed try of this start, in the code that built the 5 mocks", ref=TAG),
    "b-0080": code_block(CONTROL, "# The parts that the event of the owner adds", "self._check_findings(failed) + owner_findings)", "The fix of mock decision 0080: each try of the new start gets the reason"),
    "b-test": code_block("tests/test_control.py", "def test_more_tries_gives_the_reason_of_the_owner_to_the_writer", "def test_more_tries_gives_the_reason_of_the_owner_to_the_writer", "The test of decision 0074"),
    "b-t4": jexcerpt("runs/mock-05/questions/M5-S38-T4.json", T4A, "M5-S38, try 4, option A (correct)"),
    "b-t4f": jexcerpt("runs/mock-05/checks/M5-S38-T4-step4.json", T4F, "M5-S38, try 4, the finding of rule B9"),
    "b-t2f": jexcerpt("runs/mock-05/checks/M5-S38-T2-step4.json", T2F, "M5-S38, try 2, the finding of rule B9"),
    "b-t5": jexcerpt("runs/mock-05/questions/M5-S38-T5.json", T5A, "M5-S38, try 5, option A (correct), in the built mock 5"),
    "b-said": excerpt(D74, "The instruction reached the writer, but the question did not follow it.", "Mock decision 0074, Decision"),
}

# ----- the popups -----


def pts(*ids):
    return [{"id": i, "text": POINTS[i][0], "ctx": "Task statement %s: %s" % (POINTS[i][1]["id"], POINTS[i][1]["title"])} for i in ids]


DEVIATION = ("Claude Opus 5.5, the model of this build, and three other current models (Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1) "
             "reject a forced tool call, so the build sends its form as structured outputs.")
EXAM_43 = ("For the exam: the guide's answer for a fixed form is tool use with a JSON schema (4.3-K1). It names tool_choice \"any\" when several "
           "schemas exist and the document type is unknown (4.3-S2), and a forced tool when one extraction must run first (4.3-S3).")
lines_of("academy/sources/2026-10-14-anthropic-docs-define-tools.md", "| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1]")
FIX_USE = {"5.5-K2": ("For mock 1 the owner reads all 60, so that is not a sample.", "Mocks 1 and 5 put all 60 questions in the file, so that is not a sample. The reader was the owner for mocks 1 to 3 and a Claude model for mocks 4 and 5.")}
lines_of(S5, "The reason: the newest Claude models reject it.")


def table_use(point):
    """How step 5 uses a point, from the table of guide points in the build guide (decision 0024), with its point ID."""
    row = next(l for l in read(S5).split("\n") if l.startswith("| %s |" % point))
    use = row.split(" | ")[-1].rstrip(" |").replace("The same context. ", "")
    return "%s: %s" % (point, use.replace(" (see the deviation above)", ""))


POP = {
    "ts-4-4": {"who": "Task statement 4.4", "cls": "model", "title": TS["4.4"]["title"],
              "sent": ["How step 5 uses each point:", table_use("4.4-K1"), table_use("4.4-S1"), table_use("4.4-K2")],
              "points": pts("4.4-K1", "4.4-S1", "4.4-K2")},
    "ts-1-1": {"who": "Task statement 1.1", "cls": "model", "title": TS["1.1"]["title"],
              "sent": ["How step 5 uses the point:", table_use("1.1-S3")], "points": pts("1.1-S3")},
    "ts-4-3": {"who": "Task statement 4.3", "cls": "model", "title": TS["4.3"]["title"],
              "sent": ["How step 5 uses the point:", table_use("4.3-K1"), "The step names, but does not use:", table_use("4.3-S3"),
                       "Why: " + DEVIATION + " The Claude API documentation, page \"Define tools\", says that a forced tool call returns a 400 error on these models (copy of 14 October 2026 in academy/sources/).",
                       EXAM_43],
              "points": pts("4.3-K1", "4.3-S3")},
}
for k in POP:
    POP[k].setdefault("example", None)
POP = {"step-5-" + k: v for k, v in POP.items()}   # each key starts with its part (decision 0033)

# ----- the figures -----

GL_CODE = "M5 2L0 8l5 6M11 2l5 6-5 6"
GL_CLAUDE = "M8 0v16M0 8h16M2.5 2.5l11 11M13.5 2.5l-11 11"
GL_OWNER = "M8 1a3.2 3.2 0 1 1 0 6.4a3.2 3.2 0 1 1 0-6.4M1.5 16c0-4 3-6 6.5-6s6.5 2 6.5 6"


def box(x, y, w, h, lines, sub=None, cls="", glyph=None, href=None, step=None, card=None, num=None, a=None, s=None):
    """A node: square corners, one or two title lines, an optional sub line. In a stepper, a lights it at those steps,
    and s makes it appear at that step (decision 0037)."""
    attrs = (' data-a="%s"' % a if a else "") + (' data-s="%s"' % s if s else "")
    if step:
        attrs += ' data-step="%s" tabindex="0" role="button" aria-expanded="false"' % step
    if card:
        attrs += ' data-card="%s" tabindex="0" role="button" aria-expanded="false"' % card
    out = '<g class="ve-n %s"%s transform="translate(%d %d)"><rect class="sh" width="%d" height="%d" rx="0"/>' % (cls, attrs, x, y, w, h)
    if glyph:
        out += '<path class="gl" transform="translate(10 10) scale(.85)" d="%s"/>' % glyph
    if num is not None:
        out += '<text class="corner" x="10" y="17">%s</text>' % num
    n = len(lines) + (1 if sub else 0)
    y0 = h / 2 - (n - 1) * 10 + (6 if num is not None else 0)
    for i, t in enumerate(lines):
        out += '<text x="%d" y="%d">%s</text>' % (w / 2, y0 + i * 20, e(t))
    if sub:
        out += '<text class="sub" x="%d" y="%d">%s</text>' % (w / 2, y0 + len(lines) * 20 + 2, e(sub))
    out += "</g>"
    if href:
        out = '<a href="%s">%s</a>' % (href, out)  # the name is the visible text (check F1)
    return out


def edge(d, label=None, lx=0, ly=0, cls="", anchor="", a=None, s=None):
    st = (' data-a="%s"' % a if a else "") + (' data-s="%s"' % s if s else "")
    out = '<path class="ve-e %s"%s%s d="%s"/>' % (cls, st, ' pathLength="1"' if st and "is-async" not in cls else "", d)   # a dashed arrow keeps its dashes
    if label:
        out += '<text class="ve-el %s"%s x="%d" y="%d">%s</text>' % (anchor, st, lx, ly, e(label))
    return out


def phone_bars(rows, aria, mx, note=None):
    """The same bar chart drawn for a phone, with each label above its bar (academy decision 0043, item 3).
    rows: (label, value, hot, text, ghost), where ghost is the value of an outline bar or None."""
    out = ""
    if all(len(r[0]) <= 3 for r in rows):   # short labels, such as B1, stand left of their bars
        for i, (k, v, h, t, g) in enumerate(rows):
            w = max(2, v * 240 / mx)
            out += ('<text x="0" y="%d">%s</text><rect class="%s" x="36" y="%d" width="%d" height="20"/><text class="hv" x="%d" y="%d">%s</text>'
                    % (i * 30 + 14, e(k), "hot" if h else "", i * 30 + 4, w, 44 + w, i * 30 + 14, e(t)))
        return '<div class="frame narrow"><svg class="ve-bars ve-narrow" viewBox="0 0 340 %d" role="img" aria-label="%s">%s</svg></div>' % (len(rows) * 30 + 6, e(aria), out)
    for i, (k, v, h, t, g) in enumerate(rows):
        y = i * 46
        if g:
            out += '<rect class="ghost" x="0" y="%d" width="%d" height="18"/>' % (y + 20, g * 240 / mx)
        w = max(2, v * 240 / mx)
        out += ('<text x="0" y="%d">%s</text><rect class="%s" x="0" y="%d" width="%d" height="18"/><text class="hv" x="%d" y="%d">%s</text>'
                % (y + 10, e(k), "hot" if h else "", y + 20, w, max(w, g * 240 / mx if g else 0) + 8, y + 29, e(t)))
    for j, line in enumerate(note or []):
        out += '<text x="0" y="%d">%s</text>' % (len(rows) * 46 + 12 + j * 20, e(line))
    return '<div class="frame narrow"><svg class="ve-bars ve-narrow" viewBox="0 0 340 %d" role="img" aria-label="%s">%s</svg></div>' % (len(rows) * 46 + 20 * len(note or []) + 4, e(aria), out)


def small_bars(rows, aria, mx=None):
    """A small bar chart for a number in a figure (decision 0037, every number gets a picture). rows: (label, value, hot)."""
    mx = mx or max(v for _, v, _ in rows) or 1
    bars = "".join('<text x="0" y="%d">%s</text><rect class="%s" x="0" y="%d" width="%d" height="18"/><text class="hv" x="%d" y="%d">%d</text>'
                   % (i * 46 + 10, e(k), "hot" if h else "", i * 46 + 20, v * 280 // mx, v * 280 // mx + 8, i * 46 + 29, v)
                   for i, (k, v, h) in enumerate(rows))
    return '<div class="frame"><svg class="ve-bars ve-narrow" viewBox="0 0 340 %d" role="img" aria-label="%s">%s</svg></div>' % (len(rows) * 46, e(aria), bars)


def player(caps):
    """The arrows and captions of a stepper, in the form of Fig. 1.1-1 of tab 1 (decision 0037). caps[0] is the full picture."""
    n = len(caps) - 1
    lis = ['<li data-n="%d steps">%s</li>' % (n, caps[0])] + ['<li data-n="%d/%d">%s</li>' % (i, n, c) for i, c in enumerate(caps[1:], 1)]
    return ('<div class="ve-player"><ol class="ve-cap" aria-live="polite">%s</ol>'
            '<button data-go="-1" aria-label="Previous step">&larr;</button><button data-go="1" aria-label="Next step">&rarr;</button></div>' % "".join(lis))


# Fig. 1: the 9 steps (facts: top-of-tab-2.md, sections 1 and 2)
W, H = 150, 92
# who does the step: the form of the box says it (thin = code, thick = a Claude model, dotted = the owner)
WHO = {0: ("code", ""), 1: ("code", ""), 2: ("Claude", "who-model"), 3: ("code", ""), 4: ("Claude + code", "who-model"),
       5: ("Claude", "who-model"), 6: ("code + Claude", "who-model"), 7: ("owner or Claude", ""), 8: ("code", "")}
WHO_LONG = {0: "code", 1: "code", 2: "a Claude model", 3: "code", 4: "two Claude model calls, then code makes the verdict",
            5: "a Claude model: the writer of step 2 again, with the failed try and its findings", 6: "code and two Claude model calls for each scenario",
            7: "the owner (mocks 1 to 3), or a Claude model (mocks 4 and 5)", 8: "code, after the owner accepts the mock"}
NAMES = {0: ["Prepare the", "guide records"], 1: ["Plan the mock"], 2: ["Write the", "question"], 3: ["Check by code"],
         4: ["Check by", "a model"], 5: ["Try again"], 6: ["Check the", "complete mock"], 7: ["The questions", "are marked"],
         8: ["Build the files"]}
FULL = {0: "Prepare the guide records", 1: "Plan the mock", 2: "Write the question", 3: "Check by code", 4: "Check by a model",
        5: "Try again", 6: "Check the complete mock", 7: "The owner marks the questions", 8: "Build the files"}
for s_, name in FULL.items():   # the names of the build guide (one name for one thing)
    assert ("| %d. %s |" % (s_, name)) in read("docs/build-guide/README.md"), name
FULL[7] = "The questions are marked"   # tab 2 only: a Claude model marked mocks 4 and 5 (academy decision 0034)
POS = {0: (20, 20), 1: (20, 160), 2: (250, 160), 3: (480, 160), 4: (710, 160), 5: (480, 310), 6: (710, 460), 7: (480, 460), 8: (250, 460)}


STEP_A = {0: "1", 1: "2", 2: "3 5", 3: "4", 4: "4", 5: "5 6", 6: "7", 7: "8", 8: "9"}   # the steps of Fig. A that light each box


def step_node(s):
    x, y = POS[s]
    who, cls = WHO[s]
    return box(x, y, W, H, NAMES[s], sub=who, cls=cls, href="#step-%d" % s, num=s, a=STEP_A[s])


LEGEND = ('<g transform="translate(250 22)">'
          '<text class="ve-lab" x="0" y="10">Each box links to its step below.</text>'
          '<g class="ve-n"><rect class="sh" x="0" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="36" y="44">code</text>'
          '<g class="ve-n who-model"><rect class="sh" x="110" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="146" y="44">a Claude model</text>'
          '<g class="ve-n who-owner"><rect class="sh" x="290" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="326" y="44">the owner</text>'
          '<path class="ve-e" d="M0 76H40"/><text class="ve-lab" x="50" y="80">automatic</text>'
          '<path class="ve-e is-async" d="M150 76H190"/><text class="ve-lab" x="200" y="80">a decision of the owner</text>'
          '<path class="ve-e is-hot" d="M420 76H460"/><text class="ve-lab" x="470" y="80">the automatic loop</text></g>')

FIG1 = """
<figure class="ve-steps" data-figure="builder" id="top-fig-a">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 880 570" role="img" aria-label="The 9 steps of the mock builder. Step 0 prepares the guide records once for each version of the exam guide. Step 1 plans 60 slots. Step 2 writes a question, step 3 checks it by code and step 4 by a model. A try that fails goes to step 5 and is checked again. When all 60 slots pass, step 6 checks the complete mock, step 7 marks the questions, and step 8 builds the files after the owner accepts. Dashed arrows are decisions of the owner: more tries or a new point for an open slot, a rewrite after step 6 or after the marks, a bad mark, and accept. A rewrite with a new point goes to step 2.">
      %(edges)s
      <path data-flow="pass" data-every="2000" d="M325 206H785"/><path data-flow="fail" data-every="4400" data-delay="1000" d="M525 206V356H585V206"/>
      <g class="ve-dots" aria-hidden="true"></g>
      %(nodes)s
      <g class="ve-n who-owner" data-a="6"><rect class="sh" x="230" y="310" width="150" height="92" rx="0"/><text x="305" y="344">open slot</text><text class="sub" x="305" y="368">waits for owner</text></g>
      %(legend)s
    </svg>
  </div>
  %(player)s
  <figcaption><span class="fig-n">Fig. A</span>Code moves each try through the steps. %(auto)s. %(wait)s: an open slot, a finding of step 6, a bad mark, and a call that fails 3 times. Since mock decision 0045, %(rw)s also waits for the owner. %(rwp)s The owner %(acc)s before step 8.</figcaption>
  <section class="sources" aria-label="Sources of the top"><p class="ve-label">Sources of the top of this tab</p><ul>@SOURCES_TOP@</ul></section>
</figure>
""" % {
    "nodes": "".join(step_node(s) for s in range(9)),
    "player": player(["The 9 steps of the mock builder. Use the arrow buttons to go through them one at a time. Each box links to its step below.",
                      "Step 0 prepares the guide records, once for each version of the exam guide.",
                      "Step 1 plans %d slots." % SLOTS,
                      "Step 2: a Claude model writes a question for one slot.",
                      "Step 3 checks the try by code, and step 4 by a model. A try that passes both is done.",
                      "A try that fails step 3 or step 4 goes to step 5, where the writer tries again by itself.",
                      "After 3 tries in one start, the slot is open and waits for the owner: more tries or a new point.",
                      "When all %d slots pass, step 6 checks the complete mock." % SLOTS,
                      "Then the questions are marked in step 7. A bad mark or a finding of step 6 can lead to a rewrite, which waits for the owner.",
                      "The owner accepts the mock, and step 8 builds the files."]),
    "legend": LEGEND,
    "edges": "".join([
        edge("M95 112V160", "guide records", 103, 141, anchor="r", s="1"),
        edge("M170 206H250", "%d slots" % SLOTS, 210, 197, s="2"),
        edge("M400 206H480", "question", 440, 197, s="3"),
        edge("M630 206H710", "passes", 670, 197, s="4"),
        edge("M525 252V310", "fails", 517, 286, cls="is-hot", anchor="l", s="5"),
        edge("M760 252V356H630", cls="is-hot", s="5") + '<text class="ve-el l" data-s="5" x="752" y="298">fails or</text><text class="ve-el l" data-s="5" x="752" y="316">cannot decide</text>',
        edge("M585 310V252", "new try", 593, 278, cls="is-hot", anchor="r", s="5"),
        edge("M480 340H380", "3 tries", 430, 331, s="6"),
        edge("M380 380H480", "more tries", 430, 372, cls="is-async", s="6"),
        edge("M305 310V252", "new point", 313, 286, cls="is-async", anchor="r", s="6"),
        edge("M820 252V460", "all %d pass" % SLOTS, 812, 384, anchor="l", s="7"),
        edge("M710 506H630", "then", 670, 497, s="8"),
        edge("M780 460V420H615V402", "rewrite", 700, 411, cls="is-async", s="8"),
        edge("M525 460V402", "bad mark, rewrite", 533, 446, cls="is-async", anchor="r", s="8"),
        edge("M480 506H400", "accepts", 440, 497, cls="is-async", s="9"),
    ]),
    "auto": fact("c-auto", "A try that fails step 3 or step 4 goes to step 5, where the writer of step 2 tries again by itself"),
    "wait": fact("c-wait", "Each other way back waits for a decision of the owner"),
    "rw": fact("c-rw", "a rewrite after the marks"),
    "acc": fact("c-acc", "accepts the mock"),
    "rwp": fact("c-rwp", "The figure draws the new point of an open slot. It does not draw a rewrite with a new point, which also starts again at step 2, or the choice of a new plan."),
}

# Fig. 5-1: the loop of step 5 (facts: step-5.md, sections 2.1 to 2.3)
FIG51 = """
<figure class="ve-steps" id="step-5-fig1">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 400" role="img" aria-label="The writer, a Claude model, writes a try. Step 3 checks it by code and step 4 by a model. A pass stops the loop. A try that fails goes back to the writer with a new request: the request of step 2, the failed try and its findings. After %(t)d failed tries in one start, the slot is open and waits for the owner.">
      %(edges)s
      %(nodes)s
      <g class="ve-dim" data-a="7"><path class="ext" d="M20 300V330M640 300V330"/><path class="ln" d="M20 320H640M16 324l8-8M636 324l8-8"/><text x="330" y="312">at most %(t)d tries in one start</text></g>
      <g class="ve-n who-owner" data-a="7"><rect class="sh" x="20" y="340" width="620" height="44" rx="0"/><text x="330" y="362">after the last failed try: an open slot, the owner decides</text></g>
    </svg>
  </div>
  %(player)s
  <figcaption><span class="fig-n">Fig. 5-1</span>%(pass)s The limit of %(t)d tries is only a guard. %(open)s</figcaption>
</figure>
""" % {
    "t": TRIES,
    "nodes": "".join([
        box(20, 30, 160, 80, ["Writer"], sub="Claude", cls="who-model", a="1 6"),
        box(250, 30, 160, 80, ["Step 3"], sub="check by code", a="2"),
        box(480, 30, 160, 80, ["Step 4"], sub="check by a model", cls="who-model", a="3"),
        box(710, 30, 160, 80, ["passed"], sub="the loop stops", cls="try ok", a="4"),
        box(250, 180, 390, 90, ["new request of step 5"], sub="step 2 + failed try + findings", cls="is-key", a="5"),
    ]),
    "edges": "".join([
        edge("M180 70H250", "a try", 215, 61, s="1"),
        edge("M410 70H480", "passes", 445, 61, s="3"),
        edge("M640 70H710", "passes", 675, 61, s="4"),
        edge("M330 110V180", "fails", 338, 150, cls="is-hot", anchor="r", s="5"),
        edge("M560 110V180", "fails", 568, 150, cls="is-hot", anchor="r", s="5"),
        edge("M250 225H100V110", "tries again", 175, 216, cls="is-hot", s="6"),
        '<path data-flow="pass" data-every="2600" d="M100 70H790"/><path data-flow="retry" data-every="4200" data-delay="1300" d="M100 70H330V225H100V70"/>',
        '<g class="ve-dots" aria-hidden="true"></g>',
    ]),
    "player": player(["The loop of one slot. Use the arrow buttons to go through it one step at a time.",
                      "The writer, a Claude model, writes a try.",
                      "Step 3 checks the try by code.",
                      "If it passes, step 4 checks it by a model.",
                      "A pass of step 4 stops the loop: the slot has passed.",
                      "A try that fails step 3 or step 4 becomes a new request of step 5: the request of step 2, the failed try and its findings.",
                      "The writer tries again with the new request.",
                      "After %d failed tries in one start, the slot is open, and the owner decides." % TRIES]),
    "pass": fact("s5-pass", "A pass stops the loop."),
    "open": fact("s5-open", "A slot that stops is open, and the owner decides: more tries, a new point, or a new plan."),
}


def grid(x):
    cells = []
    for i in range(SLOTS):
        sid = "M%d-S%02d" % (x["mock"], i + 1)
        n = x["per"].get(sid, 0)
        cls = "t1" if n <= 1 else "t2" if n == 2 else "t3" if n == 3 else "t4"
        cx, cy = (i % 10) * 23, (i // 10) * 23
        txt = '<text x="%d" y="%d">%d</text>' % (cx + 10, cy + 10, n) if n > 1 else ""
        cells.append('<g class="cell %s"><rect x="%d" y="%d" width="20" height="20" rx="0"/>%s<title>%s: %d %s</title></g>'
                     % (cls, cx, cy, txt, sid, n, "try" if n == 1 else "tries"))
    return ('<div class="case"><span class="ve-label">Mock %d</span><p class="kpi-n">%d tries</p>'
            '<svg class="ve-grid" viewBox="0 0 227 135" style="overflow:visible" role="img" aria-label="Mock %d: %d tries for %d slots. %d slots passed both checks at the first try. %d slots had more than one try. The most tries for one slot: %d.">%s</svg>'
            '<p class="cap">%d of %d passed both checks at the first try</p></div>'
            % (x["mock"], x["tries"], x["mock"], x["tries"], SLOTS, x["first"], x["more"], x["max"], "".join(cells),
               x["first"], SLOTS))


FIG52 = """
<figure>
  <div class="cases">%s</div>
  <figcaption><span class="fig-n">Fig. 5-2</span>One square for each slot. A darker square had more tries, and its number is the tries. The number also counts new tries after a rewrite or a bad mark. So a slot can pass both checks at the first try and still have a number. %s %s</figcaption>
</figure>
""" % ("".join(grid(x) for x in MOCKS),
       fact("s5-counts", "The 5 mocks needed %d tries for %d questions." % (TOTAL_TRIES, 5 * SLOTS)),
       "In %d cases a slot stopped at the limit of tries and waited for the owner. The limit of %d results &ldquo;cannot decide&rdquo; never stopped a slot."
       % (TOTAL_OPENED, CANNOT))

# Fig. 5-3: the review loop (story a)
FIG53_T = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 150" role="img" aria-label="The first design review found 14 serious items. The second design review found 10 new ones. The fix: one automatic loop, each other failure waits for the owner, and the rules of the next action are code with tests.">
      <path class="ve-e" d="M250 60H318"/><text class="ve-el" x="284" y="51">answers</text>
      <path class="ve-e" d="M560 60H628"/><text class="ve-el" x="594" y="51">fix</text>
      <g class="ve-n"><rect class="sh" x="20" y="20" width="230" height="80" rx="0"/><text x="135" y="44">first design review</text>
        <rect class="bar" x="40" y="62" width="140" height="16" rx="0"/><text class="sub" x="210" y="70">14</text></g>
      <g class="ve-n"><rect class="sh" x="320" y="20" width="240" height="80" rx="0"/><text x="440" y="44">second design review</text>
        <rect class="bar" x="340" y="62" width="100" height="16" rx="0"/><text class="sub r" x="452" y="70">10 new</text></g>
      <g class="ve-n is-key"><rect class="sh" x="630" y="20" width="240" height="80" rx="0"/><text x="750" y="44">the rules are code</text><text class="sub" x="750" y="70">with tests</text></g>
      <text class="ve-lab" x="20" y="130">bar length = number of serious items</text>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 5-3</span>%s The owner said: &ldquo;%s&rdquo;</figcaption>
</figure>
"""
FIG53_T = (FIG53_T.replace('found 14 serious items. The second design review found 10 new', 'found @R1@ serious items. The second design review found @R2@ new')
           .replace('width="140" height="16" rx="0"/><text class="sub" x="210" y="70">14</text>', 'width="%d" height="16" rx="0"/><text class="sub" x="210" y="70">@R1@</text>' % (REVIEW1 * 10))
           .replace('width="100" height="16" rx="0"/><text class="sub r" x="452" y="70">10 new</text>', 'width="%d" height="16" rx="0"/><text class="sub r" x="452" y="70">@R2@ new</text>' % (REVIEW2 * 10))
           .replace("@R1@", str(REVIEW1)).replace("@R2@", str(REVIEW2)))
assert "14" not in FIG53_T.split("<figcaption>")[0].replace("140", "") or REVIEW1 == 14
FIG53 = FIG53_T % (fact("a-reviews", "A first design review found %d serious items. A second design review found %d new ones, and most of them came from the rules that answered the first." % (REVIEW1, REVIEW2)),
       fact("a-quote", "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue."))

# Fig. 5-4: M5-S38 (story b)


def tbox(t, x, lines, sub, cls):
    return box(x, 60, 150, 80, lines, sub=sub, cls="try " + cls, a=str(t))


FIG54 = """
<figure class="ve-steps" id="step-5-fig4">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 250" role="img" aria-label="Question M5-S38 of mock 5. Tries 1 to 3 fail rule B9. The owner gives more tries with a reason. Try 4 gets the reason, puts a custom ID into its correct options and fails rule B9, because it repeats questions of mocks 1 and 3. Try 5 does not get the reason, writes the old problem again and passes.">
      %(edges)s
      %(nodes)s
      <g class="ve-n who-owner" data-a="4"><rect class="sh" x="500" y="2" width="200" height="36" rx="0"/><text x="600" y="20">owner: more tries</text></g>
      <g class="ve-dim" data-a="4"><path class="ext" d="M530 150V190M870 150V190"/><path class="ln" d="M530 180H870M526 184l8-8M866 184l8-8"/><text x="700" y="172">a new start</text></g>
      <text class="ve-lab" data-a="1" x="20" y="230">B9: the question repeats the problem of a question of an earlier mock.</text>
    </svg>
  </div>
  %(player)s
  <figcaption><span class="fig-n">Fig. 5-4</span>The reason of the owner reached try 4, but not try 5. Try 5 is the question in mock 5.</figcaption>
</figure>
""" % {
    "nodes": "".join([tbox(1, 20, ["Try 1"], "fails B9", "bad"), tbox(2, 190, ["Try 2"], "fails B9", "bad"),
                      tbox(3, 360, ["Try 3"], "fails B9", "bad"),
                      box(530, 60, 150, 80, ["Try 4", "custom ID"], sub="fails B9", cls="try bad", card="b-t4", a="5"),
                      box(720, 60, 150, 80, ["Try 5", "no reason"], sub="passes", cls="try ok", card="b-t5", a="6")]),
    "edges": "".join([edge("M170 100H190", s="2"), edge("M340 100H360", s="3"), edge("M510 100H530", s="5"), edge("M680 100H720", s="6"),
                      edge("M600 38V60", "the reason", 608, 52, anchor="r", s="5"),
                      '<path class="chance" data-s="6" d="M700 30H795V60"/><text class="ve-el r" data-s="6" x="803" y="44">not sent</text>']),
    "player": player(["The tries of slot M5-S38. Use the arrow buttons to go through them one at a time.",
                      "Try 1 fails rule B9: it repeats the problem of a question of an earlier mock.",
                      "Try 2 fails B9.",
                      "Try 3 fails B9.",
                      "After 3 failed tries the slot waits for the owner, who gives more tries with a reason. This is a new start.",
                      "Try 4 gets the reason, puts a custom ID into its correct options, and fails B9.",
                      "Try 5 does not get the reason, writes the old problem again, and passes. It is the question in mock 5."]),
}

# ----- the text of step 5 -----

STEP5 = """
<section data-level="overview" aria-label="Overview">
  <p class="lvl1">Overview &middot; 30 seconds</p>
  <h4 class="takeaway">A failed try goes back to the writer with its findings</h4>
  <p>%(what)s %(again)s %(one)s %(pass)s</p>
</section>
<details class="level" data-level="explanation">
  <summary><h4>Explanation</h4><span class="ve-label">3 minutes</span></summary>
  <div class="body">
    %(fig51)s
    <p><b>What the writer gets.</b> The request of step 2, the failed try and its findings. A finding names the rule and, where it fits, the letter of the option. %(short)s The exam guide names the same three parts for a new try: %(three)s</p>
    <p><b>The limits.</b> %(guard)s A start is the first try of a slot, or the first try after a decision of the owner. The other slots continue.</p>
    <p><b>The record.</b> %(file)s</p>
    %(fig52)s
    <p class="gh">The task statements that step 5 uses</p>
    <div class="tslist">%(ts)s</div>
  </div>
</details>
<details class="level" data-level="depth">
  <summary><h4>Depth</h4><span class="ve-label">what went wrong, and the fix</span></summary>
  <div class="body">
    <h4 class="story">The review loop that ended when the rules became code</h4>
    %(fig53)s
    <p>The fix kept %(auto)s Each other failure waits for the owner. %(code)s Now the code that moves each try %(passfirst)s. Today the mock builder has %(tests)s.</p>
    <h4 class="story">The reason of the owner reached only one try</h4>
    <p>Slot M5-S38 failed %(b9)s three times. The owner gave more tries with a reason: &ldquo;%(reason)s&rdquo; %(q)s So mock decision 0074 (a decision record of the build) added the reason to the next request, %(fix)s, and %(test)s checks it.</p>
    %(fig54)s
    <p>The run files and the code show more. Try 4 got the reason and put a custom ID into its correct options: %(t4)s It failed B9, %(t4f)s. Try 2, before the reason, had already tried a custom ID and %(t2f)s. Try 5 did not get the reason. In the code, %(first)s runs before the fix, and the test checks only the first try after the decision. Try 5 wrote the old problem again: %(t5)s It passed, and it is the question in mock 5. Mock decision 0074 says: %(said)s The code shows that only the first try of the new start got the instruction. Mock decision 0080 later changed %(fix80)s: now each try of the new start gets the reason. %(limit)s</p>
    <section class="sources" aria-label="Sources of step 5">
      <p class="ve-label">Sources of step 5. Each underlined fact opens its card.</p>
      <ul>%(sources)s</ul>
    </section>
  </div>
</details>
"""


def ts_chip(key, tsid):
    return ('<div class="tsrow"><span class="chip info" data-step="step-5-%s" tabindex="0" role="button" aria-expanded="false">Task statement %s</span> '
            '<span>%s</span> <a href="%s#ts-%s">Exam guide breakdown %s &rarr;</a></div>'
            % (key, tsid, e(TS[tsid]["title"]), TAB1, tsid.replace(".", "-"), tsid))


STEP5_CARDS = []


def f(card, text):
    STEP5_CARDS.append(card)
    return fact(card, text)


step5_html = STEP5 % {
    "what": f("s5-what", "A try that fails step 3 or step 4 goes back to the writer, with its exact findings."),
    "again": f("s5-again", "The new try goes through steps 3 and 4 again."),
    "pass": f("s5-pass", "A try that passes stops the loop."),
    "one": f("c-auto", "This is the one automatic loop of the mock builder."),
    "fig51": FIG51,
    "short": f("s5-short", "The writer does not see older tries, so the request stays short."),
    "three": f("s5-three", "the original, the failed result and the errors (point 4.4-S1 of the exam guide)."),
    "guard": f("s5-guard", "Each start of a slot has at most %d tries. %d results &ldquo;cannot decide&rdquo; of step 4 also stop it." % (TRIES, CANNOT)),
    "file": f("s5-file", "Each try is a new file. No file is written over, so the history of each question stays."),
    "fig52": FIG52,
    "ts": ts_chip("ts-4-4", "4.4") + ts_chip("ts-1-1", "1.1") + ts_chip("ts-4-3", "4.3"),
    "fig53": FIG53,
    "auto": f("c-auto", "one automatic loop."),
    "code": f("a-code", "The rules of the next action became code, with tests that make no model call."),
    "passfirst": f("a-passfirst", "checks for a pass before the limits"),
    "tests": f("a-tests", "%d tests" % TESTS),
    "reason": f("b-reason", e(D004["reason"])),
    "b9": f("w-b9", "rule B9 of step 4 (a question must not repeat the problem of an earlier question)"),
    "q": f("b-q", "But the mock builder, as it was built, sent the writer only the last failed try and its findings, not the reason."),
    "fix": f("b-fix", "in the code"),
    "test": f("b-test", "a test"),
    "fig54": FIG54,
    "t4": f("b-t4", "&ldquo;Select the files to resubmit by reading the custom_id of each failed result&hellip;&rdquo;"),
    "t4f": f("b-t4f", "because it repeated questions of mock 1 (M1-S46) and mock 3 (M3-S12)"),
    "t2f": f("b-t2f", "failed B9 on the same question of mock 1"),
    "first": f("b-first", "the branch for a failed try of the start"),
    "fix80": f("b-0080", "the code"),
    "t5": f("b-t5", "&ldquo;resubmits every request instead of only the failed ones&rdquo;."),
    "said": f("b-said", "&ldquo;The instruction reached the writer, but the question did not follow it.&rdquo;"),
    "limit": f("a-limit", "A test shows that a case has a path. It does not show that the path is good."),
    "sources": "",
}


def sources(cards):
    seen, items = set(), []
    for c in cards:
        d = CARD[c]
        key = (d["src"], d["href"])
        if key in seen:
            continue
        seen.add(key)
        items.append('<li><a href="%s">%s</a> <span class="ve-label">%s</span></li>' % (e(d["href"]), e(d["title"]), e(d["src"])))
    return "".join(items)


EXTRA5 = ('<li><a href="%s">Build guide, step 5, the table of guide points</a> <span class="ve-label">%s, lines %d to %d</span></li>'
          '<li><a href="%s">The exam guide as records</a> <span class="ve-label">reference/guide-records.json</span></li>'
          % (e(link(S5, *lines_of(S5, "| 4.4-K1 |"))) , S5, lines_of(S5, "| 4.4-K1 |")[0], lines_of(S5, "| 4.3-S3 |")[0],
             e(link("reference/guide-records.json"))))
step5_html = step5_html.replace("<ul></ul>", "<ul>%s%s</ul>" % (sources(list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', step5_html)))), EXTRA5))

# ----- shared helpers for each step -----


def step_file(n):
    return os.path.relpath(glob.glob(os.path.join(ROOT, "docs/build-guide/step-%d-*.md" % n))[0], ROOT)


def table_rows(n):
    """The rows of the table of guide points of a step: (point, how the step uses it) (decision 0024)."""
    out, ctx = [], ""
    for l in read(step_file(n)).split("\n"):
        m = re.match(r"^\| ([1-5]\.[0-9]-[KS][0-9]+) \|", l)
        if m:
            use = l.split(" | ")[-1].rstrip(" |")
            w = re.match(r"(Written for [^.]*\.)", use)
            if w:
                ctx = w.group(1)
            use = use.replace("The same context.", ctx).strip()
            if m.group(1) in FIX_USE:
                use = use.replace(*FIX_USE[m.group(1)])
            out.append((m.group(1), use.replace(" (see the deviation above)", "")))
    return out


def ts_block(n, extra=None):
    """A chip for each task statement of a step, each with its popup, and the links to tab 1."""
    rows, chips = table_rows(n), []
    for tsid in dict.fromkeys(p.split("-")[0] for p, _ in rows):
        key = "step-%d-ts-%s" % (n, tsid.replace(".", "-"))
        mine = [(p, u) for p, u in rows if p.startswith(tsid + "-")]
        used = [(p, u) for p, u in mine if "This build does not use it" not in u]
        unused = [(p, u) for p, u in mine if "This build does not use it" in u]
        POP[key] = {"who": "Task statement " + tsid, "cls": "model", "title": TS[tsid]["title"], "example": None,
                    "sent": ["How step %d uses %s:" % (n, "each point" if len(used) > 1 else "the point")]
                            + ["%s: %s" % (p, u) for p, u in used]
                            + (["The step names, but does not use:"] + ["%s: %s" % (p, u) for p, u in unused] if unused else [])
                            + ((extra or {}).get(tsid) or [])
                            + (["Why: " + DEVIATION, EXAM_43] if any(p in ("4.3-K1", "4.3-S3") for p, _ in mine) else []),
                    "points": pts(*[p for p, _ in mine])}
        chips.append('<div class="tsrow"><span class="chip info" data-step="%s" tabindex="0" role="button" aria-expanded="false">Task statement %s</span> '
                     '<span>%s</span> <a href="%s#ts-%s">Exam guide breakdown %s &rarr;</a></div>'
                     % (key, tsid, e(TS[tsid]["title"]), TAB1, tsid.replace(".", "-"), tsid))
    return '<p class="gh">The task statements that step %d uses</p><div class="tslist">%s</div>' % (n, "".join(chips))


def with_sources(n, html, extra=""):
    cards = list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', html)))
    tab = step_file(n)
    rows = [l for l in read(tab).split("\n") if re.match(r"^\| [1-5]\.[0-9]-[KS][0-9]+ \|", l)]
    if rows:
        a, b = lines_of(tab, rows[0])[0], lines_of(tab, rows[-1])[0]
        extra += ('<li><a href="%s">Build guide, step %d, the table of guide points</a> <span class="ve-label">%s, lines %d to %d</span></li>'
                  % (e(link(tab, a, b)), n, tab, a, b))
    return html.replace("@SOURCES@", sources(cards) + extra)


def level(kind, body, label="what went wrong, and the fix"):
    if kind == "overview":
        return '<section data-level="overview" aria-label="Overview"><p class="lvl1">Overview &middot; 30 seconds</p>%s</section>' % body
    if kind == "explanation":
        return ('<details class="level" data-level="explanation"><summary><h4>Explanation</h4><span class="ve-label">3 minutes</span></summary>'
                '<div class="body">%s</div></details>' % body)
    return ('<details class="level" data-level="depth"><summary><h4>Depth</h4><span class="ve-label">%s</span></summary>'
            '<div class="body">%s<section class="sources" aria-label="Sources of step @N@"><p class="ve-label">Sources of step @N@. '
            'Each underlined fact opens its card.</p><ul>@SOURCES@</ul></section></div></details>' % (label, body))


PART_HTML = {}

# ----- step 0: prepare the guide records (facts: academy/facts/step-0.md) -----

S0 = step_file(0)
D17 = glob.glob(os.path.join(ROOT, "docs/decisions/0017-*.md"))[0][len(ROOT) + 1:]
D28 = glob.glob(os.path.join(ROOT, "docs/decisions/0028-*.md"))[0][len(ROOT) + 1:]
A27 = glob.glob(os.path.join(ROOT, "academy/decisions/0027-*.md"))[0][len(ROOT) + 1:]
REC = GUIDE
N_PTS = sum(len(t["points"]) for t in REC["task_statements"])
N_S17 = sum(len(v) for v in REC["section_17"].values())
assert (len(REC["domains"]), len(REC["scenarios"]), len(REC["task_statements"]), N_PTS, len(REC["sample_questions"])) == (5, 6, 30, 240, 12)
import subprocess  # noqa: E402
_chk = subprocess.run([sys.executable, "-B", os.path.join(ROOT, "src/check_guide_records.py")], capture_output=True, text=True, cwd=ROOT)
CHECKS = re.search(r"(\d+) of (\d+) checks passed", _chk.stdout)
assert CHECKS and CHECKS.group(1) == CHECKS.group(2), _chk.stdout[-300:]
N_CHECKS = int(CHECKS.group(1))
PAGE_MARKS = len(re.findall(r"(?m)^<!-- Page \d+ \|.*-->$", read("reference/exam-guide.md")))
WORDS_PDF = re.search(r"([\d,]+) words in each, and (\d+) places that differ", read(A27))
assert WORDS_PDF and WORDS_PDF.group(2) == "0"

ALL_Q = [q for m in range(1, 6) for g in jread("mocks/mock-%02d.questions.json" % m)["groups"] for q in g["questions"]]
PIDS = {p["id"] for t in REC["task_statements"] for p in t["points"]}
KEPT, TOTAL_Q = sum(1 for q in ALL_Q if q["point"] in PIDS), len(ALL_Q)
assert KEPT == TOTAL_Q
_log = subprocess.run(["git", "-C", ROOT, "log", "--format=%h %ad %s", "--date=short", "--", "reference/guide-records.json"], capture_output=True, text=True).stdout.strip().split("\n")
assert len(_log) == 1 and "2026-10-07" in _log[0], _log
CARD.update({
    "s0-has": excerpt(S0, "The file has the version of the guide, 5 domains with their weights, 6 scenarios with their stories and primary domains, 30 task statements with their 240 points, 12 sample questions, and the three lists of Section 17.", "Build guide, step 0"),
    "s0-pages": excerpt("src/step0_prepare_guide_records.py", "# A page line is a mark of the PDF page. It is not guide text.", "The code of step 0", kind="code"),
    "s0-keep": {"title": "The questions of the 5 mocks", "kind": "count", "text": "%d of %d questions of mocks/mock-01 to mock-05.questions.json have a point that is in the guide records. The script of this page counted them." % (KEPT, TOTAL_Q),
                "src": "mocks/mock-01.questions.json to mock-05.questions.json", "href": "%s/tree/%s/mocks" % (REPO, TAG)},
    "s0-same": {"title": "The history of the records file", "kind": "count", "text": "git log of reference/guide-records.json has one commit: %s. So the file has not changed since the first commit of the repository." % _log[0],
                "src": "git log -- reference/guide-records.json", "href": link("reference/guide-records.json")},
    "s0-what": excerpt(S0, "Before the program plans a mock, a script copies the parts of the exam guide that the later steps need into one file, `reference/guide-records.json` (decision 0028). No model copies text.", "Build guide, step 0"),
    "s0-slice": excerpt(S0, "The file is the one source of guide text for the code. A later step takes a slice of it by ID.", "Build guide, step 0"),
    "s0-once": excerpt(D17, "It runs one time for each version of the guide, not one time for each mock.", "Mock decision 0017, Decision"),
    "s0-ids": excerpt(S0, "Each point gets an ID that the guide does not have: the task statement, then K (knowledge) or S (skill), then the number of the bullet.", "Build guide, step 0"),
    "s0-fail": code_block("src/step0_prepare_guide_records.py", "EXPECTED = ", "EXPECTED = ", "The counts that step 0 expects"),
    "s0-exact": code_block("src/step0_prepare_guide_records.py", 'need(text and text in raw,', 'need(text and text in raw,', "Each text must be exactly in the guide"),
    "s0-check": excerpt("src/check_guide_records.py", "It does not use the code of\nstep 0.", "The second script that checks the file", kind="code"),
    "s0-review": excerpt("docs/reviews/review-guide-records.md", "The reviewer wrote its own script and compared the two files record by record and character by character, in both directions.", "The independent review of the records"),
    "s0-pdf": excerpt(A27, "The result on 13 October 2026: %s words in each, and 0 places that differ." % WORDS_PDF.group(1), "Academy decision 0027"),
    "s0-a1": excerpt(D28, "The assistant showed a proposal for step 2 that said \"the story of the scenario\" and \"a fixed form with fields\".", "Mock decision 0028, How we decided"),
    "s0-a2": excerpt(D28, "The cause: `HANDOFF.md` said to start with step 1, and each step reads the records of step 0.", "Mock decision 0028, How we decided"),
    "s0-a3": excerpt(D28, "Step 0 is designed before step 2. Each design names the exact file format and the exact fields.", "Mock decision 0028, How we decided"),
    "s0-rule": excerpt("WORKING-RULES.md", "for the design of a pipeline step, the assistant shows one proposal with all details of the step. The proposal names the exact file format and the exact fields.", "Working rule 30"),
    "s0-b": excerpt(D17, "The assistant then suggested to call the work an input and not a step. The owner said that it must be documented in each case, because a goal of the build is a record that a portal page can show.", "Mock decision 0017, How we decided"),
})

FIG01 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 300" role="img" aria-label="Step 0. A script reads the copy of the exam guide, leaves out the page headers, gives each point an ID and checks the counts and each text. If a check fails, it writes no file. Otherwise it writes one file of records. A second script, which does not use the code of step 0, checks the file. Later steps take the parts that they need, by ID.">
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 0-1</span>%(cap)s</figcaption>
</figure>""" % {
    "nodes": "".join([
        box(20, 40, 170, 90, ["exam guide"], sub="the copy, .md"),
        box(260, 40, 190, 90, ["script of step 0"], sub="code, no model", cls="is-key"),
        box(520, 40, 170, 90, ["guide records"], sub="one JSON file"),
        box(745, 40, 140, 90, ["steps"], sub="1, 2, 4, 5, 7, 8"),
        box(260, 190, 190, 70, ["no file"], sub="and the cause", cls="try bad"),
        box(520, 190, 170, 70, ["second script"], sub="%d of %d checks" % (N_CHECKS, N_CHECKS), cls="try ok"),
    ]),
    "edges": "".join([
        edge("M190 85H260", "reads", 225, 76),
        edge("M450 85H520", "writes", 485, 76),
        edge("M690 85H745", "parts", 717, 76),
        edge("M355 130V190", "a check fails", 363, 165, anchor="r"),
        edge("M605 190V130", "checks", 613, 165, anchor="r"),
    ]),
    "cap": fact("s0-what", "A script copies the parts of the exam guide that later steps need into one file. No model copies text.")
           + " " + fact("s0-slice", "A later step takes the parts that it needs, by ID."),
}

STEP0 = (level("overview",
               '<h4 class="takeaway">A script copies the exam guide into records, once for each version of the guide</h4>'
               '<p>%s %s %s %s</p>'
               % (fact("s0-what", "Before the first mock, a script copies the parts of the exam guide that the later steps need into one file of records. No model copies text."),
                  fact("s0-once", "It runs once for each version of the guide, not once for each mock."),
                  fact("s0-has", "The file has the %d domains, %d scenarios, %d task statements, %d points and %d sample questions of the guide." % (len(REC["domains"]), len(REC["scenarios"]), len(REC["task_statements"]), N_PTS, len(REC["sample_questions"]))),
                  fact("s0-slice", "A later step takes the parts that it needs from the file, by ID.")))
         + level("explanation",
                 FIG01
                 + '<p><b>Labels.</b> %s So 1.4-K2 is the second &ldquo;Knowledge of&rdquo; bullet of task statement 1.4. %s</p>'
                   % (fact("s0-ids", "Each point gets a label that the guide does not have: the task statement, then K (Knowledge of) or S (Skills in), then the number of the bullet."),
                      fact("s0-keep", "Every question of the 5 mocks keeps the ID of its point: %d of %d." % (KEPT, TOTAL_Q)))
                 + '<p><b>Checks.</b> %s %s and %s, or it writes no file. Then three checks:</p>'
                   '<ol class="checks"><li>%s</li><li>%s</li><li>%s</li></ol>'
                   % (fact("s0-pages", "The script leaves out the %d page headers of the PDF, so that no list is cut in two." % PAGE_MARKS), fact("s0-fail", "It checks the counts"), fact("s0-exact", "that each text is exactly in the guide"),
                      fact("s0-check", "A second script, which does not use the code of step 0, checks the file: %d of %d checks pass." % (N_CHECKS, N_CHECKS)),
                      fact("s0-review", "An independent reviewer wrote its own script, compared the records with the guide record by record, and found no errors."),
                      fact("s0-pdf", "On 13 October 2026, a script compared the copy of the guide with the official PDF, word for word: 0 differences."))
                 + ts_block(0))
         + level("depth",
                 '<h4 class="story">The design started at step 1, and a proposal had no source</h4>'
                 '<p>%s It named no source for the story and no fields of the form. %s The fix: %s %s</p>'
                 '<p>One more correction came earlier. %s So step 0 has a number, a decision and a box in Fig. A.</p>'
                 '<p>No source records a failure of the script or of the file. %s</p>'
                 % (fact("s0-a1", "Early in the design, a proposal for step 2 said &ldquo;the story of the scenario&rdquo; and &ldquo;a fixed form with fields&rdquo;."),
                    fact("s0-a2", "The cause: the plan of work started at step 1, but each step reads the records of step 0."),
                    fact("s0-a3", "step 0 was designed and run before step 2, and each design names the exact file format and fields."),
                    fact("s0-rule", "A rule of the owner has the same words: each design proposal names the exact file format and the exact fields."),
                    fact("s0-b", "The assistant suggested to call this work an input, not a step. The owner said that it must be documented, because a goal of the build is a record that a portal page can show."),
                    fact("s0-same", "The file has not changed since the first commit of the repository, on 7 October 2026.")))
         ).replace("@N@", "0")
PART_HTML[0] = with_sources(0, STEP0)

# ----- step 1: plan the mock (facts: academy/facts/step-1.md) -----

S1 = step_file(1)
D09 = glob.glob(os.path.join(ROOT, "docs/decisions/0009-*.md"))[0][len(ROOT) + 1:]
D47 = glob.glob(os.path.join(ROOT, "docs/decisions/0047-*.md"))[0][len(ROOT) + 1:]
D48 = glob.glob(os.path.join(ROOT, "docs/decisions/0048-*.md"))[0][len(ROOT) + 1:]
D50 = glob.glob(os.path.join(ROOT, "docs/decisions/0050-*.md"))[0][len(ROOT) + 1:]
D56 = glob.glob(os.path.join(ROOT, "docs/decisions/0056-*.md"))[0][len(ROOT) + 1:]
PG = jread("data/point-groups.json")["groups"]
GROUP_OF = {pt: g["id"] for g in PG for pt in g["points"]}
assert len(GROUP_OF) == N_PTS
DOMAIN_COUNTS = re.search(r"(?m)^DOMAIN_COUNTS = \{(.*?)\}", read("src/step1_plan.py")).group(1)
DC = [int(x.split(":")[1]) for x in DOMAIN_COUNTS.split(",")]
SCEN_IN_MOCK = number("src/step1_plan.py", r"(?m)^SCENARIOS_IN_MOCK = (\d+)")
PER_SCEN = number("src/step1_plan.py", r"(?m)^PER_SCENARIO = (\d+)")
MR_PER = number("src/step1_plan.py", r"(?m)^MULTIPLE_RESPONSE_PER_SCENARIO = (\d+)")
assert sum(DC) == SLOTS and SCEN_IN_MOCK * PER_SCEN == SLOTS
SHARED = []          # ideas (groups) with two or more slots in the plan of each mock
for m in range(1, 6):
    c = Counter(GROUP_OF[sl["point"]] for sl in jread("runs/mock-%02d/plan.json" % m)["slots"])
    SHARED.append(sum(1 for v in c.values() if v > 1))
BUILT = {m: [q["point"] for g in jread("mocks/mock-%02d.questions.json" % m)["groups"] for q in g["questions"]] for m in range(1, 6)}
SPREAD = Counter(sum(1 for m in range(1, 6) if any(GROUP_OF[pt] == g["id"] for pt in BUILT[m])) for g in PG)
assert sum(SPREAD.values()) == len(PG)
N_MOCKS = len(glob.glob(os.path.join(ROOT, "mocks/mock-*.questions.json")))
N_TS = len(REC["task_statements"])
SEEDS = number(D48, r"A script ran the rule over (\d+) seeds")
REPEAT2 = re.search(r"(\d+) questions of mock 2 repeat mock 1", read(D56))
SAME7 = re.search(r"(\d+) slots of mock 2 even had the same point as mock 1", read(D56))

CARD.update({
    "s1-what": excerpt(S1, "Before a model writes a question, code makes the plan of the mock: a list of 60 slots. Each slot says what one question must be: the scenario, the task statement, one point of that task statement, the question type, and the number of answers to select. No model works in this step.", "Build guide, step 1"),
    "s1-why": excerpt(S1, "The counts of a mock must hold each time. A model that makes the plan can make an error in a count.", "Build guide, step 1"),
    "s1-known": excerpt(S1, "the work of a mock is known before it starts, so the program can fix the plan before the writing starts", "Build guide, step 1"),
    "s1-counts": code_block("src/step1_plan.py", "QUESTIONS = ", "DOMAIN_COUNTS = ", "The counts of the plan in the code"),
    "s1-twins": excerpt(D47, "most repeats come from two points on one idea", "Mock decision 0047, Reason"),
    "s1-rule": code_block("src/step1_plan.py", "same = point_groups.conflicts(", 'raise PlanError("Two slots are in one group', "The code: no two slots of a plan on one idea"),
    "s1-idea": excerpt(D47, "1. A file that groups the 240 points by idea", "Mock decision 0047, Options"),
    "s1-notq": excerpt(D56, "They do not prevent the same question in two mocks.", "Mock decision 0056, Question"),
    "s1-point": excerpt(D56, "So inside a group, a point that the earlier mocks used less comes first.", "Mock decision 0056, Decision"),
    "s1-groups": excerpt(D47, "3. **The rule of step 1.** No two slots of one mock get points of the same group.", "Mock decision 0047, Decision"),
    "s1-least": excerpt(D50, "Then code moves the points of the least-used groups to the front.", "Mock decision 0050, Decision"),
    "s1-shared": {"title": "The plans of mocks 1 to 5", "kind": "count",
                  "text": "Ideas (groups of points) with two or more slots in the plan: %s for mocks 1 to 5. The script of this page read runs/mock-0N/plan.json and data/point-groups.json." % ", ".join(map(str, SHARED)),
                  "src": "runs/mock-01/plan.json to runs/mock-05/plan.json, data/point-groups.json", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s1-spread": {"title": "The ideas over the 5 built mocks", "kind": "count",
                  "text": "Of the %d ideas (groups of points), %s. The script of this page read mocks/mock-0N.questions.json and data/point-groups.json."
                          % (len(PG), ", ".join("%d %s in %d %s" % (SPREAD[k], "is" if SPREAD[k] == 1 else "are", k, "mock" if k == 1 else "mocks") for k in sorted(SPREAD))),
                  "src": "mocks/mock-01.questions.json to mock-05.questions.json, data/point-groups.json", "href": "%s/tree/%s/mocks" % (REPO, TAG)},
    "s1-review": excerpt(D47, "The plan is code, so code can prevent this before any question is written. A check after the writing (step 6) costs a rewrite, and it compares only one scenario.", "Mock decision 0047, Reason"),
    "s1-never": excerpt(D48, "A script ran the rule over 2000 seeds: each seed failed.", "Mock decision 0048, Question"),
    "s1-cap": excerpt(D48, "So the count must follow the groups, not the groups the count.", "Mock decision 0048, Reason"),
    "s1-bug": excerpt(D48, "The main fix: code gave the extra questions one domain at a time and never went back, so it could stop although a plan existed.", "Mock decision 0048, How we decided"),
    "s1-rep": excerpt(D56, "%s questions of mock 2 repeat mock 1" % REPEAT2.group(1), "Mock decision 0056, Question"),
    "s1-same": excerpt(D56, "%s slots of mock 2 even had the same point as mock 1, although their group had a point that mock 1 did not use." % SAME7.group(1), "Mock decision 0056, Reason"),
    "s1-owner": excerpt(D50, "Is there no simple way to ensure that similar questions are spread out between mocks?", "Mock decision 0050, How we decided"),
})

FIG11 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 330" role="img" aria-label="Step 1. Code reads the guide records, the groups of points (the ideas), the built earlier mocks, a seed, and two fixed lists: the two-answer points and the scenarios of mocks 3 to 5. It applies the rules in order: %(dc)s questions for domains 1 to 5, %(sc)d scenarios of %(ps)d questions, each of the %(nts)d task statements at least once, the least-used ideas of earlier mocks first, no two slots on one idea, and %(mr)d two-answer slots for each scenario. It writes one plan of %(n)d slots. No model works in this step.">
      %(edges)s
      %(nodes)s
      <g class="ve-n is-key"><rect class="sh" x="260" y="20" width="370" height="290" rx="0"/></g>
      <text class="ve-lab" x="276" y="44">code applies the main rules, in this order:</text>
      %(rules)s
    </svg>
  </div>
  %(dbars)s
  <figcaption><span class="fig-n">Fig. 1-1</span>%(cap)s</figcaption>
</figure>""" % {
    "dbars": small_bars([("domain %d" % (i + 1), v, v == max(DC)) for i, v in enumerate(DC)], "Questions of each domain in each plan: %s for domains 1 to 5." % ", ".join(map(str, DC))),
    "dc": ", ".join(map(str, DC)), "nts": N_TS, "sc": SCEN_IN_MOCK, "ps": PER_SCEN, "mr": MR_PER, "n": SLOTS,
    "nodes": "".join([
        box(20, 30, 170, 56, ["guide records"]), box(20, 100, 170, 56, ["ideas"], sub="%d groups of points" % len(PG)),
        box(20, 170, 170, 56, ["earlier mocks"], sub="built only"), box(20, 240, 170, 56, ["a seed"], sub="a number"),
        box(700, 125, 170, 80, ["the plan"], sub="%d slots" % SLOTS),
    ]),
    "edges": "".join([edge("M190 58H260"), edge("M190 128H260"), edge("M190 198H260"), edge("M190 268H260"),
                      edge("M630 165H700", "writes", 665, 156)]),
    "rules": "".join('<text class="ve-lab" x="276" y="%d"><tspan class="pid">%d</tspan> %s</text>' % (76 + i * 38, i + 1, e(t)) for i, t in enumerate([
        "domains 1 to 5: %s questions" % ", ".join(map(str, DC)),
        "%d scenarios, %d questions each" % (SCEN_IN_MOCK, PER_SCEN),
        "each of the %d task statements: 1 or more" % N_TS,
        "the least-used ideas of earlier mocks first",
        "no two slots on one idea",
        "%d two-answer slots in each scenario" % MR_PER,
    ])),
    "cap": fact("s1-what", "Code makes a plan of %d slots before a model writes any question. Each slot says what one question must be. No model works in this step." % SLOTS),
}

FIG12 = """
<figure>
  <div class="cases two">
    <div class="case"><span class="chip info">Dynamic decomposition</span><h3 class="kpi-n">An agent decides the next step</h3>
      <svg class="ve-mini" viewBox="0 0 300 110" role="img" aria-label="In a dynamic decomposition, a model decides the next step from what the work finds.">
        <path class="ve-e" d="M100 55H170"/><text class="ve-el" x="135" y="44">decides</text>
        <g class="ve-n is-st"><rect class="sh" x="2" y="25" width="98" height="60" rx="0"/><text x="51" y="55">Claude</text></g>
        <g class="ve-n"><rect class="sh" x="172" y="25" width="126" height="60" rx="0"/><text x="235" y="47">next step</text><text class="sub" x="235" y="69">from results</text></g></svg></div>
    <div class="case"><span class="chip info">Fixed sequence</span><h3 class="kpi-n">Step 1</h3>
      <svg class="ve-mini" viewBox="0 0 300 110" role="img" aria-label="In the mock builder, code fixes the plan before the writing starts.">
        <path class="ve-e is-st" d="M100 55H170"/><text class="ve-el" x="135" y="44">fixes</text>
        <g class="ve-n is-st"><rect class="sh" x="2" y="25" width="98" height="60" rx="0"/><text x="51" y="55">code</text></g>
        <g class="ve-n"><rect class="sh" x="172" y="25" width="126" height="60" rx="0"/><text x="235" y="47">the plan</text><text class="sub" x="235" y="69">before writing</text></g></svg></div>
  </div>
  <figcaption><span class="fig-n">Fig. 1-2</span>The guide contrasts a fixed sequence with a decomposition that changes with what the work finds (1.6-K1). Step 1 uses one reason of the fixed side: %s.</figcaption>
</figure>""" % fact("s1-known", "the work of a mock is known before it starts")

MAXS = max(SHARED)
FIG13 = """
<figure>
  <div class="frame">
    <svg class="ve-bars" viewBox="0 0 600 %(h)d" role="img" aria-label="Ideas with two or more slots in the plan: %(vals)s for mocks 1 to 5.">%(bars)s</svg>
  </div>
  <figcaption><span class="fig-n">Fig. 1-3</span>%(cap)s</figcaption>
</figure>""" % {
    "h": 5 * 34 + 10, "vals": ", ".join(map(str, SHARED)),
    "bars": "".join('<text x="0" y="%d">Mock %d</text><rect class="%s" x="80" y="%d" width="%d" height="22"/><text class="hv" x="%d" y="%d">%d</text>'
                    % (i * 34 + 16, i + 1, "hot" if v else "", i * 34 + 5, max(2, v * 400 // max(MAXS, 1)), 88 + max(2, v * 400 // max(MAXS, 1)), i * 34 + 16, v)
                    for i, v in enumerate(SHARED)),
    "cap": fact("s1-shared", "Ideas with two or more slots in one plan: %d in mock 1, then %s." % (SHARED[0], " and ".join(sorted(set(map(str, SHARED[1:])))) if len(set(SHARED[1:])) == 1 else ", ".join(map(str, SHARED[1:])))),
}
assert SHARED[1:] == [0, 0, 0, 0]

STEP1 = (level("overview",
               '<h4 class="takeaway">Code plans all %d questions before a model writes one</h4><p>%s %s</p>'
               % (SLOTS, fact("s1-what", "Before a model writes a question, code makes the plan of the mock: a list of %d slots. Each slot says what one question must be: the scenario, the task statement, one point, the question type and the number of answers." % SLOTS),
                  fact("s1-why", "The counts of a mock must hold each time, and a model that makes the plan can make an error in a count.")))
         + level("explanation",
                 FIG11
                 + '<p><b>The counts.</b> %s The weights of the guide give the domain counts. Each slot gets one point of its task statement. %s %s</p>'
                   % (fact("s1-counts", "A mock has %d scenarios of %d questions, and %s questions for domains 1 to 5." % (SCEN_IN_MOCK, PER_SCEN, ", ".join(map(str, DC)))),
                      fact("s1-idea", "An idea is a group of points of the guide on one subject: the build put the %d points into %d ideas." % (N_PTS, len(PG))),
                      fact("s1-groups", "No two slots of one mock get points of the same idea."))
                 + FIG12
                 + ts_block(1))
         + level("depth",
                 '<h4 class="story">Mock 1 repeated itself, so the plan learned the ideas</h4>'
                 + FIG13
                 + '<p>Mock 1 had questions that repeated each other. %s So the build grouped the %d points into %d ideas, and %s %s</p>'
                   % (fact("s1-twins", "Most repeats came from two points of the guide on one idea."), N_PTS, len(PG), fact("s1-rule", "code now stops a plan with two slots on one idea."), fact("s1-review", "The plan is code, so code can prevent this before any question is written."))
                 + '<p>The first version of the rule could never make a plan: %s The fix gave a task statement no more questions than its number of ideas. %s An independent review of that code then found a bug: %s</p>'
                   % (fact("s1-never", "a script ran it over %d seeds, and each seed failed." % SEEDS), fact("s1-cap", "&ldquo;So the count must follow the groups, not the groups the count.&rdquo;"),
                      fact("s1-bug", "the code could stop although a plan existed."))
                 + '<h4 class="story">Mock 2 repeated mock 1</h4>'
                 + '<p>Before mock 2, the owner asked: &ldquo;%s&rdquo; So step 1 reads the built earlier mocks, and %s That spread the ideas, but %s %s Part of the cause was in step 1: %s So now %s Step 2 got the earlier questions on the idea, and step 4 got rule B9. %s</p>'
                   % (fact("s1-owner", "Is there no simple way to ensure that similar questions are spread out between mocks?"),
                      fact("s1-least", "it puts the least-used ideas first."),
                      fact("s1-notq", "it did not prevent the same question in two mocks."),
                      fact("s1-rep", "A second review found that %s questions of mock 2 repeat mock 1." % REPEAT2.group(1)),
                      fact("s1-same", "%s slots of mock 2 had the same point as mock 1, although their idea had a point that mock 1 did not use." % SAME7.group(1)),
                      fact("s1-point", "inside an idea, the point that earlier mocks used less comes first."),
                      fact("s1-spread", "Over the %d built mocks, %d of the %d ideas are in 2 to 4 mocks, and %d are in all %d." % (N_MOCKS, sum(SPREAD[k] for k in (2, 3, 4)), len(PG), SPREAD[5], N_MOCKS))))
         ).replace("@N@", "1")
PART_HTML[1] = with_sources(1, STEP1)

# ----- step 2: write the question (facts: academy/facts/step-2.md) -----

S2 = step_file(2)
D10 = glob.glob(os.path.join(ROOT, "docs/decisions/0010-*.md"))[0][len(ROOT) + 1:]
D29 = glob.glob(os.path.join(ROOT, "docs/decisions/0029-*.md"))[0][len(ROOT) + 1:]
D40 = glob.glob(os.path.join(ROOT, "docs/decisions/0040-*.md"))[0][len(ROOT) + 1:]
D41 = glob.glob(os.path.join(ROOT, "docs/decisions/0041-*.md"))[0][len(ROOT) + 1:]
D43 = glob.glob(os.path.join(ROOT, "docs/decisions/0043-*.md"))[0][len(ROOT) + 1:]
MODELS = Counter(jread(os.path.relpath(f, ROOT))["model"] for f in glob.glob(os.path.join(ROOT, "runs/mock-0*/questions/M*-S*-T*.json")))
assert len(MODELS) == 1
MODEL = list(MODELS)[0]
N_CW = sum(x["cannot_write"] for x in MOCKS)
assert N_CW == 0
N_TECH = len(REC["section_17"]["technologies"])
SAMPLE_A = Counter(q["correct_answer"][0] for q in REC["sample_questions"])
Q_M1 = jread("runs/mock-01/questions/M1-S28-T2.json")
Q_M2A = jread("runs/mock-02/questions/M2-S08-T1.json")
Q_M2B = jread("runs/mock-02/questions/M2-S08-T2.json")
cor = lambda q: next(o["text"] for o in q["options"] if o["correct"])
D2_001 = next(d for d in jread("runs/mock-02/owner-decisions.json") if d["id"] == "D001")

CARD.update({
    "s2-fields": excerpt(S2, "The model fills a form: the question, and each option with a mark (\"correct\" or \"wrong\") and a reason. The model can also answer \"cannot write\", with a reason.", "Build guide, step 2"),
    "s2-what": excerpt(S2, "For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock.", "Build guide, step 2"),
    "s2-why": excerpt(D10, "One call makes one record with one ID, so each later verdict connects to exactly one question. If one question fails, the program writes that one again and the others do not change.", "Mock decision 0010, Reason"),
    "s2-cost": excerpt(D10, "We accepted one disadvantage: a writer that sees one slot does not see the other questions of its scenario.", "Mock decision 0010, How we decided"),
    "s2-model": {"title": "The model of each try", "kind": "count", "text": "All %d question files of mocks 1 to 5 have the model %s. None has the status cannot_write. The script of this page counted them." % (sum(MODELS.values()), MODEL),
                 "src": "runs/mock-0N/questions/", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s2-exam": excerpt("reference/exam-guide.md", "Prompt caching implementation details (beyond knowing it exists)", "Exam guide, appendix (section 17), Out-of-Scope Topics", kind="guide"),
    "s2-cache": code_block("src/step2_write.py", "# Decision 0067: the rules come first as a cached block.", "cached=[rules_for(request)])", "The rules come first, as a cached block"),
    "s2-letters": excerpt(D41, "Code mixes the options with the seed of the plan, the slot ID and the question text. So the same answer always gets the same letters.", "Mock decision 0041, Decision"),
    "s2-plan": excerpt(glob.glob(os.path.join(ROOT, "docs/decisions/0070-*.md"))[0][len(ROOT) + 1:], "2. **Step 2** (and step 5) puts the correct options at the letters of the slot.", "Mock decision 0070, Decision"),
    "s2-samplea": excerpt(D29, "in the 12 sample questions of the guide, the correct answer is A 10 times and B 2 times. A model that sees those examples can copy that. This is an assumption of the assistant. It is not checked.", "Mock decision 0029, Reason"),
    "s2-form": excerpt(D40, "Option 2. Steps 2, 4 and 6 (and step 5, which uses the request of step 2) send their form as a JSON schema in `output_config.format`.", "Mock decision 0040, Decision"),
    "s2-forced": excerpt(D29, "The form is a JSON schema of a tool, and the request forces the model to call that tool.", "Mock decision 0029, Decision"),
    "s2-test": code_block("tests/test_model_steps.py", "def test_the_form_is_sent_as_structured_outputs_with_no_tool", "def test_the_form_is_sent_as_structured_outputs_with_no_tool", "A test: no tool and no forced tool call"),
    "s2-m1": jexcerpt("runs/mock-01/questions/M1-S28-T2.json", cor(Q_M1), "M1-S28, try 2, the correct option (mock 1)"),
    "s2-m2a": jexcerpt("runs/mock-02/questions/M2-S08-T1.json", cor(Q_M2A), "M2-S08, try 1, the correct option (mock 2)"),
    "s2-m2b": jexcerpt("runs/mock-02/questions/M2-S08-T2.json", cor(Q_M2B), "M2-S08, try 2, the correct option (mock 2)"),
    "s2-d001": jexcerpt("runs/mock-02/owner-decisions.json", D2_001["reason"], "The rewrite of the owner, mock 2"),
    "s2-did": excerpt(D56, "In mock 2, the writer did not know mock 1. On a shared idea it wrote the most obvious scene again, often with the same wrong options.", "Mock decision 0056, Reason"),
    "s2-earlier": excerpt(D56, "When the idea of a slot is in an earlier mock, the writer gets the earlier questions on that idea, with the mark of each option", "Mock decision 0056, Decision"),
    "s2-bad": excerpt(D43, "The question is confusing and needs calrification. I had to read the question more than one time. Use one name for the actor, not 'the subagent' and 'Claude'.", "Mock decision 0043, Question"),
    "s2-first": excerpt(D43, "The assistant first recommended an instruction only. The owner asked if that is enough.", "Mock decision 0043, How we decided"),
    "s2-enough": excerpt(D43, "The owner asked: \"but is that enough? Only in the prompt?\" An instruction alone fails sometimes, so a check comes after it.", "Mock decision 0043, Reason"),
    "s2-b7": excerpt(D43, "1. **The instruction to the writer** (step 2, and so also step 5): \"Use one name for one actor. Write each sentence so that a reader understands it at the first reading.\"", "Mock decision 0043, Decision"),
})

REQ = [("cached", "the rules: A1 to A12 and B1 to B9"), ("", "the role and the form"),
       ("", "3 sample questions of the guide"), ("", "the story of the scenario"),
       ("", "the task statement, its point flagged"), ("", "the %d technologies of the guide" % N_TECH),
       ("", "the slot: type, options, answers"), ("if any", "earlier questions on the idea"),
       ("step 5", "the failed try and its findings")]
FIG21 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 %(h)d" role="img" aria-label="Step 2. Code builds one request for one slot: the rules first as a cached block, the role and the form, 3 sample questions of the guide, the story, the task statement with its point marked, the technologies, the slot, the earlier questions on the idea if any, and for step 5 the failed try with its findings. One Claude call answers in the form. Code then mixes the options and gives the letters,">
      <g class="ve-n is-key"><rect class="sh" x="20" y="10" width="380" height="%(rh)d" rx="0"/></g>
      <text class="ve-lab" x="36" y="32">the request, built by code</text>
      %(rows)s
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 2-1</span>%(cap)s</figcaption>
</figure>""" % {
    "h": 60 + len(REQ) * 34 + 20, "rh": 40 + len(REQ) * 34,
    "rows": "".join('<g class="blk%s"><rect x="32" y="%d" width="360" height="28" rx="0"/><text x="42" y="%d">%s%s</text></g>'
                    % (" a" if tag == "cached" else "", 44 + i * 34, 58 + i * 34, ('<tspan class="role">%s: </tspan>' % tag) if tag else "", e(t)) for i, (tag, t) in enumerate(REQ)),
    "edges": "".join([edge("M400 170H480", "sends", 440, 161), edge("M640 170H700", "answers", 670, 161)]),
    "nodes": "".join([box(480, 120, 160, 100, ["Claude"], sub="one new call", cls="who-model"),
                      box(700, 120, 170, 100, ["the form"], sub="question, options", cls=""),
                      box(700, 250, 170, 70, ["code"], sub="mixes, gives letters")]) + edge("M785 220V250"),
    "cap": fact("s2-what", "For each slot, one new Claude call writes one question. It does not know the other questions of the mock."),
}

STEP2 = (level("overview",
               '<h4 class="takeaway">One new Claude call writes each question, from a request that code builds</h4><p>%s %s Code builds the request from the guide records and the plan, and %s</p>'
               % (fact("s2-what", "For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock."),
                  fact("s2-why", "One call makes one record, so each later verdict connects to exactly one question, and a failed try is written again alone."),
                  fact("s2-letters", "code, not the model, mixes the options and gives the letters.")))
         + level("explanation",
                 FIG21
                 + '<p><b>The rules come first.</b> %s Today the writer gets the 21 rules that steps 3 and 4 check, so each of them is also checked. Two other instructions to the writer have no check. %s</p>'
                   % (fact("s2-cache", "From mock 4, the list of rules is a separate first block, cached, so a repeated list costs less (mock decision 0067)."), fact("s2-model", "Each of the %d tries of the 5 mocks used Claude Opus 5.5." % sum(MODELS.values())))
                 + '<div class="callout"><span class="chip">Beyond the exam</span><p>The cached block of rules. %s</p></div>' % fact("s2-exam", "The exam tests only that prompt caching exists.")
                 + '<p><b>The form.</b> %s %s %s</p>'
                   % (fact("s2-fields", "The writer answers in a fixed form: the question, and each option as correct or wrong, with a reason. It can also answer &ldquo;cannot write&rdquo;."),
                      fact("s2-form", DEVIATION), e(EXAM_43))
                 + '<p><b>The letters.</b> %s So %s</p>'
                   % (fact("s2-samplea", "In the %d sample questions of the guide, the correct answer is A %d times and B %d times, and a model can copy that (an assumption, not checked)." % (len(REC["sample_questions"]), SAMPLE_A["A"], SAMPLE_A["B"])),
                      fact("s2-letters", "code mixes the options and gives the letters.") + " " + fact("s2-plan", "The mix alone did not balance the letters (see step 8). From mock 5, the correct options take the letters that the plan sets."))
                 + '<p><b>The cost of one call per slot.</b> %s Step 6 checks the questions of a scenario together.</p>' % fact("s2-cost", "The writer sees one slot, so it cannot see the other questions of its scenario.")
                 + ts_block(2))
         + level("depth",
                 '<h4 class="story">The writer did not know the earlier mocks</h4>'
                 '<p>%s Example on one idea, the stop of an agentic loop:</p>'
                 '<ol class="checks"><li>Mock 1, M1-S28: %s</li><li>Mock 2, M2-S08, try 1: %s</li></ol>'
                 '<p>The owner sent it back: %s The new try asked for the cause instead: %s</p>'
                 '<p>The fix for step 2: %s In the same mock decision, step 4 got rule B9 to check it.</p>'
                 '<h4 class="story">In a test, a bad mark became an instruction and a check</h4>'
                 '<p>In the first test of the writer, the owner marked one question bad: &ldquo;%s&rdquo; %s %s %s because of that question, step 4 got rule B7 to check it.</p>'
                 '<h4 class="story">The design forced a tool call</h4>'
                 '<p>%s Before the code was written, the Claude API documentation showed that the newest models reject it. So %s The code never had a forced tool call, and %s</p>'
                 % (fact("s2-did", "In mock 2, the writer did not know mock 1. On a shared idea it wrote the most obvious scene again, often with the same wrong options."),
                    fact("s2-m1", "the correct answer checks the stop reason and continues while Claude asks for a tool."),
                    fact("s2-m2a", "the correct answer again continues while Claude asks for a tool."),
                    fact("s2-d001", "&ldquo;Use a different scene and a different angle: the cause, the fix, or a choice between rules.&rdquo;"),
                    fact("s2-m2b", "a fixed cap of 12 iterations as the main stopping rule."),
                    fact("s2-earlier", "when the idea of a slot is in an earlier mock, the writer gets the earlier questions on that idea, with the answer key of each."),
                    fact("s2-bad", "The question is confusing and needs calrification. I had to read the question more than one time."),
                    fact("s2-first", "The assistant first suggested an instruction only."),
                    fact("s2-enough", "The owner asked: &ldquo;but is that enough? Only in the prompt?&rdquo;"),
                    fact("s2-b7", "So the writer got the instruction &ldquo;Use one name for one actor&rdquo;, and"),
                    fact("s2-forced", "The first design said that the request forces the model to call a tool."),
                    fact("s2-form", "the build chose structured outputs: a JSON schema in each request."),
                    fact("s2-test", "a test checks that the shared model call sends no tool and no tool choice.")))
         ).replace("@N@", "2")
PART_HTML[2] = with_sources(2, STEP2)

# ----- step 3: check by code (facts: academy/facts/step-3.md) -----

S3 = step_file(3)
D11 = glob.glob(os.path.join(ROOT, "docs/decisions/0011-*.md"))[0][len(ROOT) + 1:]
D53 = glob.glob(os.path.join(ROOT, "docs/decisions/0053-*.md"))[0][len(ROOT) + 1:]
DOC_SO = "docs/sources/2026-10-07-anthropic-docs-structured-outputs.md"
V3, RULE3 = Counter(), Counter()
for f in glob.glob(os.path.join(ROOT, "runs/mock-0*/checks/M*-S*-T*-step3.json")):
    r = jread(os.path.relpath(f, ROOT))
    V3[r["verdict"]] += 1
    if r["verdict"] != "pass":
        for x in r["findings"]:
            RULE3[x["rule"]] += 1
assert sum(V3.values()) == TOTAL_TRIES
FAIL3 = [sum(1 for f in glob.glob(os.path.join(ROOT, "runs/mock-%02d/checks/M*-step3.json" % m)) if jread(os.path.relpath(f, ROOT))["verdict"] != "pass") for m in range(1, 6)]
SIX = []
for m in range(1, 6):
    for f in sorted(glob.glob(os.path.join(ROOT, "runs/mock-%02d/questions/M*.json" % m))):
        q = jread(os.path.relpath(f, ROOT))
        if q.get("options") and len(q["options"]) == 6:
            SIX.append(q["question_id"])
assert SIX == ["M4-S27-T3", "M5-S60-T2"], SIX
LONG = []          # one-answer questions of each built mock whose correct option is the longest (characters)
for m in range(1, 6):
    ans = {a["question_id"]: a["correct"] for a in jread("mocks/mock-%02d.answers.json" % m)["answers"]}
    n = 0
    for g in jread("mocks/mock-%02d.questions.json" % m)["groups"]:
        for q in g["questions"]:
            if q["select"] == 1:
                lens = {o["letter"]: len(o["text"]) for o in q["options"]}
                n += lens[ans[q["question_id"]][0]] == max(lens.values())
    LONG.append(n)
D30 = glob.glob(os.path.join(ROOT, "docs/decisions/0030-*.md"))[0][len(ROOT) + 1:]
T6 = jread("runs/mock-04/questions/M4-S27-T3.json")
CARD.update({
    "s3-what": excerpt("src/step3_check_code.py", "Code checks the rules A1 to A12, which have an exact answer. No model works in\nthis step.", "The code of step 3", kind="code"),
    "s3-cheap": excerpt(D11, "the code check comes before the model check, to save model calls", "Mock decision 0011"),
    "s3-split": excerpt(D30, "code checks a rule that has one correct answer, and a model checks a rule that needs judgment.", "Mock decision 0030"),
    "s3-count": excerpt(D29, "So the design does not rely on the form for a count. The code check of step 3 checks the number of options and the number of correct answers.", "Mock decision 0029, Reason"),
    "s3-docs": excerpt(DOC_SO, "Array constraints beyond `minItems` of 0 or 1", "Claude API documentation, Structured outputs, JSON Schema limitations, not supported (copy of 7 October 2026, the live page agreed on 14 October 2026)", kind="docs"),
    "s3-ask": code_block("src/step2_write.py", '"Write %d options. Mark exactly %d of them correct."', '"Write %d options. Mark exactly %d of them correct."', "What the writer is told"),
    "s3-a2": code_block("src/step3_check_code.py", 'found.append(finding("A2", "The question has %d options.', 'found.append(finding("A2", "The question has %d options.', "Rule A2 in the code"),
    "s3-six": jexcerpt("runs/mock-04/questions/M4-S27-T3.json", next(o["text"] for o in T6["options"] if o["letter"] == "F"), "M4-S27, try 3, option F: the sixth option"),
    "s3-d005": jexcerpt("runs/mock-04/owner-decisions.json", "The last try failed on the form (rules A1 and A2), not on B9.", "The decision of the owner on M4-S27"),
    "s3-runs": {"title": "The step 3 records of mocks 1 to 5", "kind": "count",
                "text": "%d tries have a step 3 record: %d pass, %d fail (per mock %s). The findings of the fails: %s. Two tries had 6 options: %s. The script of this page counted the files."
                        % (sum(V3.values()), V3["pass"], V3["fail"], ", ".join(map(str, FAIL3)), ", ".join("%s %d" % (k, v) for k, v in RULE3.most_common()), " and ".join(SIX)),
                "src": "runs/mock-0N/checks/*-step3.json", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s3-long1": excerpt(D53, "In the built mock 1, the correct option is the longest option (by characters) in 37 of the 52 questions with 1 answer. Chance is 13.", "Mock decision 0053, Question"),
    "s3-gain": excerpt(D53, "a participant who always selects the longest option must not gain from it.", "Mock decision 0053, Reason"),
    "s3-never": excerpt(D53, "2. A rule that the correct option is never the longest. Then a participant learns that the longest option is always wrong.", "Mock decision 0053, Options"),
    "s3-a12": code_block("src/step3_check_code.py", "if right and wrong and max(right) >= max(wrong):", "if right and wrong and max(right) >= max(wrong):", "Rule A12 in the code"),
    "s3-long": {"title": "The longest option in the built mocks", "kind": "count",
                "text": "One-answer questions whose correct option is the longest, by characters: %s for mocks 1 to 5. The script of this page counted mocks/mock-0N.questions.json and answers.json." % ", ".join(map(str, LONG)),
                "src": "mocks/mock-01.questions.json to mock-05.answers.json", "href": "%s/tree/%s/mocks" % (REPO, TAG)},
})
assert LONG[0] == 37

RULES_A = [("A1", "complete form"), ("A2", "options = slot"), ("A3", "correct = slot"), ("A4", "no two the same"),
           ("A5", "no “Option B”"), ("A6", "word limits"), ("A7", "not much longer"), ("A8", "ends with ?"),
           ("A9", "2 to 5 sentences"), ("A10", "1 sentence each"), ("A11", "not negative"), ("A12", "longest option")]
FIG31 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 300" role="img" aria-label="Step 3. Code checks 12 rules with an exact answer, A1 to A12. A try that fails any rule goes to step 5 with the findings and never reaches step 4. A try that passes all 12 goes to step 4. In mocks 1 to 5, %(p)d tries passed and %(f)d failed.">
      <g class="ve-n is-key"><rect class="sh" x="20" y="20" width="600" height="260" rx="0"/></g>
      <text class="ve-lab" x="36" y="42">code checks 12 rules (no model)</text>
      %(cells)s
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  %(pbars)s
  <figcaption><span class="fig-n">Fig. 3-1</span>%(cap)s</figcaption>
</figure>""" % {
    "p": V3["pass"], "f": V3["fail"],
    "pbars": small_bars([("passed step 3", V3["pass"], False), ("failed step 3", V3["fail"], True)], "Tries in mocks 1 to 5: %d passed step 3 and %d failed." % (V3["pass"], V3["fail"])),
    "cells": "".join('<g class="blk"><rect x="%d" y="%d" width="138" height="56" rx="0"/><text x="%d" y="%d"><tspan class="role">%s</tspan></text><text x="%d" y="%d">%s</text></g>'
                     % (36 + (i % 4) * 146, 56 + (i // 4) * 72, 46 + (i % 4) * 146, 72 + (i // 4) * 72, r, 46 + (i % 4) * 146, 94 + (i // 4) * 72, e(t))
                     for i, (r, t) in enumerate(RULES_A)),
    "edges": "".join([edge("M620 100H700", "%d pass" % V3["pass"], 660, 91, cls=""), edge("M620 220H700", "%d fail" % V3["fail"], 660, 211, cls="is-hot")]),
    "nodes": "".join([box(700, 60, 170, 80, ["step 4"], sub="check by a model", cls="who-model"),
                      box(700, 180, 170, 80, ["step 5"], sub="with the findings", cls="try bad")]),
    "cap": fact("s3-what", "Code checks the 12 rules that have one exact answer. No model works in this step.") + " " + fact("s3-cheap", "A try with a simple defect does not use a step 4 model call.") + " Rule A12 came after mock 1.",
}

MAXL = max(LONG)
FIG32 = """
<figure>
  <div class="frame">
    <svg class="ve-bars" viewBox="0 0 600 %(h)d" role="img" aria-label="One-answer questions whose correct option is the longest: %(vals)s of 52 for mocks 1 to 5. Chance is 13.">%(bars)s
      <path class="ve-e is-async" d="M%(cx)d 0V%(ch)d"/><text class="hv" x="%(cxt)d" y="%(ch2)d">chance: 13</text></svg>
  </div>
  <figcaption><span class="fig-n">Fig. 3-2</span>%(cap)s</figcaption>
</figure>""" % {
    "h": 5 * 34 + 30, "vals": ", ".join(map(str, LONG)), "cx": 80 + 13 * 400 // MAXL, "cxt": 84 + 13 * 400 // MAXL, "ch": 5 * 34, "ch2": 5 * 34 + 18,
    "bars": "".join('<text x="0" y="%d">Mock %d</text><rect class="%s" x="80" y="%d" width="%d" height="22"/><text class="hv" x="%d" y="%d">%d</text>'
                    % (i * 34 + 16, i + 1, "hot" if i == 0 else "", i * 34 + 5, v * 400 // MAXL, 540, i * 34 + 16, v) for i, v in enumerate(LONG)),
    "cap": fact("s3-long", "One-answer questions whose correct option is the longest: %d of 52 in mock 1, then %s." % (LONG[0], ", ".join(map(str, LONG[1:])))) + " Chance is 13.",
}

DEPTH3 = ('<h4 class="story">The writer wrote 6 options for a slot of 5</h4>'
          '<p>Twice the writer was told to write 5 options and wrote 6: %s %s The form could not stop it. %s For M5-S60 the writer tried again by itself. M4-S27 had reached its third try, so the slot waited for the owner, who gave more tries: %s</p>'
          % (" and ".join(SIX) + ".", fact("s3-six", "In M4-S27, try 3, the sixth option was F."),
             fact("s3-a2", "Rule A2 failed both tries."),
             fact("s3-d005", "&ldquo;The last try failed on the form (rules A1 and A2), not on B9.&rdquo;"))
          + '<h4 class="story">The longest option was too often correct</h4>' + FIG32
          + '<p>%s Each question passed rule A7, which looks at one question only. The build did not choose a rule that the correct option is never the longest: %s Instead, %s So from mock 2, step 1 lets the longest option be correct on 13 of the 52 one-answer slots and 3 of the 8 two-answer slots, and %s</p>'
          % (fact("s3-long1", "In the built mock 1, the correct option was the longest in 37 of the 52 one-answer questions. Chance is 13."),
             fact("s3-never", "then a participant learns that the longest option is always wrong."),
             fact("s3-gain", "a participant who always selects the longest option must not gain from it."),
             fact("s3-a12", "on each other slot, rule A12 fails a question where a correct option is as long as or longer than each wrong option.")))

STEP3 = (level("overview",
               '<h4 class="takeaway">Code checks 12 exact rules before a model checks the question</h4><p>%s %s %s</p>'
               % (fact("s3-what", "Today code checks each try against 12 rules that have one exact answer, such as the number of options and the length of the text."),
                  fact("s3-cheap", "Code runs before step 4, so a try with a simple defect does not use a step 4 model call."),
                  fact("s3-runs", "In mocks 1 to 5, %d of %d tries passed, and %d failed." % (V3["pass"], sum(V3.values()), V3["fail"]))))
         + level("explanation",
                 FIG31
                 + '<p><b>Code or a model.</b> %s</p>' % fact("s3-split", "Code checks a rule that has one correct answer, and a model checks a rule that needs judgment.")
                 + '<p><b>Why the form does not count.</b> %s %s Later, %s</p>'
                   % (fact("s3-count", "The design never relied on the form of the writer for a count: step 3 counts the options and the correct answers."),
                      fact("s3-ask", "The writer is told the number of options in words only."),
                      fact("s3-docs", "the Claude API documentation showed that a JSON schema for structured outputs cannot limit the number of items in a list, beyond a minimum of 0 or 1."))
                 + '<div class="callout"><span class="chip">Beyond the exam</span><p>The limit of a list in a JSON schema. The exam guide does not name this limit of the API.</p></div>'
                 + ts_block(3))
         + level("depth", DEPTH3)
         ).replace("@N@", "3")
PART_HTML[3] = with_sources(3, STEP3)

# ----- step 4: check by a model (facts: academy/facts/step-4.md) -----

S4 = step_file(4)
D32 = glob.glob(os.path.join(ROOT, "docs/decisions/0032-*.md"))[0][len(ROOT) + 1:]
D67 = glob.glob(os.path.join(ROOT, "docs/decisions/0067-*.md"))[0][len(ROOT) + 1:]
PRICE_IN = float(re.search(r'PRICE = \{"input": ([\d.]+)', read("src/model_call.py")).group(1))
PRICE_OUT = float(re.search(r'"output": ([\d.]+)\}', read("src/model_call.py")).group(1))
V4, RULE4, BLIND_OFF = Counter(), Counter(), 0
for f in glob.glob(os.path.join(ROOT, "runs/mock-0*/checks/M*-S*-T*-step4.json")):
    r = jread(os.path.relpath(f, ROOT))
    V4[r["verdict"]] += 1
    for x in r["findings"]:
        RULE4[x["rule"]] += 1
    b = r.get("blind_answer") or {}
    marked = sorted(o["letter"] for o in jread(os.path.relpath(f, ROOT).replace("/checks/", "/questions/").replace("-step4.json", ".json"))["options"] if o["correct"])
    if b.get("status") != "answered" or sorted(b.get("selected", [])) != marked:
        BLIND_OFF += 1
assert BLIND_OFF == 0 and V4["cannot_decide"] == 0


def dollars(usages, cached=True):
    i = sum(u["input_tokens"] for u in usages); o = sum(u["output_tokens"] for u in usages)
    w = sum(u.get("cache_write_tokens", 0) for u in usages); r = sum(u.get("cache_read_tokens", 0) for u in usages)
    return (i + w + r) * PRICE_IN / 1e6 + o * PRICE_OUT / 1e6


COST = []
for m in range(1, 6):
    us = [jread(os.path.relpath(f, ROOT)) for f in sorted(glob.glob(os.path.join(ROOT, "runs/mock-%02d/usage/*.json" % m)))]
    COST.append((round(sum(u["dollars"] for u in us), 2), round(dollars(us), 2), sum(u.get("cache_read_tokens", 0) for u in us) > 0))
TC = jread("runs/test-cache/results.json")["cost"]
T24 = jread("runs/test-0024/part2.json")
TC_WITH, TC_WITHOUT = TC["dollars"], round(dollars([TC]), 2)

CARD.update({
    "s4-what": excerpt(S4, "Some rules need judgment, so a model checks them. The step has two calls, and code sits between them.", "Build guide, step 4"),
    "s4-calls": excerpt("src/step4_check_model.py", "Call 4a answers the question with no marks and no reasons. Call 4b checks the\nrules B1 to B9", "The code of step 4", kind="code"),
    "s4-verdict": excerpt("src/step4_check_model.py", "Code checks each\nanswer, searches the feature names in the records file, and makes the verdict.\nA model does not make the verdict.", "The code of step 4", kind="code"),
    "s4-first": excerpt(S4, "Two calls with code between them make sure that the blind answer always comes first.", "Build guide, step 4"),
    "s4-order": excerpt(D32, "The guide says that prompt instructions alone have a non-zero failure rate (1.4-K2, in decision 0009).", "Mock decision 0032, Reason"),
    "s4-b6": code_block("src/step4_check_model.py", 'features = [{"name": n, "found": self.features.named(n)}', 'found.append(finding("B6", \'The feature', "Rule B6: code searches each feature name"),
    "s4-runs": {"title": "The step 4 records of mocks 1 to 5", "kind": "count",
                "text": "%d checks: %d pass, %d fail, %d cannot decide. Findings per rule: %s. Call 4a selected other letters than the answer key, or could not decide, in %d of the %d checks. Both B1 findings came from call 4b. The script of this page counted the files."
                        % (sum(V4.values()), V4["pass"], V4["fail"], V4["cannot_decide"], ", ".join("%s %d" % kv for kv in RULE4.most_common()), BLIND_OFF, sum(V4.values())),
                "src": "runs/mock-0N/checks/*-step4.json", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s4-none": excerpt(D67, "The program did not use prompt caching. Each check call sent the full text of the guide again, at the full input price.", "Mock decision 0067, Question"),
    "s4-asked": excerpt(D67, "The owner asked if the program uses prompt caching. The assistant said no", "Mock decision 0067, How we decided"),
    "s4-batch": excerpt(D67, "2. The Message Batches API. The owner rejected it: the rounds of the pipeline would wait for each batch.", "Mock decision 0067, Options"),
    "s4-test": excerpt(D67, "The calls cost $0.58 with caching. The same tokens with no caching cost $1.72.", "Mock decision 0067"),
    "s4-cache": code_block("src/model_call.py", "# Decision 0067, page \"Prompt caching\"", "CACHE_READ = ", "The cache prices in the code (read on 9 October 2026)"),
    "s4-cost": {"title": "The cost of each mock", "kind": "count",
                "text": "Dollars per mock from runs/mock-0N/usage/: %s. The same tokens with no cache, at the prices of src/model_call.py: %s. The usage files do not split the cost by step. The script of this page computed it."
                        % (", ".join("%.2f" % c[0] for c in COST), ", ".join("%.2f" % c[1] for c in COST)),
                "src": "runs/mock-0N/usage/, src/model_call.py", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s4-46": excerpt("reference/exam-guide.md", "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking", "Exam guide, 4.6-K2", kind="guide"),
    "s4-blocking": excerpt("reference/exam-guide.md", "inappropriate for blocking workflows (pre-merge checks)", "Exam guide, 4.5-K2", kind="guide"),
    "s4-write": excerpt("academy/sources/2026-10-14-anthropic-docs-prompt-caching.md", "5-minute cache write tokens are 1.25 times the base input tokens price", "Claude API documentation, Prompt caching (copy of 14 October 2026)", kind="docs"),
    "s4-read": excerpt("academy/sources/2026-10-14-anthropic-docs-prompt-caching.md", "Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are priced at 0.05x the base input price.", "Claude API documentation, Prompt caching (copy of 14 October 2026)", kind="docs"),
    "s4-changed": excerpt(D67, "The same 2 questions, checked once more with no cache and the guide in the user text, both passed.", "Mock decision 0067"),
    "s4-limit": excerpt(D32, "A limit: only call 4a is blind.", "Mock decision 0032, Reason"),
    "s4-one": excerpt(D32, "The test of call 4a covers questions with one answer only, because all 12 sample questions have one answer.", "Mock decision 0032"),
    "s4-compare": excerpt(S4, "Code compares its letters with the marks of the writer.", "Build guide, step 4"),
    "s4-batches": excerpt("reference/exam-guide.md", "The Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed latency SLA", "Exam guide, 4.5-K1", kind="guide"),
    "s4-t24": {"title": "The test before mock 1", "kind": "count", "text": "runs/test-0024/part2.json: call 4a answered %d of %d sample questions of the guide right." % (T24["right"], T24["of"]),
               "src": "runs/test-0024/part2.json", "href": link("runs/test-0024/part2.json")},
    "s4-exam": excerpt("reference/exam-guide.md", "Prompt caching implementation details (beyond knowing it exists)", "Exam guide, appendix (section 17), Out-of-Scope Topics", kind="guide"),
})
assert COST[3][2] and COST[4][2] and not any(c[2] for c in COST[:3])

FIG41 = """
<figure class="ve-steps" id="step-4-fig1">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 300" role="img" aria-label="Step 4. Call 4a, a new Claude call, answers the question with no answer key. Then call 4b checks the 9 rules B1 to B9 with the answer key. Code compares the letters, searches the feature names in the guide records, and makes the verdict: on a pass the slot has passed, and a fail or cannot decide goes to step 5.">
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  %(player)s
  <figcaption><span class="fig-n">Fig. 4-1</span>%(cap)s</figcaption>
</figure>""" % {
    "nodes": "".join([box(20, 110, 150, 80, ["question"], sub="passed step 3", a="1"),
                      box(240, 30, 180, 90, ["call 4a"], sub="no answer key", cls="who-model", a="2"),
                      box(240, 180, 180, 90, ["call 4b"], sub="9 rules, the key", cls="who-model", a="3"),
                      box(500, 105, 160, 90, ["code"], sub="makes the verdict", cls="is-key", a="4"),
                      box(730, 30, 140, 80, ["pass"], sub="slot passed", cls="try ok", a="5"),
                      box(730, 190, 140, 80, ["fail or", "cannot decide"], sub="to step 5", cls="try bad", a="5")]),
    "edges": "".join([edge("M170 150H205V75H240", s="2"), edge("M330 120V180", "then", 338, 155, anchor="r", s="3"),
                      edge("M420 75H460V135H500", "letters", 470, 66, anchor="r", s="4"), edge("M420 225H460V165H500", "results", 470, 250, anchor="r", s="4"),
                      edge("M660 135H695V70H730", s="5"), edge("M660 165H695V230H730", s="5")]),
    "player": player(["The two calls of step 4 and the verdict of code. Use the arrow buttons to go through them one step at a time.",
                      "The question has passed step 3.",
                      "Call 4a, a new Claude call, answers the question with no answer key.",
                      "Then call 4b checks the 9 rules B1 to B9 with the answer key.",
                      "Code compares the letters, searches the feature names in the guide records, and makes the verdict.",
                      "On a pass, the slot has passed. A fail or &ldquo;cannot decide&rdquo; goes to step 5."]),
    "cap": fact("s4-what", "Some rules need judgment, so a model checks them, in two calls.") + " " + fact("s4-verdict", "Code checks the answer of each call and makes the verdict. A model does not make the verdict."),
}

R4 = [(k, RULE4.get(k, 0)) for k in ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9")]
MX4 = max(v for _, v in R4)
FIG42 = """
<figure>
  <div class="frame has-narrow">
    <svg class="ve-bars" viewBox="0 0 600 %(h)d" role="img" aria-label="Findings of step 4 per rule in mocks 1 to 5: %(vals)s.">%(bars)s</svg>
  </div>
  %(phone)s
  %(pbars)s
  <figcaption><span class="fig-n">Fig. 4-2</span>%(cap)s</figcaption>
</figure>""" % {
    "h": len(R4) * 30 + 6, "vals": ", ".join("%s %d" % kv for kv in R4),
    "phone": phone_bars([(k, v, v == MX4, str(v), None) for k, v in R4], "Findings of step 4 per rule in mocks 1 to 5: %s." % ", ".join("%s %d" % kv for kv in R4), MX4),
    "pbars": small_bars([("passed step 4", V4["pass"], False), ("failed step 4", V4["fail"], True)], "Checks of step 4 in mocks 1 to 5: %d passed and %d failed." % (V4["pass"], V4["fail"])),
    "bars": "".join('<text x="0" y="%d">%s</text><rect class="%s" x="60" y="%d" width="%d" height="20"/><text class="hv" x="%d" y="%d">%d</text>'
                    % (i * 30 + 14, k, "hot" if v == MX4 else "", i * 30 + 4, max(2, v * 440 // MX4), 70 + max(2, v * 440 // MX4), i * 30 + 14, v) for i, (k, v) in enumerate(R4)),
    "cap": fact("s4-runs", "In mocks 1 to 5, step 4 made %d checks: %d passed and %d failed. Most findings were rule B9, a repeat of an earlier question." % (sum(V4.values()), V4["pass"], V4["fail"])) + " Mock 1 had rules B1 to B7. B8 and B9 came during mock 2.",
}

MXC = max(c[1] for c in COST)
FIG43 = """
<figure>
  <div class="frame has-narrow">
    <svg class="ve-bars" viewBox="0 0 760 %(h)d" role="img" aria-label="Dollars per mock: %(vals)s. Mocks 4 and 5 used prompt caching. Without the cache, the same tokens would cost %(w4).2f and %(w5).2f dollars.">%(bars)s
      <text x="0" y="%(ly)d">dark: paid. outline: the same tokens with no cache</text></svg>
  </div>
  %(phone)s
  <figcaption><span class="fig-n">Fig. 4-3</span>%(cap)s</figcaption>
</figure>""" % {
    "h": 5 * 34 + 30, "ly": 5 * 34 + 20, "vals": ", ".join("mock %d %.2f" % (i + 1, c[0]) for i, c in enumerate(COST)), "w4": COST[3][1], "w5": COST[4][1],
    "phone": phone_bars([("Mock %d%s" % (i + 1, (", no cache: $%.2f" % c[1]) if c[2] else ""), c[0], c[2], "$%.2f" % c[0], c[1] if c[2] else None) for i, c in enumerate(COST)],
                        "Dollars per mock: %s. Mocks 4 and 5 used prompt caching. Without the cache, the same tokens would cost %.2f and %.2f dollars. The outline bar shows the cost with no cache."
                        % (", ".join("mock %d %.2f" % (i + 1, c[0]) for i, c in enumerate(COST)), COST[3][1], COST[4][1]), MXC, ["dark: paid.", "outline: the same tokens with no cache"]),
    "bars": "".join('<text x="0" y="%d">Mock %d</text><rect class="ghost" x="80" y="%d" width="%d" height="22"/><rect class="%s" x="80" y="%d" width="%d" height="22"/><text class="hv" x="%d" y="%d">$%.2f%s</text>'
                    % (i * 34 + 16, i + 1, i * 34 + 5, c[1] * 400 / MXC, "hot" if c[2] else "", i * 34 + 5, c[0] * 400 / MXC, 88 + c[1] * 400 / MXC, i * 34 + 16, c[0],
                       (" (no cache: $%.2f)" % c[1]) if c[2] else "") for i, c in enumerate(COST)),
    "cap": fact("s4-cost", "The cost of each whole mock (all steps). Mocks 1 to 3 paid the full input price for the same guide text in each call. Mocks 4 and 5 used prompt caching and cost about half."),
}

DEPTH4 = ('<div class="callout"><span class="chip">Beyond the exam</span><p>%s</p>' % fact("s4-exam", "The exam tests only that prompt caching exists.")
          + '<h4 class="story">Prompt caching was missed, and added before mock 4</h4>' + FIG43
          + '<p>%s Before mock 4, %s The fix puts the guide first, the same in each call, and caches it. %s %s %s %s 2 of the 10 verdicts changed from pass to fail. %s The owner did not choose the Message Batches API: %s</p>'
          % (fact("s4-none", "The first design did not use prompt caching. Each check call sent the full text of the guide again, at the full input price."),
             fact("s4-asked", "the owner asked if the program uses prompt caching. The assistant said no."),
             fact("s4-write", "A 5-minute cache write costs 1.25 times the input price."),
             fact("s4-read", "On Claude Opus 5.5, a read from the cache costs 0.05 times the input price."),
             fact("s4-test", "A test on 10 questions cost $%.2f with caching." % TC_WITH),
             fact("s4-cache", "The same tokens would cost $%.2f with no cache, at the prices in the code." % TC_WITHOUT),
             fact("s4-changed", "A check of those 2 with no cache passed both, and the cause was not separated."),
             fact("s4-batch", "the rounds of the mock builder would wait for each batch."))
          + '</div><p>In the exam: the guide teaches the Message Batches API to save cost (%s), and says that batch processing is %s.</p>' % (fact("s4-batches", "4.5-K1"), fact("s4-blocking", "inappropriate for blocking workflows"))
          + '<h4 class="story">The blind answer never caught a question</h4>'
          + '<p>%s %s %s</p>'
          % (fact("s4-runs", "In the %d checks of mocks 1 to 5, call 4a never selected other letters than the answer key, and never said &ldquo;cannot decide&rdquo;. Both B1 findings came from call 4b." % sum(V4.values())),
             fact("s4-t24", "Before mock 1, a test gave call 4a the %d sample questions of the guide, and it answered %d of %d right." % (T24["of"], T24["right"], T24["of"])),
             fact("s4-one", "All of them have one correct answer, so the test did not cover two-answer questions.")))

STEP4 = (level("overview",
               '<h4 class="takeaway">Two new Claude calls: one answers blind, one checks 9 rules, and code decides</h4><p>%s %s %s</p>'
               % (fact("s4-calls", "Call 4a answers the question with no answer key. Today call 4b checks the 9 rules B1 to B9 with the key."),
                  fact("s4-compare", "Code compares the letters of call 4a with the answer key.") + " " + fact("s4-verdict", "Code also searches the feature names in the guide records, and makes the verdict. A model does not make the verdict."),
                  fact("s4-runs", "In mocks 1 to 5, %d of %d checks passed." % (V4["pass"], sum(V4.values())))))
         + level("explanation",
                 FIG41
                 + '<p><b>Why two calls.</b> %s %s So code enforces the order, not an instruction.</p>'
                   % (fact("s4-first", "Two calls with code between them make sure that the blind answer always comes first."), fact("s4-order", "The guide says that prompt instructions alone have a non-zero failure rate (1.4-K2)."))
                 + '<p><b>Why a new call.</b> The checker is a new call, not the writer. %s %s</p>' % (fact("s4-46", "The guide says that review instances without prior reasoning context catch more than self-review (4.6-K2)."), fact("s4-limit", "A limit: only call 4a is blind. Call 4b gets the reasons that the writer gave."))
                 + '<p><b>A rule in code.</b> %s</p>' % fact("s4-b6", "For rule B6, the model lists each feature name, and code searches it in the guide records. A name that is not there fails the question.")
                 + FIG42 + ts_block(4))
         + level("depth", DEPTH4)
         ).replace("@N@", "4")
PART_HTML[4] = with_sources(4, STEP4)

# ----- step 6: check the complete mock (facts: academy/facts/step-6.md) -----

S6 = step_file(6)
D06 = glob.glob(os.path.join(ROOT, "docs/decisions/0006-*.md"))[0][len(ROOT) + 1:]
D34 = glob.glob(os.path.join(ROOT, "docs/decisions/0034-*.md"))[0][len(ROOT) + 1:]
RUNS6, RULE6, N6 = Counter(), Counter(), 0
for f in glob.glob(os.path.join(ROOT, "runs/mock-0*/checks/M*-scenario-*-step6-run*.json")):
    r = jread(os.path.relpath(f, ROOT))
    RUNS6[r["mock"]] += 1
    for x in r["findings"]:
        RULE6[x["rule"]] += 1
        N6 += 1
RW6 = [d for m in range(1, 6) for d in jread("runs/mock-%02d/owner-decisions.json" % m) if d["action"] == "rewrite" and "-SC" in d["target"]]
S41 = {t: jread("runs/mock-02/questions/M2-S41-T%d.json" % t) for t in (1, 2)}
D2_014 = next(d for d in jread("runs/mock-02/owner-decisions.json") if d["id"] == "D014")
assert D2_014["target"] == "M2-SC5-R1-F6" and D2_014["action"] == "rewrite"
opt = lambda q, l: next(o["text"] for o in q["options"] if o["letter"] == l)

CARD.update({
    "s6-what": excerpt(S6, "Steps 3 and 4 look at one question. Some defects show only when many questions are read together.", "Build guide, step 6"),
    "s6-why": excerpt(S6, "Each writer call sees only its own slot, so two calls can write the same scene.", "Build guide, step 6"),
    "s6-calls": excerpt("src/step6_check_scenario.py", "Then two model calls read the 15 questions together: call\n6a (rules D1 and D4) and call 6b (rules D2 and D3).", "The code of step 6", kind="code"),
    "s6-back": excerpt("src/step6_check_scenario.py", "Step 6 sends no question\nback. Each finding goes to the owner (decision 0038, part 3).", "The code of step 6", kind="code"),
    "s6-rules": code_block("src/step6_check_scenario.py", 'RULES_6A = """D1.', "D3. At most one wrong option of the scenario", "The rules of calls 6a and 6b"),
    "s6-person": excerpt(D34, "A finding of this step names two questions or more, so a person selects which one to write again, or none.", "Mock decision 0034, Reason"),
    "s6-rule": excerpt(S6, "A finding of rule D4, a question that gives away the answer of another, is ignored. A finding of rule D2 or D3, one wrong idea in too many questions, is recorded as a known limit of the mock.", "Build guide, step 6"),
    "s6-runs": {"title": "The step 6 records of mocks 1 to 5", "kind": "count",
                "text": "%d runs of step 6 (%s for mocks 1 to 5) with %d findings: %s. The owner rewrote a question for %d findings. The script of this page counted the files."
                        % (sum(RUNS6.values()), ", ".join(str(RUNS6[m]) for m in range(1, 6)), N6, ", ".join("%s %d" % kv for kv in sorted(RULE6.items())), len(RW6)),
                "src": "runs/mock-0N/checks/*-step6-run*.json, runs/mock-0N/owner-decisions.json", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s6-r2": excerpt(D06, "In one scenario of one mock, at most one wrong option is the self-reported-confidence option. That option is: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger.", "Mock decision 0006, Decision"),
    "s6-r2why": excerpt(D06, "The plain reason for the limit of one: if the option appears many times, a participant can mark it wrong without thought.", "Mock decision 0006, Reason"),
    "s6-52k3": excerpt(D06, "The guide says that self-reported confidence scores are \"unreliable proxies for actual case complexity\" (5.2-K3)", "Mock decision 0006, Reason"),
    "s6-b": jexcerpt("runs/mock-02/questions/M2-S41-T1.json", opt(S41[1], "B"), "M2-S41, try 1, option B"),
    "s6-c": jexcerpt("runs/mock-02/questions/M2-S41-T1.json", opt(S41[1], "C"), "M2-S41, try 1, option C"),
    "s6-f6": {"title": "The finding of call 6b, mock 2, scenario 5", "kind": "excerpt", "text": "Finding M2-SC5-R1-F6, rule D3, names M2-S41-T1.",
              "src": "runs/mock-02/checks/M2-scenario-5-step6-run1.json, line %d" % lines_of("runs/mock-02/checks/M2-scenario-5-step6-run1.json", '"id": "M2-SC5-R1-F6"')[0],
              "href": link("runs/mock-02/checks/M2-scenario-5-step6-run1.json", lines_of("runs/mock-02/checks/M2-scenario-5-step6-run1.json", '"id": "M2-SC5-R1-F6"')[0])},
    "s6-t2": jexcerpt("runs/mock-02/questions/M2-S41-T2.json", opt(S41[2], "B"), "M2-S41, try 2, option B, the correct one (in the built mock 2)"),
    "s6-d014": jexcerpt("runs/mock-02/owner-decisions.json", D2_014["reason"], "The rewrite of the owner on finding M2-SC5-R1-F6"),
    "s6-date": excerpt(D06, "This is ruling 2 of the owner, of 29 September 2026.", "Mock decision 0006"),
    "s6-writer": excerpt(D10, "It cannot prevent two questions with the same scene, and it cannot count for ruling 2 (decision 0006).", "Mock decision 0010"),
})
assert sum(RUNS6.values()) == 33 and N6 == 108

FIG61 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 330" role="img" aria-label="Step 6 starts when all 60 slots passed. For each scenario, code checks the questions against the plan and looks for exact copies. Then call 6a reads the 15 questions with the answer key for rules D1 and D4, and call 6b reads only the wrong options for rules D2 and D3. Each finding goes to the owner, who ignores it or rewrites one question. A rewrite goes to step 5.">
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 6-1</span>%(cap)s</figcaption>
</figure>""" % {
    "nodes": "".join([box(20, 120, 150, 90, ["all 60", "passed"], sub="each scenario"),
                      box(230, 120, 150, 90, ["code"], sub="plan, copies"),
                      box(440, 30, 190, 100, ["call 6a"], sub="D1 scene, D4 answer", cls="who-model"),
                      box(440, 200, 190, 100, ["call 6b"], sub="D2, D3: wrong options", cls="who-model"),
                      box(700, 115, 170, 100, ["the owner"], sub="ignore or rewrite", cls="who-owner")]),
    "edges": "".join([edge("M170 165H230"), edge("M380 165H410V80H440"), edge("M410 165V250H440"),
                      edge("M630 80H665V145H700", "findings", 640, 72, anchor="r"), edge("M630 250H665V185H700"),
                      edge("M785 215V300", "to step 5", 777, 270, cls="is-async", anchor="l")]),
    "cap": fact("s6-calls", "Two model calls read the 15 questions of a scenario together.") + " " + fact("s6-back", "Step 6 sends no question back. Each finding goes to the owner."),
}
R6 = [(k, RULE6.get(k, 0)) for k in ("D1", "D2", "D3", "D4")]
MX6 = max(v for _, v in R6)
FIG62 = """
<figure>
  <div class="frame has-narrow">
    <svg class="ve-bars" viewBox="0 0 600 %(h)d" role="img" aria-label="Findings of step 6 in mocks 1 to 5: %(vals)s.">%(bars)s</svg>
  </div>
  %(phone)s
  <figcaption><span class="fig-n">Fig. 6-2</span>%(cap)s</figcaption>
</figure>""" % {
    "h": len(R6) * 30 + 6, "vals": ", ".join("%s %d" % kv for kv in R6),
    "phone": phone_bars([(k, v, k == "D3", str(v), None) for k, v in R6], "Findings of step 6 in mocks 1 to 5: %s." % ", ".join("%s %d" % kv for kv in R6), MX6),
    "bars": "".join('<text x="0" y="%d">%s</text><rect class="%s" x="60" y="%d" width="%d" height="20"/><text class="hv" x="%d" y="%d">%d</text>'
                    % (i * 30 + 14, k, "hot" if k == "D3" else "", i * 30 + 4, v * 440 // MX6, 70 + v * 440 // MX6, i * 30 + 14, v) for i, (k, v) in enumerate(R6)),
    "cap": fact("s6-runs", "Step 6 ran %d times over mocks 1 to 5 and made %d findings. The owner rewrote a question for %d of them." % (sum(RUNS6.values()), N6, len(RW6))),
}

STEP6 = (level("overview",
               '<h4 class="takeaway">Two calls read each scenario as a whole, and the owner decides each finding</h4><p>%s %s %s</p>'
               % (fact("s6-what", "Steps 3 and 4 look at one question. Some defects show only when many questions are read together."),
                  fact("s6-calls", "When all 60 slots have passed, two model calls read the 15 questions of each scenario together."),
                  fact("s6-back", "Step 6 sends no question back: each finding goes to the owner.")))
         + level("explanation",
                 FIG61
                 + '<p><b>Why a step for the whole mock.</b> %s %s</p>' % (fact("s6-why", "Each writer call sees only its own slot, so two calls can write the same scene."), fact("s6-rules", "So call 6a looks for the same scene twice, and a question that gives away another answer, in one scenario. Call 6b reads only the wrong options of the scenario, to find one wrong option in too many questions."))
                 + '<p><b>Why the owner decides.</b> %s %s</p>' % (fact("s6-person", "A finding can name more than one question, so a person selects which one to write again, or none."), fact("s6-rule", "From the second run of mock 2, the owner ignored the findings of a question that gives away another answer, and recorded one wrong option in too many questions as a known limit of the mock."))
                 + FIG62 + ts_block(6))
         + level("depth",
                 '<h4 class="story">Too many wrong options on the confidence of the model</h4>'
                 '<p>%s ruling 2: %s The reason: %s %s</p>'
                 '<p>%s Only call 6b checks it. In mock 2, %s Its options B and C both used the confidence of the model: %s and %s The owner sent it back: %s The new try asks for the categories to report instead: %s</p>'
                 '<p>In mocks 2 to 5, some scenarios kept more than one such option. The owner recorded them as known limits of the mock, by the rule for findings above.</p>'
                 % (fact("s6-date", "Since 29 September 2026, the owner had a ruling,"),
                    fact("s6-r2", "in one scenario of one mock, at most one wrong option uses a model that rates its own confidence and uses the rating as a filter, a threshold or a trigger."),
                    fact("s6-52k3", "the guide calls self-reported confidence scores &ldquo;unreliable proxies for actual case complexity&rdquo; (5.2-K3), so it is a fair wrong option."),
                    fact("s6-r2why", "But if it appears many times, a participant can rule it out without thought."),
                    fact("s6-writer", "The writer of step 2 sees one slot, so it cannot count these options."),
                    fact("s6-f6", "call 6b found a finding of rule D3 on question M2-S41."),
                    fact("s6-b", "&ldquo;assign a confidence score to each finding and post only the findings above a fixed threshold&rdquo;"),
                    fact("s6-c", "&ldquo;be conservative and report only high-confidence findings&rdquo;."),
                    fact("s6-d014", "&ldquo;Use at most one wrong option on model confidence, and only if this scenario has no other one.&rdquo;"),
                    fact("s6-t2", "its correct option defines the issue categories to report and to skip.")))
         ).replace("@N@", "6")
PART_HTML[6] = with_sources(6, STEP6)

# ----- step 7: the questions are marked (facts: academy/facts/step-7.md) -----

S7F = step_file(7)
D45 = glob.glob(os.path.join(ROOT, "docs/decisions/0045-*.md"))[0][len(ROOT) + 1:]
D73 = glob.glob(os.path.join(ROOT, "docs/decisions/0073-*.md"))[0][len(ROOT) + 1:]
ROUND1, ROUND2, BAD = [], [], []
for m in range(1, 6):
    ROUND1.append(len(jread("runs/mock-%02d/marking-rounds/round-1.json" % m)["question_ids"]))
    _r2 = os.path.join(ROOT, "runs/mock-%02d/marking-rounds/round-2.json" % m)
    ROUND2.append(len(jread(os.path.relpath(_r2, ROOT))["question_ids"]) if os.path.exists(_r2) else 0)
    BAD.append(sum(1 for f in glob.glob(os.path.join(ROOT, "runs/mock-%02d/marks/round-*.json" % m))
                   for r in jread(os.path.relpath(f, ROOT)) if r["mark"] == "bad"))
MARKS_ALL = sum(len(jread(os.path.relpath(f, ROOT))) for f in glob.glob(os.path.join(ROOT, "runs/mock-0*/marks/round-*.json")))
BAD_IDS = [r["question_id"] for r in jread("runs/mock-05/marks/round-1.json") if r["mark"] == "bad"]
sys.path.insert(0, os.path.join(ROOT, "src"))
import control as _control  # noqa: E402
_keep = _control.MARK_ALL
_control.MARK_ALL = {1}      # the rule before mock decision 0073
OLD_SAMPLE = _control.Control(os.path.join(ROOT, "runs/mock-05"), 5, jread("runs/mock-05/plan.json")["seed"], None, {}).sample()
_control.MARK_ALL = _keep
assert len(OLD_SAMPLE) == 20 and not any(q.split("-T")[0] in OLD_SAMPLE for q in BAD_IDS) and len(BAD_IDS) == 2
F45 = next(f for f in jread("runs/mock-05/checks/M5-scenario-5-step6-run1.json")["findings"] if f["rule"] == "D1" and any(q.startswith("M5-S45") for q in f["question_ids"]))
RW_GOOD = 0
for m in range(1, 6):
    good = {r["question_id"] for r in jread("runs/mock-%02d/marks/round-1.json" % m) if r["mark"] == "good"}
    RW_GOOD += sum(1 for d in jread("runs/mock-%02d/owner-decisions.json" % m) if d["action"] == "rewrite" and d.get("question_id") in good)
N_RW = sum(1 for m in range(1, 6) for d in jread("runs/mock-%02d/owner-decisions.json" % m) if d["action"] == "rewrite")

CARD.update({
    "s7-what": excerpt(S7F, "This step shows if those checks are right: a reader marks the questions. For mocks 1 to 3 the reader is the owner. For mocks 4 and 5 it is the second review in Cowork, also a Claude model", "Build guide, step 7"),
    "s7-file": excerpt(S7F, "It shows no verdict of a checker. The owner fills two columns: \"good\" or \"bad\", and a reason for a bad mark.", "Build guide, step 7"),
    "s7-which": excerpt(S7F, "For mock 1 the owner marks all 60 questions. For mocks 2 to 4 the file has a random sample of 20, 5 from each scenario. For mock 5 the file has all 60 questions again (decision 0073).", "Build guide, step 7"),
    "s7-bad": excerpt(S7F, "A bad mark sends the question to step 5, with the reason as the finding.", "Build guide, step 7"),
    "s7-stop": code_block("src/control.py", "STOP_MOCK_1 = ", "MARK_ALL = ", "The limits of the marks in the code"),
    "s7-tend": {"title": "Diagram 09 of the mock builder, the popup of the owner", "kind": "excerpt", "text": "A person who sees a verdict tends to agree with it.",
                "src": "docs/diagrams/09-step-7-the-owner-marks-the-questions.html, line %d" % lines_of("docs/diagrams/09-step-7-the-owner-marks-the-questions.html", "A person who sees a verdict tends to agree with it.")[0],
                "href": link("docs/diagrams/09-step-7-the-owner-marks-the-questions.html", lines_of("docs/diagrams/09-step-7-the-owner-marks-the-questions.html", "A person who sees a verdict tends to agree with it.")[0])},
    "s7-runs": {"title": "The marks of mocks 1 to 5", "kind": "count",
                "text": "Questions in round 1: %s for mocks 1 to 5. %d marks in all, %d bad: %s. %d of the %d rewrites of the owner changed a question with a good mark. The others changed a question with no mark. The script of this page counted runs/mock-0N/marking-rounds/, marks/ and owner-decisions.json."
                        % (", ".join(map(str, ROUND1)), MARKS_ALL, sum(BAD), " and ".join(BAD_IDS), RW_GOOD, N_RW),
                "src": "runs/mock-0N/marking-rounds/, runs/mock-0N/marks/", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s7-old": {"title": "The sample of 20 that the old rule gives for mock 5", "kind": "count",
               "text": "The code of src/control.py, with MARK_ALL set to {1} as before mock decision 0073, and the seed of runs/mock-05/plan.json, selects: %s. Neither %s is in it. The script of this page ran Control.sample() with no model call."
                       % (", ".join(OLD_SAMPLE), " nor ".join(q.split("-T")[0] for q in BAD_IDS)),
               "src": "src/control.py, runs/mock-05/plan.json", "href": link("src/control.py")},
    "s7-d1": {"title": "The finding of step 6 on M5-S45 (mock 5, scenario 5, run 1)", "kind": "excerpt",
              "text": "%s, rule %s, names %s: %s" % (F45["id"], F45["rule"], " and ".join(F45["question_ids"]), F45["detail"]),
              "src": "runs/mock-05/checks/M5-scenario-5-step6-run1.json, line %d" % lines_of("runs/mock-05/checks/M5-scenario-5-step6-run1.json", '"id": "%s"' % F45["id"])[0],
              "href": link("runs/mock-05/checks/M5-scenario-5-step6-run1.json", lines_of("runs/mock-05/checks/M5-scenario-5-step6-run1.json", '"id": "%s"' % F45["id"])[0])},
    "s7-refuse": code_block("src/control.py", 'problems.append("%s: no mark" % qid)', 'problems.append("%s: a bad mark has no reason" % qid)', "Code refuses an incomplete marking file"),
    "s7-all": excerpt(D73, "The owner said: \"Put all 60 questions of mock 5 in the marking file.\"", "Mock decision 0073, How we decided"),
    "s7-why60": excerpt(D73, "Plain reason: no person reads the questions of mock 5 (decision 0071). So the second review, as the only reader, reads all of them, not a sample.", "Mock decision 0073, Reason"),
    "s7-m1": excerpt(D45, "The owner marked the 60 questions of mock 1 blind: 60 good. A second review by a Claude model after the blind marking found 7 problems of the mock as a set", "Mock decision 0045, Question"),
    "s7-set": excerpt(D45, "Here the owner and the second review found each question good on its own, so steps 3 and 4 did not fail. The 7 are problems of the mock as a set.", "Mock decision 0045, Reason"),
})
lines_of("docs/diagrams/09-step-7-the-owner-marks-the-questions.html", "A person who sees a verdict tends to agree with it.")

COLS71 = [(["Question"], "code"), (["Point"], "code"), (["Correct", "answer"], "code"), (["Reasons of", "the options"], "code"), (["Mark"], "reader"), (["Reason (for", "a bad mark)"], "reader")]
FIG71 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 190" role="img" aria-label="The marking file, close up. Code writes 13 of its 15 columns, among them Question, Point, Correct answer and Reasons of the options. The reader fills two columns: Mark, and Reason (needed for a bad mark). The file has no column for the verdict of a checker.">
      <text class="ve-lab" x="20" y="22">written by code: 13 columns, among them</text><text class="ve-lab" x="600" y="22">filled by the reader: 2 columns</text>
      %(cols)s
      <g class="ve-n guard"><rect class="sh" x="20" y="120" width="850" height="50" rx="0" style="stroke-dasharray:6 5"/><text x="445" y="150">no column for the verdict of a checker</text></g>
    </svg>
  </div>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 300" role="img" aria-label="Step 7. A reader marks each question good or bad, with a reason for a bad mark. Code reads the file. A good mark keeps the question. A bad mark sends the question to step 5. Too many bad marks stop the mock.">
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 7-1</span>%(cap)s</figcaption>
</figure>""" % {
    "cols": "".join('<g class="ve-n%s"><rect class="sh" x="%d" y="34" width="134" height="64" rx="0"/>%s</g>'
                    % (" is-key" if who == "reader" else "", 20 + i * 143,
                       "".join('<text x="%d" y="%d">%s</text>' % (87 + i * 143, 70 - (len(name) - 1) * 10 + k * 20, e(t)) for k, t in enumerate(name)))
                    for i, (name, who) in enumerate(COLS71)),
    "nodes": "".join([box(20, 100, 170, 100, ["marking file"], sub="no verdict shown"),
                      box(260, 100, 170, 100, ["a reader"], sub="good or bad"),
                      box(500, 100, 150, 100, ["code"], sub="reads the file"),
                      box(720, 20, 150, 70, ["good"], sub="kept", cls="try ok"),
                      box(720, 115, 150, 70, ["bad"], sub="to step 5", cls="try bad"),
                      box(720, 210, 150, 70, ["too many bad"], sub="the mock stops", cls="guard")]),
    "edges": "".join([edge("M190 150H260", "rows", 225, 141), edge("M430 150H500", "marks", 465, 141),
                      edge("M650 150H685V55H720"), edge("M650 150H720", cls="is-async"), edge("M685 150V245H720")]),
    "cap": fact("s7-file", "The file shows no verdict of a checker. The reader fills two columns: good or bad, and a reason for a bad mark.") + " " + fact("s7-tend", "A person who sees a verdict tends to agree with it."),
}

FIG72 = """
<figure>
  <div class="cases two">%s</div>
  <figcaption><span class="fig-n">Fig. 7-2</span>%s</figcaption>
</figure>""" % ("".join(
    '<div class="case"><span class="ve-label">Mock %d</span><svg class="ve-bars" viewBox="0 0 240 106" role="img" aria-label="Mock %d: %d marked in round 1, %d in round 2, %d bad marks">'
    '<text x="0" y="16">round 1</text><rect x="70" y="4" width="%d" height="20"/><text class="hv" x="%d" y="16">%d</text>'
    '<text x="0" y="52">round 2</text><rect x="70" y="40" width="%d" height="20"/><text class="hv" x="%d" y="52">%d</text>'
    '<text x="0" y="88">bad</text><rect class="hot" x="70" y="76" width="%d" height="20"/><text class="hv" x="%d" y="88">%d</text></svg>'
    '<p class="cap">%s, round 1. Reader: %s</p></div>'
    % (m + 1, m + 1, ROUND1[m], ROUND2[m], BAD[m],
       ROUND1[m] * 130 // SLOTS, 78 + ROUND1[m] * 130 // SLOTS, ROUND1[m],
       ROUND2[m] * 130 // SLOTS, 78 + ROUND2[m] * 130 // SLOTS, ROUND2[m],
       BAD[m] * 130 // SLOTS, 78 + BAD[m] * 130 // SLOTS, BAD[m], "all" if ROUND1[m] == SLOTS else "a sample",
       "the owner" if m < 3 else "a Claude model" if m == 4 else "a Claude model. The owner filled the 20 marks of round 1 without reading the questions (mock decision 0069, academy decision 0039)")
    for m in range(5)),
    fact("s7-runs", "Over the 5 mocks, %d marks were given: %d in round 1 and %d in round 2, after a send-back. %d were bad, both in mock 5." % (MARKS_ALL, sum(ROUND1), MARKS_ALL - sum(ROUND1), sum(BAD))))

STEP7 = (level("overview",
               '<h4 class="takeaway">A reader marks the questions in a file good or bad, and the file shows no verdict</h4><p>%s %s %s</p>'
               % (fact("s7-what", "The checks before this step are code or a model. The build guide says that a reader who marks the questions shows if those checks are right. For mocks 1 to 3 the reader was the owner. For mocks 4 and 5 it was a Claude model, the second review."),
                  fact("s7-bad", "A bad mark sends the question to step 5, with the reason as the finding."),
                  fact("s7-stop", "Too many bad marks stop the mock.")))
         + level("explanation",
                 FIG71
                 + '<p><b>Which questions.</b> %s %s</p>' % (fact("s7-which", "Mock 1 and mock 5 put all 60 questions in the file. Mocks 2 to 4 put a random sample of 20, 5 from each scenario."), fact("s7-refuse", "Code refuses a file with a missing mark, or a bad mark with no reason."))
                 + FIG72 + ts_block(7))
         + level("depth",
                 '<h4 class="story">A sample of 20 would have marked neither bad question</h4>'
                 '<p>For mock 5, no person read the questions. %s %s The second review then gave the only 2 bad marks in the records of the 5 mocks: %s %s %s Only M5-S33, a copy of a question of mock 2, had no other check that found it, although it had passed step 4 with rule B9.</p>'
                 '<h4 class="story">Good on its own, wrong as a set</h4>'
                 '<p>%s %s So the 7 became rewrites, not bad marks. %s</p>'
                 % (fact("s7-all", "The owner said: &ldquo;Put all 60 questions of mock 5 in the marking file.&rdquo;"),
                    fact("s7-why60", "The reason: the second review was the only reader, so it read all of them, not a sample."),
                    " and ".join(q.split("-T")[0] for q in BAD_IDS) + ".",
                    fact("s7-old", "The old rule, a sample of 20 with the same seed, holds neither of them."),
                    fact("s7-d1", "Step 6 had already named M5-S45, with rule D1."),
                    fact("s7-m1", "The owner marked the 60 questions of mock 1 blind: 60 good. A second review by a Claude model then found 7 problems of the mock as a set."),
                    fact("s7-set", "Each question was good on its own, so steps 3 and 4 had not failed."),
                    fact("s7-runs", "Over the 5 mocks, %d of the %d rewrites of the owner changed a question that had a good mark. The other %d had no mark." % (RW_GOOD, N_RW, N_RW - RW_GOOD))))
         ).replace("@N@", "7")
PART_HTML[7] = with_sources(7, STEP7)

# ----- step 8: build the files (facts: academy/facts/step-8.md) -----

S8 = step_file(8)
D16 = glob.glob(os.path.join(ROOT, "docs/decisions/0016-*.md"))[0][len(ROOT) + 1:]
D70 = glob.glob(os.path.join(ROOT, "docs/decisions/0070-*.md"))[0][len(ROOT) + 1:]
REV2 = "docs/reviews/review-decisions-0024-to-0037.md"
FP_OK, FP_ALL, NO_KEY = 0, 0, True
for m in range(1, 6):
    b = jread("runs/mock-%02d/build.json" % m)["fingerprints"]
    for qid, fp in b.items():
        FP_ALL += 1
        FP_OK += _control.fingerprint(jread("runs/mock-%02d/questions/%s.json" % (m, qid))) == fp
    NO_KEY = NO_KEY and '"correct"' not in read("mocks/mock-%02d.questions.json" % m) and '"reason"' not in read("mocks/mock-%02d.questions.json" % m)
assert FP_OK == FP_ALL == 300 and NO_KEY
LETTERS = []
for m in range(1, 6):
    c = Counter(a["correct"][0] for a in jread("mocks/mock-%02d.answers.json" % m)["answers"] if len(a["correct"]) == 1)
    LETTERS.append([c.get(x, 0) for x in "ABCD"])

D39 = glob.glob(os.path.join(ROOT, "docs/decisions/0039-*.md"))[0][len(ROOT) + 1:]
assert LETTERS[3][3] == 22 and all(sum(l) == 52 for l in LETTERS) and LETTERS[4] == [13, 13, 13, 13]
CARD.update({
    "s8-fpdef": excerpt(S8, "each check saves a fingerprint of the question: a code of 64 characters that code calculates from the text. Before the build, code calculates the fingerprint again and compares.", "Build guide, step 8"),
    "s8-six": code_block("src/control.py", "def build_conditions(self", "def build_conditions(self", "The six conditions are in build_conditions() of the control"),
    "s8-item10": excerpt(D39, "Step 8 starts only after the command `accept` of the owner, and only when:", "Mock decision 0039, Item 10"),
    "s8-plan5": excerpt(D70, "Option 1, from mock 5.", "Mock decision 0070, Decision"),
    "s8-what": excerpt(S8, "Code builds the two files of a mock from the stored question records. Nobody edits the files by hand.", "Build guide, step 8"),
    "s8-two": excerpt("src/step8_build_files.py", "the 60 questions, with no answers and no reasons", "The code of step 8", kind="code"),
    "s8-accept": code_block("src/control.py", "def accept(self", '"""Command of the owner: accept the mock.', "The command accept of the owner"),
    "s8-cond": code_block("src/control.py", 'raise Refused("Step 8 cannot start: "', 'raise Refused("Step 8 cannot start: "', "The code lists each cause and builds no file"),
    "s8-one": excerpt(D16, "If a question exists in two places and a person can edit one of them, the two can disagree, and nobody knows which one the checks saw.", "Mock decision 0016, Reason"),
    "s8-nopoint": excerpt(S8, "The step uses no point of a task statement. It uses three facts of the exam form.", "Build guide, step 8"),
    "s8-fp": {"title": "The fingerprints of the 5 built mocks", "kind": "count",
              "text": "%d of %d fingerprints in runs/mock-0N/build.json equal the fingerprint of the question record today (fingerprint() of src/control.py). No questions file has the key \"correct\" or \"reason\". The script of this page checked them." % (FP_OK, FP_ALL),
              "src": "runs/mock-0N/build.json, runs/mock-0N/questions/", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s8-never": excerpt(REV2, "So the mock can never be built.", "The second design review"),
    "s8-cmd": excerpt(D38, "5. **Step 8 starts when the owner accepts the mock.** Code checks the conditions before it builds.", "Mock decision 0038, Decision"),
    "s8-letters": excerpt(D70, "In mock 4, D is the correct answer of 22 of the 52 questions with one answer, and B of 8. Chance is 13.", "Mock decision 0070, Question"),
    "s8-portal": excerpt(D70, "4. **A note for the portal:** the portal shows the options in a random order on each attempt, because the letters in mocks 1 to 4 are not balanced.", "Mock decision 0070, Decision"),
    "s8-count": {"title": "The correct letters of the 5 built mocks", "kind": "count",
                 "text": "One-answer questions with the correct answer A, B, C, D: %s. The script of this page counted mocks/mock-0N.answers.json." % ". ".join("mock %d: %s" % (i + 1, ", ".join(map(str, l))) for i, l in enumerate(LETTERS)),
                 "src": "mocks/mock-01.answers.json to mock-05.answers.json", "href": "%s/tree/%s/mocks" % (REPO, TAG)},
})

CONDS = ["passed steps 3 and 4, unchanged", "step 6 checked the current questions", "each finding has a decision",
         "each question that needs a mark has one", "the bad marks are below the limit", "no call failed in the last run"]
lines_of("docs/decisions/0039-the-control-in-code-the-states-and-the-records.md" if os.path.exists(os.path.join(ROOT, "docs/decisions/0039-the-control-in-code-the-states-and-the-records.md")) else glob.glob(os.path.join(ROOT, "docs/decisions/0039-*.md"))[0][len(ROOT) + 1:], "6. No call failed in the last run.")
FIG81 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 330" role="img" aria-label="Step 8. The owner accepts the mock with a command. Code checks six conditions. If one is false, code builds no file and lists the causes. If all hold, code builds the questions file with no answers, the answers file, and a record of the fingerprints.">
      <g class="ve-n is-key"><rect class="sh" x="230" y="20" width="330" height="290" rx="0"/></g>
      <text class="ve-lab" x="246" y="44">code checks %(n6)d conditions</text>
      %(conds)s
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 8-1</span>%(cap)s</figcaption>
</figure>""" % {
    "n6": len(CONDS),
    "conds": "".join('<text class="ve-lab" x="246" y="%d"><tspan class="pid">%d</tspan> %s</text>' % (80 + i * 38, i + 1, e(t)) for i, t in enumerate(CONDS)),
    "nodes": "".join([box(20, 125, 150, 80, ["the owner"], sub="accept", cls="who-owner"),
                      box(640, 20, 230, 70, ["questions file"], sub="no answers"),
                      box(640, 110, 230, 70, ["answers file"], sub="letters, reasons"),
                      box(640, 200, 230, 50, ["fingerprints"]),
                      box(640, 265, 230, 50, ["no file, causes"], cls="try bad")]),
    "edges": "".join([edge("M170 165H230"), edge("M560 140H600V55H640"), edge("M600 140V145H640"), edge("M600 140V225H640"),
                      edge("M560 290H640", "one false", 600, 281)]),
    "cap": fact("s8-what", "Code builds the two files of a mock from the stored records. Nobody edits the files by hand.") + " " + fact("s8-item10", "Step 8 starts only after the owner accepts, and only when the conditions hold.") + " " + fact("s8-cond", "If a condition is false, code builds no file and lists the causes."),
}

FIG82 = """
<figure>
  <div class="cases">%s</div>
  <figcaption><span class="fig-n">Fig. 8-2</span>%s</figcaption>
</figure>""" % ("".join(
    '<div class="case"><span class="ve-label">Mock %d</span><svg class="ve-mini" viewBox="0 0 200 110" role="img" aria-label="Mock %d, correct letters of the 52 one-answer questions: A %d, B %d, C %d, D %d.">%s<path class="chance" d="M0 %d H200"/></svg></div>'
    % (m + 1, m + 1, *LETTERS[m], "".join('<rect class="bar" x="%d" y="%d" width="34" height="%d"/><text class="ve-lab" x="%d" y="106">%s %d</text>'
                                            % (8 + i * 48, 86 - v * 3, v * 3, 8 + i * 48, "ABCD"[i], v) for i, v in enumerate(LETTERS[m])), 86 - 13 * 3)
    for m in range(5)),
    fact("s8-count", "The correct letters of the 52 one-answer questions in each built mock. The dashed line is 13, the chance number.") + " " + fact("s8-letters", "In mock 4, D was the answer %d times." % LETTERS[3][3]))

STEP8 = (level("overview",
               '<h4 class="takeaway">Code builds the mock files from the question records, only after the owner accepts</h4><p>%s %s %s</p>'
               % (fact("s8-what", "Code builds the two files of a mock from the stored question records. Nobody edits the files by hand."),
                  fact("s8-two", "One file has the 60 questions with no answers and no reasons. The other has the answers."),
                  fact("s8-accept", "The step starts only when the owner accepts the mock with a command, and code checks the conditions first.")))
         + level("explanation",
                 FIG81
                 + '<p><b>One true copy.</b> %s %s %s</p>' % (fact("s8-one", "If a question exists in two places and a person can edit one of them, the two can disagree, and nobody knows which one the checks saw."),
                                                          fact("s8-fpdef", "Each check saves a fingerprint of the question: a code of 64 characters that code calculates from its text. Before the build, code calculates it again and compares."),
                                                          fact("s8-fp", "In the 5 built mocks, each of the %d fingerprints still equals its question record." % FP_ALL))
                 + '<p class="gh">The task statements that step 8 uses</p><p>%s The reason for one true copy is plain engineering, and no point of the guide gives it. The facts of the exam format are: each question states how many answers to select, the questions are in groups by scenario, and each question has its domain for a result by domain.</p>'
                   % fact("s8-nopoint", "None. The step uses three facts of the exam format, not a point of a task statement."))
         + level("depth",
                 ('<h4 class="story">The first conditions could never be met</h4>'
                  '<p>The first design started step 8 when each question had passed steps 3, 4 and 6. But a finding that the owner ignores stays a &ldquo;fail&rdquo;, so the second design review (<a href="#step-5">step 5</a> counts its items) found: &ldquo;%s&rdquo; The fix: %s The exact conditions became code, with tests (mock decisions 0038 and 0039).</p>'
                  % (fact("s8-never", "So the mock can never be built."), fact("s8-cmd", "step 8 starts when the owner accepts the mock, and code checks the conditions before it builds.")))
                 + '<h4 class="story">The letters were not balanced</h4>' + FIG82
                 + '<p>%s So from mock 5, the plan of step 1 sets the correct letters, 13 for each of A to D (see step 2). For mocks 1 to 4, %s</p>'
                 % (fact("s8-plan5", "The fix starts at mock 5."), fact("s8-portal", "the files did not change, and a note asks the portal to show the options in a random order on each attempt.")))
         ).replace("@N@", "8")
PART_HTML[8] = with_sources(8, STEP8)

# ----- slice 3: the build in Claude Code (facts: academy/facts/claude-code.md, academy decisions 0023 and 0031) -----

DOCS_CC = "academy/sources/2026-10-14-claude-code-docs-%s.md"
JR = "docs/journal.md"
AJ = "academy/journal.md"
A10 = glob.glob(os.path.join(ROOT, "academy/decisions/0010-*.md"))[0][len(ROOT) + 1:]
D78 = glob.glob(os.path.join(ROOT, "docs/decisions/0078-*.md"))[0][len(ROOT) + 1:]
CC_LINES = len(read("CLAUDE.md").splitlines())
N_RULES = len(re.findall(r"(?m)^\d+\. ", read("WORKING-RULES.md")))
N_MOCK_DEC = len([f for f in os.listdir(os.path.join(ROOT, "docs/decisions")) if re.match(r"^\d{4}-.*\.md$", f)])
GAPS2 = number(JR, r"fixed the (\d+) gaps of the check")
GAPS3 = number(JR, r"a third independent check after these fixes found (\d+) smaller gaps")
assert "@WORKING-RULES.md" in read("CLAUDE.md").splitlines()

CARD.update({
    "cc-import": excerpt("CLAUDE.md", "@WORKING-RULES.md", "CLAUDE.md of the project"),
    "cc-first": excerpt("CLAUDE.md", "Read `HANDOFF.md` first. It says where the work stopped and what the next step is.", "CLAUDE.md of the project"),
    "cc-check": excerpt("CLAUDE.md", "Before a session stops, check the record and show the owner the result:\n\n1. `docs/journal.md` has an entry for this session.\n2. Each decision that the owner made in this session has its file in `docs/decisions/`.\n3. `HANDOFF.md` has the new state and the next step.", "CLAUDE.md of the project"),
    "cc-doc-import": excerpt(DOCS_CC % "memory", "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.", "Claude Code documentation, Memory (copy of 14 October 2026)", kind="docs"),
    "cc-doc-context": excerpt(DOCS_CC % "memory", "Claude treats them as context, not enforced configuration.", "Claude Code documentation, Memory (copy of 14 October 2026)", kind="docs"),
    "cc-31k3": excerpt("reference/exam-guide.md", "The @import syntax for referencing external files to keep CLAUDE.md modular", "Exam guide, 3.1-K3", kind="guide"),
    "cc-blind": excerpt(JR, "The blind file was not in git: only the empty file of the program was committed. The owner had sent the blind file to the Cowork session before the second review, and it came back from there unchanged", "Journal of the mock builder, 8 October 2026"),
    "cc-line": excerpt("CLAUDE.md", "5. A marking file that the owner filled is committed before anybody else reads it.", "CLAUDE.md of the project"),
    "cc-handoff": excerpt("HANDOFF.md", "This file gives a new session what it needs to continue.", "HANDOFF.md"),
    "cc-d01": excerpt(glob.glob(os.path.join(ROOT, "docs/decisions/0001-*.md"))[0][len(ROOT) + 1:], "5.4-K2, 5.4-K4, 5.6-K2", "Mock decision 0001, Exam guide points"),
    "cc-54k2": excerpt("reference/exam-guide.md", "The role of scratchpad files for persisting key findings across context boundaries", "Exam guide, 5.4-K2", kind="guide"),
    "cc-17k4": excerpt("reference/exam-guide.md", "Why starting a new session with a structured summary is more reliable than resuming with stale tool results", "Exam guide, 1.7-K4", kind="guide"),
    "cc-doc-session": excerpt(DOCS_CC % "how-claude-code-works", "Each new session starts with a fresh context window, without the conversation history from previous sessions.", "Claude Code documentation, How Claude Code works (copy of 14 October 2026)", kind="docs"),
    "cc-records": {"title": "The records of the build", "kind": "count", "text": "docs/decisions/ has %d mock decisions. WORKING-RULES.md has %d numbered rules. CLAUDE.md has %d lines. The script of this page counted them." % (N_MOCK_DEC, N_RULES, CC_LINES),
                   "src": "docs/decisions/, WORKING-RULES.md, CLAUDE.md", "href": "%s/tree/%s/docs/decisions" % (REPO, BRANCH)},
    "cc-notread": excerpt(JR, "The assistant showed a plan for the control before it read all files that `HANDOFF.md` names. The owner asked if it had read them. It had not.", "Journal of the mock builder, 7 October 2026"),
    "cc-r15": excerpt("WORKING-RULES.md", "15. An independent reviewer checks each file that a new session or a participant will rely on, before the assistant says that the file is correct. The reviewer is a new agent that did not make the file.", "Working rule 15"),
    "cc-r14": excerpt("WORKING-RULES.md", "14. The owner does not trust the assistant to find everything. A check must not depend on the memory or the judgment of the assistant alone.", "Working rule 14"),
    "cc-r12": excerpt("WORKING-RULES.md", "12. Record each decision on the day the owner makes it, as one file in `docs/decisions/`.", "Working rule 12"),
    "cc-r30": excerpt("WORKING-RULES.md", "for the design of a pipeline step, the assistant shows one proposal with all details of the step. The proposal names the exact file format and the exact fields. The owner accepts it or names what to change.", "Working rule 30"),
    "cc-r25": excerpt("WORKING-RULES.md", "25. Write one entry at the top of `docs/journal.md` for each session.", "Working rule 25"),
    "cc-six": excerpt(JR, "It read them, and changed six points of the plan.", "Journal of the mock builder, 7 October 2026"),
    "cc-doc-start": excerpt(DOCS_CC % "memory", "Claude Code has two complementary memory systems. Both are loaded at the start of every conversation.", "Claude Code documentation, Memory (copy of 14 October 2026)", kind="docs"),
    "cc-d23": excerpt("academy/facts/claude-code.md", "Verdict: decision 0023 holds. There is no example of 3.4: no record in the repository of plan mode or of the Explore subagent.", "Fact sheet of the build in Claude Code"),
    "cc-d78": excerpt(D78, "The owner asked for an independent check of all documents before the push, by an agent that did not write them.", "Mock decision 0078, How we decided"),
    "cc-a12": excerpt(glob.glob(os.path.join(ROOT, "academy/decisions/0012-*.md"))[0][len(ROOT) + 1:], "Two new agents for each part.", "Academy decision 0012"),
    "cc-a15": excerpt(glob.glob(os.path.join(ROOT, "academy/decisions/0015-*.md"))[0][len(ROOT) + 1:], "A whole-picture review after each slice. A slice is a group of parts that the assistant builds and shows to the owner together", "Academy decision 0015"),
    "cc-46s1": excerpt("reference/exam-guide.md", "Using a second independent Claude instance to review generated code without the generator's reasoning context", "Exam guide, 4.6-S1", kind="guide"),
    "cc-46k1": excerpt("reference/exam-guide.md", "Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session", "Exam guide, 4.6-K1", kind="guide"),
    "cc-46k3": excerpt("reference/exam-guide.md", "Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes", "Exam guide, 4.6-K3", kind="guide"),
    "cc-code": excerpt(JR, "Two independent reviewers checked the code, the tests and decision 0039. The first found 4 serious and 6 minor bugs. The second found 1 serious and 3 minor bugs in the fixes.", "Journal of the mock builder, 7 October 2026"),
    "cc-doc-fresh": excerpt(DOCS_CC % "sub-agents", "Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read. Claude composes a delegation message that summarizes the task, and the subagent works from there. The exception is a [fork](#fork-the-current-conversation), which inherits the parent conversation instead of starting fresh.", "Claude Code documentation, Subagents (copy of 14 October 2026)", kind="docs"),
    "cc-c1": excerpt(JR, "an independent agent checked all documents before the push.", "Journal of the mock builder, 9 October 2026"),
    "cc-c2": excerpt(JR, "a second independent check of all documents, also diagrams 03, 05, 08 and 10 and the build guide sections of steps 0, 1, 3 and 6. Commit 5244bf6 added the rule for the step 6 findings to diagram 08 and to step 6 (D4 ignored, D2 and D3 recorded as known limits, any other kind to the owner), and the build guide section of step 0. The assistant then fixed the %d gaps of the check" % GAPS2, "Journal of the mock builder, 9 October 2026"),
    "cc-c3": excerpt(JR, "a third independent check after these fixes found %d smaller gaps." % GAPS3, "Journal of the mock builder, 9 October 2026"),
    "cc-stop": excerpt(JR, "No reviewer checked the 20 fixes after the third check. The owner stopped the document checks there.", "Journal of the mock builder, 9 October 2026"),
    "cc-r8": excerpt("WORKING-RULES.md", "8. Discuss first. Do not write a document, a diagram or code before the owner asks for it.", "Working rule 8"),
    "cc-34k1": excerpt("reference/exam-guide.md", "Plan mode is designed for complex tasks involving large-scale changes, multiple valid approaches, architectural decisions, and multi-file modifications", "Exam guide, 3.4-K1", kind="guide"),
    "cc-doc-plan": excerpt(DOCS_CC % "permission-modes", "Plan mode tells Claude to research and propose changes without making them.", "Claude Code documentation, Permission modes (copy of 14 October 2026)", kind="docs"),
    "cc-nomode": excerpt(JR, "3.4-K1 is not in the list of exam guide points, because the decision does not use plan mode.", "Journal of the mock builder, 6 October 2026"),
    "cc-soon": excerpt(glob.glob(os.path.join(ROOT, "academy/decisions/0010-*.md"))[0][len(ROOT) + 1:], "The assistant moved to the build too soon. The owner stopped it: the outline was not finished.", "Academy decision 0010, How we decided"),
})
assert GAPS2 == 26 and GAPS3 == 20

FIGCC = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 190" role="img" aria-label="Three independent checks of all documents on 9 October 2026. Check 1 found gaps, with no count in the journal. Check 2, wider, found %(g2)d gaps. Check 3 found %(g3)d smaller gaps. Then the owner stopped the checks.">
      %(edges)s
      %(nodes)s
    </svg>
  </div>
  %(gbars)s
  <figcaption><span class="fig-n">Fig. C-4.6-1</span>%(cap)s</figcaption>
</figure>""" % {"g2": GAPS2, "g3": GAPS3,
                "gbars": small_bars([("check 2: gaps", GAPS2, True), ("check 3: gaps", GAPS3, False)], "Gaps found: check 2 found %d and check 3 found %d. Check 1 has no count in the journal." % (GAPS2, GAPS3)).replace("</svg>", '<text x="0" y="102">check 1: no count in the journal</text></svg>').replace('viewBox="0 0 340 92"', 'viewBox="0 0 340 112"'),
                "nodes": "".join([box(20, 50, 170, 90, ["check 1"], sub="gaps, no count", cls="who-model"),
                                  box(260, 50, 170, 90, ["check 2"], sub="%d gaps, more files" % GAPS2, cls="who-model"),
                                  box(500, 50, 170, 90, ["check 3"], sub="%d smaller gaps" % GAPS3, cls="who-model"),
                                  box(740, 50, 130, 90, ["stopped"], sub="by the owner", cls="who-owner")]),
                "edges": "".join([edge("M190 95H260", "fixes", 225, 86), edge("M430 95H500", "fixes", 465, 86), edge("M670 95H740", "fixes", 705, 86)]),
                "cap": fact("cc-d78", "The owner asked for a check by an agent that had not written the documents.") + " " + fact("cc-c2", "Check 2, also independent, found %d gaps," % GAPS2) + " " + fact("cc-c3", "and check 3 found %d." % GAPS3) + " " + fact("cc-stop", "After the fixes of check 3, the owner stopped the checks.")}


TAKE = re.compile(r'<h4 class="takeaway">(.*?)</h4>')


def take_out(body):
    """The takeaway of a part goes into its closed heading (academy decision 0039, item 4), and leaves the Overview."""
    m = TAKE.search(body)
    return (m.group(1), body[:m.start()] + body[m.end():]) if m else (None, body)


def cc_part(pid, num, title, who, body):
    take, body = take_out(body)
    head, line = (take, e(title) + " · " + e(who)) if take else (e(title), e(who))
    return ('<details class="part" id="%s"><summary><span class="pn">%s</span><span><h3>%s</h3><span class="who">%s</span></span>'
            '<span class="mm"><span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (pid, num, head, line, body))


def cc_ts(tsid, key):
    POP[key] = {"who": "Task statement " + tsid, "cls": "model", "title": TS[tsid]["title"], "example": None,
                "sent": ["The points that the build did not use:" if tsid == "3.4" else "The points that this part shows:"], "points": pts(*[p for p in CC_POINTS[tsid]])}
    return ('<p class="gh">The task statement</p><div class="tslist"><div class="tsrow"><span class="chip info" data-step="%s" tabindex="0" role="button" aria-expanded="false">Task statement %s</span> '
            '<span>%s</span> <a href="%s#ts-%s">Exam guide breakdown %s &rarr;</a></div></div>' % (key, tsid, e(TS[tsid]["title"]), TAB1, tsid.replace(".", "-"), tsid))


CC_POINTS = {"3.1": ["3.1-K3"], "1.7": ["1.7-K4"], "4.6": ["4.6-K1", "4.6-S1", "4.6-K3"], "3.4": ["3.4-K1", "3.4-K3"]}


def cc_body(pid, overview, explanation, depth, label="what went wrong, and the fix"):
    html = (level("overview", overview) + level("explanation", explanation) + level("depth", depth, label)).replace("Sources of step @N@", "Sources of this part").replace("@N@", pid)
    cards = list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', html)))
    return html.replace("@SOURCES@", sources(cards))


CC_HTML = "".join([
    cc_part("cc-3-1", "3.1", "CLAUDE.md imports the working rules", "task statement 3.1", cc_body("cc-3-1",
        '<h4 class="takeaway">One short file loads the working rules into each session</h4><p>%s %s %s</p>'
        % (fact("cc-doc-start", "Claude Code loads the CLAUDE.md of the project at the start of each session.") + " " + fact("cc-first", "Its first instruction sends the session to HANDOFF.md."),
           fact("cc-import", "A line with @WORKING-RULES.md imports the working rules of the owner."),
           fact("cc-records", "CLAUDE.md has %d lines, and WORKING-RULES.md has %d rules." % (CC_LINES, N_RULES))),
        '<p>%s This keeps CLAUDE.md short and the working rules in one file that the owner can change. %s</p>' % (fact("cc-doc-import", "An import is expanded and loaded at the start of the session."), fact("cc-31k3", "The guide names this: the @import syntax keeps CLAUDE.md modular (3.1-K3)."))
        + '<p><b>A limit.</b> %s A rule in CLAUDE.md guides the assistant. It does not block an action.</p>' % fact("cc-doc-context", "Claude Code treats CLAUDE.md as context, not as enforced configuration.")
        + cc_ts("3.1", "cc-3-1-ts"),
        '<h4 class="story">A file that was not in git</h4><p>%s %s</p>'
        % (fact("cc-blind", "The owner's blind marking file of mock 1 was not in git: only the empty file of the mock builder was committed. The owner had sent it to the chat of the second review before that review, and it came back unchanged."),
           fact("cc-line", "So CLAUDE.md got a new line in its end-of-session check: a marking file that the owner filled is committed before anybody else reads it.")))),
    cc_part("cc-1-7", "1.7", "A summary for each new session", "task statement 1.7", cc_body("cc-1-7",
        '<h4 class="takeaway">A new session starts fresh, from a summary that an earlier session wrote</h4><p>%s %s</p>'
        % (fact("cc-doc-session", "Each new session of Claude Code starts with a fresh context window, without the history of earlier sessions."),
           fact("cc-handoff", "So HANDOFF.md gives a new session what it needs to continue.")),
        '<p>%s %s %s</p>'
        % (fact("cc-r25", "The journal has one entry for each session,") + " " + fact("cc-r12", "and each decision of the owner is a file. Both are rules of the owner."), fact("cc-check", "The end-of-session check of CLAUDE.md asks for a journal entry, the decision files and an update of HANDOFF.md."),
           fact("cc-17k4", "The guide says that a new session with a structured summary is more reliable than one that resumes with stale tool results (1.7-K4).")
           + " " + fact("cc-d01", "The first decision of the build also names 5.4-K2 for the same files:") + " " + fact("cc-54k2", "files that keep key findings across context boundaries."))
        + cc_ts("1.7", "cc-1-7-ts"),
        '<h4 class="story">The summary was not read</h4><p>%s</p>'
        % (fact("cc-notread", "In a session of 7 October 2026, the assistant showed a plan before it read all files that HANDOFF.md names. The owner asked if it had read them. It had not.") + " " + fact("cc-six", "It read them, and changed six points of the plan.")), "how the build used it")),
    cc_part("cc-4-6", "4.6", "A new agent reviews each file", "task statement 4.6", cc_body("cc-4-6",
        '<h4 class="takeaway">A file is checked by an agent that did not write it</h4><p>%s %s</p>'
        % (fact("cc-r15", "A rule of the owner: an independent reviewer checks each file that a new session or a participant will rely on. The reviewer is a new agent that did not make the file."),
           fact("cc-r14", "Another rule: a check must not depend on the memory or the judgment of the assistant alone.")),
        '<p>%s %s %s</p>'
        % (fact("cc-46k1", "The exam guide gives the reason: a model that keeps the reasoning of its own work is less likely to question its decisions (4.6-K1).") + " " + fact("cc-46s1", "So the guide teaches a second, independent Claude instance that reviews without the reasoning of the writer (4.6-S1)."),
           fact("cc-doc-fresh", "In Claude Code, a subagent that is not a fork starts with a fresh context, so it does not see the conversation that made the file."),
           fact("cc-code", "On 7 October 2026, two independent reviewers checked the first code that moves each try, and its tests: the first found 4 serious and 6 minor bugs, the second found 1 serious and 3 minor bugs in the fixes."))
        + '<p>This tab was built the same way: %s %s %s</p>' % (fact("cc-a12", "a fact agent and a review agent for each part,"), fact("cc-a15", "then a whole-picture agent after each group of parts."), fact("cc-46k3", "This matches the multi-pass review of the guide: a pass for each part, plus a pass over the whole (4.6-K3)."))
        + cc_ts("4.6", "cc-4-6-ts"),
        '<h4 class="story">Three checks of all documents</h4>' + FIGCC
        + '<p>Before a push on 9 October 2026, %s %s %s %s</p>'
        % (fact("cc-c1", "an independent agent checked all documents, and the assistant fixed the gaps."),
           fact("cc-c2", "A second independent check, over more files, found %d gaps." % GAPS2),
           fact("cc-c3", "A third check found %d smaller gaps." % GAPS3),
           fact("cc-stop", "No reviewer checked the last 20 fixes. The owner stopped the checks there.")), "how the build used it")),
    cc_part("cc-3-4", "3.4", "Discuss first, not plan mode", "task statement 3.4 · no example in the build", cc_body("cc-3-4",
        '<h4 class="takeaway">The build used a rule to discuss first, not plan mode</h4><p>%s %s</p>'
        % (fact("cc-r8", "A rule of the owner: discuss first, and do not write a document, a diagram or code before the owner asks for it."),
           fact("cc-d23", "No record shows that the build used plan mode or the Explore subagent.")),
        '<p>%s %s The build had a different method: %s %s</p>'
        % (fact("cc-34k1", "The guide teaches plan mode for complex tasks with large changes and architectural decisions (3.4-K1)."),
           fact("cc-doc-plan", "Plan mode lets Claude research and propose changes without making them."),
           fact("cc-r30", "for the design of a step of the mock builder, the assistant showed one proposal with all details, and the owner accepted it or named a change (see step 0)."),
           fact("cc-r12", "Each decision of the owner became a file on the same day.") + " So the discussion did the work of plan mode: a proposal first, and a change only after the owner agreed.")
        + cc_ts("3.4", "cc-3-4-ts"),
        '<h4 class="story">In the academy work, a rule in context was not a block</h4><p>%s %s</p>'
        % (fact("cc-soon", "During the plan of the two tabs of this academy, the assistant moved to the build too soon, and the owner stopped it."),
           fact("cc-doc-context", "As the part on CLAUDE.md above says, a rule in CLAUDE.md is context, not enforced configuration, so the rule only asked the assistant to wait.")), "how the build used it")),
])

# ----- the parts -----

MINI = {s: '<svg class="minimap" viewBox="0 0 126 14" role="img" aria-label="Step %d of the steps 0 to 8">%s</svg>'
        % (s, "".join('<rect x="%d" y="1" width="12" height="12"%s/>' % (i * 14 + .5, ' class="here"' if i == s else "") for i in range(9)))
        for s in range(9)}
SLICE = {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 6: 2, 7: 2, 8: 2}


def ts_of(s):
    """The task statements of a step, in the order of its table of guide points (decision 0024)."""
    f = glob.glob(os.path.join(ROOT, "docs/build-guide/step-%d-*.md" % s))[0]
    ids = re.findall(r"(?m)^\| ([1-5]\.[0-9])-[KS][0-9]+ \|", read(os.path.relpath(f, ROOT)))
    return list(dict.fromkeys(ids))


def part(s):
    who = WHO_LONG[s]
    ts = ts_of(s)
    who += (" · task statement%s " % ("s" if len(ts) > 1 else "") + ", ".join(ts)) if ts else " · no task statement of the exam guide"
    body = step5_html if s == 5 else PART_HTML.get(s, '<p class="pending">This step comes in slice %d.</p>' % SLICE.get(s, 2))
    take, body = take_out(body)
    head, line = (take, e(FULL[s]) + " · " + e(who)) if take else (e(FULL[s]), e(who))
    return ('<details class="part" id="step-%d"><summary><span class="pn">%d</span><span><h3>%s</h3><span class="who">%s</span></span>'
            '<span class="mm">%s<span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (s, s, head, line, MINI[s], body))


PARAGRAPH = read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")
PARAGRAPH = re.search(r"   > (The mock builder is itself.*?)\n", PARAGRAPH).group(1)
TITLE = "Mocks Built with the Same Principles They Test"
assert TITLE in read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")

WORDS = """<details class="level words" id="top-words"><summary><h2>Words on this tab</h2><span class="ve-label">15 words</span></summary><div class="body"><dl class="glossary">
<dt>Mock</dt><dd>A practice exam of %(n)d questions. The mock builder made %(m)d mocks.</dd>
<dt>Slot</dt><dd>%(slot)s</dd>
<dt>Try</dt><dd>One question that the writer writes for a slot. A slot can have more than one try. The last try that passes goes into the mock.</dd>
<dt>Finding</dt><dd>A problem that a check names, with its rule, such as rule B9.</dd>
<dt>Point</dt><dd>One &ldquo;Knowledge of&rdquo; or &ldquo;Skills in&rdquo; point of a task statement of the exam guide, such as 4.4-S1. Tab 1 explains them.</dd>
<dt>Mark</dt><dd>In step 7, a reader marks each question good or bad. A bad mark sends the question back.</dd>
<dt>The owner</dt><dd>%(owner)s</dd>
<dt>IDs and labels</dt><dd>The ID M4-S27-T3 is mock 4, slot 27, try 3. The label 1.4-K2 is a point of the exam guide.</dd>
<dt>Rules</dt><dd>Rules A1 to A12 are checked by code in step 3. Rules B1 to B9 are checked by a model in step 4. Rules C and D are checked over a scenario in step 6.</dd>
<dt>Seed</dt><dd>A number that controls the random choices of the plan in step 1.</dd>
<dt>Rewrite</dt><dd>The owner sends a question back to the writer with a reason.</dd>
<dt>Answer key</dt><dd>%(key)s</dd>
<dt>Idea</dt><dd>%(idea)s</dd>
<dt>Second review</dt><dd>%(sr)s</dd>
<dt>Mock decision</dt><dd>A decision record of the build, such as mock decision 0038. The records are in the repository.</dd>
</dl></div></details>""" % {"n": SLOTS, "m": len(glob.glob(os.path.join(ROOT, "mocks/mock-*.questions.json"))), "slot": fact("w-slot", "The place of one question in the plan of a mock. Step 1 plans %d slots for each mock." % SLOTS),
                         "key": "The correct option or options of a question. The writer marks each option correct or wrong, and gives a reason.",
                         "idea": fact("s1-idea", "A group of points of the guide on one subject. The build put the %d points into %d ideas." % (N_PTS, len(PG))),
                         "sr": fact("s7-what", "A Claude model in a separate chat, outside the program, that read and marked the mocks after the checks. For mocks 4 and 5 it was the only reader."),
                         "owner": fact("w-owner", "The person who directs this work and who made the decisions of the build. The owner passed the CCAR-F exam.")}

# ----- what this shows and what it does not (academy decision 0043, item 4) -----
T24P3 = jread("runs/test-0024/part3.json")
T24D = [c for c in T24P3["checks"] if c["copy"] == "damaged"]
T24B1 = [c for c in T24D if c["rule"] == "B1"]
assert T24P3["as_expected"] == T24P3["of"] and len(T24B1) == 2 and all(c["as_expected"] for c in T24B1)
DEC = lambda n: glob.glob(os.path.join(ROOT, "docs/decisions/%04d-*.md" % n))[0][len(ROOT) + 1:]
assert [S38V[t] for t in range(1, 6)] == ["fail", "fail", "fail", "fail", "pass"], S38V
CARD.update({
    "lim-t24": {"title": "The test before mock 1, part 3", "kind": "count",
                "text": "runs/test-0024/part3.json: %d checks, %d as expected. %d damaged copies, %d of them with the mark 'correct' moved to a wrong option and the reasons swapped (rule B1). Part 3 ran call 4b alone (src/test_0024.py, rules_verdict), not call 4a. The script of this page counted them."
                        % (T24P3["of"], T24P3["as_expected"], len(T24D), len(T24B1)),
                "src": "runs/test-0024/part3.json, src/test_0024.py", "href": link("src/test_0024.py")},
    "lim-cost": {"title": "The cost of the 5 mocks", "kind": "count",
                 "text": "Dollars per mock, all steps of the program: %s. Total: %.2f. The script of this page added the usage records. The tests and the build sessions are not in this sum." % (", ".join("mock %d %.2f" % (i + 1, c[0]) for i, c in enumerate(COST)), sum(c[0] for c in COST)),
                 "src": "runs/mock-0N/usage/*.json", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "lim-m4": excerpt(DEC(69), "so 31 of the 60 questions are close", "Mock decision 0069, known limits of mock 4"),
    "lim-m5": excerpt(DEC(76), "**Known limit:** 46 of the 60 questions of mock 5 are close to a question of an earlier mock.", "Mock decision 0076"),
    "lim-person": excerpt(DEC(71), "**Known limit: no person reads the questions of mocks 4 and 5.**", "Mock decision 0071"),
    "lim-m4r1": excerpt(DEC(69), "the owner states that they did not read the 20 questions of round 1", "Mock decision 0069"),
    "lim-b9": {"title": "The step 4 verdicts of M5-S38", "kind": "count",
               "text": "runs/mock-05/checks/M5-S38-T1-step4.json to T5: %s. Try 5 is the question in mock 5." % ", ".join("try %d %s" % (t, S38V[t]) for t in range(1, 6)),
               "src": "runs/mock-05/checks/M5-S38-T*-step4.json", "href": "%s/tree/%s/runs/mock-05/checks" % (REPO, TAG)},
    "lim-s33": excerpt("runs/mock-05/marks/round-1.json", "Copy of M2-S34", "The marks of mock 5, round 1"),
})
LIMITS = """<section class="parts" id="limits" aria-label="What this shows and what it does not">
  <h2>What this shows and what it does not</h2>
  <p class="lead">The records show how the questions were checked. They show less about how good the questions are.</p>
  <div class="limits">
    <div class="callout"><span class="chip ok">The records show</span><ul class="beyond">
      <li>%(s3)s <a href="#step-3">Step 3 &rarr;</a></li>
      <li>%(s4)s %(t24a)s <a href="#step-4">Step 4 &rarr;</a></li>
      <li>%(spread)s <a href="#step-1">Step 1 &rarr;</a></li>
      <li>%(s33)s <a href="#step-7">Step 7 &rarr;</a></li>
      <li>%(cost)s <a href="#step-4">Step 4 &rarr;</a></li>
    </ul></div>
    <div class="callout"><span class="chip risk">They do not show</span><ul class="beyond">
      <li>%(blind)s %(t24)s So the records cannot show how often step 4 misses a wrong answer key. <a href="#step-4">Step 4 &rarr;</a></li>
      <li>%(m4)s %(m5)s %(all5)s <a href="#step-1">Step 1 &rarr;</a></li>
      <li>%(person)s %(m4r1)s <a href="#step-7">Step 7 &rarr;</a></li>
      <li>%(b9)s <a href="#step-5">Step 5 &rarr;</a></li>
      <li>Nobody compared the difficulty or the style of the mocks with the real exam. The mocks follow the task statements and the scenarios of the guide. %(owner)s</li>
    </ul></div>
  </div>
</section>""" % {
    "s3": fact("s3-what", "Today, code checks 12 rules that have one exact answer. Mock 1 had 11."),
    "s4": fact("s4-what", "A model checks the rules that need judgment, in two calls, and code makes the verdict."),
    "t24a": fact("s4-t24", "Before mock 1, call 4a answered %d of the %d sample questions of the guide right." % (T24["right"], T24["of"])),
    "spread": fact("s1-spread", "%d of the %d ideas are in 2 to 4 mocks." % (sum(SPREAD[k] for k in (2, 3, 4)), len(PG))),
    "s33": fact("lim-s33", "The reader of step 7 found that M5-S33 was a copy of a question of mock 2, and the question was written again."),
    "cost": fact("lim-cost", "The program runs of the %d mocks cost %.2f dollars, for all steps. The tests and the build sessions are not in this sum." % (len(COST), sum(c[0] for c in COST))),
    "blind": fact("s4-runs", "Call 4a was never tested with a wrong answer key. In the %d checks of the 5 mocks, it never selected letters other than the answer key." % sum(V4.values())),
    "t24": fact("lim-t24", "A test before mock 1 gave call 4b alone two questions with a wrong answer key and swapped reasons, and call 4b failed both."),
    "m4": fact("lim-m4", "31 of the 60 questions of mock 4 are close to a question of an earlier mock,"),
    "m5": fact("lim-m5", "and 46 of the 60 of mock 5."),
    "all5": fact("s1-spread", "%d ideas are in all %d mocks." % (SPREAD[5], N_MOCKS)),
    "person": fact("lim-person", "No person read the questions of mocks 4 and 5."),
    "m4r1": fact("lim-m4r1", "For mock 4, the owner recorded 20 good marks without reading the questions, and a Claude model was the second reader."),
    "b9": fact("lim-b9", "Rule B9 did not stop each repeat. Try 5 of M5-S38 wrote the old problem again and passed step 4."),
    "owner": fact("w-owner", "The owner passed the CCAR-F exam."),
}

BODY = """<main>
<header id="top">
  <nav class="tabs" aria-label="Tabs"><a href="%(tab1)s">Exam guide breakdown</a><span aria-current="page">Behind the mocks</span></nav>
  <h1>%(title)s</h1>
  <p class="lead">%(para)s</p>
  %(words)s
</header>
%(fig1)s
<section class="parts" id="steps" aria-label="The 9 steps">
  <h2>The 9 steps</h2>
  %(parts)s
</section>
<section class="parts" id="claude-code" aria-label="The build in Claude Code">
  <h2>The build in Claude Code</h2>
  <p class="lead">The mock builder was itself built with Claude Code. The owner gave the assistant rules in a file of the repository. These parts show where that build used a task statement of the exam, and one where it did not.</p>
  %(cc)s
</section>
%(limits)s
</main>""" % {"tab1": TAB1, "title": e(TITLE), "para": e(PARAGRAPH).replace("&#x27;", "&rsquo;").replace("'", "&rsquo;"),
             "fig1": FIG1, "parts": "".join(part(s) for s in range(9)), "words": WORDS, "cc": CC_HTML, "limits": LIMITS}

# an SVG keeps its drawn size on a narrow screen, and its frame scrolls, so no label is below 12 pixels
BODY = re.sub(r'<svg class="(ve-svg|ve-bars)" viewBox="0 0 (\d+) ', lambda m: '<svg class="%s" style="min-width:%spx" viewBox="0 0 %s ' % (m.group(1), m.group(2), m.group(2)), BODY)
TOP = BODY.split('<section class="parts" id="steps"')[0]
from popups import POPUPS  # noqa: E402
BODY = add_popups(BODY, POPUPS, 2, POP)   # the popups of the boxes (academy/popup-plan.md)
BODY = group_roles(BODY)   # academy decision 0043, item 6
BODY = code_font(BODY)   # academy decision 0038
BODY = BODY.replace("@SOURCES_TOP@", sources(list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', TOP)))), 1)
USED = set(re.findall(r'data-card="([^"]+)"', BODY))
assert USED <= set(CARD), USED - set(CARD)
CARD = {k: v for k, v in CARD.items() if k in USED}
POP = {k: v for k, v in POP.items() if 'data-step="%s"' % k in BODY}

write("behind-the-mocks.html", page("Behind the mocks: " + TITLE, BODY, "behind-the-mocks.js",
                                    "How the mock builder of the CCAR-F mocks works, step by step."))
script_file("behind-the-mocks.js", POP, CARD)
print("Wrote academy/pages/behind-the-mocks.html and behind-the-mocks.js: %d preview cards, %d popups." % (len(CARD), len(POP)))
print("Numbers: tries %s (total %d), more than one try %s, opened %s, cannot decide or cannot write %d, tests %d."
      % ([x["tries"] for x in MOCKS], TOTAL_TRIES, [x["more"] for x in MOCKS], [x["opened"] for x in MOCKS], TOTAL_CANNOT, TESTS))
