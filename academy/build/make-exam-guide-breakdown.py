"""Make tab 1, "Exam guide breakdown": academy/pages/exam-guide-breakdown.html and exam-guide-breakdown.js.

The tab has the map of the exam guide, "How we broke it down", and the 5 domains, each with its task
statements as closed parts (academy decisions 0010, 0019 and 0021). Slices 4 to 8 of decision 0022 fill
the domains one at a time. A task statement that no slice has written yet shows its guide title and says so.

The facts come from the fact sheets academy/facts/ts-N-M.md (decisions 0011 and 0012). Each excerpt of a
preview card is taken from its file, and each number is counted from its file (decision 0030). The script
stops if a text is not in its file. Part 1.1 takes the checked content of the fifth sample
(academy/sample/1-1-split-exam-guide.html, decision 0008).

Run from the folder ccar-f-mock-generator:
    python3 academy/build/make-exam-guide-breakdown.py
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import REPO, ROOT, TAG, code_block, e, excerpt, fact, lines_of, link, page, read, script_file, write  # noqa: E402

TAB2 = "behind-the-mocks.html"
EG = "reference/exam-guide.md"
GUIDE = json.loads(read("reference/guide-records.json"))
TS = {t["id"]: t for t in GUIDE["task_statements"]}
DOM = {d["id"]: d for d in GUIDE["domains"]}
SCEN = GUIDE["scenarios"]
N_PTS = sum(len(t["points"]) for t in TS.values())
N_K = sum(1 for t in TS.values() for p in t["points"] if p["kind"] == "knowledge")
N_S = N_PTS - N_K
assert len(TS) == 30 and len(DOM) == 5 and len(SCEN) == 6

CARD = {}
POP = {}


def gx(text, title):
    return excerpt(EG, text, title, kind="guide")


def jread(path):
    return json.loads(read(path))


# ----- counts from the files of the mock builder -----

QUESTIONS = [q for m in range(1, 6) for g in jread("mocks/mock-%02d.questions.json" % m)["groups"] for q in g["questions"]]
ON_TS = {t: sum(1 for q in QUESTIONS if q["point"].startswith(t + "-")) for t in TS}
assert sum(ON_TS.values()) == len(QUESTIONS) == 300


def step_file(n):
    return os.path.relpath(glob.glob(os.path.join(ROOT, "docs/build-guide/step-%d-*.md" % n))[0], ROOT)


STEP_NAME = {0: "Prepare the guide records", 1: "Plan the mock", 2: "Write the question", 3: "Check by code", 4: "Check by a model",
             5: "Try again", 6: "Check the complete mock", 7: "The questions are marked", 8: "Build the files"}
USES = {}      # task statement -> [(step, [points])], from the tables of guide points (decision 0024)
for n in range(9):
    for l in read(step_file(n)).split("\n"):
        m = re.match(r"^\| ([1-5]\.[0-9])-([KS][0-9]+) \|", l)
        if m:
            USES.setdefault(m.group(1), {}).setdefault(n, []).append(m.group(1) + "-" + m.group(2))
CC_PART = {"3.1": "cc-3-1", "1.7": "cc-1-7", "4.6": "cc-4-6", "3.4": "cc-3-4"}
TAB2_HTML = read("academy/pages/behind-the-mocks.html")
for t, pid in CC_PART.items():
    assert 'id="%s"' % pid in TAB2_HTML

# ----- the levels and the sources -----


def level(kind, body, pid):
    if kind == "overview":
        return '<section data-level="overview" aria-label="Overview"><p class="lvl1">Overview &middot; 30 seconds</p>%s</section>' % body
    if kind == "explanation":
        return ('<details class="level" data-level="explanation"><summary><h4>Explanation</h4><span class="ve-label">3 minutes</span></summary>'
                '<div class="body">%s</div></details>' % body)
    return ('<details class="level" data-level="depth"><summary><h4>Depth</h4><span class="ve-label">beyond the exam, code, and the mocks</span></summary>'
            '<div class="body">%s<section class="sources" aria-label="Sources of %s"><p class="ve-label">Sources of %s. '
            'Each underlined fact opens its card.</p><ul>@SOURCES@</ul></section></div></details>' % (body, pid, pid))


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


def with_sources(html):
    return html.replace("@SOURCES@", sources(list(dict.fromkeys(re.findall(r'data-card="([^"]+)"', html)))), 1)


# ----- the generic blocks of a task statement -----


def lab(pid):
    """1.1-K2 with its K or S letter marked (decision 0009)."""
    t, ks = pid.split("-")
    return '%s-<span class="%s">%s</span>%s' % (t, "lk" if ks[0] == "K" else "ls", ks[0], ks[1:])


def guide_text(tsid):
    """The K and S points of the guide, exact, with our labels (decision 0021)."""
    t = TS[tsid]
    head = "### **Task Statement %s: %s**" % (tsid, t["title"])
    a = lines_of(EG, head)[0]
    last = t["points"][-1]["text"]
    b = lines_of(EG, last)[0]
    CARD["ts-%s-guide" % tsid.replace(".", "-")] = {"title": "Exam guide, task statement %s" % tsid, "kind": "guide",
                                                   "text": "%s: %s. %d points: %s" % (tsid, t["title"], len(t["points"]), " / ".join(p["text"] for p in t["points"])),
                                                   "src": "%s, lines %d to %d" % (EG, a, b), "href": link(EG, a, b)}
    ks = lambda kind: "".join('<li><span class="pid">%s</span> %s</li>' % (lab(p["id"]), e(p["text"])) for p in t["points"] if p["kind"] == kind)
    return ('<h4 class="gh2">The guide&rsquo;s own text</h4><p class="ve-label">%s</p>'
            '<p class="gh">Knowledge of:</p><ul class="glist">%s</ul><p class="gh">Skills in:</p><ul class="glist">%s</ul>'
            % (fact("ts-%s-guide" % tsid.replace(".", "-"), "Exam guide, lines %d to %d" % (a, b)), ks("knowledge"), ks("skill")))


def mock_count(tsid):
    key = "ts-%s-count" % tsid.replace(".", "-")
    CARD[key] = {"title": "The questions of the 5 mocks", "kind": "count",
                 "text": "Questions whose point starts with %s, in mocks/mock-01.questions.json to mock-05.questions.json: %d of %d. The script of this page counted them."
                         % (tsid, ON_TS[tsid], len(QUESTIONS)),
                 "src": "mocks/mock-01.questions.json to mocks/mock-05.questions.json", "href": "%s/tree/%s/mocks" % (REPO, TAG)}
    return fact(key, "%d of the %d questions in the 5 mocks of this academy test %s." % (ON_TS[tsid], len(QUESTIONS), tsid))


def tab2_links(tsid, why=""):
    """The links to each step of tab 2 that uses a point of the task statement (decisions 0010 and 0024)."""
    rows = []
    for n, pts in sorted(USES.get(tsid, {}).items()):
        rows.append('<li><a href="%s#step-%d">Step %d, %s &rarr;</a> <span class="ve-label">uses %s</span></li>'
                    % (TAB2, n, n, e(STEP_NAME[n]), ", ".join(pts)))
    if tsid in CC_PART:
        rows.append('<li><a href="%s#%s">The build in Claude Code, %s &rarr;</a></li>' % (TAB2, CC_PART[tsid], tsid))
    if rows:
        return '<h4 class="gh2">In the mock builder and its build</h4><ul class="tolinks">%s</ul>' % "".join(rows)
    return '<h4 class="gh2">In the mock builder and its build</h4><p>No step of the mock builder uses a point of %s. %s</p>' % (tsid, why)


TAKEAWAY = {}   # task statement -> its takeaway heading, from its fact sheet
PART = {}       # task statement -> the HTML of its three levels
SLICE_OF = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8}


def ts_part(tsid):
    t = TS[tsid]
    pid = "ts-" + tsid.replace(".", "-")
    if tsid in PART:
        head, body = TAKEAWAY[tsid], with_sources(PART[tsid])
    else:
        head = t["title"]
        body = '<p class="pending">This part is not written yet.</p>'
    return ('<details class="part" id="%s"><summary><span class="pn">%s</span><span><h3>%s</h3></span>'
            '<span class="mm"><span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (pid, tsid, e(head), body))


def overview(tsid, takeaway, answer, fig=""):
    TAKEAWAY[tsid] = takeaway
    key = "ts-%s-title" % tsid.replace(".", "-")
    CARD[key] = gx("### **Task Statement %s: %s**" % (tsid, TS[tsid]["title"]), "Exam guide, task statement %s" % tsid)
    return level("overview", '<p class="gtitle">%s</p><p class="lead">%s</p>%s'
                 % (fact(key, "&ldquo;%s&rdquo;" % e(TS[tsid]["title"])), answer, fig), "ts-" + tsid.replace(".", "-"))



# ----- helpers for the parts -----

SRC = "academy/sources/2026-10-14-%s.md"
PAGE_NAME = {}   # copy -> the name of its page, for the card title


def D(copy, text, page_name):
    """An excerpt of a dated copy of the Anthropic documentation (decisions 0014 and 0030)."""
    if copy.startswith("claude-code-docs"):
        title = "Claude Code documentation, %s (copy of 14 October 2026)" % page_name.replace("Claude Code, ", "")
    else:
        title = "Anthropic documentation, %s (copy of 14 October 2026)" % page_name
    return excerpt(SRC % copy, text, title, kind="docs")


def card(key, c):
    CARD[key] = c
    return key


def cf(key, c, text):
    """A fact with its card."""
    CARD[key] = c
    return fact(key, text)


def box(x, y, w, h, lines, sub=None, cls="", step=None):
    attrs = ' data-step="%s" tabindex="0" role="button" aria-expanded="false"' % step if step else ""
    out = '<g class="ve-n %s"%s transform="translate(%d %d)"><rect class="sh" width="%d" height="%d" rx="0"/>' % (cls, attrs, x, y, w, h)
    n = len(lines) + (1 if sub else 0)
    y0 = h / 2 - (n - 1) * 10
    for i, t in enumerate(lines):
        out += '<text x="%d" y="%d">%s</text>' % (w / 2, y0 + i * 20, e(t))
    if sub:
        out += '<text class="sub" x="%d" y="%d">%s</text>' % (w / 2, y0 + len(lines) * 20 + 2, e(sub))
    return out + "</g>"


def edge(d, label=None, lx=0, ly=0, cls="", anchor=""):
    out = '<path class="ve-e %s" d="%s"/>' % (cls, d)
    if label:
        out += '<text class="ve-el %s" x="%d" y="%d">%s</text>' % (anchor, lx, ly, e(label))
    return out


def figure(num, svg_w, svg_h, aria, inner, cap):
    return ('<figure><div class="frame"><svg class="ve-svg" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg></div>'
            '<figcaption><span class="fig-n">Fig. %s</span>%s</figcaption></figure>' % (svg_w, svg_h, e(aria), inner, num, cap))


def code_pop(key, label, title, copy, first, last, page_name, note=""):
    """A button that opens the code of the documentation in a popup (decisions 0004 and 0032)."""
    c = code_block(SRC % copy, first, last, title)
    POP[key] = {"who": "Code", "cls": "code", "title": title, "sent": [note] if note else [], "examplehead": "From the documentation, %s" % page_name,
                "example": c["text"], "examplenote": "%s (copy of 14 October 2026)" % c["src"]}
    return '<p><span class="chip info" data-step="%s" tabindex="0" role="button" aria-expanded="false">%s</span></p>' % (key, e(label))


def code_pop_text(key, label, title, copy, text, page_name, note=""):
    """A code popup from an exact block of a dated copy."""
    c = D(copy, text, page_name)
    POP[key] = {"who": "Code", "cls": "code", "title": title, "sent": [note] if note else [], "examplehead": "From the documentation, %s" % page_name,
                "example": __import__("textwrap").dedent(text), "examplenote": "%s (copy of 14 October 2026)" % c["src"]}
    return '<p><span class="chip info" data-step="%s" tabindex="0" role="button" aria-expanded="false">%s</span></p>' % (key, e(label))


def beyond(items):
    return ('<div class="callout"><span class="chip">Beyond the exam</span><p>The exam tests the points of the guide above. These facts of the documentation go further, for work in production.</p>'
            '<ul class="beyond">%s</ul></div>' % "".join("<li>%s</li>" % i for i in items))


def exam_tests(tsid, lines):
    """The lines of section 17 of the guide for the task statement, and the questions of the 5 mocks."""
    k = tsid.replace(".", "-")
    out = []
    for i, (text, what) in enumerate(lines):
        out.append("%s %s" % (what, fact(card("ts-%s-x%d" % (k, i), gx(text, "Exam guide, section 17")), "&ldquo;%s&rdquo;" % e(text))))
    return '<div><h4 class="gh2">The exam tests</h4><p>%s. %s</p></div>' % (" ".join(out), mock_count(tsid))


# ----- part 1.1: the checked content of the fifth sample -----

SAMPLE = read("academy/sample/1-1-split-exam-guide.html")
S_CARD = json.loads(re.search(r'id="carddata">(.*?)</script>', SAMPLE, re.S).group(1).replace("<\\/", "</"))
S_POP = json.loads(re.search(r'id="popdata">(.*?)</script>', SAMPLE, re.S).group(1).replace("<\\/", "</"))


def cut(a, b):
    i = SAMPLE.index(a)
    return SAMPLE[i:SAMPLE.index(b, i)]


def from_sample(html):
    """IDs, popups and cards of the sample get the prefix of the part (decision 0033). Figures get the number of the part."""
    html = re.sub(r'data-step="([^"]+)"', lambda m: 'data-step="ts-1-1-%s"' % m.group(1), html)
    html = re.sub(r'data-card="([^"]+)"', lambda m: 'data-card="ts-1-1-%s"' % m.group(1), html)
    html = html.replace('id="fig1"', 'id="ts-1-1-fig1"')
    html = html.replace("The code of the loop is on <i>Your code sends the request</i>.", "The popup of <i>Your code sends the request</i> shows the code of the loop.")
    for a, b in (("Fig. 1<", "Fig. 1.1-1<"), ("Fig. 2<", "Fig. 1.1-2<"), ("Fig. 4<", "Fig. 1.1-3<"), ("in Fig. 1,", "in Fig. 1.1-1,")):
        html = html.replace(a, b)
    for k in set(re.findall(r'data-step="ts-1-1-([^"]+)"', html)):
        POP["ts-1-1-" + k] = S_POP[k]
    for k in set(re.findall(r'data-card="ts-1-1-([^"]+)"', html)):
        CARD["ts-1-1-" + k] = dict(S_CARD[k])
        CARD["ts-1-1-" + k]["title"] = CARD["ts-1-1-" + k]["title"].replace("In-Scope Topics, Section 17 (Appendix)", "Exam guide, section 17").replace("Technologies and Concepts, Section 17 (Appendix)", "Exam guide, section 17")
    if "ts-1-1-d-stop" in CARD:
        table = "\n".join(read(SRC % "anthropic-docs-handling-stop-reasons").split("\n")[13:21])
        assert table.count("| [`") == 7 and "model_context_window_exceeded" in table
        CARD["ts-1-1-d-stop"] = D("anthropic-docs-handling-stop-reasons", table, "Stop reasons and fallback")
    return html


LEAD11 = re.search(r'<p class="lead">(.*?)</p>', SAMPLE, re.S).group(1)
FIG11 = cut('<figure class="ve-steps" id="fig1">', "</figure>") + "</figure>"
WHO11 = cut("<p><b>Who decides.</b>", "</p>") + "</p>"
CASES11 = cut('<figure><div class="cases">', "</figure>") + "</figure>"
TESTS11 = cut("<div><h3>The exam tests</h3>", "</div>") + "</div>"
CODE11 = cut("<p><b>The loop in code.</b>", "</p>") + "</p>"
BEYOND11 = cut('<div class="callout"><span class="chip">Beyond the exam</span>', "</figure></div>") + "</figure></div>"
TESTS11 = TESTS11.replace("<div><h3>The exam tests</h3>", '<div><h4 class="gh2">The exam tests</h4>')

PART["1.1"] = (overview("1.1", "The loop runs while Claude asks for tools", from_sample(LEAD11), from_sample(FIG11))
               + level("explanation", from_sample(WHO11 + CASES11 + TESTS11) + "<p>%s</p>" % mock_count("1.1") + guide_text("1.1"), "ts-1-1")
               + level("depth", from_sample(CODE11 + BEYOND11) + tab2_links("1.1"), "ts-1-1"))


# ----- part 1.3 (facts: academy/facts/ts-1-3.md) -----

SUB, SES, PERM = "claude-code-docs-agent-sdk-subagents", "claude-code-docs-agent-sdk-sessions", "claude-code-docs-agent-sdk-permissions"
PAR, PBP, CCS = "anthropic-docs-parallel-tool-use", "anthropic-docs-claude-prompting-best-practices", "claude-code-docs-sub-agents"
D26 = glob.glob(os.path.join(ROOT, "docs/decisions/0026-*.md"))[0][len(ROOT) + 1:]
D12 = glob.glob(os.path.join(ROOT, "docs/decisions/0012-*.md"))[0][len(ROOT) + 1:]
CARD.update({
    "ts-1-3-f5": D(SUB, "The only content you pass from parent to subagent is the Agent tool's prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt.", "Agent SDK, Subagents"),
    "ts-1-3-f7": D(SUB, "only its final message returns to the parent.", "Agent SDK, Subagents"),
})
FIG13 = figure("1.3-1", 890, 350,
               "A coordinator sends three Task calls in one response. Each subagent gets only the prompt of its call, with the findings and their sources. "
               "The conversation history of the coordinator is not passed. Only the final message of each subagent comes back.",
               "".join([edge("M250 170H360"), edge("M360 170V70H540"), edge("M360 170H540"), edge("M360 170V270H540"),
                        edge("M250 48H520", "not passed", 385, 39, cls="is-async"),
                        edge("M870 70H880V340H135V220", cls="is-async"), '<path class="ve-e no-head is-async" d="M870 170H880M870 270H880"/>',
                        '<text class="ve-el" x="510" y="332">only the final message of each comes back</text>',
                        '<text class="ve-el" x="305" y="161">Task calls</text><text class="ve-el" x="450" y="261">findings + sources</text>',
                        box(20, 20, 230, 56, ["conversation history"], sub="of the coordinator"),
                        box(20, 120, 230, 100, ["Coordinator"], sub='allowedTools has "Task"', cls="who-model"),
                        box(540, 30, 330, 80, ["Subagent A"], sub="description · prompt · tools", cls="who-model"),
                        box(540, 130, 330, 80, ["Subagent B"], sub="description · prompt · tools", cls="who-model"),
                        box(540, 230, 330, 80, ["Subagent C"], sub="description · prompt · tools", cls="who-model")]),
               "Parallel subagents start from one response. %s %s The names and the allowedTools rule are those of the guide. The product today calls the tool Agent." % (fact("ts-1-3-f5", "A subagent gets only the prompt of its call."), fact("ts-1-3-f7", "Only its final message goes back.")))

PART["1.3"] = (overview("1.3", "A subagent sees none of the coordinator's conversation",
                        "A coordinator starts each subagent with a call of the Task tool. The subagent does not see the conversation of the coordinator, so the prompt of the call must hold the complete findings and their sources.",
                        FIG13)
    + level("explanation",
            "<p><b>Spawn.</b> %s %s %s</p>" % (
                cf("ts-1-3-k1", gx("The Task tool as the mechanism for spawning subagents, and the requirement that allowedTools must include \"Task\" for a coordinator to invoke subagents", "Exam guide, 1.3-K1"),
                   "The guide: a coordinator starts a subagent with the Task tool, and its allowedTools must include &ldquo;Task&rdquo;."),
                cf("ts-1-3-c1", D(CCS, "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases.", "Claude Code, Subagents"),
                   "The product renamed the tool Agent in version 2.1.63."),
                cf("ts-1-3-c2", D(PERM, "Any other tool not listed in `allowed_tools` is still available to Claude, and a call to it that needs approval falls through to the permission mode.", "Agent SDK, Permissions"),
                   "In the current Agent SDK, allowed_tools (allowedTools in the guide) only approves a tool in advance.") + " " + cf("ts-1-3-c2b", D(PERM, "Calls that need no approval in `default` mode run whether or not you list them, such as [read-only Bash commands](/docs/en/permissions#read-only-commands), tools like `Agent` that don't ask before running", "Agent SDK, Permissions"),
                   "The Agent tool runs even when the list does not name it. The exam uses the guide.")
            )
            + "<p><b>Context.</b> %s %s %s %s %s</p>" % (
                fact("ts-1-3-f5", "Only the prompt of the tool call goes from the coordinator to a subagent."),
                cf("ts-1-3-f6", D(SUB, "The parent's conversation history or tool results", "Agent SDK, Subagents"), "The subagent does not get the conversation history or the tool results of the parent."),
                fact("ts-1-3-f7", "Only the final message of the subagent goes back."),
                cf("ts-1-3-s1", gx("Including complete findings from prior agents directly in the subagent's prompt (e.g., passing web search results and document analysis outputs to the synthesis subagent)", "Exam guide, 1.3-S1"),
                   "So the coordinator puts the complete findings of earlier agents in the prompt (1.3-S1),"),
                cf("ts-1-3-f16", D(PBP, "When using multiple documents, wrap each document in `<document>` tags with `<document_content>` and `<source>` (and other metadata) subtags for clarity.", "Prompting best practices"),
                   "and keeps the content apart from its metadata, such as the source URL, to keep the attribution (1.3-S2). The documentation also separates the content and the source of a document."))
            + "<p><b>Definitions.</b> %s %s %s</p>" % (
                cf("ts-1-3-f8", D(SUB, "| `description` | `string` | Yes | Natural language description of when to use this agent |\n| `prompt` | `string` | Yes | The agent's system prompt defining its role and behavior |\n| `tools` | `string[]` | No | Array of allowed tool names.", "Agent SDK, Subagents"),
                   "An AgentDefinition gives each type of subagent a description, a system prompt and a list of tools (1.3-K3)."),
                cf("ts-1-3-f9", D(SUB, "Claude automatically decides when to invoke subagents based on the task and each subagent's `description`.", "Agent SDK, Subagents"),
                   "Claude chooses a subagent by its description."),
                cf("ts-1-3-f10", D(SUB, "A tool you leave out isn't in the subagent's session at all: Claude works without it, with no permission prompt or error.", "Agent SDK, Subagents"),
                   "A tool that the list leaves out is not in its session."))
            + "<p><b>Parallel.</b> %s %s %s</p>" % (
                cf("ts-1-3-f14", D(PAR, "When Claude calls tools, the response has a `stop_reason` of `tool_use` and can contain several `tool_use` blocks in a single assistant turn.", "Parallel tool use"),
                   "One response of Claude can hold several tool calls."),
                cf("ts-1-3-s3", gx("Spawning parallel subagents by emitting multiple Task tool calls in a single coordinator response rather than across separate turns", "Exam guide, 1.3-S3"),
                   "So the coordinator starts parallel subagents with several Task calls in one response, not across separate turns (1.3-S3)."),
                cf("ts-1-3-f15", D(SUB, "multiple subagents can run concurrently, so independent subtasks finish in the time of the slowest one rather than the sum of all of them.", "Agent SDK, Subagents"),
                   "Subagents can run at the same time."))
            + "<p><b>Goals, not steps.</b> %s %s</p>" % (cf("ts-1-3-s4", gx("Designing coordinator prompts that specify research goals and quality criteria rather than step-by-step procedural instructions, to enable subagent adaptability", "Exam guide, 1.3-S4"),
                   "A coordinator prompt gives research goals and quality criteria, not step-by-step procedures, so that a subagent can adapt (1.3-S4)."),
                cf("ts-1-3-f17", D(PBP, "**Provide clear success criteria:** Define what constitutes a successful answer to your research question.", "Prompting best practices"),
                   "The documentation also asks for clear success criteria."))
            + "<p><b>Fork.</b> %s So two approaches can start from one shared analysis (1.3-K4). Part 1.7 explains sessions.</p>" % (
                cf("ts-1-3-f11", D(SES, "Forking creates a new session that starts with a copy of the original's history but diverges from that point. The fork gets its own session ID; the original's ID and history stay unchanged.", "Agent SDK, Sessions"),
                   "A fork of a session starts with a copy of the history. The original does not change."))
            + exam_tests("1.3", [("Claude Agent SDK — agent definitions, agentic loops, stop_reason handling, hooks (PostToolUse, tool call interception), subagent spawning via Task tool, allowedTools configuration", "Among the technologies, the guide names"),
                                 ("Subagent context management: explicit context passing, structured state persistence, crash recovery using manifests", "Among the topics:")])
            + guide_text("1.3"), "ts-1-3")
    + level("depth",
            beyond([cf("ts-1-3-b1", D(SUB, "Project CLAUDE.md (loaded via [`settingSources`](/docs/en/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources)), unless the agent sets [`omitClaudeMd`](#agentdefinition-configuration)", "Agent SDK, Subagents"),
                       "A subagent is not empty: by default it also loads the CLAUDE.md of the project, unless its definition turns that off. The guide says only that the context must be in the prompt."),
                    cf("ts-1-3-b2", D(SUB, "Each subagent makes its own API requests, which count toward the query's `total_cost_usd`, and a subagent can spawn subagents of its own, so one prompt can grow into a tree of agents.", "Agent SDK, Subagents"),
                       "A subagent can start subagents of its own, and each one makes its own API requests, so one prompt can grow into a tree of agents and costs."),
                    cf("ts-1-3-b3", D(CCS, "A fork is a subagent that inherits the entire conversation so far instead of starting fresh.", "Claude Code, Subagents"),
                       "Claude Code also has a fork subagent, which inherits the whole conversation. It is not the fork_session of the guide.")])
            + code_pop("ts-1-3-code", "The code: two AgentDefinitions in Python", "Two subagents defined in code", SUB, "import asyncio", "asyncio.run(main())", "Agent SDK, Subagents",
                       "The coordinator approves the Agent tool, and each AgentDefinition has a description, a prompt and its tools.")
            + tab2_links("1.3")
            + "<p>%s %s</p>" % (cf("ts-1-3-d26", excerpt(D26, "The pipeline uses no MCP, no subagent, no hook and no session.", "Mock decision 0026"), "The mock builder itself uses no subagent."),
                                cf("ts-1-3-d12", excerpt(D12, "A subagent is necessary only for a step in which code cannot know before the call what the model must read.", "Mock decision 0012"),
                                   "No step needs one: a subagent is necessary only when code cannot know before the call what the model must read.")), "ts-1-3"))


# ----- part 1.2 (facts: academy/facts/ts-1-2.md) -----

AT, O5 = "claude-code-docs-agent-teams", "anthropic-docs-prompting-claude-opus-5"
FIG12 = figure("1.2-1", 890, 380,
               "A coordinator in the middle sends a task prompt to four subagents: web search, document analysis, synthesis and report. "
               "Each subagent has its own context and sends only its final result back. No arrow joins two subagents. When the synthesis has gaps, the coordinator sends targeted queries again.",
               "".join([edge("M380 140V55H240"), edge("M510 140V55H650"), edge("M380 250V325H240"), edge("M510 250V325H650"),
                        edge("M240 75H410V140", cls="is-async"), edge("M650 75H480V140", cls="is-async"), edge("M240 310H410V250", cls="is-async"),
                        '<text class="ve-el" x="325" y="94">result</text><text class="ve-el" x="565" y="94">result</text>',
                        edge("M240 30H650", "no direct path", 445, 16, cls="is-async no-head"), '<path class="ve-e no-head" d="M437 22l16 16M453 22l-16 16"/>',
                        edge("M760 290V195H560", "gaps? targeted queries again", 690, 186, cls="is-hot"),
                        '<text class="ve-el" x="310" y="48">task prompt</text>',
                        box(330, 140, 230, 110, ["Coordinator"], sub="split · select · join", cls="who-model"),
                        box(20, 20, 220, 70, ["Web search"], sub="own context", cls="who-model"),
                        box(650, 20, 220, 70, ["Document analysis"], sub="own context", cls="who-model"),
                        box(20, 290, 220, 70, ["Report"], sub="own context", cls="who-model"),
                        box(650, 290, 220, 70, ["Synthesis"], sub="own context", cls="who-model")]),
               "%s %s" % (cf("ts-1-2-k1", gx("Hub-and-spoke architecture where a coordinator agent manages all inter-subagent communication, error handling, and information routing", "Exam guide, 1.2-K1"),
                             "The coordinator manages all communication between the subagents, the errors and the routing of information."),
                          cf("ts-1-2-f1", gx("A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports.", "Exam guide, scenario 3"),
                             "The four subagents are those of scenario 3 of the guide, a multi-agent research system.")))

PART["1.2"] = (overview("1.2", "The coordinator splits the work and routes every result",
                        "A coordinator agent splits the task, calls only the subagents that the query needs, and is the only path between them. "
                        "Each subagent starts without the conversation of the coordinator, so a split that is too narrow leaves gaps that no subagent can see.",
                        FIG12)
    + level("explanation",
            "<p><b>The hub.</b> %s %s %s</p>" % (
                cf("ts-1-2-s4", gx("Routing all subagent communication through the coordinator for observability, consistent error handling, and controlled information flow", "Exam guide, 1.2-S4"),
                   "The guide routes all communication of the subagents through the coordinator, for observability, one way to handle errors, and control of the information (1.2-S4)."),
                cf("ts-1-2-f3", D(AT, "| **Coordination** | Main agent manages all work |", "Claude Code, Agent teams"), "In the documentation too, the main agent manages all work of its subagents,"),
                cf("ts-1-2-f4", D(SUB, "only its final message returns to the parent.", "Agent SDK, Subagents"), "and only the final message of a subagent returns to it."))
            + "<p><b>Isolated context.</b> %s Part 1.3 shows what the coordinator must pass.</p>" %
                cf("ts-1-2-k2", gx("How subagents operate with isolated context—they do not inherit the coordinator's conversation history automatically", "Exam guide, 1.2-K2"),
                   "A subagent does not get the conversation history of the coordinator (1.2-K2).")
            + "<p><b>Choose the subagents.</b> %s %s</p>" % (
                cf("ts-1-2-k3", gx("The role of the coordinator in task decomposition, delegation, result aggregation, and deciding which subagents to invoke based on query complexity", "Exam guide, 1.2-K3"),
                   "The coordinator splits the task, delegates, joins the results, and decides which subagents a query needs (1.2-K3)."),
                cf("ts-1-2-f8", D(O5, "If one subagent can complete the task, use one rather than several, and keep spawn counts low.", "Prompting Claude Opus 5"),
                   "A sample prompt in the documentation also tells Claude to use one subagent, not several, when one is enough (1.2-S1)."))
            + "<p><b>Split the scope.</b> %s %s %s</p>" % (
                cf("ts-1-2-s2", gx("Partitioning research scope across subagents to minimize duplication (e.g., assigning distinct subtopics or source types to each agent)", "Exam guide, 1.2-S2"),
                   "The guide gives each subagent a distinct subtopic or source type, so that the work does not repeat (1.2-S2)."),
                cf("ts-1-2-k4", gx("Risks of overly narrow task decomposition by the coordinator, leading to incomplete coverage of broad research topics", "Exam guide, 1.2-K4"),
                   "A split that is too narrow leaves parts of a broad topic with no coverage (1.2-K4)."),
                cf("ts-1-2-f14", gx("The subagents executed their assigned tasks correctly—the problem is what they were assigned.", "Exam guide, sample question 7"),
                   "In sample question 7 of the guide, each subagent did its task correctly. The problem was what they were given."))
            + "<p><b>Refine.</b> %s</p>" %
                cf("ts-1-2-s3", gx("Implementing iterative refinement loops where the coordinator evaluates synthesis output for gaps, re-delegates to search and analysis subagents with targeted queries, and re-invokes synthesis until coverage is sufficient", "Exam guide, 1.2-S3"),
                   "The coordinator checks the synthesis for gaps, sends targeted queries to the search and analysis subagents, and runs the synthesis again, until the coverage is sufficient (1.2-S3). Only the guide describes this loop.")
            + exam_tests("1.2", [("Multi-agent orchestration: coordinator-subagent patterns, task decomposition, parallel subagent execution, iterative refinement loops", "Among the topics, the guide names")])
            + guide_text("1.2"), "ts-1-2")
    + level("depth",
            beyond([cf("ts-1-2-b1", D(AT, "Subagents that Claude named when it spawned them can also [message each other](/docs/en/sub-agents#what-loads-at-startup)", "Claude Code, Agent teams"),
                       "In Claude Code, subagents that Claude named can also message each other. The guide routes all communication through the coordinator, and the exam uses the guide."),
                    cf("ts-1-2-b2", D(SUB, "a subagent can spawn subagents of its own, so one prompt can grow into a tree of agents.", "Agent SDK, Subagents"),
                       "A subagent can start subagents of its own, so the hub can grow into a tree. The guide shows one hub with one layer."),
                    cf("ts-1-2-b3", D(O5, "Delegation pays off on genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to small tasks.", "Prompting Claude Opus 5"),
                       "Delegation multiplies cost and time when the tasks are small.")])
            + tab2_links("1.2", "%s Part 1.3 gives the reason." % fact("ts-1-3-d26", "The mock builder uses no subagent.")), "ts-1-2"))


# ----- part 1.4 (facts: academy/facts/ts-1-4.md) -----

HOOKS, HG, MEMD, MAO = "claude-code-docs-agent-sdk-hooks", "claude-code-docs-hooks-guide", "claude-code-docs-memory", "anthropic-docs-multiagent-orchestration"
HANDOFF14 = ('<g class="ve-n" transform="translate(640 200)"><rect class="sh" width="230" height="140" rx="0"/>'
             '<text x="115" y="26">Handoff summary</text><text class="sub" x="115" y="54">customer ID</text><text class="sub" x="115" y="78">root cause</text>'
             '<text class="sub" x="115" y="102">refund amount</text><text class="sub" x="115" y="126">recommended action</text></g>')
FIG14 = figure("1.4-1", 890, 380,
               "The agent asks for process_refund. A PreToolUse hook, which is code, checks that get_customer has returned a verified customer ID. "
               "If yes, the refund runs. If no, the hook denies the call with a reason, and the agent goes back. When the agent escalates, it calls the tool "
               "escalate_to_human with a handoff summary of customer ID, root cause, refund amount and recommended action.",
               "".join([edge("M200 80H290", "tool call", 245, 71), edge("M540 80H650", "yes", 595, 71),
                        edge("M415 130V170H110V120", "no: deny + reason", 262, 162, cls="is-hot"),
                        edge("M60 120V270H330", "the agent escalates", 195, 262),
                        edge("M560 270H640"),
                        '<text class="ve-el" x="755" y="365">the human has no transcript</text>',
                        box(20, 40, 180, 80, ["Agent"], sub="asks for a refund", cls="who-model"),
                        box(290, 30, 250, 100, ["PreToolUse hook"], sub="ID returned? (your state)"),
                        box(650, 40, 220, 80, ["process_refund"], sub="runs", cls="try ok"),
                        box(330, 230, 230, 80, ["escalate_to_human"]),
                        HANDOFF14]),
               "%s %s" % (cf("ts-1-4-f1", D(HG, "Claude Code runs them at specific points in its lifecycle, which gives you deterministic control: certain actions always happen rather than relying on the LLM to choose to run them.", "Hooks guide"),
                             "A hook runs at a fixed point of the loop, so the model does not choose whether it runs."),
                          cf("ts-1-4-f12", gx("Implement a programmatic hook that intercepts tool calls to enforce a business rule (e.g., blocking operations above a threshold amount), redirecting to an escalation workflow when triggered.", "Exam guide, section 8, exercise"),
                             "The guide practices the gate and the escalation in one exercise.")))

PART["1.4"] = (overview("1.4", "A required order needs a code gate, not a prompt",
                        "When a step must come first, such as identity verification before a refund, code blocks the later tool call until the step is done, because a prompt instruction can fail. "
                        "When the agent escalates, it gives the human a structured summary, because the human does not see the conversation.",
                        FIG14)
    + level("explanation",
            "<p><b>Code or prompt.</b> %s %s</p>" % (
                cf("ts-1-4-k1", gx("The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering", "Exam guide, 1.4-K1"),
                   "The guide separates enforcement by code, such as hooks and prerequisite gates, from guidance in a prompt (1.4-K1)."),
                cf("ts-1-4-f2", D(MEMD, "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a [PreToolUse hook](/docs/en/hooks-guide) instead.", "Claude Code, Memory"),
                   "The documentation says the same: Claude treats its instructions as context, not as enforced configuration. To block an action whatever Claude decides, use a PreToolUse hook."))
            + "<p><b>A prompt can fail.</b> %s %s</p>" % (
                cf("ts-1-4-k2", gx("When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate", "Exam guide, 1.4-K2"),
                   "When compliance must be certain, such as identity verification before a financial operation, a prompt alone has a failure rate above zero (1.4-K2)."),
                cf("ts-1-4-f14", gx("programmatic enforcement provides deterministic guarantees that prompt-based approaches cannot. Options B and C rely on probabilistic LLM compliance, which is insufficient when errors have financial consequences.", "Exam guide, sample question 1"),
                   "Sample question 1 of the guide gives the reason: code gives a guarantee, a prompt gives only a probability."))
            + "<p><b>The gate.</b> %s %s %s</p>" % (
                cf("ts-1-4-s1", gx("Implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed (e.g., blocking process_refund until get_customer has returned a verified customer ID)", "Exam guide, 1.4-S1"),
                   "Code blocks process_refund until get_customer has returned a verified customer ID (1.4-S1)."),
                cf("ts-1-4-f3", D(HOOKS, "| `PreToolUse` | Yes | Yes | Tool call request (can block or modify) |", "Agent SDK, Hooks"),
                   "In the Agent SDK, a PreToolUse hook gets each tool call before it runs, and can block it. It sees one call: whether get_customer has returned an ID is state that your code keeps."),
                cf("ts-1-4-f6", D(HOOKS, "`permissionDecisionReason` tells the model why, so it avoids retrying.", "Agent SDK, Hooks"),
                   "A deny carries a reason, so the model knows why and can call get_customer first."))
            + "<p><b>Many concerns.</b> %s %s</p>" % (
                cf("ts-1-4-s2", gx("Decomposing multi-concern customer requests into distinct items, then investigating each in parallel using shared context before synthesizing a unified resolution", "Exam guide, 1.4-S2"),
                   "A request with several issues becomes distinct items. The agent investigates each one, then joins them in one resolution (1.4-S2)."),
                cf("ts-1-4-f11", D(MAO, "Agents can act in parallel with their own isolated context", "Managed Agents, Multiagent orchestration"),
                   "The guide says &ldquo;using shared context&rdquo;. In the documentation, agents that work in parallel have their own isolated context. The exam uses the guide."))
            + "<p><b>The handoff.</b> %s Only the guide describes the content of a handoff.</p>" %
                cf("ts-1-4-s3", gx("Compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to human agents who lack access to the conversation transcript", "Exam guide, 1.4-S3"),
                   "When the agent escalates, it writes a structured summary: customer ID, root cause, refund amount and recommended action, because the human does not see the transcript (1.4-K3, 1.4-S3).")
            + exam_tests("1.4", [("Claude Agent SDK — agent definitions, agentic loops, stop_reason handling, hooks (PostToolUse, tool call interception), subagent spawning via Task tool, allowedTools configuration", "Among the technologies, the guide names")])
            + "<p>%s</p>" % cf("ts-1-4-q1", gx("Add a programmatic prerequisite that blocks lookup_order and process_refund calls until get_customer has returned a verified customer ID.", "Exam guide, sample question 1, answer A"),
                               "Sample question 1 of the guide tests 1.4-S1: its correct answer is a programmatic prerequisite.")
            + guide_text("1.4"), "ts-1-4")
    + level("depth",
            beyond([cf("ts-1-4-b1", D(HOOKS, "Claude Code doesn't run the tool call, Claude receives a tool result stating the hook didn't respond before its timeout, and the turn continues.", "Agent SDK, Hooks"),
                       "A gate that is too slow fails closed: if a PreToolUse hook does not answer before its timeout, the tool call does not run."),
                    cf("ts-1-4-b2", D(PAR, "If you run in parallel and a call fails because its prerequisite hadn't completed, return `is_error: true` with the natural error message.", "Parallel tool use"),
                       "If your code runs a prerequisite and the call that depends on it in parallel, the dependent call can fail. Your code then returns an error result."),
                    cf("ts-1-4-b3", D(PERM, "A hook that returns `allow` does not skip the deny and ask rules below", "Agent SDK, Permissions"),
                       "A hook that allows a call does not skip the deny and ask rules of the permissions.")])
            + code_pop("ts-1-4-code", "The code: a PreToolUse hook in Python", "A hook that denies a tool call", HOOKS, "import asyncio", "asyncio.run(main())", "Agent SDK, Hooks",
                       "This hook blocks a write to a .env file. A prerequisite gate uses the same deny, and also reads state that the application keeps.")
            + tab2_links("1.4") + "<p>%s %s</p>" % (
                fact("ts-1-3-d26", "The mock builder uses no hook."),
                cf("ts-1-4-s2use", excerpt(step_file(2), "Here: an instruction to the writer can fail, so each rule that the writer gets is also checked, by code or by a model.", "Build guide, step 2"),
                   "It takes the general idea: an instruction to the writer can fail, so code or a model checks each rule.")), "ts-1-4"))


# ----- part 1.5 (facts: academy/facts/ts-1-5.md) -----

HREF, LOOP = "claude-code-docs-hooks", "claude-code-docs-agent-sdk-agent-loop"
D29 = glob.glob(os.path.join(ROOT, "docs/decisions/0029-*.md"))[0][len(ROOT) + 1:]
FIG15 = figure("1.5-1", 890, 270,
               "Claude asks for a tool. A PreToolUse hook, your code, sees the call first. A deny sends a reason back to Claude. An allow lets the tool run. "
               "Then a PostToolUse hook, your code, can replace the result, for example Unix time with ISO 8601, before Claude sees it.",
               "".join([edge("M170 80H230", "call", 200, 71), edge("M400 80H460", "allow", 430, 71), edge("M610 80H670", "result", 640, 71),
                        edge("M315 120V170H130V120", "deny + reason", 222, 162, cls="is-hot"),
                        edge("M770 120V240H60V120", "updatedToolOutput: Unix time → ISO 8601", 415, 232),
                        box(20, 40, 150, 80, ["Claude"], sub="asks for a tool", cls="who-model"),
                        box(230, 40, 170, 80, ["PreToolUse"], sub="your code"),
                        box(460, 40, 150, 80, ["The tool runs"], sub="an MCP tool"),
                        box(670, 40, 200, 80, ["PostToolUse"], sub="your code")]),
               "%s %s" % (cf("ts-1-5-f2", D(HOOKS, "a tool is about to be called (`PreToolUse`), a tool returned a result (`PostToolUse`)", "Agent SDK, Hooks"),
                             "Two hook events surround each tool call: PreToolUse before it, PostToolUse after it."),
                          fact("ts-1-5-k3", "The guide calls this control deterministic.")))

PART["1.5"] = (overview("1.5", "Hooks block a tool call or clean its result",
                        "A hook is your code at a fixed point of each tool call. Before the call, it can block it. After the call, it can replace the result before Claude sees it. So code, not the model, enforces a rule and cleans the data.",
                        FIG15)
    + level("explanation",
            "<p><b>Before the call.</b> %s %s %s</p>" % (
                cf("ts-1-5-k2", gx("Hook patterns that intercept outgoing tool calls to enforce compliance rules (e.g., blocking refunds above a threshold)", "Exam guide, 1.5-K2"),
                   "A hook intercepts an outgoing tool call to enforce a rule, such as no refund above a threshold (1.5-K2)."),
                cf("ts-1-5-f9", D(LOOP, "a `PreToolUse` hook that rejects a tool call prevents it from executing, and Claude receives the rejection message instead.", "Agent SDK, The agent loop"),
                   "In the Agent SDK, a PreToolUse hook that rejects a call stops it, and Claude gets the rejection message instead."),
                cf("ts-1-5-s2", gx("Implementing tool call interception hooks that block policy-violating actions (e.g., refunds exceeding $500) and redirect to alternative workflows (e.g., human escalation)", "Exam guide, 1.5-S2"),
                   "In the guide, the hook then redirects the case, for example to a human (1.5-S2). The documentation has no redirect field: a deny gives Claude its reason (see 1.4).") + " " + cf("ts-1-5-f8", D(HOOKS, "For `PreToolUse` hooks, this is where you set `permissionDecision` (`\"allow\"`, `\"deny\"`, `\"ask\"`, or `\"defer\"`)", "Agent SDK, Hooks"),
                   "A hook can also answer &ldquo;ask&rdquo;, to ask the user. The exam uses the guide."))
            + "<p><b>After the call.</b> %s %s %s</p>" % (
                cf("ts-1-5-s1", gx("Implementing PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools before the agent processes them", "Exam guide, 1.5-S1"),
                   "A PostToolUse hook makes the data of different MCP (Model Context Protocol) tools the same, such as Unix timestamps, ISO 8601 dates and numeric status codes, before the agent uses it (1.5-K1, 1.5-S1)."),
                cf("ts-1-5-f4", D(HOOKS, "To replace the tool's output before Claude sees it, set `updatedToolOutput`, which works for any tool in both SDKs.", "Agent SDK, Hooks"),
                   "The field updatedToolOutput replaces the output before Claude sees it, for any tool, not only MCP tools. The exam uses the guide."),
                cf("ts-1-5-f6", D(HOOKS, "A regex (`^mcp__`) triggers `mcp_audit_hook` for any MCP tool whose name starts with `mcp__`.", "Agent SDK, Hooks"),
                   "A matcher, a pattern of tool names, selects the tools, for example each MCP tool."))
            + "<p><b>A guarantee.</b> %s Part 1.4 explains this contrast. %s</p>" % (
                cf("ts-1-5-k3", gx("The distinction between using hooks for deterministic guarantees versus relying on prompt instructions for probabilistic compliance", "Exam guide, 1.5-K3"),
                   "The guide contrasts the deterministic guarantee of a hook with the probable compliance of a prompt (1.5-K3, 1.5-S3)."),
                cf("ts-1-5-f12", D(PERM, "For checks that must run on every tool call, use a [`PreToolUse` hook](/docs/en/agent-sdk/hooks): hooks run before every other step, and a hook deny applies even in `bypassPermissions` mode.", "Agent SDK, Permissions"),
                   "A deny of a hook holds in each permission mode, also in the mode that skips all approvals."))
            + exam_tests("1.5", [("Claude Agent SDK — agent definitions, agentic loops, stop_reason handling, hooks (PostToolUse, tool call interception), subagent spawning via Task tool, allowedTools configuration", "Among the technologies, the guide names")])
            + guide_text("1.5"), "ts-1-5")
    + level("depth",
            beyond([cf("ts-1-5-b1", D(HREF, "`updatedToolOutput` only changes what Claude sees. The tool has already run by the time the hook fires", "Claude Code, Hooks reference"),
                       "A PostToolUse hook cannot undo an action: the tool has already run. So a refund limit belongs in a PreToolUse hook."),
                    cf("ts-1-5-b2", D(HREF, "Stripping error details that Claude needs can cause it to proceed on a false assumption.", "Claude Code, Hooks reference"),
                       "MCP output that a hook replaces gets no schema check, and a hook that removes error details can mislead Claude."),
                    cf("ts-1-5-b3", D(HG, "For decisions that require judgment rather than deterministic rules, use `type: \"prompt\"` hooks.", "Hooks guide"),
                       "Claude Code also has prompt hooks, which ask a model. Only a hook that is code is deterministic."),
                    cf("ts-1-5-b4", D(HOOKS, "`PostToolUse` and `PostToolUseFailure`: Claude Code keeps the tool result and the turn continues.", "Agent SDK, Hooks"),
                       "A PostToolUse hook that times out does not stop the turn: Claude gets the original result. So a slow normalizer lets the raw data through.")])
            + code_pop_text("ts-1-5-code", "The code: a PostToolUse hook that replaces a result", "The output of a PostToolUse hook", HREF,
                            '{\n  "hookSpecificOutput": {\n    "hookEventName": "PostToolUse",\n    "additionalContext": "Additional information for Claude",\n    "updatedToolOutput": {\n      "stdout": "[redacted]",\n      "stderr": "",\n      "interrupted": false,\n      "isImage": false\n    }\n  }\n}',
                            "Claude Code, Hooks reference", "The hook returns updatedToolOutput, and Claude sees it in place of the real output. A normalizer returns the same data in one format.")
            + tab2_links("1.5", "%s %s" % (fact("ts-1-3-d26", "The mock builder uses no hook."),
                                           cf("ts-1-5-d29", excerpt(D29, "**The plain API, not the Agent SDK.**", "Mock decision 0029"), "It calls the plain API, not the Agent SDK, so it has no SDK hooks.") + " " + cf("ts-1-5-s3use", excerpt(step_file(3), "Here: a rule with one exact answer is checked by code, not by a model.", "Build guide, step 3"),
                   "Step 3 has the nearest example: a rule with one exact answer is checked by code (task statement 1.4)."))), "ts-1-5"))


# ----- part 1.7 (facts: academy/facts/ts-1-7.md) -----

CSES, CLI, BEST, HOW = "claude-code-docs-sessions", "claude-code-docs-cli-reference", "claude-code-docs-best-practices", "claude-code-docs-how-claude-code-works"
FIG17 = figure("1.7-1", 890, 320,
               "A named session A can continue three ways. To compare two approaches, fork it: a new ID with a copy of the history. "
               "If its earlier context is mostly valid, resume it by name and tell it which files changed. If its tool results are stale, start a new session with a structured summary.",
               "".join([edge("M120 120V55H560", "compare two approaches", 340, 46),
                        edge("M220 165H280"), edge("M470 165H560", "yes", 515, 156),
                        edge("M375 210V265H560", "no: results stale", 467, 256, cls="is-hot"),
                        box(20, 120, 200, 90, ["Session A"], sub="name: auth-refactor", cls="who-model"),
                        box(280, 120, 190, 90, ["Context", "mostly valid?"]),
                        box(560, 20, 310, 70, ["--resume … --fork-session"], sub="new ID, copy of the history", cls="who-model"),
                        box(560, 125, 310, 70, ["--resume auth-refactor"], sub="same ID + the changed files", cls="who-model"),
                        box(560, 230, 310, 70, ["New session"], sub="fresh context + summary", cls="who-model")]),
               "%s %s" % (cf("ts-1-7-f4", D(HOW, "Resuming a session with `claude --continue` or `claude --resume` reopens it under the same session ID and appends new messages to the existing conversation. Forking with `--fork-session` or `/branch` copies the history into a new session ID, leaving the original unchanged.", "Claude Code, How Claude Code works"),
                             "A resume keeps the session ID. A fork copies the history into a new ID and leaves the original unchanged."),
                          cf("ts-1-7-s3", gx("Choosing between session resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale)", "Exam guide, 1.7-S3"),
                             "The guide gives the test: resume when the earlier context is mostly valid, start fresh with a summary when the tool results are stale (1.7-S3).")))

PART["1.7"] = (overview("1.7", "Resume valid context, fork to compare, restart when stale",
                        "Resume a named session when its earlier context is mostly valid, and tell it which files changed. "
                        "Fork a session to try two approaches from one analysis. Start a new session with a structured summary when the old tool results are stale.",
                        FIG17)
    + level("explanation",
            "<p><b>Resume by name.</b> %s %s %s</p>" % (
                cf("ts-1-7-k1", gx("Named session resumption using --resume \\<session-name\\> to continue a specific prior conversation", "Exam guide, 1.7-K1"),
                   "The guide resumes a named conversation with --resume and the name of the session (1.7-K1, 1.7-S1)."),
                cf("ts-1-7-f3", D(BEST, "Name sessions with `/rename` and treat them like branches: each workstream gets its own persistent context.", "Claude Code, Best practices"),
                   "The Claude Code documentation advises one named session for each workstream."),
                cf("ts-1-7-c2", D(SES, "**Resume** takes a specific session ID. You track the ID.", "Agent SDK, Sessions"),
                   "In the Agent SDK, a resume takes the session ID.") + " " + cf("ts-1-7-f1", D(CSES, "| `claude --resume <name>` | Resumes the named session directly |", "Claude Code, Sessions"),
                   "A name works in the Claude Code CLI. The exam uses the guide."))
            + "<p><b>Fork.</b> %s %s</p>" % (
                cf("ts-1-7-s2", gx("Using fork_session to create parallel exploration branches (e.g., comparing two testing strategies or refactoring approaches from a shared codebase analysis)", "Exam guide, 1.7-S2"),
                   "fork_session makes branches from one shared analysis, for example to compare two refactoring approaches (1.7-K2, 1.7-S2)."),
                cf("ts-1-7-f6", D(CLI, "| `--fork-session` | When resuming, create a new session ID instead of reusing the original (use with `--resume` or `--continue`)", "Claude Code, CLI reference"),
                   "In the CLI, the flag is --fork-session, together with --resume.") + " " + cf("ts-1-7-sdkf", D(SES, "resume=session_id,\n                  fork_session=True,", "Agent SDK, Sessions"),
                   "fork_session is the option of the Python Agent SDK. The exam uses the name of the guide."))
            + "<p><b>Stale results.</b> %s %s %s</p>" % (
                cf("ts-1-7-f8", D(CSES, "Conversation history: the full history, including tool calls and results.", "Claude Code, Sessions"),
                   "A resume brings back the full history, with the old tool calls and their results."),
                cf("ts-1-7-k4", gx("Why starting a new session with a structured summary is more reliable than resuming with stale tool results", "Exam guide, 1.7-K4"),
                   "When those tool results are stale, the guide prefers a new session with a structured summary (1.7-K4)."),
                cf("ts-1-7-f10", D(SES, "Capture the results you need (analysis output, decisions, file diffs) as application state and pass them into a fresh session", "Agent SDK, Sessions"),
                   "For a session on another machine, the Agent SDK documentation advises to capture the results and pass them into a fresh session."))
            + "<p><b>Changed files.</b> %s Only the guide asks for this.</p>" %
                cf("ts-1-7-s4", gx("Informing a resumed session about specific file changes for targeted re-analysis rather than requiring full re-exploration", "Exam guide, 1.7-S4"),
                   "When the earlier context is still mostly valid, tell the resumed session which files changed, so it analyzes only those again (1.7-K3, 1.7-S4).")
            + exam_tests("1.7", [("Session management — session resumption, fork_session, named sessions, session context isolation", "Among the technologies, the guide names")])
            + guide_text("1.7"), "ts-1-7")
    + level("depth",
            beyond([cf("ts-1-7-b1", D(SES, "Forking branches the conversation history, not the filesystem. If a forked agent edits files, those changes are real and visible to any session working in the same directory.", "Agent SDK, Sessions"),
                       "A fork branches the conversation, not the files. Two forks in one folder change the same files. The guide says &ldquo;independent branches&rdquo;, and the exam uses the guide."),
                    cf("ts-1-7-b2", D(HREF, "For mid-session events like `PostToolUse` or `UserPromptSubmit`, when you resume with `--continue` or `--resume`, Claude Code replays the saved text rather than re-running the hook for past turns, so values like timestamps or commit SHAs become stale.", "Claude Code, Hooks reference"),
                       "A resume replays the saved output of hooks in the middle of a session, so values such as timestamps become stale. Hooks at the start of a session run again."),
                    cf("ts-1-7-b3", D(CSES, "* **Resume from summary**: runs [`/compact`](/docs/en/context-window#what-survives-compaction) immediately. Later requests carry the summary instead of the full history.", "Claude Code, Sessions"),
                       "On a Pro or Max plan, when a session was inactive for about an hour and is over 100,000 tokens, Claude Code also offers a third way: resume from a summary of the old history.")])
            + code_pop("ts-1-7-code", "The code: a fork in the Agent SDK", "A fork of a session in Python", SES, "# Fork: branch from session_id into a new session", "print(message.result)", "Agent SDK, Sessions",
                       "resume takes the session ID, and fork_session=True makes a new session from its history.")
            + tab2_links("1.7") + "<p>%s %s</p>" % (
                fact("ts-1-3-d26", "The mock builder uses no session."),
                cf("ts-1-7-cc", excerpt("HANDOFF.md", "This file gives a new session what it needs to continue.", "HANDOFF.md"),
                   "The build in Claude Code shows 1.7-K4, and 1.7-S3 only in part: HANDOFF.md is a structured summary for the next session.") + " " + cf("ts-1-7-cc2", excerpt("academy/facts/claude-code.md", "Verdict: the link holds on 1.7-K4 (the structured summary for a new session). 1.7-S3 holds only in part. The named resumption and fork points are not shown.", "Fact sheet of the build in Claude Code"),
                   "No record shows --resume or fork_session.")), "ts-1-7"))


# ----- part 1.6 (facts: academy/facts/ts-1-6.md) -----

WF, CW = "claude-code-docs-workflows", "claude-code-docs-common-workflows"
FIG16 = figure("1.6-1", 890, 330,
               "Left, prompt chaining for a review whose steps are known: each file gets a local pass, then one integration pass looks across the files. "
               "Right, dynamic decomposition for an open task: map the structure, find the high-impact areas, make a prioritized plan, run the next subtask, "
               "and a dependency that the subtask finds changes the plan.",
               "".join(['<text class="ve-lab" x="20" y="30">Prompt chaining: the steps are known</text>',
                        '<text class="ve-lab" x="480" y="30">Dynamic: the steps come from findings</text>',
                        '<path class="ve-e no-head is-async" d="M455 15V320"/>',
                        edge("M200 75H230V155H260"), edge("M200 155H260"), edge("M200 235H230V155H260"),
                        '<text class="ve-el" x="215" y="300">avoids attention dilution</text>',
                        edge("M575 100V130"), edge("M575 180V210"), edge("M670 235H700"),
                        edge("M785 260V290H575V260", "a dependency found: the plan changes", 680, 310, cls="is-hot"),
                        box(20, 50, 180, 50, ["File 1"], sub="local pass", cls="who-model"),
                        box(20, 130, 180, 50, ["File 2"], sub="local pass", cls="who-model"),
                        box(20, 210, 180, 50, ["File N"], sub="local pass", cls="who-model"),
                        box(260, 120, 170, 70, ["Integration pass"], sub="across the files", cls="who-model"),
                        box(480, 50, 190, 50, ["Map the structure"]),
                        box(480, 130, 190, 50, ["High-impact areas"]),
                        box(480, 210, 190, 50, ["Prioritized plan"]),
                        box(700, 210, 170, 50, ["Next subtask"], cls="who-model")]),
               "%s %s" % (cf("ts-1-6-k1", gx("When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings", "Exam guide, 1.6-K1"),
                             "The guide contrasts a fixed sequence of steps with a decomposition that adapts to what each step finds (1.6-K1)."),
                          cf("ts-1-6-s3", gx("Decomposing open-ended tasks (e.g., \"add comprehensive tests to a legacy codebase\") by first mapping structure, identifying high-impact areas, then creating a prioritized plan that adapts as dependencies are discovered", "Exam guide, 1.6-S3"),
                             "The right panel follows the example of the guide: tests for a legacy codebase (1.6-S3).")))

PART["1.6"] = (overview("1.6", "Chain fixed steps for known work, adapt for open work",
                        "When the steps of a task are known before it starts, such as a review of many files, use a fixed chain: one pass for each file, then one pass across the files. "
                        "When the task is open, map the structure first and let each finding change the plan.",
                        FIG16)
    + level("explanation",
            "<p><b>A chain.</b> %s %s</p>" % (
                cf("ts-1-6-f1", D(PBP, "Explicit prompt chaining (breaking a task into sequential API calls) is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure.", "Prompting best practices"),
                   "Prompt chaining splits a task into a sequence of separate calls. The documentation uses it when you must see each output or enforce a fixed structure."),
                cf("ts-1-6-f2", D(PBP, "Each step is a separate API call so you can log, evaluate, or branch at any point.", "Prompting best practices"),
                   "Each step is a separate call, so you can log it, check it or branch at any point."))
            + "<p><b>A review in passes.</b> %s %s %s</p>" % (
                cf("ts-1-6-s2", gx("Splitting large code reviews into per-file local analysis passes plus a separate cross-file integration pass to avoid attention dilution", "Exam guide, 1.6-S2"),
                   "A large code review becomes one local pass for each file, plus a separate pass across the files (1.6-K2, 1.6-S2)."),
                cf("ts-1-6-f10", gx("Splitting reviews into focused passes directly addresses the root cause: attention dilution when processing many files at once.", "Exam guide, sample question 12"),
                   "The guide gives the reason: attention dilution, a loss of attention when the model processes many files at once. The documentation does not use this term, and the exam uses the guide."),
                cf("ts-1-6-f11", gx("Option C misunderstands that larger context windows don't solve attention quality issues.", "Exam guide, sample question 12"),
                   "A larger context window does not fix it."))
            + "<p><b>An adaptive plan.</b> %s %s %s</p>" % (
                cf("ts-1-6-k3", gx("The value of adaptive investigation plans that generate subtasks based on what is discovered at each step", "Exam guide, 1.6-K3"),
                   "For an open investigation, the plan makes its next subtasks from what each step finds (1.6-K3)."),
                cf("ts-1-6-f5", D(HOW, "Claude decides what each step requires based on what it learned from the previous step, chaining dozens of actions together and course-correcting along the way.", "Claude Code, How Claude Code works"),
                   "This is how the loop of Claude Code works: each step depends on what the step before found."),
                cf("ts-1-6-f12", D(BEST, "Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified.", "Claude Code, Best practices"),
                   "Planning first is most useful when the approach is not clear or the code is not familiar."))
            + "<p><b>The choice.</b> %s %s</p>" % (
                cf("ts-1-6-s1", gx("Selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks", "Exam guide, 1.6-S1"),
                   "Use a chain for a predictable review with many aspects, and a dynamic decomposition for an open investigation (1.6-S1)."),
                cf("ts-1-6-46", gx("Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis", "Exam guide, 4.6-S2"),
                   "Task statement 4.6 uses the same split of a review (4.6-S2)."))
            + exam_tests("1.6", [("Prompt chaining — sequential task decomposition into focused passes", "Among the technologies, the guide names")])
            + "<p>%s</p>" % cf("ts-1-6-q12", gx("Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.", "Exam guide, sample question 12, answer A"),
                               "Sample question 12 of the guide fits 1.6-S2: its correct answer is a pass for each file, then an integration pass.")
            + guide_text("1.6"), "ts-1-6")
    + level("depth",
            beyond([cf("ts-1-6-b1", D(WF, "use a workflow to review every file changed in this PR for correctness issues, then merge the per-file findings into one ranked summary", "Claude Code, Workflows"),
                       "Claude Code can run the chain as a workflow: a script reviews each changed file, then merges the findings.") + " " + cf("ts-1-6-b1b", D(WF, "A workflow moves the plan into code.", "Claude Code, Workflows"),
                       "In a workflow, the script holds the plan. With a fixed list of passes, it is nearer to the fixed chain of the guide than to its dynamic decomposition."),
                    cf("ts-1-6-b2", D(BEST, "Run [`/batch <instruction>`](/docs/en/commands#all-commands) to have Claude split the change across 5 to 30 subagents. Each subagent works in its own worktree.", "Claude Code, Best practices"),
                       "For a large change, the command /batch splits the work across 5 to 30 subagents, each in its own copy of the repository."),
                    cf("ts-1-6-b3", D(PBP, "With adaptive thinking and subagent orchestration, Claude handles most multistep reasoning internally.", "Prompting best practices"),
                       "With adaptive thinking, in which Claude decides how much to think, the documentation says that Claude handles most reasoning in several steps by itself.")])
            + code_pop("ts-1-6-code", "The code: a workflow with one agent for each file", "A workflow that splits a review by file", WF, "export const meta = {", "return audits.filter(Boolean)", "Claude Code, Workflows",
                       "One agent lists the files. Then one agent audits each file. The example has no integration pass.")
            + tab2_links("1.6") + "<p>%s %s</p>" % (
                cf("ts-1-6-use", excerpt(step_file(1), "So these points support only one idea: the work of a mock is known before it starts, so the program can fix the plan before the writing starts.", "Build guide, step 1"),
                   "Step 1 takes only one part of 1.6: the work of a mock is known before it starts, so code fixes the plan first."), cf("ts-1-6-rev", excerpt("docs/reviews/review-decisions-0003-to-0018.md", "A list of 60 slots made by code for a generation task is neither a review nor a prompt chain.", "Review of mock decisions 0003 to 0018"),
                   "It is not a prompt chain.")), "ts-1-6"))


# ----- part 2.1 (facts: academy/facts/ts-2-1.md) -----

DEFT, OVT, TRB, TSR, CCMCP = "anthropic-docs-define-tools", "anthropic-docs-tool-use-overview", "anthropic-docs-troubleshooting-tool-use", "anthropic-docs-tool-search-tool", "claude-code-docs-mcp"
D40 = glob.glob(os.path.join(ROOT, "docs/decisions/0040-*.md"))[0][len(ROOT) + 1:]
GOOD21 = "\n".join(read(SRC % DEFT).split("\n")[92:106])
assert GOOD21.strip().startswith("{") and '"name": "get_stock_price"' in GOOD21 and GOOD21.rstrip().endswith("}")
FIG21 = figure("2.1-1", 890, 270,
               "Before: a request for the results of a web page can go to analyze_content or to analyze_document, because both say only that they analyze content. "
               "After: analyze_content is renamed extract_web_results with a web-specific description, and analyze_document is split into tools with contracts, so the request has one clear tool.",
               "".join(['<text class="ve-lab" x="20" y="24">Before: near-identical descriptions</text>',
                        '<text class="ve-lab" x="480" y="24">After: renamed and split</text>',
                        '<path class="ve-e no-head is-async" d="M455 10V260"/>',
                        edge("M190 130H220V90H250", cls="is-async"), edge("M190 150H220V190H250", cls="is-async"),
                        '<text class="ve-el" x="130" y="215">which one?</text>',
                        edge("M620 140H635V70H650", cls="is-hot"),
                        box(20, 110, 170, 60, ["Get the results", "of this web page"], cls="who-model"),
                        box(250, 60, 190, 60, ["analyze_content"], sub="analyzes content"),
                        box(250, 160, 190, 60, ["analyze_document"], sub="analyzes content"),
                        box(470, 110, 150, 60, ["Get the results", "of this web page"], cls="who-model"),
                        box(650, 40, 230, 60, ["extract_web_results"], sub="web-specific description", cls="try ok"),
                        box(650, 140, 230, 90, ["analyze_document"], sub="3 tools with contracts")]),
               "%s %s" % (cf("ts-2-1-f1", D(OVT, "Claude determines when to call a tool based on the user's request and the tool's description.", "Tool use overview"),
                             "Claude chooses a tool from the request and the description of the tool."),
                          cf("ts-2-1-s2", gx("Renaming tools and updating descriptions to eliminate functional overlap (e.g., renaming analyze_content to extract_web_results with a web-specific description)", "Exam guide, 2.1-S2"),
                             "The renamed tool is the example of the guide (2.1-S2).")))

PART["2.1"] = (overview("2.1", "The description decides which tool Claude picks",
                        "Claude chooses among tools mainly by their descriptions. So each description says what the tool does, its inputs, its output, and when to use it instead of a similar tool. "
                        "Rename or split tools that overlap, and check the system prompt for words that pull Claude to the wrong tool.",
                        FIG21)
    + level("explanation",
            "<p><b>The description chooses.</b> %s %s</p>" % (
                cf("ts-2-1-k1", gx("Tool descriptions as the primary mechanism LLMs use for tool selection; minimal descriptions lead to unreliable selection among similar tools", "Exam guide, 2.1-K1"),
                   "The guide calls the description the primary mechanism of tool selection, and a minimal description makes the choice among similar tools unreliable (2.1-K1)."),
                cf("ts-2-1-f2", D(DEFT, "**Provide extremely detailed descriptions.** This is by far the most important factor in tool performance.", "Define tools"),
                   "The documentation calls a detailed description by far the most important factor in tool performance."),
                )
            + "<p><b>What it holds.</b> %s %s %s %s</p>" % (
                cf("ts-2-1-k2", gx("The importance of including input formats, example queries, edge cases, and boundary explanations in tool descriptions", "Exam guide, 2.1-K2"),
                   "The guide puts input formats, example queries, edge cases and boundaries in the description (2.1-K2)."),
                cf("ts-2-1-s1", gx("Writing tool descriptions that clearly differentiate each tool's purpose, expected inputs, outputs, and when to use it versus similar alternatives", "Exam guide, 2.1-S1"),
                   "Each description says the purpose, the inputs, the outputs, and when to use the tool instead of a similar one (2.1-S1). A tool definition has no output field, so the output goes into the description."),
                cf("ts-2-1-f5", D(DEFT, "Aim for at least 3–4 sentences for each tool description, more if the tool is complex.", "Define tools"),
                   "The documentation asks for at least 3 or 4 sentences."),
                cf("ts-2-1-c3", D(DEFT, "for tools with complex inputs, nested objects, or format-sensitive parameters, you can use the `input_examples` field to provide schema-validated examples.", "Define tools"),
                   "For complex tools, the documentation adds a field input_examples, with example inputs, which are not the example queries of the guide."))
            + "<p><b>Overlap.</b> %s %s %s</p>" % (
                cf("ts-2-1-k3", gx("How ambiguous or overlapping tool descriptions cause misrouting (e.g., analyze_content vs analyze_document with near-identical descriptions)", "Exam guide, 2.1-K3"),
                   "Near-identical descriptions cause misrouting (2.1-K3)."),
                cf("ts-2-1-f7", D(TRB, "Sharpen descriptions. Differentiate tools by WHEN to use them, not only WHAT they do.", "Troubleshooting tool use"),
                   "The documentation separates tools by when to use them, not only by what they do."),
                cf("ts-2-1-f9", D(DEFT, "When your tools span multiple services or resources, prefix names with the service (for example, `github_list_prs`, `slack_send_message`). This makes tool selection unambiguous as your library grows", "Define tools"),
                   "When tools span several services, a prefix of the service in each name also makes the choice unambiguous."))
            + "<p><b>Split or join.</b> %s %s</p>" % (
                cf("ts-2-1-s3", gx("Splitting generic tools into purpose-specific tools with defined input/output contracts (e.g., splitting a generic analyze_document into extract_data_points, summarize_content, and verify_claim_against_source)", "Exam guide, 2.1-S3"),
                   "The guide splits a generic tool, such as analyze_document, into tools with one purpose and a defined input and output each (2.1-S3)."),
                cf("ts-2-1-c1", D(DEFT, "**Consolidate related operations into fewer tools.** Rather than creating a separate tool for every action (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter.", "Define tools"),
                   "The documentation also advises to join related actions into one tool with an action parameter. The guide names both splitting and joining, and the exam uses the guide."))
            + "<p><b>The system prompt.</b> %s %s %s %s</p>" % (
                cf("ts-2-1-f11", D(DEFT, "the API constructs a special system prompt from the tool definitions, tool configuration, and any user-specified system prompt.", "Define tools"),
                   "Claude reads the tool definitions and your system prompt in one prompt."),
                cf("ts-2-1-k4", gx("The impact of system prompt wording on tool selection: keyword-sensitive instructions can create unintended tool associations", "Exam guide, 2.1-K4"),
                   "The guide says that a keyword in the system prompt can tie a request to the wrong tool (2.1-K4). The documentation has no such statement, and the exam uses the guide."),
                cf("ts-2-1-s4", gx("Reviewing system prompts for keyword-sensitive instructions that might override well-written tool descriptions", "Exam guide, 2.1-S4"),
                   "So you review the system prompt for words that might override good tool descriptions (2.1-S4)."),
                cf("ts-2-1-f13", D(PBP, "If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language.", "Prompting best practices"),
                   "The documentation warns that Claude Opus 4.5 and 4.6 follow the system prompt more closely, so aggressive words can make them call a tool too often."))
            + exam_tests("2.1", [("Tool interface design: writing effective tool descriptions, splitting vs consolidating tools, tool naming to reduce ambiguity", "Among the topics, the guide names")])
            + "<p>%s</p>" % cf("ts-2-1-q2", gx("Expand each tool's description to include input formats it handles, example queries, edge cases, and boundaries explaining when to use it versus similar tools.", "Exam guide, sample question 2, answer B"),
                               "Sample question 2 of the guide fits 2.1: its correct answer expands each description.")
            + guide_text("2.1"), "ts-2-1")
    + level("depth",
            beyond([cf("ts-2-1-b1", D(CCMCP, "Claude Code truncates each tool description and each server's instructions at 2,048 characters by default.", "Claude Code, MCP"),
                       "Claude Code cuts each MCP tool description at 2,048 characters by default, so the important details go first."),
                    ])
            + code_pop_text("ts-2-1-code", "The code: a good tool description", "A tool definition with a detailed description", DEFT, GOOD21, "Define tools",
                            "The description says what the tool returns, when to use it, and what it does not provide.")
            + tab2_links("2.1", cf("ts-2-1-d40", excerpt(D40, "2. Structured outputs: the request carries the JSON schema in `output_config.format`, and the API makes the answer agree with it. No tool.", "Mock decision 0040"),
                                   "The mock builder sends the model no tool: each answer must fit a JSON schema that the request carries, so Claude never chooses a tool.")), "ts-2-1"))


# ----- part 2.2 (facts: academy/facts/ts-2-2.md) -----

HANDLE, SDKT = "anthropic-docs-handle-tool-calls", "claude-code-docs-agent-sdk-custom-tools"
ERR22 = "\n".join(read(SRC % HANDLE).split("\n")[207:218])
assert ERR22.strip().startswith("{") and '"is_error": true' in ERR22 and ERR22.rstrip().endswith("}")
FIG22 = figure("2.2-1", 890, 380,
               "An agent calls an MCP tool. A success returns data. A success with no matches is a valid empty result, not an error. A failure returns isError true, "
               "with a category, whether a retry can help, and a text. A transient error is retried in the subagent and passed up only if it still fails. "
               "A validation error needs new input. A business error is not retriable and the agent explains it. For a permission error, the guide names no action.",
               "".join([edge("M190 165H225", cls="no-head"), '<path class="ve-e no-head" d="M225 45V215"/>',
                        edge("M225 45H260"), edge("M225 115H260"), edge("M225 215H260", cls="is-hot"),
                        edge("M490 215H515", cls="no-head"), '<path class="ve-e no-head" d="M515 175V346"/>',
                        edge("M515 175H540"), edge("M515 232H540"), edge("M515 289H540"), edge("M515 346H540"),
                        box(20, 130, 170, 70, ["Agent"], sub="calls an MCP tool", cls="who-model"),
                        box(260, 20, 230, 50, ["data"], sub="success", cls="try ok"),
                        box(260, 90, 230, 50, ["no matches"], sub="success, not an error", cls="try ok"),
                        box(260, 170, 230, 90, ["isError: true"], sub="category · retry? · text"),
                        box(540, 150, 330, 50, ["transient"], sub="retry; pass up if it still fails"),
                        box(540, 207, 330, 50, ["validation"], sub="fix the input, call again"),
                        box(540, 264, 330, 50, ["business"], sub="retriable: false, explain it"),
                        box(540, 321, 330, 50, ["permission"], sub="the guide names no action")]),
               "%s %s" % (cf("ts-2-2-k2", gx("The distinction between transient errors (timeouts, service unavailability), validation errors (invalid input), business errors (policy violations), and permission errors", "Exam guide, 2.2-K2"),
                             "The four categories of errors are those of the guide (2.2-K2)."),
                          cf("ts-2-2-s4", gx("Distinguishing between access failures (needing retry decisions) and valid empty results (representing successful queries with no matches)", "Exam guide, 2.2-S4"),
                             "An empty result of a query that succeeded is not an access failure (2.2-S4).")))

PART["2.2"] = (overview("2.2", "Errors must say what failed and whether a retry helps",
                        "Mark a failed tool call with the error flag, and say the category, whether a new try can help, and what went wrong, so the agent can retry, fix its input, explain or escalate. "
                        "An empty result of a query that succeeded is not an error.",
                        FIG22)
    + level("explanation",
            "<p><b>The flag.</b> %s %s %s</p>" % (
                cf("ts-2-2-k1", gx("The MCP isError flag pattern for communicating tool failures back to the agent", "Exam guide, 2.2-K1"),
                   "A tool reports a failure to the agent with the isError flag of MCP (2.2-K1)."),
                cf("ts-2-2-f3", D(SDKT, "`isError` (optional): set to `true` to signal a tool failure so Claude can react to it.", "Agent SDK, Custom tools"),
                   "A TypeScript tool of the Agent SDK sets isError to true, so Claude can react to the failure."),
                cf("ts-2-2-f1", D(HANDLE, "`is_error` (optional): Set to `true` if the tool execution resulted in an error.", "Handle tool calls"),
                   "In the Claude API, the same flag is is_error on the tool result."))
            + "<p><b>Say what failed.</b> %s %s %s</p>" % (
                cf("ts-2-2-k3", gx("Why uniform error responses (generic \"Operation failed\") prevent the agent from making appropriate recovery decisions", "Exam guide, 2.2-K3"),
                   "A generic &ldquo;Operation failed&rdquo; leaves the agent with no basis to decide how to recover (2.2-K3)."),
                cf("ts-2-2-f6", D(HANDLE, "Instead of generic errors like `\"failed\"`, include what went wrong and what Claude should try next", "Handle tool calls"),
                   "The documentation agrees: say what went wrong and what Claude should try next."),
                cf("ts-2-2-f7", D(SDKT, "In both cases Claude can retry, try a different tool, or explain the failure.", "Agent SDK, Custom tools"),
                   "With an error result, Claude can retry, try a different tool, or explain the failure."))
            + "<p><b>The metadata.</b> %s %s</p>" % (
                cf("ts-2-2-s1", gx("Returning structured error metadata including errorCategory (transient/validation/permission), isRetryable boolean, and human-readable descriptions", "Exam guide, 2.2-S1"),
                   "The guide returns an errorCategory, an isRetryable flag and a description that a person can read (2.2-S1). Its list of categories has three, without business errors, which 2.2-S2 handles with retriable: false."),
                cf("ts-2-2-f2", D(HANDLE, "you can return the error message in the `content` along with `\"is_error\": true`:", "Handle tool calls"),
                   "These field names are the guide's: the documentation shows the flag and an error message in the content. The exam uses the guide."))
            + "<p><b>Retry or not.</b> %s %s %s</p>" % (
                cf("ts-2-2-k4", gx("The difference between retryable and non-retryable errors, and how returning structured metadata prevents wasted retry attempts", "Exam guide, 2.2-K4"),
                   "Metadata that says whether an error is retryable prevents wasted retries (2.2-K4)."),
                cf("ts-2-2-f8", D(HANDLE, "If a tool request is invalid or missing parameters, Claude will retry 2-3 times with corrections before apologizing to the user.", "Handle tool calls"),
                   "For invalid input, Claude tries again 2 or 3 times with corrections."),
                cf("ts-2-2-s2", gx("Including retriable: false flags and customer-friendly explanations for business rule violations so the agent can communicate appropriately", "Exam guide, 2.2-S2"),
                   "A business rule violation gets retriable: false and an explanation for the customer, so the agent can tell the customer (2.2-S2)."))
            + "<p><b>Recover locally.</b> %s %s</p>" % (
                cf("ts-2-2-s3", gx("Implementing local error recovery within subagents for transient failures, propagating to the coordinator only errors that cannot be resolved locally along with partial results and what was attempted", "Exam guide, 2.2-S3"),
                   "A subagent recovers from a transient failure itself, and passes to the coordinator only what it cannot fix, with its partial results and what it tried (2.2-S3)."),
                cf("ts-2-2-53", gx("Having subagents implement local recovery for transient failures and only propagate errors they cannot resolve, including what was attempted and partial results", "Exam guide, 5.3-S3"),
                   "Task statement 5.3 has the same point (5.3-S3)."))
            + exam_tests("2.2", [("Error handling and propagation: structured error responses, transient vs business vs permission errors, local recovery before escalation", "Among the topics, the guide names")])
            + guide_text("2.2"), "ts-2-2")
    + level("depth",
            beyond([cf("ts-2-2-b1", D(CCMCP, "Error text longer than about 11,000 characters keeps only its first 5,000 and last 5,000 characters", "Claude Code, MCP"),
                       "When Claude Code is the MCP client, it cuts an error text longer than about 11,000 characters, for a call that completes in the foreground. So the category and the retry advice go first."),
                    cf("ts-2-2-b2", D(SDKT, "The Python `@tool` decorator forwards only `content` and `is_error` from the handler's return dict. To return `structuredContent` from Python, run a [standalone MCP server](/docs/en/agent-sdk/mcp) instead of an in-process SDK server.", "Agent SDK, Custom tools"),
                       "The Python @tool decorator of an in-process SDK server forwards only the content and the flag, so there the metadata goes into the text. A standalone MCP server can return structured content."),
                    cf("ts-2-2-b3", D(SDKT, "| Handler throws an uncaught exception | The MCP server converts it to an error result carrying the raw exception message. Claude sees that message, and the agent loop continues. |", "Agent SDK, Custom tools"),
                       "In the in-process MCP server of the Agent SDK, an uncaught exception does not stop the loop, but Claude then sees only the raw message, which is close to a generic error.")])
            + code_pop_text("ts-2-2-code", "The code: an error result in the Claude API", "A tool result with is_error", HANDLE, ERR22, "Handle tool calls",
                            "The example has the flag and a message, and no errorCategory or isRetryable field.")
            + tab2_links("2.2", "%s %s" % (fact("ts-2-4-a02", "The mock builder uses no MCP server: it calls only the Claude API and reads local files."),
                                           cf("ts-2-2-near", excerpt("src/model_call.py", "# 429, 5xx and network errors. Each other error stops the run.", "The code of the model calls"),
                                              "It has a near case for errors of the Claude API, not of tools: a new call repairs a rate limit, a server error or a network error, and each other error stops the run."))), "ts-2-2"))


# ----- part 2.3 (facts: academy/facts/ts-2-3.md) -----

YAML23 = "---\nname: safe-researcher\ndescription: Research agent with restricted capabilities\ntools: Read, Grep, Glob, Bash\n---"
FIG23 = figure("2.3-1", 890, 350,
               "A coordinator delegates to four agents of the research system, and each agent has only the tools of its role: web search tools, load_document, "
               "verify_fact. The guide names no tools for the report agent. The synthesis agent checks a simple fact with its own verify_fact tool, and sends a complex check through the coordinator.",
               "".join(['<path class="ve-e no-head" d="M445 90V120M120 120H780"/>',
                        edge("M120 120V150"), edge("M340 120V150"), edge("M560 120V150"), edge("M780 120V150"),
                        edge("M560 240V280", "simple check", 568, 265, anchor="r"),
                        edge("M640 150V55H560", "complex check, through the coordinator", 735, 46, cls="is-hot"),
                        box(330, 20, 230, 70, ["Coordinator"], sub="delegates", cls="who-model"),
                        box(20, 150, 200, 90, ["Web search"], sub="web search tools", cls="who-model"),
                        box(240, 150, 200, 90, ["Document", "analysis"], sub="load_document", cls="who-model"),
                        box(460, 150, 200, 90, ["Synthesis"], sub="no web search tools", cls="who-model"),
                        box(680, 150, 190, 90, ["Report"], sub="(not in the guide)", cls="who-model"),
                        box(440, 280, 240, 50, ["verify_fact"], sub="a scoped cross-role tool", cls="try ok")]),
               "%s %s" % (cf("ts-2-3-k3", gx("Scoped tool access: giving agents only the tools needed for their role, with limited cross-role tools for specific high-frequency needs", "Exam guide, 2.3-K3"),
                             "Each agent gets only the tools of its role, plus a narrow tool for a frequent need (2.3-K3)."),
                          cf("ts-2-3-f14", gx("Option A applies the principle of least privilege by giving the synthesis agent only what it needs for the 85% common case (simple fact verification) while preserving the existing coordination pattern for complex cases.", "Exam guide, sample question 9"),
                             "In sample question 9 of the guide, verify_fact serves the 85% of simple checks, and complex checks keep the route through the coordinator.")))

PART["2.3"] = (overview("2.3", "Give each agent only the tools that its role needs",
                        "Each agent gets a small set of tools for its role, plus a narrow shared tool for a frequent need, and the coordinator handles the rest. "
                        "tool_choice sets whether Claude can, must, or must use one named tool, but Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 reject any and a forced tool.",
                        FIG23)
    + level("explanation",
            "<p><b>Few tools.</b> %s %s</p>" % (
                cf("ts-2-3-k1", gx("The principle that giving an agent access to too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability by increasing decision complexity", "Exam guide, 2.3-K1"),
                   "Too many tools, such as 18 instead of 4 or 5, make the choice of tool less reliable (2.3-K1)."),
                cf("ts-2-3-f1", D(TSR, "Claude's ability to pick the right tool degrades once you exceed 30–50 available tools.", "Tool search tool"),
                   "The documentation puts the drop higher, above 30 to 50 tools. The exam uses the guide."))
            + "<p><b>Scope by role.</b> %s %s %s</p>" % (
                cf("ts-2-3-s1", gx("Restricting each subagent's tool set to those relevant to its role, preventing cross-specialization misuse", "Exam guide, 2.3-S1"),
                   "Each subagent gets only the tools of its role (2.3-S1).") + " " + cf("ts-2-3-k2", gx("Why agents with tools outside their specialization tend to misuse them (e.g., a synthesis agent attempting web searches)", "Exam guide, 2.3-K2"),
                   "The guide says that an agent with tools of another role tends to misuse them, such as a synthesis agent that searches the web (2.3-K2)."),
                cf("ts-2-3-f5", D(SUB, "subagents can be limited to specific tools, reducing the risk of unintended actions", "Agent SDK, Subagents"),
                   "The Agent SDK documentation gives its own reason: fewer tools reduce the risk of unintended actions."),
                fact("ts-1-3-f10", "In the Agent SDK, a tool that the list of a subagent leaves out is not in its session."))
            + "<p><b>Narrow tools.</b> %s %s</p>" % (
                cf("ts-2-3-s2", gx("Replacing generic tools with constrained alternatives (e.g., replacing fetch_url with load_document that validates document URLs)", "Exam guide, 2.3-S2"),
                   "A generic tool becomes a constrained one, such as load_document that checks document URLs, in place of fetch_url (2.3-S2). Part 2.1 shows that the documentation also advises to join related actions."),
                cf("ts-2-3-s3", gx("Providing scoped cross-role tools for high-frequency needs (e.g., a verify_fact tool for the synthesis agent) while routing complex cases through the coordinator", "Exam guide, 2.3-S3"),
                   "A narrow tool of another role serves a frequent need, and complex cases still go through the coordinator (2.3-S3). Only the guide describes these two points."))
            + "<p><b>tool_choice.</b> %s %s %s %s %s %s</p>" % (
                cf("ts-2-3-k4", gx("tool_choice configuration options: \"auto\", \"any\", and forced tool selection ({\"type\": \"tool\", \"name\": \"...\"})", "Exam guide, 2.3-K4"),
                   "The guide names three options: auto, any, and a forced tool (2.3-K4)."),
                cf("ts-2-3-s5", gx("Setting tool_choice: \"any\" to guarantee the model calls a tool rather than returning conversational text", "Exam guide, 2.3-S5"),
                   "With any, Claude must call a tool and gives no text (2.3-S5)."),
                cf("ts-2-3-s4", gx("Using tool_choice forced selection to ensure a specific tool is called first (e.g., forcing extract_metadata before enrichment tools), then processing subsequent steps in follow-up turns", "Exam guide, 2.3-S4"),
                   "A forced tool makes one tool run first, and the next steps follow in later turns (2.3-S4)."),
                cf("ts-2-3-f9", D(DEFT, "* `none` prevents Claude from using any tools. This is the default value when no `tools` are provided.", "Define tools"),
                   "The documentation names four: it adds none, which blocks all tools."),
                cf("ts-2-3-f13", D(DEFT, "| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://platform.claude.com/docs/en/models/mythos-5-1/overview) | `any` and `tool` return a [400 error]", "Define tools"),
                   "Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 return a 400 error for any and for a forced tool."),
                "The exam uses the guide.")
            + exam_tests("2.3", [("Claude API — tool_use with JSON schemas, tool_choice options (\"auto\", \"any\", forced tool selection), stop_reason values (\"tool_use\", \"end_turn\"), max_tokens, system prompts", "Among the technologies, the guide names")])
            + "<p>%s</p>" % cf("ts-2-3-q9", gx("Give the synthesis agent a scoped verify_fact tool for simple lookups, while complex verifications continue delegating to the web search agent through the coordinator.", "Exam guide, sample question 9, answer A"),
                               "Sample question 9 of the guide tests 2.3-S3: its correct answer is a scoped verify_fact tool.")
            + guide_text("2.3"), "ts-2-3")
    + level("depth",
            beyond([cf("ts-2-3-b1", D(SDKT, "`tools` and bare-name `disallowedTools` entries change availability. `allowedTools` and scoped `disallowedTools` rules change permission.", "Agent SDK, Custom tools"),
                       "In the Agent SDK, the list tools removes a tool, but allowedTools only changes its permission. The guide does not separate the two."),
                    cf("ts-2-3-b2", D(DEFT, "changes to the `tool_choice` parameter will invalidate cached message blocks.", "Define tools"),
                       "A change of tool_choice between turns, as in 2.3-S4, invalidates part of the prompt cache."),
                    cf("ts-2-3-b3", D(TSR, "Because tool search loads only a focused set of relevant tools on demand, selection accuracy stays high even across thousands of tools.", "Tool search tool"),
                       "With very many tools, tool search loads only the relevant ones, on the models that support it.")])
            + code_pop_text("ts-2-3-code", "The code: a subagent with a list of tools", "A Claude Code subagent with an allowlist", CCS, YAML23, "Claude Code, Subagents",
                            "The field tools lists the only tools of the subagent.")
            + tab2_links("2.3", cf("ts-2-3-d40", excerpt(D40, "The current Claude models do not accept a forced tool call.", "Mock decision 0040"),
                                   "No step gives an agent a set of tools. Step 2 of tab 2 tells why the build sends no forced tool call: Claude Opus 5.5, the model of the build, does not accept one.")
                         + ' <a href="%s#step-2">Step 2, Write the question &rarr;</a>' % TAB2), "ts-2-3"))


# ----- part 2.4 (facts: academy/facts/ts-2-4.md) -----

SDKM = "claude-code-docs-agent-sdk-mcp"
A02 = glob.glob(os.path.join(ROOT, "academy/decisions/0002-*.md"))[0][len(ROOT) + 1:]
MCP24 = "\n".join(read(SRC % CCMCP).split("\n")[650:661])
assert MCP24.startswith("{") and "${API_KEY}" in MCP24 and MCP24.rstrip().endswith("}")
FIG24 = figure("2.4-1", 890, 320,
               "An environment variable expands into .mcp.json, the project file that the team commits. ~/.claude.json holds the personal servers of a user. "
               "Claude Code connects to the servers of both files, and the agent gets the tools of all servers together. Resources show the agent what data exists.",
               "".join([edge("M145 80V110", "${VAR} expands", 153, 99, anchor="r"),
                        edge("M270 150H305V180H340"), edge("M270 260H305V180H340"),
                        edge("M540 180H580V80H620"), edge("M745 220V120", "what data exists", 753, 175, anchor="r"),
                        box(20, 20, 250, 60, ["environment"], sub="the secret, not in git"),
                        box(20, 110, 250, 80, [".mcp.json"], sub="project: team, committed"),
                        box(20, 220, 250, 80, ["~/.claude.json"], sub="user: personal servers"),
                        box(340, 140, 200, 80, ["Claude Code"], sub="connects to each"),
                        box(620, 40, 250, 80, ["The agent"], sub="tools of all servers", cls="who-model"),
                        box(620, 220, 250, 80, ["Resources"], sub="issues, schemas, docs")]),
               "%s %s" % (cf("ts-2-4-k1", gx("MCP server scoping: project-level (.mcp.json) for shared team tooling vs user-level (~/.claude.json) for personal/experimental servers", "Exam guide, 2.4-K1"),
                             "The guide puts shared team servers in the project file .mcp.json, and personal servers in ~/.claude.json (2.4-K1)."),
                          cf("ts-2-4-k3", gx("That tools from all configured MCP servers are discovered at connection time and available simultaneously to the agent", "Exam guide, 2.4-K3"),
                             "The tools of all configured servers are available to the agent at the same time (2.4-K3).")))

PART["2.4"] = (overview("2.4", "Share MCP servers in .mcp.json, with secrets in variables",
                        "A team commits its shared MCP servers in .mcp.json and writes each token as an environment variable. A person keeps private servers in ~/.claude.json. "
                        "The agent gets the tools of all servers together, and resources show it what data exists before it searches.",
                        FIG24)
    + level("explanation",
            "<p><b>Two files.</b> %s %s %s</p>" % (
                cf("ts-2-4-f2", D(CCMCP, "Check `.mcp.json` into version control so everyone on your team gets the same MCP tools and services.", "Claude Code, MCP"),
                   "The team commits .mcp.json, so that each member gets the same MCP servers (2.4-S1)."),
                cf("ts-2-4-f3", D(CCMCP, "User-scoped servers are stored in `~/.claude.json` and provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account.", "Claude Code, MCP"),
                   "User scope is in ~/.claude.json, for all the projects of one person (2.4-S2)."),
                cf("ts-2-4-c1", D(CCMCP, "Local scope is the default. A local-scoped server loads only in the project where you added it and stays private to you. Claude Code stores it in `~/.claude.json` under that project's path, so the same server won't appear in your other projects. Use local scope for personal development servers, experimental configurations, or servers with credentials you don't want in version control.", "Claude Code, MCP"),
                   "The documentation has a third scope: local, the default, also in ~/.claude.json, which it names for experimental servers. The exam uses the guide."))
            + "<p><b>Secrets.</b> %s %s</p>" % (
                cf("ts-2-4-k2", gx("Environment variable expansion in .mcp.json (e.g., ${GITHUB_TOKEN}) for credential management without committing secrets", "Exam guide, 2.4-K2"),
                   "In .mcp.json, a token is a variable such as ${GITHUB_TOKEN}, so the secret is never committed (2.4-K2)."),
                cf("ts-2-4-f6", D(CCMCP, "allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys", "Claude Code, MCP"),
                   "Claude Code expands the variable when it loads the file, so a team shares the file and each person keeps the key."))
            + "<p><b>All tools at once.</b> %s %s</p>" % (
                cf("ts-2-4-f9", D(SDKM, "MCP tools follow the naming pattern `mcp__<server-name>__<tool-name>`.", "Agent SDK, MCP"),
                   "In the Agent SDK, each MCP tool name carries the name of its server: mcp__server__tool."),
                cf("ts-2-4-c3", D(CCMCP, "Tool search is enabled by default: MCP tools are deferred and discovered on demand.", "Claude Code, MCP"),
                   "The guide says that the tools are discovered at connection time. In Claude Code, tool search is on by default for first-party hosts: MCP tools are deferred and discovered on demand. The exam uses the guide."))
            + "<p><b>Resources.</b> %s %s</p>" % (
                cf("ts-2-4-s5", gx("Exposing content catalogs as MCP resources to give agents visibility into available data without requiring exploratory tool calls", "Exam guide, 2.4-S5"),
                   "The guide says that a catalog exposed as resources lets the agent see what data exists without exploratory tool calls (2.4-S5).") + " " + cf("ts-2-4-k4", gx("MCP resources as a mechanism for exposing content catalogs (e.g., issue summaries, documentation hierarchies, database schemas) to reduce exploratory tool calls", "Exam guide, 2.4-K4"),
                   "Examples are issue summaries and database schemas (2.4-K4)."),
                cf("ts-2-4-f13", D(CCMCP, "Claude Code automatically provides tools to list and read MCP resources when servers support them", "Claude Code, MCP"),
                   "In Claude Code, Claude itself lists and reads resources with tool calls. The exam uses the guide."))
            + "<p><b>Good servers.</b> %s Part 2.1 shows how. %s %s</p>" % (
                cf("ts-2-4-s3", gx("Enhancing MCP tool descriptions to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools (like Grep) over more capable MCP tools", "Exam guide, 2.4-S3"),
                   "The guide says that a detailed description of an MCP tool keeps the agent from using a built-in tool such as Grep in its place (2.4-S3)."),
                cf("ts-2-4-s4", gx("Choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira), reserving custom servers for team-specific workflows", "Exam guide, 2.4-S4"),
                   "For a standard integration such as Jira, the guide uses an existing community server, and a custom server only for a workflow of the team (2.4-S4)."),
                cf("ts-2-4-c6", D(CCMCP, "Verify you trust each server before connecting it.", "Claude Code, MCP"),
                   "The documentation warns: check that you trust each server before you connect it."))
            + exam_tests("2.4", [("MCP server configuration: project vs user scope, environment variable expansion, multi-server simultaneous access", "Among the topics, the guide names"),
                                 ("MCP tool and resource design: resources for content catalogs, tools for actions, description quality for adoption", "and also")])
            + guide_text("2.4"), "ts-2-4")
    + level("depth",
            beyond([cf("ts-2-4-b1", D(CCMCP, "In `claude -p` runs, [Agent SDK](/docs/en/headless) sessions, and [cloud sessions](/docs/en/claude-code-on-the-web), Claude Code can't show that prompt: it loads project-scoped servers without asking.", "Claude Code, MCP"),
                       "In an interactive session, Claude Code asks for approval before it uses a server of a committed .mcp.json. In claude -p runs, Agent SDK sessions and cloud sessions it cannot ask, and it loads the server without a prompt."),
                    cf("ts-2-4-b2", D(CCMCP, "In a remote server's `url` and `headers`, Claude Code reads credential variables from your environment as empty rather than expanding them.", "Claude Code, MCP"),
                       "For a remote server, some credential variables in the URL and the headers are read as empty, not expanded."),
                    cf("ts-2-4-b3", D(SDKM, "MCP tools require explicit permission before Claude can use them.", "Agent SDK, MCP"),
                       "In the Agent SDK, an MCP tool also needs a permission before Claude can call it.")])
            + code_pop_text("ts-2-4-code", "The code: a shared .mcp.json with variables", "An .mcp.json with variable expansion", CCMCP, MCP24, "Claude Code, MCP",
                            "${API_KEY} comes from the environment. ${API_BASE_URL:-...} has a default value.")
            + tab2_links("2.4", cf("ts-2-4-a02", excerpt(A02, "the pipeline uses no MCP server, because it calls only the Claude API and reads local files.", "Academy decision 0002"),
                                   "The mock builder uses no MCP server: it calls only the Claude API and reads local files.")), "ts-2-4"))


# ----- part 2.5 (facts: academy/facts/ts-2-5.md) -----

TREF = "claude-code-docs-tools-reference"
A35 = glob.glob(os.path.join(ROOT, "academy/decisions/0035-*.md"))[0][len(ROOT) + 1:]
YAML25 = "---\nname: code-reviewer\ndescription: Reviews code for quality and best practices\ntools: Read, Glob, Grep\nmodel: sonnet\n---"
FIG25 = figure("2.5-1", 890, 320,
               "Glob finds files by name and Grep finds entry points and callers. Then Read follows the imports, and Edit changes text that occurs once. Reading all files first fills the context. "
               "When the text of an Edit occurs twice, the guide reads and writes the whole file, and the documentation uses a longer match. "
               "On macOS, Linux and WSL, Claude Code searches with find and grep through Bash.",
               "".join([edge("M210 60H255V100H300"), edge("M210 140H255V100H300"), edge("M470 100H560"),
                        edge("M610 130V160H560V190"), edge("M670 130V160H775V190"),
                        '<text class="ve-el" x="640" y="152">two matches</text>',
                        '<text class="ve-lab" x="20" y="300">macOS, Linux and WSL: find and grep through Bash</text>',
                        box(20, 30, 190, 60, ["Glob"], sub="files by name"),
                        box(20, 110, 190, 60, ["Grep"], sub="entry points, callers"),
                        box(20, 200, 190, 60, ["Read all first"], sub="no: fills the context"),
                        box(300, 70, 170, 60, ["Read"], sub="follow imports"),
                        box(560, 70, 150, 60, ["Edit"], sub="one exact match"),
                        box(470, 190, 180, 60, ["Read + Write"], sub="the guide"),
                        box(680, 190, 190, 60, ["longer match"], sub="the documentation")]),
               "%s %s" % (cf("ts-2-5-s4", gx("Building codebase understanding incrementally: starting with Grep to find entry points, then using Read to follow imports and trace flows, rather than reading all files upfront", "Exam guide, 2.5-S4"),
                             "The guide starts with Grep to find the entry points, then follows the imports with Read, and does not read all files first (2.5-S4)."),
                          cf("ts-2-5-k4", gx("When Edit fails due to non-unique text matches, using Read + Write as a fallback for reliable file modifications", "Exam guide, 2.5-K4"),
                             "When Edit fails because its text is not unique, the guide falls back to Read and Write (2.5-K4).")))

PART["2.5"] = (overview("2.5", "Grep finds content, Glob finds files, Edit needs unique text",
                        "Search first: Glob finds files by name, Grep finds text inside files, and Read then follows only the files that matter. "
                        "Edit changes a part of a file and needs text that occurs once. If the text is not unique, the guide reads and writes the whole file.",
                        FIG25)
    + level("explanation",
            "<p><b>Grep and Glob.</b> %s %s %s</p>" % (
                cf("ts-2-5-k1", gx("Grep for content search (searching file contents for patterns like function names, error messages, or import statements)", "Exam guide, 2.5-K1"),
                   "Grep searches the content of files, for example function names, error messages or imports (2.5-K1, 2.5-S1)."),
                cf("ts-2-5-k2", gx("Glob for file path pattern matching (finding files by name or extension patterns)", "Exam guide, 2.5-K2"),
                   "Glob finds files by name or extension (2.5-K2).") + " " + cf("ts-2-5-s2", gx("Selecting Glob for finding files matching naming patterns (e.g., \\*\\*/\\*.test.tsx)", "Exam guide, 2.5-S2"),
                   "An example is every file that matches **/*.test.tsx (2.5-S2)."),
                cf("ts-2-5-f5", D(TREF, "Results are sorted by modification time and capped at 100 files.", "Claude Code, Tools reference"),
                   "In Claude Code, Glob returns at most 100 files, sorted by the time of their last change."))
            + "<p><b>Read, Write, Edit.</b> %s %s %s</p>" % (
                cf("ts-2-5-k3", gx("Read/Write for full file operations; Edit for targeted modifications using unique text matching", "Exam guide, 2.5-K3"),
                   "In the guide, Read and Write work on the whole file, and Edit changes one part, found by text that is unique (2.5-K3)."),
                cf("ts-2-5-f8", D(TREF, "The Write tool creates a new file or overwrites an existing one with the full content provided. It doesn't append or merge.", "Claude Code, Tools reference"),
                   "Write replaces the whole file."),
                cf("ts-2-5-c2", D(TREF, "**Uniqueness**: `old_string` must appear exactly once. When it appears more than once, Claude either supplies a longer string with enough surrounding context to pin down one occurrence, or sets `replace_all: true` to replace them all.", "Claude Code, Tools reference"),
                   "In the documentation, when the text occurs twice, Claude uses a longer text that occurs once, or replaces all occurrences. The guide reads and writes the whole file instead (2.5-K4, see Fig. 2.5-1). The exam uses the guide."))
            + "<p><b>Search first.</b> %s %s Part 3.4 shows the Explore subagent, which keeps a search out of the main context.</p>" % (
                cf("ts-2-5-f14", D(BEST, "Claude reads hundreds of files, filling the context.", "Claude Code, Best practices"),
                   "The documentation names the failure that 2.5-S4 prevents: Claude reads hundreds of files, and the context fills."),
                cf("ts-2-5-s5", gx("Tracing function usage across wrapper modules by first identifying all exported names, then searching for each name across the codebase", "Exam guide, 2.5-S5"),
                   "To trace a function through a wrapper module, the guide first lists all the names that it exports, then searches for each name (2.5-S5)."))
            + "<p><b>The platform.</b> %s</p>" %
                cf("ts-2-5-c1", D(TREF, "On Windows, it's part of the default tool set. On macOS, Linux, and WSL, Claude Code leaves Glob and [Grep](#grep-tool-behavior) out of the default tool set, and Claude searches with `find` and `grep` through the Bash tool instead.", "Claude Code, Tools reference"),
                   "On macOS, Linux and WSL, Claude Code leaves Grep and Glob out of its default tools, and Claude searches with find and grep through Bash. On Windows they are tools. The exam uses the guide.")
            + exam_tests("2.5", [("Built-in tools — Read, Write, Edit, Bash, Grep, Glob — their purposes and selection criteria", "Among the technologies, the guide names")])
            + guide_text("2.5"), "ts-2-5")
    + level("depth",
            beyond([cf("ts-2-5-b1", D(TREF, "By default one call returns at most 25,000 tokens, or the value you set in [`CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`](/docs/en/env-vars), and refuses a whole file over 256 KB, so Claude reads a larger file in pages with `offset` and `limit`.", "Claude Code, Tools reference"),
                       "In Claude Code, by default, Read returns at most 25,000 tokens in one call and refuses a whole file over 256 KB, so a large file comes in pages. The guide says &ldquo;full file&rdquo; with no limit."),
                    cf("ts-2-5-b3", D(TREF, "Claude Code keeps the tool inactive until you install a [code intelligence plugin](/docs/en/plugins/code-intelligence) for your language. In [cloud sessions](/docs/en/claude-code-on-the-web), Claude Code doesn't start plugin language servers, so the LSP tool stays inactive there.", "Claude Code, Tools reference"),
                       "In Claude Code, with a code intelligence plugin for the language, the LSP tool can find all references to a symbol, in place of a text search. It stays inactive in cloud sessions.")])
            + code_pop_text("ts-2-5-code", "The code: a subagent with only Read, Glob and Grep", "A review subagent with search tools only", CCS, YAML25, "Claude Code, Subagents",
                            "This subagent can search and read, but not change a file.")
            + tab2_links("2.5", "%s %s" % (cf("ts-2-5-a02", excerpt(A02, "The pipeline sends no tool definitions to the API.", "Academy decision 0002"), "The mock builder sends no tool definitions to the API, so no model in it gets these tools."),
                                           cf("ts-2-5-a35", excerpt(A35, "No record in the repository says which tool did what.", "Academy decision 0035 (proposed)"),
                                              "The build in Claude Code used its built-in tools, on WSL, where the documentation of today leaves Grep and Glob out by default. No record says which tool did what, so proposed decision 0035 leaves 2.5 out of tab 2."))), "ts-2-5"))


# ----- part 3.1 (facts: academy/facts/ts-3-1.md) -----

SDKF = "claude-code-docs-agent-sdk-claude-code-features"
IMP31 = "See @README for project overview and @package.json for available npm commands for this project.\n\n# Additional Instructions\n- git workflow @docs/git-instructions.md"
FIG31 = figure("3.1-1", 890, 340,
               "Four kinds of file, from broad to specific: the user CLAUDE.md, only for you and not in git. The project CLAUDE.md, shared with the team through git. "
               "Rule files in .claude/rules/, one topic each. A CLAUDE.md in a subdirectory, loaded when Claude works there. All are joined in the context of the session, "
               "and none overrides another. /memory and /context show the files.",
               "".join(['<path class="ve-e no-head" d="M330 20H345V320H330"/>',
                        edge("M345 165H600", "joined, none overrides", 478, 156),
                        box(20, 20, 300, 60, ["~/.claude/CLAUDE.md"], sub="user: only you, not in git"),
                        box(20, 100, 300, 60, ["./CLAUDE.md"], sub="project: the team, in git", cls="try ok"),
                        box(20, 180, 300, 60, [".claude/rules/*.md"], sub="one topic each, in git"),
                        box(20, 260, 300, 60, ["sub/CLAUDE.md"], sub="loads when used, in git"),
                        box(600, 110, 270, 110, ["Context of", "the session"], cls="who-model"),
                        box(600, 260, 270, 60, ["/memory, /context"], sub="list and check the files")]),
               "%s %s" % (cf("ts-3-1-f5", D(MEMD, "All discovered files are concatenated into context rather than overriding each other.", "Claude Code, Memory"),
                             "Claude Code joins all the files that it finds, and no file overrides another."),
                          cf("ts-3-1-k2", gx("That user-level settings apply only to that user—instructions in ~/.claude/CLAUDE.md are not shared with teammates via version control", "Exam guide, 3.1-K2"),
                             "The user file does not reach a teammate through git (3.1-K2).")))

PART["3.1"] = (overview("3.1", "Team instructions live in the project CLAUDE.md, split into files",
                        "Claude Code joins the CLAUDE.md files of the user, the project and its subdirectories, and only the project files reach teammates through git. "
                        "Imports and .claude/rules/ split a long file into topic files.",
                        FIG31)
    + level("explanation",
            "<p><b>The levels.</b> %s %s %s</p>" % (
                cf("ts-3-1-k1", gx("The CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md or root CLAUDE.md), and directory-level (subdirectory CLAUDE.md files)", "Exam guide, 3.1-K1"),
                   "The guide names three levels: the user (~/.claude/CLAUDE.md), the project (CLAUDE.md or .claude/CLAUDE.md), and the directory (a CLAUDE.md in a subdirectory) (3.1-K1)."),
                cf("ts-3-1-f1", D(MEMD, "The table below lists them in load order, from broadest scope to most specific, so a project instruction appears in context after a user instruction.", "Claude Code, Memory"),
                   "They load from broad to specific."),
                cf("ts-3-1-f4", D(MEMD, "Instead of loading them at launch, Claude Code loads each one once Claude reads, writes, or edits another file in that subdirectory.", "Claude Code, Memory"),
                   "A file in a subdirectory loads only when Claude works with a file there."))
            + "<p><b>Who gets which file.</b> %s %s</p>" % (
                cf("ts-3-1-f6", D(MEMD, "These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences.", "Claude Code, Memory"),
                   "The project file reaches the team through version control."),
                cf("ts-3-1-s1", gx("Diagnosing configuration hierarchy issues (e.g., a new team member not receiving instructions because they're in user-level rather than project-level configuration)", "Exam guide, 3.1-S1"),
                   "So when a new team member does not get an instruction, check whether it is in the user file, not the project file (3.1-S1)."))
            + "<p><b>Imports.</b> %s %s %s %s %s</p>" % (
                cf("ts-3-1-k3", gx("The @import syntax for referencing external files to keep CLAUDE.md modular (e.g., importing specific standards files relevant to each package)", "Exam guide, 3.1-K3"),
                   "The guide calls it the @import syntax, which keeps CLAUDE.md modular (3.1-K3)."),
                cf("ts-3-1-f7", D(MEMD, "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.", "Claude Code, Memory"),
                   "In the documentation, an @ and a path import a file, and the imported file loads at launch."),
                cf("ts-3-1-f8", D(MEMD, "Relative paths resolve relative to the file containing the import, not the working directory.", "Claude Code, Memory"),
                   "A relative path starts at the file that imports."),
                cf("ts-3-1-s2", gx("Using @import to selectively include relevant standards files in each package's CLAUDE.md based on maintainer domain knowledge", "Exam guide, 3.1-S2"),
                   "In the guide, the CLAUDE.md of each package imports only the standards that it needs (3.1-S2)."),
                cf("ts-3-1-f9", D(MEMD, "Splitting into [`@path` imports](#import-additional-files) helps organization but doesn't reduce context, since imported files load at launch.", "Claude Code, Memory"),
                   "An import organizes, but it does not save context: the imported file loads at launch."))
            + "<p><b>Rules.</b> %s %s %s</p>" % (
                cf("ts-3-1-s3", gx("Splitting large CLAUDE.md files into focused topic-specific files in .claude/rules/ (e.g., testing.md, api-conventions.md, deployment.md)", "Exam guide, 3.1-S3"),
                   "A large CLAUDE.md becomes topic files in .claude/rules/, such as testing.md and deployment.md (3.1-K4, 3.1-S3)."),
                cf("ts-3-1-f14", D(MEMD, "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence.", "Claude Code, Memory"),
                   "The documentation targets less than 200 lines for each CLAUDE.md."),
                "Part 3.3 shows rules that load only for some paths.")
            + "<p><b>Check.</b> %s %s %s</p>" % (
                cf("ts-3-1-s4", gx("Using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions", "Exam guide, 3.1-S4"),
                   "The guide uses /memory to check which memory files are loaded (3.1-S4)."),
                cf("ts-3-1-f16", D(MEMD, "The `/memory` command lists your CLAUDE.md, CLAUDE.local.md, and other memory file locations across user and project scopes, including user and project CLAUDE.md entries for files that don't exist yet.", "Claude Code, Memory"),
                   "In the documentation, /memory lists the locations of the files, also of files that do not exist yet."),
                cf("ts-3-1-f17", D(MEMD, "To check which `CLAUDE.md` and rules files loaded at launch, run `/context`.", "Claude Code, Memory"),
                   "For the files that loaded, it names /context. The exam uses the guide."))
            + exam_tests("3.1", [("CLAUDE.md configuration: hierarchy (user/project/directory), @import patterns, .claude/rules/ with glob patterns", "Among the topics, the guide names")])
            + guide_text("3.1"), "ts-3-1")
    + level("depth",
            beyond([cf("ts-3-1-b1", D(MEMD, "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a [PreToolUse hook](/docs/en/hooks-guide) instead.", "Claude Code, Memory"),
                       "CLAUDE.md guides Claude, but it does not enforce. To block an action, use a PreToolUse hook (part 1.5)."),
                    cf("ts-3-1-b2", D(MEMD, "Organization-wide instructions managed by IT/DevOps", "Claude Code, Memory"),
                       "The documentation has more levels than the guide: a managed policy file for an organization,") + " " + cf("ts-3-1-b2b", D(MEMD, "Personal project-specific preferences; add to `.gitignore`", "Claude Code, Memory"),
                       "and CLAUDE.local.md for personal preferences in one project, kept out of git."),
                    cf("ts-3-1-b3", D(SDKF, "When you omit `settingSources`, `query()` reads the same filesystem settings as the Claude Code CLI", "Agent SDK, Claude Code features"),
                       "The Agent SDK reads the same CLAUDE.md files as the CLI, unless the option settingSources (setting_sources in Python) turns that off.")])
            + code_pop_text("ts-3-1-code", "The code: imports in a CLAUDE.md", "Imports with @ and a path", MEMD, IMP31, "Claude Code, Memory",
                            "Each @ and a path imports a file into the context at launch.")
            + tab2_links("3.1") + "<p>%s %s</p>" % (cf("ts-3-1-a02", excerpt(A02, "The tables of guide points in the build guide use points of only 12 of the 30 task statements: 1.1, 1.3, 1.4, 1.6, 4.1, 4.2, 4.3, 4.4, 4.6, 5.3, 5.5 and 5.6. It uses no task statement of domain 2 or domain 3. This is a deliberate choice.", "Academy decision 0002"),
                                                    "No step of the mock builder uses 3.1, and this is a deliberate choice."),
                                                 cf("ts-3-1-cc", excerpt("CLAUDE.md", "@WORKING-RULES.md", "CLAUDE.md of the project"),
                                                    "The build in Claude Code used a project CLAUDE.md with one import, which shows 3.1-K3.")), "ts-3-1"))


# ----- part 3.3 (facts: academy/facts/ts-3-3.md) -----

LCB = "claude-code-docs-large-codebases"
D48 = glob.glob(os.path.join(ROOT, "docs/decisions/0048-*.md"))[0][len(ROOT) + 1:]
RULE33 = "---\npaths:\n  - \"src/api/**/*.ts\"\n---\n\n# API Development Rules\n\n- All API endpoints must include input validation\n- Use the standard error response format\n- Include OpenAPI documentation comments"
FIG33 = figure("3.3-1", 890, 330,
               "A rule file in .claude/rules/ with paths **/*.test.tsx matches test files in several folders, such as src/ui/Button.test.tsx, src/api/users.test.tsx and lib/date.test.tsx, "
               "but not src/ui/Button.tsx. When Claude edits a matching file, the rule loads into the context (in Claude Code, a read is enough too). A CLAUDE.md in src/ui/ covers that one folder only.",
               "".join(['<path class="ve-e no-head" d="M280 80H320M320 42V150"/>',
                        edge("M320 42H360"), edge("M320 96H360"), edge("M320 150H360"),
                        edge("M620 96H700"),
                        '<text class="ve-lab" x="300" y="290">a directory CLAUDE.md covers one folder only</text>',
                        box(20, 40, 260, 80, [".claude/rules/testing.md"], sub='paths: "**/*.test.tsx"'),
                        box(360, 20, 260, 44, ["src/ui/Button.test.tsx"], cls="try ok"),
                        box(360, 74, 260, 44, ["src/api/users.test.tsx"], cls="try ok"),
                        box(360, 128, 260, 44, ["lib/date.test.tsx"], cls="try ok"),
                        box(360, 182, 260, 44, ["src/ui/Button.tsx"], sub="no match"),
                        box(700, 50, 170, 90, ["Context"], sub="on an edit (guide)", cls="who-model"),
                        box(20, 250, 260, 60, ["src/ui/CLAUDE.md"], sub="only files in src/ui/")]),
               "%s %s" % (cf("ts-3-3-f1", D(MEMD, "Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with files matching the specified patterns.", "Claude Code, Memory"),
                             "A paths field in the frontmatter scopes a rule to the files that match its patterns."),
                          cf("ts-3-3-f13", gx("allows conventions to be automatically applied based on file paths regardless of directory location, essential for test files spread throughout the codebase.", "Exam guide, sample question 6"),
                             "This is the answer of the guide for test files spread through the codebase.")))

PART["3.3"] = (overview("3.3", "A rule with a glob loads only for matching files",
                        "A file in .claude/rules/ with a paths list of glob patterns loads into the context only when Claude edits a file that matches (the guide). "
                        "A glob such as **/*.test.tsx finds files by type in every folder, which a CLAUDE.md in one directory cannot do.",
                        FIG33)
    + level("explanation",
            "<p><b>The paths field.</b> %s %s %s</p>" % (
                cf("ts-3-3-k1", gx(".claude/rules/ files with YAML frontmatter paths fields containing glob patterns for conditional rule activation", "Exam guide, 3.3-K1"),
                   "A file in .claude/rules/ can have a paths field in its YAML frontmatter (the header of the file), with glob patterns (patterns of file names) that decide when the rule applies (3.3-K1)."),
                cf("ts-3-3-s1", gx("Creating .claude/rules/ files with YAML frontmatter path scoping (e.g., paths: [\"terraform/\\*\\*/\\*\"]) so rules load only when editing matching files", "Exam guide, 3.3-S1"),
                   "An example of the guide is a rule for all the files under a folder terraform/ (3.3-S1)."),
                cf("ts-3-3-f4", D(MEMD, "Use glob patterns in the `paths` field to match files by extension, directory, or any combination:", "Claude Code, Memory"),
                   "A glob matches files by extension, by directory, or both."))
            + "<p><b>When it loads.</b> %s %s %s</p>" % (
                cf("ts-3-3-k2", gx("How path-scoped rules load only when editing matching files, reducing irrelevant context and token usage", "Exam guide, 3.3-K2"),
                   "The guide says that a path rule loads only when Claude edits a matching file, so the context and the tokens stay small (3.3-K2)."),
                cf("ts-3-3-f6", D(MEMD, "A path-scoped rule loads when Claude uses the Read, Write, or Edit tool on a matching file. It also loads when Claude views a matching file with a Bash command that [counts as a read](/docs/en/tools-reference#edit-tool-behavior), such as `cat` or `head` on a single file.", "Claude Code, Memory"),
                   "In Claude Code, a read is enough: the rule also loads on the Read tool, or when a Bash command such as cat reads that single file. The exam uses the guide."),
                cf("ts-3-1-f13", D(MEMD, "Rules without [`paths` frontmatter](#path-specific-rules) are loaded at launch with the same priority as `.claude/CLAUDE.md`.", "Claude Code, Memory"),
                   "A rule with no paths loads at launch like CLAUDE.md."))
            + "<p><b>Across folders.</b> %s %s %s</p>" % (
                cf("ts-3-3-s2", gx("Using glob patterns in path-specific rules to apply conventions to files by type regardless of directory location (e.g., \\*\\*/\\*.test.tsx for all test files)", "Exam guide, 3.3-S2"),
                   "A glob applies a convention to files by type in every folder, for example **/*.test.tsx for all test files (3.3-S2)."),
                cf("ts-3-3-f9", D(MEMD, "Instead of loading them at launch, Claude Code loads each one once Claude reads, writes, or edits another file in that subdirectory.", "Claude Code, Memory"),
                   "A CLAUDE.md in a subdirectory also loads late, but only for files in that subdirectory."),
                cf("ts-3-3-s3", gx("Choosing path-specific rules over subdirectory CLAUDE.md files when conventions must apply to files spread across the codebase", "Exam guide, 3.3-S3"),
                   "So for files spread across the codebase, a path rule is the better choice (3.3-K3, 3.3-S3)."))
            + exam_tests("3.3", [("CLAUDE.md configuration: hierarchy (user/project/directory), @import patterns, .claude/rules/ with glob patterns", "Among the topics, the guide names")])
            + "<p>%s</p>" % cf("ts-3-3-q6", gx("Create rule files in .claude/rules/ with YAML frontmatter specifying glob patterns to conditionally apply conventions based on file paths", "Exam guide, sample question 6, answer A"),
                               "Sample question 6 of the guide fits 3.3: its option A, a rule file with glob patterns, is the correct answer.")
            + guide_text("3.3"), "ts-3-3")
    + level("depth",
            beyond([cf("ts-3-3-b1", D(MEMD, "If the YAML between the markers doesn't parse, Claude Code ignores the frontmatter and loads the rule as if it had no `paths`.", "Claude Code, Memory"),
                       "If the YAML of the frontmatter does not parse, Claude Code loads the rule in every session, as if it had no paths."),
                    cf("ts-3-3-b2", D(MEMD, "Use the [`InstructionsLoaded` hook](/docs/en/hooks#instructionsloaded) to log which `CLAUDE.md` and rules files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories.", "Claude Code, Memory"),
                       "In Claude Code, the InstructionsLoaded hook logs which rule files load, when and why, which helps to debug path rules."),
                    cf("ts-3-3-b3", D(MEMD, "Nested CLAUDE.md files in subdirectories and rules with [`paths:` frontmatter](#path-specific-rules) load again on demand.", "Claude Code, Memory"),
                       "After /compact, a path rule loads again only on demand, when a matching file comes up.")])
            + code_pop_text("ts-3-3-code", "The code: a rule with a paths field", "A path-scoped rule", MEMD, RULE33, "Claude Code, Memory",
                            "This rule loads only when Claude works with a .ts file under src/api/.")
            + tab2_links("3.3", "%s %s %s" % (fact("ts-3-1-a02", "Its build guide uses no task statement of domain 2 or 3, by choice."), cf("ts-g1", excerpt("academy/facts/claude-code.md", "The pipeline itself is a Python program that calls the API. It is not Claude Code.", "Fact sheet of the build in Claude Code"), "The mock builder is a Python program that calls the Claude API. It is not Claude Code."),
                                           cf("ts-3-3-d48", excerpt(D48, "Task statement 3.3 is one group, because its 6 points have one correct answer (a rules file with a path).", "Mock decision 0048"),
                                              "For the plan of a mock, 3.3 is one idea, because its 6 points have one correct answer."))), "ts-3-3"))


# ----- part 3.2 (facts: academy/facts/ts-3-2.md) -----

SKL, FOV, CDIR = "claude-code-docs-skills", "claude-code-docs-features-overview", "claude-code-docs-claude-directory"
SKILL32 = "---\nname: deep-research\ndescription: Research a topic thoroughly\ncontext: fork\nagent: Explore\n---\n\nResearch $ARGUMENTS thoroughly:\n\n1. Find relevant files using Glob and Grep\n2. Read and analyze the code\n3. Summarize findings with specific file references"
FIG32 = figure("3.2-1", 890, 300,
               "A skill with context: fork runs in a new subagent. The content of SKILL.md is its task, and it gets no conversation history. "
               "It reads files and runs searches, and only a summary returns to the main conversation. Without context: fork, the body of the skill enters the main context.",
               "".join([edge("M280 80H560", "SKILL.md content = the task", 420, 71),
                        edge("M280 125H560", "no conversation history", 420, 145, cls="is-async no-head"),
                        '<path class="ve-e no-head" d="M412 117l16 16M428 117l-16 16"/>',
                        edge("M715 160V200H150V160", "only a summary returns", 430, 192),
                        box(20, 40, 260, 120, ["Main", "conversation"], sub="skill descriptions only", cls="who-model"),
                        box(560, 40, 310, 120, ["New subagent"], sub="reads files, runs searches", cls="who-model"),
                        box(20, 225, 300, 60, ["Without context: fork"], sub="the body enters the main context")]),
               "%s %s" % (cf("ts-3-2-k3", gx("The context: fork frontmatter option for running skills in an isolated sub-agent context, preventing skill outputs from polluting the main conversation", "Exam guide, 3.2-K3"),
                             "context: fork runs a skill in an isolated subagent, so its output does not fill the main conversation (3.2-K3)."),
                          cf("ts-3-2-f10", D(SKL, "4. The subagent summarizes its results and returns them to your main conversation when it finishes", "Claude Code, Skills"),
                             "The subagent returns a summary of its results to the main conversation.")))

PART["3.2"] = (overview("3.2", "Share skills through the repository, and set how they run",
                        "A command or a skill in the .claude/ folder of the project reaches the team through git. One in ~/.claude/ stays personal. "
                        "The frontmatter of a skill sets how it runs, and unlike CLAUDE.md, the body of a skill loads only when it is used.",
                        FIG32)
    + level("explanation",
            "<p><b>Team or personal.</b> %s %s %s</p>" % (
                cf("ts-3-2-k1", gx("Project-scoped commands in .claude/commands/ (shared via version control) vs user-scoped commands in ~/.claude/commands/ (personal)", "Exam guide, 3.2-K1"),
                   "A command in .claude/commands/ of the project reaches the team through git. One in ~/.claude/commands/ is personal (3.2-K1, 3.2-S1)."),
                cf("ts-3-2-f3", D(CDIR, "Files here apply to every project you work in and are never committed to any repository.", "Claude Code, The .claude directory"),
                   "Files in ~/.claude/ are never committed."),
                cf("ts-3-2-c3", D(SKL, "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working.", "Claude Code, Skills"),
                   "Claude Code has merged commands into skills: a command file still works, and a skill in .claude/skills/ makes the same command. The exam uses the guide."))
            + "<p><b>The frontmatter.</b> %s %s</p>" % (
                cf("ts-3-2-k2", gx("Skills in .claude/skills/ with SKILL.md files that support frontmatter configuration including context: fork, allowed-tools, and argument-hint", "Exam guide, 3.2-K2"),
                   "A skill is a SKILL.md file in .claude/skills/. Its frontmatter, a header of settings, can hold context: fork, allowed-tools and argument-hint (3.2-K2)."),
                cf("ts-3-2-s2", gx("Using context: fork to isolate skills that produce verbose output (e.g., codebase analysis) or exploratory context (e.g., brainstorming alternatives) from the main session", "Exam guide, 3.2-S2"),
                   "context: fork suits a skill with long output, such as an analysis of the codebase (3.2-S2)."))
            + "<p><b>Two fields that differ.</b> %s %s %s %s</p>" % (
                cf("ts-3-2-s3", gx("Configuring allowed-tools in skill frontmatter to restrict tool access during skill execution (e.g., limiting to file write operations to prevent destructive actions)", "Exam guide, 3.2-S3"),
                   "The guide uses allowed-tools to restrict the tools of a skill (3.2-S3)."),
                cf("ts-3-2-c1", D(SKL, "The `allowed-tools` field grants permission for the listed tools during the turn that invokes the skill, so Claude can use them without prompting you for approval.", "Claude Code, Skills"),
                   "In the documentation, allowed-tools only approves the listed tools for the turn that invokes the skill.") + " " + cf("ts-3-2-c1b", D(SKL, "It does not restrict which tools are available", "Claude Code, Skills"),
                   "It does not restrict which tools are available."),
                cf("ts-3-2-s4", gx("Using argument-hint frontmatter to prompt developers for required parameters when they invoke the skill without arguments", "Exam guide, 3.2-S4"),
                   "The guide uses argument-hint to ask for missing parameters (3.2-S4)."),
                cf("ts-3-2-c2", D(SKL, "Hint shown during autocomplete to indicate expected arguments.", "Claude Code, Skills"),
                   "In the documentation, it is a hint in the autocomplete. The exam uses the guide."))
            + "<p><b>Personal variants.</b> %s %s</p>" % (
                cf("ts-3-2-k4", gx("Personal skill customization: creating personal variants in ~/.claude/skills/ with different names to avoid affecting teammates", "Exam guide, 3.2-K4"),
                   "The guide puts a personal variant in ~/.claude/skills/ with another name (3.2-K4)."),
                cf("ts-3-2-f16", D(SKL, "Enterprise over personal, and personal over project. With `deploy` in both `~/.claude/skills/` and the project's `.claude/skills/`, `/deploy` runs the personal one", "Claude Code, Skills"),
                   "With the same name, the personal skill wins over the project skill. It lives only on the machine of its owner, so it does not affect teammates."))
            + "<p><b>Skill or CLAUDE.md.</b> %s %s</p>" % (
                cf("ts-3-2-s5", gx("Choosing between skills (on-demand invocation for task-specific workflows) and CLAUDE.md (always-loaded universal standards)", "Exam guide, 3.2-S5"),
                   "A skill is for a workflow that runs on demand, and CLAUDE.md is for standards that always load (3.2-S5)."),
                cf("ts-3-2-f23", D(SKL, "In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked.", "Claude Code, Skills"),
                   "In a regular session, only the description of a skill is in context, and its body loads when it is used.") + " " + cf("ts-3-2-f23b", D(SKL, "| `disable-model-invocation: true` | Yes | Not on its own | Description not in context, full skill loads when invoked |", "Claude Code, Skills"),
                   "With disable-model-invocation, not even the description is in context."))
            + exam_tests("3.2", [("Custom commands and skills: project vs user scope, context: fork, allowed-tools, argument-hint frontmatter", "Among the topics, the guide names")])
            + guide_text("3.2"), "ts-3-2")
    + level("depth",
            beyond([cf("ts-3-2-b1", D(SKL, "Workspace trust doesn't gate this field. Claude Code applies a project skill's `allowed-tools` even in a `-p` run in a folder you've never trusted. A skill can grant itself broad tool access, so review the `allowed-tools` of skills checked into a repository before you run Claude Code there.", "Claude Code, Skills"),
                       "allowed-tools of a project skill applies even in a -p run in a folder that you have never trusted, so a repository can grant itself tools, unless managed settings of the organization withhold the field (Claude Code 2.1.282 or later)."),
                    cf("ts-3-2-b2", D(SKL, "**`disable-model-invocation: true`**: Claude can't invoke the skill on its own. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`.", "Claude Code, Skills"),
                       "The field disable-model-invocation keeps Claude from starting a skill with side effects, such as a deploy."),
                    cf("ts-3-2-b3", D(SKL, "If you include any field the spec doesn't allow, packaging or upload fails with a hard error instead of ignoring the field:", "Claude Code, Skills"),
                       "Outside Claude Code, on a claude.ai upload or in the Skills API, argument-hint is an error.")])
            + code_pop_text("ts-3-2-code", "The code: a skill with context: fork", "A research skill that runs in a forked subagent", SKL, SKILL32, "Claude Code, Skills",
                            "The Explore agent runs the task, and $ARGUMENTS takes the words after the command.")
            + tab2_links("3.2", "%s %s %s" % (fact("ts-3-1-a02", "Its build guide uses no task statement of domain 2 or 3, by choice."), cf("ts-g1", excerpt("academy/facts/claude-code.md", "The pipeline itself is a Python program that calls the API. It is not Claude Code.", "Fact sheet of the build in Claude Code"), "The mock builder is a Python program that calls the Claude API. It is not Claude Code."),
                                           cf("ts-3-2-a35", excerpt(A35, "3.2: the link holds only weakly.", "Academy decision 0035 (proposed)"),
                                              "Proposed decision 0035 leaves 3.2 out of the build in Claude Code on tab 2, because the link to the records is weak."))), "ts-3-2"))


# ----- part 3.4 (facts: academy/facts/ts-3-4.md) -----

PMODE, MCONF = "claude-code-docs-permission-modes", "claude-code-docs-model-config"
A23 = glob.glob(os.path.join(ROOT, "academy/decisions/0023-*.md"))[0][len(ROOT) + 1:]
FIG34 = figure("3.4-1", 890, 320,
               "A change that is big or unclear goes through plan mode: Claude explores and reads with no edits, writes a plan, and you approve it. Then Claude implements the plan. "
               "A small and clear change goes to direct execution. Outside plan mode, the Explore subagent can do a verbose discovery and return only a summary.",
               "".join(['<text class="ve-lab" x="460" y="20">plan mode: edits wait for approval (usually)</text>',
                        edge("M170 165H220"), edge("M410 140H435V60H460", "yes", 446, 100, anchor="r"),
                        edge("M590 60H605"), edge("M720 60H735"),
                        edge("M802 90V230", "implement the plan", 718, 165),
                        edge("M315 210V265H700", "no: small and clear", 505, 256),

                        box(20, 130, 150, 70, ["A change"]),
                        box(220, 120, 190, 90, ["Big or", "unclear?"]),
                        box(460, 30, 130, 60, ["Explore"], sub="read, no edits", cls="who-model"),
                        box(605, 30, 115, 60, ["Plan"], sub="Claude writes", cls="who-model"),
                        box(735, 30, 135, 60, ["Approve"], sub="you decide"),
                        box(440, 130, 190, 60, ["Explore subagent"], sub="outside plan mode", cls="who-model"),
                        box(700, 230, 170, 70, ["Direct", "execution"], cls="try ok")]),
               "%s %s" % (cf("ts-3-4-k1", gx("Plan mode is designed for complex tasks involving large-scale changes, multiple valid approaches, architectural decisions, and multi-file modifications", "Exam guide, 3.4-K1"),
                             "Plan mode is for complex tasks: large changes, several valid approaches, architectural decisions, many files (3.4-K1)."),
                          cf("ts-3-4-f4", D(PMODE, "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source.", "Claude Code, Permission modes"),
                             "In plan mode, Claude reads and proposes, but does not edit the source.")))

PART["3.4"] = (overview("3.4", "Plan first when the change is big or unclear",
                        "In plan mode, Claude reads the code and proposes a plan, and in most sessions the edits wait until you approve it. "
                        "Use it for large, multi-file or architectural changes, and execute a small, clear change directly.",
                        FIG34)
    + level("explanation",
            "<p><b>When to plan.</b> %s %s</p>" % (
                cf("ts-3-4-s1", gx("Selecting plan mode for tasks with architectural implications (e.g., microservice restructuring, library migrations affecting 45+ files, choosing between integration approaches with different infrastructure requirements)", "Exam guide, 3.4-S1"),
                   "The guide plans first for tasks with architectural implications, such as a library migration that touches 45 or more files (3.4-S1)."),
                cf("ts-3-4-f1", D(BEST, "Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified.", "Claude Code, Best practices"),
                   "The documentation plans first when the approach is uncertain, the change touches many files, or the code is not familiar."))
            + "<p><b>When to go direct.</b> %s %s %s</p>" % (
                cf("ts-3-4-k2", gx("Direct execution is appropriate for simple, well-scoped changes (e.g., adding a single validation check to one function)", "Exam guide, 3.4-K2"),
                   "Direct execution suits a simple change with a clear scope, such as one validation check in one function (3.4-K2)."),
                cf("ts-3-4-f2", D(BEST, "If you could describe the diff in one sentence, skip the plan.", "Claude Code, Best practices"),
                   "The documentation gives a test: if you can describe the diff in one sentence, skip the plan."),
                cf("ts-3-4-f3", D(BEST, "For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly.", "Claude Code, Best practices"),
                   "It does not use the term &ldquo;direct execution&rdquo;: it says to ask Claude to do it directly. The exam uses the term of the guide."))
            + "<p><b>Safe exploration.</b> %s %s</p>" % (
                cf("ts-3-4-k3", gx("Plan mode enables safe codebase exploration and design before committing to changes, preventing costly rework", "Exam guide, 3.4-K3"),
                   "The guide says that plan mode makes the exploration safe before any change, and so prevents costly rework (3.4-K3)."),
                cf("ts-3-4-f5", D(PMODE, "Except in interactive terminal sessions with [bypass permissions available](#skip-all-checks-with-bypasspermissions-mode), edits stay blocked until you approve the plan.", "Claude Code, Permission modes"),
                   "In Claude Code, the edits stay blocked until you approve the plan, except in an interactive terminal session where the mode that skips all checks is available. The exam uses the guide."))
            + "<p><b>Plan, then execute.</b> %s %s</p>" % (
                cf("ts-3-4-s4", gx("Combining plan mode for investigation with direct execution for implementation (e.g., planning a library migration, then executing the planned approach)", "Exam guide, 3.4-S4"),
                   "Plan mode investigates, and direct execution implements, for example a planned library migration (3.4-S4)."),
                cf("ts-3-4-f9", D(BEST, "Switch out of plan mode by approving the plan or pressing `Shift+Tab`, then let Claude code, verifying against its plan.", "Claude Code, Best practices"),
                   "In Claude Code, you approve the plan, and Claude codes against it."))
            + "<p><b>The Explore subagent.</b> %s %s %s</p>" % (
                cf("ts-3-4-s3", gx("Using the Explore subagent for verbose discovery phases to prevent context window exhaustion during multi-phase tasks", "Exam guide, 3.4-S3"),
                   "The Explore subagent takes the verbose discovery, so the main context does not fill up (3.4-S3).") + " " + cf("ts-3-4-k4", gx("The Explore subagent for isolating verbose discovery output and returning summaries to preserve main conversation context", "Exam guide, 3.4-K4"),
                   "It returns a summary (3.4-K4)."),
                cf("ts-2-5-b2", D(CCS, "Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context.", "Claude Code, Subagents"),
                   "Claude delegates to Explore when it searches without making changes."),
                cf("ts-3-4-c3", D(CCS, "When you're in plan mode and Claude needs to understand your codebase, it delegates research to the Plan subagent so that exploration output stays in a separate context window while the main conversation remains read-only.", "Claude Code, Subagents"),
                   "In plan mode, Claude Code gives the research to a different built-in subagent, Plan. The exam uses the guide."))
            + exam_tests("3.4", [("Plan mode vs direct execution: complexity assessment, architectural decisions, single-file changes", "Among the topics, the guide names")])
            + "<p>%s</p>" % cf("ts-3-4-q5", gx("Enter plan mode to explore the codebase, understand dependencies, and design an implementation approach before making changes.", "Exam guide, sample question 5, answer A"),
                               "Sample question 5 of the guide fits 3.4: its correct answer enters plan mode.")
            + guide_text("3.4"), "ts-3-4")
    + level("depth",
            beyond([cf("ts-3-4-b1", D(LCB, "Claude Code re-injects the plan file after each compaction, so the plan survives where conversation history may not", "Claude Code, Large codebases"),
                       "In Claude Code, the plan survives a compaction, the summary of a long session: Claude Code puts the plan file back after each one."),
                    cf("ts-3-4-b2", D(PMODE, "Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds.", "Claude Code, Permission modes"),
                       "In Claude Code, you can edit the proposed plan in your editor before Claude starts."),
                    cf("ts-3-4-b3", D(MCONF, "Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution", "Claude Code, Model configuration"),
                       "In Claude Code, the model alias opusplan uses Opus to plan and Sonnet to execute.")])
            + code_pop_text("ts-3-4-code", "The code: start Claude Code in plan mode", "Start a session in plan mode", PMODE, "claude --permission-mode plan", "Claude Code, Permission modes",
                            "Or press Shift+Tab in a session, or start one prompt with /plan.")
            + tab2_links("3.4") + "<p>No step of the mock builder uses 3.4. %s %s</p>" % (fact("ts-3-1-a02", "Its build guide uses no task statement of domain 2 or 3, by choice.") + " " + cf("ts-g1", excerpt("academy/facts/claude-code.md", "The pipeline itself is a Python program that calls the API. It is not Claude Code.", "Fact sheet of the build in Claude Code"), "The mock builder is a Python program that calls the Claude API. It is not Claude Code."),
                                                     cf("ts-3-4-a23", excerpt(A23, "3.4: no example. The entry says that the build used a \"discuss first\" rule, not plan mode.", "Academy decision 0023"),
                                                        "The build in Claude Code used a rule to discuss first, not plan mode.")), "ts-3-4"))


# ----- part 3.5 (facts: academy/facts/ts-3-5.md) -----

PLIB = "claude-code-docs-prompt-library"
INT35 = "\n".join(read(SRC % BEST).split("\n")[345:350])
assert INT35.startswith("I want to build [brief description].") and INT35.endswith("SPEC.md.")
FIG35 = figure("3.5-1", 890, 320,
               "In an unfamiliar domain, an interview can come first, where Claude asks questions. Then the tests are written first. Claude implements and runs the tests. "
               "If all pass, the work is done. If not, the failures go back to Claude: interacting issues in one message, independent issues one at a time.",
               "".join([edge("M210 65H260", cls="is-async"), edge("M430 65H480"), edge("M650 65H700"),
                        edge("M785 100V180", "all pass", 793, 145, anchor="r"),
                        edge("M740 100V140H565V100", "failures", 652, 132, cls="is-hot"),
                        '<path class="ve-e no-head is-async" d="M565 140V190"/>',
                        '<text class="ve-lab" x="20" y="305">2 or 3 input and output examples clarify a transformation</text>',
                        box(20, 30, 190, 70, ["Interview"], sub="if the domain is new", cls="who-model"),
                        box(260, 30, 170, 70, ["Write tests"], sub="before the code"),
                        box(480, 30, 170, 70, ["Claude", "implements"], cls="who-model"),
                        box(700, 30, 170, 70, ["Run the tests"]),
                        box(700, 180, 170, 60, ["Done"], cls="try ok"),
                        box(330, 190, 320, 80, ["interacting: one message", "independent: one at a time"])]),
               "%s %s" % (cf("ts-3-5-k2", gx("Test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement", "Exam guide, 3.5-K2"),
                             "The guide writes the tests first, then iterates on the failures (3.5-K2)."),
                          cf("ts-3-5-s5", gx("Addressing multiple interacting issues in a single detailed message when fixes interact, versus sequential iteration for independent issues", "Exam guide, 3.5-S5"),
                             "Issues that interact go in one detailed message, independent issues one at a time (3.5-S5).")))

PART["3.5"] = (overview("3.5", "Refine with examples, failing tests and an interview",
                        "When prose gives mixed results, show Claude 2 or 3 input and output examples, or write the tests first and let the failures drive the next try. "
                        "Before work in an unfamiliar domain, let Claude interview you.",
                        FIG35)
    + level("explanation",
            "<p><b>Examples.</b> %s %s %s %s</p>" % (
                cf("ts-3-5-k1", gx("Concrete input/output examples as the most effective way to communicate expected transformations when prose descriptions are interpreted inconsistently", "Exam guide, 3.5-K1"),
                   "The guide calls concrete input and output examples the most effective way to show a transformation when prose gives mixed results (3.5-K1)."),
                cf("ts-3-5-f1", D(PBP, "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure.", "Prompting best practices"),
                   "The prompting documentation of the Claude API calls them one of the most reliable ways to steer the format, the tone and the structure. The exam uses the guide."),
                cf("ts-3-5-s1", gx("Providing 2-3 concrete input/output examples to clarify transformation requirements when natural language descriptions produce inconsistent results", "Exam guide, 3.5-S1"),
                   "The guide gives 2 or 3 examples (3.5-S1)."),
                cf("ts-3-5-f3", D(PBP, "Include 3–5 examples for best results.", "Prompting best practices"),
                   "The documentation gives 3 to 5 for prompts in general. The exam uses the guide."))
            + "<p><b>Tests first.</b> %s %s %s</p>" % (
                cf("ts-3-5-s2", gx("Writing test suites covering expected behavior, edge cases, and performance requirements before implementation, then iterating by sharing test failures", "Exam guide, 3.5-S2"),
                   "The tests cover the expected behavior, the edge cases and the performance, before the code (3.5-S2).") + " " + cf("ts-3-5-s4", gx("Providing specific test cases with example input and expected output to fix edge case handling (e.g., null values in migration scripts)", "Exam guide, 3.5-S4"),
                   "A specific test case with an example input and the expected output fixes an edge case, such as null values in a migration (3.5-S4)."),
                cf("ts-3-5-f5", D(PLIB, "Test-driven development: the tests define when the work is complete, and Claude iterates on the implementation until they pass.", "Claude Code, Prompt library"),
                   "In Claude Code, the tests define when the work is complete."),
                cf("ts-3-5-f6", D(BEST, "Give Claude something that produces a pass or fail, and the loop closes on its own. Claude does the work, runs the check, reads the result, and iterates until the check passes.", "Claude Code, Best practices"),
                   "In Claude Code, Claude runs the tests and reads the failures itself. The guide says only &ldquo;sharing test failures&rdquo;, and the exam uses the guide."))
            + "<p><b>The interview.</b> %s %s %s</p>" % (
                cf("ts-3-5-k3", gx("The interview pattern: having Claude ask questions to surface considerations the developer may not have anticipated before implementing", "Exam guide, 3.5-K3"),
                   "Claude asks questions before the work, to find what the developer did not consider (3.5-K3).") + " " + cf("ts-3-5-s3", gx("Using the interview pattern to surface design considerations (e.g., cache invalidation strategies, failure modes) before implementing solutions in unfamiliar domains", "Exam guide, 3.5-S3"),
                   "The guide uses it in an unfamiliar domain (3.5-S3)."),
                cf("ts-3-5-f10", D(BEST, "For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool.", "Claude Code, Best practices"),
                   "The Claude Code documentation uses it for larger features, with the tool AskUserQuestion. The exam uses the guide."),
                cf("ts-3-5-f11", D(BEST, "Claude asks about things you might not have considered yet, including technical implementation, UI/UX, edge cases, and tradeoffs.", "Claude Code, Best practices"),
                   "Claude asks about the implementation, edge cases and tradeoffs."))
            + "<p><b>One message or a sequence.</b> %s Only the guide states this point.</p>" %
                cf("ts-3-5-k4", gx("When to provide all issues in a single message (interacting problems) versus fixing them sequentially (independent problems)", "Exam guide, 3.5-K4"),
                   "Problems that interact go in one message, and independent problems go one at a time (3.5-K4, 3.5-S5).")
            + exam_tests("3.5", [("Iterative refinement: input/output examples, test-driven iteration, interview pattern, sequential vs parallel issue resolution", "Among the topics, the guide names")])
            + guide_text("3.5"), "ts-3-5")
    + level("depth",
            beyond([cf("ts-3-5-b1", D(BEST, "Ask Claude the questions you'd ask another engineer, and for larger features have Claude interview you and write a spec before you start implementing.", "Claude Code, Best practices"),
                       "In Claude Code, the interview ends in a spec, and the documentation then starts a fresh session to implement it."),
                    cf("ts-3-5-b2", D(BEST, "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned.", "Claude Code, Best practices"),
                       "In Claude Code, after more than two corrections on one issue, the context is cluttered: clear it and start again with a better prompt."),
                    cf("ts-3-5-b3", D(BEST, "* **As a deterministic gate**: a [Stop hook](/docs/en/hooks#stop) runs your check as a script and blocks the turn from ending until it passes.", "Claude Code, Best practices"),
                       "In Claude Code, a Stop hook, a script that runs when Claude wants to end its turn, can run the tests and keep the turn going until they pass.")])
            + code_pop_text("ts-3-5-code", "The code: an interview prompt", "A prompt for the interview pattern", BEST, INT35, "Claude Code, Best practices",
                            "Claude asks the questions with AskUserQuestion, then writes SPEC.md.")
            + tab2_links("3.5", "%s %s" % (fact("ts-3-1-a02", "Its build guide uses no task statement of domain 2 or 3, by choice."), cf("ts-g1", excerpt("academy/facts/claude-code.md", "The pipeline itself is a Python program that calls the API. It is not Claude Code.", "Fact sheet of the build in Claude Code"), "The mock builder is a Python program that calls the Claude API. It is not Claude Code."))), "ts-3-5"))


# ----- part 3.6 (facts: academy/facts/ts-3-6.md) -----

HLESS, GHA, CWF, SOUT = "claude-code-docs-headless", "claude-code-docs-github-actions", "claude-code-docs-common-workflows", "claude-code-docs-agent-sdk-structured-outputs"
CLI36 = "\n".join(read(SRC % HLESS).split("\n")[163:166])
assert CLI36.startswith('claude -p "Extract') and "--json-schema" in CLI36
FIG36 = figure("3.6-1", 890, 320,
               "A pull request or a new commit starts a CI job that runs claude -p. CLAUDE.md, the prior findings and the existing tests give the context. "
               "With --output-format json and --json-schema, the findings come back as JSON, which the guide posts as inline comments on the pull request.",
               "".join([edge("M170 75H225"), edge("M425 75H480"), edge("M670 75H720", "post", 695, 66),
                        '<path class="ve-e no-head" d="M115 250V215H535V250M325 215V250"/>',
                        edge("M325 215V110", "context", 333, 165, anchor="r"),
                        box(20, 40, 150, 70, ["PR or", "new commit"]),
                        box(225, 40, 200, 70, ["claude -p"], sub="in the CI job", cls="who-model"),
                        box(480, 40, 190, 70, ["JSON"], sub="fits --json-schema"),
                        box(720, 40, 150, 70, ["Inline PR", "comments"], cls="try ok"),
                        box(20, 250, 190, 55, ["Prior findings"], sub="report only new"),
                        box(230, 250, 190, 55, ["Existing tests"], sub="for new tests"),
                        box(440, 250, 190, 55, ["CLAUDE.md"], sub="not with --bare")]),
               "%s %s" % (cf("ts-3-6-f1", D(HLESS, "Add the `-p` (or `--print`) flag to any `claude` command to run it non-interactively.", "Claude Code, Run Claude Code programmatically"),
                             "The -p flag runs Claude Code with no interaction."),
                          cf("ts-3-6-s2", gx("Using --output-format json with --json-schema to produce machine-parseable structured findings for automated posting as inline PR comments", "Exam guide, 3.6-S2"),
                             "In the guide, the structured findings become inline PR comments (3.6-S2).")))

PART["3.6"] = (overview("3.6", "In CI, run claude -p with a schema and context",
                        "In a pipeline, claude -p runs with no interaction, and --output-format json with --json-schema gives structured findings, which the guide posts as comments on the pull request (PR). "
                        "CLAUDE.md, the prior findings and the existing tests give the context.",
                        FIG36)
    + level("explanation",
            "<p><b>Run once.</b> %s %s %s</p>" % (
                cf("ts-3-6-k1", gx("The -p (or --print) flag for running Claude Code in non-interactive mode in automated pipelines", "Exam guide, 3.6-K1"),
                   "The -p flag, or --print, runs Claude Code with no interaction in a pipeline of continuous integration (CI) (3.6-K1)."),
                cf("ts-3-6-s1", gx("Running Claude Code in CI with the -p flag to prevent interactive input hangs", "Exam guide, 3.6-S1"),
                   "The guide uses it so that the CI job does not hang on a wait for input (3.6-S1)."),
                cf("ts-3-6-f2", D(HLESS, "Claude Code exits with code 0 on success and a non-zero code when the run fails, so your scripts can branch on the exit status.", "Claude Code, Run Claude Code programmatically"),
                   "Claude Code exits with code 0 on success, so a script can branch on the exit status."))
            + "<p><b>Structured findings.</b> %s %s %s</p>" % (
                cf("ts-3-6-k2", gx("--output-format json and --json-schema CLI flags for enforcing structured output in CI contexts", "Exam guide, 3.6-K2"),
                   "The guide uses --output-format json and --json-schema to enforce structured output (3.6-K2)."),
                cf("ts-3-6-f4", D(HLESS, "To get output conforming to a specific schema, use `--output-format json` with `--json-schema` and a [JSON Schema](https://json-schema.org/) definition. The response includes metadata about the request (session ID, usage, etc.) with the structured output in the `structured_output` field.", "Claude Code, Run Claude Code programmatically"),
                   "The answer then has it in the field structured_output."),
                cf("ts-3-6-c2", D(CLI, "Get validated JSON output matching a JSON Schema after the agent completes its workflow (print mode only).", "Claude Code, CLI reference"),
                   "The documentation says that the output is validated after the run, in print mode. It says &ldquo;validated&rdquo;, not &ldquo;enforced&rdquo;, and the exam uses the guide."))
            + "<p><b>Context.</b> %s %s %s</p>" % (
                cf("ts-3-6-k3", gx("CLAUDE.md as the mechanism for providing project context (testing standards, fixture conventions, review criteria) to CI-invoked Claude Code", "Exam guide, 3.6-K3"),
                   "The guide puts the project context in CLAUDE.md: testing standards, fixtures and review criteria (3.6-K3).") + " " + cf("ts-3-6-s5", gx("Documenting testing standards, valuable test criteria, and available fixtures in CLAUDE.md to improve test generation quality and reduce low-value test output", "Exam guide, 3.6-S5"),
                   "For test generation, it also names valuable test criteria, so that fewer low-value tests come out (3.6-S5)."),
                cf("ts-3-6-f9", D(GHA, "Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. Claude follows these guidelines when creating PRs and responding to requests.", "Claude Code, GitHub Actions"),
                   "The Claude Code GitHub Action also reads review criteria from CLAUDE.md."),
                cf("ts-3-6-c1", D(HLESS, "Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, custom commands, [subagents](/docs/en/sub-agents), installed plugins, MCP servers, auto memory, and CLAUDE.md.", "Claude Code, Run Claude Code programmatically"),
                   "But --bare, the mode that the documentation recommends for scripts, skips CLAUDE.md. The exam uses the guide."))
            + "<p><b>Re-runs and tests.</b> %s %s %s</p>" % (
                cf("ts-3-6-s3", gx("Including prior review findings in context when re-running reviews after new commits, instructing Claude to report only new or still-unaddressed issues to avoid duplicate comments", "Exam guide, 3.6-S3"),
                   "On a new commit, the guide gives Claude the prior findings and asks only for new or open issues, so the comments do not repeat (3.6-S3)."),
                cf("ts-3-6-s4", gx("Providing existing test files in context so test generation avoids suggesting duplicate scenarios already covered by the test suite", "Exam guide, 3.6-S4"),
                   "The guide gives the existing test files, so that new tests do not repeat them (3.6-S4)."),
                cf("ts-3-6-f15", D(CWF, "Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.", "Claude Code, Common workflows"),
                   "The documentation says that Claude reads the existing tests to match their style. It does not say that this avoids duplicates."))
            + "<p><b>An independent review.</b> %s %s</p>" % (
                cf("ts-3-6-k4", gx("Session context isolation: why the same Claude session that generated code is less effective at reviewing its own changes compared to an independent review instance", "Exam guide, 3.6-K4"),
                   "The session that wrote the code reviews it less well than an independent one (3.6-K4)."),
                cf("ts-3-6-f11", D(BEST, "A fresh context improves code review since Claude won't be biased toward code it just wrote.", "Claude Code, Best practices"),
                   "The documentation agrees: a fresh context is not biased toward the code it just wrote."))
            + exam_tests("3.6", [("Claude Code CLI — -p / --print flag for non-interactive mode, --output-format json, --json-schema for structured CI output", "Among the technologies, the guide names")])
            + "<p>%s</p>" % cf("ts-3-6-q10", gx("**Correct Answer: A.** The -p (or --print) flag is the documented way to run Claude Code in non-interactive mode.", "Exam guide, sample question 10"),
                               "Sample question 10 of the guide fits 3.6: a CI job hangs, and its correct answer adds the -p flag.")
            + guide_text("3.6"), "ts-3-6")
    + level("depth",
            beyond([cf("ts-3-6-b1", D(HLESS, "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release.", "Claude Code, Run Claude Code programmatically"),
                       "--bare is the recommended mode for scripts, and in a future release it will become the default for -p."),
                    cf("ts-3-6-b2", D(SOUT, "A result can also end with subtype `success` but no `structured_output` value, for example when the run completes without the agent producing a structured output. Treat that case as a failure as well.", "Agent SDK, Structured outputs"),
                       "In the Agent SDK, a run can end with the subtype success but no structured_output, so check structured_output, not only the subtype."),
                    cf("ts-3-6-b3", D(HLESS, "* **`dontAsk`**: Claude Code denies every call that would otherwise prompt, which is useful for locked-down CI runs.", "Claude Code, Run Claude Code programmatically"),
                       "The permission mode dontAsk denies each call that would ask for approval, for a locked-down CI run.")])
            + code_pop_text("ts-3-6-code", "The code: claude -p with a JSON schema", "A run of claude -p with a schema", HLESS, CLI36, "Claude Code, Run Claude Code programmatically",
                            "The result is JSON, with the answer in structured_output.")
            + tab2_links("3.6", "%s %s" % (fact("ts-3-1-a02", "Its build guide uses no task statement of domain 2 or 3, by choice."),
                                           fact("ts-g1", "The mock builder calls the Claude API from its own code, not Claude Code in CI.")))
            + '<p>The nearest example is the independent check of step 4 (task statement 4.6): <a href="%s#step-4">Step 4, Check by a model &rarr;</a></p>' % TAB2, "ts-3-6"))


# ----- part 4.2 (facts: academy/facts/ts-4-2.md) -----

ICON, FB51 = "anthropic-docs-increase-consistency", "anthropic-docs-prompting-claude-fable-5-1"
EX42 = "\n".join(read(SRC % FB51).split("\n")[790:799])
assert EX42.startswith("<example>") and EX42.endswith("</example>")
EXBOX42 = ('<g class="ve-n" transform="translate(20 110)"><rect class="sh" width="250" height="170" rx="0"/>'
           '<text x="125" y="28">&lt;examples&gt;</text><text class="sub" x="125" y="56">2 to 4 in the guide</text>'
           '<text class="sub" x="125" y="92">input: an ambiguous case</text><text class="sub" x="125" y="118">output: the fixed format</text>'
           '<text class="sub" x="125" y="144">reason: why this choice</text></g>')
FIG42 = figure("4.2-1", 890, 300,
               "A few-shot prompt has the instructions and a block of 2 to 4 examples. Each example has an input, often an ambiguous case, the output in the fixed format, "
               "and the reason for the choice. With a new input, Claude gives a consistent output, also for cases that the examples do not show.",
               "".join([edge("M270 60H300V135H330"), edge("M270 195H300V135H330"), edge("M430 210V170"), edge("M530 135H600"),
                        box(20, 30, 250, 60, ["Instructions"], sub="alone: inconsistent"),
                        EXBOX42,
                        box(330, 100, 200, 70, ["Claude"], cls="who-model"),
                        box(330, 210, 200, 60, ["New input"]),
                        box(600, 100, 270, 70, ["Consistent output"], sub="also for new cases", cls="try ok")]),
               "%s %s" % (cf("ts-4-2-s1", gx("Creating 2-4 targeted few-shot examples for ambiguous scenarios that show reasoning for why one action was chosen over plausible alternatives", "Exam guide, 4.2-S1"),
                             "The guide gives 2 to 4 targeted examples for ambiguous cases, each with the reason for the choice (4.2-S1)."),
                          cf("ts-4-2-f12", D(PBP, "* **Structured:** Wrap examples in `<example>` tags (multiple examples in `<examples>` tags) so Claude can distinguish them from instructions.", "Prompting best practices"),
                             "The documentation puts the examples in tags, apart from the instructions.")))

PART["4.2"] = (overview("4.2", "Few-shot examples fix what instructions alone leave inconsistent",
                        "When detailed instructions still give inconsistent output, add 2 to 4 targeted examples that show the exact output format and the hard cases, each with the reason for the choice. "
                        "Varied examples help Claude with new cases too.",
                        FIG42)
    + level("explanation",
            "<p><b>When instructions are not enough.</b> %s %s %s</p>" % (
                cf("ts-4-2-k1", gx("Few-shot examples as the most effective technique for achieving consistently formatted, actionable output when detailed instructions alone produce inconsistent results", "Exam guide, 4.2-K1"),
                   "The guide calls few-shot examples the most effective technique when detailed instructions alone give inconsistent output (4.2-K1)."),
                cf("ts-4-2-f1", D(PBP, "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure.", "Prompting best practices"),
                   "The documentation calls them one of the most reliable ways. The exam uses the guide."),
                cf("ts-4-2-f2", D(ICON, "Provide examples of your desired output. This is more effective than abstract instructions.", "Increase output consistency"),
                   "The documentation also says that an example of the output is more effective than abstract instructions."))
            + "<p><b>The format.</b> %s</p>" %
                cf("ts-4-2-s2", gx("Including few-shot examples that demonstrate specific desired output format (location, issue, severity, suggested fix) to achieve consistency", "Exam guide, 4.2-S2"),
                   "The examples show the exact format, such as location, issue, severity and suggested fix (4.2-S2).")
            + "<p><b>Hard cases.</b> %s %s %s</p>" % (
                cf("ts-4-2-k2", gx("The role of few-shot examples in demonstrating ambiguous-case handling (e.g., tool selection for ambiguous requests, branch-level test coverage gaps)", "Exam guide, 4.2-K2"),
                   "Examples show how to handle ambiguous cases, such as the choice of a tool for an unclear request (4.2-K2).") + " " + cf("ts-4-2-c3", gx("Few-shot examples (A) add token overhead without fixing the underlying issue.", "Exam guide, sample question 2"),
                   "For the choice of a tool, the guide itself puts a good tool description first (part 2.1)."),
                cf("ts-4-2-f7", D(PBP, "Include 3–5 examples for best results.", "Prompting best practices"),
                   "The documentation gives 3 to 5 examples, not 2 to 4. The exam uses the guide."),
                cf("ts-4-2-f4", D(PBP, "* **Diverse:** Cover edge cases and vary enough that Claude doesn't pick up unintended patterns.", "Prompting best practices"),
                   "The documentation advises examples that cover edge cases and vary, so that Claude does not copy a pattern by accident."))
            + "<p><b>New patterns.</b> %s %s</p>" % (
                cf("ts-4-2-k3", gx("How few-shot examples enable the model to generalize judgment to novel patterns rather than matching only pre-specified cases", "Exam guide, 4.2-K3"),
                   "The guide says that examples let Claude carry its judgment to new patterns, not only match the cases shown (4.2-K3)."),
                cf("ts-4-2-f8", D(PBP, "Claude is smart enough to generalize from the explanation.", "Prompting best practices"),
                   "The documentation says this about an instruction with its reason, not about examples: Claude generalizes from the explanation."))
            + "<p><b>False positives and extraction.</b> %s %s %s %s</p>" % (
                cf("ts-4-2-s3", gx("Providing few-shot examples distinguishing acceptable code patterns from genuine issues to reduce false positives while enabling generalization", "Exam guide, 4.2-S3"),
                   "Examples that separate acceptable code from real issues reduce false positives (4.2-S3)."),
                cf("ts-4-2-k4", gx("The effectiveness of few-shot examples for reducing hallucination in extraction tasks (e.g., handling informal measurements, varied document structures)", "Exam guide, 4.2-K4"),
                   "In extraction, examples reduce hallucination (4.2-K4)."),
                cf("ts-4-2-s5", gx("Adding few-shot examples showing correct extraction from documents with varied formats to address empty/null extraction of required fields", "Exam guide, 4.2-S5"),
                   "Examples of documents with varied formats fix required fields that come back empty (4.2-S5)."),
                cf("ts-4-2-s4", gx("Using few-shot examples to demonstrate correct handling of varied document structures (inline citations vs bibliographies, methodology sections vs embedded details)", "Exam guide, 4.2-S4"),
                   "Examples also show how to handle varied structures, such as inline citations against a bibliography (4.2-S4). Only the guide states these four points."))
            + exam_tests("4.2", [("Few-shot prompting: ambiguous scenario targeting, format consistency, false positive reduction", "Among the topics, the guide names")])
            + guide_text("4.2"), "ts-4-2")
    + level("depth",
            beyond([cf("ts-4-2-b1", D(ICON, "If you need Claude to always output valid JSON that conforms to a specific schema, use [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) instead of the prompt engineering techniques below.", "Increase output consistency"),
                       "For JSON that must always fit a schema, the documentation uses structured outputs, not examples (part 4.3)."),
                    cf("ts-4-2-b2", D(DEFT, "Examples are included in the prompt alongside your tool schema, showing Claude concrete patterns for well-formed tool calls. This helps Claude understand when to include optional parameters, what formats to use, and how to structure complex inputs.", "Define tools"),
                       "A client tool can carry its own examples of well-formed calls, which show how to fill a call. In our reading, they do not help with the choice of a tool."),
                    cf("ts-4-2-b3", D(PBP, "You can also ask Claude to evaluate your examples for relevance and diversity, or to generate additional ones based on your initial set.", "Prompting best practices"),
                       "Claude can check your examples for relevance and diversity, or write more of them.")])
            + code_pop_text("ts-4-2-code", "The code: an example with its reason", "A few-shot example with a rationale", FB51, EX42, "Prompting Claude Fable 5.1",
                            "Written for Claude Fable 5.1, to stop it from copying source text without quotation marks: the example has the request, the response, and a rationale that says why it is correct.")
            + tab2_links("4.2") + "<p>%s %s</p>" % (cf("ts-4-2-s2use11", excerpt(step_file(2), "3 sample questions of the guide as examples of the form", "Build guide, step 2"), "Step 2 gives the writer 3 sample questions of the guide as examples of the form."), cf("ts-4-2-s2use", excerpt(step_file(2), "A limit: the examples have no reason for each option, so they do not show the complete form.", "Build guide, step 2"),
                                                    "They have no reason for each option, so they do not show the complete form.")), "ts-4-2"))


# ----- part 4.1 (facts: academy/facts/ts-4-1.md) -----

CREV = "claude-code-docs-code-review"
REV41 = "\n".join(read(SRC % CREV).split("\n")[202:211])
assert REV41.startswith("# Review instructions") and REV41.endswith("most.")
FIG41 = figure("4.1-1", 890, 320,
               "Candidate findings pass through explicit criteria: report bugs and security issues, skip minor style. Then severity criteria, each with a code example, classify them. "
               "The findings are posted. If one category gives many false positives, it loses the trust of the developers, so it is disabled for a time while its prompt improves.",
               "".join([edge("M190 75H240"), edge("M470 75H520"), edge("M680 75H730"),
                        edge("M800 120V225H790"),
                        edge("M540 225H355V120", "disable, fix the prompt", 445, 216, cls="is-hot"),
                        '<text class="ve-lab" x="20" y="300">not: &#8220;be conservative&#8221; or &#8220;only high-confidence&#8221;</text>',
                        box(20, 40, 170, 70, ["Candidate", "findings"]),
                        box(240, 30, 230, 90, ["Explicit criteria"], sub="report bugs, skip style"),
                        box(520, 30, 160, 90, ["Severity"], sub="code examples"),
                        box(730, 30, 140, 90, ["Posted", "findings"], cls="try ok"),
                        box(540, 190, 250, 70, ["A noisy category?"], sub="false positives lose trust")]),
               "%s %s" % (cf("ts-4-1-s1", gx("Writing specific review criteria that define which issues to report (bugs, security) versus skip (minor style, local patterns) rather than relying on confidence-based filtering", "Exam guide, 4.1-S1"),
                             "Specific criteria say which issues to report and which to skip, in place of a filter by confidence (4.1-S1)."),
                          cf("ts-4-1-s2", gx("Temporarily disabling high false-positive categories to restore developer trust while improving prompts for those categories", "Exam guide, 4.1-S2"),
                             "The guide disables a noisy category for a time, while its prompt improves (4.1-S2).")))

PART["4.1"] = (overview("4.1", "Name what to report, not how careful to be",
                        "A review prompt gets precise when it names the categories to report and to skip, and gives a code example for each severity level. "
                        "&ldquo;Be conservative&rdquo; does not make it precise.",
                        FIG41)
    + level("explanation",
            "<p><b>Explicit criteria.</b> %s %s %s</p>" % (
                cf("ts-4-1-k1", gx("The importance of explicit criteria over vague instructions (e.g., \"flag comments only when claimed behavior contradicts actual code behavior\" vs \"check that comments are accurate\")", "Exam guide, 4.1-K1"),
                   "An explicit criterion, such as &ldquo;flag comments only when claimed behavior contradicts actual code behavior&rdquo;, works better than &ldquo;check that comments are accurate&rdquo; (4.1-K1)."),
                cf("ts-4-1-f1", D(PBP, "Claude responds well to clear, explicit instructions. Being specific about your desired output can help enhance results.", "Prompting best practices"),
                   "The documentation agrees: Claude responds well to clear, explicit instructions."),
                cf("ts-4-1-f3", D(CREV, "**Verification bar**: require evidence before a class of finding is posted.", "Claude Code, Code Review"),
                   "Code Review of Claude Code, a research preview for Team and Enterprise plans, can require evidence before a class of finding is posted."))
            + "<p><b>Vague words fail.</b> %s %s</p>" % (
                cf("ts-4-1-k2", gx("How general instructions like \"be conservative\" or \"only report high-confidence findings\" fail to improve precision compared to specific categorical criteria", "Exam guide, 4.1-K2"),
                   "The guide says that &ldquo;be conservative&rdquo; or &ldquo;only report high-confidence findings&rdquo; does not improve precision (4.1-K2)."),
                cf("ts-4-1-f5", D(O5, "If your review prompt says \"only report high-severity issues\" or \"be conservative,\" the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead.", "Prompting Claude Opus 5"),
                   "The documentation for Claude Opus 5 gives another reason: the model may report less. It advises to report everything and to filter in a separate pass. The exam uses the guide."))
            + "<p><b>Report and skip.</b> %s %s</p>" % (cf("ts-4-1-f9", D(CREV, "* **`REVIEW.md`**: review-only instructions, given to the agents that find and verify findings and consulted by the agents that rank and report them. Use it to say what your team wants flagged, at what severity, and how findings are reported.", "Claude Code, Code Review"), "In Code Review, a file REVIEW.md says what the team wants flagged, and at what severity."),
                cf("ts-4-1-f10", D(CREV, "**Skip rules**: list paths, branch patterns, and finding categories where Claude should post no findings.", "Claude Code, Code Review"),
                   "Its skip rules name the paths and categories with no findings."))
            + "<p><b>Trust.</b> %s Only the guide states this point and 4.1-S2.</p>" %
                cf("ts-4-1-k3", gx("The impact of false positive rates on developer trust: high false positive categories undermine confidence in accurate categories", "Exam guide, 4.1-K3"),
                   "A category with many false positives makes developers doubt the accurate categories too (4.1-K3).")
            + "<p><b>Severity.</b> %s %s</p>" % (
                cf("ts-4-1-s3", gx("Defining explicit severity criteria with concrete code examples for each severity level to achieve consistent classification", "Exam guide, 4.1-S3"),
                   "The guide says that explicit severity criteria, with a code example for each level, make the classification consistent (4.1-S3)."),
                cf("ts-4-1-f12", D(CREV, "State explicitly which classes of finding are Important and which are Nit at most.", "Claude Code, Code Review"),
                   "The documentation says to state in REVIEW.md which classes are Important and which are Nit, and its example uses prose, with no code (see the popup). The exam uses the guide."))
            + '<div><h4 class="gh2">The exam tests</h4><p>No line of section 17 is for 4.1 alone. %s %s</p></div>' % (
                cf("ts-4-1-x0", gx("You need to design prompts that provide actionable feedback and minimize false positives.", "Exam guide, scenario 5"),
                   "Scenario 5, Claude Code for continuous integration, asks for prompts that give actionable feedback and few false positives."),
                mock_count("4.1"))
            + guide_text("4.1"), "ts-4-1")
    + level("depth",
            beyond([cf("ts-4-1-b1", D(CREV, "At `low`, the review reports the findings it's most confident in, so you see fewer false positives.", "Claude Code, Code Review"),
                       "The command /code-review at low effort reports only the findings that it is most confident in: a filter by confidence, which the guide rejects."),
                    cf("ts-4-1-b2", D(CREV, "Length has a cost: a long `REVIEW.md` dilutes the rules that matter most.", "Claude Code, Code Review"),
                       "In Code Review, a long REVIEW.md weakens the rules that matter most."),
                    cf("ts-4-1-b3", D(CREV, "The review follows your `CLAUDE.md` like any Claude Code session, but it doesn't read [`REVIEW.md`](#review-md).", "Claude Code, Code Review"),
                       "The local /code-review follows CLAUDE.md, but it does not read REVIEW.md.")])
            + code_pop_text("ts-4-1-code", "The code: severity criteria in a REVIEW.md", "Severity criteria for a code review", CREV, REV41, "Claude Code, Code Review",
                            "Code Review is in research preview for Team and Enterprise plans.")
            + tab2_links("4.1") + "<p>%s</p>" % cf("ts-4-1-use", excerpt(step_file(4), "Written for the review of code. Here: one result for each exact rule, not one total verdict.", "Build guide, step 4"),
                                                    "The steps use 4.1-K1 for exact rules of a question, not for a review of code: for example, step 4 gives one result for each exact rule, not one total verdict."), "ts-4-1"))


# ----- part 4.3 (facts: academy/facts/ts-4-3.md) -----

SOUTA, STRICT = "anthropic-docs-structured-outputs", "anthropic-docs-strict-tool-use"
FIG43 = figure("4.3-1", 890, 320,
               "A request carries the document and extraction tools, each with a schema. With tool_choice auto, Claude can call a tool or answer in text. With any, it must call one tool and picks which. "
               "With a forced tool, it calls that tool, for example extract_metadata first. The input of the tool_use block is the data, with no syntax errors, and code still checks the values.",
               "".join(['<path class="ve-e no-head" d="M220 155H270M270 50V230"/>',
                        edge("M270 50H320"), edge("M270 140H320"), edge("M270 230H320"),
                        edge("M580 140H610V105H640"), edge("M580 230H610V105H640"),
                        edge("M755 140V200"),
                        '<text class="ve-lab" x="320" y="305">Claude Opus 5.5 and three other current models reject any and tool</text>',
                        box(20, 110, 200, 90, ["Request"], sub="tools with schemas"),
                        box(320, 20, 260, 60, ["auto"], sub="a tool call or text"),
                        box(320, 110, 260, 60, ["any"], sub="one tool, Claude picks"),
                        box(320, 200, 260, 60, ["tool: extract_metadata"], sub="that tool first"),
                        box(640, 70, 230, 70, ["tool_use input"], sub="no syntax errors (strict)", cls="who-model"),
                        box(640, 200, 230, 70, ["Code checks"], sub="the values", cls="try ok")]),
               "%s %s" % (cf("ts-4-3-k2", gx("The distinction between tool_choice: \"auto\" (model may return text instead of calling a tool), \"any\" (model must call a tool but can choose which), and forced tool selection (model must call a specific named tool)", "Exam guide, 4.3-K2"),
                             "The three settings of tool_choice are those of the guide (4.3-K2)."),
                          cf("ts-4-3-k3", gx("That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)", "Exam guide, 4.3-K3"),
                             "The guide says that a schema stops syntax errors, but not errors of meaning, such as line items that do not sum to the total (4.3-K3).")))

PART["4.3"] = (overview("4.3", "A schema guarantees the form, not the values",
                        "Give Claude a JSON schema with structured outputs or a strict tool, and the output parses. Code must still check the values, and a field that a source can lack must be nullable, so that Claude does not invent a value.",
                        FIG43)
    + level("explanation",
            "<p><b>The guarantee.</b> %s %s %s</p>" % (
                cf("ts-4-3-k1", gx("Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors", "Exam guide, 4.3-K1"),
                   "The guide calls tool use with a JSON schema the most reliable way to get output that fits the schema, with no syntax errors (4.3-K1)."),
                cf("ts-4-3-f3", D(STRICT, "Without strict mode, Claude might return incompatible types (`\"2\"` instead of `2`) or omit required fields, breaking your functions and causing runtime errors.", "Strict tool use"),
                   "In the documentation, a tool without strict: true can return wrong types or miss required fields,"),
                cf("ts-4-3-f1", D(SOUTA, "Structured outputs guarantee schema-compliant responses through constrained decoding:", "Structured outputs"),
                   "and structured outputs, a schema in output_config.format with no tool, guarantee the form. The exam uses the guide."))
            + "<p><b>The data.</b> %s %s</p>" % (
                cf("ts-4-3-s1", gx("Defining extraction tools with JSON schemas as input parameters and extracting structured data from the tool_use response", "Exam guide, 4.3-S1"),
                   "An extraction tool has the schema as its input, and the data comes from the tool_use response (4.3-S1)."),
                cf("ts-4-3-f5", D(HANDLE, "1. Extract the `name`, `id`, and `input` from the `tool_use` block.", "Handle tool calls"),
                   "The data is the input of the tool_use block."))
            + "<p><b>tool_choice.</b> %s %s %s</p>" % (
                cf("ts-4-3-s2", gx("Setting tool_choice: \"any\" to guarantee structured output when multiple extraction schemas exist and the document type is unknown", "Exam guide, 4.3-S2"),
                   "With several schemas and an unknown document type, any makes Claude call one of them (4.3-S2)."),
                cf("ts-4-3-s3", gx("Forcing a specific tool with tool_choice: {\"type\": \"tool\", \"name\": \"extract_metadata\"} to ensure a particular extraction runs before enrichment steps", "Exam guide, 4.3-S3"),
                   "A forced tool makes one extraction run first (4.3-S3)."),
                fact("ts-2-3-f13", "But Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 return a 400 error for any and for a forced tool. The exam uses the guide."))
            + "<p><b>Schema design.</b> %s %s %s %s</p>" % (
                cf("ts-4-3-k4", gx("Schema design considerations: required vs optional fields, enum fields with \"other\" + detail string patterns for extensible categories", "Exam guide, 4.3-K4"),
                   "A schema chooses between required and optional fields, and an enum can have &ldquo;other&rdquo; with a detail string (4.3-K4)."),
                cf("ts-4-3-s4", gx("Designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields", "Exam guide, 4.3-S4"),
                   "A field that a document can lack is nullable, so Claude does not invent a value (4.3-S4)."),
                cf("ts-4-3-s5", gx("Adding enum values like \"unclear\" for ambiguous cases and \"other\" + detail fields for extensible categorization", "Exam guide, 4.3-S5"),
                   "An enum value &ldquo;unclear&rdquo; covers ambiguous cases (4.3-S5)."),
                cf("ts-4-3-s6", gx("Including format normalization rules in prompts alongside strict output schemas to handle inconsistent source formatting", "Exam guide, 4.3-S6"),
                   "The prompt also gives rules to normalize formats (4.3-S6). Only the guide names these patterns."))
            + exam_tests("4.3", [("Structured output via tool_use: schema design, tool_choice configuration, nullable fields to prevent hallucination", "Among the topics, the guide names")])
            + guide_text("4.3"), "ts-4-3")
    + level("depth",
            beyond([cf("ts-4-3-b1", D(DEFT, "Forcing a tool also skips thinking on every model that accepts forced tool use: the response starts with the `tool_use` block and has no `thinking` block.", "Define tools"),
                       "On the models that accept a forced tool, the forced call skips thinking."),
                    cf("ts-4-3-b2", D(SOUTA, "While structured outputs guarantee schema compliance in most cases, there are scenarios where the output may not match your schema:", "Structured outputs"),
                       "Structured outputs fit the schema in most cases, not all. The page names cases such as a refusal or the limit of max_tokens."),
                    cf("ts-4-3-b3", D(SOUTA, "2. **Reduce optional parameters.** Make parameters `required` where possible. Each optional parameter roughly doubles a portion of the grammar's state space.", "Structured outputs"),
                       "When a schema hits the limits of complexity, the documentation advises required fields where possible, because each optional field makes the grammar much larger.")])
            + code_pop("ts-4-3-code", "The code: a request with structured outputs", "A request with a JSON schema in output_config", SOUTA, "curl https://api.anthropic.com/v1/messages", "}'", "Structured outputs",
                       "The schema goes in output_config.format, with no tool. This is the method of the mock builder.")
            + tab2_links("4.3") + "<p>%s %s</p>" % (
                cf("ts-4-3-d40", excerpt(D40, "Option 2. Steps 2, 4 and 6 (and step 5, which uses the request of step 2) send their form as a JSON schema in `output_config.format`.", "Mock decision 0040"),
                   "The mock builder keeps the purpose of 4.3 and changes the method: its steps send each form as a JSON schema in output_config.format, with no tool,") + " " + cf("ts-4-3-model", excerpt("src/model_call.py", 'MODEL = "claude-opus-5-5"', "The code of the model calls"),
                   "because its model, Claude Opus 5.5, does not accept a forced tool call."),
                cf("ts-4-3-d40b", excerpt(D40, "Code still checks each answer (decisions 0031, 0032 and 0039). A schema does not check meaning.", "Mock decision 0040"),
                   "A schema does not check meaning, so code checks the content in step 3.")), "ts-4-3"))


# ----- part 4.4 (facts: academy/facts/ts-4-4.md) -----

RETRY44 = "\n".join(read(SRC % HANDLE).split("\n")[233:244])
assert RETRY44.strip().startswith("{") and "Missing required 'location' parameter" in RETRY44
FIG44 = figure("4.4-1", 890, 320,
               "Claude extracts data from the source document. Code checks the values. If the check passes, the result is used. If it fails, and a retry can fix it, "
               "a follow-up request sends the document, the failed result and the exact errors back to Claude. If the information is absent from the source, the loop stops.",
               "".join([edge("M170 75H220"), edge("M390 75H440"), edge("M630 75H690", "pass", 660, 66),
                        edge("M535 110V170", "fail", 543, 145, anchor="r"),
                        edge("M440 205H305V110", "yes: format", 372, 196, cls="is-hot"),
                        edge("M630 205H690", "no", 660, 196),
                        '<text class="ve-lab" x="20" y="300">a retry sends the document, the failed result and the exact errors</text>',
                        box(20, 40, 150, 70, ["Source", "document"]),
                        box(220, 40, 170, 70, ["Claude", "extracts"], cls="who-model"),
                        box(440, 40, 190, 70, ["Checks in code"], sub="sums, fields"),
                        box(690, 40, 180, 70, ["Use the result"], cls="try ok"),
                        box(440, 170, 190, 70, ["Can a retry", "fix it?"]),
                        box(690, 170, 180, 70, ["Stop"], sub="information absent")]),
               "%s %s" % (cf("ts-4-4-s1", gx("Implementing follow-up requests that include the original document, the failed extraction, and specific validation errors for model self-correction", "Exam guide, 4.4-S1"),
                             "The follow-up request has the original document, the failed extraction and the specific errors (4.4-S1)."),
                          cf("ts-4-4-k2", gx("The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)", "Exam guide, 4.4-K2"),
                             "A retry does not help when the information is absent from the source (4.4-K2).")))

PART["4.4"] = (overview("4.4", "Retry with the exact errors, but not for missing facts",
                        "When an extraction fails a check, send the document, the failed result and the specific errors back, so that the model can correct it. "
                        "A retry fixes format and structure, not information that the source does not have.",
                        FIG44)
    + level("explanation",
            "<p><b>Retry with the errors.</b> %s %s</p>" % (
                cf("ts-4-4-k1", gx("Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction", "Exam guide, 4.4-K1"),
                   "On a retry, the prompt gets the specific validation errors, which guide the correction (4.4-K1)."),
                cf("ts-4-4-f1", D(PBP, "The most common chaining pattern is **self-correction:** generate a draft → have Claude review it against criteria → have Claude refine based on the review.", "Prompting best practices"),
                   "The documentation names a related pattern: a draft, a review against criteria, then a refinement."))
            + "<p><b>When a retry does not help.</b> %s %s</p>" % (
                cf("ts-4-4-s2", gx("Identifying when retries will be ineffective (e.g., information exists only in an external document not provided) versus when they will succeed (format mismatches, structural output errors)", "Exam guide, 4.4-S2"),
                   "The guide says that a retry succeeds for a format or a structure error, and fails when the information is only in a document that Claude did not get (4.4-S2). Only the guide states this limit."),
                cf("ts-4-4-f5", D(SOUTA, "* Retry with a higher `max_tokens` value to get the complete structured output", "Structured outputs"),
                   "With structured outputs, one structural error that a retry fixes is output cut off at max_tokens, sent again with a higher limit."))
            + "<p><b>Meaning, not syntax.</b> %s %s</p>" % (
                cf("ts-4-4-k4", gx("The difference between semantic validation errors (values don't sum, wrong field placement) and schema syntax errors (eliminated by tool use)", "Exam guide, 4.4-K4"),
                   "A schema stops syntax errors, but values that do not sum or a value in the wrong field are errors of meaning (4.4-K4)."),
                fact("ts-4-3-f3", "In the documentation, a tool without strict: true can still miss a required field (part 4.3)."))
            + "<p><b>Checks and feedback.</b> %s %s %s</p>" % (
                cf("ts-4-4-s4", gx("Designing self-correction validation flows: extracting \"calculated_total\" alongside \"stated_total\" to flag discrepancies, adding \"conflict_detected\" booleans for inconsistent source data", "Exam guide, 4.4-S4"),
                   "The output can carry its own checks: a calculated_total next to the stated_total, and a conflict_detected flag (4.4-S4)."),
                cf("ts-4-4-k3", gx("Feedback loop design: tracking which code constructs trigger findings (detected_pattern field) to enable systematic analysis of dismissal patterns", "Exam guide, 4.4-K3"),
                   "A detected_pattern field records which code construct caused a finding (4.4-K3),"),
                cf("ts-4-4-s3", gx("Adding detected_pattern fields to structured findings to enable analysis of false positive patterns when developers dismiss findings", "Exam guide, 4.4-S3"),
                   "so that the findings that developers dismiss show patterns of false positives (4.4-S3). Only the guide names these fields."))
            + exam_tests("4.4", [("Pydantic — schema validation, semantic validation errors, validation-retry loops", "Among the technologies, the guide names")])
            + guide_text("4.4"), "ts-4-4")
    + level("depth",
            beyond([cf("ts-4-4-b1", D(SOUTA, "Structured outputs don't guarantee the capitalization of string `enum` and `const` values:", "Structured outputs"),
                       "With structured outputs or strict tools, the schema does not guarantee the case of an enum value, so compare enum values without case."),
                    cf("ts-4-4-b2", D(SOUT, "Structured output generation can fail when the agent cannot produce valid JSON matching your schema. This typically happens when the schema is too complex for the task, the task itself is ambiguous, or the agent hits its retry limit trying to fix validation errors.", "Agent SDK, Structured outputs"),
                       "The Agent SDK retries a failed validation itself, up to a limit, and then the output can fail."),
                    cf("ts-4-4-b3", D(HANDLE, "If a tool request is invalid or missing parameters, Claude will retry 2-3 times with corrections before apologizing to the user.", "Handle tool calls"),
                       "For an invalid tool call with an error result, Claude retries 2 or 3 times with corrections. The guide gives no number of retries.")])
            + code_pop_text("ts-4-4-code", "The code: an error result that asks for a retry", "A tool result with the error", HANDLE, RETRY44, "Handle tool calls",
                            "For a client tool without strict mode: Claude reads the error and tries the call again, if the missing information is available to it.")
            + tab2_links("4.4") + "<p>%s</p>" % cf("ts-4-4-use", excerpt(step_file(5), "Here: the \"document\" is the request of step 2, the \"failed extraction\" is the failed question, and the \"validation errors\" are the findings.", "Build guide, step 5"),
                                                    "Step 5 is a retry with error feedback: the writer gets the request, the failed question and its exact findings, the three parts of 4.4-S1."), "ts-4-4"))


# ----- part 4.5 (facts: academy/facts/ts-4-5.md) -----

BATCH = "anthropic-docs-batch-processing"
D67 = "docs/decisions/0067-prompt-caching-of-the-guide-text.md"
RES45 = "\n".join(read(SRC % BATCH).split("\n")[755:774])
assert RES45.strip().startswith("client = anthropic.Anthropic()") and RES45.rstrip().endswith('print(f"Request expired {result.custom_id}")')
FIG45 = figure("4.5-1", 890, 330,
               "If somebody waits for the result, such as a pre-merge check, use the synchronous Messages API. If not, send a batch: half the price, a custom_id for each request. "
               "The results take up to 24 hours, come in any order, and are matched by custom_id. Only the failed requests, fixed where needed, go into a new batch.",
               "".join([edge("M110 120V50H260", "yes", 190, 41), edge("M200 165H260", "no", 230, 156),
                        edge("M480 165H540"), edge("M710 165H760"),
                        edge("M625 200V250"), edge("M540 280H370V200", "send again", 455, 272, cls="is-hot"),
                        box(20, 120, 180, 90, ["Does anybody", "wait?"]),
                        box(260, 20, 220, 60, ["Messages API"], sub="pre-merge check"),
                        box(260, 130, 220, 70, ["Message Batches"], sub="half price, custom_id", cls="who-model"),
                        box(540, 130, 170, 70, ["Results"], sub="up to 24 hours"),
                        box(760, 130, 110, 70, ["Use"], cls="try ok"),
                        box(540, 250, 170, 60, ["Failed only"], sub="fixed if needed")]),
               "%s %s" % (cf("ts-4-5-k2", gx("Batch processing is appropriate for non-blocking, latency-tolerant workloads (overnight reports, weekly audits, nightly test generation) and inappropriate for blocking workflows (pre-merge checks)", "Exam guide, 4.5-K2"),
                             "Batches suit work that can wait, such as an overnight report, and not a blocking check before a merge (4.5-K2)."),
                          cf("ts-4-5-s3", gx("Handling batch failures: resubmitting only failed documents (identified by custom_id) with appropriate modifications (e.g., chunking documents that exceeded context limits)", "Exam guide, 4.5-S3"),
                             "Only the failed documents go again, found by custom_id, and changed where needed, for example cut into chunks (4.5-S3).")))

PART["4.5"] = (overview("4.5", "Batch only the work that can wait a day",
                        "The Message Batches API costs half, but a batch can take up to 24 hours with no promised time, so use it only for work that nobody waits for. "
                        "Give each request a custom_id, match each result to its request by that ID, and send again only the requests that failed.",
                        FIG45)
    + level("explanation",
            "<p><b>Half the price, no promised time.</b> %s %s %s</p>" % (
                cf("ts-4-5-k1", gx("The Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed latency SLA", "Exam guide, 4.5-K1"),
                   "The Message Batches API saves 50%, takes up to 24 hours, and has no guaranteed latency in a service level agreement (4.5-K1)."),
                cf("ts-4-5-f5", D(BATCH, "This approach is well-suited to tasks that do not require immediate responses, with most batches finishing in less than 1 hour while reducing costs by 50% and increasing throughput.", "Batch processing"),
                   "The documentation says that most batches finish in less than 1 hour,"),
                cf("ts-4-5-f3", D(BATCH, "It is possible for a batch to expire and not complete within 24 hours.", "Batch processing"),
                   "but a batch can also expire before it completes."))
            + "<p><b>Who waits.</b> %s %s</p>" % (
                cf("ts-4-5-s1", gx("Matching API approach to workflow latency requirements: synchronous API for blocking pre-merge checks, batch API for overnight/weekly analysis", "Exam guide, 4.5-S1"),
                   "The synchronous API serves a blocking check before a merge, and the batch API an analysis overnight or each week (4.5-S1)."),
                cf("ts-4-5-q11", gx("This makes it unsuitable for blocking pre-merge checks where developers wait for results, but ideal for overnight batch jobs like technical debt reports.", "Exam guide, sample question 11"),
                   "Sample question 11 of the guide fits 4.5: it batches only the overnight report."))
            + "<p><b>Tool calls.</b> %s %s</p>" % (
                cf("ts-4-5-k3", gx("The batch API does not support multi-turn tool calling within a single request (cannot execute tools mid-request and return results)", "Exam guide, 4.5-K3"),
                   "The guide says that a batch request cannot run tools in the middle and continue with their results (4.5-K3)."),
                cf("ts-4-5-c1", D(BATCH, "All [server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) (web search, web fetch, code execution, MCP connectors, advisor, and tool search) work in batch requests. The batch worker runs the same server-side agentic loop as the synchronous Messages API.", "Batch processing"),
                   "In the documentation, server tools do run their loop inside a batch request, so the point holds for your own client tools. The exam uses the guide."))
            + "<p><b>custom_id.</b> %s %s</p>" % (
                cf("ts-4-5-k4", gx("custom_id fields for correlating batch request/response pairs", "Exam guide, 4.5-K4"),
                   "A custom_id links each response to its request (4.5-K4)."),
                cf("ts-4-5-f11", D(BATCH, "Batch results can be returned in any order, and may not match the ordering of requests when the batch was created. In the preceding example, the result for the second batch request is returned before the first. To correctly match results with their corresponding requests, always use the `custom_id` field.", "Batch processing"),
                   "The results come in any order, so the documentation always matches them by custom_id."))
            + "<p><b>Plan the batch.</b> %s %s %s %s</p>" % (
                cf("ts-4-5-s2", gx("Calculating batch submission frequency based on SLA constraints (e.g., 4-hour windows to guarantee 30-hour SLA with 24-hour batch processing)", "Exam guide, 4.5-S2"),
                   "The guide plans the submissions for a service level: a batch every 4 hours, plus 24 hours of processing, meets 30 hours (4.5-S2). The exam uses this arithmetic."),
                cf("ts-4-5-f47", D(BATCH, "Additionally, processing may be slowed down based on current demand and your request volume. In that case, you may see more requests expiring after 24 hours.", "Batch processing"),
                   "The documentation adds that under high demand more requests expire after 24 hours."),
                cf("ts-4-5-s4", gx("Using prompt refinement on a sample set before batch-processing large volumes to maximize first-pass success rates and reduce iterative resubmission costs", "Exam guide, 4.5-S4"),
                   "It refines the prompt on a sample before a large batch (4.5-S4)."),
                cf("ts-4-5-f16", D(BATCH, "* Dry run a single request shape with the Messages API to avoid validation errors.", "Batch processing"),
                   "The documentation tests the shape of one request on the Messages API first."))
            + exam_tests("4.5", [("Batch processing: Message Batches API appropriateness, latency tolerance assessment, failure handling by custom_id", "Among the topics, the guide names")])
            + guide_text("4.5"), "ts-4-5")
    + level("depth",
            beyond([cf("ts-4-5-b1", D(BATCH, "validation errors are returned when processing of the entire batch has ended.", "Batch processing"),
                       "Validation errors come back only when the whole batch has ended, so a wrong request can cost a long wait."),
                    cf("ts-4-5-b2", D(BATCH, "The pricing discounts from prompt caching and Message Batches can stack, providing even greater cost savings when both features are used together. However, because batch requests are processed asynchronously and concurrently, cache hits are provided on a best-effort basis.", "Batch processing"),
                       "The discounts of prompt caching and of batches can stack, but cache hits in a batch are not sure."),
                    cf("ts-4-5-b3h", D(BATCH, "The `output-300k-2026-03-24` beta header raises the `max_tokens` cap to 300,000 for batch requests using Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, or Claude Haiku 5.5.", "Batch processing"),
                       "A beta header raises the output of a batch request to 300,000 tokens, on some models only.")
                    + " " + cf("ts-4-5-b3", D(BATCH, "Extended output is available on the Message Batches API only, not the synchronous Messages API. It is supported on the Claude API and Claude Platform on AWS, and is not currently available on Amazon Bedrock, Google Cloud, or Microsoft Foundry.", "Batch processing"),
                       "This extended output exists only on the Message Batches API, on the Claude API and on Claude Platform on AWS.")])
            + code_pop_text("ts-4-5-code", "The code: results sorted by type and custom_id", "Handle the results of a batch", BATCH, RES45, "Batch processing",
                            "An invalid request must be fixed before it is sent again. A server error can be sent again as it is.")
            + tab2_links("4.5", cf("ts-4-5-d67", excerpt(D67, "2. The Message Batches API. The owner rejected it: the rounds of the pipeline would wait for each batch.", "Mock decision 0067"),
                                   "The owner rejected the Message Batches API: each round of the mock builder would wait for its batch, so the work is blocking (4.5-K2).")
                         + ' <a href="%s#step-4">Step 4, Check by a model &rarr;</a>' % TAB2), "ts-4-5"))


# ----- part 4.6 (facts: academy/facts/ts-4-6.md) -----

ETH = "anthropic-docs-extended-thinking"
D32 = glob.glob(os.path.join(ROOT, "docs/decisions/0032-*.md"))[0][len(ROOT) + 1:]
REV46 = "Use a subagent to review the rate limiter diff against PLAN.md. Check that\nevery requirement is implemented, the listed edge cases have tests, and\nnothing outside the task's scope changed. Report gaps, not style preferences."
FIG46 = figure("4.6-1", 890, 320,
               "Top: the writer keeps its reasoning, so a new reviewer instance that sees only the code and the criteria checks the code. "
               "Bottom: a large review gets one pass for each file, then an integration pass across the files, then a verification pass that adds a confidence to each finding, "
               "and the findings are routed by a calibrated confidence.",
               "".join(['<text class="ve-lab" x="20" y="14">Who reviews</text><text class="ve-lab" x="20" y="150">Split and route</text>',
                        edge("M200 55H260"), edge("M420 55H480"),
                        edge("M180 180H220V230H260"), edge("M180 230H260"), edge("M180 280H220V230H260"),
                        edge("M460 230H520"), edge("M690 230H740"),
                        box(20, 20, 180, 70, ["Writer"], sub="keeps its reasoning", cls="who-model"),
                        box(260, 20, 160, 70, ["The code"]),
                        box(480, 20, 240, 70, ["New reviewer"], sub="code and criteria only", cls="who-model"),
                        box(20, 160, 160, 40, ["File 1: pass"]), box(20, 210, 160, 40, ["File 2: pass"]), box(20, 260, 160, 40, ["File N: pass"]),
                        box(260, 195, 200, 70, ["Integration pass"], sub="across the files", cls="who-model"),
                        box(520, 195, 170, 70, ["Verification"], sub="confidence each"),
                        box(740, 195, 130, 70, ["Route"], sub="calibrated", cls="try ok")]),
               "%s %s" % (cf("ts-4-6-k1", gx("Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session", "Exam guide, 4.6-K1"),
                             "A model keeps the reasoning of its own work, so it is less likely to question its decisions in the same session (4.6-K1)."),
                          cf("ts-4-6-k3", gx("Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings", "Exam guide, 4.6-K3"),
                             "A large review splits into passes for each file plus passes across the files (4.6-K3).") + " The order of the passes in the figure is the page&rsquo;s."))

PART["4.6"] = (overview("4.6", "A new instance reviews each file, then the files together",
                        "The session that wrote the work keeps its reasoning, so it is less likely to question its own choices. Give the review to a new instance that sees only the work and the criteria, "
                        "and split a large review into one pass for each file plus one pass across the files.",
                        FIG46)
    + level("explanation",
            "<p><b>The writer is biased.</b> %s</p>" %
                cf("ts-4-6-f2", D(BEST, "A fresh context improves code review since Claude won't be biased toward code it just wrote.", "Claude Code, Best practices"),
                   "The Claude Code documentation agrees with 4.6-K1: Claude in a fresh context is not biased toward the code that it just wrote.")
            + "<p><b>A new instance.</b> %s %s %s %s</p>" % (
                cf("ts-4-6-k2", gx("Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking", "Exam guide, 4.6-K2"),
                   "The guide says that an independent instance, with no prior reasoning, finds subtle issues better than an instruction to check itself or extended thinking (4.6-K2)."),
                cf("ts-4-6-s1", gx("Using a second independent Claude instance to review generated code without the generator's reasoning context", "Exam guide, 4.6-S1"),
                   "So a second Claude instance reviews the code, without the reasoning of the writer (4.6-S1)."),
                cf("ts-4-6-f3", D(BEST, "A reviewer running in a fresh [subagent](/docs/en/sub-agents) context sees only the diff and the criteria you give it, not the reasoning that produced the change, so it evaluates the result on its own terms.", "Claude Code, Best practices"),
                   "In Claude Code, a reviewer in a fresh subagent sees only the diff and the criteria."),
                cf("ts-4-6-c2", D(ETH, "Extended thinking (`thinking.type: \"enabled\"` with `budget_tokens`) is deprecated on the Claude 4.6 models (requests using it still succeed). Claude 4.7 and later models do not support it and reject requests that use it, returning a 400 error.", "Extended thinking"),
                   "In the Claude API documentation, the mode that the guide calls extended thinking is deprecated on the Claude 4.6 models, and Claude 4.7 and later models reject it. The exam uses the guide."))
            + "<p><b>Passes.</b> %s %s %s %s Part 1.6 shows the same split.</p>" % (
                cf("ts-4-6-s2", gx("Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis", "Exam guide, 4.6-S2"),
                   "The passes for each file find local issues, and a separate integration pass follows the data flow across the files (4.6-S2)."),
                cf("ts-4-6-f9", D(WF, "Run a reviewer per file, then pass all the findings to one agent that ranks and deduplicates them.", "Claude Code, Workflows"), "The dynamic workflows of Claude Code also run a reviewer for each file, then one agent over all the findings."),
                cf("ts-4-6-f9c", D(WF, "Dynamic workflows are available on all paid plans, with Anthropic API access", "Claude Code, Workflows"), "They need a paid plan or API access."),
                cf("ts-4-6-q12", gx("Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.", "Exam guide, sample question 12"),
                   "Sample question 12 of the guide tests this split: one pass for each file, then an integration pass."))
            + "<p><b>Route by confidence.</b> %s %s %s</p>" % (
                cf("ts-4-6-s3", gx("Running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing", "Exam guide, 4.6-S3"),
                   "A verification pass adds the confidence of the model to each finding, to route the review (4.6-S3)."),
                cf("ts-4-6-f16", gx("Field-level confidence scores calibrated using labeled validation sets for routing review attention", "Exam guide, 5.5-K3"),
                   "In 5.5-K3, which is about the extraction of data, the guide calibrates confidence on labeled validation sets."),
                cf("ts-4-6-f17", gx("Option B fails because LLM self-reported confidence is poorly calibrated—the agent is already incorrectly confident on hard cases.", "Exam guide, sample question 3"),
                   "In sample question 3, which is about escalation, it calls self-reported confidence poorly calibrated. 4.6-S3 itself says only that the routing is calibrated."))
            + exam_tests("4.6", [("Confidence scoring — field-level confidence, calibration with labeled validation sets, stratified sampling for error rate measurement", "Among the technologies, the guide names")])
            + guide_text("4.6"), "ts-4-6")
    + level("depth",
            beyond([cf("ts-4-6-b1", D(CCS, "This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session", "Claude Code, Subagents"),
                       "In Claude Code, a fork sees the same system prompt, tools, model and message history as the main session, so it is not an independent reviewer."),
                    cf("ts-4-6-b2", D(BEST, "A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do.", "Claude Code, Best practices"),
                       "A reviewer that is asked to find gaps usually reports some, also when the work is sound."),
                    cf("ts-4-6-b3", D(CREV, "Each agent looks for a different class of issue, then a verification step checks candidates against actual code behavior to filter out false positives.", "Claude Code, Code Review"),
                       "Code Review of Claude Code runs several agents, each for one class of issue, then a verification step.")
                    + " " + cf("ts-4-6-b3c", D(CREV, "Code Review is in research preview, available for [Team and Enterprise](https://claude.ai/admin-settings/claude-code) subscriptions.", "Claude Code, Code Review"),
                       "It is a research preview for Team and Enterprise subscriptions.")])
            + code_pop_text("ts-4-6-code", "The code: a prompt for an independent review", "A review by a subagent", BEST, REV46, "Claude Code, Best practices",
                            "The subagent checks the diff against the plan, with no reasoning of the writer.")
            + tab2_links("4.6") + "<p>%s %s %s %s</p>" % (
                cf("ts-4-6-use", excerpt(step_file(4), "The same context. Here: a new call, with no reasoning of the writer, checks the question.", "Build guide, step 4"),
                   "In step 4, a new call with no reasoning of the writer checks each question."),
                cf("ts-4-6-lim", excerpt(D32, "A limit: only call 4a is blind. Call 4b is not completely \"without prior reasoning context\", because it gets the reason of each option from the writer.", "Mock decision 0032"),
                   "But only call 4a is blind. Call 4b gets the reason that the writer gave for each option."),
                cf("ts-4-6-mod", excerpt("src/model_call.py", "MODEL = \"claude-opus-5-5\"", "Mock builder code, src/model_call.py"),
                   "The writer and the checker use the same model, so the independence comes from the context."),
                cf("ts-4-6-d32", excerpt(D32, "For now, this design does the opposite of the point. The guide calibrates confidence with \"labeled validation sets\": \"Field-level confidence scores calibrated using labeled validation sets for routing review attention\" (5.5-K3). The guide wrote that point for the extraction of data. We have no such labels before the owner marks mock 1 (decision 0022).", "Mock decision 0032"),
                   "No step uses 4.6-S3: the build had no labeled data to calibrate a confidence.")), "ts-4-6"))


# ----- part 5.1 (facts: academy/facts/ts-5-1.md) -----

COMP, CWIN, CEDIT, COMPD = "anthropic-docs-compaction", "anthropic-docs-context-windows", "anthropic-docs-context-editing", "anthropic-docs-compaction-on-demand"
WWM = "anthropic-docs-working-with-messages"
CMP51 = "\n".join(read(SRC % COMPD).split("\n")[784:790])
assert CMP51.startswith("{") and '"type": "summarize"' in CMP51 and CMP51.endswith("}")
FIG51 = figure("5.1-1", 890, 330,
               "One request of a long support session carries, from top to bottom: the system prompt, a block of case facts that is never summarized, a summary of the older turns where numbers can blur, "
               "the recent turns word for word, and tool results cut to the relevant fields. An order lookup with more than 40 fields is cut to the few that matter. The whole history goes to Claude on each turn.",
               "".join([edge("M620 280H470", "keep a few", 545, 271), edge("M470 165H545V115H620", "each turn", 583, 106),
                        box(20, 20, 450, 40, ["System prompt"]),
                        box(20, 70, 450, 60, ["Case facts"], sub="amounts, dates, order numbers: kept as they are", cls="try ok"),
                        box(20, 140, 450, 50, ["Summary of older turns"], sub="numbers can blur here"),
                        box(20, 200, 450, 40, ["Recent turns, word for word"]),
                        box(20, 250, 450, 60, ["Tool results"], sub="only the relevant fields"),
                        box(620, 70, 250, 90, ["Claude"], cls="who-model"),
                        box(620, 250, 250, 60, ["Order lookup"], sub="40+ fields")]),
               "%s %s" % (cf("ts-5-1-s1", gx("Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent \"case facts\" block included in each prompt, outside summarized history", "Exam guide, 5.1-S1"),
                             "The guide keeps amounts, dates, order numbers and statuses in a case facts block in each prompt, outside the summary (5.1-S1)."),
                          cf("ts-5-1-s3", gx("Trimming verbose tool outputs to only relevant fields before they accumulate in context (e.g., keeping only return-relevant fields from order lookups)", "Exam guide, 5.1-S3"),
                             "It cuts each tool output to the relevant fields before it enters the context (5.1-S3).")))

PART["5.1"] = (overview("5.1", "Pin exact facts outside the summary, and trim the rest",
                        "A summary of a long conversation blurs numbers, dates and promises, so keep these facts in a separate block that each request carries word for word. "
                        "Send the history each time, but cut tool results and agent outputs to what the next step needs.",
                        FIG51)
    + level("explanation",
            "<p><b>Summaries blur facts.</b> %s %s %s %s</p>" % (
                cf("ts-5-1-k1", gx("Progressive summarization risks: condensing numerical values, percentages, dates, and customer-stated expectations into vague summaries", "Exam guide, 5.1-K1"),
                   "A summary that grows step by step turns numbers, dates and what the customer expects into vague words (5.1-K1)."),
                cf("ts-5-1-f1", D(COMP, "Compaction replaces the older turns of a conversation with a summary that Claude writes on the server, so you need no summarization code of your own.", "Compaction"),
                   "With compaction, the Claude API itself can replace older turns with a summary."),
                cf("ts-5-1-f1b", D(COMP, "While both it and [Compaction at a token threshold](https://platform.claude.com/docs/en/build-with-claude/compaction-threshold) are in beta", "Compaction overview"),
                   "Both kinds of compaction are in beta."),
                cf("ts-5-1-s2", gx("Extracting and persisting structured issue data (order IDs, amounts, statuses) into a separate context layer for multi-issue sessions", "Exam guide, 5.1-S2"),
                   "The guide keeps the data of each issue in a separate layer (5.1-S2)."))
            + "<p><b>Position.</b> %s %s %s</p>" % (
                cf("ts-5-1-k2", gx("The \"lost in the middle\" effect: models reliably process information at the beginning and end of long inputs but may omit findings from middle sections", "Exam guide, 5.1-K2"),
                   "The guide says that a model can miss findings in the middle of a long input (5.1-K2),"),
                cf("ts-5-1-s4", gx("Placing key findings summaries at the beginning of aggregated inputs and organizing detailed results with explicit section headers to mitigate position effects", "Exam guide, 5.1-S4"),
                   "so a summary of key findings goes first, with clear section headers (5.1-S4)."),
                cf("ts-5-1-f7", D(CWIN, "As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*.", "Context windows"),
                   "The documentation names a related effect of length, context rot, not of position. The exam uses the guide."))
            + "<p><b>Tool results.</b> %s %s</p>" % (
                cf("ts-5-1-k3", gx("How tool results accumulate in context and consume tokens disproportionately to their relevance (e.g., 40+ fields per order lookup when only 5 are relevant)", "Exam guide, 5.1-K3"),
                   "Tool results pile up, for example more than 40 fields for each order lookup when only 5 matter (5.1-K3)."),
                cf("ts-5-1-f14", D(DEFT, "Return semantic, stable identifiers (for example, slugs or UUIDs) rather than opaque internal references, and include only the fields Claude needs to reason about its next step.", "Define tools"),
                   "The Claude API documentation agrees: design a tool to return only the fields that Claude needs for its next step."))
            + "<p><b>The history.</b> %s %s</p>" % (
                cf("ts-5-1-k4", gx("The importance of passing complete conversation history in subsequent API requests to maintain conversational coherence", "Exam guide, 5.1-K4"),
                   "Each request carries the complete conversation history (5.1-K4),"),
                cf("ts-5-1-f6", D(WWM, "The Messages API is stateless, which means that you always send the full conversational history to the API.", "Using the Messages API"),
                   "because the Messages API of Claude is stateless."))
            + "<p><b>Agent outputs.</b> %s %s</p>" % (
                cf("ts-5-1-s5", gx("Requiring subagents to include metadata (dates, source locations, methodological context) in structured outputs to support accurate downstream synthesis", "Exam guide, 5.1-S5"),
                   "A subagent returns its findings with metadata, such as dates and source locations (5.1-S5),"),
                cf("ts-5-1-s6", gx("Modifying upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning chains when downstream agents have limited context budgets", "Exam guide, 5.1-S6"),
                   "and as structured key facts, not long reasoning, when the next agent has little room (5.1-S6)."))
            + exam_tests("5.1", [("Context window optimization: trimming verbose tool outputs, structured fact extraction, position-aware input ordering", "Among the topics, the guide names")])
            + guide_text("5.1"), "ts-5-1")
    + level("depth",
            beyond([cf("ts-5-1-b1", D(COMPD, "In your `instructions`, say what the summary must retain and tell the model not to call tools.", "Compaction on demand"),
                       "With compaction on demand, a beta of the Claude API with the header compact-2026-09-04, your instructions say what the summary must keep.")
                    + " " + cf("ts-5-1-b1h", D(COMPD, "betaHeader: compact-2026-09-04", "Compaction on demand"), "Only the models in its list support it."),
                    cf("ts-5-1-b2", D(CEDIT, "The `clear_tool_uses_20250919` strategy clears tool results when conversation context grows beyond your configured threshold.", "Context editing"),
                       "With context editing, the Claude API clears old tool results above a threshold. It removes whole results, while 5.1-S3 cuts fields.")
                    + " " + cf("ts-5-1-b2b", D(CEDIT, "Context editing is in beta with support for tool result clearing and thinking block clearing.", "Context editing"), "Context editing is in beta."),
                    cf("ts-5-1-b3", D(BEST, "Customize compaction behavior in CLAUDE.md with instructions like `\"When compacting, always preserve the full list of modified files and any test commands\"` to ensure critical context survives summarization", "Claude Code, Best practices"),
                       "In Claude Code, an instruction in CLAUDE.md can say what a compaction must keep.")])
            + code_pop_text("ts-5-1-code", "The code: a summary that keeps named facts", "Compaction with instructions", COMPD, CMP51, "Compaction on demand",
                            "A beta of the Claude API. The instructions say what the summary must keep.")
            + tab2_links("5.1", cf("ts-5-1-d12", excerpt(D12, "A plain API call already has a separate context: the Messages API is stateless, and each call sees only what the program sends", "Mock decision 0012"), "The mock builder has no long conversation: each call sees only what the program sends.")), "ts-5-1"))


# ----- part 5.2 (facts: academy/facts/ts-5-2.md) -----

CSUP, UINP = "anthropic-docs-customer-support-chat", "claude-code-docs-agent-sdk-user-input"
D06 = glob.glob(os.path.join(ROOT, "docs/decisions/0006-*.md"))[0][len(ROOT) + 1:]
RULES52 = "\n".join(read(SRC % ICON).split("\n")[339:353])
assert RULES52.strip().startswith("Here is the user query") and RULES52.rstrip().endswith('section 3.2..."')
FIG52 = figure("5.2-1", 890, 330,
               "A customer message passes four checks: does the customer ask for a human, do several customers match, is the policy silent or unclear, can the agent make no progress. "
               "A request for a human, a policy gap and no progress lead to escalate_to_human. Several matches lead to a question for one more identifier. Sentiment and self-reported confidence are not triggers.",
               "".join([edge("M170 165H200", cls="no-head"), '<path class="ve-e no-head" d="M200 47V272"/>',
                        edge("M200 47H230"), edge("M200 122H230"), edge("M200 197H230"), edge("M200 272H230"),
                        '<path class="ve-e no-head is-hot" d="M480 47H560V272M480 197H560M480 272H560"/>',
                        edge("M560 145H620", "yes", 590, 136, cls="is-hot"),
                        '<text class="ve-lab" x="20" y="322">otherwise: resolve, and acknowledge any frustration</text>',
                        box(20, 130, 150, 70, ["Customer", "message"]),
                        box(230, 20, 250, 55, ["Asks for a human?"], sub="yes: escalate at once"),
                        box(230, 95, 250, 55, ["Several matches?"], sub="yes: ask for one more ID"),
                        box(230, 170, 250, 55, ["Policy silent?"], sub="yes: escalate"),
                        box(230, 245, 250, 55, ["No progress?"], sub="yes: escalate"),
                        box(620, 110, 250, 70, ["escalate_to_human"], cls="who-model"),
                        box(620, 220, 250, 70, ["Not triggers"], sub="sentiment, own confidence")]),
               "%s %s" % (cf("ts-5-2-k1", gx("Appropriate escalation triggers: customer requests for a human, policy exceptions/gaps (not just complex cases), and inability to make meaningful progress", "Exam guide, 5.2-K1"),
                             "The three triggers of the guide are a request for a human, a gap or exception in the policy, and no meaningful progress (5.2-K1)."),
                          cf("ts-5-2-k3", gx("Why sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity", "Exam guide, 5.2-K3"),
                             "Sentiment and self-reported confidence do not show how complex a case is (5.2-K3).") + " The order of the checks is the page&rsquo;s. "
                          + cf("ts-5-2-g71f", gx("(get_customer, lookup_order, process_refund, escalate_to_human)", "Exam guide, scenario 1"), "The tool escalate_to_human is from scenario 1 of the guide.")))

PART["5.2"] = (overview("5.2", "Escalate on explicit criteria, not on mood or confidence",
                        "Write the escalation criteria and a few examples into the system prompt: a request for a human, a gap in the policy, and no progress. "
                        "Do not escalate on sentiment or on a confidence that the model gives itself, and ask for one more identifier when a lookup finds several customers.",
                        FIG52)
    + level("explanation",
            "<p><b>Measure it.</b> %s</p>" %
                cf("ts-5-2-f2", D(CSUP, "Aim for an escalation accuracy of 95% or higher.", "Customer support agent"),
                   "The documentation for a support agent aims at an escalation accuracy of 95% or more.")
            + "<p><b>A request for a human.</b> %s %s %s Only the guide states these rules.</p>" % (
                cf("ts-5-2-k2", gx("The distinction between escalating immediately when a customer explicitly demands it versus offering to resolve when the issue is straightforward", "Exam guide, 5.2-K2"),
                   "When a customer demands a human, the agent escalates at once. When the issue is simple, it offers to resolve it (5.2-K2)."),
                cf("ts-5-2-s2", gx("Honoring explicit customer requests for human agents immediately without first attempting investigation", "Exam guide, 5.2-S2"),
                   "It does not investigate first (5.2-S2)."),
                cf("ts-5-2-s3", gx("Acknowledging frustration while offering resolution when the issue is within the agent's capability, escalating only if the customer reiterates their preference", "Exam guide, 5.2-S3"),
                   "When the issue is within its capability, the agent says that it understands the frustration and offers the fix. It escalates only if the customer asks again for a human (5.2-S3)."))
            + "<p><b>Not mood or confidence.</b> %s The limit is on a confidence that nobody calibrated. Task statements 4.6 and 5.5 use a confidence that labeled data calibrates.</p>" %
                cf("ts-5-2-f11", gx("Option D solves a different problem entirely; sentiment doesn't correlate with case complexity, which is the actual issue.", "Exam guide, sample question 3"),
                   "Sample question 3 of the guide says that sentiment does not follow the complexity of a case.")
            + "<p><b>Criteria in the prompt.</b> %s %s %s</p>" % (
                cf("ts-5-2-s1", gx("Adding explicit escalation criteria with few-shot examples to the system prompt demonstrating when to escalate versus resolve autonomously", "Exam guide, 5.2-S1"),
                   "Explicit criteria and few-shot examples in the system prompt show when to escalate and when to resolve (5.2-S1)."),
                cf("ts-5-2-f7", D(CSUP, "Before you add further layers to your architecture, consider the following less exhaustive options:", "Customer support agent"),
                   "The guide for a support agent in the Claude API documentation also says: before you add further layers,")
                + " " + cf("ts-5-2-f7b", D(CSUP, "* Ensure that you are making the most out of your prompts and optimizing through prompt engineering.", "Customer support agent"),
                   "get the most out of the prompt."),
                cf("ts-5-2-s4", gx("Escalating when policy is ambiguous or silent on the customer's specific request (e.g., competitor price matching when policy only addresses own-site adjustments)", "Exam guide, 5.2-S4"),
                   "When the policy is silent, such as on a price match with a competitor, the agent escalates (5.2-S4)."))
            + "<p><b>Several matches.</b> %s %s</p>" % (
                cf("ts-5-2-s5", gx("Instructing the agent to ask for additional identifiers when tool results return multiple matches, rather than selecting based on heuristics", "Exam guide, 5.2-S5"),
                   "When a lookup returns several customers, the agent asks for another identifier, and does not guess (5.2-S5).")
                + " " + cf("ts-5-2-k4", gx("How multiple customer matches require clarification (requesting additional identifiers) rather than heuristic selection", "Exam guide, 5.2-K4"), "The guide also names this case in 5.2-K4."),
                cf("ts-5-2-f14", D(OVT, "If the user's prompt doesn't include enough information to fill all the required parameters for a tool, Claude Opus is much more likely to recognize that a parameter is missing and ask for it. Claude Sonnet might ask, especially when prompted to think before outputting a tool request. But it might also infer a reasonable value.", "Tool use overview"),
                   "A near case in the Claude API documentation: when a required parameter of a tool is missing, Claude Opus is much more likely to ask for it, and Claude Sonnet might infer a value."))
            + exam_tests("5.2", [("Escalation decision-making: explicit criteria, honoring customer preferences, policy gap identification", "Among the topics, the guide names")])
            + "<p>%s</p>" % cf("ts-5-2-q3", gx("Adding explicit escalation criteria with few-shot examples directly addresses the root cause: unclear decision boundaries.", "Exam guide, sample question 3"),
                               "Sample question 3 of the guide fits 5.2: its correct answer adds explicit criteria with few-shot examples.")
            + guide_text("5.2"), "ts-5-2")
    + level("depth",
            beyond([cf("ts-5-2-b1", D(CSUP, "Typically aim for 70-80% deflection rate, depending on the complexity of inquiries.", "Customer support agent"),
                       "The guide for a support agent aims at a deflection rate of 70% to 80%, depending on the complexity of the inquiries.")
                    + " " + cf("ts-5-2-g71", gx("Your target is 80%+ first-contact resolution while knowing when to escalate.", "Exam guide, scenario 1"),
                       "That is a different measure from the 80%+ first-contact resolution of scenario 1 of the guide."),
                    cf("ts-5-2-b2", D(UINP, "Claude requests user input in two situations: when it needs **permission to use a tool** (like deleting files or running commands), and when it has **clarifying questions** (via the `AskUserQuestion` tool).", "Agent SDK, Handle approvals and user input"),
                       "In the Agent SDK, a clarifying question to the user is a call of the tool AskUserQuestion."),
                    cf("ts-5-2-b3", D(UINP, "* **Subagents**: `AskUserQuestion` is not currently available in subagents spawned via the Agent tool", "Agent SDK, Handle approvals and user input"),
                       "AskUserQuestion is not available at present in a subagent that the Agent tool starts.")])
            + code_pop_text("ts-5-2-code", "The code: rules and answers in a prompt", "A prompt with explicit rules", ICON, RULES52, "Increase output consistency",
                            "A document assistant, not a support agent: no page that we read shows a prompt with escalation criteria. This block is the user turn, after a system prompt.")
            + tab2_links("5.2", "%s %s" % ("The mock builder is not a support agent, so it has no customer to escalate.",
                                           cf("ts-5-2-d06", excerpt(D06, "The guide says that self-reported confidence scores are \"unreliable proxies for actual case complexity\" (5.2-K3), and sample question 3 in Section 9 uses such an option as a wrong option. So it is a fair wrong option.", "Mock decision 0006"),
                                              "But rule D3 of step 6 allows at most one wrong option on self-reported confidence in each scenario, and 5.2-K3 is why such an option is a fair wrong option.")))
            + ' <p><a href="%s#step-6">Step 6, Check the complete mock &rarr;</a></p>' % TAB2, "ts-5-2"))


# ----- part 5.3 (facts: academy/facts/ts-5-3.md) -----

FIG53 = figure("5.3-1", 890, 350,
               "A subagent runs a query. Results and a valid empty result are both successes. An access failure is first retried in the subagent. If it is not resolved, "
               "the subagent returns structured error context: the failure type, the query, the partial results and the alternatives. The coordinator decides to retry, change the plan "
               "or go on, and the synthesis marks the gaps.",
               "".join([edge("M190 165H220", cls="no-head"), '<path class="ve-e no-head" d="M220 47V200"/>',
                        edge("M220 47H250"), edge("M220 117H250"), edge("M220 200H250"),
                        edge("M360 230V250", "not resolved", 368, 243, anchor="r"),
                        '<path class="ve-e no-head" d="M470 47H510V285H470M470 117H510"/>',
                        edge("M510 145H540"), edge("M710 145H750"),
                        box(20, 130, 170, 70, ["Subagent", "runs a query"], cls="who-model"),
                        box(250, 20, 220, 55, ["Results"], sub="success", cls="try ok"),
                        box(250, 90, 220, 55, ["0 matches"], sub="success, not an error", cls="try ok"),
                        box(250, 170, 220, 60, ["Access failure"], sub="retry it locally first"),
                        box(250, 250, 220, 70, ["Error context"]),
                        '<text class="ve-lab" x="250" y="340">type, query, partial results, alternatives</text>',
                        box(540, 100, 170, 90, ["Coordinator"], sub="retry, change, go on", cls="who-model"),
                        box(750, 100, 120, 90, ["Synthesis"], sub="gaps marked")]),
               "%s %s" % (cf("ts-5-3-k1", gx("Structured error context (failure type, attempted query, partial results, alternative approaches) as enabling intelligent coordinator recovery decisions", "Exam guide, 5.3-K1"),
                             "Structured error context lets the coordinator decide how to recover (5.3-K1)."),
                          cf("ts-5-3-k2", gx("The distinction between access failures (timeouts needing retry decisions) and valid empty results (successful queries with no matches)", "Exam guide, 5.3-K2"),
                             "An access failure needs a decision, but an empty result is a success (5.3-K2).")))

PART["5.3"] = (overview("5.3", "A failed subagent reports what failed, never a silent empty",
                        "A subagent retries a transient failure itself. If it cannot fix it, it tells the coordinator the failure type, the query, the partial results and the alternatives, "
                        "so that the coordinator can retry, change the plan or go on with a marked gap.",
                        FIG53)
    + level("explanation",
            "<p><b>Error context.</b> %s %s %s</p>" % (
                cf("ts-5-3-s1", gx("Returning structured error context including failure type, what was attempted, partial results, and potential alternatives to enable coordinator recovery", "Exam guide, 5.3-S1"),
                   "The subagent returns the failure type, what it tried, its partial results and possible alternatives (5.3-S1)."),
                fact("ts-2-2-f6", "For an error of a client tool, the Claude API documentation also says to name what went wrong and what Claude should try next."),
                cf("ts-5-3-f4", D(SUB, "Either way, intermediate tool calls and results stay inside the subagent; only its final message returns to the parent.", "Agent SDK, Subagents"),
                   "In the Agent SDK, only the final message of a subagent returns to its parent, so put the error context in that message."))
            + "<p><b>Empty is not failure.</b> %s Only the guide states this point, also in 2.2.</p>" %
                cf("ts-5-3-s2", gx("Distinguishing access failures from valid empty results in error reporting so the coordinator can make appropriate decisions", "Exam guide, 5.3-S2"),
                   "The report keeps an access failure apart from a valid empty result (5.3-S2).")
            + "<p><b>Two anti-patterns.</b> %s %s %s</p>" % (
                cf("ts-5-3-k3", gx("Why generic error statuses (\"search unavailable\") hide valuable context from the coordinator", "Exam guide, 5.3-K3"),
                   "A generic status such as &ldquo;search unavailable&rdquo; hides the context (5.3-K3)."),
                cf("ts-5-3-k4", gx("Why silently suppressing errors (returning empty results as success) or terminating entire workflows on single failures are both anti-patterns", "Exam guide, 5.3-K4"),
                   "An error that looks like an empty success, and a whole workflow that stops on one failure, are both anti-patterns (5.3-K4)."),
                cf("ts-5-3-f9", D(MAO, "* **What to do when an agent fails:** \"One agent failing must not fail the run. If an agent fails to read a contract, list that contract as not covered.\"", "Managed Agents, Multiagent orchestration"),
                   "An example prompt of Managed Agents says the same: one failed agent must not fail the run."))
            + "<p><b>Recover locally, then mark the gaps.</b> %s %s %s</p>" % (
                cf("ts-5-3-s3", gx("Having subagents implement local recovery for transient failures and only propagate errors they cannot resolve, including what was attempted and partial results", "Exam guide, 5.3-S3"),
                   "A subagent recovers from a transient failure itself and passes on only what it cannot fix (5.3-S3)."),
                cf("ts-5-3-f11", D(CCS, "* **Foreground**: if a rate limit, overload, or server error cuts off a subagent that already produced text output, the Agent tool returns that partial output with a note that the subagent was cut off and didn't finish its task. A subagent that produced nothing, or whose only output was tool calls, fails with", "Claude Code, Subagents"),
                   "In Claude Code, when an API error cuts off a foreground subagent that already wrote text, the Agent tool returns that partial output with a note. A subagent with no text fails with an error."),
                cf("ts-5-3-s4", gx("Structuring synthesis output with coverage annotations indicating which findings are well-supported versus which topic areas have gaps due to unavailable sources", "Exam guide, 5.3-S4"),
                   "The synthesis marks which findings are well supported and which topics have gaps (5.3-S4)."))
            + exam_tests("5.3", [("Error handling and propagation: structured error responses, transient vs business vs permission errors, local recovery before escalation", "Among the topics, the guide names")])
            + "<p>%s %s</p>" % (cf("ts-5-3-q8", gx("Return structured error context to the coordinator including the failure type, the attempted query, any partial results, and potential alternative approaches.", "Exam guide, sample question 8"),
                               "Sample question 8 of the guide fits 5.3: its correct answer returns structured error context to the coordinator."),
                                cf("ts-5-3-q8b", gx("Option B's generic status hides valuable context from the coordinator, preventing informed decisions.", "Exam guide, sample question 8"),
                               "Option B retries, as 5.3-S3 teaches, but it is wrong because it ends with a generic status."))
            + guide_text("5.3"), "ts-5-3")
    + level("depth",
            beyond([cf("ts-5-3-b1", D(SUB, "An API error that ends the subagent early, such as a rate limit, is never delivered as its result.", "Agent SDK, Subagents"),
                       "In the Agent SDK, an API error that ends a subagent early is never delivered as its result, so it cannot look like an empty success."),
                    cf("ts-5-3-b2", D(HANDLE, "When server tools encounter errors (for example, network issues with Web Search), Claude will transparently handle these errors and attempt to provide an alternative response or explanation to the user.", "Handle tool calls"),
                       "Server tools of the Claude API, such as web search, handle their own errors.")])
            + code_pop_text("ts-5-3-code", "The code: a tool result that reports an error", "An error result", HANDLE, ERR22, "Handle tool calls",
                            "This example has the failure type only. A subagent of the guide puts the full error context in its final message.")
            + tab2_links("5.3") + "<p>%s %s</p>" % (cf("ts-5-3-use", excerpt(step_file(3), "Written for errors between agents. Here: an error must never look like a pass.", "Build guide, step 3"),
                                                    "Step 3 uses 5.3-K4: an error must never look like a pass."),
                                                 cf("ts-5-3-use6", excerpt(step_file(6), "Written for errors between agents. Here: a call that fails, or an answer that is not valid, never counts as a pass.", "Build guide, step 6"),
                                                    "Step 6 uses it too: a call that fails, or an answer that is not valid, never counts as a pass.")), "ts-5-3"))


# ----- part 5.4 (facts: academy/facts/ts-5-4.md) -----

MEMT, CTXW, CMDS = "anthropic-docs-memory-tool", "claude-code-docs-context-window", "claude-code-docs-commands"
D01 = glob.glob(os.path.join(ROOT, "docs/decisions/0001-*.md"))[0][len(ROOT) + 1:]
SUM54 = "\n".join(read(SRC % LOOP).split("\n")[283:290])
assert SUM54.strip().startswith("# Summary instructions") and SUM54.rstrip().endswith("reasoning behind them")
FIG54 = figure("5.4-1", 890, 330,
               "A main agent keeps the high-level view and sends specific questions, such as finding all test files, to subagents, which keep the verbose output and send back a summary. "
               "The main agent writes key findings to a scratchpad file and reads it for later questions. Each agent exports its state, and on resume the coordinator loads a manifest. "
               "When discovery output fills the context, /compact makes it smaller.",
               "".join(['<path class="ve-e no-head" d="M330 80H300V280"/>', edge("M300 200H270"), edge("M300 280H270"),
                        '<text class="ve-el" x="380" y="160">a question, then a summary back</text>',
                        edge("M560 50H620", "write", 590, 41), edge("M620 75H560", "read", 590, 92, cls="is-async"),
                        edge("M620 210H445V100", "load on resume", 532, 201, cls="is-hot"),
                        edge("M270 295H745V250", "agents export their state", 520, 287),
                        '<text class="ve-lab" x="330" y="125">context fills: /compact</text>',
                        box(330, 20, 230, 80, ["Main agent"], sub="high-level view", cls="who-model"),
                        box(20, 170, 250, 60, ["Subagent: test files"], sub="verbose output stays", cls="who-model"),
                        box(20, 250, 250, 60, ["Subagent: refund flow"], sub="verbose output stays", cls="who-model"),
                        box(620, 20, 250, 80, ["Scratchpad file"], sub="key findings"),
                        box(620, 170, 250, 80, ["Manifest"], sub="the state of each agent")]),
               "%s %s" % (cf("ts-5-4-s1", gx("Spawning subagents to investigate specific questions (e.g., \"find all test files,\" \"trace refund flow dependencies\") while the main agent preserves high-level coordination", "Exam guide, 5.4-S1"),
                             "Subagents investigate specific questions, while the main agent keeps the coordination (5.4-S1)."),
                          cf("ts-5-4-s2", gx("Having agents maintain scratchpad files recording key findings, referencing them for subsequent questions to counteract context degradation", "Exam guide, 5.4-S2"),
                             "Agents keep scratchpad files of key findings and read them for later questions (5.4-S2).")))

PART["5.4"] = (overview("5.4", "Keep findings in files, keep exploration in subagents",
                        "A long exploration fills the context, and then the answers get worse. Send verbose searches to subagents that return summaries, "
                        "write the key findings to files, and resume from those files, not from the old conversation.",
                        FIG54)
    + level("explanation",
            "<p><b>Degradation.</b> %s %s</p>" % (
                cf("ts-5-4-k1", gx("Context degradation in extended sessions: models start giving inconsistent answers and referencing \"typical patterns\" rather than specific classes discovered earlier", "Exam guide, 5.4-K1"),
                   "In a long session, the guide says, the answers get inconsistent and name &ldquo;typical patterns&rdquo; in place of the specific classes found earlier (5.4-K1)."),
                cf("ts-5-4-f2", D(BEST, "When the context window is getting full, Claude may start \"forgetting\" earlier instructions or making more mistakes.", "Claude Code, Best practices"),
                   "The Claude Code documentation says that, when the context window gets full, Claude may forget earlier instructions or make more mistakes."))
            + "<p><b>Scratchpad files.</b> %s %s</p>" % (
                cf("ts-5-4-k2", gx("The role of scratchpad files for persisting key findings across context boundaries", "Exam guide, 5.4-K2"),
                   "A scratchpad file keeps key findings across the limits of the context (5.4-K2)."),
                cf("ts-5-4-f4", D(MEMT, "Rather than loading all relevant information up front, an agent records what it learns in memory files and reads them back on demand.", "Memory tool"),
                   "The memory tool of the Claude API works the same way, with memory files. The words scratchpad file and manifest are the guide's."))
            + "<p><b>Subagents.</b> %s %s</p>" % (
                cf("ts-5-4-k3", gx("Subagent delegation for isolating verbose exploration output while the main agent coordinates high-level understanding", "Exam guide, 5.4-K3"),
                   "A subagent takes the verbose exploration, while the main agent keeps the high-level view (5.4-K3)."),
                fact("ts-2-5-b2", "In Claude Code, the Explore subagent keeps such a search out of the main context."))
            + "<p><b>Phases.</b> %s %s</p>" % (
                cf("ts-5-4-s3", gx("Summarizing key findings from one exploration phase before spawning sub-agents for the next phase, injecting summaries into initial context", "Exam guide, 5.4-S3"),
                   "The key findings of one phase go, as a summary, into the first context of the subagents of the next phase (5.4-S3),"),
                cf("ts-5-4-f5", D(SUB, "Unless the subagent is a [fork](/docs/en/sub-agents#fork-the-current-conversation), its context window starts fresh, with no parent conversation, but isn't empty. The only content you pass from parent to subagent is the Agent tool's prompt string", "Agent SDK, Subagents"),
                   "because, in the Agent SDK, the only content that a parent passes to a subagent that is not a fork is the prompt of the Agent tool."))
            + "<p><b>Crash recovery.</b> %s %s %s</p>" % (
                cf("ts-5-4-k4", gx("Structured state persistence for crash recovery: each agent exports state to a known location, and the coordinator loads a manifest on resume", "Exam guide, 5.4-K4"),
                   "Each agent exports its state to a known place, and on resume the coordinator loads a manifest (5.4-K4)."),
                cf("ts-5-4-s4", gx("Designing crash recovery using structured agent state exports (manifests) that the coordinator loads on resume and injects into agent prompts", "Exam guide, 5.4-S4"),
                   "The coordinator puts the manifest into the prompts of the agents (5.4-S4)."),
                cf("ts-5-4-f14", D(SES, "Sessions persist the **conversation**, not the filesystem.", "Agent SDK, Sessions"),
                   "A resumed session of the Agent SDK restores the conversation, not the files, so the manifest is a design of your own."))
            + "<p><b>/compact.</b> %s %s</p>" % (
                cf("ts-5-4-s5", gx("Using /compact to reduce context usage during extended exploration sessions when context fills with verbose discovery output", "Exam guide, 5.4-S5"),
                   "When discovery output fills the context, /compact makes it smaller (5.4-S5)."),
                cf("ts-5-4-f15", D(CMDS, "Free up context by summarizing the conversation so far.", "Claude Code, Commands"),
                   "In Claude Code, /compact summarizes the conversation so far."))
            + exam_tests("5.4", [("Subagent context management: explicit context passing, structured state persistence, crash recovery using manifests", "Among the topics, the guide names")])
            + guide_text("5.4"), "ts-5-4")
    + level("depth",
            beyond([cf("ts-5-4-b1", D(CTXW, "Path-scoped rules and nested CLAUDE.md files load into message history when Claude reads, writes, or edits their trigger file, so compaction summarizes them away with everything else.", "Claude Code, Explore the context window"),
                       "In Claude Code, path-scoped rules and nested CLAUDE.md files load when Claude reads, writes or edits their trigger file, so a compaction summarizes them away with everything else."),
                    cf("ts-5-4-b2", D(HOW, "To control what's preserved during compaction, add a \"Compact Instructions\" section to CLAUDE.md", "Claude Code, How Claude Code works"),
                       "In Claude Code, a &ldquo;Compact Instructions&rdquo; section of CLAUDE.md can tell the compaction what to keep."),
                    cf("ts-5-4-b3", D(MEMT, "For long-running agents, consider using both: compaction keeps the active context small without client-side bookkeeping, and memory preserves the information that must survive summarization.", "Memory tool"),
                       "For a long-running agent, the Claude API documentation suggests both: compaction keeps the context small, and memory keeps what must survive the summary.")])
            + code_pop_text("ts-5-4-code", "The code: what a summary must keep", "Summary instructions in CLAUDE.md", LOOP, SUM54, "Agent SDK, The agent loop",
                            "In the Agent SDK, this section of CLAUDE.md asks the compactor to keep the task, the files, the test results and the decisions.")
            + tab2_links("5.4", cf("ts-5-4-d01b", excerpt(D01, "Keep one file for each decision, one HTML file for each diagram and a journal.", "Mock decision 0001"),
                                   "Mock decision 0001 keeps one file for each decision, and a journal.") + " "
                         + cf("ts-5-4-d01", excerpt(D01, "5.4-K2, 5.4-K4, 5.6-K2", "Mock decision 0001"),
                                   "It links them to 5.4-K2 and 5.4-K4. Tab 2 shows them under 1.7.")
                         + ' <a href="%s#cc-1-7">The build in Claude Code, 1.7 &rarr;</a>' % TAB2), "ts-5-4"))

# ----- part 5.5 (facts: academy/facts/ts-5-5.md) -----

TRT, CMOD, DTST, RHAL = "anthropic-docs-ticket-routing", "anthropic-docs-content-moderation", "anthropic-docs-develop-tests", "anthropic-docs-reduce-hallucinations"
SCH55 = "\n".join(read(SRC % SOUTA).split("\n")[1549:1564])
assert SCH55.strip().startswith('"output_config": {') and '"confidence": {"type": "number"},' in SCH55 and SCH55.rstrip().endswith("}")
FIG55 = figure("5.5-1", 890, 360,
               "An extraction has a confidence score for each field. A review threshold, calibrated on a labeled validation set, routes it. "
               "Low confidence or a contradictory source goes to human review by priority. High confidence goes to automation, and a stratified random sample of it goes back to human review. "
               "Before review is cut, the accuracy is checked for each document type and field, because 97% overall can hide a weak segment.",
               "".join([edge("M220 160H260"),
                        edge("M350 120V40H640"), '<text class="ve-el" x="495" y="28">low confidence, or</text><text class="ve-el" x="495" y="58">a contradictory source</text>',
                        edge("M440 160H640", "high confidence", 540, 151, cls="is-hot"),
                        edge("M350 260V200", "calibrates", 358, 234, anchor="r"),
                        edge("M670 130V70", "stratified random sample", 678, 104, cls="is-async", anchor="r"),
                        edge("M670 250V190", "check each segment first", 678, 224, anchor="r"),
                        '<text class="ve-lab" x="600" y="345">97% overall can hide a weak segment</text>',
                        box(20, 120, 200, 80, ["Extraction"], sub="confidence per field", cls="who-model"),
                        box(260, 120, 180, 80, ["Review thresholds"], sub="calibrated"),
                        box(260, 260, 180, 60, ["Labeled set"], sub="validation"),
                        box(640, 10, 230, 60, ["Human review"], sub="by priority", cls="who-owner"),
                        box(640, 130, 230, 60, ["Automated"], sub="high confidence"),
                        box(640, 250, 230, 70, ["Accuracy by segment"], sub="document type and field")]),
               "%s %s" % (cf("ts-5-5-k3", gx("Field-level confidence scores calibrated using labeled validation sets for routing review attention", "Exam guide, 5.5-K3"),
                             "Confidence scores for each field, calibrated on labeled validation sets, route the review (5.5-K3)."),
                          cf("ts-5-5-k2", gx("Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns", "Exam guide, 5.5-K2"),
                             "A stratified random sample of the high-confidence extractions measures their error rate and finds new error patterns (5.5-K2).")))

PART["5.5"] = (overview("5.5", "Trust confidence scores only after labeled data calibrates them",
                        "One total accuracy can hide a weak document type or field, so measure each segment before you cut human review. "
                        "Route low-confidence extractions, and those from contradictory sources, to people, with thresholds set on labeled data, and keep a random sample of the confident ones under review.",
                        FIG55)
    + level("explanation",
            "<p><b>One total hides a weak part.</b> %s %s %s %s %s</p>" % (
                cf("ts-5-5-k1", gx("The risk that aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields", "Exam guide, 5.5-K1"),
                   "A total accuracy, such as 97% overall, can hide poor results on some document types or fields (5.5-K1)."),
                cf("ts-5-5-s2", gx("Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review", "Exam guide, 5.5-S2"),
                   "So check the accuracy for each document type and each field before you reduce human review (5.5-S2)."),
                cf("ts-5-5-k4", gx("The importance of validating accuracy by document type and field segment before automating high-confidence extractions", "Exam guide, 5.5-K4"),
                   "Do the same before you automate the high-confidence extractions (5.5-K4)."),
                cf("ts-5-5-f1", D(TRT, "Measure the routing accuracy across different languages, aiming for no more than a 5–10% drop in accuracy for non-primary languages.", "Ticket routing"),
                   "The ticket routing guide of the Claude API documentation measures the accuracy for each language,"),
                cf("ts-5-5-f2", D(TRT, "Regularly audit routing decisions for potential biases, aiming for consistent routing accuracy (within 2–3%) across all customer groups.", "Ticket routing"),
                   "and it aims for routing accuracy within 2 to 3% across all customer groups."))
            + "<p><b>A sample of the confident ones.</b> %s %s %s The word stratified is the guide&rsquo;s.</p>" % (
                cf("ts-5-5-s1", gx("Implementing stratified random sampling of high-confidence extractions for ongoing error rate measurement and novel pattern detection", "Exam guide, 5.5-S1"),
                   "A stratified random sample of the high-confidence extractions stays under review, to measure the error rate over time and to find new patterns (5.5-S1)."),
                cf("ts-5-5-f4", D(DTST, "Design evals that mirror your real-world task distribution.", "Define success criteria and build evaluations"),
                   "For tests, the evaluation page of the Claude API documentation asks for evaluations that mirror the real mix of tasks."),
                cf("ts-5-5-f5", D(CMOD, "Keep track of the types of content being flagged by your moderation system to identify trends and potential areas for improvement.", "Content moderation"),
                   "The content moderation guide of the Claude API tracks the types of content that the system flags, to find trends."))
            + "<p><b>Calibrate the confidence.</b> %s %s %s No page in the copies of this academy describes the calibration of field-level confidence.</p>" % (
                cf("ts-5-5-s3", gx("Having models output field-level confidence scores, then calibrating review thresholds using labeled validation sets", "Exam guide, 5.5-S3"),
                   "The model outputs a confidence score for each field, and a labeled validation set calibrates the review thresholds (5.5-S3)."),
                cf("ts-5-5-f8", gx("Option B fails because LLM self-reported confidence is poorly calibrated—the agent is already incorrectly confident on hard cases.", "Exam guide, sample question 3"),
                   "In sample question 3, which is about escalation, the guide says that a self-reported confidence is poorly calibrated."),
                cf("ts-5-5-f6", D(DTST, "**Example eval test cases:** 1,000 tweets with human-labeled sentiments.", "Define success criteria and build evaluations"),
                   "The evaluation page of the Claude API documentation gives an example test set: 1,000 tweets with sentiments that people labeled."))
            + "<p><b>People get the hard cases.</b> %s %s %s</p>" % (
                cf("ts-5-5-s4", gx("Routing extractions with low model confidence or ambiguous/contradictory source documents to human review, prioritizing limited reviewer capacity", "Exam guide, 5.5-S4"),
                   "Extractions with low confidence, or with ambiguous or contradictory sources, go to human review, which gives its limited time to the most important first (5.5-S4)."),
                cf("ts-5-5-f10", D(CMOD, "For example, you might want to automatically block user queries that are deemed high risk, while users with many medium risk queries are flagged for human review.", "Content moderation"),
                   "The content moderation guide of the Claude API gives an example: block high-risk queries automatically, and flag users with many medium-risk queries for human review."),
                cf("ts-5-5-f12", D(RHAL, "Explicitly give Claude permission to admit uncertainty.", "Reduce hallucinations"),
                   "The Reduce hallucinations page of the Claude API documentation also tells you to let Claude admit uncertainty."))
            + exam_tests("5.5", [("Human review workflows: confidence calibration, stratified sampling, accuracy segmentation by document type and field", "Among the topics, the guide names")])
            + guide_text("5.5"), "ts-5-5")
    + level("depth",
            beyond([cf("ts-5-5-b1", D(DTST, "**Human grading:** Most flexible and high quality, but slow and expensive. Avoid if possible.", "Define success criteria and build evaluations"),
                       "For evaluations, the Claude API documentation calls human grading slow and expensive. That is about tests before production.")
                    + " " + fact("ts-5-5-s4", "In production, the guide keeps people on the hard cases (5.5-S4)."),
                    cf("ts-5-5-b2", D(TRT, "Measure this by periodically testing the model with a set of standardized inputs and aiming for a consistency rate of 95% or higher.", "Ticket routing"),
                       "The ticket routing guide tests the model again from time to time with a fixed set of inputs."),
                    cf("ts-5-5-b3", D(CMOD, "Regularly assess the performance of your content moderation system using metrics such as precision and recall tracking.", "Content moderation"),
                       "The content moderation guide measures precision and recall, not only accuracy.")])
            + code_pop_text("ts-5-5-code", "The code: a confidence score in a schema", "A confidence field in a structured output", SOUTA, SCH55, "Structured outputs",
                            "This example has one score for the whole answer. For 5.5, put one score on each field. The model writes the number, so it is not calibrated until you compare it with a labeled set.")
            + tab2_links("5.5") + "<p>%s %s</p>" % (
                cf("ts-5-5-use", excerpt(step_file(7), "Written for the extraction of data. Here: the bad marks are shown for each scenario and each domain, because one total can hide a bad part.", "Build guide, step 7"),
                   "Step 7 uses 5.5 outside its context. The bad marks are shown for each scenario and each domain, because one total can hide a bad part (5.5-K1)."),
                cf("ts-5-5-c3", excerpt(step_file(7), "For mocks 4 and 5 it is the second review in Cowork, also a Claude model", "Build guide, step 7"),
                   "In mocks 4 and 5, the reader is a Claude model, not a person.")), "ts-5-5"))

# ----- part 5.6 (facts: academy/facts/ts-5-6.md) -----

CIT, SRES = "anthropic-docs-citations", "anthropic-docs-search-results"
SR56 = "\n".join(read(SRC % SRES).split("\n")[28:44])
assert SR56.startswith("{") and SR56.rstrip().endswith("}") and '"type": "search_result",' in SR56
FIG56 = figure("5.6-1", 890, 380,
               "Subagents return each finding as a record with a claim, an evidence excerpt, a source and a publication date, with conflicting values annotated. The coordinator decides how to reconcile them, "
               "and the synthesis agent merges the records. The report has sections for well-established findings, contested findings with both values, and coverage gaps. "
               "A summary without sources loses the attribution. Picking one value, or a finding with no date, is wrong. Each content type keeps its own format.",
               "".join(['<text class="ve-lab" x="240" y="12">one finding</text>',
                        edge("M200 75H240"), edge("M470 75H520"), edge("M680 75H720"), edge("M795 130V180"),
                        edge("M110 120V200", "compressed", 118, 165, anchor="r"),
                        '<text class="ve-lab" x="250" y="215">Wrong: pick one value</text>',
                        '<text class="ve-lab" x="250" y="245">Wrong: no date, so an older</text>',
                        '<text class="ve-lab" x="250" y="265">figure looks like a contradiction</text>',
                        '<text class="ve-lab" x="20" y="320">Format by content type:</text>',
                        '<text class="ve-lab" x="20" y="342">financial data as tables, news as</text>',
                        '<text class="ve-lab" x="20" y="362">prose, technical findings as lists</text>',
                        box(20, 30, 180, 90, ["Subagents"], sub="search, analysis", cls="who-model"),
                        box(240, 20, 230, 110, ["claim", "evidence excerpt", "source URL or name", "publication date"], sub="conflicts annotated"),
                        box(520, 20, 160, 110, ["Coordinator"], cls="who-model"),
                        '<text class="ve-lab" x="520" y="150">decides how to reconcile</text>',
                        box(720, 20, 150, 110, ["Synthesis"], sub="merges records", cls="who-model"),
                        box(20, 200, 200, 60, ["Summary only"], sub="sources lost", cls="try bad"),
                        '<text class="ve-lab" x="520" y="174">Report</text>',
                        box(520, 180, 350, 45, ["Well-established"]),
                        box(520, 235, 350, 55, ["Contested"], sub="both values, each with its source", cls="try ok"),
                        box(520, 300, 350, 45, ["Coverage gaps"], sub="a point of 5.3-S4")]),
               "%s %s" % (cf("ts-5-6-s1", gx("Requiring subagents to output structured claim-source mappings (source URLs, document names, relevant excerpts) that downstream agents preserve through synthesis", "Exam guide, 5.6-S1"),
                             "Subagents output structured claim-source mappings, and the agents after them keep the mappings through the synthesis (5.6-S1)."),
                          cf("ts-5-6-s2", gx("Structuring reports with explicit sections distinguishing well-established findings from contested ones, preserving original source characterizations and methodological context", "Exam guide, 5.6-S2"),
                             "The report has separate sections for well-established and for contested findings (5.6-S2).")))

PART["5.6"] = (overview("5.6", "Each claim keeps its source, date and conflicts",
                        "Each subagent returns its findings as structured records: the claim, the excerpt, the source and the date. "
                        "The synthesis keeps these records, shows both values when credible sources disagree, and separates settled findings from contested ones.",
                        FIG56)
    + level("explanation",
            "<p><b>A summary loses sources.</b> %s %s</p>" % (
                cf("ts-5-6-k1", gx("How source attribution is lost during summarization steps when findings are compressed without preserving claim-source mappings", "Exam guide, 5.6-K1"),
                   "When a summary compresses findings and drops the claim-source mappings, the attribution is lost (5.6-K1)."),
                cf("ts-5-6-f1", D(SUB, "Either way, intermediate tool calls and results stay inside the subagent; only its final message returns to the parent. A `research-assistant` subagent can explore dozens of files without any of that content accumulating in the main conversation. The parent receives a concise summary, not every file the subagent read.", "Agent SDK, Subagents"),
                   "In the Agent SDK, only the final message of a subagent returns to its parent, as a concise summary. A source outside that message is lost."))
            + "<p><b>Keep the mapping.</b> %s %s</p>" % (
                cf("ts-5-6-k2", gx("The importance of structured claim-source mappings that the synthesis agent must preserve and merge when combining findings", "Exam guide, 5.6-K2"),
                   "The synthesis agent must keep and merge structured claim-source mappings (5.6-K2)."),
                cf("ts-5-6-f2", gx("Design structured output for subagents that separates content from metadata: each finding should include a claim, evidence excerpt, source URL/document name, and publication date.", "Exam guide, exercise 4"),
                   "An exercise of the guide names the fields of one finding: a claim, an evidence excerpt, a source URL or document name, and a publication date."))
            + "<p><b>The API can carry the source.</b> %s %s %s</p>" % (
                cf("ts-5-6-f4", D(CIT, "Responses may now include multiple text blocks where each text block can contain a claim that Claude is making and a list of citations that support the claim.", "Citations"),
                   "With citations on, each text block of a Claude API response can hold a claim and its citations."),
                cf("ts-5-6-f6", D(SRES, "Search result content blocks let Claude cite your own content the same way it cites web search results: each citation carries the source and title you provided.", "Search results"),
                   "Search result blocks of the Claude API, on all active models except Claude Haiku 3, carry your source and title into citations."),
                cf("ts-5-6-f8", D(RHAL, "Make Claude's response auditable by having it cite quotes and sources for each of its claims. You can also have Claude verify each claim by finding a supporting quote after it generates a response. If it can't find a quote, it must retract the claim.", "Reduce hallucinations"),
                   "Prompt advice of the Claude API documentation: have Claude cite a quote and a source for each claim, and retract a claim with no quote."))
            + "<p><b>Conflicts and dates.</b> %s %s %s %s %s No copied page of the documentation covers conflicting values or dates. These rules are the guide&rsquo;s.</p>" % (
                cf("ts-5-6-k3", gx("How to handle conflicting statistics from credible sources: annotating conflicts with source attribution rather than arbitrarily selecting one value", "Exam guide, 5.6-K3"),
                   "When credible sources give different statistics, annotate the conflict with the sources, and do not select one value arbitrarily (5.6-K3)."),
                cf("ts-5-6-s3", gx("Completing document analysis with conflicting values included and explicitly annotated, letting the coordinator decide how to reconcile before passing to synthesis", "Exam guide, 5.6-S3"),
                   "The document analysis ends with both values, annotated, and the coordinator decides how to reconcile them before the synthesis (5.6-S3)."),
                cf("ts-5-6-f9", gx("Test with conflicting source data (e.g., two credible sources with different statistics) and verify the synthesis output preserves both values with source attribution rather than arbitrarily selecting one, and structures the report to distinguish well-established from contested findings.", "Exam guide, exercise 4"),
                   "The guide&rsquo;s exercise checks that the synthesis keeps both values with their sources."),
                cf("ts-5-6-k4", gx("Temporal data: requiring publication/collection dates in structured outputs to prevent temporal differences from being misinterpreted as contradictions", "Exam guide, 5.6-K4"),
                   "A publication or collection date in the structured output stops a difference in time from looking like a contradiction (5.6-K4)."),
                cf("ts-5-6-s4", gx("Requiring subagents to include publication or data collection dates in structured outputs to enable correct temporal interpretation", "Exam guide, 5.6-S4"),
                   "So the subagents must include these dates (5.6-S4)."))
            + "<p><b>The report.</b> %s %s</p>" % (fact("ts-5-6-s2", "The report keeps the original characterizations and methods of the sources (5.6-S2),"), 
                cf("ts-5-6-s5", gx("Rendering different content types appropriately in synthesis outputs—financial data as tables, news as prose, technical findings as structured lists—rather than converting everything to a uniform format", "Exam guide, 5.6-S5"),
                   "and it gives each content type its format: financial data as tables, news as prose, technical findings as lists (5.6-S5)."))
            + exam_tests("5.6", [("Information provenance: claim-source mappings, temporal data handling, conflict annotation, coverage gap reporting", "Among the topics, the guide names")])
            + guide_text("5.6"), "ts-5-6")
    + level("depth",
            beyond([cf("ts-5-6-b1", D(CIT, "If you enable citations on any user-provided document (`document` blocks or `search_result` blocks) and also include the `output_config.format` parameter (or the deprecated `output_format` parameter), the API returns a 400 error.", "Citations"),
                       "In the Claude API, citations and the structured outputs of output_config.format do not work in one request: the API returns a 400 error.")
                    + " " + fact("ts-5-6-s4", "The guide asks for dates in structured outputs (5.6-S4),") + " "
                    + cf("ts-5-6-g1036", gx("Structured output via tool_use: schema design, tool_choice configuration, nullable fields to prevent hallucination", "Exam guide, section 17"),
                         "and it names structured output through tool_use.") + " This academy did not check whether citations work with a forced tool call.",
                    cf("ts-5-6-b2", D(CIT, "As image citations are not yet supported, PDFs that are scans of documents and do not contain extractable text are not citable.", "Citations"),
                       "Citations of the Claude API do not work for a scanned PDF with no extractable text."),
                    cf("ts-5-6-b3", D(SRES, "The text block is the minimal citable unit: Claude cites whole blocks, not substrings within a block.", "Search results"),
                       "In search result blocks of the Claude API, Claude cites a whole text block, not a part of a block.")])
            + code_pop_text("ts-5-6-code", "The code: a search result that carries its source", "A search result block", SRES, SR56, "Search results",
                            "In the Claude API, the source and the title come back in each citation. All active models except Claude Haiku 3 support it. The example has no date field, and 5.6-S4 asks for one.")
            + tab2_links("5.6") + "<p>%s %s</p>" % (
                cf("ts-5-6-use", excerpt(step_file(0), "Written for the synthesis of findings. Here: the records keep the exact guide text, so no summary loses the source.", "Build guide, step 0"),
                   "Step 0 uses 5.6-K1 outside its context: each guide record keeps the exact text of the guide, so no summary loses the source."),
                cf("ts-5-6-code0", excerpt("src/step0_prepare_guide_records.py", "need(text and text in raw, \"text is not exactly in the guide: \" + text[:60])", "Mock builder code, src/step0_prepare_guide_records.py"),
                   "The code stops when the text of a record is not exactly in the guide.")), "ts-5-6"))

# ----- the top: the map and how we broke it down -----

CARD.update({
    "m-what": gx("This guide is the authoritative reference for candidates preparing to sit the exam. It describes the exam content, lists the domains and task statements tested, provides sample questions, and recommends preparation strategies.", "Exam guide, section 1"),
    "m-items": gx("| Number of items | 60 |", "Exam guide, section 3"),
    "m-format": gx("| Item format | Multiple-choice and multiple-response items; each item states how many responses to select |", "Exam guide, section 3"),
    "m-struct": gx("| Exam structure | 4 scenarios drawn from a bank of 6 |", "Exam guide, section 3"),
    "m-weights": gx("The percentages indicate the approximate proportion of scored items drawn from each domain.", "Exam guide, section 4"),
    "m-report": gx("| Result reporting | Pass/fail with scaled score (100–1,000), plus percent-correct by domain on the score report |", "Exam guide, section 3"),
})
for d in DOM.values():
    CARD["m-d%d" % d["id"]] = gx("| %d | %s | %d%% |" % (d["id"], d["name"], d["weight"]), "Exam guide, section 4, domain %d" % d["id"])
for s in SCEN:
    _eg = read(EG)
    _i = _eg.index("### Scenario %d: %s" % (s["id"], s["name"]))
    _j = _eg.index("\n", _eg.index("Primary domains:", _i))
    CARD["m-s%d" % s["id"]] = gx(_eg[_i:_j], "Exam guide, section 5, scenario %d" % s["id"])


def map_col(d):
    lis = "".join('<li><a href="#ts-%s"><span class="pid">%s</span> %s</a></li>' % (t.replace(".", "-"), t, e(TAKEAWAY.get(t, TS[t]["title"])))
                  for t in sorted(TS, key=lambda x: (int(x.split(".")[0]), int(x.split(".")[1]))) if TS[t]["domain"] == d["id"])
    return ('<div class="tcol"><p class="ve-label"><a href="#domain-%d">Domain %d</a></p><p class="tname">%s</p>'
            '<div class="tbar" role="img" aria-label="Weight %d%%"><span style="width:%d%%"></span></div><p class="tw">%s</p><ol class="tlist">%s</ol></div>'
            % (d["id"], d["id"], e(d["name"]), d["weight"], d["weight"] * 3, fact("m-d%d" % d["id"], "%d%%" % d["weight"]), lis))


def scen_row(s):
    return ('<li><span class="sn">%d</span>%s <span class="ve-label">primary domains %s</span></li>'
            % (s["id"], fact("m-s%d" % s["id"], e(s["name"])), ", ".join(str(x) for x in sorted(s["primary_domains"]))))


def map_html():
    return """<section class="parts" id="map" aria-label="The map of the exam guide">
  <h2>The exam guide on one page</h2>
  <p>%(what)s %(items)s, %(format)s %(struct)s</p>
  <figure data-figure="map">
    <div class="tmap">%(cols)s</div>
    <figcaption><span class="fig-n">Fig. A</span>The 5 domains of the guide, with their %(nts)d task statements. %(weights)s A task statement that this page has written shows its takeaway heading. The others show the title of the guide. Each task statement opens below.</figcaption>
  </figure>
  <figure>
    <ol class="scen">%(scen)s</ol>
    <figcaption><span class="fig-n">Fig. B</span>%(scap)s</figcaption>
  </figure>
