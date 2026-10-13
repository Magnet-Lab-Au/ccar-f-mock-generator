"""Compare the copy of the exam guide with the official PDF, word for word (decision 0027).

The page quotes of tab 1 come from reference/exam-guide.md. This script reads the official
PDF (academy/sources/exam-guide-v1.0-official.pdf) and the copy, makes both into one list of
words, and lists each place where the two lists differ.

It removes only what is not text of the guide: the Markdown marks of the copy, and the running
headers, the page footers and the line breaks of the PDF. It also replaces the "fi" and "fl"
ligatures of the PDF, removes its list bullets, and keeps a hyphen at the end of a line inside its word.
Each other difference is listed.

Needs the library pypdf. Run from the folder ccar-f-mock-generator:
    python3 academy/sources/compare-exam-guide.py
"""
import difflib
import os
import re
import sys

import pypdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(ROOT, "academy", "sources", "exam-guide-v1.0-official.pdf")
COPY = os.path.join(ROOT, "reference", "exam-guide.md")


def pdf_words():
    pages = []
    for page in pypdf.PdfReader(PDF).pages:
        lines = page.extract_text().splitlines()
        keep = []
        for line in lines:
            s = line.strip()
            s = re.sub(r"^Claude Certification Program\s*Exam guide\s*", "", s)  # running header
            if s in ("Claude Certification Program", "Exam guide") or re.fullmatch(r"(Page )?\d+( of \d+)?", s):
                continue
            keep.append(s)
        pages.append("\n".join(keep))
    text = "\n".join(pages)
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"(\w)-\n(\w)", r"\1-\2", text)  # a hyphen at the end of a line stays in the word
    text = text.replace("\u2022", " ")  # list bullets
    return text.split()


def copy_words():
    with open(COPY, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)       # page notes of the copy
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M)          # headings
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)        # list marks
    text = re.sub(r"^\s*\|?\s*:?-{3,}.*$", "", text, flags=re.M)  # table rules
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)    # a link shows only its text
    text = text.replace("\\|", "\0").replace("|", " ").replace("**", "").replace("`", "")
    text = re.sub(r"\\([*<>_\[\]])", r"\1", text).replace("\0", "|")  # escaped marks are text
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)        # italics
    return text.split()


def main():
    a, b = pdf_words(), copy_words()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print("PDF: %d words. Copy: %d words. Places that differ: %d." % (len(a), len(b), len(diffs)))
    for tag, i1, i2, j1, j2 in diffs:
        ctx = " ".join(a[max(0, i1 - 6):i1])
        print("\n- %s, after \"...%s\"" % (tag, ctx))
        print("  PDF:  %s" % (" ".join(a[i1:i2]) or "(nothing)"))
        print("  Copy: %s" % (" ".join(b[j1:j2]) or "(nothing)"))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
