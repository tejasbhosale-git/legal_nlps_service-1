# Main App: Legal AI Pipeline Orchestration

## Overview
Main orchestration app that coordinates all NLP services and integrates with Azure OpenAI GPT-4o.

## Features
- **Multi-Service Coordination**: Calls all NLP services
- **Azure OpenAI Integration**: GPT-4o for legal analysis
- **Gradio Interface**: Beautiful web UI
- **Flask API**: RESTful endpoints

## Environment Variables
```bash
# NLP Service URLs
DOC_CLASSIFIER_URL=https://your-doc-classifier.onrender.com
ENTITY_RECOGNIZER_URL=https://your-entity-recognizer.onrender.com
CLAUSE_ANALYZER_URL=https://your-clause-analyzer.onrender.com

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

## API Endpoints

### Health Check
```
GET /
```

### Analyze Document
```
POST /analyze
Content-Type: application/json

{
  "text": "This is a legal document...",
  "analysis_type": "Full Legal Analysis"
}
```

## Gradio Interface
- **URL**: `https://your-main-app.onrender.com`
- **Features**: Document upload, analysis type selection, results display

## Deployment
- **Platform**: Render Free Tier
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: Auto-set by Render

## Dependencies
- No heavy models (just orchestration)
- Memory usage: ~100MB
- Fast startup time
