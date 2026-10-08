#!/usr/bin/env python3
"""Retro black & white holographic DOT portrait -> assets/portrait.svg

Renders a photo as a fine halftone grid of circular dots (dot radius scales
with brightness), monochrome, on a solid black (or transparent) field, with a
subtle scanline sweep + hologram flicker. Animations run inside an <img> on
GitHub.

    python scripts/dot_portrait.py --photo assets/me.webp
    python scripts/dot_portrait.py --photo assets/me.webp --preview preview.png
    python scripts/dot_portrait.py --photo assets/me.webp --transparent
"""
import argparse
import math

# fine grid + geometry
COLS = ROWS = 104
CELL = 3                      # px per cell -> small, fine dots
PAD = 14
GW, GH = COLS * CELL, ROWS * CELL
W, H = GW + PAD * 2, GH + PAD * 2

DOT = "#EAF2FA"              # cool near-white (essentially B&W)


def values_from_photo(path):
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    M = COLS * 2                                   # mask resolution
    im = Image.open(path).convert("L")
    im = ImageOps.fit(im, (M, M), method=Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2))
    px = im.load()

    # background level from the four corners
    corners = []
    for (ox, oy) in [(0, 0), (M - 8, 0), (0, M - 8), (M - 8, M - 8)]:
        for dy in range(8):
            for dx in range(8):
                corners.append(px[ox + dx, oy + dy])
    bg = sum(corners) / len(corners)
    thr = bg - 30

    # flood-fill the bright background inward from the border
    is_bg = [[False] * M for _ in range(M)]
    stack = []
    for i in range(M):
        for (x, y) in [(i, 0), (i, M - 1), (0, i), (M - 1, i)]:
            if px[x, y] >= thr and not is_bg[y][x]:
                is_bg[y][x] = True
                stack.append((x, y))
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < M and 0 <= ny < M and not is_bg[ny][nx] and px[nx, ny] >= thr:
                is_bg[ny][nx] = True
                stack.append((nx, ny))

    # downsample 2x blocks -> grid value, dropping background
    raw = {}
    lo, hi = 1.0, 0.0
    for r in range(ROWS):
        for c in range(COLS):
            tot = fg = 0.0
            for dy in range(2):
                for dx in range(2):
                    x, y = c * 2 + dx, r * 2 + dy
                    if not is_bg[y][x]:
                        tot += px[x, y]
                        fg += 1
            if fg >= 2:
                v = (tot / fg) / 255.0
                raw[(c, r)] = v
                lo, hi = min(lo, v), max(hi, v)

    # stretch foreground tones; no floor so dark areas thin out cleanly
    vals = {}
    rng = max(1e-3, hi - lo)
    for k, v in raw.items():
        n = ((v - lo) / rng) ** 0.82
        if n > 0.10:
            vals[k] = n
    return vals


def values_silhouette():
    vals = {}
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c + .5, r + .5
            head = ((x - 52) / 24) ** 2 + ((y - 38) / 30) ** 2 <= 1
            body = y >= 74 and ((x - 52) / 50) ** 2 + ((y - 124) / 52) ** 2 <= 1
            if head or body:
                vals[(c, r)] = 0.85
    return vals


def build(vals, transparent=False):
    maxr = CELL * 0.56
    dots = []
    for (c, r), v in vals.items():
        rad = round(maxr * (0.28 + 0.72 * v), 2)
        op = round(0.30 + 0.70 * v, 2)
        cxp = PAD + c * CELL + CELL / 2
        cyp = PAD + r * CELL + CELL / 2
        dots.append(f'<circle cx="{cxp}" cy="{cyp}" r="{rad}" opacity="{op}"/>')

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="Dot-matrix hologram portrait of Abhishek Sinha">']
    s.append(
        '<style>'
        '.holo{animation:flick 7s linear infinite}'
        '@keyframes flick{0%,92%,100%{opacity:1}93%{opacity:.8}95%{opacity:.92}96%{opacity:.74}}'
        '.scan{animation:sweep 4.6s linear infinite}'
        f'@keyframes sweep{{from{{transform:translateY(-24px)}}to{{transform:translateY({GH + 24}px)}}}}'
        '</style>')
    s.append(
        '<defs>'
        f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{DOT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{DOT}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{DOT}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="frame"><rect x="{PAD}" y="{PAD}" width="{GW}" height="{GH}"/></clipPath>'
        '</defs>')

    if not transparent:
        s.append(f'<rect width="{W}" height="{H}" fill="#000000"/>')

    # the dots, with holographic flicker + sweeping light band
    s.append('<g class="holo">')
    s.append(f'<g fill="{DOT}">{"".join(dots)}</g>')
    s.append(f'<g clip-path="url(#frame)"><rect class="scan" x="{PAD}" y="{PAD}" '
             f'width="{GW}" height="24" fill="url(#scanG)"/></g>')
    s.append('</g>')

    # subtle retro corner brackets
    L = 14
    for bx, by, dx, dy in [(PAD, PAD, 1, 1), (PAD + GW, PAD, -1, 1),
                           (PAD, PAD + GH, 1, -1), (PAD + GW, PAD + GH, -1, -1)]:
        s.append(f'<path d="M{bx} {by + L * dy}V{by}H{bx + L * dx}" fill="none" '
                 f'stroke="{DOT}" stroke-width="1.5" opacity="0.55"/>')

    s.append('</svg>')
    return "".join(s)


def preview_png(vals, out, transparent=False):
    from PIL import Image, ImageDraw
    scale = 6
    mode = "RGBA" if transparent else "RGB"
    bgfill = (0, 0, 0, 0) if transparent else (0, 0, 0)
    img = Image.new(mode, (COLS * scale, ROWS * scale), bgfill)
    d = ImageDraw.Draw(img)
    maxr = scale * 0.56
    for (c, r), v in vals.items():
        rad = maxr * (0.28 + 0.72 * v)
        cx, cy = c * scale + scale / 2, r * scale + scale / 2
        g = int(234 * (0.3 + 0.7 * v))
        col = (g, min(255, g + 8), min(255, g + 16))
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
    img.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo")
    ap.add_argument("-o", "--out", default="assets/portrait.svg")
    ap.add_argument("--preview")
    ap.add_argument("--transparent", action="store_true")
    a = ap.parse_args()
    vals = values_from_photo(a.photo) if a.photo else values_silhouette()
    open(a.out, "w").write(build(vals, a.transparent))
    print("wrote", a.out)
    if a.preview:
        preview_png(vals, a.preview, a.transparent)
        print("wrote", a.preview)
