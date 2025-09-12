# Service 2: Entity Recognizer

## Overview
Lightweight NER model for legal entity extraction.

## Model
- **Model**: `dbmdz/bert-large-cased-finetuned-conll03-english` (fallback: `distilbert-base-cased`)
- **Size**: ~50-100MB
- **Memory Usage**: ~150MB
- **Task**: Named Entity Recognition

## API Endpoints

### Health Check
```
GET /
```

### Extract Entities
```
POST /extract
Content-Type: application/json

{
  "text": "This is a legal document text..."
}
```

### Batch Extract
```
POST /batch_extract
Content-Type: application/json

{
  "texts": ["Document 1...", "Document 2..."]
}
```

## Response Format
```json
{
  "entities": {
    "B-PER": [{"text": "John Smith", "confidence": 0.95, "start": 0, "end": 9}],
    "B-ORG": [{"text": "ABC Corp", "confidence": 0.88, "start": 15, "end": 23}]
  },
  "total_entities": 2,
  "entity_types": ["B-PER", "B-ORG"],
  "text_length": 150
}
```

## Deployment
- **Platform**: Render Free Tier
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: Auto-set by Render
