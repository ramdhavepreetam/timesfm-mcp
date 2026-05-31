"""
timesfm-mcp Python quickstart.

Calls the forecasting engine directly (no MCP server, no agent required).
Useful for testing, scripting, or embedding in your own tools.

Install:
    pip install timesfm-mcp

Run:
    python examples/python_quickstart.py
"""

import sys
import os

# Allow running from the repo root without installing.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from timesfm_mcp.backends import select_backend

# --- 1. Basic point forecast ---------------------------------------------------

backend = select_backend(prefer_timesfm=True)
print(f"Active backend: {backend.name}\n")

# 24 months of fictional monthly revenue
mrr = [
    12000, 13100, 13800, 14200, 15100, 14800,
    16200, 17100, 16800, 18200, 19100, 18700,
    20100, 21200, 20800, 22100, 23200, 22800,
    24100, 25300, 24800, 26100, 27200, 26800,
]

result = backend.forecast(values=mrr, horizon=6, quantiles=[], season_length=None)

print("=== 6-month MRR point forecast ===")
for pt in result.points:
    print(f"  Month +{pt.step}: ${pt.value:,.0f}")

ctx = result.context
print(f"\nContext:")
print(f"  Trend:          {ctx.trend} ({ctx.trend_pct_per_step:+.1f}% per step)")
print(f"  Season length:  {ctx.detected_season_length}")
print(f"  Last value:     ${ctx.last_value:,.0f}")
print(f"  Volatility:     {ctx.volatility:.1f}")

# --- 2. With 90% uncertainty bands --------------------------------------------

result_bands = backend.forecast(values=mrr, horizon=6, quantiles=[0.9], season_length=None)

print("\n=== 6-month MRR forecast with 90% band ===")
for pt in result_bands.points:
    print(f"  Month +{pt.step}: ${pt.value:>8,.0f}  [{pt.lower:>8,.0f} – {pt.upper:>8,.0f}]")

# --- 3. Backtest: measure historical accuracy ---------------------------------

from timesfm_mcp.backends import BaselineBackend

holdout = 6
train = mrr[:-holdout]
test = mrr[-holdout:]

baseline = BaselineBackend()
bt_result = baseline.forecast(values=train, horizon=holdout, quantiles=[], season_length=None)
preds = [pt.value for pt in bt_result.points]

mae = sum(abs(a - p) for a, p in zip(test, preds)) / holdout
smape = sum(
    2 * abs(a - p) / (abs(a) + abs(p) + 1e-8)
    for a, p in zip(test, preds)
) / holdout * 100

print(f"\n=== Backtest (holdout = {holdout} months) ===")
print(f"  MAE:   ${mae:,.0f}")
print(f"  sMAPE: {smape:.1f}%")
print()
print("  Step  Actual     Predicted  Error")
for i, (a, p) in enumerate(zip(test, preds), start=1):
    print(f"  +{i}    ${a:>7,.0f}  ${p:>7,.0f}   {a - p:+,.0f}")

# --- 4. Season detection demo -------------------------------------------------

weekly_traffic = [
    4200, 5800, 5600, 5400, 5900, 4100, 3800,   # week 1 (Mon–Sun)
    4400, 6100, 5900, 5700, 6200, 4300, 3900,   # week 2
    4600, 6400, 6200, 5900, 6500, 4500, 4100,   # week 3
    4800, 6700, 6500, 6200, 6800, 4700, 4300,   # week 4
]

result_weekly = backend.forecast(
    values=weekly_traffic,
    horizon=7,
    quantiles=[0.8],
    season_length=7,
)

print("\n=== 7-day website traffic forecast (daily, weekly seasonality) ===")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for pt, day in zip(result_weekly.points, days):
    bar = "█" * int(pt.value / 500)
    print(f"  {day}: {pt.value:>5,.0f}  {bar}")
