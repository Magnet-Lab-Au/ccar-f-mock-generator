"""The portal form of a tab (academy decisions 0050 and 0051, and the plan of the portal, "Needs from
ccar-f-mock-generator before PR 5").

It reads the page that opens alone, as the make script wrote it, and writes the same page for the portal into
academy/pages/portal/:
  src/<tab>.body.html   the content of the body only: no script, link, meta, title or theme button
  src/<tab>.data.ts     the cards and popups, as a module
  src/<tab>.css         the styles, each rule under .academy-page, dark mode on html.dark, no fonts
  src/academy.ts        the shared code: export start(root, data), which returns a function that stops it
  public/academy/...    the images that the body uses, at /academy/...
The text of each card, popup and part is the same in both forms. Only the frame changes.
"""
import os
import re
import shutil

from lib import PAGES, ROOT

OUT = os.path.join(PAGES, "portal")
TABS = ("exam-guide-breakdown", "behind-the-mocks")
SCOPE = ".academy-page"   # make() sets the scope of its tab: ".academy-page.ap-<tab>", so two tabs never share a rule
CONTAINER = "academy"
BASE_PX = 17      # the page that opens alone sets html { font-size: 17px }; the portal keeps 16 px
HEAD = "Made by academy/build/portal_form.py in ccar-f-mock-generator. Do not edit here: change the source there and copy again."


def _route(text):
    """Links between the tabs become routes of the portal; images go under /academy/."""
    for tab in TABS:
        text = re.sub(r'(["\'])%s\.html(#[^"\']*)?\1' % re.escape(tab), lambda m: "%s/%s%s%s" % (m.group(1), tab, m.group(2) or "", m.group(1)), text)
    text = re.sub(r'(src=")(images/|icons/)', r"\1/academy/\2", text)
    return text


# ---------- styles ----------

def _blocks(css):
    """Split css into top-level items: ('rule', selectors, body) or ('at', prelude, inner text or None)."""
    out, i, n = [], 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            i = css.index("*/", i) + 2
            continue
        if css[i].isspace():
            i += 1
            continue
        j, depth, q = i, 0, None
        while j < n:
            c = css[j]
            if q:
                if c == "\\":
                    j += 2
                    continue
                if c == q:
                    q = None
            elif css.startswith("/*", j):
                j = css.index("*/", j) + 2
                continue
            elif c in "\"'":
                q = c
            elif c == ";" and depth == 0 and css[i] == "@":
                break
            elif c == "{":
                depth += 1
                if depth == 1:
                    head_end = j
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        chunk = css[i:j + 1]
        if css[j:j + 1] == ";" and chunk.startswith("@"):
            out.append(("at", chunk[:-1].strip(), None))
        else:
            head, inner = css[i:head_end].strip(), css[head_end + 1:j]
            out.append(("at" if head.startswith("@") else "rule", head, inner))
        i = j + 1
    return out


def _px(decls):
    """rem in declarations to the exact pixels of the page that opens alone (media conditions keep rem)."""
    return re.sub(r"(?<![\w.-])(-?\d*\.?\d+)rem\b", lambda m: ("%.4f" % (float(m.group(1)) * BASE_PX)).rstrip("0").rstrip(".") + "px", decls)


def _selector(s):
    s = s.strip()
    s = re.sub(r"(?<![\w.#-])main(?![\w-])", ".ap-main", s)
    if s == "*":
        return [SCOPE, SCOPE + " *"]
    if s.startswith(":root:not(.light)"):
        return []                                  # the device setting: the portal decides with .dark on html
    if s.startswith(":root.dark"):
        return ["html.dark " + SCOPE + s[len(":root.dark"):]]
    if s.startswith(":root.light"):
        return [SCOPE + s[len(":root.light"):]]
    for top in (":root", "html", "body"):
        if s == top or (s.startswith(top) and not re.match(r"[\w-]", s[len(top):len(top) + 1])):
            return [SCOPE + s[len(top):]]
    if s.startswith(".js-motion"):
        return [SCOPE + s]
    if s.startswith("::"):
        return [SCOPE + " " + s]
    return [SCOPE + " " + s]


