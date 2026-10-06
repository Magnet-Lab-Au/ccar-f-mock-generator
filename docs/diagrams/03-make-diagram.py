import re, html, os, json
root = os.path.expanduser('~/mnt/mock-builder-v3')
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
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

def words(texts):
    return sum(len(t.split()) for t in texts)

all_texts = [REC['guide']['version']] + [d['name'] for d in REC['domains']]
all_texts += [s[k] for s in REC['scenarios'] for k in ('name', 'story')]
all_texts += [t['title'] for t in REC['task_statements']] + [p['text'] for p, _ in PT.values()]
all_texts += [q[k] for q in REC['sample_questions'] for k in ('question', 'explanation')]
all_texts += [o for q in REC['sample_questions'] for o in q['options'].values()]
all_texts += [x for v in REC['section_17'].values() for x in v]
n_texts, n_words = len(all_texts), words(all_texts)
slice_texts = [SC[3]['name'], SC[3]['story'], TS['1.2']['title']] + [p['text'] for p in TS['1.2']['points']]
n_slice, n_slice_points = words(slice_texts), len(TS['1.2']['points'])
n_marks = len(re.findall(r'^<!-- Page \d+ \|.*-->$', guide, flags=re.M))
s17 = REC['section_17']
assert (len(REC['domains']), len(SC), len(TS), len(PT), len(REC['sample_questions'])) == (5, 6, 30, 240, 12)
assert n_texts == 408

q4 = dict(REC['sample_questions'][3])
first = q4['explanation'].split('. ')[0] + '.'
assert q4['explanation'].startswith(first)
q4['explanation'] = first + ' ...'
p142 = PT['1.4-K2'][0]
assert [p['id'] for p in TS['1.4']['points']][1] == '1.4-K2' and p142['kind'] == 'knowledge'

