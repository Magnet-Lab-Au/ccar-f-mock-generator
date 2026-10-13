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
    return fact(key, "Of the %d questions in the 5 mocks of this academy, %d test its points." % (len(QUESTIONS), ON_TS[tsid]))


def tab2_links(tsid, why=""):
    """The links to each step of tab 2 that uses a point of the task statement (decisions 0010 and 0024)."""
    rows = []
    for n, pts in sorted(USES.get(tsid, {}).items()):
        rows.append('<li><a href="%s#step-%d">Step %d, %s &rarr;</a> <span class="ve-label">uses %s</span></li>'
                    % (TAB2, n, n, e(STEP_NAME[n]), ", ".join(pts)))
    if tsid in CC_PART:
        rows.append('<li><a href="%s#%s">The build in Claude Code, %s &rarr;</a></li>' % (TAB2, CC_PART[tsid], tsid))
    if rows:
        return '<h4 class="gh2">In the mock builder</h4><ul class="tolinks">%s</ul>' % "".join(rows)
    return '<h4 class="gh2">In the mock builder</h4><p>No step of the mock builder uses a point of %s. %s</p>' % (tsid, why)


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
        out.append("%s %s" % (what, fact(card("ts-%s-x%d" % (k, i), gx(text, "Exam guide, section 17")), "&ldquo;%s&rdquo;." % e(text))))
    return '<div><h4 class="gh2">The exam tests</h4><p>%s %s</p></div>' % (" ".join(out), mock_count(tsid))


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
                   "Step 3 has the nearest idea: a rule with one exact answer is checked by code (task statement 1.4)."))), "ts-1-5"))


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
                   "Step 1 takes only one idea of 1.6: the work of a mock is known before it starts, so code fixes the plan first."), cf("ts-1-6-rev", excerpt("docs/reviews/review-decisions-0003-to-0018.md", "A list of 60 slots made by code for a generation task is neither a review nor a prompt chain.", "Review of mock decisions 0003 to 0018"),
                   "It is not a prompt chain.")), "ts-1-6"))


# ----- part 2.1 (facts: academy/facts/ts-2-1.md) -----

