#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: 45 stories on one 1024x1024 page.

Every story on the page happened, or was first reported, on Thursday
19 November 2026. The page is a newspaper front page: a big dated
masthead, three hero stories, ten more features in two rows of five,
a numbers strip, a dotted world map and a numbered list of briefs.

v5: GTA VI leads the hero row. The launch of GTA VI is the day's most
recognisable event worldwide, so it moves from the last feature slot
to the third hero slot; the Anthropic IPO takes its old slot. The
weakest pictures are redrawn too: India-Japan gets a real skyline
scene instead of two flat flags, the Sudan blackout is brightened so
the drone and the city read, the COP31 globe is bigger and bolder,
and the cyclone's RED ALERT chip sits clear of the spiral.

Run: python3 build_image.py  ->  writes entry.png next to this file.
The output is a JPEG (kept under 1 MiB) in a file named entry.png.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (164, 22, 33)
NAVY = (31, 58, 95)
GREY = (90, 88, 80)
LIGHT_LINE = (120, 115, 100)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    """Load a Noto face, falling back to DejaVu if it is missing."""
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("NotoSerifDisplay-Bold.ttf", s)
SERIF_XB = lambda s: font("NotoSerifDisplay-ExtraBold.ttf", s)
SERIF_I = lambda s: font("NotoSerifDisplay-Italic.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)
SANS_B = lambda s: font("NotoSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, text, fg, bg, size=13, pad_x=6, pad_y=3):
    """A small filled label; returns its width."""
    fnt = SANS_B(size)
    tw = draw.textlength(text, font=fnt)
    w = int(tw) + 2 * pad_x
    h = size + 2 * pad_y
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return w


def badge(draw, cx, cy, n, r=13):
    """A red numbered circle with a white number."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                 outline=(255, 255, 255), width=2)
    fnt = SANS_B(15 if r >= 13 else 13)
    t = str(n)
    tw = draw.textlength(t, font=fnt)
    th = fnt.getbbox(t)[3]
    draw.text((cx - tw / 2, cy - th / 2 - 1), t, font=fnt, fill=(255, 255, 255))


def skyline(draw, x, y, w, h, towers, color, lit=(255, 214, 130)):
    """A row of dark towers with a few lit windows."""
    n = len(towers)
    slot = w / n
    for i, (frac, tw_frac) in enumerate(towers):
        tw = slot * tw_frac
        th = h * frac
        tx = x + i * slot + (slot - tw) / 2
        ty = y + h - th
        draw.rectangle([tx, ty, tx + tw, y + h], fill=color)
        for wy in range(int(ty) + 5, int(y + h) - 4, 9):
            for wx in range(int(tx) + 4, int(tx + tw) - 4, 8):
                if (wx * 7 + wy * 13) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=lit)


def flag(draw, x, y, w, h, stripes):
    """A small horizontal flag from a list of stripe colours."""
    n = len(stripes)
    for i, c in enumerate(stripes):
        draw.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n],
                       fill=c)


def masthead(draw):
    """Top kicker, date masthead, rule and the date-discipline line."""
    draw.text((24, 12), "THE DAY IN WORLD NEWS", font=SANS_B(17), fill=INK)
    right = "45 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    rw = draw.textlength(right, font=SANS_B(17))
    draw.text((1000 - rw, 12), right, font=SANS_B(17), fill=RED)
    draw.text((24, 34), "Thursday 19 November 2026",
              font=SERIF_XB(62), fill=INK)
    draw.line([24, 97, 1000, 97], fill=INK, width=2)
    sub = ("Every story on this page happened, or was first reported, "
           "on Thursday 19 November 2026.")
    sw = draw.textlength(sub, font=SERIF_I(19))
    draw.text(((1024 - sw) / 2, 106), sub, font=SERIF_I(19), fill=INK)

# ---------------------------------------------------------------- pictures
# Each art_* function draws one feature picture inside the box
# (x, y, w, h). All art is original vector drawing: no photos, no
# copied art. Labels are drawn by the feature renderer, not here.

def art_shenzhen(d, x, y, w, h):
    """Shenzhen towers under a pale sky, three flags at the base."""
    d.rectangle([x, y, x + w, y + h], fill=(184, 201, 217))
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(245, 196, 90))
    towers = [(0.55, 0.8), (0.85, 0.9), (0.7, 0.75), (1.0, 0.9),
              (0.62, 0.8), (0.78, 0.85), (0.5, 0.7)]
    skyline(d, x, y + 8, w, h - 8, towers, (70, 88, 110))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(52, 66, 84))
    d.rectangle([x, y + h - 22, x + w, y + h - 19], fill=(150, 40, 48))
    for i, stripes in enumerate([
            [(200, 30, 40)],                                    # China
            [(178, 34, 52), (255, 255, 255), (60, 59, 110)],   # US
            [(255, 255, 255), (0, 57, 166), (216, 0, 0)]]):     # Russia
        fx = x + 14 + i * 34
        d.line([fx + 14, y + h - 44, fx + 14, y + h - 22],
               fill=(40, 40, 40), width=2)
        flag(d, fx, y + h - 44, 28, 16, stripes)


def art_fed(d, x, y, w, h):
    """Rising rate bars, a red arrow climbing, a gold dollar coin."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    bars = [0.25, 0.35, 0.3, 0.5, 0.62, 0.58, 0.8]
    bw = w / (len(bars) + 1)
    for i, f in enumerate(bars):
        bx = x + bw * (i + 0.5)
        d.rectangle([bx, y + h - 14 - h * f * 0.8, bx + bw * 0.62,
                     y + h - 14], fill=(52, 72, 110))
    d.line([x + 8, y + h - 34, x + w * 0.55, y + 26,
            x + w - 14, y + 10], fill=(178, 30, 40), width=3)
    d.polygon([(x + w - 14, y + 4), (x + w - 14, y + 18),
               (x + w - 2, y + 10)], fill=(178, 30, 40))
    cx, cy, r = x + w - 40, y + h - 34, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(222, 178, 60),
              outline=(150, 110, 20), width=2)
    d.text((cx - 6, cy - 11), "$", font=SANS_B(20), fill=(120, 84, 10))


def art_gta(d, x, y, w, h):
    """Leonida at night: neon skyline, a giant pink VI, a glow band."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 16, 48))
    for sx, sy in [(18, 12), (60, 26), (120, 10), (180, 30), (240, 14),
                   (280, 34), (90, 44), (210, 48), (150, 20)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(255, 255, 255))
    d.ellipse([x + w - 70, y + 6, x + w - 34, y + 42],
              fill=(255, 190, 120))
    towers = [(0.5, 0.85), (0.75, 0.9), (0.6, 0.8), (0.95, 0.9),
              (0.55, 0.85), (0.7, 0.8), (0.45, 0.75)]
    skyline(d, x, y + 18, w, h - 18, towers, (12, 8, 30),
            lit=(255, 120, 200))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(255, 45, 149))
    vi = "VI"
    fnt = SERIF_XB(int(h * 0.62))
    tw = d.textlength(vi, font=fnt)
    d.text((x + w - tw - 12, y + h * 0.06), vi, font=fnt,
           fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(255, 45, 149))


def art_gaza(d, x, y, w, h):
    """A tank crossing pale desert ground under a hot sky."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.ellipse([x + w - 46, y + 8, x + w - 18, y + 36], fill=(245, 200, 100))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(198, 168, 110))
    tx, ty = x + w * 0.28, y + h * 0.42
    d.rectangle([tx, ty, tx + w * 0.42, ty + h * 0.22], fill=(74, 84, 52))
    d.rectangle([tx + w * 0.1, ty - h * 0.16, tx + w * 0.3, ty],
                fill=(74, 84, 52))
    d.line([tx + w * 0.3, ty - h * 0.08, tx + w * 0.52, ty - h * 0.08],
           fill=(60, 68, 42), width=5)
    for i in range(5):
        wx = tx + 6 + i * (w * 0.42 - 12) / 4
        d.ellipse([wx, ty + h * 0.22, wx + 10, ty + h * 0.22 + 10],
                  fill=(52, 58, 38))


def art_cyclone(d, x, y, w, h):
    """A white cyclone spiral over a blue sea, tan coast at right."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 214))
    d.polygon([(x + w * 0.78, y), (x + w, y), (x + w, y + h),
               (x + w * 0.86, y + h)], fill=(226, 208, 170))
    cx, cy = x + w * 0.42, y + h * 0.55
    for r, a0, a1 in [(34, 20, 300), (26, 200, 120), (18, 20, 300),
                      (11, 200, 120), (5, 0, 360)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
              fill=(255, 255, 255), width=4)
    for rx in range(0, w, 26):
        d.line([x + rx, y + 8, x + rx - 8, y + 26], fill=(140, 170, 195),
               width=2)


def art_odesa(d, x, y, w, h):
    """Odesa rooftops at dusk with a burst of light over the harbour."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 190, 140))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 90, 70))
    towers = [(0.5, 0.9), (0.7, 0.8), (0.45, 0.9), (0.65, 0.8),
              (0.55, 0.9)]
    skyline(d, x, y + h * 0.2, w, h * 0.45, towers, (96, 70, 52),
            lit=(255, 190, 90))
    cx, cy = x + w * 0.72, y + h * 0.42
    for r, c in [(26, (255, 220, 120)), (18, (255, 170, 60)),
                 (10, (255, 120, 40))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for dx, dy in [(-30, -18), (24, -26), (34, 6), (-24, 14)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 190, 80), width=3)


def art_sudan(d, x, y, w, h):
    """A darkened city at night: lit windows, a drone with red lights."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 78))
    for sx, sy in [(14, 10), (52, 22), (96, 8), (140, 26), (168, 12)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(200, 210, 235))
    towers = [(0.5, 0.85), (0.8, 0.9), (0.6, 0.8), (0.95, 0.85),
              (0.45, 0.8)]
    skyline(d, x, y + 12, w, h - 12, towers, (16, 20, 38),
            lit=(255, 205, 90))
    dx, dy = x + w * 0.62, y + h * 0.3
    d.ellipse([dx - 12, dy - 5, dx + 12, dy + 5], fill=(10, 12, 22))
    d.line([dx - 20, dy - 8, dx + 20, dy + 8], fill=(120, 125, 140),
           width=2)
    d.line([dx - 20, dy + 8, dx + 20, dy - 8], fill=(120, 125, 140),
           width=2)
    for px, py in [(dx - 20, dy - 8), (dx + 20, dy + 8), (dx - 20, dy + 8),
                   (dx + 20, dy - 8)]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 60, 60))


def art_voyager(d, x, y, w, h):
    """Voyager 1 in deep space: stars, a gold dish, a pale planet."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 24))
    for sx, sy, s in [(12, 10, 2), (48, 26, 3), (90, 8, 2), (130, 30, 2),
                      (160, 12, 3), (30, 44, 2), (110, 48, 2), (170, 44, 2)]:
        d.ellipse([x + sx, y + sy, x + sx + s, y + sy + s],
                  fill=(255, 255, 255))
    cx, cy = x + w * 0.62, y + h * 0.5
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(200, 200, 210),
              outline=(120, 120, 135), width=2)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(230, 190, 90))
    d.line([cx - 22, cy + 18, cx - 34, cy + 30], fill=(180, 180, 195),
           width=3)
    d.line([cx + 30, cy - 8, cx + 44, cy - 16], fill=(180, 180, 195),
           width=2)
    px, py, pr = x + w * 0.16, y + h * 0.68, 12
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(140, 160, 190))
    d.ellipse([px - pr - 8, py - 2, px + pr + 8, py + 2],
              outline=(200, 210, 225), width=2)