def _split(selectors):
    parts, depth, cur = [], 0, ""
    for c in selectors:
        if c == "," and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        depth += c in "([" and 1 or (c in ")]" and -1 or 0)
        cur += c
    return parts + [cur]


def scope_css(css):
    out = []
    for kind, head, inner in _blocks(css):
        if kind == "at":
            name = head.split()[0]
            if name == "@font-face":
                continue                           # the portal loads the fonts (decision 0053)
            if name == "@media" and "prefers-color-scheme" in head:
                continue                           # the portal decides dark mode with .dark on html (decision 0051)
            if name == "@media" and re.fullmatch(r"\s*\((?:min|max)-width:\s*[\d.]+(?:rem|px)\)(?:\s*and\s*\((?:min|max)-width:\s*[\d.]+(?:rem|px)\))*\s*", head[len("@media"):]):
                # a width rule measures the page, not the window: in the portal the side bar and the padding take room
                body = scope_css(inner)
                if re.search(r"(^|\n)%s \{" % re.escape(SCOPE), body):
                    raise SystemExit("A width rule styles the root of the page, which a container rule cannot: " + head)
                out.append("@container %s%s {\n%s}" % (CONTAINER, head[len("@media"):], body))
                continue
            if name in ("@keyframes", "@-webkit-keyframes") or inner is None:
                if inner is not None:
                    head = head.split()[0] + " academy-" + head.split()[1]      # a page animation has its own name in the portal
                out.append(head + ("{%s}" % inner if inner is not None else ";"))
                continue
            body = scope_css(inner)
            if body.strip():
                out.append("%s {\n%s}" % (head, body))
            continue
        sels = []
        for s in _split(head):
            for x in _selector(s):
                if x not in sels:
                    sels.append(x)
        if sels:
            out.append("%s { %s }" % (", ".join(sels), _px(inner.strip())))
    return "\n".join(out) + "\n"


def _animations(css):
    """The animations use the renamed keyframes."""
    for name in set(re.findall(r"@keyframes academy-([\w-]+)", css)):
        css = re.sub(r"(animation(?:-name)?:[^;}]*?)(?<![\w-])%s(?![\w-])" % re.escape(name), r"\1academy-" + name, css)
    return css


# Inside the page, undo the base styles of the portal (Tailwind's preflight), so that each element starts from the
# browser's own style, as on the page that opens alone. A drawing keeps the attributes of its shapes, and an image keeps
# the size of its width and height attributes, so only the base styles of the portal for svg and img are undone there.
BASE = """/* the base styles of the portal do not reach the page */
{s} :where(*:not(svg, svg *, img)), {s} :where(*:not(svg, svg *, img))::before, {s} :where(*:not(svg, svg *, img))::after {{ all: revert; }}
{s} svg, {s} img {{ display: revert; vertical-align: revert; }}
{s} img {{ max-width: revert; }}
{s} {{ tab-size: 8; container: {c} / inline-size; }}
"""
# The main area of the portal has its own padding, so the page does not add its own at the sides.
END = """/* the portal pads its main area */
{s} .ap-main {{ padding-left: 0; padding-right: 0; }}
/* the layers of the portal: its top bar (z-index 40, under 1024 px) and its drawer (50) */
{s} #pop {{ z-index: 45; }}
{s} .glossary-btn {{ z-index: 41; }}
{s} #top-words {{ z-index: 42; }}
@media (max-width: 1023.98px) {{ {s} [id] {{ scroll-margin-top: 72px; }} }}
"""


# ---------- the page ----------

