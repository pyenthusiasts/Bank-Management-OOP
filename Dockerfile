# Dockerfile for Bank Management System

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package
RUN pip install -e .

# Create a non-root user
RUN useradd -m -u 1000 bankuser && \
    chown -R bankuser:bankuser /app
USER bankuser

# Expose port (if needed for web interface in future)
EXPOSE 8000

# Default command - run CLI
CMD ["python", "-m", "bank_management.cli"]
