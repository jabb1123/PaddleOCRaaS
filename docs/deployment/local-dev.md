# Local Development

Set up PaddleOCRaaS for local development and testing.

## Prerequisites

- Python 3.10
- Git
- Virtual environment (venv or conda)
- 2GB+ available disk space

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/PaddleOCRaaS.git
cd PaddleOCRaaS
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python run_app.py
```

### 5. Access Web UI

Open: **http://localhost:8000/static/index.html**

## Development Workflow

### Testing Changes

```bash
# Terminal 1: Run server with auto-reload
python run_app.py

# Terminal 2: Run tests
pytest tests/ -v

# Terminal 3: Make code changes and test
# Changes to main.py take effect immediately with auto-reload
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py

# Run with coverage
pytest --cov=. tests/
```

### Database Reset

```bash
# Backup first
cp review_queue.db review_queue.db.backup

# Delete database
rm review_queue.db

# Restart app
python run_app.py
# New database will be created
```

## Docker for Development

### Build and Run Locally

```bash
# Build image
docker build -t paddleocraas:dev .

# Run with local directory mount
docker run -p 8000:8000 \
  -v $(pwd):/app \
  paddleocraas:dev

# On Windows
docker run -p 8000:8000 ^
  -v %cd%:/app ^
  paddleocraas:dev
```

### Debug Logs

```bash
# View container logs
docker logs -f <container_id>

# Execute command in running container
docker exec <container_id> python -c "import paddleocr; print('OK')"
```

## Code Structure

```
PaddleOCRaaS/
├── main.py                 # FastAPI server + OCR logic
├── review_queue.py         # Database layer
├── run_app.py              # Server launcher
├── requirements.txt        # Python dependencies
├── static/
│   └── index.html          # Web UI
├── tests/                  # Test files
├── docs/                   # Documentation
├── docker-compose.yml      # Docker orchestration
└── Dockerfile              # Container image
```

## Common Development Tasks

### Add New Feature

1. Create branch: `git checkout -b feature/my-feature`
2. Make changes in `main.py` or other files
3. Write tests in `tests/`
4. Run tests: `pytest`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create Pull Request on GitHub

### Fix Bug

Same workflow as feature, but use `bugfix/` branch prefix.

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade paddleocr

# Update all
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

## Performance Testing

### Benchmark OCR Processing

```bash
# Test with sample file
time python -c "
from main import get_ocr_engine
engine = get_ocr_engine()
result = engine.ocr('data/sample.pdf')
print(f'Processed in time shown above')
"
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py and run
locust -f locustfile.py
```

## Debugging

### Debug Mode

```python
# Add debug output to main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Python Debugger

```python
# In your code
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

### Browser DevTools

Press F12 in browser to open developer tools:
- Console: See JavaScript errors
- Network: Monitor API calls
- Application: View local storage/cookies

## Documentation Development

### Build Docs Locally

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Build documentation
mkdocs build

# View locally
mkdocs serve
# Visit: http://localhost:8000/
```

### Edit Documentation

Documentation files are in `docs/` folder:

```
docs/
├── index.md                 # Home page
├── getting-started/         # Quick start guides
├── docker/                  # Docker documentation
├── deployment/              # Deployment guides
├── features/                # Feature documentation
├── api/                     # API documentation
├── faq.md                   # Frequently asked questions
└── ...
```

Edit `.md` files and reload to see changes with `mkdocs serve`.

---

**Next:** See [Contributing Guide](../development/contributing.md)