def make(tab):
    with open(os.path.join(PAGES, tab + ".html"), encoding="utf-8") as f:
        page = f.read()
    css_files = re.findall(r'<link rel="stylesheet" href="([^"]+)">', page)
    body = page[page.index("<body>") + len("<body>"):page.index("</body>")]
    body = re.sub(r'<button class="theme-btn" id="theme-btn" type="button">[^<]*</button>\n?', "", body, count=1)
    if "<script" in body or "<link" in body:
        raise SystemExit("A script or link is in the body of " + tab)
    body = body.replace("<main>", '<div class="ap-main">').replace("</main>", "</div>")
    if "<main" in body:
        raise SystemExit("A main element with attributes is in the body of " + tab)
    body = _route(body)
    with open(os.path.join(PAGES, tab + ".js"), encoding="utf-8") as f:
        js = f.read()
    start = js.index("window.ACADEMY = ") + len("window.ACADEMY = ")
    data = _route(js[start:js.index(";\n", start)])

    os.makedirs(os.path.join(OUT, "src"), exist_ok=True)
    with open(os.path.join(OUT, "src", tab + ".body.html"), "w", encoding="utf-8") as f:
        f.write("<!-- %s -->\n%s" % (HEAD, body.strip() + "\n"))
    with open(os.path.join(OUT, "src", tab + ".data.ts"), "w", encoding="utf-8") as f:
        f.write("// @ts-nocheck\n/* eslint-disable */\n/* %s */\nconst data = %s;\nexport default data;\n" % (HEAD, data))
    global SCOPE
    SCOPE = ".academy-page.ap-" + tab
    css = BASE.format(s=SCOPE, c=CONTAINER)
    for name in css_files:
        with open(os.path.join(PAGES, name), encoding="utf-8") as f:
            css += "/* from %s */\n%s" % (name, scope_css(f.read()))
    css += END.format(s=SCOPE)
    css = _animations(css)
    with open(os.path.join(OUT, "src", tab + ".css"), "w", encoding="utf-8") as f:
        f.write("/* %s */\n%s" % (HEAD, css))

    with open(os.path.join(ROOT, "academy", "build", "academy.js"), encoding="utf-8") as f:
        shared = f.read()
    shared = shared[:shared.index("/* the page that opens alone */")]
    with open(os.path.join(OUT, "src", "academy.ts"), "w", encoding="utf-8") as f:
        f.write("// @ts-nocheck\n/* eslint-disable */\n/* %s */\n%sexport { academyStart as start };\n" % (HEAD, shared))

    for src in sorted(set(re.findall(r'src="/academy/([^"]+)"', body))):
        to = os.path.join(OUT, "public", "academy", src)
        os.makedirs(os.path.dirname(to), exist_ok=True)
        shutil.copyfile(os.path.join(PAGES, src), to)
    preview()
    return "%s: body %d KB, data %d KB, css %d KB" % (tab, len(body) // 1024, len(data) // 1024, len(css) // 1024)


PREFLIGHT = os.path.join(os.path.expanduser("~"), "magnetlab-academy", "frontend", "node_modules", "tailwindcss", "preflight.css")


def preview():
    """A test page for each tab that imitates the portal, for check-pages.js: the base styles of Tailwind (as the portal
    loads them), a side bar of 256 px and the padding of the portal's main area, a root font size of 16 px, and dark mode
    set on html as the portal's theme-init.js does. With ?shell=0 the side bar and the padding go, for a comparison of
    screenshots with the page that opens alone. Not for the portal: the copy takes only src/ and public/."""
    d = os.path.join(OUT, "preview")
    os.makedirs(d, exist_ok=True)
    if os.path.exists(PREFLIGHT):
        # in a layer, as Tailwind 4 loads it, with the base rule of the portal's index.css; not in git (.gitignore)
        with open(PREFLIGHT, encoding="utf-8") as f:
            pre = f.read()
        with open(os.path.join(d, "preflight.css"), "w", encoding="utf-8") as f:
            f.write("@layer theme, base, components, utilities;\n@layer base {\n%s\n* { border-color: #e0e0e0; }\n}\n" % pre)
    elif not os.path.exists(os.path.join(d, "preflight.css")):
        print("Note: no preflight.css, so the test page does not have the base styles of the portal, and check-pages.js fails")
    from lib import CSP, e
    fonts = re.findall(r"@font-face[^}]*}", open(os.path.join(PAGES, "academy.css"), encoding="utf-8").read())
    files = {
        "preview.css": "/* The frame of the portal for the test pages (not for the portal). */\n"
                       + "\n".join(f.replace("url(fonts/", "url(../../fonts/") for f in fonts)
                       + "\nhtml { font-size: 16px; color-scheme: light; }\nhtml.dark { color-scheme: dark; }\n"
                         "body { margin: 0; background: #fff; color: #11293d; font-family: Sora, sans-serif; -webkit-font-smoothing: antialiased; }\nhtml.dark body { background: #11293d; color: #fff; }\n"
                         ".shell { display: flex; min-height: 100vh; }\n.side { display: none; width: 256px; flex: none; background: #f7f4e2; }\n"
                         "html.dark .side { background: #1a3e5c; }\n.content { flex: 1; min-width: 0; padding: 16px; }\n"
                         "@media (min-width: 640px) { .content { padding: 24px; } }\n@media (min-width: 1024px) { .side { display: block; } .content { padding: 40px; } }\n"
                         ".bare .side { display: none !important; } .bare .content { padding: 0 !important; }\n"
                         "/* with ?shell=0, the side padding of the page that opens alone, for the comparison of screenshots */\n"
                         ".bare .academy-page.academy-page .ap-main { padding-left: %spx; padding-right: %spx; }\n" % (1.5 * BASE_PX, 1.5 * BASE_PX),
        "theme.js": "/* as the portal's theme-init.js: dark from the device setting when nothing is stored */\n"
                    "if (matchMedia('(prefers-color-scheme: dark)').matches) document.documentElement.classList.add('dark');\n"
                    "if (new URLSearchParams(location.search).get('shell') === '0') document.documentElement.classList.add('bare');\n",
        "preview.js": "/* starts the portal form of the tab on its element, as the React page of the portal will */\n"
                      "import { start } from '../src/academy.ts';\n"
                      "const tab = document.body.dataset.tab, root = document.getElementById('ap');\n"
                      "const [body, data] = await Promise.all([fetch('../src/' + tab + '.body.html').then((r) => r.text()), import('../src/' + tab + '.data.ts')]);\n"
                      "root.innerHTML = body;\n"
                      "window.ACADEMY = data.default;   // only for check-pages.js, which reads the popups of Fig. A there\n"
                      "let stop = start(root, data.default);\n"
                      "stop(); stop = start(root, data.default);   // twice, as React StrictMode does\n",
    }
    for name, text in files.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(text)
    for tab in TABS:
        title = "Portal form: " + tab
        with open(os.path.join(d, tab + ".html"), "w", encoding="utf-8") as f:
            f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                    '<meta http-equiv="Content-Security-Policy" content="%s">\n<title>%s</title>\n<link rel="stylesheet" href="preflight.css">\n'
                    '<link rel="stylesheet" href="preview.css">\n%s\n<script src="theme.js"></script>\n'
                    '<script type="module" src="preview.js"></script>\n</head>\n<body data-tab="%s">\n<div class="shell"><div class="side"></div>'
                    '<main class="content"><div class="academy-page ap-%s" id="ap"></div></main></div>\n</body>\n</html>\n'
                    # the styles of both tabs, as in the portal after a reader has opened both
                    % (CSP, e(title), "\n".join('<link rel="stylesheet" href="../src/%s.css">' % x for x in TABS), tab, tab))


if __name__ == "__main__":
    for t in TABS:
        print(make(t))
    preview()
