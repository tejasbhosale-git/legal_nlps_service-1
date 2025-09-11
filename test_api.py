"""
Test script for ContractBERT API
"""

import os
import replicate
import json

def test_contractbert_api():
    """Test the ContractBERT API"""
    
    # Initialize client
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))
    
    # Test contract text
    test_text = "This agreement is entered into between Company A and Company B for the provision of software development services. The contractor shall deliver the project within 90 days of contract execution."
    
    print("🧪 Testing ContractBERT API...")
    print(f"📝 Test text: {test_text[:100]}...")
    
    try:
        # Run the model
        output = client.run(
            "dinchakfurk-spec/legal-nlp-pipeline:latest",
            input={
                "text": test_text,
                "task": "classification"
            }
        )
        
        print("✅ API call successful!")
        print("📊 Results:")
        print(json.dumps(output, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False

if __name__ == "__main__":
    test_contractbert_api()
