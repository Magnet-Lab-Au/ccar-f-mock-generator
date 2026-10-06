"""Makes docs/diagrams/07-step-5-try-again.html. Run: python3 07-make-diagram.py"""
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

f3 = {'step': 3, 'rule': 'A6', 'detail': 'The question has 140 words. The limit is 110.'}
f4 = {'step': 4, 'rule': 'B1', 'detail': 'The blind call selected option C. The writer marked option B. (Then the reason of the blind call.)'}
f7 = {'step': 7, 'rule': None, 'detail': '(the reason of the owner)'}
report = {'slot_id': 'M1-S17', 'status': 'open', 'tries': [
    {'question_id': 'M1-S17-T1', 'verdict': 'fail', 'findings': '(the findings of try 1)'},
    {'question_id': 'M1-S17-T2', 'verdict': 'fail', 'findings': '(the findings of try 2)'},
    {'question_id': 'M1-S17-T3', 'verdict': 'fail', 'findings': '(the findings of try 3)'}]}
EF = 'Example of a finding'
D = {
 's3': dict(title='From step 3: a code rule fails', who='Code', cls='code',
   sent=['Step 3 found that one of the 7 exact rules fails.'], example=js_(f3), examplehead=EF),
 's4': dict(title='From step 4: a rule fails, or "cannot decide"', who='One model call', cls='model',
   sent=['Step 4 found that the blind answer is different from the marks, or that one of the 6 rules fails.',
         'The verdict "cannot decide" also sends the question here, with its reason.'], example=js_(f4), examplehead=EF),
 's6': dict(title='From step 6: the check of the complete mock', who='Code and a model', cls='io',
   sent=['Step 6 reads all questions of one scenario together. It can name a question, for example when two questions have the same scene.',
         'The design of step 6 is not complete. So the form of its findings is not decided.']),
 's7': dict(title='From step 7: a bad mark of the owner', who='The owner', cls='owner',
   sent=['The owner marks a question bad, with one reason. That reason is the finding.'], example=js_(f7), examplehead=EF),
 'req': dict(title='The request of step 2', who='The same as in step 2', cls='io',
   sent=['All parts of the request of step 2: the rules, the 3 sample questions, the story, the task statement, the 14 technologies, the slot and the form.',
         'The model answers in the same form as in step 2. So each try has the same form, and steps 3 and 4 check each try in the same way.']),
 'failed': dict(title='The failed question', who='From the last try', cls='io',
   sent=['The complete record of the last failed try: the question, the options, the marks and the reasons.',
         'The writer does not see the tries before that. So the request stays short.'],
   points=[point('4.4-S1')],
   why='The guide wrote this point for the extraction of data. Here the "document" is the request of step 2, the "failed extraction" is the failed question, and the "validation errors" are the findings.'),
 'findings': dict(title='The findings', who='From the checks', cls='io',
   sent=['The list of findings of the last try. Each finding names its step, its rule and its detail.'],
   example=js_([f3, f4]), examplehead='Example: a list of two findings',
   points=[point('4.4-K1')],
   why='The guide wrote this point for the extraction of data. Here it applies to a question: with the exact findings the writer knows what to change. With no findings it can make the same error again.'),
 'writer': dict(title='The writer', who='One model call', cls='model',
   sent=['A new call of the plain API. It is the writer of step 2, with two more parts in the request.',
         'It can also answer "cannot write".']),
 'new': dict(title='A new question record', who='File', cls='io',
   sent=['A new record with the next try number. M1-S17-T2 is try 2 of slot 17.',
         'The record of try 1 stays. No file is written over. So we can see later how the question changed.']),
 'again': dict(title='Checked again', who='Steps 3 and 4', cls='io',
   sent=['The new question is a new text. A check of the old text says nothing about the new text.',
         'So steps 3 and 4 check it as a new question. The checker does not see the earlier findings.'],
   why='A checker that sees the earlier findings looks only for those findings.'),
 't1': dict(title='Try 1', who='Step 2', cls='io', sent=['The first question for the slot, from step 2.', 'If it passes the checks, the slot is full and this step does not run.']),
 't2': dict(title='Try 2', who='Step 5', cls='io', sent=['The writer gets try 1 and its findings, and writes the question again.']),
 't3': dict(title='Try 3', who='Step 5', cls='io', sent=['The writer gets try 2 and its findings, and writes the question again.', 'It does not get try 1.', 'This is the last try for the slot.']),
 'open': dict(title='The slot stays open', who='The program stops', cls='stop',
   sent=['After 3 tries with no pass, the program stops the tries for this slot.',
         'It writes the slot into the report of the run, with each try and its findings.',
         'The mock is not complete. The owner decides what happens to the slot.'],
   example=js_(report), examplehead='Example: an open slot in the report',
   points=[point('4.4-K2'), point('1.1-S3')],
   why='The first point says that some errors do not go away with a new try. The guide wrote it for the extraction of data, and it gives no number. The number 3 is a guess. The limit is not the main way to stop. The main way to stop is a question that passes. The second point names the opposite as an error.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g3[g3.index('def box('):g3.index('rows = [(')])
boxes, paths = [], []
for i, (key, name, what, tag, cls) in enumerate([
        ('s3', 'Step 3', 'A code rule fails.', 'Code', 'code'),
        ('s4', 'Step 4', 'A rule fails, or "cannot decide".', 'One model call', 'model'),
        ('s6', 'Step 6', 'The check of the complete mock names the question.', None, 'io'),
        ('s7', 'Step 7', 'The owner marks the question bad.', 'The owner', 'owner')]):
    boxes.append(box(key, 20 + i * 245, 38, 225, 100, name, what, tag, cls))
rows = [('req', 'The request of step 2', 'The rules, the examples, the story, the task statement, the slot and the form.'),
        ('failed', 'The failed question', 'Only the last try.'),
        ('findings', 'The findings', 'Each one names its step, its rule and its detail.')]
MID = 368
for i, (key, name, what) in enumerate(rows):
    top = 246 + i * 84
    boxes.append(box(key, 32, top, 336, 76, name, what, extra='row'))
    paths.append('<path class="flow" d="M368,%d C398,%d 398,%d 426,%d"/>' % (top + 38, top + 38, MID, MID))
boxes.append(box('writer', 430, 312, 180, 112, 'The writer', 'Writes the question again.', 'One model call', 'model', extra='mdl'))
boxes.append(box('new', 660, 258, 320, 100, 'A new question record', 'The next try, for example M1-S17-T2. The same form as in step 2.', 'File', 'io'))
boxes.append(box('again', 660, 390, 320, 100, 'Checked again', 'Steps 3 and 4 check it as a new question.'))
paths.append('<path class="flow" d="M612,%d C636,%d 636,308 656,308" marker-end="url(#a)"/>' % (MID, MID))
paths.append('<path class="flow" d="M820,358 V386" marker-end="url(#a)"/>')
for i, (key, name, what) in enumerate([('t1', 'Try 1', 'The first question, from step 2.'),
                                       ('t2', 'Try 2', 'The writer gets try 1 and its findings.'),
                                       ('t3', 'Try 3', 'The writer gets try 2 and its findings.')]):
    boxes.append(box(key, 20 + i * 250, 564, 200, 110, name, what))
    paths.append('<path class="failp" d="M%d,619 H%d" marker-end="url(#af)"/>' % (220 + i * 250, 266 + i * 250))
boxes.append(box('open', 770, 564, 210, 110, 'The slot stays open', 'The program writes a report. The owner decides.', extra='stop'))
labels = ''.join('<div class="lbl" style="left:%dpx;top:596px">fails</div>' % (226 + i * 250) for i in range(3))

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 692px; }')
assert '692px' in extra_css
extra_css += '''  .box.mdl { border-color: var(--model); background: var(--model-bg); }
  .box.mdl .what { color: var(--ink); }
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
<title>Step 5: try again</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 5: a failed question goes back to the writer with the findings</h1>
  <p class="sub">This diagram shows the design. The step is not built yet. The step runs only for a question that did not pass. A question that passes the checks does not come here. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 692" width="1000" height="692" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>Four steps can send a question back</div>
    <div class="shead" style="top:164px"><i>2</i>The writer gets the question and the exact findings</div>
    <div class="panel" style="left:20px;top:200px;width:360px;height:302px"></div>
    <div class="ptitle" style="left:34px;top:210px">What code sends<small>the request</small></div>
    <div class="shead" style="top:528px"><i>3</i>At most 3 tries for one slot</div>
    ''' + ''.join(boxes) + labels + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 07. Design of 6 October 2026. Status of the step: planned. The step is not built. Each exam guide text is the exact text of the guide. A script took it from the records file. The examples of findings are invented, to show the form.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/07-step-5-try-again.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'boxes', len(boxes))
