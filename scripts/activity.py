#!/usr/bin/env python3
"""Wavy retro-loader activity panel -> assets/activity-wave.svg, from your real contribution calendar.

    GITHUB_TOKEN=... python scripts/activity.py --user abhisheksinha20p
    python scripts/activity.py --demo        # offline preview: sample wave, no numbers
"""
import argparse
import math

A, V = "#2dd4bf", "#8b7cf6"


def render(weeks, stats, pct):
    W, H, n, gap = 880, 340, 52, 4
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated activity wave">',
         f'<defs><linearGradient id="v" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{A}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>',
         '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}.big{font-size:24px;font-weight:600}'
         '.seg{animation:b 1.8s ease-in-out infinite}@keyframes b{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}'
         '.col{transform-box:fill-box;transform-origin:bottom;animation:r 2.6s ease-in-out infinite}'
         '@keyframes r{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}</style>',
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#161b22" stroke="#30363d"/>',
         f'<text x="24" y="34" fill="{A}">$</text><text x="40" y="34" fill="#e6edf3">gh activity --sync</text>',
         f'<text x="{W - 24}" y="34" text-anchor="end" fill="#8b949e">active weeks {pct}</text>']
    segs, sgap = 44, 3
    sw = (W - 48 - sgap * (segs - 1)) / segs
    on = round(segs * (pct if isinstance(pct, (int, float)) else 83) / 100)
    for i in range(segs):
        fill = "url(#v)" if i < on else "#21262d"
        s.append(f'<rect class="seg" x="{24 + i * (sw + sgap):.1f}" y="62" width="{sw:.1f}" height="14" rx="2" fill="{fill}" style="animation-delay:-{i * .06:.2f}s"/>')
    tw = (W - 48 - 3 * 12) / 4
    for i, (label, value) in enumerate(stats):
        x = 24 + i * (tw + 12)
        s.append(f'<rect x="{x:.1f}" y="100" width="{tw:.1f}" height="64" rx="8" fill="#0d1117" stroke="#30363d"/>'
                 f'<text x="{x + 16:.1f}" y="124" fill="#8b949e">{label}</text>'
                 f'<text class="big" x="{x + 16:.1f}" y="152" fill="#e6edf3">{value}</text>')
    s.append('<text x="24" y="196" fill="#8b949e">contributions - last 52 weeks</text>')
    top = max(weeks) or 1
    cw, base = (W - 48 - gap * (n - 1)) / n, 320
    for i, v in enumerate(weeks):
        h = 8 + (v / top) * 100
        s.append(f'<rect class="col" x="{24 + i * (cw + gap):.1f}" y="{base - h:.1f}" width="{cw:.1f}" height="{h:.1f}" rx="1" fill="url(#v)" style="animation-delay:-{i * .09:.2f}s"/>')
    s.append(f'<line x1="24" y1="{base + 4}" x2="{W - 24}" y2="{base + 4}" stroke="#30363d"/></svg>')
    return "\n".join(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("-o", "--out", default="assets/activity-wave.svg")
    a = ap.parse_args()
    if a.demo:
        weeks = [abs(math.sin(i * .7) * math.cos(i * .23)) for i in range(52)]
        stats, pct = [(k, "--") for k in ("commits", "pull requests", "issues", "reviews")], "--"
    else:
        from ghapi import profile
        c = profile(a.user)["contributionsCollection"]
        days = c["contributionCalendar"]["weeks"][-52:]
        weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in days]
        weeks = [0] * (52 - len(weeks)) + weeks
        stats = [("commits", c["totalCommitContributions"]), ("pull requests", c["totalPullRequestContributions"]),
                 ("issues", c["totalIssueContributions"]), ("reviews", c["totalPullRequestReviewContributions"])]
        pct = f"{round(100 * sum(1 for w in weeks if w) / 52)}%"
    open(a.out, "w").write(render(weeks, stats, pct))
    print("wrote", a.out)
