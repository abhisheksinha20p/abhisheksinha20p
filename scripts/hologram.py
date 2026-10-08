#!/usr/bin/env python3
"""Pixel hologram avatar -> assets/hologram.svg (animated, works inside <img>).

    python scripts/hologram.py                      # silhouette placeholder
    python scripts/hologram.py --photo assets/me.jpg  # your photo, dithered to pixels (needs Pillow)
"""
import argparse

A, V = "#2dd4bf", "#8b7cf6"
COLS, ROWS, CELL = 26, 30, 8
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]
BANDS = ["#b6f7ee", A, "#6aa8f7", V]


def silhouette():
    keep = set()
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c + .5, r + .5
            head = ((x - 13) / 6.4) ** 2 + ((y - 9.5) / 7.8) ** 2 <= 1
            neck = abs(x - 13) <= 2.6 and 15 <= y <= 20
            body = y >= 19 and ((x - 13) / 13) ** 2 + ((y - 32) / 13.5) ** 2 <= 1
            if (head or neck or body) and not (r == 9 and c in (10, 11, 15, 16)):
                keep.add((c, r))
    return keep


def from_photo(path):
    from PIL import Image, ImageOps
    img = ImageOps.autocontrast(ImageOps.fit(Image.open(path).convert("L"), (COLS, ROWS)))
    return {(c, r) for r in range(ROWS) for c in range(COLS)
            if img.getpixel((c, r)) / 255 > BAYER[(r % 4) * 4 + (c % 4)] / 16 * .8 + .1}


def build(keep):
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            if (c, r) not in keep:
                continue
            if r >= 21 and BAYER[(r % 4) * 4 + (c % 4)] / 16 >= 1 - (r - 21) / 10:
                continue  # projection fades out at the bottom
            cells.append((c, r, BANDS[min(3, r // 8)], ((c * 7 + r * 13) % 30) / 10))
    w, h, ox, oy = 288, 310, 40, 24
    gw, gh = COLS * CELL, ROWS * CELL
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Pixel hologram avatar">',
         '<style>.p{animation:t 2.4s steps(3) infinite}@keyframes t{0%,100%{opacity:1}50%{opacity:.45}}'
         '.scan{animation:s 3.6s linear infinite}'
         f'@keyframes s{{from{{transform:translateY(-22px)}}to{{transform:translateY({gh}px)}}}}'
         '.h{animation:f 6s linear infinite}@keyframes f{0%,90%,95%,100%{opacity:1}92%{opacity:.7}96%{opacity:.82}}</style>',
         f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{A}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{A}" stop-opacity=".45"/><stop offset="1" stop-color="{A}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="c"><rect x="{ox}" y="{oy}" width="{gw}" height="{gh}"/></clipPath></defs>']
    for bx, by, dx, dy in [(ox - 14, oy - 14, 1, 1), (ox + gw + 14, oy - 14, -1, 1),
                           (ox - 14, oy + gh + 14, 1, -1), (ox + gw + 14, oy + gh + 14, -1, -1)]:
        s.append(f'<path d="M{bx} {by + 14 * dy}V{by}H{bx + 14 * dx}" fill="none" stroke="{A}" stroke-width="2" opacity=".8"/>')
    for dx, col, op in [(-2, A, .5), (2, V, .55)]:
        s.append(f'<g class="h" opacity="{op}" transform="translate({ox + dx} {oy})" fill="{col}">'
                 + "".join(f'<rect x="{c * CELL}" y="{r * CELL}" width="8" height="8"/>' for c, r, _, _ in cells) + "</g>")
    s.append(f'<g class="h" transform="translate({ox} {oy})">'
             + "".join(f'<rect class="p" x="{c * CELL}" y="{r * CELL}" width="8" height="8" fill="{col}" style="animation-delay:-{d}s"/>'
                       for c, r, col, d in cells) + "</g>")
    s.append(f'<g clip-path="url(#c)"><rect class="scan" x="{ox}" y="{oy}" width="{gw}" height="22" fill="url(#g)"/></g>')
    s.append(f'<ellipse cx="{ox + gw // 2}" cy="{oy + gh + 30}" rx="90" ry="11" fill="none" stroke="{A}" stroke-dasharray="4 4" opacity=".7"/></svg>')
    return "\n".join(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo")
    ap.add_argument("-o", "--out", default="assets/hologram.svg")
    a = ap.parse_args()
    svg = build(from_photo(a.photo) if a.photo else silhouette())
    open(a.out, "w").write(svg)
    print("wrote", a.out)
