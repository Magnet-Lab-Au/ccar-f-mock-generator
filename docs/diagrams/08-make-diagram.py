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
   sent=['Each of the 60 slots has exactly one question that passed steps 3 and 4.'],
   example=cf('C1', 'Slot M1-S41 has no question that passed.'), examplehead=EF,
   why='This step reads the mock as a whole. A hole in the mock makes each count wrong. So the step does not start before each slot is full.'),
 'C2': dict(title='Rule C2: the counts agree with the plan', who='Code', cls='code',
   sent=['Code counts the questions for each scenario, each domain, each task statement and each question type. Each count agrees with the plan of step 1.'],
   example=cf('C2', 'Domain 4 has 11 questions. The plan says 12.'), examplehead=EF,
   why='The plan gives the mock the form of the exam. After many new tries, code makes sure that the mock still agrees with its plan.'),
 'C3': dict(title='Rule C3: no two questions have the same text', who='Code', cls='code',
   sent=['No two questions of the mock have the same text.'],
   example=cf('C3', 'Questions M1-S07-T1 and M1-S52-T2 have the same text.'), examplehead=EF,
   why='Code finds an exact copy for no cost. A copy with different words is the work of the model call.'),
 'q15': dict(title='The 15 questions of one scenario', who='From steps 2 to 5', cls='io',
   sent=['All questions of one scenario that passed steps 3 and 4.',
         'Call 6a gets each question with its options and marks. Call 6b gets the wrong options with their reasons.',
         '15 questions with their options are about %d words, if they have the length of the sample questions of the exam guide.' % n15],
   why='A mock has 4 scenarios. So a mock has 4 of these sets, and 8 calls in this step.'),
 'c6a': dict(title='Call 6a: the scenes', who='One model call', cls='model',
   sent=['A model call reads the 15 questions of one scenario together. It has one job: to compare the scenes of the questions.',
         'For each of its 2 rules it returns "pass", "fail" or "cannot decide". A finding names the questions by their IDs.'],
   points=[point('4.6-K3'), point('4.6-S2')],
   why='The guide wrote these points for the review of code in many files. Here a question is the file: steps 3 and 4 are the pass for each question, and this step is the pass across the questions. Each call has one job, so that its attention is not divided.'),
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
 'fail': dict(title='A rule fails: one question goes back', who='Back to the writer', cls='stop',
   sent=['Each finding names the questions. When a finding names two questions or more, the question with the highest slot number goes to step 5. Code selects it, not the model.',
         'The writer gets the finding and the text of the other question. So it can write a different scene.']),
 'again': dict(title='Checked again', who='Steps 3, 4 and 6', cls='io',
   sent=['The new question goes through steps 3 and 4.', 'Then this step checks that scenario again: the code count and both calls.']),
 'cd': dict(title='Cannot decide: into the report', who='The owner', cls='open',
   sent=['A call can answer "cannot decide" for a rule.',
         'Then the finding goes into the report of the run. The owner sees it in step 7. No question is written again for it.'],
   why='A finding of this step names two questions or more. If the call cannot decide, the program does not know which question to write again. So a person looks at it.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g3[g3.index('def box('):g3.index('rows = [(')])
exec(g5[g5.index('def rowbox('):g5.index('rows = [(', g5.index('def rowbox('))])

boxes, paths = [], []
# the mock as a grid of 4 x 15 questions
cells = []
for r in range(4):
    for c in range(15):
        cells.append('<i class="cell%s" style="left:%dpx;top:%dpx"></i>' % (' hi' if r == 2 else '', 50 + c * 27, 88 + r * 30))
grid = ''.join(cells)
for i, (key, name, what) in enumerate([('C1', 'Each slot is full', 'Each of the 60 slots has one question that passed.'),
                                       ('C2', 'The counts agree with the plan', 'Scenario, domain, task statement and type.'),
                                       ('C3', 'No equal questions', 'No two questions have the same text.')]):
    boxes.append(rowbox(key, 530, 38 + i * 65, 450, 60, key, name, what).replace('class="box step row"', 'class="box step row crow"'))
boxes.append(box('q15', 20, 376, 220, 96, 'The 15 questions', 'All questions of one scenario, together.'))
boxes.append(box('c6a', 290, 298, 220, 112, '6a. The scenes', 'One job: compare the scenes.', 'One model call', 'model', extra='mdl'))
boxes.append(box('c6b', 290, 438, 220, 112, '6b. The wrong options', 'One job: find wrong ideas that repeat.', 'One model call', 'model', extra='mdl'))
for key, top, name, what in [('D1', 292, 'No two questions have the same scene', 'The same problem and the same correct action.'),
                             ('D4', 357, 'No question gives away another', 'No question has the answer of a different question.'),
                             ('D2', 432, 'No wrong idea repeats too often', 'In at most 2 questions of the scenario.'),
                             ('D3', 497, 'At most one confidence option', 'Ruling 2 of the owner.')]:
    boxes.append(rowbox(key, 560, top, 420, 60, key, name, what))
paths.append('<path class="flow" d="M240,424 C266,424 266,354 286,354" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M240,424 C266,424 266,494 286,494" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M510,354 H556" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M510,494 H556" marker-end="url(#a)"/>')
boxes.append(box('fail', 20, 620, 300, 118, 'A rule fails', 'The question with the highest slot number goes back to the writer, with the finding.', extra='fail'))
boxes.append(box('again', 350, 620, 300, 118, 'Checked again', 'Steps 3 and 4 check the new question. Then this step checks the scenario again.'))
boxes.append(box('cd', 680, 620, 300, 118, 'Cannot decide', 'The finding goes into the report. The owner sees it in step 7.', 'Possible', 'open'))
paths.append('<path class="flow" d="M320,679 H346" marker-end="url(#a)"/>')

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 754px; }')
assert '754px' in extra_css
extra_css += '''  .box.row .num { width: 34px; height: 34px; font-size: 14px; background: var(--model); color: var(--panel); }
  .box.crow .num { background: var(--code); }
  .box.mdl { border-color: var(--model); background: var(--model-bg); }
  .box.mdl .what { color: var(--ink); }
  .box.fail .name { color: var(--fail); }
  .cell { position: absolute; width: 21px; height: 21px; border-radius: 5px; background: var(--panel); border: 1.5px solid var(--line); }
  .cell.hi { background: var(--model-bg); border-color: var(--model); }
  .gnote { position: absolute; font-size: 12.5px; color: var(--muted); }
'''
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = g4[g4.index("fill = '''") + 10:g4.index("'''\njs2 = js[:a]")]
js2 = js[:a] + fill + js[b:]
popdiv = g3[g3.index("popdiv = '''") + 12:g3.index("'''\ndata = json.dumps")]
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
  <h1>Step 6: the mock is checked as a whole</h1>
  <p class="sub">This diagram shows the design. The step is not built yet. Steps 3 and 4 look at one question. Some defects show only when many questions are read together, for example two questions with the same scene. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 754" width="1000" height="754" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>Code counts all 60 questions</div>
    <div class="panel" style="left:20px;top:38px;width:470px;height:190px"></div>
    <div class="ptitle" style="left:34px;top:48px">One mock<small>4 scenarios, 15 questions each</small></div>
    ''' + grid + '''
    <div class="gnote" style="left:50px;top:206px;background:var(--bg);padding:0 6px">the two calls of part 2 read one scenario at a time</div>
    <div class="shead" style="top:256px"><i>2</i>Two model calls read the 15 questions of one scenario together</div>
    <div class="shead" style="top:584px"><i>3</i>What happens with a finding</div>
    ''' + ''.join(boxes) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 08. Design of 6 October 2026. Status of the step: planned. The step is not built. Each exam guide text is the exact text of the guide. A script took it from the records file. The examples of findings are invented, to show the form.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/08-step-6-check-the-complete-mock.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'boxes', len(boxes))
