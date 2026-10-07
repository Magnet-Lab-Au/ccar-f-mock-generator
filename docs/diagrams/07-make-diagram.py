"""Makes docs/diagrams/07-step-5-try-again.html. Run: python3 07-make-diagram.py"""
import html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
g9 = open(root + '/docs/diagrams/09-make-diagram.py', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
e = html.escape
PT = {p['id']: (p, t) for t in REC['task_statements'] for p in t['points']}

def point(pid):
    p, t = PT[pid]
    assert p['text'] in guide
    return {'id': pid, 'text': p['text'], 'ctx': 'From task statement %s: %s' % (t['id'], t['title'])}

def js_(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

def finding(step, rule, detail, letter=None, other=()):
    return {'step': step, 'rule': rule, 'detail': detail, 'letter': letter, 'point': None, 'other_questions': list(other)}

f3 = finding(3, 'A6', 'The question has 140 words. The limit is 110.')
f4 = finding(4, 'B1', 'The blind call selected option C. The writer marked option B. (Then the reason of the blind call.)', 'C')
f7 = finding(7, 'owner', '(the reason of the owner)')
f6 = finding(6, 'D1', 'Both questions describe a subagent that times out.', other=['M1-S33-T1'])
open_slot = {'slot_id': 'M1-S17', 'status': 'open', 'question_id': 'M1-S17-T3', 'tries': 3, 'open_reasons': ['three_tries']}
EF = 'Example of a finding'
D = {
 's3': dict(title='From step 3: a code rule fails', who='Code', cls='code',
   sent=['Step 3 found that one of the exact rules A1 to A11 fails.', 'The question comes here automatically.'],
   example=js_(f3), examplehead=EF),
 's4': dict(title='From step 4: a rule fails, or "cannot decide"', who='One model call', cls='model',
   sent=['Step 4 found that the blind answer is different from the marks, or that one of the rules B1 to B6 fails.',
         'The verdict "cannot decide" also sends the question here, with its reason. The question comes here automatically.'],
   example=js_(f4), examplehead=EF),
 'bad': dict(title='The owner marks the question bad', who='The owner', cls='owner',
   sent=['In step 7 the owner marks a question bad, with one reason. That reason is the finding, with the rule "owner".',
         'The slot gets a new start: 3 new tries.'],
   example=js_(f7), examplehead=EF),
 'rw': dict(title='The owner selects rewrite for a finding of step 6', who='The owner', cls='owner',
   sent=['Step 6 sends no question back. It finds a problem across questions, for example two questions with the same scene, and the owner decides.',
         'With "rewrite", the owner names one question of the finding and gives a reason. The writer also gets the text of the other question.',
         'The slot gets a new start: 3 new tries.'],
   example=js_(f6), examplehead=EF),
 'req': dict(title='The request of step 2', who='The same as in step 2', cls='io',
   sent=['All parts of the request of step 2: the rules, the 3 sample questions, the story, the task statement, the 14 technologies, the slot and the form.',
         'The model answers in the same form as in step 2. So steps 3 and 4 check each try in the same way.']),
 'failed': dict(title='The failed question', who='The last failed try', cls='io',
   sent=['The complete record of the last failed try: the question, the options with their letters, the marks and the reasons.',
         'The writer sees the letters that the checker saw. So a finding that names a letter is clear.',
         'The writer does not see the tries before that. So the request stays short.'],
   points=[point('4.4-S1')],
   why='The guide wrote this point for the extraction of data. Here the "document" is the request of step 2, the "failed extraction" is the failed question, and the "validation errors" are the findings.'),
 'findings': dict(title='The findings', who='From the checks or the owner', cls='io',
   sent=['The findings of the last try. Each finding has the same fields: step, rule, detail, letter, point and other_questions.'],
   example=js_([f3, f4]), examplehead='Example: a list of two findings',
   points=[point('4.4-K1')],
   why='The guide wrote this point for the extraction of data. Here it applies to a question: with the exact findings the writer knows what to change. With no findings it can make the same error again.'),
 'writer': dict(title='The writer', who='One model call', cls='model',
   sent=['A new call of the plain API. It is the writer of step 2, with two more parts in the request.',
         'It can also answer "cannot write". Code saves that answer as a try, with its reason, and the slot is open at once.',
         'A call that fails 3 times is not a try. Code saves an error record, and the owner starts the program again.']),
 'new': dict(title='A new question record', who='File', cls='io',
   sent=['A new record with the next try number. M1-S17-T2 is try 2 of slot 17.',
         'Code mixes the options again and gives new letters. The record of try 1 stays. No file is written over.'],
   example=js_({'question_id': 'M1-S17-T2', 'slot_id': 'M1-S17', 'try': 2, 'point': '1.2-K2', 'request': 5,
                'shown_try': 'M1-S17-T1', 'status': 'written', 'question': '(the question)', 'options': '(the options)'}),
   examplehead='Example: some fields of the record'),
 'again': dict(title='Checked again', who='Steps 3 and 4', cls='io',
   sent=['The new question is a new text. A check of the old text says nothing about the new text.',
         'So steps 3 and 4 check it as a new question. The checker does not see the earlier findings.'],
   why='A checker that sees the earlier findings looks only for those findings.'),
 't1': dict(title='Try 1', who='Step 2', cls='io',
   sent=['The first question of the start. For a new slot it comes from step 2.', 'If it passes the checks, the slot has the status "passed", and step 5 does not run.']),
 't2': dict(title='Try 2', who='Step 5', cls='io', sent=['The writer gets try 1 and its findings, and writes the question again.']),
 't3': dict(title='Try 3', who='Step 5', cls='io',
   sent=['The writer gets try 2 and its findings. It does not get try 1.', 'This is the last try of this start.']),
 'cd': dict(title='Two "cannot decide" results also stop the slot', who='Code', cls='code',
   sent=['If step 4 answers "cannot decide" two times in one start, the slot stops. The two results do not have to come one after the other.',
         'The rule that applies first stops the slot.'],
   why='If the checker cannot decide two times, a participant probably cannot decide either. The owner looks at it.'),
 'open': dict(title='The slot is open', who='The owner decides', cls='open',
   sent=['A rule stopped the slot. The field open_reasons names each cause: three_tries, cannot_decide_twice or cannot_write.',
         'The other slots continue. The report says what the mock waits for.'],
   example=js_(open_slot), examplehead='Example: an open slot in the report',
   points=[point('1.1-S3'), point('4.4-K2')],
   why='The number 3 is a guess. The limit is not the main way to stop. The main way to stop is a question that passes. The first point names the opposite as an error, for agent loops. The second point, for the extraction of data, says that some errors do not go away with a new try. It supports "cannot write": a slot that does not fit its scenario.'),
 'np': dict(title='new_point', who='The owner', cls='owner',
   sent=['Code selects a different point of the same task statement: a point that no slot uses now, and that this slot did not have before.',
         'The writer gets a request of step 2, with no failed try. The old tries tested a different point.',
         'The plan file does not change. The new point is in the decision of the owner.',
         'If no point is free, code refuses the command.'],
   example=js_({'id': 'D002', 'action': 'new_point', 'target': 'M1-S17', 'after_try': 3, 'point': '1.2-K5', 'reason': '(the reason)', 'date': '(the date)'}),
   examplehead='Example: the decision in owner-decisions.json'),
 'mt': dict(title='more_tries', who='The owner', cls='owner',
   sent=['The same slot gets 3 new tries.',
         'After three_tries or cannot_decide_twice, the writer gets a request of step 5 with the last try and its findings.',
         'After cannot_write, the writer gets a request of step 2, because no question exists to show.']),
 'npl': dict(title='new_plan', who='The owner', cls='stop',
   sent=['The mock stops. A new seed makes a new plan.', 'Code refuses new_plan when no slot is open.', 'How the new plan starts is not built yet.']),
 'start2': dict(title='A new start of the slot', who='Code', cls='code',
   sent=['Each start gives the slot 3 tries. A start is the first question, more_tries, new_point, a bad mark or a rewrite.',
         'The try numbers continue: T4, T5, T6. The count of "cannot decide" starts at zero.'],
   why='The decision of the owner is new information. The old count belongs to the old start.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])


# ---------- the drawing: the things themselves, not boxes of text ----------
def hot(key, cls, style, inner, label):
    return ('<div class="hot %s" data-step="%s" role="button" tabindex="0" aria-haspopup="dialog" aria-expanded="false" '
            'aria-controls="pop" aria-label="%s" style="%s">%s</div>' % (cls, key, e(label), style, inner))

sk = lambda w: '<span class="sk" style="width:%d%%"></span>' % w
opt = lambda letter, w, ok=False: '<div class="optrow%s"><b class="chip">%s</b>%s%s</div>' % (
    ' ok' if ok else '', letter, sk(w), '<em class="tick">marked</em>' if ok else '')

def src_card(key, cls, tag, name, what, left):
    return hot(key, 'srcc ' + cls, 'left:%dpx;top:62px' % left,
               '<span class="tag t-%s">%s</span><b>%s</b><small>%s</small>' % (cls, tag, name, what), name)

def tri(key, label, mark, left, top, cls='x'):
    return hot(key, 'try ' + cls, 'left:%dpx;top:%dpx' % (left, top), '<b>%s</b><small>%s</small>' % (label, mark), label)

def act(key, cls, name, what, top):
    return hot(key, 'act ' + cls, 'left:650px;top:%dpx' % top, '<b>%s</b><small>%s</small>' % (name, what), name)

reqcard = '<h4>The request of step 2</h4>' + ''.join(sk(w) for w in (92, 80, 88, 60, 76, 70, 84, 52))
qcard = ('<div class="chead"><span class="idchip">M1-S17-T1</span><span class="res">failed</span></div>'
         + sk(96) + sk(70) + opt('A', 58) + opt('B', 52, True) + opt('C', 62) + opt('D', 46))
fcard = ('<h4>The findings</h4>'
         '<div class="fnd"><b>Step 4 &middot; B1 &middot; C</b><span>Option C is also correct.</span></div>'
         '<div class="fnd"><b>Step 3 &middot; A6</b><span>The question is too long.</span></div>')
filebox = '<b>M1-S17-T2.json</b><small>the next try</small>'

parts = [
 '<div class="shead" style="top:2px"><i>1</i>Four ways a question comes back</div>',
 '<div class="grp" style="left:20px;top:40px;width:470px">automatic</div>',
 '<div class="grp" style="left:510px;top:40px;width:470px">the owner decides</div>',
 src_card('s3', 'code', 'Code', 'Step 3', 'A code rule fails.', 20),
 src_card('s4', 'model', 'One model call', 'Step 4', 'A rule fails, or "cannot decide".', 265),
 src_card('bad', 'owner', 'The owner', 'A bad mark', 'In step 7.', 510),
 src_card('rw', 'owner', 'The owner', 'A rewrite', 'Of a finding of step 6.', 755),
 '<div class="shead" style="top:186px"><i>2</i>The writer gets the failed question and the exact findings</div>',
 hot('req', 'paper', 'left:20px;top:228px', reqcard, 'The request of step 2'),
 '<div class="plus" style="left:214px;top:300px">+</div>',
 hot('failed', 'card', 'left:244px;top:228px', qcard, 'The failed question'),
 '<div class="plus" style="left:478px;top:300px">+</div>',
 hot('findings', 'paper fp', 'left:508px;top:228px', fcard, 'The findings'),
 hot('writer', 'call', 'left:790px;top:240px', '<b>The writer</b><small>The same form as step 2.</small>', 'The writer'),
 hot('new', 'filebox', 'left:820px;top:322px', filebox, 'A new question record'),
 hot('again', 'note', 'left:790px;top:404px;width:190px', 'Steps 3 and 4 check it again.', 'Checked again'),
 '<div class="shead" style="top:506px"><i>3</i>At most 3 tries for each start of a slot</div>',
 tri('t1', 'T1', 'fails', 20, 548), tri('t2', 'T2', 'fails', 124, 548), tri('t3', 'T3', 'fails', 228, 548),
 hot('cd', 'note cdn', 'left:20px;top:638px;width:290px', '<b>Or two "cannot decide"</b> in one start: the slot also stops.', 'Two cannot decide results'),
 hot('open', 'openslot', 'left:360px;top:548px', '<b>M1-S17 is open</b><small>open_reasons: three_tries</small><small>The owner selects one action.</small>', 'The slot is open'),
 act('np', 'o', 'new_point', 'A different point. A request of step 2.', 536),
 act('mt', 'o', 'more_tries', '3 new tries. A request of step 5 or of step 2.', 592),
 act('npl', 'x', 'new_plan', 'The mock stops.', 648),
 tri('t4', 'T4', 'new start', 20, 724, 'n'), tri('t5', 'T5', '', 124, 724, 'n'), tri('t6', 'T6', '', 228, 724, 'n'),
 hot('start2', 'note', 'left:360px;top:722px;width:620px',
     '<b>A new start.</b> After more_tries, new_point, a bad mark or a rewrite, the slot gets 3 new tries. The try numbers continue, and the count of "cannot decide" starts at zero.',
     'A new start of the slot'),
]
for k in ('t4', 't5', 't6'):
    D[k] = dict(title='Try %s' % k[1], who='A new start', cls='io', example='', examplehead='', examplenote='', why='', points=[],
                sent=['A try of a new start. The try numbers continue after T3.', 'This start again has at most 3 tries.'])

paths = [
 '<path class="flow" d="M716,320 C750,320 756,268 786,268" marker-end="url(#a)"/>',
 '<path class="flow" d="M885,300 V318" marker-end="url(#a)"/>',
 '<path class="flow" d="M885,386 V400" marker-end="url(#a)"/>',
 '<path class="flow" style="stroke:var(--fail)" d="M314,583 H356" marker-end="url(#af)"/>',
 '<path class="flow" d="M580,580 C612,580 614,560 646,560" marker-end="url(#a)"/>',
 '<path class="flow" d="M580,589 C612,589 614,616 646,616" marker-end="url(#a)"/>',
 '<path class="flow" d="M580,598 C612,598 614,672 646,672" marker-end="url(#a)"/>',
]

Q = "'" * 3
extra_css = g3[g3.index('extra_css = ' + Q) + 15:g3.index(Q + '\na = js.index')]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 800px; }')
assert '800px' in extra_css
extra_css += g9[g9.index('extra_css += """') + 16:g9.index('"""\na = js.index')]
extra_css += """  .grp { position: absolute; font-size: 12px; font-weight: 600; color: var(--muted); border-bottom: 1.5px solid var(--line); padding-bottom: 2px; }
  .srcc { width: 225px; height: 96px; padding: 10px 14px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 12px; }
  .srcc:hover { border-color: var(--muted); }
  .srcc .tag { margin-bottom: 6px; }
  .srcc b { display: block; font-size: 15px; } .srcc small { font-size: 12.5px; color: var(--muted); }
  .paper { width: 190px; height: 200px; padding: 12px 14px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 6px; }
  .paper:hover, .call:hover { border-color: var(--muted); }
  .paper h4 { margin: 0 0 6px; font-size: 13.5px; }
  .paper.fp { width: 210px; }
  .fnd { margin-top: 8px; padding: 6px 8px; border-radius: 6px; background: var(--fail-bg); font-size: 12px; }
  .fnd b { display: block; color: var(--fail); } .fnd span { color: var(--ink); }
  .card { width: 214px; height: 200px; }
  .filebox { width: 160px; }
  .card .res { font-weight: 700; color: var(--fail); }
  .tick { color: var(--muted); }
  .plus { position: absolute; font-size: 26px; font-weight: 700; color: var(--muted); }
  .call { width: 190px; height: 58px; padding: 7px 14px; background: var(--model-bg); border: 1.5px solid var(--model); border-radius: 28px; }
  .call b { display: block; color: var(--model); font-size: 14.5px; } .call small { font-size: 12px; }
  .note { padding: 8px 12px; font-size: 13px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 10px; }
  .note:hover { border-color: var(--muted); }
  .note.cdn { border-style: dashed; }
  .try { width: 90px; height: 70px; padding: 8px 10px; border: 1.5px solid; border-radius: 10px; text-align: center; }
  .try b { display: block; font-size: 20px; } .try small { font-size: 12px; }
  .try.x { background: var(--fail-bg); border-color: var(--fail); } .try.x b, .try.x small { color: var(--fail); }
  .try.n { height: 56px; padding: 4px 10px; background: var(--panel); border-color: var(--line); }
  .openslot { width: 220px; height: 82px; padding: 8px 14px; background: var(--open-bg); border: 1.5px solid var(--open); border-radius: 12px; }
  .openslot b { display: block; color: var(--open); font-size: 15px; } .openslot small { display: block; font-size: 12.5px; }
  .act { width: 330px; height: 48px; padding: 5px 12px; border: 1.5px solid; border-radius: 10px; }
  .act b { display: block; font-size: 13.5px; } .act small { font-size: 12px; }
  .act.o { background: var(--owner-bg); border-color: var(--owner); } .act.o b { color: var(--owner); }
  .act.x { background: var(--fail-bg); border-color: var(--fail); } .act.x b { color: var(--fail); }
"""
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = g4[g4.index('fill = ' + Q) + 10:g4.index(Q + '\njs2 = js[:a]')]
js2 = js[:a] + fill + js[b:]
sel = "document.querySelectorAll('.box.step')"
assert js2.count(sel) == 1
js2 = js2.replace(sel, "document.querySelectorAll('[data-step]')")
popdiv = g3[g3.index('popdiv = ' + Q) + 12:g3.index(Q + '\ndata = json.dumps')]
data = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Step 5: try again</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 5: a failed question goes back to the writer with the findings</h1>
  <p class="sub">This diagram shows the design. The step is not built yet. The step runs only for a question that did not pass, or that the owner sent back. Put the pointer on a part of the picture, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 800" width="1000" height="800" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 07. Design of 7 October 2026 (decisions 0033, 0038 and 0039). Status of the step: planned. The step is not built. The control of the tries exists as code with tests. The cards and the files are drawings. The examples of findings are invented, to show the form. Each exam guide text in a popup is the exact text of the guide.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
used = {p.split('data-step="')[1].split('"')[0] for p in parts if 'data-step="' in p}
assert used == set(D), (set(D) - used, used - set(D))
out = root + '/docs/diagrams/07-step-5-try-again.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
