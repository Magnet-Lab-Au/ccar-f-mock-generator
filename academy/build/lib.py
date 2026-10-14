"""Shared helpers of the page scripts in academy/build/.

Each excerpt of a preview card and each number comes from its source file (decisions 0005, 0011 and 0030).
A helper stops with an error if its text is not in the file, so the page cannot disagree with its source.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, "academy", "pages")
REPO = "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator"
TAG = "mocks-v2"          # the files of the mock builder as they were when the 5 mocks were built
BRANCH = "main"           # for files that came after the tag
e = html.escape

# the security policy of the portal (magnetlab-academy/frontend/public/_headers), minus the parts that a meta tag cannot set
CSP = ("default-src 'self'; base-uri 'none'; object-src 'none'; form-action 'self'; script-src 'self'; "
       "style-src 'self' 'unsafe-inline'; font-src 'self' data:; img-src 'self' data: blob:; connect-src 'self'")


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


_SAME = {}


def in_tag(path):
    """True if the file is at the tag with the same text as today, so a line number of today is right at the tag."""
    if path not in _SAME:
        import subprocess
        r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (TAG, path)], capture_output=True)
        _SAME[path] = r.returncode == 0 and r.stdout.decode("utf-8", "replace") == read(path)
    return _SAME[path]


def link(path, a=None, b=None):
    ref = TAG if in_tag(path) else BRANCH
    plain = "?plain=1" if path.endswith(".md") else ""
    if a is None:
        return "%s/blob/%s/%s" % (REPO, ref, path)
    return "%s/blob/%s/%s%s#L%d%s" % (REPO, ref, path, plain, a, "-L%d" % b if b and b != a else "")


def lines_of(path, text):
    """The first and last line numbers of text in the file. Stops if text is not in the file."""
    content = read(path)
    i = content.find(text)
    if i < 0:
        raise SystemExit("Not in %s: %r" % (path, text[:80]))
    a = content.count("\n", 0, i) + 1
    return a, a + text.count("\n")


def excerpt(path, text, title, kind="excerpt"):
    a, b = lines_of(path, text)
    return {"title": title, "kind": kind, "text": text,
            "src": "%s, %s" % (path, "line %d" % a if a == b else "lines %d to %d" % (a, b)), "href": link(path, a, b)}


def code_block(path, first, last, title, ref=None):
    """The lines from the line with first to the line with last, as they are in the file.
    With ref (a tag or a commit), the lines as they were at that ref, and the link goes to that ref."""
    if ref:
        import subprocess
        lines = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (ref, path)], capture_output=True, check=True).stdout.decode("utf-8").split("\n")
    else:
        lines = read(path).split("\n")
    a = next(i for i, l in enumerate(lines) if first in l)
    b = next(i for i, l in enumerate(lines) if i >= a and last in l)
    indent = min(len(l) - len(l.lstrip()) for l in lines[a:b + 1] if l.strip())
    text = "\n".join(l[indent:] for l in lines[a:b + 1])
    return {"title": title, "kind": "code", "text": text,
            "src": "%s, %s" % (path, "line %d" % (a + 1) if a == b else "lines %d to %d" % (a + 1, b + 1)),
            "href": link(path, a + 1, b + 1) if not ref else "%s/blob/%s/%s#L%d-L%d" % (REPO, ref, path, a + 1, b + 1)}


def number(path, pattern, group=1):
    """A number read from a file with a regular expression. Stops if the pattern is not in the file."""
    m = re.search(pattern, read(path))
    if not m:
        raise SystemExit("No match in %s: %r" % (path, pattern))
    return int(m.group(group))


def fact(card, text):
    return '<span class="fact" tabindex="0" role="button" data-card="%s">%s</span>' % (card, text)


def page(title, body, script, description):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="%s">
<meta name="description" content="%s">
<title>%s</title>
<link rel="stylesheet" href="academy.css">
<script src="%s"></script>
</head>
<body>
<button class="theme-btn" id="theme-btn" type="button">Dark mode</button>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="ve-ah" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker>
  <linearGradient id="ve-node" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--node-top)"/><stop offset="1" style="stop-color:var(--surface)"/></linearGradient>
</defs></svg>
%s
<div id="pop" role="dialog" aria-labelledby="poptitle" hidden>
  <div class="ptop"><span><span class="tag" id="popwho"></span><span class="pinned" id="poppin"></span></span><button id="popclose" type="button" aria-label="Close">&times;</button></div>
  <h2 id="poptitle"></h2>
  <div id="popbody"></div>
</div>
</body>
</html>
""" % (CSP, e(description), e(title), script, body)


