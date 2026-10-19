"""Count the pixels that differ between the screenshots of compare-portal-form.js.

Usage: python3 academy/build/compare-shots.py <folder>
For each tab, mode and width, it compares the height of the page and each screen of the page that opens alone with the
same screen of the portal form, and writes <tag>-diff-<n>.png with the differing pixels in red. Exit code 0 means every
screen is the same.
"""
import glob
import os
import sys

from PIL import Image, ImageChops

folder = sys.argv[1]
tags = sorted({os.path.basename(f)[:-len("-alone.height")] for f in glob.glob(os.path.join(folder, "*-alone.height"))})
if not tags:
    sys.exit("No screenshots in " + folder)
bad = 0
for tag in tags:
    ha, hb = (open(os.path.join(folder, "%s-%s.height" % (tag, s))).read() for s in ("alone", "portal"))
    if ha != hb:
        print("%s: the height differs, %s px alone and %s px in the portal form" % (tag, ha, hb))
        bad += 1
        continue
    screens = sorted(glob.glob(os.path.join(folder, tag + "-alone-*.png")))
    differ = []
    for a_path in screens:
        n = a_path[-8:-4]
        a = Image.open(a_path).convert("RGB")
        b = Image.open(os.path.join(folder, "%s-portal-%s.png" % (tag, n))).convert("RGB")
        diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 0 else 0)
        if diff.getbbox():
            differ.append(n)
            Image.composite(Image.new("RGB", a.size, (255, 0, 0)), a, diff).save(os.path.join(folder, "%s-diff-%s.png" % (tag, n)))
    print("%s: height %s px, %d screens, %d differ%s" % (tag, ha, len(screens), len(differ), (": " + ", ".join(differ)) if differ else ""))
    bad += bool(differ)
print("All pairs are the same." if not bad else "Pairs that differ: %d" % bad)
sys.exit(1 if bad else 0)
