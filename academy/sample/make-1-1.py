"""Make the sample page of task statement 1.1: academy/sample/1-1-agentic-loops.html.

The page tests the decisions 0001 to 0006 of the portal work on one real page:
the three levels, a preview card for the source of each fact, code only in a
popup, and the label "Beyond the exam".

Each guide text comes from reference/guide-records.json. Each excerpt of a
preview card comes from its source file. The script stops with an error if a
text is not in its file, so an excerpt always agrees with its source. Each link
goes to the tag mocks-v2 on GitHub.

Run from the folder ccar-f-mock-generator:
    python3 academy/sample/make-1-1.py
"""
import glob
import html
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "academy", "sample", "1-1-agentic-loops.html")
REPO = "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator"
TAG = "mocks-v2"
DOCS_TOOL_USE = "https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works"
DOCS_STOP = "https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def link(path, a=None, b=None):
    plain = "?plain=1" if path.endswith(".md") else ""
    if a is None:
        return "%s/blob/%s/%s" % (REPO, TAG, path)
    return "%s/blob/%s/%s%s#L%d%s" % (REPO, TAG, path, plain, a, "-L%d" % b if b and b != a else "")


def lines_of(path, text):
    """The first and last line numbers of text in the file. Stops if text is not in the file."""
    content = read(path)
    i = content.find(text)
    if i < 0:
        raise SystemExit("Not in %s: %r" % (path, text[:80]))
    a = content.count("\n", 0, i) + 1
    return a, a + text.count("\n")


def excerpt(path, text, title, kind="excerpt", label=None):
    a, b = lines_of(path, text)
    return {"title": title, "kind": kind, "text": text, "src": label or "%s, line %s" % (path, a if a == b else "%d to %d" % (a, b)),
            "href": link(path, a, b)}


def code_block(path, first, last, title):
    """The lines from the line with first to the line with last, as they are in the file."""
    lines = read(path).split("\n")
    a = next(i for i, l in enumerate(lines) if first in l)
    b = next(i for i, l in enumerate(lines) if i >= a and last in l)
    text = "\n".join(lines[a:b + 1])
    indent = min(len(l) - len(l.lstrip()) for l in lines[a:b + 1] if l.strip())
    text = "\n".join(l[indent:] for l in lines[a:b + 1])
    return {"title": title, "kind": "code", "text": text, "src": "%s, %s" % (path, "line %d" % (a + 1) if a == b else "lines %d to %d" % (a + 1, b + 1)),
            "href": link(path, a + 1, b + 1)}


# ----- the guide -----

guide = json.loads(read("reference/guide-records.json"))
ts = next(t for t in guide["task_statements"] if t["id"] == "1.1")
domain = next(d for d in guide["domains"] if d["id"] == ts["domain"])
P = {p["id"]: p["text"] for p in ts["points"]}
in_scope = next(t for t in guide["section_17"]["in_scope"] if t.startswith("Agentic loop implementation"))
api_tech = next(t for t in guide["section_17"]["technologies"] if t.startswith("Claude API"))
scen = [s for s in guide["scenarios"] if ts["domain"] in s["primary_domains"]]
for t in [ts["title"], in_scope, api_tech] + list(P.values()):
    lines_of("reference/exam-guide.md", t)   # each guide text is exactly in the guide

# ----- the run of mock 1, counted from the files -----

names = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, "runs/mock-01/questions/*.json"))]
per_slot = Counter(re.match(r"(M1-S\d+)-T\d+", n).group(1) for n in names)
TRIES_M1, SLOTS_M1 = len(names), len(per_slot)
MORE_M1, MAX_M1 = sum(1 for v in per_slot.values() if v > 1), max(per_slot.values())
REWRITES_M1 = sum(1 for d in json.loads(read("runs/mock-01/owner-decisions.json")) if d.get("action") == "rewrite")
failed_slots = {re.match(r"(M1-S\d+)-T\d+", os.path.basename(f)).group(1)
                for f in glob.glob(os.path.join(ROOT, "runs/mock-01/checks/M1-S*-T*-step[34].json"))
                if json.loads(read(os.path.relpath(f, ROOT)))["verdict"] != "pass"}
FAILED_M1 = sum(1 for s, v in per_slot.items() if v > 1 and s in failed_slots)   # more than one try, after a failed check
RWONLY_M1 = MORE_M1 - FAILED_M1                                                   # more than one try, only after a rewrite

# ----- the preview cards -----

