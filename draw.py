#!/usr/bin/env python3
"""Render news.png: a newspaper front page for Monday 23 November 2026.

Deterministic build-time script. Uses Pillow (DejaVu fonts) and draws only
flat shapes plus wrapped text. No network, no clock, no randomness.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
PANEL = (255, 255, 255)
GREY = (90, 90, 90)
MARGIN = 36

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def draw_text_block(draw, x, y, width, lines, fnt, fill=INK, leading=4):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def panel(draw, box, accent):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL, outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 7], fill=accent)
    return (x0 + 14, y0 + 18, x1 - 14, y1 - 12)


def kicker_head_body(draw, box, accent, kicker, headline, body, head_size,
                     body_size, illo):
    x0, y0, x1, y1 = panel(draw, box, accent)
    illo_top = y1 - 78
    draw.text((x0, y0), kicker, font=SANS_B(13), fill=accent)
    y = y0 + 22
    y = draw_text_block(draw, x0, y, x1 - x0,
                        wrap(draw, headline, SANS_B(head_size), x1 - x0),
                        SANS_B(head_size), leading=3)
    y += 4
    draw_text_block(draw, x0, y, x1 - x0,
                    wrap(draw, body, SANS(body_size), x1 - x0),
                    SANS(body_size), leading=3)
    illo(draw, x0, illo_top, x1, y1)


# ---- flat illustrations (simple shapes only) -----------------------------

def sea(draw, x0, y0, x1, y1, water):
    draw.rectangle([x0, y0 + 34, x1, y1], fill=water)
    for wx in range(x0, x1, 46):
        # clamp each wave arc to the panel so no stroke spills past its edge
        rx = min(wx + 44, x1)
        if rx - wx < 8:
            continue
        draw.arc([wx, y0 + 28, rx, y0 + 52], 0, 180, fill=INK, width=2)
        draw.arc([wx + 10, y0 + 52, min(wx + 54, x1), y0 + 74], 0, 180,
                 fill=INK, width=2)


def illo_war(draw, x0, y0, x1, y1):
    sea(draw, x0, y0, x1, y1, (168, 205, 225))
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 90, y0 + 30), (cx + 90, y0 + 30), (cx + 70, y0 + 52),
                  (cx - 70, y0 + 52)], fill=(60, 60, 60))
    draw.rectangle([cx - 30, y0 + 6, cx + 10, y0 + 30], fill=(90, 90, 90))
    draw.line([cx - 10, y0 + 6, cx - 10, y0 - 6], fill=INK, width=3)
    draw.polygon([(cx - 10, y0 - 6), (cx + 12, y0 - 1), (cx - 10, y0 + 4)],
                 fill=(176, 58, 46))
    # small drone above the ship
    dx, dy = x1 - 70, y0 + 6
    draw.ellipse([dx - 12, dy - 6, dx + 12, dy + 6], fill=INK)
    draw.line([dx - 26, dy - 10, dx + 26, dy - 10], fill=INK, width=3)
    draw.line([dx - 26, dy + 10, dx + 26, dy + 10], fill=INK, width=3)
    draw.line([dx, dy + 6, dx, dy + 16], fill=INK, width=2)


def illo_globe(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
    r = 32
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 205, 225),
                 outline=INK, width=2)
    draw.ellipse([cx - 22, cy - 18, cx - 2, cy + 2], fill=(46, 125, 91))
    draw.ellipse([cx + 4, cy + 4, cx + 22, cy + 22], fill=(46, 125, 91))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=INK, width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=INK, width=1)
    draw.line([x0 + 8, y1 - 6, x1 - 8, y1 - 6], fill=(46, 125, 91), width=4)


def illo_dome(draw, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    draw.rectangle([cx - 52, y1 - 26, cx + 52, y1 - 6], fill=(220, 220, 220),
                   outline=INK, width=2)
    for i in range(-2, 3):
        draw.rectangle([cx + i * 20 - 4, y1 - 52, cx + i * 20 + 4, y1 - 26],
                       fill=PANEL, outline=INK, width=1)
    draw.rectangle([cx - 56, y1 - 52, cx + 56, y1 - 46], fill=(31, 78, 121))
    draw.pieslice([cx - 26, y1 - 78, cx + 26, y1 - 26], 180, 360,
                  fill=(31, 78, 121), outline=INK, width=2)
    draw.line([cx, y1 - 78, cx, y1 - 92], fill=INK, width=2)
    draw.polygon([(cx, y1 - 92), (cx + 14, y1 - 88), (cx, y1 - 84)],
                 fill=(176, 58, 46))


def illo_plane(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.ellipse([cx - 62, cy - 12, cx + 62, cy + 12], fill=(31, 78, 121))
    draw.polygon([(cx - 10, cy), (cx + 26, cy - 34), (cx + 44, cy - 34),
                  (cx + 20, cy)], fill=(31, 78, 121))
    draw.polygon([(cx - 10, cy), (cx + 26, cy + 34), (cx + 44, cy + 34),
                  (cx + 20, cy)], fill=(31, 78, 121))
    draw.polygon([(cx + 44, cy - 10), (cx + 62, cy - 26), (cx + 62, cy - 8),
                  (cx + 50, cy)], fill=(31, 78, 121))
    draw.ellipse([cx - 58, cy - 5, cx - 46, cy + 5], fill=PANEL)
    # penny coin
    draw.ellipse([x1 - 34, y1 - 30, x1 - 6, y1 - 2], fill=(192, 122, 26),
                 outline=INK, width=2)
    draw.text((x1 - 27, y1 - 28), "1c", font=SANS_B(13), fill=INK)


def illo_drone(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    draw.rectangle([cx - 26, cy - 8, cx + 26, cy + 8], fill=(90, 90, 90),
                   outline=INK, width=2)
    draw.ellipse([cx - 6, cy - 4, cx + 6, cy + 4], fill=(176, 58, 46))
    for sx in (-1, 1):
        draw.line([cx + sx * 26, cy, cx + sx * 48, cy - 12], fill=INK,
                  width=2)
        draw.line([cx + sx * 34, cy - 18, cx + sx * 62, cy - 18], fill=INK,
                  width=3)
    draw.rectangle([x0 + 10, y1 - 12, x1 - 10, y1 - 6], fill=(168, 205, 225))
    draw.arc([x0 + 20, y1 - 22, x0 + 60, y1 - 2], 0, 180, fill=INK, width=2)


def illo_chip(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=(46, 107, 122),
                   outline=INK, width=2)
    draw.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(247, 242, 231),
                   outline=INK, width=2)
    for i in range(-2, 3):
        draw.line([cx + i * 12, cy - 42, cx + i * 12, cy - 30], fill=INK,
                  width=2)
        draw.line([cx + i * 12, cy + 30, cx + i * 12, cy + 42], fill=INK,
                  width=2)
        draw.line([cx - 42, cy + i * 12, cx - 30, cy + i * 12], fill=INK,
                  width=2)
        draw.line([cx + 30, cy + i * 12, cx + 42, cy + i * 12], fill=INK,
                  width=2)
    # rising bars for exports
    for i, hgt in enumerate((14, 22, 32)):
        bx = x1 - 66 + i * 18
        draw.rectangle([bx, y1 - 8 - hgt, bx + 12, y1 - 8],
                       fill=(46, 107, 122))


def illo_cargo(draw, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 78, y0 + 34), (cx + 78, y0 + 34), (cx + 60, y0 + 58),
                  (cx - 60, y0 + 58)], fill=(60, 60, 60))
    for r, cols in enumerate(((176, 58, 46), (192, 122, 26))):
        for c in range(3):
            draw.rectangle([cx - 66 + c * 34, y0 + 2 + r * 16,
                            cx - 36 + c * 34, y0 + 16 + r * 16],
                           fill=cols, outline=INK, width=1)
    draw.rectangle([x0 + 6, y1 - 10, x1 - 6, y1 - 4], fill=(168, 205, 225))
    draw.polygon([(x1 - 34, y0 + 2), (x1 - 14, y0 + 2), (x1 - 24, y0 + 20)],
                 fill=(192, 122, 26), outline=INK)
    draw.text((x1 - 27, y0 + 6), "!", font=SANS_B(11), fill=INK)


# ---- page ----------------------------------------------------------------

STORIES = [
    dict(kicker="WAR AT SEA", accent=(176, 58, 46),
         headline="Ukrainian drones strike Russian ships",
         body="A naval drone badly damaged the corvette Merkury off Libya; "
              "the cargo ship MV Angara was also hit.",
         illo=illo_war, head=30, body_size=16, lead=True),
    dict(kicker="CLIMATE", accent=(46, 125, 91),
         headline="Climate summit ends without deal",
         body="COP31 in Antalya closes after two weeks with no agreement "
              "on fossil fuels or climate finance.",
         illo=illo_globe, head=21, body_size=14),
    dict(kicker="US POLITICS", accent=(31, 78, 121),
         headline="Democrats clinch record House majority",
         body="A North Carolina recount confirms Chuck Hubbard's win: "
              "258 seats, the largest in over 30 years.",
         illo=illo_dome, head=21, body_size=14),
    dict(kicker="TRAVEL & MONEY", accent=(192, 122, 26),
         headline="Delta outage delays 1,600 flights",
         body="A systems failure snarls Thanksgiving travel week; Trump "
              "also signs the act ending the penny.",
         illo=illo_plane, head=21, body_size=14),
    dict(kicker="GULF TENSIONS", accent=(106, 61, 154),
         headline="Iran says it downed US drone",
         body="Tehran claims an MQ-9A Reaper shot down over the Strait of "
              "Hormuz; two tankers hit; Bahrain blames Iran.",
         illo=illo_drone, head=21, body_size=14),
    dict(kicker="ECONOMY", accent=(46, 107, 122),
         headline="South Korea exports pass $1 trillion",
         body="Annual exports top $1 trillion for the first time, driven "
              "by AI chip demand — only the fourth ever.",
         illo=illo_chip, head=21, body_size=14),
    dict(kicker="MARITIME SECURITY", accent=(138, 90, 43),
         headline="Indonesia seizes ship with rocket chemical",
         body="Navy stops a China-to-Bangladesh vessel carrying 405 tonnes "
              "of sodium perchlorate.",
         illo=illo_cargo, head=21, body_size=14),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN ONE PAGE"
    tf = SERIF_B(56)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 44), title, font=tf, fill=INK)
    draw.rectangle([MARGIN, 116, W - MARGIN, 119], fill=INK)
    sub = "MONDAY 23 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE"
    sf = SANS_B(21)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 128), sub, font=sf, fill=INK)
    draw.rectangle([MARGIN, 160, W - MARGIN, 163], fill=INK)

    lead = STORIES[0]
    kicker_head_body(draw, (MARGIN, 176, W - MARGIN, 436), lead["accent"],
                     lead["kicker"], lead["headline"], lead["body"],
                     lead["head"], lead["body_size"], lead["illo"])

    xs = [MARGIN, 357, 678]
    ws = [311, 311, 310]
    for row, y0 in enumerate((450, 714)):
        for col in range(3):
            s = STORIES[1 + row * 3 + col]
            kicker_head_body(draw,
                             (xs[col], y0, xs[col] + ws[col], y0 + 250),
                             s["accent"], s["kicker"], s["headline"],
                             s["body"], s["head"], s["body_size"], s["illo"])

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
