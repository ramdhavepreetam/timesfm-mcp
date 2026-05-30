# Launching `forecast-mcp`: Give your AI Agents Time-Series Forecasting Superpowers

Have you ever tried to make an AI agent predict the future? Language models are brilliant at reasoning, but they notoriously struggle with numeric time-series prediction out of the box. 

Today, we're releasing **`forecast-mcp`**, an open-source MCP server that gives agents native access to robust forecasting.

### Why use `forecast-mcp`?
* **Instant Start (No ML bloat)**: The server defaults to a statistical baseline (seasonal-naive + trend) that is fast, mathematically sound, and installs in milliseconds.
* **Google's TimesFM 2.5 Support**: If you need the heavy-hitting foundation model, `forecast-mcp` lazily loads and wraps Google's new 200M parameter TimesFM 2.5 model. Your agents can automatically predict massive series natively.
* **Backtesting Built-in**: We've included a `backtest` tool that calculates MAE and sMAPE, allowing agents to mathematically prove that their forecasting choices are robust before presenting them to users.

### Quickstart
With [MCP](https://modelcontextprotocol.io), adding forecasting to your favorite agent (like Claude Code, Cursor, or Claude Desktop) is just one line:

```bash
uvx forecast-mcp
```

Check out the repo here: [https://github.com/preetam/forecast-mcp](https://github.com/preetam/forecast-mcp)
