"""
Generate the forecast preview chart for the README and docs site.

Run:
    pip install matplotlib
    python examples/generate_chart.py

Output: docs/assets/forecast_preview.png
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from timesfm_mcp.backends import BaselineBackend

# MRR data (24 months)
history = [
    12000, 13100, 13800, 14200, 15100, 14800,
    16200, 17100, 16800, 18200, 19100, 18700,
    20100, 21200, 20800, 22100, 23200, 22800,
    24100, 25300, 24800, 26100, 27200, 26800,
]
horizon = 6

backend = BaselineBackend()
result = backend.forecast(values=history, horizon=horizon, quantiles=[0.9], season_length=None)

# --- Plot ---
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("matplotlib is not installed. Run: pip install matplotlib")
    sys.exit(1)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#161b22")

hist_x = list(range(1, len(history) + 1))
fore_x = list(range(len(history), len(history) + horizon + 1))

# History line
ax.plot(hist_x, history, color="#58a6ff", linewidth=2.0, label="History", zorder=3)

# Forecast line (starts at last history point)
fore_y = [history[-1]] + [pt.value for pt in result.points]
fore_lo = [history[-1]] + [pt.lower for pt in result.points]
fore_hi = [history[-1]] + [pt.upper for pt in result.points]

ax.plot(fore_x, fore_y, color="#f78166", linewidth=2.0, linestyle="--", label="Forecast", zorder=3)

# Shaded 90% band
ax.fill_between(fore_x, fore_lo, fore_hi, alpha=0.25, color="#f78166", label="90% band", zorder=2)

# Divider at forecast start
ax.axvline(x=len(history), color="#8b949e", linewidth=1, linestyle=":", alpha=0.6)

# Labels
ax.text(
    len(history) + 0.15, max(fore_hi) * 0.97,
    "forecast →",
    color="#8b949e", fontsize=9, va="top",
)

# Styling
ax.set_xlabel("Month", color="#c9d1d9", fontsize=11)
ax.set_ylabel("MRR (USD)", color="#c9d1d9", fontsize=11)
ax.set_title("timesfm-mcp  ·  SaaS MRR — 24-month history + 6-month forecast", color="#c9d1d9", fontsize=12, pad=12)
ax.tick_params(colors="#8b949e")
ax.spines["bottom"].set_color("#30363d")
ax.spines["left"].set_color("#30363d")
ax.spines["top"].set_color("#30363d")
ax.spines["right"].set_color("#30363d")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

legend = ax.legend(facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9", fontsize=10)

ax.text(
    0.98, 0.04,
    "Illustrative — statistical baseline backend",
    transform=ax.transAxes,
    ha="right", va="bottom",
    fontsize=8, color="#6e7681", style="italic",
)

fig.tight_layout()

out_path = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "forecast_preview.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {os.path.abspath(out_path)}")
