"""Check for decision 0037, item 12: properties of the 12 sample questions.

The script measures the four properties that became rules A8 to A11:
A8  the text ends with a question mark
A9  the text has 2 to 5 sentences
A10 each option is one sentence
A11 the question has no "NOT" and no "EXCEPT"
It also prints the first word of each option, to show the form of the options.
The method for sentences is simple: a sentence ends with ".", "?" or "!"
and a space comes after it.
The text comes from reference/guide-records.json.
Run: python3 0037-check-sample-properties.py
"""
import json
import re
from pathlib import Path

RECORDS = Path(__file__).resolve().parents[2] / "reference" / "guide-records.json"
records = json.loads(RECORDS.read_text(encoding="utf-8"))


def sentences(text):
    return [s for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s]


totals = {"A8": 0, "A9": 0, "A10": 0, "A11": 0}
samples = records["sample_questions"]
for sample in samples:
    text = sample["question"]
    options = sample["options"]
    a8 = text.strip().endswith("?")
    count = len(sentences(text))
    a9 = 2 <= count <= 5
    a10 = all(len(sentences(o)) == 1 for o in options.values())
    a11 = not re.search(r"\b(not|except)\b", text, re.IGNORECASE)
    for rule, result in (("A8", a8), ("A9", a9), ("A10", a10), ("A11", a11)):
        totals[rule] += result
    first_words = [o.split()[0] for o in options.values()]
    print(sample["number"], "| A8", a8, "| sentences", count, "| A10", a10,
          "| A11", a11, "| first words:", first_words)
for rule, total in totals.items():
    print(rule, "true for", total, "of", len(samples))
