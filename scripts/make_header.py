"""Generate the README header (light + dark) as self-contained SVGs.

The name types itself, holds, deletes and moves on to the next alias,
like someone typing at a keyboard. Pure SVG/SMIL, no JavaScript, so it
animates inside a GitHub README. Text is converted to outlines so it
looks the same on every machine. Fonts: Inter (SIL OFL, scripts/fonts/).

    pip install fonttools
    python3 scripts/make_header.py
"""
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
FONTS = {
    "sans": TTFont(ROOT / "fonts/inter-latin-400-normal.woff"),
    "sans-bold": TTFont(ROOT / "fonts/inter-latin-600-normal.woff"),
}

ALIASES = ["Toixaydungkhacbiet", "PTVK", "IBuiltDifferent", "KhangTran"]
TAGLINE = "I can make it happen."

TYPE, DELETE, HOLD, GAP = 0.11, 0.045, 1.8, 0.45  # seconds

THEMES = {
    "dark": dict(bg="#0E0F11", fg="#ECEDEE", muted="#7D828A", accent="#7AA2F7"),
    "light": dict(bg="#FAFAF9", fg="#16181B", muted="#6B7078", accent="#3B6FE0"),
}


def glyphs(s, font, size, x, y, tracking=0.0):
    """Yield (path d, x after the glyph) for each character."""
    f = FONTS[font]
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    scale = size / f["head"].unitsPerEm
    cx = x
    for ch in s:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, cx, y)))
        cx += gs[g].width * scale + tracking
        yield pen.getCommands(), cx


def typing(c, X, baseline, size):
    # timeline: (alias, type_start, delete_start, end)
    t, plan = GAP, []
    for a in ALIASES:
        typed = t + len(a) * TYPE
        dele = typed + HOLD
        end = dele + len(a) * DELETE
        plan.append((a, t, dele, end))
        t = end + GAP
    T = t
    f = lambda s: f"{s / T:.5f}"

    out, cursor = [], [(0.0, X)]
    for a, start, dele, _ in plan:
        gl = list(glyphs(a, "sans-bold", size, X, baseline, tracking=-1.8))
        n = len(gl)
        for i, (d, xa) in enumerate(gl):
            on = start + (i + 1) * TYPE
            off = dele + (n - i) * DELETE
            out.append(
                f'<path d="{d}" fill="{c["fg"]}" opacity="0"><animate attributeName="opacity" '
                f'calcMode="discrete" values="0;1;0" keyTimes="0;{f(on)};{f(off)}" '
                f'dur="{T:.3f}s" repeatCount="indefinite"/></path>'
            )
            cursor.append((on, xa))
        for i in range(n - 1, -1, -1):
            cursor.append((dele + (n - i) * DELETE, gl[i - 1][1] if i else X))
    cursor.sort()
    xs = ";".join(f"{x + 6:.1f}" for _, x in cursor)
    kt = ";".join(f(tm) for tm, _ in cursor)
    out.append(
        f'<rect y="{baseline - size * 0.74:.1f}" width="4" height="{size * 0.86:.1f}" fill="{c["accent"]}">'
        f'<animate attributeName="x" calcMode="discrete" values="{xs}" keyTimes="{kt}" '
        f'dur="{T:.3f}s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>'
        "</rect>"
    )
    return out


def header(theme):
    c = THEMES[theme]
    W, H = 1200, 270
    X = 72
    body = typing(c, X, 140, 80)
    tag = "".join(d for d, _ in glyphs(TAGLINE, "sans", 28, X + 2, 200))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{" / ".join(ALIASES)} — {TAGLINE}</title>
<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>
{chr(10).join(body)}
<path d="{tag}" fill="{c["muted"]}"/>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for t in THEMES:
        (OUT / f"header-{t}.svg").write_text(header(t))
    print("written to", OUT)
