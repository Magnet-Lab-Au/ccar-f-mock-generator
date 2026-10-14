"""Check A2 (academy/check-plan.md): computes each number of tab 2 again from its source.
Run: python3 check-numbers.py <numbers.json> <text-dir of tab 2>
An agent wrote numbers.json: part, text, value, expr (Python, or null), source. This script runs each expr,
compares the result with the value, and checks that the value appears in the text of its part."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
items = json.load(open(sys.argv[1]))
text = {os.path.basename(f)[:-3]: open(f).read() for f in glob.glob(os.path.join(sys.argv[2], "*.md")) if f.count(".") == 1}
cards = {os.path.basename(f)[:-9]: open(f).read() for f in glob.glob(os.path.join(sys.argv[2], "*.cards.md"))}
same = diff = none = 0
out = []
for x in items:
    shown = str(x["value"])
    where = text.get(x["part"], "") + cards.get(x["part"], "")
    flat = re.sub(r"[\s,]", "", where)
    on_page = all(re.sub(r"[\s,]", "", str(v)) in flat for v in (x["value"] if isinstance(x["value"], list) else [x["value"]]))
    if not x.get("expr"):
        none += 1
        out.append("- text only: %s, \"%s\", source %s%s" % (x["part"], x["text"][:80], x["source"], "" if on_page else ", VALUE NOT FOUND IN THE PART"))
        continue
    try:
        got = eval(x["expr"], {"ROOT": ROOT, "json": json, "glob": glob, "os": os, "re": re, "__builtins__": __builtins__})
    except Exception as e:
        got = "error " + type(e).__name__
    if got == x["value"] or str(got) == shown:
        same += 1
        if not on_page:
            out.append("- value not found in the part: %s, \"%s\" (%s)" % (x["part"], x["text"][:80], shown))
    else:
        diff += 1
        out.append("- DIFFERENT: %s, \"%s\": page %s, source %s" % (x["part"], x["text"][:80], shown, got))
print("# A2: the numbers of tab 2\n")
print("Numbers: %d. Computed again and the same: %d. Different: %d. From a text record only: %d.\n" % (len(items), same, diff, none))
print("\n".join(out))
