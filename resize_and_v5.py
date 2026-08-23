import os
import glob
import json
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"
BACKEND_JSON = "backend/internal/store/final_products.json"
FINAL_PRODUCTS = "frontend/public/final-products"

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)
with open(BACKEND_JSON) as f:
    b_data = json.load(f)

def process_product(prod):
    slug = prod['slug']
    folder = os.path.join(FINAL_PRODUCTS, slug)
    if not os.path.exists(folder):
        return prod
    
    old_images = prod['images']
    if isinstance(old_images, str):
        old_images = json.loads(old_images)
        
    new_images = []
    
    files = sorted(glob.glob(os.path.join(folder, "*.webp")))
    if not files:
        return prod
        
    for i, file_path in enumerate(files):
        new_filename = f"{slug}-v5-{i+1:02d}.webp"
        new_path = os.path.join(folder, new_filename)
        
        if os.path.basename(file_path) != new_filename:
            try:
                img = Image.open(file_path).convert("RGB")
                # Resize if width > 600
                if img.width > 600:
                    ratio = 600.0 / float(img.width)
                    new_h = int(float(img.height) * float(ratio))
                    img = img.resize((600, new_h), Image.Resampling.LANCZOS)
                
                img.save(new_path, "WEBP", quality=80)
                
                # Remove old file if it's different
                if file_path != new_path:
                    os.remove(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
        new_images.append(f"/final-products/{slug}/{new_filename}")
        
    prod['images'] = new_images
    return prod

print("Resizing images... this might take a minute.")

with ThreadPoolExecutor(max_workers=8) as executor:
    f_data['products'] = list(executor.map(process_product, f_data['products']))
    
with ThreadPoolExecutor(max_workers=8) as executor:
    # We must ensure we apply the same new image paths to the backend
    # Actually, they share the same slugs, so we can just copy from f_data
    f_dict = {p['slug']: p['images'] for p in f_data['products']}
    for b_prod in b_data['products']:
        if b_prod['slug'] in f_dict:
            b_prod['images'] = json.dumps(f_dict[b_prod['slug']])

with open(FRONTEND_JSON, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON, "w") as f:
    json.dump(b_data, f, indent=2)

print("Done resizing and updating JSON!")
