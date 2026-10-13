"""Make the fifth sample page of task statement 1.1: academy/sample/1-1-agentic-loops-kit.html.

The fourth sample (make-1-1-site.py) with the colors of the MagnetLab brand kit only
(claude-code-brand-kit/brand-kit.md), which the owner asked for on 13 October 2026.
The layout, the fonts, the square corners and the content stay the same.

The rules of this version, from the proposal to the owner:
- Each color is a brand kit color. Thin lines and soft fills use a kit color made fainter.
- K uses the light blue #8BC4D9 that the kit shows (the owner said yes to it). S uses gold.
- Gold is never a text color. It marks lines only: the active path, the rule over each
  section, the underline of links and the focus ring. So gold on a letter means S only.
- The K or S of each label has a small solid fill with a navy letter, the same as its tag.
- The status colors (success, error, warning, info) mark borders. The words stay navy or cream.

Run from the folder ccar-f-mock-generator:
    python3 academy/sample/make-1-1-kit.py
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import theme  # noqa: E402

spec = importlib.util.spec_from_file_location("make_1_1_site", os.path.join(HERE, "make-1-1-site.py"))
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)

# brand kit sections 3.1 to 3.5
NAVY, NAVY2 = "#11293D", "#1A3E5C"                      # Primary, Secondary (as written)
GOLD, GOLD_TEXT = "#F3A83C", "#C07A1E"                  # Accent, Accent Text
CREAM, GREY, WHITE = "#F7F4E2", "#E0E0E0", "#FFFFFF"    # Primary Text, Secondary Text, Default Background
LIGHT_BLUE = "#8BC4D9"                                  # used in the kit, not named (section 3.5)
SUCCESS, ERROR, WARNING, INFO = "#28A745", "#DC3545", "#FFC107", "#17A2B8"

LIGHT = ("--bg: {w}; --surface: {c}; --border: {g}; --border-bright: color-mix(in srgb, {n2} 45%, {w}); "
         "--text: {n}; --text-dim: {n2}; --accent: {gt}; --accent-dim: color-mix(in srgb, {go} 22%, transparent); --gold: {go}; "
         "--ok: {su}; --risk: {er}; --warn: {wa}; --info: {inf}; --node-top: var(--surface); --lift: transparent; --halo: 0%; "
         "--k: {lb}; --s: {go}; --on-k: {n}; --on-s: {n};").format(
    w=WHITE, c=CREAM, g=GREY, n=NAVY, n2=NAVY2, gt=GOLD_TEXT, go=GOLD, su=SUCCESS, er=ERROR, wa=WARNING, inf=INFO, lb=LIGHT_BLUE)
DARK = ("--bg: {n}; --surface: {n2}; --border: color-mix(in srgb, {g} 18%, transparent); "
        "--border-bright: color-mix(in srgb, {g} 40%, transparent); "
        "--text: {c}; --text-dim: {g}; --accent: {go}; --accent-dim: color-mix(in srgb, {go} 16%, transparent); --gold: {go}; "
        "--ok: {su}; --risk: {er}; --warn: {wa}; --info: {inf}; --node-top: var(--surface); --lift: transparent; --halo: 0%; "
        "--k: {lb}; --s: {go}; --on-k: {n}; --on-s: {n};").format(
    n=NAVY, n2=NAVY2, g=GREY, c=CREAM, go=GOLD, su=SUCCESS, er=ERROR, wa=WARNING, inf=INFO, lb=LIGHT_BLUE)

KIT_CSS = (
    "  /* the brand kit colors: these rules come last, so they win over the colors above */\n"
    "  :root { " + LIGHT + " }\n  " + theme.scheme_css(DARK).replace("\n", "\n  ") +
    "@media print { :root, :root:not(.light), :root.dark { " + LIGHT + " } }\n"
    # gold is never a text color
    "  .eyebrow, .ve-cap li::before, details.level > summary::before, .kpi .val, .stops .in { color: var(--text); }\n"
    "  .ve-steps .ve-el.now { fill: var(--text); font-weight: 700; }\n"
    "  .scen li.on .sn { color: var(--text); }\n"
    "  a, .sources a, #pop .open { color: var(--text); text-decoration: underline; text-decoration-color: var(--gold);"
    " text-decoration-thickness: 2px; text-underline-offset: .2em; }\n"
    # status colors mark borders; the words stay navy or cream
    "  .eyebrow .src { color: var(--text); border-color: var(--ok); }\n"
    "  .try.bad .sub, .try.ok .sub, .ve-mini .is-st .sub { fill: var(--text-dim); }\n"
    "  .chip.ok, .chip.risk, .chip.info { color: var(--text); }\n"
    "  .chip.ok { border-color: var(--ok); } .chip.risk { border-color: var(--risk); } .chip.info { border-color: var(--info); }\n"
    "  .chip.ok::before { background: var(--ok); } .chip.risk::before { background: var(--risk); } .chip.info::before { background: var(--info); }\n"
    "  #pop .tag { color: var(--text); }\n"
    "  #pop .t-code, #pop .t-model { border-color: var(--accent); } #pop .t-owner { border-color: var(--ok); }"
    " #pop .t-fail { border-color: var(--risk); } #pop .t-open { border-color: var(--warn); }\n"
    # the slot with the most tries: gold fill, navy number
    "  .cell.t4 rect { fill: var(--gold); stroke: var(--gold); } .cell.t4 text { fill: " + NAVY + "; }\n"
    # the K or S of a label: a small solid fill, the same as its tag
    "  .lk, .ls { padding: 0 .12em; } .lk { background: var(--k); color: var(--on-k); } .ls { background: var(--s); color: var(--on-s); }\n"
    "</style>")

KIT = [
    ("</style>", KIT_CSS),
    ("Fourth sample: the third sample in the look of www.magnetlab.com.au, by academy/sample/make-1-1-site.py.",
     "Fifth sample: the fourth sample with the colors of the MagnetLab brand kit only, by academy/sample/make-1-1-kit.py."),
]

site.make("1-1-agentic-loops-kit.html", KIT)
