# Main App Dockerfile (Root deployment)
FROM python:3.9-slim

WORKDIR /app

# Copy main-app requirements
COPY main-app/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main-app application code
COPY main-app/ .

# Expose port
EXPOSE $PORT

# Start command
CMD gunicorn --bind 0.0.0.0:$PORT app:app
