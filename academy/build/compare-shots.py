"""Count the pixels that differ between each pair of screenshots of compare-portal-form.js.

Usage: python3 academy/build/compare-shots.py <folder>
It prints, for each pair, the sizes and the number of pixels that differ, and writes <tag>-diff.png with the
differing pixels in red. Exit code 0 means every pair is the same.
"""
import glob
import os
import sys

from PIL import Image, ImageChops

folder = sys.argv[1]
bad = 0
pairs = sorted(glob.glob(os.path.join(folder, "*-alone.png")))
if not pairs:
    sys.exit("No screenshots in " + folder)
for alone in pairs:
    tag = os.path.basename(alone)[:-len("-alone.png")]
    a = Image.open(alone).convert("RGB")
    b = Image.open(os.path.join(folder, tag + "-portal.png")).convert("RGB")
    if a.size != b.size:
        print("%s: the size differs, %dx%d alone and %dx%d in the portal form" % (tag, a.size[0], a.size[1], b.size[0], b.size[1]))
        bad += 1
        w, h = min(a.size[0], b.size[0]), min(a.size[1], b.size[1])
        a, b = a.crop((0, 0, w, h)), b.crop((0, 0, w, h))
    diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 0 else 0)
    n = sum(1 for v in diff.getdata() if v)
    print("%s: %d pixels differ" % (tag, n))
    if n:
        bad += 1
        box = diff.getbbox()
        print("   first and last row that differ: %d to %d" % (box[1], box[3]))
        red = Image.new("RGB", a.size, (255, 0, 0))
        Image.composite(red, a, diff).save(os.path.join(folder, tag + "-diff.png"))
print("All pairs are the same." if not bad else "Pairs that differ: %d" % bad)
sys.exit(1 if bad else 0)
