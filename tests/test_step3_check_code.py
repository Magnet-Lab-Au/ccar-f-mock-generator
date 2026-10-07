"""Tests of step 3, the code check (decisions 0030, 0031 and 0038, part 8). No test makes a model call.

Run from the folder ccar-f-mock-generator:
    python3 -m unittest discover tests
"""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from step3_check_code import check, sentences  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "reference", "guide-records.json"), encoding="utf-8") as f:
    RECORDS = json.load(f)

SLOT = {"slot_id": "M1-S17", "scenario": 3, "task_statement": "1.2", "point": "1.2-K2",
        "type": "multiple_choice", "options": 4, "select": 1}
GOOD = {
    "question_id": "M1-S17-T1", "select": 1,
    "question": ("A coordinator agent sends a research task to three subagents. One subagent times out "
                 "after it has collected half of its sources. The coordinator gets an empty result and "
                 "writes a report that leaves out that topic. What is the best change to the design?"),
    "options": [
        {"letter": "A", "text": "Return structured error context with the partial results to the coordinator.", "correct": True,
         "reason": "The coordinator can then decide how to recover with the facts of the failure."},
        {"letter": "B", "text": "Increase the timeout of each subagent to a much larger value.", "correct": False,
         "reason": "A longer timeout hides the failure and does not tell the coordinator about it."},
        {"letter": "C", "text": "Let the subagent return an empty list as a successful result.", "correct": False,
         "reason": "An empty result that looks like success hides the error from the coordinator."},
        {"letter": "D", "text": "Restart the complete research task each time that a subagent fails.", "correct": False,
         "reason": "A restart loses the work of the other subagents and can fail again."},
    ],
}


def sample_as_question(sample):
    """A sample question of the guide in the form of a question record, with no reasons."""
    return {"question": sample["question"], "select": len(sample["correct_answer"]),
            "options": [{"letter": k, "text": v, "correct": k in sample["correct_answer"]}
                        for k, v in sorted(sample["options"].items())]}


def rules_of(result):
    return [f["rule"] for f in result["findings"]]


class TestCheck(unittest.TestCase):
    def changed(self, change, slot=SLOT):
        q = copy.deepcopy(GOOD)
        change(q)
        return check(q, slot)

    def test_a_good_question_passes(self):
        self.assertEqual(check(GOOD, SLOT), {"verdict": "pass", "findings": []})

    def test_a1_the_form_is_complete(self):
        r = self.changed(lambda q: q["options"][1].pop("reason"))
        self.assertEqual(r["verdict"], "fail")
        self.assertIn("A1", rules_of(r))
        self.assertEqual(r["findings"][0]["letter"], "B")
        self.assertIn("A1", rules_of(self.changed(lambda q: q.update(question=""))))
        self.assertIn("A1", rules_of(self.changed(lambda q: q["options"][0].update(correct="yes"))))

    def test_a2_the_number_of_options(self):
        self.assertIn("A2", rules_of(self.changed(lambda q: q["options"].pop())))

    def test_a3_the_number_of_correct_options(self):
        self.assertIn("A3", rules_of(self.changed(lambda q: q["options"][1].update(correct=True))))

    def test_a4_no_equal_options(self):
        r = self.changed(lambda q: q["options"][3].update(text="  return STRUCTURED error context with the partial results to the coordinator. "))
        self.assertIn("A4", rules_of(r))

    def test_a5_no_text_names_a_letter_or_an_option(self):
        self.assertIn("A5", rules_of(self.changed(lambda q: q["options"][3].update(text="All of the above, because each change helps the coordinator."))))
        r = self.changed(lambda q: q["options"][1].update(reason="Option A is better than this option."))
        self.assertIn("A5", rules_of(r))
        self.assertEqual([f["letter"] for f in r["findings"] if f["rule"] == "A5"], ["B"])

    def test_a6_the_length(self):
        self.assertIn("A6", rules_of(self.changed(lambda q: q.update(question="Which change is best for the coordinator here?"))))
        self.assertIn("A6", rules_of(self.changed(lambda q: q.update(question=GOOD["question"].replace("What is", "word " * 90 + "What is")))))
        self.assertIn("A6", rules_of(self.changed(lambda q: q["options"][2].update(text="Use more retries."))))

    def test_a7_the_correct_option_is_not_much_longer(self):
        long_text = "Return structured error context with the partial results, the failure type and the query that was attempted to the coordinator."
        self.assertIn("A7", rules_of(self.changed(lambda q: q["options"][0].update(text=long_text))))

    def test_a8_a_question_mark_at_the_end(self):
        self.assertIn("A8", rules_of(self.changed(lambda q: q.update(question=GOOD["question"].replace("design?", "design. Select the best change.")))))

    def test_a9_two_to_five_sentences(self):
        one = ("A coordinator agent sends a research task to three subagents and one subagent times out after it has "
               "collected half of its sources so what is the best change to the design of the system?")
        self.assertIn("A9", rules_of(self.changed(lambda q: q.update(question=one))))
        six = "One fact. Two facts. Three facts. Four facts. Five facts are here now. " + GOOD["question"]
        self.assertIn("A9", rules_of(self.changed(lambda q: q.update(question=six))))

    def test_a10_each_option_is_one_sentence(self):
        r = self.changed(lambda q: q["options"][1].update(text="Increase the timeout of each subagent. Then wait longer."))
        self.assertEqual([f["letter"] for f in r["findings"] if f["rule"] == "A10"], ["B"])

    def test_a11_capital_not_or_except_fails(self):
        self.assertIn("A11", rules_of(self.changed(lambda q: q.update(question=GOOD["question"].replace("What is the best", "Which is NOT a good")))))
        self.assertIn("A11", rules_of(self.changed(lambda q: q.update(question=GOOD["question"].replace("leaves out that topic.", "leaves out EXCEPT one topic.")))))

    def test_a11_small_not_in_the_last_sentence_fails(self):
        self.assertIn("A11", rules_of(self.changed(lambda q: q.update(question=GOOD["question"].replace("What is the best change", "Which change does not help")))))

    def test_a11_small_not_outside_the_last_sentence_passes(self):
        r = self.changed(lambda q: q.update(question=GOOD["question"].replace("leaves out that topic.", "does not include that topic.")))
        self.assertNotIn("A11", rules_of(r))

    def test_a1_the_letters_a_to_d_in_sequence(self):
        self.assertIn("A1", rules_of(self.changed(lambda q: q["options"][2].update(letter="A"))))
        self.assertIn("A1", rules_of(self.changed(lambda q: q["options"][2].pop("letter"))))

    def test_a1_an_option_that_is_not_a_record(self):
        r = self.changed(lambda q: q["options"].__setitem__(1, "Increase the timeout of each subagent."))
        self.assertIn("A1", rules_of(r))

    def test_a1_a_record_that_is_not_a_question(self):
        self.assertEqual(rules_of(check("not a record", SLOT))[0], "A1")

    def test_a5_a_small_letter_is_not_an_option(self):
        r = self.changed(lambda q: q["options"][1].update(text="Increase the timeout that the option a reviewer prefers here."))
        self.assertNotIn("A5", rules_of(r))

    def test_a9_the_limits_5_and_6(self):
        five = "One fact. Two facts. Three facts are here. Four facts. " + GOOD["question"].split(". ")[-1]
        self.assertNotIn("A9", rules_of(self.changed(lambda q: q.update(question=five))))
        six = "Zero facts. " + five
        self.assertIn("A9", rules_of(self.changed(lambda q: q.update(question=six))))

    def test_a11_the_options_do_not_count(self):
        r = self.changed(lambda q: q["options"][1].update(text="Do not change the design, and increase the timeout of each subagent."))
        self.assertNotIn("A11", rules_of(r))


