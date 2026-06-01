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

### With TimesFM enabled (advanced)

TimesFM 2.5 is not on PyPI — install it from source into a virtualenv first:

```bash
git clone https://github.com/google-research/timesfm.git
cd timesfm && pip install -e ".[torch]"
pip install timesfm-mcp
```

Then point Claude Desktop at the `timesfm-mcp` binary in that environment:

```json
{
  "mcpServers": {
    "forecast": {
      "command": "/path/to/your/venv/bin/timesfm-mcp"
    }
  }
}
```

Replace `/path/to/your/venv` with the path to the virtualenv where you installed both packages (e.g. `~/.venvs/timesfm`).

!!! note
    TimesFM requires ~16 GB RAM and downloads ~800 MB of model weights on first use. Allow 1–2 minutes on the first invocation. Most users should use the `uvx` baseline config above.

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

**TimesFM import error** — TimesFM 2.5 must be installed from source (see "With TimesFM enabled" above). `pip install timesfm` installs an old 1.x release with a different API and will not work.

**Server not responding** — Check the MCP logs in your client. The server logs startup info to stderr.
