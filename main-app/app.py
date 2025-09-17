"""
Main Legal AI Pipeline - Orchestration App
Coordinates all NLP services + Azure OpenAI GPT-4o
Deploy on Railway
"""

import os
import json
import requests
import logging
from flask import Flask, request, jsonify
import gradio as gr
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LegalAIPipeline:
    def __init__(self):
        """Initialize the Legal AI Pipeline"""
        # Service URLs (update these with your actual Railway URLs)
        self.doc_classifier_url = os.getenv("DOC_CLASSIFIER_URL", "http://localhost:5000")
        self.entity_recognizer_url = os.getenv("ENTITY_RECOGNIZER_URL", "http://localhost:5001")
        self.clause_analyzer_url = os.getenv("CLAUSE_ANALYZER_URL", "http://localhost:5002")
        
        # Azure OpenAI configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
        self.azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration"""
        if not self.azure_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        if not self.azure_api_key:
            raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")
        
        logger.info("✅ Legal AI Pipeline initialized successfully")
        logger.info(f"🔗 Doc Classifier: {self.doc_classifier_url}")
        logger.info(f"🔗 Entity Recognizer: {self.entity_recognizer_url}")
        logger.info(f"🔗 Clause Analyzer: {self.clause_analyzer_url}")
        logger.info(f"🔗 Azure OpenAI: {self.azure_endpoint}")
    
    def call_nlp_service(self, service_url: str, text: str, endpoint: str = "") -> Dict[str, Any]:
        """Call an NLP service"""
        try:
            url = f"{service_url}/{endpoint}" if endpoint else service_url
            response = requests.post(
                url,
                json={"text": text},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Service error: {response.status_code} - {response.text}")
                return {"error": f"Service error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Error calling service: {str(e)}")
            return {"error": f"Service call failed: {str(e)}"}
    
    def run_nlp_analysis(self, text: str) -> Dict[str, Any]:
        """Run complete NLP analysis using all services"""
        logger.info("🔍 Running complete NLP analysis...")
        
        # Call all NLP services in parallel
        doc_result = self.call_nlp_service(self.doc_classifier_url, text, "classify")
        entity_result = self.call_nlp_service(self.entity_recognizer_url, text, "extract")
        clause_result = self.call_nlp_service(self.clause_analyzer_url, text, "analyze")
        
        # Combine results
        nlp_results = {
            "document_classification": doc_result,
            "entity_recognition": entity_result,
            "clause_analysis": clause_result,
            "text_length": len(text),
            "word_count": len(text.split())
        }
        
        return nlp_results
    
    def call_azure_gpt4o(self, nlp_results: Dict[str, Any], original_text: str, analysis_type: str) -> str:
        """Call Azure OpenAI GPT-4o for legal analysis"""
        try:
            logger.info("🤖 Calling Azure OpenAI GPT-4o...")
            
            # Prepare context for GPT-4o
            context = self._prepare_legal_context(nlp_results, original_text, analysis_type)
            
            # Azure OpenAI API call
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_api_key
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert legal AI assistant specializing in Indian law. Provide comprehensive, accurate, and actionable legal analysis."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                "top_p": 0.9
            }
            
            # Make API call
            response = requests.post(
                f"{self.azure_endpoint}/chat/completions?api-version={self.azure_api_version}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                gpt_response = result["choices"][0]["message"]["content"]
                logger.info("✅ GPT-4o analysis completed successfully")
                return gpt_response
            else:
                logger.error(f"❌ Azure OpenAI error: {response.status_code} - {response.text}")
                return f"Error: Azure OpenAI API call failed with status {response.status_code}"
                
        except Exception as e:
            logger.error(f"❌ Error calling Azure OpenAI: {str(e)}")
            return f"Error: Azure OpenAI call failed: {str(e)}"
    
    def _prepare_legal_context(self, nlp_results: Dict[str, Any], original_text: str, analysis_type: str) -> str:
        """Prepare comprehensive legal context for GPT-4o"""
        
        # Extract NLP insights
        doc_class = nlp_results.get("document_classification", {})
        entities = nlp_results.get("entity_recognition", {})
        clauses = nlp_results.get("clause_analysis", {})
        
        context = f"""