S1 = "docs/build-guide/step-1-plan-the-mock.md"
S5 = "docs/build-guide/step-5-try-again.md"
D38 = "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md"
CARDS = {
    "g-domain": excerpt("reference/exam-guide.md", "The percentages indicate the approximate proportion of scored items drawn from each domain.",
                        "Section 4, the exam blueprint", kind="guide"),
    "g-scope": excerpt("reference/exam-guide.md", in_scope, "In-Scope Topics, Section 17 (Appendix)", kind="guide"),
    "g-tech": excerpt("reference/exam-guide.md", api_tech, "Technologies and Concepts, Section 17 (Appendix)", kind="guide"),
    "d-stop": {"title": "Anthropic documentation: Handling stop reasons", "kind": "docs",
               "text": "The page names seven stop_reason values: end_turn, max_tokens, stop_sequence, tool_use, pause_turn, "
                       "refusal and model_context_window_exceeded. For tool_use it says: \"Claude is calling a tool and "
                       "expects you to run it.\"",
               "src": "platform.claude.com, read on 13 October 2026", "href": DOCS_STOP},
    "b-known": excerpt(S1, "the work of a mock is known before it starts, so the program can fix the plan before the writing starts",
                       "Build guide, step 1"),
    "b-slots": excerpt(S1, "Before a model writes a question, code makes the plan of the mock: a list of 60 slots.", "Build guide, step 1"),
    "b-guard": code_block("src/control.py", "TRIES = 3", "TRIES = 3", "The limit of tries in the code"),
    "b-passfirst": code_block("src/control.py", 'if v3["verdict"] == "pass" and v4["verdict"] == "pass":',
                              'state["status"] = "open" if state["open_reasons"] else "to_write"',
                              "The code: a pass stops the loop first"),
    "b-tries": {"title": "The run records of mock 1", "kind": "count",
                "text": "The folder runs/mock-01/questions/ has %d question files, one for each try, for %d slots. "
                        "%d slots have more than one try: %d after a failed check in runs/mock-01/checks/, and %d only after a "
                        "rewrite that the owner asked for. The most tries for one slot: %d. The file runs/mock-01/owner-decisions.json "
                        "has %d rewrites that the owner asked for. The script of this page counted the files."
                        % (TRIES_M1, SLOTS_M1, MORE_M1, FAILED_M1, RWONLY_M1, MAX_M1, REWRITES_M1),
                "src": "runs/mock-01/questions/", "href": "%s/tree/%s/runs/mock-01/questions" % (REPO, TAG)},
    "b-stuck": excerpt(S5, "One slot stopped after 3 tries. Each try had corrected the last finding, and a new small finding came. "
                           "The owner gave it more tries.", "Build guide, step 5, the run of mock 1"),
    "b-reviews": excerpt(D38, "The first review found 14 serious items. Decision 0037 answered them. The second review found 10 new "
                              "serious items, and most of them come from the rules of decision 0037.", "Mock decision 0038, Question"),
    "b-quote": excerpt(D38, "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue.",
                       "Mock decision 0038, How we decided"),
    "b-oneloop": excerpt(D38, "1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5.", "Mock decision 0038, Decision"),
    "b-wait": excerpt(D38, "2. **Each other failure waits for the owner.**", "Mock decision 0038, Decision"),
    "b-tests": excerpt(D38, "6. **The control is code.** It is one part of the program, with tests that make no model call.",
                       "Mock decision 0038, Decision"),
    "b-testname": code_block("tests/test_control.py", "def test_more_tries_after_three_tries_is_step_5_with_the_last_try",
                             "def test_more_tries_after_three_tries_is_step_5_with_the_last_try", "One of the tests of the control"),
}

# ----- the popups of the two diagrams -----

LOOP_CODE = '''messages = [{"role": "user", "content": task}]
while True:
    response = client.messages.create(
        model="claude-opus-5-5", max_tokens=16000,
        tools=tools, messages=messages)
    if response.stop_reason != "tool_use":
        break                     # "end_turn", or another reason to handle
    # stop_reason is "tool_use": run each tool that Claude asked for
    messages.append({"role": "assistant", "content": response.content})
    results = [{"type": "tool_result", "tool_use_id": block.id,
                "content": run_tool(block.name, block.input)}
               for block in response.content if block.type == "tool_use"]
    messages.append({"role": "user", "content": results})'''


def pts(*ids):
    return [{"id": i, "text": P[i], "ctx": "Task statement 1.1: " + ts["title"]} for i in ids]


POP = {
    "send": {"who": "Your code", "cls": "code", "title": "Your code sends the request",
             "sent": ["The request carries the conversation history, with each tool result."],
             "examplehead": "The loop in Python", "example": LOOP_CODE,
             "examplenote": "Simplified from the Anthropic documentation, page \"How tool use works\", section \"The agentic loop "
                            "(client tools)\" (" + DOCS_TOOL_USE + "), read on 13 October 2026. The exam guide has no code.",
             "points": pts("1.1-K1")},
    "resp": {"who": "Claude", "cls": "model", "title": "Claude responds",
             "sent": ["Claude reasons about which tool to call next, from the context."],
             "points": pts("1.1-K3")},
    "check": {"who": "Your code", "cls": "code", "title": "Your code checks stop_reason",
              "sent": ["\"tool_use\": the loop continues. \"end_turn\": the loop stops. Your code decides on this field, "
                       "not on the text of the answer."],
              "points": pts("1.1-K1", "1.1-S1", "1.1-S3")},
    "run": {"who": "Your code", "cls": "code", "title": "Your code runs the tool and adds the result",
            "sent": ["Your code runs the tool that Claude asked for. Then it adds the result to the conversation, so that Claude "
                     "can use the new information in its next step."],
            "points": pts("1.1-K2", "1.1-S2")},
    "done": {"who": "Your code", "cls": "owner", "title": "The loop stops",
             "sent": ["stop_reason is \"end_turn\", so your code stops the loop."],
             "points": pts("1.1-S1", "1.1-S3")},
    "convo": {"who": "The conversation", "cls": "io", "title": "The conversation grows",
              "sent": ["Each iteration adds the tool result to the conversation history, so that Claude can reason about the next action."],
              "points": pts("1.1-K2", "1.1-S2")},
    "t-fail": {"who": "The pipeline", "cls": "fail", "title": "A try that fails",
               "sent": ["The check by code (step 3) or the check by a model (step 4) finds a problem. The question goes back to the "
                        "writer with the exact findings, and the writer tries again."],
               "points": []},
    "t-pass": {"who": "The pipeline", "cls": "owner", "title": "A try that passes stops the loop",
               "sent": ["The control looks for a pass before it looks at the count of tries. So a pass always stops the loop."],
               "examplehead": "The code", "example": CARDS["b-passfirst"]["text"],
               "examplenote": CARDS["b-passfirst"]["src"] + ", at the tag " + TAG + ".",
               "points": pts("1.1-S3")},
    "t-guard": {"who": "The pipeline", "cls": "open", "title": "The guards: then the owner decides",
                "sent": ["The slot is open after 3 failed tries, or after the checker says \"cannot decide\" two times. It is also "
                         "open when the writer answers \"cannot write\". The loop stops, and the owner decides: more tries, a new "
                         "point, or a new plan. The number 3 is a guess, and the code says so."],
                "examplehead": "The code", "example": CARDS["b-guard"]["text"],
                "examplenote": CARDS["b-guard"]["src"] + ", at the tag " + TAG + ".",
                "points": pts("1.1-S3")},
}
for d in POP.values():
    d.setdefault("example", None)
    d.setdefault("examplehead", "")
    d.setdefault("examplenote", "")

