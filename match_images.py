import fitz
from PIL import Image
import imagehash
import glob
import os
import io

# Extract PDF images
print("Extracting PDF images...")
doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
pdf_images = []
os.makedirs("frontend/public/final-products/pdf_extract", exist_ok=True)
count = 0
for i in range(len(doc)):
    for img in doc[i].get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        
        path = f"frontend/public/final-products/pdf_extract/pdf_{count}.jpg"
        with open(path, "wb") as f:
            f.write(image_bytes)
        
        # Calculate hash
        pil_img = Image.open(path)
        h = imagehash.phash(pil_img)
        pdf_images.append({"path": path, "hash": h, "id": count})
        count += 1

print(f"Extracted {len(pdf_images)} images.")

# Calculate hashes for Photoroom PNGs
print("Hashing Photoroom PNGs...")
png_hashes = []
for png_path in glob.glob("Photoroom/*.png"):
    try:
        # Composite on beige to simulate the PDF background for better hashing
        pil_img = Image.open(png_path).convert("RGBA")
        bg = Image.new("RGBA", pil_img.size, (220, 224, 227, 255))
        composite = Image.alpha_composite(bg, pil_img).convert("RGB")
        h = imagehash.phash(composite)
        png_hashes.append({"path": png_path, "hash": h})
    except Exception as e:
        print(f"Error on {png_path}: {e}")

# Match
print("Matching...")
matches = {}
for p in pdf_images:
    best_match = None
    best_dist = 1000
    for png in png_hashes:
        dist = p["hash"] - png["hash"]
        if dist < best_dist:
            best_dist = dist
            best_match = png["path"]
    
    if best_dist < 15: # Arbitrary threshold
        print(f"Matched PDF {p['id']} -> {best_match} (dist: {best_dist})")
    else:
        print(f"NO MATCH for PDF {p['id']} (best dist: {best_dist} to {best_match})")
