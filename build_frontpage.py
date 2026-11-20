#!/usr/bin/env python3
"""Build the front-page image for news-image-20261120.

Draws 'THE TWENTIETH' — a one-page world front page for Friday
20 November 2026, from the eight stories verified against live
reporting this morning (IMD Bulletin 35 at 02:15 IST, the overnight
wires, and the Wellington Test).

Everything on the page happened, or was first reported, on
20 November 2026. Stories that belong to 19 November (the Shenzhen
trilateral, the ICJ ruling, the Kyiv embassy strikes, the Han
retrial, the Fiji disaster declaration) are deliberately NOT
repeated here — this page is the 20th alone.

Run:  python3 build_frontpage.py  ->  writes entry.png (1024x1024)
Only Pillow + DejaVu fonts are needed. Output is deterministic.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (253, 252, 247)
INK = (20, 20, 20)
RED = (185, 28, 28)
GRAY = (110, 110, 110)
GREEN = (46, 189, 133)
BOX = (20, 20, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # no italic file; regular serif
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width. Returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, width, leading):
    """Draw wrapped paragraph. Returns y after last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, fill=INK, w=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
CW = W - 2 * MARGIN  # content width 952

# ---------- top bar ----------
f_top = font(SANS_B, 13)
d.text((MARGIN, 26), "FRIDAY 20 NOVEMBER 2026  ·  WORLD EDITION",
       font=f_top, fill=INK)
right = "EIGHT STORIES, RANKED BY CONSEQUENCE"
d.text((W - MARGIN - d.textlength(right, font=f_top), 26), right,
       font=f_top, fill=INK)
rule(d, MARGIN, W - MARGIN, 50)

# ---------- masthead ----------
f_mast = font(SERIF_B, 66)
mast = "THE TWENTIETH"
tw = d.textlength(mast, font=f_mast)
mx = (W - tw) / 2
# "THE " in ink, "TWENTIETH" in red
w_the = d.textlength("THE ", font=f_mast)
d.text((mx, 62), "THE ", font=f_mast, fill=INK)
d.text((mx + w_the, 62), "TWENTIETH", font=f_mast, fill=RED)
f_side = font(SANS_B, 12)
d.text((MARGIN, 96), "ONE PAGE.", font=f_side, fill=INK)
d.text((MARGIN, 112), "ONE DAY.", font=f_side, fill=INK)
r1 = "EVERY FIGURE"
r2 = "AS REPORTED."
d.text((W - MARGIN - d.textlength(r1, font=f_side), 96), r1,
       font=f_side, fill=INK)
d.text((W - MARGIN - d.textlength(r2, font=f_side), 112), r2,
       font=f_side, fill=INK)
rule(d, MARGIN, W - MARGIN, 148)
rule(d, MARGIN, W - MARGIN, 152)

# ---------- lead row ----------
ly = 168
# left: lead story — Cyclone Akvan landfall
lx, lw = MARGIN, 620
f_kick = font(SANS_B, 14)
d.text((lx, ly), "ODISHA, INDIA  ·  BAY OF BENGAL  ·  LANDFALL DAY",
       font=f_kick, fill=RED)
f_head = font(SERIF_B, 40)
y = para(d, lx, ly + 26, "Akvan comes ashore at noon.",
         f_head, INK, lw, 48)
f_body = font(SANS, 16)
y = para(d, lx, y + 8,
         "The cyclone crosses the coast close to Gopalpur around noon, "
         "weaker than feared: the India Meteorological Department's "
         "02:15 bulletin has it down to a cyclonic storm, with winds of "
         "70–80 km/h gusting to 90. A 0.5–1.0 m surge is warned for six "
         "districts, and heavy rain is forecast across Odisha today.",
         f_body, INK, lw, 23)
# stats
sy = y + 14
f_num = font(SERIF_B, 34)
f_lab = font(SANS_B, 12)
d.text((lx, sy), "12:00", font=f_num, fill=INK)
d.text((lx + d.textlength("12:00", font=f_num) + 12, sy + 20), "LANDFALL, IST", font=f_lab, fill=GRAY)
d.text((lx + 300, sy), "105,000", font=f_num, fill=INK)
d.text((lx + 300 + d.textlength("105,000", font=f_num) + 12, sy + 20), "MOVED TO SHELTERS", font=f_lab, fill=GRAY)
# context line
qy = sy + 58
f_q = font(SERIF_I, 17)
qy = para(d, lx, qy,
          "Red alert in six districts; schools shut for three days.",
          f_q, INK, lw, 24)
d.text((lx, qy + 2), "— IMD NATIONAL BULLETIN 35, 02:15 IST",
       font=font(SANS_B, 11), fill=GRAY)

