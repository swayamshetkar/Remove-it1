# Use Python 3.10 slim base image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the u2netp model into /app/models
RUN python -c "from rembg import new_session; import os; os.makedirs('/app/models', exist_ok=True); new_session('u2netp', model_dir='/app/models')"

# Copy app code
COPY . .

# Tell rembg to use /app/models
ENV U2NET_HOME=/app/models

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", ":app", "--host", "0.0.0.0", "--port", "8000"]
