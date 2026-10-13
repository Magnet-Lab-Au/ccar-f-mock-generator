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


def code_block(path, first, last, title):
    """The lines from the line with first to the line with last, as they are in the file."""
    lines = read(path).split("\n")
    a = next(i for i, l in enumerate(lines) if first in l)
    b = next(i for i, l in enumerate(lines) if i >= a and last in l)
    indent = min(len(l) - len(l.lstrip()) for l in lines[a:b + 1] if l.strip())
    text = "\n".join(l[indent:] for l in lines[a:b + 1])
    return {"title": title, "kind": "code", "text": text,
            "src": "%s, %s" % (path, "line %d" % (a + 1) if a == b else "lines %d to %d" % (a + 1, b + 1)),
            "href": link(path, a + 1, b + 1)}


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
