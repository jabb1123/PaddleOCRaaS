# Troubleshooting Guide

Common issues and solutions for PaddleOCRaaS.

## Installation Issues

### Issue: Python 3.10 not found

**Error:**
```
python: command not found
```

**Solutions:**
1. Check installed Python version: `python --version`
2. Use `python3.10` if available
3. Install Python 3.10:
   - **macOS**: `brew install python@3.10`
   - **Ubuntu**: `sudo apt install python3.10`
   - **Windows**: Download from python.org

### Issue: pip install fails

**Error:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solutions:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try again
pip install -r requirements.txt

# Or with no cache
pip install --no-cache-dir -r requirements.txt
```

### Issue: Virtual environment not activating

**Solutions:**

=== "Linux/macOS"
    ```bash
    # Verify .venv exists
    ls -la .venv/
    
    # Reactivate
    source .venv/bin/activate
    
    # Check if activated (should show .venv in prompt)
    which python
    ```

=== "Windows"
    ```cmd
    # Verify .venv exists
    dir .venv\
    
    # Reactivate
    .venv\Scripts\activate.bat
    
    # Or PowerShell
    .venv\Scripts\Activate.ps1
    ```

### Issue: "ModuleNotFoundError: No module named 'paddleocr'"

**Error:**
```
ModuleNotFoundError: No module named 'paddleocr'
```

**Solutions:**
1. Verify virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip uninstall paddlepaddle paddleocr paddlex -y
   pip install paddlepaddle==3.3.1 paddleocr==2.7.3 paddlex==3.0.1
   ```

---

## Running Application

### Issue: "Port 8000 already in use"

**Error:**
```
Address already in use
```

**Solutions:**

=== "Linux/macOS"
    ```bash
    # Find process using port
    lsof -i :8000
    
    # Kill process
    kill -9 <PID>
    
    # Or use different port
    python run_app.py --port 9000
    ```

=== "Windows"
    ```cmd
    # Find process using port
    netstat -ano | findstr :8000
    
    # Kill process
    taskkill /PID <PID> /F
    
    # Or use different port
    python run_app.py --port 9000
    ```

### Issue: "Connection refused" when accessing http://localhost:8000

**Error:**
```
Connection refused
ERROR: Failed to connect
```

**Solutions:**
1. Check if server is running
2. Verify correct host/port:
   ```bash
   python run_app.py --host 127.0.0.1 --port 8000
   ```
3. Check firewall isn't blocking port
4. Try explicit IP: `http://127.0.0.1:8000`

### Issue: Web UI won't load

**Error:**
```
Page not found
404 Not Found
```

**Solutions:**
1. Check URL: http://localhost:8000/static/index.html (not just http://localhost:8000)
2. Clear browser cache: `Ctrl+Shift+Delete` (or Cmd+Shift+Delete on Mac)
3. Try incognito/private mode
4. Check browser console for errors (F12 → Console)

### Issue: Health endpoint not responding

**Error:**
```
curl: Failed to connect
```

**Solutions:**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Check logs
# Look at server console output
```

---

## OCR Processing

### Issue: OCR processing very slow

**Cause:** Running on CPU instead of GPU

**Solutions:**
1. Check GPU availability:
   ```bash
   python -c "import paddle; print(paddle.device.get_device())"
   ```
2. Install NVIDIA CUDA 12.0+ if GPU available
3. Reduce file size/page count
4. Increase system resources

### Issue: "Out of memory" error during OCR

**Error:**
```
RuntimeError: CUDA out of memory
# or
MemoryError: Unable to allocate memory
```

**Solutions:**
1. Close other applications
2. Reduce PDF/image file size
3. Process one page at a time
4. Increase system memory
5. Use CPU instead of GPU:
   ```python
   # In code
   paddle.set_device('cpu')
   ```

### Issue: OCR quality is poor

**Symptoms:**
- Many words misrecognized
- Low confidence scores (<0.75)

**Solutions:**
1. Use higher resolution scans (200+ DPI)
2. Ensure good lighting when scanning
3. Straighten skewed pages
4. Remove background noise/shadows
5. Use clearer handwriting
6. Try different image preprocessing

---

## Web Interface

### Issue: "Invalid character" errors with special characters

**Error:**
```
JavaScript error in console
Task text with quotes fails to save
```

**Solutions:**
- Already fixed in current version
- Clear browser cache and reload
- Try different browser
- Check browser console (F12) for detailed errors

### Issue: Task cards not appearing after upload

**Symptoms:**
- Upload completes but no tasks shown
- Queue empty after upload

**Solutions:**
1. Wait longer (OCR processing may take time)
2. Refresh browser (F5)
3. Check browser console for errors
4. Check server logs for processing errors
5. Verify file was valid PDF/image

### Issue: "Edit Task" modal doesn't save

**Error:**
```
Edit doesn't apply when clicked
```

**Solutions:**
1. Refresh browser page
2. Check browser console for errors
3. Try different browser
4. Verify JavaScript is enabled

---

## Database

### Issue: Database errors

**Error:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solutions:**
```bash
# Check database
sqlite3 review_queue.db "PRAGMA integrity_check;"

