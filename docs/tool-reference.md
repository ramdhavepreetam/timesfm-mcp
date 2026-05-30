# Tool Reference

Three tools are exposed over MCP. Your agent discovers them automatically.

---

## `forecast`

Forecast a single numeric time series.

```python
forecast(
    values: list[float],
    horizon: int = 12,
    quantiles: list[float] | None = None,
    season_length: int | None = None,
) -> dict
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `values` | `list[float]` | required | Historical observations in chronological order (oldest first). Minimum 3 points. |
| `horizon` | `int` | `12` | How many future steps to predict. Range: 1–1000. |
| `quantiles` | `list[float]` | `null` | Symmetric coverage levels for uncertainty bands, e.g. `[0.9]` for a 90% band. Omit for point forecasts only. Supported: 0.80, 0.90, 0.95. |
| `season_length` | `int` | `null` | Known seasonal period: `7` for daily-with-weekly seasonality, `12` for monthly-with-yearly. Leave null to auto-detect. |

### Response

```json
{
  "backend": "baseline",
  "horizon": 6,
  "points": [
    {"step": 1, "value": 14823.4, "lower": 13201.1, "upper": 16445.7},
    {"step": 2, "value": 15310.2, "lower": 13508.3, "upper": 17112.1},
    ...
  ],
  "context": {
    "n_observations": 24,
    "detected_season_length": 12,
    "trend": "rising",
    "trend_pct_per_step": 3.82,
    "last_value": 14200.0,
    "mean": 11750.0,
    "volatility": 612.4
  },
  "notes": ["Statistical baseline (seasonal-naive + trend). Install the 'timesfm' extra for the foundation model."]
}
```

### Response fields

**`points`** — one entry per forecast step:

| Field | Description |
|-------|-------------|
| `step` | Steps ahead (1-indexed from end of input) |
| `value` | Point (median) forecast |
| `lower` | Lower quantile bound (null if no quantiles requested) |
| `upper` | Upper quantile bound (null if no quantiles requested) |

**`context`** — compact summary for agent reasoning:

| Field | Description |
|-------|-------------|
| `trend` | `"rising"`, `"falling"`, or `"flat"` |
| `trend_pct_per_step` | Approx. % change per step from the fitted linear trend |
| `detected_season_length` | Detected seasonal period; `1` means no seasonality |
| `volatility` | Std of residuals — higher means wider, less certain bands |
| `last_value` | Most recent observed value |
| `mean` | Mean of the historical series |

### Example agent prompt

> "Here's our monthly revenue for the last 24 months: [12000, 13100, 13800, 14200, 15100, 14800, 16200, 17100, 16800, 18200, 19100, 18700, 20100, 21200, 20800, 22100, 23200, 22800, 24100, 25300, 24800, 26100, 27200, 26800]. Forecast the next 6 months with a 90% confidence band."

---

## `list_backends`

Report which forecasting engine is active and why.

```python
list_backends() -> dict
```

### Response

```json
{
  "active": "baseline",
  "timesfm_available": false,
  "hint": "Install the 'timesfm' extra to enable the foundation model: pip install 'timesfm-mcp[timesfm]'."
}
```

### Example agent prompt

> "Which forecasting backend is active right now?"

---

## `backtest`

Hold out the last N points and compare TimesFM vs baseline performance.

```python
backtest(
    values: list[float],
    holdout: int = 6,
) -> dict
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `values` | `list[float]` | required | Historical observations. Must have at least `holdout + 3` points. |
| `holdout` | `int` | `6` | Number of final points to hold out for testing. |

### Response

```json
{
  "holdout": 6,
  "results": {
    "baseline": {
      "mae": 588.2,
      "smape": 2.34
    }
  }
}
```

When TimesFM is installed, a `"timesfm"` key also appears in `results` with its own `mae` and `smape`. Without the `timesfm` extra, only `"baseline"` is returned.

`mae` is mean absolute error. `smape` is symmetric mean absolute percentage error (×100, so 2.34 = 2.34%).

!!! note
    `timesfm` results only appear when the TimesFM extra is installed. Without it, only `baseline` results are returned.

### Example agent prompt

> "Backtest my revenue data with a 6-month holdout. How accurate is the forecast?"

---

## Quantile bands

The `quantiles` parameter accepts a list of symmetric coverage levels. For example:

- `[0.9]` → 90% band (lower = 5th percentile, upper = 95th percentile)
- `[0.95]` → 95% band
- `[0.8]` → 80% band

Only the maximum value in the list is used. Pass one quantile — the server uses the largest one for the band calculation.

**Baseline backend**: bands are derived from in-sample residual standard deviation, widening with forecast horizon (`√h` scaling).

**TimesFM backend**: bands come from the model's native quantile head (10th–90th deciles), linearly interpolated to match your requested level.
