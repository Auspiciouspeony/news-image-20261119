# Thursday 19 November 2026: 45 stories, six continents, one front page

One image that sums up Thursday 19 November 2026's world news, for
make.fun's "Sum up 19 November's world news in one image" bounty.

## The page

A newspaper front page, drawn from scratch with Pillow
(`build_image.py`, standard library plus PIL):

- **Masthead** — "Thursday 19 November 2026", with the rule that
  every story on the page happened, or was first reported, on that day.
- **Hero row** — the trilateral in Shenzhen (Trump, Xi and Putin),
  the Fed minutes, and **GTA VI launches today**: the day's most
  recognisable event, so it leads the hero row in v5 with a neon
  Leonida skyline and a giant pink VI.
- **Ten more features** — Gaza, cyclone Akvan, Odesa, the Sudan
  blackout, Voyager 1 at one light-day, COP31, Walmart, India–Japan
  defence talks, Nvidia pay rises, and the Anthropic IPO at $83.
- **By the numbers** — gold $3,725, the $81.3bn IPO, 9.69m GTA VI
  pre-orders, 204,070 people moving ahead of Akvan.
- **Where it happened** — a dotted world map with numbered dots for
  the 13 features, and 32 one-line briefs (stories 14–45), from oil
  and Bitcoin to the Kuwait strike, first reported overnight into
  19 November.
- **Date check** — stories reported on 17–18 November are named and
  left out, so nothing on the page is yesterday's news.

## Files

- `entry.png` — the finished page: 1024×1024, JPEG bytes, under 1 MiB.
- `build_image.py` — draws the page; run `python3 build_image.py`.
- `main.ts` — the entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` and verifies it is 1024×1024 and under 1 MiB.
  Run it with `MAKEFUN_OUTPUT_DIR=out node main.ts`.

## Facts

All 45 stories were checked against reporting of 19 November 2026
(Reuters, AP, BBC, Bloomberg, Fed, IMD, NASA, UN, IAEA, Rockstar
Games, Take-Two). The pictures are original drawings, not photos.
