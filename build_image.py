#!/usr/bin/env python3
"""Thursday 19 November 2026 — one-page front page (v4).

Draws the whole broadsheet with PIL from geometric shapes and type only:
no photos, no network, no copied art. The image is the entry; main.ts
copies it to the grader output untouched.

Layout (1024x1024, cream paper):
  masthead -> 3 hero features -> 5 features -> 5 features ->
  numbers strip -> dotted world map + 32 numbered briefs -> footer.
13 features + 32 briefs = 45 stories, all dated Thursday 19 Nov 2026.

Run:  python3 build_image_v4.py       # writes entry.png beside itself
Checks built in: every headline/deck wraps to <=2 lines, every brief fits
one line, final y stays on the canvas, 1024x1024, under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 24                      # side margin
CW = W - 2 * M              # 976 content width
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 18, 31)
NAVY = (31, 58, 95)
GREY = (110, 108, 100)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size, subdir="dejavu"):
    return ImageFont.truetype(
        os.path.join("/usr/share/fonts/truetype", subdir, name), size)


# Noto is ~10% narrower than DejaVu at the same size, which is what lets
# headlines and decks hold to two lines in these column widths.
SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s, "noto")
SERIF = lambda s: font("NotoSerif.ttf", s, "noto")
SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s, "noto")
SANS_B = lambda s: font("NotoSans-Bold.ttf", s, "noto")
SANS = lambda s: font("NotoSans-Regular.ttf", s, "noto")


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tag(draw, x, y, text, fnt, fg=(255, 255, 255), bg=None, pad=4):
    """Small label; optional solid chip behind it. Returns width used."""
    w = int(draw.textlength(text, font=fnt)) + 2 * pad
    h = fnt.size + 2 * pad
    if bg is not None:
        draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad, y + pad - 1), text, font=fnt, fill=fg)
    return w


def badge(draw, cx, cy, num, r=11):
    """Red numbered disc, white number."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = SANS_B(13)
    tw = draw.textlength(str(num), font=f)
    draw.text((cx - tw / 2, cy - 8), str(num), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- features
# (art_key, art_label, kicker, headline, deck)
FEATURES = [
    ("skyline", "SHENZHEN", "ASIA \u00b7 APEC SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen today",
     "Nuclear arms and the Iran war on the table at the first trilateral."),
    ("fed", "MORE HIKES", "AMERICAS \u00b7 FED MINUTES",
     "Fed minutes: more hikes are coming",
     "Waller backs a 50bp December move; gold falls to $3,725."),
    ("ipo", "$83", "GLOBAL \u00b7 TECH IPO",
     "Anthropic prices its IPO at $83 a share",
     "Above the $70\u2013$78 range: about 980m shares, $81.3bn raised. Debuts as ANT today."),
    ("gaza", "CENTRAL GAZA", "MIDDLE EAST \u00b7 GAZA",
     "Israeli tanks push deeper into Gaza",
     "Hamas calls it a truce breach; one killed."),
    ("cyclone", "RED ALERT", "ASIA \u00b7 CYCLONE",
     "Akvan nears coast; 204,000 to move",
     "Landfall Fri noon Narsapur; gusts 110 km/h."),
    ("odesa", "ODESA", "EUROPE \u00b7 UKRAINE WAR",
     "Russian strikes kill four in Odesa",
     "Five dead nationwide; no Donbas-for-NATO swap."),
    ("sudan", "BLACKOUT", "AFRICA \u00b7 SUDAN WAR",
     "Drones black out Sudan's cities",
     "Power stations hit; UN warns aid work disrupted."),
    ("voyager", "VOYAGER 1", "SPACE \u00b7 SCIENCE",
     "Voyager 1 reaches one light-day",
     "25.9bn km out; signal takes a full day to arrive."),
    ("cop", "21 LEFT", "GLOBAL \u00b7 CLIMATE",
     "COP31: 21 issues left, deal in doubt",
     "New drafts due Thursday; summit closes Friday."),
    ("walmart", "$187.3bn", "AMERICAS \u00b7 RETAIL",
     "Walmart reports before the open",
     "$0.64 a share expected on $187.3bn in sales."),
    ("tokyo", "TOKYO", "ASIA \u00b7 DIPLOMACY",
     "India, Japan hold 2+2 defence talks",
     "Amazon pledges $7bn for India renewables by 2030."),
    ("nvidia", "PAY RISES", "AMERICAS \u00b7 CHIPS",
     "Nvidia's new chief promises pay rises",
     "Rises land in December; H-series chips halted."),
    ("gta", "LEONIDA", "GLOBAL \u00b7 GAMES",
     "GTA VI launches today",
     "Midnight launch in New Zealand; 9.7m pre-orders."),
]

BRIEFS = [
    "New York: Oil falls as risk aversion rises; Brent $91.86",
    "Bitcoin slips 0.5% to $62,800 after Fed minutes",
    "Dollar index near 103.78, a 19-month high",
    "US 10-year yield eases to 5.07%",
    "Washington: Trump unhappy Vance did not back Iran war",
    "Senators warn AI cyber threats outpacing defences",
    "Vienna: IAEA: N. Korea enrichment extension complete",
    "Sofia: LPG tanker sunk off Bulgaria hit by shells",
    "Benghazi: Cocaine and millions of pills seized in Libya",
    "Riyadh: Saudi danger passed in three southern cities",
    "Paris: Minister says M\u00e9lenchon could win presidency",
    "Mogadishu: Somalia accuses UAE of secret bases",
    "Islamabad: Pakistan conducts Fatah-3 missile launch",
    "Ottawa: Carney adjusting China ties, seeks US deal",
    "Shenzhen: Security tight at Qilin Shanzhuang",
    "Washington: Liu Yunping leads House Democrats",
    "New Delhi: India's renewable capacity hits 299.25 GW",
    "Washington: US proposes tougher green-card rules",
    "New York: Deutsche Bank handled $582m in Epstein deals",
    "FBI says North Korean hackers stole $400m+",
    "Aden: Houthis edge closer as forces leave Bab al-Mandeb",
    "Palestinians shelter in caves after demolitions",
    "London: Four nations urge Israel to let aid into Gaza",
    "Gaza: Families bury bodies trapped years under rubble",
    "Stockholm: Activists honour children slain in Gaza",
    "Addis Ababa: Ethiopia, Eritrea mass troops on border",
    "Baghdad: Iraq launches two airstrikes on ISIS in Anbar",
    "Amman: Jordan military crash hurts five in practice",
    "Jerusalem: Knesset elects Eisenkot ally as speaker",
    "Taipei: Taiwan 'urgently needs' $14bn in US arms",
    "Kuwait: Iran drones hit Ali Al Salem US base",
    "AI-chip export licences take effect for 5 nations",
]

NUMBERS = [
    ("$3,725", "gold, down 3.2% after Fed minutes"),
    ("$81.3bn", "Anthropic's IPO, priced above range"),
    ("9.69m", "GTA VI pre-orders, worth $942m"),
    ("204,070", "people to move ahead of Akvan"),
]

# ---------------------------------------------------------------- art
# Every illustration is drawn from rectangles, ellipses, polygons and lines.
# Labels sit on plain sky or on a solid chip, never over busy shapes.

def art_skyline(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(213, 227, 235))
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(240, 190, 80))
    base = y + h
    for bx, bw, bh, col in [(0, 26, 46, (90, 110, 135)), (30, 20, 62, (70, 90, 120)),
                            (54, 30, 38, (95, 115, 140)), (88, 22, 70, (60, 80, 110)),
                            (114, 28, 50, (90, 110, 135)), (146, 24, 66, (70, 90, 120)),
                            (174, 30, 44, (95, 115, 140)), (208, 22, 58, (60, 80, 110)),
                            (234, 26, 40, (90, 110, 135)), (264, 24, 52, (70, 90, 120))]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=col)
    d.rectangle([x, base - 10, x + w, base - 6], fill=(120, 90, 60))  # table
    # three flags on the table: US, China, Russia (simple tricolours)
    for fx, cols in [(40, [(180, 40, 50), (255, 255, 255), (40, 60, 140)]),
                     (140, [(220, 40, 40), (220, 40, 40), (220, 40, 40)]),
                     (240, [(255, 255, 255), (40, 80, 180), (220, 40, 40)])]:
        for i, c in enumerate(cols):
            d.rectangle([x + fx, base - 26 + i * 5, x + fx + 22, base - 21 + i * 5], fill=c)
        d.line([x + fx, base - 26, x + fx, base - 10], fill=INK, width=1)


