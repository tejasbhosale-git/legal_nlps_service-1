# Service 2 - Entity Recognizer Dockerfile (Root deployment)
FROM python:3.9-slim

WORKDIR /app

# Copy service2 requirements
COPY service2-entity-recognizer/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service2 application code
COPY service2-entity-recognizer/ .

# Expose port
EXPOSE $PORT

# Start command
CMD gunicorn --bind 0.0.0.0:$PORT app:app
