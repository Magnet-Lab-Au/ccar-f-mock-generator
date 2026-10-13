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
    return "%s: %s" % (point, use.replace("(see the deviation above)", "(" + DEVIATION + ")"))


POP = {
    "ts-44": {"who": "Task statement 4.4", "cls": "model", "title": TS["4.4"]["title"],
              "sent": ["How step 5 uses each point:", table_use("4.4-K1"), table_use("4.4-S1"), table_use("4.4-K2")],
              "points": pts("4.4-K1", "4.4-S1", "4.4-K2")},
    "ts-11": {"who": "Task statement 1.1", "cls": "model", "title": TS["1.1"]["title"],
              "sent": ["How step 5 uses the point:", table_use("1.1-S3")], "points": pts("1.1-S3")},
    "ts-43": {"who": "Task statement 4.3", "cls": "model", "title": TS["4.3"]["title"],
              "sent": ["How step 5 uses each point:", table_use("4.3-K1"), table_use("4.3-S3")], "points": pts("4.3-K1", "4.3-S3")},
}
for k in POP:
    POP[k].setdefault("example", None)

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
            5: "a Claude model, the writer of step 2. Code selects the request.", 6: "code and two Claude model calls for each scenario",
            7: "the owner (mocks 1 to 3), or a Claude model (mocks 4 and 5)", 8: "code, after the owner accepts the mock"}
NAMES = {0: ["Prepare the", "guide records"], 1: ["Plan the mock"], 2: ["Write the", "question"], 3: ["Check by code"],
         4: ["Check by", "a model"], 5: ["Try again"], 6: ["Check the", "complete mock"], 7: ["The owner marks", "the questions"],
         8: ["Build the files"]}
FULL = {0: "Prepare the guide records", 1: "Plan the mock", 2: "Write the question", 3: "Check by code", 4: "Check by a model",
        5: "Try again", 6: "Check the complete mock", 7: "The owner marks the questions", 8: "Build the files"}
for s_, name in FULL.items():   # the names of the build guide (one name for one thing)
    assert ("| %d. %s |" % (s_, name)) in read("docs/build-guide/README.md"), name
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
<figure data-figure="builder" id="builder-fig">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 880 570" role="img" aria-label="The 9 steps of the mock builder. Step 0 prepares the guide records once for each version of the exam guide. Step 1 plans 60 slots. Step 2 writes a question, step 3 checks it by code and step 4 by a model. A question that fails goes to step 5 and is checked again. When all 60 slots pass, step 6 checks the complete mock, step 7 marks the questions, and step 8 builds the files after the owner accepts. Dashed arrows are decisions of the owner: more tries or a new point for an open slot, a rewrite after step 6 or after the marks, a bad mark, and accept. A rewrite with a new point goes to step 2.">
      %(edges)s
      %(nodes)s
      <g class="ve-n who-owner"><rect class="sh" x="230" y="310" width="150" height="92" rx="0"/><text x="305" y="344">open slot</text><text class="sub" x="305" y="368">waits for owner</text></g>
      %(legend)s
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 1</span>Code moves each question through the steps. %(auto)s. %(wait)s: an open slot, a finding of step 6, a bad mark, %(rw)s, and %(acc)s. %(rwp)s</figcaption>
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
    "auto": fact("c-auto", "A question that fails step 3 or step 4 goes back to the writer by itself"),
    "wait": fact("c-wait", "Each other way back waits for a decision of the owner"),
    "rw": fact("c-rw", "a rewrite after the marks"),
    "acc": fact("c-acc", "the acceptance of the mock"),
    "rwp": fact("c-rwp", "A rewrite with a new point goes back to step 2."),
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
        edge("M640 70H710", "passes", 675, 61, cls="is-hot"),
        edge("M330 110V180", "fails", 338, 150, anchor="r"),
        edge("M560 110V180", "fails", 568, 150, anchor="r"),
        edge("M250 225H100V110", "tries again", 175, 216),
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
    return ('<div class="case"><span class="ve-label">Mock %d</span><h3>%d tries</h3>'
            '<svg class="ve-grid" viewBox="0 0 227 135" role="img" aria-label="Mock %d: %d tries for %d slots. %d slots passed both checks at the first try. %d slots had more than one try. The most tries for one slot: %d.">%s</svg>'
            '<p class="cap">%d of %d passed both checks at the first try</p></div>'
            % (x["mock"], x["tries"], x["mock"], x["tries"], SLOTS, x["first"], x["more"], x["max"], "".join(cells),
               x["first"], SLOTS))


FIG52 = """
<figure>
  <div class="cases">%s</div>
  <figcaption><span class="fig-n">Fig. 5-2</span>One square for each slot. A number is the tries of a slot that had more than one. It also counts new tries after a rewrite or a bad mark of the owner. %s %s</figcaption>
</figure>
""" % ("".join(grid(x) for x in MOCKS),
       fact("s5-counts", "The 5 mocks needed %d tries for %d questions." % (TOTAL_TRIES, 5 * SLOTS)),
       "In %d cases a slot stopped at the guard and waited for the owner. The guard of %d results &ldquo;cannot decide&rdquo; never stopped a slot."
       % (TOTAL_OPENED, CANNOT))