def art_cop(d, x, y, w, h):
    """A big blue-green Earth with white cloud wisps, on pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 232))
    cx, cy, r = x + w * 0.5, y + h * 0.52, min(w, h) * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 170))
    for gx, gy, gr in [(cx - r * 0.45, cy - r * 0.3, r * 0.34),
                       (cx + r * 0.35, cy + r * 0.25, r * 0.4),
                       (cx + r * 0.1, cy - r * 0.55, r * 0.22)]:
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(74, 160, 90))
    for wx, wy, wl in [(cx - r * 0.7, cy - r * 0.6, r * 0.5),
                       (cx - r * 0.2, cy + r * 0.55, r * 0.6),
                       (cx + r * 0.3, cy - r * 0.1, r * 0.45)]:
        d.ellipse([wx, wy, wx + wl, wy + wl * 0.32], fill=(255, 255, 255))
    d.arc([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], 200, 330,
          fill=(120, 150, 180), width=2)


def art_walmart(d, x, y, w, h):
    """A blue shopping cart rolling across a pale shop floor."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 242))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(190, 200, 212))
    cx, cy = x + w * 0.3, y + h * 0.42
    d.line([cx - 8, cy + 6, cx - 26, cy - 12], fill=(30, 70, 150), width=4)
    d.polygon([(cx - 6, cy), (cx + w * 0.52, cy), (cx + w * 0.46, cy + 26),
               (cx + 2, cy + 26)], fill=(40, 90, 180))
    for i in range(4):
        lx = cx + 4 + i * (w * 0.44) / 4
        d.line([lx, cy + 2, lx - 2, cy + 24], fill=(140, 175, 225), width=2)
    for wx in (cx + 8, cx + w * 0.42):
        d.ellipse([wx - 6, cy + 30, wx + 6, cy + 42], fill=(30, 30, 30),
                  outline=(200, 200, 200), width=2)


