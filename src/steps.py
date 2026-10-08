"""The real steps for the control (decision 0039). It connects steps 1 to 8 to
the calls that the control makes. In the tests of the control, a fake takes
this place.
"""
import datetime
import json
import os

import step1_plan
import step3_check_code
import step8_build_files
from control import Refused
from model_call import ModelCall
from step2_write import Writer
from step4_check_model import ModelCheck
from step6_check_scenario import ScenarioCheck
from step7_marking import Marking, MarkingError
from earlier import Earlier

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_records(path=step1_plan.RECORDS):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guide_points(records):
    return {t["id"]: [p["id"] for p in t["points"]] for t in records["task_statements"]}


class RealSteps:
    def __init__(self, run_folder, records=None, model_call=None, marking_folder=None, mocks_folder=None, today=None):
        self.run_folder = run_folder
        self.records = records or load_records()
        self.model_call = model_call or ModelCall()
        self.marking_folder = marking_folder or os.path.join(ROOT, "marking")
        self.mocks_folder = mocks_folder or os.path.join(ROOT, "mocks")
        self.today = today or (lambda: datetime.date.today().isoformat())
        self.writer = Writer(self.records, self.model_call)
        self.checker = ModelCheck(self.records, self.model_call)

    def _plan(self):
        with open(os.path.join(self.run_folder, "plan.json"), encoding="utf-8") as f:
            return json.load(f)

    # step 1
    def plan(self, mock, seed):
        return step1_plan.make_plan(self.records, mock, seed, self.today(),
                                    earlier=step1_plan.earlier_points(self.mocks_folder, mock))

    # steps 2 and 5
    def _earlier(self):
        """Decision 0056: the questions of the built mocks before this one."""
        mock = self._plan()["mock"]
        if getattr(self, "_earlier_for", None) != mock:
            found = Earlier(self.mocks_folder, mock)
            self._earlier_of = found.on_idea
            self._narrow_of = found.narrow
            self._earlier_for = mock
        return self._earlier_of

    def write(self, request):
        self.writer.seed = self._plan()["seed"]
        self.writer.earlier = self._earlier()
        self.writer.narrow = self._narrow_of
        return self.writer.write(request)

    # step 3
    def check_code(self, question, slot):
        return step3_check_code.check(question, slot)

    # step 4
    def check_model(self, question, slot):
        self.checker.earlier = self._earlier()
        self.checker.narrow = self._narrow_of
        return self.checker.check(question, slot)

    # step 6
    def check_scenario(self, scenario, questions, others=()):
        return ScenarioCheck(self._plan(), self.model_call).check(scenario, questions, others)

    # step 7
    def make_marking_file(self, round_number, questions):
        return Marking(self._plan(), self.records, self.marking_folder).make(round_number, questions)

    def read_marking_file(self, round_number):
        try:
            return Marking(self._plan(), self.records, self.marking_folder).read(round_number)
        except MarkingError as e:
            raise Refused(str(e))

    def bad_marks_by_segment(self, marks):
        return Marking(self._plan(), self.records, self.marking_folder).bad_marks_by_segment(marks)

    # step 8
    def build(self, plan, questions):
        try:
            return step8_build_files.build(plan, questions, self.records, self.mocks_folder, self.today())
        except step8_build_files.BuildError as e:
            raise Refused(str(e))