# ----- the page -----

import sys  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme  # noqa: E402

e = html.escape


def fact(card, text):
    return '<span class="fact" tabindex="0" role="button" data-card="%s">%s</span>' % (card, e(text))


def guide_list():
    out = ['<p class="gh">Knowledge of:</p><ul class="glist">']
    out += ['<li><span class="pid">%s</span> %s</li>' % (i, e(t)) for i, t in P.items() if "-K" in i]
    out += ['</ul><p class="gh">Skills in:</p><ul class="glist">']
    out += ['<li><span class="pid">%s</span> %s</li>' % (i, e(t)) for i, t in P.items() if "-S" in i]
    out.append("</ul>")
    return "\n".join(out)


def hot(step, cls, x, y, w, h, inner):
    return ('<div class="node %s" data-step="%s" tabindex="0" role="button" aria-expanded="false" '
            'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>' % (cls, step, x, y, w, h, inner))


scen_list = ", ".join("%d. %s" % (s["id"], s["name"]) for s in scen)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>1.1 Agentic loops: sample page</title>
{theme_head}
<style>
:root {{
  --bg:#f6f7f9; --panel:#fff; --ink:#16202b; --muted:#556270; --line:#c5ccd4;
  --code:#1f5fae; --code-bg:#e4eefb; --model:#7a3fb0; --model-bg:#f1e7fa;
  --owner:#0f7a55; --owner-bg:#dff3ea; --open:#8a6100; --open-bg:#fbf0d2;
  --fail:#b3261e; --fail-bg:#fdecea; --shadow:0 10px 30px rgba(16,24,40,.22);
}}
{theme_css}
.theme-btn {{ position:absolute; top:10px; right:10px; z-index:5; font:600 13px system-ui,sans-serif; border:1.5px solid var(--line);
  background:var(--panel); color:var(--ink); border-radius:8px; padding:6px 10px; cursor:pointer; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif; }}
main {{ max-width:1000px; margin:0 auto; padding:56px 20px 60px; }}
.crumbs {{ font-size:13px; color:var(--muted); display:flex; flex-wrap:wrap; gap:6px 10px; align-items:center; }}
.crumbs a {{ color:var(--muted); }}
.section-tag {{ font-size:12px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:var(--code); }}
h1 {{ font-size:30px; margin:6px 0 2px; }}
.gtitle {{ color:var(--muted); margin:0 0 18px; font-style:italic; }}
.level {{ background:var(--panel); border:1.5px solid var(--line); border-radius:14px; margin:0 0 16px; }}
.level > summary, .level > .lhead {{ list-style:none; cursor:pointer; padding:14px 18px; display:flex; gap:12px; align-items:baseline; }}
.level > .lhead {{ cursor:default; }}
.level > summary::-webkit-details-marker {{ display:none; }}
.level > summary::before {{ content:"+"; font-weight:700; color:var(--muted); width:14px; }}
.level[open] > summary::before {{ content:"\\2212"; }}
.lname {{ font-weight:700; font-size:17px; }}
.ltime {{ font-size:13px; color:var(--muted); }}
.lbody {{ padding:0 18px 18px; }}
.lead {{ font-size:18px; margin:0 0 14px; max-width:70ch; }}
h2 {{ font-size:22px; margin:34px 0 4px; }}
h3 {{ font-size:16px; margin:20px 0 6px; }}
p {{ margin:0 0 10px; max-width:72ch; }}
code {{ font:14px ui-monospace,SFMono-Regular,Consolas,monospace; background:var(--bg); padding:1px 5px; border-radius:5px; }}
.fact {{ text-decoration:underline dotted var(--muted); text-underline-offset:4px; text-decoration-thickness:1.5px; cursor:help; }}
.fact:hover, .fact[aria-expanded="true"] {{ text-decoration-color:var(--ink); }}
.fact:focus-visible {{ outline:3px solid var(--code); outline-offset:2px; border-radius:3px; }}
.gh {{ font-weight:700; margin:12px 0 4px; }}
.glist {{ margin:0; padding:0; list-style:none; }}
.glist li {{ margin:0 0 8px; padding-left:12px; border-left:3px solid var(--line); max-width:80ch; }}
.pid {{ font-weight:700; font-variant-numeric:tabular-nums; margin-right:4px; }}
.beyond {{ border:1.5px dashed var(--line); border-radius:12px; padding:12px 16px; margin:12px 0; }}
.beyond .btag {{ display:inline-block; font-size:12px; font-weight:700; color:var(--muted); border:1.5px solid var(--line);
  border-radius:999px; padding:1px 10px; margin-bottom:6px; }}
.src {{ display:inline-block; font-size:12px; font-weight:700; padding:2px 10px; border-radius:999px; color:var(--owner); background:var(--owner-bg); }}
.xlink {{ display:inline-block; margin-top:6px; font-weight:600; color:var(--code); }}
.anti {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:10px; margin:10px 0 4px; }}
.anti div {{ border:1.5px solid var(--line); border-radius:10px; padding:10px 12px; font-size:14px; }}
.anti .no {{ border-color:var(--fail); background:var(--fail-bg); }}
.anti .yes {{ border-color:var(--owner); background:var(--owner-bg); }}
.anti b {{ display:block; margin-bottom:2px; }}
hr.split {{ border:0; border-top:1.5px solid var(--line); margin:40px 0 10px; }}

.scroll {{ overflow-x:auto; padding-bottom:4px; }}
.stage {{ position:relative; }}
.stage svg {{ position:absolute; inset:0; overflow:visible; }}
.node {{ position:absolute; background:var(--panel); border:1.5px solid var(--line); border-radius:10px; padding:9px 12px;
  cursor:pointer; transition:border-color .2s, box-shadow .2s, background .2s; font-size:14px; }}
