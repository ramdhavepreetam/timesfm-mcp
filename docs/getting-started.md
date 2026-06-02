# Getting Started

## System requirements

| | **Baseline** *(default)* | **TimesFM 2.5** *(optional)* |
|---|---|---|
| RAM | **Any** | **≥ 16 GB** |
| Disk | Negligible | **~800 MB** (model weights, first use) |
| Python | 3.10+ | 3.10+ |
| Extra install | None | `pip install "timesfm-mcp[timesfm]"` |

**Not sure which to use?** Start with the baseline (`uvx timesfm-mcp`). It works on any machine — laptop, CI, cloud VM — and is production-ready. Add TimesFM later if you need the neural model's extra accuracy.

## Install

=== "uvx (recommended — zero install)"

    ```bash
    uvx timesfm-mcp
    ```

    `uvx` runs the latest published version in a temporary environment. No global install needed.

=== "pip"

    ```bash
    pip install timesfm-mcp
    timesfm-mcp
    ```

=== "With TimesFM (neural backend)"

    !!! warning "System requirement: ≥ 16 GB RAM"
        TimesFM 2.5 requires at least 16 GB of RAM and downloads ~800 MB of model
        weights from HuggingFace on first use. If your machine has less RAM,
        use the baseline install above — it's production-ready on any hardware.

    ```bash
    pip install "timesfm-mcp[timesfm]"
    timesfm-mcp
    ```

    Adds a 200M-parameter neural network that improves accuracy on structured time series. PyTorch and HuggingFace Hub are pulled in automatically. The server detects TimesFM and upgrades silently — no config change needed.

## Wire up to your agent

See [Client Setup](client-setup.md) for the exact config block for your agent.

## First forecast

Once the server is running and wired up, ask your agent:

> "Here are 18 months of website sessions: [42000, 45200, 43800, 48100, 50300, 49200, 53400, 56800, 54100, 58900, 61200, 59800, 64300, 68100, 66400, 70200, 73800, 72100]. What's the trend, and what should I expect over the next 3 months?"

The agent calls `forecast(values=[...], horizon=3, quantiles=[0.9])` and returns:

- **Point forecast** for each of the next 3 steps
- **90% uncertainty band** (lower and upper bounds)
- **Context summary**: trend direction, detected seasonality, volatility
- **Plain-language explanation** written by the agent using that context

## Verify the active backend

Ask your agent: *"Which forecasting backend is active?"*

It calls `list_backends()` and tells you whether TimesFM or the statistical baseline is running.

## Check forecast accuracy with backtest

Ask your agent: *"Backtest that data — how accurate is the forecast?"*

It calls `backtest(values=[...], holdout=3)`, which holds out the last 3 points, forecasts them from history, and reports MAE and sMAPE for each backend.

## Next steps

- [Cookbook](cookbook.md) — four real-world scenarios with exact prompts
- [Tool Reference](tool-reference.md) — full parameter docs
- [How It Works](how-it-works.md) — the math and model behind the forecasts
