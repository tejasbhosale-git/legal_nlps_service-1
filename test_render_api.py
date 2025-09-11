"""
Test script for ContractBERT API on Render
"""

import requests
import json

def test_render_api(api_url):
    """Test the ContractBERT API on Render"""
    
    # Test contract text
    test_text = "This agreement is entered into between Company A and Company B for the provision of software development services. The contractor shall deliver the project within 90 days of contract execution."
    
    print("🧪 Testing ContractBERT API on Render...")
    print(f"🌐 API URL: {api_url}")
    print(f"📝 Test text: {test_text[:100]}...")
    
    try:
        # Test health endpoint
        print("\n🔍 Testing health endpoint...")
        health_response = requests.get(f"{api_url}/health")
        if health_response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
        
        # Test prediction endpoint
        print("\n🔍 Testing prediction endpoint...")
        prediction_data = {
            "text": test_text,
            "task": "classification"
        }
        
        response = requests.post(
            f"{api_url}/predict",
            json=prediction_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Your ContractBERT API is working!")
            print("📊 Results:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 ContractBERT Render API Test")
    print("=" * 50)
    
    # You'll need to replace this with your actual Render URL
    api_url = "https://your-app-name.onrender.com"  # Replace with your actual URL
    
    print("⚠️  IMPORTANT: Replace 'your-app-name' with your actual Render app name")
    print("📝 Your Render URL will be: https://YOUR-APP-NAME.onrender.com")
    
    # Uncomment the line below and replace with your actual URL
    # test_render_api(api_url)
    
    print("\n📋 After deploying to Render:")
    print("1. Get your Render app URL")
    print("2. Update the api_url in this script")
    print("3. Run: python test_render_api.py")

if __name__ == "__main__":
    main()
