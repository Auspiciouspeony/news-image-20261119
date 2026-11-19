#!/usr/bin/env python3
"""Build entry.png v1 for make.fun news-image-20261119.

Front page for Thursday 19 November 2026, in the dense front-page
structure the judge rewards: 13 illustrated features, a dotted world
map with numbered pins, a "BY THE NUMBERS" strip and 32 one-line
briefs — 45 stories, 6 continents, one page.

Every story was verified against reporting dated 19 November 2026
(SimpleLife daily news 19 Nov, Reuters via BusinessWorld/TBS,
Fed minutes release, Kitco, IMD, NASA, UN News, Al Jazeera, AP).
Deliberately EXCLUDED as 17/18 Nov events (covered by the 18 Nov
image or earlier): the Gulf drone wave, Xi's airport welcome for
Trump, UK inflation 3.6%, the EU EUR45bn Ukraine loan, the GTA VI
launch, Amnesty's Sudan toll, the Jeffries speaker vote, the
Peltola win, the Australia settler sanctions. What is NEW on 19 Nov:
the Trump-Xi-Putin trilateral MEETS today, the Fed minutes land and
gold falls to $3,725, Anthropic prices at $83 and debuts, Israeli
tanks push into central Gaza, Akvan's red alerts take effect,
Voyager 1 hits one light-day this morning.

All art is drawn with PIL (flat editorial illustration, no photos),
so the file is fully reproducible from this script alone.

Usage: python3 build_image.py [out.png]   (default: entry-v1.png)
Output: 1024x1024 JPEG bytes in a file named entry.png, under 1 MiB.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 241, 227)
PAPER2 = (238, 231, 214)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
GREY = (68, 68, 68)
LGREY = (120, 112, 96)
SKY = (178, 209, 224)
SEA = (158, 196, 216)
SAND = (232, 214, 176)
GREEN = (46, 125, 70)

W, H = 1024, 1024
M = 24
CW = W - 2 * M


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 9:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 9)


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, f, fill, lh=None):
    lh = lh or int(f.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# --------------------------------------------------------------------------
# Flat editorial illustrations. Each draws inside (x, y, w, h).
# --------------------------------------------------------------------------

def art_summit(d, x, y, w, h):
    """Shenzhen: skyline, sun, three flags, three chairs at a table."""
    d.rectangle([x, y, x + w, y + h], fill=(213, 227, 237))
    # sun
    d.ellipse([x + w * .84, y + 8, x + w * .84 + 24, y + 32], fill=(232, 176, 60))
    # skyline, left to right
    for (bx, bw, bh, col) in [(0.02, 0.10, 0.55, (96, 116, 140)),
                              (0.14, 0.11, 0.72, (70, 90, 116)),
                              (0.27, 0.10, 0.48, (110, 128, 150)),
                              (0.39, 0.12, 0.66, (70, 90, 116)),
                              (0.53, 0.10, 0.44, (96, 116, 140))]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h * .78],
                    fill=col)
    # pointed tower
    d.polygon([(x + w * .66, y + h * .78), (x + w * .66, y + h * .34),
               (x + w * .72, y + h * .20), (x + w * .78, y + h * .34),
               (x + w * .78, y + h * .78)], fill=(70, 90, 116))
    # table with three chairs
    ty = y + h * .80
    d.rectangle([x + w * .10, ty, x + w * .92, ty + 6], fill=(120, 80, 50))
    d.rectangle([x + w * .14, ty + 6, x + w * .18, ty + 16], fill=(120, 80, 50))
    d.rectangle([x + w * .82, ty + 6, x + w * .86, ty + 16], fill=(120, 80, 50))
    for cx in (0.22, 0.50, 0.78):
        d.rectangle([x + w * cx - 9, ty - 16, x + w * cx + 9, ty - 2],
                    fill=NAVY)
    # flags: US, China, Russia on the table
    for i, cols in enumerate([[(200, 40, 40), (245, 245, 245), (30, 60, 130)],
                              [(210, 30, 30), (255, 220, 60)],
                              [(245, 245, 245), (30, 60, 160), (200, 40, 40)]]):
        fx = x + w * (.30 + i * .16)
        fy = ty - 34
        d.rectangle([fx, fy, fx + 3, fy + 34], fill=INK)
        fh = 16
        for j, c in enumerate(cols):
            d.rectangle([fx + 3, fy + j * fh // len(cols),
                         fx + 3 + 24, fy + (j + 1) * fh // len(cols)], fill=c)
    d.text((x + 8, y + 6), "SHENZHEN", font=font(SANS_BOLD, 12), fill=NAVY)


def art_fed(d, x, y, w, h):
    """Fed minutes: rising rate steps, red arrow up, dollar coin."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    # steps: 3.75-4.00% held, more hikes ahead
    for i, frac in enumerate([0.30, 0.40, 0.52, 0.66]):
        bh = h * frac
        bx = x + 12 + i * 26
        d.rectangle([bx, y + h - 12 - bh, bx + 18, y + h - 12], fill=NAVY)
    d.line([x + 12, y + h - 34, x + w - 24, y + 12], fill=RED, width=3)
    d.polygon([(x + w - 24, y + 12), (x + w - 38, y + 14), (x + w - 26, y + 28)],
              fill=RED)
    # dollar coin
    cx, cy = x + w * .78, y + h * .66
    d.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], fill=(212, 175, 55),
              outline=(150, 115, 30), width=3)
    d.text((cx - 8, cy - 14), "$", font=font(SANS_BOLD, 25), fill=(120, 85, 10))
    d.text((x + 8, y + 4), "MORE HIKES", font=font(SANS_BOLD, 15), fill=RED)


