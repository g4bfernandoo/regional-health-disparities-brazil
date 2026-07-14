"""
style.py — Visual identity system for the cardiovascular research portfolio
Para, Brazil (2019-2023)

Import this at the top of every notebook:
    from style import apply_style, add_figure_rule, add_source_note, PALETTE

Design principles:
- Serif titles (Georgia) for academic authority
- Sans-serif body (Arial) for readability
- 4-color palette: navy, crimson, steel, slate
- Thin top rule as the signature visual element
- Consistent source footnote
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── PALETTE ──────────────────────────────────────────────────────────────────
PALETTE = {
    "navy"   : "#1B2A4A",   # titles, primary elements
    "crimson": "#A12020",   # key findings, alerts, Cluster 2
    "steel"  : "#E67E22",   # secondary data, Cluster 0
    "amber"  : "#E4B300",   # warnings, Cluster 1
    "slate"  : "#433D3B",   # annotations, gridlines, secondary text
    "smoke"  : "#F2F3F4",   # background panels
    "rule"   : "#D5D8DC",   # separator lines
    "white"  : "#FFFFFF",
}

# Cluster colors — consistent across all figures and the map
CLUSTER_COLORS = {
    -1: '#1B2A4A',   # navy    — reference centers (Belem, Ananindeua)
     0: "#E4B300",   # orange  — high-mortality economic corridor (21 municipalities)
     1: '#E67E22',   # amber   — rapidly deteriorating access (18 municipalities)
     2: '#E65022',   # steel   — structural care desert (67 municipalities)
     3: "#A12020",   # crimson — critical mortality burden (36 municipalities)
}

CLUSTER_LABELS = {
    -1: 'Reference Center (2)',
     0: 'High-Mortality Economic Corridor (21)',
     1: 'Rapidly Deteriorating Access (18)',
     2: 'Structural Care Desert (67)',
     3: 'Critical Mortality Burden (36)',
}

# ── TYPOGRAPHY ────────────────────────────────────────────────────────────────
# Windows: Georgia + Arial (always available)
# Linux/Mac fallback: DejaVu Serif + DejaVu Sans
FONT_TITLE = "Georgia"        # serif — titles and suptitles
FONT_BODY  = "Arial"          # sans  — axes labels, ticks, annotations

# ── GLOBAL STYLE APPLICATION ─────────────────────────────────────────────────
def apply_style():
    """
    Call once at the top of each notebook, after imports.
    Sets matplotlib rcParams globally so all figures in the session
    share the same visual identity without repeating configuration.

    What each parameter does:
    - font.family       : default font for all text
    - axes.titlesize    : size of subplot titles (ax.set_title())
    - figure.titlesize  : size of suptitles (fig.suptitle())
    - axes.labelsize    : size of x/y axis labels
    - xtick.labelsize   : size of x-axis tick labels
    - axes.spines.*     : whether to draw the border lines around the plot
    - axes.grid         : whether to show background grid lines
    - grid.color        : color of those grid lines
    - grid.alpha        : transparency of grid lines (0=invisible, 1=solid)
    - figure.facecolor  : background color of the whole figure
    - axes.facecolor    : background color of each subplot
    """
    mpl.rcParams.update({
        # Typography
        "font.family"         : FONT_BODY,
        "axes.titlesize"      : 12,
        "axes.titleweight"    : "bold",
        "axes.titlepad"       : 10,
        "figure.titlesize"    : 14,
        "figure.titleweight"  : "bold",
        "axes.labelsize"      : 10,
        "axes.labelcolor"     : PALETTE["navy"],
        "xtick.labelsize"     : 9,
        "ytick.labelsize"     : 9,
        "legend.fontsize"     : 9,
        "legend.title_fontsize": 9,

        # Spines (borders around plots)
        "axes.spines.top"     : False,
        "axes.spines.right"   : False,
        "axes.spines.left"    : True,
        "axes.spines.bottom"  : True,
        "axes.edgecolor"      : PALETTE["rule"],
        "axes.linewidth"      : 0.8,

        # Grid
        "axes.grid"           : True,
        "grid.color"          : PALETTE["rule"],
        "grid.alpha"          : 0.6,
        "grid.linewidth"      : 0.5,
        "axes.axisbelow"      : True,   # grid goes behind bars/lines

        # Colors
        "figure.facecolor"    : PALETTE["white"],
        "axes.facecolor"      : PALETTE["white"],
        "text.color"          : PALETTE["navy"],
        "xtick.color"         : PALETTE["slate"],
        "ytick.color"         : PALETTE["slate"],

        # Figure
        "figure.dpi"          : 130,
        "savefig.dpi"         : 200,
        "savefig.bbox"        : "tight",
        "savefig.facecolor"   : PALETTE["white"],
    })


def title_font(size=14, weight="bold"):
    """
    Returns a FontProperties object for serif titles.
    Use in fig.suptitle(..., fontproperties=title_font())
    or ax.set_title(..., fontproperties=title_font(size=12))
    """
    from matplotlib.font_manager import FontProperties
    return FontProperties(family=FONT_TITLE, size=size, weight=weight)


def add_figure_rule(fig, color=None, lw=2.5, y=0.98):
    """
    Adds a thin horizontal rule at the top of the figure.
    This is the signature visual element — present on every figure.

    Parameters:
        fig   : the matplotlib Figure object
        color : line color (defaults to navy)
        lw    : line width in points
        y     : vertical position in figure coordinates (0=bottom, 1=top)
    """
    color = color or PALETTE["navy"]
    line = Line2D(
        [0.02, 0.98], [y, y],          # x from 2% to 98% of figure width
        transform=fig.transFigure,      # coordinates relative to figure, not axes
        color=color,
        linewidth=lw,
        solid_capstyle="round"
    )
    fig.add_artist(line)


def add_source_note(fig, text="Source: DATASUS/SIM & IBGE (2019-2023). Author analysis.",
                    y=0.01):
    """
    Adds a small source attribution line at the bottom of every figure.
    Standard requirement for academic figures using public data.

    Parameters:
        fig  : the matplotlib Figure object
        text : the source string
        y    : vertical position (default: just above the bottom edge)
    """
    fig.text(
        0.02, y, text,
        fontsize=7,
        color=PALETTE["slate"],
        style="italic",
        transform=fig.transFigure
    )


def add_separator(fig, y=0.93, color=None, lw=0.8):
    """
    Adds a thin separator line between the suptitle and the subplots.
    Useful for multi-panel figures to visually anchor the title block.

    Parameters:
        fig   : the matplotlib Figure object
        y     : vertical position (should be just below the suptitle)
        color : line color (defaults to rule gray)
        lw    : line width
    """
    color = color or PALETTE["rule"]
    line = Line2D(
        [0.02, 0.98], [y, y],
        transform=fig.transFigure,
        color=color,
        linewidth=lw,
        solid_capstyle="butt"
    )
    fig.add_artist(line)
