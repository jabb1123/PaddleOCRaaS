# Development Setup

Set up your development environment for contributing to PaddleOCRaaS.

## Prerequisites

- Python 3.10
- Git
- GitHub account (for contributing)
- Virtual environment tool

## Initial Setup

### 1. Fork Repository (Optional)

If contributing, fork the repository on GitHub.

### 2. Clone Repository

```bash
# Your fork (if contributing)
git clone https://github.com/YOUR_USERNAME/PaddleOCRaaS.git

# Original repository
git clone https://github.com/yourusername/PaddleOCRaaS.git

cd PaddleOCRaaS
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 4. Install Dependencies

```bash
# Application dependencies
pip install -r requirements.txt

# Development dependencies
pip install pytest pytest-cov black flake8 mypy

# Documentation dependencies (optional)
pip install -r requirements-docs.txt
```

### 5. Run Tests

```bash
pytest tests/ -v
```

All tests should pass.

## Development Tools

### Code Formatting

```bash
# Format code with black
black main.py review_queue.py

# Check code style with flake8
flake8 main.py review_queue.py
```

### Type Checking

```bash
# Check types with mypy
mypy main.py --ignore-missing-imports
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_main.py::test_upload

# Run with coverage
pytest --cov=. tests/

# Watch mode (auto-run on changes)
pytest-watch
```

## Git Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/my-feature
```

### Committing Changes

```bash
git add .
git commit -m "Add my feature"
```

### Pushing to Remote

```bash
git push origin feature/my-feature
```

### Creating Pull Request

Go to GitHub and create a PR from your branch to main.

## Project Structure

```
PaddleOCRaaS/
├── main.py                 # FastAPI server + OCR
├── review_queue.py         # Database management
├── run_app.py              # Server launcher
├── requirements.txt        # Core dependencies
├── requirements-docs.txt   # Documentation dependencies
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration config
├── mkdocs.yml              # Documentation config
├── static/
│   └── index.html          # Web interface
├── tests/
│   ├── test_main.py        # Main tests
│   ├── test_review_queue.py # Database tests
│   └── ...
├── docs/                   # Documentation files
│   ├── index.md
│   ├── getting-started/
│   ├── docker/
│   ├── deployment/
│   ├── features/
│   ├── api/
│   ├── faq.md
│   └── ...
├── .github/
│   └── workflows/
│       └── deploy-docs.yml # GitHub Actions
└── ...
```

## Testing Guidelines

### Write Tests For

- New features
- Bug fixes
- API endpoints
- Database operations

### Test Structure

```python
# tests/test_feature.py
import pytest
from main import your_function

def test_feature_success():
    result = your_function()
    assert result is not None

def test_feature_error():
    with pytest.raises(Exception):
        your_function(bad_input)
```

### Run Tests Frequently

```bash
# Before committing
pytest

# After pulling updates
pytest

# Before creating PR
pytest --cov=.
```

## Code Review

When submitting a PR:

1. Ensure all tests pass: `pytest`
2. Format code: `black .`
3. Check style: `flake8 .`
4. Update documentation if needed
5. Add test coverage for new code
6. Write clear PR description

## Common Development Tasks

### Add New Endpoint

1. Add function in `main.py`
2. Add `@app.get()` or `@app.post()` decorator
3. Add test in `tests/test_main.py`
4. Update documentation

### Add Database Feature

1. Update schema in `review_queue.py`
2. Add migration if needed
3. Add function to interact with new schema
4. Add tests
5. Update documentation

### Fix Bug

1. Create test that reproduces the bug
2. Fix the bug in the code
3. Verify test passes
4. Add to CHANGELOG
5. Submit PR

## Documentation Development

### Edit Documentation

```bash
# Install doc dependencies
pip install -r requirements-docs.txt

# Serve locally
mkdocs serve

# Visit http://localhost:8000
```

### Build Documentation

```bash
# Generate static site
mkdocs build

# Output in: site/ folder
```

## Performance Development

### Profiling

```python
# Add to code
import cProfile
cProfile.run('your_function()')
```

### Benchmarking

```bash
# Time execution
time python -c "from main import get_ocr_engine; engine.ocr('file.pdf')"
```

## Debugging

### Print Debugging

```python
print(f"Debug: {variable}")
```

### Python Debugger

```python
import pdb
pdb.set_trace()  # Execution stops here
```

### Logging

```python
import logging
logging.debug("Debug message")
logging.info("Info message")
logging.error("Error message")
```

---

**Next:** See [Contributing Guide](contributing.md)
