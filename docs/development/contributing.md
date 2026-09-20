# Contributing Guide

Thank you for your interest in contributing to PaddleOCRaaS!

## How to Contribute

### Report Bugs

Found a bug? Help us fix it!

1. Check [existing issues](https://github.com/yourusername/PaddleOCRaaS/issues)
2. Create a new issue with:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Error messages/logs

### Request Features

Have an idea? Share it!

1. Check [existing issues](https://github.com/yourusername/PaddleOCRaaS/issues)
2. Create a new issue with label "enhancement"
3. Describe:
   - What feature you want
   - Why it would be useful
   - Possible implementation approach

### Improve Documentation

Help improve our documentation!

1. Report typos or unclear sections as issues
2. Submit PRs with:
   - Grammar/spelling fixes
   - Clearer explanations
   - New examples
   - Better organization

### Submit Code

Want to contribute code?

## Code Contribution Workflow

### 1. Setup Development Environment

```bash
git clone https://github.com/YOUR_USERNAME/PaddleOCRaaS.git
cd PaddleOCRaaS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest black flake8
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 3. Make Changes

- Write clear, well-commented code
- Follow existing code style
- Add tests for new features
- Update documentation

### 4. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Check code style
black --check .
flake8 .

# With coverage
pytest --cov=. tests/
```

All tests must pass!

### 5. Commit Changes

```bash
git add .
git commit -m "Clear description of changes"
```

Use clear commit messages:
- ✅ "Add OCR error handling for PDFs"
- ❌ "Fix stuff"

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title
- Description of changes
- Reference to related issues (#123)
- Screenshots if UI changes

### 7. Code Review

- Address feedback from reviewers
- Make requested changes
- Re-push to update PR
- Maintainer merges when approved

## Code Style Guidelines

### Python

- Use Black for formatting: `black .`
- Maximum line length: 88 characters
- Use type hints where helpful
- Follow PEP 8 style guide

### JavaScript/HTML

- Use 2-space indentation
- Clear variable names
- Comment complex logic
- Consistent naming conventions

### Documentation

- Use clear, simple language
- Include code examples
- Link to related sections
- Use consistent markdown formatting

## Testing

All contributions must include tests!

### Test Types

1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test multiple components together
3. **End-to-End Tests** - Test full workflow

### Example Test

```python
import pytest
from main import extract_tasks

def test_extract_tasks_success():
    """Test successful task extraction"""
    ocr_text = "TODO: Fix the bug"
    tasks = extract_tasks(ocr_text)
    assert len(tasks) > 0
    assert "Fix the bug" in tasks[0]

def test_extract_tasks_empty():
    """Test with empty text"""
    tasks = extract_tasks("")
    assert len(tasks) == 0
```

## Commit Message Guidelines

Format:
```
[TYPE] Description

Optional detailed explanation
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Test addition/modification
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `chore:` Maintenance

Examples:
- `feat: Add batch upload support`
- `fix: Handle special characters in OCR results`
- `docs: Update installation guide`
- `test: Add test for entity extraction`

## Pull Request Process

1. **Fork the repository**
2. **Create feature branch** from main
3. **Write tests** for new code
4. **Follow code style** (run Black/flake8)
5. **Update documentation** if needed
6. **Write clear PR description**
7. **Address code review feedback**
8. **Ensure all CI checks pass**
9. **Wait for approval and merge**

## PR Checklist

Before submitting:

- [ ] Tests pass locally: `pytest`
- [ ] Code formatted: `black .`
- [ ] Code style OK: `flake8 .`
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Clear PR description
- [ ] Commits are clean and organized

## Reporting Security Issues

Found a security vulnerability?

⚠️ **Do not** create a public issue

Instead:
1. Email maintainers directly
2. Describe the vulnerability
3. Include reproduction steps
4. Allow time for patch before public disclosure

## Development Process

### Bug Fixes
- Reproduce the bug with a test
- Fix the underlying cause
- Ensure test passes
- Update related documentation

### New Features
- Discuss in an issue first
- Design the feature
- Write tests
- Implement feature
- Update documentation
- Request review

### Performance Improvements
- Benchmark before/after
- Ensure tests still pass
- Document performance gains
- Request review

## Getting Help

- 💬 Ask questions in GitHub issues
- 📖 Check documentation
- 🔍 Review existing code
- 📧 Contact maintainers

## Code of Conduct

- Be respectful and professional
- Welcome all contributors
- Provide constructive feedback
- Report harassment or discrimination

## Recognition

Contributors will be:
- Mentioned in CHANGELOG
- Listed in contributors section
- Recognized for significant contributions

---

Thank you for helping make PaddleOCRaaS better! 🙏

**Questions?** Open an issue or contact the maintainers.
