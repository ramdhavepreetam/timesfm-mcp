# timesfm-mcp

[![CI](https://github.com/ramdhavepreetam/timesfm-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ramdhavepreetam/timesfm-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/timesfm-mcp.svg)](https://pypi.org/project/timesfm-mcp/)
[![Docs](https://img.shields.io/badge/docs-GitHub-blue)](https://github.com/ramdhavepreetam/timesfm-mcp/tree/main/docs)

**MCP server for Google's TimesFM 2.5 — give any AI agent zero-config time-series forecasting.**

Plug [TimesFM 2.5](https://github.com/google-research/timesfm), Google's 200M-parameter foundation model for time-series, directly into Claude Code, Claude Desktop, Cursor, or any MCP client. The agent calls `forecast`, gets point predictions + uncertainty bands + a trend/seasonality summary, and writes the explanation itself.

No ML configuration. No data pipelines. One line to run.

![Forecast chart: 24-month MRR history with 6-month point forecast and 90% confidence band](https://raw.githubusercontent.com/ramdhavepreetam/timesfm-mcp/main/docs/assets/forecast_preview.png)

*Chart generated with the statistical baseline. See "Enable TimesFM 2.5" below to use the full neural model.*

## Quickstart (30 seconds)

```bash
uvx timesfm-mcp        # runs over stdio for local agents
```

Add to your Claude Desktop / Claude Code / Cursor config:

```json
{
  "mcpServers": {
    "forecast": { "command": "uvx", "args": ["timesfm-mcp"] }
  }
}
```

Then ask your agent: *"Forecast the next 6 months from this revenue data and tell me what to expect."*

## Enable TimesFM 2.5 (optional, advanced)

TimesFM 2.5 is not on PyPI — install it from source, then install `timesfm-mcp` into the same environment:

```bash
git clone https://github.com/google-research/timesfm.git
cd timesfm && pip install -e ".[torch]"
pip install timesfm-mcp
timesfm-mcp
```

Requires ~16 GB RAM and downloads ~800 MB of model weights on first use. The server auto-detects TimesFM and upgrades to it automatically; no config change needed.

**You don't need TimesFM to get started.** `uvx timesfm-mcp` works instantly with the built-in statistical baseline — no download, no GPU, no extra install.

## Two backends, zero config

| Backend | When active | What it needs |
|---------|------------|---------------|
| **TimesFM 2.5** (Google) | When installed | Install from source — see below |
| Statistical baseline | Always | Just NumPy — already a dependency |

## Tools

| Tool | What it does |
|------|--------------|
| `forecast` | Forecast a single series with optional uncertainty bands |
| `list_backends` | Report which engine is active (timesfm / baseline) |
| `backtest` | Hold out the last N points — compare TimesFM vs baseline MAE/sMAPE |

## Documentation

Full docs in the **[docs/](https://github.com/ramdhavepreetam/timesfm-mcp/tree/main/docs)** folder:

- [Getting Started](https://github.com/ramdhavepreetam/timesfm-mcp/blob/main/docs/getting-started.md) — installation and first forecast
- [Client Setup](https://github.com/ramdhavepreetam/timesfm-mcp/blob/main/docs/client-setup.md) — Claude Desktop, Claude Code, Cursor configs
- [Tool Reference](https://github.com/ramdhavepreetam/timesfm-mcp/blob/main/docs/tool-reference.md) — full parameter docs
- [Cookbook](https://github.com/ramdhavepreetam/timesfm-mcp/blob/main/docs/cookbook.md) — SaaS MRR, e-commerce demand, traffic, cloud spend
- [How It Works](https://github.com/ramdhavepreetam/timesfm-mcp/blob/main/docs/how-it-works.md) — the math and model

## Migrating from forecast-mcp

`timesfm-mcp` is the renamed continuation of `forecast-mcp`. Update your install:

```bash
pip install timesfm-mcp      # replaces: pip install forecast-mcp
uvx timesfm-mcp              # replaces: uvx forecast-mcp
```

Update your agent config: change `"args": ["forecast-mcp"]` → `"args": ["timesfm-mcp"]`.

## License
Apache-2.0
