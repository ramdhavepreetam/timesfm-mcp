# Example: Monthly Cloud Spend Budget

## Scenario

You're preparing the quarterly cloud budget review. Finance wants to know whether to increase the cloud budget for Q3 and by how much. You have 15 months of monthly AWS/GCP/Azure spend.

## Sample data

```
Month:  1     2     3     4     5     6     7     8     9    10    11    12    13    14    15
Spend: 8200  8750  9100  9680 10200 10850 11400 12100 12800 13500 14300 15100 15900 16800 17800
```

Spend has grown consistently — roughly $600–$900 more per month each month.

## Prompt to paste to your agent

```
Here's our monthly cloud spend in USD for the last 15 months:
[8200, 8750, 9100, 9680, 10200, 10850, 11400, 12100, 12800, 13500, 14300, 15100, 15900, 16800, 17800].

Forecast the next 3 months with a 90% confidence band.
Questions:
1. What should the Q3 cloud budget be?
2. Is the growth rate concerning? What does it compound to over 12 months?
3. What's the risk of under-budgeting?
```

## Tool call

The agent calls:

```python
forecast(
    values=[8200, 8750, 9100, 9680, 10200, 10850, 11400, 12100, 12800,
            13500, 14300, 15100, 15900, 16800, 17800],
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
    {"step": 1, "value": 18158.43, "lower": 17649.65, "upper": 18667.21},
    {"step": 2, "value": 19158.43, "lower": 18438.91, "upper": 19877.95},
    {"step": 3, "value": 19516.86, "lower": 18635.62, "upper": 20398.09}
  ],
  "context": {
    "n_observations": 15,
    "detected_season_length": 2,
    "trend": "rising",
    "trend_pct_per_step": 5.463,
    "last_value": 17800.0,
    "mean": 12432.0,
    "volatility": 309.31
  }
}
```

| Month | Point forecast | 90% Lower | 90% Upper |
|-------|---------------|-----------|-----------|
| +1    | $18,158       | $17,650   | $18,667   |
| +2    | $19,158       | $18,439   | $19,878   |
| +3    | $19,517       | $18,636   | $20,398   |

The model detects a 2-month alternating pattern in the data (spend is slightly higher in even months) and a +5.5%/month trend. Volatility is low ($309/month residual std), so the bands are tight.

## Kind of answer to expect

> "Cloud spend is growing at **5.5%/month** — this is the most important number here. At that rate:
> - In 6 months: ~$24,000/month (+35%)
> - In 12 months: ~$34,000/month (+91%)
>
> The bands are tight — the model is confident in this trend because spend has been extremely consistent (sMAPE 3.6% on held-out data). This is both good news (the forecast is reliable) and bad news (the growth is real, not noise).
>
> **Q3 budget recommendation:**
>
> | Scenario | 3-month total | Peak month |
> |----------|--------------|------------|
> | Conservative (lower bounds) | $54,725 | $18,636 |
> | Point forecast sum | $56,833 | $19,517 |
> | Safe (90% upper bounds) | $58,943 | $20,398 |
> | **Recommended budget** | **$59,000** | — |
>
> Budget **$59K** for Q3. More urgently: **flag the growth rate to engineering.** At 5.5%/month, cloud spend nearly doubles in a year. A cost review now — rightsizing instances, deleting unused resources, switching to committed-use discounts — could bend this curve meaningfully before the next budget cycle."

## Backtest it

```
Backtest the cloud spend with a 3-month holdout.
```

**Actual backtest result (baseline backend):**

| Step | Actual  | Predicted | Error  |
|------|---------|-----------|--------|
| +1   | $15,900 | $15,548   | +$352  |
| +2   | $16,800 | $16,348   | +$452  |
| +3   | $17,800 | $16,797   | +$1,003 |

**MAE: $602 | sMAPE: 3.6%**

The model consistently underestimated spend slightly — it trended at ~$600/month error on average. This directional bias (always low) suggests the growth rate may be accelerating. If you see this in your own data, consider adding a buffer above the upper bound.

## Why this matters

Cloud spend is one of the most predictable cost lines in an engineering budget — it follows headcount and product growth. But 5.5%/month compounding surprises finance teams who budget flat. A model-backed projection with a confidence band forces the budget conversation to happen at the right level, not in post-quarter retrospectives.
