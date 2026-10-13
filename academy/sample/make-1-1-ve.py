"""Make the second sample page of task statement 1.1: academy/sample/1-1-agentic-loops-ve.html.

The same checked content as the first sample (make-1-1.py), drawn again in the
"Paper" register of the visual-explainer plugin: figures lead, text is caption.
This script runs the data part of make-1-1.py (everything above the line
"# ----- the page -----"), so the guide texts, the popups, the preview cards and
the counts of mock 1 are the same objects. It does not write the first sample.

Run from the folder ccar-f-mock-generator:
    python3 academy/sample/make-1-1-ve.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "make-1-1.py")
with open(SRC, encoding="utf-8") as f:
    code = f.read().split("# ----- the page -----")[0]
data = {"__file__": SRC, "__name__": "make_1_1_data"}
exec(compile(code, SRC, "exec"), data)

ROOT = data["ROOT"]
OUT = os.path.join(HERE, "1-1-agentic-loops-ve.html")
P, CARDS, POP = data["P"], data["CARDS"], data["POP"]
guide, domain, scen, ts = data["guide"], data["domain"], data["scen"], data["ts"]
per_slot = data["per_slot"]
TRIES_M1, SLOTS_M1, MORE_M1, MAX_M1, REWRITES_M1 = (data[k] for k in ("TRIES_M1", "SLOTS_M1", "MORE_M1", "MAX_M1", "REWRITES_M1"))
in_scope, TAG = data["in_scope"], data["TAG"]
e = html.escape


def fact(card, text):
    return '<span class="fact" tabindex="0" role="button" data-card="%s">%s</span>' % (card, e(text))


def node(step, x, y, w, h, title, sub=None, key=False, a=None, ref=None, glyph=None):
    attrs = ' data-step="%s" tabindex="0" role="button" aria-expanded="false"' % step if step else ""
    attrs += ' data-a="%s"' % a if a else ""
    attrs += ' data-ref="%s"' % ref if ref else ""
    out = '<g class="ve-n%s"%s transform="translate(%d %d)"><rect class="sh" width="%d" height="%d" rx="6"/>' % (
        " is-key" if key else "", attrs, x, y, w, h)
    if glyph:
        out += '<path class="gl" transform="translate(12 12)" d="%s"/>' % glyph
    if sub:
        out += '<text x="%d" y="%d">%s</text><text class="sub" x="%d" y="%d">%s</text>' % (w / 2, h / 2 - 11, e(title), w / 2, h / 2 + 13, e(sub))
    else:
        out += '<text x="%d" y="%d">%s</text>' % (w / 2, h / 2, e(title))
    return out + "</g>"


GL_CODE = "M5 2L0 8l5 6M11 2l5 6-5 6"
GL_CLAUDE = "M8 0v16M0 8h16M2.5 2.5l11 11M13.5 2.5l-11 11"

# ----- Fig. 1: the loop, as a stepper -----

blocks = [("user", "the task", 1), ("assistant", "tool_use: tool A", 2), ("user", "tool_result: A", 4),
          ("assistant", "tool_use: tool B", 5), ("user", "tool_result: B", 7), ("assistant", "text: the answer", 8)]
stack = "".join(
    '<g class="blk%s" data-s="%d" transform="translate(600 %d)"><rect width="280" height="32" rx="4"/>'
    '<text x="12" y="16"><tspan class="role">%s</tspan> %s</text></g>' % (" a" if r == "assistant" else "", s, 70 + i * 42, r, e(t))
    for i, (r, t, s) in enumerate(blocks))

FIG1 = """
<figure class="ve-steps" id="fig1">
  <div class="frame">
    <svg class="ve-svg" viewBox="0 20 900 350" role="img" aria-label="Your code sends a request to Claude. Claude responds. Your code checks stop_reason. On tool_use it runs the tool, adds the result to the conversation history and sends the next request. On end_turn the loop stops. The history on the right grows by one tool call and one result per iteration.">
      <path class="ve-e" data-a="1 5 8" pathLength="1" d="M210 76H328"/>
      <text class="ve-el" data-a="1 5 8" x="269" y="67">sends</text>
      <path class="ve-e" data-a="2 5 8" pathLength="1" d="M425 112V188"/>
      <text class="ve-el r" data-a="2 5 8" x="435" y="154">responds</text>
      <path class="ve-e is-hot" data-a="3 6" data-ref="tool" pathLength="1" d="M330 235H212"/>
      <text class="ve-el" data-a="3 6" data-ref="tool" x="271" y="226">"tool_use"</text>
      <path class="ve-e is-hot" data-a="4 7" data-ref="tool" pathLength="1" d="M115 199V114"/>
      <text class="ve-el r" data-a="4 7" data-ref="tool" x="125" y="160">adds the result</text>
      <path class="ve-e" data-a="9" data-ref="end" pathLength="1" d="M425 280V308"/>
      <text class="ve-el r" data-a="9" data-ref="end" x="435" y="299">"end_turn"</text>
      <path data-flow="loop" data-every="2600" d="M115 76H425V235H115V76"/>
      <g class="ve-dots" aria-hidden="true"></g>
      @@N_SEND@@ @@N_RESP@@
      <g class="ve-n is-key" data-step="check" tabindex="0" role="button" aria-expanded="false" data-a="3 6 9" data-ref="tool end">
        <path class="sh" d="M425 190L520 235L425 280L330 235Z"/><text x="425" y="226">stop_reason</text><text class="sub" x="425" y="249">checked</text></g>
      @@N_RUN@@ @@N_DONE@@
      <text class="ve-lab" x="600" y="52">conversation history</text>
      <g class="ve-n" data-step="convo" tabindex="0" role="button" aria-expanded="false"><rect class="hit" x="592" y="40" width="296" height="300" rx="8"/></g>
      @@STACK@@
    </svg>
  </div>
  <div class="ve-player">
    <ol class="ve-cap" aria-live="polite">
      <li data-n="9 steps">The full loop. Use the arrow buttons to go through it one step at a time.</li>
      <li data-n="1/9">Your code sends the task to Claude.</li>
      <li data-n="2/9">Claude responds: tool A.</li>
      <li data-n="3/9">Your code checks <code>stop_reason</code>: <code>"tool_use"</code>.</li>
      <li data-n="4/9">Your code runs tool A and adds the result to the conversation history.</li>
      <li data-n="5/9">Your code sends again. Claude responds: tool B.</li>
      <li data-n="6/9">Your code checks <code>stop_reason</code>: <code>"tool_use"</code>.</li>
      <li data-n="7/9">Your code runs tool B and adds the result to the conversation history.</li>
      <li data-n="8/9">Your code sends again. Claude responds: the answer.</li>
      <li data-n="9/9">Your code checks <code>stop_reason</code>: <code>"end_turn"</code>. The loop stops.</li>
    </ol>
    <button data-go="-1" aria-label="Previous step">&larr;</button>
    <button data-go="1" aria-label="Next step">&rarr;</button>
  </div>
  <figcaption><span class="fig-n">Fig. 1</span>The loop continues on <code>"tool_use"</code> and stops on <code>"end_turn"</code>. Each part opens its detail. The code of the loop is on <i>Your code sends the request</i>.</figcaption>
