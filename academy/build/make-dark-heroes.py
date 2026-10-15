"""Makes the dark-mode copies of the domain images (owner, 15 October 2026): the background outside the drawing becomes
transparent, and the dark outlines next to it become the cream colour of the text. Run from the root of the repository."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
CREAM = np.array([244, 242, 239], dtype=np.float32)
for i in range(1, 6):
    im = Image.open("academy/pages/images/domains/originals/domain-%d-hero.png" % i).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    bg = np.median(np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3)]), axis=0)
    near = ((np.abs(a - bg).max(axis=2)) < 14).astype(np.uint8) * 255
    m = Image.fromarray(near).copy()
    for xy in [(0, 0), (m.width - 1, 0), (0, m.height - 1), (m.width - 1, m.height - 1)]:
        if m.getpixel(xy) == 255:
            ImageDraw.floodfill(m, xy, 128, thresh=0)
    outside = np.array(m) == 128
    alpha = np.array(Image.fromarray(np.where(outside, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)
    mx, mn = a.max(axis=2), a.min(axis=2)
    light = (mx + mn) / 2 / 255
    sat = (mx - mn) / 255
    dark = (light < 0.5) & (sat < 0.3)
    near_out = np.array(Image.fromarray(outside.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    recolor = dark & near_out
    w = np.clip((0.55 - light) / 0.55, 0, 1)[..., None]
    out = a.copy()
    out[recolor] = CREAM * w[recolor] + a[recolor] * (1 - w[recolor])
    rgba = Image.fromarray(np.dstack([out, alpha]).clip(0, 255).astype(np.uint8), "RGBA")
    light_copy = Image.open("academy/pages/images/domains/domain-%d.webp" % i)
    box = Image.fromarray((~outside).astype(np.uint8) * 255).getbbox()
    pad = 24
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    rgba = rgba.crop(box).resize(light_copy.size, Image.LANCZOS)
    p = "academy/pages/images/domains/domain-%d-dark.webp" % i
    rgba.save(p, "WEBP", quality=85, method=6)
    print(p, rgba.size, os.path.getsize(p) // 1024, "KB", Image.open(p).mode)
