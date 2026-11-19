#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261119 bounty.

A one-page newspaper front page summing up Thursday 19 November 2026.
Stories were checked against wire reports of that day (1440, BitDigest/WSJ,
Reuters, Semblen, Daily Mirror, all dated 19 Nov 2026):

  1. Trump meets Xi and Putin in Shenzhen for the historic trilateral.
  2. Grand Theft Auto VI launches worldwide after 13 years.
  3. Anthropic debuts on Nasdaq as ANT; IPO prices at $83, $1.5T value.
  4. Israel launches a ground operation in Hamas-controlled Gaza.
  5. Ukraine's allies rally in Berlin with Trump's envoys Witkoff, Kushner.
  6. Voyager 1 reaches one light-day from Earth, a first for any craft.
  Also: dozens missing after a migrant boat sinks off Senegal; Saudi-led
  coalition says it hit 60 Houthi targets in Yemen.

Run:  python3 tools/generate-entry.py   (writes entry.png next to main.ts)
Uses only Pillow + DejaVu fonts already on this machine. The entry program
itself (main.ts) only copies the finished PNG; it imports nothing.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 239)   # warm ivory
INK = (22, 35, 63)        # deep navy
BODY = (51, 65, 92)       # slate navy
MUTED = (110, 118, 135)   # grey blue
RED = (11, 94, 89)       # deep teal accent for 19 November
CARD = (255, 255, 255)
LINE = (203, 210, 220)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REG = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with manual letter tracking."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def draw_globe(draw, cx, cy, r, color, width=4):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=color, width=3)


def panel(draw, x, y, w, h, num, color, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=LINE, width=1)
    draw.rectangle([x, y, x + w, y + 7], fill=color)
    # number badge
    bx, by, br = x + 20, y + 26, 19
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
    num_f = font(BOLD, 20)
    tw = draw.textlength(num, font=num_f)
    draw.text((bx - tw / 2, by - 13), num, font=num_f, fill=(255, 255, 255))
    # headline + body
    tx = x + 52
    twidth = x + w - 18 - tx
    hf = font(BOLD, 26)
    lines = wrap(draw, headline, hf, twidth)
    ly = y + 20
    for ln in lines[:2]:
        draw.text((tx, ly), ln, font=hf, fill=INK)
        ly += 31
    bf = font(REG, 20)
    blines = wrap(draw, body, bf, twidth)
    ly += 4
    for ln in blines[:2]:
        draw.text((tx, ly), ln, font=bf, fill=BODY)
        ly += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---- masthead ----
    d.rectangle([mx, 26, W - mx, 32], fill=RED)
    spaced(d, (mx, 46), "THE WORLD TODAY", font(BOLD, 24), INK, tracking=4)
    wk = font(BOLD, 24)
    d.text((W - mx - d.textlength("THURSDAY", font=wk), 46),
           "THURSDAY", font=wk, fill=INK)
    d.text((mx, 82), "19 NOVEMBER 2026", font=font(BOLD, 66), fill=INK)
    d.text((mx, 152), "Six stories that defined the day, from Shenzhen to deep space.",
           font=font(REG, 23), fill=MUTED)
    d.rectangle([mx, 186, W - mx, 188], fill=INK)

    # ---- lead story ----
    lx, ly, lw, lh = mx, 204, W - 2 * mx, 196
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD, outline=LINE, width=1)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    tx = lx + 30
    d.text((tx, ly + 18), "SHENZHEN  •  THE TRILATERAL", font=font(BOLD, 21), fill=RED)
    d.text((tx, ly + 48), "TRUMP, XI AND PUTIN MEET", font=font(BOLD, 38), fill=INK)
    d.text((tx, ly + 92), "IN HISTORIC SUMMIT", font=font(BOLD, 38), fill=INK)
    d.text((tx, ly + 144), "The three leaders sit down together for the first",
           font=font(REG, 22), fill=BODY)
    d.text((tx, ly + 170), "time, at the APEC summit in Shenzhen.",
           font=font(REG, 22), fill=BODY)
    draw_globe(d, lx + lw - 78, ly + 100, 58, INK)

    # ---- story grid ----
    stories = [
        ("01", (29, 78, 137), "GTA VI LAUNCHES WORLDWIDE",
         "After 13 years, Rockstar's sequel goes on sale at midnight."),
        ("02", (14, 124, 123), "ANTHROPIC DEBUTS ON NASDAQ",
         "AI firm lists as ANT; IPO prices at $83, a $1.5 trillion value."),
        ("03", (185, 122, 15), "ISRAEL LAUNCHES GAZA GROUND OP",
         "Army and Shin Bet open a joint operation in Hamas-held Gaza."),
        ("04", (109, 59, 142), "ALLIES RALLY FOR KYIV IN BERLIN",
         "European allies meet with Trump's envoys Witkoff and Kushner."),
        ("05", (74, 85, 104), "VOYAGER 1, ONE LIGHT-DAY OUT",
         "The probe passes a milestone no human-made object has reached."),
        ("06", (11, 94, 89), "MUSK'S $500M BET ON TEXAS",
         "Musk spent nearly half a billion backing Republicans to keep Texas red."),
    ]
    pw, ph, gap = 468, 164, 16
    gy = 416
    for i, (num, color, head, body) in enumerate(stories):
        x = mx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        panel(d, x, y, pw, ph, num, color, head, body)

    # ---- footer ----
    d.rectangle([mx, 946, W - mx, 947], fill=LINE)
    foot = "Thursday 19 November 2026  •  Compiled from wire reports of the day"
    ff = font(REG, 19)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 960), foot, font=ff, fill=MUTED)
    also = "Also: dozens missing after a migrant boat sinks off Senegal  •  60 Houthi targets hit in Yemen"
    af = font(REG, 18)
    d.text(((W - d.textlength(also, font=af)) / 2, 984), also, font=af, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
