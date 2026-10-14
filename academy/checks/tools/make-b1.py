"""Makes the files of check B1 (academy/check-plan.md): the mock questions of each domain, without
point, task statement or answer, and the tab 1 text of that domain. Questions that a tab shows are left out:
by ID, by question text or by option text. Run: python3 make-b1.py <text-dir> <out-dir>
The text dir is the output of extract-text.js. Prints the counts, and writes left-out.json with the reasons."""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TEXT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = s.replace("\\\"", '"').replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


tabs = ""
for f in ["exam-guide-breakdown.html", "exam-guide-breakdown.js", "behind-the-mocks.html", "behind-the-mocks.js"]:
    tabs += " " + norm(open(os.path.join(ROOT, "academy", "pages", f), encoding="utf-8").read())

left_out, keep = {}, {d: [] for d in "12345"}
for f in sorted(glob.glob(os.path.join(ROOT, "mocks", "mock-*.questions.json"))):
    for g in json.load(open(f, encoding="utf-8"))["groups"]:
        for q in g["questions"]:
            why = []
            if q["question_id"].lower() in tabs:
                why.append("ID")
            if norm(q["question"])[:120] in tabs:
                why.append("question text")
            for o in q["options"]:
                t = norm(o["text"])
                if len(t) >= 30 and t[:100] in tabs:
                    why.append("option " + o["letter"])
            if why:
                left_out[q["question_id"]] = why
                continue
            keep[str(q["domain"])].append((g, q))

for d, items in keep.items():
    out = ["# The questions of domain %s" % d, "",
           "Answer each question. Give the letter or letters, and quote one sentence of the page that supports the answer.", ""]
    last = None
    for g, q in items:
        if g["name"] + g["story"] != last:
            out += ["## Scenario: %s" % g["name"], "", g["story"], ""]
            last = g["name"] + g["story"]
        out += ["### %s (select %s)" % (q["question_id"], q["select"]), "", q["question"], ""]
        out += ["- %s. %s" % (o["letter"], o["text"]) for o in q["options"]] + [""]
    open(os.path.join(OUT, "domain-%s.questions.md" % d), "w", encoding="utf-8").write("\n".join(out))
    files = ["map.md", "breakdown.md", "domain-%s.md" % d] + sorted(os.path.basename(x) for x in glob.glob(os.path.join(TEXT, "ts-%s-*.md" % d)) if not x.endswith(".skim.md"))
    page = []
    for x in files:
        p = os.path.join(TEXT, x)
        if os.path.exists(p):
            page.append(open(p, encoding="utf-8").read())
    open(os.path.join(OUT, "domain-%s.page.md" % d), "w", encoding="utf-8").write("\n\n---\n\n".join(page))
    print("domain %s: %d questions, page %d words" % (d, len(items), sum(len(x.split()) for x in page)))
json.dump(left_out, open(os.path.join(OUT, "left-out.json"), "w"), indent=1)
print("left out: %d" % len(left_out), sorted(left_out.items())[:30])
