# Frequently Asked Questions

Quick answers to common questions about PaddleOCRaaS.

## Installation & Setup

### Q: What Python version do I need?
**A:** Python 3.10 exactly. Python 3.14 is incompatible with PaddleOCR, and NumPy 2.x breaks dependencies. Use `python --version` to check.

### Q: Can I use Docker instead of local Python?
**A:** Yes! Docker is recommended for first-time users. It avoids all dependency issues. Just run:
```bash
docker build -t paddleocraas:latest .
docker run -p 8000:8000 paddleocraas:latest
```

### Q: How much disk space do I need?
**A:** 
- Application code: ~50MB
- Python dependencies: ~500MB
- PaddleOCR models: ~1GB (downloaded on first run)
- Database: Depends on documents (typically <100MB for hundreds of documents)
- **Total: 2-3GB recommended**

### Q: Can I use a different port than 8000?
**A:** Yes! 
```bash
python run_app.py --port 5000
# or
docker run -p 5000:8000 paddleocraas:latest
```

---

## Running & Operations

### Q: How do I check if the server is running?
**A:** Test the health endpoint:
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Q: Can multiple people access it at the same time?
**A:** Yes! FastAPI/Uvicorn handles concurrent requests. For better performance, use multiple workers:
```bash
python run_app.py --workers 4
```

### Q: Can I access it from another machine?
**A:** Yes, configure the host to `0.0.0.0`:
```bash
python run_app.py --host 0.0.0.0
# Then access from another machine: http://<your-machine-ip>:8000
```

### Q: How do I backup my database?
**A:** The database is `review_queue.db` in the project folder:
```bash
# Copy the file
cp review_queue.db review_queue.db.backup
```

With Docker volumes:
```bash
docker cp paddleocr_server:/app/review_queue.db ./backup.db
```

### Q: Can I move the database to another location?
**A:** Currently it's at the project root. To change location:
1. Move `review_queue.db` to desired location
2. Update file path in `main.py` (line with `review_queue.init_db()`)
3. Restart application

---

## OCR & Processing

### Q: How long does OCR processing take?
**A:** 
- **Single page, GPU**: 2-5 seconds
- **Single page, CPU**: 10-30 seconds
- **Multi-page PDF**: ~5 seconds per page on GPU
- First run: +2-3 minutes to download/cache models

### Q: Why is OCR quality poor?
**A:** Common issues:
- Low resolution scans (<150 DPI)
- Poor lighting or shadows
- Handwriting too illegible
- Rotated pages
- Mixed languages

**Solutions:**
- Use higher resolution images (200+ DPI)
- Scan with good lighting
- Pre-process images if needed
- Rotate pages to correct orientation

### Q: Can it handle multiple languages?
**A:** Yes, PaddleOCR supports 80+ languages. English-focused optimization in this build, but multilingual text is supported.

### Q: Can it recognize cursive handwriting?
**A:** Somewhat, but it's more accurate with print handwriting. Cursive recognition varies by writing style and clarity.

### Q: How accurate is it typically?
**A:** 
- **Printed text**: 95-99% character accuracy
- **Handwritten text**: 70-90% depending on clarity
- **Mixed text**: 80-95%

Always review extracted tasks before approving.

---

## Docker

### Q: What Docker version do I need?
**A:** Docker 20.10 or newer. Check with `docker --version`.

### Q: How much disk space does the Docker image take?
**A:** ~3GB for the built image (includes OS, Python, dependencies, models).

### Q: Can I use Docker Compose instead of docker run?
**A:** Yes! Recommended for persistent storage:
```bash
docker-compose up -d
docker-compose down  # to stop
```

### Q: How do I see Docker logs?
**A:** 
```bash
# Compose
docker-compose logs -f paddleocraas

# Manual container
docker logs -f <container_id>
```

### Q: Can I use GPU with Docker?
**A:** Yes, install nvidia-docker and run:
```bash
docker run --gpus all -p 8000:8000 paddleocraas:latest
```

### Q: How do I stop the Docker container?
**A:** 
```bash
# Graceful stop
docker stop <container_id>

# Force stop
docker kill <container_id>

# Compose
docker-compose down
```

---

## Deployment & Production

### Q: Can I use this in production?
**A:** Yes! But consider:
- Add authentication/API keys
- Use reverse proxy (nginx)
- Set up monitoring
- Back up database regularly
- Use HTTPS/TLS
- Implement rate limiting

### Q: How do I deploy to AWS/GCP/Azure?
**A:** Options:
1. Push Docker image to container registry
2. Deploy using your cloud provider's container service
3. Use Kubernetes for complex setups

See [Deployment Guide](deployment/production.md) for details.

### Q: Can I run it on Kubernetes?
**A:** Yes! YAML examples provided in [Kubernetes Guide](deployment/kubernetes.md).

### Q: How do I scale to handle more documents?
**A:** 
- Use multiple workers: `--workers 4`
- Increase memory: `--memory=8g`
- Enable GPU: `--gpus all`
- Use load balancer for multiple instances

---

## Database & Data

### Q: Where is the database stored?
**A:** `review_queue.db` in the project root (SQLite file).

### Q: Can I use PostgreSQL or MySQL instead?
**A:** Currently SQLite only. PostgreSQL support could be added (file a feature request on GitHub).

