import fitz
from PIL import Image, ImageChops
import glob
import os
import math

print("Loading PDF images...")
pdf_images = []
for i in range(41):
    try:
        path = f"frontend/public/final-products/pdf_bg/pdf_{i:02d}.jpg"
        img = Image.open(path).convert("RGB")
        # Resize to a standard size for comparison
        img = img.resize((300, 400))
        pdf_images.append({"id": i, "path": path, "img": img})
    except Exception as e:
        print(e)

print("Loading Photoroom PNGs...")
png_images = []
for p in glob.glob("Photoroom/*.png"):
    img = Image.open(p).convert("RGBA")
    # Composite on the beige background of the PDF (approx 220, 224, 227)
    bg = Image.new("RGBA", img.size, (220, 224, 227, 255))
    comp = Image.alpha_composite(bg, img).convert("RGB")
    comp = comp.resize((300, 400))
    png_images.append({"name": os.path.basename(p), "img": comp, "path": p})

def rmse(img1, img2):
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    return math.sqrt(sum(sq) / float(img1.size[0] * img1.size[1]))

print("Matching PDF to Photoroom...")
matches = []
for pdf in pdf_images:
    best_match = None
    best_dist = float('inf')
    for png in png_images:
        dist = rmse(pdf["img"], png["img"])
        if dist < best_dist:
            best_dist = dist
            best_match = png["name"]
    matches.append(f"PDF_{pdf['id']:02d} -> {best_match} (dist {best_dist:.1f})")
    print(matches[-1])

with open("pdf_mapping.txt", "w") as f:
    f.write("\n".join(matches))