def art_fed(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 232, 222))
    base = y + h - 12
    for i, bh in enumerate([18, 28, 24, 40, 34, 52]):
        bx = x + 16 + i * 34
        d.rectangle([bx, base - bh, bx + 20, base], fill=NAVY)
    d.line([x + 14, base - 58, x + w - 30, base - 66], fill=RED, width=3)
    d.polygon([(x + w - 30, base - 66), (x + w - 44, base - 70), (x + w - 44, base - 60)],
              fill=RED)
    d.ellipse([x + w - 52, base - 34, x + w - 20, base - 2], fill=(212, 175, 55))
    d.ellipse([x + w - 52, base - 34, x + w - 20, base - 2], outline=(150, 120, 30))
    f = SANS_B(16)
    d.text((x + w - 42, base - 29), "$", font=f, fill=(120, 90, 20))


def art_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 228))
    pts = [(x + 12, y + h - 18), (x + 60, y + h - 34), (x + 110, y + h - 26),
           (x + 160, y + h - 44), (x + 210, y + h - 52), (x + 260, y + h - 66),
           (x + w - 16, y + 22)]
    d.line(pts, fill=(40, 140, 70), width=3)
    d.ellipse([x + w - 26, y + 12, x + w - 6, y + 32], fill=(40, 140, 70))
    # opening bell: gold dome + base, centre-left
    cx = x + 78
    d.pieslice([cx - 26, y + h - 52, cx + 26, y + h - 8], 180, 360, fill=(212, 175, 55))
    d.rectangle([cx - 30, y + h - 12, cx + 30, y + h - 6], fill=(180, 140, 40))
    d.ellipse([cx - 4, y + h - 8, cx + 4, y + h], fill=(180, 140, 40))


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.polygon([(x, y + h), (x + 70, y + 34), (x + 150, y + h)], fill=(214, 196, 160))
    d.polygon([(x + 90, y + h), (x + w, y + 44), (x + w, y + h)], fill=(204, 184, 146))
    # tank, centre-right
    tx, ty = x + w - 88, y + h - 40
    d.rectangle([tx, ty, tx + 62, ty + 16], fill=(74, 88, 66))
    d.rectangle([tx + 14, ty - 12, tx + 40, ty], fill=(74, 88, 66))
    d.line([tx + 40, ty - 8, tx + 62, ty - 12], fill=(60, 72, 54), width=4)
    for wx in (8, 26, 44):
        d.ellipse([tx + wx, ty + 16, tx + wx + 10, ty + 22], fill=(50, 60, 46))


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 222, 235))
    # India coast, right edge
    d.polygon([(x + w - 52, y), (x + w, y), (x + w, y + h),
               (x + w - 44, y + h), (x + w - 58, y + h - 30),
               (x + w - 48, y + 30)], fill=(222, 208, 170))
    # cyclone swirl: concentric arcs, centre-left
    cx, cy = x + 62, y + h // 2 + 4
    for r, col in [(44, (255, 255, 255)), (34, (150, 185, 210)),
                   (24, (255, 255, 255)), (14, (150, 185, 210))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    # rain ticks, top-right sky (clear of the chip)
    for i in range(4):
        rx = x + w - 90 + i * 12
        d.line([rx, y + 10, rx - 4, y + 22], fill=(140, 170, 195), width=2)


def art_odesa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 214, 170))
    base = y + h
    for bx, bw, bh in [(0, 30, 34), (34, 22, 48), (60, 34, 30), (98, 24, 44),
                       (126, 30, 36), (160, 26, 50)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(90, 70, 60))
    # explosion starburst, top-right clear sky
    ex, ey = x + w - 42, y + 26
    for ang in range(0, 360, 30):
        import math as _m
        r1, r2 = 6, 20
        x1, y1 = ex + r1 * _m.cos(_m.radians(ang)), ey + r1 * _m.sin(_m.radians(ang))
        x2, y2 = ex + r2 * _m.cos(_m.radians(ang)), ey + r2 * _m.sin(_m.radians(ang))
        d.line([x1, y1, x2, y2], fill=(230, 120, 30), width=3)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(245, 180, 60))
    d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 230, 150))


