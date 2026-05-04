#!/usr/bin/env python3
"""
update_readme.py

Queries the LeetCode GraphQL API for the authenticated user's solve counts
and rewrites the Progress Tracker table in README.md.

Usage (called by GitHub Actions):
    python update_readme.p

Environment variables used:
    LEETCODE_SESSION   - value of the LEETCODE_SESSION cookie
    LEETCODE_CSRF_TOKEN - value of the csrftoken cookie
"""

import os
import re
import json
import urllib.request
import urllib.error
import datetime

# ---------------------------------------------------------------------------
# LeetCode API helpers
# ---------------------------------------------------------------------------

LEETCODE_GQL = "https://leetcode.com/graphql"

STATS_QUERY = """
query userProfileUserQuestionProgressV2($userSlug: String!) {
  userProfileUserQuestionProgressV2(userSlug: $userSlug) {
    numAcceptedQuestions {
      difficulty
      count
    }
    numFailedQuestions {
      difficulty
      count
    }
    numUntouchedQuestions {
      difficulty
      count
    }
  }
}
"""

TOTAL_QUERY = """
query problemsetQuestionList {
  problemsetQuestionList: questionList(
    categorySlug: ""
    limit: 1
    skip: 0
    filters: {}
  ) {
    total: totalNum
  }
}
"""

TOTAL_BY_DIFF_QUERY = """
query problemsetStats {
  easy: questionList(categorySlug: "", limit: 1, skip: 0, filters: {difficulty: EASY}) {
    totalNum
  }
  medium: questionList(categorySlug: "", limit: 1, skip: 0, filters: {difficulty: MEDIUM}) {
    totalNum
  }
  hard: questionList(categorySlug: "", limit: 1, skip: 0, filters: {difficulty: HARD}) {
    totalNum
  }
}
"""

ME_QUERY = """
query globalData {
  userStatus {
    username
  }
}
"""


def gql_request(query: str, variables: dict = None, session: str = "", csrf: str = "") -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        LEETCODE_GQL,
        data=payload,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf}",
            "x-csrftoken": csrf,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def get_username(session: str, csrf: str) -> str:
    data = gql_request(ME_QUERY, session=session, csrf=csrf)
    return data["data"]["userStatus"]["username"]


def get_solved_counts(username: str, session: str, csrf: str) -> dict:
    """Returns dict with keys EASY, MEDIUM, HARD -> solved count."""
    data = gql_request(STATS_QUERY, {"userSlug": username}, session=session, csrf=csrf)
    progress = data["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]
    counts = {item["difficulty"].upper(): item["count"] for item in progress}
    return counts


def get_total_counts(session: str, csrf: str) -> dict:
    """Returns dict with keys EASY, MEDIUM, HARD -> total problem count."""
    data = gql_request(TOTAL_BY_DIFF_QUERY, session=session, csrf=csrf)
    d = data["data"]
    return {
        "EASY": d["easy"]["totalNum"],
        "MEDIUM": d["medium"]["totalNum"],
        "HARD": d["hard"]["totalNum"],
    }


# ---------------------------------------------------------------------------
# Progress bar helper
# ---------------------------------------------------------------------------

def make_bar(solved: int, total: int, width: int = 10) -> str:
    if total == 0:
        return "░" * width + " 0.0%"
    pct = solved / total
    filled = round(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar} {pct * 100:.1f}%"


# ---------------------------------------------------------------------------
# README rewriter
# ---------------------------------------------------------------------------

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")

# Markers that wrap the auto-generated section in the README.
# The script will only replace content between these two markers.
START_MARKER = "<!-- PROGRESS_TRACKER_START -->"
END_MARKER = "<!-- PROGRESS_TRACKER_END -->"


def build_tracker_block(solved: dict, total: dict) -> str:
    easy_s, easy_t = solved.get("EASY", 0), total.get("EASY", 0)
    med_s, med_t = solved.get("MEDIUM", 0), total.get("MEDIUM", 0)
    hard_s, hard_t = solved.get("HARD", 0), total.get("HARD", 0)
    all_s = easy_s + med_s + hard_s
    all_t = easy_t + med_t + hard_t

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"_Last updated automatically on each sync. Stats pulled from my [LeetCode profile](https://leetcode.com/u/c9reTYFM0W/)._",
        "",
        "| Difficulty | Solved | Total | Progress |",
        "|-----------|--------|-------|----------|",
        f"| 🟢 Easy | {easy_s} | {easy_t} | {make_bar(easy_s, easy_t)} |",
        f"| 🟡 Medium | {med_s} | {med_t} | {make_bar(med_s, med_t)} |",
        f"| 🔴 Hard | {hard_s} | {hard_t} | {make_bar(hard_s, hard_t)} |",
        f"| **Total** | **{all_s}** | **{all_t}** | {make_bar(all_s, all_t)} |",
        "",
        f"<!-- updated: {now} -->",
    ]
    return "\n".join(lines)


def update_readme(solved: dict, total: dict):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_block = build_tracker_block(solved, total)
    new_section = f"{START_MARKER}\n{new_block}\n{END_MARKER}"

    if START_MARKER in content and END_MARKER in content:
        # Replace existing block
        pattern = re.compile(
            re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
            re.DOTALL,
        )
        new_content = pattern.sub(new_section, content)
    else:
        # Markers missing — insert after the "## 📊 Progress Tracker" heading
        heading_pattern = re.compile(r"(##\s*📊\s*Progress Tracker\s*\n)")
        if heading_pattern.search(content):
            new_content = heading_pattern.sub(
                r"\1" + new_section + "\n\n", content, count=1
            )
        else:
            # Fallback: append at end
            new_content = content.rstrip() + "\n\n" + new_section + "\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README.md updated successfully.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    session = os.environ.get("LEETCODE_SESSION", "")
    csrf = os.environ.get("LEETCODE_CSRF_TOKEN", "")

    if not session or not csrf:
        raise EnvironmentError(
            "LEETCODE_SESSION and LEETCODE_CSRF_TOKEN environment variables must be set."
        )

    print("Fetching username...")
    username = get_username(session, csrf)
    print(f"Logged in as: {username}")

    print("Fetching solved counts...")
    solved = get_solved_counts(username, session, csrf)
    print(f"Solved: {solved}")

    print("Fetching total problem counts...")
    total = get_total_counts(session, csrf)
    print(f"Totals: {total}")

    update_readme(solved, total)


if __name__ == "__main__":
    main()
