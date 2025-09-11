import os
import json
import logging
from typing import Dict, Any, List
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, request, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the ContractBERT model and tokenizer"""
    global model, tokenizer
    
    try:
        # Use a smaller, more efficient model for Render free tier
        model_name = "distilbert-base-uncased"  # Smaller, faster model
        
        logger.info(f"Loading model: {model_name}")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model with smaller configuration
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2,  # Binary classification
            dtype=torch.float32  # Use float32 for compatibility
        )
        
        # Move to GPU if available
        if torch.cuda.is_available():
            model = model.cuda()
            logger.info("Model loaded on GPU")
        else:
            logger.info("Model loaded on CPU")
            
        model.eval()
        logger.info("Model loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

def predict(text: str, task: str = "classification") -> Dict[str, Any]:
    """
    Run prediction on input text
    
    Args:
        text: Input text to analyze
        task: Type of task (classification, sentiment, etc.)
    
    Returns:
        Dictionary containing prediction results
    """
    global model, tokenizer
    
    if model is None or tokenizer is None:
        raise RuntimeError("Model not loaded")
    
    try:
        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # Move to GPU if available
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Get predictions
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        # Get predicted class and confidence
        predicted_class = torch.argmax(predictions, dim=-1).item()
        confidence = predictions[0][predicted_class].item()
        
        # Get all class probabilities
        class_probabilities = predictions[0].tolist()
        
        result = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "class_probabilities": class_probabilities,
            "input_text": text,
            "task": task
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise e

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "model_loaded": model is not None,
        "service": "ContractBERT API"
    })

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """Prediction endpoint"""
    try:
        # Get input data
        data = request.get_json()
        
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400
        
        text = data["text"]
        task = data.get("task", "classification")
        
        # Run prediction
        result = predict(text, task)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check for Render"""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Load model on startup
    load_model()
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=port, debug=False)