def art_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 48))
    base = y + h
    for bx, bw, bh in [(0, 26, 30), (30, 20, 44), (54, 28, 26), (86, 22, 40),
                       (112, 30, 32), (146, 24, 46), (174, 26, 28)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(12, 14, 24))
    # one lit window, far left
    d.rectangle([x + 8, base - 22, x + 14, base - 14], fill=(250, 210, 90))
    # drone silhouette, top-right
    dx, dy = x + w - 56, y + 16
    d.ellipse([dx, dy, dx + 26, dy + 8], fill=(200, 200, 210))
    d.line([dx - 12, dy + 2, dx + 38, dy + 2], fill=(160, 160, 170), width=2)
    d.ellipse([dx - 14, dy - 2, dx - 6, dy + 6], fill=(160, 160, 170))
    d.ellipse([dx + 32, dy - 2, dx + 40, dy + 6], fill=(160, 160, 170))
    d.line([dx + 13, dy + 8, dx + 13, dy + 16], fill=(160, 160, 170), width=2)


def art_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    import random as _r
    _r.seed(19)
    for _ in range(26):
        sx, sy = x + _r.randint(4, w - 4), y + _r.randint(4, h - 4)
        r = _r.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # dish, right half; boom to the left
    cx, cy = x + w - 44, y + h // 2 + 6
    d.line([x + 30, cy + 12, cx - 16, cy + 4], fill=(180, 180, 190), width=3)
    d.ellipse([cx - 26, cy - 20, cx + 22, cy + 18], fill=(200, 200, 210))
    d.ellipse([cx - 26, cy - 20, cx + 22, cy + 18], outline=(140, 140, 150))
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 8], fill=(120, 120, 130))
    d.ellipse([x + 18, y + h - 18, x + 30, y + h - 6], fill=(90, 140, 200))
    d.ellipse([x + w - 16, y + 12, x + w - 6, y + 22], fill=(240, 200, 90))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 228))
    cx, cy = x + 52, y + h // 2 + 2
    d.ellipse([cx - 30, cy - 26, cx + 30, cy + 26], fill=(90, 150, 200))
    d.ellipse([cx - 16, cy - 20, cx + 2, cy - 2], fill=(110, 180, 110))
    d.ellipse([cx - 2, cy + 6, cx + 20, cy + 22], fill=(110, 180, 110))
    d.ellipse([cx - 30, cy - 26, cx + 30, cy + 26], outline=(60, 110, 160))
    # gavel, bottom-right (keeps the top-right RED ALERT chip clear)
    gx, gy = x + w - 52, y + h - 40
    d.line([gx, gy + 26, gx + 34, gy + 4], fill=(120, 85, 50), width=4)
    d.rectangle([gx + 24, gy, gx + 44, gy + 12], fill=(90, 60, 35))
    d.rectangle([gx + 6, gy + 30, gx + 40, gy + 36], fill=(140, 105, 65))


