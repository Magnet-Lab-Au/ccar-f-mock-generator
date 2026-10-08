"""Makes docs/diagrams/06-step-4-check-by-a-model.html. Run: python3 06-make-diagram.py"""
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

# facts that the examples use
assert 'iteration caps' in PT['1.1-S3'][0]['text']
assert 'non-zero failure rate' in PT['1.4-K2'][0]['text']
assert 'isolated context' in PT['1.2-K2'][0]['text'] and 'narrow task decomposition' in PT['1.2-K4'][0]['text']
assert 'coordinator agent delegates to specialized subagents' in REC['scenarios'][2]['story']
n_words = sum(len(x.split()) for t in REC['task_statements'] for x in [t['title']] + [p['text'] for p in t['points']])
n_words += sum(len(x.split()) for v in REC['section_17'].values() for x in v)
assert 5000 < n_words < 9000

def res(rule, finding, pt=None, result='fail'):
    return js_({'rule': rule, 'result': result, 'finding': finding, 'point': pt})

verdict = {'question_id': 'M1-S17-T1', 'step': 4,
           'blind_answer': {'selected': ['C'], 'reason': '(the reason of the blind call)', 'agrees': False},
           'results': '(one result for each rule B1 to B8)', 'verdict': 'fail',
           'findings': ['(the list that the writer of step 5 gets)'], 'model': '(the model of the check)', 'date': '(the date of the check)'}
