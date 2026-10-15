"""Makes the web copies of the domain images from the originals of the owner (15 October 2026). Run from the root of the repository.

The background outside the drawing becomes transparent. The outside is the cream background that touches the edge of the image.
For the light copy, small gaps, such as the gaps of a dashed border, are closed first, so that the inside of a box keeps its fill.
The dark copy closes no gap, because an area between lines that keeps the cream background shows on the dark page. Each copy is cut to
the drawing and is 520 pixels high. The dark copy (domain-N-dark.webp) also turns the dark outlines next to the outside into the
cream colour of the text, for dark mode."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os

CREAM = np.array([244, 242, 239], dtype=np.float32)
GAP = 17   # pixels: a gap narrower than this, such as in a dashed border, does not let the outside in
# boxes whose white fill is almost the colour of the background: they stay solid in the dark copy (original pixels, x0 y0 x1 y1)
SOLID = {1: [(1300, 478, 1482, 562)],    # the dashed box of the open step
         5: [(1176, 526, 1344, 642)]}    # the card "Confidence"


def outside_of(a, gap):
    bg = np.median(np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3)]), axis=0)
    near = ((np.abs(a - bg).max(axis=2)) < 14).astype(np.uint8) * 255
    shrunk = (Image.fromarray(near).filter(ImageFilter.MinFilter(gap)) if gap > 1 else Image.fromarray(near)).copy()   # close the small gaps
    for xy in [(0, 0), (shrunk.width - 1, 0), (0, shrunk.height - 1), (shrunk.width - 1, shrunk.height - 1)]:
        if shrunk.getpixel(xy) == 255:
            ImageDraw.floodfill(shrunk, xy, 128, thresh=0)
    flooded = (np.array(shrunk) == 128).astype(np.uint8) * 255
    grown = (np.array(Image.fromarray(flooded).filter(ImageFilter.MaxFilter(gap))) if gap > 1 else flooded) > 0
    return grown & (near > 0)


for i in range(1, 6):
    im = Image.open("academy/pages/images/domains/originals/domain-%d-hero.png" % i).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    outside = outside_of(a, GAP)
    alpha = np.array(Image.fromarray(np.where(outside, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)
    box = Image.fromarray((~outside).astype(np.uint8) * 255).getbbox()
    pad = 24
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    h = 520
    size = (round((box[2] - box[0]) * h / (box[3] - box[1])), h)
    # the light copy: the colours of the original
    light = Image.fromarray(np.dstack([a, alpha]).clip(0, 255).astype(np.uint8), "RGBA").crop(box).resize(size, Image.LANCZOS)
    light.save("academy/pages/images/domains/domain-%d.webp" % i, "WEBP", quality=85, method=6)
    # the dark copy: no gap is closed, so no area between lines keeps the cream background (it would show on the dark page);
    # specks of one or two pixels in the outside are removed; dark outlines next to the outside become cream
    outside = outside_of(a, 1)
    for x0, y0, x1, y1 in SOLID.get(i, []):
        outside[y0:y1, x0:x1] = False
    inside = Image.fromarray((~outside).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    outside = np.array(inside) == 0
    alpha = np.array(Image.fromarray(np.where(outside, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)
    mx, mn = a.max(axis=2), a.min(axis=2)
    lightness, sat = (mx + mn) / 2 / 255, (mx - mn) / 255
    near_out = np.array(Image.fromarray(outside.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    recolor = (lightness < 0.5) & (sat < 0.3) & near_out
    w = np.clip((0.55 - lightness) / 0.55, 0, 1)[..., None]
    out = a.copy()
    out[recolor] = CREAM * w[recolor] + a[recolor] * (1 - w[recolor])
    dark = Image.fromarray(np.dstack([out, alpha]).clip(0, 255).astype(np.uint8), "RGBA").crop(box).resize(size, Image.LANCZOS)
    dark.save("academy/pages/images/domains/domain-%d-dark.webp" % i, "WEBP", quality=85, method=6)
    print(i, size, os.path.getsize("academy/pages/images/domains/domain-%d.webp" % i) // 1024, "KB,", os.path.getsize("academy/pages/images/domains/domain-%d-dark.webp" % i) // 1024, "KB")
