#!/usr/bin/env python3
"""Self-hosted stat card + project cards -> assets/card-*.svg (dark + light).

    GITHUB_TOKEN=... python scripts/cards.py --user abhisheksinha20p --projects assets/projects.json --out assets
    python scripts/cards.py --projects assets/projects.json --out assets --no-stats   # offline: project cards only
"""
import argparse
import json
import textwrap
from xml.sax.saxutils import escape

T = {
    "dark": dict(bg="#161b22", line="#30363d", text="#e6edf3", mute="#8b949e", acc="#2dd4bf", vio="#8b7cf6"),
    "light": dict(bg="#ffffff", line="#d0d7de", text="#1f2328", mute="#57606a", acc="#0f766e", vio="#6d5bd0"),
}
FONT = "ui-monospace,SFMono-Regular,Menlo,monospace"


def frame(w, h, t, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>text{{font-family:{FONT}}}</style>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>{body}</svg>')


def stat_card(rows, t):
    body = f'<text x="24" y="38" font-size="15" font-weight="600" fill="{t["text"]}">GitHub at a glance</text>'
    for i, (k, v) in enumerate(rows):
        y = 72 + i * 28
        body += (f'<text x="24" y="{y}" font-size="13" fill="{t["mute"]}">{escape(k)}</text>'
                 f'<text x="456" y="{y}" font-size="14" font-weight="600" text-anchor="end" fill="{t["acc"]}">{escape(str(v))}</text>')
    return frame(480, 72 + len(rows) * 28 - 8, t, body)


def project_card(p, t):
    tag_col = t["acc"] if p["platform"] == "Mobile" else t["vio"]
    body = (f'<rect x="24" y="22" width="{14 + 8 * len(p["platform"])}" height="22" rx="6" fill="none" stroke="{tag_col}"/>'
            f'<text x="{24 + 7}" y="37" font-size="12" fill="{tag_col}">{escape(p["platform"])}</text>'
            f'<text x="24" y="72" font-size="17" font-weight="600" fill="{t["text"]}">{escape(p["name"])}</text>')
    for i, line in enumerate(textwrap.wrap(p["description"], 44)[:4]):
        body += f'<text x="24" y="{98 + i * 20}" font-size="13" fill="{t["mute"]}">{escape(line)}</text>'
    body += f'<text x="24" y="204" font-size="12" fill="{tag_col}">{escape(" · ".join(p["stack"]))}</text>'
    if "stars" in p:
        body += f'<text x="396" y="37" font-size="12" text-anchor="end" fill="{t["mute"]}">★ {p["stars"]}  ⑂ {p["forks"]}</text>'
    return frame(396, 226, t, body)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user")
    ap.add_argument("--projects")
    ap.add_argument("--out", default="assets")
    ap.add_argument("--no-stats", action="store_true")
    a = ap.parse_args()
    if not a.no_stats:
        from ghapi import profile, repos
        me, rs = profile(a.user), repos(a.user)
        c = me["contributionsCollection"]
        days = [d["contributionCount"] for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
        cur = 0
        for n in reversed(days if days and days[-1] else days[:-1]):  # today may not have commits yet
            if not n:
                break
            cur += 1
        best = run = 0
        for n in days:
            run = run + 1 if n else 0
            best = max(best, run)
        rows = [("Stars earned", sum(r["stargazers_count"] for r in rs)), ("Followers", me["followers"]["totalCount"]),
                ("Public repos", me["repositories"]["totalCount"]), ("Current streak", f"{cur} days"), ("Longest streak (12 mo)", f"{best} days"),
                ("Commits (12 mo)", c["totalCommitContributions"]),
                ("Pull requests (12 mo)", c["totalPullRequestContributions"]), ("Issues (12 mo)", c["totalIssueContributions"]),
                ("Code reviews (12 mo)", c["totalPullRequestReviewContributions"])]
        for n, t in T.items():
            open(f"{a.out}/card-stats-{n}.svg", "w").write(stat_card(rows, t))
    if a.projects:
        projects = json.load(open(a.projects))["projects"]
        live = {}
        if a.user and not a.no_stats:
            live = {r["name"]: r for r in rs}
        for p in projects:
            r = live.get(p.get("repo", ""))
            if r:
                p = {**p, "stars": r["stargazers_count"], "forks": r["forks_count"]}
            for n, t in T.items():
                open(f"{a.out}/card-{p['slug']}-{n}.svg", "w").write(project_card(p, t))
    print("done")