LEGAL DOCUMENT ANALYSIS REQUEST

ORIGINAL TEXT:
{original_text}

NLP ANALYSIS RESULTS:

1. DOCUMENT CLASSIFICATION:
- Type: {doc_class.get('document_type', 'Unknown')}
- Confidence: {doc_class.get('confidence', 0):.1%}
- Text Length: {doc_class.get('text_length', 0)} characters

2. ENTITY RECOGNITION:
- Total Entities: {entities.get('total_entities', 0)}
- Entity Types: {', '.join(entities.get('entity_types', []))}
- Key Entities: {json.dumps(entities.get('entities', {}), indent=2)}

3. CLAUSE ANALYSIS:
- Total Clauses: {clauses.get('total_clauses', 0)}
- Risk Summary: {clauses.get('risk_summary', {})}
- Overall Risk: {clauses.get('overall_risk', 'Unknown')}

ANALYSIS TYPE REQUESTED: {analysis_type}

INSTRUCTIONS:
Based on the above NLP analysis and original text, provide a comprehensive legal analysis focusing on:

1. Document Classification & Type
2. Key Legal Entities & Parties
3. Risk Assessment & Compliance Issues
4. Indian Legal Framework Compliance
5. Recommendations & Next Steps

Please provide:
- Clear, actionable insights
- Specific references to Indian laws where applicable
- Risk mitigation strategies
- Compliance recommendations
- Professional legal language suitable for lawyers

Focus on Indian legal system requirements and best practices.
"""
        return context
    
    def analyze_legal_document(self, text: str, analysis_type: str) -> str:
        """Complete legal analysis pipeline: NLP + LLM"""
        if not text.strip():
            return "❌ Please enter some text to analyze."
        
        try:
            logger.info(f"🚀 Starting legal analysis pipeline for: {analysis_type}")
            
            # Step 1: NLP Analysis via all services
            nlp_results = self.run_nlp_analysis(text)
            
            # Check for errors in NLP results
            errors = []
            for service, result in nlp_results.items():
                if isinstance(result, dict) and "error" in result:
                    errors.append(f"{service}: {result['error']}")
            
            if errors:
                return f"❌ NLP Analysis Errors: {'; '.join(errors)}"
            
            # Step 2: LLM Analysis via Azure OpenAI
            llm_analysis = self.call_azure_gpt4o(nlp_results, text, analysis_type)
            
            if "Error:" in llm_analysis:
                return f"❌ LLM Analysis Error: {llm_analysis}"
            
            # Step 3: Format final response
            formatted_response = f"""
# ⚖️ Legal AI Analysis Report

## 📊 Analysis Summary
- **Type**: {analysis_type}
- **Document Type**: {nlp_results['document_classification'].get('document_type', 'Unknown')}
- **Confidence**: {nlp_results['document_classification'].get('confidence', 0):.1%}
- **Entities**: {nlp_results['entity_recognition'].get('total_entities', 0)} identified
- **Overall Risk**: {nlp_results['clause_analysis'].get('overall_risk', 'Unknown')}

## 🤖 AI Legal Analysis
{llm_analysis}

## 🔍 Technical Details
- **NLP Pipeline**: Multi-Service Architecture
- **LLM**: Azure OpenAI GPT-4o
- **Architecture**: Hybrid AI System
- **Focus**: Indian Legal Framework

