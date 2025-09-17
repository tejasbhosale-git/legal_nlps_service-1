"""
Service 1: Document Classification
Lightweight DistilBERT for document type classification
Deploy on Railway
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from transformers import pipeline
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class DocumentClassifier:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load lightweight model for document classification"""
        try:
            logger.info("Loading lightweight model for document classification...")
            # Use a much smaller model that fits in 512MB
            self.model = pipeline(
                "text-classification",
                model="prajjwal1/bert-tiny",  # Tiny BERT model (~50MB)
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("✅ Lightweight document classifier loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            # Fallback to even simpler approach
            try:
                logger.info("Trying fallback model...")
                self.model = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased",  # Original model as fallback
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("✅ Fallback model loaded successfully!")
            except Exception as e2:
                logger.error(f"❌ Fallback model also failed: {str(e2)}")
                self.model = None
    
    def classify_document(self, text: str) -> dict:
        """Classify document type"""
        if not self.model:
            return {"error": "Model not loaded"}
        
        try:
            result = self.model(text)
            return {
                "document_type": result[0]["label"],
                "confidence": result[0]["score"],
                "text_length": len(text),
                "word_count": len(text.split())
            }
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}

# Initialize classifier
classifier = DocumentClassifier()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "Document Classifier",
        "status": "running",
        "model_loaded": classifier.model is not None
    })

@app.route('/classify', methods=['POST'])
def classify():
    """Classify document type"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        result = classifier.classify_document(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in classify endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/batch_classify', methods=['POST'])
def batch_classify():
    """Batch classify multiple documents"""
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({"error": "Texts array required"}), 400
        
        texts = data['texts']
        if not isinstance(texts, list):
            return jsonify({"error": "Texts must be an array"}), 400
        
        results = []
        for text in texts:
            result = classifier.classify_document(text)
            results.append(result)
        
        return jsonify({"results": results})
        
    except Exception as e:
        logger.error(f"Error in batch_classify endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
