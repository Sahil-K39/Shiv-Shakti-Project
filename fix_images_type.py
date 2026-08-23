import json

with open("backend/internal/store/final_products.json", "r") as f:
    data = json.load(f)

for p in data["products"]:
    images = p.get("images", [])
    if isinstance(images, list):
        p["images"] = json.dumps(images)
    
    sizes = p.get("sizes", [])
    if isinstance(sizes, list):
        p["sizes"] = json.dumps(sizes)
        
    colors = p.get("colors", [])
    if isinstance(colors, list):
        p["colors"] = json.dumps(colors)

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(data, f, indent=2)

print("Fixed types in final_products.json!")
