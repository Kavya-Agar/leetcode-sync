#!/usr/bin/env python3
"""
update_readme.py

Queries the LeetCode GraphQL API for the authenticated user's solve counts
and rewrites two sections in README.md:
  1. The general Progress Tracker table (Easy / Medium / Hard stats).
  2. The NeetCode 150 Progress table (per-category solved/total counts).

Usage (called by GitHub Actions):
    python update_readme.py

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
# NeetCode 150 problem list
# Maps category name -> list of (problem_number, slug) tuples
# ---------------------------------------------------------------------------

NEETCODE_150 = {
    "Arrays & Hashing": [
        (217, "contains-duplicate"),
        (242, "valid-anagram"),
        (1, "two-sum"),
        (49, "group-anagrams"),
        (347, "top-k-frequent-elements"),
        (238, "product-of-array-except-self"),
        (36, "valid-sudoku"),
        (271, "encode-and-decode-strings"),
        (128, "longest-consecutive-sequence"),
    ],
    "Two Pointers": [
        (125, "valid-palindrome"),
        (167, "two-sum-ii-input-array-is-sorted"),
        (15, "3sum"),
        (11, "container-with-most-water"),
        (42, "trapping-rain-water"),
    ],
    "Sliding Window": [
        (121, "best-time-to-buy-and-sell-stock"),
        (3, "longest-substring-without-repeating-characters"),
        (424, "longest-repeating-character-replacement"),
        (567, "permutation-in-string"),
        (76, "minimum-window-substring"),
        (239, "sliding-window-maximum"),
    ],
    "Stack": [
        (20, "valid-parentheses"),
        (155, "min-stack"),
        (150, "evaluate-reverse-polish-notation"),
        (22, "generate-parentheses"),
        (739, "daily-temperatures"),
        (853, "car-fleet"),
        (84, "largest-rectangle-in-histogram"),
    ],
    "Binary Search": [
        (704, "binary-search"),
        (74, "search-a-2d-matrix"),
        (875, "koko-eating-bananas"),
        (153, "find-minimum-in-rotated-sorted-array"),
        (33, "search-in-rotated-sorted-array"),
        (981, "time-based-key-value-store"),
        (4, "median-of-two-sorted-arrays"),
    ],
    "Linked List": [
        (206, "reverse-linked-list"),
        (21, "merge-two-sorted-lists"),
        (143, "reorder-list"),
        (19, "remove-nth-node-from-end-of-list"),
        (138, "copy-list-with-random-pointer"),
        (2, "add-two-numbers"),
        (287, "find-the-duplicate-number"),
        (146, "lru-cache"),
        (23, "merge-k-sorted-lists"),
        (25, "reverse-nodes-in-k-group"),
    ],
    "Trees": [
        (226, "invert-binary-tree"),
        (104, "maximum-depth-of-binary-tree"),
        (543, "diameter-of-binary-tree"),
        (110, "balanced-binary-tree"),
        (100, "same-tree"),
        (572, "subtree-of-another-tree"),
        (235, "lowest-common-ancestor-of-a-binary-search-tree"),
        (102, "binary-tree-level-order-traversal"),
        (199, "binary-tree-right-side-view"),
        (1448, "count-good-nodes-in-binary-tree"),
        (98, "validate-binary-search-tree"),
        (230, "kth-smallest-element-in-a-bst"),
        (105, "construct-binary-tree-from-preorder-and-inorder-traversal"),
        (124, "binary-tree-maximum-path-sum"),
        (297, "serialize-and-deserialize-binary-tree"),
    ],
    "Heap / Priority Queue": [
        (703, "kth-largest-element-in-a-stream"),
        (1046, "last-stone-weight"),
        (973, "k-closest-points-to-origin"),
        (215, "kth-largest-element-in-an-array"),
        (621, "task-scheduler"),
        (355, "design-twitter"),
        (295, "find-median-from-data-stream"),
    ],
    "Backtracking": [
        (78, "subsets"),
        (39, "combination-sum"),
        (40, "combination-sum-ii"),
        (46, "permutations"),
        (90, "subsets-ii"),
        (79, "word-search"),
        (131, "palindrome-partitioning"),
        (17, "letter-combinations-of-a-phone-number"),
        (51, "n-queens"),
    ],
    "Graphs": [
        (200, "number-of-islands"),
        (133, "clone-graph"),
        (695, "max-area-of-island"),
        (417, "pacific-atlantic-water-flow"),
        (130, "surrounded-regions"),
        (994, "rotting-oranges"),
        (286, "walls-and-gates"),
        (207, "course-schedule"),
        (210, "course-schedule-ii"),
        (684, "redundant-connection"),
        (323, "number-of-connected-components-in-an-undirected-graph"),
        (261, "graph-valid-tree"),
        (127, "word-ladder"),
    ],
    "Advanced Graphs": [
        (332, "reconstruct-itinerary"),
        (1584, "min-cost-to-connect-all-points"),
        (743, "network-delay-time"),
        (778, "swim-in-rising-water"),
        (269, "alien-dictionary"),
        (787, "cheapest-flights-within-k-stops"),
    ],
    "1-D Dynamic Programming": [
        (70, "climbing-stairs"),
        (746, "min-cost-climbing-stairs"),
        (198, "house-robber"),
        (213, "house-robber-ii"),
        (5, "longest-palindromic-substring"),
        (647, "palindromic-substrings"),
        (91, "decode-ways"),
        (322, "coin-change"),
        (152, "maximum-product-subarray"),
        (139, "word-break"),
        (300, "longest-increasing-subsequence"),
        (416, "partition-equal-subset-sum"),
    ],
    "2-D Dynamic Programming": [
        (62, "unique-paths"),
        (1143, "longest-common-subsequence"),
        (309, "best-time-to-buy-and-sell-stock-with-cooldown"),
        (518, "coin-change-ii"),
        (494, "target-sum"),
        (97, "interleaving-string"),
        (329, "longest-increasing-path-in-a-matrix"),
        (115, "distinct-subsequences"),
        (72, "edit-distance"),
        (312, "burst-balloons"),
        (10, "regular-expression-matching"),
    ],
    "Greedy": [
        (53, "maximum-subarray"),
        (55, "jump-game"),
        (45, "jump-game-ii"),
        (134, "gas-station"),
        (846, "hand-of-straights"),
        (1899, "merge-triplets-to-form-target-triplet"),
        (763, "partition-labels"),
        (678, "valid-parenthesis-string"),
    ],
    "Intervals": [
        (57, "insert-interval"),
        (56, "merge-intervals"),
        (435, "non-overlapping-intervals"),
        (252, "meeting-rooms"),
        (253, "meeting-rooms-ii"),
        (1851, "minimum-interval-to-include-each-query"),
    ],
    "Math & Geometry": [
        (48, "rotate-image"),
        (54, "spiral-matrix"),
        (73, "set-matrix-zeroes"),
        (202, "happy-number"),
        (66, "plus-one"),
        (50, "powx-n"),
        (43, "multiply-strings"),
        (2013, "detect-squares"),
    ],
    "Bit Manipulation": [
        (136, "single-number"),
        (191, "number-of-1-bits"),
        (338, "counting-bits"),
        (190, "reverse-bits"),
        (268, "missing-number"),
        (371, "sum-of-two-integers"),
        (7, "reverse-integer"),
    ],
    "Tries": [
        (208, "implement-trie-prefix-tree"),
        (211, "design-add-and-search-words-data-structure"),
        (212, "word-search-ii"),
    ],
}

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_solved_neetcode_slugs() -> set:
    """
    Scan repo root for folders named like '####-slug' and return a set
    of all slug parts (the part after the leading digits and dash).
    """
    solved = set()
    try:
        for entry in os.scandir(REPO_ROOT):
            if entry.is_dir():
                name = entry.name
                m = re.match(r"^(\d{4})-(.+)$", name)
                if m:
                    slug = m.group(2)
                    solved.add(slug)
    except Exception as e:
        print(f"Warning: could not scan repo root for NeetCode slugs: {e}")
    return solved


def build_neetcode_block(solved_slugs: set) -> str:
    """Build the NeetCode 150 progress table."""
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    total_solved = 0
    total_problems = 0

    rows = []
    for category, problems in NEETCODE_150.items():
        cat_total = len(problems)
        cat_solved = sum(1 for (_, slug) in problems if slug in solved_slugs)
        total_solved += cat_solved
        total_problems += cat_total

        if cat_solved == cat_total:
            status = f"✅ Complete ({cat_solved}/{cat_total})"
        elif cat_solved > 0:
            status = f"🔄 In Progress ({cat_solved}/{cat_total})"
        else:
            status = f"⏳ Upcoming (0/{cat_total})"

        rows.append(f"| {category} | {status} |")

    overall_pct = (total_solved / total_problems * 100) if total_problems > 0 else 0.0
    overall_bar = make_bar(total_solved, total_problems, width=20)

    lines = [
        f"**Overall: {total_solved} / {total_problems} solved ({overall_pct:.1f}%)** &nbsp; {overall_bar}",
        "",
        "| Category | Status |",
        "|----------|--------|",
    ] + rows + [
        "",
        f"<!-- neetcode-updated: {now} -->",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# README rewriter
# ---------------------------------------------------------------------------

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")

# Markers that wrap the auto-generated sections in the README.
START_MARKER = "<!-- PROGRESS_TRACKER_START -->"
END_MARKER = "<!-- PROGRESS_TRACKER_END -->"
NC_START_MARKER = "<!-- NEETCODE_150_START -->"
NC_END_MARKER = "<!-- NEETCODE_150_END -->"


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


def _replace_between_markers(content: str, start: str, end: str, new_block: str) -> str:
    """Replace or insert content between two HTML comment markers."""
    new_section = f"{start}\n{new_block}\n{end}"

    if start in content and end in content:
        pattern = re.compile(
            re.escape(start) + r".*?" + re.escape(end),
            re.DOTALL,
        )
        return pattern.sub(new_section, content)

    # Markers missing - try to insert after the matching heading
    if start == START_MARKER:
        heading_pattern = re.compile(r"(##\s*📊\s*Progress Tracker\s*\n)")
    else:
        heading_pattern = re.compile(r"(##\s*NeetCode 150 Progress\s*\n)")

    if heading_pattern.search(content):
        return heading_pattern.sub(
            r"\1" + new_section + "\n\n", content, count=1
        )

    # Fallback: append at end
    return content.rstrip() + "\n\n" + new_section + "\n"


def update_readme(solved: dict, total: dict, solved_slugs: set):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update general progress tracker
    tracker_block = build_tracker_block(solved, total)
    content = _replace_between_markers(content, START_MARKER, END_MARKER, tracker_block)

    # 2. Update NeetCode 150 tracker
    neetcode_block = build_neetcode_block(solved_slugs)
    content = _replace_between_markers(content, NC_START_MARKER, NC_END_MARKER, neetcode_block)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

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

    print("Scanning repo for NeetCode 150 solved problems...")
    solved_slugs = get_solved_neetcode_slugs()
    print(f"NeetCode 150 slugs found: {len(solved_slugs)}")

    update_readme(solved, total, solved_slugs)


if __name__ == "__main__":
    main()
