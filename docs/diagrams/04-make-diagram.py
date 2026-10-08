import re, html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
SCHEMA = open(root + '/docs/diagrams/04-form-schema-draft.json', encoding='utf-8').read().rstrip()
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
e = html.escape
TS = {t['id']: t for t in REC['task_statements']}
PT = {p['id']: (p, t) for t in REC['task_statements'] for p in t['points']}
SC = {s['id']: s for s in REC['scenarios']}

def point(pid):
    p, t = PT[pid]
    assert p['text'] in guide
    return {'id': pid, 'text': p['text'], 'ctx': 'From task statement %s: %s' % (t['id'], t['title'])}

def js_(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

answers = [q['correct_answer'][0] for q in REC['sample_questions']]
assert answers.count('A') == 10 and len(answers) == 12
tech = REC['section_17']['technologies']
assert len(tech) == 14
ts12 = TS['1.2']
ts_lines = ['Task statement 1.2: ' + ts12['title'], '']
for p in ts12['points']:
    ts_lines.append(('>> ' if p['id'] == '1.2-K2' else '   ') + p['id'] + '  ' + p['text'])
slot = {'slot_id': 'M1-S17', 'scenario': 3, 'task_statement': '1.2', 'point': '1.2-K2',
        'type': 'multiple_choice', 'options': 4, 'select': 1}
q4 = REC['sample_questions'][3]
filled = {'status': 'written', 'question': q4['question'],
          'options': [{'text': q4['options'][k], 'correct': k in q4['correct_answer'], 'reason': '(why this option is correct or wrong)'} for k in 'ABCD'],
          'cannot_write_reason': None}
record_ids = {'question_id': 'M1-S17-T1', 'slot_id': 'M1-S17', 'try': 1, 'model': '(the model of the call)', 'date': '(the date of the call)'}

D = {
 'rules': dict(title='The rules for a good question', who='Fixed text', cls='io',
   sent=['One list of exact rules for a good question. It is the same for each call.',
         'The writer and the checkers use the same list: 19 rules, A1 to A12 for code and B1 to B7 for a model.',
         'The slot shown to the writer says if the longest option may be correct (decision 0053). If not, rule A12 asks for a wrong option that is longer than each correct option.',
         'One instruction has no rule of its own: the options of a question have the same form. The instruction "one name for one actor" has a rule: B7.'],
   points=[point('4.1-K1')],
   why='The guide wrote this point for the review of code. Here it applies to a question: an exact rule gives the same result each time. A vague rule does not.'),
 'examples': dict(title='3 sample questions', who='From the records file', cls='io',
   sent=['3 of the 12 sample questions of the exam guide. They show the writer the form and the level of an exam question.',
         'Code takes them from scenarios that are not the scenario of the slot. So the writer cannot copy the scene of an example.',
         'Code mixes the options, removes the letters, marks the correct option and leaves out the explanation.'],
   points=[point('4.2-K1'), point('4.2-S2')],
   why='The guide wrote these points for output in a fixed format. Here the examples show the writer what a good exam question is.'),
 'story': dict(title='The story of the scenario', who='From the records file', cls='io',
   sent=['The story of the scenario of the slot. Each question of the mock is inside the story of its scenario.'],
   example=SC[3]['story'], examplehead='Example: the story of scenario 3'),
 'ts': dict(title='The task statement, with the point marked', who='From the records file', cls='io',
   sent=['The task statement of the slot with all its points.',
         'The point of the slot is marked. The question must test that point. The other points show the writer what is near it.'],
   example='\n'.join(ts_lines), examplehead='Example: task statement 1.2, with point 1.2-K2 marked'),
 'tech': dict(title='The 14 technologies', who='From the records file', cls='io',
   sent=['Section 17 of the exam guide lists 14 technologies and concepts.',
         'A question depends only on features that the guide names. The writer gets this list for that rule.'],
   example='\n'.join(tech[:3] + ['...']), examplehead='Example: the first 3 of the 14'),
 'slot': dict(title='The slot', who='From the plan of step 1', cls='io',
   sent=['One of the 60 slots of the plan. It says what this one question must be.',
         'A multiple-choice question has 4 options and 1 correct answer. A multiple-response question has 5 options and 2 correct answers.',
         'The exam guide gives no number for a multiple-response question. "5 options, 2 correct" is a guess.'],
   example=js_(slot), examplehead='Example: slot 17 of mock 1'),
 'form': dict(title='The form that the model must fill', who='Fixed text', cls='io',
   sent=['The blanks of the answer, as a JSON schema. The request carries it as structured outputs, in the field output_config.format. The API makes the answer agree with the schema.',
         'A deviation from the exam guide. The guide teaches a forced tool call for this (4.3-S3, below). The newest Claude models reject a forced tool call. The page "Define tools" of the Anthropic documentation, section "Controlling Claude\'s output", subsection "Forcing tool use", says for Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1: "any and tool return a 400 error". As the replacement it names "auto with strict tool use", or "structured outputs when you need a response in a fixed JSON shape". An older model, Claude Opus 5, still accepts a forced tool call, but this build keeps the choice of the model free. So this build uses structured outputs. A copy of the page, read on 7 October 2026, is in docs/sources/.',
         'A form stops format errors. It does not stop content errors, for example 3 options in place of 4. Step 3 checks those.'],
   example=SCHEMA, examplehead='The form (the draft schema, used in the test of 7 October 2026)',
   points=[point('4.3-K1'), point('4.3-S3'), point('4.3-K3')],
   why='The guide wrote these points for the extraction of data from documents. Here they apply to a question: the model fills a form, so code can read each answer with no guess. The purpose of 4.3-K1 and 4.3-S3 stays: an answer that agrees with a schema. Only the method changes.'),
 'writer': dict(title='The writer', who='One model call', cls='model',
   sent=['One call of the plain API writes one question.',
         'The call is new each time. It does not know the other questions of the mock.',
         'The model is a setting. The first value is Claude Opus 5.5 at effort "high". The test before the first full run used it.'],
   why='One call makes one record. If one question fails, the program writes that one again and the others do not change.'),
 'written': dict(title='The answer: a question', who='The filled form', cls='io',
   sent=['The model returns the question, and each option with "correct" or "wrong" and a reason.',
         'The options have no letters.',
         'Each option has its own reason. Later the answer key is built from these reasons.'],
   example=js_(filled), examplehead='Example: the form, filled with sample question 4 of the guide',
   examplenote='The reasons are left out in this example.'),
 'cannot': dict(title='The answer: "cannot write"', who='The filled form', cls='open',
   sent=['The model can answer "cannot write", with a reason. Example: the point of the slot does not fit the story of the scenario.',
         'The slot is open at once, and the owner decides. The program does not invent a question.'],
   points=[point('4.3-S4')],
   why='The guide wrote this point for the extraction of data. Here it applies to a question: if the model must fill each blank, it invents a question for a slot that does not fit. That question looks good and is bad.'),
 'letters': dict(title='Code gives the letters', who='Code', cls='code',
   sent=['Code mixes the options and gives them the letters. The seed of the plan controls the sequence, so the same answer always gets the same letters.',
         'The model does not select the letters.'],
   why='In the 12 sample questions of the exam guide, the correct answer is A 10 times. A model that sees those examples can copy that, and then a participant can guess the answer. This is an assumption. It is not checked.'),
 'ids': dict(title='Code adds the IDs', who='Code', cls='code',
   sent=['Code adds the ID of the question, the slot, the number of the try, the model and the date.',
         'M1-S17-T1 is mock 1, slot 17, try 1.'],
   example=js_(record_ids), examplehead='Example: the fields that code adds',
   why='Each later verdict names exactly one question and one try.'),
 'save': dict(title='Code saves one file', who='Code', cls='code',
   sent=['Code saves the record as one JSON file for each try, for example runs/mock-01/questions/M1-S17-T1.json.',
         'A new try makes a new file. No file is written over.',
         'Then step 3 checks the question.'],
   why='The record of each try stays. So we can see later how a question changed.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g3[g3.index('def box('):g3.index('rows = [(')])  # the function box() of diagram 03

rows = [('rules', 'The rules for a good question', 'Fixed text. The same for each call.'),
        ('examples', '3 sample questions', 'From the records file. Examples of the form.'),
        ('story', 'The story of the scenario', 'From the records file.'),
        ('ts', 'The task statement', 'From the records file. One point is marked.'),
        ('tech', 'The 14 technologies', 'From the records file. What the guide names.'),
        ('slot', 'The slot', 'From the plan of step 1.'),
        ('form', 'The form', 'The blanks that the model must fill.')]
Y0, RH, GAP, MID = 84, 62, 6, 319
boxes, paths = [], []
for i, (key, name, what) in enumerate(rows):
    top = Y0 + i * (RH + GAP)
    boxes.append(box(key, 32, top, 356, RH, name, what, extra='row'))
    yc = top + RH // 2
    paths.append('<path class="flow" d="M388,%d C414,%d 414,%d 438,%d"/>' % (yc, yc, MID, MID))
boxes.append(box('writer', 440, 264, 170, 110, 'The writer', 'Writes one question for one slot.', 'One model call', 'model', extra='mdl'))
boxes.append(box('', 425, 446, 200, 82, 'If the call fails', 'Code runs it again, at most 3 times. Then an error record.', extra='stop'))
boxes.append(box('written', 662, 209, 306, 100, 'A question', 'The question, and each option with "correct" or "wrong" and a reason.', 'Usual', 'owner'))
boxes.append(box('cannot', 662, 329, 306, 100, '"Cannot write"', 'With a reason. The slot is open, and the owner decides.', 'Possible', 'open'))
for yc in (259, 379):
    paths.append('<path class="flow" d="M612,%d C636,%d 636,%d 658,%d" marker-end="url(#a)"/>' % (MID, MID, yc, yc))
boxes.append(box('letters', 20, 624, 280, 118, 'Gives the letters', 'Mixes the options and gives them A to D, or A to E. The model does not select the letters.', 'Code', 'code'))
boxes.append(box('ids', 360, 624, 280, 118, 'Adds the IDs', 'Example: M1-S17-T1 is mock 1, slot 17, try 1.', 'Code', 'code'))
boxes.append(box('save', 700, 624, 280, 118, 'Saves one file', 'One file for each try. Then step 3 checks the question.', 'Code', 'code'))
paths.append('<path class="flow" d="M300,683 H356" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M640,683 H696" marker-end="url(#a)"/>')

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 758px; }')
assert '758px' in extra_css
extra_css += '''  .box.mdl { border-color: var(--model); background: var(--model-bg); }
  .box.mdl .what { color: var(--ink); }
'''
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = '''  function fill(d) {
    var who = document.getElementById('popwho');
    who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    var s = document.getElementById('popbody'); s.textContent = '';
    d.sent.forEach(function (t) { s.appendChild(el('p', null, t)); });
    if (d.example) {
      s.appendChild(el('h3', null, d.examplehead)); s.appendChild(el('pre', null, d.example));
      if (d.examplenote) s.appendChild(el('p', 'exnote', d.examplenote));
    }
    if (d.points.length) {
      s.appendChild(el('h3', null, 'The exam guide says'));
      var ul = el('ul');
      d.points.forEach(function (p) {
        var li = el('li'); li.appendChild(el('span', 'pid', p.id)); li.appendChild(document.createTextNode(' '));
        li.appendChild(el('span', 'ptext', p.text)); li.appendChild(el('span', 'pctx', p.ctx)); ul.appendChild(li);
      });
      s.appendChild(ul);
    }
    if (d.why) { s.appendChild(el('h3', null, d.points.length ? 'Why here' : 'Why')); s.appendChild(el('p', null, d.why)); }
  }

'''
js2 = js[:a] + fill + js[b:]
popdiv = g3[g3.index("popdiv = '''") + 12:g3.index("'''\ndata = json.dumps")]
data = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Step 2: write the question</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 2: one API call writes one question</h1>
  <p class="sub">This diagram shows step 2. The step is built, and it ran in the test of 7 October 2026. For each of the 60 slots of a mock, code builds one request, a model fills a form, and code completes the record. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 758" width="1000" height="758" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>Code builds the request, and the model fills the form</div>
    <div class="panel" style="left:20px;top:38px;width:380px;height:528px"></div>
    <div class="ptitle" style="left:34px;top:46px">What code sends<small>the request</small></div>
    <div class="panel" style="left:650px;top:163px;width:330px;height:278px"></div>
    <div class="ptitle" style="left:664px;top:171px">What comes back<small>one of two answers</small></div>
    <div class="shead" style="top:588px"><i>2</i>Code completes the record of the question</div>
    ''' + ''.join(boxes) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 04. Design of 6 October 2026, corrected on 7 October 2026 (decisions 0040, 0041 and 0043) and on 8 October 2026 (decision 0053). Status of the step: built. Each exam guide text and each example from the records file is an exact copy. A script took it from the file.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/04-step-2-write-the-question.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'boxes', len(boxes))