def script_file(name, pop, card):
    """One script file for the tab: its data, then the shared code (decision 0017)."""
    with open(os.path.join(ROOT, "academy", "build", "academy.js"), encoding="utf-8") as f:
        shared = f.read()
    data = json.dumps({"pop": pop, "card": card}, ensure_ascii=False, indent=None)
    out = "/* Made by academy/build/ from its sources. Do not edit by hand. */\nwindow.ACADEMY = %s;\n%s" % (data, shared)
    with open(os.path.join(PAGES, name), "w", encoding="utf-8") as f:
        f.write(out)


def write(name, text):
    with open(os.path.join(PAGES, name), "w", encoding="utf-8") as f:
        f.write(text)


VALUES = "auto|any|none|tool|end_turn|tool_use|max_tokens|stop_sequence|pause_turn|refusal|model_context_window_exceeded|json"
NAME = re.compile(r'(?<![\w./@#&-])(?:"(?:%s)"|[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?:\.[a-z_]+)*|[a-z]+(?:[A-Z][a-z0-9]+)+|--[a-z][a-z0-9-]*[a-z0-9]|claude -p|-p(?=[\s,.)]))(?![\w-])' % VALUES)


def code_font(html):
    """A single name in the running text is in code font (academy decision 0038): a name with an underscore, a camelCase name,
    a flag, claude -p, and a quoted value of an API field, with its quotes. Text inside a drawing, code, pre, a script or a tag
    is not changed. A list that quotes the guide (class glist) is not changed either, so its text stays as the guide has it."""
    out, skip = [], []
    for part in re.split(r"(<[^>]+>)", html):
        if part.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", part)
            tag = m.group(2).lower() if m else ""
            if tag in ("svg", "code", "script", "style", "pre", "title") or (tag == "ul" and 'class="glist' in part) or (tag == "ul" and m.group(1) and skip and skip[-1] == "ul"):
                if m.group(1):
                    if skip:
                        skip.pop()
                elif not part.endswith("/>"):
                    skip.append(tag)
            out.append(part)
        else:
            out.append(part if skip else NAME.sub(lambda x: "<code>%s</code>" % x.group(0), part))
    return "".join(out)


_RECORDS = None


def guide_points(ids):
    """The guide points of a popup, in the form of the popups of Fig. 1.1-1: the ID, the text and its task statement."""
    global _RECORDS
    if _RECORDS is None:
        _RECORDS = json.loads(read("reference/guide-records.json"))
    out = []
    for i in ids:
        for t in _RECORDS["task_statements"]:
            for p in t["points"]:
                if p["id"] == i:
                    out.append({"id": i, "text": p["text"], "ctx": "Task statement %s: %s" % (t["id"], t["title"])})
    assert len(out) == len(ids), ids
    return out


def popup_prefix(fig):
    """The part of a figure, for the key of a popup (decision 0033): ts-1-2 for Fig. 1.2-1, step-5 for Fig. 5-1, top for Fig. A."""
    if fig == "A":
        return "top"
    if fig.startswith("C-"):
        return "cc-" + fig[2:].rsplit("-", 1)[0].replace(".", "-")
    if re.match(r"^\d\.\d-\d$", fig):
        return "ts-" + fig.rsplit("-", 1)[0].replace(".", "-")
    return "step-" + fig.split("-")[0]


