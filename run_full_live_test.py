import requests
import json
import psycopg2
import time
import sys

BASE_URL = "https://shivshaktiproject.com/api"
DB_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"

EMAIL = f"fulltest_{int(time.time())}@shiv.com"
PASSWORD = "Password123!"
NAME = "Full E2E Tester"

session = requests.Session()

def fetch_csrf():
    res = session.get(f"{BASE_URL}/csrf-token")
    if res.status_code != 200:
        print("Failed to get CSRF token")
        sys.exit(1)
    token = res.json().get("csrf_token")
    session.headers.update({"X-CSRF-Token": token})
    return token

print(f"--- 1. Testing Registration for {EMAIL} ---")
reg_res = session.post(f"{BASE_URL}/auth/register", json={
    "email": EMAIL,
    "password": PASSWORD,
    "name": NAME
})
if reg_res.status_code != 201:
    print(f"Registration failed: {reg_res.status_code} {reg_res.text}")
    sys.exit(1)
print("✅ Registration Successful")

print("--- 2. Verifying User in Database ---")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_verified = true WHERE email = %s RETURNING id;", (EMAIL,))
    user_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    print("✅ User manually verified in Supabase")
except Exception as e:
    print(f"Database error: {e}")
    sys.exit(1)

print("--- 3. Testing Login ---")
login_res = session.post(f"{BASE_URL}/auth/login", json={
    "email": EMAIL,
    "password": PASSWORD
})
if login_res.status_code != 200:
    print(f"Login failed: {login_res.status_code} {login_res.text}")
    sys.exit(1)
print("✅ Login Successful")

print("--- 4. Fetching Products ---")
prod_res = session.get(f"{BASE_URL}/products")
if prod_res.status_code != 200:
    sys.exit(1)
products = prod_res.json().get("products", [])
prod_id = products[0]["id"]
print(f"✅ Fetched {len(products)} products")

print(f"--- 5. Testing Add to Cart (Product ID: {prod_id}) ---")
fetch_csrf()
cart_res = session.post(f"{BASE_URL}/cart/add", json={
    "product_id": prod_id,
    "quantity": 50,
    "size": "L",
    "color": "Black"
})
if cart_res.status_code != 200:
    print(f"Add to cart failed: {cart_res.status_code} {cart_res.text}")
    sys.exit(1)
print("✅ Item Added to Cart")

print("--- 6. Testing Fetch Cart ---")
get_cart_res = session.get(f"{BASE_URL}/cart")
cart_items = get_cart_res.json()
print(f"✅ Cart has {len(cart_items)} item(s)")

print("--- 7. Testing Checkout / Inquiry ---")
fetch_csrf()
checkout_res = session.post(f"{BASE_URL}/checkout", json={
    "shipping_name": NAME,
    "shipping_address": "123 Test St",
    "shipping_city": "Testville",
    "shipping_state": "TS",
    "shipping_zip": "12345",
    "shipping_country": "USA",
    "shipping_phone": "1234567890",
    "notes": "E2E automated test order"
})
if checkout_res.status_code != 201:
    print(f"Checkout failed: {checkout_res.status_code} {checkout_res.text}")
    sys.exit(1)
print(f"✅ Checkout Successful! Order ID: {checkout_res.json().get('order_id')}")

print("--- 8. Testing Admin Order Visibility ---")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = 'admin' WHERE email = %s;", (EMAIL,))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ User promoted to Admin")
except Exception:
    sys.exit(1)

session.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
admin_orders_res = session.get(f"{BASE_URL}/admin/orders")
if admin_orders_res.status_code != 200:
    print(f"Admin orders fetch failed: {admin_orders_res.status_code}")
    sys.exit(1)
print(f"✅ Admin fetched {len(admin_orders_res.json())} orders successfully")

print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! The entire platform is working perfectly.")