def art_tokyo(d, x, y, w, h):
    """Tokyo at dawn: a red sun, a tower silhouette, two flags on poles."""
    d.rectangle([x, y, x + w, y + h], fill=(246, 214, 170))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(214, 150, 110))
    sx, sy, sr = x + w * 0.68, y + h * 0.34, 17
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(214, 48, 48))
    tx = x + w * 0.18
    d.polygon([(tx, y + h * 0.62), (tx + 12, y + h * 0.16),
               (tx + 24, y + h * 0.62)], fill=(52, 52, 66))
    d.line([tx + 12, y + h * 0.16, tx + 12, y + h * 0.08],
           fill=(52, 52, 66), width=2)
    d.rectangle([tx - 16, y + h * 0.62, tx + 40, y + h * 0.66],
                fill=(52, 52, 66))
    for i, stripes in enumerate([
            [(255, 153, 51), (255, 255, 255), (19, 136, 8)],  # India
            [(255, 255, 255)]]):                               # Japan
        fx = x + w * 0.52 + i * (w * 0.22)
        d.line([fx, y + h * 0.34, fx, y + h * 0.62], fill=(60, 60, 60),
               width=2)
        flag(d, fx, y + h * 0.34, w * 0.17, 14, stripes)
        if i == 1:
            d.ellipse([fx + w * 0.085 - 4, y + h * 0.34 + 3,
                       fx + w * 0.085 + 4, y + h * 0.34 + 11],
                      fill=(188, 0, 45))
        else:
            d.ellipse([fx + w * 0.085 - 3, y + h * 0.34 + 4,
                       fx + w * 0.085 + 3, y + h * 0.34 + 10],
                      fill=(0, 0, 128))