EH = 'Example of a result "fail"'
D = {
 'qblind': dict(title='The question, with no answer key', who='From step 2', cls='io',
   sent=['Code takes the question and its options, with their letters.',
         'Code leaves out the marks "correct" and "wrong", and the reasons. So the model cannot see the answer key.',
         'The call also gets the text of the exam guide.']),
 'c4a': dict(title='Call 4a: the blind answer', who='One model call', cls='model',
   sent=['A new model call answers the question, as a second expert does. It has the text of the exam guide, but not the answer key.',
         'It returns the letters that it selects, and its reason. It can also say "cannot decide".',
         'Before the first full run, this call answered the 12 sample questions of the exam guide, and 12 of 12 were right (test of 7 October 2026).'],
   why='A wrong answer key is the worst defect of a mock. A checker that sees the answer key can tend to agree with it (an assumption, not checked). A checker that does not see the key must find the answer alone.'),
 'cmp': dict(title='Code compares the two answers', who='Code', cls='code',
   sent=['Code compares the letters of the blind answer with the marks of the writer.',
         'The same letters: the check goes on.',
         'Different letters: rule B1 fails. The finding gives the answer and the reason of the blind call.',
         'The blind call can be wrong. Then a good question is written again. That is a false alarm, and it is cheap. Often the question was not clear.'],
   why='Two calls with code between them make sure that the blind answer always comes first. One call with the instruction "answer first, then look at the key" does not make sure of that.'),
 'rec': dict(title='The complete question record', who='From step 2', cls='io',
   sent=['The question, the options, the marks "correct" and "wrong", and the reason of each option.',
         'A participant reads the reasons in the answer key. So the check must read them.',
         'The call does not get the private notes of the writer.']),
 'guide': dict(title='The text of the exam guide', who='From the records file', cls='io',
   sent=['The story of the scenario, all 30 task statements with their 240 points, and the lists of Section 17. That is about %d words.' % round(n_words, -2),
         'Both calls of this step get this text.'],
   why='A wrong option often comes from a different task statement than the one of the slot. And one rule asks what the guide names. So the checker needs the complete guide, not a slice.'),
 'c4b': dict(title='Call 4b: the rule check', who='One model call', cls='model',
   sent=['A new model call checks the 8 rules. It did not write the question.',
         'Each call answers in a fixed form. The form is sent as structured outputs, not as a forced tool call, because the current models reject a forced tool call (see the diagram of step 2).',
         'For each rule it returns "pass", "fail" or "cannot decide". A "fail" has a finding, and the ID of the guide point that the finding uses.',
         'Code checks that each point ID exists. A point ID that does not exist shows that the checker invented a source.',
         'The call gives no confidence number. Such a number has no meaning before a person has marked questions to compare it with.'],
   points=[point('4.6-K1'), point('4.6-K2'), point('4.3-S5')],
   why='The guide wrote the first two points for the review of code, and the third for the extraction of data. Here they apply to a question: a call that did not write the question checks it, and it can say "cannot decide" when it cannot decide.'),
 'B1': dict(title='Rule B1: only the marked options are correct', who='One model call', cls='model',
   sent=['Each option that is marked correct is correct. No other option is correct.', 'The blind answer of call 4a also tests this rule.'],
   example=res('B1', 'Options A and C are both correct. The question asks for "a way", not for "the most effective first step".'), examplehead=EH,
   why='With two correct options and one mark, a participant who knows the subject loses the point.'),
 'B2': dict(title='Rule B2: each wrong option is wrong for a guide reason', who='One model call', cls='model',
   sent=['Each wrong option is wrong for a reason that the exam guide gives. The reason of the option says so.'],
   example=res('B2', 'The reason of option D says only that the option is "not ideal". It gives no reason from the guide.'), examplehead=EH,
   why='A wrong option that is wrong for no clear reason teaches nothing. A participant cannot learn why it is wrong.'),
 'B3': dict(title='Rule B3: each reason is true', who='One model call', cls='model',
   sent=['Each reason is true and agrees with the exam guide.'],
   example=res('B3', 'The reason of option B says that prompt instructions never work. The guide says that they have a non-zero failure rate. The reason is too strong.', '1.4-K2'), examplehead=EH,
   why='A participant learns most from the reasons in the answer key. A wrong reason teaches a wrong thing.'),
 'B4': dict(title='Rule B4: the question tests its point', who='One model call', cls='model',
   sent=['The question tests the point that its slot names.'],
   example=res('B4', 'The slot names point 1.2-K2, the isolated context of subagents. The question tests point 1.2-K4, a task decomposition that is too narrow.', '1.2-K2'), examplehead=EH,
   why='The plan gives each slot one point of its task statement, and no two slots of a mock get the same point. A question on a different point leaves its own point with no question.'),
 'B5': dict(title='Rule B5: the question is inside its story', who='One model call', cls='model',
   sent=['The question is inside the story of its scenario. It does not contradict the story.'],
   example=res('B5', 'The story of scenario 3 says that a coordinator agent delegates to specialized subagents. The question describes one agent that does all the work.'), examplehead=EH,
   why='In the exam, each scenario frames a set of questions. A question that contradicts its story confuses the participant.'),
 'B6': dict(title='Rule B6: only features that the guide names', who='One model call', cls='model',
   sent=['No text depends on a feature that the exam guide does not name. This applies to the question, the options and the reasons.',
         'The model lists each feature name. Code searches each name in the records file of the guide. It ignores capital letters, and it finds a name only as a complete word or words. So "Vision" is not found inside "provisions".'],
   example=res('B6', 'Option B depends on a setting "maxTurns". The guide does not name it. The guide says "iteration caps".', '1.1-S3'), examplehead=EH,
   why='A question on a feature that the guide does not name trains a participant for a thing that the exam does not test.'),
 'B7': dict(title='Rule B7: one name for each actor, and clear sentences', who='One model call', cls='model',
   sent=['Each actor has one name in the question, the options and the reasons.',
         'A reader understands each sentence at the first reading.'],
   example=res('B7', 'The synthesis actor is called "synthesis subagent" in the question and "synthesis agent" in the options. Use one name for each actor.'), examplehead=EH,
   why='The owner marked a question bad because it used two names for one actor and was hard to read. A word limit for each sentence does not catch this: the sample questions of the guide have sentences of up to 42 words. So a model checks it.'),
 'B8': dict(title='Rule B8: not a copy of a sample question', who='One model call', cls='model',
   sent=['The question is not a close copy of a sample question of the exam guide: not the same scene with the same correct action.',
         'Call 4b gets the 12 sample questions of the guide, each with its correct answer. A question on the same point as a sample question passes if its scene is different or its correct action is different.'],
   example=res('B8', 'The question has the scene of sample question 12: a self-review in the same session misses errors, and the answer is an independent review instance.'), examplehead=EH,
   why='In mock 1, two questions were close copies of sample questions 1 and 12. A participant who read the guide knows the answer already. A word count of code does not find a copy, because a copy keeps the scene and changes the words (decision 0055).'),
 'pass': dict(title='Verdict: pass', who='Usual', cls='owner',
   sent=['The blind answer agrees with the marks, and each of the 8 rules has the result "pass".',
         'When all 60 questions of the mock passed, step 6 checks the complete mock.']),
 'fail': dict(title='Verdict: fail', who='Back to the writer', cls='stop',
   sent=['The blind answer is different from the marks, or one rule or more fails.',
         'The question goes to step 5. The writer gets the findings and writes the question again.',
         'The new question goes through steps 3 and 4 again. The two calls check it as a new question. They do not see the earlier findings.',
         'Code saves each verdict as one new file.'],
   example=js_(verdict), examplehead='Example: the fields of a verdict record'),
 'cd': dict(title='Verdict: cannot decide', who='Back to the writer', cls='open',
   sent=['No rule fails, but the blind call or the rule check cannot decide.',
         'The question goes to step 5 with the reason.',
         'If the same slot gets "cannot decide" two times, the slot goes to the owner.'],
   why='If the checker cannot decide, a participant probably cannot decide. So the question is not clear, and a new try can repair it.'),
}
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g3[g3.index('def box('):g3.index('rows = [(')])
exec(g5[g5.index('def rowbox('):g5.index('rows = [(', g5.index('def rowbox('))])