.node b {{ display:block; font-size:15px; }}
.node .who {{ font-size:11.5px; font-weight:700; padding:1px 8px; border-radius:999px; display:inline-block; margin-bottom:3px; }}
.node:hover {{ border-color:var(--muted); }}
.node:focus-visible {{ outline:3px solid var(--code); outline-offset:2px; }}
.node[aria-expanded="true"] {{ box-shadow:0 0 0 2px var(--ink); }}
.node.on {{ border-color:var(--ink); box-shadow:0 0 0 3px var(--code-bg), 0 0 0 4.5px var(--code); }}
.w-code {{ color:var(--code); background:var(--code-bg); }}
.w-model {{ color:var(--model); background:var(--model-bg); }}
.node.model {{ background:var(--model-bg); border-color:var(--model); }}
.node.done {{ border-color:var(--owner); }}
.node.done.on {{ background:var(--owner-bg); }}
.sr {{ font:700 15px ui-monospace,SFMono-Regular,Consolas,monospace; color:var(--code); }}
.arrow {{ stroke:var(--muted); stroke-width:2; fill:none; transition:stroke .2s; }}
.arrow.on {{ stroke:var(--code); stroke-width:3; }}
.alab {{ position:absolute; font:600 12.5px ui-monospace,SFMono-Regular,Consolas,monospace; color:var(--muted); background:var(--panel); padding:0 4px; }}
.dot {{ fill:var(--code); }}
.convo {{ position:absolute; border:1.5px solid var(--line); border-radius:12px; padding:10px 12px; background:var(--bg); cursor:pointer; }}
.convo:focus-visible {{ outline:3px solid var(--code); outline-offset:2px; }}
.convo[aria-expanded="true"] {{ box-shadow:0 0 0 2px var(--ink); }}
.convo .ct {{ font-weight:700; font-size:14px; margin-bottom:6px; }}
.msg {{ font:12.5px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace; border-radius:8px; padding:5px 8px; margin:0 0 5px;
  border:1px solid var(--line); background:var(--panel); animation:pop .35s ease-out; }}
.msg.a {{ border-color:var(--model); }}
.msg i {{ font-style:normal; color:var(--muted); }}
@keyframes pop {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:none; }} }}
.controls {{ display:flex; gap:10px; align-items:center; margin:6px 0 0; font-size:14px; color:var(--muted); }}
.controls button {{ font:600 14px system-ui,sans-serif; border:1.5px solid var(--line); background:var(--panel); color:var(--ink);
  border-radius:8px; padding:5px 12px; cursor:pointer; }}
.controls button:hover {{ border-color:var(--ink); }}
.iter {{ position:absolute; font-size:13px; font-weight:700; color:var(--muted); }}

.try {{ position:absolute; border:1.5px solid var(--line); border-radius:12px; background:var(--panel); padding:10px 12px; cursor:pointer; text-align:center; }}
.try:focus-visible {{ outline:3px solid var(--code); outline-offset:2px; }}
.try[aria-expanded="true"] {{ box-shadow:0 0 0 2px var(--ink); }}
.try .tn {{ font-size:22px; font-weight:800; }}
.try.f {{ border-color:var(--fail); background:var(--fail-bg); color:var(--fail); }}
.try.p {{ border-color:var(--owner); background:var(--owner-bg); color:var(--owner); }}
.try small {{ display:block; font-size:12.5px; font-weight:600; }}
.guard {{ position:absolute; border:1.5px dashed var(--open); background:var(--open-bg); color:var(--ink); border-radius:12px; padding:8px 12px;
  font-size:14px; cursor:pointer; }}
.guard:focus-visible {{ outline:3px solid var(--code); outline-offset:2px; }}
.guard[aria-expanded="true"] {{ box-shadow:0 0 0 2px var(--ink); }}
.stopnote {{ position:absolute; font-weight:700; color:var(--owner); font-size:15px; }}

#pop {{ position:fixed; z-index:10; width:420px; max-width:calc(100vw - 16px); max-height:calc(100vh - 16px); overflow:auto;
  background:var(--panel); color:var(--ink); border:1.5px solid var(--ink); border-radius:12px; box-shadow:var(--shadow);
  padding:14px 16px; font-size:14px; line-height:1.45; }}
#pop[hidden] {{ display:none; }}
#pop .ptop {{ display:flex; justify-content:space-between; align-items:flex-start; gap:10px; }}
#pop .tag {{ font-size:12px; font-weight:600; padding:2px 9px; border-radius:999px; display:inline-block; }}
.t-code {{ color:var(--code); background:var(--code-bg); }} .t-model {{ color:var(--model); background:var(--model-bg); }}
.t-owner {{ color:var(--owner); background:var(--owner-bg); }} .t-open {{ color:var(--open); background:var(--open-bg); }}
.t-fail {{ color:var(--fail); background:var(--fail-bg); }} .t-io {{ color:var(--muted); background:var(--bg); box-shadow:inset 0 0 0 1px var(--line); }}
#pop h2 {{ font-size:17px; margin:8px 0 8px; }}
#pop h3 {{ font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); margin:14px 0 6px; }}
#pop p {{ margin:0 0 6px; }}
#pop ul {{ list-style:none; margin:0; padding:0; }}
#pop li {{ margin:0 0 8px; padding-left:10px; border-left:3px solid var(--line); }}
#pop .pctx {{ display:block; margin-top:2px; font-size:12px; color:var(--muted); }}
#pop pre {{ margin:0; padding:8px 10px; border-radius:8px; background:var(--bg); border:1px solid var(--line);
  font:12px/1.45 ui-monospace,SFMono-Regular,Consolas,monospace; white-space:pre-wrap; overflow-wrap:anywhere; }}
#pop blockquote {{ margin:0; padding:8px 12px; border-left:3px solid var(--ink); background:var(--bg); border-radius:0 8px 8px 0; }}
#pop .exnote, #pop .csrc {{ font-size:12px; color:var(--muted); margin-top:6px; }}
#pop .open {{ display:inline-block; margin-top:10px; font-weight:600; color:var(--code); }}
#pop .pinned {{ font-size:12px; color:var(--muted); margin-left:8px; }}
#popclose {{ flex:none; width:30px; height:30px; border-radius:8px; border:1.5px solid var(--line); background:transparent; color:var(--ink);
  font-size:18px; line-height:1; cursor:pointer; }}
