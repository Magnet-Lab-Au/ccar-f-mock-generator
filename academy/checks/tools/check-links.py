"""Check A1 (academy/check-plan.md): tests each external link of both tabs.
Run: python3 check-links.py > result. A link fails when the server answers with an error or not at all.
For a link with a #fragment on a page of the documentation, it also looks for the fragment as an id."""
import concurrent.futures, html, os, re, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
urls = {}
for f in ["exam-guide-breakdown.html", "exam-guide-breakdown.js", "behind-the-mocks.html", "behind-the-mocks.js"]:
    t = open(os.path.join(ROOT, "academy", "pages", f), encoding="utf-8").read()
    for u in re.findall(r'https?://[^\s"\'<>\\)\]]+', t):
        u = html.unescape(u).rstrip(".,;")
        urls.setdefault(u, set()).add(f.split(".")[0])
pages = {}


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (link check of academy pages)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace") if "#" in u or True else ""
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return type(e).__name__, ""


def check(u):
    base, _, frag = u.partition("#")
    if base not in pages:
        pages[base] = get(base)
    status, body = pages[base]
    note = ""
    if status == 200 and frag and not frag.startswith("L") and ("claude.com" in base or "anthropic.com" in base):
        if not re.search(r'id=["\']%s["\']' % re.escape(frag), body):
            note = "fragment not found"
    return u, status, note


bases = sorted({u.partition("#")[0] for u in urls})
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    for b, r in zip(bases, ex.map(get, bases)):
        pages[b] = r
bad = []
for u in sorted(urls):
    u, status, note = check(u)
    if status != 200 or note:
        bad.append((u, status, note, ",".join(sorted(urls[u]))))
print("# A1: the external links of both tabs\n")
print("Links: %d. Pages: %d. Problems: %d.\n" % (len(urls), len(bases), len(bad)))
for b in bad:
    print("- %s: %s %s (%s)" % b)