DEFT, OVT, TRB, TSR, CCMCP = "anthropic-docs-define-tools", "anthropic-docs-tool-use-overview", "anthropic-docs-troubleshooting-tool-use", "anthropic-docs-tool-search-tool", "claude-code-docs-mcp"
D40 = glob.glob(os.path.join(ROOT, "docs/decisions/0040-*.md"))[0][len(ROOT) + 1:]
GOOD21 = "\n".join(read(SRC % DEFT).split("\n")[92:106])
assert GOOD21.strip().startswith("{") and '"name": "get_stock_price"' in GOOD21 and GOOD21.rstrip().endswith("}")
FIG21 = figure("2.1-1", 890, 270,
               "Before: a request to summarize a web page can go to analyze_content or to analyze_document, because both say only that they analyze content. "
               "After: analyze_content is renamed extract_web_results with a web-specific description, and analyze_document is split into tools with contracts, so the request has one clear tool.",
               "".join(['<text class="ve-lab" x="20" y="24">Before: near-identical descriptions</text>',
                        '<text class="ve-lab" x="480" y="24">After: renamed and split</text>',
                        '<path class="ve-e no-head is-async" d="M455 10V260"/>',
                        edge("M190 130H220V90H250", cls="is-async"), edge("M190 150H220V190H250", cls="is-async"),
                        '<text class="ve-el" x="130" y="215">which one?</text>',
                        edge("M620 140H635V70H650", cls="is-hot"),
                        box(20, 110, 170, 60, ["Summarize", "this web page"], cls="who-model"),
                        box(250, 60, 190, 60, ["analyze_content"], sub="analyzes content"),
                        box(250, 160, 190, 60, ["analyze_document"], sub="analyzes content"),
                        box(480, 110, 140, 60, ["Summarize", "this web page"], cls="who-model"),
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
            "<p><b>The description chooses.</b> %s %s %s</p>" % (
                cf("ts-2-1-k1", gx("Tool descriptions as the primary mechanism LLMs use for tool selection; minimal descriptions lead to unreliable selection among similar tools", "Exam guide, 2.1-K1"),
                   "The guide calls the description the primary mechanism of tool selection, and a minimal description makes the choice among similar tools unreliable (2.1-K1)."),
                cf("ts-2-1-f2", D(DEFT, "**Provide extremely detailed descriptions.** This is by far the most important factor in tool performance.", "Define tools"),
                   "The documentation calls a detailed description by far the most important factor in tool performance."),
                cf("ts-2-1-f3", D(DEFT, "The poor description is too brief and leaves Claude with many open questions about the tool's behavior and usage.", "Define tools"),
                   "A short description leaves Claude with open questions."))
            + "<p><b>What it holds.</b> %s %s %s</p>" % (
                cf("ts-2-1-k2", gx("The importance of including input formats, example queries, edge cases, and boundary explanations in tool descriptions", "Exam guide, 2.1-K2"),
                   "The guide puts input formats, example queries, edge cases and boundaries in the description (2.1-K2, 2.1-S1)."),
                cf("ts-2-1-f5", D(DEFT, "Aim for at least 3–4 sentences for each tool description, more if the tool is complex.", "Define tools"),
                   "The documentation asks for at least 3 or 4 sentences for each tool."),
                cf("ts-2-1-c3", D(DEFT, "you can use the `input_examples` field to provide schema-validated examples.", "Define tools"),
                   "It gives example inputs their own field, input_examples. The exam uses the guide."))
            + "<p><b>Overlap.</b> %s %s %s</p>" % (
                cf("ts-2-1-k3", gx("How ambiguous or overlapping tool descriptions cause misrouting (e.g., analyze_content vs analyze_document with near-identical descriptions)", "Exam guide, 2.1-K3"),
                   "Two tools with near-identical descriptions cause misrouting (2.1-K3)."),
                cf("ts-2-1-f7", D(TRB, "Sharpen descriptions. Differentiate tools by WHEN to use them, not only WHAT they do.", "Troubleshooting tool use"),
                   "The documentation says to separate tools by when to use them, not only by what they do."),
                cf("ts-2-1-f9", D(DEFT, "This makes tool selection unambiguous as your library grows", "Define tools"),
                   "Names with a prefix for each service also make the choice unambiguous."))
            + "<p><b>Split or join.</b> %s %s</p>" % (
                cf("ts-2-1-s3", gx("Splitting generic tools into purpose-specific tools with defined input/output contracts (e.g., splitting a generic analyze_document into extract_data_points, summarize_content, and verify_claim_against_source)", "Exam guide, 2.1-S3"),
                   "The guide splits a generic tool into tools with one purpose and a defined input and output each, for example analyze_document into extract_data_points, summarize_content and verify_claim_against_source (2.1-S3)."),
                cf("ts-2-1-c1", D(DEFT, "**Consolidate related operations into fewer tools.**", "Define tools"),
                   "The documentation also advises to join related actions into fewer tools. Both can hold: split a tool that does different jobs, join the actions on one resource. The guide names both, and the exam uses the guide."))
            + "<p><b>The system prompt.</b> %s %s %s</p>" % (
                cf("ts-2-1-f11", D(DEFT, "the API constructs a special system prompt from the tool definitions, tool configuration, and any user-specified system prompt.", "Define tools"),
                   "Claude reads the tool definitions and your system prompt in one prompt."),
                cf("ts-2-1-k4", gx("The impact of system prompt wording on tool selection: keyword-sensitive instructions can create unintended tool associations", "Exam guide, 2.1-K4"),
                   "So the wording of the system prompt can tie a keyword to the wrong tool, and you review the prompt for such words (2.1-K4, 2.1-S4)."),
                cf("ts-2-1-f13", D(PBP, "The fix is to dial back any aggressive language.", "Prompting best practices"),
                   "The documentation warns that aggressive words in a prompt make current models call a tool too often."))
            + exam_tests("2.1", [("Tool interface design: writing effective tool descriptions, splitting vs consolidating tools, tool naming to reduce ambiguity", "Among the topics, the guide names")])
            + "<p>%s</p>" % cf("ts-2-1-q2", gx("Expand each tool's description to include input formats it handles, example queries, edge cases, and boundaries explaining when to use it versus similar tools.", "Exam guide, sample question 2, answer B"),
                               "Sample question 2 of the guide tests 2.1: its correct answer expands each description.")
            + guide_text("2.1"), "ts-2-1")
    + level("depth",
            beyond([cf("ts-2-1-b1", D(CCMCP, "Claude Code truncates each tool description and each server's instructions at 2,048 characters by default.", "Claude Code, MCP"),
                       "Claude Code cuts each MCP tool description at 2,048 characters by default, so the important details go first."),
                    cf("ts-2-1-b2", D(TSR, "Claude's ability to pick the right tool degrades once you exceed 30–50 available tools.", "Tool search tool"),
                       "Above 30 to 50 tools, the choice degrades, also with good descriptions.")])
            + code_pop_text("ts-2-1-code", "The code: a good tool description", "A tool definition with a detailed description", DEFT, GOOD21, "Define tools",
                            "The description says what the tool returns, when to use it, and what it does not provide.")
            + tab2_links("2.1", cf("ts-2-1-d40", excerpt(D40, "The fields `name` and `description` of the tool are not sent as a tool.", "Mock decision 0040"),
                                   "The mock builder sends the model no tool: its forms go as structured outputs, so Claude never chooses a tool.")), "ts-2-1"))


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
                        box(540, 150, 330, 50, ["transient"], sub="retry in the subagent, then pass up"),
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
                   "A tool of the Agent SDK sets isError to true, so Claude can react to the failure."),
                cf("ts-2-2-f1", D(HANDLE, "`is_error` (optional): Set to `true` if the tool execution resulted in an error.", "Handle tool calls"),
                   "In the Claude API, the same flag is is_error on the tool result."))
            + "<p><b>Say what failed.</b> %s %s %s</p>" % (
                cf("ts-2-2-k3", gx("Why uniform error responses (generic \"Operation failed\") prevent the agent from making appropriate recovery decisions", "Exam guide, 2.2-K3"),
                   "A generic &ldquo;Operation failed&rdquo; leaves the agent with no basis to decide how to recover (2.2-K3)."),
                cf("ts-2-2-f6", D(HANDLE, "Instead of generic errors like `\"failed\"`, include what went wrong and what Claude should try next", "Handle tool calls"),
                   "The documentation agrees: say what went wrong and what Claude should try next."),
                cf("ts-2-2-f7", D(SDKT, "In both cases Claude can retry, try a different tool, or explain the failure.", "Agent SDK, Custom tools"),
                   "Then Claude can retry, try a different tool, or explain the failure."))
            + "<p><b>The metadata.</b> %s %s</p>" % (
                cf("ts-2-2-s1", gx("Returning structured error metadata including errorCategory (transient/validation/permission), isRetryable boolean, and human-readable descriptions", "Exam guide, 2.2-S1"),
                   "The guide returns an errorCategory, an isRetryable flag and a description that a person can read (2.2-S1)."),
                cf("ts-2-2-f2", D(HANDLE, "you can return the error message in the `content` along with `\"is_error\": true`:", "Handle tool calls"),
                   "These field names are the guide's: the documentation shows the flag and an error message in the content. The exam uses the guide."))
            + "<p><b>Retry or not.</b> %s %s %s</p>" % (
                cf("ts-2-2-k4", gx("The difference between retryable and non-retryable errors, and how returning structured metadata prevents wasted retry attempts", "Exam guide, 2.2-K4"),
                   "Metadata that says whether an error is retryable prevents wasted retries (2.2-K4)."),
                cf("ts-2-2-f8", D(HANDLE, "If a tool request is invalid or missing parameters, Claude will retry 2-3 times with corrections before apologizing to the user.", "Handle tool calls"),
                   "For invalid input, Claude tries again 2 or 3 times with corrections."),
                cf("ts-2-2-s2", gx("Including retriable: false flags and customer-friendly explanations for business rule violations so the agent can communicate appropriately", "Exam guide, 2.2-S2"),
                   "A business rule violation gets retriable: false and an explanation for the customer, so the agent can tell the customer (2.2-S2)."))
            + "<p><b>Recover locally.</b> %s Task statement 5.3 has the same points.</p>" %
                cf("ts-2-2-s3", gx("Implementing local error recovery within subagents for transient failures, propagating to the coordinator only errors that cannot be resolved locally along with partial results and what was attempted", "Exam guide, 2.2-S3"),
                   "A subagent recovers from a transient failure itself, and passes to the coordinator only what it cannot fix, with its partial results and what it tried (2.2-S3).")
            + exam_tests("2.2", [("Error handling and propagation: structured error responses, transient vs business vs permission errors, local recovery before escalation", "Among the topics, the guide names")])
            + guide_text("2.2"), "ts-2-2")
    + level("depth",
            beyond([cf("ts-2-2-b1", D(CCMCP, "Error text longer than about 11,000 characters keeps only its first 5,000 and last 5,000 characters", "Claude Code, MCP"),
                       "When Claude Code is the MCP client, it cuts an error text longer than about 11,000 characters, so the category and the retry advice go first."),
                    cf("ts-2-2-b2", D(SDKT, "The Python `@tool` decorator forwards only `content` and `is_error` from the handler", "Agent SDK, Custom tools"),
                       "A Python tool of the Agent SDK forwards only the content and the flag, so the metadata must go into the text."),
                    cf("ts-2-2-b3", D(SDKT, "A handler error doesn't stop the agent loop.", "Agent SDK, Custom tools"),
                       "An exception in a tool does not stop the loop, but Claude then sees only the raw message, which is close to a generic error.")])
            + code_pop_text("ts-2-2-code", "The code: an error result in the Claude API", "A tool result with is_error", HANDLE, ERR22, "Handle tool calls",
                            "The example has the flag and a message, and no errorCategory or isRetryable field.")
            + tab2_links("2.2", "%s %s" % (fact("ts-1-3-d26", "The mock builder uses no MCP."),
                                           cf("ts-2-2-near", excerpt("src/model_call.py", "# 429, 5xx and network errors. Each other error stops the run.", "The code of the model calls"),
                                              "It has a near case for errors of the Claude API, not of tools: a new call repairs a rate limit, a server error or a network error, and each other error stops the run."))), "ts-2-2"))


