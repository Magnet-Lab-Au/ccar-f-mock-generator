"""Steps 2 and 5: the writer call (decisions 0010, 0029, 0030, 0033, 0037 and 0040).

Step 2 writes the first question of a slot. Step 5 writes a new try: it is the
request of step 2, plus the failed question with its letters and its findings
(decision 0033). The control decides which request a slot gets (decision 0039,
item 8). This file builds the request, sends it, checks the answer, and gives
the options their letters.
"""
import json
import random
import re

from control import CallFailed
from model_call import load_form

DESCRIPTION, SCHEMA = load_form("04-form-schema-draft.json")


def plain(text):
    """Remove the backslash that the records keep from the format of the guide."""
    return re.sub(r"\\(.)", r"\1", text)


# Decisions 0030, 0043, 0053, 0055 and 0056: the 21 rules. The writer gets all of them. The text of each
# rule is the text of decision 0030, with rule A11 of decision 0038, part 8.
B9_STRICT = ("B9. The question does not have the same problem as an earlier question on the same idea, also in another setting (another tool, team, product or data). The same problem means that the same thing goes wrong, or the team must make the same choice, so the same reasoning leads to the answer. A question on the same idea passes only with a different problem: for example the cause against the fix, a different failure, or a choice between two rules. Not the same set of wrong options as an earlier question on the same idea. At most one wrong option may repeat.")
# Decision 0066: an idea with almost only one problem keeps the copy rule.
B9_COPY = ("B9. The question is not a copy of an earlier question on the same idea: not the same scene with the same answer "
           "and the same set of wrong options. At most one wrong option may repeat. This idea has almost only one problem, "
           "so the same problem and answer may come back.")
RULES = """Rules for a good question. Code checks group A. A second model checks group B.

Group A, rules with an exact answer:
A1. The form is complete: a question, and each option has a text, a mark and a reason.
A2. The number of options agrees with the slot (4 or 5).
A3. The number of correct options agrees with the slot (1 or 2).
A4. No two options have the same text.
A5. No text names a letter or a different option: no "Option B", no "all of the above", no "none of the above".
A6. The question has 25 to 110 words. Each option has 5 to 45 words.
A7. The correct option is not much longer than the wrong options: at most 1.3 times their average length.
A8. The text of the question ends with a question mark.
A9. The text of the question has 2 to 5 sentences.
A10. Each option is one sentence.
A11. The question is not a negative question. The question text does not have "NOT" or "EXCEPT" in capital letters. The last sentence of the question text does not have "not" or "except".
A12. When the slot has "longest_may_be_correct": false, at least one wrong option is longer (in characters) than each correct option.

Group B, rules that need judgment:
B1. Each option that is marked correct is correct, and no other option is correct.
B2. Each wrong option is wrong for a reason that the guide gives, and its reason says so.
B3. Each reason is true and agrees with the guide.
B4. The question tests the point of its slot.
B5. The question is inside the story of its scenario and does not contradict it.
B6. No text depends on a feature that the guide does not name. A feature is a thing of a Claude product or of MCP that has a name: a tool, a command, a flag, a parameter, a field, a file or a setting. A name that the question invents for its story is not a feature. General technology, for example Python, is not a feature.

B7. Each actor has one name in the question, the options and the reasons. A reader understands each sentence at the first reading.
B8. The question is not a close copy of a sample question of the exam guide: not the same scene with the same correct action.
%s

Two more instructions:
- The options of a question have the same form. Example: all are actions, or all are places, or all are causes.
- Use one name for one actor. Write each sentence so that a reader understands it at the first reading. (Decision 0043.)

The question does not say how many answers to select. Code adds the line "Select 1." or "Select 2." to each question. Do not give letters to the options. Code gives the letters.""" % B9_STRICT

SYSTEM = ("You write one exam question for a mock exam of the exam \"Claude Certified Architect - Foundations\". "
          "The question must follow the rules exactly, and it must use only facts that the exam guide states. "
          "Return the question in the form. " + DESCRIPTION)


