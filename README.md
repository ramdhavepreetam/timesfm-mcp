# forecast-mcp

[![CI](https://github.com/preetam/forecast-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/preetam/forecast-mcp/actions/workflows/ci.yml)

**Give any AI agent time-series forecasting superpowers.**

An [MCP](https://modelcontextprotocol.io) server that lets Claude Code, Claude
Desktop, Cursor, or any MCP client forecast a series of numbers — sales, traffic,
usage, costs — and reason about the result. Powered by Google's
[TimesFM 2.5](https://github.com/google-research/timesfm) foundation model, with a
zero-dependency statistical baseline so it works the moment you install it.

## Why

LLM agents can read, write, and run code — but they can't see the future. This
gives them a clean `forecast` tool. The agent calls it, gets point forecasts +
uncertainty bands + a compact trend/seasonality summary, and writes the
explanation and recommendation itself.

## Quickstart (30 seconds)

```bash
uvx forecast-mcp        # runs over stdio for local agents
```

Add to your Claude Desktop / Claude Code config:

```json
{
  "mcpServers": {
    "forecast": { "command": "uvx", "args": ["forecast-mcp"] }
  }
}
```

Then ask your agent: *"Forecast the next 6 months from this revenue data and tell
me what to expect."*

## Enable the foundation model

```bash
pip install "forecast-mcp[timesfm]"
```

The server auto-detects TimesFM and uses it; otherwise it runs the baseline.

## Tools

| Tool | What it does |
|------|--------------|
| `forecast` | Forecast a single series with optional uncertainty bands. |
| `list_backends` | Report which engine is active (timesfm / baseline). |
| `backtest` | Hold out the last N points and compare TimesFM vs baseline performance (MAE/MAPE). |

## License
Apache-2.0
