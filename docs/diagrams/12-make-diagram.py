"""Makes docs/diagrams/12-scenarios-of-the-mocks.html (decision 0057). Run: python3 12-make-diagram.py"""
import html, os, json, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root + '/src')
src = open(root + '/docs/diagrams/01-pipeline-overview.html', encoding='utf-8').read()
g3 = open(root + '/docs/diagrams/03-make-diagram.py', encoding='utf-8').read()
g4 = open(root + '/docs/diagrams/04-make-diagram.py', encoding='utf-8').read()
g9 = open(root + '/docs/diagrams/09-make-diagram.py', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
marker = src[src.index('<defs>'):src.index('</defs>') + 7]
e = html.escape

import step1_plan
R = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
NAMES = {x['id']: x['name'] for x in R['scenarios']}
PRIM = {x['id']: x['primary_domains'] for x in R['scenarios']}
SETS = step1_plan.scenario_sets(R, step1_plan.domain_counts(R))
MOCKS = {1: sorted(json.load(open(root + '/runs/mock-01/plan.json'))['scenarios']),
         2: sorted(json.load(open(root + '/runs/mock-02/plan.json'))['scenarios'])}
for m in (3, 4, 5):
    MOCKS[m] = list(step1_plan.fixed_scenarios(m))
def state(m):
    if os.path.exists(root + '/mocks/mock-%02d.questions.json' % m):
        return 'built' + (', fixed, decision 0057' if m >= 3 else '')
    if os.path.exists(root + '/runs/mock-%02d/plan.json' % m):
        return 'in work' + (', fixed, decision 0057' if m >= 3 else '')
    return 'planned, fixed, decision 0057'
COUNT = {s: sum(s in v for v in MOCKS.values()) for s in NAMES}
D = {}
for m, sc in MOCKS.items():
    src_ = 'runs/mock-%02d/plan.json: the seed selected the set (decision 0027).' % m if m < 3 else 'data/mock-scenarios.json: the owner fixed the set (decision 0057).'
    D['m%d' % m] = dict(title='Mock %d: scenarios %s' % (m, ', '.join(map(str, sc))), who=state(m).split(',')[0].capitalize(), cls='io',
        sent=['%d. %s (primary domains %s)' % (s, NAMES[s], ', '.join(map(str, PRIM[s]))) for s in sc] + [
              'Source: ' + src_, 'Permitted by decision 0027: %s.' % ('yes' if tuple(sc) in SETS else 'NO')])
for s in NAMES:
    D['s%d' % s] = dict(title='Scenario %d: %s' % (s, NAMES[s]), who='%d of 5 mocks' % COUNT[s], cls='code',
        sent=['Mocks: %s.' % ', '.join(str(m) for m, v in MOCKS.items() if s in v), 'Primary domains: %s.' % ', '.join(map(str, PRIM[s]))])
D['rule'] = dict(title='The 11 permitted sets (decision 0027)', who='Code', cls='code',
    sent=['Each question is in a primary domain of its scenario, and the domain counts are 16, 11, 12, 12 and 9. 11 of the 15 sets of 4 scenarios have such a table.',
          'Step 1 stops with an error if a fixed set is not one of them.'] + ['Permitted: ' + ', '.join('-'.join(map(str, x)) for x in SETS) + '.'],
    why='The owner fixed mocks 3 to 5 so that each scenario appears about equally: scenarios 1 and 4 come 4 times, the others 3 times.')
for d in D.values():
    for k in ('example', 'examplehead', 'examplenote', 'why'):
        d.setdefault(k, '')
    d.setdefault('points', [])

exec(g9[g9.index('def hot('):g9.index('sk = lambda')])
X0, W, Y0, H = 200, 120, 90, 64

def short(name):
    out = []
    for w in name.split():
        if len(' '.join(out + [w])) > 24:
            break
        out.append(w)
    return ' '.join(out)
parts = ['<div class="shead" style="top:2px"><i>1</i>Each mock uses 4 of the 6 scenarios</div>']
for s in NAMES:
    parts.append(hot('s%d' % s, 'colh', 'left:%dpx;top:44px;width:%dpx' % (X0 + (s - 1) * W, W - 8),
                     '<b>%d</b><small>%s</small>' % (s, e(short(NAMES[s]))), 'Scenario %d' % s))
for m, sc in MOCKS.items():
    y = Y0 + m * H
    parts.append(hot('m%d' % m, 'rowh', 'left:20px;top:%dpx' % y, '<b>Mock %d</b><small>%s</small>' % (
        m, state(m)), 'Mock %d' % m))
    for s in NAMES:
        parts.append('<div class="cell%s%s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (
            ' on' if s in sc else '', ' fx' if m >= 3 and s in sc else '', X0 + (s - 1) * W, y, W - 8))