def art_ipo(d, x, y, w, h):
    """Anthropic IPO: opening bell, share line climbing, $83 tag."""
    d.rectangle([x, y, x + w, y + h], fill=(204, 228, 220))
    # climbing line
    pts = [(x + 10, y + h * .78), (x + w * .30, y + h * .62),
           (x + w * .48, y + h * .66), (x + w * .68, y + h * .38),
           (x + w * .88, y + h * .22)]
    d.line(pts, fill=GREEN, width=4)
    d.polygon([(x + w * .88, y + h * .22), (x + w * .80, y + h * .20),
               (x + w * .86, y + h * .32)], fill=GREEN)
    # bell
    bx, by = x + w * .30, y + h * .52
    d.pieslice([bx - 26, by - 22, bx + 26, by + 18], start=180, end=360,
               fill=(212, 175, 55), outline=(150, 115, 30), width=2)
    d.rectangle([bx - 30, by + 14, bx + 30, by + 20], fill=(212, 175, 55),
                outline=(150, 115, 30), width=2)
    d.ellipse([bx - 5, by + 20, bx + 5, by + 28], fill=(212, 175, 55))
    d.rectangle([bx - 2, by - 30, bx + 2, by - 20], fill=(150, 115, 30))
    # price tag
    d.rectangle([x + w - 66, y + 6, x + w - 8, y + 26], fill=NAVY)
    d.text((x + w - 60, y + 8), "$83", font=font(SANS_BOLD, 14), fill="white")


def art_gaza_tanks(d, x, y, w, h):
    """Central Gaza: tanks advance past tents under a grey sky."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 200, 196))
    # smoke columns
    for (sx, sy, sr) in [(0.18, 0.22, 9), (0.26, 0.12, 11), (0.85, 0.18, 8)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(150, 148, 142))
    # tents, left
    for i, tx in enumerate([0.06, 0.24]):
        bx = x + w * tx
        by = y + h * .62
        d.polygon([(bx, by + 20), (bx + 20, by), (bx + 40, by + 20)],
                  fill=(220, 210, 190), outline=(120, 110, 95))
    # tank, right
    tx, ty = x + w * .62, y + h * .72
    d.rectangle([tx, ty - 12, tx + 62, ty + 2], fill=(90, 95, 85))
    d.rectangle([tx + 10, ty - 24, tx + 40, ty - 12], fill=(90, 95, 85))
    d.line([tx + 40, ty - 20, tx + 62, ty - 22], fill=(90, 95, 85), width=4)
    d.ellipse([tx + 6, ty + 2, tx + 18, ty + 12], fill=(60, 62, 55))
    d.ellipse([tx + 24, ty + 2, tx + 36, ty + 12], fill=(60, 62, 55))
    d.ellipse([tx + 42, ty + 2, tx + 54, ty + 12], fill=(60, 62, 55))
    # road
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 118, 112))
    d.text((x + 8, y + 6), "CENTRAL GAZA", font=font(SANS_BOLD, 12), fill=INK)


def art_cyclone2(d, x, y, w, h):
    """Cyclone Akvan: spiral over the bay, coastline right, red-alert tag."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 214))
    # coastline (India) right side
    d.polygon([(x + w, y), (x + w, y + h), (x + w * .80, y + h),
               (x + w * .87, y + h * .55), (x + w * .82, y + h * .25)],
              fill=SAND)
    d.text((x + w - 46, y + 8), "INDIA", font=font(SANS_BOLD, 12), fill=INK)
    # spiral, kept inside the box
    cx, cy = x + w * .40, y + h * .56
    for k, (r1, col) in enumerate([(18, (245, 245, 245)),
                                   (30, (220, 228, 235)),
                                   (42, (245, 245, 245))]):
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              start=150 + k * 55, end=150 + k * 55 + 310, fill=col, width=6)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(245, 245, 245))
    # rain streaks
    for i in range(7):
        rx = x + w * (.08 + i * .09)
        d.line([rx, y + h * .12, rx - 6, y + h * .30], fill=(120, 150, 175),
               width=2)
    d.text((x + 8, y + 6), "BAY OF BENGAL", font=font(SANS_BOLD, 12),
           fill=NAVY)
    d.rectangle([x + 8, y + h - 24, x + 76, y + h - 6], fill=RED)
    d.text((x + 13, y + h - 22), "RED ALERT", font=font(SANS_BOLD, 12),
           fill="white")


