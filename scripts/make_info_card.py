#!/usr/bin/env python3
"""
Hand-authored neofetch-style info card as an animated SVG.

Lines fade in and slide up one after another (SMIL only -- GitHub renders SVG
animations inside <img>, but strips JS). Edit LINES below to change the
content, then re-run: python scripts/make_info_card.py
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")

# ---- content: (label, value). Edit freely. --------------------------------
TITLE = "kermito21@github: ~$ neofetch"
HEADER = "kermito21@github"
LINES = [
    ("OS",      "Windows 11 (lives in the terminal)"),
    ("Shell",   "pwsh + git bash"),
    ("Editor",  "VS Code + Claude Code"),
    ("Stack",   "TypeScript / Python / Node"),
    ("Focus",   "markets, automation, AI agents"),
    ("Uptime",  "shipping since 2022"),
    ("Contact", "github.com/Kermito21"),
]

# ---- palette (matches wordmark + heatmap) ---------------------------------
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
ACCENT = "#39d353"          # neofetch label green, same as heatmap's top level
DIM = "#7d8590"
SWATCHES = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

PAD = 22
TITLEBAR_H = 28
LINE_H = 26
FS = 14.5
LABEL_W = 78                # px reserved for the label column

W = 470
header_rows = 2             # header + underline
rows = header_rows + len(LINES)
H = TITLEBAR_H + PAD + rows * LINE_H + 34 + PAD  # +34 for the palette strip

REVEAL_STEP = 0.28          # seconds between successive lines
FADE = 0.45


def line_group(y, inner, delay):
    """Wrap a row in a fade + slide-up SMIL animation."""
    return (
        f'<g opacity="0" transform="translate(0 6)">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
        f'dur="{FADE}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 6" to="0 0" begin="{delay:.2f}s" dur="{FADE}s" fill="freeze"/>'
        f'{inner}</g>'
    )


p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, '
    f'Consolas, monospace">',
    '<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" '
    f'stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    p.append(f'<circle cx="{18 + i*15}" cy="{TITLEBAR_H/2}" r="4.5" fill="{dot}"/>')
p.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" '
         f'font-size="11.5" text-anchor="middle">{html.escape(TITLE)}</text>')

y = TITLEBAR_H + PAD + LINE_H * 0.6
p.append(line_group(y, f'<text x="{PAD}" y="{y:.0f}" fill="{ACCENT}" '
                       f'font-size="{FS}" font-weight="bold">{html.escape(HEADER)}</text>', 0.1))
y += LINE_H * 0.8
p.append(line_group(y, f'<text x="{PAD}" y="{y:.0f}" fill="{DIM}" '
                       f'font-size="{FS}">{"-" * len(HEADER)}</text>', 0.1 + REVEAL_STEP * 0.5))

delay = 0.1 + REVEAL_STEP
for label, value in LINES:
    y += LINE_H
    inner = (
        f'<text x="{PAD}" y="{y:.0f}" fill="{ACCENT}" font-size="{FS}" '
        f'font-weight="bold">{html.escape(label)}</text>'
        f'<text x="{PAD + LABEL_W}" y="{y:.0f}" fill="{INK}" '
        f'font-size="{FS}">{html.escape(value)}</text>'
    )
    delay += REVEAL_STEP
    p.append(line_group(y, inner, delay))

# neofetch-style palette strip, then a blinking block cursor
y += LINE_H + 8
sw = 26
strip = "".join(
    f'<rect x="{PAD + i*(sw+4)}" y="{y:.0f}" width="{sw}" height="13" rx="3" '
    f'fill="{c}"/>' for i, c in enumerate(SWATCHES)
)
p.append(line_group(y, strip, delay + REVEAL_STEP))
cursor_x = PAD + len(SWATCHES) * (sw + 4) + 8
p.append(
    f'<rect x="{cursor_x}" y="{y:.0f}" width="9" height="13" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
    f'dur="1.1s" begin="{delay + REVEAL_STEP:.2f}s" repeatCount="indefinite"/></rect>'
)

p.append("</svg>")
svg = "".join(p)
with open(OUT, "w") as fh:
    fh.write(svg)
print(f"wrote {OUT}  {len(svg)/1024:.1f} KB  {W}x{H}")
