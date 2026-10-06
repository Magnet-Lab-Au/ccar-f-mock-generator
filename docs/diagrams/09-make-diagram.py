"""Makes docs/diagrams/09-step-7-the-owner-marks-the-questions.html. Run: python3 09-make-diagram.py"""
import html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
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

d22 = open(root + '/docs/decisions/0022-the-owner-reads-all-60-questions-of-mock-1-then-20-of-each-mock.md', encoding='utf-8').read()
assert 'a clean sample of 20 permits up to 6' in d22
columns = '\n'.join(['Question ID', 'Scenario', 'Point that the question must test', 'Question', 'Option A to option D (or E)',
                     'Correct answer', 'Reason of each option', 'Mark        <- the owner fills this', 'Reason      <- the owner fills this'])
marks = [{'question_id': 'M1-S17-T1', 'mark': 'good', 'reason': None, 'round': 1, 'date': '(the date)'},
         {'question_id': 'M1-S18-T2', 'mark': 'bad', 'reason': '(the reason of the owner)', 'round': 1, 'date': '(the date)'}]
D = {
 'mock': dict(title='The mock after step 6', who='60 questions', cls='io',
   sent=['Each of the 60 questions passed the code check, the two model checks and the check of the complete mock.',
         'So each question that the owner reads is a question that the checks call good.']),
 'file': dict(title='Code builds the marking file', who='Code', cls='code',
   sent=['Code builds one Excel file. It has one row for each question.',
         'The file shows no verdict of a checker.'],
   example=columns, examplehead='The columns of the file',
   why='The owner must see the point that the question must test. If the file does not show it, the owner cannot judge if the question tests it.'),
 'owner': dict(title='The owner marks each question', who='The owner', cls='owner',
   sent=['The owner marks each question "good" or "bad". A bad mark has one reason.',
         'The owner does not see the verdicts of the checkers during the marking. A person who sees a verdict tends to agree with it.'],
   points=[point('5.5-K2'), point('5.5-S1')],
   why='The guide wrote these points for the extraction of data: a person checks a sample of the results that the system is sure of. Here each question in the file passed all checks. So each bad mark shows an error that the checks did not find.'),
 'read': dict(title='Code reads the marks', who='Code', cls='code',
   sent=['Code reads the file. If a mark is missing, or a bad mark has no reason, code does not accept the file and names the rows.',
         'Code saves the marks as a record. It shows the bad marks for each scenario and each domain.'],
   example=js_(marks), examplehead='Example: two marks in the record',
   points=[point('5.5-K1')],
   why='The guide wrote this point for the extraction of data. Here it applies to the marks: one total can hide a bad part. 3 bad marks in one domain show a different problem than 3 bad marks in 3 domains.'),
 'm1': dict(title='Mock 1: all 60 questions', who='The owner', cls='owner',
   sent=['For mock 1 the owner marks all 60 questions.',
         'These 60 marks are also the first set of labels from a person. With them we can test the checker: does it pass what the owner marks good, and fail what the owner marks bad?'],
   why='Before mock 1, nobody knows how good the checker is. So the owner reads everything one time.'),
 'later': dict(title='Each later mock: 20 questions', who='The owner', cls='owner',
   sent=['For each later mock the owner marks 20 questions: 5 from each scenario, with questions from each domain. Code selects them at random.',
         'A sample with no bad mark still permits bad questions in the part that the owner did not read. For a mock of 60 questions and a clean sample of 20, that part can still have up to 6 bad questions (95% confidence).',
         'The number goes below 20 only when the results of the first mocks permit it. That number is not decided.'],
   points=[point('5.5-S2')],
   why='The guide wrote this point for the extraction of data. Here it applies to the marks: the owner reads less only after the results are good in each scenario and each domain.'),
 'good': dict(title='All marks are good', who='Go on', cls='owner',
   sent=['Each question in the file has the mark "good".', 'Step 8 builds the files of the mock.']),
 'bad': dict(title='Some marks are bad', who='Back to the writer', cls='stop',
   sent=['A question with a bad mark goes to step 5. The reason of the owner is the finding.',
         'The new question goes through steps 3, 4 and 6. Then the owner gets a new file with only the new questions.']),
 'stop': dict(title='Too many marks are bad: the mock stops', who='The mock stops', cls='stop',
   sent=['Mock 1: more than 6 bad marks of 60. A later mock: 2 or more bad marks of 20. Both numbers are guesses.',
         'The mock is not released. We correct the rules of the checker. Then all 60 questions go through the checks again.'],
   why='A bad mark says two things: this question is bad, and the checker passed a bad question. Many bad marks show that the checker is wrong, not only the questions. In a sample, more bad questions are probably in the part that the owner did not read.'),
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
    ' ok' if ok else '', letter, sk(w), '<em class="tick">correct</em>' if ok else '')
