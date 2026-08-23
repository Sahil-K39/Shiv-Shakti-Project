import requests
import json
import time
import string
import random

BASE_URL = "https://shivshaktiproject.com/api"

def random_string(n=8):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

print("=== STARTING E2E TESTS ===")

# 1. Test Products API
print("\n1. Testing Products API...")
r = requests.get(f"{BASE_URL}/products")
assert r.status_code == 200
data = r.json()
assert 'products' in data
print(f"Success! Found {len(data['products'])} products.")

# 2. Test Registration
print("\n2. Testing Registration...")
email = f"test_{random_string()}@example.com"
password = "TestPassword123!"

r = requests.post(f"{BASE_URL}/auth/register", json={
    "first_name": "Test",
    "last_name": "User",
    "email": email,
    "password": password
})
print("Register Status:", r.status_code)
print("Register Response:", r.text)
assert r.status_code in [200, 201]

# 3. Test Login
print("\n3. Testing Login...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "email": email,
    "password": password
})
print("Login Status:", r.status_code)
if r.status_code == 200:
    token = r.json().get('token')
    print("Success! Got token.")
    
    # 4. Test User Profile / Auth Check
    print("\n4. Testing Auth Profile...")
    r2 = requests.get(f"{BASE_URL}/auth/check", headers={"Authorization": f"Bearer {token}"})
    print("Auth Check Status:", r2.status_code)
else:
    print("Login Response:", r.text)

# 5. Test Contact API
print("\n5. Testing Contact Form...")
r = requests.post(f"{BASE_URL}/contact", json={
    "name": "Test User",
    "email": email,
    "subject": "Test Inquiry",
    "message": "This is a test message to ensure the contact endpoint works properly."
})
print("Contact Status:", r.status_code)
print("Contact Response:", r.text)

print("\n=== E2E TESTS FINISHED ===")