# Fig. 5-3: the review loop (story a)
FIG53_T = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 890 150" role="img" aria-label="The first review found 14 serious items. The second review found 10 new ones. The fix: one automatic loop, each other failure waits for the owner, and the control is code with tests.">
      <path class="ve-e" d="M250 60H318"/><text class="ve-el" x="284" y="51">answers</text>
      <path class="ve-e is-hot" d="M560 60H628"/><text class="ve-el" x="594" y="51">fix</text>
      <g class="ve-n"><rect class="sh" x="20" y="20" width="230" height="80" rx="0"/><text x="135" y="44">first review</text>
        <rect class="bar" x="40" y="62" width="140" height="16" rx="0"/><text class="sub" x="210" y="70">14</text></g>
      <g class="ve-n"><rect class="sh" x="320" y="20" width="240" height="80" rx="0"/><text x="440" y="44">second review</text>
        <rect class="bar" x="340" y="62" width="100" height="16" rx="0"/><text class="sub r" x="452" y="70">10 new</text></g>
      <g class="ve-n is-key"><rect class="sh" x="630" y="20" width="240" height="80" rx="0"/><text x="750" y="44">the control is code</text><text class="sub" x="750" y="70">with tests</text></g>
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
  <h4 class="takeaway">A failed question goes back to the writer with its findings</h4>
  <p>%(what)s %(again)s %(one)s %(pass)s</p>
</section>
<details class="level" data-level="explanation">
  <summary><h4>Explanation</h4><span class="ve-label">3 minutes</span></summary>
  <div class="body">
    %(fig51)s
    <p><b>What the writer gets.</b> The request of step 2, the failed try and its findings. A finding names the rule and, where it fits, the letter of the option. %(short)s The guide names the same three parts for a new try: %(three)s</p>
    <p><b>The limits.</b> %(guard)s Code checks for a pass first, so the limits are only guards. A slot that reaches a limit waits for the owner. The other slots continue.</p>
    <p><b>The record.</b> %(file)s</p>
    %(fig52)s
    <p class="gh">The task statements that step 5 uses</p>
    <div class="tslist">%(ts)s</div>
  </div>
</details>
<details class="level" data-level="depth">
  <summary><h4>Depth</h4><span class="ve-label">what went wrong, and the fix</span></summary>
  <div class="body">
    <h4 class="story">The review loop that ended when the control became code</h4>
    %(fig53)s
    <p>The answer to the first review added rules, and the new rules made new cases. The fix: %(auto)s Each other failure waits for the owner. %(code)s Code checks %(passfirst)s. Today the program has %(tests)s.</p>
    <h4 class="story">The reason of the owner reached only one try</h4>
    <p>Slot M5-S38 failed rule B9 three times. The owner gave more tries with a reason: &ldquo;%(reason)s&rdquo; %(q)s So mock decision 0074 added the reason to the next request, %(fix)s, and %(test)s checks it.</p>
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
    return ('<div class="tsrow"><span class="chip info" data-step="%s" tabindex="0" role="button" aria-expanded="false">Task statement %s</span> '
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
    "three": f("s5-three", "the original, the failed result and the errors (4.4-S1)."),
    "guard": f("s5-guard", "Each start of a slot has at most %d tries, and %d results &ldquo;cannot decide&rdquo; also stop it." % (TRIES, CANNOT)),
    "file": f("s5-file", "Each try is a new file. No file is written over, so the history of each question stays."),
    "fig52": FIG52,
    "ts": ts_chip("ts-44", "4.4") + ts_chip("ts-11", "1.1") + ts_chip("ts-43", "4.3"),
    "fig53": FIG53,
    "auto": f("c-auto", "one automatic loop."),
    "code": f("a-code", "The control became code, with tests that make no model call."),
    "passfirst": f("a-passfirst", "for a pass before the limits"),
    "tests": f("a-tests", "%d tests" % TESTS),
    "reason": f("b-reason", e(D004["reason"])),
    "q": f("b-q", "But the program, as it was built, sent the writer only the last failed try and its findings, not the reason."),
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


step5_html = step5_html.replace("<ul></ul>", "<ul>%s</ul>" % sources(list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', step5_html)))))

# ----- the parts -----

MINI = {s: '<svg class="minimap" viewBox="0 0 126 14" role="img" aria-label="Step %d of the steps 0 to 8">%s</svg>'
        % (s, "".join('<rect x="%d" y="1" width="12" height="12"%s/>' % (i * 14 + .5, ' class="here"' if i == s else "") for i in range(9)))
        for s in range(9)}
SLICE = {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 6: 2, 7: 2, 8: 2}


def part(s):
    who = WHO_LONG[s]
    body = step5_html if s == 5 else '<p class="pending">This step comes in slice %d.</p>' % SLICE[s]
    return ('<details class="part" id="step-%d"><summary><span class="pn">%d</span><span><h3>%s</h3><span class="who">%s</span></span>'
            '<span class="mm">%s<span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (s, s, e(FULL[s]), e(who), MINI[s], body))


PARAGRAPH = read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")
PARAGRAPH = re.search(r"   > (The mock builder is itself.*?)\n", PARAGRAPH).group(1)
TITLE = "Mocks Built with the Same Principles They Test"
assert TITLE in read("academy/decisions/0010-two-tabs-each-one-page-with-an-exploded-view.md")

BODY = """<main>
<header id="top">
  <nav class="tabs" aria-label="Tabs"><a href="%(tab1)s">Exam guide breakdown</a><span aria-current="page">Behind the mocks</span></nav>
  <h1>%(title)s</h1>
  <p class="lead">%(para)s</p>
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
             "fig1": FIG1, "parts": "".join(part(s) for s in range(9))}

# an SVG keeps its drawn size on a narrow screen, and its frame scrolls, so no label is below 12 pixels
BODY = re.sub(r'<svg class="ve-svg" viewBox="0 0 (\d+) ', lambda m: '<svg class="ve-svg" style="min-width:%spx" viewBox="0 0 %s ' % (m.group(1), m.group(1)), BODY)
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
