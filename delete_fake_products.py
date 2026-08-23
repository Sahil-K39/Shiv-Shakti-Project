import requests

API_BASE = "https://shiv-shakti-project-backend.onrender.com"

# Fetch all products
resp = requests.get(f"{API_BASE}/api/products")
if resp.status_code == 200:
    products = resp.json().get("products", [])
    print(f"Fetched {len(products)} products from live API.")
    
    # Actually, we don't have a DELETE endpoint in the API unless we have admin access?
    # Wait, the database is synced from JSON. 
    pass
