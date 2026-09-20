import re
from typing import Any, Optional
import hashlib
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    import fitz
except ModuleNotFoundError:  # pragma: no cover - optional PDF dependency
    fitz = None

try:
    from paddleocr import PaddleOCRVL
except ModuleNotFoundError:  # pragma: no cover - handled in execution environment
    PaddleOCRVL = None

import src.review_queue as review_queue

app = FastAPI(title="PaddleOCR API Service")

_ocr_engine = None


def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        if PaddleOCRVL is None:
            raise RuntimeError("PaddleOCR is not installed in the current environment.")
        _ocr_engine = PaddleOCRVL(pipeline_version="v1")
    return _ocr_engine


def decode_image_bytes(contents: bytes):
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file format.")
    return image


def render_pdf_to_images(pdf_bytes: bytes, dpi: int = 200):
    if fitz is None:
        raise HTTPException(
            status_code=500, detail="PDF support requires PyMuPDF to be installed."
        )

    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        image = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
            pixmap.h, pixmap.w, pixmap.n
        )
        images.append(image)
    return images


def normalize_shorthand(text: str) -> str:
    expansions = {
        r"\bw/(?=\s|$)": "with",
        r"\bb/c(?=\s|$)": "because",
        r"\bTmr\b": "Tomorrow",
        r"\btmr\b": "tomorrow",
        r"\bpls\b": "please",
        r"\binfo\b": "information",
        r"\bmsg\b": "message",
    }
    normalized = text
    for pattern, replacement in expansions.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized


def extract_entities(text: str):
    """Extract named entities (people, projects, acronyms) from text."""
    entities = []

    # Common English words to filter out
    stopwords = {
        "the",
        "and",
        "but",
        "for",
        "with",
        "from",
        "to",
        "of",
        "in",
        "on",
        "we",
        "they",
        "this",
        "that",
        "which",
        "who",
        "what",
        "when",
        "where",
        "probably",
        "maybe",
        "just",
        "should",
        "would",
        "could",
        "need",
        "have",
        "been",
        "being",
        "will",
        "make",
        "about",
        "can",
    }

    # Find capitalized words (names, projects, acronyms)
    capitalized = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)

    # Also find acronyms (all caps)
    acronyms = re.findall(r"\b[A-Z]{2,}\b", text)

    # Deduplicate and maintain order, filtering out stopwords
    seen = set()
    for item in capitalized + acronyms:
        if item not in seen and len(item) > 1 and item.lower() not in stopwords:
            seen.add(item)
            entities.append({"value": item, "type": "entity"})

    return entities


def extract_themes(text: str):
    """Extract domain themes (topics, concepts) from text."""
    themes = []

    # Theme keywords common in technical/project contexts
    theme_patterns = {
        "firmware": r"\b(firmware|fw|flashing|bootloader)\b",
        "hardware": r"\b(hardware|pcb|pcba|board|mobo|nozzle|spool)\b",
        "testing": r"\b(testing|test|qa|validation|failure|fails|crash)\b",
        "deployment": r"\b(deployment|release|production|field|customer|ship|shipment)\b",
        "documentation": r"\b(docs?|documentation|notes?|spec|specification|manual)\b",
        "scheduling": r"\b(week|schedule|timeline|deadline|date|when|asap|urgent)\b",
        "engineering": r"\b(engineering|dev|development|code|implementation|fix|patch)\b",
    }

    seen = set()
    for theme_name, pattern in theme_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            if theme_name not in seen:
                seen.add(theme_name)
                themes.append({"value": theme_name, "type": "theme"})

    return themes


def extract_tasks(text: str):
    normalized = normalize_shorthand(text)
    tasks = []
    for line in normalized.splitlines():
        candidate = line.strip()
        if not candidate:
            continue
        if re.search(
            r"\b(todo|next|follow up|need to|should|must|review|draft)\b",
            candidate,
            flags=re.IGNORECASE,
        ):
            task_entities = extract_entities(candidate)
            task_themes = extract_themes(candidate)
            tasks.append(
                {
                    "text": candidate,
                    "status": "pending",
                    "entities": task_entities,
                    "themes": task_themes,
                }
            )
    return tasks


