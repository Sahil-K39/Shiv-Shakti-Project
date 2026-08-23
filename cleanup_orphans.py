import os
import glob
import json
import shutil

FRONTEND_JSON = "frontend/src/lib/initialProducts.json"

with open(FRONTEND_JSON) as f:
    f_data = json.load(f)

valid_images = set()
for p in f_data['products']:
    images = p.get('images', [])
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except:
            pass
    for img in images:
        valid_images.add(img.split('/')[-1])

deleted_count = 0
for folder in glob.glob("frontend/public/final-products/*"):
    if os.path.isdir(folder):
        for file in glob.glob(os.path.join(folder, "*.webp")):
            basename = os.path.basename(file)
            if basename not in valid_images:
                os.remove(file)
                deleted_count += 1
                print(f"Deleted orphan: {file}")

print(f"Total deleted: {deleted_count}")
