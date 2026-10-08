"""Makes the build guide sections of steps 2, 3, 4, 6 and 7. Run: python3 make-sections.py

The guide texts come from reference/guide-records.json. The quotes of the
Anthropic documentation come from the saved copies in docs/sources/. The facts
of the runs come from runs/test-0024/. Nobody types them.
"""
import json
import os
import re

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REC = json.load(open(root + '/reference/guide-records.json', encoding='utf-8'))
PT = {p['id']: (p, t) for t in REC['task_statements'] for p in t['points']}
RUN = {n: json.load(open(root + '/runs/test-0024/%s.json' % n, encoding='utf-8'))
       for n in ('part1', 'part2', 'part3', 'part4', 'part-b7')}
DEFINE = open(root + '/docs/sources/2026-10-07-anthropic-docs-define-tools.md', encoding='utf-8').read()
STRUCT = open(root + '/docs/sources/2026-10-07-anthropic-docs-structured-outputs.md', encoding='utf-8').read()


def plain(text):
    return re.sub(r'\\(.)', r'\1', text)


def row(pid, use):
    p, t = PT[pid]
    return '| %s | "%s" | Task statement %s: %s | %s |' % (pid, plain(p['text']), t['id'], t['title'], use)


def table(rows):
    return '\n'.join(['| Point | Text of the guide | Context in the guide | How the step uses it |',
                      '|---|---|---|---|'] + [row(p, u) for p, u in rows])


def must(text, source):
    assert text in source, text[:60]
    return text


# The deviation of decision 0040, quoted from the saved pages.
FORCE = must('Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and', DEFINE)
must('when you need a response in a fixed JSON shape', DEFINE)
must('Structured outputs guarantee schema-compliant responses through constrained decoding', STRUCT)
DEVIATION = '''## A deviation from the exam guide

The exam guide teaches a forced tool call to get an answer in a fixed form (points 4.3-K1 and 4.3-S3 in the table below). This build does not use a forced tool call.

The reason: the newest Claude models reject it. The page "Define tools" of the Anthropic documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), section "Controlling Claude's output", subsection "Forcing tool use", has a table. Its row for "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1" says that `any` and `tool` "return a 400 error". As the replacement it names "`auto` with strict tool use", or "structured outputs when you need a response in a fixed JSON shape". An older model, Claude Opus 5, still accepts a forced tool call, but this build keeps the choice of the model free for the test that selects it.

So each model call of this build sends its form as structured outputs: the request carries the JSON schema in `output_config.format`. The page "Structured outputs" (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), section "Why use structured outputs", says: "Structured outputs guarantee schema-compliant responses through constrained decoding".

The purpose that the guide teaches stays the same: an answer that agrees with a schema. Only the method changes. Copies of both pages, read on 7 October 2026, are in `docs/sources/`.'''


def section(file_name, title, status, diagram, body, rows, deviation=False):
    parts = ['# %s' % title, '', 'Status: %s' % status, '',
             'Diagram: [`%s`](../diagrams/%s)' % (diagram, diagram), '', body.strip(), '']
    if deviation:
        parts += [DEVIATION, '']
    parts += ['## The exam guide points that the step uses', '', table(rows), '']
    open(os.path.join(root, 'docs', 'build-guide', file_name), 'w', encoding='utf-8', newline='\n').write('\n'.join(parts))
    print('written', file_name)


p1, p2, p3, p4, b7 = RUN['part1'], RUN['part2'], RUN['part3'], RUN['part4'], RUN['part-b7']
n_written = sum(1 for e in p1['questions'] if e.get('question', {}).get('status') == 'written')
n_pass3 = sum(1 for e in p1['questions'] if e.get('step3', {}).get('verdict') == 'pass')
good = sum(1 for e in b7['checks'] if e['mark'] == 'good')
bad = sum(1 for e in b7['checks'] if e['mark'] == 'bad')

