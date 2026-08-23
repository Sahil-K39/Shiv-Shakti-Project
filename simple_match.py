import fitz
from PIL import Image, ImageChops
import glob
import os
import math

print("Extracting PDF images...")
doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
pdf_images = []
for i in range(len(doc)):
    for img in doc[i].get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        path = f"pdf_{len(pdf_images)}.jpg"
        with open(path, "wb") as f:
            f.write(image_bytes)
        
        # Resize to 32x32 for quick matching
        pil_img = Image.open(path).resize((32, 32)).convert("RGB")
        pdf_images.append({"path": path, "img": pil_img, "id": len(pdf_images)})

print("Loading Photoroom PNGs...")
png_hashes = []
for png_path in glob.glob("Photoroom/*.png"):
    try:
        pil_img = Image.open(png_path).convert("RGBA")
        bg = Image.new("RGBA", pil_img.size, (220, 224, 227, 255))
        composite = Image.alpha_composite(bg, pil_img).convert("RGB")
        resized = composite.resize((32, 32))
        png_hashes.append({"path": png_path, "img": resized})
    except Exception as e:
        pass

def rmse(img1, img2):
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    return math.sqrt(sum(sq) / float(img1.size[0] * img1.size[1]))

print("Matching...")
for p in pdf_images:
    best_match = None
    best_dist = 1000000
    for png in png_hashes:
        dist = rmse(p["img"], png["img"])
        if dist < best_dist:
            best_dist = dist
            best_match = png["path"]
    
    print(f"Matched PDF {p['id']} -> {best_match} (dist: {best_dist})")