def art_nvidia(d, x, y, w, h):
    """A green chip with gold pins and a rising green arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 222))
    cx, cy, s = x + w * 0.38, y + h * 0.52, 26
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(24, 130, 60))
    d.rectangle([cx - s + 8, cy - s + 8, cx + s - 8, cy + s - 8],
                fill=(16, 100, 44))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(240, 240, 240))
    for i in range(4):
        px = cx - s + 6 + i * (2 * s - 12) / 3
        d.line([px, cy - s, px, cy - s - 8], fill=(190, 150, 60), width=3)
        d.line([px, cy + s, px, cy + s + 8], fill=(190, 150, 60), width=3)
    d.line([x + w * 0.62, y + h - 18, x + w * 0.8, y + h * 0.42,
            x + w - 8, y + h * 0.3], fill=(24, 130, 60), width=4)
    d.polygon([(x + w - 10, y + h * 0.2), (x + w - 10, y + h * 0.38),
               (x + w + 2, y + h * 0.3)], fill=(24, 130, 60))


def art_anthropic(d, x, y, w, h):
    """A small IPO chart: dark board, a green line climbing to $83."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 42, 66))
    for gy in range(1, 4):
        yy = y + gy * h / 4
        d.line([x + 6, yy, x + w - 6, yy], fill=(58, 76, 106), width=1)
    pts = [(0.06, 0.78), (0.24, 0.66), (0.4, 0.7), (0.58, 0.48),
           (0.74, 0.52), (0.9, 0.22)]
    xy = [(x + fx * w, y + fy * h) for fx, fy in pts]
    d.line(xy, fill=(90, 200, 120), width=3, joint="curve")
    d.ellipse([xy[-1][0] - 5, xy[-1][1] - 5, xy[-1][0] + 5, xy[-1][1] + 5],
              fill=(90, 200, 120))
    d.rectangle([x + 8, y + 8, x + 62, y + 28], fill=(240, 240, 235))
    d.text((x + 14, y + 10), "$83", font=SANS_B(15), fill=(28, 42, 66))


