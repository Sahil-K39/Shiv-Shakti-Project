import os
import json
import shutil

FRONTEND_JSON_PATH = "frontend/src/lib/initialProducts.json"
BACKEND_JSON_PATH = "backend/internal/store/final_products.json"
FINAL_PRODUCTS_DIR = "frontend/public/final-products"

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

for f_prod in f_data['products']:
    slug = f_prod['slug']
    new_images = []
    
    slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
    if not os.path.exists(slug_dir):
        continue
        
    # We rename all .webp files in the folder to have -v2
    for i, old_path in enumerate(f_prod['images']):
        filename = os.path.basename(old_path)
        if "-v2-" in filename:
            new_images.append(old_path)
            continue
            
        new_filename = filename.replace("-", "-v2-", 1) if "-" in filename else f"v2-{filename}"
        new_rel_path = f"/final-products/{slug}/{new_filename}"
        
        old_full = os.path.join(FINAL_PRODUCTS_DIR, slug, filename)
        new_full = os.path.join(FINAL_PRODUCTS_DIR, slug, new_filename)
        
        if os.path.exists(old_full):
            os.rename(old_full, new_full)
            new_images.append(new_rel_path)
        elif os.path.exists(new_full):
            new_images.append(new_rel_path)
        else:
            print(f"Missing {old_full}")
            
    f_prod['images'] = new_images
    
    # Update backend
    for b_prod in b_data['products']:
        if b_prod['sku'] == f_prod['sku']:
            b_prod['images'] = json.dumps(new_images)
            break

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

print("Renamed all images to -v2 and updated JSON.")