def art_walmart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 234, 240))
    # storefront band, upper half
    d.rectangle([x, y + 8, x + w, y + 34], fill=(30, 80, 160))
    d.rectangle([x + 10, y + 14, x + 30, y + 28], fill=(255, 255, 255))
    d.rectangle([x + 40, y + 14, x + 60, y + 28], fill=(255, 255, 255))
    d.rectangle([x + 70, y + 14, x + 90, y + 28], fill=(255, 255, 255))
    # cart, lower half
    cx, cy = x + 40, y + h - 30
    d.polygon([(cx, cy), (cx + 90, cy), (cx + 80, cy + 22), (cx + 10, cy + 22)],
              outline=(60, 60, 60), width=3)
    d.line([cx - 12, cy - 8, cx, cy], fill=(60, 60, 60), width=3)
    for wx in (16, 52):
        d.ellipse([cx + wx, cy + 24, cx + wx + 10, cy + 34], fill=(60, 60, 60))
    d.rectangle([cx + 14, cy - 16, cx + 66, cy - 4], fill=(90, 140, 200))


def art_tokyo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
    d.ellipse([x + w - 40, y + 8, x + w - 14, y + 34], fill=(220, 60, 60))
    # torii gate, centre-left
    gx = x + 30
    d.rectangle([gx, y + 18, gx + 6, y + h - 10], fill=(190, 40, 40))
    d.rectangle([gx + 44, y + 18, gx + 50, y + h - 10], fill=(190, 40, 40))
    d.rectangle([gx - 8, y + 12, gx + 58, y + 20], fill=(190, 40, 40))
    d.rectangle([gx - 2, y + 30, gx + 52, y + 36], fill=(190, 40, 40))
    # small flags, right
    for fx, cols in [(x + w - 78, [(255, 255, 255), (220, 40, 40)]),
                     (x + w - 48, [(255, 170, 60), (255, 255, 255), (20, 120, 60)])]:
        for i, c in enumerate(cols):
            d.rectangle([fx, y + h - 26 + i * 6, fx + 20, y + h - 20 + i * 6], fill=c)