</figure>
"""
FIG1 = (FIG1.replace("@@N_SEND@@", node("send", 20, 40, 190, 72, "Your code", "sends the request", a="1 5 8", glyph=GL_CODE))
        .replace("@@N_RESP@@", node("resp", 330, 40, 190, 72, "Claude", "responds", a="2 5 8", glyph=GL_CLAUDE))
        .replace("@@N_RUN@@", node("run", 20, 199, 190, 72, "Your code", "runs the tool", a="4 7", ref="tool", glyph=GL_CODE))
        .replace("@@N_DONE@@", node("done", 330, 310, 190, 44, "Done", a="9", ref="end"))
        .replace("@@STACK@@", stack))

# ----- Fig. 2: the three wrong ways to stop, and the right one -----


def mini(signal, sub, st):
    return ('<svg class="ve-mini" viewBox="0 0 240 104" role="img" aria-label="The loop stops on: %s, %s">'
            '<path class="ve-e is-st" d="M112 52H150"/>'
            '<g class="ve-n is-st"><rect class="sh" x="2" y="20" width="110" height="64" rx="5"/><text x="57" y="42">%s</text>'
            '<text class="sub" x="57" y="64">%s</text></g>'
            '<g class="ve-n"><rect class="sh" x="152" y="32" width="84" height="40" rx="5"/><text x="194" y="52">stop</text></g></svg>'
            % (e(signal), e(sub), e(signal), e(sub)))


CASES = [("risk", "Anti-pattern", "Reads the words", mini("the words", "“I am done”", "risk"),
          "Parse natural language signals to decide when the loop ends."),
         ("risk", "Anti-pattern", "Counts to a limit", mini("a counter", "10 of 10", "risk"),
          "Make an arbitrary limit of iterations the main way to stop."),
         ("risk", "Anti-pattern", "Looks for text", mini("any text", "text block", "risk"),
          "Treat text from the assistant as the sign that the work is complete."),
         ("ok", "Correct", "Checks the field", mini("stop_reason", "“end_turn”", "ok"),
          "Continue on “tool_use”. Stop on “end_turn”.")]
FIG2 = ('<figure><div class="cases">' + "".join(
    '<div class="case" data-st="%s"><span class="chip %s">%s</span><h3>%s</h3>%s<p class="cap">%s</p></div>' % (st, st, chip, t, m, e(c))
    for st, chip, t, m, c in CASES) +
    '</div><figcaption><span class="fig-n">Fig. 2</span>The guide names three anti-patterns for the stop of the loop (1.1-S3). '
    'The loop continues and stops on <code>stop_reason</code> (1.1-S1).</figcaption></figure>')

# ----- Fig. 3: what the exam tests: domain weights and scenarios -----

doms = guide["domains"]
bars = []
for i, d in enumerate(doms):
    y = 8 + i * 34
    hot = d["id"] == domain["id"]
    bars.append('<text x="0" y="%d">Domain %d</text><rect class="%s" x="96" y="%d" width="%d" height="18" rx="2"/>'
                '<text class="%s" x="%d" y="%d">%d%%</text>' % (y + 9, d["id"], "hot" if hot else "", y, d["weight"] * 14,
                                                                "hv" if hot else "", 104 + d["weight"] * 14, y + 9, d["weight"]))
primary = {s["id"] for s in scen}
chips = "".join('<li class="%s"><span class="sn">%d</span>%s</li>' % ("on" if s["id"] in primary else "", s["id"], e(s["name"]))
                for s in guide["scenarios"])
FIG3 = """
<figure>
  <div class="frame split">
    <div><p class="ve-label">Approximate weight of each domain</p>
      <svg class="ve-bars wide" viewBox="0 0 520 176" role="img" aria-label="Domain weights: @@ARIA@@. Domain 1 is the largest.">@@BARS@@</svg></div>
    <div><p class="ve-label">Scenarios with domain 1 as a primary domain</p><ul class="scen">@@CHIPS@@</ul></div>
  </div>
  <figcaption><span class="fig-n">Fig. 3</span>Domain 1 is about @@W@@% of the scored items, the largest share (@@DFACT@@). Scenarios 1, 3 and 4 have it as a primary domain.</figcaption>
</figure>
"""
FIG3 = (FIG3.replace("@@BARS@@", "".join(bars)).replace("@@CHIPS@@", chips).replace("@@W@@", str(domain["weight"]))
        .replace("@@ARIA@@", ", ".join("domain %d %d%%" % (d["id"], d["weight"]) for d in doms))
        .replace("@@DFACT@@", fact("g-domain", "Section 4")))

# ----- Fig. 4: beyond the exam: the stop reasons of the API -----

stops = ["end_turn", "tool_use", "max_tokens", "stop_sequence", "pause_turn", "refusal", "model_context_window_exceeded"]
FIG4 = ('<figure><div class="frame"><p class="ve-label">stop_reason values of the Claude API</p><ul class="stops">' +
        "".join('<li class="%s"><code>"%s"</code>%s</li>' % ("on" if s in ("end_turn", "tool_use") else "", s,
                                                             '<span class="in">in the exam guide</span>' if s in ("end_turn", "tool_use") else "")
                for s in stops) +
        '</ul></div><figcaption><span class="fig-n">Fig. 4</span>The exam guide names two values. The API has %s. '
        'A loop in production must handle them too.</figcaption></figure>' % fact("d-stop", "seven"))

# ----- Fig. 5: Behind the mocks: tries, a pass, and the guards -----

FIG5 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 900 230" role="img" aria-label="Try 1 fails a check, try 2 fails a check, try 3 passes and the loop stops. A guard of 3 tries spans the three tries. After a guard the owner decides.">
      <path class="ve-e" d="M190 70H238"/><path class="ve-e" d="M410 70H458"/>
      <path class="ve-e is-hot" d="M630 70H698"/><text class="ve-el" x="664" y="61">stops</text>
      @@T1@@ @@T2@@ @@T3@@
      <g class="ve-n"><rect class="sh" x="700" y="40" width="180" height="60" rx="6"/><text x="790" y="70">passed</text></g>
      <g class="ve-dim"><path class="ext" d="M20 116V170M630 116V170"/><path class="ln" d="M20 160H630M16 164l8-8M626 164l8-8"/><text x="325" y="152">guard: at most 3 tries</text></g>
      <g class="ve-n guard" data-step="t-guard" tabindex="0" role="button" aria-expanded="false"><rect class="sh" x="20" y="182" width="610" height="40" rx="6"/>
        <text x="325" y="202">after a guard, the slot waits for the owner</text></g>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 5</span>A pass stops the loop. The limit of 3 tries is only a guard, and so is a limit of two results &ldquo;cannot decide&rdquo;. A drawing, not a real slot.</figcaption>
</figure>
"""


