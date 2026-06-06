# 🧩 LeetCode Sync — Kavya Agar

> Automatically syncing my LeetCode solutions to GitHub via GitHub Actions. Every accepted submission gets committed here so I have a clean, version-controlled record of my progress.

---

## 👋 About Me

Hey! I'm **Kavya** — a Computer Science student at **Texas A&M University** (graduating May 2027). I'm passionate about building things that matter, whether that's full-stack apps, ML pipelines, or distributed systems. I've had the chance to work at JPMorgan Chase and AspenTech, and I'm always chasing the next challenge.

When I'm not building projects or studying, I'm grinding LeetCode — trying to sharpen the problem-solving instincts that make a real difference in technical interviews and on the job.

📍 Houston, TX &nbsp;|&nbsp; 🌐 [kavyaagar.com](https://www.kavyaagar.com) &nbsp;|&nbsp; 💼 [LinkedIn](https://linkedin.com/in/kavya-agar) &nbsp;|&nbsp; 🐙 [GitHub](https://github.com/Kavya-Agar)

---

## 🚀 My LeetCode Journey

I came into LeetCode with a solid CS foundation — data structures, algorithms, Java, Python, C++ — but knowing theory and actually solving problems under pressure are two very different things. This repo is my commitment to showing up consistently and building that muscle.

Right now I'm working through the **[NeetCode 150](https://neetcode.io/practice)** — a curated list of the most important LeetCode problems covering every major topic you'd encounter in a technical interview. The goal isn't just to memorize solutions; it's to internalize patterns so I can tackle anything thrown at me.

### 🎯 Goals
- ✅ Complete the NeetCode 150
- 🔄 Build a consistent daily practice habit
- 📈 Progress from Easy → Medium → Hard
- 💼 Be fully interview-ready for internship & new grad roles

---

## 📊 Progress Tracker
<!-- PROGRESS_TRACKER_START -->
_Last updated automatically on each sync. Stats pulled from my [LeetCode profile](https://leetcode.com/u/c9reTYFM0W/)._

| Difficulty | Solved | Total | Progress |
|-----------|--------|-------|----------|
| U0001f7e2 Easy | 19 | 947 | ░░░░░░░░░░ 2.0% |
| U0001f7e1 Medium | 13 | 2063 | ░░░░░░░░░░ 0.6% |
| U0001f534 Hard | 0 | 939 | ░░░░░░░░░░ 0.0% |
| **Total** | **32** | **3949** | ░░░░░░░░░░ 0.8% |

<!-- updated: 2026-06-06 10:01 UTC -->
<!-- PROGRESS_TRACKER_END -->
### NeetCode 150 Progress
<!-- NEETCODE_150_START -->
**Overall: 14 / 149 solved (9.4%)** &nbsp; ██░░░░░░░░░░░░░░░░░░ 9.4%

| Category | Status |
|----------|--------|
| Arrays & Hashing | U0001f504 In Progress (6/9) |
| Two Pointers | U0001f504 In Progress (2/5) |
| Sliding Window | U0001f504 In Progress (2/6) |
| Stack | ⏳ Upcoming (0/7) |
| Binary Search | ⏳ Upcoming (0/7) |
| Linked List | U0001f504 In Progress (1/10) |
| Trees | U0001f504 In Progress (2/15) |
| Heap / Priority Queue | ⏳ Upcoming (0/7) |
| Backtracking | ⏳ Upcoming (0/9) |
| Graphs | ⏳ Upcoming (0/13) |
| Advanced Graphs | ⏳ Upcoming (0/6) |
| 1-D Dynamic Programming | ⏳ Upcoming (0/12) |
| 2-D Dynamic Programming | ⏳ Upcoming (0/11) |
| Greedy | ⏳ Upcoming (0/8) |
| Intervals | ⏳ Upcoming (0/6) |
| Math & Geometry | ⏳ Upcoming (0/8) |
| Bit Manipulation | U0001f504 In Progress (1/7) |
| Tries | ⏳ Upcoming (0/3) |

<!-- neetcode-updated: 2026-06-06 10:01 UTC -->
<!-- NEETCODE_150_END -->
---

## ⚙️ How the Sync Works

This repo uses a GitHub Action to automatically pull my accepted LeetCode submissions and commit them here. No manual copy-pasting needed.

### What it does
- Fetches **only accepted solutions** from LeetCode
- Skips anything already synced — no duplicate commits
- If I submitted multiple solutions for the same problem in one day, it keeps the **latest accepted one**
- Commits solutions to the `main` branch with a timestamped commit message

### How it's triggered
The workflow runs in two ways:

1. **On a schedule** — automatically every Saturday at 8:00 AM UTC
2. **Manually** — via the [Actions tab](../../actions) → *Sync Leetcode* → *Run workflow*

### Workflow file
```yaml
name: Sync Leetcode

on:
  workflow_dispatch:
  schedule:
    - cron: "0 8 * * 6"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Sync
        uses: leetcode-sync-action@latest
        with:
          github-token: ${{ github.token }}
          leetcode-csrf-token: ${{ secrets.LEETCODE_CSRF_TOKEN }}
          leetcode-session: ${{ secrets.LEETCODE_SESSION }}
```

### Required secrets
| Secret | Description |
|--------|-------------|
| `LEETCODE_CSRF_TOKEN` | Your LeetCode `csrftoken` cookie |
| `LEETCODE_SESSION` | Your LeetCode `LEETCODE_SESSION` cookie |

> ⚠️ LeetCode session cookies expire periodically. If the workflow fails with an auth error, grab fresh cookie values from your browser's DevTools (Application → Cookies → leetcode.com) and update the secrets in Settings → Secrets and variables → Actions.

---

## 📁 Repo Structure

```
leetcode-sync/
├── .github/
│   └── workflows/
│       └── sync_leetcode.yml   # GitHub Actions workflow
├── README.md                   # You are here
└── <problem-slug>/             # Auto-created folders per problem
    └── solution.<ext>          # Your accepted solution
```

---

*Built with 💙 and a lot of coffee. Let's get these offers.*
