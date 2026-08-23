import os
import glob
from PIL import Image

FINAL_PRODUCTS = "frontend/public/final-products"
white_files = []

for root, dirs, files in os.walk(FINAL_PRODUCTS):
    for f in files:
        if f.endswith('.webp'):
            path = os.path.join(root, f)
            try:
                img = Image.open(path).convert('RGB')
                pixel = img.getpixel((10, 10))
                if pixel[0] > 245 and pixel[1] > 245 and pixel[2] > 245:
                    white_files.append(path)
            except Exception as e:
                pass

if white_files:
    print("Found white background files:")
    for w in white_files:
        print(w)
else:
    print("No white background files found!")
