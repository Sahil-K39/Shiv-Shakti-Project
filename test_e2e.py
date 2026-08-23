import requests
import json
import time
import string
import random

BASE_URL = "https://shivshaktiproject.com/api"

def random_string(n=8):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

print("=== STARTING E2E TESTS ===")

# 5. Test Fabric Quote API
print("\n5. Testing Fabric Quote Form...")
email = f"test_{random_string()}@example.com"
r = requests.post(f"{BASE_URL}/fabric-quote", json={
    "name": "Test User",
    "email": email,
    "phone": "+919876543210",
    "fabricType": "Silk",
    "quantityMeters": "100",
    "companyName": "Test Co",
    "message": "This is a test message to ensure the quote endpoint works properly."
})
print("Fabric Quote Status:", r.status_code)
print("Fabric Quote Response:", r.text)

print("\n=== E2E TESTS FINISHED ===")
