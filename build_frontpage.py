#!/usr/bin/env python3
"""Draw 'THE TWENTIETH', the world front page for Friday 20 Nov 2026.

A one-page broadsheet: eight stories, ranked by consequence, drawn
with Pillow onto a 1024x1024 sheet. Every story on the page happened,
or was first reported, on 20 November 2026 — nothing is repeated
from the 19th (no trilateral, no ICJ ruling, no Kyiv embassy
strikes, no Han retrial, no Fiji declaration).

Stories, verified this morning against live reporting:
  * lead: Cyclone Akvan's landfall near Gopalpur, ~noon IST
    (IMD National Bulletin 35, 02:15 IST 20 Nov 2026)
  * black box: Trump–Putin joint statement with no mention of
    Ukraine; Senate rebuke; Takaichi–Putin talks; Merz terms
  * APEC in Shenzhen: Xi presses open trade; COP31 in Turkiye
  * Wellington: Nicholls 113* , New Zealand 243/5 at stumps, day 1
  * EPPO charges a Spaniard over EUR 213.7m of rail fraud
  * also today: 200+ DOJ subpoenas (Alaska); Gulf Railway;
    EU AI-skills push

Run:  python3 build_frontpage.py  ->  writes entry.png (1024x1024)
Only Pillow + DejaVu fonts are needed. Output is deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

SHEET_W, SHEET_H = 1024, 1024
EDGE = 36
PAPER = (253, 252, 247)
INK = (20, 20, 20)
RED = (185, 28, 28)
GREY = (110, 110, 110)
GREEN = (46, 189, 133)
BLACKBOX = (20, 20, 20)

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class Sheet:
    """A drawable broadsheet page with word-wrap and rules."""

    def __init__(self):
        self.image = Image.new("RGB", (SHEET_W, SHEET_H), PAPER)
        self.pen = ImageDraw.Draw(self.image)
        self.content_w = SHEET_W - 2 * EDGE

    @staticmethod
    def typeface(path, size):
        return ImageFont.truetype(path, size)

    def fit_lines(self, text, face, width):
        """Split text into lines that fit width, word by word."""
        lines, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.pen.textlength(trial, font=face) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def block(self, x, y, text, face, fill, width, leading):
        """Draw a wrapped paragraph; return the y below its last line."""
        for line in self.fit_lines(text, face, width):
            self.pen.text((x, y), line, font=face, fill=fill)
            y += leading
        return y

    def hline(self, x0, x1, y, fill=INK, weight=1):
        self.pen.line([(x0, y), (x1, y)], fill=fill, width=weight)

    def text(self, x, y, s, face, fill):
        self.pen.text((x, y), s, font=face, fill=fill)

    def save(self, path="entry.png"):
        self.image.save(path, "PNG")
        print("saved", path, self.image.size)


page = Sheet()
d = page.pen

# ---------- top bar ----------
top_face = page.typeface(FONT_SANS_BOLD, 13)
page.text(EDGE, 26, "FRIDAY 20 NOVEMBER 2026  ·  WORLD EDITION",
          top_face, INK)
tag = "EIGHT STORIES, RANKED BY CONSEQUENCE"
page.text(SHEET_W - EDGE - d.textlength(tag, font=top_face), 26, tag,
          top_face, INK)
page.hline(EDGE, SHEET_W - EDGE, 50)

# ---------- masthead ----------
mast_face = page.typeface(FONT_SERIF_BOLD, 66)
mast = "THE TWENTIETH"
mx = (SHEET_W - d.textlength(mast, font=mast_face)) / 2
w_the = d.textlength("THE ", font=mast_face)
page.text(mx, 62, "THE ", mast_face, INK)
page.text(mx + w_the, 62, "TWENTIETH", mast_face, RED)
side_face = page.typeface(FONT_SANS_BOLD, 12)
page.text(EDGE, 96, "ONE PAGE.", side_face, INK)
page.text(EDGE, 112, "ONE DAY.", side_face, INK)
for line, yy in (("EVERY FIGURE", 96), ("AS REPORTED.", 112)):
    page.text(SHEET_W - EDGE - d.textlength(line, font=side_face), yy,
              line, side_face, INK)
page.hline(EDGE, SHEET_W - EDGE, 148)
page.hline(EDGE, SHEET_W - EDGE, 152)

# ---------- lead row: Cyclone Akvan comes ashore ----------
ly = 168
lx, lw = EDGE, 620
page.text(lx, ly, "ODISHA, INDIA  ·  BAY OF BENGAL  ·  LANDFALL DAY",
          page.typeface(FONT_SANS_BOLD, 14), RED)
y = page.block(lx, ly + 26, "Akvan comes ashore at noon.",
               page.typeface(FONT_SERIF_BOLD, 40), INK, lw, 48)
y = page.block(
    lx, y + 8,
    "The cyclone crosses the coast close to Gopalpur around noon, "
    "weaker than feared: the India Meteorological Department's "
    "02:15 bulletin has it down to a cyclonic storm, with winds of "
    "70–80 km/h gusting to 90. A 0.5–1.0 m surge is warned for six "
    "districts, and heavy rain is forecast across Odisha today.",
    page.typeface(FONT_SANS, 16), INK, lw, 23)
sy = y + 14
num_face = page.typeface(FONT_SERIF_BOLD, 34)
lab_face = page.typeface(FONT_SANS_BOLD, 12)
page.text(lx, sy, "12:00", num_face, INK)
page.text(lx + d.textlength("12:00", font=num_face) + 12, sy + 20,
          "LANDFALL, IST", lab_face, GREY)
page.text(lx + 300, sy, "105,000", num_face, INK)
page.text(lx + 300 + d.textlength("105,000", font=num_face) + 12,
          sy + 20, "MOVED TO SHELTERS", lab_face, GREY)
qy = page.block(lx, sy + 58,
                "Red alert in six districts; schools shut for three days.",
                page.typeface(FONT_SERIF, 17), INK, lw, 24)
page.text(lx, qy + 2, "— IMD NATIONAL BULLETIN 35, 02:15 IST",
          page.typeface(FONT_SANS_BOLD, 11), GREY)

# ---------- black box: the Trump–Putin statement ----------
bx, bw = 676, SHEET_W - EDGE - 676
by, bh = ly, 332
d.rectangle([bx, by, bx + bw, by + bh], fill=BLACKBOX)
pad = 18
ix = bx + pad
iy = by + 14
page.text(ix, iy, "WASHINGTON  ·  MOSCOW",
          page.typeface(FONT_SANS_BOLD, 12), (150, 150, 150))
hy = page.block(ix, iy + 34,
                "A peace statement that says nothing about Ukraine",
                page.typeface(FONT_SERIF_BOLD, 20), (255, 255, 255),
                bw - 2 * pad, 26)
page.block(ix, hy + 10,
           "Trump and Putin approve a joint statement with no mention of "
           "Ukraine. The Senate minority leader attacks Trump for calling "
           "Putin a \u201cfriend\u201d. Japan's Takaichi holds first talks "
           "with Putin on the APEC sidelines; Merz sets terms for peace "
           "talks after a Berlin summit.",
           page.typeface(FONT_SANS, 13), (230, 230, 230),
           bw - 2 * pad, 18)

page.hline(EDGE, SHEET_W - EDGE, 508)

# ---------- middle row: three stories ----------
def column(x, w, y, kicker, figure, head, body, head_size=19):
    page.text(x, y, kicker, page.typeface(FONT_SANS_BOLD, 11), RED)
    yy = y + 20
    if figure:
        page.text(x, yy, figure, page.typeface(FONT_SERIF_BOLD, 32), INK)
        yy += 42
    yy = page.block(x, yy, head, page.typeface(FONT_SERIF_BOLD, head_size),
                    INK, w, 24)
    page.block(x, yy + 6, body, page.typeface(FONT_SANS, 12), INK, w, 17)

col_w = 300
gap = 26
x1 = EDGE
x2 = EDGE + col_w + gap
x3 = EDGE + 2 * (col_w + gap)
ry = 524
column(x1, col_w, ry,
       "SHENZHEN, CHINA  ·  APEC SUMMIT",
       "OPEN TRADE",
       "Xi presses open trade as APEC leaders meet",
       "Leaders in Shenzhen discuss trade, investment and technology; "
       "Xi urges Asia-Pacific economies to back open trade and work "
       "together on emerging tech. India presses climate finance at "
       "COP31 in T\u00fcrkiye.")
column(x2, col_w, ry,
       "SPORT  ·  WELLINGTON",
       "113*",
       "Nicholls century steadies New Zealand",
       "Henry Nicholls finishes day one of the first Test against "
       "India unbeaten on 113 at the Basin Reserve; New Zealand close "
       "on 243 for five. Two-match series, World Test Championship "
       "points at stake.")
column(x3, col_w, ry,
       "EUROPE  ·  LAW",
       "\u20ac213.7m",
       "Brussels charges Spaniard over rail fraud",
       "EU prosecutors charge a Spanish national over \u20ac213.7m of "
       "Bulgaria railway funding fraud. Three are detained in Poland "
       "in a vast VAT-evasion inquiry.")

page.hline(EDGE, SHEET_W - EDGE, 762)

# ---------- also today: three briefs ----------
page.text(EDGE, 776, "ALSO TODAY", page.typeface(FONT_SANS_BOLD, 14), INK)
page.hline(EDGE + 110, SHEET_W - EDGE, 785)

def brief(x, w, y, figure, head, body):
    page.text(x, y, figure, page.typeface(FONT_SERIF_BOLD, 24), RED)
    yy = page.block(x, y + 34, head, page.typeface(FONT_SERIF_BOLD, 17),
                    INK, w, 21)
    page.block(x, yy + 4, body, page.typeface(FONT_SANS, 12), INK, w, 17)

ay = 800
brief(x1, col_w, ay, "200+", "Justice Dept subpoenas pile up",
      "The US Justice Department issues more than 200 subpoena "
      "requests in an Alaska election inquiry.")
brief(x2, col_w, ay, "6 nations", "Gulf Railway to link six states",
      "The project aims to join six Gulf nations by rail and cut "
      "reliance on the Strait of Hormuz.")
brief(x3, col_w, ay, "AI IN CLASS", "EU urges AI skills for all",
      "The EU encourages member states to equip teachers, students "
      "and workers with AI skills.")

# ---------- footer ----------
page.hline(EDGE, SHEET_W - EDGE, 962)
foot_face = page.typeface(FONT_SANS, 11)
page.text(EDGE, 972,
          "SOURCES: IMD, REUTERS, AP, AFP, EURONEWS, TIMES OF INDIA.  "
          "COMPILED 20 NOV 2026.",
          foot_face, GREY)
page.text(EDGE, 988,
          "LANDFALL, SCORE AND CHARGE FIGURES ARE AS OF THE DAY'S REPORTING.",
          foot_face, GREY)

page.save("entry.png")
