import os
import glob
import json
import shutil
from PIL import Image
import psycopg2
import re

BASE_DIR = "/Users/sahil/Documents/Shiv Shakti"
ALL_PRODUCTS_DIR = os.path.join(BASE_DIR, "All Products")
FINAL_PRODUCTS_DIR = os.path.join(BASE_DIR, "frontend/public/final-products")
FRONTEND_JSON_PATH = os.path.join(BASE_DIR, "frontend/src/lib/initialProducts.json")
BACKEND_JSON_PATH = os.path.join(BASE_DIR, "backend/internal/store/final_products.json")

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

max_id = max([int(p['id']) for p in f_data['products']]) if f_data['products'] else 0

aug1_groups = [
    (1,5), (6,7), (8,12), (13,17), (18,25), (26,30), (31,39), (40,44), (45,46), (47,48), (49,52), (53,58)
]
aug8_groups = [
    (1,4), (5,9), (10,15), (16,22), (23,27), (28,43), (44,48), (49,55), (56,60), (61,62), (63,71), (73,74), (75,78), (79,84), (85,95), (96,99), (100,101), (102,107), (108,110), (111,115), (116,125)
]

def extract_seq(f):
    m = re.search(r'153A(\d+)', f)
    if m:
        try:
            return int(os.path.basename(f).split('-')[0])
        except:
            pass
    return 0

def process_folder(folder_name, slug_prefix, name_prefix, groups):
    global max_id
    folder_path = os.path.join(ALL_PRODUCTS_DIR, folder_name)
    files = glob.glob(os.path.join(folder_path, "*.*"))
    files.sort(key=extract_seq)
    
    new_products = []
    
    for i, (start, end) in enumerate(groups):
        group_num = i + 1
        slug = f"{slug_prefix}_group_{group_num:02d}"
        
        # Get files in range
        group_files = [f for f in files if start <= extract_seq(f) <= end]
        if not group_files:
            print(f"Warning: No files found for {slug} (range {start}-{end})")
            continue
            
        print(f"Processing {slug} with {len(group_files)} files...")
        
        slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        
        images = []
        for j, src in enumerate(group_files):
            dst_filename = f"{slug}-v6-{j+1:02d}.webp"
            dst = os.path.join(slug_dir, dst_filename)
            
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
            
        max_id += 1
        name = f"Shiv Shakti Style {name_prefix}-GROUP-{group_num:02d}"
        sku = f"SS-FINAL-{name_prefix}-GROUP-{group_num:02d}"
        
        f_prod = {
            "id": str(max_id),
            "name": name,
            "slug": slug,
            "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
            "price": 280,
            "sku": sku,
            "category": "shakti",
            "in_stock": True,
            "images": images
        }
        
        b_prod = {
            "name": name,
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
            "sku": sku,
            "is_featured": False,
            "is_active": True,
            "sale_active": False
        }
        
        f_data['products'].append(f_prod)
        b_data['products'].append(b_prod)
        new_products.append(b_prod)
        
    return new_products

n1 = process_folder("Aug 1, 2026 08_03_55 PM (1)", "aug1", "AUG1", aug1_groups)
n2 = process_folder("Aug 8, 2026 03_16_45 PM", "aug8", "AUG8", aug8_groups)
all_new = n1 + n2

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

print(f"Added {len(all_new)} new products to JSON.")

if all_new:
    DATABASE_URL = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    for p in all_new:
        cur.execute("""
            INSERT INTO products (name, slug, description, price, sale_price, is_on_sale, currency, category, collection, sizes, colors, images, in_stock, featured, quantity, sku, is_featured, is_active, sale_active, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (sku) DO UPDATE SET images = EXCLUDED.images
        """, (p['name'], p['slug'], p['description'], p['price'], p['sale_price'], False, "INR", p['category'], p['collection'], p['sizes'], p['colors'], p['images'], True, False, p['quantity'], p['sku'], False, True, False))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Inserted into Postgres successfully.")
