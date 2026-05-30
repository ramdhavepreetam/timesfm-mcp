# Limitations

Be aware of these constraints before putting forecast-mcp outputs in front of stakeholders.

## Baseline backend

**Assumes stationarity after decomposition.** The seasonal-naive + trend model works well on stable, regular series. It will miss trend breaks, structural changes, and irregular shocks (a product launch, a pandemic, a supply chain disruption).

**Quantile bands are Gaussian.** The `σ√h` band formula assumes normally distributed residuals. Heavy-tailed series (e.g. viral traffic spikes) will have underestimated tail risk.

**Season detection has limited range.** The autocorrelation scanner tests lags up to `min(n/2, 60)`. If your series has a period longer than 60 steps (e.g. quarterly data over many years with 5-year cycles), it won't be detected.

**Minimum data: 3 observations.** Fewer than 3 points raises a `ValueError`. In practice, you need at least one full seasonal cycle for the seasonal component to be meaningful (e.g. ≥12 points for monthly data).

## TimesFM backend

**Requires ~2 GB of dependencies and ~800 MB of model weights.** Not suitable for resource-constrained environments. The first inference call incurs a download and model-load delay of 30–90 seconds.

**Not fine-tuned to your domain.** TimesFM is a zero-shot foundation model. It's broadly accurate but not specialized. A well-tuned Prophet or ARIMA model, fit to your specific series with expert seasonality knowledge, may outperform it.

**Context cap: 16,384 points.** Longer histories are silently truncated to the most recent 16,384. For very long, high-frequency series, this may lose long-run patterns.

**Quantile interpolation.** TimesFM natively outputs decile quantiles (10%, 20%, …, 90%). Requested bands outside 80%/90%/95% are linearly interpolated, which is approximate.

## General

**No multivariate support.** `forecast` takes a single series. Covariates (promotions, holidays, external drivers) are not supported.

**No real-time data.** The server is stateless; it doesn't fetch or cache historical data. You pass the numbers; it forecasts them.

**Illustrative outputs.** The model has no knowledge of your business. Treat its outputs as a starting point, not a decision. Always sanity-check against domain knowledge and use `backtest` to measure accuracy on your specific data before relying on the forecast.

**No confidence in the uncertainty bands.** A 90% band means "if the model's assumptions hold, 90% of outcomes should fall in this range." If your series violates those assumptions (heteroscedasticity, regime changes), the band is not well-calibrated.

## What to do about these limitations

- **Run `backtest`** on your actual data before presenting forecasts to stakeholders. MAE and sMAPE on a held-out window tell you how accurate the model has been historically.
- **Check `context.volatility`** — high volatility means wide bands and lower confidence. Present ranges, not point estimates.
- **Combine with domain knowledge** — the forecast is an anchor, not a verdict. Apply known events (pricing changes, seasonal promotions) as adjustments on top of the model output.
- **For critical decisions**, treat the lower bound of the uncertainty band as the planning figure, not the point forecast.