footer {{ margin-top:30px; color:var(--muted); font-size:13px; }}
</style>
</head>
<body>
{theme_btn}
<main>

<!-- ======================= Exam guide breakdown: 1.1 ======================= -->
<section id="ts">
<div class="crumbs"><span class="section-tag">Exam guide breakdown</span> <span>&rsaquo;</span>
  {domain_fact} <span>&rsaquo;</span> <span>Task statement 1.1</span>
  <a href="#behind">Behind the mocks 1.1 &darr;</a></div>
<h1>1.1 Agentic loops</h1>
<p class="gtitle">&ldquo;{ts_title}&rdquo;</p>

<div class="level">
  <div class="lhead"><span class="lname">Overview</span><span class="ltime">30 seconds</span></div>
  <div class="lbody">
    <p class="lead">In an agentic loop, your code sends a request to Claude and checks <code>stop_reason</code> in the response.
    <code>"tool_use"</code>: your code runs the tool that Claude asked for and sends the result back.
    <code>"end_turn"</code>: the loop stops.</p>
    <div class="scroll"><div class="stage" id="loop" style="width:900px;height:336px">
      <svg width="900" height="336" aria-hidden="true">
        <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" style="fill:var(--muted)"/></marker></defs>
        <path id="a1" class="arrow" d="M 212 64 L 357 64" marker-end="url(#ah)"/>
        <path id="a2" class="arrow" d="M 460 106 L 460 157" marker-end="url(#ah)"/>
        <path id="a3" class="arrow" d="M 358 200 L 213 200" marker-end="url(#ah)"/>
        <path id="a4" class="arrow" d="M 105 158 L 105 107" marker-end="url(#ah)"/>
        <path id="a5" class="arrow" d="M 460 242 L 460 273" marker-end="url(#ah)"/>
        <circle id="dot" class="dot" r="7" cx="-50" cy="-50"/>
      </svg>
      {n_send}{n_resp}{n_check}{n_run}{n_done}
      <span class="alab" style="left:246px;top:207px">"tool_use"</span>
      <span class="alab" style="left:470px;top:248px">"end_turn"</span>
      <span class="iter" id="iter" style="left:0;top:300px"></span>
      <div class="convo" data-step="convo" tabindex="0" role="button" aria-expanded="false" style="left:600px;top:0;width:300px;height:320px">
        <div class="ct">The conversation</div><div id="msgs"></div></div>
    </div></div>
    <div class="controls"><button type="button" id="play">Pause</button>
      <span>One task: Claude asks for two tools, then finishes. Put the pointer on a part, or tap it, to see the detail.</span></div>
  </div>
</div>

<details class="level">
  <summary><span class="lname">Explanation</span><span class="ltime">3 minutes</span></summary>
  <div class="lbody">
    <h3>In plain words</h3>
    <p><b>The loop.</b> Your code sends a request to Claude and looks at <code>stop_reason</code> in the response.
    <code>"tool_use"</code> means that Claude wants a tool. Your code runs the tool and sends the result back for the next iteration.
    When it is <code>"end_turn"</code>, your code stops the loop.</p>
    <p><b>The memory of the loop.</b> Your code adds each tool result to the conversation history. That is how Claude can use the
    new information when it decides the next action.</p>
    <p><b>Who decides.</b> The guide makes a distinction. In model-driven decision-making, Claude reasons about which tool to call
    next, from the context. The other side is a decision tree or a sequence of tools that somebody sets up in advance.</p>
    <p><b>Three wrong ways to stop.</b> The guide names three anti-patterns:</p>
    <div class="anti">
      <div class="no"><b>&#10007; Read the words</b>Parse natural language signals to decide when the loop ends.</div>
      <div class="no"><b>&#10007; Count to a limit</b>Make an arbitrary limit of iterations the main way to stop.</div>
      <div class="no"><b>&#10007; Look for text</b>Treat text from the assistant as the sign that the work is complete.</div>
      <div class="yes"><b>&#10003; Check the field</b>Continue on <code>"tool_use"</code>. Stop on <code>"end_turn"</code>.</div>
    </div>
    <h3>The guide's own text</h3>
    <p class="ltime">The labels 1.1-K1 to 1.1-S3 are ours. The guide has no labels.</p>
    {guide_list}
    <h3>What the exam tests</h3>
    <p>The guide lists this topic as tested: {scope_fact}.</p>
    <p>Under the Claude API, its list of technologies names {tech_fact}.</p>
    <p>Domain 1 is about {weight}% of the scored items. The scenarios with domain 1 as a primary domain are {scen}.</p>
  </div>
</details>

<details class="level">
  <summary><span class="lname">Depth</span></summary>
  <div class="lbody">
    <p><b>The loop in code.</b> Put the pointer on <i>Your code sends the request</i> in the diagram, or tap it. The popup shows the
    loop in Python.</p>
    <div class="beyond"><span class="btag">Beyond the exam</span>
      <p>The exam guide names two values of <code>stop_reason</code>: <code>"tool_use"</code> and <code>"end_turn"</code>. The Claude API
      has {stop_fact}, for example <code>"max_tokens"</code>, <code>"pause_turn"</code> and <code>"refusal"</code>. A loop in
      production should handle them too.</p></div>
    <p><b>On a real system.</b> The mock builder made a deliberate choice about loops. <a class="xlink" href="#behind">Behind the mocks 1.1 &darr;</a></p>
  </div>
</details>
</section>

<hr class="split">

<!-- ======================= Behind the mocks: 1.1 ======================= -->
<section id="behind">
<div class="crumbs"><span class="section-tag">Behind the mocks</span> <span>&rsaquo;</span> <span>1.1 Agentic loops</span>
  <span class="src">Source: the pipeline</span> <a href="#ts">Task statement 1.1 &uarr;</a></div>
<h1>A loop that stops when the work is right</h1>
<p class="gtitle">How the mock builder uses the idea of task statement 1.1</p>