def normalize_ocr_result(result: Any):
    ocr_results = []
    if not result:
        return ocr_results

    def add_block(block):
        if block is None:
            return

        if isinstance(block, dict):
            text = (
                block.get("block_content") or block.get("text") or block.get("content")
            )
            score = block.get("score", block.get("confidence", 0.0))
            box = block.get("block_bbox") or block.get("bbox") or []
        else:
            text = getattr(block, "content", None)
            score = getattr(block, "score", getattr(block, "confidence", 0.0))
            box = (
                getattr(block, "bbox", None) or getattr(block, "block_bbox", None) or []
            )

        if text in (None, ""):
            return

        ocr_results.append(
            {
                "text": str(text),
                "confidence": float(score) if score is not None else 0.0,
                "box": box,
            }
        )

    def parse_blocks(blocks):
        if not isinstance(blocks, list):
            return
        for block in blocks:
            if isinstance(block, dict):
                add_block(block)
            elif hasattr(block, "content") and hasattr(block, "bbox"):
                add_block(block)

    if isinstance(result, dict):
        payload = result.get("res", result)
        if isinstance(payload, dict):
            parse_blocks(
                payload.get("parsing_res_list")
                or payload.get("ocr_result")
                or payload.get("result")
            )
            if ocr_results:
                return ocr_results

    if isinstance(result, list):
        for item in result:
            if hasattr(item, "parsing_res_list"):
                parse_blocks(getattr(item, "parsing_res_list"))
                if ocr_results:
                    return ocr_results
            elif isinstance(item, dict):
                payload = item.get("res", item)
                if isinstance(payload, dict):
                    parse_blocks(
                        payload.get("parsing_res_list")
                        or payload.get("ocr_result")
                        or payload.get("result")
                    )
                    if ocr_results:
                        return ocr_results

    if isinstance(result, list):
        page_lines = result[0] if isinstance(result[0], list) else result
        if not page_lines:
            return ocr_results

        if len(page_lines) == 2 and isinstance(page_lines[1], tuple):
            page_lines = [page_lines]

        for line in page_lines:
            if not isinstance(line, (list, tuple)) or len(line) < 2:
                continue
            bounding_box = line[0]
            text_confidence = line[1]
            if not isinstance(text_confidence, tuple) or len(text_confidence) != 2:
                continue
            text, confidence = text_confidence
            ocr_results.append(
                {
                    "text": str(text),
                    "confidence": float(confidence),
                    "box": bounding_box,
                }
            )

    return ocr_results


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type is None:
        raise HTTPException(
            status_code=400, detail="Uploaded file must be an image or PDF."
        )

    is_pdf = file.content_type == "application/pdf" or (
        file.filename or ""
    ).lower().endswith(".pdf")
    is_image = file.content_type.startswith("image/")
    if not is_image and not is_pdf:
        raise HTTPException(
            status_code=400, detail="Uploaded file must be an image or PDF."
        )

    try:
        review_queue.init_db()
        contents = await file.read()
        total_queued = 0

        if is_pdf:
            page_images = render_pdf_to_images(contents)
            for page_index, image in enumerate(page_images):
                engine = get_ocr_engine()
                if hasattr(engine, "predict"):
                    result = engine.predict(image)
                else:
                    result = engine.ocr(image, cls=True)
                normalized = normalize_ocr_result(result)

                # Store OCR results for debugging/review
                review_queue.store_ocr_results(
                    document_name=file.filename or "unknown",
                    page_number=page_index + 1,
                    ocr_blocks=normalized,
                )

                # Extract text and calculate confidence
                full_text = "\n".join(item["text"] for item in normalized)
                avg_confidence = (
                    sum(item["confidence"] for item in normalized) / len(normalized)
                    if normalized
                    else 0.0
                )

                # Extract tasks
                tasks = extract_tasks(full_text)

                # Enqueue for review
                source_page = f"{file.filename}:page_{page_index + 1}"
                queue_result = enqueue_tasks_for_review(
                    tasks=tasks,
                    source_page=source_page,
                    ocr_confidence=avg_confidence,
                )
                total_queued += queue_result["queued"]

            return {
                "filename": file.filename,
                "page_count": len(page_images),
                "queued": total_queued,
                "status": "processed",
            }

        image = decode_image_bytes(contents)
        result = get_ocr_engine().predict(image)
        normalized = normalize_ocr_result(result)

        # Store OCR results for debugging/review
        review_queue.store_ocr_results(
            document_name=file.filename or "unknown",
            page_number=1,
            ocr_blocks=normalized,
        )

        # Extract text and calculate confidence
        full_text = "\n".join(item["text"] for item in normalized)
        avg_confidence = (
            sum(item["confidence"] for item in normalized) / len(normalized)
            if normalized
            else 0.0
        )

        # Extract tasks
        tasks = extract_tasks(full_text)

        # Enqueue for review
        source_page = file.filename
        queue_result = enqueue_tasks_for_review(
            tasks=tasks,
            source_page=source_page,
            ocr_confidence=avg_confidence,
        )

        return {
            "filename": file.filename,
            "page_count": 1,
            "queued": queue_result["queued"],
            "status": "processed",
        }
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - error path for runtime failures
        raise HTTPException(
            status_code=500, detail=f"OCR processing failed: {str(exc)}"
        )


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def enqueue_tasks_for_review(
    tasks: list,
    source_page: str,
    ocr_confidence: float = 0.9,
    confidence_threshold: float = 0.8,
) -> dict:
    """
    Enqueue tasks that meet review criteria to the review queue.

    Tasks are queued if:
    - OCR confidence is below threshold (document quality issue)
    - Task text contains unresolved shorthand
    - Task confidence is below threshold

    Args:
        tasks: List of extracted task dicts
        source_page: Source page identifier (e.g., "document.pdf:page_1")
        ocr_confidence: Overall OCR confidence for the page
        confidence_threshold: Minimum confidence to skip review

    Returns:
        Dict with summary of queued tasks
    """
    queued = 0
    skipped = 0
    reasons = []

    # Initialize review_queue database if needed
    if not review_queue.DB_PATH.exists():
        review_queue.init_db()

    # Shorthand patterns we haven't fully resolved
    unresolved_shorthand = [r"\b\w{1,3}/\w{1,3}\b", r"\b[a-z]{1,4}\s*-\s*[a-z]{1,4}\b"]

    for task in tasks:
        task_text = task.get("text", "")
        entities = task.get("entities", [])
        themes = task.get("themes", [])
        reasons_for_task = []

        # Check OCR confidence
        if ocr_confidence < confidence_threshold:
            reasons_for_task.append("low_ocr_confidence")

        # Check for unresolved shorthand
        for pattern in unresolved_shorthand:
            if re.search(pattern, task_text, re.IGNORECASE):
                reasons_for_task.append("unresolved_shorthand")
                break

        # Enqueue if any review criteria met
        if reasons_for_task:
            source_hash = hashlib.md5(task_text.encode()).hexdigest()
            review_queue.add_task_to_queue(
                source_page=source_page,
                raw_text=task_text,
                entities=entities,
                themes=themes,
                reason="|".join(reasons_for_task),
                confidence=ocr_confidence,
                source_hash=source_hash,
            )
            queued += 1
            reasons.extend(reasons_for_task)
        else:
            skipped += 1

    return {
        "queued": queued,
        "skipped": skipped,
        "reasons": list(set(reasons)),
    }


