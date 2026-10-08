"""Makes docs/diagrams/05-step-3-check-by-code.html. Run: python3 05-make-diagram.py"""
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

# the numbers of decision 0031, measured again here
w = lambda t: len(t.split())
qs = REC['sample_questions']
ql = [w(q['question']) for q in qs]
ol = [w(o) for q in qs for o in q['options'].values()]
ratios = []
for q in qs:
    c = [w(v) for k, v in q['options'].items() if k in q['correct_answer']]
    x = [w(v) for k, v in q['options'].items() if k not in q['correct_answer']]
    ratios.append((sum(c) / len(c)) / (sum(x) / len(x)))
assert (min(ql), max(ql), min(ol), max(ol)) == (33, 91, 7, 35) and round(max(ratios), 2) == 1.21
QW, OW, RATIO = (25, 110), (5, 45), 1.3
assert QW[0] <= min(ql) and max(ql) <= QW[1] and OW[0] <= min(ol) and max(ol) <= OW[1] and max(ratios) <= RATIO

def finding(rule, detail):
    return js_({'rule': rule, 'detail': detail})

verdict = {'question_id': 'M1-S17-T1', 'step': 3, 'verdict': 'fail',
           'findings': [{'rule': 'A6', 'detail': 'The question has 140 words. The limit is 110.'}],
           'date': '(the date of the check)'}
