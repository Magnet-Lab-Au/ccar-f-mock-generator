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

PORTAL = [c for c in portal.CHANGES if c[0] != '"1-1-agentic-loops-ve.html"']

# These changes apply to the text after the changes of the third sample.
SITE = [
    # fonts: Sora, and IBM Plex Mono for labels and numbers
    ("family=Sora:wght@400;500;600;700&display=swap",
     "family=Sora:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"),
    ("--font-mono: ui-monospace, 'Cascadia Mono', Consolas, monospace;", "--font-mono: 'IBM Plex Mono', ui-monospace, monospace;"),
    # light: the "band-light" colors of the website
    ("--bg: #fcfbf5; --surface: #ffffff; --border: #e4e4e7; --border-bright: #7f8a9c; --gold: #f3a83c;",
     "--bg: #fbfaf8; --surface: #f5f3ef; --border: #d9d4cb; --border-bright: #b9b2a6; --gold: #ffb84d; "
     "--k: #245780; --s: #8a4b08; --on-k: #ffffff; --on-s: #ffffff;"),
    ("--text: #11293d; --text-dim: #64748b; --accent: #2b6087; --accent-dim: rgba(43,96,135,.12);",
     "--text: #11293d; --text-dim: #5a6874; --accent: #8a4b08; --accent-dim: rgba(255,184,77,.22);"),
    ("--lift: rgb(17 41 61 / .12); --halo: 22%;", "--lift: transparent; --halo: 0%;"),
    # dark: the default colors of the website
    ("--bg: #11293d; --surface: #16344a; --border: #2c4c66; --border-bright: #6a88a2; ",
     "--bg: #0b1725; --surface: #101f30; --border: #ffffff21; --border-bright: #ffffff42; "),
    ("--text: #f3f1ea; --text-dim: #9fb0c0; --accent: #f3a83c; --accent-dim: rgba(243,168,60,.16); ",
     "--text: #f4f2ef; --text-dim: #8b9caa; --accent: #ffb84d; --accent-dim: rgba(255,184,77,.16); "),
    ("--node-top: color-mix(in srgb, var(--text) 7%, var(--surface)); --lift: rgb(0 0 0 / .45); --halo: 32%;",
     "--node-top: var(--surface); --lift: transparent; --halo: 0%; "
     "--k: #8cc0ea; --s: #ffb84d; --on-k: #0b1725; --on-s: #0b1725;"),
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
     "  .key { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2) var(--s-3); max-width: none; margin: var(--s-2) 0; font: 500 var(--t-label) var(--font-mono); color: var(--text-dim); }\n"
     "  .tag-k, .tag-s { font: 600 .62rem/1.5 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; padding: 0 .3rem; }\n"
     "  .tag-k { background: var(--k); color: var(--on-k); } .tag-s { background: var(--s); color: var(--on-s); }\n"
     "  .lk { color: var(--k); } .ls { color: var(--s); }\n"
     "  @media print { :root, :root:not(.light), :root.dark { --k: #245780; --s: #8a4b08; --on-k: #fff; --on-s: #fff; } }\n"
     "  button { font: 500 var(--t-small) var(--font-body); }\n"
     "  button:hover, button:focus-visible { border-color: var(--gold); }\n"
     "</style>"),
    # the legend on the page replaces the note about the labels
    ("<p class=\"ve-label\">The labels 1.1-K1 to 1.1-S3 are ours. The guide has no labels.</p>",
     "<p class=\"key\"><span class=\"tag-k\">K = Knowledge of</span><span class=\"tag-s\">S = Skills in</span>"
     "<span>1.1-K2 = domain 1 &middot; task statement 1 &middot; point 2. The labels are ours. The guide has no labels.</span></p>"),
    # the popups: a legend of the kinds in the list, and the colored letter in each label
    ("s.appendChild(el('h3', null, 'The exam guide says')); const ul = el('ul');",
     "s.appendChild(el('h3', null, 'The exam guide says')); const key = el('p', 'key');"
     " if (d.points.some((p) => p.id.includes('-K'))) key.appendChild(el('span', 'tag-k', 'K = Knowledge of'));"
     " if (d.points.some((p) => p.id.includes('-S'))) key.appendChild(el('span', 'tag-s', 'S = Skills in'));"
     " s.appendChild(key); const ul = el('ul');"),
    ("li.appendChild(el('b', null, p.id + ' '));",
     "const b = el('b'), m = p.id.match(/^(.*-)([KS])(.*)$/);"
     " if (m) b.append(m[1], el('span', m[2] === 'K' ? 'lk' : 'ls', m[2]), m[3] + ' '); else b.textContent = p.id + ' ';"
     " li.appendChild(b);"),
    ("Third sample: the second sample in the colors and fonts of the academy portal, by academy/sample/make-1-1-portal.py.",
     "Fourth sample: the third sample in the look of www.magnetlab.com.au, by academy/sample/make-1-1-site.py."),
]

def color_labels(text):
    return re.sub(r"(\d\.\d-)([KS])(\d)", lambda m: '%s<span class="%s">%s</span>%s' % (
        m.group(1), "lk" if m.group(2) == "K" else "ls", m.group(2), m.group(3)), text)


def make(out_name, extra=()):
    """Build the page with the changes of the third sample, then SITE, then extra, and write out_name."""
    portal.build([('"1-1-agentic-loops-ve.html"', '"%s"' % out_name)] + PORTAL + SITE + list(extra))
    out = os.path.join(HERE, out_name)
    with open(out, encoding="utf-8") as f:
        page = f.read()
    # square corners in the drawings too: each rect of the figures has rx="0"
    page, n = re.subn(r' rx="[0-9.]+"', ' rx="0"', page)
    # the K or S of each label in the text of the page, outside scripts and the title
    parts = re.split(r"(<script\b.*?</script>|<title>.*?</title>)", page, flags=re.S)
    page = "".join(x if x.startswith(("<script", "<title>")) else re.sub(r">([^<]*)<", lambda m: ">" + color_labels(m.group(1)) + "<", x)
                   for x in parts)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("Squared %d corners in the figures. Colored %d label letters." % (n, page.count('class="lk"') + page.count('class="ls"')))


if __name__ == "__main__":
    make("1-1-agentic-loops-site.html")
