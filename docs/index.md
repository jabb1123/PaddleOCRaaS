# PaddleOCRaaS

## AI-Powered OCR Extraction Pipeline for Handwritten Notes

Welcome to **PaddleOCRaaS** - a complete OCR extraction system that processes handwritten notes and documents with an intuitive web interface, database management, and comprehensive task review workflow.

### ✨ Key Features

- 🎨 **Advanced OCR Engine** - PaddleOCR with vision-language model (VL) for high-accuracy handwritten text recognition
- 🌐 **Modern Web Interface** - Beautiful, responsive UI for document upload, review, and management
- 📋 **Task Extraction** - Automatic extraction of actionable tasks, entities, and themes from OCR results
- ✅ **Review Workflow** - Complete approval/rejection/edit system with audit trail and revision history
- 🐳 **Docker Ready** - Containerized deployment for any environment
- 💾 **Persistent Storage** - SQLite database with full task versioning
- 📊 **Multi-Document Support** - Browse and review OCR results across multiple uploaded files
- 🔤 **Special Character Handling** - Robust processing of complex punctuation and mixed scripts

### 🚀 Quick Start

#### Option 1: Docker (Recommended)
```bash
# Build the image
docker build -t paddleocraas:latest .

# Run the container
docker run -p 8000:8000 paddleocraas:latest

# Access the UI
open http://localhost:8000/static/index.html
```

#### Option 2: Local Development
```bash
# Clone and setup
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the server
python run_app.py

# Access the UI
open http://localhost:8000/static/index.html
```

---

## 📚 Documentation Structure

- **[Getting Started](getting-started/quickstart.md)** - Installation, setup, and first run
- **[Docker Guide](docker/overview.md)** - Containerization, Docker Compose, deployment
- **[Deployment](deployment/local-dev.md)** - Production setup, cloud deployment, Kubernetes
- **[Features](features/ocr-pipeline.md)** - Detailed feature documentation
- **[Architecture](architecture/design.md)** - System design, database schema, API
- **[Development](development/setup.md)** - Contributing, testing, troubleshooting
- **[API Reference](api/rest.md)** - Complete REST API documentation

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│           Web Browser (Static UI)                   │
│        HTML5 + CSS + JavaScript                     │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────┐
│         FastAPI Server (uvicorn)                    │
│  • /upload    - Document upload endpoint            │
│  • /health    - Health check                        │
│  • /api/*     - Task management & OCR results       │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌────────┐  ┌──────────┐  ┌────────────┐
   │PaddleOCR│  │Review    │  │Database    │
   │Engine   │  │Queue     │  │(SQLite)    │
   │(GPU)    │  │Manager   │  │            │
   └────────┘  └──────────┘  └────────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                  Docker Container
```

---

## 📊 Pipeline Overview

The application processes documents through a 4-stage pipeline:

### Stage 1: Document Processing
- PDF/image upload via web UI
- Page extraction (images, PDFs via PyMuPDF)
- Preparation for OCR processing

### Stage 2: OCR Processing
- PaddleOCRVL text detection and recognition
- Layout analysis with bounding boxes
- Confidence scoring

### Stage 3: Data Extraction
- Task identification (keyword detection)
- Entity extraction (names, acronyms)
- Theme classification (domain-specific patterns)
- Audit trail recording

### Stage 4: Review & Approval
- Task queue management
- Web-based approval/rejection/editing
- Revision history with full audit trail
- Export-ready results

---

## 💻 System Requirements

### Minimum
- Python 3.10+
- 2 GB RAM
- 2 CPU cores
- ~1 GB disk space for models

### Recommended
- Python 3.10
- 4-8 GB RAM
- 4+ CPU cores
- GPU with CUDA support (NVIDIA)
- 2 GB disk space

### Docker
- Docker 20.10+
- Docker Compose 1.29+ (optional)

---

## 📦 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **OCR Engine** | PaddleOCR VL | 2.7.3 |
| **Backend Framework** | FastAPI | 0.104.1 |
| **ASGI Server** | Uvicorn | 0.24.0 |
| **Image Processing** | OpenCV | 4.8.1 |
| **PDF Processing** | PyMuPDF | 1.23.8 |
| **Database** | SQLite3 | Built-in |
| **Frontend** | HTML5/CSS3/JavaScript | Modern |
| **Containerization** | Docker | 20.10+ |

---

## 🎯 Use Cases

### Document Processing
- Digitize handwritten notes from meetings
- Extract structured data from form documents
- Batch process image collections

### Data Extraction
- Identify action items and tasks
- Extract names and important entities
- Classify content by domain themes

### Quality Assurance
- Review OCR results before processing
- Correct extraction errors
- Maintain quality standards

### Archival
- Store processed documents with metadata
- Track changes and approvals
- Build searchable document library

---

## 📖 Getting Help

- **Quick Issues**: Check [FAQ](faq.md)
- **Setup Problems**: See [Installation Guide](getting-started/installation.md)
- **Docker Issues**: Check [Docker Guide](docker/overview.md)
- **Development**: See [Contributing Guide](development/contributing.md)
- **Bugs**: Open an issue on GitHub

---

## 📋 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Contributors

- **Your Name** - Creator and maintainer

---

## 🔗 Links

- **Repository**: https://github.com/yourusername/PaddleOCRaaS
- **Issues**: https://github.com/yourusername/PaddleOCRaaS/issues
- **PaddleOCR**: https://github.com/PaddlePaddle/PaddleOCR
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker Docs**: https://docs.docker.com/

---

**Last Updated**: September 2026  
**Status**: Production Ready ✅