def examples(records, slot, count=3):
    """Decision 0029, part 1.2, and decision 0037, item 12: sample questions of
    scenarios that are not the scenario of the slot. Code keeps the question and
    the options, mixes the options, removes the letters, marks the correct
    option and leaves out the explanation. Which samples, when more are possible,
    was not decided: the slot ID selects them, so the same slot gets the same
    examples."""
    pool = [s for s in records["sample_questions"] if s["scenario"] != slot["scenario"]]
    rng = random.Random("examples-%s" % slot["slot_id"])
    chosen = sorted(rng.sample(pool, min(count, len(pool))), key=lambda s: s["number"])
    out = []
    for s in chosen:
        options = [{"text": plain(text), "correct": letter in s["correct_answer"]}
                   for letter, text in sorted(s["options"].items())]
        rng.shuffle(options)
        out.append({"question": plain(s["question"]), "options": options})
    return out


EARLIER_RULE = ("EARLIER QUESTIONS ON THE SAME IDEA (decisions 0056 and 0066). Earlier mocks have the questions below on the idea "
                "of this slot. Write a question with a different problem, also if you change the setting: a different thing "
                "goes wrong, or the team must make a different choice. For example the cause against the fix, a different "
                "failure, or a choice between two rules. The correct action may be the same, if the idea has only one. "
                "Do not use the same set of wrong options as an earlier question. At most one wrong option may repeat.")


EARLIER_RULE_NARROW = ("EARLIER QUESTIONS ON THE SAME IDEA (decisions 0056 and 0066). Earlier mocks have the questions below on the "
                       "idea of this slot. This idea has almost only one problem, so the same problem and answer may come back. "
                       "Use a different setting and scene. Do not use the same set of wrong options as an earlier question. "
                       "At most one wrong option may repeat.")


def earlier_text(questions):
    """The earlier questions on the same idea, with the mark of each option."""
    return json.dumps([{"question_id": q["question_id"], "question": q["question"],
                        "options": [("CORRECT: " if o["correct"] else "WRONG: ") + o["text"] for o in q["options"]]}
                       for q in questions], indent=2, ensure_ascii=False)


def request_text(request, records):
    """The text of the request of step 2 or step 5 (decisions 0029 and 0033)."""
    slot = request["slot"]
    scenarios = {s["id"]: s for s in records["scenarios"]}
    ts = next(t for t in records["task_statements"] if t["id"] == slot["task_statement"])
    point = request["point"]
    parts = [RULES.replace(B9_STRICT, B9_COPY) if request.get("narrow") else RULES, "",
             "Examples of the form of a question (from the exam guide, with the letters removed):",
             json.dumps(examples(records, slot), indent=2, ensure_ascii=False), "",
             "The story of the scenario %d (%s):" % (slot["scenario"], scenarios[slot["scenario"]]["name"]),
             plain(scenarios[slot["scenario"]]["story"]), "",
             "The task statement %s: %s. Its points (the point of the slot is marked with >>>):" % (ts["id"], ts["title"])]
    for p in ts["points"]:
        parts.append("%s %s: %s" % (">>>" if p["id"] == point else "   ", p["id"], plain(p["text"])))
    parts += ["", "The technologies that the guide names (Section 17):"]
    parts += ["- " + plain(t) for t in records["section_17"]["technologies"]]
    parts += ["", "The slot: " + json.dumps({"scenario": slot["scenario"], "task_statement": slot["task_statement"],
                                           "point": point, "type": slot["type"], "options": slot["options"],
                                           "select": slot["select"],
                                           "longest_may_be_correct": slot.get("longest_may_be_correct", True)}),
              "Write %d options. Mark exactly %d of them correct." % (slot["options"], slot["select"])]
    if request.get("earlier_questions"):
        rule = EARLIER_RULE_NARROW if request.get("narrow") else EARLIER_RULE
        parts += ["", rule, earlier_text(request["earlier_questions"])]
    if slot["select"] == 2:
        # Decision 0054: a question with 2 answers needs two different correct options.
        parts.append("The two correct options test two different parts of the point. They are not two examples of one idea.")
    if request["step"] == 2 and (request.get("findings") or request.get("other_questions")):
        # Decision 0045: a rewrite with a new point. The writer must not repeat the other questions.
        parts += ["", "A NEW QUESTION FOR THIS SLOT, ON THE POINT MARKED ABOVE. The owner asks for it:",
                  json.dumps([f["detail"] for f in request.get("findings", [])], indent=2, ensure_ascii=False)]
        if request.get("other_questions"):
            parts += ["Other questions of this mock. Do not write the same scene, and do not test the same idea:",
                      json.dumps([{"question_id": q["question_id"], "question": q.get("question"),
                                   "options": [o.get("text") for o in q.get("options", [])]}
                                  for q in request["other_questions"]], indent=2, ensure_ascii=False)]
    if request["step"] == 5:
        failed = request["failed_question"]
        shown = {"question": failed.get("question"), "select": failed.get("select"),
                 "options": failed.get("options"), "cannot_write_reason": failed.get("cannot_write_reason")}
        parts += ["", "A NEW TRY. The question below did not pass. Write a new question for the same slot. "
                  "Correct each finding. The letters are the letters that the checker saw.",
                  "The failed question:", json.dumps(shown, indent=2, ensure_ascii=False),
                  "The findings:", json.dumps(request["findings"], indent=2, ensure_ascii=False)]
        if request.get("other_questions"):
            parts += ["The other questions that a finding names. Do not write the same scene:",
                      json.dumps([{"question_id": q["question_id"], "question": q.get("question"),
                                   "options": [o.get("text") for o in q.get("options", [])]}
                                  for q in request["other_questions"]], indent=2, ensure_ascii=False)]
    return "\n".join(parts)


