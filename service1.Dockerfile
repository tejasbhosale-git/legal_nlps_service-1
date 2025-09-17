# Service 1 - Document Classifier Dockerfile (Root deployment)
FROM python:3.9-slim

WORKDIR /app

# Copy service1 requirements
COPY service1-doc-classifier/requirements_lightweight.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service1 application code
COPY service1-doc-classifier/ .

# Expose port
EXPOSE $PORT

# Start command using lightweight app
CMD gunicorn --bind 0.0.0.0:$PORT app_lightweight:app
