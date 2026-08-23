import os
import glob
import json
import shutil
from PIL import Image
import psycopg2

BASE_DIR = "/Users/sahil/Documents/Shiv Shakti"
ALL_PRODUCTS_DIR = os.path.join(BASE_DIR, "All Products")
FINAL_PRODUCTS_DIR = os.path.join(BASE_DIR, "frontend/public/final-products")
FRONTEND_JSON_PATH = os.path.join(BASE_DIR, "frontend/src/lib/initialProducts.json")
BACKEND_JSON_PATH = os.path.join(BASE_DIR, "backend/internal/store/final_products.json")
DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

slugs_to_update = {}

for num in range(48, 94):
    slug = f"go_{num}"
    source_dir = os.path.join(ALL_PRODUCTS_DIR, f"Go{num}")
    dest_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        
    os.makedirs(dest_dir, exist_ok=True)
    
    src_files = sorted(glob.glob(os.path.join(source_dir, "*.*")))
    
    images = []
    for i, src in enumerate(src_files):
        dst_filename = f"{slug}-v7-{i+1:02d}.webp"
        dst = os.path.join(dest_dir, dst_filename)
        
        try:
            img = Image.open(src).convert("RGB")
            if img.width > 600:
                ratio = 600.0 / float(img.width)
                new_h = int(float(img.height) * float(ratio))
                img = img.resize((600, new_h), Image.Resampling.LANCZOS)
            
            img.save(dst, "WEBP", quality=85)
            images.append(f"/final-products/{slug}/{dst_filename}")
        except Exception as e:
            print(f"Error {src}: {e}")
            
    slugs_to_update[slug] = images

# Update JSON
for p in f_data['products']:
    if p['slug'] in slugs_to_update:
        p['images'] = slugs_to_update[p['slug']]
        
for p in b_data['products']:
    if p['slug'] in slugs_to_update:
        p['images'] = json.dumps(slugs_to_update[p['slug']])
        
with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

print("Updated JSON files.")

# Update Postgres
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
for slug, images in slugs_to_update.items():
    cur.execute("UPDATE products SET images = %s WHERE slug = %s", (json.dumps(images), slug))
conn.commit()
cur.close()
conn.close()
print("Updated Postgres database.")
