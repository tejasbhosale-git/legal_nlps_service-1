"""
Unified Legal NLP Services
All 3 NLP services in one Flask application for Railway deployment
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
    """Service 1: Lightweight Document Classification"""
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

class EntityRecognizer:
    """Service 2: Entity Recognition"""
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load lightweight NER model"""
        try:
            logger.info("Loading NER model for entity recognition...")
            # Using a smaller NER model that fits in memory limits
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

class ClauseAnalyzer:
    """Service 3: Clause Analysis"""
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load model for clause analysis"""
        try:
            logger.info("Loading model for clause analysis...")
            # Try to load a legal-specific model first
            try:
                self.model = pipeline(
                    "text-classification",
                    model="nlpaueb/legal-bert-base-uncased",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("✅ Legal-BERT loaded successfully!")
            except:
                # Fallback to DistilBERT if legal model is too large
                logger.info("Legal-BERT too large, using DistilBERT...")
                self.model = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("✅ DistilBERT loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            self.model = None
    
    def analyze_clauses(self, text: str) -> dict:
        """Analyze contract clauses for risks and types"""
        if not self.model:
            return {"error": "Model not loaded"}
        
        try:
            # Split text into sentences for clause analysis
            sentences = text.split('. ')
            clauses = []
            
            for sentence in sentences:
                if len(sentence.strip()) > 10:  # Only analyze meaningful sentences
                    result = self.model(sentence)
                    clauses.append({
                        "text": sentence.strip(),
                        "classification": result[0]["label"],
                        "confidence": result[0]["score"],
                        "risk_level": self._assess_risk(result[0]["label"], result[0]["score"])
                    })
            
            # Overall risk assessment
            high_risk_clauses = [c for c in clauses if c["risk_level"] == "High"]
            medium_risk_clauses = [c for c in clauses if c["risk_level"] == "Medium"]
            
            return {
                "clauses": clauses,
                "total_clauses": len(clauses),
                "risk_summary": {
                    "high_risk": len(high_risk_clauses),
                    "medium_risk": len(medium_risk_clauses),
                    "low_risk": len(clauses) - len(high_risk_clauses) - len(medium_risk_clauses)
                },
                "overall_risk": self._calculate_overall_risk(clauses),
                "text_length": len(text)
            }
        except Exception as e:
            return {"error": f"Clause analysis failed: {str(e)}"}
    
    def _assess_risk(self, label: str, confidence: float) -> str:
        """Assess risk level based on classification"""
        risk_keywords = ["termination", "penalty", "liability", "indemnity", "breach", "damages"]
        label_lower = label.lower()
        
        if any(keyword in label_lower for keyword in risk_keywords):
            return "High" if confidence > 0.7 else "Medium"
        elif confidence > 0.8:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_overall_risk(self, clauses: list) -> str:
        """Calculate overall document risk"""
        if not clauses:
            return "Unknown"
        
        high_risk_count = sum(1 for c in clauses if c["risk_level"] == "High")
        medium_risk_count = sum(1 for c in clauses if c["risk_level"] == "Medium")
        
        if high_risk_count > len(clauses) * 0.3:
            return "High"
        elif high_risk_count > 0 or medium_risk_count > len(clauses) * 0.5:
            return "Medium"
        else:
            return "Low"

# Initialize all services
doc_classifier = DocumentClassifier()
entity_recognizer = EntityRecognizer()
clause_analyzer = ClauseAnalyzer()

# Health check endpoint
@app.route('/')
def health_check():
    """Health check endpoint for all services"""
    return jsonify({
        "service": "Unified Legal NLP Services",
        "status": "running",
        "services": {
            "document_classifier": True,
            "entity_recognizer": entity_recognizer.model is not None,
            "clause_analyzer": clause_analyzer.model is not None
        }
    })

# Service 1: Document Classification
@app.route('/classify', methods=['POST'])
def classify_document():
    """Classify document type"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        result = doc_classifier.classify_document(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in classify endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Service 2: Entity Recognition
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
        
        result = entity_recognizer.extract_entities(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in extract_entities endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Service 3: Clause Analysis
@app.route('/analyze', methods=['POST'])
def analyze_clauses():
    """Analyze contract clauses"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        result = clause_analyzer.analyze_clauses(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_clauses endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Combined analysis endpoint
@app.route('/analyze_all', methods=['POST'])
def analyze_all():
    """Run all NLP services on the text"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Run all services
        classification = doc_classifier.classify_document(text)
        entities = entity_recognizer.extract_entities(text)
        clauses = clause_analyzer.analyze_clauses(text)
        
        return jsonify({
            "document_classification": classification,
            "entity_recognition": entities,
            "clause_analysis": clauses,
            "text_length": len(text),
            "word_count": len(text.split())
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_all endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
