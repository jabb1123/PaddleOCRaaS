# First Steps

After installation, take these first steps to become familiar with PaddleOCRaaS.

## 📍 Step 1: Access the Web Interface

### Start the Application

=== "Docker"
    ```bash
    docker run -p 8000:8000 paddleocraas:latest
    ```

=== "Local Python"
    ```bash
    python run_app.py
    ```

### Open in Browser
Navigate to: **http://localhost:8000/static/index.html**

You should see a clean, modern interface with two main tabs:
- 📋 **Tasks** - Upload documents and manage extracted tasks
- 🔍 **OCR Results** - View raw OCR output by document

---

## 🎯 Step 2: Upload Your First Document

### Prepare a Document
- Have a PDF or image file ready
- Recommended: Start with a 1-2 page document for testing
- Supported: PDF, JPG, PNG, JPEG, BMP

### Upload Process
1. Click the **Tasks** tab
2. Look for the upload area (large box in the middle)
3. Either:
   - Click to select a file
   - Drag and drop a file onto the area
4. Wait for upload and processing
   - Progress indicator shows status
   - OCR processing happens automatically
   - May take 30-60 seconds depending on file size and GPU

### What Happens
```
Upload → Page Extraction → OCR Processing → Task Extraction → Database Storage
  ↓          ↓                  ↓                  ↓              ↓
File      Pages extracted   Text recognized   Tasks identified  Ready for review
```

---

## 👀 Step 3: Review Extracted Tasks

Once processing completes, you'll see the **Queue Stats**:
- 📊 Pending tasks (ready for review)
- ✅ Approved tasks
- ❌ Rejected tasks

### Task Card Display
Each task shows:
- 📝 **Task Text** - Extracted action item
- 🏷️ **Entities** - Names and acronyms found
- 📌 **Themes** - Domain classification
- 🔍 **Score** - OCR confidence

### Actions Available
For each task, you can:
- ✅ **Approve** - Mark as correct (final approval)
- ❌ **Reject** - Discard if incorrect
- ✏️ **Edit** - Modify text, entities, or themes before approving

---

## ✏️ Step 4: Approve, Reject, or Edit a Task

### Approve Task
1. Click **Approve** button on a task
2. Task moves to "Approved" count
3. Original OCR text saved in database
4. Audit trail created

### Reject Task
1. Click **Reject** button on a task
2. Task moves to "Rejected" count
3. Task no longer appears in pending queue
4. Reason recorded in database

### Edit Task
1. Click **Edit** button on a task
2. Modal dialog opens with editable fields:
   - Task text (main content)
   - Entities (comma-separated)
   - Themes (comma-separated)
3. Make corrections
4. Click **Save** to save changes
5. Task still shows as pending until approved/rejected
6. Revision history recorded

### Revision History
- Every edit creates a new revision
- Full audit trail of changes
- Original OCR always preserved
- Can view change history (database level)

---

## 🔍 Step 5: Review OCR Results

For detailed inspection of OCR processing:

1. Click **OCR Results** tab
2. Select a document from the dropdown
   - Shows all uploaded documents
   - Displays page count and total text blocks
3. View OCR blocks organized by page
4. Each block shows:
   - 📍 Bounding box coordinates
   - 📄 Text content
   - 📊 Confidence score
   - 📋 Page number

### Understanding Confidence Scores
- **0.95-1.0**: Excellent recognition
- **0.85-0.95**: Good, minor uncertainties
- **0.75-0.85**: Fair, some OCR errors possible
- **< 0.75**: Poor, likely contains errors

### Use Cases
- Debug OCR quality
- Identify why a task was extracted incorrectly
- Understand text layout and positioning

---

## 📊 Step 6: Explore the Database

The application stores everything in **review_queue.db** (SQLite):

### View Stored Data

=== "Task Queue"
    ```bash
    sqlite3 review_queue.db "SELECT id, text, status FROM tasks LIMIT 5;"
    ```

=== "Approvals"
    ```bash
    sqlite3 review_queue.db "SELECT COUNT(*) as approved FROM tasks WHERE status='approved';"
    ```

