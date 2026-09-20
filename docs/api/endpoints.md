# API Endpoints Reference

Complete list of all REST API endpoints.

## Endpoints by Category

### Health & Status
- `GET /health` - Health check

### Document Management
- `POST /upload` - Upload document
- `GET /api/documents` - List documents

### Task Queue
- `GET /api/queue` - Get pending tasks
- `POST /api/approve/{task_id}` - Approve task
- `POST /api/reject/{task_id}` - Reject task
- `POST /api/edit/{task_id}` - Edit task

### OCR Results
- `GET /api/ocr/{document_name}` - Get OCR results
- `GET /api/ocr/{document_name}/pages` - Get OCR by page

## Full Endpoint Details

See [REST API Reference](rest.md) for full documentation of each endpoint including request/response formats.

---

## Common API Patterns

### Retrieve Queue
```bash
curl http://localhost:8000/api/queue
```

### Approve Task
```bash
curl -X POST http://localhost:8000/api/approve/1
```

### Upload File
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

---

**See Also:** [REST API Reference](rest.md)
