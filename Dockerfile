# Use Python 3.10 slim base image
FROM python:3.10-bullseye

WORKDIR /app

# Install system dependencies for Pillow and rembg
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Tell rembg to store the model in /app/models
ENV U2NET_HOME=/app/models
RUN mkdir -p /app/models

# Preload the u2netp model at build time
RUN python -c "from rembg.session_factory import new_session; new_session('u2netp')" || true

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["sh", "-c", "uvicorn remove_bg_cli:app --host 0.0.0.0 --port $PORT"]
