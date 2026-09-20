# Configuration Guide

Configure PaddleOCRaaS for your deployment scenario.

## Environment Variables

### PADDLEOCR_HOST
**Default**: `0.0.0.0` (in Docker) / `127.0.0.1` (local)

Controls which network interface the server binds to:
- `127.0.0.1` - Localhost only (not accessible from other machines)
- `0.0.0.0` - All interfaces (accessible from any machine on the network)
- `192.168.1.10` - Specific IP address

### PADDLEOCR_PORT
**Default**: `8000`

Which port the server listens on.

## Setting Environment Variables

### Local Python

=== "Linux/macOS"
    ```bash
    export PADDLEOCR_HOST=0.0.0.0
    export PADDLEOCR_PORT=8000
    python run_app.py
    ```

=== "Windows (PowerShell)"
    ```powershell
    $env:PADDLEOCR_HOST = "0.0.0.0"
    $env:PADDLEOCR_PORT = "8000"
    python run_app.py
    ```

=== "Windows (Command Prompt)"
    ```cmd
    set PADDLEOCR_HOST=0.0.0.0
    set PADDLEOCR_PORT=8000
    python run_app.py
    ```

### Docker

```bash
docker run \
  -p 8000:8000 \
  -e PADDLEOCR_HOST=0.0.0.0 \
  -e PADDLEOCR_PORT=8000 \
  paddleocraas:latest
```

### Docker Compose

Edit `docker-compose.yml` or use environment file `.env`.

## CLI Arguments

Override environment variables with command-line arguments:

```bash
python run_app.py --host 0.0.0.0 --port 8000 --workers 4
```

### Available Arguments
- `--host HOST` - Server bind address
- `--port PORT` - Server port
- `--workers WORKERS` - Number of worker processes

## Configuration Precedence

CLI arguments override environment variables, which override defaults:

```
CLI args > Environment variables > Defaults
```

Example:
```bash
# Environment variable set
export PADDLEOCR_PORT=5000

# CLI argument overrides it
python run_app.py --port 8000  # Uses 8000, not 5000
```

## Common Scenarios

### Local Development
```bash
python run_app.py
# Runs on 127.0.0.1:8000 (localhost only)
```

### Team Development (Same Network)
```bash
python run_app.py --host 0.0.0.0
# Runs on 0.0.0.0:8000 (accessible from other machines)
```

### Multiple Instances
```bash
python run_app.py --port 8000
python run_app.py --port 8001
python run_app.py --port 8002
# Use load balancer to distribute traffic
```

### High Performance
```bash
python run_app.py --host 0.0.0.0 --port 8000 --workers 4
# 4 worker processes for better concurrency
```

### Docker Production
```bash
docker run \
  -p 80:8000 \
  -e PADDLEOCR_HOST=0.0.0.0 \
  -e PADDLEOCR_PORT=8000 \
  -v paddleocr_db:/app \
  --restart unless-stopped \
  paddleocraas:latest
```

---

**Next**: See [Docker Compose Setup](docker-compose.md) for orchestration configuration.
