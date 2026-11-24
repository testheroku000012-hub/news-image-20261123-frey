# THE WORLD TODAY — news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/testheroku000012-hub/news-image-20261123-frey/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/testheroku000012-hub/news-image-20261123-frey/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One front page summing up Monday 23 November 2026: the COP31 collapse in
Antalya, the Friday markets meltdown, the Gulf on edge, and six briefs.
Bounty page: https://make.fun/bounty/news-image-20261123

- `entry.png` — the rendered 1024x1024 front page (drawn at build time).
- `build.py` — the Pillow renderer that draws `entry.png` (build-time only).
- `main.py` — the entry point: stdlib-only, validates the PNG header and
  copies `entry.png` to `MAKEFUN_OUTPUT_DIR`.

Build: `python3 build.py` (needs Pillow, local build machine only).
Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`.