def check_answer(answer):
    """The answer must be a complete form. Otherwise the call failed (decision 0029, the contract)."""
    if not isinstance(answer, dict) or answer.get("status") not in ("written", "cannot_write"):
        raise CallFailed("The answer has no valid status.")
    if answer["status"] == "cannot_write":
        if not isinstance(answer.get("cannot_write_reason"), str) or not answer["cannot_write_reason"].strip():
            raise CallFailed("The answer cannot_write has no reason.")
        return
    if not isinstance(answer.get("question"), str) or not answer["question"].strip():
        raise CallFailed("The answer has no question.")
    options = answer.get("options")
    if not isinstance(options, list) or not options:
        raise CallFailed("The answer has no options.")


def give_letters(answer, slot, seed=0):
    """Decision 0029, part 4.1: code mixes the options and gives the letters. The
    model does not select them. "The seed controls the sequence": the seed of
    the plan, with the slot and the question text, so the same answer always
    gets the same letters."""
    options = [dict(o) for o in answer["options"]]
    random.Random("letters-%s-%s-%s" % (seed, slot["slot_id"], answer["question"])).shuffle(options)
    for letter, o in zip("ABCDEFGHIJ", options):
        o["letter"] = letter
    return [{k: o[k] for k in ("letter", "text", "correct", "reason") if k in o} for o in options]


class Writer:
    def __init__(self, records, model_call, seed=0, earlier=None):
        self.records = records
        self.model_call = model_call
        self.seed = seed
        self.earlier = earlier   # decision 0056: a function from a point to the earlier questions
        self.narrow = None       # decision 0066: a function from a point to True for a narrow idea

    def write(self, request):
        if self.earlier is not None:
            request = dict(request, earlier_questions=self.earlier(request["point"]))
        if self.narrow is not None:
            request = dict(request, narrow=self.narrow(request["point"]))
        answer, model = self.model_call.ask(SYSTEM, request_text(request, self.records), SCHEMA)
        check_answer(answer)
        out = {"status": answer["status"], "model": model,
               "cannot_write_reason": answer.get("cannot_write_reason")}
        if answer["status"] == "written":
            out["question"] = answer["question"]
            out["options"] = give_letters(answer, request["slot"], self.seed)
        return out
