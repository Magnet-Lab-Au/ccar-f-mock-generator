"""Check for decision 0031: the limits of rules A5, A6 and A7 against the 12 sample questions.

It reads reference/guide-records.json. It prints the lengths of each sample
question and says if each one passes the limits.
Run: python3 0031-check-sample-lengths.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "..", "reference", "guide-records.json"), encoding="utf-8") as f:
    QUESTIONS = json.load(f)["sample_questions"]

QUESTION_WORDS = (25, 110)   # rule A6
OPTION_WORDS = (5, 45)       # rule A6
CORRECT_RATIO = 1.3          # rule A7
LETTER_WORDS = re.compile(r"\b(option [A-E]\b|all of the above|none of the above|both [A-E] and [A-E])", re.I)  # rule A5


def words(text):
    return len(text.split())


all_pass = True
q_lengths, o_lengths, ratios = [], [], []
for q in QUESTIONS:
    correct = [words(v) for k, v in q["options"].items() if k in q["correct_answer"]]
    wrong = [words(v) for k, v in q["options"].items() if k not in q["correct_answer"]]
    ratio = (sum(correct) / len(correct)) / (sum(wrong) / len(wrong))
    q_lengths.append(words(q["question"]))
    o_lengths += correct + wrong
    ratios.append(ratio)
    ok = (QUESTION_WORDS[0] <= words(q["question"]) <= QUESTION_WORDS[1]
          and all(OPTION_WORDS[0] <= n <= OPTION_WORDS[1] for n in correct + wrong)
          and ratio <= CORRECT_RATIO
          and not LETTER_WORDS.search(q["question"] + " " + " ".join(q["options"].values())))
    all_pass = all_pass and ok
    print("sample question %2d: question %2d words, correct %s, wrong %s, ratio %.2f  %s"
          % (q["number"], words(q["question"]), correct, wrong, ratio, "PASS" if ok else "FAIL"))
print("question words: %d to %d" % (min(q_lengths), max(q_lengths)))
print("option words: %d to %d" % (min(o_lengths), max(o_lengths)))
print("largest ratio: %.2f" % max(ratios))
print("all 12 pass" if all_pass else "NOT all pass")
