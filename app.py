"""
Legal NLP Pipeline - Hugging Face Spaces
Multi-model legal document analysis
"""

import gradio as gr
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    pipeline
)
import requests
import json
from typing import Dict, List, Any

class LegalNLPPipeline:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load all legal NLP models"""
        print("Loading legal NLP models...")
        
        # Model 1: Document Type Classification
        self.models['doc_classifier'] = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Model 2: ContractBERT for clause classification
        try:
            self.models['contract_bert'] = pipeline(
                "text-classification",
                model="nlpaueb/legal-bert-base-uncased",
                device=0 if torch.cuda.is_available() else -1
            )
        except:
            print("ContractBERT not available, using DistilBERT")
            self.models['contract_bert'] = self.models['doc_classifier']
        
        # Model 3: NER for Indian entities
        try:
            self.models['indic_ner'] = pipeline(
                "ner",
                model="ai4bharat/IndicNER",
                device=0 if torch.cuda.is_available() else -1
            )
        except:
            print("IndicNER not available, using basic NER")
            self.models['indic_ner'] = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=0 if torch.cuda.is_available() else -1
            )
        
        print("All models loaded successfully!")
    
    def analyze_document(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """Analyze legal document"""
        results = {
            "input_text": text,
            "analysis_type": analysis_type,
            "results": {}
        }
        
        if analysis_type == "Document Classification":
            # Classify document type
            doc_result = self.models['doc_classifier'](text)
            results["results"]["document_type"] = doc_result[0]
            
        elif analysis_type == "Clause Analysis":
            # Analyze clauses and risks
            clause_result = self.models['contract_bert'](text)
            results["results"]["clause_analysis"] = clause_result[0]
            
        elif analysis_type == "Entity Recognition":
            # Extract Indian entities
            ner_result = self.models['indic_ner'](text)
            results["results"]["entities"] = ner_result
            
        elif analysis_type == "Full Analysis":
            # Run all analyses
            doc_result = self.models['doc_classifier'](text)
            clause_result = self.models['contract_bert'](text)
            ner_result = self.models['indic_ner'](text)
            
            results["results"] = {
                "document_type": doc_result[0],
                "clause_analysis": clause_result[0],
                "entities": ner_result
            }
        
        return results

# Initialize pipeline
pipeline_instance = LegalNLPPipeline()

def analyze_legal_document(text: str, analysis_type: str) -> str:
    """Gradio interface function"""
    if not text.strip():
        return "Please enter some text to analyze."
    
    try:
        results = pipeline_instance.analyze_document(text, analysis_type)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Legal NLP Pipeline") as demo:
    gr.Markdown("# 🏛️ Legal NLP Pipeline")
    gr.Markdown("Analyze legal documents with multiple specialized models")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Legal Document Text",
                placeholder="Enter your legal document text here...",
                lines=10
            )
            
            analysis_type = gr.Dropdown(
                choices=[
                    "Document Classification",
                    "Clause Analysis", 
                    "Entity Recognition",
                    "Full Analysis"
                ],
                value="Full Analysis",
                label="Analysis Type"
            )
            
            analyze_btn = gr.Button("🔍 Analyze Document", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(
                label="Analysis Results",
                lines=20,
                max_lines=25
            )
    
    # Example texts
    gr.Markdown("## 📝 Example Texts")
    examples = [
        [
            "This agreement is entered into between Company A and Company B for the provision of software development services. The contractor shall deliver the project within 90 days of contract execution.",
            "Full Analysis"
        ],
        [
            "The parties agree that any disputes arising from this contract shall be resolved through arbitration in Mumbai, India.",
            "Clause Analysis"
        ],
        [
            "Mr. Rajesh Kumar, residing at 123 MG Road, Bangalore, Karnataka, India, hereby agrees to the terms and conditions.",
            "Entity Recognition"
        ]
    ]
    
    gr.Examples(
        examples=examples,
        inputs=[text_input, analysis_type],
        outputs=output,
        fn=analyze_legal_document
    )
    
    # Event handlers
    analyze_btn.click(
        fn=analyze_legal_document,
        inputs=[text_input, analysis_type],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
