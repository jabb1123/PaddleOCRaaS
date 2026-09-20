# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV, PaddleOCR, and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY review_queue.py .
COPY run_app.py .
COPY static/ ./static/

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables for Docker deployment
ENV PADDLEOCR_HOST=0.0.0.0
ENV PADDLEOCR_PORT=8000

# Expose port (can be overridden with -p in docker run)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "run_app.py"]
