# Railway Deployment Guide for Legal NLP Pipeline

This guide explains how to deploy the Legal NLP Pipeline microservices architecture on Railway.

## Architecture Overview

The project consists of 4 services:
1. **Main App** - Orchestration service with Gradio UI
2. **Service 1** - Document Classifier (Lightweight)
3. **Service 2** - Entity Recognizer
4. **Service 3** - Clause Analyzer

## Prerequisites

1. Railway account ([railway.app](https://railway.app))
2. GitHub repository with your code
3. Azure OpenAI account and API keys

## Deployment Steps

### 1. Deploy Each Service Separately

Deploy each service as a separate Railway project:

#### Main App Deployment
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `main-app/`
4. Railway will auto-detect Python and use `requirements.txt`
5. Set environment variables:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   DOC_CLASSIFIER_URL=https://your-service1-url.railway.app
   ENTITY_RECOGNIZER_URL=https://your-service2-url.railway.app
   CLAUSE_ANALYZER_URL=https://your-service3-url.railway.app
   ```

#### Service 1 - Document Classifier
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `service1-doc-classifier/`
4. Use `requirements_lightweight.txt` for faster deployment
5. No additional environment variables needed

#### Service 2 - Entity Recognizer
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `service2-entity-recognizer/`
4. Railway will use `requirements.txt`
5. No additional environment variables needed

#### Service 3 - Clause Analyzer
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `service3-clause-analyzer/`
4. Railway will use `requirements.txt`
5. No additional environment variables needed

### 2. Configure Service URLs

After all services are deployed, update the Main App environment variables with the actual Railway URLs:

```bash
DOC_CLASSIFIER_URL=https://service1-doc-classifier-production.railway.app
ENTITY_RECOGNIZER_URL=https://service2-entity-recognizer-production.railway.app
CLAUSE_ANALYZER_URL=https://service3-clause-analyzer-production.railway.app
```

### 3. Custom Start Commands

Each service uses these start commands (configured in `railway.json`):

- **Main App**: `gunicorn --bind 0.0.0.0:$PORT main-app.app:app`
- **Service 1**: `gunicorn --bind 0.0.0.0:$PORT app_lightweight:app`
- **Service 2**: `gunicorn --bind 0.0.0.0:$PORT app:app`
- **Service 3**: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 4. Memory and Resource Optimization

For Railway's resource limits:

- **Service 1** uses the lightweight version (`app_lightweight.py`) with keyword matching instead of ML models
- **Services 2 & 3** use smaller transformer models that fit within memory limits
- All services include fallback mechanisms for model loading

## Environment Variables

### Main App Required Variables:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
DOC_CLASSIFIER_URL=https://your-service1.railway.app
ENTITY_RECOGNIZER_URL=https://your-service2.railway.app
CLAUSE_ANALYZER_URL=https://your-service3.railway.app
```

### Service Environment Variables:
- Services 1-3 don't require additional environment variables
- Railway automatically provides `PORT` variable

## Testing the Deployment

### Health Checks
Each service has a health check endpoint at `/`:
- Main App: `https://your-main-app.railway.app/`
- Service 1: `https://your-service1.railway.app/`
- Service 2: `https://your-service2.railway.app/`
- Service 3: `https://your-service3.railway.app/`

### API Endpoints
- **Main App**: `/analyze` (POST) - Complete legal analysis
- **Service 1**: `/classify` (POST) - Document classification
- **Service 2**: `/extract` (POST) - Entity extraction
- **Service 3**: `/analyze` (POST) - Clause analysis

### Test Request Example:
```bash
curl -X POST https://your-main-app.railway.app/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This employment agreement is between ABC Corp and John Smith...", "analysis_type": "Contract Review"}'
```

## Troubleshooting

### Common Issues:

1. **Service Connection Errors**
   - Verify all service URLs are correct in Main App environment variables
   - Check that all services are running and healthy

2. **Memory Issues**
   - Service 1 uses lightweight keyword matching
   - Services 2 & 3 have fallback models for memory constraints

3. **Model Loading Errors**
   - Check service logs in Railway dashboard
   - Models automatically fall back to smaller alternatives

4. **Azure OpenAI Errors**
   - Verify API key and endpoint are correct
   - Check Azure OpenAI service quota and limits

## Cost Optimization

- Use Service 1's lightweight version for better resource usage
- Railway provides $5/month free tier
- Monitor usage in Railway dashboard
- Consider using Railway's sleep mode for development

## Monitoring

- Use Railway's built-in logging and monitoring
- Each service provides health check endpoints
- Main app includes comprehensive error handling and logging

## Security

- Store API keys as Railway environment variables (encrypted)
- Use HTTPS for all service communication
- Railway provides automatic SSL certificates

## Scaling

- Railway automatically handles scaling based on traffic
- Each service can be scaled independently
- Consider upgrading Railway plan for higher traffic

---

**Note**: This deployment uses a microservices architecture where each service runs independently. The Main App orchestrates calls to all NLP services and combines results with Azure OpenAI for comprehensive legal analysis.
