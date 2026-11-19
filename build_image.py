#!/usr/bin/env python3
"""Render the Thursday 19 November 2026 newspaper front page.

One image, 1024x1024, JPEG bytes written to entry.png next to this file:
a masthead, 13 illustrated feature stories, 32 one-line briefs, a
numbers strip, a dotted world map and a footer. Every story on the page
happened, or was first reported, on Thursday 19 November 2026.
Run:  python3 build_image.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 241, 227)      # newsprint cream
INK = (24, 24, 24)          # near-black text
RED = (176, 32, 32)         # kicker / badge red
RULE = (60, 55, 48)         # hairline rules
SOFT = (90, 84, 72)         # secondary text

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LIB_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    """Load a font face, trying DejaVu then Liberation, else plain sans."""
    for folder in (FONT_DIR, LIB_DIR):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), size)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, name, start, width):
    """Largest size (from `start` down) at which `text` fits `width`."""
    size = start
    while size > 10:
        fnt = font(name, size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
        size -= 1
    return font(name, 10)


# ---------------------------------------------------------------- data ---

MASTHEAD = "Thursday 19 November 2026"
SUBTITLE = ("Every story on this page happened, or was first reported, "
            "on Thursday 19 November 2026.")
TOP_LEFT = "THE DAY IN WORLD NEWS"
TOP_RIGHT = "45 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"

# (tag, kicker, headline, deck, art key) — 13 features.
FEATURES = [
    ("SHENZHEN", "ASIA \u00b7 APEC SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen today",
     "Nuclear arms and the Iran war on the table at the first trilateral.",
     "shenzhen"),
    ("MORE HIKES", "AMERICAS \u00b7 FED MINUTES",
     "Fed minutes: more hikes are coming",
     "Waller backs a 50bp December move; gold falls to $3,725.",
     "fed"),
    ("$83", "GLOBAL \u00b7 TECH IPO",
     "Anthropic prices its IPO at $83 a share",
     "Above the $70\u2013$78 range: about 980m shares, $81.3bn raised. "
     "Debuts as ANT today.",
     "ipo"),
    ("CENTRAL GAZA", "MIDDLE EAST \u00b7 GAZA",
     "Israeli tanks push deeper into Gaza",
     "Hamas calls it a truce breach; one killed, families flee.",
     "gaza"),
    ("BAY OF BENGAL", "ASIA \u00b7 CYCLONE",
     "Akvan nears coast; 204,000 to move",
     "Landfall Fri noon Narsapur\u2013Puri; gusts 110 km/h.",
     "akvan"),
    ("ODESA", "EUROPE \u00b7 UKRAINE WAR",
     "Russian strikes kill four in Odesa",
     "Five dead nationwide. Zelenskyy rejects Donbas for NATO.",
     "odesa"),
    ("BLACKOUT", "AFRICA \u00b7 SUDAN WAR",
     "Drone strikes black out Sudan\u2019s cities",
     "Power stations hit; UN warns aid work is disrupted.",
     "sudan"),
    ("1 LIGHT-DAY", "SPACE \u00b7 SCIENCE",
     "Voyager 1 reaches one light-day",
     "25.9bn km out; its signal takes a full day to arrive.",
     "voyager"),
    ("21 LEFT", "GLOBAL \u00b7 CLIMATE",
     "COP31: 21 issues left, deal in doubt",
     "New draft texts due early Thursday. Summit closes Friday.",
     "cop"),
    ("$187.3bn", "AMERICAS \u00b7 RETAIL",
     "Walmart reports before the open",
     "$0.64 a share expected on $187.3bn in sales.",
     "walmart"),
    ("TOKYO", "ASIA \u00b7 DIPLOMACY",
     "India, Japan hold 2+2 defence talks",
     "Amazon pledges $7bn for renewables in India by 2030.",
     "tokyo"),
    ("PAY RISES", "AMERICAS \u00b7 CHIPS",
     "Nvidia\u2019s new chief promises pay rises",
     "Rises land in December. Nvidia halts H-series chips to China.",
     "nvidia"),
    ("", "US \u00b7 POLITICS",
     "Liu Yunping leads House Democrats",
     "First Taiwanese American and Asian American in the chair.",
     "liu"),  # no dark tag: the art carries a "FIRST" speech bubble
]

# One-line briefs, numbered 14-45, two columns of sixteen.
BRIEFS = [
    "New York: Oil falls as risk aversion rises; Brent $91.86",
    "Bitcoin slips 0.5% to about $62,800 after Fed minutes",
    "Dollar index near 103.78, a 19-month high",
    "US 10-year yield eases to 5.07%",
    "Washington: Trump unhappy Vance did not back Iran war \u2014 NYT",
    "Washington: Senators warn AI cyber threats outpacing defences",
    "Vienna: IAEA says North Korea enrichment extension complete",
    "Sofia: LPG tanker that sank off Bulgaria was hit by projectiles",
    "Benghazi: Cocaine and millions of pills seized in Libya",
    "Riyadh: Saudi Arabia says danger passed in three southern oases",
    "Paris: Minister says M\u00e9lenchon could win presidency",
    "Mogadishu: Somalia accuses UAE of building secret bases",
    "Islamabad: Pakistan conducts Fatah-3 missile launch",
    "Ottawa: Carney says Canada adjusting China ties, seeks US deal",
    "Shenzhen: Security tight at Qilin Shanzhuang ahead of summit",
    "Bhopal: India women open Asian Champions Trophy vs Malaysia",
    "New Delhi: India\u2019s renewable capacity hits 299.25 GW",
    "Washington: US proposes tougher green-card rules",
    "New York: Deutsche Bank handled $582m in Epstein deals \u2014 FT",
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
    "Taipei: Taiwan \u2018urgently needs\u2019 $14bn in US arms",
    "Zurich: Surgeon sets record with 3,200 heart objects",
    "Washington: AI-chip export licences take effect for 5 nations",
]

NUMBERS = [
    ("$3,725", "gold, down 3.2% after the Fed minutes"),
    ("$81.3bn", "Anthropic\u2019s IPO, priced above range"),
    ("25.9bn km", "Voyager 1 from Earth: one light-day"),
    ("204,070", "people identified for Akvan evacuation"),
]

MAP_CAPTION = [
    "Numbered dots mark stories 1\u201313.",
    "8 Voyager 1: in space, 25.9bn km out.",
    "3 Anthropic: Nasdaq, New York. 13 Liu: Washington.",
]

FOOTER = ("DATE CHECK \u2014 left out, reported 17\u201318 Nov: Gulf drone wave, "
          "Xi\u2019s airport welcome, UK inflation 3.6%, EU \u20ac45bn loan, "
          "GTA VI launch, Amnesty Sudan toll, Jeffries vote, Peltola win. "
          "Sources: Reuters, AP, BBC, Bloomberg, Fed, IMD, NASA, UN, IAEA. "
          "Original drawings.")


# ------------------------------------------------------- panel pieces ---

def tag(draw, x, y, text, fill=INK, fg=(250, 246, 236)):
    """Small dark label chip; returns its width."""
    fnt = font(SANS_B, 11)
    w = int(draw.textlength(text, font=fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=2, fill=fill)
    draw.text((x + 6, y + 2), text, font=fnt, fill=fg)
    return w


def badge(draw, x, y, n):
    """Red circled story number, bottom-left of an art panel."""
    r = 11
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED,
                 outline=(250, 246, 236), width=1)
    fnt = font(SANS_B, 12)
    s = str(n)
    tw = draw.textlength(s, font=fnt)
    draw.text((x + r - tw / 2, y + 4), s, font=fnt, fill=(255, 255, 255))


def panel(draw, x, y, w, h, bg):
    """Art panel: filled rect with a thin dark border."""
    draw.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=1)
    return x, y, w, h


def skyline(draw, x, y, w, h, color):
    """A row of dark buildings of varied heights along the base."""
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(12, 26)
        bh = rnd.randint(int(h * 0.35), int(h * 0.85))
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=color)
        bx += bw + 3


def flag(draw, x, y, colors):
    """A tiny vertical tricolour flag on a pole."""
    draw.line([x, y, x, y + 26], fill=INK, width=2)
    for i, c in enumerate(colors):
        draw.rectangle([x + 2, y + i * 6, x + 16, y + i * 6 + 6], fill=c)


# ------------------------------------------------------------ art work ---

def art_shenzhen(d, x, y, w, h):
    panel(d, x, y, w, h, (216, 231, 240))
    d.ellipse([x + w - 42, y + 8, x + w - 14, y + 36], fill=(232, 190, 90))
    skyline(d, x, y + 18, w, h - 18, (58, 74, 96))
    d.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 10], fill=(120, 92, 60))
    flag(d, x + 30, y + h - 44, [(200, 40, 40), (255, 255, 255), (40, 60, 160)])
    flag(d, x + 90, y + h - 44, [(0, 0, 0), (200, 30, 30), (240, 200, 0)])
    flag(d, x + 150, y + h - 44, [(255, 255, 255), (40, 60, 200), (200, 30, 30)])


def art_fed(d, x, y, w, h):
    panel(d, x, y, w, h, (228, 222, 208))
    base = y + h - 12
    bars = [26, 40, 34, 52, 46, 64]
    bw = 16
    for i, bh in enumerate(bars):
        bx = x + 18 + i * (bw + 6)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(38, 52, 86))
    d.line([x + 12, base - 58, x + w - 16, base - 78], fill=RED, width=3)
    d.polygon([(x + w - 16, base - 78), (x + w - 30, base - 78),
               (x + w - 22, base - 66)], fill=RED)
    d.ellipse([x + w - 52, y + h - 46, x + w - 20, y + h - 14],
              fill=(212, 168, 60), outline=(150, 110, 30), width=2)
    d.text((x + w - 42, y + h - 42), "$", font=font(SANS_B, 20),
           fill=(120, 84, 20))


def art_ipo(d, x, y, w, h):
    panel(d, x, y, w, h, (206, 229, 220))
    pts = [(x + 10, y + h - 22), (x + 55, y + h - 44), (x + 95, y + h - 34),
           (x + 140, y + h - 52), (x + 185, y + h - 40), (x + w - 12, y + h - 62)]
    d.line(pts, fill=(30, 120, 70), width=3, joint="curve")
    d.polygon([(x + w - 12, y + h - 62), (x + w - 26, y + h - 60),
               (x + w - 18, y + h - 48)], fill=(30, 120, 70))
    cx, cy = x + w // 2, y + h - 34
    d.pieslice([cx - 26, cy - 18, cx + 26, cy + 18], 180, 360,
               fill=(212, 168, 60), outline=(150, 110, 30), width=2)
    d.rectangle([cx - 30, cy + 14, cx + 30, cy + 19], fill=(212, 168, 60),
                outline=(150, 110, 30), width=1)
    d.ellipse([cx - 4, cy + 19, cx + 4, cy + 25], fill=(150, 110, 30))
    tag(d, x + w - 52, y + 6, "$83", fill=(30, 40, 70))


def art_gaza(d, x, y, w, h):
    panel(d, x, y, w, h, (210, 208, 192))
    d.polygon([(x, y + h), (x + 50, y + 26), (x + 100, y + h)],
              fill=(170, 164, 140))
    d.polygon([(x + 70, y + h), (x + 130, y + 40), (x + w, y + h)],
              fill=(186, 180, 156))
    tx, ty = x + w // 2 - 30, y + h - 40
    d.rectangle([tx, ty, tx + 64, ty + 18], fill=(74, 84, 66))
    d.rectangle([tx + 14, ty - 12, tx + 44, ty], fill=(74, 84, 66))
    d.line([tx + 44, ty - 6, tx + 84, ty - 10], fill=(60, 68, 54), width=4)
    for wx in range(tx + 4, tx + 60, 12):
        d.ellipse([wx, ty + 18, wx + 9, ty + 27], fill=(52, 58, 48))


def art_akvan(d, x, y, w, h):
    panel(d, x, y, w, h, (208, 226, 238))
    cx, cy = x + w // 2 - 18, y + h // 2 + 4
    for r, col in [(34, (120, 160, 190)), (26, (90, 135, 170)),
                   (18, (60, 105, 145)), (10, (40, 80, 120))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 80, 120))
    d.polygon([(x + w - 52, y + 8), (x + w - 8, y + 8), (x + w - 8, y + h - 8),
               (x + w - 52, y + h - 8)], fill=(232, 214, 170))
    d.line([x + w - 52, y + 8, x + w - 52, y + h - 8], fill=(200, 170, 110),
           width=1)
    d.text((x + w - 48, y + h // 2 - 6), "INDIA", font=font(SANS_B, 10),
           fill=(120, 60, 40))
    tag(d, x + w - 82, y + h - 24, "RED ALERT", fill=RED)


def art_odesa(d, x, y, w, h):
    panel(d, x, y, w, h, (232, 210, 170))
    skyline(d, x, y + 6, w, h - 6, (96, 78, 60))
    ex, ey = x + w - 52, y + 22
    for dx, dy in [(0, -14), (12, -8), (14, 6), (0, 14), (-12, 6), (-13, -7)]:
        d.polygon([(ex, ey), (ex + dx, ey + dy), (ex + dy // 2, ey - dx // 2)],
                  fill=(240, 150, 40))
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(250, 200, 60))
    d.ellipse([x + 30, y + 10, x + 52, y + 26], fill=(120, 116, 108))
    d.ellipse([x + 44, y + 4, x + 60, y + 16], fill=(140, 136, 128))


def art_sudan(d, x, y, w, h):
    panel(d, x, y, w, h, (28, 34, 52))
    for sx, sy in [(20, 14), (60, 26), (120, 10), (160, 30), (40, 44),
                   (100, 48), (150, 52)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(220, 220, 200))
    d.rectangle([x + 14, y + h - 22, x + w - 14, y + h - 8], fill=(16, 20, 32))
    for wx in range(x + 20, x + w - 20, 14):
        d.rectangle([wx, y + h - 30, wx + 5, y + h - 22], fill=(240, 200, 80))
    cx, cy = x + w // 2, y + 26
    d.ellipse([cx - 22, cy - 5, cx + 22, cy + 5], fill=(200, 200, 190))
    d.line([cx, cy, cx, cy + 12], fill=(200, 200, 190), width=3)
    d.line([cx - 22, cy, cx - 30, cy - 8], fill=(200, 200, 190), width=2)
    d.line([cx + 22, cy, cx + 30, cy - 8], fill=(200, 200, 190), width=2)


def art_voyager(d, x, y, w, h):
    panel(d, x, y, w, h, (16, 22, 44))
    import random
    rnd = random.Random(19)
    for _ in range(26):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, h - 4)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx, sy, sx + r, sy + r], fill=(235, 235, 220))
    px, py = x + w // 2 + 10, y + h // 2 - 6
    d.polygon([(px, py), (px + 26, py - 12), (px + 26, py + 12)],
              outline=(220, 220, 210), width=2)
    d.line([px, py, px - 22, py + 10], fill=(220, 220, 210), width=2)
    d.ellipse([px - 26, py + 6, px - 18, py + 14], fill=(200, 180, 90))
    for i in range(5):
        tx = x + 12 + i * 14
        ty = y + h - 18 - i * 3
        d.ellipse([tx, ty, tx + 3, ty + 3], fill=(240, 210, 90))


def art_cop(d, x, y, w, h):
    panel(d, x, y, w, h, (226, 232, 222))
    cx, cy, r = x + 34, y + h // 2 + 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 200),
              outline=(40, 90, 140), width=2)
    d.ellipse([cx - 12, cy - 14, cx + 2, cy - 2], fill=(90, 170, 110))
    d.ellipse([cx - 2, cy + 4, cx + 14, cy + 16], fill=(90, 170, 110))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 90, 140), width=1)
    d.line([cx - 34, y + 8, cx + 74, y + 8], fill=(200, 60, 50), width=2)
    tag(d, x + w - 58, y + h - 24, "21 LEFT", fill=RED)


def art_walmart(d, x, y, w, h):
    panel(d, x, y, w, h, (210, 226, 238))
    d.rectangle([x + 8, y + h - 34, x + w - 8, y + h - 14], fill=(70, 90, 130))
    d.rectangle([x + 8, y + h - 44, x + w - 8, y + h - 34], fill=(240, 240, 235))
    for wx in range(x + 14, x + w - 14, 18):
        d.line([wx, y + h - 44, wx, y + h - 34], fill=(180, 180, 170), width=1)
    cx, cy = x + w // 2 + 30, y + h - 44
    d.rectangle([cx, cy, cx + 34, cy + 12], fill=(200, 200, 190),
                outline=(80, 80, 80), width=1)
    d.line([cx + 34, cy + 4, cx + 44, cy + 4], fill=(80, 80, 80), width=2)
    d.line([cx + 44, cy + 4, cx + 40, cy + 14], fill=(80, 80, 80), width=2)
    d.ellipse([cx + 6, cy + 13, cx + 11, cy + 18], fill=(60, 60, 60))
    d.ellipse([cx + 24, cy + 13, cx + 29, cy + 18], fill=(60, 60, 60))


def art_tokyo(d, x, y, w, h):
    panel(d, x, y, w, h, (238, 230, 214))
    gx = x + 26
    d.rectangle([gx, y + 12, gx + 52, y + 20], fill=(178, 40, 40))
    d.rectangle([gx + 8, y + 20, gx + 14, y + h - 10], fill=(178, 40, 40))
    d.rectangle([gx + 38, y + 20, gx + 44, y + h - 10], fill=(178, 40, 40))
    d.rectangle([gx + 4, y + 34, gx + 48, y + 40], fill=(178, 40, 40))
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(200, 50, 50))
    d.rectangle([x + w - 52, y + 46, x + w - 22, y + 52], fill=(240, 240, 235))
    d.rectangle([x + w - 52, y + 52, x + w - 22, y + 58], fill=(60, 120, 60))
    d.rectangle([x + w - 52, y + 46, x + w - 42, y + 58], fill=(240, 150, 40))


def art_nvidia(d, x, y, w, h):
    panel(d, x, y, w, h, (228, 232, 220))
    cx, cy = x + 44, y + h // 2 + 6
    for k in range(-2, 3):
        d.line([cx - 22, cy + k * 9, cx - 30, cy + k * 9], fill=(40, 110, 60),
               width=2)
        d.line([cx + 22, cy + k * 9, cx + 30, cy + k * 9], fill=(40, 110, 60),
               width=2)
    d.rectangle([cx - 22, cy - 22, cx + 22, cy + 22], fill=(60, 160, 80),
                outline=(30, 100, 50), width=2)
    d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=(30, 110, 55))
    d.line([x + 84, y + h - 18, x + w - 14, y + 16], fill=(40, 130, 70),
           width=3)
    d.polygon([(x + w - 14, y + 16), (x + w - 28, y + 16),
               (x + w - 20, y + 28)], fill=(40, 130, 70))
    tag(d, x + w - 74, y + h - 24, "PAY RISES", fill=(30, 40, 70))


def art_liu(d, x, y, w, h):
    panel(d, x, y, w, h, (226, 230, 238))
    bx, by = x + w - 66, y + h - 40
    d.rectangle([bx, by, bx + 44, by + 28], fill=(40, 56, 96))
    d.rectangle([bx - 4, by - 6, bx + 48, by], fill=(30, 44, 80))
    d.rectangle([bx + 18, by - 4, bx + 26, by], fill=(24, 24, 24))
    d.polygon([(bx - 16, by - 34), (bx + 4, by - 38), (bx + 2, by - 16),
               (bx - 14, by - 12)], fill=(250, 250, 246),
              outline=(120, 120, 110))
    d.ellipse([x + 22, y + 10, x + 62, y + 50], fill=(250, 250, 246),
              outline=(120, 120, 110), width=1)
    d.text((x + 28, y + 20), "FIRST", font=font(SANS_B, 11), fill=INK)


ART = {
    "shenzhen": art_shenzhen, "fed": art_fed, "ipo": art_ipo,
    "gaza": art_gaza, "akvan": art_akvan, "odesa": art_odesa,
    "sudan": art_sudan, "voyager": art_voyager, "cop": art_cop,
    "walmart": art_walmart, "tokyo": art_tokyo, "nvidia": art_nvidia,
    "liu": art_liu,
}


# ---------------------------------------------------------- world map ---

# Coarse land mask, 64 columns x 30 rows, equirectangular-ish.
# '#' is land; columns run from 168W to 192E, rows from 78N to 52S.
WORLD = [
    "                  ###          ##########################        ",
    "    #########    ####        ##############################     ",
    "   ############   ##  ###   ################################    ",
    "   ############      #######################  #############     ",
    "    ###########     #########################  ###########      ",
    "     #########      #######################   ##########       ",
    "     #########       ######################    #########        ",
    "     #########       ####################      ########         ",
    "      ########       ###################       #######  ##      ",
    "      ########        ##################        ######  ##      ",
    "      ########        #################         #####  ###      ",
    "       ######         ################          ####  ####      ",
    "        #####         ###############           ###   ###       ",
    "         ####         ###############            ##   ###       ",
    "          ###         ###############            ##   ##        ",
    "          #####       ##############              #  ####       ",
    "          ######       ############                   #####     ",
    "          ######       ###########                    ######    ",
    "           #####       ##########                      #####    ",
    "           #####       #########                       ######   ",
    "           ####        ########                        ######   ",
    "           ####         ######  #                      #####    ",
    "           ###          #####                          ####     ",
    "           ###          ####                                    ",
    "            ##          ###                                     ",
    "            ##                                                  ",
    "            ##                                                  ",
    "                                                         ##      ",
    "                                                         #       ",
    "                                                                ",
]

# (story number, grid col, grid row) — approximate story locations.
PINS = [
    (1, 47, 13), (2, 14, 9), (3, 17, 8), (4, 34, 11), (5, 43, 14),
    (6, 33, 7), (7, 33, 15), (9, 15, 16), (10, 11, 10), (11, 51, 10),
    (12, 8, 9), (13, 15, 11),
]


def draw_map(d, x, y, w, h):
    """Dotted world map with numbered red pins for stories 1-13."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 228),
                outline=INK, width=1)
    cols, rows = 64, 30
    cw, ch = w / cols, h / rows
    dot = (110, 130, 118)
    for r, line in enumerate(WORLD):
        for c, mark in enumerate(line):
            if mark == "#":
                px = x + c * cw + cw / 2
                py = y + r * ch + ch / 2
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=dot)
    fnt = font(SANS_B, 8)
    for n, c, r in PINS:
        px = x + c * cw + cw / 2
        py = y + r * ch + ch / 2
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(n)
        tw = d.textlength(s, font=fnt)
        d.text((px - tw / 2, py - 4), s, font=fnt, fill=(255, 255, 255))