def art_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 238, 226))
    cx, cy = x + 44, y + h // 2
    d.rectangle([cx - 22, cy - 22, cx + 22, cy + 22], fill=(118, 185, 0))
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(90, 150, 0))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    for px in (cx - 30, cx + 26):
        for py in (cy - 16, cy - 4, cy + 8):
            d.line([px, py, px + 8 if px < cx else px - 8, py],
                   fill=(70, 110, 0), width=2)
    d.line([x + w - 78, y + h - 16, x + w - 18, y + 16], fill=(40, 140, 70), width=3)
    d.polygon([(x + w - 18, y + 16), (x + w - 32, y + 18), (x + w - 20, y + 30)],
              fill=(40, 140, 70))


def art_gta(d, x, y, w, h):
    # dusk gradient: violet top -> orange horizon
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(58 + (245 - 58) * t)
        g = int(32 + (140 - 32) * t)
        b = int(110 + (60 - 110) * t)
        d.line([x, y + i, x + w, y + i], fill=(r, g, b))
    d.ellipse([x + w // 2 - 16, y + 8, x + w // 2 + 16, y + 40], fill=(255, 190, 90))
    base = y + h
    for bx, bw, bh in [(0, 22, 30), (26, 16, 44), (46, 24, 34), (74, 18, 50),
                       (96, 26, 38), (126, 20, 46), (150, 24, 32), (178, 18, 40)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(20, 12, 30))
        for wy in range(base - bh + 6, base - 4, 9):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 4], fill=(255, 210, 110))
    # palm, left foreground
    px, py = x + 14, base
    d.line([px, py, px + 6, py - 26], fill=(15, 10, 25), width=3)
    for dx, dy in [(-12, -30), (16, -32), (-4, -36), (10, -26)]:
        d.line([px + 6, py - 26, px + 6 + dx, py - 26 + dy // 3 + 8],
               fill=(15, 10, 25), width=2)
    # neon VI, top-right clear sky (pink halo, white core)
    f = SANS_B(30)
    d.text((x + w - 64, y + 6), "VI", font=f, fill=(255, 80, 200))
    d.text((x + w - 66, y + 4), "VI", font=f, fill=(255, 255, 255))


ART = {
    "skyline": art_skyline, "fed": art_fed, "ipo": art_ipo, "gaza": art_gaza,
    "cyclone": art_cyclone, "odesa": art_odesa, "sudan": art_sudan,
    "voyager": art_voyager, "cop": art_cop, "walmart": art_walmart,
    "tokyo": art_tokyo, "nvidia": art_nvidia, "gta": art_gta,
}

# label placement per feature: (position, chip) — chips keep text off busy art
# position: "tl" top-left, "tr" top-right, "br" bottom-right
LABEL_STYLE = {
    "skyline": ("tl", None), "fed": ("tl", None), "ipo": ("tl", (20, 40, 90)),
    "gaza": ("tl", None), "cyclone": ("tr", RED), "odesa": ("tl", None),
    "sudan": ("tl", None), "voyager": ("tl", None), "cop": ("tr", RED),
    "walmart": ("tl", (255, 255, 255)), "tokyo": ("tl", None),
    "nvidia": ("br", (255, 255, 255)), "gta": ("tl", None),
}
LABEL_FG = {
    "ipo": (255, 255, 255), "cyclone": (255, 255, 255), "cop": (255, 255, 255),
    "walmart": NAVY, "nvidia": (30, 110, 40),
    "sudan": (255, 255, 255), "voyager": (255, 255, 255), "gta": (255, 255, 255),
}

# ---------------------------------------------------------------- layout

def draw_feature(d, idx, x, y, w, art_h, head_size, deck_size):
    """One feature card. Returns the y just below the deck."""
    key, label, kicker, headline, deck = FEATURES[idx]
    d.rectangle([x, y, x + w, y + art_h], outline=(200, 195, 185))
    ART[key](d, x + 1, y + 1, w - 2, art_h - 2)
    pos, chip = LABEL_STYLE[key]
    lf = SANS_B(11)
    fg = LABEL_FG.get(key, INK)
    tw = int(d.textlength(label, font=lf)) + 8
    if pos == "tl":
        lx, ly = x + 5, y + 5
    elif pos == "tr":
        lx, ly = x + w - tw - 5, y + 5
    else:
        lx, ly = x + w - tw - 5, y + art_h - 20
    if chip is not None:
        d.rectangle([lx - 4, ly - 3, lx + tw, ly + 13], fill=chip)
    d.text((lx, ly), label, font=lf, fill=fg)
    badge(d, x + 12, y + art_h - 12, idx + 1)
    ky = y + art_h + 6
    d.text((x, ky), kicker, font=SANS_B(11), fill=RED)
    hy = ky + 15
    hl, hy2 = wrap(d, headline, SERIF_B(head_size), w), None
    lh = int(head_size * 1.15)
    yy = hy
    for ln in hl:
        d.text((x, yy), ln, font=SERIF_B(head_size), fill=INK)
        yy += lh
    dy = yy + 2
    dl, _ = wrap(d, deck, SANS(deck_size), w), None
    dlh = int(deck_size * 1.22)
    for ln in dl:
        d.text((x, dy), ln, font=SANS(deck_size), fill=(60, 58, 52))
        dy += dlh
    return dy, len(hl), len(dl)


# Dotted world map: coarse continent polygons, lon/lat -> x/y.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 42),
     (-75, 35), (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22),
     (-110, 24), (-115, 30), (-120, 34), (-125, 40), (-125, 48),
     (-135, 58), (-150, 60), (-165, 60)],
    # Greenland
    [(-55, 60), (-40, 65), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-60, 70)],
    # South America
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-45, -5), (-38, -8), (-35, -10), (-40, -20), (-48, -28), (-55, -35),
     (-65, -40), (-70, -50), (-73, -55), (-70, -45), (-72, -35), (-72, -20),
     (-78, -10), (-80, 0)],
    # Africa
    [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (5, 37), (10, 37), (20, 32),
     (30, 31), (35, 28), (38, 22), (40, 15), (43, 11), (48, 11), (51, 10),
     (45, 0), (40, -10), (35, -18), (30, -25), (25, -33), (18, -35),
     (15, -30), (12, -18), (10, -5), (8, 4), (0, 5), (-8, 5), (-15, 10)],
    # Eurasia
    [(-10, 36), (-9, 43), (-5, 48), (0, 50), (5, 55), (8, 57), (12, 55),
     (18, 56), (21, 59), (25, 60), (30, 62), (35, 65), (45, 68), (60, 69),
     (75, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66),
     (178, 65), (170, 60), (160, 55), (150, 60), (140, 55), (135, 45),
     (130, 40), (127, 38), (122, 32), (115, 25), (108, 18), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (77, 8), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 28), (48, 30), (45, 32), (40, 36),
     (35, 36), (30, 36), (25, 38), (20, 40), (15, 44), (10, 44), (5, 43),
     (0, 40), (-5, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -35), (125, -33), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -30), (150, -22),
     (146, -19), (142, -15), (140, -17), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (133, 34), (137, 36), (140, 39), (142, 43), (144, 44),
     (141, 40), (138, 35), (132, 33)],
    # Indonesia
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -9), (130, -5), (135, -4), (140, -7), (138, -9), (125, -11),
     (110, -9), (100, -2)],
    # New Zealand
    [(167, -45), (170, -41), (173, -38), (176, -38), (178, -42), (174, -46),
     (170, -47)],
]

