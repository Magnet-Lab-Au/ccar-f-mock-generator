"""The questions of the earlier mocks on the same idea (decision 0056).

A mock is earlier when it has a lower number and is built: its files
mocks/mock-NN.questions.json and mocks/mock-NN.answers.json exist. The idea of
a question is the group of its point (decision 0047). The writer of step 2 and
call 4b of step 4 get these questions, so that a later mock does not repeat
the same question.
"""
import json
import os

import point_groups


NARROW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "narrow-ideas.json")


class EarlierError(Exception):
    """A built mock file cannot be read."""


class Earlier:
    def __init__(self, mocks_folder, mock, groups=None, narrow_path=NARROW):
        groups = groups or point_groups.load()
        self.of = point_groups.group_of(groups)
        # Decision 0066: the ideas with almost only one problem keep the copy rule.
        self.narrow_groups = set()
        if narrow_path and os.path.exists(narrow_path):
            with open(narrow_path, encoding="utf-8") as f:
                self.narrow_groups = {g["id"] for g in json.load(f)["groups"]}
        self.questions = []
        for n in range(1, mock):
            qpath = os.path.join(mocks_folder, "mock-%02d.questions.json" % n)
            apath = os.path.join(mocks_folder, "mock-%02d.answers.json" % n)
            if not os.path.exists(qpath):
                continue
            try:
                with open(qpath, encoding="utf-8") as f:
                    built = json.load(f)
                with open(apath, encoding="utf-8") as f:
                    answers = {a["question_id"]: a["correct"] for a in json.load(f)["answers"]}
                for g in built["groups"]:
                    for q in g["questions"]:
                        right = answers[q["question_id"]]
                        self.questions.append({
                            "question_id": q["question_id"], "point": q["point"], "question": q["question"],
                            "options": [{"text": o["text"], "correct": o["letter"] in right} for o in q["options"]]})
            except (OSError, ValueError, KeyError, TypeError) as e:
                raise EarlierError("The built mock %d cannot be read: %s" % (n, e))

    def narrow(self, point):
        """True if the idea of this point has almost only one problem (decision 0066)."""
        return self.of[point]["id"] in self.narrow_groups

    def on_idea(self, point):
        """The earlier questions whose point is in the group of this point."""
        group = self.of[point]["id"]
        return [q for q in self.questions if self.of[q["point"]]["id"] == group]