card = ('<div class="chead"><span class="idchip">M1-S17</span><span class="sc">Scenario 3</span></div>'
        + sk(96) + sk(88) + sk(54) + opt('A', 62) + opt('B', 55, True) + opt('C', 66) + opt('D', 48))

def row(cells, cls=''):
    return '<div class="r %s">%s</div>' % (cls, ''.join('<span class="%s">%s</span>' % c for c in cells))
good = '<b class="good">good</b>'
bad = '<b class="bad">bad</b>'
sheet = ('<div class="bar"><i class="xl"></i>M1-round1.xlsx</div>'
         + row([('', 'ID'), ('', 'Question'), ('', 'Answer'), ('fill', 'Mark'), ('fill', 'Reason')], 'h')
         + row([('', 'M1-S01'), ('', sk(80)), ('', 'A'), ('fill', good), ('fill', '')])
         + row([('', 'M1-S02'), ('', sk(64)), ('', 'C'), ('fill', good), ('fill', '')])
         + row([('', 'M1-S03'), ('', sk(72)), ('', 'B, D'), ('fill', bad), ('fill', 'C is also correct.')])
         + row([('', 'M1-S04'), ('', sk(58)), ('', 'D'), ('fill', '<i class="caret"></i>'), ('fill', '')]))
person = ('<svg viewBox="0 0 90 78" width="90" height="78" aria-hidden="true"><circle cx="45" cy="24" r="17" style="fill:var(--owner)"/>'
          '<path d="M11,78 C11,54 28,46 45,46 C62,46 79,54 79,78 Z" style="fill:var(--owner)"/></svg><b>The owner</b><small>"good" or "bad", and one reason for a bad mark</small>')
record = '<b>marks.json</b><small>the marks record</small>'

def grid(on, risk=()):
    out = []
    for r in range(4):
        for c in range(15):
            cls = 'on' if (r, c) in on else ('risk' if (r, c) in risk else 'off')
            out.append('<i class="%s"></i>' % cls)
    return '<div class="g60">%s</div>' % ''.join(out)
ALL = {(r, c) for r in range(4) for c in range(15)}
picks = {0: (1, 4, 7, 10, 13), 1: (0, 3, 8, 11, 14), 2: (2, 5, 6, 9, 12), 3: (1, 3, 7, 10, 14)}
SAMPLE = {(r, c) for r, cols in picks.items() for c in cols}
RISK = {(0, 2), (1, 6), (2, 10), (3, 5), (0, 11), (3, 12)}
assert len(SAMPLE) == 20 and len(RISK) == 6 and not (SAMPLE & RISK) and all(len(v) == 5 for v in picks.values())
m1 = '<div class="big">60<small>of 60</small></div><div class="gwrap">%s<span>each row is one scenario</span></div><p>The owner reads everything one time. The 60 marks are also the first labels from a person. We test the checker with them.</p>' % grid(ALL)
later = ('<div class="big">20<small>of 60</small></div><div class="gwrap">%s<span>5 from each scenario, selected at random</span></div>'
         '<p>Up to 6 bad questions can still hide in the 40 that the owner does not read, also when all 20 marks are good.</p>' % grid(SAMPLE, RISK))

def bar(top, title, sub, segs):
    out = ['<div class="blabel" style="top:%dpx"><b>%s</b><small>%s</small></div>' % (top + 6, title, sub)]
    for i, (key, cls, big, small) in enumerate(segs):
        out.append(hot(key, 'seg ' + cls + (' first' if i == 0 else ' last' if i == 2 else ''),
                       'left:%dpx;top:%dpx;width:260px' % (200 + i * 260, top), '<b>%s</b><small>%s</small>' % (big, small), big))
    return ''.join(out)

