#!/usr/bin/env python3
"""Build the Bamzal favicon as a dark rounded tile with a white "B" mark.

Why a tile (not a transparent white mark + media query): the browser tab
color is NOT exposed to the page, and an incognito window forces a dark tab
chrome regardless of prefers-color-scheme. A solid tile makes the icon
visible on ANY tab color — incognito-black, light, dark, bookmarks.

Source of truth: bamzal-favicon-a-512.png (dark "B" mark on transparent bg).
The diagonal slash is transparent and shows the tile colour through it.
"""
import base64
import io
from PIL import Image, ImageDraw

SRC = "bamzal-favicon-a-512.png"
SIZES = [16, 32, 48, 180, 512]
INK = (13, 17, 28, 255)      # deep navy-ink tile
MARK_SCALE = 0.74            # white mark size relative to the tile
RADIUS_FRAC = 0.22           # rounded-corner radius relative to the tile


def whiten(img: Image.Image) -> Image.Image:
    """Recolor every visible pixel to pure white, preserving alpha."""
    img = img.convert("RGBA")
    out = [(255, 255, 255, a) for (_r, _g, _b, a) in img.getdata()]
    w = Image.new("RGBA", img.size)
    w.putdata(out)
    return w


def tile(size: int, white_mark_full: Image.Image) -> Image.Image:
    """Dark rounded tile with the centered white mark."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=round(size * RADIUS_FRAC), fill=255
    )
    plate = Image.new("RGBA", (size, size), INK)
    canvas.paste(plate, (0, 0), mask)

    m = round(size * MARK_SCALE)
    mark = white_mark_full.resize((m, m), Image.LANCZOS)
    off = (size - m) // 2
    canvas.alpha_composite(mark, (off, off))
    return canvas


base = Image.open(SRC).convert("RGBA")
white_full = whiten(base)

tiles = {s: tile(s, white_full) for s in SIZES}
for s, im in tiles.items():
    im.save(f"bamzal-favicon-tile-{s}.png")

tiles[180].save("bamzal-favicon-tile-apple.png")
tiles[48].save(
    "bamzal-favicon-tile.ico", sizes=[(16, 16), (32, 32), (48, 48)]
)

# Static SVG favicon = the same tile (embed the 180 tile, no media query).
buf = io.BytesIO()
tiles[180].save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">'
    f'<image width="180" height="180" href="data:image/png;base64,{b64}"/>'
    "</svg>"
)
with open("bamzal-favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("tiles:", [f"bamzal-favicon-tile-{s}.png" for s in SIZES])
print("svg bytes:", len(svg.encode("utf-8")))
print("done")
