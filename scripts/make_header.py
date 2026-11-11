"""Generate the README header (light + dark) as self-contained SVGs.

Text is converted to outlines so it looks the same on every machine.
Fonts: Inter and JetBrains Mono (SIL OFL, see scripts/fonts/).

    pip install fonttools
    python3 scripts/make_header.py
"""
import math
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
FONTS = {
    "sans": TTFont(ROOT / "fonts/inter-latin-400-normal.woff"),
    "sans-bold": TTFont(ROOT / "fonts/inter-latin-600-normal.woff"),
    "mono": TTFont(ROOT / "fonts/jetbrains-mono-latin-400-normal.woff"),
}

NAME = "toixaydungkhacbiet"
ROLE = "AI ENGINEER"
TAGLINE = "I can make it happen."

THEMES = {
    "dark": dict(bg="#0E0F11", fg="#ECEDEE", muted="#7D828A", faint="#24272C", accent="#7AA2F7"),
    "light": dict(bg="#FAFAF9", fg="#16181B", muted="#6B7078", faint="#E6E7E9", accent="#3B6FE0"),
}


def outline(s, font, size, x, y, tracking=0.0):
    """Return (svg path d, advance width) for text set at baseline y."""
    f = FONTS[font]
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    scale = size / f["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cx = 0.0
    for ch in s:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + cx, y))
        gs[g].draw(tp)
        cx += gs[g].width * scale + tracking
    return pen.getCommands(), cx - tracking


def loss_curve(x0, y0, w, h, n=60):
    """A smooth, slightly noisy decaying curve — a training-loss plot."""
    pts = []
    for i in range(n + 1):
        t = i / n
        v = math.exp(-4.2 * t) * 0.92 + 0.06 + 0.018 * math.sin(i * 1.7) * (1 - t)
        pts.append((x0 + t * w, y0 + (1 - v) * h))
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    return d, pts[-1]


def header(theme):
    c = THEMES[theme]
    W, H = 1200, 320
    X = 72
    role_d, role_w = outline(ROLE, "mono", 15, X + 20, 108, tracking=3.2)
    name_d, name_w = outline(NAME, "sans-bold", 76, X - 4, 196, tracking=-2.2)
    tag_d, tag_w = outline(TAGLINE, "sans", 28, X, 252)

    # right-hand plot
    px, py, pw, ph = 800, 92, 320, 150
    curve, end = loss_curve(px, py, pw, ph)
    grid = "".join(
        f'<circle cx="{px + i * pw / 8:.1f}" cy="{py + j * ph / 4:.1f}" r="1.4" fill="{c["faint"]}"/>'
        for i in range(9) for j in range(5)
    )
    caption_d, _ = outline("train/loss", "mono", 13, px, py + ph + 34)
    caret_x = X + tag_w + 6

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{NAME} — AI engineer. {TAGLINE}</title>
<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>
<circle cx="{X + 4}" cy="102" r="4" fill="{c["accent"]}"/>
<path d="{role_d}" fill="{c["muted"]}"/>
<path d="{name_d}" fill="{c["fg"]}"/>
<path d="{tag_d}" fill="{c["muted"]}"/>
<rect x="{caret_x:.1f}" y="228" width="2.5" height="30" fill="{c["accent"]}">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
{grid}
<path d="{curve}" fill="none" stroke="{c["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
      pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
  <animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.4s" begin="0.3s" fill="freeze" calcMode="spline" keySplines=".3 0 .2 1" keyTimes="0;1"/>
</path>
<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="4" fill="{c["accent"]}" opacity="0">
  <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="2.7s" fill="freeze"/>
</circle>
<path d="{caption_d}" fill="{c["muted"]}"/>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for t in THEMES:
        (OUT / f"header-{t}.svg").write_text(header(t))
    print("written to", OUT)