# right: diplomacy box (black)
bx, bw = 676, W - MARGIN - 676
by, bh = ly, 332
d.rectangle([bx, by, bx + bw, by + bh], fill=BOX)
pad = 18
ix = bx + pad
iy = by + 14
d.text((ix, iy), "WASHINGTON  ·  MOSCOW", font=font(SANS_B, 12),
       fill=(150, 150, 150))
hy = iy + 34
hy = para(d, ix, hy,
          "A peace statement that says nothing about Ukraine",
          font(SERIF_B, 20), (255, 255, 255), bw - 2 * pad, 26)
hy = para(d, ix, hy + 10,
          "Trump and Putin approve a joint statement with no mention of "
          "Ukraine. The Senate minority leader attacks Trump for calling "
          "Putin a \u201cfriend\u201d. Japan's Takaichi holds first talks "
          "with Putin on the APEC sidelines; Merz sets terms for peace "
          "talks after a Berlin summit.",
          font(SANS, 13), (230, 230, 230), bw - 2 * pad, 18)

rule(d, MARGIN, W - MARGIN, 508)

# ---------- row 2: three columns ----------
def story_col(x, w, y, kicker, big, bigfill, head, body, head_size=19):
    d.text((x, y), kicker, font=font(SANS_B, 11), fill=RED)
    yy = y + 20
    if big:
        d.text((x, yy), big, font=font(SERIF_B, 32), fill=bigfill)
        yy += 42
    yy = para(d, x, yy, head, font(SERIF_B, head_size), INK, w, 24)
    yy = para(d, x, yy + 6, body, font(SANS, 12), INK, w, 17)
    return yy

col_w = 300
gap = 26
x1, x2, x3 = MARGIN, MARGIN + col_w + gap, MARGIN + 2 * (col_w + gap)
ry = 524
story_col(x1, col_w, ry,
          "SHENZHEN, CHINA  ·  APEC SUMMIT",
          "OPEN TRADE", INK,
          "Xi presses open trade as APEC leaders meet",
          "Leaders in Shenzhen discuss trade, investment and technology; "
          "Xi urges Asia-Pacific economies to back open trade and work "
          "together on emerging tech. India presses climate finance at "
          "COP31 in T\u00fcrkiye.")
story_col(x2, col_w, ry,
          "SPORT  ·  WELLINGTON",
          "113*", INK,
          "Nicholls century steadies New Zealand",
          "Henry Nicholls finishes day one of the first Test against "
          "India unbeaten on 113 at the Basin Reserve; New Zealand close "
          "on 243 for five. Two-match series, World Test Championship "
          "points at stake.")
story_col(x3, col_w, ry,
          "EUROPE  ·  LAW",
          "\u20ac213.7m", INK,
          "Brussels charges Spaniard over rail fraud",
          "EU prosecutors charge a Spanish national over \u20ac213.7m of "
          "Bulgaria railway funding fraud. Three are detained in Poland "
          "in a vast VAT-evasion inquiry.")

rule(d, MARGIN, W - MARGIN, 762)

# ---------- also today ----------
d.text((MARGIN, 776), "ALSO TODAY", font=font(SANS_B, 14), fill=INK)
rule(d, MARGIN + 110, W - MARGIN, 785)

def mini_col(x, w, y, big, head, body):
    d.text((x, y), big, font=font(SERIF_B, 24), fill=RED)
    yy = para(d, x, y + 34, head, font(SERIF_B, 17), INK, w, 21)
    para(d, x, yy + 4, body, font(SANS, 12), INK, w, 17)

ay = 800
mini_col(x1, col_w, ay, "200+", "Justice Dept subpoenas pile up",
         "The US Justice Department issues more than 200 subpoena "
         "requests in an Alaska election inquiry.")
mini_col(x2, col_w, ay, "6 nations", "Gulf Railway to link six states",
         "The project aims to join six Gulf nations by rail and cut "
         "reliance on the Strait of Hormuz.")
mini_col(x3, col_w, ay, "AI IN CLASS", "EU urges AI skills for all",
         "The EU encourages member states to equip teachers, students "
         "and workers with AI skills.")

# ---------- footer ----------
rule(d, MARGIN, W - MARGIN, 962)
f_foot = font(SANS, 11)
d.text((MARGIN, 972),
       "SOURCES: IMD, REUTERS, AP, AFP, EURONEWS, TIMES OF INDIA.  "
       "COMPILED 20 NOV 2026.",
       font=f_foot, fill=GRAY)
d.text((MARGIN, 988),
       "LANDFALL, SCORE AND CHARGE FIGURES ARE AS OF THE DAY'S REPORTING.",
       font=f_foot, fill=GRAY)

img.save("entry.png", "PNG")
print("saved entry.png", img.size)
