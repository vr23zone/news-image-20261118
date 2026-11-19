#!/usr/bin/env python3
"""Draw entry.png: the world news of Wednesday 18 November 2026, by post.

THE WORLD BY POST — a stamp album for one day. Twelve perforated postage
stamps carry the day's biggest stories, each with a flat vector scene
drawn here in code, a place line, a headline and a two-to-three-line
caption, cancelled by a round postmark dated 18 NOV 2026. Below them a
POSTCARD BRIEFS strip adds 26 more of Wednesday's stories as numbered
one-liners, every one with its own emoji. An airmail (par avion) striped
border frames the page. 38 stories, 8 continents (the classic seven plus
Zealandia), plus deep space — all first reported on Wednesday
18 November 2026:

Stamps:
 1. Xi Jinping hosts Vladimir Putin in Shenzhen on the APEC sidelines;
    on Thursday Donald Trump joins them for the first-ever
    US-China-Russia trilateral summit (The Hindu / BBC / Reuters).
 2. US jets strike a Revolutionary Guards missile site on Iran's Qeshm
    Island; Iran answers with combat drones against bases in Kuwait and
    Bahrain (Reuters / BBC).
 3. A seven-stage Ukrainian drone-and-missile attack drops one arch of
    the Kerch Bridge into the strait; Zelensky calls it unprecedented
    (Horizon, 4 sources).
 4. Democrat Mary Peltola beats Republican Dan Sullivan in Alaska, the
    last midterm Senate race called; Democrats take the Senate 56-44
    (AP).
 5. The United States loses its measles-elimination status after 26
    years: 5,412 cases and 10 deaths in 2026 (PAHO via Zark News).
 6. Congo's Ebola outbreak passes 11,000 cases, the second-largest on
    record; around Bunia and Beni nearly three in four infected children
    under five die (Horizon / Zark News).
 7. NASA's Voyager 1 crosses one light-day from Earth, about 16 billion
    miles, at 5:16 a.m. ET on 18 November (NASA JPL via Zark News / ABC).
 8. Nvidia posts a record quarter and a $130bn revenue forecast; its
    board rules out reinstalling founder Jensen Huang as CEO
    (Horizon / Level Headlines).
 9. Fifteen million internal Deutsche Bank documents leak to Der Spiegel
    and about fifty media outlets, alleging the bank turned a blind eye
    to fraud and financed arms dealers (Horizon).
10. COP31 in Antalya launches the second Global Stocktake under the
    Paris Agreement while 21 negotiating issues stay deadlocked; the
    summit closes Friday (UN News).
11. Grand Theft Auto VI billboards go up from Tokyo to Sydney on the eve
    of the 19 November launch; New Zealand networks brace for about
    35 petabytes of downloads (Euronews).
12. Nations League final night: England beat Spain 3-2 to end Spain's
    43-match unbeaten run, Germany thrash the Netherlands 5-0, Norway
    (Haaland's stoppage-time penalty) and Portugal win 3-2 thrillers
    (Nigfooty / Aktualita).

Briefs 13-38 are listed in BRIEFS below with their sources named in the
README. All wording is typeset by this script from Noto Sans / Noto
Serif, and every emoji from Noto Color Emoji, so the text is exact.
Deterministic: the same bytes come out on every run.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
NOTO = "/usr/share/fonts/truetype/noto"

SERIF_B = f"{NOTO}/NotoSerif-Bold.ttf"
SANS_B = f"{NOTO}/NotoSans-Bold.ttf"
SANS = f"{NOTO}/NotoSans-Regular.ttf"
EMOJI_TTF = f"{NOTO}/NotoColorEmoji.ttf"

W, H = 1024, 1024
PAPER = (246, 239, 220)
INK = (29, 39, 51)
NAVY = (23, 54, 93)
RED = (179, 49, 42)
GREY = (84, 92, 110)
STAMP_FACE = (255, 253, 246)
TEAL = (14, 107, 98)

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def tw(d, s, f):
    return d.textlength(s, font=f)


def fit_font(d, s, path, start, minimum, maxw):
    size = start
    while size > minimum and tw(d, s, font(path, size)) > maxw:
        size -= 1
    return font(path, size)


def wrap(d, s, f, maxw, maxlines):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
            if len(lines) == maxlines:
                return lines
    if cur:
        lines.append(cur)
    return lines[:maxlines]


# ---------------- emoji (Noto Color Emoji, rendered once, cached) ----------
_emoji_cache = {}


def emoji_img(ch, h):
    if ch not in _emoji_cache:
        tile = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((6, 6), ch, font=font(EMOJI_TTF, 109), embedded_color=True)
        bbox = tile.getbbox()
        _emoji_cache[ch] = tile.crop(bbox) if bbox else tile
    src = _emoji_cache[ch]
    w2 = max(1, round(src.width * h / src.height))
    return src.resize((w2, h), Image.LANCZOS)


def paste_emoji(img, ch, x, y, h):
    e = emoji_img(ch, h)
    img.paste(e, (int(x), int(y)), e)
    return e.width


# ---------------- small drawing helpers ----------
def rr(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def star(d, cx, cy, r1, r2, n, **kw):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, **kw)


# ---------------- stamp scenes (212 x 74 each, flat vector) ----------
SW, SH = 212, 74


def scene_base(d, ox, oy, sky):
    d.rectangle([ox, oy, ox + SW, oy + SH], fill=sky)


def sc_summit(d, ox, oy):
    scene_base(d, ox, oy, (214, 233, 247))
    d.ellipse([ox + 168, oy + 6, ox + 196, oy + 34], fill=(247, 197, 78))
    rng = random.Random(7)
    for i in range(9):  # Shenzhen skyline
        bw = rng.randint(12, 24)
        bh = rng.randint(22, 48)
        bx = ox + 4 + i * 15
        d.rectangle([bx, oy + SH - 14 - bh, bx + bw, oy + SH - 14], fill=(70, 98, 138))
    d.rectangle([ox, oy + SH - 14, ox + SW, oy + SH], fill=(88, 120, 92))
    for fx, col in ((52, (206, 52, 44)), (106, (240, 240, 240)), (160, (38, 84, 168))):
        d.line([ox + fx, oy + 20, ox + fx, oy + 58], fill=(60, 60, 60), width=3)
        d.polygon([(ox + fx, oy + 20), (ox + fx + 20, oy + 25), (ox + fx, oy + 31)], fill=col)


def sc_qeshm(d, ox, oy):
    scene_base(d, ox, oy, (168, 205, 232))
    d.rectangle([ox, oy + 44, ox + SW, oy + SH], fill=(84, 142, 196))
    d.polygon([(ox + 18, oy + 50), (ox + 62, oy + 34), (ox + 116, oy + 44),
               (ox + 104, oy + 56), (ox + 34, oy + 58)], fill=(178, 148, 96))  # Qeshm island
    d.rectangle([ox + 58, oy + 38, ox + 70, oy + 46], fill=(110, 110, 116))
    d.rectangle([ox + 74, oy + 40, ox + 82, oy + 46], fill=(110, 110, 116))
    for i, (dx, dy) in enumerate(((140, 16), (168, 10), (192, 20))):  # drones
        d.line([ox + dx - 6, oy + dy, ox + dx + 6, oy + dy], fill=(40, 44, 52), width=2)
        d.line([ox + dx, oy + dy - 4, ox + dx, oy + dy + 4], fill=(40, 44, 52), width=2)
        d.arc([ox + dx - 52, oy + dy - 2, ox + dx - 4, oy + dy + 26], 300, 360,
              fill=(90, 90, 90), width=1)
    star(d, ox + 44, oy + 20, 13, 5, 8, fill=(240, 122, 40))
    star(d, ox + 44, oy + 20, 6, 2, 8, fill=(250, 208, 90))


def sc_kerch(d, ox, oy):
    scene_base(d, ox, oy, (219, 233, 242))
    d.rectangle([ox, oy + 50, ox + SW, oy + SH], fill=(110, 165, 214))
    for px in (36, 168):  # pylons
        d.rectangle([ox + px, oy + 18, ox + px + 8, oy + 56], fill=(96, 104, 116))
    d.rectangle([ox + 4, oy + 26, ox + 88, oy + 31], fill=(70, 78, 90))       # standing deck
    d.rectangle([ox + 128, oy + 26, ox + 208, oy + 31], fill=(70, 78, 90))
    d.polygon([(ox + 90, oy + 28), (ox + 126, oy + 28), (ox + 118, oy + 52),
               (ox + 94, oy + 46)], fill=(70, 78, 90))                        # fallen arch
    for sx in (98, 108, 118):  # splashes
        d.polygon([(ox + sx, oy + 58), (ox + sx + 3, oy + 48), (ox + sx + 6, oy + 58)],
                  fill=(240, 248, 255))
    d.line([ox + 40, oy + 18, ox + 104, oy + 27], fill=(150, 158, 170), width=1)
    d.line([ox + 172, oy + 18, ox + 110, oy + 27], fill=(150, 158, 170), width=1)


def sc_alaska(d, ox, oy):
    scene_base(d, ox, oy, (226, 238, 240))
    d.polygon([(ox, oy + 40), (ox + 40, oy + 12), (ox + 82, oy + 40)], fill=(240, 246, 250),
              outline=(170, 190, 200))
    d.polygon([(ox + 130, oy + 42), (ox + 172, oy + 14), (ox + 212, oy + 42)],
              fill=(240, 246, 250), outline=(170, 190, 200))
    cx = ox + 106  # capitol
    d.rectangle([cx - 34, oy + 46, cx + 34, oy + 64], fill=(248, 248, 244), outline=(150, 150, 145))
    d.pieslice([cx - 20, oy + 22, cx + 20, oy + 52], 180, 360, fill=(248, 248, 244),
               outline=(150, 150, 145))
    d.rectangle([cx - 2, oy + 14, cx + 2, oy + 24], fill=(120, 120, 118))
    d.rectangle([ox, oy + 64, ox + SW, oy + SH], fill=(196, 220, 205))
    d.rectangle([ox + 12, oy + 50, ox + 44, oy + 68], fill=(255, 255, 255), outline=(90, 90, 90), width=2)
    d.line([ox + 19, oy + 59, ox + 26, oy + 65], fill=(30, 140, 70), width=3)
    d.line([ox + 26, oy + 65, ox + + 38, oy + 54], fill=(30, 140, 70), width=3)


def sc_measles(d, ox, oy):
    scene_base(d, ox, oy, (253, 238, 218))
    def virus(cx, cy, r, col):
        for a in range(0, 360, 36):
            x2 = cx + (r + 7) * math.cos(math.radians(a))
            y2 = cy + (r + 7) * math.sin(math.radians(a))
            d.line([cx, cy, x2, y2], fill=col, width=3)
            d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=col)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        for (dx, dy) in ((-8, -4), (6, 2), (-2, 9), (10, -9)):
            d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=(255, 214, 170))
    virus(ox + 62, oy + 38, 20, (206, 84, 52))
    virus(ox + 128, oy + 24, 11, (224, 122, 74))
    virus(ox + 150, oy + 52, 8, (224, 122, 74))
    tx = ox + 186  # thermometer
    d.rectangle([tx - 4, oy + 8, tx + 4, oy + 52], fill=(255, 255, 255), outline=(120, 120, 120))
    d.rectangle([tx - 2, oy + 26, tx + 2, oy + 52], fill=(206, 52, 44))
    d.ellipse([tx - 8, oy + 50, tx + 8, oy + 66], fill=(206, 52, 44))


def sc_ebola(d, ox, oy):
    scene_base(d, ox, oy, (253, 243, 227))
    d.ellipse([ox + 178, oy + 6, ox + 202, oy + 30], fill=(247, 197, 78))
    d.rectangle([ox, oy + 60, ox + SW, oy + SH], fill=(214, 186, 138))
    tx, ty = ox + 66, oy + 26  # medical tent
    d.polygon([(tx - 38, ty + 34), (tx, ty), (tx + 38, ty + 34)], fill=(250, 250, 246),
              outline=(170, 170, 165))
    d.rectangle([tx - 30, ty + 34, tx + 30, ty + 40], fill=(240, 240, 235))
    d.rectangle([tx - 4, ty + 12, tx + 4, ty + 26], fill=(206, 52, 44))
    d.rectangle([tx - 8, ty + 16, tx + 8, ty + 21], fill=(206, 52, 44))
    for (vx, vy, vr) in ((158, 22, 5), (178, 44, 4), (146, 52, 3), (196, 26, 3)):
        d.ellipse([ox + vx - vr, oy + vy - vr, ox + vx + vr, oy + vy + vr], fill=(178, 92, 60))


def sc_voyager(d, ox, oy):
    scene_base(d, ox, oy, (10, 15, 38))
    rng = random.Random(42)
    for _ in range(46):
        sx, sy = rng.randint(2, SW - 3), rng.randint(2, SH - 3)
        d.point((ox + sx, oy + sy), fill=(235, 240, 255))
    d.ellipse([ox + 12, oy + 48, ox + 30, oy + 66], fill=(86, 148, 224))  # Earth
    for r in (12, 19, 26):  # signal arcs home
        d.arc([ox + 30 - r, oy + 57 - r, ox + 30 + r, oy + 57 + r], 300, 40,
              fill=(140, 190, 250), width=1)
    px, py = ox + 138, oy + 34  # probe
    d.ellipse([px - 24, py - 16, px + 10, py + 16], fill=(238, 240, 244))  # big dish
    d.ellipse([px - 17, py - 10, px + 3, py + 10], outline=(170, 176, 188), width=2)
    d.rectangle([px + 8, py - 4, px + 26, py + 5], fill=(196, 164, 92))     # bus + gold record
    d.ellipse([px + 27, py - 3, px + 35, py + 5], fill=(222, 184, 96))
    d.line([px + 14, py + 4, px + 52, py + 22], fill=(200, 205, 215), width=2)  # boom
    d.line([px + 10, py - 2, px - 6, py - 22], fill=(200, 205, 215), width=2)


def sc_nvidia(d, ox, oy):
    scene_base(d, ox, oy, (238, 247, 238))
    cx, cy = ox + 76, oy + 37  # chip
    rr(d, [cx - 26, cy - 22, cx + 26, cy + 22], 5, fill=(28, 34, 30))
    rr(d, [cx - 13, cy - 11, cx + 13, cy + 11], 3, fill=(118, 185, 0))
    for i in range(5):
        px = cx - 20 + i * 10
        d.rectangle([px, cy - 29, px + 4, cy - 22], fill=(90, 96, 100))
        d.rectangle([px, cy + 22, px + 4, cy + 29], fill=(90, 96, 100))
        py = cy - 16 + i * 8
        d.rectangle([cx - 33, py, cx - 26, py + 3], fill=(90, 96, 100))
        d.rectangle([cx + 26, py, cx + 33, py + 3], fill=(90, 96, 100))
    pts = [(ox + 128, oy + 58), (ox + 148, oy + 46), (ox + 164, oy + 50), (ox + 186, oy + 28)]
    d.line(pts, fill=(34, 150, 60), width=4, joint="curve")
    d.polygon([(ox + 186, oy + 28), (ox + 176, oy + 29), (ox + 183, oy + 37)], fill=(34, 150, 60))
    d.line([ox + 124, oy + 62, ox + 200, oy + 62], fill=(150, 155, 150), width=2)


def sc_deutsche(d, ox, oy):
    scene_base(d, ox, oy, (238, 241, 246))
    cx = ox + 66  # bank
    d.polygon([(cx - 40, oy + 22), (cx, oy + 6), (cx + 40, oy + 22)], fill=(120, 128, 148))
    d.rectangle([cx - 40, oy + 22, cx + 40, oy + 27], fill=(120, 128, 148))
    for i in range(4):
        px = cx - 32 + i * 19
        d.rectangle([px, oy + 27, px + 8, oy + 54], fill=(168, 176, 192))
    d.rectangle([cx - 42, oy + 54, cx + 42, oy + 60], fill=(120, 128, 148))
    d.rectangle([ox, oy + 62, ox + SW, oy + SH], fill=(196, 200, 208))
    rng = random.Random(3)  # leaked pages flying out
    for i in range(6):
        px = ox + 128 + rng.randint(0, 58)
        py = oy + 8 + rng.randint(0, 40)
        d.rectangle([px, py, px + 13, py + 17], fill=(255, 255, 255), outline=(150, 150, 155))
        d.line([px + 3, py + 5, px + 10, py + 5], fill=(170, 170, 175), width=1)
        d.line([px + 3, py + 9, px + 10, py + 9], fill=(170, 170, 175), width=1)


def sc_cop31(d, ox, oy):
    scene_base(d, ox, oy, (230, 244, 234))
    gx, gy, gr = ox + 62, oy + 37, 27  # globe
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(84, 148, 224))
    d.ellipse([gx - 16, gy - 18, gx - 2, gy - 6], fill=(94, 178, 110))
    d.ellipse([gx + 2, gy + 2, gx + 18, gy + 14], fill=(94, 178, 110))
    d.ellipse([gx - 20, gy + 8, gx - 8, gy + 18], fill=(94, 178, 110))
    tx = ox + 128  # thermometer
    d.rectangle([tx - 4, oy + 8, tx + 4, oy + 50], fill=(255, 255, 255), outline=(120, 120, 120))
    d.rectangle([tx - 2, oy + 18, tx + 2, oy + 50], fill=(224, 96, 50))
    d.ellipse([tx - 9, oy + 46, tx + 9, oy + 64], fill=(224, 96, 50))
    d.polygon([(ox + 168, oy + 44), (ox + 186, oy + 26), (ox + 190, oy + 46),
               (ox + 178, oy + 56)], fill=(64, 160, 90))  # leaf
    d.line([ox + 170, oy + 54, ox + 188, oy + 30], fill=(44, 120, 66), width=2)


def sc_gta(d, ox, oy):
    d.rectangle([ox, oy, ox + SW, oy + 30], fill=(43, 52, 96))
    d.rectangle([ox, oy + 30, ox + SW, oy + 52], fill=(146, 92, 128))
    d.rectangle([ox, oy + 52, ox + SW, oy + SH], fill=(232, 140, 120))
    rng = random.Random(11)
    for i in range(10):  # skyline
        bw = rng.randint(10, 20)
        bh = rng.randint(14, 34)
        bx = ox + i * 21
        d.rectangle([bx, oy + SH - bh, bx + bw, oy + SH], fill=(30, 30, 44))
    bx, by = ox + 66, oy + 10  # billboard with gamepad
    d.rectangle([bx, by, bx + 78, by + 34], fill=(250, 246, 235), outline=(30, 30, 44), width=2)
    d.rectangle([bx, by + 44, bx + 6, oy + SH], fill=(30, 30, 44))
    d.rectangle([bx + 72, by + 44, bx + 78, oy + SH], fill=(30, 30, 44))
    gx, gy = bx + 39, by + 17
    rr(d, [gx - 17, gy - 9, gx + 17, gy + 9], 8, fill=(40, 40, 56))
    d.line([gx - 11, gy, gx - 5, gy], fill=(240, 240, 240), width=3)
    d.line([gx - 8, gy - 3, gx - 8, gy + 3], fill=(240, 240, 240), width=3)
    d.ellipse([gx + 7, gy - 5, gx + 11, gy - 1], fill=(240, 120, 120))
    d.ellipse([gx + 11, gy + 1, gx + 15, gy + 5], fill=(120, 200, 240))


def sc_nations(d, ox, oy):
    for i in range(6):  # mown stripes
        col = (86, 168, 92) if i % 2 == 0 else (102, 182, 106)
        d.rectangle([ox + i * 36, oy, ox + (i + 1) * 36, oy + SH], fill=col)
    d.rectangle([ox + 168, oy + 8, ox + 204, oy + 52], outline=(255, 255, 255), width=3)  # goal
    d.line([ox + 168, oy + 8, ox + 168, oy + 52], fill=(255, 255, 255), width=3)
    bx, by = ox + 62, oy + 40  # ball
    d.ellipse([bx - 15, by - 15, bx + 15, by + 15], fill=(250, 250, 250), outline=(60, 60, 60), width=2)
    d.polygon([(bx - 4, by - 5), (bx + 4, by - 5), (bx + 6, by + 3), (bx, by + 7), (bx - 6, by + 3)],
              fill=(40, 40, 46))
    d.ellipse([ox + 20, oy + 10, ox + 34, oy + 24], fill=(250, 250, 250), outline=(60, 60, 60), width=1)


# ---------------- content ----------
# place, accent, emoji, headline, caption, scene
STAMPS = [
    ("SHENZHEN · CHINA", (179, 49, 42), "🤝", "THREE POWERS, ONE TABLE",
     "Xi hosts Putin on APEC's sidelines; on Thursday Trump joins them — the first US–China–Russia summit ever held.",
     sc_summit),
    ("QESHM STRAIT · IRAN", (184, 92, 14), "💥", "THE GULF ERUPTS AGAIN",
     "US jets strike Iran's Qeshm missile site; Tehran answers with drones on bases in Kuwait and Bahrain.",
     sc_qeshm),
    ("KERCH STRAIT · CRIMEA", (32, 80, 158), "🌉", "AN ARCH FALLS",
     "Ukraine's seven-stage attack drops a Kerch Bridge arch into the strait. Zelensky: “unprecedented.”",
     sc_kerch),
    ("ALASKA · USA", (32, 80, 158), "🗳️", "ALASKA FLIPS THE SENATE",
     "Peltola beats Sullivan in the last midterm race called — Democrats take the Senate 56–44.",
     sc_alaska),
    ("UNITED STATES", (179, 49, 42), "🦠", "MEASLES-FREE NO MORE",
     "After 26 years, America loses measles-elimination status: 5,400 cases and 10 deaths in 2026.",
     sc_measles),
    ("DR CONGO", TEAL, "🏥", "EBOLA'S YOUNGEST VICTIMS",
     "Cases pass 11,000 — and around Bunia and Beni, three of four infected under-fives do not survive.",
     sc_ebola),
    ("DEEP SPACE", (59, 63, 143), "🛰️", "ONE LIGHT-DAY OUT",
     "Voyager 1 crosses one light-day from Earth — 16 billion miles out; its signals now take a full day to reach home.",
     sc_voyager),
    ("SANTA CLARA · USA", (74, 124, 15), "💹", "NVIDIA BEATS; HUANG OUT",
     "A record quarter and a $130bn forecast — but the board rules out founder Jensen Huang's return as chief.",
     sc_nvidia),
    ("FRANKFURT · GERMANY", (91, 74, 138), "🏦", "15 MILLION FILES",
     "50 newsrooms get the leak, alleging blind eyes to fraud and financing for arms dealers.",
     sc_deutsche),
    ("ANTALYA · TÜRKİYE", TEAL, "🌍", "PARIS: A REALITY CHECK",
     "COP31 opens the second Global Stocktake — 21 issues deadlocked, and Friday's deadline looms.",
     sc_cop31),
    ("SYDNEY · AUSTRALIA", (184, 92, 14), "🎮", "GTA VI EVE",
     "Billboards from Tokyo to Sydney count down to launch day; New Zealand braces for 35 petabytes of downloads.",
     sc_gta),
    ("NATIONS LEAGUE · EUROPE", (46, 125, 50), "⚽", "SPAIN'S RUN ENDS AT 43",
     "England end Spain's 43-match unbeaten run, 3–2; Germany hit five past the Dutch; Norway, Portugal win thrillers.",
     sc_nations),
]

# number, emoji, lead, rest — every brief reported on Wed 18 Nov 2026
BRIEFS = [
    (13, "🚀", "YEMEN", "Houthi drones strike Saudi pipeline stations near Riyadh"),
    (14, "🌊", "ADEN", "Houthi forces close to 60 km from Yemen's port capital"),
    (15, "🏛️", "ISRAEL", "Knesset elects Kahana speaker 66–120; Netanyahu snubbed"),
    (16, "🕊️", "GAZA DEAL", "Trump's peace board: both sides failing their pledges"),
    (17, "❄️", "GAZA", "Tent camps face a fourth winter; the cold turns deadly"),
    (18, "🇬🇧", "WEST BANK", "UK sanctions settlement firms; Israel threatens reply"),
    (19, "🤝", "MANILA", "Trump hails a “very big” trade deal with the Philippines"),
    (20, "🚕", "WAYMO", "Driverless cars pulled off every US freeway after incidents"),
    (21, "📡", "OUTAGES", "America's failure wave reaches the NSA's secret network"),
    (22, "✈️", "SIBERIA", "Russian An-12 transport crashes; all 19 aboard are killed"),
    (23, "🚢", "FINLAND", "Ukrainian drones damage a Russian warship in the Gulf"),
    (24, "💣", "EUROPE", "8,000 bomb threats in a month hit schools and airports"),
    (25, "📈", "BRITAIN", "Inflation climbs to 3.6% as fuel prices bite households"),
    (26, "📉", "MARKETS", "Slide: DAX –2.1%, CAC –1.6%, S&P –1.0%, gold –2.3%"),
    (27, "🦠", "HOSPITALS", "Superbug Klebsiella resists even the newest antibiotics"),
    (28, "🎓", "SEOUL", "$75,000 bounties offered to catch AI exam cheats"),
    (29, "💧", "THAILAND", "Clean water rushed to villages poisoned by mine arsenic"),
    (30, "🎤", "COSTA RICA", "Journalist probing drug gangs is shot dead"),
    (31, "✝️", "PERU", "Pope Leo XIV pleads: “There is no need to hate each other”"),
    (32, "🇭🇹", "HAITI", "Crowds chant “Thank you, Bukele” to Salvadoran troops"),
    (33, "⚖️", "THE HAGUE", "Court rules Thursday on Myanmar genocide case"),
    (34, "🌴", "FIJI", "National disaster declared over El Niño drought"),
    (35, "🐸", "SULAWESI", "New flying frog wraps its eggs in gel, not foam"),
    (36, "🐒", "TANZANIA", "Chimps fish termites 143 miles further south than ever"),
    (37, "👣", "ANTARCTICA", "Even footprints can harm its rarest tiny ecosystems"),
    (38, "🗣️", "NEW ZEALAND", "Debate erupts: become Australia's seventh state?"),
]


def postmark(img, cx, cy):
    tile = Image.new("RGBA", (84, 84), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    col = (52, 64, 92, 205)
    td.ellipse([6, 6, 78, 78], outline=col, width=3)
    td.ellipse([13, 13, 71, 71], outline=col, width=1)
    f = font(SANS_B, 13)
    for i, line in enumerate(("18 NOV", "2026")):
        w_ = td.textlength(line, font=f)
        td.text((42 - w_ / 2, 27 + i * 15), line, font=f, fill=col)
    tile = tile.rotate(14, resample=Image.BICUBIC, expand=False)
    img.paste(tile, (int(cx - 42), int(cy - 42)), tile)


def draw_stamp(img, d, x, y, w, h, st):
    place, accent, emo, head, cap, scene = st
    d.rectangle([x, y, x + w, y + h], fill=STAMP_FACE)
    d.rectangle([x + 5, y + 5, x + w - 5, y + h - 5], outline=(216, 210, 192), width=1)
    # place line + denomination
    pf = fit_font(d, place, SANS_B, 13, 10, w - 70)
    d.text((x + 12, y + 8), place, font=pf, fill=accent)
    df = font(SANS_B, 11)
    d.text((x + w - 12 - tw(d, "1ST", df), y + 8), "1ST", font=df, fill=accent)
    # art
    scene(d, x + 10, y + 26)
    d.rectangle([x + 10, y + 26, x + 10 + SW, y + 26 + SH], outline=(190, 184, 164), width=1)
    # headline with emoji
    ew = paste_emoji(img, emo, x + 11, y + 105, 16)
    hf = fit_font(d, head, SANS_B, 16, 11, w - 24 - ew)
    d.text((x + 15 + ew, y + 104), head, font=hf, fill=INK)
    # caption
    cf = font(SANS, 11)
    for i, line in enumerate(wrap(d, cap, cf, w - 22, 3)):
        d.text((x + 11, y + 126 + i * 13), line, font=cf, fill=(58, 67, 86))
    # postmark over the art's top-right corner
    postmark(img, x + w - 34, y + 40)
    # perforations: paper-coloured punches along every edge
    r = 4
    for px in range(x + 2, x + w, 12):
        d.ellipse([px - r, y - r, px + r, y + r], fill=PAPER)
        d.ellipse([px - r, y + h - r, px + r, y + h + r], fill=PAPER)
    for py in range(y + 2, y + h, 12):
        d.ellipse([x - r, py - r, x + r, py + r], fill=PAPER)
        d.ellipse([x + w - r, py - r, x + w + r, py + r], fill=PAPER)


def airmail_border(d):
    band = 16
    cols = ((207, 53, 39), (39, 75, 159))
    k = 0
    for x in range(-30, W + 30, 46):
        c = cols[k % 2]
        k += 1
        d.polygon([(x, 0), (x + 23, 0), (x + 23 - 11, band), (x - 11, band)], fill=c)
        d.polygon([(x, H), (x + 23, H), (x + 23 - 11, H - band), (x - 11, H - band)], fill=c)
    k = 0
    for y in range(-30, H + 30, 46):
        c = cols[k % 2]
        k += 1
        d.polygon([(0, y), (0, y + 23), (band, y + 23 - 11), (band, y - 11)], fill=c)
        d.polygon([(W, y), (W, y + 23), (W - band, y + 23 - 11), (W - band, y - 11)], fill=c)


def check_layout():
    """Refuse to draw if any caption would truncate or any brief overflow."""
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    cf = font(SANS, 11)
    for st in STAMPS:
        lines = wrap(d0, st[4], cf, 210, 99)
        assert len(lines) <= 3, f"caption needs {len(lines)} lines: {st[3]}"
        assert " ".join(lines) == " ".join(st[4].split()), f"caption wraps lossy: {st[3]}"
    num_f, lead_f, body_f = font(SANS_B, 13), font(SANS_B, 13), font(SANS, 13)
    for (num, emo, lead, rest) in BRIEFS:
        w = (tw(d0, str(num), num_f) + 5 + emoji_img(emo, 13).width + 4
             + tw(d0, lead + " — ", lead_f) + tw(d0, rest, body_f))
        assert w <= 467, f"brief {num} is {w:.0f}px wide"


def main():
    check_layout()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    hf = font(SANS_B, 15)
    s = "P A R   A V I O N   ·   A I R   M A I L   ·   V I A   A É R E A"
    d.text(((W - tw(d, s, hf)) / 2, 28), s, font=hf, fill=(39, 75, 159))
    tf = font(SERIF_B, 57)
    t = "THE WORLD BY POST"
    d.text(((W - tw(d, t, tf)) / 2, 48), t, font=tf, fill=NAVY)
    d.line([30, 118, 994, 118], fill=INK, width=3)
    d.line([30, 124, 994, 124], fill=INK, width=1)
    df = font(SANS_B, 27)
    s = "WEDNESDAY · 18 NOVEMBER 2026"
    d.text(((W - tw(d, s, df)) / 2, 132), s, font=df, fill=RED)
    sf = font(SANS_B, 15)
    s = "38 STORIES · 8 CONTINENTS · ONE DAY — EVERY STORY FIRST REPORTED ON WEDNESDAY"
    d.text(((W - tw(d, s, sf)) / 2, 166), s, font=sf, fill=INK)

    # ---- stamps: 4 x 3 ----
    sw_, sh_, gx, gy = 232, 170, 12, 10
    x0, y0 = 30, 192
    for i, st in enumerate(STAMPS):
        cx = x0 + (i % 4) * (sw_ + gx)
        cy = y0 + (i // 4) * (sh_ + gy)
        draw_stamp(img, d, cx, cy, sw_, sh_, st)

    # ---- postcard briefs ----
    by = 736
    d.rectangle([30, by, 994, by + 28], fill=TEAL)
    ew = paste_emoji(img, "✉️", 42, by + 5, 18)
    bf = font(SANS_B, 17)
    d.text((48 + ew, by + 5), "POSTCARD BRIEFS — THE REST OF WEDNESDAY, IN SHORT",
           font=bf, fill=(255, 255, 255))
    num_f = font(SANS_B, 13)
    lead_f = font(SANS_B, 13)
    body_f = font(SANS, 13)
    rows_y = by + 38
    for j, (num, emo, lead, rest) in enumerate(BRIEFS):
        col = 0 if j < 13 else 1
        row = j if j < 13 else j - 13
        x = 30 if col == 0 else 527
        y = rows_y + row * 16
        maxw = 467
        ns = f"{num}"
        d.text((x, y), ns, font=num_f, fill=RED)
        cx = x + tw(d, ns, num_f) + 5
        cx += paste_emoji(img, emo, cx, y + 1, 13) + 4
        lt = lead + " — "
        d.text((cx, y), lt, font=lead_f, fill=INK)
        cx += tw(d, lt, lead_f)
        d.text((cx, y), rest, font=body_f, fill=(58, 67, 86))

    # ---- footer ----
    d.line([30, 982, 994, 982], fill=INK, width=1)
    ff = font(SANS, 11)
    s = ("SOURCES: REUTERS · BBC · AP · AFP · UN NEWS · NASA/JPL · THE HINDU · "
         "STRAITS TIMES · MERCOPRESS · PEOPLE · PHYS.ORG — DRAWN BY PROGRAM, NO PHOTOS")
    f2 = fit_font(d, s, SANS, 11, 9, 964)
    d.text(((W - tw(d, s, f2)) / 2, 990), s, font=f2, fill=GREY)

    airmail_border(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
