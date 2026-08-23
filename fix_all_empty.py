import os
import json
from PIL import Image

FRONTEND_JSON_PATH = "frontend/src/lib/initialProducts.json"
BACKEND_JSON_PATH = "backend/internal/store/final_products.json"
FINAL_PRODUCTS_DIR = "frontend/public/final-products"
PHOTOROOM_DIR = "All Products/Photoroom"
ALL_PRODUCTS_DIR = "All Products"

with open(FRONTEND_JSON_PATH) as f:
    f_data = json.load(f)
with open(BACKEND_JSON_PATH) as f:
    b_data = json.load(f)

def convert_image(src, dst):
    img = Image.open(src)
    img = img.convert("RGB")
    img.save(dst, "WEBP", quality=85)

for i, f_prod in enumerate(f_data['products']):
    if len(f_prod['images']) == 0:
        slug = f_prod['slug']
        
        # Where should images come from?
        # If go_42 to go_47, they come from Photoroom.
        # If go_48 to go_93, they come from All Products/GO_48
        
        if slug in ["go_42", "go_44", "go_45", "go_46", "go_47"]:
            num = slug.split('_')[1]
            src_dir = PHOTOROOM_DIR
            files = [f for f in os.listdir(src_dir) if f.lower().startswith(f"go{num}_")]
        elif slug.startswith("go_"):
            num = slug.replace("go_", "").upper() # e.g. 48, 85_1
            src_dir = os.path.join(ALL_PRODUCTS_DIR, f"GO_{num}")
            if not os.path.exists(src_dir):
                print(f"Directory not found: {src_dir}")
                continue
            files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        else:
            print(f"Unknown empty slug: {slug}")
            continue
            
        files.sort()
        slug_dir = os.path.join(FINAL_PRODUCTS_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        
        images = []
        for j, file in enumerate(files):
            src = os.path.join(src_dir, file)
            dst_filename = f"{slug}-{j+1:02d}.webp"
            dst = os.path.join(slug_dir, dst_filename)
            convert_image(src, dst)
            images.append(f"/final-products/{slug}/{dst_filename}")
            
        f_prod['images'] = images
        # Find corresponding backend product
        for b_prod in b_data['products']:
            if b_prod['sku'] == f_prod['sku']:
                b_prod['images'] = json.dumps(images)
                break
        print(f"Fixed {slug} with {len(images)} images.")

with open(FRONTEND_JSON_PATH, "w") as f:
    json.dump(f_data, f, indent=2)

with open(BACKEND_JSON_PATH, "w") as f:
    json.dump(b_data, f, indent=2)

