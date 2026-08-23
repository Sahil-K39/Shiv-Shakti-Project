import json

with open("backend/internal/store/final_products.json", "r") as f:
    data = json.load(f)

# The mapping will be based on the number in the SKU
# Go02 -> pdf_00.jpg, Go03 -> pdf_01.jpg, ..., Go41 -> pdf_39.jpg
# Wait! Let's sort the GoXX products by their SKU number.
go_products = []
for p in data["products"]:
    sku = p.get("sku", "")
    if sku.startswith("SS-FINAL-GO-"):
        num_part = sku.replace("SS-FINAL-GO-", "").split("-")[0]
        try:
            num = int(num_part)
            if num <= 41:
                go_products.append((num, p))
        except:
            pass

go_products.sort(key=lambda x: x[0])

# Now assign pdf_00.jpg to the first, etc.
for idx, (num, p) in enumerate(go_products):
    if idx < 41:
        img_url = f"/final-products/pdf_bg/pdf_{idx:02d}.jpg"
        
        # Convert images string back to list if needed
        images = p.get("images", [])
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except:
                images = []
        
        # Replace the first image, or insert at beginning
        # Actually, let's just make it the primary image (index 0) and keep the rest
        # Wait, if we keep the rest, they will be PNGs. That's fine!
        if len(images) > 0 and images[0].startswith("/final-products/pdf_bg/"):
            images[0] = img_url
        else:
            images.insert(0, img_url)
            
        p["images"] = images

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated final_products.json with PDF images for Go02-Go41!")
