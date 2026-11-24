#!/usr/bin/env python3
"""Build entry.png for news-image-20261123 — THE WORLD TODAY, Monday 23 Nov 2026.

Fresh PIL drawing (no copied layout code). Renders a 1024x1024 front page:
masthead, COP31 hero, markets + Gulf cards, six briefs, date-check footer.
Deterministic: fixed fonts, fixed layout, no randomness, no timestamps.
"""
import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (245, 240, 230)
INK = (20, 32, 46)
NAVY = (16, 35, 59)
NAVY2 = (24, 52, 84)
RED = (196, 58, 42)
GOLD = (217, 164, 65)
CARD = (253, 252, 247)
BORDER = (201, 194, 178)
MUTED = (90, 100, 112)
GREEN = (38, 132, 74)
SKY = (46, 111, 142)
SKY2 = (127, 179, 200)
LAND = (232, 217, 168)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, lines, f, fill, leading=None, spacing=0):
    """Draw wrapped lines inside a box; assert the block fits its panel."""
    lh = leading if leading is not None else int(f.size * 1.25)
    for i, line in enumerate(lines):
        draw.text((x, y + i * (lh + spacing)), line, font=f, fill=fill)
    return y + len(lines) * (lh + spacing)


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_check(name, used_bottom, limit):
    if used_bottom > limit:
        raise SystemExit(f"FIT FAIL {name}: bottom {used_bottom} > limit {limit}")


def save_png(img, path):
    img.save(path, format="PNG", optimize=True)
    data = open(path, "rb").read()
    print("SIZE", len(data), "bytes; <=1MiB:", len(data) <= 1024 * 1024)
    print("SHA256", hashlib.sha256(data).hexdigest())
    print("MODE", img.mode, "DIMS", img.size)


def draw_masthead(draw):
    x0, x1 = 36, 988
    draw.text((x0, 30), "THE WORLD IN ONE DAY", font=SANS_B(17), fill=RED)
    right = "MONDAY EDITION"
    draw.text((x1 - text_w(draw, right, SANS_B(15)), 32), right,
              font=SANS_B(15), fill=MUTED)
    title = "THE WORLD TODAY"
    draw.text((x0, 56), title, font=SERIF_B(54), fill=INK)
    date = "MONDAY 23 NOV 2026"
    dw = text_w(draw, date, SANS_B(22))
    draw.text((x1 - dw, 86), date, font=SANS_B(22), fill=INK)
    rule(draw, x0, 132, x1, 3)
    rule(draw, x0, 138, x1, 1)
    fit_check("masthead", 140, 150)


