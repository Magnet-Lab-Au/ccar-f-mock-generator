"""The control of the pipeline (decision 0038).

The control decides what happens next to a slot and to a mock. It does not
do the work of a step. It calls each step through one object, `steps`:

    steps.plan(mock, seed)                 step 1, returns the plan
    steps.write(request)                   steps 2 and 5, returns the answer of the writer
    steps.check_code(question, slot)       step 3, returns a verdict
    steps.check_model(question, slot)      step 4, returns a verdict
    steps.check_scenario(scenario, qs)     step 6, returns the results of one scenario
    steps.make_marking_file(round, qs)     step 7, makes the file that the owner fills
    steps.read_marking_file(round)         step 7, returns the marks of the owner
    steps.build(plan, questions)           step 8, builds the two files

A step that calls a model raises CallFailed when the call fails. The control
runs the call again, at most 3 times (decision 0037, item 10).

In the tests, `steps` is a fake. No test makes a model call.

The control calculates the status of each slot and the state of the mock
from the records each time. No file stores them (decision 0037, item 2).
"""
import datetime
import hashlib
import json
import os
import random

CALL_RUNS = 3          # runs of a call that fails (decision 0037, item 10). A guess.
TRIES = 3              # tries for one slot (decision 0033). A guess.
CANNOT_DECIDE = 2      # "cannot decide" results that stop a slot (decision 0023)
MARKS_LATER_MOCK = 20  # the sample of a later mock (decision 0022)
STOP_MOCK_1 = 7        # bad marks of 60 that stop mock 1 (decision 0035): more than 6
STOP_LATER_MOCK = 2    # bad marks of 20 that stop a later mock (decision 0035)


class CallFailed(Exception):
    """A step that calls a model raises this when the call fails."""


class Refused(Exception):
    """The control refuses a command of the owner. The message names the cause."""