<div class="level">
  <div class="lhead"><span class="lname">Overview</span><span class="ltime">30 seconds</span></div>
  <div class="lbody">
    <p class="lead">The mock builder is not an agentic loop. Code and the owner decide each next step. No model decides it. The
    builder has one automatic loop for questions: a question that fails a check goes back to the writer. The main way to stop is a pass. The limits
    are only guards.</p>
    <div class="scroll"><div class="stage" style="width:900px;height:200px">
      <svg width="900" height="200" aria-hidden="true">
        <defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" style="fill:var(--muted)"/></marker></defs>
        <path class="arrow" d="M 150 50 L 196 50" marker-end="url(#ah2)"/>
        <path class="arrow" d="M 350 50 L 396 50" marker-end="url(#ah2)"/>
        <path class="arrow" d="M 550 50 L 596 50" marker-end="url(#ah2)"/>
      </svg>
      <div class="try f" data-step="t-fail" tabindex="0" role="button" aria-expanded="false" style="left:0;top:0;width:150px;height:100px">
        <div class="tn">Try 1</div><small>fails a check</small></div>
      <div class="try f" data-step="t-fail" tabindex="0" role="button" aria-expanded="false" style="left:200px;top:0;width:150px;height:100px">
        <div class="tn">Try 2</div><small>fails a check</small></div>
      <div class="try p" data-step="t-pass" tabindex="0" role="button" aria-expanded="false" style="left:400px;top:0;width:150px;height:100px">
        <div class="tn">Try 3</div><small>passes</small></div>
      <div class="stopnote" style="left:606px;top:26px;width:280px">&#10003; The loop stops: the question passed.</div>
      <div class="guard" data-step="t-guard" tabindex="0" role="button" aria-expanded="false" style="left:0;top:122px;width:550px;height:62px">
        <b>The guards</b>: 3 failed tries, or "cannot decide" two times. Then the loop stops and the owner decides.</div>
    </div></div>
    <div class="controls"><span>A drawing, not a real slot. Put the pointer on a part, or tap it, to see the code.</span></div>
  </div>
</div>

<details class="level">
  <summary><span class="lname">The story</span><span class="ltime">3 minutes</span></summary>
  <div class="lbody">
    <h3>Why the builder does not need an agentic loop</h3>
    <p>The work of a mock is {known_fact}. Before a model writes any question, code makes {slots_fact}. Each slot says what one
    question must be. So code follows a fixed sequence of steps. That is the other side of the distinction in 1.1-K3: no model
    decides what happens next.</p>
    <h3>The one loop</h3>
    <p>A question that fails the check by code or the check by a model goes back to the writer with the exact findings, and the
    writer tries again. The loop stops when a question passes both checks. A {guard_fact} and a limit of two results "cannot
    decide" are only guards. After a guard, the slot waits for the owner.</p>
    <p>This matches 1.1-S3: an arbitrary limit of iterations must not be the main way to stop. The guide wrote that point for agentic
    loops. The builder uses the same idea for a loop of retries.</p>
    <h3>What happened in mock 1</h3>
    <p>Mock 1 needed {tries_fact}. {rewrites} of the tries were rewrites that the owner asked for after the marks. {more} slots
    needed more than one try: {failed} after a failed check, and {rwonly} only after a rewrite that the owner asked for. {stuck_fact}</p>
    <h3>What went wrong, and the fix</h3>
    <p>The first design had many automatic paths for repair. {reviews_fact} The owner said: &ldquo;{quote_fact}&rdquo;</p>
    <p>The fix: {oneloop_fact}, and {wait_fact}. The control became code, with {tests_fact}.</p>
  </div>
</details>

<details class="level">
  <summary><span class="lname">Depth</span></summary>
  <div class="lbody">
    <p><b>The code.</b> Put the pointer on <i>Try 3</i> or on <i>The guards</i> in the diagram. The popups show the lines of the control
    that make a pass stop the loop first, and the limit of tries.</p>
    <p><b>The tests.</b> Each case of the control is a test, for example {testname_fact}.</p>
    <p><b>The sources.</b> Each underlined fact on this page opens its source: the sentence of the decision, the lines of code, or the
    count from the run records. The link in each card opens the file at the tag <code>{tag}</code> of the repository.</p>
  </div>
</details>
</section>

<footer>Sample page for the portal work (decisions 0001 to 0006 in academy/decisions). A script made this page:
academy/sample/make-1-1.py. Each guide text is the exact text of reference/guide-records.json. Each excerpt in a card is taken from
its file by the script.</footer>

<div id="pop" role="dialog" aria-labelledby="poptitle" hidden>
  <div class="ptop"><span><span id="popwho" class="tag"></span><span id="poppin" class="pinned"></span></span>
    <button id="popclose" type="button" aria-label="Close">&times;</button></div>
  <h2 id="poptitle"></h2>
  <div id="popbody"></div>