# ----- part 2.3 (facts: academy/facts/ts-2-3.md) -----

YAML23 = "---\nname: safe-researcher\ndescription: Research agent with restricted capabilities\ntools: Read, Grep, Glob, Bash\n---"
FIG23 = figure("2.3-1", 890, 350,
               "A coordinator delegates to four agents of the research system, and each agent has only the tools of its role: web search tools, load_document, "
               "verify_fact, and the tools of the report. The synthesis agent checks a simple fact with its own verify_fact tool, and sends a complex check through the coordinator.",
               "".join(['<path class="ve-e no-head" d="M445 90V120M120 120H780"/>',
                        edge("M120 120V150"), edge("M340 120V150"), edge("M560 120V150"), edge("M780 120V150"),
                        edge("M560 240V280", "simple check", 568, 265, anchor="r"),
                        edge("M640 150V55H560", "complex check, through the coordinator", 735, 46, cls="is-hot"),
                        box(330, 20, 230, 70, ["Coordinator"], sub="delegates", cls="who-model"),
                        box(20, 150, 200, 90, ["Web search"], sub="web search tools", cls="who-model"),
                        box(240, 150, 200, 90, ["Document", "analysis"], sub="load_document", cls="who-model"),
                        box(460, 150, 200, 90, ["Synthesis"], sub="verify_fact only", cls="who-model"),
                        box(680, 150, 190, 90, ["Report"], sub="its own tools", cls="who-model"),
                        box(460, 280, 200, 50, ["verify_fact"], sub="a narrow shared tool", cls="try ok")]),
               "%s %s" % (cf("ts-2-3-k3", gx("Scoped tool access: giving agents only the tools needed for their role, with limited cross-role tools for specific high-frequency needs", "Exam guide, 2.3-K3"),
                             "Each agent gets only the tools of its role, plus a narrow tool for a frequent need (2.3-K3)."),
                          cf("ts-2-3-f14", gx("Option A applies the principle of least privilege by giving the synthesis agent only what it needs for the 85% common case (simple fact verification) while preserving the existing coordination pattern for complex cases.", "Exam guide, sample question 9"),
                             "In sample question 9 of the guide, verify_fact serves the 85% of simple checks, and complex checks keep the route through the coordinator.")))

