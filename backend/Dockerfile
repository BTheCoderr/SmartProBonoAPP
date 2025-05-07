# Use Python 3.11 slim image
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages
RUN pip uninstall -y bson pymongo flask-pymongo && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Set ownership to appuser
RUN chown -R appuser:appuser /app

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/uploads /app/instance \
    && chmod 755 /app/logs /app/uploads /app/instance \
    && chown -R appuser:appuser /app/logs /app/uploads /app/instance

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 