boxes, paths = [], []
# section 1
boxes.append(box('qblind', 20, 38, 230, 112, 'The question alone', 'The question and the options. No marks and no reasons.'))
boxes.append(box('c4a', 300, 38, 220, 112, '4a. The blind answer', 'A second expert answers the question alone.', 'One model call', 'model', extra='mdl'))
boxes.append(box('cmp', 570, 38, 200, 112, 'Code compares', 'The blind answer and the marks.', 'Code', 'code'))
boxes.append(box('', 820, 38, 160, 50, 'The same', '', extra='chip ok'))
boxes.append(box('', 820, 100, 160, 50, 'B1 fails', '', extra='chip bad'))
paths.append('<path class="flow" d="M250,94 H296" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M520,94 H566" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M770,94 C794,94 794,63 816,63" marker-end="url(#a)"/>')
paths.append('<path class="failp" d="M770,94 C794,94 794,125 816,125" marker-end="url(#af)"/>')
# section 2
rows = [('B1', 'The marked options are correct', 'No other option is correct.'),
        ('B2', 'Each wrong option: a reason', 'A reason that the guide gives.'),
        ('B3', 'Each reason is true', 'It agrees with the exam guide.'),
        ('B4', 'The question tests its point', 'The point that the slot names.'),
        ('B5', 'The question is inside its story', 'It does not contradict the scenario.'),
        ('B6', 'Only what the guide names', 'No feature that the guide does not name.'),
        ('B7', 'One name for each actor', 'Each sentence is clear at once.'),
        ('B8', 'Not a copy of a sample question', 'Not the scene and answer of a sample.')]
for i, (key, name, what) in enumerate(rows):
    boxes.append(rowbox(key, 582, 262 + i * 65, 386, 60, key, name, what))
MID = 487
boxes.append(box('rec', 20, 359, 230, 96, 'The complete record', 'The question, the marks and the reasons.'))
boxes.append(box('guide', 20, 519, 230, 96, 'The exam guide text', 'About %d words. Both calls get it. Call 4b also gets the 12 sample questions.' % round(n_words, -2)))
boxes.append(box('c4b', 300, 431, 220, 112, '4b. The rule check', 'One result for each of the 8 rules.', 'One model call', 'model', extra='mdl'))
for yc in (407, 567):
    paths.append('<path class="flow" d="M250,%d C276,%d 276,%d 296,%d" marker-end="url(#a)"/>' % (yc, yc, MID, MID))
paths.append('<path class="flow" d="M520,%d H566" marker-end="url(#a)"/>' % MID)
# section 3
boxes.append(box('pass', 20, 846, 300, 118, 'Pass', 'Each rule passes. The question waits for the check of the complete mock.', 'Usual', 'owner'))
boxes.append(box('fail', 350, 846, 300, 118, 'Fail', 'A rule fails. The question goes back to the writer with the findings.', extra='fail'))
boxes.append(box('cd', 680, 846, 300, 118, 'Cannot decide', 'Back to the writer with the reason. The second time, the owner decides.', 'Possible', 'open'))

extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 980px; }')
assert '980px' in extra_css
extra_css += '''  .box.row .num { width: 34px; height: 34px; font-size: 14px; background: var(--model); color: var(--panel); }
  .box.mdl { border-color: var(--model); background: var(--model-bg); }
  .box.mdl .what { color: var(--ink); }
  .box.fail .name { color: var(--fail); }
  .box.chip { padding: 12px 14px; }
  .box.chip .name { font-size: 14px; }
  .box.chip.ok { border-color: var(--owner); background: var(--owner-bg); }
  .box.chip.bad { border-color: var(--fail); background: var(--fail-bg); }
  .box.chip.bad .name { color: var(--fail); }
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
<title>Step 4: check by a model</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 4: a model checks each question two times</h1>
  <p class="sub">This diagram shows step 4. The step is built, and it ran in the test of 7 October 2026. Some rules need judgment, so a model checks them. First a model answers the question without the answer key. Then a second call checks 8 rules with the answer key. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 980" width="1000" height="980" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>Without the answer key: does a second expert select the same answer?</div>
    <div class="shead" style="top:176px"><i>2</i>With the answer key: does the question pass 8 rules?</div>
    <div class="panel" style="left:570px;top:212px;width:410px;height:582px"></div>
    <div class="ptitle" style="left:584px;top:222px">The 8 rules<small>group B of the 20 rules for a good question</small></div>
    <div class="shead" style="top:810px"><i>3</i>Code makes the verdict</div>
    ''' + ''.join(boxes) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 06. Design of 6 October 2026, corrected on 7 October 2026 (decisions 0040, 0041 and 0043) and on 8 October 2026 (decision 0055). Status of the step: built. Each exam guide text is the exact text of the guide. A script took it from the records file. The examples of findings are invented, to show the form.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/06-step-4-check-by-a-model.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'boxes', len(boxes), 'guide words', n_words)