</section>""" % {"what": fact("m-what", "The exam guide is the official reference for the CCAR-F exam: it lists the domains and the task statements that the exam tests."),
                 "items": fact("m-items", "The exam has 60 questions"),
                 "format": fact("m-format", "and each question states how many answers to select."),
                 "struct": fact("m-struct", "Each exam uses 4 of the 6 scenarios of the guide."),
                 "cols": "".join(map_col(DOM[i]) for i in range(1, 6)), "nts": len(TS),
                 "weights": fact("m-weights", "A weight is the approximate share of the scored questions."),
                 "scen": "".join(scen_row(s) for s in SCEN),
                 "scap": "The 6 scenarios of the guide, each with its primary domains."}


BREAKDOWN = """<section class="parts" id="breakdown" aria-label="How we broke it down">
  <h2>How we broke it down</h2>
  <p>The guide gives each task statement two lists of points: &ldquo;Knowledge of&rdquo; and &ldquo;Skills in&rdquo;. %(count)s</p>
  <p class="key"><span class="tag-k">K = Knowledge of</span><span class="tag-s">S = Skills in</span><span>%(lab)s = domain 1 &middot; task statement 1.1 &middot; Knowledge of, point 2. The labels are ours. The guide has no labels.</span></p>
  <p>Each task statement opens in three levels: the <b>Overview</b> (about 30 seconds), the <b>Explanation</b> (about 3 minutes), with the guide&rsquo;s own text and what the exam tests, and the <b>Depth</b>, with facts beyond the exam, code in popups, and the steps of the mock builder (the program that wrote the mocks of this academy, see tab 2) and of its build in Claude Code that use the task statement.</p>
