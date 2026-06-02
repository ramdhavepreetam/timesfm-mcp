# Self-Hosting

By default, `timesfm-mcp` runs over stdio — the MCP client starts and manages the process. For multi-user or remote deployments, run it as an HTTP server.

## HTTP transport

```bash
timesfm-mcp --http
```

Default: `0.0.0.0:8000`. Set `PORT` to change the port:

```bash
PORT=9000 timesfm-mcp --http
```

Point any MCP client that supports HTTP transport at `http://your-host:8000`.

## Docker

```dockerfile
FROM python:3.12-slim

RUN pip install timesfm-mcp

EXPOSE 8000

CMD ["timesfm-mcp", "--http"]
```

Build and run:

```bash
docker build -t timesfm-mcp .
docker run -p 8000:8000 timesfm-mcp
```

With TimesFM:

```dockerfile
FROM python:3.12-slim

RUN pip install "timesfm-mcp[timesfm]"

EXPOSE 8000

CMD ["timesfm-mcp", "--http"]
```

!!! note
    The TimesFM image requires ~16 GB RAM on the host. Model weights (~800 MB) are downloaded at first startup. For most deployments, the baseline-only image above is the right choice.

## Force baseline only

On a resource-constrained host, set the backend env var:

```bash
TIMESFM_MCP_BACKEND=baseline timesfm-mcp --http
```

This prevents the server from even attempting to import TimesFM.

## Health check

The HTTP server doesn't currently expose a `/health` endpoint. Use a simple TCP check or monitor the process.

## Security note

The server does not implement authentication. Do not expose `timesfm-mcp --http` directly on a public interface without a reverse proxy with auth (e.g. nginx + basic auth or a JWT middleware). For internal use behind a VPN, the default config is fine.

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
