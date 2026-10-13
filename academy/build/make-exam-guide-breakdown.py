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
from lib import REPO, ROOT, TAG, e, excerpt, fact, lines_of, link, page, read, script_file, write  # noqa: E402

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
    return fact(key, "The 5 mocks of this academy have %d questions on its points, of %d." % (ON_TS[tsid], len(QUESTIONS)))


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
        body = '<p class="pending">This task statement comes in slice %d.</p>' % SLICE_OF[t["domain"]]
    return ('<details class="part" id="%s"><summary><span class="pn">%s</span><span><h3>%s</h3></span>'
            '<span class="mm"><span class="more" aria-hidden="true"></span></span></summary><div class="body">%s</div></details>'
            % (pid, tsid, e(head), body))


def overview(tsid, takeaway, answer, fig=""):
    TAKEAWAY[tsid] = takeaway
    key = "ts-%s-title" % tsid.replace(".", "-")
    CARD[key] = gx("### **Task Statement %s: %s**" % (tsid, TS[tsid]["title"]), "Exam guide, task statement %s" % tsid)
    return level("overview", '<h4 class="takeaway">%s</h4><p class="gtitle">%s</p><p class="lead">%s</p>%s'
                 % (e(takeaway), fact(key, "&ldquo;%s&rdquo;" % e(TS[tsid]["title"])), answer, fig), "ts-" + tsid.replace(".", "-"))


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
    for a, b in (("Fig. 1<", "Fig. 1.1-1<"), ("Fig. 2<", "Fig. 1.1-2<"), ("Fig. 4<", "Fig. 1.1-3<"), ("in Fig. 1,", "in Fig. 1.1-1,")):
        html = html.replace(a, b)
    for k in set(re.findall(r'data-step="ts-1-1-([^"]+)"', html)):
        POP["ts-1-1-" + k] = S_POP[k]
    for k in set(re.findall(r'data-card="ts-1-1-([^"]+)"', html)):
        CARD["ts-1-1-" + k] = S_CARD[k]
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
    CARD["m-s%d" % s["id"]] = gx("### Scenario %d: %s" % (s["id"], s["name"]), "Exam guide, section 5, scenario %d" % s["id"])


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
    <figcaption><span class="fig-n">Fig. A</span>The 5 domains of the guide, with their %(nts)d task statements. %(weights)s Each task statement opens below.</figcaption>
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
                 "scap": "The 6 scenarios of the guide, each with its primary domains. An exam draws 4 of them."}


BREAKDOWN = """<section class="parts" id="breakdown" aria-label="How we broke it down">
  <h2>How we broke it down</h2>
  <p>The guide gives each task statement two lists of points: &ldquo;Knowledge of&rdquo; and &ldquo;Skills in&rdquo;. %(count)s</p>
  <p class="key"><span class="tag-k">K = Knowledge of</span><span class="tag-s">S = Skills in</span><span>%(lab)s = domain 1 &middot; task statement 1.1 &middot; Knowledge of, point 2. The labels are ours. The guide has no labels.</span></p>
  <p>Each task statement opens in three levels: the <b>Overview</b> (about 30 seconds), the <b>Explanation</b> (about 3 minutes), with the guide&rsquo;s own text and what the exam tests, and the <b>Depth</b>, with facts beyond the exam, code in popups, and the steps of the mock builder that use the task statement.</p>
</section>""" % {"lab": lab("1.1-K2"), "count": fact("m-count", "The guide has %d task statements with %d points: %d Knowledge of and %d Skills in." % (len(TS), N_PTS, N_K, N_S))}
CARD["m-count"] = {"title": "The exam guide as records", "kind": "count",
                   "text": "reference/guide-records.json has %d task statements and %d points: %d of kind knowledge and %d of kind skill. The script of this page counted them." % (len(TS), N_PTS, N_K, N_S),
                   "src": "reference/guide-records.json", "href": link("reference/guide-records.json")}

DOMAIN_SUMMARY = {}   # domain -> one or two sentences, written from the titles of its task statements (decision 0021)


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
  <p class="lead">The CCAR-F exam guide, broken down into its 5 domains and %(nts)d task statements. Each task statement opens from a short answer to the guide&rsquo;s own text and beyond.</p>
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
