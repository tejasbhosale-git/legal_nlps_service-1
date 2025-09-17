#!/bin/bash
# Test script for Service 1 - Document Classifier

echo "🧪 Testing Service 1 - Document Classifier"
echo "=========================================="

# Get the service URL
if [ -z "$1" ]; then
    echo "Usage: $0 <SERVICE_1_URL>"
    echo "Example: $0 https://your-service1-production-xxxx.up.railway.app"
    exit 1
fi

SERVICE_URL=$1

echo ""
echo "1️⃣ Testing Health Check..."
curl -s "$SERVICE_URL/" | jq . || echo "Health check response (raw):" && curl -s "$SERVICE_URL/"

echo ""
echo ""
echo "2️⃣ Testing Document Classification..."
curl -s -X POST "$SERVICE_URL/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This employment agreement is entered into between ABC Corporation and John Smith. The employee shall receive a monthly salary of ₹75,000 and shall be entitled to 21 days of annual leave as per the Industrial Disputes Act, 1947."
  }' | jq . || echo "Classification response (raw):" && curl -s -X POST "$SERVICE_URL/classify" -H "Content-Type: application/json" -d '{"text": "This employment agreement is entered into between ABC Corporation and John Smith."}'

echo ""
echo ""
echo "3️⃣ Testing Error Handling (Empty Text)..."
curl -s -X POST "$SERVICE_URL/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": ""}' | jq . || echo "Error handling response (raw):" && curl -s -X POST "$SERVICE_URL/classify" -H "Content-Type: application/json" -d '{"text": ""}'

echo ""
echo ""
echo "🎯 Service 1 testing completed!"