class TestMultipleResponse(unittest.TestCase):
    def test_five_options_and_two_correct_pass(self):
        q = copy.deepcopy(GOOD)
        q["select"] = 2
        q["options"].append({"letter": "E", "text": "Let the coordinator ask the subagent again for the missing sources.",
                             "correct": True, "reason": "The coordinator can then fill the gap with the help of the subagent."})
        slot = dict(SLOT, type="multiple_response", options=5, select=2)
        self.assertEqual(check(q, slot)["verdict"], "pass")
        self.assertIn("A3", rules_of(check(q, SLOT)))


class TestSampleQuestions(unittest.TestCase):
    """Decision 0024: step 3 checks the 12 sample questions with the rules that need
    no slot and no reason for each option, A4 to A11."""

    def test_the_12_sample_questions_pass_a4_to_a11(self):
        rules = {"A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"}
        for sample in RECORDS["sample_questions"]:
            q = sample_as_question(sample)
            self.assertEqual(sum(o["correct"] for o in q["options"]), 1)
            r = check(q, None, rules=rules)
            self.assertEqual(r["findings"], [], "sample question %s" % sample["number"])

    def test_a7_runs_on_a_sample_question(self):
        # The sample questions have no reason for each option. A7 must still run.
        q = sample_as_question(RECORDS["sample_questions"][0])
        right = [o for o in q["options"] if o["correct"]][0]
        right["text"] = " ".join(["word"] * 40) + "."
        self.assertIn("A7", rules_of(check(q, None, rules={"A7"})))

    def test_a5_runs_on_a_sample_option_with_no_reason(self):
        q = sample_as_question(RECORDS["sample_questions"][0])
        q["options"][3]["text"] = "All of the above."
        self.assertIn("A5", rules_of(check(q, None, rules={"A5"})))

    def test_the_known_limit_of_the_sentence_method(self):
        # Decision 0031: a dot and then a quote mark does not end a sentence.
        q7 = [s for s in RECORDS["sample_questions"] if s["number"] == 7][0]
        self.assertEqual(len(sentences(q7["question"])), 3)


if __name__ == "__main__":
    unittest.main()
