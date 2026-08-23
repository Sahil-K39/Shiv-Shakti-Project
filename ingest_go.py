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

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

existing_slugs = {p['slug'] for p in f_data['products']}

max_id = max([int(p['id']) for p in f_data['products']]) if f_data['products'] else 0

go_folders = glob.glob(os.path.join(ALL_PRODUCTS_DIR, "Go*"))
new_products = []

for folder in sorted(go_folders):
    folder_name = os.path.basename(folder)
    # folder_name is like Go48 or Go85_1
    slug = folder_name.lower()
    
    if slug.startswith("go") and slug[2].isdigit():
        slug = f"go_{slug[2:]}"
        
    if slug in existing_slugs:
        continue # Skip if already in frontend (like go_42 which came from Photoroom)
        
    print(f"Processing {slug} from {folder_name}...")
    
    slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)
    
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))]
    files.sort()
    
    images = []
    for i, f in enumerate(files):
        src = os.path.join(folder, f)
        dst_filename = f"{slug}-v3-{i+1:02d}.webp"
        dst = os.path.join(slug_dir, dst_filename)
        
        img = Image.open(src).convert("RGB")
        img.save(dst, "WEBP", quality=85)
        
        images.append(f"/final-products/{slug}/{dst_filename}")
        
    max_id += 1
    
    # name logic: Go85_1 -> GO-85-1
    name_suffix = folder_name[2:].replace('_', '-').upper()
    
    f_prod = {
        "id": str(max_id),
        "name": f"Shiv Shakti Style GO-{name_suffix}",
        "slug": slug,
        "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
        "price": 280,
        "sku": f"SS-FINAL-GO-{name_suffix}",
        "category": "shakti",
        "in_stock": True,
        "images": images
    }
    
    b_prod = {
        "name": f"Shiv Shakti Style GO-{name_suffix}",
        "slug": slug,
        "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
        "price": 280,
        "sale_price": 0,
        "category": "shakti",
        "collection": "SS26",
        "sizes": "[\"XS\",\"S\",\"M\",\"L\",\"XL\"]",
        "colors": "[\"Void Black\"]",
        "images": json.dumps(images),
        "quantity": 50,
        "sku": f"SS-FINAL-GO-{name_suffix}",
        "is_featured": False,
        "is_active": True,
        "sale_active": False
    }
    
    f_data['products'].append(f_prod)
    b_data['products'].append(b_prod)
    new_products.append(b_prod)

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

print(f"Added {len(new_products)} new products to JSON.")

if new_products:
    DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    for p in new_products:
        cur.execute("""
            INSERT INTO products (name, slug, description, price, sale_price, is_on_sale, currency, category, collection, sizes, colors, images, in_stock, featured, quantity, sku, is_featured, is_active, sale_active, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (sku) DO UPDATE SET images = EXCLUDED.images
        """, (p['name'], p['slug'], p['description'], p['price'], p['sale_price'], False, "INR", p['category'], p['collection'], p['sizes'], p['colors'], p['images'], True, False, p['quantity'], p['sku'], False, True, False))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Inserted into Postgres successfully.")

