import numpy as np
import cv2
from fastapi.testclient import TestClient
import main

class DummyOCR:
    def ocr(self, image, cls=True):
        return [[[[0,0],[10,0],[10,10],[0,10]], ('hello', 0.99)]]

main._ocr_engine = DummyOCR()
img = np.zeros((10, 10, 3), dtype=np.uint8)
_, encoded = cv2.imencode('.png', img)
raw = encoded.tobytes()
client = TestClient(main.app)
resp = client.post('/upload', files={'file': ('note.png', raw, 'image/png')})
print('status=', resp.status_code)
print('body=', resp.text)
print('json=', resp.json())