def tri(n, x, ok):
    return ('<g class="ve-n try %s" data-step="%s" tabindex="0" role="button" aria-expanded="false" transform="translate(%d 30)">'
            '<rect class="sh" width="170" height="80" rx="6"/><text x="85" y="29">Try %d</text><text class="sub" x="85" y="54">%s</text></g>'
            % ("ok" if ok else "bad", "t-pass" if ok else "t-fail", x, n, "passes" if ok else "fails a check"))


FIG5 = FIG5.replace("@@T1@@", tri(1, 20, False)).replace("@@T2@@", tri(2, 240, False)).replace("@@T3@@", tri(3, 460, True))

# ----- Fig. 6: who decides the next step -----

FIG6 = """
<figure>
  <div class="cases two">
    <div class="case"><span class="chip info">Task statement 1.1</span><h3>Agentic loop</h3>
      <svg class="ve-mini" viewBox="0 0 300 110" role="img" aria-label="In an agentic loop, Claude reasons about which tool to call next.">
        <path class="ve-e" d="M100 55H178"/><text class="ve-el" x="140" y="44">decides</text>
        <g class="ve-n is-st"><rect class="sh" x="2" y="25" width="98" height="60" rx="5"/><text x="51" y="55">Claude</text></g>
        <g class="ve-n"><rect class="sh" x="180" y="25" width="116" height="60" rx="5"/><text x="238" y="47">next step</text><text class="sub" x="238" y="69">which tool</text></g></svg></div>
    <div class="case" data-st="ok"><span class="chip ok">The mock builder</span><h3>Fixed sequence of steps</h3>
      <svg class="ve-mini" viewBox="0 0 300 110" role="img" aria-label="In the mock builder, code and the owner decide the next step. No model decides it.">
        <path class="ve-e is-st" d="M100 55H178"/><text class="ve-el" x="140" y="44">decide</text>
        <g class="ve-n is-st"><rect class="sh" x="2" y="10" width="98" height="40" rx="5"/><text x="51" y="30">code</text></g>
        <g class="ve-n is-st"><rect class="sh" x="2" y="60" width="98" height="40" rx="5"/><text x="51" y="80">the owner</text></g>
        <g class="ve-n"><rect class="sh" x="180" y="25" width="116" height="60" rx="5"/><text x="238" y="47">next step</text><text class="sub" x="238" y="69">from the plan</text></g></svg></div>
  </div>
  <figcaption><span class="fig-n">Fig. 6</span>The work of a mock is @@KNOWN@@: code makes @@SLOTS@@ before a model writes any question. So the builder uses the other side of the distinction in 1.1-K3.</figcaption>
</figure>
"""
FIG6 = FIG6.replace("@@KNOWN@@", fact("b-known", "known before it starts")).replace("@@SLOTS@@", fact("b-slots", "a plan of 60 slots"))

# ----- Fig. 7: the 60 slots of mock 1, by number of tries -----

