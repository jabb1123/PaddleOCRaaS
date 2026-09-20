# Docker Quick Start

Get started with Docker in 2 minutes.

## Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/products/docker-desktop))

## Build & Run

### Step 1: Build Image
```bash
docker build -t paddleocraas:latest .
```

### Step 2: Run Container
```bash
docker run -p 8000:8000 paddleocraas:latest
```

### Step 3: Open in Browser
Visit: **http://localhost:8000/static/index.html**

## That's It! 🎉

Upload a file and test OCR processing.

---

## Common Variants

### Custom Port
```bash
docker run -p 5000:8000 paddleocraas:latest
# Visit: http://localhost:5000
```

### Persistent Database
```bash
docker run -p 8000:8000 -v paddleocr_db:/app paddleocraas:latest
# Database survives container restarts
```

### Using Docker Compose
```bash
docker-compose up -d
docker-compose down  # to stop
```

---

## Next Steps
- [Docker Overview](overview.md) - Learn more about Docker setup
- [Configuration](configuration.md) - Advanced configuration
- [Troubleshooting](../development/troubleshooting.md) - Having issues?

---

**Tip**: For persistent storage in production, always use the volume mount (`-v paddleocr_db:/app`)
