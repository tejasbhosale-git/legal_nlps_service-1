"""
Service 2: Entity Recognition
Lightweight NER model for legal entity extraction
Deploy on Render Free Tier
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

class EntityRecognizer:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load lightweight NER model"""
        try:
            logger.info("Loading NER model for entity recognition...")
            # Using a smaller NER model that fits in 512MB
            self.model = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("✅ Entity recognizer loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load NER model: {str(e)}")
            # Fallback to a smaller model
            try:
                self.model = pipeline(
                    "ner",
                    model="distilbert-base-cased",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("✅ Fallback NER model loaded!")
            except Exception as e2:
                logger.error(f"❌ Fallback model also failed: {str(e2)}")
                self.model = None
    
    def extract_entities(self, text: str) -> dict:
        """Extract legal entities from text"""
        if not self.model:
            return {"error": "Model not loaded"}
        
        try:
            entities = self.model(text)
            
            # Group entities by type
            entity_groups = {}
            for entity in entities:
                label = entity["entity"]
                if label not in entity_groups:
                    entity_groups[label] = []
                entity_groups[label].append({
                    "text": entity["word"],
                    "confidence": entity["score"],
                    "start": entity["start"],
                    "end": entity["end"]
                })
            
            return {
                "entities": entity_groups,
                "total_entities": len(entities),
                "entity_types": list(entity_groups.keys()),
                "text_length": len(text)
            }
        except Exception as e:
            return {"error": f"Entity extraction failed: {str(e)}"}

# Initialize recognizer
recognizer = EntityRecognizer()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "Entity Recognizer",
        "status": "running",
        "model_loaded": recognizer.model is not None
    })

@app.route('/extract', methods=['POST'])
def extract_entities():
    """Extract entities from text"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        result = recognizer.extract_entities(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in extract_entities endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/batch_extract', methods=['POST'])
def batch_extract():
    """Batch extract entities from multiple texts"""
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({"error": "Texts array required"}), 400
        
        texts = data['texts']
        if not isinstance(texts, list):
            return jsonify({"error": "Texts must be an array"}), 400
        
        results = []
        for text in texts:
            result = recognizer.extract_entities(text)
            results.append(result)
        
        return jsonify({"results": results})
        
    except Exception as e:
        logger.error(f"Error in batch_extract endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