PART["2.3"] = (overview("2.3", "Give each agent only the tools that its role needs",
                        "Each agent gets a small set of tools for its role, plus a narrow shared tool for a frequent need, and the coordinator handles the rest. "
                        "tool_choice sets whether Claude can, must, or must use one named tool, but the newest models reject the forced settings.",
                        FIG23)
    + level("explanation",
            "<p><b>Few tools.</b> %s %s</p>" % (
                cf("ts-2-3-k1", gx("The principle that giving an agent access to too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability by increasing decision complexity", "Exam guide, 2.3-K1"),
                   "Too many tools, such as 18 instead of 4 or 5, make the choice of tool less reliable (2.3-K1)."),
                cf("ts-2-3-f1", D(TSR, "Claude's ability to pick the right tool degrades once you exceed 30–50 available tools.", "Tool search tool"),
                   "The documentation puts the drop higher, above 30 to 50 tools. The exam uses the guide."))
            + "<p><b>Scope by role.</b> %s %s %s</p>" % (
                cf("ts-2-3-s1", gx("Restricting each subagent's tool set to those relevant to its role, preventing cross-specialization misuse", "Exam guide, 2.3-S1"),
                   "Each subagent gets only the tools of its role, so that it does not misuse tools of another role, such as a synthesis agent that searches the web (2.3-K2, 2.3-S1)."),
                cf("ts-2-3-f5", D(SUB, "subagents can be limited to specific tools, reducing the risk of unintended actions", "Agent SDK, Subagents"),
                   "The documentation gives its own reason: fewer tools reduce the risk of unintended actions."),
                fact("ts-1-3-f10", "A tool that the list of a subagent leaves out is not in its session."))
            + "<p><b>Narrow tools.</b> %s %s</p>" % (
                cf("ts-2-3-s2", gx("Replacing generic tools with constrained alternatives (e.g., replacing fetch_url with load_document that validates document URLs)", "Exam guide, 2.3-S2"),
                   "A generic tool becomes a constrained one, such as load_document that checks document URLs, in place of fetch_url (2.3-S2)."),
                cf("ts-2-3-s3", gx("Providing scoped cross-role tools for high-frequency needs (e.g., a verify_fact tool for the synthesis agent) while routing complex cases through the coordinator", "Exam guide, 2.3-S3"),
                   "A narrow tool of another role serves a frequent need, and complex cases still go through the coordinator (2.3-S3). Only the guide describes these two points."))
            + "<p><b>tool_choice.</b> %s %s %s %s</p>" % (
                cf("ts-2-3-k4", gx("tool_choice configuration options: \"auto\", \"any\", and forced tool selection ({\"type\": \"tool\", \"name\": \"...\"})", "Exam guide, 2.3-K4"),
                   "The guide names three options: auto, any, and a forced tool (2.3-K4). With any, Claude must call a tool and gives no text (2.3-S5). A forced tool makes one tool run first, and the next steps follow in later turns (2.3-S4)."),
                cf("ts-2-3-f9", D(DEFT, "When working with the `tool_choice` parameter, there are four possible options:", "Define tools"),
                   "The documentation names four: it adds none, which blocks all tools."),
                cf("ts-2-3-f13", D(DEFT, "| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://platform.claude.com/docs/en/models/mythos-5-1/overview) | `any` and `tool` return a [400 error]", "Define tools"),
                   "Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 return a 400 error for any and for a forced tool."),
                "The exam uses the guide. The mock builder follows the documentation (step 2 of tab 2).")
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
                                   "No step gives an agent a set of tools. Step 2 of tab 2 tells why the build sends no forced tool call: the current models do not accept one.")
                         + ' <a href="%s#step-2">Step 2, Write the question &rarr;</a>' % TAB2), "ts-2-3"))


