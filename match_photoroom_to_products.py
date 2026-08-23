import fitz
from PIL import Image, ImageChops
import glob
import os
import math

print("Loading Photoroom PNGs...")
png_hashes = []
for png_path in glob.glob("Photoroom/*.png"):
    try:
        pil_img = Image.open(png_path).convert("RGBA")
        # Composite on white or beige to match the JPG background
        bg = Image.new("RGBA", pil_img.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(bg, pil_img).convert("RGB")
        resized = composite.resize((32, 32))
        png_hashes.append({"path": png_path, "img": resized})
    except Exception as e:
        pass

print("Loading Products JPGs...")
jpg_hashes = []
for jpg_path in glob.glob("Products/*.jpg"):
    try:
        pil_img = Image.open(jpg_path).convert("RGB")
        resized = pil_img.resize((32, 32))
        jpg_hashes.append({"path": jpg_path, "img": resized})
    except Exception as e:
        pass

def rmse(img1, img2):
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    return math.sqrt(sum(sq) / float(img1.size[0] * img1.size[1]))

print("Matching...")
matches = []
for p in png_hashes:
    best_match = None
    best_dist = 1000000
    for jpg in jpg_hashes:
        dist = rmse(p["img"], jpg["img"])
        if dist < best_dist:
            best_dist = dist
            best_match = jpg["path"]
    
    matches.append(f"{p['path']}={best_match}")

with open("mapping.txt", "w") as f:
    f.write("\n".join(matches))

print(f"Mapped {len(matches)} images.")
