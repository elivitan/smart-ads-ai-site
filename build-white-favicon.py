#!/usr/bin/env python3
"""Generate a white version of the Bamzal favicon mark (for dark browser tabs)
and an adaptive SVG favicon that shows white on dark mode, dark on light mode.

Source of truth: bamzal-favicon-a-512.png (dark "B" mark on transparent bg).
The diagonal slash is transparent and is preserved in every output.
"""
import base64
from PIL import Image

SRC = "bamzal-favicon-a-512.png"
SIZES = [16, 32, 48, 180, 512]


def whiten(img: Image.Image) -> Image.Image:
    """Recolor every visible pixel to pure white, preserving the alpha channel
    (keeps antialiased edges smooth and the transparent slash intact)."""
    img = img.convert("RGBA")
    out = [(255, 255, 255, a) for (_r, _g, _b, a) in img.getdata()]
    w = Image.new("RGBA", img.size)
    w.putdata(out)
    return w


base = Image.open(SRC).convert("RGBA")
white_full = whiten(base)

# --- white PNGs at every size ---
for s in SIZES:
    white_full.resize((s, s), Image.LANCZOS).save(f"bamzal-favicon-w-{s}.png")

# white apple-touch (180, opaque-friendly but kept transparent like the original set)
white_full.resize((180, 180), Image.LANCZOS).save("bamzal-favicon-w-apple.png")

# white .ico (multi-size)
white_full.resize((48, 48), Image.LANCZOS).save(
    "bamzal-favicon-w.ico", sizes=[(16, 16), (32, 32), (48, 48)]
)

# --- adaptive SVG favicon: embed dark-180 + white-180, toggle by color-scheme ---
def b64_180(img: Image.Image) -> str:
    import io
    buf = io.BytesIO()
    img.resize((180, 180), Image.LANCZOS).save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

dark_b64 = b64_180(base)
white_b64 = b64_180(white_full)

svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">'
    "<style>"
    ".w{display:none}"
    "@media (prefers-color-scheme:dark){.d{display:none}.w{display:inline}}"
    "</style>"
    f'<image class="d" width="180" height="180" href="data:image/png;base64,{dark_b64}"/>'
    f'<image class="w" width="180" height="180" href="data:image/png;base64,{white_b64}"/>'
    "</svg>"
)
with open("bamzal-favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("white PNGs:", [f"bamzal-favicon-w-{s}.png" for s in SIZES])
print("svg bytes:", len(svg.encode("utf-8")))
print("done")
