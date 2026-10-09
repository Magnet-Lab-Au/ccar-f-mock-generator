"""The test of prompt caching before mock 4 (decision 0067).

Calls 4a and 4b check 10 questions of the built mock 3 again, in the new order
of the request (the cached guide block first). The script compares each new
verdict with the stored verdict of mock 3, and saves the tokens, the cached
tokens and the cost. It changes no record of mock 3.

For a fair comparison, call 4b uses the text of rule B9 that checked mock 3
(decision 0056), not the stricter text of decision 0066.

Run from the folder ccar-f-mock-generator (the API key comes from the environment):
    python3 src/test_cache.py
It writes runs/test-cache/results.json.
"""
import json
import os
import sys

import step4_check_model
from earlier import Earlier
from model_call import ModelCall, cost
from step4_check_model import ModelCheck
from steps import ROOT, load_records
from step2_write import B9_STRICT
from test_b9 import mock3_questions

FOLDER = os.path.join(ROOT, "runs", "test-cache")
OLD_B9 = ("B9. The question is not a repeat of an earlier question on the same idea: not the same scene with the same "
          "answer, and no wrong option of an earlier question.")


def stored_verdict(question_id):
    with open(os.path.join(ROOT, "runs", "mock-03", "checks", question_id + "-step4.json"), encoding="utf-8") as f:
        return json.load(f)


def main():
    step4_check_model.RULES_TEXT = step4_check_model.RULES_TEXT.replace(B9_STRICT, OLD_B9)
    records = load_records()
    call = ModelCall()
    check = ModelCheck(records, call, earlier=Earlier(os.path.join(ROOT, "mocks"), 3).on_idea)
    chosen = mock3_questions()[::6]
    results = []
    for question, slot in chosen:
        before = stored_verdict(question["question_id"])
        n = len(call.usage)
        after = check.check(question, slot)
        entry = {"question_id": question["question_id"], "stored": before["verdict"], "new": after["verdict"],
                 "stored_findings": [f["rule"] for f in before.get("findings", [])],
                 "new_findings": [{"rule": f["rule"], "detail": f["detail"]} for f in after["findings"]],
                 "usage": call.usage[n:]}
        results.append(entry)
        print(entry["question_id"], entry["stored"], "->", entry["new"], entry["usage"], flush=True)
    os.makedirs(FOLDER, exist_ok=True)
    data = {"decision": "0067", "mock": 3, "results": results, "cost": cost(call.usage)}
    with open(os.path.join(FOLDER, "results.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    changed = [r for r in results if r["stored"] != r["new"]]
    print("Changed verdicts: %d of %d. Cost: $%.2f. Cache reads: %d tokens. Cache writes: %d tokens."
          % (len(changed), len(results), data["cost"]["dollars"], data["cost"]["cache_read_tokens"],
             data["cost"]["cache_write_tokens"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