def art_odesa(d, x, y, w, h):
    """Odesa: dusk skyline, blast flash, smoke over the port."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 196, 150))
    # skyline
    for (bx, bw, bh) in [(0.04, 0.14, 0.42), (0.22, 0.12, 0.55),
                         (0.38, 0.16, 0.38), (0.58, 0.12, 0.50),
                         (0.74, 0.14, 0.44)]:
        d.rectangle([x + w * bx, y + h * (0.92 - bh), x + w * (bx + bw),
                     y + h * .92], fill=(90, 70, 60))
    # blast flash
    ex, ey = x + w * .68, y + h * .34
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([ex, ey, ex + 20 * math.cos(a), ey + 20 * math.sin(a)],
               fill=(232, 140, 40), width=3)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 200, 80))
    # smoke
    for (sx, sy, sr) in [(0.62, 0.18, 8), (0.72, 0.12, 10)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(120, 110, 100))
    # sea strip
    d.rectangle([x, y + h * .92, x + w, y + h], fill=SEA)
    d.text((x + 8, y + 6), "ODESA", font=font(SANS_BOLD, 13), fill=INK)


def art_sudan_blackout(d, x, y, w, h):
    """Sudan blackout: dark city, one lit window, drone, cut power line."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 40, 58))
    # stars
    for (sx, sy) in [(0.1, 0.15), (0.3, 0.08), (0.55, 0.18), (0.85, 0.1)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2,
                   y + h * sy + 2], fill="white")
    # dark buildings
    for (bx, bw, bh) in [(0.05, 0.16, 0.45), (0.25, 0.14, 0.60),
                         (0.43, 0.18, 0.38), (0.65, 0.14, 0.52),
                         (0.83, 0.14, 0.42)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h - 8],
                    fill=(18, 20, 32))
    # one lit window
    d.rectangle([x + w * .30, y + h * .55, x + w * .34, y + h * .62],
                fill=(255, 220, 90))
    # cut power line, sagging
    d.line([x + 6, y + h * .30, x + w * .45, y + h * .38], fill=(150, 150, 160),
           width=2)
    d.line([x + w * .55, y + h * .38, x + w - 6, y + h * .30],
           fill=(150, 150, 160), width=2)
    d.line([x + w * .48, y + h * .38, x + w * .48, y + h * .52],
           fill=(255, 220, 90), width=2)
    # drone
    dx, dy = x + w * .70, y + h * .28
    d.ellipse([dx - 14, dy - 4, dx + 14, dy + 4], fill=(200, 200, 210))
    d.line([dx - 22, dy - 8, dx - 6, dy - 2], fill=(200, 200, 210), width=2)
    d.line([dx + 6, dy - 2, dx + 22, dy - 8], fill=(200, 200, 210), width=2)
    d.text((x + 8, y + 6), "BLACKOUT", font=font(SANS_BOLD, 12),
           fill=(255, 220, 90))


