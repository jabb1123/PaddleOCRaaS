# REST API Reference

Complete REST API documentation for PaddleOCRaaS.

## Base URL

```
http://localhost:8000
```

## Health Check

### GET /health

Check if the service is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Document Upload

### POST /upload

Upload a PDF or image file for OCR processing.

**Request:**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

**Response:**
```json
{
  "filename": "document.pdf",
  "status": "processing",
  "page_count": 4,
  "message": "File uploaded and queued for processing"
}
```

**Status Codes:**
- `200` - File uploaded successfully
- `400` - Invalid file format
- `413` - File too large
- `500` - Server error

---

## Queue Management

### GET /api/queue

Retrieve pending tasks from the review queue.

**Query Parameters:**
- `status` (optional) - Filter by status: pending, approved, rejected

**Response:**
```json
[
  {
    "id": 1,
    "text": "Fix the API endpoint",
    "entities": ["API", "endpoint"],
    "themes": ["development"],
    "status": "pending",
    "created_at": "2026-09-19T10:30:00"
  },
  ...
]
```

---

## Task Actions

### POST /api/approve/{task_id}

Approve a task.

**Request:**
```bash
curl -X POST http://localhost:8000/api/approve/1
```

**Response:**
```json
{
  "message": "Task approved",
  "task_id": 1,
  "status": "approved"
}
```

### POST /api/reject/{task_id}

Reject a task.

**Request:**
```bash
curl -X POST http://localhost:8000/api/reject/1
```

**Response:**
```json
{
  "message": "Task rejected",
  "task_id": 1,
  "status": "rejected"
}
```

### POST /api/edit/{task_id}

Edit a task before approval.

**Request:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated task text",
    "entities": ["Entity1", "Entity2"],
    "themes": ["theme1"]
  }' \
  http://localhost:8000/api/edit/1
```

**Response:**
```json
{
  "message": "Task updated",
  "task_id": 1,
  "revision": 2
}
```

---

## Document Management

### GET /api/documents

List all uploaded documents.

**Response:**
```json
[
  {
    "document_name": "document.pdf",
    "page_count": 4,
    "upload_date": "2026-09-19T10:30:00"
  },
  ...
]
```

---

## OCR Results

### GET /api/ocr/{document_name}

Get all OCR results for a document.

**Response:**
```json
{
  "document_name": "document.pdf",
  "total_blocks": 27,
  "pages": {
    "1": {
      "blocks": [
        {
          "text": "Sample text from page 1",
          "confidence": 0.95,
          "bbox": [10, 20, 100, 40]
        },
        ...
      ]
    },
    ...
  }
}
```

### GET /api/ocr/{document_name}/pages

Get OCR results grouped by page.

**Response:**
```json
{
  "document_name": "document.pdf",
  "pages": [
    {
      "page_number": 1,
      "block_count": 8,
      "blocks": [...]
    },
    ...
  ]
}
```

---

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Authentication

Currently no authentication required. For production deployment, add:
- API keys
- JWT tokens
- OAuth2
- TLS/HTTPS

---

**See Also:** [API Endpoints Reference](endpoints.md)
