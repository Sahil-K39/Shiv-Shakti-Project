import json
import cv2
import numpy as np
import os

with open("frontend/src/lib/initialProducts.json") as f:
    data = json.load(f)

products_stats = []

for p in data["products"]:
    images = p.get("images", [])
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except:
            images = [images]
            
    if not images:
        continue
        
    first_image = images[0]
    if first_image.startswith("/"):
        first_image = first_image[1:]
        
    img_path = os.path.join("frontend/public", first_image)
    if not os.path.exists(img_path):
        continue
        
    img = cv2.imread(img_path)
    if img is None:
        continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Let's just look at the variance of the outer 20 pixels
    h, w = gray.shape
    top = gray[0:20, :]
    bottom = gray[h-20:h, :]
    left = gray[:, 0:20]
    right = gray[:, w-20:w]
    
    border_pixels = np.concatenate([top.flatten(), bottom.flatten(), left.flatten(), right.flatten()])
    std_dev = float(np.std(border_pixels))
    
    products_stats.append({"id": p["id"], "name": p["name"], "std_dev": std_dev, "image": images[0]})

# Sort by std_dev descending
products_stats.sort(key=lambda x: x["std_dev"], reverse=True)

for mp in products_stats[:30]:
    print(f"ID {mp['id']}, Name: {mp['name']}, StdDev: {mp['std_dev']:.2f}, Img: {mp['image']}")
