import json

with open("mid_products.json", "r") as f:
    mid_data = json.load(f)

with open("backend/internal/store/final_products.json", "r") as f:
    current_data = json.load(f)

# Filter out the 50 products we just added from old_products.json
current_data["products"] = [p for p in current_data["products"] if not (p.get("sku", "").startswith("SS-FINAL-GO-") and int(p["sku"].split("-")[-1]) >= 42)]

current_skus = set(p.get("sku") for p in current_data["products"])

restored = 0
for p in mid_data["products"]:
    sku = p.get("sku")
    if sku not in current_skus:
        current_data["products"].append(p)
        restored += 1

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(current_data, f, indent=2)

print(f"Restored {restored} products from mid_products.json.")
