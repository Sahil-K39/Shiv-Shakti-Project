import json

with open("old_products.json", "r") as f:
    old_data = json.load(f)

with open("backend/internal/store/final_products.json", "r") as f:
    current_data = json.load(f)

current_skus = set(p.get("sku") for p in current_data["products"])

restored = 0
for p in old_data["products"]:
    sku = p.get("sku")
    if sku not in current_skus:
        # It's one of the deleted products (Go42 - Go93)
        current_data["products"].append(p)
        restored += 1

with open("backend/internal/store/final_products.json", "w") as f:
    json.dump(current_data, f, indent=2)

print(f"Restored {restored} products.")
