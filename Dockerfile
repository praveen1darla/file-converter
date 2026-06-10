FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for poppler (PDF to image) and other tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /tmp/FileConverter

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run with gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120"]