### Q: How do I export the data?
**A:** 
```bash
# Export to CSV
sqlite3 review_queue.db "SELECT * FROM tasks;" > tasks.csv

# Or use any SQLite browser tool
```

### Q: How do I view the database?
**A:** 
```bash
# Command line
sqlite3 review_queue.db
# Then: .tables (to see tables), SELECT * FROM tasks;

# GUI tools
# - DB Browser for SQLite (free)
# - DBeaver (free, comprehensive)
# - VS Code SQLite extension
```

### Q: Can I delete old records?
**A:** Yes, directly in SQLite:
```bash
sqlite3 review_queue.db "DELETE FROM tasks WHERE date(created_at) < date('now', '-30 days');"
```

### Q: How do I reset everything?
**A:** 
```bash
# Stop the app
# Backup first!
cp review_queue.db review_queue.db.backup

# Delete the database
rm review_queue.db

# Restart app
python run_app.py
# New empty database will be created
```

---

## Web Interface

### Q: Why do some special characters display incorrectly?
**A:** Fixed in recent version. Uses HTML5 data attributes for safe character handling. If still seeing issues, clear browser cache or try incognito mode.

### Q: Can I upload multiple files at once?
**A:** Currently one at a time. Multi-file upload could be added (feature request on GitHub).

### Q: How do I search for tasks?
**A:** Currently no search UI, but you can filter via the API or database:
```bash
curl "http://localhost:8000/api/queue?status=pending"
```

### Q: Can I export approved tasks?
**A:** Not through UI currently. Export from database:
```bash
sqlite3 review_queue.db "SELECT * FROM tasks WHERE status='approved';" > approved_tasks.csv
```

### Q: Is the web interface mobile-friendly?
**A:** Somewhat. Desktop experience is better. Mobile optimizations could be added.

---

## API & Integration

### Q: Can I use this as an API?
**A:** Yes! FastAPI provides REST endpoints. See [API Reference](api/rest.md) for all endpoints.

### Q: How do I authenticate API requests?
**A:** Currently no authentication. Add API keys or OAuth2 if needed (feature request).

### Q: Can I integrate this with my application?
**A:** Yes! Use REST API endpoints to:
- Upload documents
- Retrieve tasks
- Approve/reject/edit tasks
- Get OCR results

See [API Documentation](api/rest.md) for examples.

---

## Troubleshooting

### Q: "Port 8000 already in use"
**A:** 
```bash
# Use different port
python run_app.py --port 9000

# Or find and stop what's using 8000
lsof -i :8000  # Check
kill -9 <PID>  # Kill (if it's yours)
```

### Q: "ModuleNotFoundError: No module named 'paddleocr'"
**A:** 
```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Q: "CUDA/GPU not recognized"
**A:** 
```bash
# Check if GPU available
python -c "import paddle; print(paddle.device.get_device())"

# If CPU only, that's OK (just slower)
# Or install CUDA 12.0+ and try again
```

### Q: "Out of memory" error
**A:** 
- Close other applications
- Reduce file size/page count
- Use smaller PDF/image resolution
- Increase system RAM

### Q: Database appears corrupted
**A:** 
```bash
# Backup original
cp review_queue.db review_queue.db.corrupted

# Check for corruption
sqlite3 review_queue.db "PRAGMA integrity_check;"

# If corrupted, reset
rm review_queue.db
python run_app.py  # Creates fresh DB
```

---

## Performance & Monitoring

### Q: How can I monitor performance?
**A:** 
```bash
# Docker resource usage
docker stats <container_id>

# Server logs show timing
# Check console output for processing duration
```

### Q: How do I optimize for large files?
**A:** 
- Use GPU (10x faster than CPU)
- Enable multiple workers for concurrent uploads
- Increase memory/CPU allocation
- Consider processing in batches

### Q: Can I see detailed logs?
**A:** 
```bash
# View logs
docker-compose logs -f

# Adjust log level in code if needed
```

---

## Security

### Q: Is my data secure?
**A:** 
- Database stored locally by default
- No data sent to external services
- Deploy behind firewall/reverse proxy for production
- Consider adding authentication

### Q: Can I use HTTPS?
**A:** Yes, deploy behind nginx/reverse proxy with TLS certificate. See [Production Guide](deployment/production.md).

### Q: What about file upload security?
**A:** Currently accepts any PDF/image. In production:
- Validate file types strictly
- Scan uploads for malware
- Limit file size
- Run in sandboxed environment

---

## Contributing

### Q: Can I contribute?
**A:** Yes! See [Contributing Guide](development/contributing.md). We welcome:
- Bug reports
- Feature requests
- Code contributions
- Documentation improvements

### Q: How do I report bugs?
**A:** Open an issue on GitHub with:
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Your environment (OS, Python version, etc.)

### Q: How do I request features?
**A:** Open a GitHub issue with description of what you need and why.

---

## Other Questions?

Can't find the answer? 

- 📖 Check [Documentation](../index.md)
- 💬 Open a [GitHub Issue](https://github.com/yourusername/PaddleOCRaaS/issues)
- 📧 Contact via GitHub
- 🔍 Search existing issues

---

**Last Updated**: September 2026