yt = Y0 + 6 * H
for s in NAMES:
    parts.append('<div class="tot" style="left:%dpx;top:%dpx;width:%dpx">%d of 5</div>' % (X0 + (s - 1) * W, yt, W - 8, COUNT[s]))
parts.append(hot('rule', 'rpanel', 'left:20px;top:%dpx' % (yt + 50), '<h4>Each set is one of the 11 sets that decision 0027 permits</h4><small>A set outside them stops step 1 with an error.</small>', 'The permitted sets'))
paths = []
base9 = g9[g9.index('extra_css += """') + len('extra_css += """'):g9.index('"""\na = js.index')]
extra_css = g3[g3.index("extra_css = '''") + 15:g3.index("'''\na = js.index")]
extra_css = extra_css.replace('.stage { height: 836px; }', '.stage { height: 640px; }')
assert '640px' in extra_css
extra_css += base9 + """  .colh, .rowh, .rpanel { background: var(--panel); border: 1.5px solid var(--line); border-radius: 10px; }
  .colh:hover, .rowh:hover, .rpanel:hover { border-color: var(--muted); }
  .colh { height: 70px; padding: 6px 8px; text-align: center; }
  .colh b { display: block; font-size: 18px; } .colh small { font-size: 11px; color: var(--muted); line-height: 1.2; display: block; }
  .rowh { width: 160px; height: 52px; padding: 6px 12px; }
  .rowh b { display: block; font-size: 14px; } .rowh small { font-size: 11.5px; color: var(--muted); }
  .cell { position: absolute; height: 52px; border-radius: 8px; border: 1.5px dashed var(--line); }
  .cell.on { background: var(--code); border: none; opacity: .75; }
  .cell.on.fx { background: var(--owner); }
  .tot { position: absolute; text-align: center; font-weight: 700; font-size: 13px; }
  .rpanel { width: 712px; height: 64px; padding: 10px 14px; border-color: var(--code); }
  .rpanel h4 { margin: 0 0 4px; font-size: 14px; } .rpanel small { color: var(--muted); }
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
<title>Scenarios of the 5 mocks</title>
<style>''' + css + extra_css + '''</style>
</head>
<body>
<main>
  <h1>The scenarios of the 5 mocks</h1>
  <p class="sub">This diagram shows decision 0057. It changes step 1 (the plan). Mocks 1 and 2 have the sets that their seeds selected. The owner fixed the sets of mocks 3 to 5, so that each scenario appears about equally. Put the pointer on a mock, a scenario or the rule to see the detail.</p>

  <div class="scroll">
  <div class="stage">
    <svg viewBox="0 0 1000 640" width="1000" height="640" aria-hidden="true">
      ''' + marker + '''
      ''' + '\n      '.join(paths) + '''
    </svg>
    ''' + '\n    '.join(parts) + '''
    ''' + popdiv + '''
  </div>
  </div>

  <footer>Diagram 12. Decision 0057 of 8 October 2026. Status: built in step 1. It ran for mocks 3 and 4, not yet for mock 5. Blue: a set that the seed selected. Green: a set that the owner fixed. The sets come from runs/mock-01/plan.json, runs/mock-02/plan.json and data/mock-scenarios.json.</footer>
</main>

<script id="stepdata" type="application/json">''' + data + '''</script>
<script>''' + js2 + '''</script>
</body>
</html>
'''
out = root + '/docs/diagrams/12-scenarios-of-the-mocks.html'
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'hot', page.count('data-step='))
