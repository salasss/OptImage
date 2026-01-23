# Image Optimizer API
![Python Version](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
A lightweight microservice for optimizing and resizing images using FastAPI.

## Features

- **Image Optimization** : Compress images while maintaining quality
- **Image Resizing** : Resize images with aspect ratio preservation
- **Format Conversion** : Convert images to WebP, JPEG, or PNG
- **Background Tasks** : Archive original images asynchronously
- **Health Checks** : Monitor API health status
- **Metrics** : Prometheus metrics for monitoring

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/salasss/OptImage.git
cd OptImage
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at `http://localhost:8000`
- **API Docs** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health

### Run with Docker

```bash
# Build the image
docker build -t image-optimizer-api .

# Run the container
docker run -d -p 8000:8000 --name image-optimizer image-optimizer-api
```

## API Endpoints

### `GET /`
Returns API information.

**Response:**
```json
{
  "message": "Image Optimizer API is running",
  "docs": "/docs"
}
```

### `POST /optimize`
Optimize and resize an image.

**Parameters:**
- `file` (required): Image file to optimize
- `width` (optional): Target width in pixels
- `height` (optional): Target height in pixels
- `format` (optional): Output format - WEBP (default), JPEG, or PNG
- `quality` (optional): Quality level 1-100 (default: 80)

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/optimize" \
  -F "file=@image.jpg" \
  -F "width=800" \
  -F "format=WEBP" \
  -F "quality=85" \
  --output optimized.webp
```

**Example with Python:**
```python
import requests

with open("image.jpg", "rb") as f:
    files = {"file": f}
    data = {
        "width": 800,
        "format": "WEBP",
        "quality": 85
    }
    response = requests.post("http://localhost:8000/optimize", 
                            files=files, data=data)
    
    with open("optimized.webp", "wb") as output:
        output.write(response.content)
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Project Structure

```
image-optimizer-api/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/                    # API routes
│   ├── core/                   # Configuration
│   └── services/
│       └── image_processor.py  # Image processing logic
├── tests/                      # Unit tests
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
└── README.md
```

## Dependencies

- **FastAPI** : Modern web framework
- **Uvicorn** : ASGI server
- **Pillow** : Image processing
- **python-multipart** : File upload handling
- **prometheus-fastapi-instrumentator** : Metrics collection
- **pytest** : Testing framework
- **httpx** : HTTP client for tests

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Monitoring

Prometheus metrics are exposed at `http://localhost:8000/metrics`

## License

MIT

