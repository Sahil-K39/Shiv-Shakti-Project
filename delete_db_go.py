import os
import psycopg2

DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# We want to delete all products where slug starts with 'go_' and the number is >= 48,
# OR it ends with '_studio'

cur.execute("SELECT id, slug FROM products WHERE slug LIKE 'go_%'")
rows = cur.fetchall()

to_delete = []
for row in rows:
    pid, slug = row
    num_str = slug.replace("go_", "")
    
    if num_str.endswith("_studio"):
        to_delete.append(pid)
        continue
        
    num_part = num_str.split("_")[0]
    if num_part.isdigit() and int(num_part) >= 48:
        to_delete.append(pid)

print(f"Deleting {len(to_delete)} products from DB...")
if to_delete:
    cur.execute("DELETE FROM products WHERE id = ANY(%s)", (to_delete,))
    conn.commit()

cur.execute("SELECT count(*) FROM products")
print(f"Remaining products: {cur.fetchone()[0]}")

cur.close()
conn.close()