slots = sorted(per_slot.items(), key=lambda kv: int(kv[0].split("S")[1]))
cells = []
for i, (sid, n) in enumerate(slots):
    x, y = (i % 15) * 34, (i // 15) * 34
    cells.append('<g class="cell t%d"><rect x="%d" y="%d" width="28" height="28" rx="3"/>%s<title>%s: %d %s</title></g>' % (
        min(n, 4), x, y, '<text x="%d" y="%d">%d</text>' % (x + 14, y + 15, n) if n > 1 else "", sid, n, "try" if n == 1 else "tries"))
FIG7 = """
<figure>
  <div class="frame split">
    <div><p class="ve-label">Mock 1: one square per slot, the number is the tries</p>
      <svg class="ve-grid" viewBox="0 0 510 136" role="img" aria-label="60 slots. @@MORE@@ slots needed more than one try. The most tries for one slot: @@MAX@@.">@@CELLS@@</svg></div>
    <div class="kpi"><span class="ve-label">Tries for 60 slots</span><span class="val">@@TRIES@@</span>
      <span class="ve-label">@@MORE@@ of 60 slots needed more than one try</span>
      <span class="ve-label">@@RW@@ tries were rewrites that the owner asked for</span></div>
  </div>
  <figcaption><span class="fig-n">Fig. 7</span>Mock 1 needed @@TFACT@@. @@STUCK@@</figcaption>
</figure>
"""
FIG7 = (FIG7.replace("@@CELLS@@", "".join(cells)).replace("@@MORE@@", str(MORE_M1)).replace("@@MAX@@", str(MAX_M1))
        .replace("@@TRIES@@", str(TRIES_M1)).replace("@@RW@@", str(REWRITES_M1))
        .replace("@@TFACT@@", fact("b-tries", "%d tries for %d slots" % (TRIES_M1, SLOTS_M1)))
        .replace("@@STUCK@@", fact("b-stuck", "One slot stopped at the guard, and the owner gave it more tries.")))

# ----- Fig. 8: the review cycle, and the fix -----

FIG8 = """
<figure>
  <div class="frame">
    <svg class="ve-svg" viewBox="0 0 900 150" role="img" aria-label="The first review found 14 serious items. The second review found 10 new ones. The fix: one automatic loop, each other failure waits for the owner, and the control is code with tests.">
      <path class="ve-e" d="M250 60H318"/><text class="ve-el" x="284" y="51">answers</text>
      <path class="ve-e is-hot" d="M560 60H628"/><text class="ve-el" x="594" y="51">fix</text>
      <g class="ve-n"><rect class="sh" x="20" y="20" width="230" height="80" rx="6"/><text x="135" y="44">first review</text>
        <rect class="bar" x="40" y="62" width="140" height="16" rx="2"/><text class="sub" x="210" y="70">14</text></g>
      <g class="ve-n"><rect class="sh" x="320" y="20" width="240" height="80" rx="6"/><text x="440" y="44">second review</text>
        <rect class="bar" x="340" y="62" width="100" height="16" rx="2"/><text class="sub r" x="452" y="70">10 new</text></g>
      <g class="ve-n is-key"><rect class="sh" x="630" y="20" width="250" height="80" rx="6"/><text x="755" y="44">the control is code</text><text class="sub" x="755" y="70">with tests</text></g>
      <text class="ve-lab" x="20" y="130">bar length = number of serious items</text>
    </svg>
  </div>
  <figcaption><span class="fig-n">Fig. 8</span>@@REV@@ The owner said: &ldquo;@@QUOTE@@&rdquo; The fix: @@ONE@@, and @@WAIT@@. The control became code, with @@TESTS@@.</figcaption>
</figure>
"""
FIG8 = (FIG8.replace("@@REV@@", fact("b-reviews", "A first review found 14 serious items. A second review found 10 new ones, and most of them came from the answers to the first."))
        .replace("@@QUOTE@@", fact("b-quote", "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue."))
        .replace("@@ONE@@", fact("b-oneloop", "one automatic loop")).replace("@@WAIT@@", fact("b-wait", "each other failure waits for the owner"))
        .replace("@@TESTS@@", fact("b-tests", "tests that make no model call")))

# ----- the guide text and the sources -----

glist = ('<p class="gh">Knowledge of:</p><ul class="glist">' +
         "".join('<li><span class="pid">%s</span> %s</li>' % (i, e(t)) for i, t in P.items() if "-K" in i) +
         '</ul><p class="gh">Skills in:</p><ul class="glist">' +
         "".join('<li><span class="pid">%s</span> %s</li>' % (i, e(t)) for i, t in P.items() if "-S" in i) + "</ul>")
sources = "".join('<li><a href="%s">%s</a> <span class="ve-label">%s</span></li>' % (e(c["href"]), e(c["title"]), e(c["src"]))
                  for c in CARDS.values())


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1.1 Agentic loops: the loop runs while Claude asks for tools</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23f7f7f4'/%3E%3Cpath d='M20 22h24v20H20z' fill='none' stroke='%232c4cd0' stroke-width='5'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500&family=Atkinson+Hyperlegible+Next:wght@400;600&family=Atkinson+Hyperlegible+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  /* tokens: Paper register (visual-explainer style guide) */
  :root {
    color-scheme: light dark;
    --bg: #f7f7f4; --surface: #ffffff; --border: #e3e3dc; --border-bright: #8e8e8a;
    --text: #17191c; --text-dim: #575c63; --accent: #2c4cd0; --accent-dim: rgba(44,76,208,.12);
    --ok: #1d7443; --warn: #836000; --risk: #b3301d; --info: #1b6a94;
    --node-top: var(--surface); --lift: rgb(18 22 20 / .12); --halo: 22%;
    --font-display: 'Newsreader', Georgia, serif;
    --font-body: 'Atkinson Hyperlegible Next', 'Segoe UI', sans-serif;
    --font-mono: 'Atkinson Hyperlegible Mono', ui-monospace, monospace;
    --t-label: .75rem; --t-small: .875rem; --t-body: 1rem; --t-lead: 1.25rem; --t-h2: 1.625rem; --t-h1: clamp(2.25rem, 5.5vw, 4rem);
    --s-1: .25rem; --s-2: .5rem; --s-3: .75rem; --s-4: 1rem; --s-5: 1.5rem; --s-6: 2rem; --s-7: 3rem; --s-8: 4.5rem;
    --r-1: 4px; --r-2: 10px;
    --ease: cubic-bezier(.16,1,.3,1); --fast: 150ms; --med: 300ms; --slow: 500ms;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #111316; --surface: #181b1f; --border: #262a30; --border-bright: #62676c;
      --text: #e8e8e3; --text-dim: #9ba1a9; --accent: #93a6ff; --accent-dim: rgba(147,166,255,.14);
      --ok: #6cc492; --warn: #e3b94d; --risk: #f0806b; --info: #6fb8dc;
      --node-top: color-mix(in srgb, var(--text) 7%, var(--surface)); --lift: rgb(0 0 0 / .45); --halo: 32%;
    }
  }
  html { font-size: 17px; }
  * { box-sizing: border-box; margin: 0; }
  body { background: var(--bg); color: var(--text); font: 400 var(--t-body)/1.6 var(--font-body); text-wrap: pretty; font-kerning: normal; font-synthesis: none; -webkit-font-smoothing: antialiased; }
  ::selection { background: var(--accent-dim); }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  main { max-width: 64rem; margin: 0 auto; padding: var(--s-7) var(--s-5) var(--s-8); display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--s-6); }
  section, figure, header, details { min-width: 0; }
  header { display: grid; gap: var(--s-4); }
  h1, h2 { font-family: var(--font-display); font-weight: 500; text-wrap: balance; }
  h1 { font-size: var(--t-h1); line-height: 1.05; letter-spacing: -.03em; max-width: 18ch; }
  h2 { font-size: var(--t-h2); line-height: 1.2; letter-spacing: -.01em; }
  h3 { font-size: var(--t-body); line-height: 1.3; font-weight: 600; }
  .eyebrow { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2) var(--s-3); font: 600 var(--t-label) var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
  .eyebrow::before { content: ''; width: 1.25rem; height: 2px; background: currentColor; }
  .eyebrow a { color: var(--text-dim); letter-spacing: 0; text-transform: none; font-weight: 500; }
  .eyebrow .src { color: var(--ok); border: 1px solid currentColor; border-radius: var(--r-1); padding: 0 var(--s-2); letter-spacing: .04em; }
  .ve-label { font: 500 var(--t-label) var(--font-mono); color: var(--text-dim); }
  .lead { font-size: var(--t-lead); line-height: 1.5; color: var(--text-dim); max-width: 46ch; }
  .lead b, .lead code { color: var(--text); }
  .gtitle { font-family: var(--font-display); font-style: italic; color: var(--text-dim); }
  p { max-width: 65ch; }
  code { font: .875em var(--font-mono); font-variant-ligatures: none; }
  .fact { text-decoration: underline dotted var(--text-dim) 1.5px; text-underline-offset: .22em; cursor: help; border-radius: var(--r-1); }
  .fact:hover, .fact[aria-expanded="true"] { text-decoration-color: var(--accent); background: var(--accent-dim); }
  .split-line { border: 0; border-top: 1px solid var(--border); margin: var(--s-6) 0 0; }

  /* levels: level 1 is the open header and figure; levels 2 and 3 are details */
  details.level { border-top: 1px solid var(--border); padding-top: var(--s-4); }
  details.level > summary { list-style: none; cursor: pointer; display: flex; align-items: baseline; gap: var(--s-3); }
  details.level > summary::-webkit-details-marker { display: none; }
  details.level > summary::before { content: '+'; font: 600 var(--t-lead) var(--font-mono); color: var(--accent); width: 1rem; }
  details.level[open] > summary::before { content: '\2212'; }
  details.level > summary h2 { font-size: var(--t-h2); }
  details.level > summary .ve-label { margin-left: var(--s-2); }
  details.level > .body { display: grid; gap: var(--s-6); margin-top: var(--s-5); grid-template-columns: minmax(0, 1fr); }
  .lvl1 { font: 600 var(--t-label) var(--font-mono); color: var(--text-dim); letter-spacing: .08em; text-transform: uppercase; }

  /* figures */
  .frame { background: radial-gradient(circle at 1px 1px, color-mix(in srgb, var(--text) 13%, transparent) 1px, transparent 1.5px) 0 0 / 20px 20px, var(--bg); border: 1px solid var(--border); border-radius: var(--r-2); padding: var(--s-5); overflow-x: auto; }
  .frame.split { display: grid; gap: var(--s-5); grid-template-columns: minmax(0, 1fr); }
  @media (min-width: 52rem) { .frame.split { grid-template-columns: 3fr 2fr; } }
  figcaption { color: var(--text-dim); margin-top: var(--s-3); max-width: 65ch; }
  .fig-n { font: 600 var(--t-label) var(--font-mono); color: var(--text); margin-right: var(--s-2); }
  .ve-svg { width: 100%; min-width: 700px; height: auto; display: block; font: 500 17px var(--font-body); }
  .ve-n .sh { fill: url(#ve-node); stroke: var(--border-bright); stroke-width: 1.5; filter: drop-shadow(0 6px 14px var(--lift)); transition: stroke var(--fast) var(--ease), opacity var(--med) var(--ease); }
  .ve-n.is-key .sh { fill: color-mix(in srgb, var(--accent) 11%, var(--surface)); stroke: var(--accent); stroke-width: 2; filter: drop-shadow(0 0 16px color-mix(in srgb, var(--accent) var(--halo), transparent)); }
  .ve-n text { fill: var(--text); text-anchor: middle; dominant-baseline: central; font-weight: 600; }
  .ve-n .sub { fill: var(--text-dim); font: 500 14px var(--font-mono); }
  .ve-n .gl { fill: none; stroke: var(--text-dim); stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; }
  .ve-n[data-step] { cursor: pointer; outline: none; }
  .ve-n[data-step]:hover .sh, .ve-n[data-step]:focus-visible .sh, .ve-n[aria-expanded="true"] .sh { stroke: var(--accent); stroke-width: 2.25; }
  .ve-n .hit { fill: transparent; stroke: var(--border); stroke-dasharray: 4 4; }
  .ve-e { fill: none; stroke: var(--text-dim); stroke-width: 1.75; marker-end: url(#ve-ah); }
  .ve-e.is-hot { stroke: var(--accent); stroke-width: 2.75; filter: drop-shadow(0 0 5px color-mix(in srgb, var(--accent) 45%, transparent)); }
  .ve-e.is-async { stroke-dasharray: 6 5; stroke-width: 1.25; }
  .ve-el { fill: var(--text-dim); font: 500 14px var(--font-mono); text-anchor: middle; paint-order: stroke; stroke: var(--bg); stroke-width: 5px; stroke-linejoin: round; }
  .ve-el.r { text-anchor: start; }
  .ve-lab { fill: var(--text-dim); font: 500 13px var(--font-mono); }
  .blk rect { fill: var(--surface); stroke: var(--border-bright); stroke-width: 1; }
  .blk.a rect { stroke: var(--accent); }
  .blk text { fill: var(--text); font: 500 14px var(--font-mono); dominant-baseline: central; }
  .blk .role { fill: var(--text-dim); }
  [data-flow] { fill: none; stroke: none; }
  .ve-dots circle { fill: var(--accent); filter: drop-shadow(0 0 4px var(--accent)); }
  .ve-steps:not(.is-full) .ve-dots { display: none; }
  .ve-dim path { fill: none; stroke-width: 1; } .ve-dim .ext { stroke: var(--border-bright); } .ve-dim .ln { stroke: var(--text-dim); }
  .ve-dim text { fill: var(--text); font: 500 14px var(--font-mono); text-anchor: middle; }
  .try.bad .sh { stroke: var(--risk); stroke-width: 2; } .try.bad .sub { fill: var(--risk); }
  .try.ok .sh { stroke: var(--ok); stroke-width: 2; } .try.ok .sub { fill: var(--ok); }
  .guard .sh { stroke-dasharray: 6 5; stroke: var(--warn); filter: none; }
  .bar { fill: var(--border-bright); }
  .ve-n .sub.r { text-anchor: start; }

  /* linked highlighting */
  .ve-ref { text-decoration: underline dotted var(--text-dim) 1px; text-underline-offset: .22em; border-radius: var(--r-1); transition: background var(--fast) var(--ease); }
  .ve-ref.is-lit { background: var(--accent-dim); text-decoration-color: var(--accent); }
  svg.has-lit path[data-ref]:not(.is-lit), svg.has-lit g[data-ref]:not(.is-lit) .sh { opacity: .25; }
  svg.has-lit text[data-ref]:not(.is-lit) { fill: var(--text-dim); }
  .ve-e.is-lit { stroke: var(--accent); } .ve-n.is-lit .sh { stroke: var(--accent); }

  /* stepper */
  .ve-steps [data-a], .ve-steps [data-s] { transition: opacity var(--med) var(--ease); }
  .ve-steps.is-step [data-a]:not(.now) { opacity: .35; }
  .ve-steps.is-step [data-s]:not(.on) { opacity: 0; }
  .ve-steps .ve-n.now .sh { stroke: var(--accent); stroke-width: 2.25; }
  .ve-steps .ve-e.now { stroke: var(--accent); stroke-width: 2.75; }
  .ve-steps .ve-el.now { fill: var(--accent); }
  .ve-steps .blk.now rect { fill: var(--accent-dim); stroke: var(--accent); stroke-width: 2; }
  .js-motion .ve-steps.is-step .ve-e.now { stroke-dasharray: 1; animation: ve-draw var(--slow) var(--ease); }
  @keyframes ve-draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
  .ve-player { display: grid; grid-template-columns: auto auto minmax(0, 1fr); align-items: center; gap: var(--s-2) var(--s-3); margin-top: var(--s-4); }
  .ve-cap { grid-column: 1 / -1; list-style: none; padding: 0; min-height: 3.2em; }
  .ve-cap li::before { content: attr(data-n); font: 600 var(--t-label) var(--font-mono); color: var(--accent); margin-right: var(--s-3); font-variant-numeric: tabular-nums; }
  button { font: 500 var(--t-small) var(--font-mono); color: var(--text); background: var(--surface); border: 1px solid var(--border-bright); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); cursor: pointer; }
  button:hover, button:focus-visible { border-color: var(--accent); }

  /* small multiples */
  .cases { display: grid; grid-template-columns: repeat(auto-fit, minmax(14.5rem, 1fr)); gap: var(--s-4); }
  .cases.two { grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); }
  .case { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-2); padding: var(--s-4); display: grid; gap: var(--s-3); align-content: start; }
  .case[data-st=ok] { --st: var(--ok); } .case[data-st=risk] { --st: var(--risk); } .case:not([data-st]) { --st: var(--info); }
  .case .cap { color: var(--text-dim); font-size: var(--t-small); }
  .ve-mini { width: 100%; height: auto; font: 600 15px var(--font-body); }
  .ve-mini .ve-n .sh { filter: none; } .ve-mini .ve-n .sub { font-size: 13px; }
  .ve-mini .is-st.ve-e { stroke: var(--st); stroke-width: 2.75; }
  .ve-mini .is-st .sh { stroke: var(--st); stroke-width: 2; } .ve-mini .is-st .sub { fill: var(--st); }
  .chip { display: inline-flex; align-items: center; gap: var(--s-2); font: 600 var(--t-label) var(--font-mono); padding: 2px var(--s-2); border: 1px solid currentColor; border-radius: var(--r-1); white-space: nowrap; justify-self: start; }
  .chip::before { content: ''; width: .5rem; height: .5rem; background: currentColor; }
  .chip.ok { color: var(--ok); } .chip.ok::before { border-radius: 50%; }
  .chip.risk { color: var(--risk); }
  .chip.info { color: var(--info); } .chip.info::before { transform: rotate(45deg) scale(.85); }

  /* bars, scenarios, stop reasons, grid */
  .ve-bars { width: 100%; height: auto; font: 500 13px var(--font-mono); overflow: visible; }
  .ve-bars text { fill: var(--text-dim); dominant-baseline: central; }
  .ve-bars rect { fill: var(--border-bright); }
  .ve-bars rect.hot { fill: var(--accent); } .ve-bars text.hv { fill: var(--text); font-weight: 600; }
  .scen, .stops { list-style: none; padding: 0; display: grid; gap: var(--s-2); margin-top: var(--s-3); }
  .scen li { display: flex; gap: var(--s-3); align-items: baseline; color: var(--text-dim); }
  .scen li.on { color: var(--text); font-weight: 600; }
  .scen .sn { font: 600 var(--t-label) var(--font-mono); border: 1px solid var(--border-bright); border-radius: var(--r-1); padding: 0 var(--s-2); }
  .scen li.on .sn { border-color: var(--accent); color: var(--accent); }
  .stops { grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr)); }
  .stops li { border: 1px dashed var(--border-bright); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); color: var(--text-dim); display: grid; }
  .stops li.on { border: 2px solid var(--accent); color: var(--text); }
  .stops .in { font: 500 var(--t-label) var(--font-mono); color: var(--accent); }
  .ve-grid { width: 100%; max-width: 30rem; height: auto; font: 600 13px var(--font-mono); }
  .cell rect { fill: var(--surface); stroke: var(--border-bright); }
  .cell.t2 rect { fill: color-mix(in srgb, var(--accent) 25%, var(--surface)); stroke: var(--accent); }
  .cell.t3 rect { fill: color-mix(in srgb, var(--accent) 50%, var(--surface)); stroke: var(--accent); }
  .cell.t4 rect { fill: var(--accent); stroke: var(--accent); }
  .cell text { fill: var(--text); text-anchor: middle; dominant-baseline: central; }
  .cell.t4 text { fill: var(--surface); }
  .kpi { display: grid; gap: var(--s-2); align-content: start; }
  .kpi .val { font: 600 2.75rem/1 var(--font-body); font-variant-numeric: tabular-nums; letter-spacing: -.04em; color: var(--accent); }

  .gh { font-weight: 600; margin-top: var(--s-3); }
  .glist { list-style: none; padding: 0; display: grid; gap: var(--s-2); margin-top: var(--s-2); }
  .glist li { padding-left: var(--s-3); border-left: 2px solid var(--border-bright); max-width: 75ch; }
  .pid { font: 600 var(--t-label) var(--font-mono); margin-right: var(--s-2); }
  .callout { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-2); padding: var(--s-4); display: grid; gap: var(--s-3); }
  .callout .chip { color: var(--text-dim); }
  .sources { border-top: 1px solid var(--border); padding-top: var(--s-4); display: grid; gap: var(--s-2); }
  .sources ul { list-style: none; padding: 0; display: grid; gap: var(--s-1); }
  .sources a { color: var(--accent); }

  /* popups and preview cards */
  #pop { position: fixed; z-index: 10; width: 26rem; max-width: calc(100vw - 16px); max-height: calc(100vh - 16px); overflow: auto; background: var(--surface); color: var(--text); border: 1px solid var(--border-bright); border-radius: var(--r-2); box-shadow: 0 12px 32px var(--lift); padding: var(--s-4); font-size: var(--t-small); line-height: 1.5; }
  #pop[hidden] { display: none; }
  #pop .ptop { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--s-3); }
  #pop .tag { font: 600 var(--t-label) var(--font-mono); padding: 2px var(--s-2); border: 1px solid currentColor; border-radius: var(--r-1); color: var(--text-dim); }
  #pop .t-code, #pop .t-model { color: var(--accent); } #pop .t-owner { color: var(--ok); } #pop .t-fail { color: var(--risk); } #pop .t-open { color: var(--warn); }
  #pop h2 { font: 600 var(--t-body) var(--font-body); margin: var(--s-3) 0 var(--s-2); }
  #pop h3 { font: 600 var(--t-label) var(--font-mono); text-transform: uppercase; letter-spacing: .08em; color: var(--text-dim); margin: var(--s-4) 0 var(--s-2); }
  #pop p { margin-bottom: var(--s-2); }
  #pop ul { list-style: none; padding: 0; display: grid; gap: var(--s-2); }
  #pop li { padding-left: var(--s-3); border-left: 2px solid var(--border-bright); }
  #pop .pctx { display: block; font-size: var(--t-label); color: var(--text-dim); }
  #pop pre { padding: var(--s-3); border-radius: var(--r-1); background: var(--bg); border: 1px solid var(--border); font: 12.5px/1.45 var(--font-mono); white-space: pre-wrap; overflow-wrap: anywhere; }
  #pop blockquote { padding: var(--s-2) var(--s-3); border-left: 2px solid var(--accent); background: var(--bg); }
  #pop .exnote, #pop .csrc { font: 500 var(--t-label) var(--font-mono); color: var(--text-dim); margin-top: var(--s-2); }
  #pop .open { display: inline-block; margin-top: var(--s-3); font-weight: 600; color: var(--accent); }
  #pop .pinned { font: 500 var(--t-label) var(--font-mono); color: var(--text-dim); margin-left: var(--s-2); }
  #popclose { width: 2rem; height: 2rem; padding: 0; font-size: 1.1rem; line-height: 1; }

  .js-motion main > * { transition: opacity var(--slow) var(--ease), transform var(--slow) var(--ease); }
  .js-motion main > :not(.in) { opacity: 0; transform: translateY(1rem); }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
  @media print {
    :root { --bg: #fff; --surface: #fff; --text: #17191c; --text-dim: #575c63; --accent: #2c4cd0; --border: #e3e3dc; --border-bright: #8e8e8a; }
    .ve-player button, .ve-dots, #pop { display: none; }
    .frame { overflow: visible; background: #fff; } .ve-svg { min-width: 0; } svg * { filter: none !important; }
    .js-motion main > * { opacity: 1 !important; transform: none !important; }
    figure, .case { break-inside: avoid; }
  }
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="ve-ah" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker>
  <linearGradient id="ve-node" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--node-top)"/><stop offset="1" style="stop-color:var(--surface)"/></linearGradient>
</defs></svg>
<main>

<!-- ============ Exam guide breakdown 1.1 ============ -->
<header id="ts">
  <p class="eyebrow">Exam guide breakdown &middot; Domain 1 &middot; Task statement 1.1 <a href="#behind">Behind the mocks 1.1 &darr;</a></p>
  <h1>The loop runs while Claude asks for tools</h1>
  <p class="gtitle">&ldquo;@@TS_TITLE@@&rdquo;</p>
  <p class="lead">Your code sends a request to Claude and checks <code>stop_reason</code>. <b class="ve-ref" data-ref="tool" tabindex="0"><code>"tool_use"</code>: run the tool and send the result back.</b> <b class="ve-ref" data-ref="end" tabindex="0"><code>"end_turn"</code>: stop.</b></p>
  <p class="lvl1">Overview &middot; 30 seconds</p>
</header>
@@FIG1@@

<details class="level">
  <summary><h2>Explanation</h2><span class="ve-label">3 minutes</span></summary>
  <div class="body">
    <p><b>Who decides.</b> The guide makes a distinction. In model-driven decision-making, Claude reasons about which tool to call next, from the context. The other side is a decision tree or a sequence of tools that somebody sets up in advance. <b>The memory of the loop:</b> your code adds each tool result to the conversation history, so that Claude can use the new information when it decides the next action.</p>
    @@FIG2@@
    @@FIG3@@
    <div><h3>The exam tests</h3><p>@@SCOPE@@</p></div>
    <div><h3>The guide&rsquo;s own text</h3><p class="ve-label">The labels 1.1-K1 to 1.1-S3 are ours. The guide has no labels.</p>@@GLIST@@</div>
  </div>
</details>

<details class="level">
  <summary><h2>Depth</h2></summary>
  <div class="body">
    <p><b>The loop in code.</b> Put the pointer on <i>Your code sends the request</i> in Fig. 1, or tap it. The popup shows the loop in Python.</p>
    <div class="callout"><span class="chip">Beyond the exam</span>@@FIG4@@</div>
    <p><b>On a real system.</b> The mock builder made a deliberate choice about loops. <a href="#behind">Behind the mocks 1.1 &darr;</a></p>
  </div>
</details>

<hr class="split-line">

<!-- ============ Behind the mocks 1.1 ============ -->
<header id="behind">
  <p class="eyebrow">Behind the mocks &middot; 1.1 Agentic loops <span class="src">Source: the pipeline</span> <a href="#ts">Task statement 1.1 &uarr;</a></p>
  <h1>A pass stops the loop. The limits are only guards.</h1>
  <p class="lead">The mock builder is not an agentic loop. <b>Code and the owner decide each next step.</b> No model decides it. The builder has one small loop: a question that fails a check goes back to the writer.</p>
  <p class="lvl1">Overview &middot; 30 seconds</p>
</header>
@@FIG5@@

<details class="level">
  <summary><h2>The story</h2><span class="ve-label">3 minutes</span></summary>
  <div class="body">
    @@FIG6@@
    <p>A question that fails the check by code or the check by a model goes back to the writer with the exact findings. A @@GUARD@@ and a limit of two results &ldquo;cannot decide&rdquo; are only guards. This follows 1.1-S3: an arbitrary limit of iterations must not be the main way to stop. The guide wrote that point for agent loops. The builder uses the same idea for a loop of retries.</p>
    @@FIG7@@
    @@FIG8@@
  </div>
</details>

<details class="level">
  <summary><h2>Depth</h2></summary>
  <div class="body">
    <p><b>The code.</b> Put the pointer on <i>Try 3</i> or on the guard in Fig. 5. The popups show the lines of the control that make a pass stop the loop first, and the limit of tries.</p>
    <p><b>The tests.</b> Each case of the control is a test, for example @@TESTNAME@@.</p>
  </div>
</details>

<section class="sources" aria-label="Sources">
  <p class="ve-label">Sources. Each underlined fact opens its card. The links open the files at the tag <code>@@TAG@@</code>.</p>
  <ul>@@SOURCES@@</ul>
  <p class="ve-label">Second sample, drawn with the visual-explainer plugin by academy/sample/make-1-1-ve.py. The content is the checked content of the first sample.</p>
</section>

</main>
<div id="pop" role="dialog" aria-labelledby="poptitle" hidden>
  <div class="ptop"><span><span id="popwho" class="tag"></span><span id="poppin" class="pinned"></span></span>
    <button id="popclose" type="button" aria-label="Close">&times;</button></div>
  <h2 id="poptitle"></h2>
  <div id="popbody"></div>
</div>
<script type="application/json" id="popdata">@@POPDATA@@</script>
<script type="application/json" id="carddata">@@CARDDATA@@</script>
<script>
(function () {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* popups (data-step) and preview cards (data-card) */
  const POP = JSON.parse(document.getElementById('popdata').textContent);
  const CARD = JSON.parse(document.getElementById('carddata').textContent);
  const pop = document.getElementById('pop');
  const OPEN_DELAY = 300, CLOSE_DELAY = 350, GAP = 10, EDGE = 8;
  let current = null, pinned = false, openTimer = null, closeTimer = null;
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  function fillStep(d) {
    const who = document.getElementById('popwho'); who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    const s = document.getElementById('popbody'); s.textContent = '';
    d.sent.forEach((t) => s.appendChild(el('p', null, t)));
    if (d.example) { s.appendChild(el('h3', null, d.examplehead)); s.appendChild(el('pre', null, d.example)); if (d.examplenote) s.appendChild(el('p', 'exnote', d.examplenote)); }
    if (d.points.length) { s.appendChild(el('h3', null, 'The exam guide says')); const ul = el('ul');
      d.points.forEach((p) => { const li = el('li'); li.appendChild(el('b', null, p.id + ' ')); li.appendChild(document.createTextNode(p.text)); li.appendChild(el('span', 'pctx', p.ctx)); ul.appendChild(li); });
      s.appendChild(ul); }
  }
  const KIND = { excerpt: 'Source', code: 'Code', guide: 'Exam guide', docs: 'Anthropic docs', count: 'Run records' };
  function fillCard(c) {
    const who = document.getElementById('popwho'); who.className = 'tag ' + (c.kind === 'code' ? 't-code' : c.kind === 'guide' ? 't-model' : '');
    who.textContent = KIND[c.kind] || 'Source';
    document.getElementById('poptitle').textContent = c.title;
    const s = document.getElementById('popbody'); s.textContent = '';
    if (c.kind === 'code') s.appendChild(el('pre', null, c.text)); else { const q = el('blockquote'); q.textContent = c.text; s.appendChild(q); }
    s.appendChild(el('p', 'csrc', c.src));
    const a = el('a', 'open', c.kind === 'docs' ? 'Open the page' : 'Open in the repository'); a.href = c.href; a.target = '_blank'; a.rel = 'noopener'; s.appendChild(a);
  }
  function place() {
    if (!current) return;
    const b = current.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    const pw = pop.offsetWidth, ph = pop.offsetHeight; let left, top;
    if (current.classList.contains('fact')) { left = b.left; top = b.bottom + 6; if (top + ph > vh - EDGE) top = b.top - 6 - ph; }
    else if (b.right + GAP + pw <= vw - EDGE) { left = b.right + GAP; top = b.top; }
    else if (b.left - GAP - pw >= EDGE) { left = b.left - GAP - pw; top = b.top; }
    else if (b.bottom + GAP + ph <= vh - EDGE) { left = b.left; top = b.bottom + GAP; }
    else { left = b.left; top = b.top - GAP - ph; }
    pop.style.left = Math.max(EDGE, Math.min(left, vw - pw - EDGE)) + 'px';
    pop.style.top = Math.max(EDGE, Math.min(top, vh - ph - EDGE)) + 'px';
  }
  const setPinned = (v) => { pinned = v; document.getElementById('poppin').textContent = v ? 'kept open' : ''; };
  function open(t, pin) {
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (current && current !== t) current.setAttribute('aria-expanded', 'false');
    current = t;
    if (t.dataset.step) fillStep(POP[t.dataset.step]); else fillCard(CARD[t.dataset.card]);
    pop.hidden = false; pop.scrollTop = 0; t.setAttribute('aria-expanded', 'true'); setPinned(pin); place();
  }
  function close(returnFocus) {
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (!current) return;
    const t = current; t.setAttribute('aria-expanded', 'false'); pop.hidden = true; current = null; setPinned(false);
    if (returnFocus) t.focus({ preventScroll: true });
  }
  function scheduleClose() {
    clearTimeout(closeTimer); if (pinned) return;
    closeTimer = setTimeout(() => {
      if (pinned) return;
      if (current && (current.matches(':hover') || pop.matches(':hover'))) return;
      if (current && (document.activeElement === current || pop.contains(document.activeElement))) return;
      close(false);
    }, CLOSE_DELAY);
  }
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) { e.preventDefault(); close(true); } });
  document.querySelectorAll('[data-step],[data-card]').forEach((t) => {
    t.addEventListener('mouseenter', () => { clearTimeout(closeTimer); if (pinned || current === t) return; clearTimeout(openTimer); openTimer = setTimeout(() => { if (!pinned) open(t, false); }, OPEN_DELAY); });
    t.addEventListener('mouseleave', () => { clearTimeout(openTimer); scheduleClose(); });
    t.addEventListener('click', (e) => { e.stopPropagation(); if (current === t && pinned) close(false); else open(t, true); });
    t.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (current === t && pinned) close(true); else open(t, true); } });
    t.addEventListener('blur', () => { if (!pinned) scheduleClose(); });
  });
  document.addEventListener('click', (e) => { if (current && !pop.contains(e.target)) close(false); });
  pop.addEventListener('mouseenter', () => clearTimeout(closeTimer));
  pop.addEventListener('mouseleave', scheduleClose);
  document.getElementById('popclose').addEventListener('click', (e) => { e.stopPropagation(); close(true); });
  addEventListener('scroll', place, true); addEventListener('resize', place);

  /* linked highlighting */
  const linked = [...document.querySelectorAll('[data-ref]')], refs = (x) => x.dataset.ref.split(' ');
  let hovered = null, focused = null;
  const paint = () => {
    const keys = (hovered || focused)?.dataset.ref.split(' ') ?? [];
    for (const t of linked) t.classList.toggle('is-lit', refs(t).some((k) => keys.includes(k)));
    for (const svg of document.querySelectorAll('svg')) svg.classList.toggle('has-lit', !!svg.querySelector('.is-lit'));
  };
  for (const x of document.querySelectorAll('.ve-ref')) {
    x.addEventListener('pointerenter', () => { hovered = x; paint(); }); x.addEventListener('pointerleave', () => { hovered = null; paint(); });
    x.addEventListener('focus', () => { focused = x; paint(); }); x.addEventListener('blur', () => { focused = null; paint(); });
  }

  /* stepper: opens on the full picture (k = 0); the arrows go one step at a time; nothing plays by itself */
  for (const root of document.querySelectorAll('.ve-steps')) {
    const parts = [...root.querySelectorAll('[data-a]')], lines = [...root.querySelectorAll('[data-s]')], caps = [...root.querySelectorAll('.ve-cap li')];
    const n = caps.length; let i = 0;
    const show = (k) => {
      i = Math.max(0, Math.min(n - 1, k));
      const full = i === 0;
      for (const p of parts) p.classList.toggle('now', !full && p.dataset.a.split(' ').includes(String(i)));
      for (const l of lines) { l.classList.toggle('on', full || +l.dataset.s <= i); l.classList.toggle('now', !full && +l.dataset.s === i); }
      caps.forEach((c, j) => c.hidden = j !== i);
      root.classList.toggle('is-full', full); root.classList.toggle('is-step', !full);
      root.dispatchEvent(new Event('ve:step'));
    };
    root.addEventListener('click', (e) => { const b = e.target.closest('[data-go]'); if (b) show(i + +b.dataset.go); });
    show(0);
  }

  if (!still) {
    /* flow dots: one dot goes round the loop while the full picture shows */
    for (const svg of document.querySelectorAll('svg:has([data-flow])')) {
      const layer = svg.querySelector('.ve-dots'), steps = svg.closest('.ve-steps');
      const routes = [...svg.querySelectorAll('[data-flow]')].map((p) => ({ p, len: p.getTotalLength(), every: +p.dataset.every, next: 0 }));
      let dots = [], visible = false, running = false;
      const live = () => visible && (!steps || steps.classList.contains('is-full'));
      const tick = (t) => {
        if (!live()) { running = false; for (const d of dots) d.c.remove(); dots = []; return; }
        for (const r of routes) if (t >= r.next) { r.next = t + r.every; const c = document.createElementNS(svg.namespaceURI, 'circle'); c.setAttribute('r', 5); layer.append(c); dots.push({ c, r, t0: t }); }
        dots = dots.filter((d) => { const s = (t - d.t0) * .45; if (s > d.r.len) { d.c.remove(); return false; } const pt = d.r.p.getPointAtLength(s); d.c.setAttribute('cx', pt.x); d.c.setAttribute('cy', pt.y); return true; });
        requestAnimationFrame(tick);
      };
      const start = () => { if (!running && live()) { running = true; requestAnimationFrame(tick); } };
      steps?.addEventListener('ve:step', start);
      new IntersectionObserver(([en]) => { visible = en.isIntersecting; start(); }).observe(svg);
    }
    document.documentElement.classList.add('js-motion');
    const io = new IntersectionObserver((entries) => { for (const en of entries) if (en.isIntersecting) { io.unobserve(en.target); en.target.classList.add('in'); } }, { rootMargin: '0px 0px -10% 0px' });
    for (const x of document.querySelectorAll('main > *')) io.observe(x);
  }
})();
</script>
</body>
</html>
"""

out = (PAGE.replace("@@TS_TITLE@@", e(ts["title"])).replace("@@FIG1@@", FIG1).replace("@@FIG2@@", FIG2).replace("@@FIG3@@", FIG3)
       .replace("@@FIG4@@", FIG4).replace("@@FIG5@@", FIG5).replace("@@FIG6@@", FIG6).replace("@@FIG7@@", FIG7).replace("@@FIG8@@", FIG8)
       .replace("@@SCOPE@@", "The guide lists this topic as tested: " + fact("g-scope", "“%s”" % in_scope) +
                ". Under the Claude API, its list of technologies names " + fact("g-tech", "“stop_reason values (\"tool_use\", \"end_turn\")”") + ".")
       .replace("@@GLIST@@", glist).replace("@@GUARD@@", fact("b-guard", "limit of 3 tries"))
       .replace("@@TESTNAME@@", fact("b-testname", "“more tries after three tries”")).replace("@@TAG@@", TAG)
       .replace("@@SOURCES@@", sources)
       .replace("@@POPDATA@@", json.dumps(POP, ensure_ascii=False).replace("</", "<\\/"))
       .replace("@@CARDDATA@@", json.dumps(CARDS, ensure_ascii=False).replace("</", "<\\/")))
assert "@@" not in out, out[out.find("@@") - 40: out.find("@@") + 40]
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print("Wrote %s: %d popups, %d cards." % (os.path.relpath(OUT, ROOT), len(POP), len(CARDS)))
