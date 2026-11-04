"""Generate the pixel-art SVGs used in the profile README.

Run:  python3 scripts/make_pixel_art.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

BG = "#F3EEE3"      # paper
INK = "#2E2A26"     # ink
MUTED = "#9A9184"   # soft grey-brown
ACCENT = "#E2725B"  # terracotta
SAGE = "#6B8F71"    # sage green
SKY = "#5B8BB0"     # dusty blue
SUN = "#E8B04B"     # mustard

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000"] * 7,
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "*": ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
}


def runs(rows, x0, y0, cell, palette):
    """Turn an ascii bitmap into merged horizontal <rect>s."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch in palette:
                start = c
                while c < len(row) and row[c] == ch:
                    c += 1
                out.append(
                    f'<rect x="{x0 + start * cell}" y="{y0 + r * cell}" '
                    f'width="{(c - start) * cell}" height="{cell}" fill="{palette[ch]}"/>'
                )
            else:
                c += 1
    return out


def text(s, x, y, px, color, gap=1):
    rows = [""] * 7
    for ch in s.upper():
        g = FONT[ch]
        for i in range(7):
            rows[i] += g[i] + "0" * gap
    return runs(rows, x, y, px, {"1": color})


def text_width(s, px, gap=1):
    return len(s) * (5 + gap) * px - gap * px


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img">\n'
        f"<title>{title}</title>\n"
        f'<rect width="{w}" height="{h}" fill="{BG}"/>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


def frame(w, h, t=4, inset=10):
    """A thin pixel frame with notched corners."""
    a, b = inset, inset
    W, H = w - 2 * inset, h - 2 * inset
    return [
        f'<rect x="{a + t}" y="{b}" width="{W - 2 * t}" height="{t}" fill="{INK}"/>',
        f'<rect x="{a + t}" y="{b + H - t}" width="{W - 2 * t}" height="{t}" fill="{INK}"/>',
        f'<rect x="{a}" y="{b + t}" width="{t}" height="{H - 2 * t}" fill="{INK}"/>',
        f'<rect x="{a + W - t}" y="{b + t}" width="{t}" height="{H - 2 * t}" fill="{INK}"/>',
    ]


def blink(inner, dur="1.1s", begin="0s"):
    return (
        f'<g><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
        f'dur="{dur}" begin="{begin}" repeatCount="indefinite"/>' + "".join(inner) + "</g>"
    )


# --------------------------------------------------------------------------- banner
def marquee(s, x, y, w, h, px, color, bg, dur="9s"):
    seg = s + "   "
    seg_w = len(seg) * 6 * px
    reps = w // seg_w + 2
    out = [f'<clipPath id="mq"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>',
           '<g clip-path="url(#mq)"><g>',
           f'<animateTransform attributeName="transform" type="translate" from="0 0" '
           f'to="-{seg_w} 0" dur="{dur}" repeatCount="indefinite"/>']
    out += text(seg * reps, x + 10, y + (h - 7 * px) // 2, px, color)
    out.append("</g></g>")
    return out


def banner():
    W, H = 880, 250
    body = frame(W, H)

    def center(t, px):
        return (W - text_width(t, px)) // 2

    body += text("hi, i'm", center("hi, i'm", 3), 42, 3, MUTED)
    body += text("arman tsarukyan", center("arman tsarukyan", 6), 72, 6, INK)

    nx = center("arman tsarukyan", 6)
    mx = nx + 44
    mq_w = text_width("arman tsarukyan", 6) - 44
    body += text("aka", mx - 44, 140, 2, MUTED)
    body += marquee("toixaydungkhacbiet * ai engineer *", mx, 130, mq_w, 34, 3, SUN, INK)

    line = "> i can make it happen"
    lx = center(line, 2) - 8
    body += text(line, lx, 188, 2, SAGE)
    cx = lx + text_width(line, 2) + 6
    body.append(blink([f'<rect x="{cx}" y="188" width="10" height="14" fill="{SAGE}"/>']))
    return svg(W, H, body, "Arman Tsarukyan aka Toixaydungkhacbiet - AI engineer")


# --------------------------------------------------------------------------- inventory
ICONS = {
    "cloud": ["...XXX...", "..XXXXX..", ".XXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", ".XXXXXXX."],
    "spark": ["....X....", "....X....", "...XXX...", "XXXXXXXXX", "...XXX...", "....X....", "....X...."],
    "db":    [".XXXXXXX.", "X.......X", ".XXXXXXX.", "X.......X", ".XXXXXXX.", "X.......X", ".XXXXXXX."],
    "chart": [".......XX", ".......XX", "....XX.XX", "....XX.XX", ".XX.XX.XX", ".XX.XX.XX", "XXXXXXXXX"],
}

SLOTS = [
    ("cloud", SKY, "cloud", ["aws", "azure", "gcp", "kubernetes", "gh actions", "git"]),
    ("spark", ACCENT, "ml & ai", ["python", "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy"]),
    ("db", SAGE, "data", ["postgres", "mysql", "sql server", "redis"]),
    ("chart", SUN, "tools", ["power bi", "matplotlib", "notion", "trello"]),
]


def inventory():
    W, H = 880, 290
    body = frame(W, H)
    body += text("inventory", 40, 34, 3, INK)
    body += text("lv. 99 ai engineer", W - 40 - text_width("lv. 99 ai engineer", 2), 38, 2, MUTED)
    # dashed divider
    for x in range(40, W - 40, 12):
        body.append(f'<rect x="{x}" y="66" width="6" height="3" fill="{MUTED}"/>')

    col_w = (W - 80) // 4
    for i, (icon, color, title, items) in enumerate(SLOTS):
        x = 40 + i * col_w
        body += runs(ICONS[icon], x, 88, 3, {"X": color})
        body += text(title, x + 38, 90, 2, color)
        for j, item in enumerate(items):
            y = 126 + j * 24
            body.append(f'<rect x="{x}" y="{y + 4}" width="6" height="6" fill="{color}"/>')
            body += text(item, x + 16, y, 2, INK)
    return svg(W, H, body, "Tech inventory")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    (OUT / "inventory.svg").write_text(inventory())
    print("written to", OUT)
