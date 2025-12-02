"""Send a test email to verify Resend integration."""
import requests
import json
import time

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(3)

# Test data
test_data = {
    "name": "Maliha Test",
    "email": "test@example.com",
    "message": "🧪 This is a test email from your Portfolio backend!\n\nResend API integration is working correctly.\n\nSent from: noreply@malihamehnaz.cloud\nDelivered to: malihamehnazcse@gmail.com"
}

print("\n📧 Sending test email...")
print(f"From: Portfolio <noreply@malihamehnaz.cloud>")
print(f"To: malihamehnazcse@gmail.com")
print(f"Name: {test_data['name']}")
print(f"Reply-To: {test_data['email']}\n")

try:
    response = requests.post('http://localhost:8001/send', json=test_data)
    print(f"✅ Status: {response.status_code}")
    print(f"📬 Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 202:
        print("\n🎉 Email sent successfully!")
        print("📥 Check your inbox at malihamehnazcse@gmail.com")
    else:
        print("\n⚠️ Unexpected status code")
        
except Exception as e:
    print(f"❌ Error: {e}")
