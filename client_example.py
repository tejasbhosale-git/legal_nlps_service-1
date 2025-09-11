"""
Example client code for using ContractBERT via Replicate API
"""

import os
import replicate
import json
from typing import Dict, Any, Optional

class ContractBERTClient:
    """Client for interacting with ContractBERT on Replicate"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the client
        
        Args:
            api_token: Replicate API token. If None, will try to get from environment
        """
        self.api_token = api_token or os.environ.get("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("API token is required. Set REPLICATE_API_TOKEN environment variable or pass api_token parameter")
        
        self.client = replicate.Client(api_token=self.api_token)
        self.model_name = None  # Will be set after deployment
    
    def set_model_name(self, model_name: str):
        """Set the deployed model name"""
        self.model_name = model_name
    
    def analyze_contract(self, text: str, task: str = "classification") -> Dict[str, Any]:
        """
        Analyze contract text using ContractBERT
        
        Args:
            text: Contract text to analyze
            task: Type of analysis task
            
        Returns:
            Analysis results
        """
        if not self.model_name:
            raise ValueError("Model name not set. Call set_model_name() first")
        
        try:
            output = self.client.run(
                self.model_name,
                input={
                    "text": text,
                    "task": task
                }
            )
            return output
        except Exception as e:
            return {"error": str(e)}
    
    def batch_analyze(self, texts: list, task: str = "classification") -> list:
        """
        Analyze multiple contract texts
        
        Args:
            texts: List of contract texts
            task: Type of analysis task
            
        Returns:
            List of analysis results
        """
        results = []
        for text in texts:
            result = self.analyze_contract(text, task)
            results.append(result)
        return results

def main():
    """Example usage of ContractBERTClient"""
    
    # Initialize client
    try:
        client = ContractBERTClient()
        print("✅ Client initialized successfully")
    except ValueError as e:
        print(f"❌ Error initializing client: {e}")
        print("Please set your REPLICATE_API_TOKEN environment variable")
        return
    
    # Set your deployed model name
    model_name = "tejasbhosale-git/legal-nlp-pipeline:latest"
    client.set_model_name(model_name)
    
    # Example contract texts
    sample_contracts = [
        "This agreement is entered into between Company A and Company B for the provision of software services.",
        "The contractor shall deliver the project within 90 days of contract execution.",
        "Any disputes arising from this contract shall be resolved through arbitration.",
        "The client agrees to pay the contractor $50,000 upon completion of the project."
    ]
    
    print("\n🔍 Analyzing sample contracts...")
    
    # Analyze each contract
    for i, contract_text in enumerate(sample_contracts, 1):
        print(f"\n--- Contract {i} ---")
        print(f"Text: {contract_text[:100]}...")
        
        result = client.analyze_contract(contract_text)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Predicted class: {result.get('predicted_class', 'N/A')}")
            print(f"✅ Confidence: {result.get('confidence', 'N/A'):.3f}")
            print(f"✅ Class probabilities: {result.get('class_probabilities', 'N/A')}")
    
    # Batch analysis example
    print("\n📊 Batch Analysis Results:")
    batch_results = client.batch_analyze(sample_contracts[:2])
    
    for i, result in enumerate(batch_results, 1):
        if "error" not in result:
            print(f"Contract {i}: Class {result.get('predicted_class')} (Confidence: {result.get('confidence', 0):.3f})")

def test_with_curl():
    """Example of how to test the API with curl"""
    print("\n🌐 Testing with curl:")
    print("""
    # Replace with your actual deployed model name
    curl -X POST \\
      -H "Authorization: Token YOUR_API_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{
        "input": {
          "text": "This contract is between Company A and Company B.",
          "task": "classification"
        }
      }' \\
      https://api.replicate.com/v1/models/tejasbhosale-git/legal-nlp-pipeline/predictions
    """)

if __name__ == "__main__":
    print("🚀 ContractBERT Replicate Client Example")
    print("=" * 50)
    
    # Run the main example
    main()
    
    # Show curl example
    test_with_curl()
    
    print("\n📝 Next Steps:")
    print("1. Deploy your model to Replicate")
    print("2. Update the model_name in this script")
    print("3. Set your REPLICATE_API_TOKEN environment variable")
    print("4. Run this script to test the API")