parts = [
 '<div class="shead" style="top:2px"><i>1</i>The owner reads the questions. No verdict of a checker is in view.</div>',
 '<div class="card back" style="left:36px;top:66px"></div><div class="card back" style="left:28px;top:58px"></div>',
 hot('mock', 'card', 'left:20px;top:50px', card, 'The mock after step 6'),
 '<div class="cap" style="left:20px;top:278px;width:262px">60 questions that passed all checks</div>',
 '<div class="alab" style="left:272px;top:96px;width:78px">code builds<br>the sheet</div>',
 hot('file', 'sheet', 'left:350px;top:50px', sheet, 'The marking file'),
 '<div class="cap noview" style="left:350px;top:238px;width:450px"><i class="eye"></i>The sheet does not show the verdict of a checker.</div>',
 hot('owner', 'person', 'left:846px;top:40px', person, 'The owner marks'),
 '<div class="alab" style="left:810px;top:92px">marks</div>',
 hot('read', 'filebox', 'left:852px;top:212px', record, 'The marks record'),
 '<div class="alab" style="left:806px;top:186px">code<br>saves</div>',
 '<div class="shead" style="top:310px"><i>2</i>How many questions the owner marks</div>',
 hot('m1', 'gpanel', 'left:20px;top:346px', '<h4>Mock 1</h4>' + m1, 'Mock 1: all 60 questions'),
 hot('later', 'gpanel', 'left:510px;top:346px', '<h4>Each later mock</h4>' + later, 'Each later mock: 20 questions'),
 '<div class="shead" style="top:574px"><i>3</i>What the marks decide</div>',
 bar(612, 'Mock 1', '60 marks', [('good', 'g', 'No bad mark', 'Step 8 builds the files.'),
                                  ('bad', 'a', '1 to 6 bad marks', 'Those questions go back to the writer.'),
                                  ('stop', 'x', '7 or more bad marks', 'The mock stops.')]),
 bar(692, 'A later mock', '20 marks', [('good', 'g', 'No bad mark', 'Step 8 builds the files.'),
                                        ('bad', 'a', '1 bad mark', 'That question goes back to the writer.'),
                                        ('stop', 'x', '2 or more bad marks', 'The mock stops.')]),
]
paths = ['<path class="flow" d="M288,146 H346" marker-end="url(#a)"/>',
         '<path class="flow" d="M848,118 H806" marker-end="url(#a)"/>',
         '<path class="flow" d="M802,234 C822,234 828,244 848,244" marker-end="url(#a)"/>']

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 774px; }')
assert '774px' in extra_css
extra_css += """  .hot { position: absolute; cursor: pointer; }
  .hot:focus-visible { outline: 3px solid var(--code); outline-offset: 2px; }
  .hot[aria-expanded="true"] { box-shadow: 0 0 0 2px var(--ink); }
  .cap { position: absolute; font-size: 12.5px; color: var(--muted); text-align: center; }
  .alab { position: absolute; font-size: 12px; font-weight: 600; color: var(--muted); line-height: 1.25; text-align: center; }
  .sk { display: block; height: 7px; border-radius: 4px; background: var(--line); margin: 7px 0; }
  .card { position: absolute; width: 246px; height: 204px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 12px; padding: 12px 14px; }
  .card.back { background: var(--bg); }
  .card.hot:hover { border-color: var(--muted); }
  .chead { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 12px; color: var(--muted); }
  .idchip { font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
  .optrow { display: flex; align-items: center; gap: 8px; margin-top: 7px; }
  .optrow .sk { margin: 0; flex: none; }
  .chip { flex: none; width: 21px; height: 21px; border-radius: 50%; border: 1.5px solid var(--line); font-size: 11px; display: grid; place-items: center; }
  .optrow.ok .chip { background: var(--owner); border-color: var(--owner); color: var(--panel); }
  .optrow.ok .sk { background: var(--owner); opacity: .5; }
  .tick { font-style: normal; font-size: 11px; font-weight: 700; color: var(--owner); margin-left: auto; }
  .sheet { width: 450px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 8px; overflow: hidden; font-size: 12.5px; }
  .sheet:hover { border-color: var(--muted); }
  .sheet .bar { height: 28px; display: flex; align-items: center; gap: 8px; padding: 0 10px; font-weight: 700; background: var(--bg); }
  .xl { width: 14px; height: 14px; border-radius: 3px; background: var(--owner); }
  .r { display: grid; grid-template-columns: 74px 104px 68px 62px 1fr; height: 32px; border-top: 1px solid var(--line); }
  .r > span { display: flex; align-items: center; padding: 0 8px; overflow: hidden; white-space: nowrap; border-left: 1px solid var(--line); }
  .r > span:first-child { border-left: none; font-variant-numeric: tabular-nums; }
  .r .sk { margin: 0; }
  .r.h > span { font-weight: 700; font-size: 12px; color: var(--muted); }
  .r .fill { background: var(--owner-bg); }
  .r.h .fill { color: var(--owner); }
  .good { color: var(--owner); } .bad { color: var(--fail); }
  .caret { width: 2px; height: 16px; background: var(--ink); }
  .noview { text-align: left; display: flex; align-items: center; gap: 8px; }
  .eye { flex: none; width: 22px; height: 12px; border: 1.5px solid var(--muted); border-radius: 50%; position: relative; }
  .eye::after { content: ''; position: absolute; left: -3px; right: -3px; top: 4px; border-top: 1.5px solid var(--fail); transform: rotate(-28deg); }
  .person { width: 142px; text-align: center; padding: 6px 4px 8px; border-radius: 12px; }
  .person:hover { background: var(--owner-bg); }
  .person svg { position: static; display: block; margin: 0 auto 4px; }
  .person b { display: block; font-size: 15px; }
  .person small, .filebox small { display: block; font-size: 12px; color: var(--muted); line-height: 1.3; }
  .filebox { width: 132px; height: 62px; padding: 12px 12px 0; background: var(--panel); border: 1.5px solid var(--line); border-radius: 4px 0 4px 4px; font-size: 13px; }
  .filebox:hover { border-color: var(--muted); }
  .filebox::before { content: ''; position: absolute; right: -1.5px; top: -1.5px; border-style: solid; border-width: 0 16px 16px 0; border-color: transparent var(--bg) transparent transparent; }
  .filebox::after { content: ''; position: absolute; right: -1.5px; top: -1.5px; width: 16px; height: 16px; border-left: 1.5px solid var(--line); border-bottom: 1.5px solid var(--line); background: var(--panel); border-radius: 0 0 0 3px; }
  .gpanel { width: 470px; height: 204px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 12px; padding: 12px 16px; }
  .gpanel:hover { border-color: var(--muted); }
  .gpanel h4 { margin: 0; font-size: 15px; }
  .big { position: absolute; left: 16px; top: 44px; font-size: 44px; font-weight: 700; line-height: 1; color: var(--owner); }
  .big small { display: block; font-size: 13px; font-weight: 600; color: var(--muted); margin-top: 4px; }
  .gwrap { position: absolute; left: 150px; top: 44px; }
  .gwrap span { display: block; font-size: 12px; color: var(--muted); margin-top: 5px; }
  .g60 { display: grid; grid-template-columns: repeat(15, 15px); gap: 4px; }
  .g60 i { height: 15px; border-radius: 4px; }
  .g60 .on { background: var(--owner); }
  .g60 .off { background: var(--line); opacity: .55; }
  .g60 .risk { border: 1.5px dashed var(--fail); background: var(--fail-bg); }
  .gpanel p { position: absolute; left: 16px; right: 16px; bottom: 10px; margin: 0; font-size: 13px; color: var(--muted); }
  .blabel { position: absolute; left: 20px; width: 170px; }
  .blabel b { display: block; font-size: 15px; } .blabel small { color: var(--muted); font-size: 12.5px; }
  .seg { height: 60px; padding: 9px 14px; border: 1.5px solid; }
  .seg b { display: block; font-size: 14px; } .seg small { font-size: 12.5px; }
  .seg.first { border-radius: 10px 0 0 10px; } .seg.last { border-radius: 0 10px 10px 0; }
  .seg.g { background: var(--owner-bg); border-color: var(--owner); }
  .seg.g b { color: var(--owner); }
  .seg.a { background: var(--open-bg); border-color: var(--open); }
  .seg.a b { color: var(--open); }
  .seg.x { background: var(--fail-bg); border-color: var(--fail); }
  .seg.x b { color: var(--fail); }
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
<title>Step 7: the owner marks the questions</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 7: a person is the last check</h1>
  <p class="sub">This diagram shows the design. The step is not built yet. Each check before this step is code or a model. This step shows if those checks are right: a person reads the questions and marks them. Put the pointer on a part of the picture, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 774" width="1000" height="774" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 09. Design of 6 October 2026. Status of the step: planned. The step is not built. The question card and the sheet are drawings. They show the form, not real questions. Each exam guide text in a popup is the exact text of the guide.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/09-step-7-the-owner-marks-the-questions.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