</section>""" % {"lab": lab("1.1-K2"), "count": fact("m-count", "The guide has %d task statements with %d points: %d Knowledge of and %d Skills in." % (len(TS), N_PTS, N_K, N_S))}
CARD["m-count"] = {"title": "The exam guide as records", "kind": "count",
                   "text": "reference/guide-records.json has %d task statements and %d points: %d of kind knowledge and %d of kind skill. The script of this page counted them." % (len(TS), N_PTS, N_K, N_S),
                   "src": "reference/guide-records.json", "href": link("reference/guide-records.json")}

DOMAIN_SUMMARY = {}   # domain -> one or two sentences, written from the titles of its task statements (decision 0021)
DOMAIN_SUMMARY[5] = ("Reliable systems over long work: context that keeps the facts, escalation and ambiguity, errors that travel between agents, "
                     "context in large codebases, human review with calibrated confidence, and the provenance of each claim.")
DOMAIN_SUMMARY[4] = ("Prompts that give reliable output: explicit criteria, few-shot examples, structured output with tool use and JSON schemas, "
                     "validation with retries, batch processing, and reviews by several instances or passes.")
DOMAIN_SUMMARY[3] = ("Claude Code for a team: CLAUDE.md files and their levels, commands and skills, rules for some paths, "
                     "plan mode against direct work, refinement step by step, and Claude Code in a CI/CD pipeline.")
DOMAIN_SUMMARY[2] = ("Tools that Claude can use well: descriptions that make the choice clear, errors that say what went wrong, "
                     "the right tools for each agent and the choice of tool_choice, MCP servers, and the built-in tools of Claude Code.")
DOMAIN_SUMMARY[1] = ("Agents that run themselves: the loop of tool calls, a coordinator with subagents and what each subagent gets, "
                     "workflows with enforced steps and handoffs, hooks of the Agent SDK, how to split a task, and sessions that resume or fork.")


def domain_html(d):
    ts = sorted((t for t in TS if TS[t]["domain"] == d["id"]), key=lambda x: int(x.split(".")[1]))
    summ = DOMAIN_SUMMARY.get(d["id"], "")
    return ('<section class="parts" id="domain-%d" aria-label="Domain %d"><h2>Domain %d: %s</h2>'
            '<p class="ve-label">%s of the scored questions &middot; %d task statements</p>%s%s</section>'
            % (d["id"], d["id"], d["id"], e(d["name"]), fact("m-d%d" % d["id"], "about %d%%" % d["weight"]), len(ts),
               "<p>%s</p>" % summ if summ else "", "".join(ts_part(t) for t in ts)))


TITLE = "Exam guide breakdown"
BODY = """<main>
<header id="top">
  <nav class="tabs" aria-label="Tabs"><span aria-current="page">Exam guide breakdown</span><a href="%(tab2)s">Behind the mocks</a></nav>
  <h1>%(title)s</h1>
  <p class="lead">The CCAR-F exam guide, broken down into its 5 domains and %(nts)d task statements. Each task statement opens in three levels: a short answer, an explanation with the guide&rsquo;s own text, and facts beyond the exam.</p>
