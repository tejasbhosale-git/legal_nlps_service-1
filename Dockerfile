# Service 1 - Document Classifier Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_lightweight.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_lightweight.txt

# Copy application code
COPY . .

# Expose port
EXPOSE $PORT

# Start command using lightweight app
CMD gunicorn --bind 0.0.0.0:$PORT app_lightweight:app
