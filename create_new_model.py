"""
Create a new model on Replicate
"""

import os
import replicate

def create_new_model():
    """Create a new model on Replicate"""
    try:
        client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))
        
        print("🚀 Creating new model on Replicate...")
        
        # Create a new model
        model = client.models.create(
            owner="tejasbhosale-git",
            name="contractbert-legal-nlp",
            description="ContractBERT model for legal text analysis and contract classification",
            visibility="public",
            hardware="gpu-t4"
        )
        
        print(f"✅ New model created: {model.owner}/{model.name}")
        print(f"🔗 URL: https://replicate.com/{model.owner}/{model.name}")
        
        return model
        
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        return None

def main():
    """Main function"""
    print("🚀 Create New ContractBERT Model")
    print("=" * 50)
    
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("❌ REPLICATE_API_TOKEN not set!")
        return
    
    model = create_new_model()
    
    if model:
        print("\n📝 Next steps:")
        print("1. Go to the new model page")
        print("2. Click 'Settings' tab")
        print("3. Connect GitHub repository: https://github.com/tejasbhosale-git/nlp_legal")
        print("4. Click 'Deploy'")

if __name__ == "__main__":
    main()