# ------------------------------------------------------------------ stories
# (number, art, art label, kicker, headline, deck)
FEATURES = [
    (1, art_shenzhen, "SHENZHEN", "ASIA \u00b7 APEC SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen today",
     "Nuclear arms and the Iran war on the table at the first trilateral."),
    (2, art_fed, "MORE HIKES", "AMERICAS \u00b7 FED MINUTES",
     "Fed minutes: more hikes are coming",
     "Waller backs a 50bp December move; gold falls to $3,725."),
    (3, art_gta, "LEONIDA", "GLOBAL \u00b7 GAMES",
     "GTA VI launches today",
     "Midnight launch in New Zealand; 9.7m pre-orders."),
    (4, art_gaza, "CENTRAL GAZA", "MIDDLE EAST \u00b7 GAZA",
     "Israeli tanks push deeper into Gaza",
     "Hamas calls it a truce breach; one killed."),
    (5, art_cyclone, None, "ASIA \u00b7 CYCLONE",
     "Akvan nears coast; 204,000 to move",
     "Landfall Fri noon Narsapur; gusts 110 km/h."),
    (6, art_odesa, "ODESA", "EUROPE \u00b7 UKRAINE WAR",
     "Russian strikes kill four in Odesa",
     "Five dead nationwide; no Donbas-for-NATO swap."),
    (7, art_sudan, "BLACKOUT", "AFRICA \u00b7 SUDAN WAR",
     "Drones black out Sudan's cities",
     "Power stations hit; UN warns aid work disrupted."),
    (8, art_voyager, "VOYAGER 1", "SPACE \u00b7 SCIENCE",
     "Voyager 1 reaches one light-day",
     "25.9bn km out; signal takes a full day to arrive."),
    (9, art_cop, None, "GLOBAL \u00b7 CLIMATE",
     "COP31: 21 issues left, deal in doubt",
     "New drafts due Thursday; summit closes Friday."),
    (10, art_walmart, "$187.3bn", "AMERICAS \u00b7 RETAIL",
     "Walmart reports before the open",
     "$0.64 a share expected on $187.3bn in sales."),
    (11, art_tokyo, "TOKYO", "ASIA \u00b7 DIPLOMACY",
     "India, Japan hold 2+2 defence talks",
     "Amazon pledges $7bn for India renewables by 2030."),
    (12, art_nvidia, None, "AMERICAS \u00b7 CHIPS",
     "Nvidia's new chief promises pay rises",
     "Rises land in December; H-series chips halted."),
    (13, art_anthropic, None, "GLOBAL \u00b7 TECH IPO",
     "Anthropic IPO at $83 a share",
     "$81.3bn raised; debuts as ANT today."),
]

