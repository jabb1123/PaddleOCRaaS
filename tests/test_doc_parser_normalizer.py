import main

SAMPLE_DOC_RESULT = {
    "res": {
        "parsing_res_list": [
            {
                "block_content": "Moloss + SBCs",
                "score": 0.99,
                "block_bbox": [66, 150, 694, 232],
            },
            {
                "block_content": "Need to bring this to engineering support",
                "score": 0.91,
                "block_bbox": [31, 1799, 1557, 2122],
            },
        ]
    }
}


def test_doc_parser_normalizer_extracts_block_text():
    parsed = main.normalize_ocr_result(SAMPLE_DOC_RESULT)

    assert len(parsed) == 2
    assert parsed[0]["text"] == "Moloss + SBCs"
    assert parsed[0]["confidence"] == 0.99
    assert parsed[1]["text"] == "Need to bring this to engineering support"