def add_popups(body, specs, tab, pop):
    """Put each popup of the plan on its box (academy/popup-plan.md). A label that is not in its figure stops the build."""
    attrs = ' data-step="%s" tabindex="0" role="button" aria-expanded="false"'
    seen = {}
    for sp in [x for x in specs if x["tab"] == tab]:
        part = popup_prefix(sp["fig"])
        n = seen[part] = seen.get(part, 0) + 1   # counted for each part, because a part can have several figures
        key = "%s-pop%d" % (part, n)
        cls = "io"
        for m in sp["match"]:
            cap = body.index('<span class="fig-n">Fig. %s</span>' % sp["fig"])
            start = body.rfind("<figure", 0, cap)
            found = []
            for v in (html.escape(m), html.escape(m, quote=False)):
                pos = body.find(">%s<" % v, start, cap)
                while pos >= 0:   # a figure with a phone drawing has each label twice (academy decision 0043)
                    found.append(pos)
                    pos = body.find(">%s<" % v, pos + 1, cap)
                if found:
                    break
            if not found:
                raise SystemExit("Popup label not in Fig. %s: %r" % (sp["fig"], m))
            first = found[0]
            panel_end = body.find('<div class="ba-panel"', first, cap)
            panel_end = cap if panel_end < 0 else panel_end
            if not sp.get("every"):   # "every": one popup on each copy of a label, such as "own context" in Fig. 1.2-1
                found = [first] + [x for x in found[1:] if first < body.rfind('<div class="frame narrow">', start, x) and x < panel_end]
            for pos in reversed(found):
                tag = body.rfind("<", 0, pos)
                while body.startswith(("<tspan", "<code"), tag):
                    tag = body.rfind("<", 0, tag)
                target = tag
                if not sp.get("text_el"):
                    g = body.rfind("<g ", start, pos)
                    li = body.rfind("<li", start, pos)
                    if g >= 0 and body.find("</g>", g, pos) < 0:
                        target = g
                    elif li >= 0 and body.find("</li>", li, pos) < 0:
                        target = li
                end = body.index(">", target)
                head = body[target:end]
                if "data-step=" in head or "data-card=" in head:
                    raise SystemExit("The box of %r in Fig. %s opens something already" % (m, sp["fig"]))
                if "who-model" in head:
                    cls = "model"
                elif "who-owner" in head:
                    cls = "owner"
                cut = target + len(re.match(r"<[a-zA-Z0-9]+", head).group(0))
                body = body[:cut] + attrs % key + body[cut:]
        pop[key] = {"who": sp["who"], "cls": cls, "title": sp["title"], "sent": sp["sent"], "points": guide_points(sp["points"]), "example": None}
    return body


def group_roles(body):
    """A drawing with popups is a group, not one picture, so that a screen reader reaches its popups (academy decision 0043, item 6)."""
    def one(m):
        svg = m.group(0)
        return svg.replace(' role="img"', ' role="group"', 1) if "data-step=" in svg else svg
    return re.sub(r"<svg\b[^>]*>.*?</svg>", one, body, flags=re.S)


SOURCES_RX = re.compile(r'<section class="sources" aria-label="([^"]*)">\s*<p class="ve-label">.*?</p>\s*<ul>(.*?)</ul>\s*</section>', re.S)


def fold_sources(body):
    """Each list of sources is a closed section that the reader opens (owner, 15 October 2026)."""
    def one(m):
        name = re.sub(r"^Sources of ts-(\d)-(\d)$", r"Sources of part \1.\2", m.group(1))
        name = {"Sources of the top": "Sources of the introduction"}.get(name, name)
        return ('<details class="sources" aria-label="%s"><summary class="ve-label">%s (%d)</summary><ul>%s</ul></details>'
                % (name, name, m.group(2).count("<li"), m.group(2)))
    out, n = SOURCES_RX.subn(one, body)
    assert 'class="sources"' not in SOURCES_RX.sub("", body) or n == body.count('<section class="sources"'), "a list of sources has another form"
    return out


def glossary_panel(dl, extra=""):
    """The glossary in a panel at the side, which a fixed button opens at any point of the page (owner, 15 October 2026)."""
    return ('<button type="button" class="glossary-btn" aria-controls="top-words" aria-expanded="false">Glossary</button>'
            '<aside class="glossary-panel" id="top-words" aria-label="Glossary" hidden><div class="gp-head"><h2>Glossary</h2>'
            '<button type="button" class="gp-close">Close</button></div>%s%s</aside>' % (dl, extra))