# -------------------------------------------------------------- layout ---

MX = 24                      # side margin
CW = W - 2 * MX              # 976 content width


def draw_feature(d, x, y, w, art_h, idx, head_size, head_lead,
                 deck_size, deck_lead):
    """One feature card: art panel on top, kicker, headline, deck."""
    tag_text, kicker, headline, deck, key = FEATURES[idx]
    ART[key](d, x, y, w, art_h)
    if tag_text:
        tag(d, x + 6, y + 6, tag_text)
    badge(d, x + 6, y + art_h - 28, idx + 1)
    ty = y + art_h + 8
    d.text((x, ty), kicker, font=font(SANS_B, 12), fill=RED)
    ty += 18
    hf = font(SERIF_B, head_size)
    lines = wrap(d, headline, hf, w)
    assert len(lines) <= 2, f"headline {idx + 1} wraps to {len(lines)}"
    ty = draw_lines(d, x, ty, lines, hf, INK, head_lead)
    ty += 2
    df = font(SANS, deck_size)
    lines = wrap(d, deck, df, w)
    assert len(lines) <= 2, f"deck {idx + 1} wraps to {len(lines)}"
    ty = draw_lines(d, x, ty, lines, df, INK, deck_lead)
    return ty


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top kicker row ------------------------------------------------
    d.text((MX, 12), TOP_LEFT, font=font(SANS_B, 13), fill=INK)
    rf = font(SANS_B, 13)
    d.text((W - MX - d.textlength(TOP_RIGHT, font=rf), 12), TOP_RIGHT,
           font=rf, fill=RED)

    # --- masthead -------------------------------------------------------
    mf = fit_font(d, MASTHEAD, SERIF_B, 66, CW)
    d.text((MX, 40), MASTHEAD, font=mf, fill=INK)
    d.line([MX, 102, W - MX, 102], fill=INK, width=2)

    # --- subtitle -------------------------------------------------------
    sf = font(SERIF_I, 15)
    sw = d.textlength(SUBTITLE, font=sf)
    d.text(((W - sw) / 2, 112), SUBTITLE, font=sf, fill=SOFT)

    # --- row 1: three big features --------------------------------------
    col_w = (CW - 2 * 11) // 3
    y = 129
    for i in range(3):
        x = MX + i * (col_w + 11)
        draw_feature(d, x, y, col_w, 111, i, 26, 30, 14, 17)

    # --- row 2: five features -------------------------------------------
    col5 = (CW - 4 * 10) // 5
    y = 371
    for j, i in enumerate(range(3, 8)):
        x = MX + j * (col5 + 10)
        draw_feature(d, x, y, col5, 62, i, 20, 23, 12, 15)

    # --- row 3: five features -------------------------------------------
    y = 539
    for j, i in enumerate(range(8, 13)):
        x = MX + j * (col5 + 10)
        draw_feature(d, x, y, col5, 56, i, 20, 23, 12, 15)

    # --- numbers strip --------------------------------------------------
    d.line([MX, 700, W - MX, 700], fill=RULE, width=1)
    d.text((MX, 706), "BY THE NUMBERS", font=font(SANS_B, 12), fill=RED)
    n_w = CW // 4
    vf = font(SERIF_B, 30)
    cf = font(SANS, 11)
    for k, (value, caption) in enumerate(NUMBERS):
        x = MX + k * n_w
        d.text((x, 722), value, font=vf, fill=INK)
        d.text((x, 754), caption, font=cf, fill=SOFT)
    d.line([MX, 768, W - MX, 768], fill=RULE, width=1)

    # --- bottom: map + briefs -------------------------------------------
    hf = font(SANS_B, 12)
    d.text((MX, 772), "WHERE IT HAPPENED", font=hf, fill=RED)
    d.text((330, 772), "ALSO ON THURSDAY 19 NOVEMBER", font=hf, fill=RED)
    draw_map(d, MX, 788, 294, 138)
    cy = 932
    for line in MAP_CAPTION:
        d.text((MX, cy), line, font=font(SANS, 10), fill=INK)
        cy += 12

    bf = font(SERIF, 11)
    nf = font(SERIF_B, 11)
    lead = 12.2
    for col in range(2):
        x = 330 + col * 335
        for r in range(16):
            n = 14 + col * 16 + r
            yy = 788 + r * lead
            d.text((x, yy), f"{n:>2}", font=nf, fill=RED)
            d.text((x + 24, yy), BRIEFS[n - 14], font=bf, fill=INK)

    # --- footer ---------------------------------------------------------
    d.line([MX, 986, W - MX, 986], fill=RULE, width=1)
    ff = font(SANS, 10)
    lines = wrap(d, FOOTER, ff, CW)
    assert len(lines) <= 2, f"footer wraps to {len(lines)}"
    end_y = draw_lines(d, MX, 992, lines, ff, SOFT, 12)
    assert end_y <= 1020, f"page overflows: final y {end_y}"

    img.save(OUT, "JPEG", quality=88)
    total = len(FEATURES) + len(BRIEFS)
    print(f"wrote {OUT}  {W}x{H}  {os.path.getsize(OUT)} bytes  "
          f"{len(FEATURES)} features + {len(BRIEFS)} briefs = {total} stories")


if __name__ == "__main__":
    main()
