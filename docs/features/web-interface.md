# Web Interface Guide

Using the PaddleOCRaaS web interface.

## Accessing the Interface

```
http://localhost:8000/static/index.html
```

Or just `http://localhost:8000` and click the link.

## Main Features

### 1. Upload Documents
- Support: PDF, PNG, JPG, JPEG, GIF, WebP
- Max file size: 100MB (configurable)
- Formats: Text documents, scanned images, handwritten notes

### 2. View Task Queue
- Displays all pending OCR tasks
- Shows task text and extracted entities
- Real-time updates

### 3. Review & Approve
- Examine OCR results
- Approve accurate results
- Reject or edit incorrect results

### 4. OCR Results Viewer
- View full OCR output
- See confidence scores
- Review by page

### 5. Search & Filter
- Search by text content
- Filter by status (pending, approved, rejected)
- Filter by document name

## Workflow

### Step 1: Upload Document

1. Click "Upload Document"
2. Select PDF or image file
3. Click "Upload"
4. Wait for processing to complete

### Step 2: Review Queue

1. See pending tasks in queue
2. Read OCR-extracted text
3. Review entities and themes

### Step 3: Approve/Reject

Each task shows:
- **Approve** - Accept the result
- **Reject** - Mark as incorrect
- **Edit** - Modify the text before approving

### Step 4: View Results

1. Click "View Results" to see full OCR output
2. Browse by page
3. See confidence scores

---

**See Also:** [Getting Started](../getting-started/first-steps.md)
