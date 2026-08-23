import os
import glob
import json
import re
from PIL import Image
import psycopg2

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"
BACKEND_JSON = "backend/internal/store/final_products.json"
FINAL_PRODUCTS = "frontend/public/final-products"
DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"

def extract_seq(f):
    m = re.search(r'153A(\d+)', f)
    if m:
        try:
            return int(os.path.basename(f).split('-')[0])
        except:
            pass
    return 0

aug1_groups = [
    (1,5), (6,7), (8,12), (13,17), (18,25), (26,30), (31,39), (40,44), (45,46), (47,48), (49,52), (53,58)
]
aug8_groups = [
    (1,4), (5,9), (10,15), (16,22), (23,27), (28,43), (44,48), (49,55), (56,60), (61,62), (63,71), (73,74), (75,78), (79,84), (85,95), (96,99), (100,101), (102,107), (108,110), (111,115), (116,125)
]

aug1_dir = "All Products/Aug 1, 2026 08_03_55 PM (1)"
aug8_dir = "All Products/Aug 8, 2026 03_16_45 PM"

all_aug1_files = sorted(glob.glob(os.path.join(aug1_dir, "*.*")), key=extract_seq)
all_aug8_files = sorted(glob.glob(os.path.join(aug8_dir, "*.*")), key=extract_seq)

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)

# Find max ID
max_id = max([int(p["id"]) for p in f_data['products']], default=0)

new_products = []

def process_batch(prefix, group_idx, start, end, files):
    global max_id
    matched_files = [f for f in files if start <= extract_seq(f) <= end]
    if not matched_files:
        return
    
    slug = f"{prefix}_group_{group_idx:02d}"
    print(f"Processing {slug} with {len(matched_files)} files...")
    
    out_dir = os.path.join(FINAL_PRODUCTS, slug)
    os.makedirs(out_dir, exist_ok=True)
    
    image_paths = []
    
    for i, file_path in enumerate(matched_files):
        new_filename = f"{slug}-v6-{i+1:02d}.webp"
        new_path = os.path.join(out_dir, new_filename)
        
        try:
            img = Image.open(file_path).convert("RGB")
            # Resize directly to max width 600px
            if img.width > 600:
                ratio = 600.0 / float(img.width)
                new_h = int(float(img.height) * float(ratio))
                img = img.resize((600, new_h), Image.Resampling.LANCZOS)
            
            img.save(new_path, "WEBP", quality=85)
            image_paths.append(f"/final-products/{slug}/{new_filename}")
        except Exception as e:
            print(f"Error {file_path}: {e}")
            
    if not image_paths:
        return
        
    max_id += 1
    
    new_products.append({
      "id": max_id,
      "name": f"Studio Collection {prefix.upper()} {group_idx}",
      "slug": slug,
      "price": 19200,
      "sale_price": None,
      "description": "Exclusive avant-garde studio collection piece. Handcrafted detail.",
      "category": "Studio",
      "colors": "[]",
      "sizes": "[\"OS\"]",
      "in_stock": True,
      "images": image_paths,
      "is_active": True
    })

for i, (start, end) in enumerate(aug1_groups, 1):
    process_batch("aug1", i, start, end, all_aug1_files)
    
for i, (start, end) in enumerate(aug8_groups, 1):
    process_batch("aug8", i, start, end, all_aug8_files)

# Append to JSON
f_data['products'].extend(new_products)

with open(FRONTEND_JSON, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON, "w") as f:
    json.dump(f_data, f, indent=2)
    
print(f"Added {len(new_products)} new products to JSON.")

# Insert to DB
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
for p in new_products:
    cur.execute("""
        INSERT INTO products (id, name, slug, price, sale_price, description, category, colors, sizes, in_stock, images, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (slug) DO UPDATE SET images = EXCLUDED.images
    """, (
        p['id'], p['name'], p['slug'], p['price'], p['sale_price'], p['description'],
        p['category'], p['colors'], p['sizes'], p['in_stock'], json.dumps(p['images']), p['is_active']
    ))
conn.commit()
cur.close()
conn.close()
print("Inserted into Postgres successfully.")
