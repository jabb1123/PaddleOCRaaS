# Production Deployment

Deploy PaddleOCRaaS to production environments.

## Pre-Deployment Checklist

- [ ] Docker image built and tested
- [ ] Database backup strategy in place
- [ ] Reverse proxy configured (nginx/traefik)
- [ ] HTTPS/TLS certificates obtained
- [ ] Firewall rules configured
- [ ] Monitoring/alerting set up
- [ ] Scaling parameters determined
- [ ] Disaster recovery plan

## Deployment Options

### Option 1: Cloud VM (AWS EC2, Azure VM, GCP Compute)

```bash
# 1. Launch instance (Ubuntu 20.04 LTS recommended)
# 2. Install Docker
curl https://get.docker.com | sh

# 3. Clone repository
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS

# 4. Build image
docker build -t paddleocraas:latest .

# 5. Run with persistent storage
docker run -d \
  -p 80:8000 \
  -e PADDLEOCR_HOST=0.0.0.0 \
  -e PADDLEOCR_PORT=8000 \
  -v paddleocr_db:/app \
  --restart unless-stopped \
  --name paddleocr \
  paddleocraas:latest
```

### Option 2: Kubernetes Cluster

See [Kubernetes Guide](kubernetes.md) for full setup.

### Option 3: Managed Container Service

**AWS ECS:**
```bash
# Push to ECR
aws ecr create-repository --repository-name paddleocraas
docker tag paddleocraas:latest <your-account>.dkr.ecr.us-east-1.amazonaws.com/paddleocraas:latest
docker push <your-account>.dkr.ecr.us-east-1.amazonaws.com/paddleocraas:latest

# Create ECS task definition and service
```

**Google Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/paddleocraas

# Deploy
gcloud run deploy paddleocraas \
  --image gcr.io/PROJECT_ID/paddleocraas \
  --platform managed \
  --memory 4Gi \
  --cpu 2
```

## Reverse Proxy Setup

### Nginx Configuration

```nginx
upstream paddleocraas {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Performance settings
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    location / {
        proxy_pass http://paddleocraas;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Large file uploads
        client_max_body_size 100M;
        proxy_request_buffering off;
    }
}
```

## Monitoring & Logging

### Health Checks

```bash
# Monitor health endpoint
curl -f http://localhost:8000/health || systemctl restart paddleocr
```

### Container Logs

```bash
# View logs
docker logs -f paddleocr

# Save logs to file
docker logs paddleocr > logs.txt 2>&1
```

### Resource Monitoring

```bash
# Docker stats
docker stats paddleocr

# System monitoring
top
df -h
```

## Scaling

### Horizontal Scaling (Multiple Instances)

```bash
# Run multiple instances on different ports
docker run -p 8001:8000 paddleocraas:latest &
docker run -p 8002:8000 paddleocraas:latest &
docker run -p 8003:8000 paddleocraas:latest &

# Use nginx upstream to load balance
```

### Vertical Scaling (Increase Resources)

```bash
docker run \
  --cpus=4 \
  --memory=8g \
  paddleocraas:latest \
  python run_app.py --workers 4
```

## Backup & Recovery

### Database Backup

```bash
# Manual backup
cp review_queue.db review_queue.db.$(date +%Y%m%d_%H%M%S).backup

# Automated backup (cron)
0 2 * * * cp /app/review_queue.db /backups/review_queue.db.$(date +\%Y\%m\%d).backup

# Off-site backup
0 3 * * * aws s3 cp /backups/review_queue.db.* s3://my-bucket/backups/
```

### Restore from Backup

```bash
# Stop service
docker stop paddleocr

# Restore database
cp review_queue.db.backup review_queue.db

# Restart
docker start paddleocr
```

## Performance Tuning

### Optimize Image Size

```bash
# Use multi-stage build (optional enhancement)
# Reduces image from 3GB to ~2GB
```

### CPU/GPU Allocation

```bash
# CPU cores for workers
docker run -p 8000:8000 --cpus=4 paddleocraas:latest

# GPU support
docker run --gpus all -p 8000:8000 paddleocraas:latest
```

### Connection Pooling

```bash
# Increase uvicorn workers
python run_app.py --workers 8
```

## Security Hardening

### Add Authentication

```python
# Add API key validation
# Implement rate limiting
# Enable CORS restrictions
```

### Network Security

```bash
# Firewall rules
ufw allow 443/tcp  # HTTPS only
ufw allow 22/tcp   # SSH (if needed)
ufw deny 8000/tcp  # Block direct container access
```

### File Security

```bash
# Restrict database permissions
chmod 600 review_queue.db

# Non-root container user (enhancement)
# Run Docker container as non-root user
```

## Monitoring Dashboard

Example Prometheus metrics (add to monitoring):

```
paddleocr_requests_total{endpoint="/upload"}
paddleocr_processing_duration_seconds
paddleocr_database_size_bytes
paddleocr_container_memory_bytes
paddleocr_gpu_utilization_percent
```

---

**See Also:** [Kubernetes Deployment](kubernetes.md), [Production Checklist](#pre-deployment-checklist)