def fingerprint(question):
    """SHA-256 of what a participant sees (decision 0036).

    The fields are written as JSON with sorted keys, in UTF-8 (decision 0039).
    """
    options = question.get("options") if isinstance(question.get("options"), list) else []
    data = {
        "question_id": question.get("question_id"),
        "question": question.get("question"),
        "select": question.get("select"),
        "options": [[o.get("letter"), o.get("text"), o.get("correct"), o.get("reason")]
                    if isinstance(o, dict) else [None, o, None, None] for o in options],
    }
    text = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Control:
    def __init__(self, folder, mock, seed, steps, guide_points, today=None):
        """folder: the run folder, for example runs/mock-01.
        guide_points: for each task statement ID, the list of its point IDs."""
        self.folder = folder
        self.mock = mock
        self.prefix = "M%d" % mock
        self.seed = seed
        self.steps = steps
        self.guide_points = guide_points
        self.today = today or (lambda: datetime.date.today().isoformat())
        self.run_number = None

    # ----- files -----

    def _path(self, *parts):
        return os.path.join(self.folder, *parts)

    def _read(self, *parts):
        with open(self._path(*parts), encoding="utf-8") as f:
            return json.load(f)

    def _exists(self, *parts):
        return os.path.exists(self._path(*parts))

    def _write_new(self, data, *parts):
        """Write a record. A record is never written over."""
        path = self._path(*parts)
        if os.path.exists(path):
            raise RuntimeError("The record exists already: " + path)
        self._write(path, data)

    def _write(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _list(self, folder):
        path = self._path(folder)
        if not os.path.isdir(path):
            return []
        return sorted(os.listdir(path))

    # ----- the records -----

    def plan(self):
        return self._read("plan.json")

    def slots(self):
        return self.plan()["slots"]

    def decisions(self):
        if not self._exists("owner-decisions.json"):
            return []
        return self._read("owner-decisions.json")

    def tries(self, slot_id):
        """The question records of one slot, in the sequence of their try numbers."""
        records = [self._read("questions", name) for name in self._list("questions")
                   if name.startswith(slot_id + "-T")]
        return sorted(records, key=lambda r: r["try"])

    def verdict(self, question_id, step):
        name = "%s-step%d.json" % (question_id, step)
        if not self._exists("checks", name):
            return None
        return self._read("checks", name)

    def step6_records(self, scenario):
        start = "%s-scenario-%s-step6-run" % (self.prefix, scenario)
        records = [self._read("checks", n) for n in self._list("checks") if n.startswith(start)]
        return sorted(records, key=lambda r: r["run"])

    def marking_rounds(self):
        rounds = [self._read("marking-rounds", n) for n in self._list("marking-rounds")]
        return sorted(rounds, key=lambda r: r["round"])

    def marks(self):
        result = []
        for name in self._list("marks"):
            result.extend(self._read("marks", name))
        return result

    def errors(self):
        return [self._read("errors", n) for n in self._list("errors")]

    # ----- the status of a slot -----

    def send_backs(self, slot_id):
        """Each event that gives the slot a new start: 3 new tries, and the count of
        "cannot decide" at zero (decisions 0033 and 0037, item 7).

        `after_try` is the try number when the event happened. Each try with a
        higher number belongs to the new start."""
        events = []
        for d in self.decisions():
            if d["action"] in ("new_point", "more_tries") and d["target"] == slot_id:
                events.append({"kind": d["action"], "after_try": d["after_try"],
                               "decision": d})
            if d["action"] == "rewrite" and d["question_id"].startswith(slot_id + "-T"):
                events.append({"kind": "rewrite", "after_try": d["after_try"], "decision": d})
        for m in self.marks():
            if m["mark"] == "bad" and m["question_id"].startswith(slot_id + "-T"):
                events.append({"kind": "bad_mark", "after_try": m["try"], "mark": m})
        return sorted(events, key=lambda e: e["after_try"])

    def point_of(self, slot):
        """The point of a slot: the point of the plan, or the last point of `new_point`."""
        point = slot["point"]
        for d in self.decisions():
            if d["action"] == "new_point" and d["target"] == slot["slot_id"]:
                point = d["point"]
        return point

    def slot_state(self, slot):
        """Returns the status of the slot and the facts that decide it."""
        slot_id = slot["slot_id"]
        tries = self.tries(slot_id)
        events = self.send_backs(slot_id)
        start = events[-1]["after_try"] if events else 0
        in_round = [t for t in tries if t["try"] > start]
        state = {"slot_id": slot_id, "tries": len(tries), "open_reasons": [],
                 "question_id": tries[-1]["question_id"] if tries else None,
                 "last_event": events[-1] if events else None, "in_round": in_round}
        if not in_round:
            state["status"] = "to_write"
            return state
        current = in_round[-1]
        if current["status"] == "cannot_write":
            state["status"] = "open"
            state["open_reasons"] = ["cannot_write"]
            return state
        v3 = self.verdict(current["question_id"], 3)
        v4 = self.verdict(current["question_id"], 4)
        if v3 is None or (v3["verdict"] == "pass" and v4 is None):
            state["status"] = "to_check"
            return state
        if v3["verdict"] == "pass" and v4["verdict"] == "pass":
            state["status"] = "passed"
            return state
        # The current try failed. Check the two limits (decision 0037, item 6).
        cannot_decide = 0
        for t in in_round:
            v = self.verdict(t["question_id"], 4)
            if v is not None and v["verdict"] == "cannot_decide":
                cannot_decide += 1
        if len(in_round) >= TRIES:
            state["open_reasons"].append("three_tries")
        if cannot_decide >= CANNOT_DECIDE:
            state["open_reasons"].append("cannot_decide_twice")
        state["status"] = "open" if state["open_reasons"] else "to_write"
        return state

    # ----- the request of the writer -----

    def request_for(self, slot, state):
        """Step 2 or step 5, and which try the writer sees."""
        request = {"slot": slot, "point": self.point_of(slot), "step": 2,
                   "shown_try": None, "failed_question": None, "findings": [],
                   "other_questions": []}
        in_round = state["in_round"]
        event = state["last_event"]
        if in_round:
            # A try of this start failed: step 5 shows that try (decision 0033, item 4).
            failed = in_round[-1]
            return self._step5(request, failed, self._check_findings(failed))
        if event is None:
            return request
        if event["kind"] == "new_point":
            return request
        if event["kind"] == "bad_mark":
            q = self._question(event["mark"]["question_id"])
            finding = {"step": 7, "rule": "owner", "detail": event["mark"]["reason"],
                       "letter": None, "point": None, "other_questions": []}
            return self._step5(request, q, [finding])
        if event["kind"] == "rewrite":
            d = event["decision"]
            q = self._question(d["question_id"])
            f = self._step6_finding(d["target"])
            others = [i for i in f["question_ids"] if i != d["question_id"]]
            finding = {"step": 6, "rule": f["rule"], "detail": f["detail"],
                       "letter": None, "point": None, "other_questions": others}
            owner = {"step": 7, "rule": "owner", "detail": d["reason"],
                     "letter": None, "point": None, "other_questions": []}
            request = self._step5(request, q, [finding, owner])
            request["other_questions"] = [self._question(i) for i in others]
            return request
        # more_tries: the last try before the decision.
        tries = self.tries(slot["slot_id"])
        last = tries[-1]
        if last["status"] == "cannot_write":
            return request
        return self._step5(request, last, self._check_findings(last))

    def _step5(self, request, question, findings):
        request.update({"step": 5, "shown_try": question["question_id"],
                        "failed_question": question, "findings": findings})
        return request

    def _check_findings(self, question):
        findings = []
        for step in (3, 4):
            v = self.verdict(question["question_id"], step)
            if v is not None:
                findings.extend(v["findings"])
        return findings

    def _question(self, question_id):
        return self._read("questions", question_id + ".json")

    def _step6_finding(self, finding_id):
        for scenario in self.plan()["scenarios"]:
            for record in self.step6_records(scenario):
                for f in record["findings"]:
                    if f["id"] == finding_id:
                        return f
        return None

    # ----- the automatic work -----

    def _call(self, kind, target, function, *args):
        """Run a call. Run it again when it fails, at most CALL_RUNS times.
        After that, save an error record and return None."""
        cause = None
        for _ in range(CALL_RUNS):
            try:
                return function(*args)
            except CallFailed as e:
                cause = str(e)
        n = len(self._list("errors")) + 1
        self._write_new({"id": "E%03d" % n, "run": self.run_number, "step": kind,
                         "target": target, "cause": cause, "date": self.today()},
                        "errors", "E%03d.json" % n)
        return None

    def _start_run(self):
        n = len(self._list("runs")) + 1
        self.run_number = n
        self._write_new({"run": n, "date": self.today()}, "runs", "run-%03d.json" % n)

    def run(self):
        """One run of the program. It does the automatic work, then it stops
        and writes the report."""
        if not self._exists("plan.json"):
            plan = self.steps.plan(self.mock, self.seed)
            self._write_new(plan, "plan.json")
        if self.state()["state"] in ("stopped", "built"):
            return self.report()
        self._start_run()
        for slot in self.slots():
            self._work_on_slot(slot)
        if all(self.slot_state(s)["status"] == "passed" for s in self.slots()):
            for scenario in self.plan()["scenarios"]:
                if self._step6_needed(scenario):
                    self._run_step6(scenario)
            self._make_marking_round()
        return self.report()

    def _failed_this_run(self, target):
        return any(e["target"] == target and e["run"] == self.run_number for e in self.errors())

    def _work_on_slot(self, slot):
        while True:
            state = self.slot_state(slot)
            status = state["status"]
            if status in ("passed", "open"):
                return
            if status == "to_write":
                if self._failed_this_run(slot["slot_id"]):
                    return
                request = self.request_for(slot, state)
                answer = self._call("write", slot["slot_id"], self.steps.write, request)
                if answer is None:
                    return
                self._save_try(slot, request, answer, state)
            else:
                question = self._question(state["question_id"])
                if self._failed_this_run(question["question_id"]):
                    return
                if self.verdict(question["question_id"], 3) is None:
                    v = self.steps.check_code(question, slot)
                    self._save_verdict(question, 3, v)
                else:
                    v = self._call("check_model", question["question_id"],
                                   self.steps.check_model, question, slot)
                    if v is None:
                        return
                    self._save_verdict(question, 4, v)

    def _save_try(self, slot, request, answer, state):
        n = state["tries"] + 1
        qid = "%s-T%d" % (slot["slot_id"], n)
        record = {"question_id": qid, "slot_id": slot["slot_id"], "try": n,
                  "point": request["point"], "select": slot["select"],
                  "request": request["step"], "shown_try": request["shown_try"],
                  "status": answer["status"], "date": self.today()}
        if answer.get("model"):
            record["model"] = answer["model"]
        if answer["status"] == "written":
            record["question"] = answer["question"]
            record["options"] = answer["options"]
        else:
            record["cannot_write_reason"] = answer["cannot_write_reason"]
        self._write_new(record, "questions", qid + ".json")

    def _save_verdict(self, question, step, v):
        record = {"question_id": question["question_id"], "step": step,
                  "verdict": v["verdict"], "findings": v["findings"],
                  "fingerprint": fingerprint(question), "date": self.today()}
        # Step 4 adds its own fields: blind_answer, results, features, model (decision 0032).
        for key, value in v.items():
            record.setdefault(key, value)
        self._write_new(record, "checks", "%s-step%d.json" % (question["question_id"], step))

    def _current_questions(self, scenario):
        result = []
        for slot in self.slots():
            if slot["scenario"] == scenario:
                result.append(self._question(self.slot_state(slot)["question_id"]))
        return result

    def _step6_current(self, scenario):
        """The last record of step 6 for the scenario, if it checked the current questions."""
        records = self.step6_records(scenario)
        if not records:
            return None
        group = [s for s in self.slots() if s["scenario"] == scenario]
        if any(self.slot_state(s)["status"] != "passed" for s in group):
            return None
        last = records[-1]
        now = {q["question_id"]: fingerprint(q) for q in self._current_questions(scenario)}
        return last if last["fingerprints"] == now else None

    def _step6_needed(self, scenario):
        return self._step6_current(scenario) is None

    def _checked_scenario(self, scenario, questions):
        """Call step 6 and check its answer. An answer that is not valid counts as a
        call that failed, as in step 4 (decision 0032)."""
        results = self.steps.check_scenario(scenario, questions)
        ids = {q["question_id"] for q in questions}
        for r in results:
            if r["result"] == "pass":
                continue
            if not r["findings"]:
                raise CallFailed("rule %s has the result %s and no finding" % (r["rule"], r["result"]))
            for f in r["findings"]:
                unknown = [i for i in f["question_ids"] if i not in ids]
                if not f["question_ids"] or unknown:
                    raise CallFailed("a finding of rule %s names no question or an unknown "
                                     "question: %s" % (r["rule"], ", ".join(unknown)))
        return results

    def _run_step6(self, scenario):
        questions = self._current_questions(scenario)
        results = self._call("check_scenario", "scenario-%s" % scenario,
                             self._checked_scenario, scenario, questions)
        if results is None:
            return
        run = len(self.step6_records(scenario)) + 1
        findings = []
        for r in results:
            if r["result"] == "pass":
                continue
            for f in r["findings"]:
                findings.append({"id": "%s-SC%s-R%d-F%d" % (self.prefix, scenario, run,
                                                            len(findings) + 1),
                                 "rule": r["rule"], "result": r["result"],
                                 "question_ids": f["question_ids"], "detail": f["detail"]})
        record = {"mock": self.mock, "scenario": scenario, "run": run,
                  "results": results, "findings": findings,
                  "verdict": "pass" if not findings else "fail",
                  "fingerprints": {q["question_id"]: fingerprint(q) for q in questions},
                  "date": self.today()}
        self._write_new(record, "checks",
                        "%s-scenario-%s-step6-run%d.json" % (self.prefix, scenario, run))

    # ----- the marks of the owner -----

    def sample(self):
        """The slots that the owner must mark (decision 0022).
        Mock 1: all 60. A later mock: 20, 5 from each scenario, with each domain."""
        slots = self.slots()
        if self.mock == 1:
            return [s["slot_id"] for s in slots]
        rng = random.Random("%s-sample" % self.seed)
        def domain(s):
            return s["task_statement"].split(".")[0]
        domains = {domain(s) for s in slots}
        for _ in range(1000):
            chosen = []
            for scenario in self.plan()["scenarios"]:
                group = [s for s in slots if s["scenario"] == scenario]
                chosen.extend(rng.sample(group, MARKS_LATER_MOCK // 4))
            if {domain(s) for s in chosen} == domains:
                return sorted(s["slot_id"] for s in chosen)
        raise RuntimeError("No sample has each domain.")

    def to_mark(self):
        """The current questions that need a mark and have no mark yet.
        A slot needs a mark when it is in the sample, or when it was sent back."""
        marked = {(m["question_id"], m["fingerprint"]) for m in self.marks()}
        sample = set(self.sample())
        result = []
        for slot in self.slots():
            state = self.slot_state(slot)
            if state["status"] != "passed":
                continue
            sent_back = [e for e in self.send_backs(slot["slot_id"])
                         if e["kind"] in ("rewrite", "bad_mark")]
            if slot["slot_id"] not in sample and not sent_back:
                continue
            q = self._question(state["question_id"])
            if (q["question_id"], fingerprint(q)) not in marked:
                result.append(q["question_id"])
        return result

    def _open_round(self):
        rounds = self.marking_rounds()
        read = {m["round"] for m in self.marks()}
        for r in rounds:
            if r["round"] not in read:
                return r
        return None

    def _make_marking_round(self):
        if any(self._step6_needed(s) for s in self.plan()["scenarios"]):
            return
        if self._open_round() is not None:
            return
        ids = self.to_mark()
        if not ids:
            return
        n = len(self.marking_rounds()) + 1
        questions = [self._question(i) for i in ids]
        self.steps.make_marking_file(n, questions)
        self._write_new({"round": n, "question_ids": ids,
                         "fingerprints": {q["question_id"]: fingerprint(q) for q in questions},
                         "date": self.today()},
                        "marking-rounds", "round-%d.json" % n)

    def read_marks(self):
        """Command of the owner: read the marking file of the open round."""
        r = self._open_round()
        if r is None:
            raise Refused("No marking file waits for marks.")
        given = {m["question_id"]: m for m in self.steps.read_marking_file(r["round"])}
        problems = []
        for qid in r["question_ids"]:
            m = given.get(qid)
            if m is None:
                problems.append("%s: the row is missing" % qid)
            elif m.get("mark") is None:
                problems.append("%s: no mark" % qid)
            elif m.get("mark") not in ("good", "bad"):
                problems.append('%s: the mark "%s" is not good or bad' % (qid, m.get("mark")))
            elif m["mark"] == "bad" and not (m.get("reason") or "").strip():
                problems.append("%s: a bad mark has no reason" % qid)
        if problems:
            raise Refused("The marking file is not complete: " + "; ".join(problems))
        records = []
        for qid in r["question_ids"]:
            q = self._question(qid)
            records.append({"question_id": qid, "try": q["try"], "mark": given[qid]["mark"],
                            "reason": given[qid].get("reason") or "", "round": r["round"],
                            "date": self.today(), "fingerprint": r["fingerprints"][qid]})
        self._write_new(records, "marks", "round-%d.json" % r["round"])
        return self.report()

    def bad_marks_first_round(self):
        return [m for m in self.marks() if m["round"] == 1 and m["mark"] == "bad"]

    def stop_limit_reached(self):
        limit = STOP_MOCK_1 if self.mock == 1 else STOP_LATER_MOCK
        return len(self.bad_marks_first_round()) >= limit

    # ----- the decisions of the owner -----

    def marking_pending(self):
        """True when a marking file waits, or when a question needs a mark."""
        return self._open_round() is not None or bool(self.to_mark())

    def open_findings(self):
        """The findings of the last run of step 6 of each scenario that have no
        decision of the owner. A rewrite of one finding does not hide the others."""
        decided = {d["target"] for d in self.decisions() if d["action"] in ("ignore", "rewrite")}
        result = []
        for scenario in self.plan()["scenarios"]:
            records = self.step6_records(scenario)
            if not records:
                continue
            result.extend(f for f in records[-1]["findings"] if f["id"] not in decided)
        return result

    def findings_wait(self):
        """Why the owner cannot see the findings of step 6 now, or None."""
        # A slot that waits only for the new try of a rewrite of the owner does not
        # hide the other findings. The owner can decide all findings of a run together.
        def waits_for_rewrite(state):
            event = state["last_event"]
            return (state["status"] == "to_write" and not state["in_round"]
                    and event is not None and event["kind"] == "rewrite")
        busy = set()
        for slot in self.slots():
            state = self.slot_state(slot)
            if state["status"] == "passed":
                continue
            if not waits_for_rewrite(state):
                return "The program has work to do first. Start the program."
            busy.add(slot["scenario"])
        for scenario in self.plan()["scenarios"]:
            if scenario not in busy and self._step6_needed(scenario):
                return "Step 6 must check the new questions first. Start the program."
        if self.marking_pending():
            return "Mark the questions first. Then decide on the findings of step 6."
        return None

    def visible_findings(self):
        """The owner sees the findings only when the automatic work is done and no
        marking waits (decision 0038, part 4)."""
        if self.findings_wait() is not None:
            return []
        return self.open_findings()

    def decide(self, action, target, reason, question_id=None):
        """Command of the owner. Saves one decision in owner-decisions.json."""
        if self.state()["state"] in ("stopped", "built"):
            raise Refused("The mock is %s." % self.state()["state"])
        decisions = self.decisions()
        d = {"id": "D%03d" % (len(decisions) + 1), "action": action, "target": target,
             "reason": reason, "date": self.today()}
        if action in ("new_point", "more_tries"):
            slot = self._slot(target)
            state = self.slot_state(slot)
            if state["status"] != "open":
                raise Refused("The slot %s is not open." % target)
            d["after_try"] = state["tries"]
            if action == "new_point":
                d["point"] = self._select_new_point(slot, len(decisions) + 1)
        elif action in ("ignore", "rewrite"):
            wait = self.findings_wait()
            if wait is not None:
                raise Refused(wait)
            finding = next((f for f in self.open_findings() if f["id"] == target), None)
            if finding is None:
                raise Refused("The finding %s does not wait for a decision." % target)
            if action == "rewrite":
                if question_id not in finding["question_ids"]:
                    raise Refused("A rewrite names one question of the finding.")
                if not self._exists("questions", question_id + ".json"):
                    raise Refused("The question %s does not exist." % question_id)
                slot = self._slot(self._question(question_id)["slot_id"])
                state = self.slot_state(slot)
                if state["status"] != "passed" or state["question_id"] != question_id:
                    raise Refused("The question %s is not the current try of its slot."
                                  % question_id)
                d["question_id"] = question_id
                d["after_try"] = self._question(question_id)["try"]
        elif action == "new_plan":
            if target != self.prefix:
                raise Refused("The target of new_plan is the mock, %s." % self.prefix)
            if not any(self.slot_state(s)["status"] == "open" for s in self.slots()):
                raise Refused("new_plan is an action for an open slot. No slot is open.")
        else:
            raise Refused("Unknown action: %s" % action)
        if not (reason or "").strip() and action in ("rewrite",):
            raise Refused("A rewrite must have a reason.")
        decisions.append(d)
        self._write(self._path("owner-decisions.json"), decisions)
        return d

    def _slot(self, slot_id):
        for s in self.slots():
            if s["slot_id"] == slot_id:
                return s
        raise Refused("No slot %s." % slot_id)

    def _select_new_point(self, slot, n):
        """A different point of the same task statement. No other slot has it now,
        and this slot did not have it before."""
        used = {self.point_of(s) for s in self.slots()}
        used.add(slot["point"])
        used.update(d["point"] for d in self.decisions()
                    if d["action"] == "new_point" and d["target"] == slot["slot_id"])
        free = [p for p in self.guide_points[slot["task_statement"]] if p not in used]
        if not free:
            raise Refused("The task statement %s has no free point." % slot["task_statement"])
        return random.Random("%s-%s-%d" % (self.seed, slot["slot_id"], n)).choice(free)

    # ----- step 8 -----

    def build_conditions(self):
        """The conditions before step 8. Returns the list of causes that stop the build."""
        causes = []
        for slot in self.slots():
            state = self.slot_state(slot)
            if state["status"] != "passed":
                causes.append("%s: the status is %s" % (slot["slot_id"], state["status"]))
                continue
            q = self._question(state["question_id"])
            fp = fingerprint(q)
            for step in (3, 4):
                v = self.verdict(q["question_id"], step)
                if v is None or v["verdict"] != "pass" or v["fingerprint"] != fp:
                    causes.append("%s: no valid pass of step %d" % (q["question_id"], step))
        if not causes:
            for scenario in self.plan()["scenarios"]:
                if self._step6_current(scenario) is None:
                    causes.append("scenario %s: step 6 did not check the current questions"
                                  % scenario)
            for f in self.open_findings():
                causes.append("%s: the finding of step 6 has no decision" % f["id"])
            if self._open_round() is not None:
                causes.append("a marking file waits for marks")
            for qid in self.to_mark():
                causes.append("%s: no mark" % qid)
        if self.stop_limit_reached():
            causes.append("the bad marks reached the limit that stops the mock")
        errors = [e for e in self.errors() if e["run"] == self._last_run()]
        for e in errors:
            causes.append("%s: a call failed 3 times" % e["target"])
        return causes

    def accept(self, reason=""):
        """Command of the owner: accept the mock. Code checks the conditions, then step 8 builds."""
        if self.state()["state"] in ("stopped", "built"):
            raise Refused("The mock is %s." % self.state()["state"])
        causes = self.build_conditions()
        if causes:
            raise Refused("Step 8 cannot start: " + "; ".join(causes))
        questions = [self._question(self.slot_state(s)["question_id"]) for s in self.slots()]
        files = self.steps.build(self.plan(), questions)
        decisions = self.decisions()
        decisions.append({"id": "D%03d" % (len(decisions) + 1), "action": "accept",
                          "target": self.prefix, "reason": reason, "date": self.today()})
        self._write(self._path("owner-decisions.json"), decisions)
        self._write_new({"files": files, "fingerprints": {q["question_id"]: fingerprint(q)
                                                          for q in questions},
                         "date": self.today()}, "build.json")
        return self.report()

    # ----- the state of the mock, and the report -----

    def _last_run(self):
        runs = self._list("runs")
        return len(runs) if runs else None

    def state(self):
        """The state of the mock, and what it waits for."""
        if self._exists("build.json"):
            return {"state": "built", "waiting_for": []}
        if any(d["action"] == "new_plan" for d in self.decisions()):
            return {"state": "stopped", "waiting_for": ["the owner decided new_plan"]}
        if self._exists("plan.json") and self.stop_limit_reached():
            return {"state": "stopped", "waiting_for": ["too many bad marks"]}
        if not self._exists("plan.json"):
            return {"state": "in_work", "waiting_for": []}
        waiting = []
        work = False
        last_run = self._last_run()
        failed = {e["target"] for e in self.errors() if e["run"] == last_run}
        states = [self.slot_state(s) for s in self.slots()]
        for st in states:
            if st["status"] == "open":
                waiting.append("open slot %s: %s" % (st["slot_id"], ", ".join(st["open_reasons"])))
            elif st["status"] != "passed":
                if st["slot_id"] in failed or st["question_id"] in failed:
                    waiting.append("a call failed 3 times for %s: start the program again"
                                   % st["slot_id"])
                else:
                    work = True
        if all(st["status"] == "passed" for st in states):
            for scenario in self.plan()["scenarios"]:
                if self._step6_needed(scenario):
                    if "scenario-%s" % scenario in failed:
                        waiting.append("a call of step 6 failed 3 times for scenario %s: "
                                       "start the program again" % scenario)
                    else:
                        work = True
            if not work and not waiting:
                if self._open_round() is not None:
                    return {"state": "ready_to_mark",
                            "waiting_for": ["marks of round %d" % self._open_round()["round"]]}
                if self.to_mark():
                    work = True
                else:
                    for f in self.open_findings():
                        waiting.append("finding %s of step 6: ignore or rewrite" % f["id"])
                    if not waiting:
                        waiting.append("accept the mock")
        if work:
            for f in self.visible_findings():
                waiting.append("finding %s of step 6: ignore or rewrite" % f["id"])
            return {"state": "in_work", "waiting_for": waiting + ["start the program"]}
        return {"state": "waits_for_owner", "waiting_for": waiting}

    def report(self):
        """Code builds the report from the records. Nobody edits it (decision 0037, item 10)."""
        st = self.state()
        report = {"mock": self.mock, "date": self.today(), "state": st["state"],
                  "waiting_for": st["waiting_for"], "slots": [], "step6_findings": [],
                  "errors": []}
        if self._exists("plan.json"):
            for slot in self.slots():
                s = self.slot_state(slot)
                report["slots"].append({"slot_id": s["slot_id"], "status": s["status"],
                                        "question_id": s["question_id"], "tries": s["tries"],
                                        "open_reasons": s["open_reasons"]})
            report["step6_findings"] = self.visible_findings()
        if st["state"] not in ("stopped", "built"):
            last_run = self._last_run()
            report["errors"] = [e for e in self.errors() if e["run"] == last_run]
        self._write(self._path("report.json"), report)
        return report
