import os
import glob
import json
import shutil
from PIL import Image
import shutil

BASE_DIR = "/Users/sahil/Documents/Shiv Shakti"
ALL_PRODUCTS_DIR = os.path.join(BASE_DIR, "All Products")
FINAL_PRODUCTS_DIR = os.path.join(BASE_DIR, "frontend/public/final-products")

FRONTEND_JSON_PATH = os.path.join(BASE_DIR, "frontend/src/lib/initialProducts.json")
BACKEND_JSON_PATH = os.path.join(BASE_DIR, "backend/internal/store/final_products.json")

os.makedirs(FINAL_PRODUCTS_DIR, exist_ok=True)

frontend_products = []
backend_products = []
product_id_counter = 1

def add_product(slug, name_suffix, sku_suffix, images):
    global product_id_counter
    name = f"Shiv Shakti Style {name_suffix}"
    sku = f"SS-FINAL-{sku_suffix}"
    
    frontend_products.append({
        "id": str(product_id_counter),
        "name": name,
        "slug": slug,
        "description": "Exclusive handcrafted design from The Shiv Shakti collection.",
        "price": 280,
        "sku": sku,
        "category": "shakti",
        "in_stock": True,
        "images": images
    })
    
    backend_products.append({
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
    })
    product_id_counter += 1

def convert_image(src, dst):
    img = Image.open(src)
    img = img.convert("RGB")
    img.save(dst, "WEBP", quality=85)

def convert_image(src, dst):
    # print(f"Copying {src} to {dst}")
    shutil.copy2(src, dst)

# 1. Photoroom
photoroom_dir = os.path.join(ALL_PRODUCTS_DIR, "Photoroom")
if os.path.exists(photoroom_dir):
    files = [f for f in os.listdir(photoroom_dir) if f.lower().endswith('.png') or f.lower().endswith('.jpg')]
    groups = {}
    for f in files:
        prefix = f[:4] # e.g. Go02
        groups.setdefault(prefix, []).append(f)
    
    for prefix, group_files in sorted(groups.items()):
        group_files.sort()
        slug = prefix.lower()
        slug = f"{slug[:2]}_{slug[2:]}" # go02 -> go_02
        
        name_suffix = prefix.upper()
        sku_suffix = prefix.upper()
        
        slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        
        images = []
        for i, f in enumerate(group_files):
            src = os.path.join(photoroom_dir, f)
            dst_filename = f"{slug}-{i+1:02d}.webp"
            dst = os.path.join(slug_dir, dst_filename)
            convert_image(src, dst)
            images.append(f"/final-products/{slug}/{dst_filename}")
        
        add_product(slug, f"{slug[:2].upper()}-{slug[3:]}", f"{slug[:2].upper()}-{slug[3:]}", images)

# 2. GO_ folders
go_folders = glob.glob(os.path.join(ALL_PRODUCTS_DIR, "GO_*"))
for folder in sorted(go_folders):
    folder_name = os.path.basename(folder)
    slug = folder_name.lower()
    
    slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)
    
    files = [f for f in os.listdir(folder) if f.lower().endswith('.webp')]
    files.sort()
    
    images = []
    for i, f in enumerate(files):
        src = os.path.join(folder, f)
        dst_filename = f"{slug}-{i+1:02d}.webp"
        dst = os.path.join(slug_dir, dst_filename)
        convert_image(src, dst)
        images.append(f"/final-products/{slug}/{dst_filename}")
        
    add_product(slug, folder_name.replace('_', '-'), folder_name.replace('_', '-'), images)

# 3. Aug 1 folder
def sort_key(x):
    try:
        return int(os.path.basename(x).split('-')[0])
    except:
        return x

aug1_dir = os.path.join(ALL_PRODUCTS_DIR, "Aug 1, 2026 08_03_55 PM (1)")
if os.path.exists(aug1_dir):
    files = [f for f in os.listdir(aug1_dir) if f.lower().endswith('.jpg')]
    files.sort(key=sort_key)
    
    group_num = 1
    for i in range(0, len(files), 6):
        group_files = files[i:i+6]
        slug = f"aug1_group_{group_num:02d}"
        
        slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        
        images = []
        for j, f in enumerate(group_files):
            src = os.path.join(aug1_dir, f)
            dst_filename = f"{slug}-{j+1:02d}.webp"
            dst = os.path.join(slug_dir, dst_filename)
            convert_image(src, dst)
            images.append(f"/final-products/{slug}/{dst_filename}")
        
        add_product(slug, f"AUG1-GROUP-{group_num:02d}", f"AUG1-GROUP-{group_num:02d}", images)
        group_num += 1

# 4. Aug 8 folder
aug8_dir = os.path.join(ALL_PRODUCTS_DIR, "Aug 8, 2026 03_16_45 PM")
if os.path.exists(aug8_dir):
    files = [f for f in os.listdir(aug8_dir) if f.lower().endswith('.jpg')]
    files.sort(key=sort_key)
    
    group_num = 1
    for i in range(0, len(files), 6):
        group_files = files[i:i+6]
        slug = f"aug8_group_{group_num:02d}"
        
        slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        
        images = []
        for j, f in enumerate(group_files):
            src = os.path.join(aug8_dir, f)
            dst_filename = f"{slug}-{j+1:02d}.webp"
            dst = os.path.join(slug_dir, dst_filename)
            convert_image(src, dst)
            images.append(f"/final-products/{slug}/{dst_filename}")
        
        add_product(slug, f"AUG8-GROUP-{group_num:02d}", f"AUG8-GROUP-{group_num:02d}", images)
        group_num += 1

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump({"products": frontend_products}, f, indent=2)

with open(BACKEND_JSON_PATH, "w") as f:
    json.dump({"products": backend_products}, f, indent=2)

print(f"Processed {len(frontend_products)} products.")