</div>
</main>
<script type="application/json" id="popdata">{popdata}</script>
<script type="application/json" id="carddata">{carddata}</script>
<script>
(function () {{
  /* ----- the popups and the preview cards ----- */
  var POP = JSON.parse(document.getElementById('popdata').textContent);
  var CARD = JSON.parse(document.getElementById('carddata').textContent);
  var pop = document.getElementById('pop');
  var OPEN_DELAY = 300, CLOSE_DELAY = 350, GAP = 10, EDGE = 8;
  var current = null, pinned = false, openTimer = null, closeTimer = null;
  function el(tag, cls, text) {{ var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }}
  function fillStep(d) {{
    var who = document.getElementById('popwho'); who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    var s = document.getElementById('popbody'); s.textContent = '';
    d.sent.forEach(function (t) {{ s.appendChild(el('p', null, t)); }});
    if (d.example) {{ s.appendChild(el('h3', null, d.examplehead)); s.appendChild(el('pre', null, d.example));
      if (d.examplenote) s.appendChild(el('p', 'exnote', d.examplenote)); }}
    if (d.points.length) {{ s.appendChild(el('h3', null, 'The exam guide says'));
      var ul = el('ul'); d.points.forEach(function (p) {{ var li = el('li'); var b = el('b', null, p.id + ' ');
        li.appendChild(b); li.appendChild(document.createTextNode(p.text)); li.appendChild(el('span', 'pctx', p.ctx)); ul.appendChild(li); }});
      s.appendChild(ul); }}
  }}
  var KIND = {{ excerpt: 'Source', code: 'Code', guide: 'Exam guide', docs: 'Anthropic docs', count: 'Run records' }};
  function fillCard(c) {{
    var who = document.getElementById('popwho'); who.className = 'tag ' + (c.kind === 'code' ? 't-code' : c.kind === 'guide' ? 't-model' : 't-io');
    who.textContent = KIND[c.kind] || 'Source';
    document.getElementById('poptitle').textContent = c.title;
    var s = document.getElementById('popbody'); s.textContent = '';
    if (c.kind === 'code') s.appendChild(el('pre', null, c.text));
    else {{ var q = el('blockquote'); q.textContent = c.text; s.appendChild(q); }}
    s.appendChild(el('p', 'csrc', c.src));
    var a = el('a', 'open', c.kind === 'docs' ? 'Open the page' : 'Open in the repository'); a.href = c.href; a.target = '_blank'; a.rel = 'noopener';
    s.appendChild(a);
  }}
  function place() {{
    if (!current) return;
    var b = current.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    var pw = pop.offsetWidth, ph = pop.offsetHeight, left, top;
    if (current.classList.contains('fact')) {{ left = b.left; top = b.bottom + 6; if (top + ph > vh - EDGE) top = b.top - 6 - ph; }}
    else if (b.right + GAP + pw <= vw - EDGE) {{ left = b.right + GAP; top = b.top; }}
    else if (b.left - GAP - pw >= EDGE) {{ left = b.left - GAP - pw; top = b.top; }}
    else if (b.bottom + GAP + ph <= vh - EDGE) {{ left = b.left; top = b.bottom + GAP; }}
    else {{ left = b.left; top = b.top - GAP - ph; }}
    pop.style.left = Math.max(EDGE, Math.min(left, vw - pw - EDGE)) + 'px';
    pop.style.top = Math.max(EDGE, Math.min(top, vh - ph - EDGE)) + 'px';
  }}
  function setPinned(v) {{ pinned = v; document.getElementById('poppin').textContent = v ? 'kept open' : ''; }}
  function open(t, pin) {{
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (current && current !== t) current.setAttribute('aria-expanded', 'false');
    current = t;
    if (t.dataset.step) fillStep(POP[t.dataset.step]); else fillCard(CARD[t.dataset.card]);
    pop.hidden = false; pop.scrollTop = 0; t.setAttribute('aria-expanded', 'true'); setPinned(pin); place();
  }}
  function close(returnFocus) {{
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (!current) return;
    var t = current; t.setAttribute('aria-expanded', 'false'); pop.hidden = true; current = null; setPinned(false);
    if (returnFocus) t.focus({{ preventScroll: true }});
  }}
  function scheduleClose() {{
    clearTimeout(closeTimer); if (pinned) return;
    closeTimer = setTimeout(function () {{
      if (pinned) return;
      if (current && (current.matches(':hover') || pop.matches(':hover'))) return;
      if (current && (document.activeElement === current || pop.contains(document.activeElement))) return;
      close(false);
    }}, CLOSE_DELAY);
  }}
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape' && current) {{ e.preventDefault(); close(true); }} }});
  document.querySelectorAll('[data-step],[data-card]').forEach(function (t) {{
    t.addEventListener('mouseenter', function () {{ clearTimeout(closeTimer); if (pinned || current === t) return;
      clearTimeout(openTimer); openTimer = setTimeout(function () {{ if (!pinned) open(t, false); }}, OPEN_DELAY); }});
    t.addEventListener('mouseleave', function () {{ clearTimeout(openTimer); scheduleClose(); }});
    t.addEventListener('click', function (e) {{ e.stopPropagation(); if (current === t && pinned) close(false); else open(t, true); }});
    t.addEventListener('keydown', function (e) {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault();
      if (current === t && pinned) close(true); else open(t, true); }} }});
    t.addEventListener('blur', function () {{ if (!pinned) scheduleClose(); }});
  }});
  document.addEventListener('click', function (e) {{ if (current && !pop.contains(e.target)) close(false); }});
  pop.addEventListener('mouseenter', function () {{ clearTimeout(closeTimer); }});
  pop.addEventListener('mouseleave', scheduleClose);
  document.getElementById('popclose').addEventListener('click', function (e) {{ e.stopPropagation(); close(true); }});
  window.addEventListener('scroll', place, true); window.addEventListener('resize', place);

  /* ----- the animation of the loop ----- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nodes = {{ send: 'n-send', resp: 'n-resp', check: 'n-check', run: 'n-run', done: 'n-done' }};
  var msgs = document.getElementById('msgs'), iterEl = document.getElementById('iter'), sr = document.getElementById('srval');
  var dot = document.getElementById('dot'), btn = document.getElementById('play');
  var MSG = {{ task: ['user', 'the task'], call1: ['assistant', 'tool_use: tool A'], res1: ['user', 'tool_result: A'],
              call2: ['assistant', 'tool_use: tool B'], res2: ['user', 'tool_result: B'], fin: ['assistant', 'text: the answer'] }};
  var SEQ = [];
  [1, 2, 3].forEach(function (i) {{
    SEQ.push({{ n: 'send', it: i }}, {{ a: 'a1' }}, {{ n: 'resp' }}, {{ a: 'a2' }});
    if (i < 3) SEQ.push({{ n: 'check', sr: 'tool_use', m: 'call' + i }}, {{ a: 'a3' }}, {{ n: 'run', m: 'res' + i }}, {{ a: 'a4' }});
    else SEQ.push({{ n: 'check', sr: 'end_turn', m: 'fin' }}, {{ a: 'a5' }}, {{ n: 'done', end: true }});
  }});
  var k = 0, playing = !reduce, timer = null;
  function clearOn() {{ document.querySelectorAll('.node.on,.arrow.on').forEach(function (x) {{ x.classList.remove('on'); }}); }}
  function addMsg(key) {{ var m = MSG[key], d = el('div', 'msg' + (m[0] === 'assistant' ? ' a' : ''));
    d.appendChild(el('i', null, m[0] + ' · ')); d.appendChild(document.createTextNode(m[1])); msgs.appendChild(d); }}
  function reset() {{ msgs.textContent = ''; addMsg('task'); sr.textContent = '?'; iterEl.textContent = ''; }}
  function moveDot(id, ms, then) {{
    var p = document.getElementById(id), L = p.getTotalLength(), t0 = null;
    p.classList.add('on');
    function f() {{ if (!playing) {{ dot.setAttribute('cx', -50); return; }}
      var now = Date.now(); if (t0 === null) t0 = now; var r = Math.min(1, (now - t0) / ms), pt = p.getPointAtLength(L * r);
      dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
      if (r < 1) timer = setTimeout(f, 16); else {{ dot.setAttribute('cx', -50); then(); }} }}
    f();
  }}
  function step() {{
    if (!playing) return;
    if (k >= SEQ.length) {{ k = 0; clearOn(); reset(); }}
    var s = SEQ[k++];
    clearOn();
    if (s.a) {{ moveDot(s.a, 650, function () {{ timer = setTimeout(step, 80); }}); return; }}
    document.getElementById(nodes[s.n]).classList.add('on');
    if (s.it) iterEl.textContent = 'Iteration ' + s.it;
    if (s.sr) sr.textContent = '"' + s.sr + '"';
    if (s.m) addMsg(s.m);
    timer = setTimeout(step, s.end ? 2600 : 1100);
  }}
  function showAll() {{ reset(); ['call1', 'res1', 'call2', 'res2', 'fin'].forEach(addMsg); sr.textContent = '"end_turn"';
    iterEl.textContent = '3 iterations'; document.getElementById('n-done').classList.add('on'); }}
  btn.addEventListener('click', function () {{
    playing = !playing; btn.textContent = playing ? 'Pause' : 'Play';
    clearTimeout(timer); if (playing) {{ if (k >= SEQ.length) k = 0; if (k === 0) reset(); step(); }}
  }});
  if (reduce) {{ btn.textContent = 'Play'; showAll(); }} else {{ reset(); step(); }}
}})();
</script>
{theme_js}
</body>
</html>
"""

n_send = hot("send", "", 0, 24, 210, 80, '<span class="who w-code">Your code</span><b>Sends the request</b>')
n_resp = hot("resp", "model", 360, 24, 200, 80, '<span class="who w-model">Claude</span><b>Responds</b>')
n_check = hot("check", "", 360, 160, 200, 80,
              '<span class="who w-code">Your code</span><b>Checks stop_reason</b><span class="sr" id="srval">?</span>')
n_run = hot("run", "", 0, 160, 210, 80, '<span class="who w-code">Your code</span><b>Runs the tool, adds the result</b>')
n_done = hot("done", "done", 360, 275, 200, 40, '<b>Done</b>')
for i, n in [("n-send", "n_send"), ("n-resp", "n_resp"), ("n-check", "n_check"), ("n-run", "n_run"), ("n-done", "n_done")]:
    globals()[n] = globals()[n].replace('class="node', 'id="%s" class="node' % i, 1)

DARK = ("--bg:#12171d; --panel:#1b222b; --ink:#e8edf2; --muted:#9eabb8; --line:#3b4654; "
        "--code:#8bbcf5; --code-bg:#1c3350; --model:#cfa6f0; --model-bg:#38254a; "
        "--owner:#7fd6b1; --owner-bg:#173a2d; --open:#f0cc6e; --open-bg:#40330f; "
        "--fail:#ff8f86; --fail-bg:#4a1f1c; --shadow:0 10px 30px rgba(0,0,0,.6);")
page = PAGE.format(
    theme_css=theme.scheme_css(DARK), theme_head=theme.HEAD, theme_btn=theme.BUTTON, theme_js=theme.JS,
    domain_fact=fact("g-domain", "Domain 1: %s, about %d%%" % (domain["name"], domain["weight"])),
    ts_title=e(ts["title"]), n_send=n_send, n_resp=n_resp, n_check=n_check, n_run=n_run, n_done=n_done,
    guide_list=guide_list(),
    scope_fact=fact("g-scope", "“%s”" % in_scope),
    tech_fact=fact("g-tech", "“stop_reason values (\"tool_use\", \"end_turn\")”"),
    weight=domain["weight"], scen=e(scen_list),
    stop_fact=fact("d-stop", "more values"),
    known_fact=fact("b-known", "known before it starts"),
    slots_fact=fact("b-slots", "a plan of 60 slots"),
    guard_fact=fact("b-guard", "limit of 3 tries"),
    tries_fact=fact("b-tries", "%d tries for %d slots" % (TRIES_M1, SLOTS_M1)), rewrites=REWRITES_M1,
    more=MORE_M1, failed=FAILED_M1, rwonly=RWONLY_M1,
    stuck_fact=fact("b-stuck", "One slot stopped at the guard, and the owner gave it more tries."),
    reviews_fact=fact("b-reviews", "A first review found 14 serious items. A second review found 10 new ones, and most of them came from the answers to the first."),
    quote_fact=fact("b-quote", "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue."),
    oneloop_fact=fact("b-oneloop", "one automatic loop"),
    wait_fact=fact("b-wait", "each other failure waits for the owner"),
    tests_fact=fact("b-tests", "tests that make no model call"),
    testname_fact=fact("b-testname", "“more tries after three tries”"),
    tag=TAG,
    popdata=json.dumps(POP, ensure_ascii=False).replace("</", "<\\/"),
    carddata=json.dumps(CARDS, ensure_ascii=False).replace("</", "<\\/"),
)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("Wrote %s: %d popups, %d cards. Mock 1: %d tries, %d slots, %d with more than one, at most %d."
      % (os.path.relpath(OUT, ROOT), len(POP), len(CARDS), TRIES_M1, SLOTS_M1, MORE_M1, MAX_M1))