# story pins: (lon, lat) — 8 (Voyager) has no earthly pin, noted in text
PINS = {1: (114, 22), 2: (-77, 39), 3: (-74, 41), 4: (34, 31), 5: (85, 19),
        6: (31, 46), 7: (32, 15), 9: (-48, -1), 10: (-94, 36), 11: (139, 35),
        12: (-122, 37), 13: (175, -41)}


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
           (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_map(d, x, y, w, h):
    lon0, lon1, lat0, lat1 = -172, 192, 78, -58
    step = 7
    dot = (110, 135, 120)
    for gy in range(y, y + h, step):
        lat = lat1 + (lat0 - lat1) * (gy - y) / max(h - 1, 1)
        for gx in range(x, x + w, step):
            lon = lon0 + (lon1 - lon0) * (gx - x) / max(w - 1, 1)
            if any(_inside(lon, lat, p) for p in CONTINENTS):
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=dot)
    for num, (lon, lat) in PINS.items():
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        badge(d, px, py, num, r=9)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    problems = []

    # ---- masthead
    d.text((M, 10), "THE DAY IN WORLD NEWS", font=SANS_B(15), fill=INK)
    right = "45 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    d.text((W - M - d.textlength(right, font=SANS_B(15)), 10), right,
           font=SANS_B(15), fill=RED)
    d.text((M, 28), "Thursday 19 November 2026", font=SERIF_B(60), fill=INK)
    d.line([M, 96, W - M, 96], fill=RULE, width=2)
    sub = "Every story on this page happened, or was first reported, on Thursday 19 November 2026."
    d.text(((W - d.textlength(sub, font=SERIF_I(16))) / 2, 102), sub,
           font=SERIF_I(16), fill=(70, 68, 62))

    # ---- hero row (3 across)
    y = 128
    hero_w = [317, 317, 320]
    hx = [M, M + 317 + 12, M + 317 + 12 + 317 + 12]
    ends = []
    for i in range(3):
        end, hl, dl = draw_feature(d, i, hx[i], y, hero_w[i], 92, 26, 14)
        ends.append(end)
        if hl > 2 or dl > 2:
            problems.append(f"hero {i+1}: headline {hl} lines, deck {dl} lines")
    y = max(ends) + 10

    # ---- rows 2 and 3 (5 across)
    col_w, gap = 187, 10
    xs = [M + i * (col_w + gap) for i in range(5)]
    xs[4] = W - M - col_w
    for row, base in enumerate((3, 8)):
        ends = []
        for j in range(5):
            end, hl, dl = draw_feature(d, base + j, xs[j], y, col_w, 64, 19, 13)
            ends.append(end)
            if hl > 2 or dl > 2:
                problems.append(f"feature {base+j+1}: headline {hl} lines, deck {dl} lines")
        y = max(ends) + 10

    # ---- numbers strip (cells start right of the header, labels fit the cell)
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6
    d.text((M, y), "BY THE NUMBERS", font=SANS_B(12), fill=INK)
    x0 = M + 135
    cell = (W - M - x0) // 4
    for i, (num, label) in enumerate(NUMBERS):
        cx = x0 + i * cell
        if d.textlength(label, font=SANS(11)) > cell - 4:
            problems.append(f"number label {i} overflows its cell")
        d.text((cx, y - 4), num, font=SERIF_B(29), fill=NAVY)
        d.text((cx, y + 26), label, font=SANS(11), fill=(60, 58, 52))
    y += 46
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 8

    # ---- map + briefs
    d.text((M, y), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    bx = 340
    d.text((bx, y), "ALSO ON THURSDAY 19 NOVEMBER", font=SANS_B(12), fill=INK)
    y += 18
    d.line([bx, y - 4, W - M, y - 4], fill=RED, width=1)
    map_y, map_h = y, 148
    draw_map(d, M, map_y, 300, map_h)
    note = ("Numbered dots mark stories 1\u201313. 8 Voyager 1: in space, "
            "25.9bn km out. 3 Anthropic: Nasdaq, New York. "
            "13 GTA VI: first launch in New Zealand.")
    ny = map_y + map_h + 6
    for ln in wrap(d, note, SANS(10), 300):
        d.text((M, ny), ln, font=SANS(10), fill=(70, 68, 62))
        ny += 12
    # briefs, two columns of 16
    bf = SANS(10)
    bf_n = SANS_B(10)
    col_x = [bx, bx + 336]
    col_w_b = 324
    for ci in range(2):
        by = y
        for k in range(16):
            n = 14 + ci * 16 + k
            text = BRIEFS[n - 14]
            num_w = d.textlength(f"{n} ", font=bf_n)
            if d.textlength(text, font=bf) > col_w_b - num_w - 4:
                problems.append(f"brief {n} overflows one line")
            d.text((col_x[ci], by), f"{n}", font=bf_n, fill=RED)
            d.text((col_x[ci] + num_w, by), text, font=bf, fill=INK)
            by += 12
    y = map_y + map_h + 6 + 3 * 12 + 8

    # ---- footer
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 4
    foot1 = ("DATE CHECK \u2014 left out, reported 17\u201318 Nov: Xi's airport welcome, UK inflation 3.6%, "
             "EU \u20ac45bn loan, Amnesty Sudan toll, Jeffries vote, Peltola win. "
             "Kuwait strike first reported overnight into 19 Nov.")
    foot2 = ("Sources: Reuters, AP, BBC, Bloomberg, Fed, IMD, NASA, UN, IAEA, Rockstar Games, Take-Two. "
             "Original drawings.")
    for ln in (foot1, foot2):
        for sub_ln in wrap(d, ln, SANS(10), CW):
            d.text((M, y), sub_ln, font=SANS(10), fill=(70, 68, 62))
            y += 12

    if y > H - 2:
        problems.append(f"layout overflow: final y={y}")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" -", p)
        return None
    img.save(OUT, "JPEG", quality=88)
    size = os.path.getsize(OUT)
    print(f"stories: {len(FEATURES)} features + {len(BRIEFS)} briefs = "
          f"{len(FEATURES) + len(BRIEFS)}")
    print(f"size: {img.size}, bytes: {size} ({'OK <1MiB' if size < 1048576 else 'TOO BIG'})")
    print(f"final y: {y} / {H}")
    return OUT


if __name__ == "__main__":
    out = build()
    raise SystemExit(0 if out else 1)
