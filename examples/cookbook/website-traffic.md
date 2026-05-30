# Example: Website Traffic Forecasting

## Scenario

You're renewing your CDN contract and need to commit to a bandwidth tier. You have 18 months of monthly session data and need a 3-month outlook to right-size the commitment.

## Sample data

```
Month:     1      2      3      4      5      6      7      8      9
Sessions: 42000  45200  43800  48100  50300  49200  53400  56800  54100

Month:    10     11     12     13     14     15     16     17     18
Sessions: 58900  61200  59800  64300  68100  66400  70200  73800  72100
```

## Prompt to paste to your agent

```
Here are our monthly website sessions for the past 18 months:
[42000, 45200, 43800, 48100, 50300, 49200, 53400, 56800, 54100,
 58900, 61200, 59800, 64300, 68100, 66400, 70200, 73800, 72100].

Forecast the next 3 months with a 90% confidence band.
I'm renewing our CDN contract — what bandwidth tier should I commit to?
What's the risk of going with the point forecast vs. the upper bound?
```

## Tool call

The agent calls:

```python
forecast(
    values=[42000, 45200, 43800, 48100, 50300, 49200, 53400, 56800, 54100,
            58900, 61200, 59800, 64300, 68100, 66400, 70200, 73800, 72100],
    horizon=3,
    quantiles=[0.9]
)
```

## Actual output (baseline backend)

```json
{
  "backend": "baseline",
  "horizon": 3,
  "points": [
    {"step": 1, "value": 77517.44, "lower": 75011.0, "upper": 80023.9},
    {"step": 2, "value": 75817.44, "lower": 72272.8, "upper": 79362.1},
    {"step": 3, "value": 81234.88, "lower": 76893.5, "upper": 85576.2}
  ],
  "context": {
    "n_observations": 18,
    "detected_season_length": 2,
    "trend": "rising",
    "trend_pct_per_step": 3.224,
    "last_value": 72100.0,
    "mean": 57650.0,
    "volatility": 1523.78
  }
}
```

| Month | Point forecast | 90% Lower | 90% Upper |
|-------|---------------|-----------|-----------|
| +1    | 77,517        | 75,011    | 80,024    |
| +2    | 75,817        | 72,273    | 79,362    |
| +3    | 81,235        | 76,894    | 85,576    |

The model detects a 2-month alternating pattern (odd months slightly higher than even) and a +3.2%/month trend. Month +3 is the forecast peak at ~81K.

## Kind of answer to expect

> "Sessions are growing at ~3.2%/month. The model picks up a 2-month alternating rhythm in the data (month +2 dips to ~75,800 before month +3 rebounds to ~81,200).
>
> **CDN tier recommendation:**
>
> | Scenario | Peak sessions (month 3) | Risk |
> |----------|------------------------|------|
> | Point forecast | 81,235 | ~50% of outcomes exceed this |
> | 90% upper bound | 85,576 | ~5% of outcomes exceed this |
> | **Recommended commit** | **90,000** | Upper bound + ~5% headroom |
>
> At 3.2%/month growth, sessions reach ~95K in 6 months (outside your current contract window). If the CDN allows mid-contract tier upgrades, commit to 90K now and plan to revisit at renewal.
>
> Committing to the point forecast (81K) saves money but leaves you exposed if the dip in month +2 reverses harder than expected — the upper bound at month +3 is 85.5K, and any traffic spike could push you above that."

## Backtest it

```
Backtest the traffic data with a 3-month holdout.
```

**Actual backtest result (baseline backend):**

| Step | Actual | Predicted | Error  |
|------|--------|-----------|--------|
| +1   | 70,200 | 71,745    | −1,545 |
| +2   | 73,800 | 70,045    | +3,755 |
| +3   | 72,100 | 75,390    | −3,290 |

**MAE: 2,863 sessions | sMAPE: 3.9%**

The model was within ~2,900 sessions on average. The worst miss was month +2 (+3,755) when the series rebounded more than expected. The 90% upper bound absorbed that miss — 79,362 exceeded the 73,800 actual, so the band held.

## Why this matters

CDN over-commitment wastes budget; under-commitment triggers overage charges and potential rate limiting. A model-backed number — with an explicit confidence band — gives you a defensible argument for the tier you choose, rather than "we eyeballed last quarter and added 20%."
