import os
import json
import shutil
import glob

# Paths
new_bg_dir = "New Colour BG"
public_dir = "frontend/public/final-products/new_bg"
json_path = "backend/internal/store/final_products.json"

# Ensure public dir exists
os.makedirs(public_dir, exist_ok=True)

# Load JSON
with open(json_path, 'r') as f:
    data = json.load(f)

products = data["products"]
sku_map = {p["sku"]: p for p in products}

updated_count = 0

# Loop through all GoXX folders in New Colour BG
for folder in os.listdir(new_bg_dir):
    folder_path = os.path.join(new_bg_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    # folder is like Go42
    if not folder.lower().startswith("go"):
        continue
        
    num_str = folder[2:]
    sku = f"SS-FINAL-GO-{num_str}"
    
    if sku not in sku_map:
        print(f"SKU {sku} not found in JSON for folder {folder}")
        continue
        
    # Get all jpgs in this folder
    jpgs = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))
    if not jpgs:
        continue
        
    new_image_paths = []
    
    # Copy images and create paths
    for i, jpg in enumerate(jpgs):
        filename = os.path.basename(jpg)
        new_name = f"go{num_str}-{i+1:02d}.jpg"
        dest_path = os.path.join(public_dir, new_name)
        
        # Copy file
        shutil.copy2(jpg, dest_path)
        
        # Add to new image paths
        new_image_paths.append(f"/final-products/new_bg/{new_name}")
        
    # Update JSON
    sku_map[sku]["images"] = json.dumps(new_image_paths)
    updated_count += 1
    print(f"Updated {sku} with {len(new_image_paths)} images")

# Save JSON
with open(json_path, 'w') as f:
    json.dump(data, f, indent=4)
    
print(f"Successfully updated {updated_count} products!")
