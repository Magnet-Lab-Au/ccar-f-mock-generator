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
from lib import (REPO, ROOT, TAG, code_block, e, excerpt, fact, lines_of, link, number, page, read,  # noqa: E402
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
    "w-forced": excerpt("docs/sources/2026-10-07-anthropic-docs-define-tools.md", "| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://anthropic.com/glasswing)", "Anthropic documentation, Define tools, copy of 7 October 2026 (the live page agreed on 13 October 2026)", kind="docs"),
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
    "b-fix": code_block(CONTROL, "# more_tries: the last try before the decision.", "return self._step5(request, last, self._check_findings(last) + owner)", "The fix of decision 0074"),
    "b-first": code_block(CONTROL, "if in_round:", "return self._step5(request, failed, self._check_findings(failed))", "The branch that runs first: a failed try of this start"),
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


DEVIATION = "The newest Claude models reject a forced tool call, so the build sends its form as structured outputs."
lines_of(S5, "The reason: the newest Claude models reject it.")


def table_use(point):
    """How step 5 uses a point, from the table of guide points in the build guide (decision 0024), with its point ID."""
    row = next(l for l in read(S5).split("\n") if l.startswith("| %s |" % point))
    use = row.split(" | ")[-1].rstrip(" |").replace("The same context. ", "")
    return "%s: %s" % (point, use.replace(" (see the deviation above)", ""))


POP = {
    "ts-44": {"who": "Task statement 4.4", "cls": "model", "title": TS["4.4"]["title"],
              "sent": ["How step 5 uses each point:", table_use("4.4-K1"), table_use("4.4-S1"), table_use("4.4-K2")],
              "points": pts("4.4-K1", "4.4-S1", "4.4-K2")},
    "ts-11": {"who": "Task statement 1.1", "cls": "model", "title": TS["1.1"]["title"],
              "sent": ["How step 5 uses the point:", table_use("1.1-S3")], "points": pts("1.1-S3")},
    "ts-43": {"who": "Task statement 4.3", "cls": "model", "title": TS["4.3"]["title"],
              "sent": ["How step 5 uses each point:", table_use("4.3-K1"), table_use("4.3-S3"),
                       "Why: " + DEVIATION + " The Anthropic documentation, page \"Define tools\", says that a forced tool call returns a 400 error on Claude Opus 5.5 (read on 7 October 2026, and again on 13 October 2026).",
                       "For the exam: the exam guide teaches the forced tool call (tool_choice). Answer the exam with it."],
              "points": pts("4.3-K1", "4.3-S3")},
}
for k in POP:
    POP[k].setdefault("example", None)
POP = {"step-5-" + k: v for k, v in POP.items()}   # each key starts with its part (decision 0033)

# ----- the figures -----

GL_CODE = "M5 2L0 8l5 6M11 2l5 6-5 6"
GL_CLAUDE = "M8 0v16M0 8h16M2.5 2.5l11 11M13.5 2.5l-11 11"
GL_OWNER = "M8 1a3.2 3.2 0 1 1 0 6.4a3.2 3.2 0 1 1 0-6.4M1.5 16c0-4 3-6 6.5-6s6.5 2 6.5 6"


def box(x, y, w, h, lines, sub=None, cls="", glyph=None, href=None, step=None, card=None, num=None):
    """A node: square corners, one or two title lines, an optional sub line."""
    attrs = ""
    if step:
        attrs = ' data-step="%s" tabindex="0" role="button" aria-expanded="false"' % step
    if card:
        attrs = ' data-card="%s" tabindex="0" role="button" aria-expanded="false"' % card
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
        out = '<a href="%s" aria-label="%s">%s</a>' % (href, e(" ".join(lines)), out)
    return out


def edge(d, label=None, lx=0, ly=0, cls="", anchor=""):
    out = '<path class="ve-e %s" d="%s"/>' % (cls, d)
    if label:
        out += '<text class="ve-el %s" x="%d" y="%d">%s</text>' % (anchor, lx, ly, e(label))
    return out


# Fig. 1: the 9 steps (facts: top-of-tab-2.md, sections 1 and 2)
W, H = 150, 92
# who does the step: the form of the box says it (thin = code, thick = a Claude model, dotted = the owner)
WHO = {0: ("code", ""), 1: ("code", ""), 2: ("Claude", "who-model"), 3: ("code", ""), 4: ("Claude + code", "who-model"),
       5: ("Claude", "who-model"), 6: ("code + Claude", "who-model"), 7: ("owner or Claude", "who-owner"), 8: ("code", "")}
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


def step_node(s):
    x, y = POS[s]
    who, cls = WHO[s]
    return box(x, y, W, H, NAMES[s], sub=who, cls=cls + (" is-key" if s == 5 else ""), href="#step-%d" % s, num=s)


LEGEND = ('<g transform="translate(250 22)">'
          '<text class="ve-lab" x="0" y="10">Each box links to its step below.</text>'
          '<g class="ve-n"><rect class="sh" x="0" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="36" y="44">code</text>'
          '<g class="ve-n who-model"><rect class="sh" x="110" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="146" y="44">a Claude model</text>'
          '<g class="ve-n who-owner"><rect class="sh" x="290" y="30" width="28" height="18" rx="0"/></g><text class="ve-lab" x="326" y="44">the owner</text>'
          '<path class="ve-e" d="M0 76H40"/><text class="ve-lab" x="50" y="80">automatic</text>'
          '<path class="ve-e is-async" d="M150 76H190"/><text class="ve-lab" x="200" y="80">a decision of the owner</text>'
          '<path class="ve-e is-hot" d="M420 76H460"/><text class="ve-lab" x="470" y="80">the automatic loop</text></g>')

FIG1 = """
<figure data-figure="builder" id="top-fig-a">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 880 570" role="img" aria-label="The 9 steps of the mock builder. Step 0 prepares the guide records once for each version of the exam guide. Step 1 plans 60 slots. Step 2 writes a question, step 3 checks it by code and step 4 by a model. A try that fails goes to step 5 and is checked again. When all 60 slots pass, step 6 checks the complete mock, step 7 marks the questions, and step 8 builds the files after the owner accepts. Dashed arrows are decisions of the owner: more tries or a new point for an open slot, a rewrite after step 6 or after the marks, a bad mark, and accept. A rewrite with a new point goes to step 2.">
      %(edges)s
      %(nodes)s
      <g class="ve-n who-owner"><rect class="sh" x="230" y="310" width="150" height="92" rx="0"/><text x="305" y="344">open slot</text><text class="sub" x="305" y="368">waits for owner</text></g>
      %(legend)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. A</span>Code moves each try through the steps. %(auto)s. %(wait)s: an open slot, a finding of step 6, a bad mark, and a call that fails 3 times. Since mock decision 0045, %(rw)s also waits for the owner. %(rwp)s The owner %(acc)s before step 8.</figcaption>
  <section class="sources" aria-label="Sources of Fig. A"><p class="ve-label">Sources of Fig. A</p><ul>@SOURCES_TOP@</ul></section>
</figure>
""" % {
    "nodes": "".join(step_node(s) for s in range(9)),
    "legend": LEGEND,
    "edges": "".join([
        edge("M95 112V160", "guide records", 103, 141, anchor="r"),
        edge("M170 206H250", "%d slots" % SLOTS, 210, 197),
        edge("M400 206H480", "question", 440, 197),
        edge("M630 206H710", "passes", 670, 197),
        edge("M525 252V310", "fails", 517, 286, cls="is-hot", anchor="l"),
        edge("M760 252V356H630", cls="is-hot") + '<text class="ve-el l" x="752" y="298">fails or</text><text class="ve-el l" x="752" y="316">cannot decide</text>',
        edge("M585 310V252", "new try", 593, 278, cls="is-hot", anchor="r"),
        edge("M480 340H380", "3 tries", 430, 331),
        edge("M380 380H480", "more tries", 430, 372, cls="is-async"),
        edge("M305 310V252", "new point", 313, 286, cls="is-async", anchor="r"),
        edge("M820 252V460", "all %d pass" % SLOTS, 812, 384, anchor="l"),
        edge("M710 506H630", "then", 670, 497),
        edge("M480 506H400", "accepts", 440, 497, cls="is-async"),
        edge("M780 460V420H615V402", "rewrite", 700, 411, cls="is-async"),
        edge("M525 460V402", "bad mark, rewrite", 533, 446, cls="is-async", anchor="r"),
    ]),
    "auto": fact("c-auto", "A try that fails step 3 or step 4 goes to step 5, where the writer of step 2 tries again by itself"),
    "wait": fact("c-wait", "Each other way back waits for a decision of the owner"),
    "rw": fact("c-rw", "a rewrite after the marks"),
    "acc": fact("c-acc", "accepts the mock"),
    "rwp": fact("c-rwp", "A rewrite with a new point starts again at step 2. The figure does not draw this arrow, or the choice of a new plan."),
}

# Fig. 5-1: the loop of step 5 (facts: step-5.md, sections 2.1 to 2.3)
FIG51 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 400" role="img" aria-label="The writer, a Claude model, writes a try. Step 3 checks it by code and step 4 by a model. A pass stops the loop. A try that fails goes back to the writer with a new request: the request of step 2, the failed try and its findings. After %(t)d failed tries in one start, the slot is open and waits for the owner.">
      %(edges)s
      %(nodes)s
      <g class="ve-dim"><path class="ext" d="M20 300V330M640 300V330"/><path class="ln" d="M20 320H640M16 324l8-8M636 324l8-8"/><text x="330" y="312">at most %(t)d tries in one start</text></g>
      <g class="ve-n who-owner"><rect class="sh" x="20" y="340" width="620" height="44" rx="0"/><text x="330" y="362">after the last failed try: an open slot, the owner decides</text></g>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 5-1</span>%(pass)s The limit of %(t)d tries is only a guard. %(open)s</figcaption>
</figure>
""" % {
    "t": TRIES,
    "nodes": "".join([
        box(20, 30, 160, 80, ["Writer"], sub="Claude", cls="who-model"),
        box(250, 30, 160, 80, ["Step 3"], sub="check by code"),
        box(480, 30, 160, 80, ["Step 4"], sub="check by a model", cls="who-model"),
        box(710, 30, 160, 80, ["passed"], sub="the loop stops", cls="try ok"),
        box(250, 180, 390, 90, ["new request of step 5"], sub="step 2 + failed try + findings", cls="is-key"),
    ]),
    "edges": "".join([
        edge("M180 70H250", "a try", 215, 61),
        edge("M410 70H480", "passes", 445, 61),
        edge("M640 70H710", "passes", 675, 61),
        edge("M330 110V180", "fails", 338, 150, cls="is-hot", anchor="r"),
        edge("M560 110V180", "fails", 568, 150, cls="is-hot", anchor="r"),
        edge("M250 225H100V110", "tries again", 175, 216, cls="is-hot"),
    ]),
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
            '<svg class="ve-grid" viewBox="0 0 227 135" role="img" aria-label="Mock %d: %d tries for %d slots. %d slots passed both checks at the first try. %d slots had more than one try. The most tries for one slot: %d.">%s</svg>'
            '<p class="cap">%d of %d passed both checks at the first try</p></div>'
            % (x["mock"], x["tries"], x["mock"], x["tries"], SLOTS, x["first"], x["more"], x["max"], "".join(cells),
               x["first"], SLOTS))


FIG52 = """
<figure>
  <div class="cases">%s</div>
  <figcaption><span class="fig-n">Fig. 5-2</span>One square for each slot. A darker square had more tries, and its number is the tries. The number also counts new tries after a rewrite or a bad mark of the owner. So a slot can pass both checks at the first try and still have a number. %s %s</figcaption>
</figure>
""" % ("".join(grid(x) for x in MOCKS),
       fact("s5-counts", "The 5 mocks needed %d tries for %d questions." % (TOTAL_TRIES, 5 * SLOTS)),
       "In %d cases a slot stopped at the limit of tries and waited for the owner. The limit of %d results &ldquo;cannot decide&rdquo; never stopped a slot."
       % (TOTAL_OPENED, CANNOT))

# Fig. 5-3: the review loop (story a)
FIG53_T = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 150" role="img" aria-label="The first review found 14 serious items. The second review found 10 new ones. The fix: one automatic loop, each other failure waits for the owner, and the rules of the next action are code with tests.">
      <path class="ve-e" d="M250 60H318"/><text class="ve-el" x="284" y="51">answers</text>
      <path class="ve-e is-hot" d="M560 60H628"/><text class="ve-el" x="594" y="51">fix</text>
      <g class="ve-n"><rect class="sh" x="20" y="20" width="230" height="80" rx="0"/><text x="135" y="44">first review</text>
        <rect class="bar" x="40" y="62" width="140" height="16" rx="0"/><text class="sub" x="210" y="70">14</text></g>
      <g class="ve-n"><rect class="sh" x="320" y="20" width="240" height="80" rx="0"/><text x="440" y="44">second review</text>
        <rect class="bar" x="340" y="62" width="100" height="16" rx="0"/><text class="sub r" x="452" y="70">10 new</text></g>
      <g class="ve-n is-key"><rect class="sh" x="630" y="20" width="240" height="80" rx="0"/><text x="750" y="44">the rules are code</text><text class="sub" x="750" y="70">with tests</text></g>
      <text class="ve-lab" x="20" y="130">bar length = number of serious items</text>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 5-3</span>%s The owner said: &ldquo;%s&rdquo;</figcaption>
</figure>
"""
FIG53_T = (FIG53_T.replace('found 14 serious items. The second review found 10 new', 'found @R1@ serious items. The second review found @R2@ new')
           .replace('width="140" height="16" rx="0"/><text class="sub" x="210" y="70">14</text>', 'width="%d" height="16" rx="0"/><text class="sub" x="210" y="70">@R1@</text>' % (REVIEW1 * 10))
           .replace('width="100" height="16" rx="0"/><text class="sub r" x="452" y="70">10 new</text>', 'width="%d" height="16" rx="0"/><text class="sub r" x="452" y="70">@R2@ new</text>' % (REVIEW2 * 10))
           .replace("@R1@", str(REVIEW1)).replace("@R2@", str(REVIEW2)))
assert "14" not in FIG53_T.split("<figcaption>")[0].replace("140", "") or REVIEW1 == 14
FIG53 = FIG53_T % (fact("a-reviews", "A first review found %d serious items. A second review found %d new ones, and most of them came from the rules that answered the first." % (REVIEW1, REVIEW2)),
       fact("a-quote", "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue."))

# Fig. 5-4: M5-S38 (story b)


def tbox(t, x, lines, sub, cls):
    return box(x, 60, 150, 80, lines, sub=sub, cls="try " + cls)


FIG54 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 250" role="img" aria-label="Question M5-S38 of mock 5. Tries 1 to 3 fail rule B9. The owner gives more tries with a reason. Try 4 gets the reason, puts a custom ID into its correct options and fails rule B9, because it repeats questions of mocks 1 and 3. Try 5 does not get the reason, writes the old problem again and passes.">
      %(edges)s
      %(nodes)s
      <g class="ve-n who-owner"><rect class="sh" x="500" y="2" width="200" height="36" rx="0"/><text x="600" y="20">owner: more tries</text></g>
      <g class="ve-dim"><path class="ext" d="M530 150V190M870 150V190"/><path class="ln" d="M530 180H870M526 184l8-8M866 184l8-8"/><text x="700" y="172">a new start</text></g>
      <text class="ve-lab" x="20" y="230">B9: the question repeats the problem of a question of an earlier mock.</text>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 5-4</span>The reason of the owner reached try 4, but not try 5. Try 5 is the question in mock 5.</figcaption>
</figure>
""" % {
    "nodes": "".join([tbox(1, 20, ["Try 1"], "fails B9", "bad"), tbox(2, 190, ["Try 2"], "fails B9", "bad"),
                      tbox(3, 360, ["Try 3"], "fails B9", "bad"),
                      box(530, 60, 150, 80, ["Try 4"], sub="custom ID: fails B9", cls="try bad", card="b-t4"),
                      box(720, 60, 150, 80, ["Try 5"], sub="no reason: passes", cls="try ok", card="b-t5")]),
    "edges": "".join([edge("M170 100H190"), edge("M340 100H360"), edge("M510 100H530"), edge("M680 100H720"),
                      edge("M600 38V60", "the reason", 608, 52, cls="is-hot", anchor="r"),
                      '<path class="ve-e is-async" d="M700 30H795V60"/><text class="ve-el r" x="803" y="44">not sent</text>']),
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
    <p>The run files and the code show more. Try 4 got the reason and put a custom ID into its correct options: %(t4)s It failed B9, %(t4f)s. Try 2, before the reason, had already tried a custom ID and %(t2f)s. Try 5 did not get the reason. In the code, %(first)s runs before the fix, and the test checks only the first try after the decision. Try 5 wrote the old problem again: %(t5)s It passed, and it is the question in mock 5. Mock decision 0074 says: %(said)s The code shows that only the first try of the new start got the instruction. The code still works this way. %(limit)s</p>
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
    "what": f("s5-what", "A question that fails step 3 or step 4 goes back to the writer, with the failed try and its exact findings."),
    "again": f("s5-again", "The new try goes through steps 3 and 4 again."),
    "pass": f("s5-pass", "A question that passes stops the loop."),
    "one": f("c-auto", "This is the one automatic loop of the mock builder."),
    "fig51": FIG51,
    "short": f("s5-short", "The writer does not see older tries, so the request stays short."),
    "three": f("s5-three", "the original, the failed result and the errors (point 4.4-S1 of the exam guide)."),
    "guard": f("s5-guard", "Each start of a slot has at most %d tries. %d results &ldquo;cannot decide&rdquo; of step 4 also stop it." % (TRIES, CANNOT)),
    "file": f("s5-file", "Each try is a new file. No file is written over, so the history of each question stays."),
    "fig52": FIG52,
    "ts": ts_chip("ts-44", "4.4") + ts_chip("ts-11", "1.1") + ts_chip("ts-43", "4.3"),
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
    out = []
    for l in read(step_file(n)).split("\n"):
        m = re.match(r"^\| ([1-5]\.[0-9]-[KS][0-9]+) \|", l)
        if m:
            out.append((m.group(1), l.split(" | ")[-1].rstrip(" |").replace("The same context. ", "")))
    return out


def ts_block(n, extra=None):
    """A chip for each task statement of a step, each with its popup, and the links to tab 1."""
    rows, chips = table_rows(n), []
    for tsid in dict.fromkeys(p.split("-")[0] for p, _ in rows):
        key = "step-%d-ts-%s" % (n, tsid.replace(".", "-"))
        mine = [(p, u) for p, u in rows if p.startswith(tsid + "-")]
        POP[key] = {"who": "Task statement " + tsid, "cls": "model", "title": TS[tsid]["title"], "example": None,
                    "sent": ["How step %d uses %s:" % (n, "each point" if len(mine) > 1 else "the point")]
                            + ["%s: %s" % (p, u) for p, u in mine] + ((extra or {}).get(tsid) or []),
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


def level(kind, body):
    if kind == "overview":
        return '<section data-level="overview" aria-label="Overview"><p class="lvl1">Overview &middot; 30 seconds</p>%s</section>' % body
    if kind == "explanation":
        return ('<details class="level" data-level="explanation"><summary><h4>Explanation</h4><span class="ve-label">3 minutes</span></summary>'
                '<div class="body">%s</div></details>' % body)
    return ('<details class="level" data-level="depth"><summary><h4>Depth</h4><span class="ve-label">what went wrong, and the fix</span></summary>'
            '<div class="body">%s<section class="sources" aria-label="Sources of step @N@"><p class="ve-label">Sources of step @N@. '
            'Each underlined fact opens its card.</p><ul>@SOURCES@</ul></section></div></details>' % body)


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
        box(740, 40, 130, 90, ["steps"], sub="1, 2, 4, 5, 7, 8"),
        box(260, 190, 190, 70, ["no file"], sub="and the cause", cls="try bad"),
        box(520, 190, 170, 70, ["second script"], sub="%d of %d checks" % (N_CHECKS, N_CHECKS), cls="try ok"),
    ]),
    "edges": "".join([
        edge("M190 85H260", "reads", 225, 76),
        edge("M450 85H520", "writes", 485, 76, cls="is-hot"),
        edge("M690 85H740", "parts", 715, 76),
        edge("M355 130V190", "a check fails", 363, 165, anchor="r"),
        edge("M605 190V130", "checks", 613, 165, anchor="r"),
    ]),
    "cap": fact("s0-what", "A script copies the parts of the exam guide that later steps need into one file. No model copies text.")
           + " " + fact("s0-slice", "A later step takes the parts that it needs, by ID."),
}

STEP0 = (level("overview",
               '<h4 class="takeaway">A script copies the exam guide into records, once</h4>'
               '<p>%s %s %s %s</p>'
               % (fact("s0-what", "Before the first mock, a script copies the parts of the exam guide that the later steps need into one file of records. No model copies text."),
                  fact("s0-once", "It runs once for each version of the guide, not once for each mock."),
                  fact("s0-has", "The file has the %d domains, %d scenarios, %d task statements, %d points and %d sample questions of the guide." % (len(REC["domains"]), len(REC["scenarios"]), len(REC["task_statements"]), N_PTS, len(REC["sample_questions"]))),
                  fact("s0-slice", "A later step takes the parts that it needs from the file, by ID.")))
         + level("explanation",
                 FIG01
                 + '<p><b>IDs.</b> %s So 1.4-K2 is the second &ldquo;Knowledge of&rdquo; bullet of task statement 1.4. %s</p>'
                   % (fact("s0-ids", "Each point gets an ID that the guide does not have: the task statement, then K (Knowledge of) or S (Skills in), then the number of the bullet."),
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
                 '<p>%s It had no source for the story and no fields. %s The fix: %s %s</p>'
                 '<p>One more correction came earlier. %s So step 0 has a number, a decision and a box in Fig. A.</p>'
                 '<p>No source records a failure of the script or of the file. %s</p>'
                 % (fact("s0-a1", "Early in the design, a proposal for step 2 said &ldquo;the story of the scenario&rdquo; and &ldquo;a fixed form with fields&rdquo;."),
                    fact("s0-a2", "The cause: the plan of work started at step 1, but each step reads the records of step 0."),
                    fact("s0-a3", "step 0 was designed and run before step 2, and each design names the exact file format and fields."),
                    fact("s0-rule", "Working rule 30 has the same words: each design proposal names the exact file format and the exact fields."),
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
      <text class="ve-lab" x="276" y="44">code applies, in this order:</text>
      %(rules)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 1-1</span>%(cap)s</figcaption>
</figure>""" % {
    "dc": ", ".join(map(str, DC)), "nts": N_TS, "sc": SCEN_IN_MOCK, "ps": PER_SCEN, "mr": MR_PER, "n": SLOTS,
    "nodes": "".join([
        box(20, 30, 170, 56, ["guide records"]), box(20, 100, 170, 56, ["ideas"], sub="%d groups of points" % len(PG)),
        box(20, 170, 170, 56, ["earlier mocks"], sub="built only"), box(20, 240, 170, 56, ["a seed"], sub="a number"),
        box(700, 125, 170, 80, ["the plan"], sub="%d slots" % SLOTS),
    ]),
    "edges": "".join([edge("M190 58H260"), edge("M190 128H260"), edge("M190 198H260"), edge("M190 268H260"),
                      edge("M630 165H700", "writes", 665, 156, cls="is-hot")]),
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
  <figcaption><span class="fig-n">Fig. 1-2</span>The guide contrasts a fixed sequence with a decomposition that changes with what the work finds (1.6-K1). Step 1 uses one idea of the fixed side: %s.</figcaption>
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
                      fact("s1-spread", "Over the %d built mocks, %d of the %d ideas are in 2 to 4 mocks." % (N_MOCKS, sum(SPREAD[k] for k in (2, 3, 4)), len(PG)))))
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
    "s2-what": excerpt(S2, "For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock.", "Build guide, step 2"),
    "s2-why": excerpt(D10, "One call makes one record with one ID, so each later verdict connects to exactly one question. If one question fails, the program writes that one again and the others do not change.", "Mock decision 0010, Reason"),
    "s2-cost": excerpt(D10, "We accepted one disadvantage: a writer that sees one slot does not see the other questions of its scenario.", "Mock decision 0010, How we decided"),
    "s2-model": {"title": "The model of each try", "kind": "count", "text": "All %d question files of mocks 1 to 5 have the model %s. None has the status cannot_write. The script of this page counted them." % (sum(MODELS.values()), MODEL),
                 "src": "runs/mock-0N/questions/", "href": "%s/tree/%s/runs" % (REPO, TAG)},
    "s2-cache": code_block("src/step2_write.py", "# Decision 0067: the rules come first as a cached block.", "cached=[rules_for(request)])", "The rules come first, as a cached block"),
    "s2-letters": excerpt(D41, "Code mixes the options with the seed of the plan, the slot ID and the question text. So the same answer always gets the same letters.", "Mock decision 0041, Decision"),
    "s2-samplea": excerpt(D29, "in the 12 sample questions of the guide, the correct answer is A 10 times and B 2 times. A model that sees those examples can copy that.", "Mock decision 0029, Reason"),
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
    "s2-enough": excerpt(D43, "The owner asked: \"but is that enough? Only in the prompt?\" An instruction alone fails sometimes, so a check comes after it.", "Mock decision 0043, Reason"),
    "s2-b7": excerpt(D43, "1. **The instruction to the writer** (step 2, and so also step 5): \"Use one name for one actor. Write each sentence so that a reader understands it at the first reading.\"", "Mock decision 0043, Decision"),
})