# (number, text) — briefs 14 to 45, one line each.
BRIEFS = [
    (14, "New York: Oil falls as risk aversion rises; Brent $91.86"),
    (15, "Bitcoin slips 0.5% to $62,800 after Fed minutes"),
    (16, "Dollar index near 103.78, a 19-month high"),
    (17, "US 10-year yield eases to 5.07%"),
    (18, "Washington: Trump unhappy Vance did not back Iran war"),
    (19, "Senators warn AI cyber threats outpacing defences"),
    (20, "Vienna: IAEA: N. Korea enrichment extension complete"),
    (21, "Sofia: LPG tanker sunk off Bulgaria hit by shells"),
    (22, "Benghazi: Cocaine and millions of pills seized in Libya"),
    (23, "Riyadh: Saudi danger passed in three southern cities"),
    (24, "Paris: Minister says M\u00e9lenchon could win presidency"),
    (25, "Mogadishu: Somalia accuses UAE of secret bases"),
    (26, "Islamabad: Pakistan conducts Fateh-3 missile launch"),
    (27, "Ottawa: Carney adjusting China ties, seeks US deal"),
    (28, "Shenzhen: Security tight at Qilin Shanzhuang"),
    (29, "Washington: Liu Yunping leads House Democrats"),
    (30, "New Delhi: India's renewable capacity hits 299.25 GW"),
    (31, "Washington: US proposes tougher green-card rules"),
    (32, "New York: Deutsche Bank handled $58bn in Epstein deals"),
    (33, "FBI says North Korean hackers stole $400m+"),
    (34, "Aden: Houthis edge closer as forces leave Bab al-Mandeb"),
    (35, "Palestinians shelter in caves after demolitions"),
    (36, "London: Four nations urge Israel to let aid into Gaza"),
    (37, "Gaza: Families bury bodies trapped years under rubble"),
    (38, "Stockholm: Activists honour children slain in Gaza"),
    (39, "Addis Ababa: Ethiopia, Eritrea mass troops on border"),
    (40, "Baghdad: Iraq launches two airstrikes on ISIS in Anbar"),
    (41, "Amman: Jordan military crash hurts five in practice"),
    (42, "Jerusalem: Knesset elects Eisenkot ally as speaker"),
    (43, "Taipei: Taiwan 'urgently needs' $14bn in US arms"),
    (44, "Kuwait: Iran drones hit Ali Al Salem US base"),
    (45, "AI-chip export licences take effect for 5 nations"),
]

NUMBERS = [
    ("$3,725", "gold, down 3.2% after Fed"),
    ("$81.3bn", "Anthropic IPO, above range"),
    ("9.69m", "GTA VI pre-orders, $942m"),
    ("204,070", "people to move ahead of Akvan"),
]


def draw_feature(d, f, x, y, w, art_h, hero):
    """One feature: picture, number badge, kicker, headline, deck."""
    n, art, label, kicker, headline, deck = f
    art(d, x, y, w, art_h)
    d.rectangle([x, y, x + w, y + art_h], outline=(90, 85, 70), width=1)
    if label:
        chip(d, x + 4, y + 4, label, INK, (250, 247, 238), size=12)
    if n == 5:
        chip(d, x + 4, y + 4, "RED ALERT", (255, 255, 255), RED, size=12)
    if n == 9:
        chip(d, x + 4, y + 4, "21 LEFT", (255, 255, 255), RED, size=12)
    if n == 12:
        chip(d, x + w - 74, y + 4, "PAY RISES", (255, 255, 255),
             (24, 130, 60), size=12)
    badge(d, x + 15, y + art_h - 2, n, r=13 if hero else 11)
    ky = y + art_h + 14
    ksize = 14 if hero else 12
    d.text((x, ky), kicker, font=SANS_B(ksize), fill=RED)
    hy = ky + (20 if hero else 17)
    hfnt = SERIF_B(25 if hero else 19)
    hl = wrap(d, headline, hfnt, w)
    lh = 27 if hero else 22
    for i, line in enumerate(hl):
        d.text((x, hy + i * lh), line, font=hfnt, fill=INK)
    dy = hy + len(hl) * lh + 2
    dfnt = SANS(15 if hero else 13)
    dlh = 17 if hero else 15
    dl = wrap(d, deck, dfnt, w)
    for i, line in enumerate(dl):
        d.text((x, dy + i * dlh), line, font=dfnt, fill=INK)
    return len(hl), len(dl)

# ------------------------------------------------------------------- sections

