import psycopg2
import json

DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT slug, images FROM products WHERE images LIKE '%-v2-%'")
rows = cur.fetchall()
for r in rows:
    print(f"Found -v2- in DB: {r[0]}")

# Also delete any products that are NOT in final_products.json!
with open("backend/internal/store/final_products.json") as f:
    b_data = json.load(f)

valid_slugs = [p['slug'] for p in b_data['products']]

cur.execute("SELECT slug FROM products")
db_slugs = [r[0] for r in cur.fetchall()]

for slug in db_slugs:
    if slug not in valid_slugs:
        print(f"Deleting ghost product from DB: {slug}")
        cur.execute("DELETE FROM products WHERE slug = %s", (slug,))

conn.commit()
cur.close()
conn.close()
