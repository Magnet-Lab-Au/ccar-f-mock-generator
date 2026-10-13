"""Make the fourth sample page of task statement 1.1: academy/sample/1-1-agentic-loops-site.html.

The third sample (make-1-1-portal.py) in the look of the website www.magnetlab.com.au,
which the owner asked for on 13 October 2026: square corners, thin rules, flat boxes
with no shadow or glow, IBM Plex Mono for labels, and the website colors. The values
come from the stylesheet of the website, read on 13 October 2026: the dark colors
are its default, and the light colors are its "band-light" sections. The content does
not change. It does not write the first, second or third sample.

Run from the folder ccar-f-mock-generator:
    python3 academy/sample/make-1-1-site.py
"""
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("make_1_1_portal", os.path.join(HERE, "make-1-1-portal.py"))
portal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(portal)

OUT = os.path.join(HERE, "1-1-agentic-loops-site.html")
changes = [c for c in portal.CHANGES if c[0] != '"1-1-agentic-loops-ve.html"']
changes.insert(0, ('"1-1-agentic-loops-ve.html"', '"1-1-agentic-loops-site.html"'))

# These changes apply to the text after the changes of the third sample.
SITE = [
    # fonts: Sora, and IBM Plex Mono for labels and numbers
    ("family=Sora:wght@400;500;600;700&display=swap",
     "family=Sora:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"),
    ("--font-mono: ui-monospace, 'Cascadia Mono', Consolas, monospace;", "--font-mono: 'IBM Plex Mono', ui-monospace, monospace;"),
    # light: the "band-light" colors of the website
    ("--bg: #fcfbf5; --surface: #ffffff; --border: #e4e4e7; --border-bright: #7f8a9c; --gold: #f3a83c;",
     "--bg: #fbfaf8; --surface: #f5f3ef; --border: #d9d4cb; --border-bright: #b9b2a6; --gold: #ffb84d;"),
    ("--text: #11293d; --text-dim: #64748b; --accent: #2b6087; --accent-dim: rgba(43,96,135,.12);",
     "--text: #11293d; --text-dim: #5a6874; --accent: #8a4b08; --accent-dim: rgba(255,184,77,.22);"),
    ("--lift: rgb(17 41 61 / .12); --halo: 22%;", "--lift: transparent; --halo: 0%;"),
    # dark: the default colors of the website
    ("--bg: #11293d; --surface: #16344a; --border: #2c4c66; --border-bright: #6a88a2; ",
     "--bg: #0b1725; --surface: #101f30; --border: #ffffff21; --border-bright: #ffffff42; "),
    ("--text: #f3f1ea; --text-dim: #9fb0c0; --accent: #f3a83c; --accent-dim: rgba(243,168,60,.16); ",
     "--text: #f4f2ef; --text-dim: #8b9caa; --accent: #ffb84d; --accent-dim: rgba(255,184,77,.16); "),
    ("--node-top: color-mix(in srgb, var(--text) 7%, var(--surface)); --lift: rgb(0 0 0 / .45); --halo: 32%;",
     "--node-top: var(--surface); --lift: transparent; --halo: 0%;"),
    # square corners
    ("--r-1: 4px; --r-2: 10px;", "--r-1: 0; --r-2: 0;"),
    # headings: the section headings of the website, with no line under the main heading
    ("--t-h1: clamp(2rem, 4.6vw, 3.25rem);", "--t-h1: clamp(1.75rem, 3.6vw, 2.75rem);"),
    ("h1 { font-size: var(--t-h1); line-height: 1.12; letter-spacing: -.02em; max-width: 20ch; width: fit-content; padding-bottom: .4rem; border-bottom: 3px solid var(--gold); }",
     "h1 { font-size: var(--t-h1); line-height: 1.12; letter-spacing: -.038em; max-width: 22ch; }"),
    ("h2 { font-size: var(--t-h2); line-height: 1.2; letter-spacing: -.01em; }",
     "h2 { font-size: var(--t-h2); line-height: 1.2; letter-spacing: -.02em; }"),
    # labels: the wide letter spacing of the website labels
    ("font: 600 var(--t-label) var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }",
     "font: 600 var(--t-label) var(--font-mono); letter-spacing: .16em; text-transform: uppercase; color: var(--accent); }"),
    (".lvl1 { font: 600 var(--t-label) var(--font-mono); color: var(--text-dim); letter-spacing: .08em;",
     ".lvl1 { font: 600 var(--t-label) var(--font-mono); color: var(--text-dim); letter-spacing: .16em;"),
    # figures: a flat stage with no dot grid
    (".frame { background: radial-gradient(circle at 1px 1px, color-mix(in srgb, var(--text) 13%, transparent) 1px, transparent 1.5px) 0 0 / 20px 20px, var(--bg);",
     ".frame { background: var(--bg);"),
    # flat boxes, a gold rule over each section, buttons in the text font
    ("</style>",
     "  /* the look of the website: flat, square, thin rules */\n"
     "  .ve-n .sh, .ve-n.is-key .sh, .ve-e.is-hot, .ve-dots circle { filter: none; }\n"
     "  header { border-top: 1px solid var(--gold); padding-top: var(--s-5); }\n"
     "  .eyebrow { max-width: none; }\n"
     "  a { color: var(--accent); }\n"
     "  button { font: 500 var(--t-small) var(--font-body); }\n"
     "  button:hover, button:focus-visible { border-color: var(--gold); }\n"
     "</style>"),
    ("Third sample: the second sample in the colors and fonts of the academy portal, by academy/sample/make-1-1-portal.py.",
     "Fourth sample: the third sample in the look of www.magnetlab.com.au, by academy/sample/make-1-1-site.py."),
]

portal.build(changes + SITE)

# square corners in the drawings too: each rect of the figures has rx="0"
with open(OUT, encoding="utf-8") as f:
    page = f.read()
page, n = re.subn(r' rx="[0-9.]+"', ' rx="0"', page)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("Squared %d corners in the figures." % n)