def numbers_strip(d):
    """Four big figures across the page, under a rule."""
    d.line([24, 700, 1000, 700], fill=INK, width=2)
    d.text((24, 708), "BY THE NUMBERS", font=SANS_B(13), fill=INK)
    xs = [170, 390, 590, 810]
    for (value, label), gx in zip(NUMBERS, xs):
        d.text((gx, 708), value, font=SERIF_B(30), fill=NAVY)
        d.text((gx, 742), label, font=SANS(12), fill=INK)
    d.line([24, 762, 1000, 762], fill=INK, width=1)


# A coarse world map, one character per dot cell ('#' = land).
# 58 columns of longitude, 30 rows of latitude, drawn as dots.
# A coarse world map: land runs per row, (first, last) column inclusive.
# 58 columns of longitude, 30 rows of latitude; drawn as dots.
MAP_LAND = [
    [(2, 6), (8, 14), (16, 18), (27, 27), (30, 55)],
    [(2, 7), (8, 15), (16, 17), (29, 56)],
    [(3, 7), (8, 16), (23, 23), (26, 28), (30, 56)],
    [(4, 8), (9, 17), (26, 29), (30, 56)],
    [(5, 8), (9, 18), (24, 25), (27, 29), (31, 56)],
    [(5, 9), (10, 19), (24, 24), (26, 33), (34, 56)],
    [(5, 10), (11, 20), (25, 34), (35, 50), (51, 55)],
    [(5, 11), (12, 21), (26, 33), (36, 48), (50, 54), (55, 55)],
    [(6, 12), (13, 22), (26, 34), (35, 46), (47, 53), (54, 55)],
    [(6, 13), (14, 22), (25, 32), (34, 43), (47, 53), (54, 55)],
    [(6, 14), (15, 23), (25, 33), (35, 38), (40, 44), (47, 52), (53, 53)],
    [(6, 15), (16, 23), (25, 34), (35, 38), (40, 44), (47, 51), (53, 54)],
    [(6, 16), (17, 22), (25, 35), (40, 43), (44, 46), (47, 50)],
    [(6, 17), (18, 21), (26, 30), (33, 36), (40, 43), (47, 50)],
    [(7, 18), (19, 21), (26, 35), (42, 42), (47, 50)],
    [(7, 21), (22, 25), (27, 35), (48, 50)],
    [(7, 21), (22, 27), (28, 35), (48, 53)],
    [(7, 21), (22, 28), (29, 35), (48, 54)],
    [(7, 21), (22, 28), (30, 34), (49, 54), (55, 57)],
    [(8, 22), (23, 28), (30, 34), (50, 54), (55, 57)],
    [(8, 22), (23, 28), (30, 33), (36, 36), (50, 55)],
    [(8, 22), (23, 27), (30, 33), (36, 36), (49, 55)],
    [(8, 22), (23, 27), (30, 33), (49, 55)],
    [(9, 23), (24, 27), (30, 33), (49, 55)],
    [(9, 23), (24, 26), (30, 32), (50, 54), (55, 56)],
    [(9, 23), (24, 26), (30, 32), (55, 56)],
    [(9, 23), (24, 26), (56, 56)],
    [(9, 23), (24, 25)],
    [(9, 23), (24, 25)],
    [(9, 23), (24, 24)],
]
MAP_ROWS = ["".join("#" if any(a <= c <= b for a, b in runs) else "."
                    for c in range(58)) for runs in MAP_LAND]

# Numbered map dots, in page pixels: (story, x, y).
# 8 Voyager 1 is in space and 3/13 are off-map places: the caption
# under the map says so instead of plotting them on the wrong land.
MAP_DOTS = [
    (1, 253, 859), (2, 98, 842), (3, 302, 927), (4, 193, 850),
    (5, 227, 866), (6, 188, 828), (7, 184, 874), (9, 138, 854),
    (10, 82, 854), (11, 273, 844), (12, 58, 846), (13, 114, 826),
]


