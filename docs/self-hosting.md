# Self-Hosting

By default, `forecast-mcp` runs over stdio — the MCP client starts and manages the process. For multi-user or remote deployments, run it as an HTTP server.

## HTTP transport

```bash
forecast-mcp --http
```

Default: `0.0.0.0:8000`. Set `PORT` to change the port:

```bash
PORT=9000 forecast-mcp --http
```

Point any MCP client that supports HTTP transport at `http://your-host:8000`.

## Docker

```dockerfile
FROM python:3.12-slim

RUN pip install forecast-mcp

EXPOSE 8000

CMD ["forecast-mcp", "--http"]
```

Build and run:

```bash
docker build -t forecast-mcp .
docker run -p 8000:8000 forecast-mcp
```

With TimesFM:

```dockerfile
FROM python:3.12-slim

RUN pip install "forecast-mcp[timesfm]"

EXPOSE 8000

CMD ["forecast-mcp", "--http"]
```

!!! note
    The TimesFM image will be ~3 GB and requires a host with at least 4 GB RAM. Model weights are downloaded at first startup.

## Force baseline only

On a resource-constrained host, set the backend env var:

```bash
FORECAST_MCP_BACKEND=baseline forecast-mcp --http
```

This prevents the server from even attempting to import TimesFM.

## Health check

The HTTP server doesn't currently expose a `/health` endpoint. Use a simple TCP check or monitor the process.

## Security note

The server does not implement authentication. Do not expose `forecast-mcp --http` directly on a public interface without a reverse proxy with auth (e.g. nginx + basic auth or a JWT middleware). For internal use behind a VPN, the default config is fine.

## Reverse proxy example (nginx)

```nginx
server {
    listen 80;
    server_name forecast.internal;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
