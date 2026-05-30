# Example: Forecasting SaaS MRR

## Scenario

You have 24 months of monthly recurring revenue (MRR) and want a 6-month outlook with a quantified uncertainty band for hiring and budget planning.

## Sample data

```
Month:  1      2      3      4      5      6      7      8      9     10     11     12
MRR: 12000  13100  13800  14200  15100  14800  16200  17100  16800  18200  19100  18700

Month: 13     14     15     16     17     18     19     20     21     22     23     24
MRR: 20100  21200  20800  22100  23200  22800  24100  25300  24800  26100  27200  26800
```

## Prompt to paste to your agent

```
Here's our MRR for the last 24 months (in USD):
[12000, 13100, 13800, 14200, 15100, 14800, 16200, 17100, 16800, 18200, 19100, 18700,
 20100, 21200, 20800, 22100, 23200, 22800, 24100, 25300, 24800, 26100, 27200, 26800].

Forecast the next 6 months with a 90% confidence band and tell me:
1. What's the trend?
2. What should I plan for (conservative vs. optimistic)?
3. What does this mean for hiring?
```

## Tool call

The agent calls:

```python
forecast(
    values=[12000, 13100, 13800, 14200, 15100, 14800, 16200, 17100, 16800,
            18200, 19100, 18700, 20100, 21200, 20800, 22100, 23200, 22800,
            24100, 25300, 24800, 26100, 27200, 26800],
    horizon=6,
    quantiles=[0.9]
)
```

## Actual output (baseline backend)

```json
{
  "backend": "baseline",
  "horizon": 6,
  "points": [
    {"step": 1, "value": 28512.70, "lower": 27819.52, "upper": 29205.87},
    {"step": 2, "value": 28112.70, "lower": 27132.40, "upper": 29092.99},
    {"step": 3, "value": 29825.39, "lower": 28624.78, "upper": 31026.00},
    {"step": 4, "value": 29425.39, "lower": 28039.05, "upper": 30811.73},
    {"step": 5, "value": 31138.09, "lower": 29588.11, "upper": 32688.06},
    {"step": 6, "value": 30738.09, "lower": 29040.17, "upper": 32436.00}
  ],
  "context": {
    "n_observations": 24,
    "detected_season_length": 2,
    "trend": "rising",
    "trend_pct_per_step": 3.326,
    "last_value": 26800.0,
    "mean": 19733.33,
    "volatility": 421.41
  }
}
```

| Month | Point forecast | 90% Lower | 90% Upper |
|-------|---------------|-----------|-----------|
| +1    | $28,513       | $27,820   | $29,206   |
| +2    | $28,113       | $27,132   | $29,093   |
| +3    | $29,825       | $28,625   | $31,026   |
| +4    | $29,425       | $28,039   | $30,812   |
| +5    | $31,138       | $29,588   | $32,688   |
| +6    | $30,738       | $29,040   | $32,436   |

The model detects a 2-step seasonal pattern (alternating high-low months visible in the raw data) and a +3.3%/month trend.

## Kind of answer to expect

> "MRR is growing at ~3.3%/month. The forecast alternates between a higher and lower step each month — the model detected a 2-month rhythm in the data, likely reflecting end-of-month vs. mid-month billing cycles or seasonal churn patterns.
>
> By month 6 the point forecast reaches ~$30,700 — roughly 15% above today's $26,800.
>
> The 90% bands are tight relative to the level (lower bound never drops below $27,100), which reflects low residual volatility (~$421/month). The model is fairly confident in this range.
>
> **For hiring:** Conservative planning floor is the month-6 lower bound: $29,040. Committing headcount against the $30,700 midpoint means betting on being in the upper half — reasonable given the tight band, but the lower bound is the safer anchor.
>
> **For optimistic planning:** Upper bound peaks at ~$32,700 in month 5."

## Backtest it first

```
Now backtest that with a 6-month holdout.
```

```python
backtest(values=[...same list...], holdout=6)
```

**Actual backtest result (baseline backend):**

| Step | Actual  | Predicted | Error    |
|------|---------|-----------|----------|
| +1   | $24,100 | $24,495   | −$395    |
| +2   | $25,300 | $24,095   | +$1,205  |
| +3   | $24,800 | $25,790   | −$990    |
| +4   | $26,100 | $25,390   | +$710    |
| +5   | $27,200 | $27,085   | +$115    |
| +6   | $26,800 | $26,685   | +$115    |

**MAE: $588 | sMAPE: 2.3%**

2.3% error on held-out data means the forecast was off by ~$588/month on average — very accurate for this series. The confidence bands reflect that low volatility correctly.

## Why this matters

A 3.3%/month trend compounds to +22% over 6 months. Without a model, teams often eyeball flat or straight-line growth. The uncertainty band forces an honest conversation about planning against a range rather than a single number.
