# Service 3 - Clause Analyzer Dockerfile (Root deployment)
FROM python:3.9-slim

WORKDIR /app

# Copy service3 requirements
COPY service3-clause-analyzer/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service3 application code
COPY service3-clause-analyzer/ .

# Expose port
EXPOSE $PORT

# Start command
CMD gunicorn --bind 0.0.0.0:$PORT app:app
