"""
Service 3: Clause Analysis
Lightweight model for contract clause classification and risk detection
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

class ClauseAnalyzer:
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

# Initialize analyzer
analyzer = ClauseAnalyzer()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "Clause Analyzer",
        "status": "running",
        "model_loaded": analyzer.model is not None
    })

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
        
        result = analyzer.analyze_clauses(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_clauses endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/batch_analyze', methods=['POST'])
def batch_analyze():
    """Batch analyze multiple texts"""
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({"error": "Texts array required"}), 400
        
        texts = data['texts']
        if not isinstance(texts, list):
            return jsonify({"error": "Texts must be an array"}), 400
        
        results = []
        for text in texts:
            result = analyzer.analyze_clauses(text)
            results.append(result)
        
        return jsonify({"results": results})
        
    except Exception as e:
        logger.error(f"Error in batch_analyze endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