---
*Generated by Legal AI Pipeline - Multi-Service NLP + LLM System*
"""
            
            logger.info("✅ Legal analysis pipeline completed successfully")
            return formatted_response
            
        except Exception as e:
            logger.error(f"❌ Error in legal analysis pipeline: {str(e)}")
            return f"❌ Analysis Failed: {str(e)}"

# Initialize the pipeline
try:
    legal_ai = LegalAIPipeline()
    logger.info("🎉 Legal AI Pipeline ready for deployment!")
except Exception as e:
    logger.error(f"❌ Failed to initialize Legal AI Pipeline: {str(e)}")
    legal_ai = None

# Flask API endpoints
@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "Legal AI Pipeline - Main Orchestration",
        "status": "running",
        "pipeline_loaded": legal_ai is not None
    })

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """Analyze legal document"""
    if not legal_ai:
        return jsonify({"error": "Pipeline not initialized"}), 500
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text field required"}), 400
        
        text = data['text']
        analysis_type = data.get('analysis_type', 'Full Legal Analysis')
        
        result = legal_ai.analyze_legal_document(text, analysis_type)
        return jsonify({"analysis": result})
        
    except Exception as e:
        logger.error(f"Error in analyze_document endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Gradio interface
def create_gradio_interface():
    """Create Gradio interface"""
    if not legal_ai:
        return gr.Interface(
            fn=lambda x, y: "❌ Legal AI Pipeline initialization failed.",
            inputs=[gr.Textbox(label="Document Text"), gr.Dropdown(choices=["Risk Assessment"])],
            outputs=gr.Textbox(label="Analysis Result"),
            title="Legal AI Pipeline - Initialization Error"
        )
    
    with gr.Blocks(title="Legal AI Pipeline", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # ⚖️ Legal AI Pipeline
        **Multi-Service Architecture: NLP Services + Azure OpenAI GPT-4o**
        
        Comprehensive legal document analysis powered by specialized NLP services and advanced language understanding.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="📄 Legal Document Text",
                    placeholder="Enter your legal document text here...",
                    lines=12,
                    max_lines=20
                )
                
                analysis_type = gr.Dropdown(
                    choices=[
                        "Risk Assessment",
                        "Compliance Check",
                        "Contract Review", 
                        "Legal Summary",
                        "Entity Analysis",
                        "Clause Analysis",
                        "Full Legal Analysis"
                    ],
                    value="Full Legal Analysis",
                    label="🎯 Analysis Type"
                )
                
                analyze_btn = gr.Button(
                    "🔍 Analyze with Legal AI",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=3):
                output = gr.Textbox(
                    label="📋 Legal Analysis Report",
                    lines=25,
                    max_lines=30,
                    show_copy_button=True
                )
        
        # Example documents
        gr.Markdown("## 📝 Example Legal Documents")
        examples = [
            [
                "This employment agreement is entered into between ABC Corporation, a company incorporated under the Companies Act, 2013, and John Smith, residing at Mumbai, Maharashtra. The employee shall receive a monthly salary of ₹75,000 and shall be entitled to 21 days of annual leave as per the Industrial Disputes Act, 1947. Any disputes arising from this agreement shall be subject to the jurisdiction of courts in Mumbai.",
                "Contract Review"
            ],
            [
                "The parties agree that all personal data collected under this service agreement shall be processed in accordance with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011, and applicable data protection laws.",
                "Compliance Check"
            ]
        ]
        
        gr.Examples(
            examples=examples,
            inputs=[text_input, analysis_type],
            outputs=output,
            fn=legal_ai.analyze_legal_document
        )
        
        # Event handlers
        analyze_btn.click(
            fn=legal_ai.analyze_legal_document,
            inputs=[text_input, analysis_type],
            outputs=output
        )
        
        # Footer
        gr.Markdown("""
        ---
        **Legal AI Pipeline** | Multi-Service NLP + LLM Architecture | Powered by Railway & Azure OpenAI
        """)
    
    return demo

if __name__ == "__main__":
    # Create Gradio interface
    demo = create_gradio_interface()
    
    # Launch with Flask integration
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860)),
        share=False
    )