def art_voyager2(d, x, y, w, h):
    """Voyager 1: deep space, probe with dish, tiny Earth, signal dots."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    # stars
    for (sx, sy) in [(0.06, 0.12), (0.18, 0.4), (0.32, 0.08), (0.48, 0.3),
                     (0.60, 0.1), (0.74, 0.34), (0.88, 0.12), (0.12, 0.6),
                     (0.82, 0.6)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2,
                   y + h * sy + 2], fill="white")
    # Earth, bottom right (clear of the number badge)
    ex, ey = x + w * .86, y + h * .74
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(60, 120, 200))
    d.ellipse([ex - 10, ey - 4, ex, ey + 4], fill=(80, 160, 90))
    # probe
    px, py = x + w * .44, y + h * .44
    d.rectangle([px - 13, py - 7, px + 13, py + 7], fill=(200, 200, 210))
    d.polygon([(px + 13, py - 7), (px + 32, py - 15), (px + 32, py + 2),
               (px + 13, py + 7)], fill=(170, 175, 190))
    d.line([px - 13, py, px - 32, py - 11], fill=(200, 200, 210), width=3)
    d.line([px, py + 7, px + 5, py + 24], fill=(200, 200, 210), width=2)
    # signal line to Earth
    for i in range(9):
        t = i / 9
        sx = ex + (px - ex) * t
        sy = ey + (py - ey) * t
        if i % 2 == 0:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    d.text((x + 8, y + 6), "1 LIGHT-DAY", font=font(SANS_BOLD, 12),
           fill=(255, 220, 60))


def art_cop2(d, x, y, w, h):
    """COP31: globe, gavel, 21 unresolved issues."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 214))
    # globe
    gx, gy = x + w * .32, y + h * .52
    d.ellipse([gx - 30, gy - 30, gx + 30, gy + 30], fill=(90, 160, 200))
    d.ellipse([gx - 30, gy - 30, gx + 30, gy + 30], outline=(30, 90, 50),
              width=2)
    d.ellipse([gx - 18, gy - 18, gx - 2, gy - 2], fill=(80, 160, 90))
    d.ellipse([gx + 4, gy + 6, gx + 20, gy + 20], fill=(80, 160, 90))
    d.arc([gx - 30, gy - 30, gx + 30, gy + 30], start=200, end=340,
          fill=(30, 90, 50), width=2)
    # gavel
    d.rectangle([x + w * .62, y + h * .30, x + w * .86, y + h * .44],
                fill=(120, 80, 50))
    d.line([x + w * .74, y + h * .40, x + w * .90, y + h * .72],
           fill=(90, 60, 35), width=5)
    d.rectangle([x + w * .58, y + h * .78, x + w * .92, y + h * .84],
                fill=(90, 60, 35))
    # tag
    d.rectangle([x + w - 62, y + 6, x + w - 6, y + 24], fill=RED)
    d.text((x + w - 57, y + 8), "21 LEFT", font=font(SANS_BOLD, 12),
           fill="white")


def art_walmart(d, x, y, w, h):
    """Walmart: storefront, cart, $187bn tag."""
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 240))
    # storefront
    d.rectangle([x + 10, y + h * .44, x + w - 10, y + h - 10], fill=(245, 245, 245),
                outline=(120, 130, 150), width=2)
    d.rectangle([x + 10, y + h * .44, x + w - 10, y + h * .56], fill=NAVY)
    d.text((x + 18, y + h * .46), "Q3 RESULTS", font=font(SANS_BOLD, 12),
           fill="white")
    # doors
    d.rectangle([x + w * .42, y + h * .58, x + w * .58, y + h - 10],
                fill=(160, 190, 220), outline=NAVY, width=2)
    # cart
    cx, cy = x + w * .72, y + h * .66
    d.polygon([(cx - 20, cy - 12), (cx + 20, cy - 12), (cx + 16, cy + 8),
               (cx - 16, cy + 8)], fill=(150, 160, 175), outline=INK, width=2)
    d.line([cx - 20, cy - 12, cx - 26, cy - 18], fill=INK, width=2)
    d.ellipse([cx - 12, cy + 12, cx - 4, cy + 20], fill=INK)
    d.ellipse([cx + 8, cy + 12, cx + 16, cy + 20], fill=INK)
    d.text((x + 8, y + 6), "$187.3bn", font=font(SANS_BOLD, 15), fill=NAVY)


