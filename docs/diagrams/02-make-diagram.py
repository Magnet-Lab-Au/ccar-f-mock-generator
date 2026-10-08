import re, html, os, json
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pts = open(root + '/reference/task-statements-and-points.md', encoding='utf-8').read()
guide = open(root + '/reference/exam-guide.md', encoding='utf-8').read()
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
e = html.escape

def point(pid):
    m = re.search(r'^- \*\*' + re.escape(pid) + r'\*\* (.+)$', pts, flags=re.M)
    ts = pid.split('-')[0]
    t = re.search(r'^### Task Statement ' + re.escape(ts) + r': (.+)$', pts, flags=re.M)
    assert m and t, pid
    return {'id': pid, 'text': m.group(1).strip(), 'ctx': 'From task statement %s: %s' % (ts, t.group(1).strip())}

def fact(section, q):
    assert guide.count(q) == 1, q
    return {'id': section, 'text': q, 'ctx': 'A fact about the exam. It is not a task statement point.'}

doms = [('1', 'Agentic Architecture & Orchestration', '27%', 16, 7),
        ('2', 'Tool Design & MCP Integration', '18%', 11, 5),
        ('3', 'Claude Code Configuration & Workflows', '20%', 12, 6),
        ('4', 'Prompt Engineering & Structured Output', '20%', 12, 6),
        ('5', 'Context Management & Reliability', '15%', 9, 6)]
for n, name, w, q, ts in doms:
    assert guide.count('| %s | %s | %s |' % (n, name, w)) == 1, name
    assert len(re.findall(r'^### Task Statement %s\.\d' % n, pts, flags=re.M)) == ts
    assert q > ts
assert sum(d[3] for d in doms) == 60 and sum(d[4] for d in doms) == 30
scen = [('1', 'Customer Support Resolution Agent', '1, 2, 5'), ('2', 'Code Generation with Claude Code', '3, 5'),
        ('3', 'Multi-Agent Research System', '1, 2, 5'), ('4', 'Developer Productivity with Claude', '1, 2, 3'),
        ('5', 'Claude Code for Continuous Integration', '3, 4'), ('6', 'Structured Data Extraction', '4, 5')]
for n, name, d in scen:
    assert guide.count('### Scenario %s: %s' % (n, name)) == 1, name
# number of points for each task statement
counts = [len(re.findall(r'^- \*\*%s-[KS]\d+\*\*' % re.escape(t), pts, flags=re.M))
          for t in re.findall(r'^### Task Statement (\d\.\d):', pts, flags=re.M)]
assert len(counts) == 30 and sum(counts) == 240
lo, hi = min(counts), max(counts)

