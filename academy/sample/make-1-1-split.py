"""Split the fifth sample into two linked pages, as the portal will have them (owner, 13 October 2026).

Reads academy/sample/1-1-agentic-loops-kit.html (made by make-1-1-kit.py) and writes:
- academy/sample/1-1-split-exam-guide.html: the task statement page of "Exam guide breakdown"
- academy/sample/1-1-split-behind-the-mocks.html: its entry in "Behind the mocks"

Each page links to the other. Each page lists only the sources of its own cards. The
figures of the second page are numbered from 1 again. Nothing else changes: the text, the
figures, the popups and the cards are the checked content of the fifth sample.

Run from the folder ccar-f-mock-generator, after make-1-1-kit.py:
    python3 academy/sample/make-1-1-split.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "1-1-agentic-loops-kit.html")
GUIDE, BEHIND = "1-1-split-exam-guide.html", "1-1-split-behind-the-mocks.html"

with open(SRC, encoding="utf-8") as f:
    page = f.read()

m0, m1 = page.index("<main>") + len("<main>"), page.index("</main>")
head, main, tail = page[:m0], page[m0:m1], page[m1:]

# the two parts of main, and the sources at the end
i_hr = main.index('<hr class="split-line">')
i_behind = main.index("\n", i_hr) + 1
i_src = main.index('<section class="sources"')
guide_part, behind_part, sources = main[:i_hr], main[i_behind:i_src], main[i_src:]

# the sources list has one item for each card, in the order of the card data
CARD = json.loads(re.search(r'id="carddata">(.*?)</script>', page, re.S).group(1).replace("<\\/", "</"))
POP = json.loads(re.search(r'id="popdata">(.*?)</script>', page, re.S).group(1).replace("<\\/", "</"))
cards = list(CARD)
items = re.findall(r"<li>.*?</li>", sources, re.S)
assert len(items) == len(cards), (len(items), len(cards))
intro = re.search(r'<p class="ve-label">Sources\..*?</p>', sources, re.S).group(0)


def sources_of(part, note):
    used = set(re.findall(r'data-card="([^"]+)"', part))
    # a popup that quotes the code of a card names the source of that card in its note
    for step in set(re.findall(r'data-step="([^"]+)"', part)):
        used |= {cid for cid, c in CARD.items() if c["src"] in POP.get(step, {}).get("examplenote", "")}
    lis = "".join(li for cid, li in zip(cards, items) if cid in used)
    return ('<section class="sources" aria-label="Sources">\n  %s\n  <ul>%s</ul>\n  <p class="ve-label">%s</p>\n</section>\n'
            % (intro, lis, note)), len(used)


NOTE = ("Split sample: the fifth sample as two linked pages, by academy/sample/make-1-1-split.py. "
        "The content is the checked content of the first sample.")

# links between the two pages
assert guide_part.count('href="#behind">Behind the mocks 1.1 &darr;') == 2
guide_part = guide_part.replace('href="#behind">Behind the mocks 1.1 &darr;', 'href="%s">Behind the mocks 1.1 &rarr;' % BEHIND)
assert behind_part.count('href="#ts">Task statement 1.1 &uarr;') == 1
behind_part = behind_part.replace('href="#ts">Task statement 1.1 &uarr;', 'href="%s">Exam guide breakdown 1.1 &rarr;' % GUIDE)

# the figures of the second page start again at Fig. 1
behind_part = re.sub(r"Fig\. ([5-8])", lambda m: "Fig. %d" % (int(m.group(1)) - 4), behind_part)

guide_title = re.search(r"<title>(.*?)</title>", head).group(1)
behind_head = head.replace("<title>%s</title>" % guide_title, "<title>Behind the mocks 1.1: a pass stops the loop</title>", 1)

for name, h, part in ((GUIDE, head, guide_part), (BEHIND, behind_head, behind_part)):
    src_html, n = sources_of(part, NOTE)
    out = h + part + src_html + tail
    assert "#behind" not in out.replace('id="behind"', "") and 'href="#ts"' not in out
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(out)
    print("Wrote academy/sample/%s: %d cards in its sources, %d popups and cards on the page."
          % (name, n, len(re.findall(r'data-(?:step|card)="', part))))