EH = 'Example of a finding'
D = {
 'q': dict(title='The question record', who='From step 2', cls='io',
   sent=['The record that step 2 saved for one try: the question, and each option with its letter, its mark "correct" or "wrong" and its reason.']),
 'slot': dict(title='The slot', who='From the plan of step 1', cls='io',
   sent=['The slot says what the question must be: the scenario, the point, the number of options and the number of correct answers.',
         'Code compares the question with its slot.']),
 'hdr': dict(title='Step 3: code checks 12 rules', who='Code', cls='code',
   sent=['Each of these 12 rules has one exact answer. So code checks them, and not a model.',
         'The step is cheap and fast. It runs before the model check of step 4, so a question with a simple defect does not use a model call.',
         'The rules that need judgment are the work of step 4, for example "only the marked answer is correct".'],
   points=[point('1.4-K1'), point('1.4-K2'), point('4.3-K3'), point('4.4-K4')],
   why='The guide wrote these points for workflows and for the extraction of data. Here they apply to a question record: the form of step 2 stops format errors, but it cannot count the options. So code checks the content.'),
 'A1': dict(title='Rule A1: the form is complete', who='Code', cls='code',
   sent=['The record has a question. Each option has a text, a mark "correct" or "wrong", and a reason. No text is empty.'],
   example=finding('A1', 'Option C has no reason.'), examplehead=EH,
   why='The answer key is built from the reasons. An option with no reason leaves a hole in the answer key.'),
 'A2': dict(title='Rule A2: the number of options', who='Code', cls='code',
   sent=['The question has the number of options that its slot says: 4 for multiple-choice, 5 for multiple-response.'],
   example=finding('A2', 'The question has 5 options. The slot says 4.'), examplehead=EH,
   why='The form of step 2 cannot count. Code can.'),
 'A3': dict(title='Rule A3: the number of correct options', who='Code', cls='code',
   sent=['The number of options that are marked correct is the number that the slot says: 1 for multiple-choice, 2 for multiple-response.'],
   example=finding('A3', '2 options are marked correct. The slot says 1.'), examplehead=EH,
   why='The question tells the participant how many answers to select. The marks must agree with that number.'),
 'A4': dict(title='Rule A4: no equal options', who='Code', cls='code',
   sent=['No two options have the same text.'],
   example=finding('A4', 'Options B and D have the same text.'), examplehead=EH,
   why='Two equal options are one option.'),
 'A5': dict(title='Rule A5: no letters in the text', who='Code', cls='code',
   sent=['No text names a letter or a different option. Examples: "Option B", "all of the above", "none of the above".'],
   example=finding('A5', 'The reason of option A has the words "Option B".'), examplehead=EH,
   why='Code mixes the options and gives the letters. A text that names a letter becomes wrong when the sequence changes.'),
 'A6': dict(title='Rule A6: the length', who='Code', cls='code',
   sent=['The question has %d to %d words. Each option has %d to %d words.' % (QW + OW),
         'These limits come from the 12 sample questions of the exam guide. A script measured them: the questions have %d to %d words, and the options have %d to %d words. Each limit is that range with a small margin.' % (min(ql), max(ql), min(ol), max(ol))],
   example=finding('A6', 'The question has 140 words. The limit is 110.'), examplehead=EH,
   why='The sample questions show the form of the exam. A mock question that is much longer or much shorter trains the wrong pace.'),
 'A7': dict(title='Rule A7: the correct option is not much longer', who='Code', cls='code',
   sent=['The correct option is at most %.1f times as long as the average of the wrong options.' % RATIO,
         'In the 12 sample questions of the exam guide, the largest value is %.2f.' % max(ratios)],
   example=finding('A7', 'The correct option has 40 words. The wrong options have 18 words on average. The limit is 1.3 times.'), examplehead=EH,
   why='If the correct option is always the longest, a participant can guess the answer from its length.'),
 'A8': dict(title='Rule A8: a question mark at the end', who='Code', cls='code',
   sent=['The text of the question ends with a question mark.', 'Each of the 12 sample questions of the guide does.'],
   example=finding('A8', 'The question does not end with a question mark.'), examplehead=EH),
 'A9': dict(title='Rule A9: 2 to 5 sentences', who='Code', cls='code',
   sent=['The text of the question has 2 to 5 sentences.',
         'A sentence ends with ".", "?" or "!" and a space comes after it. Known limit: a dot and then a quote mark does not end a sentence.'],
   example=finding('A9', 'The question has 6 sentences. The limit is 2 to 5.'), examplehead=EH),
 'A10': dict(title='Rule A10: each option is one sentence', who='Code', cls='code',
   sent=['No option has a sentence end inside it.'],
   example=finding('A10', 'Option B has more than one sentence.'), examplehead=EH),
 'A11': dict(title='Rule A11: not a negative question', who='Code', cls='code',
   sent=['The question text does not have "NOT" or "EXCEPT" in capital letters.',
         'The last sentence of the question text does not have "not" or "except" in small letters.',
         'The options do not count.'],
   example=finding('A11', 'The last sentence of the question has "not".'), examplehead=EH,
   why='No sample question of the guide is a negative question. A negative question tests careful reading more than knowledge.'),
 'A12': dict(title='Rule A12: the longest option', who='Code', cls='code',
   sent=['The plan marks each slot: may the longest option be correct? The seed says yes for 13 of the 52 slots with 1 answer and for 3 of the 8 slots with 2 answers (decision 0053).',
         'On the other slots, a wrong option must be longer (in characters) than each correct option. An equal length fails.',
         'A slot of a plan before decision 0053 has no mark. The rule does not apply to it.'],
   example=finding('A12', 'The longest option is a correct option (96 characters). The slot needs a wrong option that is longer than each correct option.'), examplehead=EH,
   why='In mock 1, the correct option was the longest in 37 of the 52 questions with 1 answer. Chance is 13. A participant who selects the longest option should not gain from it.'),
 'pass': dict(title='Pass', who='Usual', cls='owner',
   sent=['No rule fails.', 'The question goes to step 4. There a model checks the rules that need judgment.']),
 'fail': dict(title='Fail', who='Back to the writer', cls='stop',
   sent=['One rule or more fails.', 'The question goes to step 5. The writer gets the question and the exact findings, and writes it again.',
         'The new question goes through this check again.']),
 'rec': dict(title='The verdict record', who='File', cls='io',
   sent=['Code saves each verdict as one new file, for example runs/mock-01/checks/M1-S17-T1-step3.json.',
         'No file is written over. So the record of each check stays.'],
   example=js_(verdict), examplehead='Example: a verdict "fail"'),
 'finding': dict(title='A finding is exact', who='Code', cls='code',
   sent=['Each finding names the rule and the detail: what is wrong, where, and what the limit is.'],
   points=[point('4.4-K1')],
   why='The guide wrote this point for the extraction of data. Here it applies to a question: the writer of step 5 gets the exact findings, so it knows what to change.'),
 'err': dict(title='An error is not a pass', who='The step stops', cls='stop',
   sent=['If the file of the question is missing or cannot be read, the step reports an error.',
         'It never says "pass" for a question that it did not read.'],
   points=[point('5.3-K4')],
   why='The guide wrote this point for agents that report errors. Here it applies to a check: an empty result must not look like a success.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g3[g3.index('def box('):g3.index('rows = [(')])

def rowbox(key, left, top, wd, h, num, name, what):
    return ('<div class="box step row" data-step="%s" role="button" tabindex="0" aria-haspopup="dialog" aria-expanded="false" aria-controls="pop" '
            'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class="num">%s</div><div class="head"><span class="name">%s</span></div><p class="what">%s</p></div>'
            % (key, left, top, wd, h, num, e(name), e(what)))

rows = [('A1', 'The form is complete', 'Each option: a text, a mark, a reason.'),
        ('A2', 'The number of options', '4 or 5, as the slot says.'),
        ('A3', 'The number of correct options', '1 or 2, as the slot says.'),
        ('A4', 'No equal options', 'No two options have the same text.'),
        ('A5', 'No letters in the text', 'No "Option B", no "all of the above".'),
        ('A6', 'The length', 'Question %d to %d words. Option %d to %d.' % (QW + OW)),
        ('A7', 'Correct option not much longer', 'At most %.1f times the wrong options.' % RATIO),
        ('A8', 'A question mark at the end', 'The question ends with "?".'),
        ('A9', '2 to 5 sentences', 'In the text of the question.'),
        ('A10', 'Each option is one sentence', 'No sentence end inside an option.'),
        ('A11', 'Not a negative question', 'No "NOT" or "EXCEPT" in capital letters.'),
        ('A12', 'The longest option', 'Most slots: a wrong option is the longest.')]
boxes, paths = [], []
boxes.append(box('hdr', 312, 84, 376, 60, 'Code checks 12 rules', 'Each rule has one exact answer.', 'Code', 'code', extra='hdr row'))
for i, (key, name, what) in enumerate(rows):
    boxes.append(rowbox(key, 312, 150 + i * 58, 376, 54, key, name, what))
MID = 465
boxes.append(box('q', 20, 337, 230, 96, 'The question record', 'The question and its options, from step 2.', extra=''))
boxes.append(box('slot', 20, 497, 230, 96, 'The slot', 'What the question must be, from the plan.', extra=''))
for yc in (385, 545):
    paths.append('<path class="flow" d="M250,%d C276,%d 276,%d 296,%d" marker-end="url(#a)"/>' % (yc, yc, MID, MID))
boxes.append(box('pass', 750, 330, 230, 110, 'Pass', 'No rule fails. Step 4 checks the question next.', 'Usual', 'owner'))
boxes.append(box('fail', 750, 490, 230, 110, 'Fail', 'A rule fails. The question goes back to the writer with the findings.', extra='fail'))
paths.append('<path class="flow" d="M700,%d C724,%d 724,385 746,385" marker-end="url(#a)"/>' % (MID, MID))
paths.append('<path class="failp" d="M700,%d C724,%d 724,545 746,545" marker-end="url(#af)"/>' % (MID, MID))
boxes.append(box('rec', 20, 914, 300, 118, 'The verdict record', 'One new file for each check: the question, the verdict and the findings.', 'File', 'io'))
boxes.append(box('finding', 350, 914, 300, 118, 'A finding is exact', 'It names the rule and the detail, so the writer knows what to change.', 'Code', 'code'))
boxes.append(box('err', 680, 914, 300, 118, 'An error is not a pass', 'If code cannot read the question, it reports an error.', extra='stop'))

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 1048px; }')
assert '1048px' in extra_css
extra_css += '''  .box.row .num { width: 34px; height: 34px; font-size: 14px; }
  .box.fail .name { color: var(--fail); }
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
<title>Step 3: check by code</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 3: code checks each question against 12 exact rules</h1>
  <p class="sub">This diagram shows step 3. The step is built, and it ran in the test of 7 October 2026. Before a model looks at a question, code checks the rules that have one exact answer. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 1048" width="1000" height="1048" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>One question goes through 12 rules</div>
    <div class="panel" style="left:300px;top:38px;width:400px;height:820px"></div>
    <div class="ptitle" style="left:314px;top:46px">The 12 rules<small>group A of the 20 rules for a good question</small></div>
    <div class="shead" style="top:876px"><i>2</i>Code saves the verdict</div>
    ''' + ''.join(boxes) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 05. Design of 6 October 2026, corrected on 7 October 2026 (decisions 0031, 0037 and 0038) and on 8 October 2026 (rule A12, decision 0053). Status of the step: built. Each exam guide text is the exact text of the guide. A script took it from the records file, and measured the 12 sample questions.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/05-step-3-check-by-code.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'boxes', len(boxes))
