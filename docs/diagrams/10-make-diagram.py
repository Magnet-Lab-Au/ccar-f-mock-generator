"""Makes docs/diagrams/10-step-8-build-the-files.html. Run: python3 10-make-diagram.py"""
import html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
g9 = open(root + '/docs/diagrams/09-make-diagram.py', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
e = html.escape

def js_(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

def fact(section, q):
    assert guide.count(q) == 1, q
    return {'id': section, 'text': q, 'ctx': 'A fact about the exam. It is not a task statement point.'}

q_example = {'number': 17, 'question_id': 'M1-S17-T2', 'domain': 1, 'task_statement': '1.2', 'point': '1.2-K2',
             'type': 'multiple_choice', 'select': 1, 'question': '(the text of the question)',
             'options': [{'letter': 'A', 'text': '(option A)'}, {'letter': 'B', 'text': '(option B)'},
                         {'letter': 'C', 'text': '(option C)'}, {'letter': 'D', 'text': '(option D)'}]}
a_example = {'number': 17, 'question_id': 'M1-S17-T2', 'correct': ['B'],
             'reasons': [{'letter': 'A', 'correct': False, 'reason': '(why A is wrong)'},
                         {'letter': 'B', 'correct': True, 'reason': '(why B is correct)'}, '...']}
D = {
 'rec': dict(title='The question records', who='From steps 2 to 7', cls='io',
   sent=['The stored question records are the one true copy of the questions. Each record has the question, the options, the marks and the reasons.',
         'The results of its checks are separate records: the verdicts of step 3, step 4 and step 6, and the mark of the owner if the owner read the question.'],
   why='If a question is in two places and a person can edit one of them, the two can disagree. Then nobody knows which one the checks saw. So the files are built from the records, and nobody edits a file by hand.'),
 'gate': dict(title='Six conditions before the build', who='Code', cls='code',
   sent=['The build starts only after the command "accept" of the owner. Then code checks six conditions:',
         '1. Each of the 60 questions passed steps 3 and 4, and no question changed after its checks. 2. Step 6 checked the current questions of each scenario. 3. Each finding of step 6 has a decision of the owner. 4. Each question that needs a mark has a mark. 5. The bad marks are below the stop limit. 6. No call failed in the last run.',
         'If one condition is false, code builds no file and lists the causes.'],
   why='A file for participants must have only questions that passed each check.'),
 'fp': dict(title='The fingerprint', who='Code', cls='code',
   sent=['Each check saves a fingerprint of the record that it checked. A fingerprint is a short code that code calculates from the text of the record. If one letter of the text changes, the fingerprint changes.',
         'Before the build, code calculates the fingerprint of each record again and compares.',
         'A different fingerprint shows that the record changed after its check. Then the build stops, and the record must pass the checks again.'],
   why='The rule is that nobody edits a record after its check. A rule alone does not make sure of that. With the fingerprint, code can prove that the question in the mock is the question that the checks saw.'),
 'qfile': dict(title='The questions file', who='File', cls='io',
   sent=['The 60 questions with their options and letters. The file has no answers and no reasons.',
         'Each question has its domain, its task statement and its point.',
         'Each question has the field "select", 1 or 2. The portal shows it as the line "Select 1." or "Select 2."'],
   example=js_(q_example), examplehead='Example: one question in the file',
   points=[fact('Section 3', 'each item states how many responses to select')],
   why='Code adds the line that says how many answers to select. So the line cannot be missing or wrong.'),
 'afile': dict(title='The answers file', who='File', cls='io',
   sent=['For each question: the correct letters, and the reason of each option.',
         'The reasons are the explanation that a participant reads after the mock.'],
   example=js_(a_example), examplehead='Example: one entry in the file'),
 'seq': dict(title='The sequence of the questions', who='Code', cls='code',
   sent=['The 60 questions are in 4 groups, one for each scenario. Each group starts with the story of its scenario and has 15 questions.',
         'Inside a group, a seed sets the sequence. The same seed gives the same sequence.'],
   points=[fact('Section 5', 'Each scenario presents a realistic production context that frames a set of questions.')],
   why='A mock has the same form as the exam. In the exam, a participant reads the story of a scenario and then answers its questions.'),
 'during': dict(title='During the mock: the questions', who='The portal', cls='io',
   sent=['The portal shows the questions file to the participant.', 'The answers are in a different file. So they are not in the page that the participant has open.']),
 'after': dict(title='After the mock: the answers', who='The portal', cls='io',
   sent=['After the mock, the portal shows the correct answers and the reason of each option.',
         'The format of the portal is not known yet. A converter from these two files to that format comes later.']),
 'domains': dict(title='A result for each domain', who='The portal', cls='io',
   sent=['Each question in the file has its domain. So the portal can show the share of correct answers for each of the 5 domains.',
         'The bars in the picture are an example. They are not real results.'],
   points=[fact('Section 3', 'Pass/fail with scaled score (100–1,000), plus percent-correct by domain on the score report')],
   why='The exam reports a result for each domain. A mock that does the same shows a participant where to study more.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g9[g9.index('def hot('):g9.index('sk = lambda')])
sk = lambda w: '<span class="sk" style="width:%d%%"></span>' % w
opt = lambda letter, w, ok=False: '<div class="optrow%s"><b class="chip">%s</b>%s%s</div>' % (
    ' ok' if ok else '', letter, sk(w), '<em class="tick">correct</em>' if ok else '')
stamps = ''.join('<span class="stamp">%s</span>' % t for t in ('step 3', 'step 4', 'step 6'))
card = ('<div class="chead"><span class="idchip">M1-S17</span><span class="sc">fingerprint a41f</span></div>'
        + sk(96) + sk(70) + opt('A', 62) + opt('B', 55, True) + opt('C', 66) + opt('D', 48) + '<div class="stamps">%s</div>' % stamps)
gate = ('<h4>After "accept", code checks</h4>'
        '<p class="ck">Each question passed its checks.</p>'
        '<p class="ck">Each finding and mark is settled.</p>'
        '<p class="ck">No record changed after its check.</p>')
fp = ('<div class="fprow"><span class="fpc">record a41f</span><b>=</b><span class="fpc">check a41f</span><em class="yes">build</em></div>'
      '<div class="fprow"><span class="fpc no">record 9c2e</span><b>&ne;</b><span class="fpc">check a41f</span><em class="nope">stop</em></div>')
qfile = ('<div class="bar"><i class="jf"></i>mock-01.questions.json</div><div class="fbody"><b class="qn">17</b><div class="fl">' + sk(92) + sk(60)
         + '<div class="chips">' + ''.join('<b class="chip">%s</b>' % c for c in 'ABCD') + '<small>no answers</small></div></div></div>')
arow = lambda n, letters, w: '<div class="arow"><b class="qn">%d</b>%s%s</div>' % (n, ''.join('<b class="chip okc">%s</b>' % c for c in letters), sk(w))
afile = '<div class="bar"><i class="jf"></i>mock-01.answers.json</div><div class="fbody col">' + arow(17, 'B', 58) + arow(18, 'D', 66) + arow(19, 'AC', 50) + '</div>'

def group(i):
    cells = ''.join('<i></i>' for _ in range(15))
    return ('<h4>Scenario group %d</h4><div class="story"><small>the story</small>%s%s</div><div class="g15">%s</div><span>questions %d to %d</span>'
            % (i + 1, sk(94), sk(72), cells, i * 15 + 1, i * 15 + 15))
person = ('<svg viewBox="0 0 90 78" width="60" height="52" aria-hidden="true"><circle cx="45" cy="24" r="17" style="fill:var(--muted)"/>'
          '<path d="M11,78 C11,54 28,46 45,46 C62,46 79,54 79,78 Z" style="fill:var(--muted)"/></svg><b>A participant</b>')
dbars = '<h4>The result for each domain</h4>' + ''.join(
    '<div class="dbar"><small>Domain %d</small><i style="width:%dpx"></i></div>' % (i + 1, w) for i, w in enumerate((104, 72, 118, 88, 60)))

parts = [
 '<div class="shead" style="top:2px"><i>1</i>Code builds the files only from records that passed each check</div>',
 '<div class="card tall back" style="left:36px;top:66px"></div><div class="card tall back" style="left:28px;top:58px"></div>',
 hot('rec', 'card tall', 'left:20px;top:50px', card, 'The question records'),
 '<div class="cap" style="left:20px;top:300px;width:262px">60 question records. Each one passed its checks.</div>',
 hot('gate', 'gate', 'left:346px;top:50px', gate, 'Three checks before the build'),
 hot('fp', 'fp', 'left:346px;top:194px', fp, 'The fingerprint'),
 '<div class="failnote" style="left:346px;top:286px">A check fails: code builds no file and names the cause.</div>',
 hot('qfile', 'jfile', 'left:690px;top:50px', qfile, 'The questions file'),
 hot('afile', 'jfile', 'left:690px;top:188px', afile, 'The answers file'),
 '<div class="shead" style="top:346px"><i>2</i>The 60 questions are in groups by scenario, as in the exam</div>',
] + [hot('seq', 'grp', 'left:%dpx;top:382px' % (20 + i * 247), group(i), 'The sequence of the questions') for i in range(4)] + [
 '<div class="shead" style="top:546px"><i>3</i>Two files, so that the answers stay away until the end</div>',
 hot('during', 'jmini', 'left:20px;top:596px', '<i class="jf"></i><b>questions</b><small>no answers</small>', 'During the mock'),
 '<div class="alab" style="left:150px;top:592px;width:96px">during<br>the mock</div>',
 '<div class="pers" style="left:262px;top:586px">' + person + '</div>',
 '<div class="alab" style="left:374px;top:592px;width:96px">after<br>the mock</div>',
 hot('after', 'jmini', 'left:490px;top:596px', '<i class="jf"></i><b>answers</b><small>and reasons</small>', 'After the mock'),
 hot('domains', 'dpanel', 'left:690px;top:582px', dbars, 'A result for each domain'),
]
paths = ['<path class="flow" d="M288,160 H342" marker-end="url(#a)"/>',
         '<path class="flow" d="M640,150 C664,150 664,110 686,110" marker-end="url(#a)"/>',
         '<path class="flow" d="M640,150 C664,150 664,248 686,248" marker-end="url(#a)"/>',
         '<path class="flow" d="M146,630 H258" marker-end="url(#a)"/>',
         '<path class="flow" d="M486,630 H374" marker-end="url(#a)"/>',
         '<path class="flow" d="M616,630 H686" marker-end="url(#a)"/>']

base9 = g9[g9.index('extra_css += """') + len('extra_css += """'):g9.index('"""\na = js.index')]
extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 712px; }')
assert '712px' in extra_css
extra_css += base9 + """  .card.tall { height: 236px; }
  .stamps { display: flex; gap: 5px; margin-top: 12px; }
  .stamp { font-size: 10.5px; font-weight: 700; color: var(--owner); background: var(--owner-bg); border: 1px solid var(--owner); border-radius: 999px; padding: 1px 7px; white-space: nowrap; }
  .stamp::before { content: '\\2713  '; }
  .gate, .fp, .jfile, .grp, .dpanel { background: var(--panel); border: 1.5px solid var(--line); border-radius: 12px; }
  .gate:hover, .fp:hover, .jfile:hover, .grp:hover, .dpanel:hover, .jmini:hover { border-color: var(--muted); }
  .gate { width: 290px; height: 134px; padding: 12px 16px; border-color: var(--code); }
  .gate h4, .grp h4, .dpanel h4 { margin: 0 0 8px; font-size: 14.5px; }
  .ck { margin: 5px 0; padding-left: 24px; position: relative; font-size: 13.5px; }
  .ck::before { content: '\\2713'; position: absolute; left: 0; top: -1px; width: 17px; height: 17px; border-radius: 50%; background: var(--code); color: var(--panel); font-size: 11px; font-weight: 700; display: grid; place-items: center; }
  .fp { width: 290px; height: 82px; padding: 10px 14px; }
  .fprow { display: flex; align-items: center; gap: 8px; margin: 3px 0; font-size: 12.5px; }
  .fpc { font: 12px/1 ui-monospace, Consolas, monospace; padding: 5px 8px; border-radius: 6px; background: var(--bg); border: 1px solid var(--line); }
  .fpc.no { border-color: var(--fail); color: var(--fail); }
  .fprow em { margin-left: auto; font-style: normal; font-weight: 700; font-size: 12.5px; }
  .yes { color: var(--owner); } .nope { color: var(--fail); }
  .failnote { position: absolute; width: 290px; padding: 7px 12px; border: 1.5px dashed var(--fail); border-radius: 10px; background: var(--fail-bg); font-size: 12.5px; }
  .jfile { width: 290px; height: 128px; overflow: hidden; }
  .jfile .bar { height: 30px; display: flex; align-items: center; gap: 8px; padding: 0 12px; font-weight: 700; font-size: 13px; background: var(--bg); border-bottom: 1px solid var(--line); }
  .jf { flex: none; width: 13px; height: 16px; border-radius: 2px; background: var(--code); display: inline-block; }
  .fbody { display: flex; gap: 12px; padding: 12px 14px; }
  .fbody.col { display: block; padding: 9px 14px; }
  .qn { flex: none; width: 26px; font-size: 13px; font-variant-numeric: tabular-nums; }
  .fl { flex: 1; } .fl .sk:first-child { margin-top: 3px; }
  .chips { display: flex; align-items: center; gap: 6px; margin-top: 10px; }
  .chips small { margin-left: auto; font-size: 11.5px; color: var(--muted); }
  .arow { display: flex; align-items: center; gap: 6px; height: 25px; }
  .arow .sk { margin: 0 0 0 6px; flex: none; width: 45% !important; }
  .okc { background: var(--owner); border-color: var(--owner); color: var(--panel); }
  .grp { width: 219px; height: 150px; padding: 10px 14px; }
  .story { background: var(--code-bg); border-radius: 8px; padding: 5px 10px 4px; margin-bottom: 9px; }
  .story small { font-size: 11px; font-weight: 700; color: var(--code); }
  .story .sk { margin: 5px 0; background: var(--code); opacity: .35; }
  .g15 { display: grid; grid-template-columns: repeat(15, 1fr); gap: 3px; }
  .g15 i { height: 10px; border-radius: 3px; background: var(--muted); opacity: .55; }
  .grp > span { display: block; margin-top: 6px; font-size: 12px; color: var(--muted); }
  .jmini { width: 122px; height: 68px; padding: 10px 12px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 8px; }
  .jmini b { margin-left: 8px; font-size: 14px; } .jmini small { display: block; margin-top: 4px; font-size: 12px; color: var(--muted); }
  .pers { position: absolute; width: 96px; text-align: center; }
  .pers svg { position: static; display: block; margin: 0 auto 2px; }
  .pers b { font-size: 13px; }
  .dpanel { width: 290px; height: 124px; padding: 10px 14px; }
  .dbar { display: flex; align-items: center; gap: 8px; height: 16px; }
  .dbar small { width: 62px; font-size: 11.5px; color: var(--muted); }
  .dbar i { height: 8px; border-radius: 4px; background: var(--owner); }
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
<title>Step 8: build the files</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 8: code builds the two files of the mock</h1>
  <p class="sub">This diagram shows step 8. The step is built, and it built mocks 1 to 5, from 8 to 9 October 2026. This is the last step. Code builds the files that the portal uses, and only from records that passed each check. Nobody edits the files by hand. Put the pointer on a part of the picture, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 712" width="1000" height="712" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 10. Design of 6 October 2026, corrected on 7 October 2026 (decisions 0036 and 0039). Status of the step: built, ran for mocks 1 to 5. The cards, the files and the bars are drawings. They show the form, not real questions or real results. Each exam guide text in a popup is the exact text of the guide.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/10-step-8-build-the-files.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
