# Contributing

We welcome contributions to `timesfm-mcp`!

## Development Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

1. Clone the repository.
2. Create an environment and install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```
3. Run tests using `pytest`:
   ```bash
   pytest tests/
   ```

## Guidelines
- The core MCP server must always remain usable *without* heavy ML dependencies. 
- Ensure that the `baseline` backend continues to work robustly for basic statistical predictions.
- The `TimesFMBackend` should be loaded lazily so that it does not block initialization if `timesfm` is not installed.
