import json

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"
BACKEND_JSON = "backend/internal/store/final_products.json"

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)
with open(BACKEND_JSON) as f:
    b_data = json.load(f)

def should_keep(slug):
    # Remove go_48 to go_93
    if slug.startswith("go_"):
        num_str = slug.replace("go_", "")
        if "_" in num_str and num_str != "85_1" and num_str != "63_1":
            # Like go_42_studio
            if num_str.endswith("_studio"):
                return False
                
        num = num_str.split("_")[0]
        if num.isdigit() and int(num) >= 48:
            return False
            
    return True

f_kept = [p for p in f_data['products'] if should_keep(p['slug'])]
b_kept = [p for p in b_data['products'] if should_keep(p['slug'])]

f_data['products'] = f_kept
b_data['products'] = b_kept

print(f"Frontend products: {len(f_kept)}")
print(f"Backend products: {len(b_kept)}")

with open(FRONTEND_JSON, "w") as f:
    json.dump(f_data, f, indent=2)
with open(BACKEND_JSON, "w") as f:
    json.dump(b_data, f, indent=2)

