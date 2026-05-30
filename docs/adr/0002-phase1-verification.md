# ADR 0002 — Phase 1 Verification

**Status:** Accepted
**Date:** 2026-05-29

## Context
As part of the initial launch of the `forecast-mcp` server, Phase 1 was scoped to verify the core architecture (ADR 0001) using the pure-NumPy baseline fallback mechanism. The tests verify that the server can boot and serve MCP clients immediately without the heavy machine learning dependencies (TimesFM 2.5), maintaining zero-friction adoption.

## Actions Taken
1. Set up the local environment in a Python 3.10 virtual environment using `uv venv` and `uv pip install -e ".[dev]"`.
2. Executed the test suite using `pytest tests/`.
3. Verified the MCP server manually via Python integration (simulating the FastMCP inspector).
4. Tested the `forecast` tool on a 36-point sample seasonal series with `horizon=6` and `quantiles=[0.9]`.
5. Tested the `list_backends` tool.

## Results & Quirks
- **Test Suite:** Passed (5/5).
- **Tool Listing:** Both `forecast` and `list_backends` were successfully exposed as MCP tools.
- **Backend Detection:** `list_backends` correctly fell back to the `baseline` engine and provided the correct installation hint for TimesFM.
- **Forecast Generation:**
  - The series successfully extrapolated 6 points ahead.
  - Uncertainty bands widened correctly with the horizon.
  - `context` reliably reported trend and seasonality (e.g. `{'n_observations': 36, 'detected_season_length': 2, 'trend': 'rising', 'trend_pct_per_step': 4.21, 'last_value': 63.0, 'mean': 35.5556, 'volatility': 1.2371}`).
- **Quirks/Notes:** 
  - Since `timesfm` >= 2.5 is not formally published on standard PyPI (or requires fetching from Google Research's github), users running `pip install "forecast-mcp[timesfm]"` might experience dependency resolution failures unless we point to the repository or clarify the installation instructions in the README. We will continue respecting the current setup and lazy load approach in Phase 2.
