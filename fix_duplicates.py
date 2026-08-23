import os
import json
import shutil
from PIL import Image

FINAL_PRODUCTS_DIR = "/Users/sahil/Documents/Shiv Shakti/frontend/public/final-products"
FRONTEND_JSON_PATH = "/Users/sahil/Documents/Shiv Shakti/frontend/src/lib/initialProducts.json"
BACKEND_JSON_PATH = "/Users/sahil/Documents/Shiv Shakti/backend/internal/store/final_products.json"
PHOTOROOM_DIR = "/Users/sahil/Documents/Shiv Shakti/All Products/Photoroom"
ALL_PRODUCTS_DIR = "/Users/sahil/Documents/Shiv Shakti/All Products"

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

dups = ["42", "44", "45", "46", "47"]

def convert_image(src, dst):
    img = Image.open(src)
    img = img.convert("RGB")
    img.save(dst, "WEBP", quality=85)

max_id = max(int(p['id']) for p in f_data['products'])

for dup in dups:
    slug = f"go_{dup}"
    sku = f"SS-FINAL-GO-{dup}"
    
    # 1. Fix the original product (Photoroom version) which was overwritten
    photoroom_files = [f for f in os.listdir(PHOTOROOM_DIR) if f.lower().startswith(f"go{dup}_")]
    photoroom_files.sort()
    
    slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)
    
    pr_images = []
    for i, file in enumerate(photoroom_files):
        src = os.path.join(PHOTOROOM_DIR, file)
        dst_filename = f"{slug}-{i+1:02d}.webp"
        dst = os.path.join(slug_dir, dst_filename)
        convert_image(src, dst)
        pr_images.append(f"/final-products/{slug}/{dst_filename}")
    
    # Find and fix in frontend json
    for p in f_data['products']:
        if p['sku'] == sku:
            p['images'] = pr_images
            break
            
    # Find and fix in backend json
    for p in b_data['products']:
        if p['sku'] == sku:
            p['images'] = json.dumps(pr_images)
            break
            
    # 2. Add the STUDIO product
    studio_folder = os.path.join(ALL_PRODUCTS_DIR, f"GO_{dup}")
    studio_files = [f for f in os.listdir(studio_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    studio_files.sort()
    
    studio_slug = f"go_{dup}_studio"
    studio_sku = f"SS-FINAL-GO-{dup}-STUDIO"
    studio_name = f"Shiv Shakti Style GO-{dup} Studio"
    
    studio_dir = os.path.join(FINAL_PRODUCTS_DIR, studio_slug)
    os.makedirs(studio_dir, exist_ok=True)
    
    st_images = []
    for i, file in enumerate(studio_files):
        src = os.path.join(studio_folder, file)
        dst_filename = f"{studio_slug}-{i+1:02d}.webp"
        dst = os.path.join(studio_dir, dst_filename)
        convert_image(src, dst)
        st_images.append(f"/final-products/{studio_slug}/{dst_filename}")
        
    max_id += 1
    
    # Check if already exists just in case
    exists = any(p['sku'] == studio_sku for p in f_data['products'])
    if not exists:
        f_data['products'].append({
            "id": max_id,
            "name": studio_name,
            "slug": studio_slug,
            "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
            "price": 280,
            "sku": studio_sku,
            "category": "shakti",
            "in_stock": True,
            "images": st_images
        })
        b_data['products'].append({
            "name": studio_name,
            "slug": studio_slug,
            "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
            "price": 280,
            "sale_price": 0,
            "category": "shakti",
            "collection": "SS26",
            "sizes": "[\"XS\",\"S\",\"M\",\"L\",\"XL\"]",
            "colors": "[\"Void Black\"]",
            "images": json.dumps(st_images),
            "quantity": 50,
            "sku": studio_sku,
            "is_featured": False,
            "is_active": True,
            "sale_active": False
        })
    else:
        for p in f_data['products']:
            if p['sku'] == studio_sku:
                p['images'] = st_images
        for p in b_data['products']:
            if p['sku'] == studio_sku:
                p['images'] = json.dumps(st_images)

# Remove the empty duplicate entries that might still be in the lists
# Wait, process.py appended to the list, so there are literally TWO dictionaries with the same SKU in the JSON arrays!
# We must remove duplicates.
unique_f = []
seen_sku = set()
for p in reversed(f_data['products']):
    if p['sku'] not in seen_sku:
        seen_sku.add(p['sku'])
        unique_f.append(p)
unique_f.reverse()
f_data['products'] = unique_f

unique_b = []
seen_sku_b = set()
for p in reversed(b_data['products']):
    if p['sku'] not in seen_sku_b:
        seen_sku_b.add(p['sku'])
        unique_b.append(p)
unique_b.reverse()
b_data['products'] = unique_b

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)

with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

print(f"Fixed {len(dups)} duplicates. Total unique products: {len(f_data['products'])}")
