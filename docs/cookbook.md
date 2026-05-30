# Cookbook

Real-world scenarios with realistic sample data, exact agent prompts, and the kind of answer to expect.

Each example follows the same pattern:

1. **Context** — what you're measuring and why you're forecasting it
2. **Prompt** — paste this to your agent
3. **Tool call** — what the agent does under the hood
4. **Actual output** — real numbers from the baseline backend (what you'll actually get)
5. **Then: backtest** — how to verify the numbers before trusting them

All outputs in this cookbook were produced by running the baseline backend on the shown data. They will reproduce exactly with `pip install forecast-mcp`.

---

## SaaS MRR

24 months of monthly recurring revenue → 6-month outlook for hiring and budget planning.

**Prompt:**

> "Here's our MRR for the last 24 months (in USD):
> [12000, 13100, 13800, 14200, 15100, 14800, 16200, 17100, 16800, 18200, 19100, 18700, 20100, 21200, 20800, 22100, 23200, 22800, 24100, 25300, 24800, 26100, 27200, 26800].
> Forecast the next 6 months with a 90% confidence band and tell me what to plan for."

**Tool call:**

```python
forecast(values=[12000, 13100, 13800, 14200, 15100, 14800, 16200, 17100, 16800,
                 18200, 19100, 18700, 20100, 21200, 20800, 22100, 23200, 22800,
                 24100, 25300, 24800, 26100, 27200, 26800],
         horizon=6, quantiles=[0.9])
```

**Actual output (baseline backend):**

| Month | Point  | 90% Lower | 90% Upper |
|-------|--------|-----------|-----------|
| +1    | $28,513 | $27,820  | $29,206   |
| +2    | $28,113 | $27,132  | $29,093   |
| +3    | $29,825 | $28,625  | $31,026   |
| +4    | $29,425 | $28,039  | $30,812   |
| +5    | $31,138 | $29,588  | $32,688   |
| +6    | $30,738 | $29,040  | $32,436   |

Context: trend = rising (+3.3%/month), season = 2 (alternating high-low pattern), volatility = $421.

**Agent answer:**

> "MRR is growing at ~3.3%/month. The forecast alternates slightly each month — the model detected a 2-step rhythm in the data (likely end-of-month vs. mid-month patterns). By month 6 the point forecast is ~$30,700. The 90% bands are tight (lower bound stays above $27K), reflecting low volatility. For hiring: plan against the month-6 lower bound of $29,040. Upper bound (~$32,700) is your optimistic headroom."

**Backtest (MAE: $588, sMAPE: 2.3%)** — the model was within ~$590/month on held-out data. High confidence.

---

## E-commerce demand & restock

12 weeks of weekly unit sales → 4-week restock forecast.

**Prompt:**

> "Here are weekly unit sales for the last 12 weeks:
> [312, 287, 341, 398, 421, 385, 367, 412, 445, 389, 428, 461].
> Forecast the next 4 weeks with a 90% band. I have a 3-week lead time — what's the safe quantity to order?"

**Tool call:**

```python
forecast(values=[312, 287, 341, 398, 421, 385, 367, 412, 445, 389, 428, 461],
         horizon=4, quantiles=[0.9], season_length=4)
```

**Actual output (baseline backend):**

| Week | Point | 90% Lower | 90% Upper |
|------|-------|-----------|-----------|
| +1   | 493   | 446       | 540       |
| +2   | 437   | 370       | 504       |
| +3   | 476   | 394       | 558       |
| +4   | 509   | 414       | 604       |

**Agent answer:** Upper-bound sum for weeks 2–4 (the lead-time window) = 1,666 units — the safe restock quantity. Point forecast sum = 1,422.

**Backtest (MAE: 26 units, sMAPE: 5.9%)** — within 56 units at worst; week +3 nearly exact.

---

## Website traffic

18 months of monthly sessions → 3-month outlook for CDN capacity planning.

**Prompt:**

> "Here are our monthly website sessions for the past 18 months:
> [42000, 45200, 43800, 48100, 50300, 49200, 53400, 56800, 54100, 58900, 61200, 59800, 64300, 68100, 66400, 70200, 73800, 72100].
> Forecast the next 3 months with a 90% band. What CDN tier should I commit to?"

**Tool call:**

```python
forecast(values=[42000, 45200, 43800, 48100, 50300, 49200, 53400, 56800, 54100,
                 58900, 61200, 59800, 64300, 68100, 66400, 70200, 73800, 72100],
         horizon=3, quantiles=[0.9])
```

**Actual output (baseline backend):**

| Month | Point  | 90% Lower | 90% Upper |
|-------|--------|-----------|-----------|
| +1    | 77,517 | 75,011    | 80,024    |
| +2    | 75,817 | 72,273    | 79,362    |
| +3    | 81,235 | 76,894    | 85,576    |

**Agent answer:** Recommend committing to 90,000 sessions/month (upper bound + ~5% headroom). At 3.2%/month growth, the 85K upper bound will be breached within the contract window.

**Backtest (MAE: 2,863 sessions, sMAPE: 3.9%)** — worst miss was 3,755 sessions, well within the 90% band.

---

## Monthly cloud spend

15 months of AWS/GCP/Azure spend → 3-month budget forecast.

**Prompt:**

> "Here's our monthly cloud spend in USD for the last 15 months:
> [8200, 8750, 9100, 9680, 10200, 10850, 11400, 12100, 12800, 13500, 14300, 15100, 15900, 16800, 17800].
> Forecast the next 3 months with a 90% band. What should the Q3 budget be?"

**Tool call:**

```python
forecast(values=[8200, 8750, 9100, 9680, 10200, 10850, 11400, 12100, 12800,
                 13500, 14300, 15100, 15900, 16800, 17800],
         horizon=3, quantiles=[0.9])
```

**Actual output (baseline backend):**

| Month | Point  | 90% Lower | 90% Upper |
|-------|--------|-----------|-----------|
| +1    | $18,158 | $17,650  | $18,667   |
| +2    | $19,158 | $18,439  | $19,878   |
| +3    | $19,517 | $18,636  | $20,398   |

**Agent answer:** Budget $59K for Q3 (90% upper bound sum). Flag the 5.5%/month growth rate to engineering — at this rate, spend nearly doubles in 12 months.

**Backtest (MAE: $602, sMAPE: 3.6%)** — model consistently underestimated slightly. Directional bias (always low) suggests accelerating growth; add a buffer above the upper bound.

---

## Tips for getting the best results

**Provide at least one full seasonal cycle.** For monthly data with yearly seasonality, 12+ months is the minimum; 24+ is better.

**Always backtest on your own data.** The cookbook numbers are from the baseline backend on this specific data. Your series will have different accuracy. Run `backtest` before trusting the forecast.

**Use the lower bound for commitment decisions.** Budget approvals, hiring plans, inventory orders — commit against the lower bound of the uncertainty band, not the point forecast.

**Use `season_length` when you know it.** The auto-detector works from autocorrelation and needs sufficient data. If you know your data has a 7-day or 12-month cycle, pass it explicitly.
