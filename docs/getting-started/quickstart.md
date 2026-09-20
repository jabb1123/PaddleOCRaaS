# Quick Start

Get PaddleOCRaaS up and running in 5 minutes.

## 🚀 Fastest Path (Docker)

### Prerequisites
- Docker installed ([install Docker](https://docs.docker.com/get-docker/))

### Build & Run

```bash
# Clone the repository
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS

# Build the Docker image
docker build -t paddleocraas:latest .

# Run the container
docker run -p 8000:8000 paddleocraas:latest
```

### Access the Application
Open your browser and visit: **http://localhost:8000/static/index.html**

### Test It
1. Click the upload area or drag a PDF/image file
2. Wait for OCR processing (GPU accelerated)
3. Review extracted tasks in the queue
4. Approve, reject, or edit tasks
5. View OCR results in the OCR Results tab

**That's it!** 🎉

---

## 🏃 Local Development Setup

### Prerequisites
- Python 3.10+ ([install Python](https://www.python.org/downloads/))
- pip or poetry
- ~2GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python run_app.py
```

### Access the Application
Open your browser and visit: **http://localhost:8000/static/index.html**

---

## 📁 File Upload

### Supported Formats
- ✅ **PDF** (.pdf)
- ✅ **Images** (.jpg, .png, .jpeg, .bmp)

### Size Limits
- Maximum file size: No hard limit (depends on available memory)
- Recommended: < 50MB per file
- Multi-page PDFs supported (up to 100 pages)

### Upload Process
1. Select **Tasks** tab
2. Click upload area or drag files
3. Select PDF/image file
4. Wait for processing (progress shown)
5. Tasks appear in queue when ready

---

## 🔄 Typical Workflow

### 1️⃣ Upload Document
- Drop PDF or image file
- Wait for OCR processing
- See progress indicator

### 2️⃣ Review Extracted Tasks
- Browse pending tasks in queue
- Read original OCR text
- Check extracted entities and themes

### 3️⃣ Manage Tasks
- **Approve** ✅ - Mark as correct
- **Reject** ❌ - Discard incorrect extraction
- **Edit** ✏️ - Modify task text

### 4️⃣ Review OCR Results
- Click **OCR Results** tab
- Select document from dropdown
- View all text blocks per page
- See confidence scores

---

## ⚙️ Configuration

### Default Settings
- **Host**: localhost (127.0.0.1)
- **Port**: 8000
- **Workers**: 1

### Customize for Docker
```bash
docker run -p 5000:8000 \
  -e PADDLEOCR_HOST=0.0.0.0 \
  -e PADDLEOCR_PORT=8000 \
  paddleocraas:latest
```

### Customize Locally
```bash
python run_app.py --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📊 API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload File
```bash
curl -X POST -F "file=@document.pdf" \
  http://localhost:8000/upload
```

### List Tasks
```bash
curl http://localhost:8000/api/queue
```

### Approve Task
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"version": 1}' \
  http://localhost:8000/api/approve/1
```

See [API Reference](../api/rest.md) for complete documentation.

---

## 🐛 Common Issues

### Issue: "Connection refused" when opening http://localhost:8000
**Solution**: 
- Check if server is running (`python run_app.py`)
- Check port 8000 is not blocked by firewall
- Try http://127.0.0.1:8000 instead

### Issue: Docker build fails with "insufficient space"
**Solution**:
- Free up disk space (images need ~3GB)
- Or use a smaller base image in Dockerfile

### Issue: OCR processing very slow
**Solution**:
- Check if GPU is available/enabled
- Reduce file size or page count
- See [Performance Tuning](../deployment/production.md#performance-tuning)

### Issue: Web UI doesn't load
**Solution**:
- Check browser console for errors
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito/private mode

---

## 📚 Next Steps

### Learn More
- [Full Installation Guide](installation.md)
- [Docker Guide](../docker/overview.md)
- [Feature Documentation](../features/ocr-pipeline.md)

### Set Up Production
- [Production Deployment](../deployment/production.md)
- [Kubernetes Setup](../deployment/kubernetes.md)

### Development
- [Contributing Guide](../development/contributing.md)
- [Testing Guide](../development/testing.md)

---

## 💬 Need Help?

- Check [FAQ](../faq.md)
- Read [Troubleshooting](../development/troubleshooting.md)
- Open an issue on [GitHub](https://github.com/yourusername/PaddleOCRaaS/issues)
