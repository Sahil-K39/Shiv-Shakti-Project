import json
import psycopg2

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"
BACKEND_JSON = "backend/internal/store/final_products.json"

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)
with open(BACKEND_JSON) as f:
    b_data = json.load(f)

def should_keep(slug):
    if slug.startswith("aug1_") or slug.startswith("aug8_"):
        return False
    return True

f_kept = [p for p in f_data['products'] if should_keep(p['slug'])]
b_kept = [p for p in b_data['products'] if should_keep(p['slug'])]

f_data['products'] = f_kept
b_data['products'] = b_kept

print(f"Frontend products: {len(f_kept)}")
print(f"Backend products: {len(b_kept)}")

with open(FRONTEND_JSON, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON, "w") as f:
    json.dump(b_data, f, indent=2)

DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("DELETE FROM products WHERE slug LIKE 'aug1_%' OR slug LIKE 'aug8_%'")
conn.commit()

cur.execute("SELECT count(*) FROM products")
print(f"Remaining Postgres products: {cur.fetchone()[0]}")

cur.close()
conn.close()

