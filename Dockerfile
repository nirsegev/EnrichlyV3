# Use Python 3.9 slim image
FROM python:3.9-slim

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create start script with proper environment variable evaluation
RUN echo '#!/bin/bash\nport="${PORT:-8000}"\nuvicorn main:app --host 0.0.0.0 --port "$port"' > start.sh && \
    chmod +x start.sh

# Command to run the application
CMD ["bash", "start.sh"] 