"""Check C3, script part (academy/check-plan.md): the rules of Simplified Technical English in the page text.
Run: python3 check-sentences.py <text-dir>. It leaves out code, the guide's own point texts (lines "- 1.1-K1 ..."),
quotes in curly quotes, popup code examples and the preview cards. It lists sentences over 25 words,
semicolons, em dashes and contractions, for each tab."""
import collections, glob, os, re, sys

TEXT = sys.argv[1]
stats = collections.Counter()
long_ = collections.defaultdict(list)
marks = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(TEXT, "*", "*.md"))):
    if f.endswith((".skim.md", ".cards.md")):
        continue
    tab = os.path.basename(os.path.dirname(f))
    part = os.path.basename(f)[:-3]
    t = open(f, encoding="utf-8").read()
    t = t.split("\n## Figure labels")[0] + "\n" + "\n".join(
        l for l in t.split("\n## Popups on the figures")[-1].split("\n") if l.startswith("- Popup")) if "## Popups on the figures" in t else t.split("\n## Figure labels")[0]
    t = re.sub(r"```[\s\S]*?```", " ", t)
    t = "\n".join(l for l in t.split("\n") if not re.match(r"^- \d\.\d-[KS]\d", l))
    t = re.sub(r"“[^”]*”", "“Q”", t)
    for para in t.split("\n"):
        para = para.strip()
        if not para or para.startswith("#"):
            continue
        for s in re.split(r"(?<=[.?!])\s+(?=[A-Z“(])", para):
            w = len(s.split())
            if w < 3:
                continue
            stats[tab, "sentences"] += 1
            if w > 25:
                stats[tab, "over 25 words"] += 1
                long_[tab].append((w, part, s))
            if ";" in s:
                marks[tab].append(("semicolon", part, s))
            if "—" in s:
                marks[tab].append(("em dash", part, s))
            if re.search(r"\b\w+n't\b|\b(it|that|there|what)'s\b|\b\w+'(re|ll|ve|d)\b", s, re.I):
                marks[tab].append(("contraction", part, s))
print("# C3, script part: sentence rules\n")
for tab in sorted({k[0] for k in stats}):
    n, o = stats[tab, "sentences"], stats[tab, "over 25 words"]
    print("## %s: %d sentences, %d over 25 words (%.1f%%)\n" % (tab, n, o, 100.0 * o / max(n, 1)))
    for w, part, s in sorted(long_[tab], reverse=True)[:25]:
        print("- %d words, %s: %s" % (w, part, s[:220]))
    for kind, part, s in marks[tab]:
        print("- %s, %s: %s" % (kind, part, s[:200]))
    print()
