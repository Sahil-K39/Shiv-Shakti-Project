import os
import json

ALL_PRODUCTS_DIR = "/Users/sahil/Documents/Shiv Shakti/All Products"
PHOTOROOM_DIR = os.path.join(ALL_PRODUCTS_DIR, "Photoroom")

# 1. Collect all product groups from Photoroom
photoroom_groups = set()
for f in os.listdir(PHOTOROOM_DIR):
    if f.lower().endswith(('.png', '.jpg')):
        prefix = f[:4].lower() # e.g. go02
        if prefix.startswith("go") and prefix[2:].isdigit():
            photoroom_groups.add(f"go_{prefix[2:]}")

# 2. Collect all GO_* folders
go_folders = []
for f in os.listdir(ALL_PRODUCTS_DIR):
    if f.startswith("GO_") and os.path.isdir(os.path.join(ALL_PRODUCTS_DIR, f)):
        go_folders.append(f.lower())

# 3. Collect Aug 1 groups
aug1_groups = []
aug1_dir = os.path.join(ALL_PRODUCTS_DIR, "Aug 1, 2026 08_03_55 PM (1)")
files = [f for f in os.listdir(aug1_dir) if f.lower().endswith('.jpg')]
num_aug1_groups = len(files) // 6 + (1 if len(files) % 6 != 0 else 0)
for i in range(1, num_aug1_groups + 1):
    aug1_groups.append(f"aug1_group_{i:02d}")

# 4. Collect Aug 8 groups
aug8_groups = []
aug8_dir = os.path.join(ALL_PRODUCTS_DIR, "Aug 8, 2026 03_16_45 PM")
files = [f for f in os.listdir(aug8_dir) if f.lower().endswith('.jpg')]
num_aug8_groups = len(files) // 6 + (1 if len(files) % 6 != 0 else 0)
for i in range(1, num_aug8_groups + 1):
    aug8_groups.append(f"aug8_group_{i:02d}")

# Create expected slugs
expected_slugs = set()
expected_slugs.update(photoroom_groups)
for go_folder in go_folders:
    # If the go folder already exists in photoroom, the script made a _studio variant!
    if go_folder in photoroom_groups:
        expected_slugs.add(f"{go_folder}_studio")
    else:
        expected_slugs.add(go_folder)
        
expected_slugs.update(aug1_groups)
expected_slugs.update(aug8_groups)

# Now check initialProducts.json
with open("/Users/sahil/Documents/Shiv Shakti/frontend/src/lib/initialProducts.json") as f:
    f_data = json.load(f)

actual_slugs = set(p['slug'] for p in f_data['products'])

print(f"Total expected slugs from folders: {len(expected_slugs)}")
print(f"Total actual slugs in JSON: {len(actual_slugs)}")

missing_in_json = expected_slugs - actual_slugs
extra_in_json = actual_slugs - expected_slugs

if missing_in_json:
    print("MISSING from JSON:", sorted(missing_in_json))
if extra_in_json:
    print("EXTRA in JSON:", sorted(extra_in_json))

