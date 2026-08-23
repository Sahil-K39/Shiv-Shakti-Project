import json
import psycopg2
import os
import shutil

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"
BACKEND_JSON = "backend/internal/store/final_products.json"

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)
with open(BACKEND_JSON) as f:
    b_data = json.load(f)

f_data['products'] = [p for p in f_data['products'] if not (p['slug'].startswith("aug1_") or p['slug'].startswith("aug8_"))]
b_data['products'] = [p for p in b_data['products'] if not (p['slug'].startswith("aug1_") or p['slug'].startswith("aug8_"))]

with open(FRONTEND_JSON, 'w') as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON, 'w') as f:
    json.dump(b_data, f, indent=2)

DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("DELETE FROM products WHERE slug LIKE 'aug1_%' OR slug LIKE 'aug8_%'")
conn.commit()
cur.close()
conn.close()

# Also delete folders in final-products
import glob
for d in glob.glob("frontend/public/final-products/aug*"):
    if os.path.isdir(d):
        shutil.rmtree(d)

print("Deleted all old aug products.")