NONE = 'No exam guide text. Plain reason.'
PLAN = json.load(open(root + '/runs/mock-01/plan.json', encoding='utf-8'))
EX = PLAN['slots'][0]
D = {
 'IN': dict(title='What the step receives', cls='io', who='Input', status='built', points=[], none=NONE,
   sent=['The guide records: the 6 scenarios and their primary domains, the 5 domain weights, and the 30 task statements with their 240 points.',
         'A mock number.',
         'A seed. A seed is a number that controls the random selections.'],
   why='Step 0 makes the guide records. The seed has a plain reason: the same seed gives the same plan, so we can make a plan again and compare it, for example after a change to the code.'),
 'S': dict(title='Step 1: plan the mock', cls='code', who='Code', status='built', none=NONE,
   sent=['Code makes the plan of one mock, in 5 parts.', 'The plan is a list of 60 slots. Each slot says what one question must be.', 'No model works in this step.'],
   points=[point('1.4-K2'), point('1.6-K1'), point('1.6-S1')],
   why='The guide wrote these points for workflows with a fixed sequence and for reviews. Here they apply to a plan: the counts of a mock must be the same each time, and the work is known before it starts, so code makes a fixed plan.'),
 '1': dict(title='Part 1: select 4 scenarios', cls='code', who='Code', status='built', none=NONE,
   sent=['The exam uses 4 of its 6 scenarios. So 15 sets of 4 scenarios are possible.',
         'The seed selects one set, and the sequence of the 4 groups in the mock. The step uses only the 11 sets in which each question fits a primary domain of its scenario.',
         'It does not use these 4 sets: 1-2-3-4, 1-2-5-6, 2-3-5-6 and 2-4-5-6.'],
   table=dict(head=['Scenario', 'Primary domains'], rows=[['%s. %s' % (n, name), d] for n, name, d in scen]),
   points=[fact('Section 5', 'During the exam, 4 scenarios are presented and picked at random from the full set of the 6 scenarios below.')],
   why='The limit to 11 sets is not from the guide. The exam can use all 15 sets. Example: none of the scenarios 1, 2, 3 and 4 has Domain 4 as a primary domain, but a mock needs 12 questions of Domain 4. Those questions would be forced into a story that does not fit them. A script checked all 15 sets.'),
 '2': dict(title='Part 2: share the 60 questions', cls='code', who='Code', status='built', none=NONE,
   sent=['Each scenario gets 15 questions.', 'Each domain gets its number of questions: 16, 11, 12, 12 and 9.',
         'Each question is in a primary domain of its scenario.',
         'Many tables fit. Code takes the most even table: the smallest sum of the squares of its numbers. If two tables are equal, the seed selects one.'],
   table=dict(head=['Domain', 'Weight', 'Questions'], rows=[['%s. %s' % (n, name), w, str(q)] for n, name, w, q, ts in doms] + [['Total', '100%', '60']]),
   points=[fact('Section 4', 'The percentages indicate the approximate proportion of scored items drawn from each domain.')],
   why='Each number is the weight for 60 questions, rounded. Example: 27% of 60 is 16.2, so Domain 1 has 16 questions. The guide gives no number of questions for each scenario. The reason for 15 is plain: equal parts.'),
 '3': dict(title='Part 3: select the task statements', cls='code', who='Code', status='built', points=[], none=NONE,
   sent=['Each of the 30 task statements gets at least 1 question.',
         'In each domain, the task statements share the questions equally. But a task statement gets no more questions than its number of point groups (decision 0048).',
         'The seed sets an order of the task statements. In that order, a task statement gets one extra question if a full plan stays possible.',
         'Example: Domain 5 has 6 task statements and 9 questions. Each task statement gets 1 question, and 3 of them get a second question.',
         'Example: task statement 3.3 has one group, so it gets 1 question. Another task statement of Domain 3 gets 3.',
         'The seed also decides which scenario of the table each question goes to.'],
   why='Each mock then covers the complete guide. A group is one idea, so two questions on a task statement with one group are two questions on one idea.'),
 '4': dict(title='Part 4: select one point for each question', cls='code', who='Code', status='built', points=[], none=NONE,
   sent=['Each task statement has %d to %d points. A point is one thing to know or one skill.' % (lo, hi),
         'The file data/point-groups.json puts each of the 240 points into one group. Two points in one group describe one idea. A group can hold points of different task statements (decision 0047).',
         'No two slots of one mock get points of the same group.',
         'The seed sets an order of the points. Code takes the first point whose group is free and that keeps a full plan possible (decision 0048).',
         'Code checks "possible" with a matching of task statements to free groups. No model makes this check.'],
   why='The writer and the checker know exactly what the question must test. Mock 1 got repeats from two points on one idea (decision 0046). The groups prevent this before a question is written.'),
 '5': dict(title='Part 5: set the question type', cls='code', who='Code', status='built', none=NONE,
   sent=['Multiple-choice: the participant selects 1 answer.', 'Multiple-response: the question has 5 options, and the participant selects 2 answers. A multiple-choice question has 4 options.',
         'The step makes 2 questions of each scenario multiple-response. That gives 8 multiple-response questions and 52 multiple-choice questions.'],
   points=[fact('Section 3', 'Multiple-choice and multiple-response items; each item states how many responses to select')],
   why='The guide gives no number for each type. All 12 sample questions of the guide are multiple-choice. The number 8 is a guess. It has no source.'),
 'OUT': dict(title='What the step returns', cls='io', who='Output', status='built', points=[], none=NONE,
   sent=['One plan file: the mock number, the seed, the version of the guide, the date, the 4 scenarios in the sequence of the groups, the table of scenarios and domains, and the 60 slots.',
         'The slots get the numbers 1 to 60, group by group. The seed sets the sequence inside a group. The slot number is the question number in the finished mock.',
         'A slot has an ID, the scenario, the task statement, one point, the question type, the number of options and the number of answers to select.',
         'The first slot of the plan of mock 1: %s.' % json.dumps(EX)],
   why='Step 2 writes one question for each slot. The later checks compare each question with its slot.'),
 'F': dict(title='The step stops', cls='stop', who='The step stops', status='built', points=[], none=NONE,
   sent=['A guide record is missing or not valid, or the counts of the plan do not add up to 60. Example: a task statement with an unknown domain.',
         'The groups file is not correct, or the groups allow no plan at all.',
         'The step stops with an error that names the cause.', 'It writes no plan.'],
   why='A plan with wrong counts makes a mock with wrong counts. So the step stops, and it does not write a wrong plan.'),
}

