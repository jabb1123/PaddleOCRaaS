# Architecture Overview

High-level system architecture of PaddleOCRaaS.

## System Components

### 1. Web Server (FastAPI)
- Framework: FastAPI with Uvicorn
- Purpose: REST API and web UI serving
- Components:
  - Static file serving (web UI)
  - API endpoints
  - Document upload handling

### 2. OCR Engine (PaddleOCR)
- Framework: PaddleOCR with PaddlePaddle
- Purpose: Document OCR processing
- Supports: PDF, images (PNG, JPG, etc.)
- Modes: CPU or GPU acceleration

### 3. Task Queue (SQLite)
- Database: SQLite
- Purpose: Store tasks, results, metadata
- Tables:
  - Tasks (pending, approved, rejected)
  - Results (OCR output)
  - Documents (uploaded files metadata)

### 4. Container Runtime (Docker)
- Format: Docker container
- Orchestration: Docker Compose or Kubernetes
- Storage: Named volumes for persistence

## Data Flow

```
User Upload
    ↓
FastAPI /upload endpoint
    ↓
Document stored in volume
    ↓
PaddleOCR processing
    ↓
Results stored in SQLite
    ↓
Web UI shows tasks
    ↓
User approves/rejects/edits
    ↓
Final results stored
```

## Deployment Modes

1. **Local Development**
   - Python + FastAPI
   - SQLite on disk
   - CPU-based OCR

2. **Docker Container**
   - Containerized application
   - Volume-mounted database
   - Single instance

3. **Docker Compose**
   - Multi-container orchestration
   - Named volumes
   - Bridge networking

4. **Kubernetes**
   - Pod-based deployment
   - Persistent volumes
   - Horizontal scaling via HPA

5. **Cloud Platform**
   - AWS ECS, Google Cloud Run, Azure
   - Managed scaling
   - Cloud storage integration

---

**See Also:** [OCR Pipeline](../features/ocr-pipeline.md)
