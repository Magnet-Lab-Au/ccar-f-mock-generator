"""Makes docs/diagrams/08-step-6-check-the-complete-mock.html. Run: python3 08-make-diagram.py"""
import html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
g5 = open(root + '/docs/diagrams/05-make-diagram.py', encoding='utf-8').read()
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

w = lambda t: len(t.split())
qs = REC['sample_questions']
n15 = round(15 * sum(w(q['question']) + sum(w(o) for o in q['options'].values()) for q in qs) / 12, -2)
assert n15 == 1900
assert 'self-reported confidence scores' in PT['5.2-K3'][0]['text']
assert 'times out' in qs[7]['question']  # sample question 8 is the source of the scene in the D1 example

def cf(rule, detail):
    return js_({'rule': rule, 'detail': detail})

def df(rule, ids, detail):
    return js_({'rule': rule, 'result': 'fail', 'findings': [{'question_ids': ids, 'detail': detail}]})

EF = 'Example of a finding'
D = {
 'C1': dict(title='Rule C1: each slot is full', who='Code', cls='code',
   sent=['The current try of each of the 60 slots has the status passed. The current try is the try with the highest number.'],
   example=cf('C1', 'Slot M1-S41 has no question that passed.'), examplehead=EF,
   why='This step reads the mock as a whole. A hole in the mock makes each count wrong. So the step does not start before each slot is full. If C1 or C2 fails, the step stops with an error, and the mock waits for the owner.'),
 'C2': dict(title='Rule C2: the counts agree with the plan', who='Code', cls='code',
   sent=['Code counts the questions for each scenario, each domain, each task statement and each question type. Each count agrees with the plan of step 1.'],
   example=cf('C2', 'Domain 4 has 11 questions. The plan says 12.'), examplehead=EF,
   why='The plan gives the mock the form of the exam. After many new tries, code makes sure that the mock still agrees with its plan.'),
 'C3': dict(title='Rule C3: no two questions have the same text', who='Code', cls='code',
   sent=['No two questions of the mock have the same text.'],
   example=cf('C3', 'Questions M1-S07-T1 and M1-S52-T2 have the same text.'), examplehead=EF,
   why='Code finds an exact copy for no cost. A copy with different words is the work of the model call. A failure of C3 is a finding for the owner, as for the rules of the calls.'),
 'q15': dict(title='The 15 questions of one scenario', who='From steps 2 to 5', cls='io',
   sent=['The current try of each of the 15 slots of one scenario. Each one passed steps 3 and 4.',
         'Call 6a gets each question with its options and marks. Call 6b gets the wrong options with their reasons.',
         '15 questions with their options are about %d words, if they have the length of the sample questions of the exam guide.' % n15],
   why='A mock has 4 scenarios. So a mock has 4 of these sets, and 8 calls in this step.'),
 'c6a': dict(title='Call 6a: the scenes', who='One model call', cls='model',
   sent=['A model call reads the 15 questions of one scenario together. It has one job: to compare the scenes of the questions.',
         'For each of its 2 rules it returns "pass", "fail" or "cannot decide". A finding names the questions by their IDs.'],
   points=[point('4.6-K3'), point('4.6-S2')],
   why='The guide wrote these points for the review of code in many files. Here a question is the file: steps 3 and 4 are the pass for each question, and this step is the pass across the questions. The guide does not say to give each call one job. That is an assumption of the assistant: one call with 4 jobs can divide its attention.'),
 'c6b': dict(title='Call 6b: the wrong options', who='One model call', cls='model',
   sent=['A second model call reads the wrong options of the same 15 questions. It has one job: to find a wrong idea that repeats.',
         'For each of its 2 rules it returns "pass", "fail" or "cannot decide".'],
   why='A writer call sees only its own slot. It cannot know which wrong ideas the other questions use. Only a call that reads the questions together can count them.'),
 'D1': dict(title='Rule D1: no two questions have the same scene', who='One model call', cls='model',
   sent=['Two questions have the same scene when they have the same problem and the same correct action.'],
   example=df('D1', ['M1-S33-T1', 'M1-S38-T1'], 'Both questions describe a subagent that times out, and both ask how the error goes back to the coordinator.'), examplehead=EF,
   why='A writer call sees only its own slot. So two writer calls can write the same scene. Two questions with the same scene test one thing two times.'),
 'D4': dict(title='Rule D4: no question gives away another', who='One model call', cls='model',
   sent=['No question gives away the answer of a different question.'],
   example=df('D4', ['M1-S35-T1', 'M1-S33-T1'], 'The text of question M1-S35-T1 says that the coordinator gets structured error context. That is the correct answer of question M1-S33-T1.'), examplehead=EF,
   why='If one question answers another, a participant gets a point without the knowledge.'),
 'D2': dict(title='Rule D2: no wrong idea repeats too often', who='One model call', cls='model',
   sent=['No wrong idea is a wrong option in more than 2 questions of the scenario.', 'The number 2 is a guess. It can change after the first runs.'],
   example=df('D2', ['M1-S31-T1', 'M1-S36-T2', 'M1-S40-T1', 'M1-S44-T1'], 'The idea "use a model with a larger context window" is a wrong option in 4 questions.'), examplehead=EF,
   why='If the same wrong idea comes again and again, a participant can mark it wrong without thought.'),
 'D3': dict(title='Rule D3: at most one confidence option', who='One model call', cls='model',
   sent=['At most one wrong option of the scenario is this option: a model rates its own confidence, and the rating is used as a filter, a threshold or a trigger.',
         'A use of confidence that the exam guide teaches as correct does not count. The option also does not count when it is the correct answer.'],
   example=df('D3', ['M1-S32-T1', 'M1-S45-T1'], 'Each of these 2 questions has a wrong option in which the model rates its own confidence and a threshold sends the case to a person.'), examplehead=EF,
   points=[point('5.2-K3')],
   why='The guide wrote this point for escalation in customer support. It shows that this wrong option is fair. But if it comes many times, a participant can mark it wrong without thought. So the owner set a limit of one for each scenario.'),
 'finding': dict(title='A finding has an ID, and it waits', who='Code', cls='code',
   sent=['Each "fail" and each "cannot decide" of a call is a finding. Code gives each finding an ID.',
         'Example: M1-SC3-R1-F1 is mock 1, scenario 3, run 1 of step 6, finding 1.',
         'Step 6 sends no question back. Each finding waits for the owner.'],
   example=js_({'id': 'M1-SC3-R1-F1', 'rule': 'D1', 'result': 'fail', 'question_ids': ['M1-S33-T1', 'M1-S38-T1'],
                'detail': 'Both questions describe a subagent that times out, and both ask how the error goes back to the coordinator.'}),
   examplehead='Example: one finding in the record of step 6',
   why='A finding of this step names two questions or more. A person decides which one to write again, or none. An automatic choice needs more limits and statuses, and nobody knows yet if it is necessary. After mock 1 we know which findings occur.'),
 'report': dict(title='The report', who='Code', cls='code',
   sent=['Code puts each finding that has no decision into the field step6_findings of the report. The field shows the findings only after the automatic work and the marks of the owner are done.',
         'The field waiting_for says what the owner must do.'],
   example=js_({'state': 'waits_for_owner', 'waiting_for': ['finding M1-SC3-R1-F1 of step 6: ignore or rewrite']}),
   examplehead='Example: two fields of report.json'),
 'blind': dict(title='The owner marks first', who='The owner', cls='owner',
   sent=['The owner marks the questions in step 7 with no verdict in view.',
         'Code shows the findings only when the automatic work is done, step 6 checked the current questions, and no question waits for a mark.'],
   why='A mark that the owner gives after a verdict of a checker is not a blind mark.'),
 'ignore': dict(title='ignore: the finding closes', who='The owner', cls='owner',
   sent=['The owner reads the finding and its questions, and decides that the questions can stay.',
         'Code saves the decision. No question changes.']),
 'rewrite': dict(title='rewrite: one question goes back', who='The owner', cls='stop',
   sent=['The owner names the current try of one question of the finding, and gives a reason.',
         'That question goes to step 5. The writer gets the question, the finding, the reason of the owner and the text of the other question. So it can write a different scene.',
         'The other findings of the same run stay open. The owner decides each one.'],
   example=js_({'id': 'D004', 'action': 'rewrite', 'target': 'M1-SC3-R1-F1', 'question_id': 'M1-S38-T1', 'after_try': 1,
                'reason': 'Write a different scene.', 'date': '(the date)'}),
   examplehead='Example: the decision in owner-decisions.json'),
 'again': dict(title='Checked again, and no limit of rounds', who='Steps 3, 4 and 6', cls='io',
   sent=['The new question goes through steps 3 and 4.',
         'Then step 6 runs again, for its scenario only. The owner marks the new question, and then sees the new findings.',
         'No limit counts these rounds. The owner starts each one.'],
   why='The owner reads all 60 questions of mock 1, so a decision of the owner costs little. A limit would be one more guess.'),
 'valid': dict(title='An answer that is not valid', who='Code', cls='code',
   sent=['Code checks each answer of a call. A "fail" or "cannot decide" must have a finding, and each finding must name only current questions of this scenario.',
         'An answer that is not valid counts as a call that failed. Code runs the call again, at most 3 times. Then code saves an error record, and the owner starts the program again.'],
   why='A finding that names a question that does not exist gives the owner nothing to decide.'),
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
qc = lambda t: '<span class="qchip">%s</span>' % t

def rule(key, cls, name, what, left, top, width):
    return hot(key, 'rule ' + cls, 'left:%dpx;top:%dpx;width:%dpx' % (left, top, width),
               '<b class="rid">%s</b><span><b>%s</b><small>%s</small></span>' % (key, name, what), '%s: %s' % (key, name))

def call(key, name, job, left, top):
    return hot(key, 'call', 'left:%dpx;top:%dpx' % (left, top), '<b>%s</b><small>%s</small>' % (name, job), name)

# 1. the mock: 60 squares, one row for each scenario
mock = ('<h4>One mock</h4><div class="g60">%s</div><span class="glab">4 scenarios, 15 questions each. '
        'Each square is one question that passed steps 3 and 4.</span>' % ''.join('<i class="on"></i>' for _ in range(60)))

# 2. the 15 questions of one scenario
stack = ('<div class="chead"><span class="idchip">Scenario 3</span><span class="sc">15 questions</span></div>'
         + ''.join('<div class="mini">%s%s</div>' % (qc('M1-S%02d' % n), sk(40 + (n * 13) % 45)) for n in (31, 32, 33, 38, 45))
         + '<div class="more">and 10 more</div>')

# 3. one finding, the report, the owner
fcard = ('<div class="chead"><span class="idchip">M1-SC3-R1-F1</span><span class="res">D1 &middot; fail</span></div>'
         + '<div class="fq">' + qc('M1-S33-T1') + qc('M1-S38-T1') + '</div>' + sk(94) + sk(80) + sk(52))
record = '<b>report.json</b><small>step6_findings</small>'
person = ('<svg viewBox="0 0 90 78" width="70" height="60" aria-hidden="true"><circle cx="45" cy="24" r="17" style="fill:var(--owner)"/>'
          '<path d="M11,78 C11,54 28,46 45,46 C62,46 79,54 79,78 Z" style="fill:var(--owner)"/></svg>'
          '<b>The owner marks first</b><small>Then the owner sees the findings</small>')

parts = [
 '<div class="shead" style="top:2px"><i>1</i>Code counts all 60 questions</div>',
 '<div class="gpanel" style="left:20px;top:44px">%s</div>' % mock,
 rule('C1', 'c', 'Each slot is full', 'The current try of each of the 60 slots passed.', 520, 44, 460),
 rule('C2', 'c', 'The counts agree with the plan', 'Scenario, domain, task statement and type.', 520, 100, 460),
 rule('C3', 'c', 'No equal questions', 'No two questions have the same text.', 520, 156, 460),
 '<div class="shead" style="top:236px"><i>2</i>Two model calls read the 15 questions of one scenario together</div>',
 '<div class="card back" style="left:36px;top:294px"></div><div class="card back" style="left:28px;top:286px"></div>',
 hot('q15', 'card', 'left:20px;top:278px', stack, 'The 15 questions of one scenario'),
 call('c6a', '6a. The scenes', 'One job: compare the scenes.', 360, 278),
 rule('D1', 'm tall', 'No two questions have the same scene', 'Same problem, same correct action.', 360, 346, 290),
 rule('D4', 'm tall', 'No question gives away another', 'It does not show another answer.', 360, 414, 290),
 call('c6b', '6b. The wrong options', 'One job: find wrong ideas that repeat.', 690, 278),
 rule('D2', 'm tall', 'No wrong idea repeats too often', 'At most 2 questions of the scenario.', 690, 346, 290),
 rule('D3', 'm tall', 'At most one confidence option', 'Ruling 2 of the owner.', 690, 414, 290),
 hot('valid', 'valid', 'left:360px;top:484px;width:620px',
     'Code runs the call again after <b>an answer that is not valid</b>: a finding with no question, or with a question that is not in the scenario.',
     'An answer that is not valid'),
 '<div class="cap" style="left:20px;top:512px;width:262px">4 scenarios, so 8 calls for one mock</div>',
 '<div class="shead" style="top:564px"><i>3</i>Step 6 sends no question back. Each finding waits for the owner.</div>',
 hot('finding', 'card fcard', 'left:20px;top:606px', fcard, 'A finding has an ID'),
 hot('report', 'filebox', 'left:318px;top:644px', record, 'The report'),
 hot('blind', 'person', 'left:500px;top:610px', person, 'The owner marks first'),
 hot('ignore', 'seg g first2', 'left:720px;top:606px;width:260px', '<b>ignore</b><small>The finding closes.</small>', 'ignore'),
 hot('rewrite', 'seg x last2', 'left:720px;top:678px;width:260px', '<b>rewrite M1-S38-T1</b><small>Back to the writer, with a reason.</small>', 'rewrite'),
 hot('again', 'again', 'left:318px;top:784px;width:662px',
     '<b>Checked again.</b> Steps 3 and 4 check the new question. Then step 6 runs again for scenario 3 only, and the owner marks the new question. '
     'No limit counts these rounds: the owner starts each one.', 'Checked again'),
]
paths = [
 '<path class="flow" d="M286,330 C320,330 326,306 356,306" marker-end="url(#a)"/>',
 '<path class="flow" d="M286,344 C318,344 326,269 366,269 H664 C680,269 676,306 686,306" marker-end="url(#a)"/>',
 '<path class="flow" d="M298,675 H314" marker-end="url(#a)"/>',
 '<path class="flow" d="M472,675 H496" marker-end="url(#a)"/>',
 '<path class="flow" d="M680,654 C700,654 700,639 716,639" marker-end="url(#a)"/>',
 '<path class="flow" d="M680,664 C700,664 700,711 716,711" marker-end="url(#a)"/>',
 '<path class="flow" style="stroke:var(--fail)" d="M850,746 V780" marker-end="url(#af)"/>',
 '<path class="flow" d="M314,814 H160 V760" marker-end="url(#a)"/>',
]

g9 = open(root + '/docs/diagrams/09-make-diagram.py', encoding='utf-8').read()
Q = "'" * 3
extra_css = g3[g3.index('extra_css = ' + Q) + 15:g3.index(Q + '\na = js.index')]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 870px; }')
assert '870px' in extra_css
extra_css += g9[g9.index('extra_css += """') + 16:g9.index('"""\na = js.index')]
extra_css += """  .gpanel { position: absolute; height: 172px; }
  .g60 { margin-top: 10px; }
  .glab { display: block; font-size: 12.5px; color: var(--muted); margin-top: 8px; }
  .rule { min-height: 48px; display: flex; align-items: center; gap: 10px; padding: 0 12px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 10px; }
  .rule:hover { border-color: var(--muted); }
  .rule .rid { flex: none; width: 34px; height: 26px; border-radius: 6px; display: grid; place-items: center; font-size: 12.5px; }
  .rule.c .rid { background: var(--code-bg); color: var(--code); }
  .rule.tall { height: 60px; }
  .rule.m .rid { background: var(--model-bg); color: var(--model); }
  .rule > span { min-width: 0; }
  .rule span b { display: block; font-size: 13.5px; line-height: 1.25; }
  .rule span small { display: block; font-size: 12px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .call { width: 290px; height: 56px; padding: 7px 14px; background: var(--model-bg); border: 1.5px solid var(--model); border-radius: 28px; }
  .call:hover { box-shadow: 0 0 0 2px var(--model); }
  .call b { display: block; color: var(--model); font-size: 14.5px; } .call small { font-size: 12.5px; }
  .card .mini { display: flex; align-items: center; gap: 8px; margin-top: 7px; }
  .card .mini .sk { margin: 0; flex: 1; }
  .card .more { font-size: 12px; color: var(--muted); margin-top: 8px; }
  .qchip { flex: none; font-size: 11.5px; font-weight: 700; padding: 1px 7px; border-radius: 6px; background: var(--bg); border: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .valid { min-height: 30px; padding: 5px 12px; font-size: 12.5px; color: var(--muted); border: 1.5px dashed var(--code); border-radius: 8px; }
  .valid b { color: var(--code); }
  .fcard { width: 276px; height: 132px; }
  .fcard .res { font-weight: 700; color: var(--fail); }
  .fq { display: flex; gap: 6px; margin-bottom: 8px; }
  .person { width: 178px; }
  .seg { height: 66px; }
  .seg.first2 { border-radius: 10px 10px 0 0; } .seg.last2 { border-radius: 0 0 10px 10px; }
  .again { padding: 8px 14px; font-size: 13px; background: var(--panel); border: 1.5px solid var(--line); border-radius: 10px; }
  .again:hover { border-color: var(--muted); }
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
<title>Step 6: check the complete mock</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 6: code and two model calls check the mock as a whole</h1>
  <p class="sub">This diagram shows step 6. The step is built, and it ran in the test of 7 October 2026: call 6a found two questions with the same scene that the test put in on purpose. Steps 3 and 4 look at one question. Some defects show only when many questions are read together, for example two questions with the same scene. Step 6 finds them, and the owner decides. Put the pointer on a part of the picture, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 870" width="1000" height="870" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 08. Design of 7 October 2026 (decisions 0034, 0038 and 0039). Status of the step: built. The cards and the files are drawings. The examples of findings are invented, to show the form. Each exam guide text in a popup is the exact text of the guide.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
keys = set(D)
used = {p.split('data-step="')[1].split('"')[0] for p in parts if 'data-step="' in p}
assert used == keys, (keys - used, used - keys)
out = root + '/docs/diagrams/08-step-6-check-the-complete-mock.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
