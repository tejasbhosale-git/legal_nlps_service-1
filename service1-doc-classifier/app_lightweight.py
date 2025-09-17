"""
Service 1: Document Classification - Ultra Lightweight Version
Minimal model for document type classification
Deploy on Render Free Tier
"""

import os
import json
import logging
from flask import Flask, request, jsonify
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LightweightDocumentClassifier:
    def __init__(self):
        self.legal_keywords = {
            "contract": ["agreement", "contract", "terms", "conditions", "parties"],
            "employment": ["employee", "employer", "salary", "job", "work", "employment"],
            "lease": ["lease", "rent", "tenant", "landlord", "property", "rental"],
            "nda": ["confidential", "non-disclosure", "secret", "proprietary", "nda"],
            "service": ["service", "consulting", "professional", "client", "deliverable"]
        }
        logger.info("✅ Lightweight document classifier initialized!")
    
    def classify_document(self, text: str) -> dict:
        """Classify document type using keyword matching"""
        try:
            text_lower = text.lower()
            scores = {}
            
            for doc_type, keywords in self.legal_keywords.items():
                score = 0
                for keyword in keywords:
                    if keyword in text_lower:
                        score += 1
                scores[doc_type] = score / len(keywords)
            
            # Get the best match
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type]
            
            return {
                "document_type": best_type,
                "confidence": confidence,
                "text_length": len(text),
                "word_count": len(text.split()),
                "method": "keyword_matching"
            }
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}

# Initialize classifier
classifier = LightweightDocumentClassifier()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "Lightweight Document Classifier",
        "status": "running",
        "model_loaded": True
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
