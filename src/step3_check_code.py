"""Step 3 of the pipeline: code checks each question (decisions 0011, 0030, 0031 and 0038, part 8).

Code checks the rules A1 to A12, which have an exact answer. No model works in
this step. The control calls check(question, slot) and saves the verdict record
with the fingerprint and the date (decision 0039).

A question record has `question`, `select` and `options`. Each option has
`letter`, `text`, `correct` and `reason` (decision 0029).
"""
import re

# The limits of decision 0031. Each one is the range of the 12 sample questions
# of the guide, with a small margin.
QUESTION_WORDS = (25, 110)   # A6
OPTION_WORDS = (5, 45)       # A6
LONGER_LIMIT = 1.3           # A7
SENTENCES = (2, 5)           # A9

# Rule A5. The exact list is not decided (decision 0031). This is the first
# list, the same as in docs/decisions/0031-check-sample-lengths.py.
# The letter must be a capital letter, so that "the option a reviewer prefers" passes.
LETTER_WORDS = re.compile(r"\b((?i:option) [A-E]\b|(?i:all of the above)|(?i:none of the above)|(?i:both) [A-E] (?i:and) [A-E]\b)")


def words(text):
    return len(text.split())


def sentences(text):
    """A sentence ends with ".", "?" or "!" and a space comes after it (decision 0031).
    Known limit: a dot and then a quote mark does not end a sentence."""
    return [s for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s]


def finding(rule, detail, letter=None):
    return {"step": 3, "rule": rule, "detail": detail, "letter": letter, "point": None,
            "other_questions": []}


def _form_findings(question, slot):
    """Rule A1: the form is complete. Returns the findings, and the options that
    are complete enough for the other rules."""
    found = []
    if not isinstance(question, dict):
        return [finding("A1", "The question record is not complete.")], []
    text = question.get("question")
    if not isinstance(text, str) or not text.strip():
        found.append(finding("A1", "The question has no text."))
    options = question.get("options")
    if not isinstance(options, list) or not options:
        found.append(finding("A1", "The question has no options."))
        return found, []
    good = []
    for i, o in enumerate(options):
        letter = o.get("letter") if isinstance(o, dict) else None
        name = "Option %s" % (letter or i + 1)
        if not isinstance(o, dict):
            found.append(finding("A1", "%s is not complete." % name))
            continue
        missing = []
        if not isinstance(o.get("text"), str) or not o["text"].strip():
            missing.append("a text")
        if not isinstance(o.get("correct"), bool):
            missing.append("a mark")
        if not isinstance(o.get("reason"), str) or not o["reason"].strip():
            missing.append("a reason")
        if missing:
            found.append(finding("A1", "%s has no %s." % (name, " and no ".join(missing)), letter))
        if isinstance(o.get("text"), str) and o["text"].strip():
            good.append(o)
    letters = [o.get("letter") if isinstance(o, dict) else None for o in options]
    if letters != list("ABCDE"[:len(options)]):
        found.append(finding("A1", "The options do not have the letters A to %s in sequence." % "ABCDE"[min(len(options), 5) - 1]))
    return found, good