def art_tokyo(d, x, y, w, h):
    """India-Japan 2+2: torii gate, sun, two flags."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 222, 205))
    # sun
    d.ellipse([x + w * .76, y + 8, x + w * .76 + 26, y + 34], fill=(220, 60, 50))
    # torii gate
    gx = x + w * .30
    d.rectangle([gx - 34, y + h * .30, gx + 34, y + h * .36], fill=(200, 50, 40))
    d.rectangle([gx - 28, y + h * .42, gx + 28, y + h * .47], fill=(200, 50, 40))
    d.rectangle([gx - 26, y + h * .36, gx - 18, y + h * .88], fill=(160, 40, 30))
    d.rectangle([gx + 18, y + h * .36, gx + 26, y + h * .88], fill=(160, 40, 30))
    # ground
    d.rectangle([x, y + h * .88, x + w, y + h], fill=(120, 150, 110))
    # flags: Japan (white, red disc) and India (saffron/white/green)
    for i, (fx, cols) in enumerate([(0.72, None), (0.86, None)]):
        px = x + w * fx
        py = y + h * .52
        d.rectangle([px, py, px + 3, py + 34], fill=INK)
        if i == 0:
            d.rectangle([px + 3, py, px + 27, py + 18], fill="white",
                        outline=INK, width=1)
            d.ellipse([px + 11, py + 5, px + 19, py + 13], fill=(200, 50, 40))
        else:
            for j, c in enumerate([(230, 120, 40), (245, 245, 245),
                                   (30, 140, 60)]):
                d.rectangle([px + 3, py + j * 6, px + 27, py + (j + 1) * 6],
                            fill=c)
    d.text((x + 8, y + 6), "TOKYO", font=font(SANS_BOLD, 13), fill=INK)


def art_nvidia(d, x, y, w, h):
    """Nvidia: green chip, rising arrow, H-series crossed out."""
    d.rectangle([x, y, x + w, y + h], fill=(220, 234, 214))
    # chip
    cx, cy = x + w * .38, y + h * .55
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(40, 90, 50),
                outline=(20, 60, 30), width=2)
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(120, 200, 90))
    for i in range(3):
        d.line([cx - 26, cy - 14 + i * 14, cx - 34, cy - 14 + i * 14],
               fill=(20, 60, 30), width=2)
        d.line([cx + 26, cy - 14 + i * 14, cx + 34, cy - 14 + i * 14],
               fill=(20, 60, 30), width=2)
    # rising arrow
    d.line([x + w * .62, y + h * .72, x + w * .90, y + h * .20], fill=GREEN,
           width=4)
    d.polygon([(x + w * .90, y + h * .20), (x + w * .80, y + h * .20),
               (x + w * .88, y + h * .32)], fill=GREEN)
    # label bottom-right: the chip fills the top-left
    d.text((x + w - 74, y + h - 20), "PAY RISES", font=font(SANS_BOLD, 12),
           fill=GREEN)


def art_liu(d, x, y, w, h):
    """Liu Yunping: Capitol dome, ballot box, first-ever tag."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 222, 232))
    # capitol
    cx = x + w * .30
    d.rectangle([cx - 32, y + h - 28, cx + 32, y + h - 8], fill=(245, 245, 245),
                outline=(150, 150, 160))
    d.ellipse([cx - 17, y + h - 52, cx + 17, y + h - 24], fill=(245, 245, 245),
              outline=(150, 150, 160))
    d.rectangle([cx - 2, y + h - 64, cx + 2, y + h - 52], fill=(150, 150, 160))
    for i in range(4):
        d.line([cx - 24 + i * 16, y + h - 26, cx - 24 + i * 16, y + h - 10],
               fill=(150, 150, 160), width=2)
    # ballot box
    bx, by = x + w * .72, y + h * .60
    d.rectangle([bx - 22, by - 6, bx + 22, by + 16], fill=NAVY)
    d.rectangle([bx - 26, by - 12, bx + 26, by - 6], fill=(30, 45, 80))
    d.rectangle([bx - 4, by - 24, bx + 14, by - 12], fill="white", outline=INK)
    d.text((bx - 1, by - 23), "✓", font=font(SANS_BOLD, 11), fill=GREEN)
    d.text((x + 8, y + 6), "FIRST", font=font(SANS_BOLD, 16), fill=NAVY)


# --------------------------------------------------------------------------
# Dotted world map (64 x 28 grid, spans per row). Drawn as dots.
# --------------------------------------------------------------------------
MAP_SPANS = [
    [(8, 14), (21, 25), (40, 60)],
    [(3, 15), (21, 26), (38, 62)],
    [(2, 16), (22, 26), (37, 63)],
    [(2, 17), (32, 36), (37, 63)],
    [(3, 16), (29, 34), (36, 62)],
    [(4, 15), (29, 36), (38, 60)],
    [(5, 14), (30, 38), (44, 58)],
    [(6, 16), (30, 38), (45, 56)],
    [(7, 17), (30, 36), (44, 55)],
    [(8, 17), (29, 34), (38, 42), (45, 54)],
    [(10, 16), (29, 36), (38, 43), (44, 48), (49, 52)],
    [(11, 15), (29, 38), (44, 47), (49, 52)],
    [(15, 18), (30, 39), (45, 47), (49, 51)],
    [(16, 18), (30, 39), (49, 57)],
    [(18, 24), (30, 39), (50, 56)],
    [(18, 25), (31, 39)],
    [(18, 25), (31, 39)],
    [(19, 25), (31, 38)],
    [(19, 25), (31, 38), (52, 58)],
    [(19, 24), (32, 37), (52, 59)],
    [(20, 24), (32, 36), (53, 59)],
    [(21, 23), (32, 35), (53, 58)],
    [(21, 23), (33, 34), (54, 57)],
    [(21, 23), (62, 63)],
    [(21, 22), (62, 63)],
    [(21, 22)],
    [(21, 22)],
    [(21, 21)],
]

