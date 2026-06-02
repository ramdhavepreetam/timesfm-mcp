# Client Setup

Paste the config block for your agent. You only need to do this once.

## Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["timesfm-mcp"]
    }
  }
}
```

Restart Claude Desktop. You'll see "forecast" appear in the MCP tools panel.

### With TimesFM enabled

!!! warning "System requirement: ≥ 16 GB RAM · ~800 MB disk"
    TimesFM downloads ~800 MB of model weights on first use and requires at least
    16 GB of RAM. **Most users should use the `uvx` baseline config above** —
    it works on any machine with no download.

```bash
pip install "timesfm-mcp[timesfm]"
```

Then update your Claude Desktop config to use the installed binary instead of `uvx`:

```json
{
  "mcpServers": {
    "forecast": {
      "command": "timesfm-mcp"
    }
  }
}
```

Allow 1–2 minutes on the first invocation while model weights download and load.

## Claude Code

Add to your project's `.mcp.json`, or run the CLI command:

```bash
claude mcp add forecast -- uvx timesfm-mcp
```

Or manually in `.mcp.json`:

```json
{
  "mcpServers": {
    "forecast": {
      "command": "uvx",
      "args": ["timesfm-mcp"]
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
      "args": ["timesfm-mcp"]
    }
  }
}
```

Restart Cursor. The forecast tools are now available to Cursor's agent.

## Any other MCP client

The server speaks the standard MCP stdio transport. Start it with:

```bash
uvx timesfm-mcp          # stdio (default)
timesfm-mcp --http       # HTTP transport on port 8000
```

Set `PORT` to change the HTTP port:

```bash
PORT=9000 timesfm-mcp --http
```

## Environment variables

| Variable | Default | Effect |
|----------|---------|--------|
| `TIMESFM_MCP_BACKEND` | `auto` | Set to `baseline` to force the statistical backend even when TimesFM is installed |
| `PORT` | `8000` | HTTP port (only used with `--http`) |

## Troubleshooting

**"No tools found"** — Check that `uvx` is on your PATH (`which uvx`). Install with `pip install uv` or `brew install uv`.

**TimesFM import error** — Run `pip install "timesfm-mcp[timesfm]"` and restart the server. If `pip install timesfm` was previously run separately, uninstall it first (`pip uninstall timesfm`) to avoid the old 1.x version shadowing the bundled 2.5 source.

**Server not responding** — Check the MCP logs in your client. The server logs startup info to stderr.
