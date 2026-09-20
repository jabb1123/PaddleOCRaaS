# Database Features

Database management and features for PaddleOCRaaS.

## Features

### Persistent Storage
- SQLite database stores all data
- Survives application restarts
- Accessible via Docker volumes

### Task Management
- Track task status (pending, approved, rejected)
- Store OCR results
- Maintain document metadata

### Search Capabilities
- Search tasks by text
- Filter by status
- Filter by document name

### Versioning
- Track creation and update timestamps
- Maintain audit trail
- Version history of changes

## Using the Database

### Query Tasks

```bash
sqlite3 review_queue.db
```

### View All Tasks
```sql
SELECT id, text, status, created_at FROM tasks;
```

### Count by Status
```sql
SELECT status, COUNT(*) FROM tasks GROUP BY status;
```

### Search Tasks
```sql
SELECT * FROM tasks WHERE text LIKE '%search_term%';
```

## Backup & Recovery

### Backup
```bash
# Manual backup
cp review_queue.db review_queue.db.backup

# Scheduled backup (cron)
0 2 * * * cp /path/to/review_queue.db /path/to/backups/review_queue.db.$(date +\%Y\%m\%d)
```

### Recovery
```bash
# Restore from backup
cp review_queue.db.backup review_queue.db
```

## Maintenance

### Check Database
```bash
sqlite3 review_queue.db "PRAGMA integrity_check;"
```

### Optimize
```bash
sqlite3 review_queue.db "VACUUM;"
```

### Clean Old Data
```bash
# Delete results older than 6 months
sqlite3 review_queue.db "DELETE FROM ocr_results WHERE date(created_at) < date('now', '-180 days');"
```

---

**See Also:** [Database Schema](../architecture/database.md)