def box(key, top, h, num, name, tag, tagcls, what, ts, extra='', left=40, w=540):
    numhtml = '<div class="num">%s</div>' % num if num else ''
    cls = 'box step ' + extra + ('' if num else ' nonum')
    tshtml = '<p class="ts">%s</p>' % e(ts) if ts else ''
    return ('<div class="%s" data-step="%s" role="button" tabindex="0" aria-haspopup="dialog" aria-expanded="false" aria-controls="pop" '
            'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s<div class="head"><span class="name">%s</span><span class="tag t-%s">%s</span></div>'
            '<p class="what">%s</p>%s</div>') % (cls, key, left, top, w, h, numhtml, e(name), tagcls, e(tag), e(what), tshtml)

boxes = ''.join([
 box('IN', 10, 100, '', 'What the step receives', 'Input', 'io', 'The guide records, the point groups, a mock number and a seed.', 'Step 0 makes the guide records. The owner confirms the point groups.'),
 box('S', 150, 88, '', 'Step 1: plan the mock', 'Code', 'code', 'Code makes the plan in 5 parts. No model works.', 'Exam guide: task statements 1.4 and 1.6', extra='hdr'),
 box('1', 246, 112, '1', 'Select 4 scenarios', 'Code', 'code', 'The seed selects 4 of the 6 scenarios, from the 11 sets that fit.', 'Exam guide: Section 5. The limit to 11 sets is not from the guide.'),
 box('2', 378, 112, '2', 'Share the 60 questions', 'Code', 'code', '15 questions for each scenario. 16, 11, 12, 12 and 9 questions for the 5 domains.', 'Exam guide: Section 4. The number 15 is not from the guide.'),
 box('3', 510, 112, '3', 'Select the task statements', 'Code', 'code', 'Each of the 30 task statements gets at least 1 question.', 'Not from the exam guide. Plain reason.'),
 box('4', 642, 112, '4', 'Select one point for each question', 'Code', 'code', 'Each question gets one point of its task statement. No two points of one mock are in one group.', 'Not from the exam guide. Plain reason.'),
 box('5', 774, 112, '5', 'Set the question type', 'Code', 'code', '2 questions of each scenario are multiple-response. The other 52 are multiple-choice.', 'Exam guide: Section 3. The number 8 is a guess.'),
 box('OUT', 934, 130, '', 'What the step returns', 'Output', 'io', 'One plan file with 60 slots and the seed. Example from the plan of mock 1: scenario %s, task statement %s, point %s, %s, select %s.' % (EX['scenario'], EX['task_statement'], EX['point'], EX['type'].replace('_', '-'), EX['select']), 'The same seed gives the same plan.'),
 box('F', 500, 132, '', 'The step stops', 'No plan', 'stop', 'A record or the groups file is not valid, or the counts do not add up to 60. The step names the cause and writes no plan.', '', extra='stop', left=700, w=270),
])