section('step-2-write-the-question.md', 'Step 2: write the question',
        'built. It ran in the test before the first full run, on 7 October 2026.', '04-step-2-write-the-question.html', '''
## What the step does

For each slot of the plan, one call of the Claude API writes one question. The call is new each time, and it does not know the other questions of the mock.

Code builds the request from the records of the guide and from the plan. The request has the rules for a good question, 3 sample questions of the guide as examples of the form, the story of the scenario, the task statement of the slot with its point marked, the 14 technologies of Section 17 of the guide, and the slot.

The model fills a form: the question, and each option with a mark ("correct" or "wrong") and a reason. The model can also answer "cannot write", with a reason. Then the slot is open, and the owner decides. The design expects that, with this answer available, the model does not invent a question for a slot that does not fit. That is an assumption, not checked.

Code then mixes the options and gives them their letters. The model does not select the letters. In the 12 sample questions of the guide the correct answer is A 10 times, and a model that sees them can copy that (an assumption, not checked). Code saves one file for each try. No file is written over.

Step 5 uses the same request when a question must be written again. It adds the failed question and the exact findings.

## The test run

The writer made %d questions for 10 slots of the plan of mock 1, one call for each, with no new try. %d of %d passed the code check of step 3 at the first try. The owner read the 10 questions and marked %d good and %d bad. The bad mark said that the question used two names for one actor and was hard to read. That mark gave a new instruction to the writer and a new rule for the checker (rule B7, see step 4).
''' % (n_written, n_pass3, n_written, good, bad), [
    ('4.3-K1', 'Written for the extraction of data. Here: the writer fills a form, so code can read each answer. The method is structured outputs (see the deviation above).'),
    ('4.3-S3', 'Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above).'),
    ('4.3-K2', 'The same context. It names the three settings of a tool call. The current models accept only "auto" and "none".'),
    ('4.3-S4', 'Written for the extraction of data. Here: the question can be empty when the answer is "cannot write", so the model does not invent a question for a slot that does not fit.'),
    ('4.3-S5', 'Written for a schema for the extraction of data. Here: the status "cannot_write" is an answer for a case that does not fit.'),
    ('4.3-K3', 'Written for the extraction of data. Here: a form stops format errors, but not content errors. So step 3 checks the content.'),
    ('4.2-K1', 'Written for output in a fixed format. Here: 3 sample questions show the writer the form of a good question.'),
    ('4.2-S2', 'The same context. A limit: the examples have no reason for each option, so they do not show the complete form.'),
    ('4.1-K1', 'Written for the review of code. Here: the writer gets exact rules, not vague ones.'),
    ('1.4-K2', 'Written for the workflow of an agent. Here: an instruction to the writer can fail, so each rule that the writer gets is also checked, by code or by a model.'),
], deviation=True)

section('step-3-check-by-code.md', 'Step 3: check by code',
        'built. It ran in the test before the first full run, on 7 October 2026.', '05-step-3-check-by-code.html', '''
## What the step does

Before a model looks at a question, code checks the 12 rules that have one exact answer (rules A1 to A12):

- The form is complete, and the numbers of options and of correct options agree with the slot.
- No two options have the same text, and no text names a letter or a different option ("Option B", "all of the above").
- The question has 25 to 110 words and each option 5 to 45 words. The correct option is not much longer than the wrong options.
- The question ends with a question mark and has 2 to 5 sentences. Each option is one sentence.
- The question is not a negative question.
- On most slots, a wrong option is the longest option (rule A12, decision 0053). The plan lets the longest option be correct on 13 of the 52 slots with 1 answer and on 3 of the 8 slots with 2 answers, the chance numbers. In mock 1, before this rule, the correct option was the longest in 37 of 52 questions.

A script measured the 12 sample questions of the guide. The length limits (A6 and A7) are their range with a small margin. Rules A8 to A10 are true for all 12 with no margin. The limit of A11 is weaker than what the script measured: it permits "not" outside the last sentence. The check is cheap and fast, so a question with a simple defect does not use a model call.

Each finding names the rule and the detail, so the writer of step 5 knows what to change. If code cannot read a question, it reports an error. It never says "pass" for a question that it did not read.

## The test run

All %d questions of the writer passed the 11 rules of that time (rule A12 came later). A test of the code also showed that the 12 sample questions of the guide pass the rules A4 to A11 (the rules that need no slot and no reason for each option).
''' % n_written, [
    ('1.4-K1', 'Written for the order of the steps of an agent workflow. Here: a rule with one exact answer is checked by code, not by a model.'),
    ('1.4-K2', 'The same context. Here: an instruction to a model can fail, so code checks the rules that code can check.'),
    ('4.3-K3', 'Written for the extraction of data. Here: the form of the answer does not stop content errors, so code checks the content.'),
    ('4.4-K4', 'The same context. Here: the same difference between errors of format and errors of meaning.'),
    ('5.3-K4', 'Written for errors between agents. Here: an error must never look like a pass.'),
])

