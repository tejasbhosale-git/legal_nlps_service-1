"""
Simple deployment script using Replicate Python client
"""

import os
import replicate
import json

def test_api_connection():
    """Test if we can connect to Replicate API"""
    try:
        # Initialize client
        client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))
        
        # Test with a simple model to verify connection
        print("🔍 Testing API connection...")
        
        # List models to test connection
        models = client.models.list()
        print("✅ Successfully connected to Replicate API!")
        print(f"📊 Found {len(list(models))} models in your account")
        
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def create_model_deployment():
    """Create a new model deployment"""
    try:
        client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))
        
        print("🚀 Creating model deployment...")
        
        # Since you already have the model created on Replicate, 
        # we just need to push the code to it
        print("📝 Your model is already created at: tejasbhosale-git/legal-nlp-pipeline")
        print("🔧 You can now use the Replicate web interface to upload your code")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def show_usage_example():
    """Show how to use the deployed model"""
    print("\n📖 How to use your deployed model:")
    print("=" * 50)
    
    example_code = '''
import replicate

# Initialize client
client = replicate.Client(api_token="YOUR_API_TOKEN")

# Run your ContractBERT model
output = client.run(
    "tejasbhosale-git/legal-nlp-pipeline:latest",
    input={
        "text": "This contract agreement is between Company A and Company B for software services.",
        "task": "classification"
    }
)

print(output)
'''
    
    print(example_code)
    
    print("\n🌐 Or use the web interface:")
    print("1. Go to: https://replicate.com/tejasbhosale-git/legal-nlp-pipeline")
    print("2. Click on 'Playground' tab")
    print("3. Enter your contract text")
    print("4. Click 'Run' to test")

def main():
    """Main deployment function"""
    print("🚀 ContractBERT Replicate Deployment")
    print("=" * 50)
    
    # Check API token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("❌ REPLICATE_API_TOKEN not set!")
        print("Please set it with: $env:REPLICATE_API_TOKEN = 'your_token'")
        return
    
    # Test API connection
    if not test_api_connection():
        return
    
    # Show deployment info
    create_model_deployment()
    
    # Show usage example
    show_usage_example()
    
    print("\n✅ Setup complete!")
    print("📝 Next steps:")
    print("1. Upload your code to the Replicate model page")
    print("2. Test using the playground")
    print("3. Use the API in your applications")

if __name__ == "__main__":
    main()