extra_css = '''
  .stage { height: 1080px; }
  .t-io { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--line); }
  .box.nonum { padding-left: 14px; }
  .box.hdr { border-color: var(--code); background: var(--code-bg); }
  .box.hdr .what { color: var(--ink); }
  .group { position: absolute; left: 24px; top: 138px; width: 572px; height: 764px; border: 1.5px solid var(--code); border-radius: 14px; }
  #pop table { border-collapse: collapse; width: 100%; font-size: 13px; margin: 8px 0 2px; }
  #pop th, #pop td { text-align: left; padding: 3px 6px 3px 0; border-bottom: 1px solid var(--line); vertical-align: top; }
  #pop th { font-size: 12px; color: var(--muted); }
  #pop td + td, #pop th + th { text-align: right; white-space: nowrap; padding-right: 0; padding-left: 12px; }
'''
# popup script: the script of diagram 01, with a new function to fill the popup
a = js.index('  function fill(d) {'); b = js.index('  function place() {')
fill = '''  function fill(d) {
    var who = document.getElementById('popwho');
    who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    var s = document.getElementById('popsent'); s.textContent = '';
    d.sent.forEach(function (t) { s.appendChild(el('p', null, t)); });
    if (d.table) {
      var tb = el('table'), tr = el('tr');
      d.table.head.forEach(function (h) { tr.appendChild(el('th', null, h)); }); tb.appendChild(tr);
      d.table.rows.forEach(function (r) { var x = el('tr'); r.forEach(function (c) { x.appendChild(el('td', null, c)); }); tb.appendChild(x); });
      s.appendChild(tb);
    }
    var ul = document.getElementById('poppoints'); ul.textContent = '';
    if (d.points.length === 0) {
      ul.appendChild(el('li', 'none', d.none));
    } else {
      d.points.forEach(function (p) {
        var li = el('li'); li.appendChild(el('span', 'pid', p.id)); li.appendChild(document.createTextNode(' '));
        li.appendChild(el('span', 'ptext', p.text));
        li.appendChild(el('span', 'pctx', p.ctx)); ul.appendChild(li);
      });
    }
    document.getElementById('popwhy').textContent = d.why;
    document.getElementById('popstatus').textContent = 'Status: ' + d.status;
  }

'''
js2 = js[:a] + fill + js[b:]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
popdiv = src[src.index('<div id="pop"'):src.index('</div>\n  </div>\n  </div>\n\n  <div class="notes">')] + '</div>'
assert 'popstatus' in popdiv and popdiv.count('<div') == popdiv.count('</div>')
data = json.dumps(D).replace('</', '<\\/')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Step 1: plan the mock</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>Step 1: plan the mock</h1>
  <p class="sub">This diagram shows step 1. The step is built. It made the plan of mock 1 on 7 October 2026. Code makes the plan of one mock: a list of 60 slots. Put the pointer on a box, or select it with the keyboard, to see the detail. A click keeps the detail open.</p>

  <div class="legend">
    <span class="key"><span class="tag t-code">Code</span> no model works</span>
    <span class="key"><span class="swatch"></span> the usual path</span>
    <span class="key"><span class="swatch f"></span> the step fails</span>
  </div>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 1080" width="1000" height="1080" aria-hidden="true">
      ''' + marker + '''
      <path class="flow" d="M310,110 V134" marker-end="url(#a)"/>
      <path class="flow" d="M310,358 V374" marker-end="url(#a)"/>
      <path class="flow" d="M310,490 V506" marker-end="url(#a)"/>
      <path class="flow" d="M310,622 V638" marker-end="url(#a)"/>
      <path class="flow" d="M310,754 V770" marker-end="url(#a)"/>
      <path class="flow" d="M310,902 V930" marker-end="url(#a)"/>
      <path class="failp" d="M596,566 H696" marker-end="url(#af)"/>
    </svg>
    <div class="group"></div>
    ''' + boxes + '''
    <div class="lbl" style="left:604px;top:540px">the step fails</div>
    ''' + popdiv + '''
  </div>
  </div>

  <div class="notes">
    <div class="note">
      <h2>What the exam guide gives</h2>
      <ul>
        <li>From the guide: 60 questions, 4 of the 6 scenarios, the 5 domain weights and the two question types.</li>
        <li>Not from the guide: 15 questions for each scenario, 8 multiple-response questions, at least 1 question for each task statement, one point for each slot, and the limit to 11 sets of scenarios. Each of these has a plain reason. The detail on each box gives it.</li>
      </ul>
    </div>
    <div class="note">
      <h2>Not decided yet</h2>
      <ul>
        <li>A task statement can be a bad fit for a scenario, also when its domain fits. The plan does not prevent this. The writer can answer "cannot write", and the owner decides.</li>
        <li>How the program selects the scenarios across more than one mock.</li>
      </ul>
    </div>
  </div>

  <footer>Diagram 02. Design of 6 October 2026, corrected on 7 October 2026 (decisions 0027 and 0037). Status of the step: built. The example slot comes from the plan of mock 1. Each exam guide text is the exact text of the guide. A script took each text from the guide files.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/02-step-1-plan-the-mock.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'points per task statement', lo, hi, 'emdash', page.count('—'))