# ----- part 2.4 (facts: academy/facts/ts-2-4.md) -----

SDKM = "claude-code-docs-agent-sdk-mcp"
A02 = glob.glob(os.path.join(ROOT, "academy/decisions/0002-*.md"))[0][len(ROOT) + 1:]
MCP24 = "\n".join(read(SRC % CCMCP).split("\n")[650:661])
assert MCP24.startswith("{") and "${API_KEY}" in MCP24 and MCP24.rstrip().endswith("}")
FIG24 = figure("2.4-1", 890, 320,
               "An environment variable expands into .mcp.json, the project file that the team commits. ~/.claude.json holds the personal servers of a user. "
               "Claude Code or the Agent SDK connects to the servers of both files, and the agent gets the tools of all servers together. Resources show the agent what data exists.",
               "".join([edge("M145 80V110", "${VAR} expands", 153, 99, anchor="r"),
                        edge("M270 150H305V180H340"), edge("M270 260H305V180H340"),
                        edge("M540 180H580V80H620"), edge("M745 220V120", "what data exists", 753, 175, anchor="r"),
                        box(20, 20, 250, 60, ["environment"], sub="the secret, not in git"),
                        box(20, 110, 250, 80, [".mcp.json"], sub="project: team, committed"),
                        box(20, 220, 250, 80, ["~/.claude.json"], sub="user: personal servers"),
                        box(340, 140, 200, 80, ["Claude Code", "or Agent SDK"], sub="connects"),
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
                cf("ts-2-4-f3", D(CCMCP, "User-scoped servers are stored in `~/.claude.json` and provide cross-project accessibility", "Claude Code, MCP"),
                   "User scope is in ~/.claude.json, for all the projects of one person (2.4-S2)."),
                cf("ts-2-4-c1", D(CCMCP, "Use local scope for personal development servers, experimental configurations, or servers with credentials you don't want in version control.", "Claude Code, MCP"),
                   "The documentation has a third scope: local, the default, also in ~/.claude.json, which it names for experimental servers. The exam uses the guide."))
            + "<p><b>Secrets.</b> %s %s</p>" % (
                cf("ts-2-4-k2", gx("Environment variable expansion in .mcp.json (e.g., ${GITHUB_TOKEN}) for credential management without committing secrets", "Exam guide, 2.4-K2"),
                   "In .mcp.json, a token is a variable such as ${GITHUB_TOKEN}, so the secret is never committed (2.4-K2)."),
                cf("ts-2-4-f6", D(CCMCP, "allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys", "Claude Code, MCP"),
                   "Claude Code expands the variable when it loads the file, so a team shares the file and each person keeps the key."))
            + "<p><b>All tools at once.</b> %s %s</p>" % (
                cf("ts-2-4-f9", D(SDKM, "MCP tools follow the naming pattern `mcp__<server-name>__<tool-name>`.", "Agent SDK, MCP"),
                   "Each tool name carries the name of its server, so the tools of many servers can sit side by side."),
                cf("ts-2-4-c3", D(CCMCP, "Only tool names and server instructions load at session start", "Claude Code, MCP"),
                   "The guide says that the tools are discovered at connection time. In Claude Code, by default, only the tool names load at the start, and the full definitions load on demand. The exam uses the guide."))
            + "<p><b>Resources.</b> %s %s</p>" % (
                cf("ts-2-4-s5", gx("Exposing content catalogs as MCP resources to give agents visibility into available data without requiring exploratory tool calls", "Exam guide, 2.4-S5"),
                   "A server can expose a catalog, such as issue summaries or database schemas, as resources, so the agent sees what data exists without exploratory tool calls (2.4-K4, 2.4-S5)."),
                cf("ts-2-4-f13", D(CCMCP, "Claude Code automatically provides tools to list and read MCP resources when servers support them", "Claude Code, MCP"),
                   "Claude Code gives Claude tools to list and read them."))
            + "<p><b>Good servers.</b> %s Part 2.1 shows how. %s %s</p>" % (
                cf("ts-2-4-s3", gx("Enhancing MCP tool descriptions to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools (like Grep) over more capable MCP tools", "Exam guide, 2.4-S3"),
                   "A detailed description of an MCP tool keeps the agent from using a built-in tool such as Grep in its place (2.4-S3)."),
                cf("ts-2-4-s4", gx("Choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira), reserving custom servers for team-specific workflows", "Exam guide, 2.4-S4"),
                   "For a standard integration such as Jira, the guide uses an existing community server, and a custom server only for a workflow of the team (2.4-S4)."),
                cf("ts-2-4-c6", D(CCMCP, "Verify you trust each server before connecting it.", "Claude Code, MCP"),
                   "The documentation warns: check that you trust each server before you connect it."))
            + exam_tests("2.4", [("MCP server configuration: project vs user scope, environment variable expansion, multi-server simultaneous access", "Among the topics, the guide names"),
                                 ("MCP tool and resource design: resources for content catalogs, tools for actions, description quality for adoption", "and")])
            + guide_text("2.4"), "ts-2-4")
    + level("depth",
            beyond([cf("ts-2-4-b1", D(CCMCP, "For security reasons, Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files.", "Claude Code, MCP"),
                       "In an interactive session, Claude Code asks for approval before it uses a server of a committed .mcp.json. In a non-interactive run it cannot ask, and it loads the server without a prompt."),
                    cf("ts-2-4-b2", D(CCMCP, "In a remote server's `url` and `headers`, Claude Code reads credential variables from your environment as empty rather than expanding them.", "Claude Code, MCP"),
                       "For a remote server, some credential variables in the URL and the headers are read as empty, not expanded."),
                    cf("ts-2-4-b3", D(SDKM, "MCP tools require explicit permission before Claude can use them.", "Agent SDK, MCP"),
                       "In the Agent SDK, an MCP tool also needs a permission before Claude can call it.")])
            + code_pop_text("ts-2-4-code", "The code: a shared .mcp.json with variables", "An .mcp.json with variable expansion", CCMCP, MCP24, "Claude Code, MCP",
                            "${API_KEY} comes from the environment. ${API_BASE_URL:-...} has a default value.")
            + tab2_links("2.4", cf("ts-2-4-a02", excerpt(A02, "the pipeline uses no MCP server, because it calls only the Claude API and reads local files.", "Academy decision 0002"),
                                   "The mock builder uses no MCP server: it calls only the Claude API and reads local files.")), "ts-2-4"))

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
  <p>Each task statement opens in three levels: the <b>Overview</b> (about 30 seconds), the <b>Explanation</b> (about 3 minutes), with the guide&rsquo;s own text and what the exam tests, and the <b>Depth</b>, with facts beyond the exam, code in popups, and the steps of the mock builder (the program that wrote the mocks of this academy, see tab 2) that use the task statement.</p>
</section>""" % {"lab": lab("1.1-K2"), "count": fact("m-count", "The guide has %d task statements with %d points: %d Knowledge of and %d Skills in." % (len(TS), N_PTS, N_K, N_S))}
CARD["m-count"] = {"title": "The exam guide as records", "kind": "count",
                   "text": "reference/guide-records.json has %d task statements and %d points: %d of kind knowledge and %d of kind skill. The script of this page counted them." % (len(TS), N_PTS, N_K, N_S),
                   "src": "reference/guide-records.json", "href": link("reference/guide-records.json")}

DOMAIN_SUMMARY = {}   # domain -> one or two sentences, written from the titles of its task statements (decision 0021)
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
