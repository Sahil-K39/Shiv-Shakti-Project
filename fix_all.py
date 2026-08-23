import json
import os
import shutil

# Read the sorted lists
with open("sorted_photo.txt") as f1, open("sorted_prod.txt") as f2:
    photos = f1.read().splitlines()
    prods = f2.read().splitlines()

# Create a mapping from Photoroom filename to Products filename
mapping = {}
for i in range(min(len(photos), len(prods))):
    mapping[photos[i]] = prods[i]

# Read final_products.json
with open("backend/internal/store/final_products.json", "r") as f:
    data = json.load(f)

# Ensure output dir exists
out_dir = "frontend/public/final-products/original_bg"
os.makedirs(out_dir, exist_ok=True)

# For each product in the JSON, update its images
for p in data["products"]:
    sku = p.get("sku", "")
    if not sku.startswith("SS-FINAL-GO-"):
        continue
    
    # Extract the Go prefix
    num_str = sku.replace("SS-FINAL-GO-", "").split("-")[0]
    go_prefix = f"Go{int(num_str):02d}" # e.g. Go02
    
    # Parse images
    images = p.get("images", [])
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except:
            images = []
            
    # Filter out the wrong pdf_bg images
    filtered_images = [img for img in images if "/pdf_bg/" not in img]
    
    # Now, find all Photoroom images for this Go prefix in the original array
    # The original array had strings like "/final-products/photoroom/go02-01.png"
    # Wait, the mapping uses original Photoroom filenames like Go02_IMG_0534.png.
    # We can just search the mapping keys that start with the prefix!
    matching_photos = [k for k in mapping.keys() if k.startswith(go_prefix + "_")]
    matching_photos.sort()
    
    new_images = []
    for idx, photo_name in enumerate(matching_photos):
        prod_name = mapping[photo_name]
        
        # Copy the original JPG
        src = f"Products/{prod_name}"
        dst_filename = f"{go_prefix.lower()}-orig-{idx+1:02d}.jpg"
        dst = f"{out_dir}/{dst_filename}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            new_images.append(f"/final-products/original_bg/{dst_filename}")
            
    # Combine: put new JPGs first, then the remaining images (like the PNGs)
    # Wait, if we put the new JPGs first, they will be the primary images!
    # And we still have the PNGs as secondary images if needed, or we can just replace them.
    # The user said "use the products with the original studio backgrounds", let's just make them the ONLY images, or put them first.
    # Let's put them first, and keep the PNGs as secondary images.
    final_images = new_images + [img for img in filtered_images if not img.startswith(f"/final-products/original_bg/")]
    
    p["images"] = json.dumps(final_images)

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(data, f, indent=2)

print("Fixed final_products.json with original backgrounds!")
