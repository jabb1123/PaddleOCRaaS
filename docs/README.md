# README for Documentation

This documentation site provides comprehensive guides for PaddleOCRaaS.

## Structure

- **[Home](index.md)** - Project overview and introduction
- **[Getting Started](getting-started/quickstart.md)** - Quick start guide
- **[Docker](docker/overview.md)** - Docker deployment and configuration
- **[Deployment](deployment/production.md)** - Production deployment guides
- **[Features](features/ocr-pipeline.md)** - Feature documentation
- **[API Reference](api/rest.md)** - REST API documentation
- **[FAQ](faq.md)** - Frequently asked questions

## Building Documentation

### Prerequisites
```bash
pip install -r requirements-docs.txt
```

### Build Locally
```bash
mkdocs serve
# Visit: http://localhost:8000
```

### Build Static Site
```bash
mkdocs build
# Output in: site/ folder
```

## Deploying Documentation

Documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

Manual deployment:
```bash
mkdocs gh-deploy
```

## Contributing to Documentation

1. Edit `.md` files in `docs/` folder
2. Preview with `mkdocs serve`
3. Commit and push changes
4. GitHub Actions automatically deploys

## Documentation Style Guide

- Use clear, concise language
- Include code examples
- Add links to related pages
- Use headings properly (#, ##, ###)
- Keep paragraphs short
- Use lists for multiple items
- Add admonitions for important notes

### Example Admonition
```markdown
!!! note
    This is an important note
```

## Troubleshooting

### Documentation won't build
```bash
# Verify all dependencies
pip list | grep mkdocs

# Reinstall if needed
pip install -r requirements-docs.txt --force-reinstall
```

### Changes not showing
```bash
# Clear cache
rm -rf site/

# Rebuild
mkdocs build
```

---

Last updated: September 2026
