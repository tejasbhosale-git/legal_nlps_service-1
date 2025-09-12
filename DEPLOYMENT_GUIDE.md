# 🚀 Legal AI Pipeline - Multi-Service Deployment Guide

## 🏗️ Architecture Overview

```
Service 1: Document Classifier (DistilBERT) → Render Free Tier
Service 2: Entity Recognizer (NER Model) → Render Free Tier  
Service 3: Clause Analyzer (Legal-BERT) → Render Free Tier
Main App: Orchestration + Azure GPT-4o → Render Free Tier
```

## 📋 Deployment Steps

### **Step 1: Deploy Service 1 - Document Classifier**

1. **Create new Render Web Service**
   - Name: `legal-ai-doc-classifier`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

2. **Environment Variables**
   - `PORT`: `5000` (auto-set by Render)

3. **Files to upload**
   - `app.py`
   - `requirements.txt`

### **Step 2: Deploy Service 2 - Entity Recognizer**

1. **Create new Render Web Service**
   - Name: `legal-ai-entity-recognizer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

2. **Environment Variables**
   - `PORT`: `5001` (auto-set by Render)

3. **Files to upload**
   - `service2_entity_recognizer.py`
   - `requirements_service2.txt`

### **Step 3: Deploy Service 3 - Clause Analyzer**

1. **Create new Render Web Service**
   - Name: `legal-ai-clause-analyzer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements_service3.txt`
   - Start Command: `python service3_clause_analyzer.py`

2. **Environment Variables**
   - `PORT`: `5002` (auto-set by Render)

3. **Files to upload**
   - `service3_clause_analyzer.py`
   - `requirements_service3.txt`

### **Step 4: Deploy Main App - Orchestration**

1. **Create new Render Web Service**
   - Name: `legal-ai-main-app`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements_main.txt`
   - Start Command: `python main_app.py`

2. **Environment Variables**
   - `DOC_CLASSIFIER_URL`: `https://legal-ai-doc-classifier.onrender.com`
   - `ENTITY_RECOGNIZER_URL`: `https://legal-ai-entity-recognizer.onrender.com`
   - `CLAUSE_ANALYZER_URL`: `https://legal-ai-clause-analyzer.onrender.com`
   - `AZURE_OPENAI_ENDPOINT`: `https://your-resource.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions`
   - `AZURE_OPENAI_API_KEY`: `your_azure_openai_api_key_here`
   - `AZURE_OPENAI_API_VERSION`: `2025-01-01-preview`
   - `AZURE_OPENAI_DEPLOYMENT_NAME`: `gpt-4o`

3. **Files to upload**
   - `main_app.py`
   - `requirements_main.txt`

## 🎯 Expected Memory Usage

- **Service 1**: ~300MB (DistilBERT)
- **Service 2**: ~150MB (NER Model)
- **Service 3**: ~200MB (Legal-BERT)
- **Main App**: ~100MB (No heavy models)

**Total**: Each service stays well under 512MB limit! ✅

## 🔗 Service URLs

After deployment, you'll get URLs like:
- `https://legal-ai-doc-classifier.onrender.com`
- `https://legal-ai-entity-recognizer.onrender.com`
- `https://legal-ai-clause-analyzer.onrender.com`
- `https://legal-ai-main-app.onrender.com`

## 🧪 Testing

1. **Test individual services**:
   ```bash
   curl -X POST https://legal-ai-doc-classifier.onrender.com/classify \
        -H "Content-Type: application/json" \
        -d '{"text": "This is a contract agreement"}'
   ```

2. **Test main app**:
   - Visit: `https://legal-ai-main-app.onrender.com`
   - Use the Gradio interface

## 🎉 Benefits

✅ **Free Tier Compatible**: Each service under 512MB  
✅ **Scalable**: Deploy services independently  
✅ **Fault Tolerant**: If one service fails, others continue  
✅ **Cost Effective**: No heavy model hosting costs  
✅ **Fast**: Lightweight models load quickly  

## 🚀 Ready to Deploy!

Your **Legal AI Pipeline** is ready for multi-service deployment! 🎯
