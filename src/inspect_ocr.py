from pathlib import Path
from pprint import pprint

from main import render_pdf_to_images, get_ocr_engine

pdf = Path('data/Note Aug 10, 2026.pdf').read_bytes()
images = render_pdf_to_images(pdf)
ocr = get_ocr_engine()
result = ocr.predict(images[0])
print('TYPE:', type(result))
if isinstance(result, dict):
    print('KEYS:', list(result.keys()))
    for key, value in result.items():
        print('KEY', key, 'TYPE', type(value))
        if isinstance(value, dict):
            print('  SUBKEYS', list(value.keys())[:10])
        elif isinstance(value, list):
            print('  LIST_LEN', len(value))
            if value:
                first = value[0]
                print('  FIRST_TYPE', type(first))
                if isinstance(first, dict):
                    print('  FIRST_KEYS', list(first.keys())[:10])
                elif isinstance(first, (list, tuple)):
                    print('  FIRST_LEN', len(first))
                    print('  FIRST_SAMPLE', first[:2])
        break
else:
    print('NOT_DICT')
    print(type(result[0]) if isinstance(result, list) else type(result))
    if isinstance(result, list):
        print(result[:2])
