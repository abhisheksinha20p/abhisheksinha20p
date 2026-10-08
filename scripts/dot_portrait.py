#!/usr/bin/env python3
"""Retro black & white holographic DOT portrait -> assets/portrait.svg

Renders a photo as a halftone grid of circular dots (dot radius scales with
brightness), monochrome, on a dark field, with CSS scanline + flicker + a
sweeping light band so it reads as a retro hologram. Animations run inside
an <img> on GitHub.

    python scripts/dot_portrait.py --photo assets/me.jpg
    python scripts/dot_portrait.py --photo assets/me.jpg --preview preview.png

Needs Pillow. Falls back to a silhouette if no photo is given.
"""
import argparse
import math

# grid + geometry
COLS = ROWS = 56
CELL = 6                     # px per cell in the SVG
PAD = 30                     # frame padding
GW, GH = COLS * CELL, ROWS * CELL
W, H = GW + PAD * 2, GH + PAD * 2

BG = "#070a0f"
DOT = "#E8F0FA"              # cool white, essentially B&W
GRID_INK = "#2b3a4a"


def _smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def values_from_photo(path):
    from PIL import Image, ImageOps, ImageEnhance
    M = COLS * 2                                   # work at 2x for a clean mask
    im = Image.open(path).convert("L")
    im = ImageOps.fit(im, (M, M), method=Image.LANCZOS)
    px = im.load()

    # estimate background level from the four corners
    corners = []
    for (ox, oy) in [(0, 0), (M - 6, 0), (0, M - 6), (M - 6, M - 6)]:
        for dy in range(6):
            for dx in range(6):
                corners.append(px[ox + dx, oy + dy])
    bg = sum(corners) / len(corners)
    thr = bg - 32                                  # "bright like background"

    # flood-fill the bright background inward from every border pixel
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

    # downsample 2x blocks -> grid cell value, dropping background
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
            if fg >= 2:                            # cell is mostly foreground
                v = (tot / fg) / 255.0
                raw[(c, r)] = v
                lo, hi = min(lo, v), max(hi, v)

    # stretch foreground tones + gentle gamma so the face reads
    vals = {}
    rng = max(1e-3, hi - lo)
    for k, v in raw.items():
        n = (v - lo) / rng
        n = n ** 0.85
        vals[k] = 0.12 + 0.88 * n
    return vals


def values_silhouette():
    vals = {}
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c + .5, r + .5
            head = ((x - 28) / 13) ** 2 + ((y - 20) / 16) ** 2 <= 1
            body = y >= 40 and ((x - 28) / 27) ** 2 + ((y - 66) / 28) ** 2 <= 1
            if head or body:
                vals[(c, r)] = 0.85
    return vals


