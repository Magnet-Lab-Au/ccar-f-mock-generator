"""Makes docs/diagrams/11-repeats-across-mocks.html (decision 0056). Run: python3 11-make-diagram.py"""
import html, os, json, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root + '/src')
import point_groups
from step2_write import EARLIER_RULE
from step4_check_model import RULES_TEXT
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
g9 = open(root + '/docs/diagrams/09-make-diagram.py', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
e = html.escape

# Real records.
built = json.load(open(root + '/mocks/mock-01.questions.json', encoding='utf-8'))
answers = {a['question_id']: a['correct'] for a in json.load(open(root + '/mocks/mock-01.answers.json', encoding='utf-8'))['answers']}
M1 = next(q for g in built['groups'] for q in g['questions'] if q['question_id'] == 'M1-S28-T2')
OLD = json.load(open(root + '/runs/mock-02/questions/M2-S08-T1.json', encoding='utf-8'))
NEW = json.load(open(root + '/runs/mock-02/questions/M2-S08-T2.json', encoding='utf-8'))
NEWV = json.load(open(root + '/runs/mock-02/checks/M2-S08-T2-step4.json', encoding='utf-8'))
DEC = next(d for d in json.load(open(root + '/runs/mock-02/owner-decisions.json', encoding='utf-8')) if d.get('question_id') == 'M2-S08-T1')
G = point_groups.group_of(point_groups.load())
GROUP = G['1.1-S3']
B9 = next(l for l in RULES_TEXT.splitlines() if l.startswith('B9.'))
b9_new = next(r for r in NEWV['results'] if r['rule'] == 'B9')['result']

def opts(q, marks):
    return ['%s %s. %s' % ('(correct)' if ok else '(wrong)', letter, text) for letter, text, ok in marks]

m1_opts = [(o['letter'], o['text'], o['letter'] in answers[M1['question_id']]) for o in M1['options']]
old_opts = [(o['letter'], o['text'], o['correct']) for o in OLD['options']]
new_opts = [(o['letter'], o['text'], o['correct']) for o in NEW['options']]

D = {
 'm1': dict(title='Mock 1, question M1-S28 (built)', who='Earlier mock', cls='io',
   sent=['Point %s, group %s: "%s".' % (M1['point'], GROUP['id'], GROUP['idea']), M1['question']] + opts(M1, m1_opts),
   why='Mock 1 is built, so its questions are fixed. A later mock can test the same idea again, but not with the same question.'),
 'group': dict(title='One idea: group %s' % GROUP['id'], who='data/point-groups.json', cls='code',
   sent=['The group "%s" holds the points %s.' % (GROUP['idea'], ', '.join(GROUP['points'])),
         'Inside one mock, no two slots get points of one group (decision 0047). Across mocks, a shared idea is allowed: the guide has 95 ideas, and 5 mocks have 300 slots (decision 0049).'],
   why='So the idea of the loop that stops on stop_reason comes back. The rule of decision 0056 is about the question, not the idea.'),
 'old': dict(title='Mock 2, first try M2-S08-T1: a repeat', who='Before decision 0056', cls='stop',
   sent=['Point %s. The same scene as M1-S28: the loop stops too early. The same answer: continue while stop_reason is "tool_use". The wrong options are the same three ideas: a phrase match, "text means done", and a fixed iteration cap.' % OLD['point'],
         OLD['question']] + opts(OLD, old_opts),
   why='The writer did not know mock 1. It wrote the most obvious scene again. A second review and an independent agent found 13 such strong repeats in mock 2.'),
 'step1': dict(title='Step 1: the point that earlier mocks used less comes first', who='Code', cls='code',
   sent=['Inside a group, code sorts the points of a task statement: first the group that earlier mocks used less (decision 0050), then the point that earlier mocks used less (decision 0056). The seed keeps the order inside the same counts.',
         'Example: in mock 2, slot M2-S32 got point 3.3-S2, the point of M1-S43, although 3.3-K1, 3.3-K2, 3.3-K3 and 3.3-S3 were unused. With decision 0056, an unused point comes first.'],
   why='A new point of the same idea gives the writer a new part of the idea to test.'),
 'step2': dict(title='Step 2: the writer sees the earlier questions', who='One model call', cls='model',
   sent=['When the idea of the slot is in an earlier built mock, the request has the earlier questions on that idea, with the mark of each option.',
         'The request also has this instruction: "%s"' % EARLIER_RULE],
   why='The owner changed the first suggestion: a different angle, not a different correct action, because some ideas have only one correct action. The wrong options must never be the same.'),
 'step4': dict(title='Step 4: rule B9 in call 4b', who='One model call', cls='model',
   sent=[B9, 'Call 4b gets the earlier questions on the same idea. With none, B9 passes. A failure goes back to the writer automatically, as for each other rule.'],
   why='The check is in step 4, not in step 6. Step 4 sends a failure back at once. A finding of step 6 waits for the owner after the marking.'),
 'rewrite': dict(title='The owner decides a rewrite', who='The owner', cls='owner',
   sent=['%s: rewrite %s. The reason of the owner: "%s"' % (DEC['id'], DEC['question_id'], DEC['reason'])],
   why='The 13 strong repeats of mock 2 got a rewrite with the new rule. The 4 close repeats stay as known limits (decision 0058).'),
 'new': dict(title='Mock 2, new try M2-S08-T2', who='After decision 0056', cls='owner',
   sent=['The same idea, a new angle: the question asks for the cause. The wrong options are new.', NEW['question']] + opts(NEW, new_opts) +
        ['Rule B9 in call 4b: %s.' % b9_new],
   why='The idea of mock 1 comes back, but a participant who took mock 1 meets a new question.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g9[g9.index('def hot('):g9.index('sk = lambda')])

def qcard(qid, label, text, marks, extra=''):
    rows = ''.join('<div class="orow%s"><b class="chip">%s</b><span>%s</span></div>' % (' ok' if ok else '', letter, e(t[:58] + ('…' if len(t) > 58 else '')))
                   for letter, t, ok in marks)
    return ('<div class="chead"><span class="idchip">%s</span><span class="sc">%s</span></div><p class="qt">%s</p>%s%s'
            % (qid, label, e(text[:150] + '…'), rows, extra))

parts = [
 '<div class="shead" style="top:2px"><i>1</i>The same idea comes back in a later mock</div>',
 hot('m1', 'card qc', 'left:20px;top:46px', qcard('M1-S28-T2', 'mock 1, built', M1['question'], m1_opts), 'Mock 1, question M1-S28'),
 hot('group', 'gpanel', 'left:380px;top:110px', '<h4>Group %s</h4><p>%s</p><div class="pts">%s</div>' % (
     GROUP['id'], e(GROUP['idea']), ''.join('<b>%s</b>' % p for p in GROUP['points'])), 'One idea'),
 hot('old', 'card qc rep', 'left:654px;top:46px', qcard('M2-S08-T1', 'mock 2, first try', OLD['question'], old_opts,
     '<div class="flag">same scene, same answer, same wrong options</div>'), 'Mock 2, first try'),
 '<div class="shead" style="top:372px"><i>2</i>Three steps stop the same question</div>',
 hot('step1', 'spanel', 'left:20px;top:414px', '<h4>Step 1: plan (example: slot M2-S32)</h4><div class="prow"><b>3.3-K1</b><small>unused</small><em>first</em></div>'
     '<div class="prow"><b>3.3-S3</b><small>unused</small><em>first</em></div><div class="prow dim"><b>3.3-S2</b><small>in mock 1</small><em>later</em></div>',
     'Step 1'),
 hot('step2', 'spanel', 'left:345px;top:414px', '<h4>Step 2: the writer</h4><div class="req"><small>the request</small><div class="eq">earlier questions on this idea: M1-S28</div>'
     '<p>a different scene and a different angle: the cause, the fix, or a choice between rules</p></div>', 'Step 2'),
 hot('step4', 'spanel', 'left:670px;top:414px', '<h4>Step 4: rule B9</h4><p class="b9">not the same scene with the same answer, and no wrong option of an earlier question</p>'
     '<div class="pf"><span class="pass">pass: on to step 6</span><span class="fail">fail: back to the writer</span></div>', 'Step 4'),
 '<div class="shead" style="top:620px"><i>3</i>The result: the same idea, a new question</div>',
 hot('rewrite', 'mini', 'left:20px;top:664px', '<b>%s</b><small>rewrite of M2-S08-T1</small>' % DEC['id'], 'The rewrite of the owner'),
 hot('new', 'card qc new', 'left:300px;top:654px', qcard('M2-S08-T2', 'mock 2, new try', NEW['question'], new_opts,
     '<div class="flag ok">B9: %s</div>' % b9_new), 'Mock 2, new try'),
 '<div class="cap" style="left:654px;top:690px;width:320px">The angle is now the cause. No wrong option repeats M1-S28.</div>',
]
paths = ['<path class="flow" d="M292,170 H376" marker-end="url(#a)"/>',
         '<path class="flow" d="M604,170 H650" marker-end="url(#a)"/>',
         '<path class="flow" d="M290,498 H341" marker-end="url(#a)"/>',
         '<path class="flow" d="M615,498 H666" marker-end="url(#a)"/>',
         '<path class="flow" d="M218,698 H296" marker-end="url(#a)"/>']

base9 = g9[g9.index('extra_css += """') + len('extra_css += """'):g9.index('"""\na = js.index')]
extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 990px; }')
assert '990px' in extra_css
extra_css += base9 + """  .card.qc { width: 326px; height: 306px; font-size: 12px; }
  .card.qc.rep { border-color: var(--fail); }
  .card.qc.new { width: 326px; height: 300px; border-color: var(--owner); }
  .qt { margin: 0 0 6px; color: var(--ink); line-height: 1.35; }
  .orow { display: flex; gap: 7px; align-items: flex-start; margin-top: 5px; line-height: 1.3; }
  .orow span { color: var(--muted); }
  .orow.ok .chip { background: var(--owner); border-color: var(--owner); color: var(--panel); }
  .orow.ok span { color: var(--ink); }
  .flag { margin-top: 8px; font-size: 11.5px; font-weight: 700; color: var(--fail); }
  .flag.ok { color: var(--owner); }
  .gpanel, .spanel, .mini { background: var(--panel); border: 1.5px solid var(--line); border-radius: 12px; }
  .gpanel:hover, .spanel:hover, .mini:hover { border-color: var(--muted); }
  .gpanel { width: 224px; height: 128px; padding: 10px 14px; border-color: var(--code); }
  .gpanel h4, .spanel h4 { margin: 0 0 6px; font-size: 14px; }
  .gpanel p { margin: 0 0 8px; font-size: 12.5px; }
  .pts { display: flex; gap: 6px; flex-wrap: wrap; } .pts b { font-size: 12px; padding: 2px 8px; border-radius: 999px; background: var(--code-bg); color: var(--code); }
  .spanel { width: 270px; height: 170px; padding: 10px 14px; font-size: 12.5px; }
  .prow { display: flex; align-items: center; gap: 8px; height: 26px; border-top: 1px solid var(--line); }
  .prow small { color: var(--muted); } .prow em { margin-left: auto; font-style: normal; font-weight: 700; color: var(--owner); }
  .prow.dim em { color: var(--muted); }
  .req { background: var(--bg); border-radius: 8px; padding: 6px 10px; }
  .req small { font-size: 11px; color: var(--muted); }
  .eq { margin: 4px 0; padding: 4px 8px; border-radius: 6px; background: var(--model-bg); font-weight: 600; }
  .req p, .b9 { margin: 4px 0 0; }
  .pf { display: flex; flex-direction: column; gap: 5px; margin-top: 10px; }
  .pf span { font-weight: 700; font-size: 12px; } .pass { color: var(--owner); } .fail { color: var(--fail); }
  .mini { width: 196px; height: 66px; padding: 10px 12px; }
  .mini b { display: block; font-size: 14px; } .mini small { font-size: 12px; color: var(--muted); }
"""
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = g4[g4.index("fill = '''") + 10:g4.index("'''\njs2 = js[:a]")]
js2 = js[:a] + fill + js[b:]
sel = "document.querySelectorAll('.box.step')"
assert js2.count(sel) == 1
js2 = js2.replace(sel, "document.querySelectorAll('[data-step]')")
popdiv = g3[g3.index("popdiv = '''") + 12:g3.index("'''\ndata = json.dumps")]
data = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>No repeat across mocks</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Across mocks: the same idea may come back, the same question may not</h1>
  <p class="sub">This diagram shows decision 0056. It changes step 1 (the plan), step 2 (the writer) and step 4 (the check). The example is real: a question of mock 1, the repeat in the first try of mock 2, and the rewrite under the new rule. Put the pointer on a part of the picture, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 990" width="1000" height="990" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 11. Decision 0056 of 8 October 2026. Status: built, ran for the rewrites of mock 2. The question texts in the cards and popups are the real texts from mocks/mock-01.questions.json and runs/mock-02/questions/.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/11-repeats-across-mocks.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