# Backup corrupted database
cp review_queue.db review_queue.db.corrupted

# Delete and restart (creates fresh DB)
rm review_queue.db
python run_app.py
```

### Issue: Database grows too large

**Symptoms:**
- Slow queries
- Disk space issues

**Solutions:**
```bash
# Backup database
cp review_queue.db review_queue.db.backup

# Delete old records
sqlite3 review_queue.db "DELETE FROM tasks WHERE date(created_at) < date('now', '-90 days');"

# Vacuum to reclaim space
sqlite3 review_queue.db "VACUUM;"
```

### Issue: Can't access database from another process

**Error:**
```
database is locked
```

**Solutions:**
1. Stop the application
2. Try query again
3. Or use `-timeout` parameter in sqlite3

---

## Docker Issues

### Issue: Docker build fails

**Error:**
```
Step X/Y: ERROR
```

**Solutions:**
1. Check available disk space (need ~5GB)
2. Delete old images: `docker image prune`
3. Rebuild without cache: `docker build --no-cache .`
4. Check Dockerfile syntax

### Issue: Docker container won't start

**Solutions:**
```bash
# Check logs
docker logs <container_id>

# Run with verbose output
docker run -it paddleocraas:latest bash

# Check resource limits
docker inspect <container_id> | grep -A5 Memory
```

### Issue: Port mapping not working

**Error:**
```
curl: Failed to connect to localhost:5000
```

**Solutions:**
```bash
# Verify port mapping
docker port <container_id>

# Re-run with correct port
docker run -p 5000:8000 paddleocraas:latest
```

### Issue: Database not persisting

**Error:**
```
Database lost when container restarts
```

**Solutions:**
```bash
# Use named volume
docker run -v paddleocr_db:/app paddleocraas:latest

# Or verify volume is mounted
docker inspect <container_id> | grep -A10 Mounts
```

---

## Docker Compose Issues

### Issue: docker-compose command not found

**Error:**
```
docker: 'compose' is not a command
```

**Solutions:**
- Use `docker-compose` (older syntax)
- Or upgrade Docker to latest version
- Install Docker Compose separately

### Issue: Services won't start

**Error:**
```
ERROR: Service <name> failed to build
```

**Solutions:**
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## GPU Issues

### Issue: GPU not recognized

**Symptoms:**
- OCR runs on CPU
- CUDA not available

**Solutions:**
1. Verify NVIDIA GPU: `nvidia-smi`
2. Install CUDA 12.0+
3. Install nvidia-docker
4. Run: `docker run --gpus all paddleocraas:latest`

---

## Performance Issues

### Issue: Server slow to respond

**Solutions:**
1. Check CPU/memory usage: `docker stats`
2. Increase workers: `--workers 4`
3. Add more resources: `--cpus=4 --memory=8g`
4. Check database size

### Issue: High memory usage

**Solutions:**
1. Limit memory: `--memory=4g`
2. Clear old database records
3. Reduce concurrent uploads
4. Increase workers (distribute load)

---

## Getting More Help

### Enable Debug Logging

```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

```bash
# Application logs
# Look at console output when running

# Docker logs
docker logs -f <container_id>

# Compose logs
docker-compose logs -f paddleocraas
```

### Report Issues

1. Collect system information:
   ```bash
   python --version
   docker --version
   nvidia-smi  # If using GPU
   ```

2. Collect error messages/logs
3. Steps to reproduce
4. Open GitHub issue with above information

---

**Still need help?** Check [FAQ](../faq.md) or open an [issue on GitHub](https://github.com/yourusername/PaddleOCRaaS/issues).
