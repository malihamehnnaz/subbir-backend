"""Test script for the portfolio backend API."""
import requests
import json

BASE_URL = "http://localhost:8001"

print("Testing Portfolio Email API...\n")

# Test 1: Root endpoint
print("1. Testing root endpoint (GET /)...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✓ Root endpoint working\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")

# Test 2: Health endpoint
print("2. Testing health endpoint (GET /health)...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    print("   ✓ Health endpoint working\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")

# Test 3: Contact form endpoint
print("3. Testing contact form endpoint (POST /send)...")
test_data = {
    "name": "Test User",
    "email": "test@example.com",
    "message": "This is a test message from the API test script."
}
try:
    response = requests.post(f"{BASE_URL}/send", json=test_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 202:
        print("   ✓ Contact form endpoint working\n")
    else:
        print("   ⚠ Unexpected status code\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")

# Test 4: Invalid email validation
print("4. Testing email validation (invalid email)...")
invalid_data = {
    "name": "Test User",
    "email": "invalid-email",
    "message": "This should fail validation."
}
try:
    response = requests.post(f"{BASE_URL}/send", json=invalid_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 422:
        print("   ✓ Email validation working\n")
    else:
        print("   ⚠ Expected 422 status code\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")

print("All tests completed!")