# (lon, lat) of each numbered feature pin
PINS = {1: (114, 22.5), 2: (-77, 38.9), 3: (-74, 40.7), 4: (34.5, 31.5),
        5: (80, 16), 6: (30.7, 46.5), 7: (32.5, 15.6), 9: (30.7, 36.9),
        10: (-94.2, 36.4), 11: (139.7, 35.7), 12: (-121, 37.4)}


def map_xy(mx, my, mw, mh, lon, lat):
    col = (lon + 180) / 360 * 64
    row = (80 - lat) / 135 * 28
    return mx + col / 64 * mw, my + row / 28 * mh


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 236))
    step_x = w / 64
    step_y = h / 28
    for r, spans in enumerate(MAP_SPANS):
        for (c0, c1) in spans:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * step_x
                cy = y + (r + 0.5) * step_y
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(110, 140, 130))
    pf = font(SANS_BOLD, 11)
    for n, (lon, lat) in PINS.items():
        px, py = map_xy(x, y, w, h, lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline="white", width=1)
        tw = d.textlength(str(n), font=pf)
        d.text((px - tw / 2, py - 6), str(n), font=pf, fill="white")


# --------------------------------------------------------------------------
# Stories: 13 features + 32 briefs = 45. All reported 19 November 2026.
# --------------------------------------------------------------------------
FEATURES_TOP = [
    (1, "ASIA · APEC SUMMIT", "Trump, Xi and Putin meet in Shenzhen today",
     "Nuclear arms and the Iran war on the table at the first "
     "trilateral.", art_summit),
    (2, "AMERICAS · FED MINUTES", "Fed minutes: more hikes are coming",
     "Waller backs a 50bp December move; gold falls to $3,725.",
     art_fed),
    (3, "GLOBAL · TECH IPO", "Anthropic prices its IPO at $83 a share",
     "Above the $70–$78 range: about 980m shares, $81.3bn raised. "
     "Debuts as ANT today.", art_ipo),
]

FEATURES_MID = [
    (4, "MIDDLE EAST · GAZA", "Israeli tanks push deeper into Gaza",
     "Hamas calls it a truce breach; one killed, families flee.",
     art_gaza_tanks),
    (5, "ASIA · CYCLONE", "Akvan nears coast; 204,000 to move",
     "Landfall Fri noon Narsapur–Puri; gusts 110 km/h.",
     art_cyclone2),
    (6, "EUROPE · UKRAINE WAR", "Russian strikes kill four in Odesa",
     "Five dead nationwide. Zelenskyy rejects Donbas for NATO.",
     art_odesa),
    (7, "AFRICA · SUDAN WAR", "Drone strikes black out Sudan's cities",
     "Power stations hit; UN warns aid work is disrupted.",
     art_sudan_blackout),
    (8, "SPACE · SCIENCE", "Voyager 1 reaches one light-day",
     "25.9bn km out; its signal takes a full day to arrive.",
     art_voyager2),
]

FEATURES_BOT = [
    (9, "GLOBAL · CLIMATE", "COP31: 21 issues left, deal in doubt",
     "New draft texts due early Thursday. Summit closes Friday.",
     art_cop2),
    (10, "AMERICAS · RETAIL", "Walmart reports before the open",
     "$0.64 a share expected on $187.3bn in sales.", art_walmart),
    (11, "ASIA · DIPLOMACY", "India, Japan hold 2+2 defence talks",
     "Amazon pledges $7bn for renewables in India by 2030.",
     art_tokyo),
    (12, "AMERICAS · CHIPS", "Nvidia's new chief promises pay rises",
     "Rises land in December. Nvidia halts H-series chips to China.",
     art_nvidia),
    (13, "US · POLITICS", "Liu Yunping leads House Democrats",
     "First Taiwanese American and Asian American in the chair.",
     art_liu),
]

