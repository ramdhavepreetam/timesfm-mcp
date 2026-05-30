# Client Setup

Paste the config block for your agent. You only need to do this once.

## Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["forecast-mcp"]
    }
  }
}
```

Restart Claude Desktop. You'll see "forecast" appear in the MCP tools panel.

### With TimesFM enabled

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["--from", "forecast-mcp[timesfm]", "forecast-mcp"]
    }
  }
}
```

!!! note
    TimesFM downloads ~800 MB of model weights on first use. Allow 1–2 minutes on the first invocation.

## Claude Code

Add to your project's `.mcp.json`, or run the CLI command:

```bash
claude mcp add forecast -- uvx forecast-mcp
```

Or manually in `.mcp.json`:

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["forecast-mcp"]
    }
  }
}
```

Verify it's active:

```
/mcp
```

You should see `forecast` listed with tools `forecast`, `list_backends`, `backtest`.

## Cursor

Open **Settings → MCP** (or `~/.cursor/mcp.json`) and add:

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["forecast-mcp"]
    }
  }
}
```

Restart Cursor. The forecast tools are now available to Cursor's agent.

## Any other MCP client

The server speaks the standard MCP stdio transport. Start it with:

```bash
uvx forecast-mcp          # stdio (default)
forecast-mcp --http       # HTTP transport on port 8000
```

Set `PORT` to change the HTTP port:

```bash
PORT=9000 forecast-mcp --http
```

## Environment variables

| Variable | Default | Effect |
|----------|---------|--------|
| `FORECAST_MCP_BACKEND` | `auto` | Set to `baseline` to force the statistical backend even when TimesFM is installed |
| `PORT` | `8000` | HTTP port (only used with `--http`) |

## Troubleshooting

**"No tools found"** — Check that `uvx` is on your PATH (`which uvx`). Install with `pip install uv` or `brew install uv`.

**TimesFM import error** — Run `pip install "forecast-mcp[timesfm]"` and restart the server.

**Server not responding** — Check the MCP logs in your client. The server logs startup info to stderr.
