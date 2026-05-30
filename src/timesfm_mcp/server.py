"""timesfm-mcp: Google TimesFM 2.5 forecasting tools for MCP-compatible AI agents.

Run locally (stdio, for Claude Desktop / Claude Code / Cursor):
    uvx timesfm-mcp

Or over HTTP for a hosted deployment:
    timesfm-mcp --http
"""

from __future__ import annotations

import os
import sys

from fastmcp import FastMCP

from .backends import select_backend
from .models import ForecastResult

mcp = FastMCP("timesfm-mcp")

# Honour an env flag so users can force the baseline (e.g. on a tiny box).
_PREFER_TIMESFM = os.getenv("TIMESFM_MCP_BACKEND", "auto").lower() != "baseline"


@mcp.tool
def forecast(
    values: list[float],
    horizon: int = 12,
    quantiles: list[float] | None = None,
    season_length: int | None = None,
) -> dict:
    """Forecast a single numeric time series.

    Args:
        values: The historical observations in chronological order (oldest first).
        horizon: How many future steps to predict.
        quantiles: Symmetric coverage levels for uncertainty bands, e.g. [0.9].
            Omit for point forecasts only.
        season_length: Known seasonal period (e.g. 7 for daily-with-weekly,
            12 for monthly-with-yearly). Leave null to auto-detect.

    Returns:
        A forecast with point values, optional uncertainty bands, and a compact
        `context` summary (trend, seasonality, volatility). Use the context to
        write a plain-language explanation and a recommended action for the user.
    """
    if horizon < 1 or horizon > 1000:
        raise ValueError("horizon must be between 1 and 1000.")
    backend = select_backend(prefer_timesfm=_PREFER_TIMESFM)
    result: ForecastResult = backend.forecast(values, horizon, quantiles or [], season_length)
    return result.model_dump()


@mcp.tool
def list_backends() -> dict:
    """Report which forecasting engine is active and why."""
    backend = select_backend(prefer_timesfm=_PREFER_TIMESFM)
    return {
        "active": backend.name,
        "timesfm_available": backend.name == "timesfm",
        "hint": "Install the 'timesfm' extra to enable the foundation model: pip install 'timesfm-mcp[timesfm]'.",
    }


@mcp.tool
def backtest(values: list[float], holdout: int = 6) -> dict:
    """Hold out the last N points and compare TimesFM vs baseline performance.

    Args:
        values: Historical observations (at least holdout + 3 points).
        holdout: Number of final points to hold out for testing.

    Returns:
        A dictionary with MAE and sMAPE for both baseline and TimesFM backends,
        demonstrating the performance lift over the baseline.
    """
    if len(values) <= holdout + 2:
        raise ValueError(f"Need at least {holdout + 3} observations for backtest with holdout={holdout}.")

    train = values[:-holdout]
    test = values[-holdout:]

    from .backends import BaselineBackend, TimesFMBackend

    results = {}

    # Baseline
    baseline = BaselineBackend()
    try:
        b_res = baseline.forecast(train, horizon=holdout, quantiles=[], season_length=None)
        b_preds = [p.value for p in b_res.points]

        b_mae = sum(abs(a - b) for a, b in zip(test, b_preds)) / holdout
        b_smape = sum(2 * abs(a - b) / (abs(a) + abs(b) + 1e-8) for a, b in zip(test, b_preds)) / holdout * 100

        results["baseline"] = {
            "mae": round(b_mae, 4),
            "smape": round(b_smape, 4),
        }
    except Exception as e:
        results["baseline"] = {"error": str(e)}

    # TimesFM
    if _PREFER_TIMESFM:
        try:
            timesfm = TimesFMBackend()
            t_res = timesfm.forecast(train, horizon=holdout, quantiles=[], season_length=None)
            t_preds = [p.value for p in t_res.points]

            t_mae = sum(abs(a - b) for a, b in zip(test, t_preds)) / holdout
            t_smape = sum(2 * abs(a - b) / (abs(a) + abs(b) + 1e-8) for a, b in zip(test, t_preds)) / holdout * 100

            results["timesfm"] = {
                "mae": round(t_mae, 4),
                "smape": round(t_smape, 4),
            }
        except Exception as e:
            results["timesfm"] = {"error": str(e), "hint": "Ensure timesfm is installed."}

    return {"holdout": holdout, "results": results}


def main() -> None:
    if "--http" in sys.argv:
        mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
    else:
        mcp.run()  # stdio by default


if __name__ == "__main__":
    main()
