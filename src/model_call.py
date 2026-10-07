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

from control import CallFailed, RunStopped

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMS = os.path.join(ROOT, "docs", "diagrams")

# The model and the effort are settings. The test of decision 0024 decides them.
# These are first values, not decisions.
MODEL = "claude-opus-5-5"
EFFORT = "high"
# Thinking is always on in Claude Opus 5.5, and its tokens count toward
# max_tokens. The calls stream, so a high limit causes no HTTP timeout.
MAX_TOKENS = 64000

# The errors that a new call can repair (the Claude API skill, shared/error-codes.md):
# 429, 5xx and network errors. Each other error stops the run.
RETRYABLE = {"RateLimitError", "InternalServerError", "APIConnectionError", "APITimeoutError"}


def classify(error):
    names = {c.__name__ for c in type(error).__mro__}
    if names & RETRYABLE or (getattr(error, "status_code", 0) or 0) >= 500:
        return CallFailed("%s: %s" % (type(error).__name__, error))
    return RunStopped("%s: %s" % (type(error).__name__, error))


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
    try:
        import anthropic
    except ImportError:
        raise RunStopped("The package anthropic is not installed. Install it with: pip install anthropic")
    return anthropic.Anthropic()


class ModelCall:
    def __init__(self, client=None, model=MODEL, effort=EFFORT, max_tokens=MAX_TOKENS):
        self._client = client
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.usage = []   # one entry for each answer: input and output tokens

    @property
    def client(self):
        if self._client is None:
            self._client = default_client()
        return self._client

    def ask(self, system, text, schema):
        """Send one request. Return (answer as a dict, the model that answered)."""
        try:
            with self.client.messages.stream(
                    model=self.model, max_tokens=self.max_tokens, system=system,
                    messages=[{"role": "user", "content": text}],
                    output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}}) as stream:
                response = stream.get_final_message()
        except (CallFailed, RunStopped):
            raise
        except Exception as e:
            raise classify(e)
        u = getattr(response, "usage", None)
        if u is not None:
            self.usage.append({"input": getattr(u, "input_tokens", 0) or 0, "output": getattr(u, "output_tokens", 0) or 0})
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
        return lower_enums(answer), getattr(response, "model", self.model)


SMALL = ("status", "result")          # values like "pass" and "cannot_decide"
CAPITAL = ("rule", "letter", "selected")   # values like "B1" and "C"


def lower_enums(answer):
    """The page "Structured outputs", section "Invalid outputs", says: "Structured
    outputs don't guarantee the capitalization of string enum and const values".
    So code writes each enum value in one fixed form before it compares."""
    def fix(key, value):
        if isinstance(value, str) and key in SMALL:
            return value.lower()
        if isinstance(value, str) and key in CAPITAL:
            return value.upper()
        if isinstance(value, list) and key in CAPITAL:
            return [v.upper() if isinstance(v, str) else v for v in value]
        return lower_enums(value)
    if isinstance(answer, dict):
        return {k: fix(k, v) for k, v in answer.items()}
    if isinstance(answer, list):
        return [lower_enums(v) for v in answer]
    return answer
