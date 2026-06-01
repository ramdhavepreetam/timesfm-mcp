# How It Works

## Architecture

```
Your agent (Claude, Cursor, …)
       │  MCP (stdio or HTTP)
       ▼
  timesfm-mcp server
       │
       ├── BaselineBackend  ← always available
       └── TimesFMBackend   ← loaded lazily if installed
```

The server exposes three MCP tools (`forecast`, `list_backends`, `backtest`). When a tool is called, the server selects the best available backend, runs the forecast, and returns a structured JSON response the agent uses to write a plain-language explanation.

## Statistical baseline backend

The default backend runs in milliseconds with no external dependencies beyond NumPy. It combines two classical techniques:

**1. Linear trend decomposition**

A least-squares line is fit to the historical values. This captures the underlying growth or decline rate.

**2. Seasonal-naive component**

After removing the trend, the detrended residuals carry seasonal patterns. The forecast repeats the last observed seasonal cycle: for a monthly series with detected season length 12, month 25's seasonal component equals month 13's detrended value.

**3. Uncertainty bands**

The in-sample residual standard deviation σ sets the band width. At horizon *h*, the band scales as `σ × √h` — widening naturally as uncertainty compounds over time. Z-scores map coverage levels to band widths (90% → z ≈ 1.645, 95% → z ≈ 1.960).

### Season detection

Season length is detected via autocorrelation. The algorithm tests lags from 2 to `min(n/2, 60)` and selects the lag with the highest normalized autocorrelation above 0.35. If no lag clears that threshold, it returns 1 (no seasonality).

## TimesFM 2.5 backend

[TimesFM 2.5](https://github.com/google-research/timesfm) is Google's 200M-parameter foundation model for time-series forecasting, trained on a large corpus of real-world time series. It handles irregular seasonality, trend shifts, and complex patterns that stump classical methods.

**What it does differently**: Instead of fitting a parametric model, it uses a patched-transformer architecture to directly predict the distribution of future values given the history. It produces native quantile forecasts (deciles 10%–90%) that are used for uncertainty bands.

**Context window**: up to 1,024 historical points. Longer histories are truncated to the most recent 1,024.

**Installation**: TimesFM 2.5 is not on PyPI. Clone and install from source (`git clone https://github.com/google-research/timesfm && pip install -e ".[torch]"`), then `pip install timesfm-mcp` into the same environment. The model weights (~800 MB) download from Hugging Face on first use. Requires ~16 GB RAM.

## Backend selection

```python
TIMESFM_MCP_BACKEND=auto  # (default) use TimesFM if installed, else baseline
TIMESFM_MCP_BACKEND=baseline  # always use the statistical baseline
```

The server checks for TimesFM at startup by importing `timesfm` and verifying that the PyTorch backend class is present. If PyTorch is not installed (so `timesfm.TimesFM_2p5_200M_torch` is missing), it silently falls back to the baseline. This means `forecast` always returns a result — even without the ML extra.

## Response design

The `context` object in the response is intentionally compact and machine-readable. The agent reads it and writes its own explanation in natural language. This keeps the server output small (JSON, not prose) while giving the agent everything it needs to write a good recommendation:

- `trend` and `trend_pct_per_step` → "Revenue is growing at ~4%/month"
- `detected_season_length` → mention if seasonality was found
- `volatility` → "The 90% band is wide because the series is volatile — plan conservatively"
- `last_value` + point forecasts → "From $X today to $Y in 6 months"