REQ = [("cached", "the rules: A1 to A12 and B1 to B9"), ("", "the role and the form"),
       ("", "3 sample questions of the guide"), ("", "the story of the scenario"),
       ("", "the task statement, its point marked"), ("", "the %d technologies of the guide" % N_TECH),
       ("", "the slot: type, options, answers"), ("if any", "earlier questions on the idea"),
       ("step 5", "the failed try and its findings")]
FIG21 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 %(h)d" role="img" aria-label="Step 2. Code builds one request for one slot: the rules first as a cached block, the role and the form, 3 sample questions of the guide, the story, the task statement with its point marked, the technologies, the slot, the earlier questions on the idea if any, and for step 5 the failed try with its findings. One Claude call answers in the form. Code then mixes the options and gives the letters, and saves one file for the try.">
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
    "edges": "".join([edge("M400 170H480", "sends", 440, 161, cls="is-hot"), edge("M640 170H700", "answers", 670, 161)]),
    "nodes": "".join([box(480, 120, 160, 100, ["Claude"], sub="one new call", cls="who-model"),
                      box(700, 120, 170, 100, ["the form"], sub="question, options", cls=""),
                      box(700, 250, 170, 70, ["code"], sub="mixes, gives letters")]) + edge("M785 220V250"),
    "cap": fact("s2-what", "For each slot, one new Claude call writes one question. It does not know the other questions of the mock."),
}

