# Docker Overview

Learn how to deploy PaddleOCRaaS using Docker for consistent, reproducible environments.

## Why Docker?

### Benefits
- 🔄 **Consistency** - Same environment across development, testing, and production
- 📦 **Isolation** - No conflicts with system libraries or other projects
- 🚀 **Portability** - Run on any machine with Docker installed
- 📈 **Scalability** - Easy to scale horizontally with orchestration
- 🛠️ **Maintenance** - Simplified dependency management
- ☁️ **Cloud Ready** - Deploy to AWS, GCP, Azure, Kubernetes, etc.

### Disadvantages Overcome
- Slightly larger disk footprint (~3GB for image)
- Learning curve for Docker commands
- Monitoring complexity in multi-container setups

---

## Docker Files Provided

| File | Purpose |
|------|---------|
| **Dockerfile** | Container image definition |
| **docker-compose.yml** | Multi-container orchestration |
| **.dockerignore** | Build optimization |
| **docker-build.sh** | Unix/Linux/Mac helper script |
| **docker-build.bat** | Windows batch script |
| **requirements-docs.txt** | Documentation build dependencies |

---

## 🏗️ Architecture

### Single Container
```
┌─────────────────────────────────────┐
│    Docker Container                 │
│  ┌───────────────────────────────┐  │
│  │  Python 3.10 Slim Base        │  │
│  │  ├── System Libraries         │  │
│  │  ├── Python Packages          │  │
│  │  └── Application Code         │  │
│  │      ├── main.py              │  │
│  │      ├── review_queue.py      │  │
│  │      ├── run_app.py           │  │
│  │      └── static/              │  │
│  └───────────────────────────────┘  │
│  Port 8000 (configurable)           │
│  Volume: /app (database, uploads)   │
└─────────────────────────────────────┘
```

### Docker Compose Setup
```
┌──────────────────────────────────────────┐
│       Docker Compose Network             │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  paddleocraas Service              │ │
│  │  - Port mapping: 8000:8000         │ │
│  │  - Environment variables           │ │
│  │  - Volume: paddleocr_db:/app       │ │
│  │  - Auto-restart: unless-stopped    │ │
│  └────────────────────────────────────┘ │
│            │                             │
│            ▼                             │
│  ┌────────────────────────────────────┐ │
│  │  Named Volume: paddleocr_db        │ │
│  │  - Persistent storage              │ │
│  │  - Survives container restarts     │ │
│  │  - Can be backed up                │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

---

## 📋 Image Contents

### Base Image
- **OS**: Debian Slim (minimal)
- **Python**: 3.10
- **Size**: ~3GB total (with dependencies)

### System Dependencies
```
libsm6              # OpenCV video I/O support
libxext6            # X11 extensions (GUI support)
libxrender-dev      # X11 rendering support
libgomp1            # OpenMP support (threading)
libglib2.0-0        # GLib library
libgl1-mesa-glx     # OpenGL support
build-essential     # C/C++ compiler (for pip installs)
```

### Python Packages
From `requirements.txt`:
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **PaddleOCR** - OCR engine
- **PaddlePaddle** - Deep learning framework
- **OpenCV** - Image processing
- **PyMuPDF** - PDF processing
- **NumPy** - Numerical computing
- And 12+ more...

---

## 🚀 Quick Start

### Build

```bash
docker build -t paddleocraas:latest .
```

### Run (Basic)

```bash
docker run -p 8000:8000 paddleocraas:latest
```

### Run (Production)

```bash
docker run -p 8080:8000 \
  -e PADDLEOCR_HOST=0.0.0.0 \
  -e PADDLEOCR_PORT=8000 \
  -v paddleocr_db:/app \
  --name paddleocr_prod \
  --restart unless-stopped \
  paddleocraas:latest
```

### Docker Compose

```bash
docker-compose up -d
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| PADDLEOCR_HOST | 0.0.0.0 | Bind address (0.0.0.0 for external, 127.0.0.1 for local) |
| PADDLEOCR_PORT | 8000 | Internal port (container port) |

### Port Mapping

```bash
# External:Internal port mapping
docker run -p EXTERNAL:INTERNAL paddleocraas:latest

# Examples
docker run -p 8000:8000        # localhost:8000
docker run -p 5000:8000        # localhost:5000
docker run -p 80:8000          # localhost:80 (requires root on Unix)
docker run -p 192.168.1.1:5000:8000  # Specific IP:port
```

