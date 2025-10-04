# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for Pillow + rembg)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if you have it, else install directly
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the u2netp model into /app/models
RUN mkdir -p /app/models && \
    python -c "from rembg import download_model; download_model('u2netp', '/app/models')"

# Copy app code into container
COPY . .

# Tell rembg to use /app/models instead of ~/.u2net
ENV U2NET_HOME=/app/models

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
