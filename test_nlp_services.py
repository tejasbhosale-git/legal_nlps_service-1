#!/usr/bin/env python3
"""
Test script for Unified Legal NLP Services
"""
import requests
import json

def test_nlp_services(base_url):
    """Test all NLP service endpoints"""
    print(f"🧪 Testing Unified Legal NLP Services at: {base_url}")
    print("=" * 60)
    
    # Test document for all services
    test_document = """
    This employment agreement is entered into between ABC Corporation, 
    a company incorporated in Mumbai, Maharashtra, and John Smith, 
    residing at Delhi, India. The employee shall receive a monthly 
    salary of ₹75,000 and shall report to Manager Sarah Johnson.
    The agreement shall terminate upon 30 days written notice by either party. 
    The employee agrees to indemnify the company against any damages.
    """
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test 2: Document Classification
    print("\n2️⃣ Testing Document Classification...")
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
        else:
            print(f"❌ Classification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Classification error: {str(e)}")
    
    # Test 3: Entity Recognition
    print("\n3️⃣ Testing Entity Recognition...")
    try:
        response = requests.post(
            f"{base_url}/extract",
            json={"text": test_document.strip()},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Entity recognition passed!")
            result = response.json()
            print(f"Total Entities: {result.get('total_entities', 0)}")
            print(f"Entity Types: {result.get('entity_types', [])}")
        else:
            print(f"❌ Entity recognition failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Entity recognition error: {str(e)}")
    
    # Test 4: Clause Analysis
    print("\n4️⃣ Testing Clause Analysis...")
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json={"text": test_document.strip()},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Clause analysis passed!")
            result = response.json()
            print(f"Total Clauses: {result.get('total_clauses', 0)}")
            print(f"Overall Risk: {result.get('overall_risk', 'Unknown')}")
        else:
            print(f"❌ Clause analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Clause analysis error: {str(e)}")
    
    # Test 5: Combined Analysis
    print("\n5️⃣ Testing Combined Analysis...")
    try:
        response = requests.post(
            f"{base_url}/analyze_all",
            json={"text": test_document.strip()},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Combined analysis passed!")
            result = response.json()
            print(f"Document Type: {result['document_classification'].get('document_type', 'Unknown')}")
            print(f"Total Entities: {result['entity_recognition'].get('total_entities', 0)}")
            print(f"Overall Risk: {result['clause_analysis'].get('overall_risk', 'Unknown')}")
        else:
            print(f"❌ Combined analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Combined analysis error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Unified NLP Services testing completed!")

if __name__ == "__main__":
    service_url = input("Enter your NLP Services URL (from Railway): ").strip()
    if not service_url:
        print("❌ Please provide a valid URL")
        exit(1)
    
    # Remove trailing slash if present
    service_url = service_url.rstrip('/')
    
    # Add https:// if not present
    if not service_url.startswith(('http://', 'https://')):
        service_url = f"https://{service_url}"
    
    test_nlp_services(service_url)
