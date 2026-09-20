# Docker Compose Setup

Complete orchestration with docker-compose.yml.

## Quick Start

```bash
docker-compose up -d
docker-compose down
```

## File Overview

The `docker-compose.yml` includes:
- **Service**: `paddleocraas` container with PaddleOCRaaS application
- **Ports**: Configurable external port (default 8000)
- **Volumes**: Named volume `paddleocr_db` for persistent storage
- **Network**: Custom bridge network for service communication
- **Health Checks**: Automatic monitoring via /health endpoint
- **Restart Policy**: `unless-stopped` for automatic recovery

## Configuration

### Environment Variables

Edit `.env` or set via environment:

```bash
PADDLEOCR_PORT=8000
```

### Port Mapping

Default mapping: `8000:8000` (external:internal)

Change external port:
```bash
PADDLEOCR_PORT=5000 docker-compose up -d
# Access at: http://localhost:5000
```

### Persistent Storage

Database stored in named volume `paddleocr_db`:

```bash
# View volume location
docker volume inspect paddleocr_db

# Backup volume
docker run --rm -v paddleocr_db:/app -v $(pwd):/backup \
  alpine tar czf /backup/db.tar.gz -C /app .

# Restore volume
docker run --rm -v paddleocr_db:/app -v $(pwd):/backup \
  alpine tar xzf /backup/db.tar.gz -C /app
```

## Common Commands

### Start Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f paddleocraas
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### Restart Service
```bash
docker-compose restart paddleocraas
```

### Execute Command in Container
```bash
docker-compose exec paddleocraas bash
```

### View Service Status
```bash
docker-compose ps
```

## Scaling

Run multiple instances:

```bash
docker-compose up -d --scale paddleocraas=3
```

Then use a load balancer (nginx, traefik) to distribute traffic.

---

**Next**: See [Configuration Guide](configuration.md) for advanced options.
