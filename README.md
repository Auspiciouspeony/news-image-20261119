# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Auspiciouspeony/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Auspiciouspeony/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of Thursday 19 November 2026:
45 stories — 13 pictured features, 32 briefs, a world map, a numbers
strip and a date check — on a single front page. Every story on the page
happened, or was first reported, on that day. Three leaders meet in
Shenzhen, GTA VI launches, and the biggest IPO ever debuts.

`build_image.py` draws the page from scratch with Pillow (original
drawings, no photos). `main.ts` copies the rendered `entry.png` to the
output directory and checks it is 1024x1024 and under 1 MiB.

## Run it

```sh
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
