#!/usr/bin/env python3
"""THE WORLD TODAY - Monday 23 November 2026.
Front page built fresh from the 23 Nov research dossier.
Deterministic: Pillow only, no network, no external assets.
Render: python3 generate.py  ->  news.png (1024x1024)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 248, 236)
INK = (18, 18, 18)
RED = (178, 24, 24)
NAVY = (28, 54, 92)
BLUE = (46, 92, 140)
GOLD = (176, 124, 20)
GREY = (90, 88, 82)
LIGHT = (238, 232, 216)
OCEAN = (205, 226, 240)
LAND = (168, 198, 134)
LAND_EDGE = (92, 124, 64)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
DS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, w, text, font, fill=INK, leading=None, max_lines=None):
    if leading is None:
        leading = font.size + 3
    lines = wrap(d, text, font, w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stickmen
# FIXED CHARACTER BLOCK (defined once, reused in every scene):
#   tie  = negotiator  (navy suit, red tie)
#   helm = rescuer     (yellow helmet, orange vest)
#   cap  = sailor      (white cap, navy shirt)
#   case = delegate    (grey suit, brown briefcase)
# One line weight, one palette, one pose language for the whole page.
def stick(d, x, y, s, role, pose="stand", flip=False):
    """Draw a stickman. (x,y) = ground point under the feet. s = height px."""
    lw = max(2, int(s * 0.075))
    fx = -1 if flip else 1
    head_r = s * 0.14
    hx, hy = x, y - s * 0.86
    neck = (x, y - s * 0.72)
    hip = (x, y - s * 0.38)
    shirt = {"tie": NAVY, "helm": (196, 90, 20), "cap": NAVY, "case": (74, 74, 74)}[role]
    skin = (232, 190, 150)
    # legs
    if pose == "run":
        d.line([hip, (x - s * 0.22 * fx, y)], fill=INK, width=lw)
        d.line([hip, (x + s * 0.20 * fx, y - s * 0.10)], fill=INK, width=lw)
    elif pose == "kneel":
        d.line([hip, (x - s * 0.18 * fx, y)], fill=INK, width=lw)
        d.line([hip, (x + s * 0.16 * fx, y - s * 0.16)], fill=INK, width=lw)
    else:
        d.line([hip, (x - s * 0.13 * fx, y)], fill=INK, width=lw)
        d.line([hip, (x + s * 0.13 * fx, y)], fill=INK, width=lw)
    # torso
    d.line([neck, hip], fill=shirt, width=lw + 1)
    # arms
    sh = (x, y - s * 0.68)
    if pose == "point":
        d.line([sh, (x + s * 0.34 * fx, y - s * 0.72)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.14 * fx, y - s * 0.42)], fill=shirt, width=lw)
    elif pose == "carry":
        d.line([sh, (x + s * 0.30 * fx, y - s * 0.42)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.26 * fx, y - s * 0.44)], fill=shirt, width=lw)
    elif pose == "shake":
        d.line([sh, (x + s * 0.30 * fx, y - s * 0.55)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.12 * fx, y - s * 0.45)], fill=shirt, width=lw)
    elif pose == "wave":
        d.line([sh, (x + s * 0.26 * fx, y - s * 0.92)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.14 * fx, y - s * 0.45)], fill=shirt, width=lw)
    elif pose == "hold":
        d.line([sh, (x + s * 0.28 * fx, y - s * 0.50)], fill=shirt, width=lw)
        d.line([sh, (x + s * 0.24 * fx, y - s * 0.50)], fill=shirt, width=lw)
    elif pose == "lift":
        d.line([sh, (x + s * 0.30 * fx, y - s * 0.88)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.28 * fx, y - s * 0.86)], fill=shirt, width=lw)
    else:
        d.line([sh, (x + s * 0.16 * fx, y - s * 0.42)], fill=shirt, width=lw)
        d.line([sh, (x - s * 0.16 * fx, y - s * 0.42)], fill=shirt, width=lw)
    # head
    d.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r],
              fill=skin, outline=INK, width=1)
    # role headgear / tie / case
    if role == "tie":
        d.line([neck, (x, y - s * 0.46)], fill=RED, width=max(2, int(s * 0.06)))
        d.polygon([(x - s * 0.05, y - s * 0.46), (x + s * 0.05, y - s * 0.46),
                   (x, y - s * 0.38)], fill=RED)
        d.arc([hx - head_r, hy - head_r, hx + head_r, hy + head_r * 0.4],
              180, 360, fill=INK, width=2)
    elif role == "helm":
        d.pieslice([hx - head_r - 1, hy - head_r - 2, hx + head_r + 1, hy + head_r * 0.5],
                   180, 360, fill=(240, 200, 30), outline=INK, width=1)
        d.rectangle([hx - head_r - 2, hy - 1, hx + head_r + 2, hy + 2],
                    fill=(240, 200, 30), outline=INK)
    elif role == "cap":
        d.pieslice([hx - head_r - 1, hy - head_r - 1, hx + head_r + 1, hy + head_r * 0.3],
                   180, 360, fill=(245, 245, 245), outline=INK, width=1)
        d.rectangle([hx - head_r - 1, hy - 1, hx + head_r + 3, hy + 2],
                    fill=(245, 245, 245), outline=INK)
    elif role == "case":
        d.line([neck, (x, y - s * 0.48)], fill=(120, 90, 40), width=max(2, int(s * 0.05)))
        # briefcase held at side
        bx = x - s * 0.30 * fx
        d.rectangle([bx - s * 0.11, y - s * 0.34, bx + s * 0.11, y - s * 0.16],
                    fill=(146, 104, 52), outline=INK, width=1)
        d.line([(bx, y - s * 0.34), (bx, y - s * 0.40)], fill=INK, width=2)
    return (hx, hy)


def waves(d, x0, y0, w, y, color=BLUE):
    for i in range(5):
        xx = x0 + i * (w // 4)
        d.arc([xx, y - 4, xx + w // 4, y + 4], 200, 340, fill=color, width=2)


# ---------------------------------------------------------------- lead scenes
def scene_l1(d, x, y, w, h):
    """Benghazi: sea drone hits a warship at the port."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    d.rectangle([x, y, x + w, y + 22], fill=(214, 233, 245))
    d.ellipse([x + w - 34, y + 4, x + w - 12, y + 26], fill=(255, 236, 150),
              outline=GOLD, width=1)
    # pier
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 110, 96))
    # warship hull, listing to starboard (bow low, stern high)
    d.polygon([(x + 34, y + h - 30), (x + 66, y + h - 40), (x + w - 78, y + h - 48),
               (x + w - 52, y + h - 36), (x + w - 58, y + h - 16), (x + 48, y + h - 16)],
              fill=(96, 106, 118), outline=INK)
    d.line([(x + 34, y + h - 30), (x + w - 78, y + h - 48)], fill=(70, 80, 92), width=2)
    # superstructure + funnel + mast with flag
    d.rectangle([x + 120, y + h - 66, x + 188, y + h - 46], fill=(128, 136, 146),
                outline=INK)
    d.rectangle([x + 196, y + h - 60, x + 210, y + h - 46], fill=(90, 90, 90),
                outline=INK)
    d.line([(x + 150, y + h - 66), (x + 150, y + h - 80)], fill=INK, width=2)
    d.polygon([(x + 150, y + h - 80), (x + 168, y + h - 74), (x + 150, y + h - 70)],
              fill=RED)
    # portholes along the hull
    for hx_ in range(x + 84, x + w - 90, 26):
        d.ellipse([hx_, y + h - 34, hx_ + 6, y + h - 28], fill=(220, 230, 240),
                  outline=INK)
    # smoke + fire at the bow
    for (sx, sy, r) in [(x + 52, y + h - 56, 8), (x + 62, y + h - 66, 11),
                        (x + 76, y + h - 76, 8)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    d.polygon([(x + 40, y + h - 32), (x + 52, y + h - 52), (x + 64, y + h - 32)],
              fill=(240, 120, 30))
    d.polygon([(x + 46, y + h - 32), (x + 52, y + h - 44), (x + 58, y + h - 32)],
              fill=(255, 200, 40))
    # sea drone skimming the water
    dx, dy = x + w - 96, y + h - 26
    d.ellipse([dx - 12, dy - 4, dx + 12, dy + 4], fill=(60, 60, 60), outline=INK)
    d.ellipse([dx - 20, dy - 8, dx - 8, dy - 2], fill=(200, 200, 200), outline=INK)
    d.ellipse([dx + 8, dy - 8, dx + 20, dy - 2], fill=(200, 200, 200), outline=INK)
    waves(d, x, y, w, y + h - 6)
    # sailor on the pier pointing at the blast, rescuer running in
    stick(d, x + w - 22, y + h - 16, 52, "cap", "point", flip=True)
    stick(d, x + 18, y + h - 16, 48, "helm", "run")
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def scene_l2(d, x, y, w, h):
    """Cikande: rescuers carry a survivor from the burning candy factory."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    d.rectangle([x, y, x + w, y + 20], fill=(240, 228, 210))
    # factory block
    d.rectangle([x + 14, y + 30, x + w - 90, y + h - 14], fill=(176, 120, 88), outline=INK)
    d.rectangle([x + 14, y + 30, x + w - 90, y + 42], fill=(120, 70, 60), outline=INK)
    d.text((x + 22, y + 31), "MILKITA", font=F(DJB, 9), fill=(255, 255, 255))
    for wx in range(x + 28, x + w - 100, 34):
        d.rectangle([wx, y + 48, wx + 18, y + 62], fill=(60, 60, 70), outline=INK)
    # flames + smoke from the roof
    for fx in (x + 40, x + 90, x + 140):
        d.polygon([(fx - 14, y + 32), (fx, y + 6), (fx + 14, y + 32)], fill=(240, 120, 30))
        d.polygon([(fx - 7, y + 32), (fx, y + 16), (fx + 7, y + 32)], fill=(255, 200, 40))
    for (sx, sy, r) in [(x + 60, y + 2, 8), (x + 110, y - 2, 10)]:
        d.ellipse([sx - r, sy, sx + r, sy + r], fill=(110, 110, 110))
    # rubble
    d.polygon([(x + w - 86, y + h - 14), (x + w - 40, y + h - 30), (x + w - 8, y + h - 14)],
              fill=(140, 130, 118), outline=INK)
    # stretcher team: two rescuers carrying a survivor
    d.line([(x + w - 96, y + h - 30), (x + w - 42, y + h - 30)], fill=(200, 60, 40), width=3)
    stick(d, x + w - 100, y + h - 14, 50, "helm", "carry")
    stick(d, x + w - 38, y + h - 14, 50, "helm", "carry", flip=True)
    # survivor lying on the stretcher
    d.line([(x + w - 84, y + h - 38), (x + w - 52, y + h - 38)], fill=(232, 190, 150), width=5)
    d.ellipse([x + w - 52, y + h - 44, x + w - 42, y + h - 34], fill=(232, 190, 150),
              outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def scene_l3(d, x, y, w, h):
    """New Delhi: two PMs shake hands before the palace, delegates behind."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 214))
    d.rectangle([x, y, x + w, y + 18], fill=(188, 210, 235))
    # Rashtrapati Bhavan facade
    d.rectangle([x + 20, y + 34, x + w - 20, y + h - 16], fill=(214, 178, 132), outline=INK)
    d.polygon([(x + w // 2 - 46, y + 22), (x + w // 2 + 46, y + 22), (x + w // 2, y + 6)],
              fill=(190, 150, 100), outline=INK)
    # dome sitting on the roofline, with a spire
    d.pieslice([x + w // 2 - 17, y + 8, x + w // 2 + 17, y + 40], 180, 360,
               fill=(240, 210, 160), outline=INK)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + 2)], fill=INK, width=2)
    d.ellipse([x + w // 2 - 2, y + 1, x + w // 2 + 2, y + 5], fill=GOLD, outline=INK)
    for cx in range(x + 44, x + w - 40, 44):
        d.rectangle([cx, y + 44, cx + 10, y + h - 16], fill=(190, 150, 100), outline=INK)
    # flags
    for fx, col in ((x + 30, (255, 153, 51)), (x + w - 38, (255, 153, 51))):
        d.line([(fx, y + 22), (fx, y + 44)], fill=INK, width=2)
        d.polygon([(fx, y + 22), (fx + 20, y + 27), (fx, y + 32)], fill=col)
    # red carpet
    d.polygon([(x + w // 2 - 34, y + h - 16), (x + w // 2 + 34, y + h - 16),
               (x + w // 2 + 52, y + h), (x + w // 2 - 52, y + h)], fill=RED)
    # the handshake
    stick(d, x + w // 2 - 26, y + h - 14, 58, "tie", "shake")
    stick(d, x + w // 2 + 26, y + h - 14, 58, "tie", "shake", flip=True)
    # delegates with briefcases flanking
    stick(d, x + 34, y + h - 14, 46, "case", "stand")
    stick(d, x + w - 34, y + h - 14, 46, "case", "stand", flip=True)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


# ---------------------------------------------------------------- mini scenes
def mini_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    d.polygon([(x + 20, y + h - 22), (x + w - 20, y + h - 22), (x + w - 30, y + h - 8),
               (x + 30, y + h - 8)], fill=(150, 60, 50), outline=INK)
    d.rectangle([x + w // 2 - 14, y + h - 40, x + w // 2 + 14, y + h - 22],
                fill=(240, 240, 240), outline=INK)
    d.polygon([(x + 30, y + h - 24), (x + 42, y + h - 44), (x + 54, y + h - 24)],
              fill=(240, 120, 30))
    d.ellipse([x + 44, y + 2, x + 62, y + 18], fill=(120, 120, 120))
    waves(d, x, y, w, y + h - 3)


def mini_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # conference table + flags + globe
    d.ellipse([x + w - 52, y + 4, x + w - 8, y + 34], fill=(120, 180, 120), outline=INK)
    d.arc([x + w - 52, y + 4, x + w - 8, y + 34], 0, 180, fill=BLUE, width=2)
    d.rectangle([x + 10, y + h - 16, x + w - 10, y + h - 8], fill=(120, 84, 50), outline=INK)
    for fx, col in ((x + 16, (0, 128, 0)), (x + 34, (178, 24, 24)), (x + 52, (28, 54, 92))):
        d.line([(fx, y + 8), (fx, y + h - 16)], fill=INK, width=1)
        d.polygon([(fx, y + 8), (fx + 12, y + 12), (fx, y + 16)], fill=col)
    stick(d, x + w - 68, y + h - 8, 26, "tie", "point")


def mini_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 236, 220))
    pts = [(x + 8, y + h - 12), (x + 44, y + h - 18), (x + 76, y + h - 14),
           (x + 108, y + 12), (x + 140, y + 16), (x + w - 10, y + 8)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.rectangle([x + w - 34, y + 4, x + w - 8, y + 18], fill=(30, 30, 30), outline=INK)
    d.text((x + w - 31, y + 5), "AI", font=F(DJB, 9), fill=(255, 255, 255))


def mini_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 230, 222))
    d.rectangle([x + 20, y + h - 14, x + w - 20, y + h - 6], fill=(200, 200, 200), outline=INK)
    d.polygon([(x + w // 2 - 34, y + h - 14), (x + w // 2 + 34, y + h - 14),
               (x + w // 2, y + 10)], fill=(220, 220, 220), outline=INK)
    d.ellipse([x + w // 2 - 12, y + 4, x + w // 2 + 12, y + 22], fill=(240, 240, 240),
              outline=INK)
    for cx in range(x + w // 2 - 24, x + w // 2 + 20, 12):
        d.line([(cx, y + h - 24), (cx, y + h - 14)], fill=INK, width=1)
    d.rectangle([x + w - 44, y + 4, x + w - 10, y + 18], fill=(178, 24, 24), outline=INK)
    d.text((x + w - 41, y + 5), "258", font=F(DJB, 9), fill=(255, 255, 255))


def mini_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 130))
    d.ellipse([x + 8, y + h - 22, x + 36, y + h - 2], fill=(255, 255, 255), outline=INK)
    d.polygon([(x + 22, y + h - 18), (x + 28, y + h - 12), (x + 22, y + h - 6),
               (x + 16, y + h - 12)], fill=INK)
    # trophy
    d.polygon([(x + w - 56, y + 6), (x + w - 26, y + 6), (x + w - 32, y + 26),
               (x + w - 50, y + 26)], fill=GOLD, outline=INK)
    d.rectangle([x + w - 48, y + 26, x + w - 34, y + 32], fill=GOLD, outline=INK)
    d.rectangle([x + w - 52, y + 32, x + w - 30, y + 36], fill=GOLD, outline=INK)
    d.line([(x + 40, y + h - 6), (x + w - 60, y + h - 6)], fill=(255, 255, 255), width=2)


def mini_medical(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 238))
    d.rectangle([x + 10, y + 6, x + w - 70, y + h - 8], fill=(40, 40, 60), outline=INK)
    d.ellipse([x + 22, y + 12, x + 46, y + 32], fill=(200, 220, 240), outline=BLUE, width=2)
    d.ellipse([x + 52, y + 12, x + 76, y + 32], fill=(200, 220, 240), outline=BLUE, width=2)
    d.text((x + w - 62, y + h - 16), "AI", font=F(DJB, 12), fill=RED)
    # pink ribbon bow
    d.polygon([(x + w - 42, y + 4), (x + w - 29, y + 12), (x + w - 42, y + 20)],
              fill=(220, 60, 120))
    d.polygon([(x + w - 16, y + 4), (x + w - 29, y + 12), (x + w - 16, y + 20)],
              fill=(220, 60, 120))
    d.ellipse([x + w - 32, y + 9, x + w - 26, y + 15], fill=(180, 30, 100))


def mini_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 204))
    d.polygon([(x + 14, y + h - 8), (x + 60, y + h - 26), (x + 110, y + h - 8),
               (x + 150, y + h - 20), (x + w - 10, y + h - 8)], fill=(150, 170, 120),
              outline=INK)
    pts = [(x + 8, y + 14), (x + 30, y + 14), (x + 40, y + 4), (x + 52, y + 26),
           (x + 64, y + 6), (x + 78, y + 22), (x + 92, y + 14), (x + 118, y + 14)]
    d.line(pts, fill=RED, width=2)
    d.rectangle([x + w - 56, y + 4, x + w - 6, y + 18], fill=(255, 255, 255), outline=INK)
    d.text((x + w - 53, y + 5), "M6.5", font=F(DJB, 10), fill=RED)


def mini_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 236, 240))
    d.rectangle([x + 14, y + 8, x + w - 60, y + h - 6], fill=(245, 245, 245), outline=INK)
    d.rectangle([x + w // 2 - 34, y + 12, x + w // 2 - 26, y + 28], fill=RED)
    d.rectangle([x + w // 2 - 40, y + 18, x + w // 2 - 20, y + 24], fill=RED)
    d.ellipse([x + w - 44, y + 6, x + w - 16, y + 30], fill=(120, 60, 160), outline=INK)
    for (vx, vy) in ((x + w - 38, y + 12), (x + w - 24, y + 20), (x + w - 32, y + 26)):
        d.ellipse([vx - 2, vy - 2, vx + 2, vy + 2], fill=(255, 255, 255))
    stick(d, x + w - 62, y + h - 6, 24, "helm", "stand")


def mini_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 244))
    # fuselage + wing + tail
    d.ellipse([x + 10, y + 12, x + 92, y + 24], fill=(245, 245, 245), outline=INK)
    d.polygon([(x + 38, y + 12), (x + 54, y + 2), (x + 64, y + 12)], fill=(200, 60, 60),
              outline=INK)
    d.polygon([(x + 12, y + 12), (x + 20, y + 4), (x + 26, y + 12)], fill=(200, 60, 60),
              outline=INK)
    for wx in (72, 78, 84):
        d.ellipse([x + wx, y + 16, x + wx + 3, y + 19], fill=NAVY)
    d.rectangle([x + 110, y + h - 26, x + w - 12, y + h - 8], fill=(255, 255, 255),
                outline=INK)
    d.text((x + 114, y + h - 25), "PROTEST", font=F(DJB, 8), fill=RED)
    d.line([(x + 126, y + h - 26), (x + 126, y + h - 34)], fill=INK, width=2)


def mini_hockey(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 240))
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 4], fill=(245, 245, 245), outline=INK)
    d.line([(x + 44, y + 8), (x + 66, y + h - 12)], fill=(120, 60, 30), width=3)
    d.line([(x + w - 44, y + 8), (x + w - 66, y + h - 12)], fill=(178, 24, 24), width=3)
    d.ellipse([x + w // 2 - 7, y + h - 18, x + w // 2 + 7, y + h - 6], fill=INK)
    d.text((x + 10, y + 4), "MTL", font=F(DJB, 10), fill=RED)
    d.text((x + w - 42, y + 4), "DET", font=F(DJB, 10), fill=NAVY)


MINI = [mini_tanker, mini_cop, mini_market, mini_capitol, mini_football,
        mini_medical, mini_quake, mini_hospital, mini_plane, mini_hockey]

# ---------------------------------------------------------------- brief glyphs
def glyph(d, x, y, kind):
    """One small drawn glyph per brief, 20x20 box at (x,y)."""
    s = 20
    cx, cy = x + 10, y + 10
    if kind == "chart":  # B1 power index
        d.line([(x + 2, y + 16), (x + 7, y + 10), (x + 12, y + 12), (x + 18, y + 4)],
               fill=NAVY, width=2)
        d.polygon([(x + 18, y + 4), (x + 14, y + 4), (x + 18, y + 8)], fill=NAVY)
    elif kind == "gold":  # B2 gold
        d.polygon([(x + 3, y + 13), (x + 8, y + 6), (x + 13, y + 6), (x + 18, y + 13)],
                  fill=GOLD, outline=INK)
        d.line([(x + 3, y + 13), (x + 18, y + 13)], fill=INK, width=2)
    elif kind == "up":  # B3 futures
        d.polygon([(x + 10, y + 3), (x + 17, y + 12), (x + 12, y + 12), (x + 12, y + 17),
                   (x + 8, y + 17), (x + 8, y + 12), (x + 3, y + 12)], fill=(0, 128, 0))
    elif kind == "cricket":  # B4
        d.line([(x + 4, y + 4), (x + 14, y + 14)], fill=(150, 100, 40), width=3)
        d.ellipse([x + 12, y + 12, x + 19, y + 19], fill=RED, outline=INK)
    elif kind == "drop":  # B5 reservoir
        d.polygon([(x + 10, y + 2), (x + 17, y + 12), (x + 10, y + 18), (x + 3, y + 12)],
                  fill=BLUE, outline=INK)
    elif kind == "gem":  # B6 Bulgari
        d.polygon([(x + 4, y + 7), (x + 10, y + 3), (x + 16, y + 7), (x + 14, y + 16),
                   (x + 6, y + 16)], fill=(120, 220, 230), outline=INK)
        d.line([(x + 4, y + 7), (x + 16, y + 7)], fill=INK, width=1)
    elif kind == "rubble":  # B7 Dymer
        d.polygon([(x + 2, y + 17), (x + 8, y + 8), (x + 14, y + 12), (x + 18, y + 17)],
                  fill=(140, 130, 118), outline=INK)
        d.ellipse([x + 12, y + 3, x + 18, y + 9], fill=(240, 200, 30), outline=INK)
    elif kind == "drone":  # B8 IRGC claim
        d.ellipse([x + 6, y + 8, x + 14, y + 12], fill=(60, 60, 60), outline=INK)
        d.ellipse([x + 2, y + 5, x + 7, y + 8], fill=(200, 200, 200), outline=INK)
        d.ellipse([x + 13, y + 5, x + 18, y + 8], fill=(200, 200, 200), outline=INK)
        d.text((x + 2, y + 13), "78?", font=F(DJB, 7), fill=RED)
    elif kind == "barrel":  # B9 oil
        d.ellipse([x + 4, y + 4, x + 16, y + 9], fill=(40, 40, 40), outline=INK)
        d.rectangle([x + 4, y + 7, x + 16, y + 17], fill=(60, 60, 60), outline=INK)
        d.ellipse([x + 4, y + 14, x + 16, y + 19], fill=(30, 30, 30), outline=INK)
    elif kind == "star":  # B10 NATO
        d.polygon([(x + 10, y + 2), (x + 12, y + 8), (x + 18, y + 8), (x + 13, y + 12),
                   (x + 15, y + 18), (x + 10, y + 14), (x + 5, y + 18), (x + 7, y + 12),
                   (x + 2, y + 8), (x + 8, y + 8)], fill=NAVY)
    elif kind == "flag":  # B11 Sudan
        d.line([(x + 4, y + 3), (x + 4, y + 18)], fill=INK, width=2)
        d.rectangle([x + 4, y + 3, x + 18, y + 7], fill=RED)
        d.rectangle([x + 4, y + 7, x + 18, y + 11], fill=(255, 255, 255), outline=INK)
        d.rectangle([x + 4, y + 11, x + 18, y + 15], fill=INK)
    elif kind == "chip":  # B12 Nvidia
        d.rectangle([x + 5, y + 5, x + 15, y + 15], fill=(30, 90, 30), outline=INK)
        for px in (8, 12):
            d.line([(px, y + 2), (px, y + 5)], fill=INK, width=1)
            d.line([(px, y + 15), (px, y + 18)], fill=INK, width=1)
        d.text((x + 7, y + 7), "NV", font=F(DJB, 6), fill=(255, 255, 255))
    elif kind == "blast":  # B13 Iowa
        d.polygon([(x + 10, y + 2), (x + 13, y + 8), (x + 18, y + 9), (x + 13, y + 12),
                   (x + 15, y + 18), (x + 10, y + 14), (x + 5, y + 18), (x + 7, y + 12),
                   (x + 2, y + 9), (x + 7, y + 8)], fill=(240, 140, 30), outline=INK)
    elif kind == "bottle":  # B14 Bisleri
        d.rectangle([x + 7, y + 3, x + 13, y + 6], fill=BLUE, outline=INK)
        d.rectangle([x + 5, y + 6, x + 15, y + 18], fill=(180, 220, 245), outline=INK)
        d.line([(x + 5, y + 12), (x + 15, y + 12)], fill=RED, width=2)
    elif kind == "letter":  # B15 blood letter
        d.rectangle([x + 3, y + 4, x + 17, y + 16], fill=(255, 255, 255), outline=INK)
        d.line([(x + 6, y + 8), (x + 14, y + 8)], fill=RED, width=1)
        d.line([(x + 6, y + 11), (x + 14, y + 11)], fill=RED, width=1)
        d.line([(x + 6, y + 14), (x + 11, y + 14)], fill=RED, width=1)
    elif kind == "wheat":  # B16 food deal
        d.ellipse([x + 6, y + 3, x + 10, y + 9], fill=GOLD, outline=INK)
        d.ellipse([x + 10, y + 3, x + 14, y + 9], fill=GOLD, outline=INK)
        d.ellipse([x + 8, y + 8, x + 12, y + 14], fill=GOLD, outline=INK)
        d.line([(x + 10, y + 14), (x + 10, y + 19)], fill=(120, 90, 40), width=2)
    elif kind == "bolt":  # B17 energy bills
        d.polygon([(x + 12, y + 2), (x + 6, y + 11), (x + 10, y + 11), (x + 8, y + 18),
                   (x + 14, y + 9), (x + 10, y + 9)], fill=(240, 200, 30), outline=INK)
    elif kind == "plate":  # B18 cloned plates
        d.rectangle([x + 2, y + 6, x + 18, y + 14], fill=(255, 255, 255), outline=INK)
        d.text((x + 4, y + 7), "AB12", font=F(DJB, 6), fill=NAVY)
    elif kind == "cap":  # B19 Purdue
        d.polygon([(x + 2, y + 8), (x + 10, y + 3), (x + 18, y + 8), (x + 10, y + 13)],
                  fill=INK)
        d.line([(x + 14, y + 10), (x + 14, y + 16)], fill=GOLD, width=2)
    elif kind == "badge":  # B20 FBI shooting
        d.polygon([(x + 10, y + 2), (x + 16, y + 5), (x + 16, y + 12), (x + 10, y + 18),
                   (x + 4, y + 12), (x + 4, y + 5)], fill=GOLD, outline=INK)
        d.ellipse([x + 8, y + 8, x + 12, y + 12], fill=NAVY)
    elif kind == "hack":  # B21 FBI database
        d.rectangle([x + 3, y + 6, x + 17, y + 16], fill=(40, 40, 60), outline=INK)
        d.text((x + 5, y + 8), "</>", font=F(DJB, 7), fill=(120, 255, 120))
    elif kind == "tax":  # B22 data-centre tax
        d.rectangle([x + 4, y + 4, x + 16, y + 16], fill=(255, 255, 255), outline=INK)
        d.text((x + 6, y + 6), "$%", font=F(DJB, 8), fill=RED)
    elif kind == "card":  # B23 credit card
        d.rectangle([x + 2, y + 5, x + 18, y + 15], fill=NAVY, outline=INK)
        d.rectangle([x + 2, y + 8, x + 18, y + 10], fill=GOLD)
        d.text((x + 4, y + 11), "10%", font=F(DJB, 6), fill=(255, 255, 255))
    elif kind == "doc":  # B24 executive order
        d.rectangle([x + 4, y + 2, x + 16, y + 18], fill=(255, 255, 255), outline=INK)
        d.line([(x + 7, y + 6), (x + 13, y + 6)], fill=INK, width=1)
        d.line([(x + 7, y + 10), (x + 13, y + 10)], fill=INK, width=1)
        d.ellipse([x + 11, y + 13, x + 17, y + 19], fill=RED, outline=INK)
    elif kind == "gavel":  # B25 appeals court
        d.line([(x + 4, y + 15), (x + 16, y + 4)], fill=(120, 80, 40), width=3)
        d.rectangle([x + 11, y + 3, x + 18, y + 9], fill=(120, 80, 40), outline=INK)
        d.line([(x + 3, y + 17), (x + 17, y + 17)], fill=INK, width=2)
    elif kind == "coin":  # B26 NZ dollar
        d.ellipse([x + 2, y + 2, x + 18, y + 18], fill=GOLD, outline=INK)
        d.text((x + 6, y + 5), "$", font=F(DJB, 10), fill=INK)
    elif kind == "poll":  # B28 Spain poll
        for i, hh in enumerate((6, 12, 9)):
            bx = x + 3 + i * 6
            d.rectangle([bx, y + 18 - hh, bx + 4, y + 18], fill=(RED if i == 0 else NAVY))
    d.rectangle([x, y, x + 20, y + 20], outline=(200, 194, 178), width=1)


# ---------------------------------------------------------------- world map
# Hand-plotted continent outlines (lon, lat). Equirectangular, equal x/y scale.
NA = [(-168, 66), (-162, 60), (-156, 58), (-152, 60), (-145, 60), (-140, 60),
      (-135, 57), (-130, 54), (-126, 49), (-124, 43), (-121, 37), (-117, 33),
      (-112, 29), (-109, 25), (-105, 20), (-100, 17), (-95, 16), (-92, 15),
      (-88, 13), (-84, 11), (-81, 9), (-79, 9), (-82, 13), (-85, 16), (-87, 21),
      (-90, 21), (-91, 19), (-95, 19), (-97, 22), (-97, 26), (-94, 29), (-90, 29),
      (-85, 30), (-82, 28), (-81, 25), (-80, 31), (-76, 35), (-74, 39), (-71, 41),
      (-69, 44), (-66, 45), (-61, 46), (-56, 47), (-54, 49), (-57, 52), (-60, 55),
      (-64, 58), (-68, 58), (-72, 62), (-78, 62), (-84, 66), (-90, 66), (-94, 69),
      (-100, 68), (-110, 68), (-120, 69), (-130, 70), (-140, 70), (-150, 71),
      (-158, 71), (-165, 68)]
GREENLAND = [(-55, 60), (-48, 60), (-42, 62), (-38, 65), (-32, 68), (-26, 70),
             (-20, 73), (-22, 77), (-30, 80), (-40, 81), (-52, 80), (-58, 77),
             (-58, 72), (-56, 66)]
SA = [(-79, 9), (-77, 5), (-80, -2), (-81, -6), (-77, -12), (-73, -17), (-70, -22),
      (-70, -28), (-72, -35), (-73, -42), (-74, -48), (-71, -53), (-66, -55),
      (-65, -50), (-63, -43), (-59, -38), (-54, -34), (-50, -30), (-45, -24),
      (-41, -22), (-39, -16), (-36, -10), (-35, -7), (-38, -4), (-42, -2),
      (-46, -1), (-50, 0), (-53, 4), (-57, 6), (-61, 9), (-65, 10), (-70, 11),
      (-74, 10), (-77, 8)]
AFRICA = [(-6, 35), (-9, 32), (-14, 28), (-16, 23), (-17, 18), (-16, 13), (-13, 9),
          (-9, 5), (-5, 5), (0, 6), (5, 4), (9, 4), (9, 0), (12, -3), (13, -7),
          (12, -11), (13, -15), (12, -19), (13, -23), (15, -27), (17, -31),
          (19, -34), (25, -34), (30, -30), (33, -26), (36, -21), (40, -16),
          (40, -11), (42, -6), (45, -2), (50, 0), (51, 6), (51, 11), (47, 11),
          (43, 12), (40, 15), (38, 20), (36, 25), (34, 28), (32, 31), (28, 31),
          (22, 33), (16, 32), (11, 34), (8, 37), (3, 37), (-1, 35)]
EURASIA = [(-9, 37), (-9, 42), (-3, 44), (-1, 46), (-2, 48), (-1, 50), (2, 51),
           (4, 53), (7, 55), (8, 58), (6, 60), (5, 62), (8, 64), (12, 66), (16, 69),
           (20, 70), (25, 71), (29, 71), (32, 69), (33, 68), (38, 68), (43, 68),
           (47, 69), (52, 69), (56, 69), (60, 69), (66, 71), (70, 72), (74, 73),
           (79, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 76), (110, 74),
           (115, 73), (120, 73), (126, 72), (132, 72), (138, 72), (144, 72),
           (150, 71), (156, 70), (162, 69), (168, 67), (173, 66), (178, 65),
           (178, 64), (172, 62), (166, 60), (162, 58), (160, 55), (158, 52),
           (156, 51), (153, 54), (150, 59), (144, 59), (141, 55), (141, 50),
           (140, 45), (137, 43), (133, 42), (130, 42), (127, 40), (126, 38),
           (123, 38), (121, 35), (122, 32), (120, 28), (118, 25), (115, 23),
           (112, 21), (109, 19), (108, 16), (106, 11), (105, 9), (103, 7),
           (101, 6), (100, 8), (98, 10), (97, 14), (95, 16), (93, 18), (91, 22),
           (89, 22), (87, 21), (85, 19), (83, 17), (80, 14), (78, 9), (76, 10),
           (74, 15), (72, 19), (70, 21), (67, 24), (64, 25), (61, 25), (58, 25),
           (57, 26), (55, 26), (52, 25), (50, 26), (49, 28), (48, 30), (50, 28),
           (52, 26), (54, 25), (56, 26), (58, 24), (59, 22), (57, 19), (55, 17),
           (52, 15), (48, 14), (45, 13), (43, 12), (41, 15), (39, 19), (37, 22),
           (35, 25), (35, 28), (34, 31), (36, 36), (33, 36), (30, 36), (27, 37),
           (24, 36), (22, 37), (20, 39), (19, 40), (17, 39), (16, 38), (15, 40),
           (13, 42), (12, 44), (10, 44), (8, 44), (6, 43), (4, 43), (1, 41),
           (0, 39), (-2, 37), (-5, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-2, 57), (0, 54), (1, 51), (-2, 50)]
IRELAND = [(-10, 52), (-8, 55), (-6, 55), (-6, 52), (-8, 51)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36), (141, 39),
         (141, 41), (142, 43), (144, 44), (143, 42), (141, 39), (139, 37), (137, 35),
         (135, 34), (132, 33), (130, 32)]
BORNEO = [(109, 1), (111, 3), (113, 5), (116, 6), (118, 2), (117, -2), (115, -4),
          (112, -4), (110, -2)]
SUMATRA = [(95, 5), (98, 3), (100, 0), (103, -3), (105, -5), (104, -6), (102, -4),
           (100, -1), (97, 2)]
JAVA = [(106, -6), (110, -7), (114, -8), (114, -9), (110, -8), (106, -7)]
NEWGUINEA = [(131, -1), (135, -2), (138, -3), (141, -4), (145, -6), (147, -8),
             (146, -8), (143, -8), (141, -8), (138, -7), (135, -5), (132, -3)]
PHILIPPINES = [(120, 18), (122, 17), (122, 14), (121, 11), (123, 10), (124, 12),
               (126, 15), (123, 18)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (123, -34), (129, -32),
             (132, -32), (135, -35), (137, -36), (140, -38), (144, -38), (147, -39),
             (150, -37), (153, -32), (153, -27), (151, -24), (148, -20), (146, -19),
             (143, -15), (142, -11), (141, -14), (140, -17), (137, -16), (135, -13),
             (133, -12), (131, -12), (128, -14), (125, -14), (122, -17), (119, -20),
             (116, -21)]
NZ_N = [(173, -35), (176, -38), (178, -38), (176, -40), (174, -41)]
NZ_S = [(167, -45), (169, -43), (171, -42), (173, -41), (172, -43), (169, -46),
        (167, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
              (43, -22), (43, -18)]
SRILANKA = [(80, 6), (81, 8), (80, 9), (79, 8)]
TAIWAN = [(120, 23), (121, 25), (121, 23)]
LANDS = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, IRELAND, JAPAN, BORNEO,
         SUMATRA, JAVA, NEWGUINEA, PHILIPPINES, AUSTRALIA, NZ_N, NZ_S,
         MADAGASCAR, SRILANKA, TAIWAN]

PINS = [  # (number, lon, lat, city)
    (1, 20.1, 32.1, "Benghazi"), (2, 106.3, -6.1, "Cikande"),
    (3, 77.2, 28.6, "New Delhi"), (4, 56.5, 26.6, "Strait of Hormuz"),
    (5, 30.7, 36.9, "Antalya"), (6, 127.0, 37.5, "Seoul"),
    (7, -77.0, 38.9, "Washington"), (8, 8.5, 47.4, "Zurich"),
    (9, 0.1, 52.2, "Cambridge"), (10, 167.0, -16.0, "Vanuatu"),
    (11, 29.5, 1.5, "Ituri"), (12, -122.3, 47.6, "Seattle"),
    (13, -73.6, 45.5, "Montreal"),
]
DOTS = [  # brief-story cities (small dots, no numbers)
    (-74.0, 40.7, "New York"), (174.8, -41.3, "Wellington"),
    (-0.1, 51.5, "London"), (12.5, 41.9, "Rome"), (30.3, 50.8, "Dymer"),
    (4.35, 50.85, "Brussels"), (32.5, 15.6, "Khartoum"),
    (-121.0, 37.35, "Santa Clara"), (-91.3, 40.8, "Middletown"),
    (76.8, 29.1, "Haryana"), (-86.9, 40.4, "W. Lafayette"),
    (-102.5, 47.98, "New Town"), (-3.7, 40.4, "Madrid"),
    (103.8, 1.35, "Singapore"),
]

# ---------------------------------------------------------------- content
LEADS = [
    dict(n=1, kick="WAR  •  LIBYA", scene=scene_l1,
         head="SUSPECTED UKRAINIAN SEA DRONE SINKS RUSSIAN CORVETTE IN BENGHAZI",
         body=("The Russian corvette Merkury was left listing and largely submerged at "
               "Benghazi naval base after a suspected Ukrainian sea-drone strike early "
               "Sunday, satellite images show. Libyan officials say four drones were "
               "intercepted and two hit the ship; 10 people were hurt. No side has "
               "claimed responsibility."),
         src="Reuters / Al Jazeera — 23 Nov"),
    dict(n=2, kick="DISASTER  •  INDONESIA", scene=scene_l2,
         head="24 CONFIRMED DEAD IN CIKANDE CANDY-FACTORY FIRE; DOZENS STILL MISSING",
         body=("Indonesia confirmed 24 dead on Monday in the blaze at the PT Fonusa "
               "Agung Mulia candy plant in Cikande, Banten, as rescuers searched for "
               "about 30 workers still missing in unstable rubble. About 300 people "
               "were inside; 29 survived. A suspected air-conditioner short circuit "
               "is blamed."),
         src="Reuters / AP — 23 Nov"),
    dict(n=3, kick="DIPLOMACY  •  INDIA", scene=scene_l3,
         head="NEPAL'S PM SHAH GETS CEREMONIAL WELCOME IN NEW DELHI, MEETS MODI",
         body=("Nepal PM Balendra Shah received a Guard of Honour at Rashtrapati Bhavan "
               "on Monday before bilateral talks with PM Narendra Modi at Hyderabad "
               "House — his first foreign trip since taking office in March. Energy, "
               "trade and post-flood rebuilding top the agenda."),
         src="IANS / Radio Nepal — 23 Nov"),
]

SECONDARIES = [
    dict(n=4, kick="GULF  •  HORMUZ", scene=mini_tanker,
         head="SIXTH TANKER HIT IN STRAIT OF HORMUZ",
         body=("UKMTO confirmed a vessel struck at 06:00 GMT Monday; Iran claims six "
               "tankers hit since Sunday. The strait carries ~20% of seaborne oil."),
         src="The Independent / Al Jazeera"),
    dict(n=5, kick="CLIMATE  •  ANTALYA", scene=mini_cop,
         head="SAUDI SWAY LOOMED OVER FAILED COP31 DEAL",
         body=("Reuters: Saudi officials had routine access to the presidency as "
               "fossil-fuel phase-out language stalled. First no-deal COP since 2009."),
         src="Reuters — 23 Nov"),
    dict(n=6, kick="MARKETS  •  SEOUL", scene=mini_market,
         head="KOSPI SINKS 5.3% IN AI ROUT",
         body=("Seoul fell to 4,632 on Monday after Friday's 5.2% drop. Taiwan's "
               "short-selling ban began; US futures rebounded."),
         src="Al Jazeera / Seeking Alpha"),
    dict(n=7, kick="POLITICS  •  WASHINGTON", scene=mini_capitol,
         head="DEMOCRATS SEAL 258 HOUSE SEATS",
         body=("Largest House majority since 1992 after Chuck Hubbard flipped North "
               "Carolina's 5th by 330 votes in a recount; Rep. Foxx conceded Sunday."),
         src="BBC — 23 Nov"),
    dict(n=8, kick="SPORT  •  ZURICH", scene=mini_football,
         head="FIFA SET TO CONFIRM UK AS 2035 WOMEN'S WORLD CUP HOST",
         body=("FIFA is scheduled to confirm the UK — the sole bidder — as host of the "
               "2035 Women's World Cup on Monday. A 48-team, 104-match tournament."),
         src="BBC Sport — scheduled Mon"),
    dict(n=9, kick="HEALTH  •  CAMBRIDGE", scene=mini_medical,
         head="NHS LAUNCHES WORLD'S BIGGEST AI BREAST-SCREENING TRIAL",
         body=("Nearly 700,000 women will be invited across 30 UK sites in the EDITH "
               "trial; AI will replace one of two human readers on mammograms."),
         src="BBC / Digital Health"),
    dict(n=10, kick="QUAKE  •  VANUATU", scene=mini_quake,
         head="M6.5 QUAKE SHAKES VANUATU REGION",
         body=("A very deep magnitude 6.5 quake struck at 02:40 UTC Monday, about 600 km "
               "down. No damage reported; Australia says no tsunami threat."),
         src="USGS / Xinhua"),
    dict(n=11, kick="HEALTH  •  ITURI", scene=mini_hospital,
         head="FIGHTING IN ITURI DISRUPTS CONGO EBOLA RESPONSE",
         body=("WHO chief: fighting near an Ituri hospital forced staff to shelter in a "
               "maternity ward for 24+ hours. Outbreak: 11,613 cases, 5,678 deaths."),
         src="Reuters / Al Jazeera"),
    dict(n=12, kick="USA  •  SEATTLE", scene=mini_plane,
         head="ICE DETENTION VIDEO SPARKS SEATTLE AIRPORT PROTEST",
         body=("Protesters marched at Sea-Tac after video showed masked officers "
               "detaining a father and daughter boarding a flight. Both remain detained."),
         src="The Guardian — 23 Nov"),
    dict(n=13, kick="SPORT  •  MONTREAL", scene=mini_hockey,
         head="RED WINGS TRADE CAPTAIN LARKIN TO CANADIENS",
         body=("Detroit dealt Dylan Larkin to Montreal for Kirby Dach, Samuel "
               "Montembeault, prospect Michael Hage and four draft picks in a "
               "blockbuster trade."),
         src="NHL.com / TSN"),
]

BRIEFS = [  # (glyph, bold lead, text) — 27 briefs, B1–B26 + B28 (B27 dropped)
    ("chart", "NEW DELHI — ", "India keeps Asia's No.3 power rank (40.5) in the Lowy Index 2026, closing on China. — The Hindu BusinessLine"),
    ("gold", "SINGAPORE — ", "Gold rebounds above $3,550 to $3,578/oz in Asian trade, snapping five days of losses after a 9% weekly slide. — Bloomberg"),
    ("up", "NEW YORK — ", "US stock futures rebound: Nasdaq 100 +~3%, S&P 500 +2%, Dow +~700 into a short Thanksgiving week. — FeedCast"),
    ("cricket", "WELLINGTON — ", "First India–NZ Test drawn: NZ 239/5 after India declared 720/9, a record Test total in New Zealand. — cricket.com.au"),
    ("drop", "LONDON — ", "England's reservoirs fall to 58% of capacity despite widespread rain; 16 reservoirs are less than half full. — Water Magazine"),
    ("gem", "ROME — ", "Funeral held Monday for Paolo Bulgari, the jeweller who built the family firm into a global luxury brand; he died aged 89. — AP"),
    ("rubble", "DYMER — ", "Monday update: toll from the Russian drone strike on a Kyiv-region apartment block rises to 11; a boy, 7, was pulled alive. — BBC"),
    ("drone", "TEHRAN — ", "IRGC claims it has downed 78 US drones (58 MQ-9s, 20 MQ-1s). The US has not commented. — Press TV"),
    ("barrel", "LONDON — ", "Brent falls to $92.55 and WTI to $83.45 as AI-bubble fears shake equities, outweighing Middle East supply risk. — FinScans"),
    ("star", "BRUSSELS — ", "NATO council meets Monday on Russian missiles in Poland; Warsaw confirmed three Kh-101 missiles fell 20 Nov. — Bytes Europe"),
    ("flag", "KHARTOUM — ", "US adviser Boulos decries Sudan violence, urges an end to arms flows, after a drone hit a UN building in Khartoum. — PANA"),
    ("chip", "SANTA CLARA — ", "Nvidia rebounds 6.7% after-hours to $133.92 after Friday's 14% plunge; Bessent seeks answers on China chips. — Benzinga"),
    ("blast", "MIDDLETOWN — ", "US Army delays the controlled blast of unstable explosives in Iowa to Wednesday, citing emergency powers. — Reuters"),
    ("bottle", "NEW DELHI — ", "Food regulator FSSAI orders prosecution of Bisleri International over unsafe packaged drinking water. — The Hindu"),
    ("letter", "HARYANA — ", "Congress legislator Gokul Setia writes a letter in blood to the Haryana chief minister and says police briefly detained him. — The Hindu"),
    ("wheat", "LONDON — ", "UK–EU food deal praised by British firms as a step that aligns trade: “We're pretty aligned anyway.” — Grand Herald"),
    ("bolt", "LONDON — ", "Centrica boss “very worried” about the impact of soaring energy bills on customers. — Grand Herald"),
    ("plate", "LONDON — ", "Victims of cloned number plates in England and Wales will get a new reporting tool. — Grand Herald"),
    ("cap", "WEST LAFAYETTE — ", "A Purdue professor and his two daughters are found dead in a suspected murder-suicide. — Curbside News"),
    ("badge", "NEW TOWN — ", "FBI investigates a shooting near New Town, North Dakota, that killed one person; the probe is in its early stages. — Valley News Live"),
    ("hack", "WASHINGTON — ", "The FBI's criminal database is reportedly hacked again, a wire roundup says. No official FBI confirmation. — Butler County News"),
    ("tax", "WASHINGTON — ", "Trump proposes a big tax on US companies that build data centres abroad. — Butler County News"),
    ("card", "WASHINGTON — ", "Trump says he will work with Democrats on a 10% cap on credit-card interest rates. — Butler County News"),
    ("doc", "WASHINGTON — ", "Executive order directs federal contractors to coordinate congressional responses with the White House. — Butler County News"),
    ("gavel", "WASHINGTON — ", "Appeals court rules against the federal pregnancy-accommodation rule in three states, AP reports. — AP"),
    ("coin", "WELLINGTON — ", "New Zealand dollar climbs above 0.5450 against the US dollar on strong retail sales data. — Grand Herald"),
    ("poll", "MADRID — ", "Spain poll (22 Nov, reported Monday): the PP leads and would need far-right Vox to govern; snap election is 29 Nov. — Particle"),
]

STATS = [
    ("258", "Democratic seats in the US House — largest majority since 1992"),
    ("−5.3%", "KOSPI at midday Monday (4,632), after −5.21% on Friday"),
    ("$3,578/oz", "Gold spot in Asian trade, +1.1%, after a 9% weekly slide"),
    ("M6.5", "Vanuatu-region quake, 02:40 UTC, ~600 km deep, no tsunami threat"),
    ("24", "Confirmed dead in the Cikande candy-factory fire; ~30 still missing"),
    ("700,000", "Women invited to the NHS EDITH AI breast-screening trial"),
]
TALLY = [("N. America", 13, RED), ("Europe", 11, NAVY), ("Asia", 5, (0, 128, 0)),
         ("SE Asia / Oceania", 4, (200, 120, 20)), ("Africa", 3, (120, 60, 160)),
         ("Middle East", 2, GOLD), ("Global", 2, GREY)]

DATE_CHECK = ("DATE CHECK — NOT today's news: COP31 collapsed 22 Nov · Merkury hit 22 Nov · "
              "Cikande fire 21 Nov · Hormuz tankers hit over the weekend · Skubal's $450m Mets "
              "deal 22 Nov · Delta 1,600+ flights delayed 22 Nov · Kh-101 missiles in Poland "
              "20 Nov · Chile reopens beef market to Colombia 22 Nov.")


# ---------------------------------------------------------------- build
def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    X0, X1 = 16, 1008

    # ---- masthead
    d.rectangle([0, 0, W, 58], fill=(12, 12, 12))
    d.text((W // 2, 6), "THE WORLD TODAY", font=F(DSB, 40), fill=(255, 255, 255),
           anchor="ma")
    d.text((W // 2, 48), "Monday 23 November 2026  •  40 stories  •  7 regions  •  One page",
           font=F(DJB, 10), fill=(232, 196, 90), anchor="ma")
    d.rectangle([0, 58, W, 61], fill=RED)

    # ---- date check
    y = 66
    y = block(d, X0, y, X1 - X0, DATE_CHECK, F(DJB, 8), fill=NAVY, leading=10,
              max_lines=2)
    d.line([(X0, y + 2), (X1, y + 2)], fill=INK, width=1)
    y += 6

    # ---- stat strip
    bw = int((X1 - X0 - 5 * 6) / 6)
    for i, (num, cap) in enumerate(STATS):
        bx = X0 + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 38], fill=(255, 255, 255), outline=INK)
        d.rectangle([bx, y, bx + bw, y + 3], fill=RED)
        d.text((bx + bw / 2, y + 4), num, font=F(DJB, 14), fill=RED, anchor="ma")
        block(d, bx + 4, y + 21, bw - 8, cap, F(DJ, 7), fill=INK, leading=8,
              max_lines=2)
    y += 44

    # ---- region tally bar
    total = sum(c for _, c, _ in TALLY)
    bx = X0
    for name, c, col in TALLY:
        wseg = (X1 - X0) * c / total
        d.rectangle([bx, y, bx + wseg, y + 12], fill=col, outline=PAPER)
        bx += wseg
    y += 14
    tx = X0
    for name, c, col in TALLY:
        lab = f"{name} {c}"
        d.text((tx, y), lab, font=F(DJB, 8), fill=col)
        tx += d.textlength(lab + "   •   ", font=F(DJB, 8))
    y += 12
    d.line([(X0, y), (X1, y)], fill=INK, width=1)
    y += 5

    # ---- leads
    d.text((X0, y), "TOP STORIES — MONDAY 23 NOVEMBER", font=F(DJB, 10), fill=RED)
    y += 13
    colw = int((X1 - X0 - 2 * 8) / 3)
    lead_top = y
    for i, L in enumerate(LEADS):
        lx = X0 + i * (colw + 8)
        d.text((lx, y), f"{L['n']}  {L['kick']}", font=F(DJB, 9), fill=RED)
        L["scene"](d, lx, y + 14, colw, 78)
        hy = y + 96
        hy = block(d, lx, hy, colw, L["head"], F(DJB, 12), leading=14, max_lines=2)
        hy = block(d, lx, hy + 1, colw, L["body"], F(DJ, 9), leading=11, max_lines=5)
        d.text((lx, hy + 1), "Source: " + L["src"], font=F(DJ, 7), fill=GREY)
        if i < 2:
            d.line([(lx + colw + 4, y), (lx + colw + 4, hy + 10)], fill=(200, 194, 178))
    y = lead_top + 190
    d.line([(X0, y), (X1, y)], fill=INK, width=1)
    y += 5

    # ---- secondaries: 2 rows x 5
    scolw = int((X1 - X0 - 4 * 8) / 5)
    for row in range(2):
        for col in range(5):
            S = SECONDARIES[row * 5 + col]
            sx = X0 + col * (scolw + 8)
            sy = y + row * 108
            d.text((sx, sy), f"{S['n']}  {S['kick']}", font=F(DJB, 7), fill=RED)
            S["scene"](d, sx, sy + 11, scolw, 34)
            ty = block(d, sx, sy + 48, scolw, S["head"], F(DJB, 9), leading=10.5,
                       max_lines=2)
            ty = block(d, sx, ty, scolw, S["body"], F(DJ, 7.5), leading=9.5,
                       max_lines=3)
            d.text((sx, ty), "Source: " + S["src"], font=F(DJ, 6.5), fill=GREY)
    y += 218
    d.line([(X0, y), (X1, y)], fill=INK, width=1)
    y += 4

    # ---- map + pin index
    d.text((X0, y), "WHERE IT HAPPENED", font=F(DJB, 11), fill=NAVY)
    d.text((X1, y), "Numbered pins = lead & secondary stories  •  dots = briefs",
           font=F(DJ, 8), fill=GREY, anchor="ra")
    y += 15
    mx, my, mw, mh = X0, y, 560, 186
    lat_top, lat_bot = 84.0, -60.0

    def proj(lon, lat):
        return (mx + (lon + 180.0) / 360.0 * mw,
                my + (lat_top - lat) / (lat_top - lat_bot) * mh)

    d.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN, outline=INK)
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = proj(lon, 0)
        d.line([(gx, my), (gx, my + mh)], fill=(255, 255, 255), width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, gy = proj(0, lat)
        d.line([(mx, gy), (mx + mw, gy)], fill=(255, 255, 255), width=1)
    _, eq = proj(0, 0)
    d.line([(mx, eq), (mx + mw, eq)], fill=(150, 190, 215), width=1)
    # continents
    for poly in LANDS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Europe/Asia divider (Urals–Caucasus line, subtle)
    div = [(60, 68), (60, 55), (55, 50), (48, 46), (44, 42), (40, 42)]
    d.line([proj(lon, lat) for lon, lat in div], fill=(120, 140, 90), width=1)
    d.text((proj(60, 60)[0] + 3, proj(60, 60)[1]), "URALS", font=F(DJB, 6),
           fill=(90, 110, 70))
    # ocean labels
    for lab, lon, lat in (("PACIFIC", -150, 8), ("ATLANTIC", -35, 18),
                          ("INDIAN", 85, -28), ("PACIFIC", 155, 5)):
        px, py = proj(lon, lat)
        d.text((px, py), lab, font=F(DJB, 7), fill=(110, 150, 185), anchor="mm")
    # brief dots first, then numbered pins on top (nudged where cities cluster)
    for lon, lat, city in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY, outline=(255, 255, 255))
    NUDGE = {1: (-6, 6), 13: (9, -5)}
    for n, lon, lat, city in PINS:
        px, py = proj(lon, lat)
        dx_, dy_ = NUDGE.get(n, (0, 0))
        if (dx_, dy_) != (0, 0):
            d.line([(px, py), (px + dx_, py + dy_)], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            px, py = px + dx_, py + dy_
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255),
                  width=2)
        d.text((px, py - 1), str(n), font=F(DJB, 8), fill=(255, 255, 255), anchor="mm")
    map_bottom = my + mh

    # pin index panel (right of map)
    px0 = mx + mw + 10
    pw = X1 - px0
    d.text((px0, my), "PIN INDEX", font=F(DJB, 10), fill=RED)
    iy = my + 15
    pin_names = {1: "Benghazi — corvette hit", 2: "Cikande — factory fire",
                 3: "New Delhi — Nepal PM visit", 4: "Hormuz — 6th tanker",
                 5: "Antalya — COP31 fallout", 6: "Seoul — KOSPI −5.3%",
                 7: "Washington — Dems 258 seats", 8: "Zurich — FIFA 2035",
                 9: "Cambridge — AI screening", 10: "Vanuatu — M6.5 quake",
                 11: "Ituri — Ebola response", 12: "Seattle — ICE protest",
                 13: "Montreal — Larkin trade"}
    for col_i, nums in enumerate(((1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13))):
        cx0 = px0 + col_i * (pw // 2 + 4)
        cy = iy
        for n in nums:
            d.ellipse([cx0, cy, cx0 + 11, cy + 11], fill=RED, outline=(255, 255, 255))
            d.text((cx0 + 5.5, cy + 5), str(n), font=F(DJB, 7), fill=(255, 255, 255),
                   anchor="mm")
            d.text((cx0 + 15, cy), pin_names[n], font=F(DJ, 8), fill=INK)
            cy += 14
    iy = my + 15 + 7 * 14 + 4
    d.line([(px0, iy), (X1, iy)], fill=(200, 194, 178))
    iy += 4
    d.text((px0, iy), "BRIEF CITIES (dots)", font=F(DJB, 8), fill=NAVY)
    iy += 11
    cities = ", ".join(c for _, _, c in DOTS)
    iy = block(d, px0, iy, pw, cities, F(DJ, 7.5), fill=GREY, leading=9.5,
               max_lines=3)
    y = map_bottom + 5
    d.line([(X0, y), (X1, y)], fill=INK, width=1)
    y += 5

    # ---- briefs: 3 columns x 9 rows
    d.text((X0, y), "ALSO ON MONDAY — THE REST OF THE WORLD IN ONE LINE EACH",
           font=F(DJB, 10), fill=RED)
    y += 13
    bcolw = int((X1 - X0 - 2 * 8) / 3)
    row_h = 19
    for idx, (kind, lead, text) in enumerate(BRIEFS):
        col, row = idx % 3, idx // 3
        bx = X0 + col * (bcolw + 8)
        by = y + row * row_h
        glyph(d, bx, by, kind)
        tx = bx + 24
        d.text((tx, by - 1), f"{14 + idx}", font=F(DJB, 7.5), fill=RED)
        # headline lead + wrapped text on one text block
        full = lead + text
        lines = wrap(d, full, F(DJ, 7.5), bcolw - 24 - 22)
        ly = by - 1
        for li, ln in enumerate(lines[:2]):
            if li == 0:
                d.text((tx + 20, ly), ln, font=F(DJ, 7.5), fill=INK)
            else:
                d.text((tx, ly), ln, font=F(DJ, 7.5), fill=INK)
            ly += 9
    y += 9 * row_h + 3
    d.line([(X0, y), (X1, y)], fill=INK, width=1)

    # ---- footer
    d.rectangle([0, y + 2, W, H], fill=(12, 12, 12))
    d.text((W // 2, y + 7),
           "All the day's news, in one image — Monday 23 November 2026",
           font=F(DJB, 9), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, y + 19),
           "Sources: Reuters, AP, BBC, Al Jazeera, The Hindu, NHL.com, USGS, WHO, Lowy Institute, "
           "IANS, The Guardian, Bloomberg, FXStreet, Press TV, PANA, TSN  •  Cut-off 08:15 UTC",
           font=F(DJ, 7), fill=(200, 200, 200), anchor="ma")
    return im


if __name__ == "__main__":
    img = build()
    img.save("news.png", optimize=True)
    print("saved news.png", img.size)
