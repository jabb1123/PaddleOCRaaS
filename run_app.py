#!/usr/bin/env python3
"""
Start the PaddleOCR Review Queue web app.

Usage:
    python run_app.py                          # Default: localhost:8000
    python run_app.py --host 0.0.0.0 --port 8080

Environment variables:
    PADDLEOCR_HOST - Server host (default: 127.0.0.1, use 0.0.0.0 for Docker)
    PADDLEOCR_PORT - Server port (default: 8000)

Docker usage:
    docker run -p 5000:8000 -e PADDLEOCR_HOST=0.0.0.0 -e PADDLEOCR_PORT=8000 paddleocraas:latest
"""
import os
import argparse

import uvicorn

def parse_args():
    parser = argparse.ArgumentParser(description="Start PaddleOCR Review Queue web app")
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: from env or 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind to (default: from env or 8000)",
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="Number of worker processes (default: 1)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Get host and port from args, env vars, or defaults
    host = args.host or os.getenv("PADDLEOCR_HOST", "127.0.0.1")
    port = args.port or int(os.getenv("PADDLEOCR_PORT", "8000"))
    workers = args.workers

    print("Starting PaddleOCR Review Queue web app...")
    print(f"Visit http://{host}:{port}/static/index.html")
    print("Press Ctrl+C to stop\n")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,
        log_level="info",
    )