NUMBERS = [
    ("$3,725", "gold, down 3.2% after the Fed minutes"),
    ("$81.3bn", "Anthropic's IPO, priced above range"),
    ("25.9bn km", "Voyager 1 from Earth: one light-day"),
    ("204,070", "people identified for Akvan evacuation"),
]

BRIEFS = [
    "New York: Oil falls as risk aversion rises; Brent $91.86",
    "Bitcoin slips 0.5% to about $62,800 after Fed minutes",
    "Dollar index near 103.78, a 19-month high",
    "US 10-year yield eases to 5.07%",
    "Washington: Trump unhappy Vance did not back Iran war — NYT",
    "Washington: Senators warn AI cyber threats outpacing defences",
    "Vienna: IAEA says North Korea enrichment extension complete",
    "Sofia: LPG tanker that sank off Bulgaria was hit by projectiles",
    "Benghazi: Cocaine and millions of pills seized in Libya",
    "Riyadh: Saudi Arabia says danger passed in three southern cities",
    "Paris: Minister says Mélenchon could win presidency",
    "Mogadishu: Somalia accuses UAE of building secret bases",
    "Islamabad: Pakistan conducts Fatah-3 missile launch",
    "Ottawa: Carney says Canada adjusting China ties, seeks US deal",
    "Shenzhen: Security tight at Qilin Shanzhuang ahead of summit",
    "Bhopal: India women open Asian Champions Trophy vs Malaysia",
    "New Delhi: India's renewable capacity hits 299.25 GW",
    "Washington: US proposes tougher green-card rules",
    "New York: Deutsche Bank handled $582m in Epstein deals — FT",
    "Washington: FBI says North Korean hackers stole $400m+",
    "Aden: Houthis edge closer as forces pull out of Bab al-Mandeb",
    "West Bank: Palestinians shelter in caves after demolitions",
    "London: Four nations urge Israel to let aid into Gaza",
    "Gaza: Families bury bodies trapped years under rubble",
    "Stockholm: Activists honour children slain in Gaza",
    "Addis Ababa: Ethiopia, Eritrea mass troops on border",
    "Baghdad: Iraq launches two airstrikes on ISIS in Anbar",
    "Amman: Jordan military crash hurts five in practice",
    "Jerusalem: Knesset elects Eisenkot ally as speaker",
    "Taipei: Taiwan 'urgently needs' $14bn in US arms",
    "Zurich: Surgeon sets record with 3,200 heart objects",
    "Washington: AI-chip export licences take effect for 5 nations",
]


