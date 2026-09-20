#!/bin/bash
# Docker build and run script for PaddleOCRaaS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
IMAGE_NAME="paddleocraas"
IMAGE_TAG="latest"
PORT=8000
HOST="0.0.0.0"
COMMAND="run"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        build)
            COMMAND="build"
            shift
            ;;
        run)
            COMMAND="run"
            shift
            ;;
        up)
            COMMAND="compose-up"
            shift
            ;;
        down)
            COMMAND="compose-down"
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

case $COMMAND in
    build)
        echo -e "${BLUE}Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
        docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .
        echo -e "${GREEN}Build complete!${NC}"
        ;;
    
    run)
        echo -e "${BLUE}Running Docker container...${NC}"
        echo "  Host: $HOST"
        echo "  Port: $PORT"
        
        docker run -p "${PORT}:8000" \
            -e PADDLEOCR_HOST="${HOST}" \
            -e PADDLEOCR_PORT=8000 \
            -v paddleocr_db:/app \
            --name paddleocr_server \
            --rm \
            "${IMAGE_NAME}:${IMAGE_TAG}"
        ;;
    
    compose-up)
        echo -e "${BLUE}Starting with Docker Compose...${NC}"
        PADDLEOCR_PORT="${PORT}" docker-compose up -d
        echo -e "${GREEN}Container started!${NC}"
        echo -e "${BLUE}Access at: http://localhost:${PORT}/static/index.html${NC}"
        ;;
    
    compose-down)
        echo -e "${BLUE}Stopping Docker Compose...${NC}"
        docker-compose down
        echo -e "${GREEN}Stopped!${NC}"
        ;;
    
    *)
        echo "Usage: $0 {build|run|up|down} [options]"
        echo ""
        echo "Commands:"
        echo "  build           Build Docker image"
        echo "  run             Run Docker container"
        echo "  up              Start with docker-compose"
        echo "  down            Stop docker-compose"
        echo ""
        echo "Options:"
        echo "  --port PORT     Port to use (default: 8000)"
        echo "  --host HOST     Host to bind (default: 0.0.0.0)"
        echo "  --tag TAG       Image tag (default: latest)"
        ;;
esac
