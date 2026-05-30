# Example: E-commerce Demand & Restock

## Scenario

You manage inventory for a consumer electronics SKU. You have 12 weeks of sales data, a 3-week lead time on restocks, and need to know how many units to order now to avoid a stockout.

## Sample data

```
Week:   1    2    3    4    5    6    7    8    9   10   11   12
Units: 312  287  341  398  421  385  367  412  445  389  428  461
```

A 4-week cycle is visible: week 1 and 3 of each 4-week group are high, week 2 is low, week 4 is moderate.

## Prompt to paste to your agent

```
Here are weekly unit sales for the last 12 weeks:
[312, 287, 341, 398, 421, 385, 367, 412, 445, 389, 428, 461].

Forecast the next 4 weeks with a 90% confidence band. I have a 3-week lead time
on restocks, so I need to place an order now that covers weeks 2–4 of the forecast.
What's the safe quantity to order to avoid a stockout?
```

## Tool call

The agent calls:

```python
forecast(
    values=[312, 287, 341, 398, 421, 385, 367, 412, 445, 389, 428, 461],
    horizon=4,
    quantiles=[0.9],
    season_length=4
)
```

`season_length=4` is specified explicitly. With only 12 data points the autocorrelation detector has limited signal; the explicit value encodes what you know about the business cycle.

## Actual output (baseline backend)

```json
{
  "backend": "baseline",
  "horizon": 4,
  "points": [
    {"step": 1, "value": 493.03, "lower": 445.65, "upper": 540.41},
    {"step": 2, "value": 437.03, "lower": 370.02, "upper": 504.03},
    {"step": 3, "value": 476.03, "lower": 393.97, "upper": 558.09},
    {"step": 4, "value": 509.03, "lower": 414.27, "upper": 603.79}
  ],
  "context": {
    "n_observations": 12,
    "detected_season_length": 4,
    "trend": "rising",
    "trend_pct_per_step": 3.101,
    "last_value": 461.0,
    "mean": 387.17,
    "volatility": 28.80
  }
}
```

| Week | Point forecast | 90% Lower | 90% Upper |
|------|---------------|-----------|-----------|
| +1   | 493 units     | 446       | 540       |
| +2   | 437 units     | 370       | 504       |
| +3   | 476 units     | 394       | 558       |
| +4   | 509 units     | 414       | 604       |

The seasonal pattern comes through clearly: week +2 is the trough (437), week +4 is the cycle peak (509). Trend is +3.1%/week.

## Kind of answer to expect

> "Demand is trending up at ~3.1%/week on a 4-week seasonal pattern. Week +2 is the low point of the upcoming cycle (437 units); week +4 is the peak (509 units).
>
> **Restock window (weeks 2–4):**
>
> | Week | Point | 90% Upper |
> |------|-------|-----------|
> | +2   | 437   | 504       |
> | +3   | 476   | 558       |
> | +4   | 509   | 604       |
> | **Total** | **1,422** | **1,666** |
>
> **Safe restock quantity: 1,666 units** (90% upper bound sum for weeks 2–4). This is what you need to be 90% confident you won't stock out during the lead-time window.
>
> **If storage is constrained:** Order 1,422 units (point forecast sum) and accept ~10% stockout risk. Given you're entering a rising trend week, I'd lean toward the upper bound — a stockout at week +4 (your cycle peak) is costly."

## Backtest it

```
Backtest with a 4-week holdout to see how accurate the forecast would have been.
```

```python
backtest(values=[312, 287, 341, 398, 421, 385, 367, 412, 445, 389, 428, 461], holdout=4)
```

**Actual backtest result (baseline backend, season=4 via auto-detect):**

| Step | Actual | Predicted | Error |
|------|--------|-----------|-------|
| +1   | 445    | 481       | −36   |
| +2   | 389    | 445       | −56   |
| +3   | 428    | 427       | +1    |
| +4   | 461    | 472       | −11   |

**MAE: 26 units | sMAPE: 5.9%**

The model was within 56 units at worst and nailed week +3. A 5.9% sMAPE on a noisy weekly series is solid. The restock buffer from the upper bound absorbs the worst-case error (56 units) comfortably.

## Why this matters

Manual restock decisions often use a fixed reorder point ("order when stock < 200 units"). A growing trend makes that threshold go stale quickly. The forecast accounts for both trend and seasonality, so the reorder quantity adapts to where demand is actually heading.
