import os
import glob

base = "All Products"

# 1. Photoroom products
photoroom_files = glob.glob(f"{base}/Photoroom/*.png") + glob.glob(f"{base}/Photoroom/*.jpg")
pr_products = set()
for f in photoroom_files:
    basename = os.path.basename(f).lower()
    if basename.startswith("go"):
        prefix = basename[:4]
        if prefix[2:].isdigit():
            pr_products.add(f"go_{prefix[2:]}")

# 2. GO_* folders
go_folders = set()
for d in os.listdir(base):
    if d.startswith("GO_") and os.path.isdir(os.path.join(base, d)):
        go_folders.add(d.lower())
        
# 3. Aug 1 / Aug 8
aug1_files = glob.glob(f"{base}/Aug 1*/*.jpg")
aug8_files = glob.glob(f"{base}/Aug 8*/*.jpg")

print(f"Photoroom product count (by prefix): {len(pr_products)}")
print(f"GO_* folders count: {len(go_folders)}")
print(f"Aug 1 images count: {len(aug1_files)}")
print(f"Aug 8 images count: {len(aug8_files)}")

overlap = pr_products.intersection(go_folders)
print(f"\nOverlap between Photoroom and GO_* folders: {len(overlap)}")
print(f"Overlapping items: {sorted(list(overlap))}")

print(f"\nTotal unique GO products (Photoroom + GO_*): {len(pr_products.union(go_folders))}")

