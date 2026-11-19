# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Auspiciouspeony/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Auspiciouspeony/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Thursday 19 November 2026 in one front page: 45 stories, six continents.
Trump, Xi and Putin meet in Shenzhen; Fed minutes point to more hikes;
Anthropic prices its IPO at $83; Israeli tanks push deeper into Gaza;
Cyclone Akvan nears the Indian coast; Voyager 1 reaches one light-day;
and GTA VI launches at midnight, rolling out from New Zealand. Thirteen
illustrated features, a by-the-numbers strip, a dotted world map and
32 numbered briefs — every story happened, or was first reported,
on Thursday 19 November 2026.

## Run it

```sh
python3 build_image.py            # draws entry.png (1024x1024, <1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

`build_image.py` draws everything with Pillow from geometric shapes and
type alone — no photos, no network — and checks itself as it goes: every
headline and deck wraps to at most two lines, every brief fits one line,
and the page stays inside the 1024x1024 canvas.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
