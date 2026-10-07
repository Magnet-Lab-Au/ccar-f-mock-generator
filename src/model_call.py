"""One model call with a fixed form (decisions 0029, 0032, 0034 and 0040).

The request carries the form as a JSON schema in `output_config.format`
(structured outputs, decision 0040). The code reads the drafts of the forms
from docs/diagrams/, so that the decisions and the code use one copy.

A call that fails raises CallFailed. The control runs the call again, at most
3 times (decision 0037, item 10). The tests give a fake client. No test makes
a model call.
"""
import copy
import json
import os

from control import CallFailed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMS = os.path.join(ROOT, "docs", "diagrams")

# The model and the effort are settings. The test of decision 0024 decides them.
# These are first values, not decisions.
MODEL = "claude-opus-5-5"
EFFORT = "high"
MAX_TOKENS = 16000


def strict(schema):
    """Add "additionalProperties": false to each object of a schema. The
    documentation of structured outputs requires it (decision 0040)."""
    schema = copy.deepcopy(schema)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "object" or (isinstance(node.get("type"), list) and "object" in node["type"]):
                node["additionalProperties"] = False
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk(schema)
    return schema


def load_form(file_name, key=None):
    """Return (description, schema) of a draft form."""
    with open(os.path.join(FORMS, file_name), encoding="utf-8") as f:
        data = json.load(f)
    if key is not None:
        data = data[key]
    return data["description"], strict(data["input_schema"])


def default_client():
    """The Anthropic client. It reads the key from the environment, never from
    a file of the repository (CLAUDE.md)."""
    import anthropic
    return anthropic.Anthropic()


class ModelCall:
    def __init__(self, client=None, model=MODEL, effort=EFFORT, max_tokens=MAX_TOKENS):
        self._client = client
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens

    @property
    def client(self):
        if self._client is None:
            self._client = default_client()
        return self._client

    def ask(self, system, text, schema):
        """Send one request. Return (answer as a dict, the model that answered)."""
        try:
            response = self.client.messages.create(
                model=self.model, max_tokens=self.max_tokens, system=system,
                messages=[{"role": "user", "content": text}],
                output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}})
        except Exception as e:   # each API or network error: the control runs the call again
            raise CallFailed("%s: %s" % (type(e).__name__, e))
        stop = getattr(response, "stop_reason", None)
        if stop == "refusal":
            details = getattr(response, "stop_details", None)
            raise CallFailed("The model declined the request (refusal, %s)." % getattr(details, "category", None))
        if stop == "max_tokens":
            raise CallFailed("The answer reached max_tokens and is not complete.")
        texts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
        if not texts:
            raise CallFailed("The answer has no text block.")
        try:
            answer = json.loads(texts[0])
        except ValueError as e:
            raise CallFailed("The answer is not valid JSON: %s" % e)
        return answer, getattr(response, "model", self.model)