def check(question, slot, rules=None):
    """Return {"verdict": "pass" or "fail", "findings": [...]}.
    `rules` limits the check to some rules, for example A4 to A11 for the sample
    questions of the guide (decision 0024). None means all rules."""
    use = (lambda r: True) if rules is None else (lambda r: r in rules)
    found = []
    form, options = _form_findings(question, slot)
    if use("A1"):
        found.extend(form)
    if not isinstance(question, dict):
        question = {}
    # The other rules run on each option that has a text, also when A1 fails, so
    # that a check with only some rules (decision 0024) still sees each option.
    text = question.get("question") if isinstance(question.get("question"), str) else ""
    all_options = question.get("options") if isinstance(question.get("options"), list) else []
    texts = options

    if use("A2") and slot is not None and len(all_options) != slot.get("options"):
        found.append(finding("A2", "The question has %d options. The slot needs %s." % (len(all_options), slot.get("options"))))
    if use("A3") and slot is not None:
        correct = sum(1 for o in all_options if isinstance(o, dict) and o.get("correct") is True)
        if correct != slot.get("select"):
            found.append(finding("A3", "%d options are marked correct. The slot needs %s." % (correct, slot.get("select"))))
    if use("A4"):
        seen = {}
        for o in texts:
            key = " ".join(o["text"].lower().split())
            if key in seen:
                found.append(finding("A4", "Options %s and %s have the same text." % (seen[key], o.get("letter")), o.get("letter")))
            else:
                seen[key] = o.get("letter")
    if use("A5"):
        if text and LETTER_WORDS.search(text):
            found.append(finding("A5", 'The question names a letter or an option: "%s".' % LETTER_WORDS.search(text).group(0)))
        for o in texts:
            reason = o.get("reason") if isinstance(o.get("reason"), str) else ""
            for part, value in (("text", o["text"]), ("reason", reason)):
                m = LETTER_WORDS.search(value)
                if m:
                    found.append(finding("A5", 'The %s of option %s names a letter or an option: "%s".' % (part, o.get("letter"), m.group(0)), o.get("letter")))
    if use("A6"):
        n = words(text)
        if not QUESTION_WORDS[0] <= n <= QUESTION_WORDS[1]:
            found.append(finding("A6", "The question has %d words. The limit is %d to %d." % (n, QUESTION_WORDS[0], QUESTION_WORDS[1])))
        for o in texts:
            n = words(o["text"])
            if not OPTION_WORDS[0] <= n <= OPTION_WORDS[1]:
                found.append(finding("A6", "Option %s has %d words. The limit is %d to %d." % (o.get("letter"), n, OPTION_WORDS[0], OPTION_WORDS[1]), o.get("letter")))
    if use("A7"):
        right = [words(o["text"]) for o in texts if o.get("correct") is True]
        wrong = [words(o["text"]) for o in texts if o.get("correct") is False]
        if right and wrong:
            ratio = (sum(right) / len(right)) / (sum(wrong) / len(wrong))
            if ratio > LONGER_LIMIT:
                found.append(finding("A7", "The correct options are %.2f times as long as the wrong options. The limit is %.1f." % (ratio, LONGER_LIMIT)))
    if use("A8") and not text.strip().endswith("?"):
        found.append(finding("A8", "The question does not end with a question mark."))
    if use("A9"):
        n = len(sentences(text))
        if not SENTENCES[0] <= n <= SENTENCES[1]:
            found.append(finding("A9", "The question has %d sentences. The limit is %d to %d." % (n, SENTENCES[0], SENTENCES[1])))
    if use("A10"):
        for o in texts:
            if len(sentences(o["text"])) != 1:
                found.append(finding("A10", "Option %s has more than one sentence." % o.get("letter"), o.get("letter")))
    if use("A11") and text:
        # Decision 0038, part 8. The options do not count.
        m = re.search(r"\b(NOT|EXCEPT)\b", text)
        if m:
            found.append(finding("A11", 'The question has "%s" in capital letters.' % m.group(0)))
        last = sentences(text)[-1] if sentences(text) else ""
        m = re.search(r"\b(not|except)\b", last)
        if m:
            found.append(finding("A11", 'The last sentence of the question has "%s".' % m.group(0)))
    if use("A12") and slot is not None and slot.get("longest_may_be_correct") is False:
        # Decision 0053. A slot of a plan before decision 0053 has no field, and
        # the rule does not apply to it.
        right = [len(o["text"]) for o in texts if o.get("correct") is True]
        wrong = [len(o["text"]) for o in texts if o.get("correct") is False]
        if right and wrong and max(right) >= max(wrong):
            longest = max(texts, key=lambda o: (len(o["text"]), o.get("correct") is True))
            found.append(finding("A12", "The longest option is a correct option (%d characters). The slot needs a "
                                        "wrong option that is longer than each correct option." % max(right),
                                 longest.get("letter")))
    return {"verdict": "fail" if found else "pass", "findings": found}
