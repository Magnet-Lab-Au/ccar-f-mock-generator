"""Make the third sample page of task statement 1.1: academy/sample/1-1-agentic-loops-portal.html.

The second sample (make-1-1-ve.py) in the colors and fonts of the academy portal,
for comparison only. This script runs make-1-1-ve.py with these changes and no
other: the font link, the color and font variables, the heading weight and size,
the gold line under the main heading, and the gold focus ring. The values come
from frontend/src/styles/index.css and the page headings of the portal
(magnetlab-academy). It does not write the first or the second sample.

Run from the folder ccar-f-mock-generator:
    python3 academy/sample/make-1-1-portal.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "make-1-1-ve.py")
with open(SRC, encoding="utf-8") as f:
    code = f.read()

CHANGES = [
    ('"1-1-agentic-loops-ve.html"', '"1-1-agentic-loops-portal.html"'),
    # fonts: the portal uses Sora for the text and the headings. It has no mono font.
    ("https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500&family=Atkinson+Hyperlegible+Next:wght@400;600&family=Atkinson+Hyperlegible+Mono:wght@400;500;600&display=swap",
     "https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap"),
    ("--font-display: 'Newsreader', Georgia, serif;", "--font-display: 'Sora', system-ui, sans-serif;"),
    ("--font-body: 'Atkinson Hyperlegible Next', 'Segoe UI', sans-serif;", "--font-body: 'Sora', system-ui, sans-serif;"),
    ("--font-mono: 'Atkinson Hyperlegible Mono', ui-monospace, monospace;", "--font-mono: ui-monospace, 'Cascadia Mono', Consolas, monospace;"),
    # light: canvas, surface, edge, ink, muted, brand-500; the states of the portal; gold for marks
    ("--bg: #f7f7f4; --surface: #ffffff; --border: #e3e3dc; --border-bright: #8e8e8a;",
     "--bg: #fcfbf5; --surface: #ffffff; --border: #e4e4e7; --border-bright: #7f8a9c; --gold: #f3a83c;"),
    ("--text: #17191c; --text-dim: #575c63; --accent: #2c4cd0; --accent-dim: rgba(44,76,208,.12);",
     "--text: #11293d; --text-dim: #64748b; --accent: #2b6087; --accent-dim: rgba(43,96,135,.12);"),
    ("--ok: #1d7443; --warn: #836000; --risk: #b3301d;", "--ok: #15803d; --warn: #92400e; --risk: #dc2626;"),
    ("--lift: rgb(18 22 20 / .12);", "--lift: rgb(17 41 61 / .12);"),
    # dark: the navy canvas of the portal; gold is the signal, as on its buttons
    ("--bg: #111316; --surface: #181b1f; --border: #262a30; --border-bright: #62676c; ",
     "--bg: #11293d; --surface: #16344a; --border: #2c4c66; --border-bright: #6a88a2; "),
    ("--text: #e8e8e3; --text-dim: #9ba1a9; --accent: #93a6ff; --accent-dim: rgba(147,166,255,.14); ",
     "--text: #f3f1ea; --text-dim: #9fb0c0; --accent: #f3a83c; --accent-dim: rgba(243,168,60,.16); "),
    ("--ok: #6cc492; --warn: #e3b94d; --risk: #f0806b;", "--ok: #4ade80; --warn: #fbbf24; --risk: #f87171;"),
    # headings: Sora semibold, as the page headings of the portal, with its gold line
    ("--t-h1: clamp(2.25rem, 5.5vw, 4rem);", "--t-h1: clamp(2rem, 4.6vw, 3.25rem);"),
    ("h1, h2 { font-family: var(--font-display); font-weight: 500;", "h1, h2 { font-family: var(--font-display); font-weight: 600;"),
    ("h1 { font-size: var(--t-h1); line-height: 1.05; letter-spacing: -.03em; max-width: 18ch; }",
     "h1 { font-size: var(--t-h1); line-height: 1.12; letter-spacing: -.02em; max-width: 20ch; width: fit-content; padding-bottom: .4rem; border-bottom: 3px solid var(--gold); }"),
    (":focus-visible { outline: 2px solid var(--accent);", ":focus-visible { outline: 2px solid var(--gold);"),
    ("Second sample, drawn with the visual-explainer plugin by academy/sample/make-1-1-ve.py.",
     "Third sample: the second sample in the colors and fonts of the academy portal, by academy/sample/make-1-1-portal.py."),
    # print and the tab icon
    ("--text: #17191c; --text-dim: #575c63; --accent: #2c4cd0; --border: #e3e3dc; --border-bright: #8e8e8a;",
     "--text: #11293d; --text-dim: #64748b; --accent: #2b6087; --border: #e4e4e7; --border-bright: #7f8a9c;"),
    ("fill='%23f7f7f4'/%3E%3Cpath d='M20 22h24v20H20z' fill='none' stroke='%232c4cd0'",
     "fill='%2311293d'/%3E%3Cpath d='M20 22h24v20H20z' fill='none' stroke='%23f3a83c'"),
]


def build(changes):
    """Run make-1-1-ve.py with each change made exactly once."""
    out = code
    for old, new in changes:
        assert out.count(old) == 1, "not found once: " + old
        out = out.replace(old, new)
    exec(compile(out, SRC, "exec"), {"__file__": SRC, "__name__": "make_1_1_built"})


if __name__ == "__main__":
    build(CHANGES)