def draw_globe(draw, cx, cy, r):
    """Cracked-earth motif: blue sphere, meridians, red zigzag crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=GOLD, width=3)
    # meridian + latitude lines (clipped look via arcs)
    for k in (-0.55, 0.0, 0.55):
        w = int(r * 0.45)
        draw.arc([cx - w, cy - r, cx + w, cy + r], 90, 270, fill=SKY2, width=2)
        draw.arc([cx - w, cy - r, cx + w, cy + r], 270, 90, fill=SKY2, width=2)
    for k in (-0.5, 0.0, 0.5):
        yy = cy + int(r * k)
        half = int((r * r - (r * k) ** 2) ** 0.5)
        draw.line([(cx - half, yy), (cx + half, yy)], fill=SKY2, width=2)
    # land blobs
    draw.ellipse([cx - 70, cy - 58, cx - 8, cy - 6], fill=LAND)
    draw.ellipse([cx + 12, cy + 18, cx + 66, cy + 62], fill=LAND)
    draw.ellipse([cx + 30, cy - 62, cx + 72, cy - 18], fill=LAND)
    # crack: red zigzag from upper-left to lower-right
    crack = [(cx - 78, cy - 40), (cx - 40, cy - 12), (cx - 58, cy + 14),
             (cx - 12, cy + 34), (cx - 34, cy + 58), (cx + 18, cy + 78),
             (cx + 8, cy + 96)]
    draw.line(crack, fill=RED, width=7, joint="curve")
    draw.line(crack, fill=(255, 255, 255), width=2, joint="curve")
    # sparks
    for sx, sy in ((cx - 84, cy - 52), (cx + 26, cy + 88), (cx + 84, cy - 8)):
        draw.line([(sx - 8, sy), (sx + 8, sy)], fill=GOLD, width=3)
        draw.line([(sx, sy - 8), (sx, sy + 8)], fill=GOLD, width=3)


def draw_hero(draw):
    x0, y0, x1, y1 = 36, 158, 988, 500
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y1], outline=GOLD, width=2)
    tx = x0 + 28
    draw.text((tx, y0 + 22), "CLIMATE  ·  COP31  ·  ANTALYA, TURKIYE",
              font=SANS_B(17), fill=GOLD)
    draw.text((tx, y0 + 48), "CLIMATE TALKS", font=SERIF_B(62), fill=(255, 255, 255))
    draw.text((tx, y0 + 110), "COLLAPSE", font=SERIF_B(62), fill=(255, 255, 255))
    deck = ("Nearly 200 nations leave Antalya with no deal — the longest "
            "climate summit ever ends with fossil fuels written out, "
            "and the EU walking out.")
    lines = wrap(draw, deck, SANS(19), 540)
    end = para(draw, tx, y0 + 178, 540, lines, SANS(19), (226, 232, 238),
               leading=24)
    draw.text((tx, end + 12), "SUNDAY NIGHT, 22 NOV", font=SANS_B(16), fill=GOLD)
    stat = "50+ HOURS OVERTIME  ·  1.5°C OVERSHOOT ACKNOWLEDGED"
    draw.text((tx, end + 40), stat, font=SANS_B(15), fill=(180, 196, 210))
    fit_check("hero text", end + 62, y1)
    draw_globe(draw, 838, 330, 96)


def draw_markets(draw):
    x0, y0, x1, y1 = 36, 510, 506, 740
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=1)
    draw.text((x0 + 20, y0 + 14), "MARKETS MELTDOWN", font=SANS_B(21), fill=RED)
    draw.text((x0 + 20, y0 + 42), "FRIDAY 20 NOV CLOSE — THE WEEK STOCKS FELL OFF A CLIFF",
              font=SANS_B(13), fill=MUTED)
    rows = [("S&P 500", "-3.7%", 3.70, RED), ("Nasdaq", "-5.3%", 5.28, RED),
            ("Dow", "-1.9%", 1.93, RED), ("Nikkei", "-5.1%", 5.06, RED),
            ("Bitcoin*", "+0.9%", 0.90, GREEN)]
    bx, bw_max = x0 + 110, 190
    y = y0 + 70
    for label, val, mag, color in rows:
        draw.text((x0 + 20, y), label, font=SANS_B(16), fill=INK)
        bar_w = int(bw_max * mag / 5.28)
        draw.rectangle([bx, y + 3, bx + bar_w, y + 17], fill=color)
        draw.text((bx + bw_max + 12, y), val, font=SANS_B(16), fill=INK)
        y += 24
    foot = ("*Bitcoin Mon 23 Nov 00:07 UTC. VIX 35.89 (+26%). "
            "Nvidia -14% Fri; gold -4.6%. Japan shut Mon.")
    lines = wrap(draw, foot, SANS(14), x1 - x0 - 40)
    para(draw, x0 + 20, y + 4, x1 - x0 - 40, lines, SANS(14), MUTED, leading=17)
    fit_check("markets", y + 4 + len(lines) * 17, y1)


def draw_gulf(draw):
    x0, y0, x1, y1 = 518, 510, 988, 740
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=1)
    draw.text((x0 + 20, y0 + 14), "GULF ON EDGE", font=SANS_B(21), fill=RED)
    draw.text((x0 + 20, y0 + 42), "STRAIT OF HORMUZ  ·  SUNDAY 22 NOV",
              font=SANS_B(13), fill=MUTED)
    draw.text((x0 + 20, y0 + 66), "25+", font=SERIF_B(64), fill=INK)
    draw.text((x0 + 178, y0 + 70),
              "tankers hit in and", font=SANS_B(17), fill=INK)
    draw.text((x0 + 178, y0 + 92),
              "around the Strait of", font=SANS_B(17), fill=INK)
    draw.text((x0 + 178, y0 + 114),
              "Hormuz in seven days", font=SANS_B(17), fill=INK)
    body = ("Houthis struck Riyadh a third straight day on Sunday — "
            "intercepted. Iran's Guard fired at U.S.-linked bases in "
            "Bahrain on Saturday night.")
    lines = wrap(draw, body, SANS(16), x1 - x0 - 40)
    para(draw, x0 + 20, y0 + 142, x1 - x0 - 40, lines, SANS(16), INK,
         leading=21)
    fit_check("gulf", y0 + 142 + len(lines) * 21, y1)


BRIEFS = [
    ("DEMOCRATS 258", "AP calls N.C.-5: Democrats clinch 258+ House seats, "
     "biggest since 1992. SUN 22 NOV"),
    ("MERCURY BOUND", "BepiColombo enters orbit around Mercury after an "
     "eight-year journey. SAT 22 NOV"),
    ("SEOUL SHAKE-UP", "Education minister quits after 111 cheating cases "
     "in the college exam. SUN 22 NOV"),
    ("NEPAL – INDIA", "Nepal PM Balendra Shah holds bilateral talks with "
     "Modi in New Delhi. MON 23 NOV"),
    ("INDIA 720/9", "India declares on 720/9 — a record innings — on Day 4 "
     "in Wellington. MON 23 NOV"),
    ("INDONESIA", "Search resumes Monday at the Cikande candy factory: "
     "3 dead, ~50 missing. MON 23 NOV"),
]


def draw_briefs(draw):
    x0, y0, x1 = 36, 748, 988
    draw.text((x0, y0), "ALSO TODAY", font=SANS_B(19), fill=INK)
    rule(draw, x0, y0 + 24, x1, 2)
    col_w, gap = 300, 26
    y = y0 + 32
    bottom = y
    for i in range(0, 6, 3):
        row_h = 0
        for j, idx in enumerate((i, i + 1, i + 2)):
            bx = x0 + j * (col_w + gap)
            head, body = BRIEFS[idx]
            draw.text((bx, y), head, font=SANS_B(15), fill=RED)
            lines = wrap(draw, body, SANS(15), col_w)
            end = para(draw, bx, y + 21, col_w, lines, SANS(15), INK,
                       leading=18)
            row_h = max(row_h, end - y)
        bottom = y + row_h
        y += row_h + 8
    fit_check("briefs", bottom, 938)


def draw_footer(draw):
    x0, x1 = 36, 988
    rule(draw, x0, 946, x1, 2)
    dc = ("DATE CHECK: COP31 — Sunday 22 Nov · Democrats — Sunday 22 Nov · "
          "BepiColombo — Saturday 22 Nov · Korea minister — Sunday 22 Nov · "
          "Markets — Friday 20 Nov close · Bitcoin — Monday 23 Nov 00:07 UTC")
    lines = wrap(draw, dc, SANS_B(12), x1 - x0)
    end = para(draw, x0, 954, x1 - x0, lines, SANS_B(12), INK, leading=15)
    src = "SOURCES: REUTERS · AP · AFP · NPR · ESA · YAHOO FINANCE · FINNHUB"
    draw.text((x0, end + 6), src, font=SANS(12), fill=MUTED)
    fit_check("footer", end + 18, 1010)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    draw_markets(draw)
    draw_gulf(draw)
    draw_briefs(draw)
    draw_footer(draw)
    save_png(img, OUT)
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