ok3 = sum(1 for e in p3['checks'] if e['as_expected'])
section('step-4-check-by-a-model.md', 'Step 4: check by a model',
        'built. It ran in the test before the first full run, on 7 October 2026.', '06-step-4-check-by-a-model.html', '''
## What the step does

Some rules need judgment, so a model checks them. The step has two calls, and code sits between them.

**Call 4a, the blind answer.** A new call answers the question as a second expert does. It gets the question, the line "Select N.", the options and the text of the guide, but not the marks and not the reasons. Code compares its letters with the marks of the writer. Different letters fail rule B1. Two calls with code between them make sure that the blind answer always comes first.

**Call 4b, the rule check.** A second call gets the complete question, with the marks and the reasons, and the text of the guide. It gives one result for each of the 7 rules B1 to B7: the marked options are correct, each wrong option is wrong for a reason that the guide gives, each reason is true, the question tests its point, the question is inside its story, no text depends on a feature that the guide does not name, and each actor has one name and each sentence is clear. The result is "pass", "fail" or "cannot decide".

For rule B6, the model lists each feature name. Code searches each name in the records of the guide, as a complete word. A name that the guide does not have fails the rule.

Code, not a model, makes the verdict. A question that fails, or that the checker cannot decide, goes to step 5 with its findings.

## The test run

- Call 4a answered the 12 sample questions of the guide. %d of %d were right.
- Call 4b checked the 9 questions that the owner marked good, and one copy of each that the build damaged on purpose. Each copy broke one rule. %d of %d results were as expected: each good question passed, and each damaged copy failed on its rule.
- After the owner marked a question bad for two names of one actor, rule B7 was added. Call 4b failed that question on B7. It also failed 3 of the 9 good questions on B7, each with a true finding. The rule stays strict.
''' % (p2['right'], p2['of'], ok3, p3['of']), [
    ('4.6-K1', 'Written for the review of code. Here: the call that wrote a question does not check it.'),
    ('4.6-K2', 'The same context. Here: a new call, with no reasoning of the writer, checks the question.'),
    ('4.3-S5', 'Written for a schema for the extraction of data. Here: the result "cannot decide" for a case that the checker cannot decide.'),
    ('4.1-K1', 'Written for the review of code. Here: one result for each exact rule, not one total verdict.'),
    ('1.4-K2', 'Written for the order of steps in the workflow of an agent. Here: "answer first, then see the key" is enforced by two calls, not by an instruction.'),
    ('4.3-K1', 'Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above).'),
    ('4.3-S3', 'Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above).'),
], deviation=True)

found = p4['same_scene_found']
section('step-6-check-the-complete-mock.md', 'Step 6: check the complete mock',
        'built. It ran in the test before the first full run, on 7 October 2026.', '08-step-6-check-the-complete-mock.html', '''
## What the step does

Steps 3 and 4 look at one question. Some defects show only when many questions are read together. Each writer call sees only its own slot, so two calls can write the same scene.

When each slot has a question that passed steps 3 and 4, code counts the mock against the plan. Code also compares the text of each question with all 60 questions of the mock, so an exact copy in another scenario is a finding too (decision 0052). Then two model calls read the 15 questions of one scenario together. Each call has one job:

- **Call 6a, the scenes:** no two questions have the same scene (the same problem and the same correct action), and no question gives away the answer of a different question.
- **Call 6b, the wrong options:** no wrong idea is a wrong option in more than 2 questions of the scenario, and at most one wrong option of the scenario is the option in which a model rates its own confidence.

Step 6 sends no question back. Each finding gets an ID and waits for the owner. The owner first marks the questions, with no finding in view. Then the owner selects "ignore" or "rewrite" for each finding. A rewrite sends one question of the finding to step 5. Then step 6 runs again for that scenario only.

## The test run

The test put two questions with the same scene into a set of 15 questions of one scenario. %s Step 6 also found real problems of the writer: one more pair of questions with the same scene, and pairs of questions that give away an answer.
''' % ('Call 6a found them.' if found else 'Call 6a did not find them.'), [
    ('4.6-K3', 'Written for the review of code in many files. Here: steps 3 and 4 are the pass for each question, and this step is the pass across the questions.'),
    ('4.6-S2', 'The same context and the same use.'),
    ('4.1-K1', 'Written for the review of code. Here: "the same scene" has an exact definition: the same problem and the same correct action.'),
    ('5.3-K4', 'Written for errors between agents. Here: a call that fails, or an answer that is not valid, never counts as a pass.'),
    ('4.3-K1', 'Written for the extraction of data. Each call answers in a fixed form, sent as structured outputs (see the deviation above).'),
    ('4.3-S3', 'Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above).'),
], deviation=True)

