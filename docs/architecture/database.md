# Database Schema

SQLite database schema for PaddleOCRaaS.

## Tables

### tasks
Stores extracted tasks/entities from OCR results.

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    document_name TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    themes TEXT,
    entities TEXT
);
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique task ID (auto-increment) |
| text | TEXT | Task description/text |
| document_name | TEXT | Source document filename |
| status | TEXT | Current status: pending, approved, rejected |
| created_at | TIMESTAMP | Task creation time |
| updated_at | TIMESTAMP | Last modification time |
| themes | TEXT | Associated themes (JSON) |
| entities | TEXT | Associated entities (JSON) |

### documents
Tracks uploaded documents and OCR processing.

```sql
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT UNIQUE NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ocr_status TEXT DEFAULT 'processing',
    page_count INTEGER
);
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique document ID |
| filename | TEXT | Document filename |
| upload_time | TIMESTAMP | Upload timestamp |
| ocr_status | TEXT | OCR status: processing, completed, error |
| page_count | INTEGER | Number of pages in document |

### ocr_results
Stores raw OCR output from PaddleOCR.

```sql
CREATE TABLE IF NOT EXISTS ocr_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name TEXT,
    page_number INTEGER,
    ocr_text TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique result ID |
| document_name | TEXT | Source document |
| page_number | INTEGER | Page number in document |
| ocr_text | TEXT | Recognized text from page |
| confidence | REAL | Confidence score (0.0-1.0) |
| created_at | TIMESTAMP | Creation timestamp |

## Relationships

```
documents
    ↓ (one-to-many)
tasks, ocr_results
```

- One document can have many tasks
- One document can have many OCR results (one per page)
- Tasks reference documents by filename

## Queries

### Get all pending tasks
```sql
SELECT * FROM tasks WHERE status = 'pending' ORDER BY created_at DESC;
```

### Get OCR results for document
```sql
SELECT ocr_text FROM ocr_results 
WHERE document_name = ? 
ORDER BY page_number;
```

### Get document statistics
```sql
SELECT 
    d.filename,
    COUNT(t.id) as task_count,
    SUM(CASE WHEN t.status = 'approved' THEN 1 ELSE 0 END) as approved_count
FROM documents d
LEFT JOIN tasks t ON d.filename = t.document_name
GROUP BY d.filename;
```

### Get approval statistics
```sql
SELECT 
    status,
    COUNT(*) as count
FROM tasks
GROUP BY status;
```

## Maintenance

### Backup Database
```bash
cp review_queue.db review_queue.db.backup
```

### Verify Database Integrity
```bash
sqlite3 review_queue.db "PRAGMA integrity_check;"
```

### Optimize Database
```bash
sqlite3 review_queue.db "VACUUM;"
```

### Delete Old Records
```bash
# Delete tasks older than 90 days
sqlite3 review_queue.db "DELETE FROM tasks WHERE date(created_at) < date('now', '-90 days');"

# Delete OCR results older than 90 days
sqlite3 review_queue.db "DELETE FROM ocr_results WHERE date(created_at) < date('now', '-90 days');"
```

---

**See Also:** [Deployment](../deployment/production.md), [Database Management](../features/database.md)