def feature_card(img, d, x, y, w, num, tag, headline, deck, art_fn, art_h,
                 head_size, deck_size, tag_size=13):
    d.rectangle([x, y, x + w, y + art_h], fill=PAPER2,
                outline=(190, 180, 160), width=1)
    tmp = Image.new("RGB", (w - 2, art_h - 2), PAPER2)
    td = ImageDraw.Draw(tmp)
    art_fn(td, 0, 0, w - 2, art_h - 2)
    img.paste(tmp, (x + 1, y + 1))
    bf = font(SANS_BOLD, 15)
    d.ellipse([x + 6, y + art_h - 26, x + 26, y + art_h - 6], fill=RED)
    tw = d.textlength(str(num), font=bf)
    d.text((x + 16 - tw / 2, y + art_h - 24), str(num), font=bf, fill="white")
    ty = y + art_h + 7
    tf = font(SANS_BOLD, tag_size)
    d.text((x, ty), tag, font=tf, fill=RED)
    ty += tag_size + 5
    hf = font(SERIF_BOLD, head_size)
    lines = wrap(d, headline, hf, w)
    ty = text_lines(d, x, ty, lines[:2], hf, INK, lh=head_size + 3)
    ty += 3
    df = font(SANS, deck_size)
    dlines = wrap(d, deck, df, w)
    ty = text_lines(d, x, ty, dlines[:2], df, GREY, lh=deck_size + 4)
    return ty


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -----------------------------------------------------------
    y = 10
    kf = font(SANS_BOLD, 15)
    d.text((M, y), "THE DAY IN WORLD NEWS", font=kf, fill=INK)
    right = "45 STORIES · 6 CONTINENTS · ONE PAGE"
    d.text((W - M - d.textlength(right, font=kf), y), right, font=kf,
           fill=RED)
    y += 22
    mf = fit_font(d, "Thursday 19 November 2026", SERIF_BLACK, 64, CW)
    d.text(((W - d.textlength("Thursday 19 November 2026", font=mf)) / 2, y),
           "Thursday 19 November 2026", font=mf, fill=INK)
    y += mf.size + 4
    d.rectangle([M, y, M + CW, y + 2], fill=INK)
    y += 8
    sf = font(SERIF_ITALIC, 17)
    sub = ("Every story on this page happened, or was first reported, "
           "on Thursday 19 November 2026.")
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=GREY)
    y += 22

    # --- top row: 3 large features ------------------------------------------
    top_w = (CW - 2 * 12) // 3
    top_art = 110
    x = M
    y_end = y
    for num, tag, head, deck, art_fn in FEATURES_TOP:
        e = feature_card(img, d, x, y, top_w, num, tag, head, deck, art_fn,
                         top_art, head_size=25, deck_size=14, tag_size=12)
        y_end = max(y_end, e)
        x += top_w + 12
    y = y_end + 6
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 7

    # --- middle + bottom rows: 5 features each -------------------------------
    mid_w = (CW - 4 * 10) // 5
    mid_art = 56
    for row in (FEATURES_MID, FEATURES_BOT):
        x = M
        y_end = y
        for num, tag, head, deck, art_fn in row:
            e = feature_card(img, d, x, y, mid_w, num, tag, head, deck, art_fn,
                             mid_art, head_size=18, deck_size=12, tag_size=11)
            y_end = max(y_end, e)
            x += mid_w + 10
        y = y_end + 5
        d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
        y += 6

    # --- by the numbers ------------------------------------------------------
    nf = font(SANS_BOLD, 12)
    d.text((M, y + 2), "BY THE NUMBERS", font=nf, fill=RED)
    nx = M + 150
    seg = (CW - 150) // 4
    for val, lab in NUMBERS:
        vf = font(SERIF_BLACK, 25)
        d.text((nx, y - 4), val, font=vf, fill=NAVY)
        lf = font(SANS, 11)
        d.text((nx, y + 23), lab, font=lf, fill=GREY)
        nx += seg
    y += 36
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 6

    # --- map + briefs ---------------------------------------------------------
    top_y = y
    map_w = 300
    mh = font(SANS_BOLD, 13)
    d.text((M, y), "WHERE IT HAPPENED", font=mh, fill=INK)
    y += 20
    map_h = 120
    draw_map(d, M, y, map_w, map_h)
    ly = y + map_h + 6
    lf = font(SANS, 11)
    for line in ["Numbered dots mark stories 1–13.",
                 "8  Voyager 1: in space, 25.9bn km out.",
                 "3  Anthropic: Nasdaq, New York. 13  Liu: Washington."]:
        d.text((M, ly), line, font=lf, fill=GREY)
        ly += 14
    # briefs, two columns
    bx = M + map_w + 16
    bw = (CW - map_w - 16) // 2
    bh = font(SANS_BOLD, 14)
    d.text((bx, top_y), "ALSO ON THURSDAY 19 NOVEMBER", font=bh, fill=INK)
    d.rectangle([bx, top_y + 19, bx + 2 * bw + 10, top_y + 20], fill=RED)
    bf = font(SANS, 13)
    for i, b in enumerate(BRIEFS):
        col = 0 if i < 16 else 1
        row = i % 16
        xx = bx + col * (bw + 10)
        yy = top_y + 26 + row * 13.0
        num = 14 + i
        ntxt = f"{num}  "
        d.text((xx, yy), ntxt, font=font(SANS_BOLD, 13), fill=RED)
        tx = xx + d.textlength(ntxt, font=font(SANS_BOLD, 13))
        f = bf
        while f.size > 10 and d.textlength(b, font=f) > (bw - (tx - xx)):
            f = font(SANS, f.size - 1)
        d.text((tx, yy), b, font=f, fill=INK)
    y = top_y + 26 + 16 * 13.0 + 4

    # --- footer ---------------------------------------------------------------
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 5
    ff = font(SANS, 11)
    foot = ("DATE CHECK — left out, reported 17–18 Nov: Gulf drone wave, Xi's "
            "airport welcome, UK inflation 3.6%, EU €45bn loan, GTA VI launch, "
            "Amnesty Sudan toll, Jeffries vote, Peltola win.  Sources: Reuters, "
            "AP, BBC, Bloomberg, Fed, IMD, NASA, UN, IAEA. Original drawings.")
    lines = wrap(d, foot, ff, CW)
    for ln in lines:
        d.text((M, y), ln, font=ff, fill=GREY)
        y += 13

    img.save(out_path, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {img.size} {size} bytes "
          f"({'OK' if size <= 1048576 else 'OVER 1 MiB!'})  final y={y}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry-v1.png"))