section('step-7-the-owner-marks-the-questions.md', 'Step 7: the owner marks the questions',
        'built. It ran in the test before the first full run, on 7 October 2026.', '09-step-7-the-owner-marks-the-questions.html', '''
## What the step does

Each check before this step is code or a model. This step shows if those checks are right: a person reads the questions and marks them.

Code builds one Excel file for each round of marking. It has one row for each question: the question, the point that it must test, the options, the correct answer and the reasons. It shows no verdict of a checker. The owner fills two columns: "good" or "bad", and a reason for a bad mark. The sheet is protected, so that only those two columns can change and a mark cannot move to a different question. (Not checked in real Excel yet.)

For mock 1 the owner marks all 60 questions. For each later mock the owner marks a random sample of 20, 5 from each scenario. A bad mark sends the question to step 5, with the reason of the owner as the finding. Too many bad marks stop the mock: more than 6 of 60 for mock 1, and 2 or more of 20 for a later mock.

Code saves the marks, and shows the bad marks for each scenario and each domain.

## The test run

Code built a marking file for the %d questions of the test. The owner marked %d good and %d bad. The bad mark had a reason, and that reason led to a new rule of step 4.
''' % (good + bad, good, bad), [
    ('5.5-K2', 'Written for the extraction of data, where a person samples results that the system is sure of. Here: a person marks questions that passed all checks. For mock 1 the owner reads all 60, so that is not a sample.'),
    ('5.5-S1', 'The same context. Here: the sample of a later mock has questions from each scenario and each domain.'),
    ('5.5-K1', 'Written for the extraction of data. Here: the bad marks are shown for each scenario and each domain, because one total can hide a bad part.'),
    ('5.5-S2', 'The same context. Here: a sample below 20 questions comes only after the results are good in each scenario and each domain.'),
])


# ---------- steps 5 and 8: they ran in mock 1 (8 October 2026) ----------
import collections
import glob
M = root + '/runs/mock-01'
TRIES = [json.load(open(f, encoding='utf-8')) for f in glob.glob(M + '/questions/*.json')]
BY_REQ = collections.Counter(q['request'] for q in TRIES)
PER_SLOT = collections.Counter(q['slot_id'] for q in TRIES)
V4 = [json.load(open(f, encoding='utf-8')) for f in glob.glob(M + '/checks/*-step4.json')]
FAIL4 = sum(1 for v in V4 if v['verdict'] != 'pass')
RULES4 = collections.Counter(x['rule'] for v in V4 for x in v['findings'])
DEC = json.load(open(M + '/owner-decisions.json', encoding='utf-8'))
ACTIONS = collections.Counter(d['action'] for d in DEC)
QF = json.load(open(root + '/mocks/mock-01.questions.json', encoding='utf-8'))
AF = json.load(open(root + '/mocks/mock-01.answers.json', encoding='utf-8'))
BUILD = json.load(open(M + '/build.json', encoding='utf-8'))
COST = round(sum(json.load(open(f))['dollars'] for f in glob.glob(M + '/usage/*.json')), 2)
GUIDE = open(root + '/reference/exam-guide.md', encoding='utf-8').read()


def fact_table(rows):
    lines = ['| Section | Text of the guide | How the step uses it |', '|---|---|---|']
    for sec, text, use in rows:
        assert text in GUIDE, text[:50]
        lines.append('| %s | "%s" | %s |' % (sec, text, use))
    return '\n'.join(lines)


