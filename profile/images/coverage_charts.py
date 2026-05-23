#!/usr/bin/env python3
"""Coverage bar charts for the profile parity & benchmark pages.

Reproducible generator (mirrors MobilitySpark/berlinmod/bench/chart.py in spirit:
matplotlib -> committed PNG, embedded via <img>). Emits two horizontal-bar charts
from the measured coverage numbers:

  streaming-coverage.png  — Flink / Kafka / Nebula vs the 1,945 streamable surface
  database-coverage.png   — MobilityDB / MobilityDuck / MobilitySpark vs the SQL surface

Solid bar = confirmed (L3 proven / reference); lighter bar = wired but not yet
proven. Re-run after the numbers change:  python3 coverage_charts.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
TRACK = "#ececec"   # the 0->100% track behind each bar


def hbar(path, title, rows, subtitle):
    """rows: list of (label, pct, value_text, color, proven_bool)."""
    fig, ax = plt.subplots(figsize=(7.6, 2.5), dpi=150)
    ys = list(range(len(rows)))[::-1]               # top-to-bottom
    for y, (label, pct, vtext, color, proven) in zip(ys, rows):
        ax.barh(y, 100, color=TRACK, height=0.55, zorder=1)          # track
        ax.barh(y, pct, color=color, height=0.55, zorder=2,
                alpha=1.0 if proven else 0.55,
                hatch=None if proven else "////", edgecolor=color)
        ax.text(pct + 1.5, y, vtext, va="center", ha="left",
                fontsize=10, color="#222", zorder=3)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=11)
    ax.set_xlim(0, 128)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100%"], fontsize=9, color="#666")
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left", pad=14)
    ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=9, color="#666")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color="#f0f0f0", zorder=0)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {path}")


# Streaming — solid = proven callable, hatched/light = wired (not yet proven)
hbar(
    HERE / "streaming-coverage.png",
    "Streaming — MEOS function coverage",
    [
        ("MobilityFlink",  100.0, "100.0%  ·  1945 / 1945  · proven", "#1a9988", True),
        ("MobilityKafka",  100.0, "100.0%  ·  1945 / 1945  · proven", "#1a9988", True),
        ("MobilityNebula",  12.6, "12.6%  ·  245 / 1945  · wired",    "#1a9988", False),
    ],
    "of 1,945 streamable MEOS functions   (solid = proven callable · hatched = wired)",
)

# Database — per-platform colour family from chart.py; MobilityDB = reference
hbar(
    HERE / "database-coverage.png",
    "Databases — MobilityDB SQL surface coverage",
    [
        ("MobilityDB",    100.0, "100%  ·  reference",            "#0f4ec9", True),
        ("MobilityDuck",  100.0, "100.0%  ·  943 / 943 active",   "#c47000", True),
        ("MobilitySpark",  99.6, "99.6%  ·  1571 / 1577",         "#1f7a23", True),
    ],
    "of the MobilityDB public SQL API   (each engine over its active-addressable scope)",
)
