# Service 1: Document Classifier

## Overview
Lightweight DistilBERT model for legal document type classification.

## Model
- **Model**: `distilbert-base-uncased`
- **Size**: ~250MB
- **Memory Usage**: ~300MB
- **Task**: Document type classification

## API Endpoints

### Health Check
```
GET /
```

### Classify Document
```
POST /classify
Content-Type: application/json

{
  "text": "This is a legal document text..."
}
```

### Batch Classify
```
POST /batch_classify
Content-Type: application/json

{
  "texts": ["Document 1...", "Document 2..."]
}
```

## Response Format
```json
{
  "document_type": "LABEL_0",
  "confidence": 0.95,
  "text_length": 150,
  "word_count": 25
}
```

## Deployment
- **Platform**: Render Free Tier
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: Auto-set by Render
