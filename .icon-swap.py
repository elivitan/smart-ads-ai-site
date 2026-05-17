"""Replace emoji icons with monoline SVG (Lucide-style) for a more enterprise look.

Run from this folder:
    python .icon-swap.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Lucide-style SVGs: 24x24, fill=none, stroke=currentColor, stroke-width=1.5.
# Wrapper class .icon controls size (sets to 20px / 28px / 40px by context).
def svg(paths: str, w: str = "20") -> str:
    return (
        f'<svg class="icon" width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{paths}</svg>'
    )

# Each entry: emoji -> Lucide-style SVG path body
ICONS = {
    "🤖": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M12 2v6M9 13v2M15 13v2M8 8h8"/>',  # bot
    "📘": '<path d="M18 2H9a3 3 0 0 0-3 3v14a3 3 0 0 1 3-3h9z"/><path d="M6 19a3 3 0 0 0 3 3h9V16"/>',  # book/Meta proxy
    "🎵": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',  # music
    "📌": '<path d="M12 17v5"/><path d="M9 10.76V6a1 1 0 0 1 .553-.894l1.224-.612a3 3 0 0 1 2.446 0l1.224.612A1 1 0 0 1 15 6v4.76l1.553 1.659a1 1 0 0 1-.733 1.681H8.18a1 1 0 0 1-.733-1.681z"/>',  # pin
    "🔎": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',  # search
    "🔒": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',  # lock
    "🔐": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="16" r="1"/>',  # lock-keyhole
    "⚡": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',  # zap
    "🛡": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',  # shield-check
    "🎯": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',  # target
    "📊": '<path d="M3 3v18h18"/><path d="M7 16V8M12 16V5M17 16v-6"/>',  # bar-chart
    "📢": '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 5V5L6 10H4a1 1 0 0 0-1 1z"/><path d="M15 8a5 5 0 0 1 0 8"/><path d="M18 5a9 9 0 0 1 0 14"/>',  # megaphone
    "🔌": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 1 1-12 0z"/><path d="M12 18v4"/>',  # plug
    "🛍": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',  # shopping-bag
    "🗄": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v6c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 11v6c0 1.7 4 3 9 3s9-1.3 9-3v-6"/>',  # database
    "📡": '<path d="m4.9 16.1 14.2-14.2"/><path d="M9 22 22 9"/><path d="M2 15 15 2"/><path d="M4 4l2 2"/><path d="m13 13 7 7"/>',  # satellite
    "🔄": '<path d="M21 12a9 9 0 0 0-15.5-6.4L2 9"/><path d="M2 4v5h5"/><path d="M3 12a9 9 0 0 0 15.5 6.4L22 15"/><path d="M22 20v-5h-5"/>',  # refresh
    "📱": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',  # smartphone
    "🌐": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',  # globe
    "🚀": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',  # rocket
    "📧": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/>',  # mail
    "⚖": '<path d="M16 16h6l-3-7-3 7zM2 16h6l-3-7-3 7zM7 21h10M12 3v18M3 7h18"/>',  # scale
    "🤝": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="M21 3 12 12"/><path d="M3.29 8.71a3 3 0 0 0-.6 3.4l5.59 5.59"/>',  # handshake
    "🕵": '<circle cx="10" cy="8" r="5"/><path d="M2 21l8-13 8 13"/><circle cx="18" cy="18" r="3"/>',  # detective
    "📍": '<path d="M20 10c0 7-8 12-8 12s-8-5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',  # map-pin
    "🏪": '<path d="M3 9V21h18V9"/><path d="M2 9l3-6h14l3 6"/><path d="M9 21v-6h6v6"/>',  # store
    "👤": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',  # user
    "✓": '<path d="M5 12l5 5 9-11"/>',  # check
    "💎": '<path d="M2.5 9 6 3h12l3.5 6L12 22z"/><path d="M2.5 9h19"/><path d="m6 3 6 6 6-6M12 9v13"/>',  # gem
    "🎨": '<circle cx="12" cy="12" r="10"/><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.4-.4-.4-.6-.9-.6-1.4 0-1.1.9-2 2-2h2.5c2.8 0 5-2.2 5-5C22 5.6 17.5 2 12 2z"/>',  # palette
    "✅": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',  # check-circle
    "❌": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/>',  # x-circle
    "📈": '<path d="M3 3v18h18"/><path d="m7 14 4-4 4 4 5-5"/>',  # trending-up
    "🧠": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>',  # brain
}

# Special: brand X — replace 𝕏 (U+1D54F) with a tasteful X glyph
X_GLYPH = svg('<path d="M3 3l18 18M21 3 3 21"/>')


def main() -> None:
    # Patch shared.css to define .icon styling
    css_path = HERE / "shared.css"
    css_text = css_path.read_text(encoding="utf-8")
    if ".icon{" not in css_text and ".icon {" not in css_text:
        css_text += (
            "\n/* ---- ICONS (monoline, currentColor) ---- */\n"
            ".icon{display:inline-block;vertical-align:-3px;flex-shrink:0;}\n"
            ".tech-item h4 .icon,.cap-content h3 .icon{margin-right:8px;color:var(--accent);}\n"
            ".flow-icon .icon{color:var(--accent);}\n"
            ".flow-icon{background:var(--accent-light);border-radius:50%;width:56px;height:56px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px;}\n"
        )
        css_path.write_text(css_text, encoding="utf-8")
        print(f"  updated shared.css (added .icon styles)")

    # Sweep html files
    for html in sorted(HERE.glob("*.html")):
        text = html.read_text(encoding="utf-8")
        before = text
        for emoji, paths in ICONS.items():
            # Use 28px for flow-icon containers (large), 20px elsewhere
            small = svg(paths, "20")
            large = svg(paths, "28")
            # Detect emoji inside a flow-icon container — render larger
            text = re.sub(
                rf'(<div class="flow-icon">)\s*{re.escape(emoji)}\s*(</div>)',
                lambda m: m.group(1) + large + m.group(2),
                text,
            )
            text = text.replace(emoji, small)
        # X glyph
        text = text.replace("𝕏", X_GLYPH)
        if text != before:
            html.write_text(text, encoding="utf-8")
            n = sum(before.count(e) for e in ICONS) + before.count("𝕏")
            print(f"  {html.name}: swapped {n} emoji")

    print("Done.")


if __name__ == "__main__":
    main()
