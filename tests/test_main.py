import io

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health_endpoint_returns_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_upload_requires_image_content_type():
    response = client.post(
        "/upload",
        files={"file": ("notes.txt", b"hello world", "text/plain")},
    )

    assert response.status_code == 400
    assert "image" in response.json()["detail"].lower()


def test_invalid_image_bytes_are_rejected():
    response = client.post(
        "/upload",
        files={"file": ("broken.png", b"not-a-real-image", "image/png")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid image file format."


def test_ocr_engine_is_initialized_lazily():
    class DummyBlock:
        def __init__(self):
            self.label = "text"
            self.bbox = [0, 0, 10, 10]
            self.content = "hello"
            self.score = 0.99

    class DummyResult(dict):
        def __init__(self):
            super().__init__()
            self["parsing_res_list"] = [DummyBlock()]

    class DummyOCR:
        def predict(self, image):
            return [DummyResult()]

    main._ocr_engine = None
    main.PaddleOCRVL = lambda **kwargs: DummyOCR()

    engine = main.get_ocr_engine()
    result = engine.predict(None)
    assert result[0]["parsing_res_list"][0].label == "text"


def test_valid_image_upload_returns_standardized_results():
    class DummyBlock:
        def __init__(self):
            self.label = "text"
            self.bbox = [0, 0, 10, 10]
            self.content = "hello"
            self.score = 0.99

    class DummyResult(dict):
        def __init__(self):
            super().__init__()
            self["parsing_res_list"] = [DummyBlock()]

    class DummyOCR:
        def predict(self, image):
            return [DummyResult()]

    main._ocr_engine = DummyOCR()

    image = np.zeros((10, 10, 3), dtype=np.uint8)
    success, encoded = cv2.imencode(".png", image)
    assert success is True
    image_bytes = encoded.tobytes()

    response = client.post(
        "/upload",
        files={"file": ("note.png", image_bytes, "image/png")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "note.png"
    assert payload["status"] == "processed"
    assert "queued" in payload
