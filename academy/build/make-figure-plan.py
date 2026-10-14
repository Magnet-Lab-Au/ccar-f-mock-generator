"""Makes academy/figure-plan.html from academy/figure-plan.md (academy decision 0037).

The Markdown file is the record. This page shows the same text with the look of the academy pages,
so that the owner can read the plan in a browser. Run: python3 academy/build/make-figure-plan.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
NAME = sys.argv[1] if len(sys.argv) > 1 else "figure-plan"   # also: popup-plan
SRC = os.path.join(ROOT, "academy", NAME + ".md")
OUT = os.path.join(ROOT, "academy", NAME + ".html")
CHIP = {"Redraw": "info", "Add": "ok", "Keep": ""}


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


def cell(t, head):
    t = t.strip()
    if not head and t in CHIP:
        return '<span class="chip %s">%s</span>' % (CHIP[t], t)
    if not head:
        for kind in ("Stepper", "Small multiples", "Before / after", "Live figure", "Close-up"):
            if t.startswith(kind):
                return '<b class="kind">%s</b>%s' % (kind, inline(t[len(kind):]))
    return inline(t)


def table(rows):
    head = [c for c in rows[0].strip("|").split("|")]
    body = [r.strip("|").split("|") for r in rows[2:]]
    out = ['<div class="table-scroll"><table><thead><tr>%s</tr></thead><tbody>' % "".join("<th>%s</th>" % cell(c, True) for c in head)]
    for r in body:
        st = next((c.strip() for c in r if c.strip() in CHIP), "")
        out.append('<tr data-change="%s">%s</tr>' % (st, "".join("<td>%s</td>" % cell(c, False) for c in r)))
    out.append("</tbody></table></div>")
    return "".join(out)


def convert(md):
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            out.append(table(rows)); continue
        if l.startswith("# "):
            out.append("<h1>%s</h1>" % inline(l[2:]))
        elif l.startswith("### "):
            out.append("<h3>%s</h3>" % inline(l[4:]))
        elif l.startswith("## "):
            out.append("<h2>%s</h2>" % inline(l[3:]))
        elif l.startswith("- ") or re.match(r"^\d+\. ", l):
            tag = "ul" if l.startswith("- ") else "ol"
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or re.match(r"^\d+\. ", lines[i])):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag)); continue
        elif l.strip():
            out.append("<p>%s</p>" % inline(l))
        i += 1
    return "\n".join(out)


STYLE = """
main { max-width: 80rem; }
table { border-collapse: collapse; width: 100%; font-size: var(--t-small); }
th { text-align: left; font: 500 var(--t-label) var(--font-mono); color: var(--text-dim); background: var(--surface); padding: var(--s-2) var(--s-3); }
td { border-top: 1px solid var(--border); padding: var(--s-2) var(--s-3); vertical-align: top; }
td:first-child { font-family: var(--font-mono); white-space: nowrap; }
tr[data-change="Keep"] td { color: var(--text-dim); }
.table-scroll { overflow-x: auto; border: 1px solid var(--border); }
.kind { font-weight: 600; }
ul, ol { padding-left: var(--s-5); display: grid; gap: var(--s-1); }
"""

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="pages/academy.css">
<style>%s</style>
</head>
<body>
<main>
%s
</main>
</body>
</html>
""" % (NAME.replace("-", " ").capitalize(), STYLE, convert(open(SRC, encoding="utf-8").read()))
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print("Wrote academy/%s.html" % NAME)
