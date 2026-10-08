#!/usr/bin/env python3
"""Radar charts -> <out>-dark.svg / <out>-light.svg (swap with <picture>).

    python scripts/radar.py --data assets/skills.json -o assets/radar          # self-rated
    GITHUB_TOKEN=... python scripts/radar.py --github USER -o assets/radar-langs  # from your repos' bytes
"""
import argparse
import json
import math
from collections import Counter
from xml.sax.saxutils import escape

THEMES = {
    "dark": dict(grid="#30363d", label="#c9d1d9", title="#e6edf3", fill="#2dd4bf", stroke="#2dd4bf"),
    "light": dict(grid="#d0d7de", label="#1f2328", title="#1f2328", fill="#0f766e", stroke="#0f766e"),
}


def render(title, axes, t):
    W, H, cx, cy, R = 440, 400, 220, 215, 125
    n = len(axes)
    pt = lambda i, k: (cx + R * k * math.sin(2 * math.pi * i / n), cy - R * k * math.cos(2 * math.pi * i / n))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">',
         f'<text x="{W / 2}" y="30" text-anchor="middle" font-family="ui-monospace,Menlo,monospace" font-size="15" font-weight="600" fill="{t["title"]}">{escape(title)}</text>']
    for ring in (.25, .5, .75, 1):
        s.append(f'<polygon points="{" ".join("%.1f,%.1f" % pt(i, ring) for i in range(n))}" fill="none" stroke="{t["grid"]}"/>')
    for i, a in enumerate(axes):
        x, y = pt(i, 1)
        lx, ly = pt(i, 1.17)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["grid"]}"/>'
                 f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-family="ui-monospace,Menlo,monospace" font-size="12" fill="{t["label"]}">{escape(a["label"])}</text>')
    poly = " ".join("%.1f,%.1f" % pt(i, a["value"] / 100) for i, a in enumerate(axes))
    s.append(f'<polygon points="{poly}" fill="{t["fill"]}" fill-opacity=".22" stroke="{t["stroke"]}" stroke-width="2" stroke-linejoin="round"/>')
    s += [f'<circle cx="{pt(i, a["value"] / 100)[0]:.1f}" cy="{pt(i, a["value"] / 100)[1]:.1f}" r="3.5" fill="{t["stroke"]}"/>' for i, a in enumerate(axes)]
    return "\n".join(s + ["</svg>"])


def language_axes(user, limit):
    from ghapi import repos, request
    total = Counter()
    for r in repos(user):
        total.update(request(r["languages_url"]))
    top = total.most_common(limit)
    if not top:
        raise SystemExit("no language data found")
    return [{"label": k, "value": round(100 * v / top[0][1])} for k, v in top]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--github")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--limit", type=int, default=7)
    a = ap.parse_args()
    if a.github:
        title, axes = "Languages (by code written)", language_axes(a.github, a.limit)
    else:
        d = json.load(open(a.data))
        title, axes = d["title"], d["axes"]
    for name, t in THEMES.items():
        open(f"{a.out}-{name}.svg", "w").write(render(title, axes, t))
    print("wrote", a.out)