=== "OCR Results"
    ```bash
    sqlite3 review_queue.db "SELECT document_name, COUNT(*) as blocks FROM ocr_results GROUP BY document_name;"
    ```

### Database Schema
- **tasks** - Extracted tasks/items
- **task_metadata** - Entity/theme associations
- **review_queue** - Current queue status
- **task_revisions** - Edit history
- **ocr_results** - Raw OCR output blocks

---

## 🧪 Step 7: Test with Sample Data

### Option 1: Create Test Document
Create a simple text document, scan it, or use existing PDF

### Option 2: Test Keywords
Upload a document containing these keywords to see task extraction:
- "TODO", "TASK", "ACTION", "IMPORTANT"
- "DONE", "COMPLETED", "APPROVED"

### Option 3: Test Entities
Try documents with:
- Person names: "John Smith", "Dr. Wilson"
- Acronyms: "API", "HTTP", "OCR"
- Mixed case: "iPhone", "JavaScript"

---

## 🔧 Step 8: Understand Configuration

### Environment Variables
Customize server behavior:

```bash
# Set host and port
export PADDLEOCR_HOST=0.0.0.0
export PADDLEOCR_PORT=8000
python run_app.py
```

### Command-line Arguments
```bash
python run_app.py --host 0.0.0.0 --port 8000 --workers 4
```

### Browser Access
- **Local only**: http://127.0.0.1:8000
- **Network access**: http://0.0.0.0:8000 or http://<your-ip>:8000

---

## 📚 Step 9: Read Documentation

Explore different sections to learn more:

| Topic | Resource |
|-------|----------|
| **Installation Details** | [Installation Guide](installation.md) |
| **Docker Deployment** | [Docker Guide](../docker/overview.md) |
| **OCR Pipeline Details** | [OCR Pipeline Docs](../features/ocr-pipeline.md) |
| **API Reference** | [REST API Docs](../api/rest.md) |
| **Production Setup** | [Production Guide](../deployment/production.md) |

---

## 🐛 Step 10: Troubleshoot Common Issues

### Web UI Won't Load
```bash
# Check if server is running
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

### Upload Stuck
```bash
# Check server logs for errors
# Ctrl+C to stop, review console output
```

### Database Error
```bash
# Backup and reset database
cp review_queue.db review_queue.db.backup
rm review_queue.db
python run_app.py  # Creates new database
```

### Poor OCR Quality
- Try higher resolution images (200+ DPI)
- Ensure documents are properly oriented
- Check GPU is being utilized (if available)

---

## ✨ Next Steps

### Learn More
1. **Deep Dive**: [OCR Pipeline Details](../features/ocr-pipeline.md)
2. **Scale Up**: [Docker & Deployment](../docker/overview.md)
3. **Integrate**: [API Reference](../api/rest.md)

### Set Up Production
1. **Server**: [Production Deployment](../deployment/production.md)
2. **Container**: [Kubernetes Setup](../deployment/kubernetes.md)
3. **Monitor**: [Performance & Monitoring](../deployment/production.md#monitoring)

### Get Involved
1. **Contribute**: [Contributing Guide](../development/contributing.md)
2. **Develop**: [Development Setup](../development/setup.md)
3. **Test**: [Testing Guide](../development/testing.md)

---

## 💡 Tips

✅ **Best Practices**
- Start with small documents (1-2 pages)
- Batch similar documents together
- Review and approve in sessions
- Monitor database size periodically

⚠️ **Common Mistakes**
- Running out of disk space during OCR
- Not checking health endpoint before testing
- Assuming all OCR is 100% accurate (review carefully)
- Forgetting to create backups before database resets

📞 **Need Help?**
- Check [FAQ](../faq.md)
- Read [Troubleshooting Guide](../development/troubleshooting.md)
- Open [GitHub Issue](https://github.com/yourusername/PaddleOCRaaS/issues)

---

**Congratulations!** 🎉 You're now familiar with the basics of PaddleOCRaaS. Explore more features and deployment options in the documentation.
