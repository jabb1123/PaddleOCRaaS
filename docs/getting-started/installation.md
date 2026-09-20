# Installation Guide

Complete installation instructions for all deployment scenarios.

## System Requirements

### Python Installation
- **Python**: 3.10 (required - 3.14 incompatible, NumPy 2.x breaks dependencies)
- **pip**: Latest version
- **Virtual Environment**: Recommended (venv or conda)

### System Dependencies
- **OS**: Linux, macOS, Windows
- **RAM**: 2GB minimum, 4-8GB recommended
- **CPU**: 2 cores minimum, 4+ cores recommended
- **Disk**: 2GB for application + dependencies

### Optional but Recommended
- **GPU**: NVIDIA CUDA 12.0+ for accelerated OCR
- **Docker**: 20.10+ for containerized deployment
- **Git**: For cloning the repository

---

## Option 1: Docker Installation (Recommended)

### Prerequisites
- Docker 20.10+ installed
- Docker Compose 1.29+ (optional)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS

# Build image
docker build -t paddleocraas:latest .

# Run container
docker run -p 8000:8000 paddleocraas:latest
```

### Verification
```bash
# Check if running
docker ps | grep paddleocraas

# Test health endpoint
curl http://localhost:8000/health

# Access web UI
# Open: http://localhost:8000/static/index.html
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f paddleocraas

# Stop services
docker-compose down
```

**Advantages:**
- ✅ No local dependencies needed
- ✅ Consistent across all environments
- ✅ Easy to scale
- ✅ GPU support via nvidia-docker

---

## Option 2: Local Python Installation

### Prerequisites
- Python 3.10 installed
- pip available
- Virtual environment (highly recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS
```

### Step 2: Create Virtual Environment

=== "Linux/macOS"
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

=== "Windows (Command Prompt)"
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version  # Should be 3.10.x

# Check PaddleOCR
python -c "import paddleocr; print('PaddleOCR OK')"

# Check FastAPI
python -c "import fastapi; print('FastAPI OK')"
```

### Step 5: Download OCR Models (First Run)

```bash
# Run app once to download models (~1GB)
python run_app.py

# Press Ctrl+C after models are downloaded
# Models are cached in ~/.paddlex/official_models/
```

### Step 6: Start the Application

```bash
python run_app.py

# Output should show:
# 🚀 Starting PaddleOCR Review Queue web app...
# 📖 Visit http://127.0.0.1:8000/static/index.html
# ✋ Press Ctrl+C to stop
```

### Step 7: Access Web UI

Open browser: **http://localhost:8000/static/index.html**

---

## Option 3: GPU Acceleration

### Prerequisites
- NVIDIA GPU with CUDA Compute Capability 3.5+
- NVIDIA CUDA 12.0+ installed
- NVIDIA cuDNN installed

### Local Installation with GPU

```bash
# Follow Option 2, then verify GPU:
python -c "import paddle; print(paddle.device.cuda.get_device_name(0))"

# Should output your GPU name if available
```

### Docker with GPU

```bash
# Install NVIDIA Container Runtime first
# See: https://github.com/NVIDIA/nvidia-docker

# Run with GPU support
docker run --gpus all \
  -p 8000:8000 \
  paddleocraas:latest
```

### GPU Verification

```bash
# Check if GPU is being used
python -c "import paddle; print(f'GPUs available: {paddle.device.get_device()}')"
```

---

## Troubleshooting Installation

### Issue: Python 3.10 not found
```bash
# Check available Python versions
python --version  # or python3 --version

# Install Python 3.10 from python.org
# macOS: brew install python@3.10
# Linux: sudo apt install python3.10
```

### Issue: pip install fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt

# If still fails, try with --no-cache-dir
pip install --no-cache-dir -r requirements.txt
```

### Issue: PaddleOCR import fails
```bash
# Reinstall paddlepaddle and paddleocr
pip uninstall paddlepaddle paddleocr paddlex -y
pip install paddlepaddle==3.3.1 paddleocr==2.7.3 paddlex==3.0.1
```

### Issue: "No space left on device"
- Models are ~1GB during first run
- Temporary files ~500MB
- Clean up disk space and retry

### Issue: Slow OCR processing
- Check GPU availability: `python -c "import paddle; print(paddle.device.get_device())"`
- If CPU only, consider using GPU or reducing file size

---

## Verification Checklist

After installation, verify everything works:

```bash
# ✅ Python version
python --version  # Should be 3.10.x

# ✅ Virtual environment
which python  # Should show .venv path

# ✅ Dependencies
pip list | grep -E "fastapi|paddleocr|opencv"

# ✅ Server starts
python run_app.py &
sleep 3

# ✅ Health endpoint
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# ✅ Web UI accessible
curl http://localhost:8000/static/index.html | head -20
# Should return HTML

# ✅ Database works
python -c "from src import review_queue; review_queue.init_db()"

# Stop server
kill %1
```

---

## Updating Installation

### Update Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Update packages
pip install --upgrade -r requirements.txt

# Or specific package
pip install --upgrade paddleocr
```

### Update from Git

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies (in case of changes)
pip install -r requirements.txt

# Restart application
python run_app.py
```

### Update Docker Image

```bash
# Rebuild image
docker build --no-cache -t paddleocraas:latest .

# Stop old container
docker stop paddleocr_server

# Run new container
docker run -p 8000:8000 paddleocraas:latest
```

---

## Uninstallation

### Local Python

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows

# Remove database and cache files (optional)
rm review_queue.db
rm -rf ~/.paddlex/official_models/  # Frees ~1GB
```

### Docker

```bash
# Stop container
docker-compose down  # or docker stop container_name

# Remove image
docker image rm paddleocraas:latest

# Remove volumes (optional - keeps data)
docker volume rm paddleocr_db
```

---

## Next Steps

1. **Quick Start**: Run through [5-minute Quick Start](quickstart.md)
2. **First Steps**: Follow [First Steps Guide](first-steps.md)
3. **Docker**: Learn about [Docker Deployment](../docker/overview.md)
4. **Development**: See [Development Setup](../development/setup.md)

---

## Getting Help

- **Installation Issues**: Check [Troubleshooting](../development/troubleshooting.md)
- **Configuration**: See [Configuration Guide](../docker/configuration.md)
- **FAQ**: Check [FAQ](../faq.md)
- **GitHub Issues**: [Report Issues](https://github.com/yourusername/PaddleOCRaaS/issues)
