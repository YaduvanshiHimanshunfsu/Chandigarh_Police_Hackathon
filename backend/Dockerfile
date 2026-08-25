FROM python:3.11-slim

WORKDIR /app

# System dependencies for OpenCV, WeasyPrint, FFmpeg, ExifTool
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libimage-exiftool-perl \
    libgl1 \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with PyTorch CPU optimization and timeout resilience
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 --retries=10 \
        torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --default-timeout=1000 --retries=10 -r requirements.txt

# Copy application code
COPY . .

# Create directories for uploads and reports
RUN mkdir -p /app/uploads /app/reports

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
