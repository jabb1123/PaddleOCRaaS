# Testing Guide

Comprehensive testing guide for PaddleOCRaaS development.

## Running Tests

### All Tests

```bash
pytest
# or
pytest tests/ -v
```

### Specific Test File

```bash
pytest tests/test_main.py -v
```

### Specific Test Function

```bash
pytest tests/test_main.py::test_health_check -v
```

### With Coverage

```bash
pytest --cov=. tests/
```

## Test Structure

Tests are organized by module:

```
tests/
├── test_main.py                    # API endpoints
├── test_review_queue.py            # Database operations
├── test_entity_theme_extraction.py # Task extraction logic
└── conftest.py                     # Shared fixtures
```

## Writing Tests

### Basic Test

```python
import pytest

def test_function_success():
    """Test successful execution"""
    result = my_function()
    assert result is not None
    assert result == expected_value
```

### Test with Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return {"text": "TODO: Fix bug"}

def test_with_fixture(sample_data):
    result = process(sample_data)
    assert result is not None
```

### Test Exceptions

```python
def test_function_error():
    """Test error handling"""
    with pytest.raises(ValueError):
        my_function(bad_input)
```

## Test Types

### Unit Tests
Test individual functions in isolation.

```python
def test_extract_tasks():
    tasks = extract_tasks("TODO: Fix bug")
    assert len(tasks) > 0
```

### Integration Tests
Test multiple components working together.

```python
def test_upload_and_extract():
    # Upload file
    response = client.post("/upload", files={"file": file})
    assert response.status_code == 200
    # Extract tasks
    tasks = get_tasks()
    assert len(tasks) > 0
```

### End-to-End Tests
Test full user workflows.

```python
def test_full_workflow():
    # Upload
    # Process
    # Review
    # Approve
```

## Fixtures

Reusable test data and setup:

```python
# conftest.py
import pytest

@pytest.fixture
def test_file():
    """Provide test PDF file"""
    return "data/test.pdf"

@pytest.fixture
def test_client():
    """Provide FastAPI test client"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
```

## Mocking

Mock external dependencies:

```python
from unittest.mock import patch

@patch('main.get_ocr_engine')
def test_with_mock(mock_ocr):
    mock_ocr.return_value.ocr.return_value = []
    # Test code
```

## Coverage

Check code coverage:

```bash
# Generate coverage report
pytest --cov=. tests/

# View HTML report
pytest --cov=. --cov-report=html tests/
# Open htmlcov/index.html
```

Aim for 80%+ coverage!

## CI/CD Testing

Tests run automatically on:
- Pull requests
- Commits to main branch
- Manual trigger via GitHub Actions

See `.github/workflows/` for configuration.

## Performance Tests

### Benchmark Function

```python
import time

def test_ocr_performance():
    start = time.time()
    result = get_ocr_engine().ocr("document.pdf")
    duration = time.time() - start
    assert duration < 10.0  # Should complete within 10 seconds
```

### Load Testing

```bash
pip install locust

# Create locustfile.py with load test
# Run: locust -f locustfile.py
```

## Common Test Scenarios

### Test File Upload

```python
def test_upload_pdf(test_client):
    response = test_client.post(
        "/upload",
        files={"file": ("test.pdf", open("data/test.pdf", "rb"))}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "processing"
```

### Test API Endpoints

```python
def test_queue_endpoint(test_client):
    response = test_client.get("/api/queue")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

### Test Database Operations

```python
def test_add_task_to_queue():
    task = add_task_to_queue(
        text="Test task",
        entities=["Entity1"],
        themes=["Theme1"]
    )
    assert task is not None
    assert task.status == "pending"
```

### Test Error Handling

```python
def test_upload_invalid_file(test_client):
    response = test_client.post(
        "/upload",
        files={"file": ("test.txt", b"Invalid")}
    )
    assert response.status_code == 400
```

## Debugging Tests

### Print Debugging

```python
def test_something():
    result = my_function()
    print(f"Result: {result}")  # Will show in pytest output with -s flag
    assert result
```

Run with output:
```bash
pytest -s tests/
```

### Use Debugger

```python
import pdb

def test_something():
    result = my_function()
    pdb.set_trace()  # Execution stops here
    assert result
```

Run:
```bash
pytest --pdb tests/
```

## Test Best Practices

✅ **DO:**
- Write clear, descriptive test names
- Test one thing per test
- Use fixtures for reusable data
- Mock external dependencies
- Keep tests fast
- Commit code with tests
- Run tests before committing

❌ **DON'T:**
- Test implementation details
- Create interdependent tests
- Use sleep() in tests
- Leave tests failing
- Commit broken code
- Skip important tests

## Running Tests in Docker

```bash
docker-compose run --rm paddleocraas pytest tests/ -v
```

---

**See Also:** [Contributing Guide](../development/contributing.md)
