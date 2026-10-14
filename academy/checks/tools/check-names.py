"""Check E3 (academy/check-plan.md): two names for one thing across both tabs.
Run: python3 check-names.py <text-dir> [pairs...]. The text dir is the output of extract-text.js (both tabs).
It reports three kinds: (1) spelling forms of one word or pair of words (hyphen, space, joined),
(2) "the documentation" without the name of decision 0039 item 11, and (3) the counts of each given pair "a=b"."""
import collections, glob, os, re, sys

TEXT = sys.argv[1]
files = [f for f in glob.glob(os.path.join(TEXT, "*", "*.md")) if not f.endswith((".skim.md", ".cards.md"))]
text = {f: open(f, encoding="utf-8").read() for f in files}
# Leave out code blocks and code-like words, which have their own spelling.
plain = {f: re.sub(r"```[\s\S]*?```", " ", t) for f, t in text.items()}

forms = collections.defaultdict(collections.Counter)
for f, t in plain.items():
    words = re.findall(r"[A-Za-z][A-Za-z-]*[A-Za-z]|[A-Za-z]", t)
    low = [w.lower() for w in words]
    for i, w in enumerate(low):
        forms[w.replace("-", "")][w] += 1
        if i + 1 < len(low):
            forms[(w + low[i + 1]).replace("-", "")][w + " " + low[i + 1]] += 1
print("# E3: two names for one thing\n")
print("## 1. Spelling forms of one name\n")
for k, c in sorted(forms.items()):
    c = collections.Counter({x: n for x, n in c.items() if not x.endswith(" s")})  # "guide s" is "guide's"
    if len(c) > 1 and len(k) > 5 and any("-" in x or " " in x for x in c) and any(" " not in x for x in c):
        print("- " + ", ".join('"%s" %d' % kv for kv in c.most_common()))
print("\n## 2. \"the documentation\" without its name\n")
for f, t in sorted(plain.items()):
    for m in re.finditer(r"[^.\n]{0,60}\b[Tt]he documentation\b[^.\n]{0,40}", t):
        s = m.group(0)
        if not re.search(r"(API|Code|Anthropic|SDK|MCP) documentation", s):
            print("- %s: %s" % (os.path.relpath(f, TEXT), s.strip()))
print("\n## 3. Given pairs\n")
for pair in sys.argv[2:]:
    names = pair.split("=")
    counts = []
    for n in names:
        rx = re.compile(r"\b" + re.escape(n) + r"\b", re.I)
        where = collections.Counter(os.path.relpath(f, TEXT).split("/")[0] for f, t in plain.items() for _ in rx.finditer(t))
        counts.append('"%s" %s' % (n, dict(where) or 0))
    print("- " + " | ".join(counts))
