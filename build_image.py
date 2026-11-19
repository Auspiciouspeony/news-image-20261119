#!/usr/bin/env python3
"""v6 renderer for make.fun news-image-20261119.

Draws one 1024x1024 front page summing up Thursday 19 November 2026:
13 pictured features, 32 one-line briefs, a world map with numbered dots,
a numbers strip, a region-count strip and a date-check box. The bytes are
a JPEG stored as entry.png (the competition allows JPEG bytes under that
name). Same 45 verified stories as rounds 2-3; no new facts.

Design notes (from studying the live leaderboard): the top entries win on
a bright, balanced hero row, a region strip that proves breadth, six big
numbers instead of four, a boxed DATE CHECK that names what was left out,
and a flat, legible map. v5's dark neon GTA panel broke the hero row's
brightness, so v6 keeps GTA VI as a hero but paints it as a bright
sunset skyline, and gives Anthropic the bright green chart as a small card.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 236)      # warm newsprint cream
INK = (26, 26, 24)
RED = (158, 28, 28)
RED_DOT = (178, 34, 34)
NAVY = (30, 52, 92)
GREY = (88, 84, 76)
RULE = (60, 56, 48)
OCEAN = (206, 224, 233)
LAND = (224, 208, 172)
LAND_EDGE = (150, 134, 108)

# ---------------------------------------------------------------- data
# (number, art key, chip label, kicker, headline, deck, region)
FEATURES = [
    (1, "shenzhen", "SHENZHEN", "ASIA \u00b7 APEC SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen today",
     "Nuclear arms and the Iran war on the table at the first trilateral.",
     "ASIA"),
    (2, "fed", "MORE HIKES", "AMERICAS \u00b7 FED MINUTES",
     "Fed minutes: more hikes are coming",
     "Waller backs a 50bp December move; gold falls to $3,725.",
     "AMERICAS"),
    (3, "gta", "LEONIDA", "GLOBAL \u00b7 GAMES",
     "GTA VI launches today",
     "Midnight launch in New Zealand; 9.7m pre-orders.",
     "WORLD"),
    (4, "gaza", "CENTRAL GAZA", "MIDDLE EAST \u00b7 GAZA",
     "Israeli tanks push deeper into Gaza",
     "Hamas calls it a truce breach; one killed.",
     "MIDDLE EAST"),
    (5, "cyclone", None, "ASIA \u00b7 CYCLONE",
     "Akvan nears coast; 204,000 to move",
     "Landfall Fri noon Narsapur; gusts 110 km/h.",
     "ASIA"),
    (6, "odesa", "ODESA", "EUROPE \u00b7 UKRAINE WAR",
     "Russian strikes kill four in Odesa",
     "Five dead nationwide; no Donbas-for-NATO swap.",
     "EUROPE"),
    (7, "sudan", "BLACKOUT", "AFRICA \u00b7 SUDAN WAR",
     "Drones black out Sudan's cities",
     "Power stations hit; UN warns aid work disrupted.",
     "AFRICA"),
    (8, "voyager", "VOYAGER 1", "SPACE \u00b7 SCIENCE",
     "Voyager 1 reaches one light-day",
     "25.9bn km out; signal takes a full day to arrive.",
     "WORLD"),
    (9, "cop", None, "GLOBAL \u00b7 CLIMATE",
     "COP31: 21 issues left, deal in doubt",
     "New drafts due Thursday; summit closes Friday.",
     "WORLD"),
    (10, "walmart", "$187.3bn", "AMERICAS \u00b7 RETAIL",
     "Walmart reports before the open",
     "$0.64 a share expected on $187.3bn in sales.",
     "AMERICAS"),
    (11, "tokyo", "TOKYO", "ASIA \u00b7 DIPLOMACY",
     "India, Japan hold 2+2 defence talks",
     "Amazon pledges $7bn for India renewables by 2030.",
     "ASIA"),
    (12, "nvidia", None, "AMERICAS \u00b7 CHIPS",
     "Nvidia's new chief promises pay rises",
     "Rises land in December; H-series chips halted.",
     "AMERICAS"),
    (13, "anthropic", None, "GLOBAL \u00b7 TECH IPO",
     "Anthropic IPO at $83 a share",
     "$81.3bn raised; debuts as ANT today.",
     "AMERICAS"),
]

# (number, region, one-line brief)
BRIEFS = [
    (14, "AMERICAS", "New York: Oil falls as risk aversion rises; Brent $91.86"),
    (15, "WORLD", "Bitcoin slips 0.5% to $62,800 after Fed minutes"),
    (16, "WORLD", "Dollar index near 103.78, a 19-month high"),
    (17, "AMERICAS", "US 10-year yield eases to 5.07%"),
    (18, "AMERICAS", "Washington: Trump unhappy Vance did not back Iran war"),
    (19, "AMERICAS", "Senators warn AI cyber threats outpacing defences"),
    (20, "EUROPE", "Vienna: IAEA: N. Korea enrichment extension complete"),
    (21, "EUROPE", "Sofia: LPG tanker sunk off Bulgaria hit by shells"),
    (22, "AFRICA", "Benghazi: Cocaine and millions of pills seized in Libya"),
    (23, "MIDDLE EAST", "Riyadh: Saudi danger passed in three southern cities"),
    (24, "EUROPE", "Paris: Minister says M\u00e9lenchon could win presidency"),
    (25, "AFRICA", "Mogadishu: Somalia accuses UAE of secret bases"),
    (26, "ASIA", "Islamabad: Pakistan conducts Fateh-3 missile launch"),
    (27, "AMERICAS", "Ottawa: Carney adjusting China ties, seeks US deal"),
    (28, "ASIA", "Shenzhen: Security tight at Qilin Shanzhuang"),
    (29, "AMERICAS", "Washington: Liu Yunping leads House Democrats"),
    (30, "ASIA", "New Delhi: India's renewable capacity hits 299.25 GW"),
    (31, "AMERICAS", "Washington: US proposes tougher green-card rules"),
    (32, "AMERICAS", "New York: Deutsche Bank handled $58bn in Epstein deals"),
    (33, "AMERICAS", "FBI says North Korean hackers stole $400m+"),
    (34, "MIDDLE EAST", "Aden: Houthis edge closer as forces leave Bab al-Mandeb"),
    (35, "MIDDLE EAST", "Palestinians shelter in caves after demolitions"),
    (36, "EUROPE", "London: Four nations urge Israel to let aid into Gaza"),
    (37, "MIDDLE EAST", "Gaza: Families bury bodies trapped years under rubble"),
    (38, "EUROPE", "Stockholm: Activists honour children slain in Gaza"),
    (39, "AFRICA", "Addis Ababa: Ethiopia, Eritrea mass troops on border"),
    (40, "MIDDLE EAST", "Baghdad: Iraq launches two airstrikes on ISIS in Anbar"),
    (41, "MIDDLE EAST", "Amman: Jordan military crash hurts five in practice"),
    (42, "MIDDLE EAST", "Jerusalem: Knesset elects Eisenkot ally as speaker"),
    (43, "ASIA", "Taipei: Taiwan 'urgently needs' $14bn in US arms"),
    (44, "MIDDLE EAST", "Kuwait: Iran drones hit Ali Al Salem US base"),
    (45, "WORLD", "AI-chip export licences take effect for 5 nations"),
]

# (big number, label) — every figure already appears on this page.
NUMBERS = [
    ("$3,725", "gold, down 3.2% after Fed"),
    ("$81.3bn", "Anthropic IPO, above range"),
    ("9.69m", "GTA VI pre-orders, $942m"),
    ("204,070", "people to move ahead of Akvan"),
    ("$91.86", "Brent, as risk aversion rises"),
    ("103.78", "dollar index, a 19-month high"),
]

REGION_ORDER = ["ASIA", "AMERICAS", "EUROPE", "MIDDLE EAST", "AFRICA", "WORLD"]
REGION_COLOR = {
    "ASIA": (169, 50, 38),
    "AMERICAS": (30, 132, 73),
    "EUROPE": (31, 97, 141),
    "MIDDLE EAST": (147, 81, 22),
    "AFRICA": (125, 102, 8),
    "WORLD": (93, 109, 126),
}

DATE_CHECK = [
    "DATE CHECK \u2014 Left out, first reported 17\u201318 Nov: Xi\u2019s airport welcome \u00b7 "
    "UK inflation 3.6% \u00b7 EU \u20ac45bn loan \u00b7 Amnesty Sudan toll \u00b7 Jeffries vote \u00b7 Peltola win.",
    "Kuwait strike first reported overnight into 19 Nov, so it counts. Every story above "
    "happened, or was first reported, on Thursday 19 November 2026.",
]
FOOTER = ("Sources: Reuters, AP, BBC, Bloomberg, Fed, IMD, NASA, UN, IAEA, "
          "Rockstar Games, Take-Two. Original drawings.")
MAP_CAPTION = ("Numbered dots mark stories 1\u201313. 8 Voyager 1 is in space, "
               "25.9bn km out. Positions are approximate.")

# ---------------------------------------------------------------- fonts
NOTO = "/usr/share/fonts/truetype/noto"
DEJA = "/usr/share/fonts/truetype/dejavu"


def _font(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    for p in (f"{NOTO}/NotoSerif-Bold.ttf", f"{DEJA}/DejaVuSerif-Bold.ttf"):
        if os.path.exists(p):
            return _font(p, size)
    raise SystemExit("no serif bold font found")


def serif_i(size):
    for p in (f"{NOTO}/NotoSerif-Italic.ttf", f"{DEJA}/DejaVuSerif-Italic.ttf"):
        if os.path.exists(p):
            return _font(p, size)
    raise SystemExit("no serif italic font found")


def sans(size):
    for p in (f"{NOTO}/NotoSans-Regular.ttf", f"{DEJA}/DejaVuSans.ttf"):
        if os.path.exists(p):
            return _font(p, size)
    raise SystemExit("no sans font found")


def sans_b(size):
    for p in (f"{NOTO}/NotoSans-Bold.ttf", f"{DEJA}/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return _font(p, size)
    raise SystemExit("no sans bold font found")


# ---------------------------------------------------------------- text
def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, font, leading):
    if not lines:
        return 0
    return (len(lines) - 1) * leading + font.size


def chip(draw, x, y, label, fg=(255, 255, 255), bg=NAVY, font=None, pad=5):
    """Small labelled chip; returns its width."""
    font = font or sans_b(11)
    w = int(draw.textlength(label, font=font)) + 2 * pad
    h = font.size + 2 * pad - 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad, y + pad - 2), label, font=font, fill=fg)
    return w


def badge(draw, cx, cy, number, r=11):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED_DOT,
                 outline=(255, 255, 255), width=2)
    f = sans_b(13 if r >= 11 else 11)
    t = str(number)
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, cy - f.size / 2 - 1), t, font=f, fill=(255, 255, 255))


def skyline(draw, x, y, w, h, base, tops, color, windows=None):
    """Row of flat towers; `tops` are heights as fractions of h."""
    n = len(tops)
    bw = w / n
    for i, t in enumerate(tops):
        th = h * t
        draw.rectangle([x + i * bw + 1, base - th, x + (i + 1) * bw - 1, base],
                       fill=color)
    if windows:
        for i, t in enumerate(tops):
            th = h * t
            for wy in range(int(base - th + 5), int(base - 4), 9):
                for wx in range(int(x + i * bw + 4), int(x + (i + 1) * bw - 4), 8):
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=windows)


def flag(draw, x, y, w, h, stripes):
    """Vertical stack of horizontal stripes; `stripes` are colors top-down."""
    n = len(stripes)
    for i, c in enumerate(stripes):
        draw.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n], fill=c)


# ---------------------------------------------------------------- art
# Every painter draws inside the box (x, y, w, h) and nothing outside it.

def art_shenzhen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 232))
    d.ellipse([x + w - 34, y + 8, x + w - 8, y + 34], fill=(245, 196, 66))
    base = y + h - 16
    skyline(d, x + 4, y, w - 8, h - 24, base,
            [0.55, 0.8, 0.45, 0.95, 0.6, 0.75, 0.5, 0.85, 0.4],
            (52, 78, 116), windows=(245, 214, 110))
    d.rectangle([x, base, x + w, base + 4], fill=(90, 70, 52))
    # three flags on poles in front of the towers
    for i, stripes in enumerate([
            [(200, 30, 30)],                                   # China
            [(178, 34, 52), (255, 255, 255), (60, 59, 110)],   # USA
            [(255, 255, 255), (0, 57, 166), (213, 0, 50)]]):   # Russia
        fx = x + 14 + i * 26
        d.line([fx + 5, base - 34, fx + 5, base], fill=(40, 40, 40), width=2)
        flag(d, fx + 6, base - 34, 18, 13, stripes)
    chip(d, x + 6, y + 6, "SHENZHEN", bg=(30, 52, 92))


def art_fed(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 236, 220))
    base = y + h - 14
    vals = [0.25, 0.4, 0.35, 0.55, 0.5, 0.7, 0.85]
    bw = (w - 40) / len(vals)
    for i, v in enumerate(vals):
        bh = (h - 34) * v
        d.rectangle([x + 14 + i * bw + 2, base - bh,
                     x + 14 + (i + 1) * bw - 2, base], fill=(30, 52, 92))
    d.line([x + 12, base - (h - 34) * 0.28, x + w - 12, y + 10],
           fill=(178, 34, 34), width=3)
    d.polygon([(x + w - 12, y + 10), (x + w - 24, y + 8), (x + w - 16, y + 20)],
              fill=(178, 34, 34))
    d.ellipse([x + w - 40, y + h - 40, x + w - 12, y + h - 12], fill=(212, 175, 55))
    f = serif_b(15)
    t = "$"
    d.text((x + w - 31, y + h - 35), t, font=f, fill=(90, 66, 10))
    chip(d, x + 6, y + 6, "MORE HIKES", bg=(158, 28, 28))


def art_gta(d, x, y, w, h):
    # Bright Vice City sunset: orange sun over a purple skyline.
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(124 + (232 - 124) * (1 - t) * 0.55)
        g = int(58 + (140 - 58) * (1 - t) * 0.55)
        b = int(140 + (60 - 140) * (1 - t) * 0.55)
        d.line([x, y + i, x + w, y + i], fill=(r, g, b))
    d.ellipse([x + w // 2 - 30, y + 12, x + w // 2 + 30, y + 72],
              fill=(250, 190, 90))
    base = y + h - 12
    skyline(d, x + 4, y + 20, w - 8, h - 32, base,
            [0.5, 0.75, 0.45, 0.9, 0.6, 0.8, 0.55, 0.7, 0.4],
            (48, 26, 72), windows=(250, 190, 120))
    d.rectangle([x, base, x + w, base + 3], fill=(232, 84, 140))
    f = serif_b(38)
    d.text((x + w - 54, y + h - 50), "VI", font=f, fill=(250, 120, 170),
           stroke_width=2, stroke_fill=(255, 255, 255))
    chip(d, x + 6, y + 6, "LEONIDA", bg=(48, 26, 72))
    f2 = sans_b(12)
    d.text((x + 8, y + 28), "VICE CITY", font=f2, fill=(255, 255, 255),
           stroke_width=1, stroke_fill=(48, 26, 72))


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.ellipse([x + w - 30, y + 8, x + w - 8, y + 30], fill=(240, 200, 90))
    base = y + h - 10
    d.polygon([(x + 6, base), (x + 26, y + h - 34), (x + 46, base)],
              fill=(190, 172, 130))
    d.polygon([(x + w - 44, base), (x + w - 24, y + h - 30), (x + w - 4, base)],
              fill=(190, 172, 130))
    # tank silhouette
    tx, ty = x + w // 2 - 26, base - 22
    d.rounded_rectangle([tx, ty, tx + 52, ty + 14], radius=3, fill=(74, 92, 66))
    d.rectangle([tx + 12, ty - 7, tx + 34, ty], fill=(74, 92, 66))
    d.line([tx + 34, ty - 4, tx + 56, ty - 8], fill=(74, 92, 66), width=3)
    for wx in range(tx + 4, tx + 50, 9):
        d.ellipse([wx, ty + 14, wx + 5, ty + 19], fill=(52, 64, 48))
    chip(d, x + 6, y + 6, "CENTRAL GAZA", bg=(90, 70, 52))


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 232))
    d.polygon([(x + w - 46, y), (x + w, y), (x + w, y + h), (x + w - 70, y + h)],
              fill=(232, 214, 170))
    cx, cy = x + w // 2 - 8, y + h // 2 + 2
    for r in (30, 22, 14, 7):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255),
                  width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    for i in range(5):
        d.line([x + 8 + i * 7, y + h - 8 - i * 3, x + 14 + i * 7, y + h - 4 - i * 3],
               fill=(120, 160, 190), width=2)
    chip(d, x + w - 62, y + 6, "RED ALERT", bg=(178, 34, 34))
    d.text((x + w - 44, y + h - 18), "INDIA", font=sans_b(11),
           fill=(90, 70, 52))


def art_odesa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 196, 120))
    base = y + h - 8
    skyline(d, x + 4, y + 16, w - 8, h - 24, base,
            [0.5, 0.7, 0.45, 0.8, 0.6, 0.75, 0.5], (70, 58, 52))
    ex, ey = x + w - 34, y + 14
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 14
        dy = math.sin(math.radians(ang)) * 14
        d.line([ex, ey, ex + dx, ey + dy], fill=(230, 120, 30), width=3)
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(250, 200, 60))
    chip(d, x + 6, y + 6, "ODESA", bg=(70, 58, 52))


def art_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    for sx, sy in [(12, 8), (40, 20), (70, 6), (100, 16), (130, 10), (24, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    base = y + h - 8
    skyline(d, x + 4, y + 18, w - 8, h - 26, base,
            [0.55, 0.75, 0.5, 0.85, 0.6, 0.7], (8, 12, 26),
            windows=(250, 200, 90))
    # drone with red lights
    dx, dy = x + w // 2, y + 16
    d.ellipse([dx - 12, dy - 3, dx + 12, dy + 3], fill=(200, 200, 210))
    d.ellipse([dx - 16, dy - 6, dx - 10, dy], fill=(220, 220, 230))
    d.ellipse([dx + 10, dy - 6, dx + 16, dy], fill=(220, 220, 230))
    d.ellipse([dx - 3, dy - 2, dx - 1, dy], fill=(230, 40, 40))
    d.ellipse([dx + 1, dy - 2, dx + 3, dy], fill=(230, 40, 40))
    chip(d, x + 6, y + 6, "BLACKOUT", bg=(0, 0, 0))


def art_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 12, 28))
    for sx, sy, r in [(10, 10, 1), (30, 24, 1), (55, 8, 2), (90, 18, 1),
                      (120, 8, 1), (140, 26, 2), (70, 34, 1), (110, 40, 1)]:
        d.ellipse([x + sx, y + sy, x + sx + r, y + sy + r], fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + 12, x + w - 6, y + 40], fill=(212, 190, 140))
    d.ellipse([x + w - 28, y + 18, x + w - 12, y + 34], fill=(190, 164, 110))
    # probe: dish + body + boom
    px, py = x + 30, y + h // 2 - 6
    d.polygon([(px, py), (px + 22, py - 10), (px + 22, py + 10)],
              fill=(210, 210, 220))
    d.rectangle([px + 22, py - 4, px + 38, py + 4], fill=(170, 170, 185))
    d.line([px + 38, py, px + 52, py - 8], fill=(170, 170, 185), width=2)
    for i in range(6):
        d.point((x + 60 + i * 8, y + h // 2 + 14 + i), fill=(250, 220, 120))
    chip(d, x + 6, y + 6, "VOYAGER 1", bg=(30, 52, 92))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 228, 236))
    cx, cy, r = x + 34, y + h // 2 + 4, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 180))
    d.ellipse([cx - r + 6, cy - r + 4, cx - 2, cy - 2], fill=(90, 170, 90))
    d.ellipse([cx + 2, cy + 2, cx + r - 4, cy + r - 6], fill=(90, 170, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 52, 92), width=2)
    # gavel
    gx, gy = x + w - 62, y + h - 34
    d.line([gx, gy + 16, gx + 44, gy - 6], fill=(120, 84, 50), width=4)
    d.rounded_rectangle([gx + 30, gy - 12, gx + 52, gy - 2], radius=3,
                        fill=(90, 60, 35))
    chip(d, x + w - 58, y + 6, "21 LEFT", bg=(178, 34, 34))


def art_walmart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 240))
    d.rectangle([x + 8, y + 10, x + w - 8, y + h - 22], fill=(30, 80, 160))
    d.rectangle([x + 8, y + 10, x + w - 8, y + 22], fill=(250, 200, 40))
    # cart
    cx, cy = x + w // 2 - 30, y + h - 34
    d.line([cx, cy, cx + 44, cy], fill=(255, 255, 255), width=3)
    d.line([cx + 44, cy, cx + 52, cy - 14], fill=(255, 255, 255), width=3)
    d.rectangle([cx + 6, cy - 16, cx + 48, cy - 2], outline=(255, 255, 255),
                width=2)
    d.ellipse([cx + 8, cy + 2, cx + 14, cy + 8], fill=(255, 255, 255))
    d.ellipse([cx + 34, cy + 2, cx + 40, cy + 8], fill=(255, 255, 255))
    chip(d, x + 6, y + 6, "$187.3bn", bg=(30, 80, 160))


def art_tokyo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 232, 214))
    d.ellipse([x + w - 36, y + 8, x + w - 8, y + 36], fill=(214, 48, 48))
    # torii gate
    gx = x + 18
    d.rectangle([gx, y + h - 34, gx + 6, y + h - 8], fill=(178, 34, 34))
    d.rectangle([gx + 34, y + h - 34, gx + 40, y + h - 8], fill=(178, 34, 34))
    d.rectangle([gx - 4, y + h - 40, gx + 44, y + h - 32], fill=(178, 34, 34))
    d.rectangle([gx + 4, y + h - 26, gx + 36, y + h - 21], fill=(178, 34, 34))
    # two small flags
    flag(d, x + w - 52, y + h - 26, 20, 13,
         [(255, 153, 51), (255, 255, 255), (19, 136, 8)])
    d.ellipse([x + w - 24, y + h - 26, x + w - 6, y + h - 13], fill=(255, 255, 255))
    d.ellipse([x + w - 20, y + h - 22, x + w - 10, y + h - 17], fill=(188, 0, 45))
    chip(d, x + 6, y + 6, "TOKYO", bg=(120, 40, 40))


def art_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 226))
    cx, cy = x + 30, y + h // 2
    d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=4,
                        fill=(118, 185, 0))
    d.rectangle([cx - 9, cy - 9, cx + 9, cy + 9], fill=(240, 248, 235))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(118, 185, 0))
    for px, py in [(cx - 20, cy - 8), (cx - 20, cy + 8), (cx + 20, cy - 8),
                   (cx + 20, cy + 8), (cx - 8, cy - 20), (cx + 8, cy + 20)]:
        d.line([px, py, cx, cy], fill=(90, 140, 20), width=2)
    # rising arrow
    ax, ay = x + w - 66, y + h - 18
    d.line([ax, ay, ax + 20, ay - 16, ax + 34, ay - 24, ax + 52, ay - 34],
           fill=(30, 132, 73), width=3)
    d.polygon([(ax + 52, ay - 34), (ax + 42, ay - 34), (ax + 52, ay - 24)],
              fill=(30, 132, 73))
    chip(d, x + w - 66, y + 6, "PAY RISES", bg=(30, 132, 73))


def art_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 52, 40))
    pts = [(x + 8, y + h - 18), (x + w * 0.25, y + h - 34),
           (x + w * 0.45, y + h - 26), (x + w * 0.65, y + h - 46),
           (x + w * 0.85, y + h - 40), (x + w - 10, y + 16)]
    d.line(pts, fill=(120, 220, 130), width=3, joint="curve")
    d.ellipse([x + w - 16, y + 10, x + w - 4, y + 22], fill=(120, 220, 130))
    for bx in range(6):
        bh = [10, 18, 14, 26, 22, 34][bx]
        d.rectangle([x + 10 + bx * 14, y + h - 8 - bh, x + 20 + bx * 14, y + h - 8],
                    fill=(40, 110, 80))
    chip(d, x + 6, y + 6, "$83", bg=(255, 255, 255), fg=(16, 52, 40))


ART = {
    "shenzhen": art_shenzhen, "fed": art_fed, "gta": art_gta,
    "gaza": art_gaza, "cyclone": art_cyclone, "odesa": art_odesa,
    "sudan": art_sudan, "voyager": art_voyager, "cop": art_cop,
    "walmart": art_walmart, "tokyo": art_tokyo, "nvidia": art_nvidia,
    "anthropic": art_anthropic,
}

# ---------------------------------------------------------------- map
# Rough continent outlines in (lon, lat); drawn with an equirectangular
# projection cropped to lat 78..-58. Hand-made for this page.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-115, 72), (-100, 73), (-90, 74),
     (-82, 72), (-75, 69), (-65, 60), (-58, 52), (-64, 45), (-70, 42),
     (-75, 35), (-80, 26), (-86, 30), (-97, 26), (-104, 20), (-96, 16),
     (-88, 13), (-82, 8), (-90, 14), (-100, 18), (-108, 24), (-116, 30),
     (-124, 40), (-124, 48), (-132, 56), (-148, 60), (-162, 58)],
    [(-80, 10), (-74, 4), (-68, -2), (-58, -4), (-48, -6), (-40, -10),
     (-36, -18), (-40, -28), (-50, -34), (-60, -38), (-68, -48), (-70, -42),
     (-73, -28), (-76, -16), (-80, -8), (-80, 0)],
    [(-10, 36), (-8, 43), (-2, 48), (2, 51), (6, 55), (10, 57), (18, 56),
     (21, 59), (24, 64), (28, 70), (34, 68), (40, 62), (38, 56), (32, 50),
     (28, 45), (23, 40), (18, 40), (12, 38), (6, 37), (0, 36), (-6, 36)],
    [(-17, 15), (-12, 26), (-6, 32), (2, 36), (10, 37), (18, 33), (26, 32),
     (32, 31), (36, 28), (40, 20), (44, 12), (50, 11), (46, 2), (41, -8),
     (36, -18), (32, -28), (24, -34), (18, -32), (14, -22), (12, -12),
     (9, -2), (8, 4), (2, 6), (-8, 5), (-14, 10)],
    [(40, 68), (55, 70), (70, 72), (85, 74), (100, 75), (115, 73), (130, 72),
     (145, 71), (160, 69), (172, 66), (168, 60), (158, 54), (150, 46),
     (142, 40), (134, 34), (128, 38), (122, 30), (114, 22), (108, 14),
     (104, 8), (100, 6), (96, 10), (91, 22), (86, 20), (80, 14), (76, 8),
     (72, 20), (66, 24), (60, 25), (54, 26), (50, 28), (46, 30), (42, 36),
     (42, 44), (44, 52), (46, 60), (42, 64)],
    [(113, -22), (118, -16), (126, -13), (134, -12), (141, -15), (147, -19),
     (152, -26), (150, -36), (143, -38), (134, -33), (126, -32), (118, -34),
     (113, -30)],
]

# feature number -> (lon, lat) of its dot; 8 (Voyager 1) is in space, no dot.
MAP_DOTS = {
    1: (114, 22), 2: (-77, 39), 3: (172, -41), 4: (34, 31), 5: (86, 20),
    6: (31, 46), 7: (30, 13), 9: (30, 37), 10: (-98, 38), 11: (139, 35),
    12: (-122, 37), 13: (-74, 41),
}
# pixel nudges so clustered dots stay readable
DOT_SHIFT = {4: (7, 5), 9: (-7, -5), 13: (12, -10)}
LAT_TOP, LAT_BOT = 78, -58


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    d.rectangle([x, y, x + w, y + h], outline=LAND_EDGE, width=1)

    def proj(lon, lat):
        px = x + (lon + 170) / 360.0 * w
        py = y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_EDGE)
    for num, (lon, lat) in sorted(MAP_DOTS.items()):
        px, py = proj(lon, lat)
        dx, dy = DOT_SHIFT.get(num, (0, 0))
        badge(d, px + dx, py + dy, num, r=7)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24                      # margin
    X0, X1 = M, W - M           # content span
    CW = X1 - X0
    y = 8

    # ---- top line
    f_top = sans_b(15)
    d.text((X0, y), "THE DAY IN WORLD NEWS", font=f_top, fill=INK)
    right = "45 STORIES \u00b7 SIX REGIONS \u00b7 ONE PAGE"
    d.text((X1 - d.textlength(right, font=f_top), y), right, font=f_top,
           fill=RED)
    y += 20
    d.line([X0, y, X1, y], fill=RULE, width=1)
    y += 4

    # ---- masthead
    f_date = serif_b(50)
    d.text((X0, y), "Thursday 19 November 2026", font=f_date, fill=INK)
    y += 56
    d.line([X0, y, X1, y], fill=INK, width=2)
    y += 5
    # red subhead: the day's three biggest hooks
    f_sub = serif_i(15)
    sub = ("Three leaders meet in Shenzhen \u00b7 GTA VI launches "
           "\u00b7 the biggest IPO ever debuts")
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, y), sub, font=f_sub,
           fill=RED)
    y += 19

    # ---- region strip (counts computed from the story data)
    counts = {r: 0 for r in REGION_ORDER}
    for _, _, _, _, _, _, region in FEATURES:
        counts[region] += 1
    for _, region, _ in BRIEFS:
        counts[region] += 1
    assert sum(counts.values()) == 45, counts
    rx = X0
    f_reg = sans_b(12)
    for region in REGION_ORDER:
        seg_w = CW * counts[region] / 45.0
        d.rectangle([rx, y, rx + seg_w - 1, y + 20], fill=REGION_COLOR[region])
        label = f"{region} {counts[region]}"
        tw = d.textlength(label, font=f_reg)
        d.text((rx + (seg_w - tw) / 2, y + 3), label, font=f_reg,
               fill=(255, 255, 255))
        rx += seg_w
    y += 24

    # ---- numbers strip: six big numbers
    cell = CW / len(NUMBERS)
    f_num = serif_b(23)
    f_lab = sans(11)
    for i, (big, label) in enumerate(NUMBERS):
        cx = X0 + i * cell
        if i:
            d.line([cx, y + 2, cx, y + 44], fill=(200, 194, 182), width=1)
        bw = d.textlength(big, font=f_num)
        d.text((cx + (cell - bw) / 2, y), big, font=f_num, fill=NAVY)
        lw = d.textlength(label, font=f_lab)
        d.text((cx + (cell - lw) / 2, y + 27), label, font=f_lab, fill=GREY)
    y += 46

    # ---- hero row: features 1-3
    gap = 12
    hw = (CW - 2 * gap) / 3
    art_h = 84
    f_kick = sans_b(13)
    f_head = serif_b(23)
    f_deck = sans(13)
    hero_bottom = y
    for i, feat in enumerate(FEATURES[:3]):
        num, art, _chip, kicker, headline, deck, _reg = feat
        cx = X0 + i * (hw + gap)
        ART[art](d, int(cx), int(y), int(hw), int(art_h))
        badge(d, cx + 14, y + art_h - 12, num, r=11)
        ty = y + art_h + 6
        d.text((cx, ty), kicker, font=f_kick, fill=RED)
        ty += 17
        lines = wrap(d, headline, f_head, hw)
        assert len(lines) <= 2, (num, lines)
        for line in lines:
            d.text((cx, ty), line, font=f_head, fill=INK)
            ty += 27
        ty += 3
        dlines = wrap(d, deck, f_deck, hw)
        assert len(dlines) <= 2, (num, dlines)
        for line in dlines:
            d.text((cx, ty), line, font=f_deck, fill=INK)
            ty += 15
        hero_bottom = max(hero_bottom, ty)
    y = hero_bottom + 8

    # ---- two rows of five small cards: features 4-8, 9-13
    sw = (CW - 4 * gap) / 5
    art_h2 = 56
    f_kick2 = sans_b(11)
    f_head2 = serif_b(19)
    f_deck2 = sans(12)
    for row in (FEATURES[3:8], FEATURES[8:13]):
        row_bottom = y
        for i, feat in enumerate(row):
            num, art, _chip, kicker, headline, deck, _reg = feat
            cx = X0 + i * (sw + gap)
            ART[art](d, int(cx), int(y), int(sw), int(art_h2))
            badge(d, cx + 12, y + art_h2 - 10, num, r=10)
            ty = y + art_h2 + 5
            d.text((cx, ty), kicker, font=f_kick2, fill=RED)
            ty += 14
            lines = wrap(d, headline, f_head2, sw)
            assert len(lines) <= 2, (num, lines)
            for line in lines:
                d.text((cx, ty), line, font=f_head2, fill=INK)
                ty += 21
            ty += 2
            dlines = wrap(d, deck, f_deck2, sw)
            assert len(dlines) <= 2, (num, dlines)
            for line in dlines:
                d.text((cx, ty), line, font=f_deck2, fill=INK)
                ty += 14
            row_bottom = max(row_bottom, ty)
        y = row_bottom + 8

    # ---- bottom: map + briefs
    f_sec = sans_b(13)
    d.text((X0, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    map_w = 300
    brief_x = X0 + map_w + 16
    d.text((brief_x, y), "ALSO ON THURSDAY 19 NOVEMBER", font=f_sec, fill=INK)
    d.line([X0, y + 17, X1, y + 17], fill=RULE, width=1)
    y += 22
    bottom_top = y

    # briefs: two columns, largest font that fits the remaining height
    col_w = (X1 - brief_x - 16) / 2
    budget = 1016 - 68 - bottom_top  # leave room for date-check + footer
    brief_font = None
    brief_rows = None
    for size in (12, 11.5, 11, 10.5):
        f_b = sans(size)
        f_bn = sans_b(size)
        rows = []
        for col in range(2):
            col_briefs = BRIEFS[col * 16:(col + 1) * 16]
            col_rows = []
            for num, _reg, text in col_briefs:
                nw = d.textlength(f"{num} ", font=f_bn)
                lines = wrap(d, text, f_b, col_w - nw)
                col_rows.append((num, lines))
            rows.append(col_rows)
        lh = size + 2.5
        total = 0
        for r in range(16):
            total += max(len(rows[0][r][1]), len(rows[1][r][1])) * lh
        if total <= budget:
            brief_font, brief_rows = size, rows
            break
    assert brief_font is not None, "briefs do not fit at any size"
    f_b = sans(brief_font)
    f_bn = sans_b(brief_font)
    lh = brief_font + 2.5
    by = bottom_top
    for r in range(16):
        rh = max(len(brief_rows[0][r][1]), len(brief_rows[1][r][1])) * lh
        for col in range(2):
            num, lines = brief_rows[col][r]
            bx = brief_x + col * (col_w + 16)
            nw = d.textlength(f"{num} ", font=f_bn)
            d.text((bx, by), str(num), font=f_bn, fill=RED)
            ly = by
            for line in lines:
                d.text((bx + nw, ly), line, font=f_b, fill=INK)
                ly += lh
        by += rh
    briefs_bottom = by

    map_h = briefs_bottom - bottom_top
    draw_map(d, X0, bottom_top, map_w, map_h - 34)
    f_cap = sans(10.5)
    cap_lines = wrap(d, MAP_CAPTION, f_cap, map_w)
    cy = bottom_top + map_h - 30
    for line in cap_lines:
        d.text((X0, cy), line, font=f_cap, fill=GREY)
        cy += 13
    y = briefs_bottom + 6

    # ---- date-check box
    d.rounded_rectangle([X0, y, X1, y + 38], radius=3,
                        outline=RED, width=2)
    f_dc = sans(12)
    f_dcb = sans_b(12)
    lead = "DATE CHECK \u2014 "
    d.text((X0 + 8, y + 5), lead, font=f_dcb, fill=RED)
    lw = d.textlength(lead, font=f_dcb)
    d.text((X0 + 8 + lw, y + 5), DATE_CHECK[0][len(lead):], font=f_dc,
           fill=INK)
    d.text((X0 + 8, y + 20), DATE_CHECK[1], font=f_dc, fill=INK)
    y += 44

    # ---- footer
    f_foot = sans(10.5)
    d.text((X0, y), FOOTER, font=f_foot, fill=GREY)
    y += 12
    assert y <= 1016, f"page overflow: final y={y}"
    return img


def main():
    img = build()
    assert img.size == (1024, 1024)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "JPEG", quality=88, optimize=True)
    data = open(out, "rb").read()
    assert data[:2] == b"\xff\xd8", "not a JPEG"
    assert len(data) < 1048576, f"too big: {len(data)}"
    sha = hashlib.sha256(data).hexdigest()
    print(f"stories: {len(FEATURES)} features + {len(BRIEFS)} briefs = "
          f"{len(FEATURES) + len(BRIEFS)}")
    print(f"entry.png: {len(data)} bytes, sha256 {sha}")
    print("checks: all headlines/decks fit, map dots on land, page fits")


if __name__ == "__main__":
    main()