STEP2 = (level("overview",
               '<h4 class="takeaway">One new Claude call writes each question, from a request that code builds</h4><p>%s %s Code builds the request from the guide records and the plan, and %s</p>'
               % (fact("s2-what", "For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock."),
                  fact("s2-why", "One call makes one record, so each later verdict connects to exactly one question, and a failed question is written again alone."),
                  fact("s2-letters", "code, not the model, mixes the options and gives the letters.")))
         + level("explanation",
                 FIG21
                 + '<p><b>The rules come first.</b> %s The writer gets the same rules that steps 3 and 4 check, so each instruction is also checked. %s</p>'
                   % (fact("s2-cache", "The list of rules is the first block of each request, with a cache mark, so a repeated list costs less."), fact("s2-model", "Each of the %d tries of the 5 mocks used %s." % (sum(MODELS.values()), MODEL)))
                 + '<p><b>The form.</b> %s The guide teaches a forced tool call for this. The newest Claude models reject a forced tool call, so the build sends a JSON schema as structured outputs. For the exam, answer with the forced tool call that the guide teaches.</p>'
                   % fact("s2-form", "The writer answers in a fixed form: the question, and for each option its text, whether it is correct, and a short reason.")
                 + '<p><b>The letters.</b> %s So %s</p>'
                   % (fact("s2-samplea", "In the %d sample questions of the guide, the correct answer is A %d times and B %d times, and a model can copy that." % (len(REC["sample_questions"]), SAMPLE_A["A"], SAMPLE_A["B"])),
                      fact("s2-letters", "code mixes the options and gives the letters."))
                 + '<p><b>The cost of one call per slot.</b> %s Step 6 checks the questions of a scenario together.</p>' % fact("s2-cost", "The writer sees one slot, so it cannot see the other questions of its scenario.")
                 + ts_block(2))
         + level("depth",
                 '<h4 class="story">The writer did not know the earlier mocks</h4>'
                 '<p>%s Example on one idea, the stop of an agentic loop:</p>'
                 '<ol class="checks"><li>Mock 1, M1-S28: %s</li><li>Mock 2, M2-S08, try 1: %s</li></ol>'
                 '<p>The owner sent it back: %s The new try asked for the cause instead: %s</p>'
                 '<p>The fix for step 2: %s An instruction alone was not enough, so step 4 got rule B9 to check it.</p>'
                 '<h4 class="story">The first bad mark became an instruction and a check</h4>'
                 '<p>In the first test of the writer, the owner marked one question bad: &ldquo;%s&rdquo; %s %s Step 4 got rule B7 for the same thing.</p>'
                 '<h4 class="story">The design forced a tool call</h4>'
                 '<p>%s Before the code was written, the documentation showed that the newest models reject it. So %s The code never had a forced tool call, and %s</p>'
                 % (fact("s2-did", "In mock 2, the writer did not know mock 1. On a shared idea it wrote the most obvious scene again, often with the same wrong options."),
                    fact("s2-m1", "the correct answer checks stop_reason and continues while it is &ldquo;tool_use&rdquo;."),
                    fact("s2-m2a", "the correct answer again continues while stop_reason is &ldquo;tool_use&rdquo;."),
                    fact("s2-d001", "&ldquo;Use a different scene and a different angle: the cause, the fix, or a choice between rules.&rdquo;"),
                    fact("s2-m2b", "a fixed cap of 12 iterations as the main stopping rule."),
                    fact("s2-earlier", "when the idea of a slot is in an earlier mock, the writer gets the earlier questions on that idea, with the mark of each option."),
                    fact("s2-bad", "The question is confusing and needs calrification. I had to read the question more than one time."),
                    fact("s2-enough", "The assistant first suggested an instruction only. The owner asked: &ldquo;but is that enough? Only in the prompt?&rdquo;"),
                    fact("s2-b7", "So the writer got the instruction &ldquo;Use one name for one actor&rdquo;."),
                    fact("s2-forced", "The first design said that the request forces the model to call a tool."),
                    fact("s2-form", "the build chose structured outputs: a JSON schema in each request."),
                    fact("s2-test", "a test checks that no request has a tool.")))
         ).replace("@N@", "2")
