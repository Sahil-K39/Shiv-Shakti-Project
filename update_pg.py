import json
import psycopg2

BACKEND_JSON = "backend/internal/store/final_products.json"

with open(BACKEND_JSON) as f:
    b_data = json.load(f)

DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

for p in b_data['products']:
    cur.execute("UPDATE products SET images = %s WHERE slug = %s", (p['images'], p['slug']))

conn.commit()
cur.close()
conn.close()
print("Postgres updated!")
