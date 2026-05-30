# forecast-mcp

[![CI](https://github.com/ramdhavepreetam/forecast-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ramdhavepreetam/forecast-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/forecast-mcp.svg)](https://pypi.org/project/forecast-mcp/)
[![Docs](https://img.shields.io/badge/docs-GitHub-blue)](https://github.com/ramdhavepreetam/forecast-mcp/tree/main/docs)

**Give any AI agent time-series forecasting superpowers.**

An [MCP](https://modelcontextprotocol.io) server that lets Claude Code, Claude
Desktop, Cursor, or any MCP client forecast a series of numbers — sales, traffic,
usage, costs — and reason about the result. Powered by Google's
[TimesFM 2.5](https://github.com/google-research/timesfm) foundation model, with a
zero-dependency statistical baseline so it works the moment you install it.

![Forecast chart: 24-month MRR history with 6-month point forecast and 90% confidence band](https://raw.githubusercontent.com/ramdhavepreetam/forecast-mcp/main/docs/assets/forecast_preview.png)

*Illustrative — statistical baseline backend. Your agent calls `forecast(values=[...], horizon=6, quantiles=[0.9])` and gets back these numbers plus a plain-language summary.*

## Why

LLM agents can read, write, and run code — but they can't see the future. This
gives them a clean `forecast` tool. The agent calls it, gets point forecasts +
uncertainty bands + a compact trend/seasonality summary, and writes the
explanation and recommendation itself.

## Quickstart (30 seconds)

```bash
uvx forecast-mcp        # runs over stdio for local agents
```

Add to your Claude Desktop / Claude Code / Cursor config:

```json
{
  "mcpServers": {
    "forecast": { "command": "uvx", "args": ["forecast-mcp"] }
  }
}
```

Then ask your agent: *"Forecast the next 6 months from this revenue data and tell me what to expect."*

## Enable the foundation model

```bash
pip install "forecast-mcp[timesfm]"
```

The server auto-detects TimesFM and uses it; otherwise it falls back to the statistical baseline.
Both backends always return a result — no configuration needed.

## Tools

| Tool | What it does |
|------|--------------|
| `forecast` | Forecast a single series with optional uncertainty bands. |
| `list_backends` | Report which engine is active (timesfm / baseline). |
| `backtest` | Hold out the last N points and compare TimesFM vs baseline performance (MAE/sMAPE). |

## Documentation

Full docs in the **[docs/](https://github.com/ramdhavepreetam/forecast-mcp/tree/main/docs)** folder:

- [Getting Started](https://github.com/ramdhavepreetam/forecast-mcp/blob/main/docs/getting-started.md) — installation and first forecast
- [Client Setup](https://github.com/ramdhavepreetam/forecast-mcp/blob/main/docs/client-setup.md) — Claude Desktop, Claude Code, Cursor configs
- [Tool Reference](https://github.com/ramdhavepreetam/forecast-mcp/blob/main/docs/tool-reference.md) — full parameter docs
- [Cookbook](https://github.com/ramdhavepreetam/forecast-mcp/blob/main/docs/cookbook.md) — SaaS MRR, e-commerce demand, traffic, cloud spend
- [How It Works](https://github.com/ramdhavepreetam/forecast-mcp/blob/main/docs/how-it-works.md) — the math and model

## License
Apache-2.0