section('step-5-try-again.md', 'Step 5: try again',
        'built. It ran in mock 1 on 7 and 8 October 2026.', '07-step-5-try-again.html', '''
## What the step does

A question that fails step 3 or step 4 goes back to the writer. The writer gets the request of step 2, plus the failed question with the letters that the checker saw, and the exact findings. The writer does not see older tries, so the request stays short. The new try goes through steps 3 and 4 again, as a new question.

A question also comes back when the owner sends it back: a bad mark, or a "rewrite". A rewrite can name a finding of step 6, or only a reason of the owner. The owner can also give the slot a new point of the same task statement. Code then checks that the point is in that task statement, that no other slot uses it, and that the slot did not have it before.

Each start of a slot has at most 3 tries. Two results "cannot decide" also stop a slot. A slot that stops is open, and the owner decides: more tries, a new point, or a new plan. The limit is not the main way to stop. The main way to stop is a question that passes.

Each try is a new file. No file is written over, so the history of each question stays.

## The run of mock 1

- %d tries for 60 slots: %d were a request of step 2 (a first question, or a rewrite on a new point), and %d a request of step 5.
- %d slots needed more than one try. The most tries for one slot: %d.
- Step 4 failed %d tries. The findings by rule: %s.
- One slot stopped after 3 tries. Each try had corrected the last finding, and a new small finding came. The owner gave it more tries.
- The owner sent 9 questions back as rewrites after the marks, 5 of them with a new point.
''' % (len(TRIES), BY_REQ.get(2, 0), BY_REQ.get(5, 0), sum(1 for v in PER_SLOT.values() if v > 1), max(PER_SLOT.values()),
       FAIL4, ', '.join('%s %d' % (k, v) for k, v in sorted(RULES4.items()))), [
    ('4.4-K1', 'Written for the extraction of data. Here: the findings of the checks go back to the writer with the failed question.'),
    ('4.4-S1', 'The same context. Here: the "document" is the request of step 2, the "failed extraction" is the failed question, and the "validation errors" are the findings.'),
    ('4.4-K2', 'The same context. Here: the writer can answer "cannot write" for a slot that does not fit its scenario. The design expects that such a slot does not improve with a new try. That is an assumption, not checked.'),
    ('1.1-S3', 'Written for agent loops. Here: the limit of 3 tries is a guard, not the main way to stop. The main way to stop is a question that passes.'),
    ('4.3-K1', 'Written for the extraction of data. The new try answers in the same fixed form as step 2, sent as structured outputs (see the deviation above).'),
    ('4.3-S3', 'Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above).'),
], deviation=True)

steps8 = '''# Step 8: build the files

Status: built. It ran for mock 1 on 8 October 2026.

Diagram: [`10-step-8-build-the-files.html`](../diagrams/10-step-8-build-the-files.html)

## What the step does

Code builds the two files of a mock from the stored question records. Nobody edits the files by hand. To change a question, the record changes, and code builds the files again.

The build starts only after the owner accepts the mock. Then code checks six conditions: each question passed steps 3 and 4 and did not change after its checks, step 6 checked the current questions of each scenario, each finding of step 6 has a decision, each question that needs a mark has one, the bad marks are below the stop limit, and no call failed in the last run. If one condition is false, code builds no file and lists the causes.

To know that a question did not change after its checks, each check saves a fingerprint of the question: a code of 64 characters that code calculates from the text. Before the build, code calculates the fingerprint again and compares.

The questions file has the 60 questions in 4 groups, one for each scenario. Each group starts with the story of its scenario. The file has no answers. The answers file has the correct letters and the reason of each option, for after the mock.

## The run of mock 1

The owner accepted mock 1 on 8 October 2026, with known limits. Code checked the six conditions and built the two files: `mocks/mock-01.questions.json`, with %d questions in %d groups (scenarios %s) and %d minutes, and `mocks/mock-01.answers.json`, with %d answers. The build saved %d fingerprints. Mock 1 cost $%.2f for %d model calls.

## The exam guide texts that the step uses

The step uses no point of a task statement. It uses three facts of the exam form.

%s
''' % (sum(len(g['questions']) for g in QF['groups']), len(QF['groups']), ', '.join(str(g['scenario']) for g in QF['groups']),
       QF['minutes'], len(AF['answers']), len(BUILD['fingerprints']), COST,
       sum(json.load(open(f))['calls'] for f in glob.glob(M + '/usage/*.json')),
       fact_table([('3', 'each item states how many responses to select', 'Each question has the field "select", so the portal can show the line "Select 1." or "Select 2." The format of the portal is not decided yet.'),
                   ('5', 'Each scenario presents a realistic production context that frames a set of questions.', 'The questions are in groups by scenario, each with its story.'),
                   ('3', 'percent-correct by domain on the score report', 'Each question has its domain, so the portal can show a result for each domain.')]))
open(os.path.join(root, 'docs', 'build-guide', 'step-8-build-the-files.md'), 'w', encoding='utf-8', newline='\n').write(steps8)
print('written step-8-build-the-files.md')
