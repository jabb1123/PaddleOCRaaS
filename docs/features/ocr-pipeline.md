# OCR Pipeline

The core OCR processing pipeline for handwritten document extraction.

## Pipeline Stages

### Stage 1: Document Processing
**Input:** PDF or image file  
**Output:** Individual page images

- Extract pages from PDF using PyMuPDF
- Render pages to high-quality images
- Prepare for OCR processing
- Handle multi-page documents

### Stage 2: OCR Recognition
**Input:** Page images  
**Output:** Text with bounding boxes and confidence scores

- Use PaddleOCRVL (Vision-Language model)
- Text detection (character-level bounding boxes)
- Character recognition
- Confidence scoring for each recognized character
- GPU-accelerated for speed

### Stage 3: Data Extraction
**Input:** OCR results  
**Output:** Structured tasks with entities and themes

- **Task Detection** - Identify actionable items via keywords
- **Entity Extraction** - Find names, acronyms, important terms
- **Theme Classification** - Categorize by domain/topic
- **Normalization** - Expand shorthand, clean text

### Stage 4: Review & Approval
**Input:** Extracted data  
**Output:** Approved tasks in database

- Queue management interface
- Manual review workflow
- Approve/reject/edit capabilities
- Revision history tracking
- Database persistence

## Technical Details

### Text Detection
- Outputs bounding boxes for each text block
- Character-level or line-level detection
- Enables spatial understanding of document layout

### Confidence Scoring
- Per-character confidence when available
- Ranges from 0.0 (completely uncertain) to 1.0 (certain)
- Helps identify OCR errors

### Special Character Handling
- Robust handling of:
  - Apostrophes and quotes
  - Mixed case (iPhone, JavaScript)
  - Acronyms (API, HTTP, OCR)
  - Punctuation marks
  - Diacritical marks (é, ñ, ü)

### Multi-Language Support
- 80+ languages supported by PaddleOCR
- English optimized in this build
- Mixed-language text supported

## Performance Characteristics

| Metric | GPU | CPU |
|--------|-----|-----|
| Single Page | 2-5 seconds | 10-30 seconds |
| 10-Page PDF | 20-50 seconds | 2-5 minutes |
| Memory (Peak) | 2-4GB | 1-2GB |
| Throughput | 60-100 pages/min | 10-15 pages/min |

## Quality Factors

### OCR Accuracy Affected By
- Image resolution (higher = better)
- Image quality (lighting, contrast)
- Handwriting clarity (printed > cursive)
- Document orientation (straight > tilted)
- Language complexity (English > CJK)

### Typical Accuracy Rates
| Text Type | Accuracy |
|-----------|----------|
| Printed text | 95-99% |
| Clear handwriting | 80-95% |
| Cursive handwriting | 60-85% |
| Mixed or unclear | 50-75% |

## Optimization Tips

### Improve Speed
- Enable GPU acceleration
- Use multiple workers
- Process smaller batches
- Reduce image resolution if quality allows

### Improve Accuracy
- Use high-resolution scans (200+ DPI)
- Ensure good lighting
- Straighten skewed pages
- Remove background noise/shadows
- Review and correct results

### Improve Entity Extraction
- Use consistent naming conventions
- Include context (entity type labels)
- Separate entities clearly
- Use consistent formatting

---

**Next:** [Web Interface](web-ui.md)