D = {
 'dom': dict(title='The 5 domains', who='Section 4 of the guide', cls='io',
   sent=['Section 4 of the guide has a table of the 5 domains and their weights.', 'The script makes one record for each domain.'],
   fields='id, name, weight', example=js_(REC['domains'][0]),
   use='Step 1 uses the weights. They give the number of questions for each domain in a mock.'),
 'scen': dict(title='The 6 scenarios', who='Section 5 of the guide', cls='io',
   sent=['Section 5 of the guide has the 6 scenarios. Each scenario has a name, a story of one paragraph and a line with its primary domains.',
         'The script makes one record for each scenario.'],
   fields='id, name, story, primary domains', example=js_(SC[3]),
   use='Step 1 selects 4 of the 6 scenarios for a mock. Each question of a mock is in the story of its scenario.'),
 'ts': dict(title='The 30 task statements and their 240 points', who='Section 6 of the guide', cls='io',
   sent=['Section 6 of the guide has the 30 task statements. Each task statement has two lists: "Knowledge of" and "Skills in". Each bullet in those lists is one point.',
         'The script gives each point an ID. The ID is the task statement, then K or S, then the number of the bullet. So 1.4-K2 is the second bullet below "Knowledge of" in task statement 1.4.',
         'The IDs are ours. The guide does not number its bullets.'],
   fields='Task statement: id, domain, title, points. Point: id, kind, text.', example=js_(p142),
   use='Each question of a mock tests one point. The plan of the mock names that point by its ID.'),
 'sq': dict(title='The 12 sample questions', who='Section 9 of the guide', cls='io',
   sent=['Section 9 of the guide has 12 sample questions. Each one has 4 options, the correct answer and an explanation.',
         'The script makes one record for each sample question.'],
   fields='number, scenario, question, options, correct answer, explanation', example=js_(q4),
   examplenote='The explanation is shortened in this example. The file has the complete text.',
   use='Before the first full run, the checker must pass all 12 sample questions. We also compare the first new questions with them.'),
 's17': dict(title='The three lists of Section 17', who='Section 17 of the guide', cls='io',
   sent=['Section 17 of the guide has three lists: %d technologies and concepts, %d topics in scope and %d topics out of scope.' % (len(s17['technologies']), len(s17['in_scope']), len(s17['out_of_scope'])),
         'The script copies each list.'],
   fields='technologies, topics in scope, topics out of scope',
   example=js_({'out_of_scope': [s17['out_of_scope'][0], '...']}),
   use='A question depends only on features that the guide names. These lists are a part of what the guide names.'),
 'script': dict(title='The script', who='Code', cls='code',
   sent=['A script reads the guide file and makes the records. It copies each text with no change.',
         'No model works in this step. A model can change a word when it copies. A script cannot.',
         'The guide file has %d page marks from the PDF. A page mark can be in the middle of a list. The script leaves the page marks out, so that no list is cut in two.' % n_marks,
         'Before the script writes the file, it checks the counts and it checks that each text is exactly in the guide. If a check fails, it writes no file and names the cause.'],
   points=[point('1.3-S2'), point('5.6-K1'), point('5.6-K2')],
   why='The guide wrote these points for agents that pass findings to other agents. Here they apply to record files: each later step takes guide text from these records by ID, so each question keeps the link to its source.'),
 'c2': dict(title='Check: a second script', who='Passed', cls='owner',
   sent=['A second script, with its own code, compares the records with the guide.',
         'Examples of its checks: the 240 bullets of Section 6 are the 240 points, in the same sequence. Each of the %d texts of the file is exactly in the guide. Each sample question has its 4 options, its answer and its scenario.' % n_texts,
         'Result of 6 October 2026: 41 of 41 checks passed.'],
   why='A check must not depend on the code that made the file.'),
 'c3': dict(title='Check: an independent reviewer', who='Passed', cls='owner',
   sent=['A reviewer that did not make the file compared it with the guide, with its own script and by reading.',
         'The reviewer also looked at each place where a page mark of the PDF cuts a list. No bullet was lost or moved.',
         'Result of 6 October 2026: no errors found. 240 of 240 points agree.'],
   why='The maker of a file does not see its own errors well. So a reviewer that did not make the file checks it.'),
 'c1': dict(title='Check: our copy against the original', who='Not done yet', cls='open',
   sent=['The records come from our copy of the exam guide. This check compares that copy with the original guide, character for character.',
         'Result: not done yet.'],
   why='The other two checks show that the records agree with our copy. Only this check shows that our copy agrees with the original.'),
 'u1': dict(title='The records file', who='File', cls='io',
   sent=['One file: reference/guide-records.json.', 'It has all records of the guide: %d texts with about %d words.' % (n_texts, round(n_words, -2)),
         'It is a small database for the code. No model call reads it.']),
 'u2': dict(title='Code takes a slice', who='Code', cls='code',
   sent=['Each model call needs a different part of the guide. Code selects that part by ID.',
         'Example for one question: the story of scenario 3, and task statement 1.2 with its %d points.' % n_slice_points,
         'This slice has about %d words. The complete file has about %d words.' % (round(n_slice, -1), round(n_words, -2))]),
 'u3': dict(title='The call for one question', who='One model call', cls='model',
   sent=['The call gets only its slice. It does not read the file.', 'So each call gets what it needs and no more, and the exact text of the guide.']),
}
for d in D.values():
    for k in ('fields', 'example', 'examplenote', 'use', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

def box(key, left, top, w, h, name, what, tag=None, tagcls='io', extra=''):
    taghtml = '<span class="tag t-%s">%s</span>' % (tagcls, e(tag)) if tag else ''
    attrs = ('class="box step nonum %s" data-step="%s" role="button" tabindex="0" aria-haspopup="dialog" aria-expanded="false" aria-controls="pop"' % (extra, key)
             if key else 'class="box nonum %s"' % extra)
    return ('<div %s style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class="head"><span class="name">%s</span>%s</div><p class="what">%s</p></div>'
            % (attrs, left, top, w, h, e(name), taghtml, e(what)))

rows = [('dom', 'Section 4', 'The domains and their weights', '5 domains', 'id, name, weight'),
        ('scen', 'Section 5', 'The scenarios', '6 scenarios', 'id, name, story, primary domains'),
        ('ts', 'Section 6', 'The task statements', '30 task statements, 240 points', 'Each point has an ID, for example 1.4-K2'),
        ('sq', 'Section 9', 'The sample questions', '12 sample questions', 'question, 4 options, correct answer, explanation'),
        ('s17', 'Section 17', 'Technologies and topics', '3 lists', 'technologies, topics in scope, topics out of scope')]
Y0, RH, GAP = 84, 68, 8
centers = [Y0 + i * (RH + GAP) + RH // 2 for i in range(5)]
MID = 273
boxes, paths = [], []
for i, (key, sec, what_l, name_r, what_r) in enumerate(rows):
    top = Y0 + i * (RH + GAP)
    boxes.append(box(key, 32, top, 236, RH, sec, what_l, extra='row'))
    boxes.append(box(key, 592, top, 376, RH, name_r, what_r, extra='row'))
    yc = centers[i]
    paths.append('<path class="flow" d="M268,%d C300,%d 300,%d 328,%d"/>' % (yc, yc, MID, MID))
    paths.append('<path class="flow" d="M532,%d C562,%d 562,%d 588,%d" marker-end="url(#a)"/>' % (MID, MID, yc, yc))
boxes.append(box('script', 330, 222, 200, 102, 'The script', 'Copies each text with no change. No model works.', 'Code', 'code', extra='hdr'))
boxes.append(box('', 330, 372, 200, 82, 'If a check fails', 'The script writes no file and names the cause.', extra='stop'))
boxes.append(box('c2', 20, 534, 310, 104, 'A second script', '41 of 41 checks passed.', 'Passed', 'owner'))
boxes.append(box('c3', 345, 534, 310, 104, 'An independent reviewer', 'No errors found. 240 of 240 points agree.', 'Passed', 'owner'))
boxes.append(box('c1', 670, 534, 310, 104, 'Copy against the original', 'Our guide file against the original guide.', 'Not done yet', 'open'))
boxes.append(box('u1', 20, 702, 280, 118, 'The records file', 'All records of the guide: about %d words.' % round(n_words, -2), 'File', 'io'))
boxes.append(box('u2', 360, 702, 280, 118, 'Code takes a slice', 'Example for one question: the story of scenario 3, and task statement 1.2 with its %d points.' % n_slice_points, 'Code', 'code'))
boxes.append(box('u3', 700, 702, 280, 118, 'The call for one question', 'Gets only that slice: about %d words. It does not read the file.' % round(n_slice, -1), 'One model call', 'model'))
paths.append('<path class="flow" d="M300,761 H356" marker-end="url(#a)"/>')
paths.append('<path class="flow" d="M640,761 H696" marker-end="url(#a)"/>')

extra_css = '''
  .stage { height: 836px; }
  .t-io { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--line); }
  .box.nonum { padding-left: 14px; }
  .box.row { padding-top: 9px; padding-bottom: 9px; }
  .box.row .what { margin-top: 1px; }
  .box.hdr { border-color: var(--code); background: var(--code-bg); }
  .box.hdr .what { color: var(--ink); }
  .box.stop .name { font-size: 14px; color: var(--fail); }
  .panel { position: absolute; border: 1.5px solid var(--line); border-radius: 14px; }
  .ptitle { position: absolute; font-weight: 700; font-size: 15px; }
  .ptitle small { margin-left: 8px; font-weight: 400; font-size: 12.5px; color: var(--muted); }
  .shead { position: absolute; left: 20px; font-weight: 700; font-size: 16px; display: flex; align-items: center; gap: 10px; }
  .shead i { font-style: normal; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center;
             background: var(--ink); color: var(--bg); font-size: 14px; }
  #pop pre { margin: 0; padding: 8px 10px; border-radius: 8px; background: var(--bg); border: 1px solid var(--line);
             font: 12px/1.45 ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace; white-space: pre-wrap; overflow-wrap: anywhere; }
  #pop .exnote { font-size: 12px; color: var(--muted); margin-top: 4px; }
'''
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = '''  function fill(d) {
    var who = document.getElementById('popwho');
    who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    var s = document.getElementById('popbody'); s.textContent = '';
    d.sent.forEach(function (t) { s.appendChild(el('p', null, t)); });
    if (d.fields) { s.appendChild(el('h3', null, 'Fields of the record')); s.appendChild(el('p', null, d.fields)); }
    if (d.example) {
      s.appendChild(el('h3', null, 'Example from the file')); s.appendChild(el('pre', null, d.example));
      if (d.examplenote) s.appendChild(el('p', 'exnote', d.examplenote));
    }
    if (d.use) { s.appendChild(el('h3', null, 'Where the pipeline uses it')); s.appendChild(el('p', null, d.use)); }
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
popdiv = '''<div id="pop" role="dialog" aria-labelledby="poptitle" hidden>
      <div class="ptop"><span><span id="popwho" class="tag"></span><span id="poppin" class="pinned"></span></span>
        <button id="popclose" type="button" aria-label="Close">&times;</button></div>
      <h2 id="poptitle"></h2>
      <div id="popbody"></div>
    </div>'''
data = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Step 0: prepare the guide records</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 0: from the exam guide to records that code can read</h1>
  <p class="sub">The exam guide is a document for people. The program needs its text in small parts, each with an ID. Step 0 makes those parts one time for each version of the guide. It ran on 6 October 2026. Put the pointer on a box, or select it with the keyboard, to see the detail and an example. A click keeps the detail open.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 836" width="1000" height="836" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    <div class="shead" style="top:2px"><i>1</i>A script copies the guide into records</div>
    <div class="panel" style="left:20px;top:38px;width:260px;height:440px"></div>
    <div class="ptitle" style="left:34px;top:46px">The exam guide<small>for people</small></div>
    <div class="panel" style="left:580px;top:38px;width:400px;height:440px"></div>
    <div class="ptitle" style="left:594px;top:46px">The records file<small>guide-records.json, for code</small></div>
    <div class="shead" style="top:496px"><i>2</i>Three checks of the file</div>
    <div class="shead" style="top:664px"><i>3</i>How a later step uses the file</div>
    ''' + ''.join(boxes) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 03. Design of 6 October 2026. The step ran on 6 October 2026. Each example is the exact content of the records file. A script took it from the file.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/03-step-0-prepare-the-guide-records.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'texts', n_texts, 'words', n_words, 'slice', n_slice, n_slice_points, 'marks', n_marks)