</header>
%(map)s
%(breakdown)s
%(domains)s
</main>""" % {"tab2": TAB2, "title": e(TITLE), "nts": len(TS), "map": map_html(), "breakdown": BREAKDOWN,
             "domains": "".join(domain_html(DOM[i]) for i in range(1, 6))}

BODY = re.sub(r'<svg class="(ve-svg|ve-bars)" viewBox="0 (\d+) (\d+) ', lambda m: '<svg class="%s" style="min-width:%spx" viewBox="0 %s %s ' % (m.group(1), m.group(3), m.group(2), m.group(3)), BODY)
USED = set(re.findall(r'data-card="([^"]+)"', BODY))
assert USED <= set(CARD), USED - set(CARD)
CARD = {k: v for k, v in CARD.items() if k in USED}
POP = {k: v for k, v in POP.items() if 'data-step="%s"' % k in BODY}
for k, v in POP.items():
    v.setdefault("example", None)

write("exam-guide-breakdown.html", page("Exam guide breakdown: the CCAR-F exam guide, task statement by task statement", BODY,
                                        "exam-guide-breakdown.js", "The CCAR-F exam guide in 5 domains and 30 task statements, each in three levels."))
script_file("exam-guide-breakdown.js", POP, CARD)
print("Wrote academy/pages/exam-guide-breakdown.html and exam-guide-breakdown.js: %d preview cards, %d popups, %d of %d task statements written."
      % (len(CARD), len(POP), len(PART), len(TS)))
