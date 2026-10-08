"""Tiny GitHub API helpers shared by the profile scripts (stdlib only)."""
import json
import os
import urllib.request

API = "https://api.github.com"


def request(url, payload=None):
    headers = {"User-Agent": "profile-scripts", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(payload).encode() if payload is not None else None
    with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=30) as r:
        return json.load(r)


def graphql(query, **variables):
    out = request(API + "/graphql", {"query": query, "variables": variables})
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def repos(user):
    """All public, non-fork repos owned by `user`."""
    page, found = 1, []
    while True:
        batch = request(f"{API}/users/{user}/repos?per_page=100&type=owner&page={page}")
        found += [r for r in batch if not r["fork"]]
        if len(batch) < 100:
            return found
        page += 1


PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      contributionCalendar { weeks { contributionDays { contributionCount } } }
    }
  }
}"""


def profile(user):
    return graphql(PROFILE_QUERY, login=user)["user"]