def build(vals):
    maxr = CELL * 0.52
    dots = []
    for (c, r), v in vals.items():
        rad = round(maxr * (0.35 + 0.65 * v), 2)      # brighter -> bigger dot
        op = round(0.45 + 0.55 * v, 2)
        cxp = PAD + c * CELL + CELL / 2
        cyp = PAD + r * CELL + CELL / 2
        dots.append(f'<circle cx="{cxp}" cy="{cyp}" r="{rad}" opacity="{op}"/>')

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" role="img" aria-label="Dot-matrix hologram portrait of Abhishek Sinha">')
    s.append(
        '<style>'
        '.holo{animation:flick 7s linear infinite}'
        '@keyframes flick{0%,93%,100%{opacity:1}94%{opacity:.78}96%{opacity:.9}97%{opacity:.72}}'
        '.scan{animation:sweep 4.2s linear infinite}'
        f'@keyframes sweep{{from{{transform:translateY(-30px)}}to{{transform:translateY({GH + 30}px)}}}}'
        '.shim{animation:shim 5s ease-in-out infinite}'
        '@keyframes shim{0%,100%{opacity:.0}50%{opacity:.5}}'
        '</style>')
    s.append(
        '<defs>'
        f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{DOT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{DOT}" stop-opacity=".30"/>'
        f'<stop offset="1" stop-color="{DOT}" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="vg" cx="0.5" cy="0.45" r="0.62">'
        f'<stop offset="0" stop-color="#0d1c26"/><stop offset="1" stop-color="{BG}"/></radialGradient>'
        f'<pattern id="scanlines" width="1" height="3" patternUnits="userSpaceOnUse">'
        f'<rect width="1" height="3" fill="none"/><rect width="1" height="1" fill="#000" opacity="0.22"/></pattern>'
        f'<clipPath id="frame"><rect x="{PAD}" y="{PAD}" width="{GW}" height="{GH}" rx="10"/></clipPath>'
        '</defs>')

    # backdrop
    s.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    s.append(f'<rect x="{PAD}" y="{PAD}" width="{GW}" height="{GH}" rx="10" fill="url(#vg)"/>')

    # faint alignment grid
    grid = [f'<g stroke="{GRID_INK}" stroke-width="0.5" opacity="0.25">']
    for i in range(0, COLS + 1, 7):
        grid.append(f'<line x1="{PAD + i * CELL}" y1="{PAD}" x2="{PAD + i * CELL}" y2="{PAD + GH}"/>')
    for i in range(0, ROWS + 1, 7):
        grid.append(f'<line x1="{PAD}" y1="{PAD + i * CELL}" x2="{PAD + GW}" y2="{PAD + i * CELL}"/>')
    grid.append('</g>')
    s.append(f'<g clip-path="url(#frame)">{"".join(grid)}</g>')

    # the dots (holographic flicker on the whole group)
    s.append(f'<g class="holo" clip-path="url(#frame)">')
    s.append(f'<g fill="{DOT}">{"".join(dots)}</g>')
    # sweeping light band
    s.append(f'<rect class="scan" x="{PAD}" y="{PAD}" width="{GW}" height="30" fill="url(#scanG)"/>')
    # scanline overlay
    s.append(f'<rect x="{PAD}" y="{PAD}" width="{GW}" height="{GH}" fill="url(#scanlines)"/>')
    s.append('</g>')

    # retro corner brackets
    L = 16
    for bx, by, dx, dy in [(PAD, PAD, 1, 1), (PAD + GW, PAD, -1, 1),
                           (PAD, PAD + GH, 1, -1), (PAD + GW, PAD + GH, -1, -1)]:
        s.append(f'<path d="M{bx} {by + L * dy}V{by}H{bx + L * dx}" fill="none" '
                 f'stroke="{DOT}" stroke-width="2" opacity="0.85"/>')

    # projector base
    s.append(f'<ellipse class="shim" cx="{W/2}" cy="{PAD + GH + 8}" rx="120" ry="9" '
             f'fill="none" stroke="{DOT}" stroke-dasharray="3 5" opacity="0.5"/>')

    s.append('</svg>')
    return "".join(s)


def preview_png(vals, out):
    from PIL import Image, ImageDraw
    scale = 10
    img = Image.new("RGB", (W * scale // CELL * CELL // CELL, 0))  # placeholder
    img = Image.new("RGB", (COLS * scale, ROWS * scale), (7, 10, 15))
    d = ImageDraw.Draw(img)
    maxr = scale * 0.52
    for (c, r), v in vals.items():
        rad = maxr * (0.35 + 0.65 * v)
        cx, cy = c * scale + scale / 2, r * scale + scale / 2
        g = int(232 * (0.45 + 0.55 * v))
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(g, g + 6 if g + 6 < 256 else 255, g + 10 if g + 10 < 256 else 255))
    img.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo")
    ap.add_argument("-o", "--out", default="assets/portrait.svg")
    ap.add_argument("--preview")
    a = ap.parse_args()
    vals = values_from_photo(a.photo) if a.photo else values_silhouette()
    open(a.out, "w").write(build(vals))
    print("wrote", a.out)
    if a.preview:
        preview_png(vals, a.preview)
        print("wrote", a.preview)
