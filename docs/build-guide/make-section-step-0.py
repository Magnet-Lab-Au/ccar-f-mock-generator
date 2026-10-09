"""Makes the build guide section of step 0. Run: python3 make-section-step-0.py

The counts come from reference/guide-records.json, and the guide texts come
from the same file. Nobody types them.
"""
import json
import os
import re

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
PT = {p['id']: (p, t) for t in REC['task_statements'] for p in t['points']}


def plain(text):
    return re.sub(r'\\(.)', r'\1', text)


def row(pid, use):
    p, t = PT[pid]
    return '| %s | "%s" | Task statement %s: %s | %s |' % (pid, plain(p['text']), t['id'], t['title'], use)


points = sum(len(t['points']) for t in REC['task_statements'])
text = '''# Step 0: prepare the guide records

Status: built. It ran on 6 October 2026.

Diagram: [`03-step-0-prepare-the-guide-records.html`](../diagrams/03-step-0-prepare-the-guide-records.html)

## What the step does

Before the program plans a mock, a script copies the parts of the exam guide that the later steps need into one file, `reference/guide-records.json` (decision 0028). No model copies text. The file is the one source of guide text for the code. A later step takes a slice of it by ID.

The file has the version of the guide, %d domains with their weights, %d scenarios with their stories and primary domains, %d task statements with their %d points, %d sample questions, and the three lists of Section 17.

Each point gets an ID that the guide does not have: the task statement, then K (knowledge) or S (skill), then the number of the bullet. Example: `1.4-K2` is the second bullet below "Knowledge of:" in task statement 1.4.

## The checks

- A second script checks the counts, and checks that each text in the file is exactly in the guide. It passed 41 of 41 checks.
- An independent reviewer checked the file and found no errors (`docs/reviews/review-guide-records.md`).
- The comparison of `reference/exam-guide.md` with the original, character for character, is not done.

If a count is wrong or a text is not exactly in the guide, the script writes no file and names the cause.

## The exam guide points that the step uses

Decision 0017 chose these points for step 0. Decision 0028 is the design of the step.

| Point | Text of the guide | Context in the guide | How the step uses it |
|---|---|---|---|
%s
''' % (len(REC['domains']), len(REC['scenarios']), len(REC['task_statements']), points, len(REC['sample_questions']),
       '\n'.join([
           row('1.3-S2', 'Written for agents that pass context to other agents. Here: each record keeps its ID, so each later step and each question keeps the link to its source.'),
           row('5.6-K1', 'Written for the synthesis of findings. Here: the records keep the exact guide text, so no summary loses the source.'),
           row('5.6-K2', 'The same context. Here: the IDs of the points are the mapping between a question and the text of the guide.'),
       ]))
out = root + '/docs/build-guide/step-0-prepare-the-guide-records.md'
open(out, 'w', encoding='utf-8', newline='\n').write(text)
print('written', out)
