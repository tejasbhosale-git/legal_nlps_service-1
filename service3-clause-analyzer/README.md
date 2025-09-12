# Service 3: Clause Analyzer

## Overview
Lightweight model for contract clause classification and risk detection.

## Model
- **Primary**: `nlpaueb/legal-bert-base-uncased`
- **Fallback**: `distilbert-base-uncased`
- **Size**: ~100-200MB
- **Memory Usage**: ~200MB
- **Task**: Contract clause analysis & risk assessment

## API Endpoints

### Health Check
```
GET /
```

### Analyze Clauses
```
POST /analyze
Content-Type: application/json

{
  "text": "This is a contract clause text..."
}
```

### Batch Analyze
```
POST /batch_analyze
Content-Type: application/json

{
  "texts": ["Clause 1...", "Clause 2..."]
}
```

## Response Format
```json
{
  "clauses": [
    {
      "text": "Termination clause...",
      "classification": "LABEL_0",
      "confidence": 0.92,
      "risk_level": "High"
    }
  ],
  "total_clauses": 1,
  "risk_summary": {
    "high_risk": 1,
    "medium_risk": 0,
    "low_risk": 0
  },
  "overall_risk": "High",
  "text_length": 150
}
```

## Deployment
- **Platform**: Render Free Tier
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: Auto-set by Render
