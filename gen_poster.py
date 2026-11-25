#!/usr/bin/env python3
"""Generate the Spotlight poster for @crisxai5 (1080x1080, original artwork).

Dark navy editorial poster:
  - dark navy background
  - cyan / violet glows
  - faint grid (data-ledger texture)
  - neural-net nodes + glowing lines
  - rising candlesticks
  - large legible @crisxai5 headline + subtitle

All artwork is drawn from scratch (no image assets). Glows are composited on
top of the finished artwork so the content and the glows share one canvas.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (8, 10, 30)
CYAN = (86, 234, 244)
VIOLET = (180, 120, 255)
WHITE = (238, 244, 255)
GREEN = (56, 230, 120)
RED = (255, 88, 88)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_glow(color, center, radius, intensity=0.10):
    """Build an RGBA radial glow layer (no canvas attached)."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(int(radius), 0, -8):
        a = int(255 * intensity * (1 - r / radius) ** 2.2)
        gd.ellipse(
            [center[0] - r, center[1] - r, center[0] + r, center[1] + r],
            fill=(color[0], color[1], color[2], a),
        )
    return glow


def draw_grid(draw, color=(130, 150, 255, 24)):
    """Faint data-ledger grid, drawn under the artwork."""
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=color, width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=color, width=1)


def draw_candlestick(draw, x, y, w, color):
    """Rising candlestick: green up, red down. x = center, y = top of body."""
    body_h = 26
    draw.rectangle(
        [x - w / 2, y, x + w / 2, y + body_h], fill=color, outline=(255, 255, 255, 40)
    )
    draw.line([(x, y), (x, y + body_h)], fill=(255, 255, 255, 60), width=2)


def main():
    canvas = Image.new("RGBA", (W, H), NAVY)
    d = ImageDraw.Draw(canvas)

    # 1) faint grid
    draw_grid(d)

    # 2) neural-net nodes and glowing lines
    cx, cy = 540, 430
    nodes = [
        (cx - 150, cy - 130),
        (cx - 60, cy - 180),
        (cx + 90, cy - 120),
        (cx - 120, cy + 90),
        (cx + 60, cy + 130),
        (cx + 150, cy - 10),
        (cx, cy + 160),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 6), (6, 5), (5, 1),
        (3, 6), (0, 4), (1, 6), (3, 5),
    ]
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        d.line([(x1, y1), (x2, y2)], fill=(150, 200, 255, 70), width=2)
    for i, (x, y) in enumerate(nodes):
        col = CYAN if i % 2 == 0 else VIOLET
        d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col + (255,), outline=WHITE + (255,))

    # 3) rising candlesticks (right side)
    base_x = 860
    levels = [370, 340, 312, 288, 262, 240]
    for i, y in enumerate(levels):
        up = i % 2 == 0
        col = GREEN if up else RED
        draw_candlestick(d, base_x + i * 36, y, 22, col)

    # 4) headline @crisxai5 with cyan halo
    fb = ImageFont.truetype(FONT_BOLD, 168)
    txt = "@crisxai5"
    bbox = d.textbbox((0, 0), txt, font=fb)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    for ox in range(-4, 5):
        for oy in range(-4, 5):
            if ox == 0 and oy == 0:
                continue
            d.text((cx - tw / 2 + ox, 190 - th / 2 + oy), txt, font=fb, fill=(86, 234, 244, 60))
    d.text((cx - tw / 2, 190 - th / 2), txt, font=fb, fill=WHITE)

    # 5) subtitle
    fr = ImageFont.truetype(FONT_REG, 46)
    sub = "AI AGENTS  /  CRYPTO INSIGHTS  /  WEB3"
    sbox = d.textbbox((0, 0), sub, font=fr)
    sw = sbox[2] - sbox[0]
    d.text((cx - sw / 2, 968 - 26), sub, font=fr, fill=WHITE)

    # 6) ambient glows composited on top of the finished artwork
    cyan_glow = make_glow(CYAN, (300, 300), 460, 0.10)
    violet_glow = make_glow(VIOLET, (840, 640), 520, 0.12)
    canvas = Image.alpha_composite(canvas, cyan_glow)
    canvas = Image.alpha_composite(canvas, violet_glow)

    out = canvas.convert("RGB")
    out.save("poster.png")
    print("poster.png written: %dx%d" % (out.width, out.height))


if __name__ == "__main__":
    main()