### Volumes

```bash
# Named volume (recommended)
docker run -v paddleocr_db:/app paddleocraas:latest

# Bind mount (local directory)
docker run -v /home/user/data:/app/data paddleocraas:latest

# Multiple volumes
docker run \
  -v paddleocr_db:/app \
  -v /home/user/uploads:/app/uploads \
  paddleocraas:latest
```

---

## 📊 Performance Tuning

### CPU & Memory

```bash
# Limit resources
docker run \
  --cpus=2.0 \
  --memory=4g \
  -p 8000:8000 \
  paddleocraas:latest
```

### Multiple Workers

```bash
# Run with 4 worker processes
docker run -p 8000:8000 paddleocraas:latest \
  python run_app.py --workers 4
```

### GPU Support

```bash
# Enable NVIDIA GPU
docker run --gpus all \
  -p 8000:8000 \
  paddleocraas:latest

# Specific GPU
docker run --gpus '"device=0"' \
  -p 8000:8000 \
  paddleocraas:latest
```

---

## 🏥 Health Checks

### Endpoint
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Docker Health Status
```bash
# Check container health
docker ps | grep paddleocraas

# View detailed health info
docker inspect <container_id> | grep -A5 Health
```

### Automatic Monitoring
- Health check interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3 consecutive failures marks unhealthy
- Grace period: 5 seconds after start

---

## 📁 Storage Management

### Database Location
```bash
# Inside container
/app/review_queue.db

# On host machine (with named volume)
docker volume inspect paddleocr_db
# View mount point
```

### Backup Database

```bash
# Copy database out
docker cp paddleocr_server:/app/review_queue.db ./backup.db

# Copy database in
docker cp ./backup.db paddleocr_server:/app/review_queue.db
```

### Persistent Storage Scenarios

**Development (Quick Testing)**
```bash
docker run -p 8000:8000 paddleocraas:latest
# Database lost on container stop (OK for testing)
```

**Production (Persistent)**
```bash
docker run -p 8000:8000 \
  -v paddleocr_db:/app \
  --restart unless-stopped \
  paddleocraas:latest
# Database survives container restarts
```

**Shared Data (Team Development)**
```bash
docker run -p 8000:8000 \
  -v /shared/paddleocr_data:/app \
  paddleocraas:latest
# Shared across team via NFS mount
```

---

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker logs <container_id>

# Run with verbose output
docker run -it paddleocraas:latest bash
```

### Port already in use
```bash
# Find process using port
lsof -i :8000  # Unix/Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
docker run -p 9000:8000 paddleocraas:latest
```

### Out of memory
```bash
# Increase memory limit
docker run --memory=8g paddleocraas:latest

# Or limit model caching
docker run -e PADDLE_MODEL_CACHE=/tmp paddleocraas:latest
```

### Network issues
```bash
# Test from inside container
docker exec <container_id> curl http://localhost:8000/health

# Test DNS resolution
docker exec <container_id> nslookup google.com
```

---

## 🔐 Security Considerations

### Network Security
- Don't expose 0.0.0.0 on public internet without reverse proxy
- Use nginx/traefik as reverse proxy with TLS
- Implement firewall rules

### Volume Security
- Named volumes more secure than bind mounts
- Restrict file permissions on bind mount directories
- Back up database regularly

### Application Security
- No authentication currently (add if exposed)
- Consider API keys or OAuth2 for production
- Validate file uploads

### Container Security
- Run with non-root user (optional enhancement)
- Use read-only filesystem where possible
- Scan image for vulnerabilities

---

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml with load balancer
version: '3.8'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - app1
      - app2
  
  app1:
    build: .
    expose:
      - 8000
  
  app2:
    build: .
    expose:
      - 8000
```

### Vertical Scaling
```bash
# Increase resources
docker run \
  --cpus=8.0 \
  --memory=16g \
  --workers 8 \
  paddleocraas:latest
```

---

## 🚀 Next Steps

### Deployment Options
- [Local Development](local-dev.md) - Single container for testing
- [Production Deployment](../deployment/production.md) - Multi-container setup
- [Docker Compose Setup](docker-compose.md) - Using docker-compose.yml
- [Kubernetes](../deployment/kubernetes.md) - Enterprise orchestration

### Learn More
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Status**: ✅ Ready for production deployment
