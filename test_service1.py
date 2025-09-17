#!/usr/bin/env python3
"""
Test script for Service 1 - Document Classifier
"""
import requests
import json

def test_service1(base_url):
    """Test Service 1 endpoints"""
    print(f"🧪 Testing Service 1 at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test 2: Document Classification
    print("\n2️⃣ Testing Document Classification...")
    test_document = """
    This employment agreement is entered into between ABC Corporation, 
    a company incorporated under the Companies Act, 2013, and John Smith, 
    residing at Mumbai, Maharashtra. The employee shall receive a monthly 
    salary of ₹75,000 and shall be entitled to 21 days of annual leave.
    """
    
    try:
        response = requests.post(
            f"{base_url}/classify",
            json={"text": test_document.strip()},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Document classification passed!")
            result = response.json()
            print(f"Document Type: {result.get('document_type', 'Unknown')}")
            print(f"Confidence: {result.get('confidence', 0):.2%}")
            print(f"Method: {result.get('method', 'Unknown')}")
            print(f"Word Count: {result.get('word_count', 0)}")
        else:
            print(f"❌ Document classification failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Classification error: {str(e)}")
    
    # Test 3: Empty Text Handling
    print("\n3️⃣ Testing Empty Text Handling...")
    try:
        response = requests.post(
            f"{base_url}/classify",
            json={"text": ""},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 400:
            print("✅ Empty text handling passed!")
            print(f"Error message: {response.json().get('error', 'No error message')}")
        else:
            print(f"⚠️ Expected 400 error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Empty text test error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Service 1 testing completed!")

if __name__ == "__main__":
    # Replace this with your actual Service 1 URL
    service_url = input("Enter your Service 1 URL (from Railway dashboard): ").strip()
    if not service_url:
        print("❌ Please provide a valid URL")
        exit(1)
    
    # Remove trailing slash if present
    service_url = service_url.rstrip('/')
    
    test_service1(service_url)