def world_map(d):
    """Dotted world map with numbered red dots, plus its caption."""
    d.text((24, 772), "WHERE IT HAPPENED", font=SANS_B(14), fill=INK)
    d.text((330, 772), "ALSO ON THURSDAY 19 NOVEMBER",
           font=SANS_B(14), fill=INK)
    d.line([24, 790, 1000, 790], fill=RED, width=2)
    x0, y0, step = 26, 798, 5
    for r, row in enumerate(MAP_ROWS[:28]):
        for c, ch in enumerate(row):
            if ch == "#":
                px, py = x0 + c * step, y0 + r * step
                d.ellipse([px, py, px + 2, py + 2], fill=(110, 128, 110))
    for n, dx, dy in MAP_DOTS:
        badge(d, dx, dy, n, r=10)
    caption = ("Numbered dots mark stories 1\u201313. 8 Voyager 1: in space, "
               "25.9bn km out. 13 Anthropic: Nasdaq, New York. "
               "3 GTA VI: first launch in New Zealand.")
    cl = wrap(d, caption, SANS(11), 292)
    for i, line in enumerate(cl):
        d.text((24, 942 + i * 13), line, font=SANS(11), fill=INK)


def briefs(d):
    """The numbered briefs, 14-29 left, 30-45 right, one line each."""
    fnt = SANS(12)
    nfnt = SANS_B(12)
    left = BRIEFS[:16]
    right = BRIEFS[16:]
    for col, items in ((330, left), (655, right)):
        for i, (n, text) in enumerate(items):
            by = 796 + i * 11
            num = str(n) + " "
            nw = d.textlength(num, font=nfnt)
            d.text((col, by), num, font=nfnt, fill=RED)
            d.text((col + nw, by), text, font=fnt, fill=INK)
    return left, right


def footer(d):
    """Date-check line and sources, under the bottom rule."""
    d.line([24, 986, 1000, 986], fill=INK, width=1)
    d.text((24, 994),
           "DATE CHECK \u2014 left out, reported 17\u201318 Nov: Xi's airport "
           "welcome, UK inflation 3.6%, EU \u20ac45bn loan, Amnesty Sudan "
           "toll, Jeffries vote, Peltola win.",
           font=SANS(12), fill=INK)
    d.text((24, 1008),
           "Sources: Reuters, AP, BBC, Bloomberg, Fed, IMD, NASA, UN, "
           "IAEA, Rockstar Games, Take-Two. Original drawings. Kuwait "
           "strike first reported overnight into 19 Nov.",
           font=SANS(12), fill=INK)


def build():
    """Draw the whole page and save it; return (path, size, problems)."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    problems = []

    hero_xs = [24, 348, 672]
    for f, fx in zip(FEATURES[:3], hero_xs):
        hl, dl = draw_feature(d, f, fx, 128, 304, 86, True)
        if hl > 2 or dl > 2:
            problems.append(f"hero {f[0]}: headline {hl} lines, deck {dl}")

    row2_xs = [24, 222, 420, 618, 816]
    for f, fx in zip(FEATURES[3:8], row2_xs):
        hl, dl = draw_feature(d, f, fx, 344, 184, 64, False)
        if hl > 2 or dl > 2:
            problems.append(f"feature {f[0]}: headline {hl} lines, deck {dl}")

    row3_xs = [24, 222, 420, 618, 816]
    for f, fx in zip(FEATURES[8:], row3_xs):
        hl, dl = draw_feature(d, f, fx, 524, 184, 64, False)
        if hl > 2 or dl > 2:
            problems.append(f"feature {f[0]}: headline {hl} lines, deck {dl}")

    numbers_strip(d)
    world_map(d)
    briefs(d)
    footer(d)

    stories = len(FEATURES) + len(BRIEFS)
    if stories != 45:
        problems.append(f"story count {stories} != 45")
    img.save(OUT, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(OUT)
    if size >= 1048576:
        problems.append(f"entry.png {size} bytes >= 1 MiB")
    return OUT, size, problems


if __name__ == "__main__":
    path, size, problems = build()
    print(f"wrote {path}: {size} bytes, "
          f"{len(FEATURES)} features + {len(BRIEFS)} briefs = "
          f"{len(FEATURES) + len(BRIEFS)} stories")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("checks OK")
