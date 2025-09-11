"""
Final test script - run this after deploying your model
"""

import os
import replicate
import json

def test_deployed_model():
    """Test the deployed ContractBERT model"""
    
    # Initialize client
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))
    
    # Test contract text
    test_text = "This agreement is entered into between Company A and Company B for the provision of software development services. The contractor shall deliver the project within 90 days of contract execution."
    
    print("🧪 Testing Deployed ContractBERT Model...")
    print(f"📝 Test text: {test_text[:100]}...")
    
    try:
        # Run the model
        output = client.run(
            "tejasbhosale-git/contractbert-legal-nlp:latest",
            input={
                "text": test_text,
                "task": "classification"
            }
        )
        
        print("✅ SUCCESS! Your ContractBERT API is working!")
        print("📊 Results:")
        print(json.dumps(output, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print("\n💡 Make sure you've deployed your model first!")
        print("1. Go to: https://replicate.com/tejasbhosale-git/contractbert-legal-nlp")
        print("2. Click 'Settings' tab")
        print("3. Upload your code files")
        print("4. Click 'Deploy'")
        return False

if __name__ == "__main__":
    test_deployed_model()
