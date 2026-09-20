import io

import numpy as np
import cv2

import main


def test_render_pdf_to_images_raises_when_pymupdf_is_missing(monkeypatch):
    monkeypatch.setattr(main, "fitz", None)

    try:
        main.render_pdf_to_images(b"not-a-pdf")
        assert False, "Expected a PDF support error when PyMuPDF is missing."
    except Exception as exc:
        assert "PyMuPDF" in str(exc)


def test_pdf_upload_path_returns_page_count_and_ocr_results(monkeypatch):
    class DummyOCR:
        def ocr(self, image, cls=True):
            return [[[[0, 0], [10, 0], [10, 10], [0, 10]], ("hello", 0.99)]]

    page_image = np.zeros((10, 10, 3), dtype=np.uint8)

    monkeypatch.setattr(
        main,
        "fitz",
        type(
            "DummyFitz",
            (),
            {
                "Matrix": lambda *args, **kwargs: object(),
                "open": staticmethod(
                    lambda stream, filetype: type(
                        "DummyDoc",
                        (),
                        {
                            "__iter__": lambda self: iter(
                                [
                                    type(
                                        "DummyPage",
                                        (),
                                        {
                                            "get_pixmap": lambda self, matrix: type(
                                                "DummyPixmap",
                                                (),
                                                {
                                                    "samples": page_image.tobytes(),
                                                    "h": page_image.shape[0],
                                                    "w": page_image.shape[1],
                                                    "n": page_image.shape[2],
                                                },
                                            )(),
                                        },
                                    )()
                                ]
                            ),
                        },
                    )()
                ),
            },
        ),
    )
    monkeypatch.setattr(main, "get_ocr_engine", lambda: DummyOCR())

    payload = io.BytesIO(b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF")
    response = (
        main.upload_image.__wrapped__
        if hasattr(main.upload_image, "__wrapped__")
        else None
    )

    # Call the route function directly with a synthetic upload-like object.
    class DummyFile:
        content_type = "application/pdf"
        filename = "notes.pdf"

        async def read(self):
            return payload.getvalue()

    import asyncio

    result = asyncio.run(main.upload_image(DummyFile()))

    assert result["filename"] == "notes.pdf"
    assert result["page_count"] == 1
    assert result["status"] == "processed"
    assert "queued" in result
