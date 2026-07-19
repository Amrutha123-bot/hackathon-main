# Use slim Python image to minimize base image size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only the minimal system dependencies needed
# build-essential: for compiling Python packages with C extensions (chromadb needs it)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY backend/ .

# Render expects the service to listen on port 10000
EXPOSE 10000

# Run the FastAPI application with uvicorn
# --host 0.0.0.0 makes it accessible from outside the container
# --port 10000 is Render's expected port for free tier
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]