PART_HTML[2] = with_sources(2, STEP2)

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
    who += " · task statements " + ", ".join(ts) if ts else " · no task statement of the exam guide"
    body = step5_html if s == 5 else PART_HTML.get(s, '<p class="pending">This step comes in slice %d.</p>' % SLICE.get(s, 2))
    return ('<details class="part" id="step-%d"><summary><span class="pn">%d</span><span><h3>%s</h3><span class="who">%s</span></span>'
            '<span class="mm">%s<span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (s, s, e(FULL[s]), e(who), MINI[s], body))


PARAGRAPH = read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")
PARAGRAPH = re.search(r"   > (The mock builder is itself.*?)\n", PARAGRAPH).group(1)
TITLE = "Mocks Built with the Same Principles They Test"
assert TITLE in read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")

WORDS = """<details class="level words" id="top-words"><summary><h2>Words on this tab</h2><span class="ve-label">8 words</span></summary><div class="body"><dl class="glossary">
<dt>Mock</dt><dd>A practice exam of %(n)d questions. The mock builder made %(m)d mocks.</dd>
<dt>Slot</dt><dd>%(slot)s</dd>
<dt>Try</dt><dd>One question that the writer writes for a slot. A slot can have more than one try. The last try that passes goes into the mock.</dd>
<dt>Finding</dt><dd>A problem that a check names, with its rule, such as rule B9.</dd>
<dt>Point</dt><dd>One &ldquo;Knowledge of&rdquo; or &ldquo;Skills in&rdquo; point of a task statement of the exam guide, such as 4.4-S1. Tab 1 explains them.</dd>
<dt>Mark</dt><dd>In step 7, a reader marks each question good or bad. A bad mark sends the question back.</dd>
<dt>The owner</dt><dd>%(owner)s</dd>
<dt>Mock decision</dt><dd>A decision record of the build, such as mock decision 0038. The records are in the repository.</dd>
</dl></div></details>""" % {"n": SLOTS, "m": len(glob.glob(os.path.join(ROOT, "mocks/mock-*.questions.json"))), "slot": fact("w-slot", "The place of one question in the plan of a mock. Step 1 plans %d slots for each mock." % SLOTS),
                         "owner": fact("w-owner", "The person who directs this work and who made the decisions of the build. The owner passed the CCAR-F exam.")}

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
  <p class="pending">This part comes in slice 3.</p>
</section>
</main>""" % {"tab1": TAB1, "title": e(TITLE), "para": e(PARAGRAPH).replace("&#x27;", "&rsquo;").replace("'", "&rsquo;"),
             "fig1": FIG1, "parts": "".join(part(s) for s in range(9)), "words": WORDS}

# an SVG keeps its drawn size on a narrow screen, and its frame scrolls, so no label is below 12 pixels
BODY = re.sub(r'<svg class="(ve-svg|ve-bars)" viewBox="0 0 (\d+) ', lambda m: '<svg class="%s" style="min-width:%spx" viewBox="0 0 %s ' % (m.group(1), m.group(2), m.group(2)), BODY)
TOP = BODY.split('<section class="parts" id="steps"')[0]
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
