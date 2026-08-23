import os
import json
import shutil
import glob

new_bg_dir = "New Colour BG"
public_dir = "frontend/public/final-products/new_bg"
json_path = "backend/internal/store/final_products.json"

with open(json_path, 'r') as f:
    data = json.load(f)

products = data["products"]
sku_map = {p["sku"]: p for p in products}

manual_map = {
    "Go85": "SS-FINAL-GO-85-1",
    "Go63": "SS-FINAL-GO-63-1",
}

updated = 0

for folder, sku in manual_map.items():
    folder_path = os.path.join(new_bg_dir, folder)
    if not os.path.isdir(folder_path):
        continue
        
    jpgs = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))
    if not jpgs:
        continue
        
    new_image_paths = []
    num_str = folder[2:]
    for i, jpg in enumerate(jpgs):
        new_name = f"go{num_str}-{i+1:02d}.jpg"
        dest_path = os.path.join(public_dir, new_name)
        shutil.copy2(jpg, dest_path)
        new_image_paths.append(f"/final-products/new_bg/{new_name}")
        
    if sku in sku_map:
        sku_map[sku]["images"] = json.dumps(new_image_paths)
        updated += 1

with open(json_path, 'w') as f:
    json.dump(data, f, indent=4)
print(f"Fixed {updated} products")