# Pydantic models for API requests
class RejectRequest(BaseModel):
    reason: str = ""


class EditRequest(BaseModel):
    new_text: str
    reason: str = ""


# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# API endpoints for review queue management
@app.get("/")
async def root():
    """Serve the web UI."""
    return {"message": "Visit /static/index.html"}


@app.get("/api/queue")
def get_queue_status():
    """Get current review queue status."""
    review_queue.init_db()

    pending = review_queue.get_review_queue(limit=100)
    approved = review_queue.get_approved_tasks(limit=100)

    # Parse JSON strings back to objects
    for task in pending:
        if isinstance(task.get("entities"), str):
            import json

            task["entities"] = json.loads(task["entities"] or "[]")
        if isinstance(task.get("themes"), str):
            import json

            task["themes"] = json.loads(task["themes"] or "[]")

    return {
        "pending": pending,
        "approved": approved,
        "rejected": [],  # Could add rejected tracking if needed
    }


@app.post("/api/approve/{task_id}")
def approve_task_endpoint(task_id: int):
    """Approve a task."""
    success = review_queue.approve_task(task_id, approved_by="web_user")
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "approved"}


@app.post("/api/reject/{task_id}")
def reject_task_endpoint(task_id: int, request: RejectRequest):
    """Reject a task."""
    success = review_queue.reject_task(
        task_id, reason=request.reason, rejected_by="web_user"
    )
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "rejected"}


@app.post("/api/edit/{task_id}")
def edit_task_endpoint(task_id: int, request: EditRequest):
    """Edit and approve a task."""
    success = review_queue.edit_task(
        task_id, new_text=request.new_text, reason=request.reason, edited_by="web_user"
    )
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "edited_and_approved"}


@app.get("/api/documents")
def list_documents():
    """Get all documents with OCR results."""
    docs = review_queue.get_documents()
    return {"documents": docs}


@app.get("/api/ocr/{document_name}")
def get_ocr_results(document_name: str, page: Optional[int] = None):
    """Get OCR results for a document (optionally filtered by page)."""
    results = review_queue.get_ocr_results(document_name, page_number=page)
    return {
        "document": document_name,
        "page": page,
        "blocks": results,
        "total": len(results),
    }


@app.get("/api/ocr/{document_name}/pages")
def get_ocr_pages(document_name: str):
    """Get all pages for a document."""
    results = review_queue.get_ocr_results(document_name)
    # Group by page number
    pages = {}
    for block in results:
        page_num = block["page_number"]
        if page_num not in pages:
            pages[page_num] = []
        pages[page_num].append(block)

    return {
        "document": document_name,
        "pages": pages,
        "page_count": len(pages),
    }
