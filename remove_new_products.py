import json

with open("backend/internal/store/final_products.json", "r") as f:
    data = json.load(f)

# Keep only products whose SKU is < 42
filtered = []
for p in data["products"]:
    sku = p.get("sku", "")
    if sku.startswith("SS-FINAL-GO-"):
        num_part = sku.replace("SS-FINAL-GO-", "").split("-")[0]
        try:
            num = int(num_part)
            if num >= 42:
                continue # Skip Go42 to Go93
        except:
            pass
    filtered.append(p)

data["products"] = filtered

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Reduced from to {len(filtered)} products.")
